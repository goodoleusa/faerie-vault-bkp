---
type: system-reference
title: Canonical Emergence Formulas
created: 2026-05-04
updated: 2026-05-18
tags: [emergence, formulas, faerie2, experimental, crystallized]
promotion_state: capture
source_path: "80-Publications/canonical-emergence-metrics.md"
source_hash: "sha256:721b4880d933f393994578923c7d437c99219cb81b03922f1e376b48dd17deb2"
doc_hash: "sha256:"
hash_ts: 2026-05-18T00:00:00Z
hash_method: body-sha256-v1
cloud_path: ""
promoted_to: ""
promoted_at: ""
---

> [↑ Dashboards](../../Dashboards.md) · [⌂ Hive](../Hive.md)

# Canonical Emergence Formulas — Live Experimental Document

**Status:** Crystallized (HONEY.md mth00420-422)  
**Confidence:** 0.70 (validated Phase C; 2nd charter pending)  
**Last Updated:** 2026-05-04  

These formulas are the **lived-in theory** of how faerie2 orchestrates agent emergence. They feed back into themselves; each formula's output becomes input to the next, creating a self-reinforcing system.

---

## Core Formula: FFMx (Focused Force Multiplier)

**The Self-Referential Formula** — Agent chains inherit all ancestor context, compounding exponentially.

```
FFMx = (A × Q × E^1.5) / T
```

**Components:**
- **A** = artifact count (manifests written by all agents)
- **Q** = quality (average agent confidence in outputs: 0.0–1.0)
- **E** = emergence depth (monkeybranching: how many generations of agents spawned?)
- **k = 1.5** = emergence exponent (each generation doesn't just add; it **compounds**)
- **T** = tokens burned (total context consumed)

**Result:** Dimensionless efficiency scalar (manifests per token, weighted by quality & depth)

**Empirical baseline:** FFMx = 44.4 (measured 2026-04-21 to 2026-04-28)  
**Success threshold:** FFMx_post / FFMx_pre ≥ 1.5 (50% improvement)

---

## Why E^1.5 (The Self-Referential Part)

**The insight:** Agent monkeybranching depth doesn't add linearly; it compounds.

```
Depth 1: 1 agent
  → Contribution = 1.0

Depth 2: 1 agent → 1 child agent
  → Each child inherits parent's manifest (context inheritance)
  → Problem decomposition multiplies
  → Contribution = 2^1.5 = 2.83×

Depth 3: 1 agent → 1 child → 1 grandchild
  → Grandchild reads parent + grandparent manifests
  → Context inheritance: 3 manifests worth of context
  → Contribution = 3^1.5 = 5.20×

Depth 4: Agent D reads manifests from A, B, C (ancestors)
  → Contribution = 4^1.5 = 8.00× (quadratic-ish growth)
```

**The self-reference:** Each agent's output becomes the next agent's input. There's no external "emergence generator"—the system bootstraps from agent chains reading manifests and spawning follow-ups.

**Empirical grounding:** k=1.5 is calibrated from Phase C sessions. If k=1.0 (linear), deep chains wouldn't be rewarded enough. If k=2.0 (quadratic), noise would amplify. The Goldilocks point is k=1.5.

---

## Quality Gate: Citation Density

**Formula:**
```
citation_density = manifests_with_cross_citations / total_manifests
```

**Range:** 0.0–1.0

**Threshold:** ≥ 0.30 (PASS), 0.20–0.29 (CAUTION), < 0.20 (FAIL)

**Interpretation:**
High citation density = agents read prior manifests and reference them in discovered_work. This is the **direct measurement of stigmergy working**. Low citation density = agents spawning independently (no knowledge transfer).

**In dashboard:**
- Green ≥ 0.30 (strong emergence signal)
- Yellow 0.20–0.29 (weak emergence)
- Red < 0.20 (isolation mode, broken discovery)

---

## Quality Gate: Brittleness

**Formula:**
```
brittleness = (W_ratio × 0.60) + (baseline_test_gap × 0.25) + (evidence_quality_delta × 0.15)
```

**Components:**
- **W_ratio** = west-bearing manifests / total manifests (higher = more backtracking/re-validation)
- **baseline_test_gap** = how far assumptions diverge from baseline upon testing (0–1)
- **evidence_quality_delta** = belief_index variance (uncertainty in reporting)

**Threshold:** < 0.40 (PASS), 0.40–0.54 (CAUTION), ≥ 0.55 (FAIL)

**Interpretation:**
Low brittleness = solid assumptions, minimal backtracking, confident discovery. High brittleness = agents constantly re-validating (W-edges), suggesting fragile assumptions.

**In dashboard:**
- Green < 0.40 (assumptions holding)
- Yellow 0.40–0.54 (expected backtracking during deep work)
- Red ≥ 0.55 (foundational issues, design needs rework)

---

## Quality Gate: Downstream Impact

**Formula:**
```
downstream_impact = N_edges_resolved / total_N_edges_discovered
```

**Components:**
- **N_edges_resolved** = north-bearing tasks that were unblocked (prerequisite work completed)
- **total_N_edges_discovered** = all north-bearing tasks identified in session

**Threshold:** ≥ 0.60 (PASS), 0.40–0.59 (CAUTION), < 0.40 (FAIL)

**Interpretation:**
High downstream impact = agent work unblocks other agents (north-edge resolution). This is how missions parallelize. Low impact = agents finishing work that doesn't help downstream.

**In dashboard:**
- Green ≥ 0.60 (unblocking productive)
- Yellow 0.40–0.59 (some unblocking, but gaps)
- Red < 0.40 (work is isolated, not enabling others)

---

## Synthesis: Per-Archetype Emergence

**Formula:**
```
archetype_balance = correlation(
  NAVIGATOR_score,
  MAKER_score,
  BRIDGE_score,
  DEEP_DIVER_score
)
```

**Range:** 0.0–1.0 (perfect correlation = all archetypes equally strong)

**Threshold:** ≥ 0.75 (PASS), 0.60–0.74 (CAUTION), < 0.60 (FAIL)

**Interpretation:**
Balanced emergence means all four cognitive archetypes (navigator, maker, bridge, deep-diver) contribute roughly equally. If correlation < 0.75, one archetype is bottlenecking (e.g., all ships are blocked by missing north-edge unblocking).

**In dashboard:**
- Green ≥ 0.75 (all archetypes firing)
- Yellow 0.60–0.74 (one archetype lagging)
- Red < 0.60 (severe imbalance; single-archetype bottleneck)

---

## Membench Bridge: What Metrics Predict Emergence

| Metric | Formula | What It Predicts | Link to Emergence |
|--------|---------|------------------|-------------------|
| **M1** | HONEY retention % | Citation density will rise/fall | High M1 → high citations next session |
| **M3** | Tasks / 100k tokens | FFMx will rise/fall | High M3 → FFMx trending up (efficient shipping) |
| **M4** | Discovery coverage % | Downstream impact will rise/fall | High M4 → N-edges unblocked (down-stream payload) |
| **M6** | Bearing diversity entropy | Per-archetype balance | High M6 → balanced bearing distribution |
| **M7** | Cross-citation index | Brittleness will improve | High M7 → agents reading + learning (lower brittleness) |
| **M11** | HONEY usage % | Emergence trajectory | High M11 → crystallized knowledge driving emergence |

**The bridge:** These membench metrics are **leading indicators** of emergence. When M1 drops, expect citation_density to drop 1–2 sessions later. When M3 rises, FFMx improvement follows.

---

## Session Health Narrative: What Good Looks Like

**High-emergence session:**
- FFMx > 44.4 baseline
- Citation density ≥ 0.30 (agents reading manifests)
- Brittleness < 0.40 (assumptions holding)
- Downstream impact ≥ 0.60 (N-edges resolved)
- Per-archetype balance ≥ 0.75 (no bottleneck)
- M3 > 1.10, M11 > 70%

**Low-emergence session:**
- FFMx < 44.4
- Citation density < 0.20 (isolated agents)
- Brittleness > 0.54 (constant backtracking)
- Downstream impact < 0.40 (work doesn't unblock)
- Per-archetype balance < 0.60 (one archetype stuck)
- M3 < 1.0, M11 < 50%

---

## Integration with /dev-eval Dashboard

The /dev-eval vault dashboards **consume these formulas** and render them as:

1. **Timeline Events** correlating emergent moments to metric shifts
2. **Root Cause Analysis** explaining why FFMx moved based on Q/E/A/T components
3. **Lessons Learned** extracting what worked and why
4. **Failures→Gold** converting low-emergence moments into insights

**Example:** "At T+32min, citation_density jumped from 0.18 to 0.34 (>0.30 threshold). Root cause: gauge updater manifest landed, presend began reading real-time signals. Agents now had better routing info → higher cross-citations. FFMx impact: +8% throughput improvement predicted for next session."

---

## Crystallized Methods (HONEY.md)

These formulas are locked in HONEY.md as:

- **mth00420:** FFMx formula (A × Q × E^1.5 / T) — self-referential emergence amplification
- **mth00421:** Quality gates (citation, brittleness, impact) — local emergence health triad
- **mth00422:** Per-archetype balance — emergence bottleneck detection

All three are **confidence 0.70** (empirically validated Phase C; awaiting 2nd charter for promotion to 0.85).

---

## Failure Modes & Debugging

| Symptom | Root Cause | Action |
|---------|-----------|--------|
| FFMx low, A high | Quality Q is poor | Audit manifest quality_score fields; retrain agents |
| FFMx low, Q high | Emergence depth E shallow | Agents not spawning follow-ups; check discovery protocol |
| Citation density < 0.20 | Agents not reading manifests | Verify frontier scan is wired; check agent prompts |
| Brittleness > 0.54 | High W-ratio (constant backtracking) | Design has fragile assumptions; do assumption validation sprint |
| Downstream impact < 0.40 | N-edges not resolved | North-bearing tasks blocked; review blockers, increase UNBLOCK bearing spawns |
| Archetype balance < 0.60 | One archetype bottleneck | Identify lagging archetype; review presend routing; increase that type's spawns |

---

## References

- **FFMX-EQUATION-SPECIFICATION.md** (this vault, forensics/) — Full technical spec with code
- **membench-emergence-bridge.md** (repo docs/) — How membench metrics correlate to emergence
- **emergence-quality-metrics-system-20260503.md** (this vault, Hive/) — System design & 6-gate framework
- **mth00420–422** (HONEY.md) — Crystallized methods
- **CLAUDE.md** — Release Readiness Gates (6 gates, all must PASS for v2.0)

---

**This document lives alongside /dev-eval dashboards. Every session's eval report should reference these formulas when explaining why metrics moved.**

