---
type: reference
status: active
tags: [skill, faerie, orchestrator, waves]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:033efebecba8e41c1e73f0d15e2d7afe89480a898b2358a85f243271f70a3fc3
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /faerie — Session Orchestrator

Self-orienting session orchestrator. Reads → launches → briefs in 1 turn.

---

## Invocation

| Command | Behavior |
|---------|----------|
| `/faerie` | Standard session start (WORK mode) |
| `/faerie focus on X` | Prioritize tasks related to X |
| `/faerie --explain` | Dry run — show what /faerie would do |
| `/faerie --queue` | Queue manager mode only |
| `/faerie --review` | Red-team top findings, no tasks launched |
| `/faerie --train` | Load training queue, run autotune |
| `/faerie --train {agent-type}` | Train a specific agent type |

---

## What /faerie Does

### Step 0 — Context reads (bash, parallel)
- Read piston-checkpoint.json (wave state, context %)
- Read sprint-queue.json (task counts, priorities)
- Run lean queries: eval score, wave, queue, flags, droplets

### Step 1 — Wave planning
- Classify tasks into W1 (45s) / W2 (180s) / W3 (600s) tiers
- Select agents via `7x_select_agent.py` (performance-ranked)
- Capture baselines for each task

### Step 2 — Wave 1 (inline, Haiku)
- Spawn all W1 agents **without** `run_in_background` — faerie waits
- W1 = fast triage: validation, state reads, scout work

### Step 3 — Wave 2 (inline, Sonnet)
- Spawn all W2 agents after W1 returns — faerie waits
- W2 = feature work: research, analysis, builds

### Step 4 — Respond (one response)
- Read W1+W2 dashboard_lines (≤80 chars each)
- Output dashboard (pre-built by build_dashboard.py)

### Step 5 — Wave 3 (background, after response)
- Spawn W3 agents with `run_in_background: true`
- W3 = deep synthesis, multi-source correlation

---

## Dashboard Format

```
FAERIE 2026-04-24 15:05 | TURN 0 COMPLETE
================================================================
EVAL: 0.64→  T:0.75  M:0.67  R:0.67
GAPS: QUALITY=0.35 → write NECTAR for today's work
WAVE 1  (2 agents)
  trail-finder-A  → 3 abandoned tasks found
  context-manager → HONEY+NECTAR loaded (120 items, 15KB)
WAVE 2  (2 agents)
  data-engineer   → pipeline clean, 50K rows ingested
  memory-keeper   → 12 findings promoted to NECTAR
QUEUE: 8 HIGH | 3 MED | 1 LOW
MEMORY: brief fresh | HONEY 2.1K
================================================================
NEXT: /run to claim tasks | /handoff to close session
```

---

## Key Behaviors

- **TURN 0 rule:** Do not respond until W1 AND W2 are both complete
- **No inline status updates:** User sees nothing until the dashboard
- **Post-compact:** Read piston-checkpoint, launch next wave — do NOT re-read files
- **Fresh-start detection:** If brief age >8h, runs emergency_handoff.py first

---

## Files Read

| File | Purpose |
|------|---------|
| `~/.claude/hooks/state/piston-checkpoint.json` | Wave state + context % |
| `~/.claude/hooks/state/sprint-queue.json` | Task queue |
| `~/.claude/hooks/state/faerie-brief.json` | Session brief (cold start only) |
| `~/.claude/hooks/state/handoff-snapshot-summary.json` | Prior session summary |

---

## Related

- [[run]] — /run skill reference
- [[../Hive/piston-rocket-physics]] — wave model explained
- [[../Onboarding/01-first-session]] — first session walkthrough
- [[../Architecture/piston-waves]] — technical piston architecture
