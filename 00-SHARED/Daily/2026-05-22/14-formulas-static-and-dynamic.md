---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: formulas-composable-substrate
status: synthesis-log
canon_candidate: true
---

# Formulas — the static + dynamic composable layer

User asked (verbatim):

> "and how do formulas play into this"
> "both static and dynamic (functions, using outputs as inputs to the
>  function)"

Formulas complete the picture between shapes (the measurement
substrate) and missions (the emergent pattern). Where shapes COUNT
things, formulas COMPUTE things — and importantly, the dynamic kind
composes (one formula's output becomes another formula's input).

## The two kinds

### Static formulas — closed-form predicate / aggregation

A static formula is a fixed function that maps current state → a
scalar (or fixed-shape struct):

```
manifest_count_today(forensics) → int
active_charter_count(forensics) → int
ffmx(metric_log, window=24h) → float  (Forensic Frequency Mutation Index)
bearing_distribution(manifests, window=24h) → {N,S,E,W: %}
cluster_prefix_density(charters) → {term: count}
```

These are the "vital signs" — read once, get a number. Each
membench probe is essentially a static formula returning a quality
metric.

### Dynamic formulas — function composition

A dynamic formula takes other formulas' outputs as inputs:

```
emergence_health(...) =
    bearing_diversity(bearing_distribution())
  × charter_kpi_progress(active_charters)
  × manifest_signing_coverage(recent_manifests)
  × (1 - charter_creep_penalty(active_count, max=15))
```

The composition means:
- Output of one formula → input to another
- Late binding: a formula's value at time T can depend on a
  formula's value at time T-Δ (history-aware)
- Recursive: a formula can call itself with reduced scope (probe a
  subtree)

The `_formulas.py` registry (`scripts/_formulas.py` + the
`swarmy_formula` MCP verb dispatcher) is the canonical home today.
Each formula has a slug, a target value, a computation function, and
optional dependencies on other formulas.

## How formulas fit shapes

**Shapes COUNT, formulas COMPUTE.** They compose:

| Shape | Formula derived from it |
|---|---|
| `mcp.tools.granular` (count of granular MCP tools) | `formula:mcp_consolidation_index = 1 - count/baseline` |
| `manifest.signed_by.missing` (count of unsigned manifests) | `formula:signing_coverage = 1 - count/total_manifests` |
| `charter.active.count` (count of active charters) | `formula:charter_creep_pressure = max(0, count - cap) / cap` |
| `manifest.discovered_work.entries` (count) | `formula:discovery_rate = count_today / count_yesterday` |

A shape detector returns a count. A formula transforms counts (and
other formulas' outputs) into bounded scores [0, 1] suitable for
mutation classification.

The shape registry (proposed `_meta/shapes.json`) + the formula
registry (`scripts/_formulas.py`) together form the complete
measurement layer:
- Shapes count instances
- Formulas score health
- Formulas compose to produce composite indices

## How formulas fit RAP / mutation assessment

A formula returning `[0, 1]` is the **target** of a mutation. Each
RAP cut declares which formula it intends to move:

```json
{
  "cut": 3,
  "target_formula": "mcp_consolidation_index",
  "baseline_formula_value": 0.0,        // (85/85 = no consolidation yet)
  "shape_baseline": {"mcp.tools.granular": 85},
  "expected_direction": "increase",
  "new_state_formula_value": 0.118,     // ((85-75)/85 = 11.8% reduction)
  "shape_new_state": {"mcp.tools.granular": 75},
  "delta": +0.118,
  "verdict": "beneficial",
  "verdict_confidence": 0.95
}
```

Now the verdict has a NUMBER attached. Across many cuts, the
formula's trajectory tells the system's evolution story
quantitatively.

## How formulas fit evolution

The genetic-drift charter pressure model assumes:
- Beneficial mutations propagate (the protocol is canonized)
- Harmful mutations roll back (the protocol is rejected)
- Neutral mutations accumulate (no pressure, may be pruned later)

**Without formulas:** these classifications are subjective.

**With formulas:** the classification is:

```
mutation.verdict = case
  delta > +ε AND target_direction_aligned → beneficial
  abs(delta) < ε                          → neutral
  delta > +ε AND target_direction_violated → harmful
  formula_compute_failed                   → uncertain
```

Where `ε` is a configured noise threshold per formula. Pressure
becomes mechanical: when a beneficial mutation pattern recurs N
times across cuts, propose canonization (charter the protocol);
when a harmful mutation pattern recurs N times, propose moratorium.

## How formulas fit membench

Membench probes ARE formulas with measurement-time semantics:

```
membench_probe(name, system_state) → score [0, 1]
```

Each probe = a formula (often dynamic, composing several
shape-counts + base formulas). The aggregate health = a higher-order
formula composing the probes.

Today's probes (per `scripts/3x_membench_probes.py`):
- `decision_findable` — % of recent decisions discoverable from
  forensics in <60s
- `cold_orientation` — does a charter pass 60-second test
- `frontier_grok` — agent comprehension of recent manifests
- ... etc.

Each is a formula. Their composition into `emergence_health` is
also a formula (dynamic — uses each probe's output as input).

## The cross-domain composition

The killer property of formulas: they compose ACROSS domains.

```
swarm_vitality(t) =
    weighted_sum(
      0.3 × signing_coverage(t),
      0.2 × charter_progression_rate(t),
      0.2 × mission_emergence_rate(t),
      0.2 × consolidation_index(t),
      0.1 × cross_repo_alignment(t)
    )
```

A single number tells you: is the swarm healthy NOW? Trajectory of
this number over time tells you: is the swarm evolving healthily?

Mutations that move `swarm_vitality` up are the kind worth
canonizing. Mutations that move it down get rolled back. Mutations
that don't move it are noise.

## The interaction with mission emergence

When a SHAPE is recognized as a recurring pattern:
1. It gets a `cluster_prefix` (the mission's w3w address)
2. A shape DETECTOR is written (the count function)
3. A FORMULA is derived from the shape (the score function)
4. A charter forms when the shape converges enough to bound
5. Future agents in any repo carrying the shape consume the
   formula's protocol (the cross-repo mission propagation)

The formula is the bridge — it's WHERE the shape's count becomes
actionable. Without formulas, shapes are just numbers. With
formulas, shapes are MEASURED MISSIONS.

## What's wired today + what's missing

| Piece | State |
|---|---|
| Static formulas (`_formulas.py`) | ✅ shipped (formula_get/list/etc via swarmy_formula MCP) |
| `MetricRun` lifecycle | ✅ shipped (`_metric_lib.py`) |
| Membench probes | ✅ shipped (`3x_membench_probes.py` + `9x_membench_scorer.py`) |
| Formula composition via outputs-as-inputs | ⚠ partial (no formal DAG resolver) |
| Shape registry | ❌ not yet (open enhancement) |
| Shape→formula derivation | ⚠ implicit (each shape's formula is hand-written) |
| Cross-domain composition (vitality) | ❌ no top-level formula yet |
| Formula trajectory tracking | ⚠ per-metric in `forensics/eval/`; no formula-aware UI |
| Mutation verdict mechanical from formula delta | ⚠ classification exists; not wired to formula values |

The open enhancements are all small (no breaking changes; pure
additions). The biggest leverage:
1. `_meta/shapes.json` registry
2. `_meta/formulas.json` declaring which formulas compose into which
3. A `swarm-vitality` composite formula + a daily timeline view

## Single-line summary

**Shapes count, formulas compute (static) or compose
(dynamic = outputs-as-inputs). Together they ground every doctrine
(mission emergence, charter claim, mutation assessment, membench,
evolution) in real numbers. The cluster_prefix is the mission's
address; the shape is its essence; the formula is its measurement;
the verdict is its mutation classification — and the trajectory of
the formula over time is the system's evolution.**

---

*Closes the doctrine arc 08-14. Together they describe the COMPLETE
substrate for emergent missions + claimable charters + measured
mutations + cross-repo propagation. Open enhancements: shape registry
+ formula DAG resolver + swarm-vitality composite. Should fold into
Part 5 of `docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` (or its
own doc 46-FORMULAS-AS-MEASUREMENT-CANONICAL).*
