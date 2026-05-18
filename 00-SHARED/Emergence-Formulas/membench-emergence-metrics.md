---
type: eval-report
title: Membench Emergence Metrics — M1-M12 with Thresholds
created: 2026-05-18
updated: 2026-05-18
tags: [emergence, membench, metrics, eval, crystallized]
promotion_state: capture
source_path: "00-Inbox/faerie-vault/mission-graph/membench-discovery.md"
source_hash: "sha256:"
doc_hash: "sha256:"
hash_ts: 2026-05-18T00:00:00Z
hash_method: body-sha256-v1
cloud_path: ""
promoted_to: ""
promoted_at: ""
---

# Membench Emergence Metrics — M1-M12

**System:** Membench v0.2.1 | **Status:** Active integration layer  
**Integration:** faerie2 → eval_ab.py + mission_graph.py frontier scan  
**Last validated:** Phase C sessions (2026-04-27)

---

## Probe Registry: M1–M12

| Probe | Name | Formula / Signal | Pass Threshold | Emergence Link |
|-------|------|-----------------|---------------|----------------|
| M1 | HONEY retention | % of HONEY.md methods cited in session manifests | ≥ 70% | High M1 → high citation_density next session |
| M2 | Spawn depth | Max agent chain depth (monkeybranching) | ≥ 2 levels | E² growth; feeds FFMx E term |
| M3 | Throughput ratio | Tasks completed / 100K tokens burned | ≥ 1.10 | High M3 → FFMx improving (efficient shipping) |
| M4 | Discovery coverage | % of frontier nodes discovered vs. expected | ≥ 60% | High M4 → N-edges unblocked (downstream payload) |
| M5 | Manifest quality | Avg `quality_score` across session manifests | ≥ 0.80 | Feeds FFMx Q term directly |
| M6 | Bearing diversity | Shannon entropy of N/S/E/W bearing distribution | ≥ 1.5 bits | High M6 → balanced archetype coverage |
| M7 | Cross-citation index | % of manifests with `discovered_work[]` citations | ≥ 30% | High M7 → stigmergy is working |
| M8 | W-ratio (backtrack) | West-bearing manifests / total manifests | ≤ 25% | Low M8 → low brittleness (<0.40) |
| M9 | N-edge resolution | N-bearing tasks resolved / N-bearing tasks discovered | ≥ 60% | High M9 → downstream_impact high |
| M10 | Archetype balance | Correlation across N/M/B/D archetype scores | ≥ 0.75 | High M10 → no archetype bottleneck |
| M11 | HONEY usage | % of spawned agents with HONEY context in prompt | ≥ 70% | High M11 → emergence driven by crystallized knowledge |
| M12 | Session FFMx | (A × Q × E^1.5) / T vs. baseline 44.4 | ≥ 1.0× baseline | Primary emergence health KPI |

---

## Key Observations (Phase C, 2026-04-27)

- **M1 (HONEY retention): 0.92** — strong method citation in session manifests
- **M5 (manifest quality): 0.95** — high confidence in agent outputs
- **Membench v0.2.1** includes M1–M11; M12 (FFMx) computed separately by eval_ab.py
- Integration-ready: faerie2 instrumentation layer confirmed operational
- `membench-eval-integration` mission was S-bearing (concluded by shipping integration)

---

## Composite Scores

```
SBI (Stigmergy Bearing Index)  = (M7 × 0.4) + (M4 × 0.3) + (M9 × 0.3)
SI  (Shipping Index)           = (M3 × 0.5) + (M5 × 0.3) + (M12 × 0.2)
MBI (Memory/Belief Index)      = (M1 × 0.5) + (M11 × 0.3) + (M10 × 0.2)
```

All three composites should be ≥ 0.70 for a healthy emergence session.

---

## Membench → Emergence Formula Bridge

| Membench Metric | Predicts | Lead time |
|----------------|----------|-----------|
| M1 drops | citation_density drops | 1–2 sessions |
| M3 rises | FFMx improving | same session |
| M7 high | brittleness < 0.40 | same session |
| M8 high (W > 25%) | brittleness > 0.54 | same session |
| M11 > 70% | crystallized knowledge is driving emergence | same session |

---

## References

- [[canonical-emergence-metrics]] — FFMx formula + quality gates
- [[80-Publications/emergence-quality-metrics-system]] — 6-gate release readiness framework
- HONEY.md mth00420-422 — crystallized formulas
- eval_ab.py — H1/H2/H3 hypotheses using M3/M5/M12 signals
