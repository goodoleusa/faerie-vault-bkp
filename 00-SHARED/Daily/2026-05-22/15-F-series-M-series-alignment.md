---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: f-and-m-series-alignment
status: synthesis-log
canon_candidate: true
---

# F-series (swarmy internal) ↔ M-series (external benchmark) alignment

User stated (verbatim):

> "keep F1-F15 (the name for faerie-now-swarmy internal metrics)
>  aligned with M1-M15 (similar class metrics for external comparison)"

This closes the membench naming question: there are **two parallel
metric series** that should always sit at the same number for the
same concept.

## The two series

| Series | Scope | Lives at | Purpose |
|---|---|---|---|
| **M1-M15** | External / cross-system benchmark | `/mnt/d/0local/gitrepos/membench/METRICS.md` (canonical spec) + `scripts/probes/M{N}_*.py` (swarmy's M-implementations) | Compare swarmy vs other agent systems; benchmark-grade |
| **F1-F15** | Internal / swarmy-specific | `scripts/probes/F{N}_*.py` (swarmy's F-implementations) | Tune swarmy via internal-only signals; benchmark-relative |

**Alignment rule:** F1 = same concept as M1, F2 = same concept as M2,
etc. The threshold may differ (M is benchmark-grade ceiling; F is
swarmy-specific target). The DEFINITION never differs.

## Today's state (per canonical /membench/METRICS.md)

| # | M-series (defined upstream) | F-series (swarmy probe) | Status |
|---|---|---|---|
| 1 | Retention | F1 retention | ✅ M1 implemented; F1 = same |
| 2 | Relevance | F2 relevance | ⚠ M2 defined upstream; F2 not implemented |
| 3 | Work Efficiency / Parallelization | F3 work efficiency | ✅ M3 implemented |
| 4 | Overhead | F4 overhead | ⚠ M4 defined upstream; F4 not impl |
| 5 | Continuity | F5 continuity | ⚠ M5 defined upstream; F5 not impl |
| 6 | Coordination (diagnostic) | F6 coordination | ⚠ M6 defined upstream; F6 not impl |
| 7 | Crystallization (diagnostic) | F7 crystallization | ⚠ M7 defined upstream; F7 not impl |
| 8 | Confabulation (VETO GATE) | F8 confabulation | ✅ M8 implemented |
| 9 | Ceiling-Hit (diagnostic) | F9 ceiling-hit | ⚠ M9 defined upstream; F9 not impl |
| 10 | Coverage (composite multiplier) | F10 coverage | ⚠ M10 defined upstream; F10 not impl |
| 11 | Bootstrap (VETO GATE) | F11 bootstrap | ✅ M11 implemented |
| 12-15 | NOT YET DEFINED in canonical spec | NOT YET DEFINED | ❌ design needed upstream FIRST |

## Where the work needs to happen

### Upstream (membench repo)

The canonical METRICS.md spec at
`/mnt/d/0local/gitrepos/membench/METRICS.md` defines M1-M11 today.
M12-M15 don't exist there yet. **Design them upstream first** —
otherwise swarmy's F12-F15 would be canonized against nothing.

Candidates for M12-M15 the swarmy work surfaced this session that
could inform the upstream design:

- **M12 — Cross-repo propagation** — when a SHAPE (mission essence)
  is canonized in one repo, what fraction of sister repos with the
  same shape adopt the protocol within N days? Direct measure of
  "missions move SAFELY + SWIFTLY across repos."

- **M13 — Charter-claim health** — what fraction of orphan missions
  emerging in the mission graph get claimed by an aligned active
  charter (vs left orphan vs new-charter-spawned)? Healthy = high
  claim rate (system absorbing emergence).

- **M14 — Shape-trajectory drift** — how much do shapes' counts
  drift against their target_direction over a rolling window?
  Beneficial cuts move shapes toward target; harmful cuts pull
  them away.

- **M15 — Formula composition coherence** — when a top-level
  composite formula (e.g., swarm-vitality) computes, do the
  underlying primitive formulas' values agree on direction? If
  the composite says "healthy" while underlying probes say
  "regressing," that's a measurement bug.

These are candidate definitions — upstream membench repo would
need to author + accept them before the F12-F15 implementations
land in swarmy.

### Downstream (swarmy faerie2 repo)

Once M12-M15 are defined upstream:
1. Implement F12-F15 probes at `scripts/probes/F{N}_*.py`
2. Add their thresholds to `PROBE_THRESHOLD` + `F_PROBE_THRESHOLD`
   in `scripts/3x_membench_probes.py`
3. Update `_meta/swarmy.config.json::f_metric_aliases` so the
   harness knows F12==M12 for cross-scoring
4. Wire into `swarmy_metrics(verb='membench')` for live measurement

## What just changed (today)

1. **Moved active probes OUT of quarantine.** `scripts/probes/`
   now holds the canonical M1, M3, M8, M11 implementations.
   Quarantine is for DEAD code, not active runners.

2. **Removed M12 stub** from `PROBE_THRESHOLD`. It was a threshold
   for a non-existent probe — and the canonical METRICS.md spec
   doesn't define M12 either. Stub deleted with a comment pointing
   at the upstream design path.

3. **Added F_PROBE_THRESHOLD** as a sibling dict (default-equal to
   M thresholds). F-series implementations can override per-metric
   when swarmy's internal target differs from the benchmark ceiling.

4. **Canonized the F↔M alignment** in this doc + via the env config
   path (`_meta/swarmy.config.json::f_metric_aliases` — to be wired
   in next pass).

## Single-line summary

**F1-F15 (swarmy internal) and M1-M15 (external benchmark) are
parallel series at the same number for the same concept. M1-M11
are defined upstream + implemented in `scripts/probes/`. M12-M15
need upstream design FIRST — candidate definitions surfaced this
session: cross-repo propagation, charter-claim health, shape-
trajectory drift, formula composition coherence. F-series mirrors
M-series; implementations land in `scripts/probes/F{N}_*.py` once
the upstream spec exists.**

---

*Closes the doctrine arc 08-15. M-series spec lives upstream at
`/mnt/d/0local/gitrepos/membench/METRICS.md` and should remain
the source-of-truth. Swarmy's role is to IMPLEMENT (not redefine)
M-series + maintain F-series mirrors.*
