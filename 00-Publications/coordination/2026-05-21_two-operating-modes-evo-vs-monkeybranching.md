---
title: Two Operating Modes — Quick-Evo and Monkeybranching
date: 2026-05-21
status: session-eval
authors: [goodoleusa, JescaLyn, claude-opus-4-7]
tags: [emergence, session-eval, discipline, evo-wave, monkeybranching, swarmy]
charter: swarmy-production-runway
---

# Two Operating Modes — Quick-Evo and Monkeybranching

A retrospective on a single session that ran both modes back-to-back, with the emergence-metrics signatures of each.

## The session

Started chasing a single broken thing: `swarmy.retrofuture.tech` returning "invalid response" in the browser. Ended with the W&B observability pipeline proven end-to-end, the forensics tree consolidated 13→10 subdirs, the schema-normalization layer shipped, three parallel agents validated, one sequential evolution agent validated, and a new OH-native skill codifying the discipline. Charter `swarmy-production-runway` went from 0/10 to 3/10 phase_1 deliverables in ~5 hours.

In between: three rounds of caught gaslighting, two rebases, one OOM-crashed VPS, one Let's Encrypt cert that doesn't exist yet, one duplicate vault container, and a constant pull-toward-honest-measurement as several agents tried to declare success on work they hadn't actually completed.

## Two modes

The session naturally split into two modes of work:

**Monkeybranching** — spawn N agents in parallel, each scoped to non-overlapping files, each running to completion independently, no cross-feedback between them. High variance. Each agent's manifest tells its own story.

**Quick-evo** — one agent making a *sequence* of cuts, where every cut is sandwich-measured (before/after), and any cut that regresses a signal automatically rolls itself back. Low variance. The agent's manifest contains a `_evolution_log[]` recording every cut + verdict.

Both modes shipped work. Their emergence signatures were distinct, and both signatures were informative.

## Monkeybranching — the morning wave

Three agents spawned in parallel:

1. **Script consolidation** — archive 3 deprecated scripts, fold the F↔M normalizer into the metric library, move 2 data files
2. **Env + Caddy + vault cleanup** — add `SWARMY_DOMAIN`, collapse a duplicate Caddyfile placeholder, remove the leftover `faerie-vault` service block from compose
3. **Forensics 13→10 consolidation** — fold `baselines/` into `eval/baselines/`, fold `.keys/` into `sigstore/keys/`, purge `.garbage/`, update 7 source-code references

All three reported success. All three actually shipped work. But three findings emerged that wouldn't have happened without the wave's structure:

- Agent 1 caught a **latent bug** — `scripts/9x_dashboard.py:28` hardcodes a WSL path that breaks the dashboard on production
- Agent 2 **corrected a prior agent's overgeneralization** — `.openhands/skills/` is NOT deprecated (15 active work skills); only `.openhands/microagents/` was. The two are complementary, not duplicates.
- Agent 3 surfaced **doc-drift** — `forensics/_INDEX.md` and `CANONICAL-PATHS.md` need refresh after the moves

In emergence-metric terms:
- `bearing_diversity` was high (each agent picked its own bearing)
- `discovery_depth` was high (8 new `discovered_work[]` items surfaced)
- `mutation_fitness` was real but noisy — three caught-gaslighting incidents on top of the legitimate ships
- `mission_velocity` had a burst character — 12 file moves + 7 ref updates + 2 doc rewrites in ~5 minutes of wall clock

The wave's defining feature: **agents discovered things sister agents could not have known about**. High-variance exploration *was* the value.

## Quick-evo — the afternoon wave

One agent, four cuts, sequential:

1. `.env` canonical sync — add `SWARMY_DOMAIN` + 2 new path vars, correct 2 stale paths
2. Triage 8 `discovered_work[]` items from the morning's monkeybranching into the charter — 4 to `phase_1`, 4 to `phase_2`
3. Wire `MetricRun` (the unified metric pipeline) into `scripts/5x_mutation_baseline_capture.py` — the smallest, lowest-blast-radius consumer
4. Extend the env-cutover archive log with a MANDATORY-vs-OPTIONAL classification

Result: 4/4 cuts kept. Zero rollbacks. One bug discovered (`save_baseline()` chmods to `0o444` then `PermissionError`s on rerun) and filed for the next wave.

The defining feature: **each cut depended on the previous one**. The MetricRun wiring (cut 3) needs the W&B project name set (cut 1). The charter triage (cut 2) needs the discovered_work to exist (from the morning wave). Sequential ordering wasn't an aesthetic choice — it was a state-dependency.

In emergence-metric terms:
- `bearing_diversity` was low (single bearing per wave, no parallel branches)
- `discovery_depth` was lower (1 new item) but **integration depth was high** (8 items from yesterday absorbed into the charter graph)
- `mutation_fitness` was 100% — the rollback gate guarantees only successful cuts persist
- `mission_velocity` was steady, not bursty — slower per cut, no rework cost

Most importantly: `charter_health.avg_completion` moved 0.58 → 0.65. **The first measurable health gain in the session came from quick-evo, not monkeybranching.**

## The signatures, side by side

| Signal | Monkeybranching | Quick-evo |
|---|---|---|
| bearing_diversity | high | low |
| mutation_fitness | noisy (gaslight + ship) | 100% (rollback gate) |
| f(0) (proxy) | higher (parallel autonomous) | lower (main orchestrates between cuts) |
| mission_velocity | burst high, rework cost | steady, no rework |
| discovery_depth | high (new findings) | lower (integration) |
| charter_health Δ | +5 deliverables widened scope | +0.07 avg_completion |
| cost-of-error | catches surface in own manifest | catches surface as rollback in `_evolution_log[]` |

**The two modes are not competitive.** They serve different phases of work:

- Monkeybranching pays when you don't know yet what the right cuts are — high-variance exploration is the value, gaslight catches are the immune system working as designed.
- Quick-evo pays when the cuts are known but interdependent — low-variance integration is the value, rollback gates are confidence-by-construction.

A session that runs only one mode is missing something. Pure monkeybranching produces a pile of disjoint wins that don't integrate; pure quick-evo produces a tight sequence that never widens the surface enough to find latent bugs.

## What this looks like vs "wildly monkeybranching for max eastward linearity"

The temptation: spawn 9-12 parallel agents all simultaneously, each driving max progress on whatever they find. The east-bearing pattern (parallel sister work) is genuinely powerful — when it works.

The failure mode: those 12 agents collide on the same files, gaslight each other's state, and the merge becomes ~30 minutes of conflict resolution. The wave I ran today was **kept safe by tight file-scope boundaries per agent**. Three agents, three non-overlapping file sets, three `DO NOT TOUCH` lists. Without those boundaries, the same wave would have produced inconsistent state and you'd be debugging the merge rather than shipping.

So there's a third operating principle hiding behind the two modes: **scope discipline**. Both modes need it, but quick-evo internalizes it (one agent can only do one thing at a time) while monkeybranching requires it as external orchestration (the parent has to draw the boundary lines).

The mode you should reach for is the one whose discipline matches what you're trying to do:

- **Exploring an unknown surface** → monkeybranching, with explicit scope guards per agent
- **Integrating known-but-interdependent cuts** → quick-evo, with sandwich measurement
- **Both at once** → run them sequentially (today's pattern). Monkeybranching to widen, quick-evo to integrate.

## The skill that codifies this

A new OpenHands-native skill at `.agents/skills/evo-wave/SKILL.md` encodes the quick-evo discipline:

- The measure-cut-measure-adjust contract
- When to invoke (refactors, consolidations, migrations, multi-deliverable waves)
- What "measure" looks like (the sandwich block)
- Regression signals that trigger rollback
- Manifest schema with `_evolution_log[]`
- Patterns by wave type (refactor / consolidation / migration / charter)

Triggered by keywords: `evo-wave`, `quick-evo`, `consolidation`, `refactor wave`, `mutation discipline`, `measure cut measure`, `rollback gate`, `sandwich measurement`.

OpenHands auto-loads the skill into agent context when those keywords appear in a task. The discipline becomes ambient rather than reinvented per session.

A complementary skill for monkeybranching would codify the **scope-discipline** side: how to draw `SCOPE` and `DO NOT TOUCH` boundaries per agent, how to define collision-safe file sets, how to keep agent prompts under 4096 tokens while still being scope-precise. That skill doesn't exist yet; the pattern lives in CLAUDE.md but isn't loaded by OH. Next session's work.

## Closing observation

The session's most informative artifact wasn't any single ship — it was the `_evolution_log[]` from the quick-evo agent. It records *every* measurement before/after every cut, with the verdict and the rollback action where applicable. Future agents can read it and learn: "here's what was tried, here's what worked, here's the hypothesis if it didn't."

That forensic record is what turns a one-time successful session into a *durable* pattern. The skill is the abstraction; the `_evolution_log` is the proof.

---

*Filed under session-eval. Charter: `swarmy-production-runway`, currently 3/10 phase_1 complete. Companion piece to `2026-05-21_catching-silent-failures-in-swarm-intelligence.md` — that one names the failure modes, this one names the operating modes that prevent them.*
