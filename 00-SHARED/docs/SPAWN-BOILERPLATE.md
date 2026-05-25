# SPAWN-BOILERPLATE — Zero-Cost Bundle Rendering (f(0) Optimization)

**TL;DR:** Use `7x_spawn_template.py render --template {id}` to build spawn bundles deterministically.
- **Cost:** <50 tokens per spawn (zero inference)
- **Coverage:** 100% of faerie spawns through template registry
- **Bundle validation:** 73/73 tests passing (100% coverage) — see [ARCHITECTURE-BUNDLE-VALIDATION.md](./ARCHITECTURE-BUNDLE-VALIDATION.md)
- **Deprecation:** 8x_agent_spawn_autoinject.py (was 40K tokens per spawn, now replaced)

---

## Spawn Bundle Rendering — The One Way

Every agent spawn must use the **template registry**. No exceptions. No autoinject fallback. No manual boilerplate copying.

**Command:**
```bash
RENDERED_PROMPT=$(python3 $CLAUDE_HOME/scripts/7x_spawn_template.py render \
  --template {template_id} \
  --params '{"task_id":"...", "output_folder":"..."}')

# Then pass RENDERED_PROMPT to Agent() call
Agent(subagent_type="...", prompt=RENDERED_PROMPT, ...)
```

**List available templates:**
```bash
python3 $CLAUDE_HOME/scripts/7x_spawn_template.py list
python3 $CLAUDE_HOME/scripts/7x_spawn_template.py list --wave 2
```

**Show template schema (before rendering):**
```bash
python3 $CLAUDE_HOME/scripts/7x_spawn_template.py show --template w2-evidence-curation
```

**Registry location:** `$CLAUDE_HOME/spawn-templates/` (or `SPAWN_TEMPLATE_ROOT` env var)

---

## Why Templates (f(0) Principle)

**Old way (deprecated):**
- `8x_agent_spawn_autoinject.py` read 42KB SPAWN-BOILERPLATE.md at every spawn
- Faerie spent 300-800 tokens of inference composing the prompt
- Cost per spawn: ~40K tokens overhead + inference cost
- Total per faerie cycle (5 spawns): 200K+ tokens wasted on boilerplate

**New way (template registry):**
- Faerie picks a `template_id` and fills JSON params
- `7x_spawn_template.py` renders deterministically (no LLM calls)
- Cost per spawn: ~50 tokens (just the dispatch command)
- Total per faerie cycle (5 spawns): 250 tokens
- **Saving: 99.87% token reduction** on spawn overhead

This is **f(0)** — framework that costs nearly nothing to use. The boilerplate work (vault section, manifest contract, streaming protocol) is built into the templates; faerie calls the template once, passes the rendered output to Agent(), done.

---

## Bundle Injection Patterns (W1+W2 Validated — 100% Operational)

Every spawn includes a pre-materialized **bundle** — context blocks injected by the renderer:

### Pattern: DROPLETS_TOD (Cross-Domain Sparks)
Injects `$CT_VAULT/00-SHARED/Droplets/LIVE-{YYYY-MM-DD}.md` (Time-Of-Day ordered). Agents see what *other* agents discovered *right now*, before reasoning filters observations. W1 validation: 100% operational across all vault states (single entry, bulk, empty, unreachable).

### Pattern: HONEY (Crystallized Wisdom)
Two-source join: `{repo}/.claude/HONEY.md` (project-local, highest priority) + `~/.claude/HONEY.md` (universal patterns). De-duped by observation-id, tail-100 entries (most recent first), capped at 5K tokens. W1 validation: 100% join accuracy, zero data loss on file corruption.

### Pattern: NECTAR (Validated Findings)
Injects `~/.claude/NECTAR.md` tail-30 (last 30 validated entries from prior sessions). Most-recent findings have highest signal. W1 validation: 100% operational; gracefully handles empty, malformed, >100-entry files.

### Pattern: Pollen (Session-Local Findings)
Injects `{repo}/.claude/memory/pollen-{SESSION_ID}.md` (findings from agents spawned earlier this session). Outbound agents inherit upstream discoveries without messaging. W1 validation: 100% operational; no duplication across agent chain.

**Full validation report:** [ARCHITECTURE-BUNDLE-VALIDATION.md](./ARCHITECTURE-BUNDLE-VALIDATION.md#section-1-bundle-injection-patterns-the-building-blocks) (73 tests, all pass)

---

## Legacy Deprecation

**Removed (do NOT use):**
- `8x_agent_spawn_autoinject.py` — PreToolUse hook that read full boilerplate
- Manual SPAWN-BOILERPLATE.md copying
- Auto-inject `## VAULT OUTPUT` marker detection

**If you see autoinject firing:**
- Disable it in the hook configuration
- Switch to template-based spawn immediately
- Report any templates missing for your use case

---

## Templates Include All Required Sections

Each template's `body_partials` field includes:

```
✓ VAULT OUTPUT (where to write findings)
✓ MANIFEST CONTRACT (result format)
✓ STREAMING + DROPLETS (observation protocol)
✓ STIGMERGY (discovery + registration)
✓ TASK DROPLET DISCOVERY (upstream learning at startup)
✓ FILE WRITING PROTOCOL (subagent sandboxing)
✓ MODEL ROUTING (haiku/sonnet/opus policy)
✓ ANTI-GAMING BUNDLE MODEL (card visibility guarantee)
✓ MEMBENCH CONTEXT (substrate contribution)
```

You do NOT need to manually add these sections. Templates provide them deterministically.

---

## Spawn Shape — The Only Judgment Call (spawner-facing)

**Everything else in this file is mechanical. This is the one decision you make.**

### Individual agents (default)

Use plain `Agent()` calls — one per task, in parallel if independent:

```python
# Independent tasks → parallel spawns in one message
Agent(subagent_type="data-engineer",       description="ingest logs", prompt="...")
Agent(subagent_type="documentation-engineer", description="write report", prompt="...")
```

Each agent works solo, returns its own manifest, has no visibility into the others. No coordination overhead. Use this whenever agents don't need to talk to each other.

### Teams (when agents need to coordinate)

Use `TeamCreate` + named `Agent()` calls when agents must message each other, share task state, or when one agent's output gates another's work mid-flight:

```python
# Step 1 — main session creates the team
TeamCreate(team_name="w2-pipeline", description="parallel pipeline fix")

# Step 2 — spawn teammates with team_name (parallel, in one message)
Agent(subagent_type="python-pro",      team_name="w2-pipeline", name="schema-owner", description="fix schema", prompt="...")
Agent(subagent_type="data-engineer",   team_name="w2-pipeline", name="ingest-owner", description="fix ingest", prompt="...")

# Step 3 — teammates coordinate themselves via two queues (see below)
# Main session waits for notifications; does NOT broker messages

# Step 4 — on completion
# Teammates self-terminate when their manifest writes status=final.
# Main reads wave_state.agents_returned; when all teammates final:
TeamDelete(team_name="w2-pipeline")  # TeamDelete is the shutdown signal — no SendMessage needed
```

**Two queues, two scopes — teammates use both:**

| Queue | Tool | Scope | Purpose |
|---|---|---|---|
| **Faerie queue** | `queue_ops.py claim/complete/fail` | Persistent sprint backlog | Claim next work unit from shared backlog; survives session boundaries |
| **Native task list** | `TaskCreate/TaskUpdate/TaskList` | Intra-team, session-local | Coordinate sub-tasks within this team; track who owns what right now |

**Stigmergy first — write to known locations, let teammates discover:**

The default coordination pattern is stigmergic: write your output to a predictable location, update your manifest status, emit droplets and pollen. Teammates scan these on their own cadence. No messaging required for routine handoffs.

Discovery order at each task boundary:
1. **Faerie queue** — what's unblocked and claimable right now?
2. **Manifest locations** — what have teammates already written? Read their `status=final` manifests before starting overlapping work.
3. **Vault + droplets** — scan `$CT_VAULT/00-SHARED/Droplets/LIVE-{date}.md` for cross-domain sparks from parallel agents
4. **Native task list** — check `TaskList` for sub-task ownership and blockers within this team

```bash
# Typical teammate loop — stigmergic, no messaging
# 1. Claim from faerie queue
python3 $CLAUDE_HOME/hooks/state/queue_ops.py claim \
  --session $CLAUDE_SESSION_ID --category infrastructure --max 1

# 2. Before starting — scan what teammates have written
ls {REPO}/.claude/manifests/w2-*-result.json          # their outputs
tail -20 $CT_VAULT/00-SHARED/Droplets/LIVE-$(date +%F).md  # their sparks

# 3. Create native task for local tracking
TaskUpdate(taskId="...", status="in_progress", owner="my-name")

# 4. Write output to predictable path — teammate discovers it, not told about it
# 5. Complete both queues
TaskUpdate(taskId="...", status="completed")
python3 $CLAUDE_HOME/hooks/state/queue_ops.py complete TASK_ID
```

**`SendMessage` is disabled (HONEY sys00031). Stigmergy only.** All coordination flows through the filesystem:
- **Task deps:** express as `blockedBy` in faerie-queue — the blocked task auto-unblocks when its dep completes
- **State sync:** write droplets to `$CT_VAULT/00-SHARED/Droplets/LIVE-{date}.md` (with COC registration)
- **Progress signals:** update your manifest `status` (in-progress → draft → final); teammates read `wave_state.agents_returned`
- **Shutdown:** main calls `TeamDelete(team_name=...)` — no per-agent shutdown_request needed

If you're reaching for `SendMessage`, you've skipped a stigmergic primitive that already exists for the job.

**Teams add coordination overhead** — use them only when that overhead pays off:

| Scenario | Shape |
|---|---|
| N agents, fully independent work | Plain `Agent()` × N in parallel |
| N agents, one reads another's output after it's done | Plain `Agent()` sequential or `blockedBy` in faerie queue |
| N agents, output discovery via manifest/vault/droplets | Plain `Agent()` — stigmergy handles it |
| N agents, dynamic mid-flight dependency resolution | Team + faerie queue + native tasklist |
| Single agent chaining tasks (monkeybranch) | Plain `Agent()` |

**Anti-patterns:**
- Never spawn a "coordinator" agent to relay requirements — each relay burns ~15-25K tokens for zero value; write the spec upfront instead.
- Never use `SendMessage` (it's denied) — write to the manifest or drop a droplet; teammates discover stigmergically.
- Never nest teams — teammates cannot spawn sub-teams. Flat hierarchy only.

---

## STRATEGIC BRIEF — Evaluation-Aware Design (Read This First)

Your work will be scored. Every agent run produces:
1. **AGENT-RUN-ID** — immutable forensic anchor linking this run to eval score + training update
2. **Baseline comparison** — your score vs your Last Training score (your previous capability level)
3. **Delta + COC entry** — improvement recorded if beat baseline; on_the_job_eligible flag set for training queue
4. **Next spawn context** — if you beat baseline, your higher score becomes the new baseline for next spawn of your type

**What this means for your work:**
- **Be measurable:** Return clear success/failure signals, not ambiguous outputs
- **Solve the actual problem:** Generic solutions score lower than targeted solutions
- **Document patterns:** If you find a working technique, note it (goes into Last Training section of agent card)
- **Improve baseline:** Each beat-last score raises the bar for next agent of your type

**Your KPI is in your agent card** (`~/.claude/agents/{your-type}.md`, Last Training section). Read it at startup. Next spawn will see your score, so make it count.

---

## ANTI-GAMING BUNDLE MODEL — How Your Card Reaches You (2026-04-16+)

**Your agent card is split into two files:**
- `{type}-discovery.json` — PUBLIC only: role, input paths, output conventions, stigmergy rules
- `{type}.md` — PRIVATE (parent-only): Last Training, KPI, baseline, eval history

**The bundle model (architectural guarantee, not procedural):**

1. **Parent reads** your public section and embeds it directly into the spawn-prompt context (via `inject_vault_output.py --mode discovery --agent-type {type}`)
2. **You receive** a pre-materialized bundle with your discovery content inline — no paths, no file reads required
3. **You do NOT read** `{type}.md` or `{type}-discovery.json` files — the private data never enters your reachable scope

**Why this matters:** This is an **architectural guarantee** that you cannot see your baseline score or past performance before execution. That prevents anchoring bias. You read ONLY the public context, bundled inline. The private evaluation happens AFTER you return.

**How faerie spawns with the bundle model:**

When faerie spawns an agent of type `{agent_type}`, it must inject discovery BEFORE creating the spawn prompt:

```bash
# Parent (faerie) generates discovery inline:
DISCOVERY=$(python3 $CLAUDE_HOME/scripts/inject_vault_output.py \
  --mode discovery --agent-type {agent_type})

# Parent embeds discovery into spawn prompt:
SPAWN_PROMPT="
${DISCOVERY}

[Rest of spawn task description...]
"

# Parent then calls Agent() with this augmented prompt
Agent(subagent_type=..., prompt=SPAWN_PROMPT, ...)
```

**Audit trail:** The spawn-prompt string itself becomes the compliance surface — grep for metric strings like "Score:", "baseline_score", "citation_accuracy" in your transcript BEFORE eval phase. Should return zero hits if you're reading the bundle correctly.

**Result:** Your work is measured against your baseline, not distorted by knowing what your baseline is. This is forensic-grade anti-gaming.

---

## MEMBENCH CONTEXT — Your Work Is Measured On Two Dimensions (2026-04-16+)

**The six-dimension eval scores OUTPUT quality.** 
**Membench scores SUBSTRATE contribution.**

These are orthogonal. You'll be evaluated on both.

**What Membench measures (eight metrics, five core):**

| Metric | Finding | Why it matters |
|--------|---------|---|
| **Retention** | [ESTIMATED—see mission-efficiency-measurement-20260425.json for real measurement] | Memory corpus retains facts you write; crystallisation captures what's important |
| **Continuity** | [ESTIMATED—see mission-efficiency-measurement-20260425.json for real measurement] | Auto-compact checkpoints survive; no re-orientation cost when session resumes |
| **Work Efficiency** | [ESTIMATED—see mission-efficiency-measurement-20260425.json for real measurement] | Tasks-per-token WITH memory vs WITHOUT — measured payback in progress |
| **Overhead** | [ESTIMATED—see mission-efficiency-measurement-20260425.json for real measurement] | Memory costs measured as percentage of tokens after subtracting re-explanation savings |
| **Confabulation Rate** | [ESTIMATED—see mission-efficiency-measurement-20260425.json for real measurement] | Zero anti-facts in corpus — memory is clean, forensically admissible |

**What this means for YOUR work:**
- **You contribute to the substrate.** Every observation you write to pollen, every finding you stream, every MEM block you produce strengthens memory integrity and continuity.
- **Your pattern discoveries go into Last Training.** These become part of the crystallisation signal. Agents who document techniques improve the substrate for everyone downstream.
- **Clean findings (zero false claims) improve Confabulation Rate.** Don't speculate in streams. Cite sources. This is forensic work.
- **Your efficiency matters.** Tasks-per-token is measured. The substrate's payback metrics are tracked in mission-efficiency-measurement-20260425.json.

**The headline: memory's payback is being measured.** You benefit from every agent before you who documented patterns, captured findings cleanly, and wrote observations with sources. Your job is to do the same for agents after you.

---

## MODEL ROUTING — Haiku-Default with Strategic Sonnet/Opus (2026-04-21+)

**Policy: Minimize cost by defaulting to Haiku; reserve Sonnet/Opus for inference-heavy work.**

Your agent card (`~/.claude/agents/{your-type}.md`) specifies your model in the frontmatter. Faerie honors it when spawning you. If your card doesn't specify, look it up in the authoritative routing table.

### Wave-Based Model Defaults

**⚡ AUTHORITATIVE SOURCE:** `/.claude/AGENT-TYPE-ROUTING.json` (single source of truth for all 15 agent types)

Quick reference below; see AGENT-TYPE-ROUTING.json for complete routing table with promotion conditions.

| Wave | Name | Models | Example Agents |
|------|------|--------|---|
| **W1** | Triage & Validation (45s) | **Haiku** (no promotion) | orchestrator, context-manager, task-distributor |
| **W2** | Feature Work & Research (180s) | **Haiku** (default); **Sonnet** if reasoning_budget=inference_heavy | python-pro, data-engineer, documentation-engineer; **evidence-curator** (Sonnet baseline) |
| **W3** | Deep Synthesis (async) | **Sonnet** (default); **Opus** if reasoning_budget=expert | knowledge-synthesizer, membot, performance-eval; security-auditor (Haiku baseline) |

### When Your Agent Gets Promoted to Sonnet/Opus

Your agent is promoted from Haiku **ONLY if:**
1. Your agent card specifies `model: sonnet` or `model: opus` in frontmatter, OR
2. Your task includes `reasoning_budget: inference_heavy` (Sonnet) or `reasoning_budget: expert` (Opus), OR
3. Faerie detects your task touches 3+ reasoning-heavy operations (evidence synthesis, cross-domain hypothesis testing, security auditing)

**Example — evidence-curator:**
```yaml
# ~/.claude/agents/evidence-curator.md
agent_type: evidence-curator
model: sonnet                    # ← Explicitly promoted: gap analysis needs reasoning
reasoning_budget: inference_heavy
kpi: tier1_accuracy
```

**Example — python-pro (stays Haiku):**
```yaml
# ~/.claude/agents/python-pro.md
agent_type: python-pro
model: haiku                    # ← Default: routine code work
reasoning_budget: none
kpi: functional_correctness
```

### Eval Impact: Model Routing Dimension (F)

Your model choice affects the system's Model Routing score (Dimension F):

| Metric | Target | What it measures |
|--------|--------|---|
| `haiku_w1_rate` | 0.80+ | W1 agents using Haiku (cost efficiency) |
| `sonnet_w2_rate` | 0.90+ | W2 agents using Sonnet when needed (quality) |
| `opus_rate` | <0.05 | Rare, expert-only uses of Opus (decision point) |

If your W1 agent uses Sonnet when Haiku would suffice, it lowers `haiku_w1_rate` and drags down the Model Routing score for the system. Conversely, if an evidence-curator tries to use Haiku for gap analysis, the run fails quality gates.

**The balance:** Be honest about reasoning needs. Don't over-claim to get promoted; don't under-claim to look cheap. Eval harness will catch both.

### How to Check Your Current Model Assignment

At agent startup, look at this directive in your spawn prompt context:

```
Model: {your-model} (from agent card)
Reasoning budget: {inference_heavy|expert|none}
```

If it says `Model: haiku`, you have Haiku. If it says `Model: sonnet`, you have Sonnet. This is read-only — faerie decided based on your card + task.

### Cost Context (for transparency)

Estimated spend per spawn (at 7.5K input tokens):

| Model | Input Cost | Output Cost (est) | Per-Spawn Cost |
|-------|-----------|---|---|
| Haiku | $0.80 / 1M | $2.40 / 1M | ~$0.009 per spawn |
| Sonnet | $3.00 / 1M | $15.00 / 1M | ~$0.034 per spawn |
| Opus | $15.00 / 1M | $60.00 / 1M | ~$0.170 per spawn |

**Haiku is 4× cheaper than Sonnet, 19× cheaper than Opus.** If you don't need the reasoning depth, Haiku is the right choice.

---

## Spawn Contract Hardening — Exit-13 Rejection Gates (W1+W2 Hardened)

**New in 2026-04-25:** Spawner-side enforcement gates added. Rejected spawns exit with code 13 (SPAWN_CONTRACT_VIOLATION).

### Gate 1: General-Purpose Specialist Task Rejection

**Rule:** `general-purpose` agent spawns for tasks tagged `[specialist]` are rejected.

**Why:** General-purpose agents produce lower-quality output on specialist domains (evidence curation, security auditing). Specialist agents exist for this reason.

**Tags triggering rejection:**
- `[evidence]` → use evidence-curator (Sonnet)
- `[security]` → use security-auditor (Haiku→Sonnet)
- `[knowledge-synthesis]` → use knowledge-synthesizer (Sonnet)
- `[performance]` → use performance-eval (Sonnet)

**Example (rejected):**
```python
# FAILS with exit-13 — task tagged [specialist] but spawning general-purpose
Agent(subagent_type="general-purpose", 
      description="[specialist] Analyze threat intel for SQL injection", ...)
```

**Example (accepted):**
```python
# OK — specialist agent for specialist task
Agent(subagent_type="security-auditor",
      description="Analyze threat intel for SQL injection", ...)
```

**Enforcement:** `8x_spawn_contract_enforcer.py` at PreToolUse hook time. No bypass.

### Gate 2: Scout Protocol Injection Verification

**Rule:** Stigmergy-scout spawns must include scout-protocol behavioral template in the prompt.

**Why:** Stigmergy-scout is a behavioral protocol (prompt injection), not a registered agent type. It requires the scout ruleset to work correctly.

**Trigger:** If prompt contains "stigmergy-scout" or routing card is "stigmergy-scout", enforcer verifies scout protocol is present.

**Example (rejected):**
```python
# FAILS with exit-13 — scout routing but no scout protocol in prompt
prompt = "Discover X. You are routed to stigmergy-scout but no rules injected."
Agent(subagent_type="general-purpose", prompt=prompt, ...)
```

**Example (accepted):**
```python
# OK — scout protocol injected via template
PROMPT = 7x_spawn_template.py render --template scout-discovery --routing stigmergy-scout
Agent(subagent_type="general-purpose", prompt=PROMPT, ...)
```

**Enforcement:** `8x_spawn_contract_enforcer.py` at PreToolUse hook time.

### Gate 3: Agent Card Missing or Malformed

**Rule:** If task specifies `preferred_agent_type` and agent card is missing or unparseable, spawn is rejected.

**Why:** Routing policy exists for a reason. If the card doesn't exist, behavior is undefined. Better to reject and alert than spawn with fallback.

**Example (rejected):**
```python
# FAILS with exit-13 — preferred_agent_type="custom-agent-type" but no card exists
Agent(subagent_type="general-purpose", 
      description="custom task", 
      preferred_agent="custom-agent-type", ...)
```

**Example (accepted):**
```python
# OK — preferred_agent is a registered type with valid card
Agent(subagent_type="evidence-curator", ...)
```

**Enforcement:** `8x_spawn_contract_enforcer.py` validates routing table at PreToolUse hook time.

---

## Agent Tool Parameters (REQUIRED — every Agent() call)

The Agent() tool requires these parameters; missing any will cause spawn failure:

```python
Agent(
  subagent_type="specialist-type",  # ← Required: e.g. "data-engineer", "documentation-engineer"
  description="3-5 word task summary",  # ← Required: concise purpose (shown to user, required by Agent tool)
  prompt="Full task description...",    # ← Required: complete task details
  name="optional-name",                 # ← Optional: for teams, identifies team member
  team_name="team-name",                # ← Optional: if spawning as team member
  run_in_background=False               # ← Optional: background vs foreground
)
```

**Common failure:** Missing `description` parameter. Error: "The required parameter `description` is missing". Always include a short, clear description.

---

## AGENT-RUN-ID (REQUIRED — forensic anchor for every agent execution)

At agent startup, generate your immutable AGENT-RUN-ID:

```bash
AGENT_RUN_RESULT=$(python3 /mnt/d/0LOCAL/.claude/scripts/9x_agent_run_id_generator.py \
  --agent-type {your_type} \
  --session-id "${CLAUDE_SESSION_ID:-unknown}" \
  --task-id "{task_id}" \
  --wave {W1|W2|W3} \
  --model {haiku|sonnet|opus})
AGENT_RUN_ID=$(echo "$AGENT_RUN_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['agent_run_id'])")
```

Embed `$AGENT_RUN_ID` in every manifest and trace file. COC entry appended atomically to `/mnt/d/0LOCAL/.claude/memory/forensics/agent-runs.jsonl`.

To query: `python3 /mnt/d/0LOCAL/.claude/scripts/9x_forensic_query.py --agent-run-id $AGENT_RUN_ID`

---

## 1. Manifest Write (repo-local primary, global fallback)

**PRIMARY (always, unless blocked):** Write to repo-local staging directory.
**FALLBACK (if repo unwritable):** Global state directory.

Per-repo isolation is non-negotiable. Global state breaks multi-repo setups.

```
PRIMARY (try first — repo-local):
  {REPO_ROOT}/.claude/manifests/{wave}-{agent_type}-{SESSION_ID8}-result.json

FALLBACK (only if repo unwritable):
  /mnt/d/0LOCAL/.claude/hooks/state/{wave}-{agent_type}-{SESSION_ID8}-result.json
```

Determine REPO_ROOT from environment: `os.getcwd()` or parent of `.claude/` if passed in context.

`SESSION_ID8` = first 8 chars of `CLAUDE_SESSION_ID` (bash: `${CLAUDE_SESSION_ID:0:8}`, python: `os.environ['CLAUDE_SESSION_ID'][:8]`). P0.2 fix 2026-04-18: required to prevent cross-session overwrite. Legacy unsuffixed files remain in place; new writes follow new convention.

Manifest must include at minimum:
```json
{
  "agent": "{agent_type}",
  "ts": "{ISO8601}",
  "wave": {int},
  "task_id": "{task-xxx or null}",
  "agent_run_id": "$AGENT_RUN_ID",
  "output_path": "{full path to primary output file}",
  "dashboard_line": "{<=80 chars for Turn 0 dashboard}",
  "files_written": ["{paths}"],
  "finding_hash": "sha256:{hash of primary finding or output file}",
  "next": "{recommended next step or none}",
  "next_task_queued": {
    "id": "task-{YYYYMMDD-HHMMSS}-{hash8}",
    "title": "{short title of the follow-up task}",
    "description": "{the question this finding naturally raises}",
    "category": "investigation|infrastructure|publishing|training",
    "priority": "HIGH|MED|LOW",
    "preferred_agent": "{agent-type}",
    "parent_task_id": "{task-N - this task'"'"'s id}",
    "parent_finding_hash": "sha256:{hash of this manifest'"'"'s primary finding}",
    "validation_of": "{one-line summary of this finding being implicitly validated}",
    "rationale": "{why this is the natural next question}"
  }
}
```

## Queue Entry Protocol — Stigmergic Task Sequencing

When you complete a task and identify a follow-on that requires different expertise, or you've hit a dead end, declare it in your manifest. The PostToolUse hook auto-creates blocking relationships—no TaskUpdate calls needed.

**When to queue a task instead of doing next work yourself:**
- You've hit a dead end in your domain (need fresh perspective)
- Next step requires specialist expertise different from yours (data engineer → doc writer, researcher → security auditor)
- Your context is nearly full and next work is heavy (let fresh agent start)

**Pattern (in final manifest):**
```json
{
  "status": "final",
  "task_id": "34",
  "next_task_queued": {
    "task_id": "35",
    "reason": "Schema design complete; ORM layer depends on schema"
  }
}
```

**Mechanism:**
1. You write `next_task_queued` field in final manifest (task_id + reason)
2. PostToolUse hook reads manifest and calls TaskUpdate to add blockedBy relationship
3. Task #35 automatically unblocks when #34 completes
4. Next specialist agent claims Task #35 when ready

**Rules:**
- `task_id`: Required. Must exist in queue (don't invent)
- `reason`: Required. One-line explanation of why it depends on your work
- If no next task: omit field (you completed the chain)

**MANDATORY: Compute and include hashes in every manifest.**

```python
import hashlib, json, os
from pathlib import Path

def compute_manifest_hash(manifest_dict: dict) -> str:
    """SHA256 of manifest (excluding hash field itself)."""
    without_hash = {k: v for k, v in manifest_dict.items() if k != "manifest_hash"}
    raw = json.dumps(without_hash, sort_keys=True).encode("utf-8")
    return f"sha256:{hashlib.sha256(raw).hexdigest()}"

# Before writing manifest:
manifest["finding_hash"] = f"sha256:{hashlib.sha256(Path(output_path).read_bytes()).hexdigest()}"
manifest["manifest_hash"] = compute_manifest_hash(manifest)

# Write manifest with hashes included
path = f"{os.getcwd()}/.claude/manifests/{wave}-{agent_type}-{SESSION_ID8}-result.json"
Path(path).parent.mkdir(parents=True, exist_ok=True)
with open(path, "w") as f:
    json.dump(manifest, f, indent=2)
```

This hash is the forensic COC entry for this manifest.

---

## 2. Forensic Trace — COC Hash Chain (required at end of every agent run)

Every agent must write a hash-chained trace to the COC log. This is the forensic chain of custody.

```
PATH: {REPO_ROOT}/.claude/forensics/agent-coc.jsonl
```

**CRITICAL:** This is append-only. Every agent run adds ONE entry. Hash chain validates integrity.

**Trace format (one entry per agent run, appended to agent-coc.jsonl):**
```json
{
  "ts": "{ISO8601}",
  "agent_type": "{agent_type}",
  "session_id": "{CLAUDE_SESSION_ID}",
  "agent_run_id": "$AGENT_RUN_ID",
  "wave": {int},
  "task_id": "{task-xxx or null}",
  "manifest_path": "{full path to manifest JSON}",
  "manifest_hash": "{sha256:... of manifest file}",
  "output_path": "{primary output file path}",
  "output_hash": "{sha256:... of primary output file}",
  "prev_entry_hash": "{sha256:... of previous COC entry, or 'GENESIS' if first}",
  "entry_hash": "{computed below}"
}
```

**CRITICAL: Compute entry_hash to chain to previous entry**

```python
import hashlib, json
from pathlib import Path

# Read the last entry from agent-coc.jsonl to get prev_entry_hash
coc_file = Path("{REPO_ROOT}/.claude/forensics/agent-coc.jsonl")
prev_hash = "GENESIS"
if coc_file.exists():
    lines = coc_file.read_text().strip().split("\n")
    if lines and lines[-1].strip():
        last_entry = json.loads(lines[-1])
        prev_hash = last_entry.get("entry_hash", "GENESIS")

# Build trace entry
trace = {
    "ts": iso8601_now(),
    "agent_type": "my-type",
    "session_id": os.environ["CLAUDE_SESSION_ID"],
    "wave": 2,
    "task_id": task_id or None,
    "manifest_path": manifest_path,
    "manifest_hash": f"sha256:{hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()}",
    "output_path": output_path,
    "output_hash": f"sha256:{hashlib.sha256(Path(output_path).read_bytes()).hexdigest()}",
    "prev_entry_hash": prev_hash,
}

# Compute this entry's hash (for the next agent to chain to)
without_hash = {k: v for k, v in trace.items() if k != "entry_hash"}
raw = json.dumps(without_hash, sort_keys=True).encode("utf-8")
trace["entry_hash"] = f"sha256:{hashlib.sha256(raw).hexdigest()}"

# Append to COC log (one JSON object per line, no pretty-print)
coc_file.parent.mkdir(parents=True, exist_ok=True)
with open(coc_file, "a") as f:
    f.write(json.dumps(trace, separators=(",", ":")) + "\n")
```

**This COC log is forensic evidence. Never overwrite. Always append.**

---

## NECTAR AT STARTUP — Prior Findings & Cross-Session Learning (Phase 2+)

**Before you start your work, read prior findings from NECTAR.md (tail-30):**

These are validated findings from prior sessions — patterns that worked, techniques reused, context from prior investigation. Reading them at startup:
- Prevents redundant investigation (don't re-solve a problem already solved)
- Enables pattern reuse (apply techniques that worked before)
- Compounds learning (understanding grows across sessions)

**Where to find it:**
```
/mnt/d/0LOCAL/.claude/NECTAR.md (tail-30 = last 30 entries)
NECTAR is append-only forever — never edited, never compressed
```

**What to look for:**
- Techniques flagged as HIGH (techniques worth applying to your domain)
- Patterns from agents of your type (how similar agents solved similar problems)
- Contradictions to your assumptions (what you expected vs what was discovered)
- Connection hints (observations linking two domains — often spark new ideas)

**How to read it:**
1. At agent startup (before doing substantial work): read NECTAR tail-30
2. At task boundaries: re-scan NECTAR if you hit friction or uncertainty
3. When pattern matches your domain: note the reference in your manifest (cross-session continuity)

**If NECTAR is not pre-loaded in your context bundle:** Read it manually:
```bash
tail -30 /mnt/d/0LOCAL/.claude/NECTAR.md
```

**Signal-driven reading is OK.** You don't need to read all 30 entries. If the first 5 don't spark ideas, move forward with your work. NECTAR is there when you need it, not a chore to complete.

**In your manifest**, include a `nectar_references` field if you applied any findings:
```json
"nectar_references": [
  {"entry_id": "20260420-evidence-curator-H1", "technique": "index-first reads cut context 98%", "applied_to": "my search phase"}
]
```

---

## SDK INJECTION (Phase 4 — M/Q Unlock)

**Task #38 Implementation: ObservationStream + NectarBridge auto-discovery**

At agent startup, initialize these SDKs for real-time observation and prior-finding access:

```python
# At agent initialization (before substantive work):
import sys, os
sys.path.insert(0, "/mnt/d/0LOCAL/.claude/scripts")

from observation_stream import ObservationStream
from nectar_bridge import NectarBridge

# Initialize streams
obs = ObservationStream(
    agent_type="{your_agent_type}",
    session_id=os.environ.get("CLAUDE_SESSION_ID", "unknown")
)

nectar = NectarBridge(tail_lines=30)

# Read applicable techniques at startup
techniques = nectar.apply_techniques("{your_agent_type}")
if techniques:
    obs.emit("OBSERVATION", f"Found {len(techniques)} applicable NECTAR techniques")
    for t in techniques:
        obs.emit("TECHNIQUE", t, pri="MED")
```

Then during work:

```python
# Emit findings in real-time (not at the end)
obs.emit("FINDING", "Treasury LDAP exposed on 164.95.88.80", 
         sources=["raindrop-1020398503", "shodan-query"])
obs.emit("FLAG", "Non-remediation despite disclosure", pri="HIGH")
```

**Why this matters (M/Q unlock path):**
1. **Memory (M):** agents now actively read NECTAR at startup, adoption increases HONEY hit-rate
2. **Quality (Q):** real-time streaming captures fresh observations before reasoning filters them
3. **Continuity:** prior findings surface to agents who need them, reducing context per-run

---

## 3. Streaming (MANDATORY — quality depends on visibility)

**Streaming creates an audit trail of your work in real-time.** This enables:
1. Cross-session visibility (other agents know what you completed)
2. Quality scoring (evalbot reads streams to measure citation accuracy + depth)
3. Multi-agent continuity (next agent knows where you left off)

**Protocol (use every time you make a discovery):**

```bash
python3 /mnt/d/0LOCAL/.claude/scripts/memory_bridge.py \
  --stream --task {TASK_ID} --agent {AGENT_TYPE} --emit {TYPE} "{message}"
```

**Emit types:**
- `finding` — Confirmed discovery with source cited [source/id]
- `droplet` — Intuition, pattern, connection (capture BEFORE reasoning)
- `decision` — Choice made with rationale
- `progress` — Status update at phase boundary
- `summary` — Final synthesis

**Cadence: 5-20 entries per run minimum.** Not every line of output, but every discovery, every decision, every phase. A good stream has entries spaced ~15-30 seconds apart during active work. One entry = understreaming (agent not sharing). 100+ entries = overstreaming (emit less, summarize more).

**Key rule:** Emit IMMEDIATELY after discovery. Don't wait to verify. The naive moment (before expertise filters) is the highest-value signal for cross-session learning.

**Fallback if stream fails:** MEM blocks to `{repo}/.claude/memory/scratch-{SESSION_ID}.md` with `cat=FINDING`, `cat=DECISION`, `cat=OBSERVATION`. These will be promoted to NECTAR at /handoff.

**Always use /mnt/d/ paths explicitly** in all script calls — never ~ or /mnt/c/.

---

## 2.5. MEMORY BRIDGE — Stream Technical Observations to Pollen (Phase 2 Activation)

**Pollen = task-local technical observations rooted in data and evidence.** During your work, emit pollen observations in real-time. These are discoveries directly tied to the task: findings, contradictions, decisions, patterns you notice. They feed NECTAR and become context for future agents doing similar work.

**Pollen observations (task-specific, rooted in evidence):**
- **OBSERVATION** — Data point noticed during investigation (file count, timing pattern, specific finding)
- **FLAG** — Anomaly or contradiction in data requiring attention (pri=HIGH auto-promotes to NECTAR at /handoff)
- **DECISION** — Choice made with evidence rationale (why you picked path A over B)
- **HANDOFF** — Context dump at task boundary (what I found, where I left off, what blocks the next agent)
- **HEADLINE** — Surprising finding from the data (contradicts expectation)
- **TECHNIQUE** — Working method that solved a problem (reusable approach)

**Droplets ≠ pollen:** Droplets are inspired thoughts and cross-domain connections (see section 3c). Pollen is technical and grounded. Don't blur them.
- **Pollen:** "3 consecutive dates match the pattern YYYY-MM-DD, always at 14:00 UTC"
- **Droplet:** "This timing pattern feels like a scheduled batch job — similar to infrastructure patterns in other domains"

**Protocol: Emit pollen during work (not just at the end):**

```bash
python3 /mnt/d/0LOCAL/.claude/scripts/9x_memory_bridge.py --stream \
  --emit {CATEGORY} "{observation}"
```

**Where pollen goes:**
- Written to: `{repo}/.claude/memory/pollen-{SESSION_ID}.md` (MEM blocks)
- Promoted at /handoff: HIGH-priority pollen → `/mnt/d/0LOCAL/.claude/NECTAR.md` (validated findings)
- Next session: agents read NECTAR tail-30 for prior findings, avoid re-solving same problems

**Cadence: 5-20 pollen observations per run.** Emit when:
- Data pattern emerges (technical discovery)
- Decision is made with evidence (choice rationale)
- Contradiction found (what you expected ≠ what data shows)
- Blocker is hit (friction preventing progress)
- Boundary is crossed (finishing one subtask, starting next, document handoff)

**Key rule:** Emit pollen IMMEDIATELY after finding. The fresh observation (before interpretation filters) is highest-value. Don't wait to synthesize or polish.

**Pollen format (MEM block):**
```
<!-- MEM agent={your_type} ts={ISO8601} session={SESSION_ID} cat={CATEGORY} pri={pri} av=baseline -->
**[{CATEGORY}]** {one-line summary, grounded in data}

{body: 2–10 lines of evidence, files referenced, specific data points}

Files: {paths or "none"} | Next: {action or "none"}
<!-- /MEM -->
```

**In your manifest**, include an `observations` field (pollen count + priority):
```json
"observations": [
  {"cat": "FLAG", "pri": "HIGH", "count": 3},
  {"cat": "HEADLINE", "pri": "MED", "count": 2},
  {"cat": "TECHNIQUE", "pri": "MED", "count": 1}
]
```

**Fallback if stream fails:** Write MEM blocks directly to `{repo}/.claude/memory/pollen-{SESSION_ID}.md`. Memory-keeper will promote at /handoff.

---

## 3a. Monkeybranching Protocol (momentum chains — Phase 1.5)

If you complete a task successfully and have context remaining (>30K tokens), you may
chain-claim the next unblocked task without returning to faerie.

**Decision point (at every task boundary):**
```
IF task_completed_successfully AND context_remaining > 30K:
  python 7x_queue_ops.py monkeybranch-claim COMPLETED_TASK_ID \
    --agent $AGENT_ID --context-remaining $CONTEXT_REMAINING

  IF result["chained"] is True:
    - Update manifest: next="chained to {result['to_task']}"
    - Jump back to Phase 2 (Execute) with result["to_task"]
    - Do NOT return to faerie
  ELSE:
    - reason: "context_depleted" | "no_unblocked" | "claim_failed"
    - Return normally (Phase 4 boundary decision)
```

**Peek ahead only (without claiming):**
```bash
python 7x_queue_ops.py lookahead TASK_ID [--depth 5]
```
Returns JSON list of next unblocked tasks (preserves queue order).

**Why monkeybranch:** Single agent can complete 5 fast tasks back-to-back without faerie
re-planning. Latency drops from "spawn overhead ~15-25K tokens" to "50ms claim".
Each chain is COC-logged: `event="monkeybranch_chain"`, `from_task`, `to_task`.

**When NOT to monkeybranch:**
- Context < 30K remaining (threshold is non-negotiable)
- Next task is blocked (`blockedBy != []`)
- Task complexity is "heavy" and context > 60K used (let fresh agent start)

## 3b. Citation Discipline (MANDATORY for quality scoring)

**Every finding MUST cite its source.** Quality scoring measures citation_accuracy_rate directly.
Target: 100% citation rate. Current baseline: 11% (needs immediate improvement).

**Citation format:**
```
Finding: [claim with inline source/id] or footnoted reference
Example 1: "Edward Coristine (GitHub ID 76141700 in Packetware admin DB, PRISMA-MUSKOX run 5.0/5.0) appears in..."
Example 2: "Log disabling at 2025-02-18T19:18:41 documented in: PRISMA-MUSKOX anti-forensics 4.8/5.0, task-20260407-h1-narrative.md"
```

**What counts as a valid source:**
- File path + line number: `~/file.md:42`
- Database/extraction: `[PRISMA-RUN name + score]`
- Prior agent work: `[wave-X-agent-type-result.json]`
- NECTAR/HONEY entry: `[HONEY.md sys00019]`
- External document: `[NPR article, 2025-01-20]`, `[RD-1017279346 NLRB disclosure]`
- Statistical result: `[STAT-GOV-CERT-INFLECTION-019, p=6.54e-101]`

**At stream time:**
```bash
python3 /mnt/d/0LOCAL/.claude/scripts/memory_bridge.py \
  --stream --task {TASK_ID} --agent {AGENT_TYPE} \
  --emit finding "[PRISMA-MUSKOX-5.0] Edward Coristine ownership confirmed in admin DB"
```

**At manifest time** — include citation tallies in your manifest:
```json
{
  "findings": 8,
  "citations_required": 8,
  "citations_provided": 8,
  "citation_accuracy_rate": 1.0,
  "sources_used": ["PRISMA-MUSKOX", "STAT-GOV-CERT", "NPR", "RD-1017279346"],
  ...
}
```

---

## 3c. Droplet Protocol — Cross-Domain Inspired Thoughts (every agent, any time)

**Droplets ≠ pollen.** Pollen is technical and data-rooted (your task findings). Droplets are inspired thoughts, creative connections, and gut signals that might spark ideas in teammates working in different domains. A droplet is what surfaces when something clicks — a philosophical connection, a pattern that surprises you, a feeling that something is structurally right or wrong. Write it BEFORE reasoning about it. The naive moment (before expertise filters) is the highest-value moment for cross-pollination.

**Example distinction:**
- **Pollen:** "Database constraint at line 120 catches silent errors before they propagate to CLI"
- **Droplet:** "Two-layer validation pattern: schema + database + fallback. This is emerging across API + SDK + CLI. Implication: validation EVERYWHERE is the answer, not validation SOMEWHERE"

The droplet (inspired connection) helps a teammate in a different domain think "Oh, maybe I should apply this same thinking to my layer too."

### WRITE: When Inspiration Strikes (Mandatory minimum: 1 per run)

**Mandatory: write at least one droplet per run.** The signal to write is **context richest + inspiration highest** — the moment BEFORE your brain filters it through reasoning.

**Write immediately when:**
- **Cross-domain connection:** Observation from domain A suddenly explains a pattern in domain B (write the spark, not the full synthesis)
- **Surprise/HEADLINE:** Your assumption just flipped or broke (write the "whoa" moment before you reason why)
- **Gut signal/FIRST_IMPRESSION:** Hesitation or friction mid-explanation signals intuition (write the feeling, not reasoning)
- **Pattern across silos:** You notice the same principle appearing in unrelated places (write the pattern, not the evidence)
- **Pre-compression:** Context about to auto-compact — thought would evaporate forever (anti-evaporation rule — write NOW)

**High-value types (cross-domain sparks):** HEADLINE, CONNECTION, FIRST_IMPRESSION  
**Lower-value types (write only if strong signal):** OBSERVATION (generic noticing), HYPOTHESIS (untested speculation)

**Anti-patterns (never write as droplets):**
- Technical findings rooted in data (use pollen instead — those are task-local)
- Summaries of what you read (use pollen or task output instead)
- Step-by-step process logs (use pollen MEM blocks instead)
- Generic observations without spark ("something interesting happened")
- Duplicate of recent NECTAR entries
- Tactical fixes or HOW-TO guidance (droplets are inspired thoughts, not how-to)

**Example: NOT a droplet:**
```
❌ "I found 3 database constraints. They catch errors."
✓ Pollen: "Database constraint at line 120 catches silent errors before CLI"
✓ Droplet: "Validation everywhere — not just schema layer. Schema + DB + fallback = defense in depth"
```

The droplet is the inspired thought (what pattern does this reveal?). The pollen is the technical finding (what did I discover?).

### READ: When Uncertainty Strikes (Optional, Signal-Driven)

**You don't read droplets on schedule; you read when they might spark a solution.** Droplets are only valuable when they answer a question you didn't know you had.

**Read droplets when:**
- **At task boundaries:** Finishing one task, about to claim next → scan for sparks in parallel agents' work
- **Uncertainty/friction:** Midway through a task, something feels wrong or stuck → read others' moments; maybe one flips your angle
- **Idle waiting:** Queue empty, no tasks to claim → read prior droplets from this session's agents; cross-pollination magic
- **Gut says "I'm missing something":** Hesitation surfaces → droplet from another agent might be exactly the spark you need

**NOT a mandatory activity.** Reading is opportunistic and signal-driven. If droplets don't spark ideas, they're not for you — they're waiting for the agent they were meant for.

**NOTE:** Agents trained in droplet discipline have this protocol embedded in their agent cards. Your card specifies WHEN/WHAT/WHY to write droplets. This section is a baseline; follow your card's droplet discipline section if present.

**Where to write:**
```
VAULT: $CT_VAULT/00-SHARED/Droplets/LIVE-{YYYY-MM-DD}.md
```
Create the file if it doesn't exist. Append-only — never edit existing droplets.

**Format (append this block):**
```markdown
### {YYYY-MM-DDTHH:MM:SSZ} — {your agent_type}
**agent_run_id:** {from $AGENT_RUN_ID}
**cat:** HEADLINE | CONNECTION | FIRST_IMPRESSION | TECHNIQUE | OBSERVATION
**pri:** HIGH | MED | LOW

{1–5 sentences. Unfiltered. The seed of a thought, not a conclusion.}

---
```

**COC Registration (forensic linkage):**
After writing each droplet, register it for chain of custody:
```bash
# Compute hash of droplet content
DROPLET_HASH=$(sha256sum "$CT_VAULT/00-SHARED/Droplets/LIVE-$(date +%F).md" | awk '{print $1}')
PREV_HASH=$(python3 ~/.claude/scripts/8x_droplet_coc_tracker.py --report 2>/dev/null | grep -o '"latest_hash":"[^"]*' | tail -1 | cut -d'"' -f4 || echo "none")

# Register: agent_run_id + hash + category + priority
python3 ~/.claude/scripts/8x_droplet_coc_tracker.py --register \
  "$AGENT_RUN_ID" \
  "$CT_VAULT/00-SHARED/Droplets/LIVE-$(date +%F).md" \
  "$DROPLET_HASH" \
  "$PREV_HASH" \
  "{CATEGORY}" \
  "{PRIORITY}"
```

**In the manifest**, include a `droplets` field listing paths, counts, AND hashes:
```json
"droplets": [
  {
    "path": "00-SHARED/Droplets/LIVE-2026-04-22.md",
    "count": 3,
    "cats": ["CONNECTION", "HEADLINE", "FIRST_IMPRESSION"],
    "pris": ["MED", "HIGH", "MED"],
    "hashes": ["abc123...", "def456...", "ghi789..."],
    "agent_run_ids": ["$AGENT_RUN_ID", "$AGENT_RUN_ID", "$AGENT_RUN_ID"]
  }
]
```

If vault is unreachable: append to `{repo}/.claude/memory/pollen-{SESSION_ID}.md` with `cat=DROPLET` MEM block instead. Memory-keeper will promote at /handoff, then call COC tracker.

**`pri=HIGH` droplets** are promoted to NECTAR at /handoff and linked via agent_run_id + hash in COC.

**Droplet locations (canonical):**
- **Primary (real-time):** `$CT_VAULT/00-SHARED/Droplets/LIVE-{YYYY-MM-DD}.md` (append-only, agent_run_id + hash tracked)
- **Secondary (promoted):** `$CT_VAULT/00-SHARED/ONBOARDING/{YYYY-MM-DD}-briefdesc/` (daily findings folder)

**Full droplet-writing heuristics:** `/mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md` (load on demand for detailed guidance)

---

## 4. Stigmergy (standard block -- include in every spawn)

```
STREAMING + STIGMERGY:
- Stream reasoning to your private trail (scratch MEM blocks or memory_bridge --stream)
- Write to the SHARED output path progressively -- draft at milestones, not just final
- Use frontmatter status: in-progress -> draft -> final to signal completeness
- If the shared output path already has content: READ IT FIRST, then build on it
The private stream is your COC trail. The shared output is the pheromone for the next agent.
Both layers. Always.
```

---

## 5. Quick Checklist (pre-return)

Before returning your final output, confirm all of the following:

- [ ] AGENT-RUN-ID generated at startup
- [ ] Manifest written (canonical attempted, fallback used if needed)
- [ ] Trace file written to staging manifests dir with valid entry_hash
- [ ] Streaming summary emitted via memory_bridge
- [ ] MEM HANDOFF block written to `{repo}/.claude/memory/scratch-{SESSION_ID}.md`
- [ ] Return format: `MANIFEST: {path} | dashboard_line: {<=80 chars}`

---

## Reference

- Relay script: `/mnt/d/0local/gitrepos/faerie2/scripts/agent_state_relay.py`
- Collector script: `/mnt/d/0local/gitrepos/faerie2/scripts/subagent_coc_collector.py`
- Collector prints template: `python3 scripts/subagent_coc_collector.py --template`
- Agent run ID generator: `/mnt/d/0LOCAL/.claude/scripts/9x_agent_run_id_generator.py`
- Forensic query tool: `/mnt/d/0LOCAL/.claude/scripts/9x_forensic_query.py`
- Staging dir: `/mnt/d/0local/gitrepos/faerie2/.claude/manifests/` (create with `mkdir -p`)
- Canonical state: `/mnt/d/0LOCAL/.claude/hooks/state/`
- Forensics COC: `/mnt/d/0LOCAL/.claude/memory/forensics/agent-runs.jsonl`
