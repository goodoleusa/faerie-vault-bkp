# Implementation Roadmap — 4-Phase Rollout with Anti-Bloat Guardrail

## Phase 1 (Week 1) — Measurement Only, Zero Policy Change

**Objective:** Wire three previously-missing metrics. No behavioral changes.

### Tasks:

1. **f(0) Context Burden Ratio** in `0x_spawn_template.py`
   - Record `main_tokens` per spawn
   - Aggregate to `forensics/session-metrics/{date}.json`
   - Target: median f0 across last 10 sessions ≤ 0.05

2. **Aged Score** in `0x_reputation_summary.py`
   - Add `aged_score = score_0 / (1 + 0.1 * days_since_eval)`
   - Compute alongside existing `composite_score`
   - Routing reads `aged_score` for dispatch (recommendation, not active)

3. **Mission Coherence Entropy** in `0x_mission_graph.py --query topology`
   - Compute: `coherence = 1 - H(labels) / H_max`
   - Output to session dashboards
   - Target: ≥ 0.90

**Expected impact:** Zero behavioral change. Three new observables.

---

## Phase 2 (Week 2) — Shadow Mode for Pressure & Gates

**Objective:** Compare new formulas to current implicit logic. Build disagreement data.

### Tasks:

4. **Context Pressure (logistic sigmoid)**
   - Compute `pressure = 1 / (1 + e^(-k·(c - c_mid)))`
   - Log alongside hardcoded W1/W2/W3 decisions
   - Track: agreement %, disagreement type, impact

5. **Phase Gate Probability (sigmoid)**
   - Compute `P(advance) = sigmoid(w1·q + w2·b + w3·(q-b) + bias)`
   - Log alongside hard thresholds
   - Track: decision divergence, especially near 0.80/0.85 boundaries

**Expected impact:** 5 sessions of shadow data → identifies failure modes of current logic.

---

## Phase 3 (Week 3) — Cutover for Proven Wins

**Objective:** Promote formulas with >80% shadow agreement and positive delta.

### Tasks:

6. **Replace W1/W2/W3 thresholds** with logistic pressure
   - Cutover if: shadow agreement > 80% AND Membench delta ≥ 0
   - Update piston_checkpoint.json to use `pressure()` curve

7. **Add bundle mixture weights** to template
   - Default: recency mode (α=0.15, β=0.30, γ=0.35, δ=0.20)
   - Opt-in: relevance mode for specialists
   - Expected impact: ~5–10% bundle token reduction on focused tasks

**Expected impact:** Smoother wave transitions, measurable token savings.

---

## Phase 4 (Week 4) — Research-Grade Additions

**Objective:** Wire lower-ROI but high-signal metrics.

### Tasks:

8. **Discovery Rate Power Law** (predictive)
   - Implement: `discovery(N, ρ, t) = 1.5 · N^0.8 · ρ^0.6 · e^(-0.5·t)`
   - Use for: throughput prediction before spawning

9. **Emergence Quantification** (post-hoc)
   - Per session: `emergence_value = Σ(utility·novelty) / 277K`
   - Add to session reports

10. **Compression Efficiency QA** on manifests
    - Flag: `efficiency < 0.8`
    - Auto-prompt agent to tighten

**Expected impact:** New dashboards. No operational change.

---

## Anti-Bloat Guardrail (Fundamental Governance Rule)

**No formula promotes without measured equilibrium-respecting evidence.**

### Protocol:

1. **Baseline (10 sessions)**
   - Measure all raw metrics under current (implicit) formulas
   - Record decision outcomes

2. **Propose formula + fit parameters**
   - Optimize parameters (k, c_mid, α, β, λ) to minimize reconstruction error
   - Define: "acceptable agreement" (80%+ on safe decisions)

3. **Shadow mode (5 sessions)**
   - Compute new formula in parallel with baseline
   - Track: decision divergence, decision impact, Membench change

4. **Cutover criteria (ALL must hold):**
   - Shadow agreement > 80% on safe decisions
   - Formula catches ≥1 decision baseline missed
   - Membench delta ≥ 0 (no harm)
   - Agent leadership approves

5. **Promotion**
   - Move from shadow to active
   - Document in RELEASE-NOTES
   - Archive baseline for regression testing

### Why This Matters

- **Prevents formula churn:** Only proven formulas get promoted
- **Respects equilibrium:** Mutations measured before and after
- **Builds confidence:** 80%+ shadow agreement ≠ 100%, but better than assertion
- **Reversible:** If formula breaks, revert to shadow-mode data (no guessing)

---

## Risk Mitigations

| Risk | Mitigation |
|------|-----------|
| Over-fitting to one session | Replicate FFMx calibration across N≥30 sessions before fixing thresholds |
| Sigmoid T mis-tuning | Start T=0.1 (sharp), tune via shadow runs to find inflection zone |
| Decay rate too aggressive | Cap λ at 0.1; anything higher punishes legitimate long-cycle specialists |
| Bundle weights starve specialists | Always offer relevance variant as fallback |
| Phase gates become meaningless | Temperature T must produce 30–70% acceptance band, not 0–100% |

---

## Success Metrics

By end of Phase 4:

1. **f(0) ≤ 0.05** — Main orchestration overhead under 5%
2. **Membench delta ≥ +0.02** — Measurable system improvement
3. **Mission coherence ≥ 0.90** — Team focus on high-priority labels
4. **Shadow agreement > 80%** on all active formulas — High confidence in replacements
5. **Zero regressions** — No harmful mutations detected

---

**Timeline:** 4 weeks. Staffing: 1 ai-engineer (phase 1–3) + 1 data-scientist (calibration/replication).

**Cost:** ~60 tokens/session for measurement (Phase 1), ~100 tokens/session for shadow mode (Phase 2).
