---
title: Archetype Role Stability — 2nd Charter Validation Framework
date: 2026-05-03
tags: [archetype-validation, measurement-framework, emergence-health, mutation-discipline, 2nd-charter-prep]
mission: mutation-archetype-2nd-charter-prep
status: active
document_type: measurement-framework
confidence_baseline: 0.70
---

# Archetype Role Stability — 2nd Charter Validation Framework

**Purpose:** Define how cognitive archetypes are measured, validated, and crystallized across 2+ charter sessions. This framework ensures archetype roles hold stable across missions (n ≥ 2 requirement for promotion to HONEY confidence 0.80+).

**Timeline:** 2026-05-04 to 2026-05-10 (~5–7 days)

**Success metric:** Archetype roles are stable (correlation >0.75 across missions) → promote to HONEY confidence 0.80+

**Failure metric:** Archetype roles are mission-adaptive → roster becomes per-mission selection model

---

## Why 2nd Charter Validation is Required

### Single-Charter Insufficiency (n=1 Problem)

The first emergence loop (2026-05-03) validated the **formula** for emergence health:

```
emergence_health = (edge_density × 0.35) + (clustering_coeff × 0.30) + (linearity × 0.25) + ((1 - W_ratio) × 0.10)

mth00407: confidence 0.92 (n=1, formula predicted 0.87, observed 0.87)
```

But the formula doesn't validate **archetype role stability**. The formula says:

> "When all four archetypes are present, emergence ≥0.87. Each archetype contributes differently: NAVIGATOR→edge_density, BRIDGE→clustering, DEEP-DIVER→linearity, MAKER→low W_ratio."

**What n=1 proves:**
- The formula prediction was correct for that specific mission
- The archetype assignments matched observed component contributions
- The roster (NAVIGATOR+MAKER+BRIDGE+DEEP-DIVER, 6 agents total) produced emergent health ≥0.87

**What n=1 does NOT prove:**
- Whether archetype roles are **consistently** assigned the same cognitive task across different missions
- Whether the same agent pairing (primary + secondary) works across mission types
- Whether archetype roles are **universal** (true across all charters) or **mission-adaptive** (must change per mission type)
- Whether emergence health >0.87 is repeatable (or was that session lucky?)

### The Crystallization Gate (n ≥ 2)

Per HONEY.md and charter-crystallization-rules.md:

> "Promote a pattern to HONEY method when ALL of the following are true:
> 1. Repeatability — pattern appeared in 2+ charter sessions
> 2. Generalizability — pattern applies across charter types
> 3. Novelty — not already captured in existing HONEY entry
> 4. Actionability — agent can apply mechanically in future session"

**Archetype role stability is a pattern.** After n=1 (emergence loop), it's a **candidate method (confidence 0.70)**, not yet crystallized. The 2nd charter will test:

1. **Repeatability:** Do the same archetypes produce the same component contributions across 2 different missions?
2. **Generalizability:** Do archetype roles hold for mission types other than "emergence loop" (e.g., publication, audit, integration)?
3. **Coherence:** Are the archetype + agent pairings (NAVIGATOR=research-analyst+evidence-analyst, etc.) stable, or does each mission need different pairings?

---

## Archetype Role Definitions

### NAVIGATOR Archetype
**Cognitive pattern:** Frontier scanning, edge discovery, routing signals

**Manifest signal:** `edge_density` component
- Writes manifests with discovered_work[] entries pointing to unblocked tasks
- Scans mission frontiers, identifies N/S/E/W bearings
- Low edge_density when NAVIGATOR is absent/weak; high when present

**Agent roles:**
- Primary: **research-analyst** — reads manifests, scans evidence, compiles frontier intelligence
- Secondary: **evidence-analyst** — validates assumptions, confirms discovered work is real (not hallucinated)

**Success measure for 2nd charter:** edge_density ≥0.65 (same or better than emergence loop baseline 0.70)

---

### BRIDGE Archetype
**Cognitive pattern:** Cross-domain synthesis, mission clustering, coherence

**Manifest signal:** `clustering_coeff` component
- Groups related work within mission; identifies sister tasks (E-edges)
- Writes manifests with high inter-mission coherence signals
- Low clustering when BRIDGE is absent; high when present

**Agent roles:**
- Primary: **knowledge-synthesizer** — cross-references discoveries, identifies patterns, bridges silos
- Secondary: **documentation-engineer** — writes coherence-maintaining docs, ensures domain transitions are clear

**Success measure for 2nd charter:** clustering_coeff ≥0.75 (same or better than emergence loop baseline 0.82)

---

### DEEP-DIVER Archetype
**Cognitive pattern:** Assumption validation, bearing legality, DAG structure enforcement

**Manifest signal:** `linearity` component
- Validates compass bearing chains (no illegal progressions like S→N or W→S)
- Writes manifests that maintain DAG topology
- Low linearity when DEEP-DIVER is absent; high when present

**Agent roles:**
- Primary: **security-auditor** — verifies assumptions, tests edge cases, validates foundations
- Secondary: **evidence-analyst** — provides rigorous backing, filters hallucinations

**Success measure for 2nd charter:** linearity ≥0.90 (same or better than emergence loop baseline 0.94)

---

### MAKER Archetype
**Cognitive pattern:** Execution, parallel shipping, backtrack minimization

**Manifest signal:** `1 - W_ratio` component (inverse)
- Ships work efficiently, avoids unnecessary backtracking
- Writes manifests with low W-edge density (<5%)
- High W_ratio when MAKER is absent/weak; low when present

**Agent roles:**
- Primary: **python-pro** — fast shipping, artifact generation, iteration
- Secondary: **fullstack-developer** — integration, end-to-end delivery, shipping coherence

**Success measure for 2nd charter:** W_ratio ≤0.05 (same or better than emergence loop baseline 0.038)

---

## Measurement Metrics (Per-Archetype, Per-Mission)

### 1. **Edge Density (NAVIGATOR Validation)**

**Formula:**
```
edge_density = (sum of discovered_work[] entries per manifest) / (total manifests)
```

**How to measure:**
1. Count all discovered_work[] entries across all manifests in the mission
2. Divide by total manifest count
3. Record as: `{manifest_id: X, edge_count: N, edge_density: N/X}`

**Target range:** 0.65–0.80 (indicates NAVIGATOR is actively discovering unblocked work)

**Data source:** All manifest files written during mission, especially those with NAVIGATOR + agent pairings

**Red flag:**
- edge_density < 0.50 (NAVIGATOR not discovering; agents working in isolation)
- Manifests written by NAVIGATOR agents but discovered_work[] is empty (frontier scanning broken)

---

### 2. **Clustering Coefficient (BRIDGE Validation)**

**Formula:**
```
clustering_coeff = (number of interconnected mission sub-clusters) / (total mission clusters)

Operationally:
- Identify all tasks in mission
- Group by mission field + compass bearing (N-cluster, S-cluster, E-cluster, W-cluster)
- Count how many of these 4 clusters have inter-cluster E-edges
- clustering_coeff = inter-cluster connections / possible connections
```

**How to measure:**
1. Parse all discovered_work[] entries, filter by mission
2. Build a graph: nodes = tasks, edges = discovered_work[] connections
3. Identify clusters (nodes reachable via compass edges within same bearing)
4. Count E-edges that cross clusters (sister work at same level)
5. Record as: `{mission: X, clusters: N, cross_edges: K, clustering_coeff: K/(N*(N-1)/2)}`

**Target range:** 0.70–0.85 (indicates BRIDGE is maintaining mission cohesion)

**Data source:** All discovered_work[] entries, especially those with BRIDGE + agent pairings

**Red flag:**
- clustering_coeff < 0.60 (work scattered, no coherent mission blocks)
- E-edges are sparse despite parallel work opportunities (BRIDGE not identifying sister tasks)

---

### 3. **Linearity (DEEP-DIVER Validation)**

**Formula:**
```
linearity = (legal bearing chains) / (total bearing chains)

Legal chains:
- N → {N, S, E, W}
- S → {S, E, W}
- E → {E, S, W, N}
- W → {W, N, E}

Illegal chains:
- S → N (can't un-conclude and go back to unblocking)
- W → S (can't conclude after backtrack without baseline re-seat)
- Cycles (X → Y → X)
```

**How to measure:**
1. Extract all bearing chains from discovered_work[] entries
2. Validate each chain against legal progression rules
3. Count legal vs total
4. Record as: `{mission: X, total_chains: N, legal_chains: K, linearity: K/N}`

**Target range:** 0.90–0.98 (strict DAG enforcement, DEEP-DIVER is validating)

**Data source:** All discovered_work[] entries with bearing fields, graph topology validation

**Red flag:**
- linearity < 0.85 (bearing rules not enforced; DEEP-DIVER validation weak)
- Any S→N chains found (indicates confused bearing logic)
- Cycles detected (topological sort fails, deadlock risk)

---

### 4. **W-Ratio (MAKER Validation)**

**Formula:**
```
W_ratio = (count of W-bearing edges) / (total edges)
health_component = 1 - W_ratio
```

**How to measure:**
1. Count all discovered_work[] entries with bearing="W"
2. Count total edges
3. Compute W_ratio
4. Record as: `{mission: X, total_edges: N, W_edges: K, W_ratio: K/N, health_impact: 1 - K/N}`

**Target range:** 0.02–0.05 (low backtrack, MAKER is shipping efficiently)

**Data source:** All discovered_work[] entries with bearing field

**Red flag:**
- W_ratio > 0.10 (more than 10% backtrack = mission regression, assumptions failing)
- Clustering of W-edges (same task being revisited multiple times = cascade failure)

---

## Cross-Charter Stability Measures

**After 2 charters, compute correlation:**

```
For each archetype A:
  - Chart: component_contribution[A] vs mission
  - Correlation: corr(component_1st_charter, component_2nd_charter)
  - Threshold: correlation ≥ 0.75 = role is stable (universal)
  - If < 0.75: role is mission-adaptive (must select differently per mission)
```

**Example (NAVIGATOR):**
```
Charter 1 (emergence loop):
  - edge_density: 0.70
  - NAVIGATOR agents: research-analyst + evidence-analyst
  - Contribution: NAVIGATOR was active frontier scanner

Charter 2 (new mission, TBD):
  - edge_density: ?
  - NAVIGATOR agents: research-analyst + evidence-analyst
  - Contribution: if ≥0.65 and bearing-discovery pattern matches → role is stable
```

**Correlation logic:**
- Stable (corr > 0.75): archetype role is universal → promote to HONEY (confidence 0.80+)
- Unstable (corr 0.50–0.75): archetype role is mission-adaptive → keep candidate (confidence 0.70), run 3rd charter
- Broken (corr < 0.50): archetype roles don't hold → revert to per-mission selection model

---

## Archetype Pairing Stability

**Primary + Secondary pairing validation:**

Current LIFTOFF ROSTER (locked 2026-05-03):

| Archetype | Primary | Secondary |
|-----------|---------|-----------|
| NAVIGATOR | research-analyst | evidence-analyst |
| MAKER | python-pro | fullstack-developer |
| BRIDGE | knowledge-synthesizer | documentation-engineer |
| DEEP-DIVER | security-auditor | evidence-analyst |

**Pairing hypothesis for 2nd charter:**
- Same archetype pairings work across mission types
- Primary agent carries the archetype's cognitive load
- Secondary agent provides validation/backing

**How to test:**
1. Assign same primary+secondary pairings in 2nd charter
2. Observe agent manifest patterns (does primary write high-quality discovered_work[]? does secondary validate?)
3. If patterns match emergence loop → pairings are stable (confidence 0.85)
4. If patterns differ → pairings may be mission-dependent (reclassify as adaptive, confidence 0.65)

**Red flag:**
- Primary agent writes shallow manifests (low quality)
- Secondary agent never validates / rare secondary contributions
- Pairing swaps needed mid-mission for performance

---

## Timeline: 2nd Charter (2026-05-04 to 2026-05-10)

### Phase 0: Pre-Charter (2026-05-03 EOD)
- [ ] Finalize this measurement framework (done)
- [ ] Create charter with archetype assignment + expected metrics
- [ ] Pre-register hypothesis: "archetype roles will correlate >0.75 across missions"
- [ ] Baseline metrics file created: `forensics/archetype-baseline-charter-2.json`

### Phase 1: Charter Execution (2026-05-04 to 2026-05-07, ~3–4 days)
- [ ] Spawn W1 with same archetype roster (NAVIGATOR+MAKER+BRIDGE+DEEP-DIVER, 6 agents)
- [ ] Agents write manifests with full discovered_work[] discovery
- [ ] Record all manifests to `forensics/{date}/` with mission field
- [ ] Daily dashboard: edge_density, clustering_coeff, linearity, W_ratio tracking

### Phase 2: Post-Charter Measurement (2026-05-08 to 2026-05-09)
- [ ] Extract all discovered_work[] entries from charter
- [ ] Compute per-archetype component contributions
- [ ] Compute correlations vs. charter 1 baseline
- [ ] Write measurement report to `forensics/archetype-measurement-charter-2.json`
- [ ] Evaluate: stable (corr > 0.75) or adaptive (corr < 0.75)?

### Phase 3: Crystallization Decision (2026-05-10)
- **If stable (corr ≥ 0.75):**
  - Promote to HONEY.md: `[mth00425 | method | 1yr | 0.80]` Archetype role stability (2/2 charters, high correlation)
  - Liftoff roster locked to HONEY (confidence raised from 0.70 to 0.80+)
  - Document: archetype roles are universal across mission types
  
- **If unstable (corr 0.50–0.75):**
  - Keep as NECTAR candidate (confidence remains 0.70)
  - Note: archetype roles are mission-adaptive
  - Plan 3rd charter with different mission type to test generalizability
  
- **If broken (corr < 0.50):**
  - Revert: roster becomes mission-adaptive model
  - Each mission selects archetype agents based on frontier analysis
  - Confidence: 0.55 (failed validation)

---

## Success Criteria (KPIs for 2nd Charter)

**All metrics must be GREEN for validation to pass:**

| Metric | Target | Threshold | Status |
|--------|--------|-----------|--------|
| **edge_density** | 0.65–0.80 | ≥0.60 | TBD (measure during charter) |
| **clustering_coeff** | 0.70–0.85 | ≥0.65 | TBD |
| **linearity** | 0.90–0.98 | ≥0.85 | TBD |
| **W_ratio** | 0.02–0.05 | ≤0.10 | TBD |
| **emergence_health** | ≥0.87 | ≥0.85 | TBD |
| **archetype_correlation** (vs charter 1) | ≥0.75 | ≥0.70 | TBD |
| **charter_duration** | ≤7 days | ≤10 days | TBD |

**Outcome:**
- All GREEN → promote to HONEY (confidence 0.80)
- 1–2 YELLOW (threshold met, target missed) → NECTAR candidate (confidence 0.70)
- Any RED → revert to adaptive model (confidence 0.55)

---

## Confidence Trajectory

### Starting Point (2026-05-03)

```
mth00407 (emergence formula): confidence 0.92, n=1
mth00425 (archetype roles, CANDIDATE): confidence 0.70, n=1
```

**Rationale:** Formula validated. Archetype assignments observed. But repeatability not yet tested.

### After 2nd Charter (2026-05-10, TBD)

**Scenario A: Stable (corr ≥0.75)**
```
mth00425 (archetype roles, VALIDATED): confidence 0.80, n=2
Evidence: 2/2 charters with consistent component contributions; correlation ≥0.75
Next step: Use in future charters with high confidence
```

**Scenario B: Unstable (corr 0.50–0.75)**
```
mth00425 (archetype roles, INCONCLUSIVE): confidence 0.70, n=2
Evidence: 2 charters show mission dependency; correlation 0.50–0.75
Next step: Run 3rd charter with different mission type; refine archetype selection model
```

**Scenario C: Broken (corr < 0.50)**
```
mth00425 (archetype roles, FAILED): confidence 0.55, n=2
Evidence: 2/2 charters show different role patterns; no universal model
Next step: Switch to per-mission archetype selection; catalog mission-specific pairings
```

---

## Mutation Discipline: Baseline & Measurement

**Baseline (locked 2026-05-03):**
```json
{
  "charter": "emergence-loop-2026-05-03",
  "archetype_roles": {
    "NAVIGATOR": {
      "component": "edge_density",
      "value": 0.70,
      "primary_agent": "research-analyst",
      "secondary_agent": "evidence-analyst"
    },
    "BRIDGE": {
      "component": "clustering_coeff",
      "value": 0.82,
      "primary_agent": "knowledge-synthesizer",
      "secondary_agent": "documentation-engineer"
    },
    "DEEP_DIVER": {
      "component": "linearity",
      "value": 0.94,
      "primary_agent": "security-auditor",
      "secondary_agent": "evidence-analyst"
    },
    "MAKER": {
      "component": "W_ratio_inverse",
      "value": 0.962,
      "primary_agent": "python-pro",
      "secondary_agent": "fullstack-developer"
    }
  },
  "emergence_health": 0.97
}
```

**Measurement point (2026-05-10, to be filled):**
```json
{
  "charter": "second-charter-TBD-2026-05-04-to-05-10",
  "archetype_roles": {
    "NAVIGATOR": {
      "component": "edge_density",
      "value": null,
      "correlation_vs_baseline": null
    },
    "BRIDGE": {
      "component": "clustering_coeff",
      "value": null,
      "correlation_vs_baseline": null
    },
    "DEEP_DIVER": {
      "component": "linearity",
      "value": null,
      "correlation_vs_baseline": null
    },
    "MAKER": {
      "component": "W_ratio_inverse",
      "value": null,
      "correlation_vs_baseline": null
    }
  },
  "emergence_health": null,
  "stability_verdict": null,
  "confidence_promotion": null
}
```

---

## References

- **mth00407:** Emergence formula validated (edge_density, clustering, linearity, W_ratio; n=1)
- **mth00406:** Emergence health floor ≥0.80; alert on delta <-0.05
- **charter-crystallization-rules.md:** n ≥ 2 requirement for HONEY promotion
- **LIFTOFF ROSTER:** Canonical archetype assignment (locked 2026-05-03)
- **EMERGENCE-FORMULA-NARRATIVE.md:** Component breakdown and evidence

---

## Document Status

- **Version:** 1.0
- **Created:** 2026-05-03
- **Status:** ACTIVE (measurement framework ready for 2nd charter)
- **Next review:** 2026-05-10 (post-measurement)
- **Owner:** documentation-engineer (mutation discipline)
- **Confidence:** This framework itself is 0.88 (based on prior session emergence patterns and crystallization rules)
