---
type: canonical-formulas
title: Faerie2 Canonical Formulas
created: 2026-05-05
updated: 2026-05-18
tags: [emergence, formulas, mutable-parameters, ffmx, piston, mutation-discipline]
promotion_state: capture
source_path: "vault-native"
source_hash: "sha256:55b61620ef57f6e7c27824e38daf0e9b95fc946a2c9e75329ba359f318c8dcc0"
doc_hash: "sha256:"
hash_ts: 2026-05-18T00:00:00Z
hash_method: body-sha256-v1
cloud_path: ""
promoted_to: ""
promoted_at: ""
---

# Faerie2 Canonical Formulas

**Single source of truth for all system formulas: spawn pressure, mutation testing, quality gates, FFMx metrics, and emergence tuning.**

Version: Living (continuous refinement via mutation discipline)  
**Last updated:** 2026-05-05T23:00:00Z  
Supersedes: faerie2-formulas.json, formulas.json, formulas-living-consolidated.json, ffmx-formulas-calibration-guide.md

---

## North Star: f(0) Orchestration Burden ≈ 0

**Definition:** Main session orchestration overhead as % of total session tokens.

```
f(0) = main_tokens / total_session_tokens
Target: ≤5% (aspirational)
Tolerance: If f(0) = 8%, adjust bundle size or increase parallelism—don't panic
Feedback: If f(0) > 10%: reduce bundle size OR increase agent parallelism. If f(0) < 2%: can afford deeper main reasoning.
```

**Measurement hook:** `9x_f0_tracker.py` captures presend cost, agent costs, final total.  
**Frequency:** Every session (feeds living formula feedback)

---

## Mutable Parameters (Tunable via Mutation Discipline)

### Spawn Pressure (Context-Driven)

#### Context-Pressure Logistic Sigmoid (PROPOSED — 2026-05-05)

**Purpose:** Replace discrete W1/W2/W3 thresholds with continuous spawn pressure curve.

```
p(c) = 1 / (1 + e^(-k·(c - c_mid)))

where:
  c = current_context_fill_pct (0-100)
  c_mid = midpoint_context_pct (tunable, default: 60)
  k = steepness (tunable, default: 0.05, lower=gentler curve)
  p(c) = spawn_probability (0-1)

Behavior:
  c ≤ 25%: p(c) ≈ 0.95 (spawn often, teams large)
  c = 50%: p(c) ≈ 0.50 (balance)
  c ≥ 75%: p(c) ≈ 0.05 (spawn rarely, teams small)
```

**Calibration (current):**
| Parameter | Min | Current | Max | Unit |
|-----------|-----|---------|-----|------|
| c_mid | 40 | 60 | 80 | % |
| k | 0.01 | 0.05 | 0.15 | steepness |

**Measurement:** Log (context_fill, p(c), spawn_decision) every spawn decision. Monthly: refit sigmoid to data.

**Replaces:** WAVE_1_SPAWN_MAX_CONTEXT_PCT (70), WAVE_2_SPAWN_MAX_CONTEXT_PCT (80), WAVE_3_SPAWN_MAX_CONTEXT_PCT (87)

---

### Quality Gates (Compass Phases)

| Gate | Baseline | Current | Min | Max | Unit | Meaning |
|------|----------|---------|-----|-----|------|---------|
| **SEED_QUALITY_MIN** | 0.50 | 0.78 | 0.30 | 0.70 | score | Min quality to exit SEED phase (fast hypothesis vs rigorous baseline) |
| **DEEPEN_QUALITY_MIN** | 0.70 | 0.82 | 0.60 | 0.85 | score | Min quality to exit DEEPEN phase (focused ingest) |
| **EXTEND_QUALITY_MIN** | 0.80 | 0.89 | 0.70 | 0.90 | score | Min quality to exit EXTEND phase (cross-validation) |
| **FULL_QUALITY_MIN** | 0.85 | 0.92 | 0.80 | 0.95 | score | Min quality for production-ready artifact (highest bar) |

**Measurement source:** quality-gates-measurer (N=52, 2026-04-28). Recalibration based on pass-rate targets.

**Coupled to:** Agent compass navigation; regresses if agents cannot assess own quality.

---

### Belief Gates (Honesty & Self-Awareness)

| Gate | Baseline | Current | Min | Max | Unit | Meaning |
|------|----------|---------|-----|-----|------|---------|
| **DEEPEN_BELIEF_MIN** | 0.50 | 0.50 | 0.30 | 0.70 | score | Min honesty/self-awareness in DEEPEN phase |
| **EXTEND_BELIEF_MIN** | 0.75 | 0.75 | 0.65 | 0.90 | score | Min honesty for edge case exploration (safety gate) |

**Purpose:** Agents must know their limits. Low belief = agent hiding confidence.

**Coupled to:** Manifest truthfulness, contradiction-caught rate, false-confidence incidents.

---

### Reputation System (Agent Scoring)

| Weight | Current | Min | Max | Purpose |
|--------|---------|-----|-----|---------|
| **TRUTHFULNESS** | 0.35 | 0.20 | 0.50 | Reward honest self-reporting |
| **KNOWLEDGE_DEPTH** | 0.30 | 0.20 | 0.40 | Deep knowledge over surface work |
| **WISDOM (Collaboration)** | 0.20 | 0.10 | 0.35 | Cross-citation, monkeybranching depth |
| **EFFICIENCY (FFMx)** | 0.15 | 0.05 | 0.30 | Token efficiency per artifact |

**Composite score:** weighted blend of above dimensions.

**Recovery threshold:** Below 0.50 = agent moved to retraining tasks only (quarantine + recovery mode).

**Decay formula (PROPOSED):** `score_aged(t) = score_0 / (1 + λ·days)`
- λ = decay constant (default: 0.1/day, half-life ~7 days)
- Purpose: Prevent permanent reputation caste; enable meritocracy

---

### Memory & Bundle Tuning

| Parameter | Baseline | Current | Min | Max | Unit | Meaning |
|-----------|----------|---------|-----|-----|------|---------|
| **NECTAR_INJECTION_TOKENS** | 1200 | 1200 | 800 | 3000 | tokens | Measured: 1,204 tokens (theory was 2-3K, 40-60% cheaper) |
| **HONEY_INJECTION_TOKENS** | 200 | 200 | 50 | 1500 | tokens | Measured: ~200 tokens (theory was 1,500, 7.5x cheaper via compression) |
| **BUNDLE_EMISSION_THRESHOLD** | 30 | 30 | 20 | 50 | % context remaining | When agents should emit bundles for future scouts |

**Coupled to:** Agent ramp-up efficiency, emergence signal freshness, bundle overhead.

---

### Emergence Multiplier (Cross-Session Knowledge Compounding)

**Formula:**
```
mission_ffmx = cross_citations × (1 + monkeybranching_depth × EMERGENCE_MULTIPLIER_BASE)
```

| Parameter | Current | Min | Max | Meaning |
|-----------|---------|-----|-----|---------|
| **EMERGENCE_MULTIPLIER_BASE** | 1.0 | 0.5 | 2.5 | Controls emergence intensity |

**Tuning guide:**
- 0.5 = conservative emergence (safe, low variation)
- 1.0 = balanced emergence (current sweet spot)
- 2.5 = maximum emergence (high risk/reward for large expeditions)

**Coupled to:** Cross-citation count, monkeybranching depth, M1 (retention), M8 (confabulation).

**Living adjustment:** If mission_ffmx < 1,200: raise to 1.3. If M1/M8 regress: revert.

---

### Spawn Bundle Mixture (PROPOSED)

**Purpose:** Auditable token allocation across context layers.

```
bundle = 0.15·HONEY + 0.30·NECTAR + 0.35·pollen + 0.20·task_context
```

| Layer | Weight | Max Tokens | Purpose |
|-------|--------|-----------|---------|
| HONEY | 0.15 | 200 | Global + project architectural principles |
| NECTAR | 0.30 | 1200 | Crystallized memory (tail-50 observations) |
| Pollen | 0.35 | 500 | Raw forensic signals (mission frontier) |
| Task Context | 0.20 | 800 | Immediate task + bundle (input context) |

**Expected impact:** 5-10% bundle size reduction on focused tasks.

**Living feedback:** Track bundle_size per session. If >3500 tokens: tighten weights. If <1500: loosen.

---

## Immutable Constants (Cannot Override)

| Constant | Value | Unit | Reason | Meaning |
|----------|-------|------|--------|---------|
| **AUTO_COMPACT_THRESHOLD** | 93.5 | % | Hard architectural ceiling | Context fill at which auto-compact fires |
| **BUILTIN_OVERHEAD_TOKENS** | 9000 | tokens | Fixed by Claude architecture | Overhead before user context starts |
| **USABLE_CONTEXT_WINDOW** | 191000 | tokens | 200K - 9K | Actual tokens for agents + memory |

---

## FFMx Force Multiplier Index

### Metric 1: FFMx (Dispatch Efficiency) — Single-Session

**Purpose:** Measure agent spawn efficiency within one session.

```
FFMx = N_completed × Q × (1 + D) × P

where:
  N_completed = count of agents returning valid manifest (0-6)
  Q = average manifest quality score (0.0-1.0)
    • 0.25 per field: output_path, dashboard_line, files_written, next_mission_node
  D = discovery rate (new work found)
    • discovered_work_items / max(N_completed, 1)
  P = piston efficiency multiplier (0.7-1.2)
    • 1.0 base
    • -0.3 if W1→W2 latency > 60s (slow transition)
    • +0.2 if adaptive manifest bundling used (faster reads)
    • -0.1 if prescan cache miss_rate > 0.5 (frontier discovery slow)
```

**Current baseline:** 44.4 per session (Phase C 2026-05-03)  
**Target range:** 30-40 per session  
**Interpretation:** 44.4 is above target; system discovering more work or agents high-quality. Healthy.

**When to use:** Validate manifest structure, track spawn productivity, monitor piston efficiency across W1/W2/W3.

---

### Metric 2: mission_ffmx (Emergence Force Multiplier) — Multi-Session

**Purpose:** Measure cross-session collaboration strength and knowledge compounding.

```
mission_ffmx = cross_citations × (1 + monkeybranching_depth × EMERGENCE_MULTIPLIER_BASE)

where:
  cross_citations = count of manifest discoveries referencing prior manifests
  monkeybranching_depth = average citation distance (manifest layers back)
  EMERGENCE_MULTIPLIER_BASE = tuning knob (0.5-2.5, currently 1.0)
```

**Current calibration:**
- **Target range:** 1,000-2,000+ per session (good day)
- **Baseline:** 800-1,200 per typical session
- **Critical floor:** <200 (isolation; agents not discovering each other)

**Coupling to membench:** Dominates by compression ratio (ln term, >70% of total).

**Living tuning:** If FFMx down, check compression ratio first.

---

## Mutation Discipline (Required Protocol)

Every formula change MUST follow this protocol:

### 5-Phase Protocol

1. **Measure baseline (T=0)** — 3 sessions minimum
   - Capture M1-M15 membench scores
   - Record FFMx dispatch + mission_ffmx
   - Measure coupling values (A-G in calibration table)

2. **Hypothesis** — Predict impact before change
   - Example: "If we reduce manifest overhead 60→45 tokens, FFMx-A improves to 0.75, lifting M3 by 12%"

3. **Mutation phase** — Apply change for 3 sessions
   - Edit formula parameter
   - Observe behavior (but don't measure yet)

4. **Measure again (T=1)** — 3 sessions post-mutation
   - Re-measure all baseline metrics
   - Compute deltas (T1 - T0)

5. **Evaluate** — Accept/revert/iterate
   - Hypothesis validated? (error <20%) → ACCEPT
   - Negative emergence? (couplings regress) → REVERT
   - Mixed results? → ITERATE (hybrid tuning)
   - **Lock to HONEY only if confidence ≥0.80**

---

### FFMx-Membench Coupling Framework

| Dimension | Factor | Membench Link | Current | Target | Leverage Action |
|-----------|--------|---|---------|--------|-----------------|
| **A** | Throughput (tasks/session) | M3 (Work Efficiency) | 0.50 | 0.75 | Reduce manifest overhead 60→45 tok; faster bundling |
| **B** | Memory (NECTAR retrieval latency) | M1 (Retention), M2 (Relevance) | 0.667 | 0.80 | Activate M6 citation tracking; improve NECTAR indexing |
| **C** | Resilience (manifest persistence) | M5 (Continuity) | 1.0 | 1.0 | Maintain via springboard validation; no regression |
| **D** | Quality (confabulation rate) | M8 (<5% veto gate) | 1.0 | 1.0 | Monthly audit; alarm if M8 >3% |
| **E** | Piston (W1→W2 latency) | M14 (Per-Agent Leverage) | 0.50 | 0.75 | Measure post-mutation; target <30sec latency |
| **F** | Model Routing (archetype balance) | M15 (Leverage Distribution) | 0.50 | 0.75+ | Measure correlation ≥0.75 across agent types |
| **G** | Defense (adversarial veto) | M11 (Bootstrap: ≥70%) | null | 0.85 | Build 50-item adversarial probe; measure pass rate |

---

## Measurement Infrastructure (Hooks)

| Hook | File | Trigger | Captures | Output | Cadence |
|------|------|---------|----------|--------|---------|
| **f(0) tracker** | 9x_f0_tracker.py | PostCompact | presend_tokens, agents, agent_total, context_fill | forensics/metrics/session-{ID}-f0.json + timeseries | Every session |
| **Context pressure** | 9x_context_pressure_logger.py | PreSpawn | context_fill, p(c), spawn_decision, wave | forensics/metrics/context-pressure-log.jsonl | Every spawn |
| **Mission coherence** | 9x_mission_coherence_analyzer.py | PostWave | investigation_labels, entropy_H, coherence_score | forensics/metrics/coherence-{wave}.json | After each wave |
| **Reputation tracker** | 9x_reputation_tracker.py | SubagentStop | agent_type, prior_score, task_outcome, days, decay | forensics/metrics/reputation-{agent}.jsonl | Every agent done |
| **FFMx health monitor** | 0x_ffmx_health_monitor.py | PostSession | mission_ffmx trend, cross_citations, monkeybranching | forensics/daily/ffmx-health-report-{date}.json | Daily |

---

## Living Feedback Loops

### f(0) Adjustment (Weekly)
- **Inputs:** 9x_f0_tracker.py outputs (last 7 days)
- **Decision:** If f(0) > 0.08: tighten bundle OR increase parallelism. If f(0) < 0.02: afford deeper main reasoning
- **Owner:** Main session review

### Context Pressure Tuning (Monthly)
- **Inputs:** context-pressure-log.jsonl (30 sessions), actual spawn timings
- **Decision:** Refit sigmoid (c_mid, k) if observed vs predicted >20% divergence
- **Owner:** Mutation eval

### Compression Ratio Focus (Session-level)
- **Inputs:** FFMx composite, token_in vs token_out
- **Decision:** If FFMx down: check compression ratio first (dominates 70% of multiplier)
- **Owner:** Main spawn planning

### Mission Drift Detection (Post-wave)
- **Inputs:** coherence_score from 9x_mission_coherence_analyzer.py
- **Decision:** If coherence < 0.75: warn 'mission drift'. If > 0.95: may be over-constrained
- **Owner:** Main

---

## Anti-Bloat Guardrail

**Rule:** No formula change becomes permanent without measured equilibrium-respecting evidence.

**Process:**
1. Measure baseline (10 sessions)
2. Propose formula + fit parameters
3. Run shadow mode (5 sessions, no behavioral change)
4. Cutover only when: shadow agreement >80% AND catches ≥1 decision baseline missed AND no harm (Membench delta ≥0)

---

## Implementation Roadmap

### Phase 1: Measurement (Immediate — This/Next 3 Sessions)
- Wire 9x_f0_tracker.py (PostCompact) → start measuring f(0)
- Wire 9x_context_pressure_logger.py (PreSpawn) → log p(c) vs spawn
- Wire 9x_mission_coherence_analyzer.py (PostWave) → measure team focus
- Create forensics/metrics/{timeseries,session-logs} directories

### Phase 2: Shadow Mode (Sessions 4-8)
- Implement Context Pressure Sigmoid but run in shadow (no behavioral change)
- Log p(c) values, compare to actual W1/W2/W3 decisions
- Measure: does sigmoid predict spawn timing >80% accuracy?

### Phase 3: Cutover (Sessions 9-12)
- Replace hardcoded wave thresholds with sigmoid queries
- Monitor f(0), coherence, FFMx (should maintain or improve)
- Living adjustment: refit formula weekly

### Phase 4: Research (Ongoing)
- Test alternative formulas (reputation decay, bundle mixture, entropy)
- Measure impact on agent quality, discovery density
- Publish monthly formula performance report

---

## References

- **Membench metrics:** `/mnt/d/0local/gitrepos/membench/METRICS.md`
- **Emergence implementation:** `/mnt/d/0local/gitrepos/faerie2/docs/emergence-quality-metrics-implementation.md`
- **Mutation baseline (T0):** `/mnt/d/0local/gitrepos/faerie2/forensics/mutation-baselines/mutation-baseline-T0.json`
- **Session evaluations:** `/mnt/d/0local/gitrepos/faerie2/forensics/eval-history.jsonl`
- **CLAUDE.md dispatch doctrine:** `/mnt/d/0local/gitrepos/faerie2/CLAUDE.md`

---

## Supersedes

This canonical formulas doc supersedes:
- ❌ `.claude/faerie2-formulas.json` (archived)
- ❌ `.claude/formulas.json` (archived)
- ❌ `.claude/formulas-living-consolidated.json` (archived)
- ❌ `docs/ffmx-formulas-calibration-guide.md` (archived)

**All new formula work goes here. All references point here.**

---

**Document version:** 1.0 | **Date:** 2026-05-05 | **Status:** Consolidation Complete | **Confidence:** High

