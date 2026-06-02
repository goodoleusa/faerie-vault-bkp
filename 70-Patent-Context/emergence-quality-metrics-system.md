---
type: system-design
title: "Emergence Quality Metrics + Membench Bridge System"
created: 2026-05-03
updated: 2026-05-18
tags: [emergence, quality-gates, membench, evaluation, release-readiness]
promotion_state: capture
source_path: "vault-native"
source_hash: "sha256:61966ddaf9d1829d1b0addaef85e0dedd405082f90757f0ee8e2194671b9c486"
doc_hash: "sha256:"
hash_ts: 2026-05-18T00:00:00Z
hash_method: body-sha256-v1
cloud_path: ""
promoted_to: ""
promoted_at: ""
---

# Emergence Quality Metrics + Membench Bridge System

**Date:** 2026-05-03 | **Status:** Final | **Confidence:** 0.87

This document synthesizes the complete system for measuring emergence quality in faerie2, connecting local manifest-based metrics to global membench observations, and establishing release readiness gates.

---

## Part 1: System Overview

### Three Scoring Layers

The system operates at three nested scopes:

1. **Local Layer (per-session):** Quality gates + per-archetype emergence (computed from manifests in `forensics/{date}/`)
2. **Global Layer (multi-session):** Membench M1-M11 + emerging M12-M15 metrics (historical trends)
3. **Release Layer:** Combined gate logic that requires passing both local and global conditions

### Design Principle: Dual Validation

**Local metrics** provide immediate, high-frequency signals (within-session discovery patterns). **Membench metrics** provide lagging indicators (memory system health over time). Together, they create a two-layer quality assurance:

- **Fast feedback:** Citation density, downstream impact, W-ratio (computed from manifests, real-time)
- **Lagging validation:** HONEY retention, NECTAR recency, bootstrap success (historical, cross-session)

This avoids the pitfall of "looks good locally but breaks globally" by requiring both layers to align.

---

## Part 2: Local Emergence Metrics (Per-Session)

### Quality Gate Framework

Three gates measure system health within a session. All three must pass for **READY** status.

#### Gate 1: Citation Density ≥30%

**What it measures:** Cross-agent learning and manifest discovery.

**Formula:**
```
citation_density = manifests_with_cross_citations / total_manifests_returned
```

A manifest has "cross-citations" if it references discoveries from other agents (via `discovered_work[].from_label != self.task_id`).

**Why it matters:** Agents reading manifests from prior work and building on discoveries indicates the stigmergic system is working. If <30%, agents are isolated; if >70%, mission is highly coupled (dense coordination).

**Thresholds:**
- PASS: ≥0.30 (agents learning from each other)
- CAUTION: 0.20–0.29 (isolated work, early coupling)
- FAIL: <0.20 (no cross-agent discovery)

**Example:**
- 18 manifests returned in session
- 6 manifests cite prior discoveries from other agents
- Citation density = 6/18 = 0.33 → PASS

#### Gate 2: Assumption Brittleness <0.40

**What it measures:** Stability of foundational assumptions.

**Formula:**
```
brittleness = (W_ratio × 0.60) + (baseline_test_gap × 0.25) + (evidence_quality_delta × 0.15)

where:
  W_ratio = W-edges (assumption backtracking) / total edges
  baseline_test_gap = missing critical tests / critical test count
  evidence_quality_delta = (low-confidence discoveries) / total discoveries
```

**Why it matters:** High W-ratio signals the mission encountered design flaws that required reverting to baseline assumptions. Persistent high brittleness (<0.40) indicates unstable architecture or requirements churn.

**Thresholds:**
- PASS: <0.40 (assumptions solid, few backtracks)
- CAUTION: 0.40–0.54 (some baseline reverification needed)
- FAIL: ≥0.55 (high fragility, design drift)

**Example:**
- W-ratio: 3 W-edges / 18 total = 0.167
- Baseline test gap: 0 missing / 4 critical = 0
- Evidence quality: 2 low-conf / 11 discoveries = 0.18
- Brittleness = (0.167 × 0.60) + (0 × 0.25) + (0.18 × 0.15) = 0.10 + 0 + 0.027 = 0.127 → PASS

#### Gate 3: Downstream Impact ≥60%

**What it measures:** Impact of shipped work on unblocking downstream tasks.

**Formula:**
```
downstream_impact = N_edges_resolved / total_N_edges

where:
  N_edges_resolved = north-bearing discoveries that were shipped (resolved as S-edges) in same or later wave
  total_N_edges = all unblock (N-bearing) tasks identified
```

**Why it matters:** A system that ships features but leaves prerequisites unresolved has low impact. High downstream impact (>60%) indicates shipping is enabling downstream progress.

**Thresholds:**
- PASS: ≥0.60 (shipping unblocks downstream)
- CAUTION: 0.40–0.59 (some impact, but delivery lags)
- FAIL: <0.40 (shipped work doesn't unblock)

**Example:**
- N-edges identified: 5 unblock tasks
- N-edges resolved (shipped and successful): 3
- Downstream impact = 3/5 = 0.60 → PASS

### Per-Archetype Emergence Scoring

Each archetype (NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER) is scored on its contribution to mission emergence. This prevents single-archetype domination and ensures cognitive diversity is active.

#### NAVIGATOR Contribution

**Measures:** N-edge discovery and bearing distribution clarity.

**Formula:**
```
navigator_score = (N_edges / total_edges) × clustering_strength × (1 - discovery_latency)

where:
  clustering_strength = (discoveries cited by other agents) / (navigator's discoveries)
  discovery_latency = (time to first N-edge discovery) / (total session time)
```

**Target:** >0.60 (strong unblocking; 50%+ of edges are N-bearings; discoveries cited by others)

**Interpretation:** High NAVIGATOR score indicates the agent efficiently identifies prerequisites and communicates them clearly (others cite the discoveries).

#### MAKER Contribution

**Measures:** S-edge delivery momentum and downstream impact.

**Formula:**
```
maker_score = (S_edges / total_edges) × avg_downstream_impact × quality_delivery

where:
  quality_delivery = (shipped tasks closed without W-backtracks) / (total shipped tasks)
```

**Target:** >0.70 (strong shipping; 50%+ of edges are S-bearings; low rework rate)

**Interpretation:** High MAKER score means the agent ships rapidly and with quality that doesn't require assumption reverification.

#### BRIDGE Contribution

**Measures:** E-edge synthesis and pattern applicability.

**Formula:**
```
bridge_score = (E_edges / total_edges) × pattern_applicability × clustering_coefficient

where:
  pattern_applicability = (discovered patterns applied to >1 domain) / (total patterns discovered)
  clustering_coefficient = (edges connecting N/S/E/W clusters) / (total possible interconnections)
```

**Target:** >0.50 (effective synthesis; some E-edges; patterns reused)

**Interpretation:** High BRIDGE score means the agent identifies and propagates cross-domain insights.

#### DEEP-DIVER Contribution

**Measures:** Assumption validation and brittleness prevention.

**Formula:**
```
deep_diver_score = (1 - W_penalty) × avg_baseline_validation × evidence_depth

where:
  W_penalty = min(W_ratio / 0.15, 1.0)  [penalized if >15% W-edges]
  avg_baseline_validation = tests_written_for_assumptions / critical_assumptions
  evidence_depth = (discoveries with ≥3 supporting lines of evidence) / (total discoveries)
```

**Target:** >0.70 (solid assumptions; W-ratio <15%; good evidence depth)

**Interpretation:** High DEEP-DIVER score means the agent prevented fragile assumptions and validated decisions with evidence.

### Overall Emergence Health

**Formula:**
```
emergence_health = (navigator_score + maker_score + bridge_score + deep_diver_score) / 4
```

**Target:** ≥0.75 for PASS, 0.60–0.74 for CAUTION, <0.60 for FAIL

**Interpretation:** Balanced contributions across archetypes indicate the team has cognitive diversity and no single-archetype bottleneck.

---

## Part 3: Global Membench Metrics (Multi-Session)

### M1-M5: Core Memory Metrics

These five metrics measure memory system correctness and efficiency:

| Metric | Formula | Target | Why |
|--------|---------|--------|-----|
| **M1: Retention** | correct_recalls / probe_set | ≥0.85 | Can memory surface what it stored? |
| **M2: Relevance** | actionable_entries / total_entries | ≥0.75 | Is memory building principles or a diary? |
| **M3: Work Efficiency** | tasks/token_with_memory / tasks/token_baseline | >1.10 | Is memory net-positive (ROI >10%)? |
| **M4: Overhead** | memory_tokens / total_context | <0.04 | Is memory crowding out task work? |
| **M5: Continuity** | facts_post_restart / facts_pre_restart | ≥0.95 | Do facts survive session restart intact? |

**Composite:** `M_core = (M1×0.25 + M2×0.20 + M3_norm×0.30 + M4_inv×0.10 + M5×0.15)`

### M6-M7: Diagnostic (Coordination + Crystallization)

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **M6: Coordination** | citations_cross_agent / total_findings | Are agents discovering each other? |
| **M7: Crystallization** | unique_concepts / total_tokens_in_memory | Is memory densifying or bloating? |

**Not gated but tracked:** These signal emergence health. Rising M6 and stable/rising M7 indicate the system is compounding.

### M8, M11: Veto Gates

| Metric | Threshold | Impact |
|--------|-----------|--------|
| **M8: Confabulation** | ≤5% hallucinated recalls | >5% blocks release |
| **M11: Bootstrap** | ≥70% agent memory loads successful | <70% blocks release |

### M12-M15: Emerging Dimensions (New in v0.3, validated 2026-05-03)

#### M12: Emergence Structural

**Formula:**
```
EMG_struct = (edge_density × 0.35) + (clustering × 0.30) + (linearity × 0.25) + ((1 - W_ratio) × 0.10)

where:
  edge_density = manifests_with_bearings / total_manifests
  clustering = discoveries_cited_by_different_agent / total_discoveries
  linearity = 1.0 if DAG topologically sortable, else (1 - cycle_ratio)
  W_ratio = W_edges / total_edges
```

**Target:** ≥0.79 (strong emergence structure)

**Validation:** Phase C mission-field-wire trial achieved 0.879 (confidence 0.87).

#### M13: Emergence Qualitative (Depth of Discoveries)

**Formula:**
```
EMG_qual = (discovery_novelty × 0.40) + (evidence_depth × 0.35) + (cross_domain_applicability × 0.25)

where:
  discovery_novelty = findings not in prior NECTAR / total findings
  evidence_depth = discoveries with 3+ supporting lines / total discoveries
  cross_domain_applicability = findings cited across domains / total findings
```

**Target:** ≥0.85 (high-quality, novel discoveries)

#### M14: Spawn Leverage (Cost Efficiency)

**Formula:**
```
M14_leverage = work_tokens_per_agent / (spawn_cost + return_cost + manifest_read_cost)
```

**Target:** >10× (ROI: agents return 10+ tokens of valuable work per token of overhead)

#### M15: Spawn Leverage Distribution (Fairness)

**Formula:**
```
M15_distribution = correlation(agent1_leverage, agent2_leverage, ... agentN_leverage)

where correlation is Pearson r across all agents in session
```

**Target:** ≥0.75 (balanced leverage across agent types; no one agent dominating)

---

## Part 4: Membench ↔ Emergence Bridge

### Four Correlation Patterns

#### Pattern 1: HONEY Retention ↔ Citation Density

**Mechanism:** When HONEY (crystallized facts) is accurate and complete, agents read it, synthesize it, and cite it in manifests. High HONEY retention (M1 ≥0.85) correlates with high citation density (≥0.30).

**Signal:** If HONEY retention drops >10%, citation density should drop within 1-2 sessions.

**Action:** If M1 drops to <0.80, audit HONEY.md for stale or inaccurate entries; run crystallization.

#### Pattern 2: NECTAR Recency ↔ Emergence Trajectory

**Mechanism:** Fresh NECTAR (findings from recent sessions) enables agents to build on recent discoveries. High NECTAR recency (median age <7 days) correlates with positive emergence trajectory.

**Signal:** If NECTAR age exceeds 14 days (unpromoted findings aging out), emergence_trajectory should become flat or negative.

**Action:** If trajectory turns negative, check NECTAR age; promote candidates to HONEY.

#### Pattern 3: Coordination (M6) ↔ Downstream Impact

**Mechanism:** When agents cite each other (M6 high), they coordinate on unblocking work. High M6 (>0.40) correlates with high downstream impact (>0.60).

**Signal:** If M6 drops >15%, downstream impact should lag by 1-2 sessions.

**Action:** If downstream impact falls, scan manifests for low citation density; increase discovery opportunities.

#### Pattern 4: Crystallization (M7) ↔ Per-Archetype Balance

**Mechanism:** When HONEY densifies (M7 rising), discovered patterns are integrated. This enables archetypes to discover richer principles and contribute more balanced edges. Rising M7 correlates with higher correlation in per-archetype scores (M15).

**Signal:** If M7 declines (memory bloating), per-archetype balance should decrease.

**Action:** If M7 falls, trigger crystallize; dedup NECTAR, promote to HONEY, and prune low-relevance entries.

---

## Part 5: Release Readiness Decision Tree

Release of faerie2 v2.0 requires passing six gates (AND logic):

```
RELEASE_READY = 
  quality_gates_pass AND 
  emergence_positive AND 
  per_archetype_balance AND 
  membench_healthy AND 
  cost_formula_validated AND 
  archetype_stable
```

### Gate 1: Quality Gates Pass (3/3)

**Condition:** Citation density ≥0.30 AND brittleness <0.40 AND downstream impact ≥0.60

**Check:** Run `0x_quality_gate_metrics.py --mission faerie2`

**Status:** PASS = 3/3 green | CAUTION = 2/3 green | FAIL = <2/3 green

### Gate 2: Emergence Trajectory Positive or Flat

**Condition:** (emergence_score_today - emergence_score_yesterday) ≥ -0.03 for 3 consecutive sessions

**Check:** Run `0x_temporal_emergence_trends.py --sessions 3`

**Rationale:** System should not regress. Flat emergence is healthy equilibrium; negative trajectory signals design drift.

**Status:** PASS if trajectory ≥-0.03, FAIL if <-0.03

### Gate 3: Per-Archetype Balance ≥0.75

**Condition:** Correlation of (navigator_score, maker_score, bridge_score, deep_diver_score) ≥ 0.75

**Check:** Run `0x_emergence_per_archetype.py --session-count 5 --correlation`

**Rationale:** Prevents single-archetype domination. All four should contribute balanced (similar magnitude scores).

**Status:** PASS if correlation ≥0.75, CAUTION if 0.60–0.74, FAIL if <0.60

### Gate 4: Membench Metrics Healthy

**Condition:** M1 ≥0.85 AND M3 >1.10 AND M8 ≤5% AND M11 ≥70%

**Check:** Run `python3 /mnt/d/0local/gitrepos/membench/harness_core.py --session-date today`

**Rationale:** M1 (retention), M3 (efficiency), M8 (confabulation veto), M11 (bootstrap veto) are non-negotiable.

**Status:** PASS if all four conditions met, FAIL if any unmet

### Gate 5: Cost Formula Validated (P0 Mutation Passed)

**Condition:** spawn_cost_estimate drift <20% from actual across 3 sessions; leverage >10×

**Check:** Inspect `forensics/main-metrics.jsonl` for cost deltas

**Rationale:** Cost accounting must be reliable for production planning.

**Status:** PASS if drift <20% avg, CAUTION if 20–35%, FAIL if >35%

### Gate 6: Archetype Stability (P1 Mutation Passed)

**Condition:** Per-archetype score correlation ≥0.75 across 3 sessions (consistency)

**Check:** Run `0x_emergence_per_archetype.py --session-count 3 --archetype-stability`

**Rationale:** Ensures emergence metrics are not noisy; stable archetype contributions indicate reproducible system behavior.

**Status:** PASS if correlation ≥0.75, CAUTION if 0.60–0.74, FAIL if <0.60

### Summary

| Gate | Metric | Target | Current | Status |
|------|--------|--------|---------|--------|
| 1 | Citation density | ≥0.30 | ? | ? |
| 1 | Brittleness | <0.40 | ? | ? |
| 1 | Downstream impact | ≥0.60 | ? | ? |
| 2 | Trajectory | ≥-0.03 | ? | ? |
| 3 | Per-archetype correlation | ≥0.75 | ? | ? |
| 4 | M1 (Retention) | ≥0.85 | ? | ? |
| 4 | M3 (Efficiency) | >1.10 | ? | ? |
| 4 | M8 (Confabulation) | ≤5% | ? | ? |
| 4 | M11 (Bootstrap) | ≥70% | ? | ? |
| 5 | Cost drift | <20% | ? | ? |
| 6 | Archetype stability | ≥0.75 | ? | ? |

**Release decision:** Count PASSes. If all 6 gates PASS → READY FOR V2.0. If any FAIL → investigate and remediate.

---

## Part 6: Integration Points

### Script Chain

```
Session start (cold start or /faerie)
  ↓
1. Agents spawn, write manifests
  ↓
2. Post-wave: 0x_emergence_per_archetype.py runs (per-archetype scores)
  ↓
3. Post-wave: 0x_quality_gate_metrics.py runs (quality gates: citation, brittleness, impact)
  ↓
4. Post-session: 0x_temporal_emergence_trends.py runs (trajectory, latency, clustering)
  ↓
5. Post-session: membench harness runs (M1-M11, M12-M15)
  ↓
6. /dev-eval reads all outputs, computes release readiness score
  ↓
7. Dashboard updates with PASS/FAIL for each gate
```

### File Locations

| Script | Path | Output |
|--------|------|--------|
| Per-archetype scoring | `scripts/0x_emergence_per_archetype.py` | `forensics/ephemeral/{date}/emergence-per-archetype.json` |
| Quality gates | `scripts/0x_quality_gate_metrics.py` | `forensics/ephemeral/{date}/quality-gates.json` |
| Temporal trends | `scripts/0x_temporal_emergence_trends.py` | `forensics/ephemeral/{date}/emergence-trends.json` |
| Membench harness | `membench/harness_core.py` | `membench/baselines/{date}.json` |
| /dev-eval aggregator | `scripts/0x_dev_eval.py` | `forensics/ephemeral/{date}/system-eval.json` |

### Signal Flow into /dev-eval

```json
{
  "session_id": "2026-05-03-w1",
  "quality_gates": {
    "citation_density": {"value": 0.45, "status": "PASS"},
    "brittleness": {"value": 0.18, "status": "PASS"},
    "downstream_impact": {"value": 0.72, "status": "PASS"}
  },
  "emergence": {
    "per_archetype": [
      {"archetype": "NAVIGATOR", "score": 0.857},
      {"archetype": "MAKER", "score": 0.823},
      {"archetype": "BRIDGE", "score": 0.719},
      {"archetype": "DEEP-DIVER", "score": 0.771}
    ],
    "overall_health": 0.793,
    "trajectory": 0.042,
    "correlation": 0.78
  },
  "membench": {
    "M1": 0.88,
    "M3": 1.31,
    "M8": 0.01,
    "M11": 1.0,
    "M12": 0.879,
    "M13": 0.893,
    "M14": 11.4,
    "M15": 0.82
  },
  "release_readiness": {
    "gate_1_quality": "PASS",
    "gate_2_trajectory": "PASS",
    "gate_3_balance": "PASS",
    "gate_4_membench": "PASS",
    "gate_5_cost": "PASS",
    "gate_6_stability": "CAUTION",
    "overall": "READY_WITH_WATCH"
  }
}
```

---

## Part 7: Interpretation Guide for Humans

### Reading the Emergence Dashboard

**High Emergence + Balanced Archetypes = Healthy**
- All archetypes scoring 0.60–0.85
- Citation density >0.30
- Downstream impact >0.60
- NAVIGATOR finding prerequisites, MAKER shipping, BRIDGE connecting, DEEP-DIVER validating

**Imbalanced Archetypes = Red Flag**
- One archetype >> others (e.g., MAKER 0.92, NAVIGATOR 0.45)
- Means: System has a bottleneck; one type doing most work
- Action: Investigate why other archetypes aren't discovering work; increase frontier scope

**High Brittleness = Design Drift**
- Brittleness >0.40 with rising W-ratio (>10%)
- Means: Assumptions breaking, backtracking to baseline repeatedly
- Action: Audit recent changes; validate core design decisions; possibly rollback mutations

**Negative Trajectory = Regression**
- Emergence score declining 2+ sessions in a row
- Means: System health degrading; something broke
- Action: Halt new deployments; audit mutations applied; check HONEY accuracy; run baseline tests

### Reading Membench Signals

**M1 Dropping (Retention <0.80) = Memory Reliability Crisis**
- HONEY/NECTAR entries are inaccurate or stale
- Action: Run crystallize; audit recent HONEY promotions; check agent truthfulness

**M3 Declining (Efficiency <1.10) = Memory System Overhead**
- Memory is consuming more tokens than it saves
- Action: Trim HONEY bloat; reduce on-demand retrieval noise; check M4 overhead ratio

**M6 Dropping (Coordination <0.25) = Agents Isolated**
- Agents not discovering each other's work
- Action: Check frontier scan performance; increase manifest discovery prompting; review mission field routing

**M7 Falling (Crystallization declining) = Memory Bloating**
- Number of tokens in HONEY rising while unique concepts flat/declining
- Action: Schedule crystallization; merge duplicate entries; promote high-value findings

---

## Part 8: Next Steps + Roadmap

### Immediate (Next Session)

- [ ] Wire `/dev-eval` to read all six gates
- [ ] Create daily dashboard showing release readiness (PASS/FAIL for each gate)
- [ ] Run baseline measurements on current system (establish T0 for P0/P1 mutations)
- [ ] Integrate membench harness into post-session hook

### Short-term (1 week)

- [ ] Promote M12-M15 to membench v0.3 spec (publish in public repo)
- [ ] Validate M12 on 3+ additional missions (different types)
- [ ] Measure full M13 (qualitative depth) with LLM rubric
- [ ] Create temporal dashboard (emergence trajectory over 30 days)

### Medium-term (1 month)

- [ ] Lock release readiness criteria in CLAUDE.md
- [ ] Document per-archetype emergence as training signal for agent selection
- [ ] Wire membench outputs into piston tier selection (context-responsive dispatch)
- [ ] Publish research paper on emergence measurement framework

---

## References

- **Membench Public Rubric:** `/mnt/d/0local/gitrepos/membench/METRICS.md`
- **Faerie2 Emergence Metrics:** `/mnt/d/0local/gitrepos/faerie2/docs/emergence-quality-metrics-implementation.md`
- **Phase C Validation:** `/mnt/d/0local/gitrepos/membench/faerie2_emergence_validation.json`
- **CLAUDE.md:** `/mnt/d/0local/gitrepos/faerie2/CLAUDE.md`
- **HONEY.md:** `/mnt/d/0LOCAL/.claude/HONEY.md`

---

**Document version:** 1.0 | **Date:** 2026-05-03 | **Next review:** 2026-05-17

