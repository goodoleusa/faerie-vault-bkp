# Dynamo — Multi-Session Faerie

Run 2+ Claude sessions on the same queue simultaneously. Sessions coordinate via atomic
file claims and session heartbeats — no network, no server, no configuration required.

---

## Quick Start

Open two terminals. In each:

```bash
cd /mnt/d/0local/gitrepos/faerie2   # or your faerie2 clone
claude                               # start Claude CLI
/faerie                              # orient + launch first wave
```

Both sessions read the same queue. `claim_task.py` handles atomic claiming — whichever
session touches a task first owns it for 2 hours.

---

## Three Dynamo Patterns

### 1. Throughput — Parallel Queue Burn

Both sessions run `/run` on the same queue. No coordination needed.

| Session A | Session B |
|-----------|-----------|
| `/run` (loops) | `/run` (loops) |
| Claims HIGH tasks first | Claims next unclaimed task |
| 2h stale window prevents double-work | Reclaims if A crashes |

**When to use:** Queue backlog. Time-sensitive sprints. Independent tasks (HTML, IPFS, analysis).

**Session setup:**
```bash
# Terminal A
/faerie
/run         # loops until queue empty

# Terminal B (same queue, different session)
/faerie
/run         # claims whatever A hasn't
```

**Queue scope (explicit):**
```bash
python3 ~/.claude/skills/run/claim_task.py --scope global   # always ~/.claude queue
python3 ~/.claude/skills/run/claim_task.py --scope repo     # this repo's queue only
python3 ~/.claude/skills/run/claim_task.py                  # auto: env var → repo → global
```

**Expected gain:** ~1.5–2× throughput vs single session. Collisions <5% (atomic claim lock).

---

### 2. Adversarial — Red-Team Review

One session writes, one session reviews. Built-in quality gate.

| Session A (WORK) | Session B (REVIEW) |
|------------------|--------------------|
| `/faerie` | `/faerie --review` |
| Runs tasks, produces outputs | Red-teams findings, flags gaps |
| Writes to Agent-Outbox | Reads Agent-Outbox, writes to Human-Inbox/flags/ |
| Claims `status: queued` tasks | Does NOT consume the queue |

**When to use:** Investigation findings before publication. Architecture decisions. High-stakes output.

**Session setup:**
```bash
# Terminal A — worker
/faerie
/run

# Terminal B — reviewer (no queue consumption)
/faerie --review
# Reads recent Agent-Outbox outputs, challenges assumptions, flags gaps
```

**What `--review` does:**
- Skips task claiming
- Reads latest outputs from `$CT_VAULT/00-SHARED/Agent-Outbox/`
- Spawns red-team agents to stress-test findings
- Writes flags to `~/.claude/memory/REVIEW-INBOX.md` and `Human-Inbox/flags/`

---

### 3. Complementary — Split by Role

Sessions take different category focuses. Each session's piston claims tasks matching its affinity.

| Session A | Session B |
|-----------|-----------|
| `/faerie focus on data` | `/faerie focus on publish` |
| Claims `-data` category tasks | Claims `-publish` category tasks |
| Data engineer, evidence curator | Report writer, IPFS publisher |
| High affinity for ingest/ETL work | High affinity for reporting/site work |

**When to use:** Full pipeline run. Investigation from raw data to published report in parallel.

**Session setup:**
```bash
# Terminal A — investigation focus
/faerie focus on investigation

# Terminal B — infrastructure focus
/faerie focus on infrastructure
```

**Affinity routing:** Sessions declare preferred agent types. Claim lottery weights by affinity
(0.9 = strongly prefer, 0.5 = willing, 0.1 = evergreen/low priority). Sessions don't block on
affinity — if queue load is heavy on one type, sessions can drift to claim whatever's available.

| Category flag | Default team | Typical affinity |
|---------------|-------------|-----------------|
| `-data` / `data` | data-engineer, security-auditor, data-scientist | 0.9 |
| `-evidence` | evidence-curator, security-auditor | 0.8 |
| `-publish` | report-writer, fullstack-developer, ipfs-publisher | 0.8 |
| `-analysis` | data-scientist, research-analyst, knowledge-synthesizer | 0.7 |
| `-memory` | memory-keeper, context-manager | 0.6 |

---

## Collision Avoidance

`claim_task.py` uses atomic file locking (O_CREAT|O_EXCL). Two sessions cannot claim the same task.

| Mechanism | Detail |
|-----------|--------|
| Lock file | `sprint-queue.json.lock` — exclusive, 30s auto-expiry if stale |
| Session stamp | `claimed_by_session` + `claimed_at` written on claim |
| Stale window | Claims older than 2h are auto-released (session crash recovery) |
| Scope isolation | `--scope repo` vs `--scope global` keeps queues independent if needed |

**If a session crashes mid-task:** The claim expires after 2 hours. Any live session running `/run`
reclaims it automatically.

---

## Wave Model

Each session's piston runs three wave tiers. Sessions share queue but each run their own waves.

| Tier | Model | Timeout | Execution |
|------|-------|---------|-----------|
| Fast-tier | Haiku | ~45s | Inline (awaited — session waits) |
| Medium-tier | Sonnet | ~180s | Inline (awaited — session waits) |
| Synthesis-tier | Sonnet | ~600s | Background (fires after dashboard, non-blocking) |

Fast and medium-tier agents complete inline (awaited — session waits). Synthesis-tier agents run in background. All tiers dispatch in parallel from the mission frontier; response timing is driven by mission complexity and available context, not tier sequencing.

**Multi-session wave coordination:** Sessions write `surfacing-plan-{session_id}.json` after each
wave. Peer sessions read these to avoid spawning duplicate agent types. Coordination is stigmergic
— no direct session-to-session communication.

---

## Session Heartbeat

Sessions register presence via `session_heartbeat.py`. Faerie reads heartbeat at startup to
detect active peers and adjust affinity allocation.

```bash
# Read active sessions
python3 ~/.claude/hooks/state/session_heartbeat.py read

# Example output
{"active_sessions": ["sess-abc123", "sess-def456"], "ts": "2026-04-07T..."}
```

Sessions older than 2h are considered inactive and removed from coordination.

---

## Shared Memory Safety

All shared files are append-only. Concurrent writes are safe.

| File | Safe for concurrent write | Mechanism |
|------|--------------------------|-----------|
| `NECTAR.md` | Yes | Append-only, each entry tagged `session_id` |
| `REVIEW-INBOX.md` | Yes | Append-only |
| `pollen-{SID}.md` | Per-session (no sharing) | Separate file per session |
| `sprint-queue.json` | Yes (serialized) | Exclusive file lock on every write |
| `streams/{task_id}.jsonl` | Yes | Hash-chained JSONL, concurrent appends safe |

---

## Scope Flag Reference

`--scope` controls which queue file `claim_task.py` reads:

| Scope | Queue file | Use when |
|-------|-----------|----------|
| `auto` (default) | env var → repo `.claude/` → `~/.claude/` | Normal operation |
| `repo` | `{git_root}/.claude/hooks/state/sprint-queue.json` | Stay in this repo's queue |
| `global` | `~/.claude/hooks/state/sprint-queue.json` | Cross-repo faerie tasks |
| `investigation` | `~/.claude/memory/investigations/{id}/sprint-queue.json` | Isolated investigation queue |

**Set via env var (per-repo):**
```bash
# In repo .claude/settings.json or shell
export SPRINT_QUEUE_FILE=/path/to/custom/sprint-queue.json
```

---

## Diagnostics

```bash
# Queue status across scopes
python3 ~/.claude/skills/run/claim_task.py --status
python3 ~/.claude/skills/run/claim_task.py --scope global --status

# Active sessions
python3 ~/.claude/hooks/state/session_heartbeat.py read

# Release a stuck claim
python3 ~/.claude/skills/run/claim_task.py --release TASK_ID

# Multi-session eval metrics
cat ~/.claude/hooks/state/piston-multi-session-eval.json
```

---

## Reference

| File | Purpose |
|------|---------|
| `.claude/skills/run/claim_task.py` | Atomic queue claimer (scope flag, lock, TTL) |
| `~/.claude/hooks/state/sprint-queue.json` | Global queue |
| `{repo}/.claude/hooks/state/sprint-queue.json` | Repo-local queue |
| `~/.claude/hooks/state/session_heartbeat.py` | Session presence |
| `~/.claude/hooks/state/piston-config.json` | Affinity weights |
| `docs/PISTON-MULTI-SESSION-DESIGN.md` | Full architecture spec |
