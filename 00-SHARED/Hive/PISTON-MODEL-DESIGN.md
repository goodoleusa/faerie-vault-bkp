---
title: "Piston Model: Orchestrated Agent Rhythm"
date: 2026-03-28
type: system-design
status: implemented
tags: [architecture, agents, orchestration, piston-model, surfacing]
related: [surfacing_scheduler.py, faerie.md, handoff.md, queue_ops.py]
doc_hash: sha256:064373e35da25d3f21bf0d870fb881d429bd576dfa5fd173caad3892aa75f599
hash_ts: 2026-03-29T16:16:21Z
hash_method: body-sha256-v1
---

# Piston Model — Orchestrated Agent Rhythm

## Problem

Flat batch launching wastes potential. Four agents launch together, all return together (~3min), parent processes four returns at once, and context jumps by 60K tokens. If that pushes past the compaction threshold, auto-compact fires and insights evaporate. Meanwhile, between launch and return, the parent session is idle — waiting, not working.

Previous model: **factory** — batch in, batch out, hope for the best.

New model: **orchestra** — instruments enter at different times, creating rhythm, depth, and forward motion.

## Design: Speed Tiers as Pistons

Agents are classified into three speed tiers based on typical return time:

| Tier | Return | Role | Metaphor | Example Agents |
|------|--------|------|----------|----------------|
| **Fast** | ~30-60s | Momentum | Percussion | Explore, security-auditor, admin-sync, token-optimizer |
| **Medium** | ~2-5min | Workhorse | Melody | data-engineer, data-scientist, evidence-analyst, python-pro |
| **Deep** | ~5-20min | Synthesizer | Harmony | research-analyst, fullstack-developer, workflow-orchestrator |

### The Piston Stroke

```
Time 0s     Fast agents launch (Wave 1)
            ├── security-auditor: validate hashes
            └── context-manager: triage queue

Time ~45s   Fast returns arrive → parent processes immediately
            ├── Results feed Wave 2 prompts
            └── Fast agent auto-claims next fast task (relaunch)

Time ~30s   Medium agents launch (Wave 2)
            ├── python-pro: build streaming handoff
            └── evidence-curator: siphon REVIEW-INBOX

Time ~90s   Deep agent launches (Wave 3)
            └── research-analyst: cross-investigation synthesis

Time ~3min  Medium returns → parent synthesizes substantive work
            Meanwhile fast agents on 3rd-4th task cycle

Time ~10min Deep return → crystallize jewels → queue new cycle
```

### Why This Beats Flat Batching

1. **No idle parent**: Fast returns arrive within a minute. Parent always has work to process.
2. **Forward feeding**: Wave 1 findings enrich Wave 2 prompts. Wave 2 results give Wave 3 richer context.
3. **Controlled surfacing**: Returns stagger naturally instead of clustering. No 60K spike.
4. **Queue flywheel**: Each completed task may spawn successor tasks. Fast completions keep the flywheel spinning.
5. **Crashlanding prevention**: Budget allocated per wave. If Wave 1+2 consume more than expected, Wave 3 scales down or cancels.

## Token Budget Allocation

Per wave, token budgets are capped to prevent surfacing overload:

- **Wave 1 (Fast)**: 15% of remaining budget, max 30K tokens
- **Wave 2 (Medium)**: 50% of remaining (after Wave 1), max 60K
- **Wave 3 (Deep)**: Whatever remains after Wave 1+2, minus synthesis reserve (8K)

The synthesis reserve ensures the parent always has headroom to process returns and crystallize findings.

## Self-Calibration

Speed tier assignments are defaults. After 3+ observations, `surfacing_scheduler.py calibrate` replaces defaults with actual measured return times. A "fast" agent that consistently takes 3 minutes gets reclassified. The system learns its own rhythm.

Metrics tracked per surfacing event:
- `tokens_returned`: actual return size
- `duration_sec`: time from launch to return
- `launch_ctx_pct` / `return_ctx_pct`: context state before/after
- `near_compact_threshold`: did this return risk auto-compact?

## Overnight Opus Synthesis (Batch API)

Real-time sessions use Sonnet/Haiku (cheap, fast). Opus is reserved for between-session batch synthesis:

```
User's day:  Sonnet/Haiku sessions → NECTAR, scratch, streams, queue completions
Night:       Batch API (Opus, 50% off) processes accumulated work
               → HONEY crystallization (deeper, richer)
               → Cross-session pattern detection
               → Hypothesis confidence recalculation
               → Agent card training updates
Morning:     /faerie reads overnight-enriched HONEY → "wake up smarter"
```

### How It Works

At `/handoff`, the system queues overnight batch jobs:
1. Collect day's NECTAR entries, scratch observations, stream files
2. Package as Batch API request (Opus model, 24h turnaround, 50% discount)
3. Batch job performs: crystallize NECTAR→HONEY, evaluate hypotheses, update agent cards
4. Results written to `overnight-synthesis.json`
5. Next `/faerie` reads synthesis results → session starts with deeper context

### Product Economics

| Model | When | Cost | Purpose |
|-------|------|------|---------|
| Haiku | Real-time, fast tier | Lowest | Triage, validation, momentum |
| Sonnet | Real-time, medium tier | Moderate | Substantive work, analysis |
| Opus (Batch) | Overnight | 50% off standard | Crystallization, synthesis |

The user experiences opus-quality insights without opus-cost sessions. The piston model makes Sonnet sessions feel like opus through orchestration.

## Implementation

### Files Modified
- `~/.claude/scripts/surfacing_scheduler.py` — Added `SPEED_TIERS`, `get_speed_tier()`, `piston_plan()`
- `~/.claude/commands/faerie.md` — References `surfacing_scheduler.py piston` for launch planning
- `~/.claude/commands/handoff.md` — Queues overnight batch synthesis
- `~/.claude/hooks/state/sprint-queue.json` — All tasks tagged with `agent_type`
- `~/.claude/scripts/debloat.py` — Token-based budgets (chars/4), fixed KeyError on scan

### Commands
```bash
# Plan a piston launch
python3 ~/.claude/scripts/surfacing_scheduler.py piston

# Classify a single agent
python3 ~/.claude/scripts/surfacing_scheduler.py classify research-analyst

# Self-calibrate from history
python3 ~/.claude/scripts/surfacing_scheduler.py calibrate

# View current calibration state
python3 ~/.claude/scripts/surfacing_scheduler.py report
```

## Relationship to Existing Systems

- **surfacing_scheduler.py**: Piston is a new `plan` mode alongside flat `plan`. Both coexist.
- **queue_ops.py**: Unchanged. `claim --category --max` already supports piston relaunch.
- **context_phase.py**: Provides phase state (LIFTOFF/ORBIT/DEORBIT/REENTRY) that constrains wave launches.
- **session_metrics.py**: Tracks piston effectiveness via leverage ratio and surfacing quality.
- **/faerie**: Conductor. Reads piston plan, launches waves, processes returns, relaunches.
- **/run**: Tight queue consumer. Operates WITHIN a wave — claims and chains through tasks.

## Design Principles

1. **Flow over throughput**: Moving through work matters more than completing the most tasks. One connected insight > three disconnected completions.
2. **Natural rhythm over rigid scheduling**: Speed tiers create organic stagger. Self-calibration adapts to reality.
3. **Forward motion compounds**: Each return generates new work. The flywheel spins faster as the session progresses.
4. **Opus is the special sauce**: Save the expensive model for the one thing it does that cheaper models can't — deep cross-domain synthesis. Everything else, orchestration does better.
