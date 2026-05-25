---
type: primer
status: active
tags: [commands, primer, faerie, training, evolution]
parent: ../HOME.md
up: ../HOME.md
created: 2026-04-24
doc_hash: sha256:719b3224580286fcc7ca060cd0da59909490e835d626a7e005c3dc6fd0e9f635
hash_ts: 2026-04-25T01:29:51Z
hash_method: body-sha256-v1
---

> [↑ Home](../HOME.md) · [Skills Reference](Skills-Reference/INDEX.md)

# faerie2 Command Primer

One document. Every command you need to run, evaluate, or dev-tweak faerie.

Organized by **intent** — what you are trying to do — not by alphabet.

---

## Quick-Reference Card

```
COLD START:    /preflight → /faerie
WARM DISPATCH: /run
EVAL CHECK:    /dev-eval | /metrics | /dev-status
TRAINING:      /train --run {agent} | /train --roster {cat}
HANDOFF:       /handoff (memory promote) → /done (sprint close)
TWEAK:         /debloat | /update-config | /dev-health
KNOWLEDGE:     /crystallize (HONEY) | /droplet (insight)
QUEUE:         /queue (view) | /task (add) | /focus (filter)
```

---

## Section 1 — Running Faerie (orchestrate work)

### `/preflight`
**When:** Before every `/faerie` cold start.
**What it does:** Pre-session scan — checks queue health, hook wiring, piston state, context budget, and any stale manifests. Surfaces blockers before they become mid-session surprises.
**Produces:** Console summary of pass/fail checks; writes `preflight-result.json` to `~/.claude/hooks/state/`.
**Pitfalls:** Skipping this on a new session means `/faerie` may launch into a broken hook or a stale queue claim.

---

### `/faerie`
**When:** Cold start — beginning of a workday or new session after `/handoff`.
**What it does:** Session orchestrator. Reads `piston-checkpoint.json` + `sprint-queue.json`, then executes the current wave (W1/W2/W3) by spawning agents via `7x_spawn_template.py --bundle`. Collects `dashboard_line` returns. Scans for presents (orphaned HIGH droplets, lonely tasks, eval jumps).
**Wave shape:**
- W1 — parallel haiku spawns, fast triage, 45s target
- W2 — single-lane or team sonnet dispatches, 180s target
- W3 — deep synthesis, background, no blocking

**Output:** FAERIE dashboard to stdout (W1+W2 results + PRESENTS + NEXT). W3 runs in background.
**Key constraint:** Spawns MUST be rendered via `7x_spawn_template.py --bundle` (enforced by `8x_spawn_contract_enforcer.py` PreToolUse hook — direct prompt construction is blocked).
**Pitfall:** Do not run `/faerie` mid-session after auto-compact. After compact, read `piston-checkpoint.json` and continue — `/faerie` is a cold-start instrument only.

---

### `/run`
**When:** Warm dispatch — queue has tasks and you want to execute them without a full cold start.
**What it does:** Queue consumer. Claims up to 4 HIGH-priority unclaimed tasks atomically, renders context bundles to disk (`~/.claude/hooks/state/bundles/{task_id}.json`), emits compact JSONL references (one line per task), then main parses those lines and calls `Agent(prompt=f"READ: {bundle_path}...")` for each.
**Common args:**
```
/run               # batch loop until queue empty
/run --once        # claim one batch then stop
/run --dry-run     # show what would be claimed, no side effects
/run --max-count 3 # claim up to 3 (default: 4)
```
**Output:** JSONL task refs + final summary JSON (`status`, `consumed`, `remaining`, `dashboard_line`). Manifest at `~/.claude/hooks/state/wave-orchestrator-result.json`.
**Pitfall:** Bundles are NOT printed to stdout — they live on disk. Main receives only a path reference (~100 tokens per task, not ~5K). Do not expect bundle content inline.

---

### `/new` and `/sprint`
**When:** Starting a new sprint or onboarding a fresh project phase.
**What they do:** `/new` initializes sprint state (writes fresh `sprint-queue.json`, resets piston). `/sprint` sets the sprint milestone and configures wave shapes for the work ahead.
**Produces:** Updated `sprint-queue.json` + `waves-config.json` entries.

---

### `/handoff`
**When:** End of workday — not just end of a CLI session.
**What it does:** Three-step session wind-down.
1. Spawns membot (background, fresh 200K context) with a session summary written from conversation memory.
2. Runs mechanical scripts: `emergency_handoff.py`, `session_stop_hook.py`, `eval_harness.py --quick`, `5x_handoff_snapshot_writer.py`.
3. Prints brief (composite score + hot items for next session).

**Produces:** `handoff-snapshot.json`, `faerie-brief.json`, updated `NECTAR.md` (HIGH flags promoted), vault `HANDOFF-SNAPSHOT.md`.
**Critical rule:** Spawn membot FIRST. The live conversation context is the richest source of "what happened" — it cannot be reconstructed from files.
**Pitfall:** Do NOT read HONEY, NECTAR, or queue files inline in the parent at handoff. Parent context is low — delegate everything to membot.

---

### `/done` and `/end`
**When:** Sprint close — the milestone is met, not just a daily wind-down.
**What they do:** Archive completed sprint artifacts, mark sprint milestone done in state, write sprint retrospective droplet. `/end` is the alias.
**Produces:** Sprint archive in `forensics/sprints/`, updated `sprint-queue.json` with sprint status = `complete`.

---

## Section 2 — Evaluating Performance

### `/dev-eval`
**When:** After a wave completes, after an agent run of interest, or when you suspect a score drop.
**What it measures:** Full breakdown across dimensions A–G (Accuracy, Breadth, Coherence, Depth, Evidence, Framing, Generation quality) + meta-metrics M1–M11 (throughput, memory, resilience, quality, piston efficiency, model routing, etc.) + trend arrow vs last run.
**Output:** Vault doc in `$CT_VAULT/00-SHARED/ONBOARDING/{date}/`. Console summary with scores + deltas.
**How to interpret:** Any dimension < 0.70 is a red flag. Trend arrows matter more than absolute score — a rising 0.65 is healthier than a falling 0.85.
**How often:** After each significant wave, and always before a sprint close.

---

### `/metrics`
**When:** Quick system health check mid-session.
**What it measures:** Session + agent dashboard — spawn count, return count, context burn rate, queue depth, agents in flight.
**Output:** Console dashboard. Does not write a vault doc.
**How often:** On demand. Lightweight — use freely.

---

### `/dev-status`
**When:** All-in-one view: eval + queue + memory + agents in a single call.
**What it measures:** Composite of `/dev-eval` summary + queue state + pollen line count + agent roster.
**Output:** Console block. Good for a morning orientation check.

---

### `/dev-checkpoint`
**When:** During a long session, between waves, when you want to record progress without doing a full handoff.
**What it does:** Session eval checkpoint — snapshots current scores to `piston-checkpoint.json` and writes a checkpoint vault doc.
**Produces:** Updated `piston-checkpoint.json` + vault checkpoint entry.

---

### `/dev-health`
**When:** After changes to hooks, scripts, or settings; or when something feels off in the system plumbing.
**What it measures:** Nervous-system health — hook wiring (are registered hooks actually firing?), script equilibrium (TIER/REPLACES/METRIC/LOAD declarations), budget headroom.
**Output:** Pass/fail report with file paths for any violations. Integrates with `9x_equilibrium_audit.py`.
**How often:** After any `settings.json` change. Before a sprint. Anytime a hook behaves unexpectedly.

---

### `/dev-pressure`
**When:** Before `/crystallize`, or when HONEY/NECTAR feels stale.
**What it measures:** Crystallization pressure — token budget headroom for HONEY and NECTAR, recurrence counts on native memory entries, flagged HONEY candidates.
**Output:** Pressure score per memory file + list of candidates ready for integration.

---

### `/eval`
**When:** Reading eval-cards for an agent type.
**What it does:** Agent eval surface — loads the eval-card for a given agent type and displays KPIs, score history, and penalty schedule.
**Usage:** `/eval documentation-engineer` — shows the public eval-card at `forensics/eval-cards/documentation-engineer.md`.

---

### `/dev-compare`
**When:** Choosing between models for a wave, or benchmarking a new model.
**What it does:** Model comparison benchmark — runs a standard task set against two model configs and outputs side-by-side quality/cost metrics.
**Produces:** Vault comparison doc + delta table.

---

### `/vanilla`
**When:** Establishing a baseline before testing an orchestration change.
**What it does:** Runs a task against vanilla Claude (no faerie orchestration, no tools, no hooks) and records baseline scores. Used to measure the delta that faerie adds.
**Produces:** `vanilla-baseline-{date}.json` in `forensics/`.

---

## Section 3 — Dev Tweaks (modify substrate)

### `/debloat`
**When:** Periodically, and before a major sprint.
**What it does:** System health scan — checks all memory files against token budgets, identifies oversize components, flags scripts without TIER/REPLACES declarations.
**CLI equivalent:** `python3 ~/.claude/scripts/debloat.py --scan`

### `/update-config`
**When:** Changing hooks, env vars, or permissions in `settings.json`.
**What it does:** Guided settings.json update with pre/post validation — ensures hook paths are real, matchers are valid, no duplicate entries.

### `/system`
**When:** Orientation to the meta-architecture before making substrate changes.
**What it does:** Prints the architecture overview: piston wave frame, hook registry, memory topology, agent roster, eval pipeline.

### `/rule`
**When:** Loading a sauce rule on demand without full rules reload.
**What it does:** Appends a rule from `~/.claude/rules/` to the active session context.

### `/token-optimizer`
**When:** After observing high context burn or before a W1 that needs to fit in a tight budget.
**What it does:** Caching/batching audit — identifies hot prompts that should be cached, flags sweep operations that should be batched, estimates potential token savings.

### `/hookify`
**When:** You want to convert a pattern into an enforced hook.
**What it does:** Guides creation of a new PreToolUse or PostToolUse hook rule in `settings.json` + the hook script. Available via `hookify@claude-plugins-official` plugin (enabled in `settings.json`).

### `/claude-docs`
**When:** Deep-diving Claude API context window behavior, auto-compact triggers, or token counting.
**What it does:** Surfaces Claude API documentation context. See `forensics/` for past `/claude-docs` runs on context metrics and auto-compact behavior.

---

## Section 4 — Training and Agent Evolution

**This is the architecture of how agents get better over time.**

### How On-the-Job (OTJ) Learning Works

Every agent run automatically feeds the eval pipeline:

1. Agent completes task, writes manifest with `dashboard_line` + findings.
2. PostToolUse hook fires `8x_roster_update.py` (registers the run).
3. `eval_harness.py` scores the run against the agent's KPIs.
4. `9x_agent_card_updater.py` reads `system-eval.json` → updates the agent's card in `~/.claude/agents/{type}.md` IF the new score beats the existing last score.
5. Score history accumulates. Tier promotion fires when 3 consecutive evalbot updates reach ≥ 0.90.

This runs silently in the background. No manual steps required for OTJ learning.

---

### Where Agent Evolution is Recorded

**Private card** (locked; eval-writes only):
```
~/.claude/agents/{agent-type}.md
```
Contains:
- `## Last Training` — locked BASELINE + append-only Self-Updates
- BASELINE: `date | score | source | tier` (only eval writes here)
- Self-Updates: agent-appended observations from runs

**Public eval-card** (readable by anyone):
```
faerie2/forensics/eval-cards/{agent-type}.md
```
Contains: KPIs, score history, penalty schedule, capability inventory.

**Live vault dashboard** (Dataview-driven):
```
vault/00-SHARED/Dashboards/agent-eval-LIVE.md
```
Auto-updated via `9x_agent_card_updater.py` at SubagentStop.

---

### Agents Currently Eval-Tracked

The following agent types have registered eval-cards (as of last audit):
- `workflow-orchestrator` — throughput, piston efficiency, model routing
- `memory-keeper` / `membot` — memory retention, continuity
- `evidence-curator` — quality, evidence tier accuracy
- `data-scientist` — quality, analysis depth
- `report-writer` — quality, clarity
- `documentation-engineer` — coverage, example accuracy
- `error-coordinator` — resilience
- `queue-janitor` — queue drain rate (newly registered)

To see the current roster: `ls /mnt/d/0local/gitrepos/faerie2/forensics/eval-cards/`

---

### `/train` — Unified Training Hub

**Replaces:** `/autotune` (deprecated), `/training-roster` (deprecated), `/continual-learning` (deprecated — now embedded in `/faerie` roundup+learn step).

```
/train                           # view training queue (what's pending)
/train --run {agent-type}        # autotune one agent (was /autotune)
/train --roster {category}       # batch training for a category (was /training-roster)
/train --prep {category}         # prep roster for sprint (stage training tasks)
```

**`/train` (no args):**
Reads `~/.claude/hooks/state/training-snapshot.json` (written by `7x_training_orchestrator.py` at PostToolUse) and displays the current training queue: which agents are pending eval, last scores, training priority.

**`/train --run {agent-type}`:**
Autotunes one agent. Spawns an eval agent that:
1. Loads the agent's public eval-card from `forensics/eval-cards/`
2. Runs the agent against a scored benchmark task set
3. Compares score to BASELINE
4. If score beats BASELINE: calls `9x_agent_self_append.py` to append Self-Update to the private card; updates BASELINE if tier-promotion threshold is met
5. Returns a scored manifest

Example:
```
/train --run documentation-engineer
```

**`/train --roster {category}`:**
Batch training for all agents in a category. Categories: `core`, `investigation`, `infrastructure`, `specialist`.
Spawns eval agents in parallel (W1 shape). Each agent evaluated against its own KPI set.

Example:
```
/train --roster core
```

**`/train --prep {category}`:**
Stages training tasks in `sprint-queue.json` for the named category without executing them. Useful before a sprint where you want to slot training into the queue flow rather than running it inline.

---

### How to View an Agent's Evolution

**View score history and KPIs:**
```bash
cat /mnt/d/0local/gitrepos/faerie2/forensics/eval-cards/documentation-engineer.md
```

**See last 5 training entries:**
```bash
grep -A2 "Last Training" /mnt/d/0LOCAL/.claude/agents/documentation-engineer.md | head -20
```

**Check if a score beat baseline:**
```bash
python3 /mnt/d/0local/gitrepos/faerie2/scripts/9x_beat_last_verifier.py
```

**Training snapshot (all agents, current state):**
```bash
cat ~/.claude/hooks/state/training-snapshot.json | python3 -m json.tool | grep -E "agent|score|tier"
```

---

### Deprecated Training Commands — Redirect Table

| Deprecated | Redirect | Notes |
|---|---|---|
| `/autotune` | `/train --run {agent}` | Exact functional replacement |
| `/training-roster` | `/train --roster {category}` | Batch now category-scoped |
| `/continual-learning` | `/faerie` | OTJ learning is always-on; the explicit skill is gone |

Do not use the deprecated commands. They will not resolve and will cause confusion.

---

## Section 5 — Memory and Knowledge Capture

### `/crystallize`
**When:** Pressure-driven — run `/dev-pressure` first. Only run when recurrence count ≥ 3 across 3+ sessions on a HONEY candidate.
**What it does:** Integrates validated NECTAR entries into HONEY. This is NOT compression — it is synthesis: denser, richer statements carrying more meaning in fewer lines.
**Critical rule:** Do not queue this as a system task. HONEY crystallization is a human choice. Budget headroom alone is not sufficient reason to run it.

### `/handoff`
Memory promotion happens HERE, not at session stop. pollen → NECTAR → vault. (See Section 1.)

### `/droplet`
**When:** Immediately when a deep insight forms — especially when reasoning spans 3+ documents.
**What it does:** Appends a timestamped insight to `$CT_VAULT/00-SHARED/Droplets/LIVE-{date}.md`.
**Rule:** Write droplets immediately. Auto-compact fires at peak context richness — batch capture loses what stream capture preserves.

### `/context-roundup`
**When:** End of a dense session before `/handoff`, or when pollen is crowded.
**What it does:** Collects all MEM blocks from pollen, deduplicates, and writes a canonical context index. Surfaces HIGH-priority items for membot.

---

## Section 6 — Queue Operations

### `/queue`
**When:** Anytime you want to see the current task landscape.
**What it does:** Sprint-aware queue view — shows tasks by priority and wave, claim state, blockedBy dependencies, and drain rate.
**Common args:** `/queue --high` (HIGH only), `/queue --wave W2`, `/queue --blocked` (show dependency chains).

### `/task`
**When:** You want to add a task from current conversation context without leaving the session.
**What it does:** Writes a new task entry to `sprint-queue.json` via `7x_queue_ops.py`. Prompts for goal, priority, wave, and blockedBy.

### `/focus`
**When:** You want to filter the queue to a specific domain or agent type for a sprint.
**What it does:** Sets a queue focus filter in `sprint-queue.json`. Subsequent `/run` calls only claim tasks matching the filter.

### `/suggest`
**When:** The queue feels stale or you want faerie's read on the highest-value next steps.
**What it does:** Reads current queue + piston state + eval trend and proposes 3–5 high-value next tasks with rationale. Does not write to queue — you confirm before anything is added.

---

## Worked Examples

**Example 1: Check how documentation-engineer has improved over the last 5 runs**
```bash
cat /mnt/d/0local/gitrepos/faerie2/forensics/eval-cards/documentation-engineer.md | grep -A3 "score"
# Then compare to private card:
grep -A2 "Self-Updates" /mnt/d/0LOCAL/.claude/agents/documentation-engineer.md | tail -15
```

**Example 2: Run a full cold start correctly**
```
/preflight          # verify no broken hooks or stale claims
/faerie             # orient, read piston state, launch W1
# (W1 agents run, returns arrive)
# faerie launches W2 automatically
# W3 spawns in background
/dev-checkpoint     # snapshot scores mid-session
```

**Example 3: End of day with memory promotion**
```
/handoff            # spawn membot (background), run mechanical scripts, print brief
# (next morning)
/preflight
/faerie             # reads faerie-brief.json written by last night's membot
```

---

## Hook and Script Reference (what fires when)

| Trigger | Script | Purpose |
|---|---|---|
| PreToolUse: Agent | `8x_spawn_contract_enforcer.py` | Block direct prompt construction |
| PreToolUse: Write/Edit | `8x_vault_frontmatter_validator.py` | Enforce vault frontmatter schema |
| PostToolUse: Agent | `8x_roster_update.py` | Register agent run |
| PostToolUse: Write/Bash | `9x_forensic_signer.py` | Sign forensic artifacts |
| PostToolUse: eval_harness | `7x_training_orchestrator.py` | Write training snapshot |
| PostToolUse: eval_harness | `9x_beat_last_verifier.py` | Check if score beat baseline |
| SubagentStop | `agent_tracker.py stop` | Track agent lifecycle |
| Stop | `session_stop_hook.py` | CLI run end — transcript capture, state COC |
| PreCompact | `8x_precompact_springboard.py` | Checkpoint before context wipe |

---

> Cross-links: [Skills Reference](Skills-Reference/INDEX.md) · [Home](../HOME.md)
