---
type: design-narrative
blueprint: "[[Blueprints/TechDoc.blueprint]]"
agent_type: python-pro
session_id: queue-analyzer-integration-20260329
doc_hash: sha256:pending
status: final
---

# Queue Analyzer Design — Intent-Driven Piston Model

## Overview

`queue_analyzer.py` is the scoring and wave-assignment engine for `/faerie`. It answers: given what the human wants to do this session (intent), which tasks should run first, second, and third?

The key insight: the same 42-task queue looks completely different depending on session intent. A "clear blockers" session vs a "build momentum" session vs a "do deep work" session requires three different orderings of the same tasks.

---

## Intent Scoring Logic

### `--unblock` — clear whatever is blocking other work

Prioritizes tasks tagged `blocker=true` or tasks that `blocks` many downstream tasks. Easy tasks get a small bonus (quick wins unblock faster). Complex tasks with zero blocks score 0 — they're not the bottleneck.

```
blocker=true        → 1.0  (W1 immediately)
blocks > 2 tasks    → 0.8  (high downstream impact)
complexity=easy     → 0.3  (quick wins)
everything else     → 0.0  (background / skip)
```

Example session: `/faerie --unblock` with current queue routes `faerie2 CLI transition` (complex blocker) and `vault_annotation_sync wire-in` (medium blocker) to W1. Everything else that isn't a quick win goes to W3 or background — the session stays laser-focused on unblocking.

### `--momentum` — clear the backlog, build velocity

Prioritizes easy tasks to generate completed-task count and build throughput. Medium tasks are bonus. Complex and synthesis tasks are skipped entirely (they'd stall momentum).

```
complexity=easy     → 1.0  (W1/W2)
complexity=medium   → 0.4  (W3)
complexity=complex  → 0.0  (background)
```

Example session: `/faerie --momentum` puts 19 easy tasks (WHOIS, DNS checks, link fixes, boilerplate, blueprint stubs) into W1/W2/W3. A focused session can clear 8-10 tasks.

### `--deep` — commit to hard problems

Prioritizes complex tasks with no dependency blocks — tasks that are ready to go but require significant agent effort. Synthesis tasks are included. Blockers get a small bonus (they tend to be complex).

```
complexity=complex  → 1.0
dep-free            → +0.3 (can start now)
estimated_tokens > 50K → +0.5 (real work)
blocker=true        → +0.2 (leverage bonus)
```

Example session: `/faerie --deep` routes `/share command build`, `/preflight command`, `batch API business plan`, and `transcript forensic index` to the front waves. These are the high-leverage complex builds.

### default (balanced)

Mix of all three. Blockers go first, then easy tasks, then dep-free tasks. Good for general sessions where you don't have a specific intent.

```
blocker=true        → +0.9
complexity=easy     → +0.5
no dependencies     → +0.3
always              → +0.1 (floor)
cap                 → 1.0
```

---

## Wave Assignment Rules

After scoring, `assign_waves()` distributes tasks into execution tiers:

| Wave | Execution | Max tasks | Threshold |
|---|---|---|---|
| W1 | Inline sync (faerie waits) | 2 | score > 0.85 OR blocker with score > 0.8 |
| W2 | Inline sync (faerie waits) | 2 | score > 0.5 |
| W3 | Background (post-response) | unbounded | score > 0.2 OR synthesis |
| bg | Fire-and-forget | unbounded | everything else OR deps not met |

Overflow cascade: if W1 is full (2 tasks), high-score tasks spill to W2. If W2 is full, they spill to W3. This prevents wave starvation while keeping inline execution fast.

Dependency guard: if a task has `dependencies: [task_id, ...]` and those tasks aren't completed, it's forced to `background` regardless of score. The piston can't run a task whose inputs aren't ready.

---

## Integration with /faerie

Step 6 of `~/.claude/skills/faerie/SKILL.md` calls `queue_analyzer.py` as a subprocess, parses the JSON output, and uses wave assignments to drive agent spawning:

```
/faerie [--unblock|--deep|--momentum] [natural language focus]
    ↓
queue_analyzer.py --intent {intent} --output-json
    ↓ wave_target on each task
spawn_inline(W1 agent, W1 tasks)    ← faerie waits
spawn_inline(W2 agent, W2 tasks)    ← faerie waits  
spawn_background(W3 agent, W3 tasks) ← fires after dashboard
fire_and_forget(bg tasks)
```

Category → agent routing in Step 6:
- `investigation` → `research-analyst`
- `infrastructure` → `python-pro`
- `meta` / `meta-dev` → `context-manager` / `python-pro`
- `review` → `code-reviewer`
- `publishing` → `documentation-engineer`
- `training` → `membot`
- `forensic` → `evidence-analyst`
- `vault` → `memory-keeper`

---

## Schema Fields (added by `init-schema`)

`queue_ops.py init-schema` adds these fields to every queue task if missing:

| Field | Default | Purpose |
|---|---|---|
| `complexity` | `"medium"` | Scoring: easy/medium/complex/synthesis |
| `blocker` | `false` | Boolean: does this block other tasks? |
| `blocks` | `[]` | List of task IDs this task unblocks |
| `dependencies` | `[]` | List of task IDs that must complete first |
| `wave_target` | `null` | Set at runtime by queue_analyzer.py |
| `estimated_tokens` | `0` | For deep intent scoring (>50K = real work) |

Run: `python3 ~/.claude/hooks/state/queue_ops.py init-schema`

---

## Example Session: `/faerie --unblock`

Scenario: the nuclear-triple report is blocked because `faerie2 CLI transition` hasn't landed — all new sessions still pull from the legacy CLI-GIT repo.

```
$ /faerie --unblock

queue_analyzer output:
  W1: task-20260325-235934-6855 [BLOCKER] → Transition CLI-GIT to faerie2
  W1: task-20260328-031340-4700 [BLOCKER] → Wire vault_annotation_sync into /faerie

faerie spawns W1 (inline, waits for both):
  → python-pro handles CLI transition + legacy cleanup
  → python-pro handles vault_annotation_sync wiring

After W1 returns: both blockers resolved.
W2 is empty (unblock intent, no score>0.5 tasks beyond blockers).
W3: 19 easy tasks queued for background.

Dashboard shows:
  WAVE 1 (143s): faerie2 transition complete, vault sync wired
  WAVE 3: 19 easy tasks launched in background
  UNBLOCKED: nuclear-triple report can now proceed
```

The session unblocked one critical path and cleared the infrastructure debt in a single piston cycle.

---

## Files

- `~/.claude/scripts/queue_analyzer.py` — scoring + wave assignment engine
- `~/.claude/hooks/state/queue_ops.py` — queue ops + `init-schema` command
- `~/.claude/hooks/state/sprint-queue.json` — live queue (50 tasks, 42 queued)
- `~/.claude/skills/faerie/SKILL.md` — Step 6 (intent-driven piston launch)
