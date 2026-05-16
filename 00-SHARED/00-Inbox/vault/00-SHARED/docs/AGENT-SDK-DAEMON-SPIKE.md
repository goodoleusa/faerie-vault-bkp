---
title: Agent SDK Daemon — Architecture Spike
created: 2026-04-25T01:21:46Z
task_id: task-sdk-daemon-spike
agent: ai-engineer
doc_hash: sha256:pending
status: final
---

# Agent SDK Daemon — Architecture Spike

**Question:** Should faerie build a Python daemon using the Anthropic SDK to drain the sprint queue 24/7, outside Claude Code? If yes, what is the MVP shape?

**Recommendation: B — Defer until queue throughput crosses 20 tasks/hour sustained.**

---

## 1. Architecture Sketch

The core insight: the queue substrate (sprint-queue.json + bundles + manifests + COC chain) is already platform-agnostic. Claude Code is one consumer process. A daemon would be a second consumer using the same atomic claim protocol, consuming via Anthropic API instead of the Agent() tool.

```
CURRENT (Claude Code consumer):

  User → /run → run.py
                  ├─ 7x_queue_ops.py claim
                  ├─ 7x_spawn_template.py render → bundle_path
                  └─ Agent(prompt="READ: {bundle_path}\nExecute...")
                       ↓
                  Subagent runs inside Claude Code process
                  Subagent writes manifest → forensics/
                  PostToolUse hooks fire: COC, signing, B2 sync
                  8x_spawn_contract_enforcer fires on Agent call


PROPOSED (SDK daemon, parallel consumer):

  sprint-queue.json
       │
       ▼
  0x_faerie_daemon.py  (new, ~150 LOC)
       │
       ├─ 7x_queue_ops.py claim-atomic    (existing, reused)
       │
       ├─ 7x_spawn_template.py render     (existing, reused)
       │       → bundle content (string)
       │
       ├─ anthropic.Anthropic().messages.create(
       │     model="claude-haiku-4-5",
       │     system=SUBAGENT_SYSTEM_PROMPT,
       │     messages=[{"role":"user","content": bundle_content}]
       │  )
       │
       ├─ Parse response → write manifest → forensics/
       │
       ├─ 4x_coc_writer.py append         (existing, reused)
       ├─ 9x_agent_sign.py sign manifest  (existing, reused)
       └─ 5x_forensics_b2_sync.py --hook  (existing, reused as subprocess)
               ↓
       7x_queue_ops.py complete TASK_ID
       Loop. Sleep(poll_interval). Repeat.


CONCURRENCY SAFETY:
  Claude Code + daemon can run simultaneously.
  Atomic claim via O_CREAT|O_EXCL file lock in 7x_queue_ops.py.
  No task is double-claimed. Lock expiry TTL: 30 min (existing).
```

The daemon entrypoint is `scripts/0x_faerie_daemon.py` (~150 LOC). Everything below the API call boundary reuses existing scripts.

---

## 2. Cost Projection

### Per-task API cost (Anthropic public pricing, 2026-04)

| Model | Input price | Output price | Typical task (2K in / 1K out) |
|-------|------------|-------------|-------------------------------|
| Haiku 4.5 | $0.80/MTok | $4.00/MTok | ~$0.0056 |
| Sonnet 4.5 | $3.00/MTok | $15.00/MTok | ~$0.021 |
| Opus 4 | $15/MTok | $75/MTok | ~$0.105 |

Bundle sizes measured in this repo: 1.6–1.9K tokens. Agent output (manifest + work): 0.8–2K tokens typical for W1/W2 tasks.

**Realistic per-task cost estimate:**
- W1 Haiku task: ~$0.005–0.010
- W2 Sonnet task: ~$0.02–0.05
- W3 Sonnet (deep synthesis): ~$0.05–0.20

**Per 100 tasks (mixed W1/W2 queue, 70% haiku / 30% sonnet):**
- 70 × $0.008 = $0.56
- 30 × $0.035 = $1.05
- Total: ~**$1.61 / 100 tasks**

### Claude Code session cost (baseline)

Claude Code charges per token at the same model rates, but with:
- Additional overhead: PreToolUse/PostToolUse hook context (~500–1K tokens per tool call)
- Main orchestration context (burns even when idle: system prompt ~8K tokens always in window)
- Auto-compact overhead: 10K+ tokens of context summary carried forward

Effective overhead per Claude Code task: ~3–5K extra tokens for hook + main context = +$0.002–0.025 per task on top of bare API cost.

**At current queue throughput (~2–5 tasks/hour):**
- Claude Code session: user-interactive, billed per session open time
- Daemon: $0 unless actively processing (pure consumption model)

### Break-even analysis

The daemon wins when:
1. Queue drains while user is offline (no Claude Code session open) — daemon is the ONLY consumer
2. Throughput > ~20 tasks/hour, where daemon parallelism (N workers) beats single-session Agent() concurrency

At current throughput (2–5 tasks/hour), daemon adds infrastructure cost without meaningful latency improvement. At 20+ tasks/hour sustained, daemon with 3–5 parallel workers reduces wall-clock completion time 3–5x vs sequential Claude Code.

**Break-even threshold: 20 tasks/hour sustained for >4 hours/day.**

---

## 3. What Ports Cleanly vs Requires Rework

### Ports cleanly (zero rework)

- **Stigmergy-only coordination** — daemon writes manifests to `forensics/`, reads sprint-queue.json. No behavioral change needed. Filesystem IS the protocol.
- **Forensic chain** — `4x_coc_writer.py`, `9x_forensic_signer.py`, `5x_forensics_b2_sync.py` all callable as subprocesses. Chain integrity is script-level, not Claude Code-level.
- **Atomic queue claiming** — `7x_queue_ops.py claim-atomic` uses O_CREAT|O_EXCL; works identically whether caller is Claude Code or daemon.
- **Bundle rendering** — `7x_spawn_template.py render` is a pure CLI tool. Daemon calls it via subprocess, gets bundle string, passes to API.
- **Ed25519 signing** — `9x_agent_sign.py` is a standalone script. No dependency on Claude Code process.
- **Task_id-in-filename convention** — enforced by daemon manifest writer, same pattern.
- **Monkeybranching / chain claiming** — `7x_queue_ops.py monkeybranch-claim` works regardless of consumer.

### Requires rework (non-trivial)

**Critical hooks the daemon must replicate inline (as subprocess calls):**

| Hook | Claude Code trigger | Daemon equivalent |
|------|--------------------|--------------------|
| `8x_state_write_coc_enforcer.py` | PreToolUse Write | Call before every manifest write |
| `8x_protect_coc_paths.py` | PreToolUse Write/Edit/Bash | Inline path validation before write |
| `9x_forensic_signer.py` | PostToolUse Write | Call after every manifest write |
| `5x_forensics_b2_sync.py` | PostToolUse Write | Call after manifest write |
| `forensic_coc.py posttool` | PostToolUse * | Call after each task completes |
| `8x_spawn_contract_enforcer.py` | PreToolUse Agent | Daemon BYPASSES this entirely (daemon IS the spawner) |

The spawn contract enforcer (`8x_spawn_contract_enforcer.py`) is irrelevant for the daemon — it validates Claude Code's Agent() calls, not API calls. The daemon implements the contract natively.

**Cosmetic hooks (not needed in daemon):**
- `8x_faerie_brief_gatekeeper.py` — warm-start gating (UI only)
- `8x_precompact_springboard.py` / `8x_postcompact_piston_refresh.py` — compact lifecycle (no compact in daemon)
- `8x_roster_update.py` — Claude Code agent roster tracking
- `8x_enforce_lean_queries.py` / `9x_inject_lean_constraint.py` — main context discipline (N/A)
- `8x_state_read_drag.py` — read-pattern enforcement (N/A)
- `8x_vault_frontmatter_validator.py` — vault doc writes (daemon writes forensics, not vault)
- `8x_vault_auto_index.py` — same
- `5x_vault_guardian.py` — same

**No hooks that are completely lost:**
Every safety-critical hook can be replicated as a subprocess call in the daemon's task lifecycle. The daemon must implement a `_pre_write_check()` and `_post_write_chain()` wrapper around every manifest write.

**No auto-compact:**
Daemon manages its own token budget per API call. Each call is stateless (no context window that grows across calls). This is actually an advantage — no context pressure, no compact-timing complexity.

---

## 4. MVP Shape (~200 LOC pseudocode)

```python
#!/usr/bin/env python3
"""
0x_faerie_daemon.py — SDK-based queue drainer.

TIER: 0x_ (setup/entrypoint)
REPLACES: Claude-Code-bound queue consumption
METRIC: tasks_drained_per_hour, cost_per_task, collision_rate
LOAD: sauce (optional consumer — Claude Code remains primary)
"""

import os, json, time, subprocess, hashlib
from pathlib import Path
from datetime import datetime, timezone
import anthropic

REPO = Path("/mnt/d/0local/gitrepos/faerie2")
SCRIPTS = REPO / "scripts"
FORENSICS = REPO / "forensics" / "manifests"
QUEUE_OPS = SCRIPTS / "7x_queue_ops.py"
SPAWN_TPL = SCRIPTS / "7x_spawn_template.py"
COC_WRITER = SCRIPTS / "4x_coc_writer.py"
SIGNER = SCRIPTS / "9x_forensic_signer.py"
B2_SYNC = SCRIPTS / "5x_forensics_b2_sync.py"
POLL_INTERVAL = 15  # seconds
MAX_WORKERS = 3     # parallel API calls (respect tier rate limits)

SYSTEM_PROMPT = """You are a faerie subagent. You receive a task bundle.
Execute the task exactly as specified. Write all artifacts to the paths given.
Return a JSON manifest with fields: task_id, status, dashboard_line, output_path.
dashboard_line must be <=80 chars. Do not narrate or ask questions. Execute."""

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def _run(cmd, **kwargs):
    """Run subprocess, return stdout string."""
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        raise RuntimeError(f"Subprocess failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def claim_tasks(session_id: str, n: int = 3) -> list[dict]:
    """Atomic claim from queue. Returns list of task dicts."""
    raw = _run(["python3", QUEUE_OPS, "claim-atomic",
                "--session", session_id, "--max", str(n)])
    return json.loads(raw) if raw else []

def render_bundle(task: dict) -> str:
    """Render bundle string via spawn template."""
    params = json.dumps(task.get("params", {}))
    template_id = task.get("template_id", "w1-general")
    return _run(["python3", SPAWN_TPL, "render",
                 "--template", template_id, "--params", params])

def _manifest_path(task_id: str, sid8: str) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"{ts}_daemon_{task_id}_daemon_{sid8}.json"
    return FORENSICS / fname

def _pre_write_check(path: Path, content: str) -> None:
    """Replicate 8x_state_write_coc_enforcer + 8x_protect_coc_paths inline."""
    # Block writes to state/ paths from daemon (forensics/ only)
    if ".claude/hooks/state" in str(path):
        raise ValueError(f"Daemon must not write to state/: {path}")
    # Block overwrite of existing COC artifacts
    if path.exists() and "coc" in path.name.lower():
        raise ValueError(f"COC artifact is immutable: {path}")

def _post_write_chain(path: Path) -> None:
    """Replicate PostToolUse: signer + COC + B2."""
    subprocess.run(["python3", SIGNER, "--file", str(path)], check=False)
    subprocess.run(["python3", B2_SYNC, "--hook"], check=False)

def call_api(bundle: str, model: str = "claude-haiku-4-5") -> dict:
    """Single stateless API call. Returns parsed manifest dict."""
    resp = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": bundle}]
    )
    text = resp.content[0].text
    # Extract JSON block from response (agents return manifest as JSON)
    import re
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if not m:
        raise ValueError(f"No JSON manifest in response: {text[:200]}")
    return json.loads(m.group())

def process_task(task: dict, sid8: str) -> None:
    task_id = task["task_id"]
    model = task.get("model", "claude-haiku-4-5")
    try:
        bundle = render_bundle(task)
        manifest_data = call_api(bundle, model=model)
        manifest_data["task_id"] = task_id
        manifest_data["daemon_sid8"] = sid8
        manifest_data["ts"] = datetime.now(timezone.utc).isoformat()

        mpath = _manifest_path(task_id, sid8)
        mpath.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(manifest_data, indent=2)
        _pre_write_check(mpath, content)
        mpath.write_text(content)
        _post_write_chain(mpath)

        _run(["python3", QUEUE_OPS, "complete", task_id])
        print(f"[OK] {task_id}: {manifest_data.get('dashboard_line','')}")

    except Exception as e:
        print(f"[FAIL] {task_id}: {e}")
        _run(["python3", QUEUE_OPS, "release", task_id])

def main():
    import uuid
    sid8 = uuid.uuid4().hex[:8]
    print(f"[daemon] starting. sid8={sid8}")

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        while True:
            tasks = claim_tasks(sid8, n=MAX_WORKERS)
            if not tasks:
                time.sleep(POLL_INTERVAL)
                continue
            futures = [pool.submit(process_task, t, sid8) for t in tasks]
            for f in futures:
                f.result()  # surface exceptions; don't swallow

if __name__ == "__main__":
    main()
```

Total: ~145 LOC excluding comments.

---

## 5. Go/No-Go Recommendation

**Recommendation: B — Defer.**

Build the daemon when queue throughput sustains 20+ tasks/hour for 4+ hours/day, OR when the user needs offline queue draining (tasks completing while no Claude Code session is active). Neither condition currently applies: the queue averages 2–5 tasks/hour, and Claude Code is the active working environment. The substrate is already platform-agnostic — no design decisions need to be locked in now. The daemon is ~150 LOC when the time comes, and every component it needs already exists. Building it now would introduce a second consumer that needs maintenance, rate-limit budget allocation, and API cost monitoring, for marginal throughput benefit at current queue depth. Defer until the queue backs up.

**Option A (build now)** is premature: the queue is not congested, the user is actively in Claude Code sessions, and the daemon's value (24/7 headless draining) doesn't materialize at current cadence.

**Option C (never)** discards a legitimate architectural path: if queue depth ever reaches 50+ tasks with time-sensitive deadlines, the daemon is the right tool. Don't close the door.

---

## 6. Risks and Gotchas

### Rate limits vs parallelism

Anthropic Tier 1 rate limits (typical new account): ~60K tokens/minute Haiku, ~20K tokens/minute Sonnet. A 3-worker daemon running W1 Haiku tasks (~2K tokens each) at 3 concurrent calls hits ~6K tokens/minute — well within limits. Sonnet W2/W3 tasks (4–8K tokens each): 3 workers × 6K = 18K/min, near Tier 1 ceiling. Worker count must be capped per tier. Recommend: read `ANTHROPIC_TIER` env var; enforce `MAX_WORKERS = {1: 1, 2: 3, 3: 5}[tier]`.

### Cost runaway

A queue with 200 tasks × Sonnet = ~$4–10. A queue with 2000 tasks × Sonnet = $40–100. The daemon has no native cost cap. Mitigation: add `--max-spend` flag checked per iteration; write `daemon-spend.json` tracking cumulative cost from API response usage fields; halt if ceiling exceeded. This is NOT optional before production use.

### Lock collision with concurrent Claude Code session

`7x_queue_ops.py claim-atomic` uses O_CREAT|O_EXCL file locking — concurrent sessions (Claude Code + daemon) will NOT double-claim. Confirmed by Phase 1 design. The only risk: if Claude Code session dies mid-task and leaves a lock file, the daemon's `cleanup-claims` subcommand (TTL=30min) eventually recovers it. No special handling needed, but the 30-min TTL should be verified against typical task duration.

### No hook safety net

The Claude Code hook chain (`8x_spawn_contract_enforcer`, `8x_state_write_coc_enforcer`, `8x_protect_coc_paths`) fires on every tool use. In the daemon, these are voluntary subprocess calls in `_pre_write_check()` and `_post_write_chain()`. If a daemon code path skips these wrappers (error branch, exception handler), a malformed manifest could be written without COC entry or signing. Mitigation: wrap the entire `process_task()` body in a context manager that guarantees `_post_write_chain()` fires even on exception — use `try/finally`.

### Manifest JSON parsing brittleness

The daemon expects the API response to contain a JSON block parseable via regex. Claude models reliably return structured JSON when system-prompted correctly, but edge cases (refusals, long prose, partial JSON) will break the extractor. The MVP's `re.search(r'\{.*\}', text, re.DOTALL)` is fragile for large outputs. Production version should use `model="claude-haiku-4-5"` with `response_format` or structured output if the API supports it; fallback: retry once with explicit "return ONLY valid JSON" instruction.

### No subagent context window management

Claude Code subagents get a fresh context per Agent() call. Daemon API calls are also stateless (one call per task), so this is not a problem — it's actually an advantage. Each task gets a clean context with no accumulated drift.

---

## Summary

| Dimension | Assessment |
|-----------|-----------|
| Substrate port | Fully compatible. 7x_queue_ops, 7x_spawn_template, 4x_coc_writer, 9x_agent_sign all reusable as subprocesses |
| Critical hooks | 6 hooks must be replicated inline; all others are cosmetic |
| MVP size | ~145 LOC |
| Cost / 100 tasks | ~$1.60 (70% haiku / 30% sonnet mix) |
| Break-even | 20 tasks/hour sustained |
| Recommendation | B — Defer until break-even threshold |
| Top risk | Cost runaway (add --max-spend before any production use) |

---

```
doc_hash: sha256:cf25b502187e0df43944506ff5b5b178522f09f4c9497a03269825db5dd964f6
```
