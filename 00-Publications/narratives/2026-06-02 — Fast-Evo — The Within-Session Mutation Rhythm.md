---
title: "Fast-Evo — The Within-Session Mutation Rhythm"
type: architecture-narrative
created: 2026-06-02
canonical_tier: { agents: true, humans: true }
tags: [f0, evolve, fast-evo, survey, measure-cut-measure, sandwich, gates, mutation-fitness]
mirror_of: "reckon/docs/151-FAST-EVO-CANONICAL.md"
pairs_with: ["150-GATES-VS-INSIGHT-CANONICAL", "survey/SKILL.md"]
---

# Fast-Evo — The Within-Session Mutation Rhythm

*A mutation is only as trustworthy as the measurement that brackets it. Fast-evo is
the within-session form of the measure-cut-measure sandwich: one agent, one context
window, baseline locked before the first cut, verdict before the context closes. It
feeds the gate — the gate cannot run without it.*

---

## The gap it closes

The slow/cross-session evolve cycle (days to weeks) is the canonical mutation pathway.
But it has a minimum latency: you cannot span sessions in a single context window. When
a bottleneck is small enough to fix right now — a single script, a config line, a
schema field — waiting for the cross-session cycle is pure drag. The agent sitting
inside the problem already holds the baseline state in live memory. The right move is:
lock the baseline, cut the change, re-measure, classify, and return the verdict in one
flight.

That is fast-evo. It is not a shortcut around the gate; it is the substrate the gate
reads. Without a fast-evo measurement cycle, there is no delta for the gate to
evaluate.

---

## The sandwich (measure-cut-measure)

Three steps, always in order:

**Baseline.** Lock the measurement before the change. If you skip this, the delta is
fiction.

**Cut.** Apply the smallest change that is testable. "Smallest" means one variable
changes; everything else holds. Two-variable cuts produce uninterpretable deltas — the
gate cannot assign causality.

**Re-measure.** Use the same instrument, same scope as the baseline. Compare the delta
to the noise threshold from the shape registry. Classify: beneficial / neutral /
harmful / uncertain.

The sandwich is not a documentation ritual. It is the only mechanism that produces a
trustworthy delta. A change without a baseline is an assertion, not a measurement;
assertions cannot pass gates; a gate that never fires is not a gate.

---

## Deep and wide in one window

Survey doctrine names two modes: **probe** (deep, one focus) and **sweep** (wide, N
disjoint lanes). Fast-evo is primarily a probe instrument — one variable at a time. But
a single context window often needs both modes. The pattern for both:

1. Lock a global baseline.
2. Run lanes in series (sweep), each with its own cut and re-measure.
3. Integrate: compare lane verdicts, resolve interactions, emit one manifest.

**Critical rule:** lanes must be truly disjoint. If lane B reads a file lane A writes,
serialize them or treat the whole thing as a single probe with sequential cuts. Parallel
lanes with shared state produce an uninterpretable combined delta.

The integrated manifest entry is what the gate reads. Per-lane entries are the audit
trail.

---

## Same six steps as slow-evolve — different clock speed

Fast-evo and slow-evolve are the same shape at different timescales:

| Step | Slow evolve | Fast-evo |
|---|---|---|
| Read state | `eval-dashboard` across prior sessions | current context holds the state |
| Identify candidate | `metrics_evolve` ranking | agent spots bottleneck directly |
| **Pre-register** | **charter block BEFORE mutation applied** | **`_evolution_log[]` entry in manifest, written first** |
| Apply | deploy to live system | apply in working context |
| Sandwich | `5a_baseline_capture` → sessions → `5b_measure_post` | baseline → cut → re-measure in one window |
| Classify + act | beneficial → LOCK IN + NECTAR; harmful → rollback | KEPT / ROLLED-BACK / REFUSED + manifest |

The pre-registration discipline is identical at both scales. You must predict before
you measure. A fast-evo `_evolution_log[]` entry written *after* the cut is a
post-hoc rationalization, not a measurement.

---

## What breaks the gate (and therefore the sandwich)

| Break | Effect |
|---|---|
| No baseline captured | delta is always beneficial. Gate fires blindly. |
| Two variables changed at once | delta attributed to wrong variable. Rollback cannot isolate harm. |
| Different instrument at re-measure | delta is instrument noise. Gate fires on noise. |
| Pre-reg written after the cut | no predictive record; cannot distinguish prediction from rationalization. |
| Lane isolation violated | beneficial lane A masks harmful lane B; both survive. |

---

## REFUSED is a first-class verdict

A fast-evo cycle that ends in refusal is not a failed cycle. The cycle succeeded in
identifying the work should not be done. The `_evolution_log[]` carries
`"verdict": "REFUSED"` with the lens that fired. The forensic record is complete. The
baseline was measured; the work was evaluated; the refusal is the crystallized
artifact.

---

## The operating rule

Lock the baseline before the first cut. One variable per lane. Write the pre-reg entry
before applying the mutation. Same instrument at baseline and re-measure.

KEPT / ROLLED-BACK / REFUSED are all legitimate terminal states.

If any rule is skipped, the delta is not a measurement — it is an assertion. Gates do
not run on assertions.
