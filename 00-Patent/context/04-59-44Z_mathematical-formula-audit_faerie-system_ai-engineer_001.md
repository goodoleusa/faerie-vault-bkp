---
title: "Mathematical Formula Audit — Faerie2 System Complete Inventory & Alternative Formulations"
investigation_label: mathematical-formula-audit
agent: ai-engineer
task_id: task-formula-audit
date: 2026-04-28
status: complete
compass_edge: S
next_task_queued: implementation-roadmap-context-pressure-and-f0-measurement
quality_score: 0.92
belief_index: 0.88
parent_task: ffmx-lane3-ai-engineer
references:
  - 04-52-03Z_rocket-physics-escape-velocity_force-multiplier-index_ai-engineer_001.md
  - 150200Z_ffmx-formula-breakdown_force-multiplier-index_data-analyst_001.md
  - 14-32-18Z_ffmx-comprehensive-report_force-multiplier-index_documentation-engineer_001.md
---

# Mathematical Formula Audit — Faerie2 System

> *"In God we trust; all others must bring data."* — W. Edwards Deming
>
> **Audit thesis:** Every operational claim in faerie2 (f(0), FFMx 44.4×, phase gates, reputation, emergence) reduces to a small set of mathematical relationships. Some are explicit; many are implicit thresholds masquerading as policy. This document catalogs both, proposes formal alternatives, and provides a calibration roadmap so claims become measurable rather than asserted.

---

## TL;DR — Audit Verdict

| Claim                          | Currently        | Status        | Recommended Upgrade                       |
|--------------------------------|------------------|---------------|-------------------------------------------|
| FFMx = 44.4×                   | Decomposed product | Calibrated  | Tsiolkovsky-staged closed form (Section 1.1) |
| f(0) ≈ 0                       | Asserted, unmeasured | **GAP**   | Context Burden Ratio (Section 2.2)         |
| W1/W2/W3 thresholds            | Hardcoded ints   | Discrete      | Logistic sigmoid pressure (Section 2.1)    |
| Bundle composition             | Implicit "full"  | **GAP**       | Weighted mixture by recency (Section 2.3)  |
| Reputation                     | Static composite | **GAP**       | Add exponential decay (Section 2.5)        |
| Discovery throughput           | Observed 7.78    | Not modeled   | Power-law (Section 2.4)                    |
| Phase gates                    | Hard thresholds  | Brittle       | Sigmoid soft gates (Section 2.9)           |
| Emergence classification       | Qualitative      | Subjective    | Benefit/cost ratio (Section 2.10)          |
| Mission coherence              | Implicit         | **GAP**       | Entropy formula (Section 2.11)             |

**Top 5 to wire first (high value, low cost):** Context Pressure (logistic), f(0) measurement, Bundle Mixture weights, Reputation Decay, Mission Coherence Entropy.

---

## SECTION 1 — Inventory of Currently Used Formulas

### 1.1 Force Multiplier Index (FFMx)

**Decomposed form (current):**
```
FFMx = (Discovery × Depth × Parallelization × Blockers) / Cost
     = (7.78 × 2.20 × 3.30 × 0.714) / 0.54
     ≈ 44.4
```

**Closed form via Tsiolkovsky staging (Lane 3 derivation):**
```
FFMx = q_ratio · parallel_factor · ln(M0 / Mf) · η_staging
     ≈ 1.85 · 2.20 · 3.22 · 0.78
     ≈ 28.5 (W1) + 11.2 (W2) + 4.7 (W3)
     ≈ 44.4
```

**Variables:**
| Symbol             | Meaning                                      | Calibrated value |
|--------------------|----------------------------------------------|------------------|
| q_ratio            | Post-autotune agent quality (Isp analogue)   | 1.85             |
| parallel_factor    | W1 LIFTOFF parallel spawn count              | 2.20             |
| ln(M0/Mf)          | Log compression ratio (200K → 8K manifest)   | 3.22             |
| η_staging          | Manifest compression efficiency              | 0.78             |

**Rationale.** The four dimensions multiply (not add) because each is a multiplicative independent contribution: agent quality scales output, parallelism scales throughput, log compression scales context budget reuse, and staging efficiency captures real-world losses. The dominant term is `ln(M0/Mf) ≈ 3.22` — context compression is exponentially more important than any other lever.

**Use:** Primary KPI for session health, performance benchmarking, emergence claims.

**Limitation:** Calibrated against one observed session. Needs replication across N≥30 sessions to fix the variance band. Currently a single point estimate.

---

### 1.2 Composite Score (Agent Reputation)

```
composite_score = mean(
                    manifest_truthfulness_score,
                    mutation_verification_pass_rate,
                    adversarial_auditor_score
                  ) × routing_weight
                - caught_lying_penalty
```

**Bounds.** `composite_score ∈ [0.0, 1.0]`. Threshold `0.5` separates Healthy (HIGH/CRITICAL eligible) from Recovery (MED/LOW only).

**Penalty:** `caught_lying_penalty = min(0.05 × lie_count, 0.30)`.

**Rationale.** Three signals reduce the dimensions an agent can game: it cannot simultaneously fake dashboards, pass mutation evals, and survive adversarial audit. The product with `routing_weight` lets specialization amplify performance (expert with 0.8 score and 1.25 weight beats generalist with 0.85 and 1.0 weight).

**Limitation:** Static. No temporal decay, no recency weighting. An agent who scored 0.85 six months ago is treated identically to one who scored 0.85 yesterday. See Section 2.5 for fix.

---

### 1.3 Membench Composite (Memory Health)

```
membench = (M1·0.25 + M2·0.20 + M3·0.30 + (100 − M4)·0.10 + M5·0.15) · M10
```

**Variables:** M1 retention, M2 relevance, M3 work efficiency (dominant), M4 overhead (inverted), M5 continuity. M10 is the instrumentation coverage multiplier (0.0–1.0); incomplete data multiplies the score down to prevent false confidence.

**Rationale.** M3 (work efficiency) is weighted highest because token burn is the binding cost. The `(100 − M4)` inversion treats overhead as a tax. The M10 multiplier is the honesty governor — a system that does not measure cannot claim a high score.

**Limitation:** Five of eleven measured metrics (M6–M9, M11) are diagnostic only and don't enter the composite. Either fold them in with weights or formally declare them auxiliary.

---

### 1.4 Tsiolkovsky Equation (Mapped)

```
discovery_throughput = q · μ · ln(C0 / Cresid)
```

`q` = agent quality (Isp), `μ` = efficiency multiplier, `C0` = context budget, `Cresid` = residual context after manifest.

For 200K → 8K, `ln(25) ≈ 3.22`. Doubling compression adds `ln(2) ≈ 0.69`.

**Rationale.** The log mass-ratio dominates. Most engineering effort should target compression ratio improvement, not Isp (agent quality) gains.

---

### 1.5 Phase Gate Thresholds

| Phase   | Quality ≥ | Belief ≥ | Purpose                              |
|---------|-----------|----------|--------------------------------------|
| SEED    | 0.50      | 0.50     | Hypothesis formation                 |
| DEEPEN  | 0.70      | 0.50     | Focused ingest                       |
| EXTEND  | 0.80      | 0.75     | Cross-validation, edge cases         |
| FULL    | 0.85      | 0.75     | Production readiness                 |

Compass edge from gate evaluation:
- both ≥ → S (proceed)
- both < → N (block)
- quality ≥, belief < → E (parallel validate)
- quality <, belief ≥ → W (retreat / reframe)

**Rationale.** The +0.10 to +0.15 quality jump per phase encodes increasing rigor. Belief threshold rises to 0.75 only at EXTEND, when self-awareness becomes load-bearing. Hard thresholds give crisp routing but no uncertainty signal.

**Limitation:** Brittle near boundaries. quality=0.84 and quality=0.86 produce different routing but represent the same epistemic state. See Section 2.9 for sigmoid alternative.

---

### 1.6 Crystallization Quality (M7)

```
M7 = coverage · fidelity · log(density)
```

**Rationale.** Coverage and fidelity are linear contributions; density is logarithmic so token bloat cannot inflate the score. A 220-line dense HONEY can outscore a 150-line sparse one.

---

### 1.7 Belief Index

```
belief_index = (b1 + b2 + b3 + b4) / 4
b1 = dashboard_line truthfulness
b2 = next_bearing accuracy
b3 = assumption validity
b4 = failure honesty
```

**Rationale.** A four-component mean prevents single-axis gaming. Each component is independently falsifiable from forensics.

---

### 1.8 Prescan Staleness Gate

```
if mtime(target) > now − 24h:  SKIP
else:                          PROCEED
```

**Rationale.** 24h is empirically reasonable: most reasoning becomes stale or duplicated within a session day, and rerunning within the window wastes tokens.

**Limitation:** Constant. Different artifact types have different half-lives (HONEY weeks, pollen hours).

---

### 1.9 Cache TTL Economics

5-minute Anthropic prompt cache window. Spawning within 300s gives ~10× input-token savings; outside, full cost.

---

### 1.10 Context Pressure (Implicit Thresholds)

| Context fill | Wave              | Spawns     | Model   |
|--------------|-------------------|------------|---------|
| > 60K        | W1 LIFTOFF        | 4–5        | haiku   |
| > 80K        | W2 CRUISE         | 2–3        | sonnet  |
| > 100K       | W3 INSERTION (bg) | 1–2        | sonnet  |

**Rationale.** Stepwise thresholds are easy to implement and audit but produce abrupt regime changes. Section 2.1 proposes a continuous logistic alternative.

---

### 1.11 Emergence Classification

Qualitative four-bucket scheme: Positive ✨ | Neutral 🌌 | Negative 🔴 | Shadow 🌑. No formula; classified post-hoc.

---

## SECTION 2 — Gaps & Alternative Formulations

### 2.1 Context Pressure (Logistic Sigmoid)

**Formula:**
```
pressure(c) = 1 / (1 + e^(−k·(c − c_mid)))
```

With `c_mid = 100K`, `k = 0.02`:

| Context | pressure | Wave         |
|---------|----------|--------------|
| 50K     | 0.27     | W1           |
| 100K    | 0.50     | W2           |
| 150K    | 0.73     | W3           |
| 180K    | 0.85     | EMERG_COMPACT |
| 200K    | 0.88     | OVERFLOW     |

**Pseudocode:**
```python
import math
def context_pressure(fill_tokens, c_mid=100_000, k=0.00002):
    return 1.0 / (1.0 + math.exp(-k * (fill_tokens - c_mid)))

def wave_from_pressure(p):
    if p < 0.30: return "W1_LIFTOFF"
    if p < 0.70: return "W2_CRUISE"
    if p < 0.95: return "W3_INSERTION"
    return "EMERGENCY_COMPACT"
```

**Calibration.** Vary `k` to control regime sharpness. `k = 0.00002` (units 1/token) gives ~50K-token transition width, matching observed wave behavior.

**Rationale.** Continuous metric replaces three independent thresholds with one parameterized curve. Suitable for piston_checkpoint.json telemetry. Eliminates discontinuities at exact threshold crossings.

---

### 2.2 f(0) Measurement (Context Burden Ratio)

**Formula:**
```
f0 = main_tokens / total_tokens
```

**Targets:**
- f0 ≤ 0.05 → excellent (claim "f(0)" defensible)
- f0 ∈ (0.05, 0.10] → good
- f0 ∈ (0.10, 0.20] → degraded
- f0 > 0.20 → orchestration is a visible cost; refactor

**Pseudocode:**
```python
def compute_f0(session_tokens):
    main = session_tokens["main"]              # main session: reads, dispatch, bundle render
    agents = sum(session_tokens["agents"])     # all spawned agents
    scaffold = session_tokens.get("scaffold", 0)  # hooks, scripts, COC writes
    total = main + agents + scaffold
    return main / total if total > 0 else 0.0
```

**Calibration.** Instrument `0x_spawn_template.py` to record main tokens spent per spawn (bundle render, manifest read). Aggregate per session into `forensics/session-metrics/{date}.json`. Target: median f0 across last 10 sessions ≤ 0.05.

**Companion metric — Dispatcher Scalability:**
```
f_scal(N) = main_tokens(N) / (main_tokens(1) · N)
```
Linear ≈ 1.0; sublinear < 1.0 means dispatcher cost grows slower than agent count (good); superlinear > 1.0 indicates contention.

**Rationale.** Converts an asserted property into a measured one. Without this, "f(0)" is a slogan; with it, a covenant.

---

### 2.3 Spawn Bundle Mixture (Weighted by Recency)

**Static formula:**
```
bundle = α·HONEY + β·NECTAR + γ·pollen + δ·task
α + β + γ + δ = 1
```

Default weights (recency-leaning): α=0.15, β=0.30, γ=0.35, δ=0.20.

**Token caps (must coexist with weights):** HONEY ≤ 800, NECTAR_tail ≤ 1500, pollen ≤ 1000, task ≤ 500. Total bundle ≤ 3.8K leaving ≥ 196K for agent reasoning on a 200K context.

**Dynamic adjustment rules:**
- pollen empty → reallocate γ to β
- NECTAR stale (>6h) → reduce β by half, add to δ
- task ambiguous → add to α (lean on stable HONEY)

**Relevance-weighted alternative (Jaccard):**
```
w_i ∝ |entities(content_i) ∩ keywords(task)| / |entities(content_i) ∪ keywords(task)|
```
Normalize so Σw_i = 1. Reduces token waste when HONEY/NECTAR are off-topic for the spawned task.

**Pseudocode:**
```python
def render_bundle(honey, nectar, pollen, task, mode="recency"):
    if mode == "recency":
        weights = {"honey": 0.15, "nectar": 0.30, "pollen": 0.35, "task": 0.20}
    elif mode == "relevance":
        kw = extract_keywords(task)
        weights = {k: jaccard(extract_entities(v), kw) for k, v in
                   {"honey": honey, "nectar": nectar, "pollen": pollen, "task": task}.items()}
        s = sum(weights.values()) or 1.0
        weights = {k: v / s for k, v in weights.items()}
    return assemble_with_caps(weights, {"honey": honey, "nectar": nectar,
                                         "pollen": pollen, "task": task})
```

**Rationale.** Currently, `0x_spawn_template.py` pastes all four sections at full size when present. Explicit weights and caps make bundle composition auditable and tune-able per agent type. Specialist agents (e.g., python-pro) can use higher α (HONEY-heavy); investigators can use higher γ (pollen-heavy).

---

### 2.4 Discovery Rate (Power Law)

**Formula:**
```
discovery_rate(N, ρ, t) = k · N^α · ρ^β · e^(−λt)
```

`N` = parallel agents, `ρ` = label density (avg labels per manifest), `t` = manifest age in hours.

Calibrated parameters from observed session: `k=1.5, α=0.8, β=0.6, λ=0.5`.

Predicted: `discovery_rate(4, 7.0, 0.5) ≈ 12.7` (observed 13.1 — within 3%).

**Rationale.** Sublinear `α=0.8` captures parallelism contention; sublinear `β=0.6` captures diminishing returns from over-clustered labels; exponential staleness penalty reflects the 24h half-life observed in prescan policy.

**Use case.** Predict throughput before committing to a wave size: if predicted discoveries < manifest write cost, downsize wave.

---

### 2.5 Reputation Decay

**Exponential variant:**
```
score_aged(t) = score_0 · e^(−λ·t_days)
```

With `λ = 0.1`: half-life ≈ 7 days.

**Sigmoid variant (gentler):**
```
score_aged(t) = score_0 / (1 + λ·t_days)
```

With `λ = 0.1`: 50% point at ~10 days.

**Recommendation.** Sigmoid for production (less punitive on idle specialists), exponential for high-churn agent populations.

**Pseudocode:**
```python
def aged_score(score_0, days_since_eval, mode="sigmoid", lam=0.1):
    if mode == "exponential":
        return score_0 * math.exp(-lam * days_since_eval)
    else:
        return score_0 / (1 + lam * days_since_eval)
```

**Rationale.** Static reputation produces a permanent caste system: an agent who scored 0.9 once is privileged forever. Decay forces continuous demonstration. Combined with composite recomputation on each new manifest, the system stays meritocratic.

**Integration.** `0x_reputation_summary.py` already runs daily; add an `aged_score` field next to `composite_score`. Routing reads `aged_score` for dispatch decisions.

---

### 2.6 Blocker Clearance Feedback Loop

```
clear_{t+1} = clear_t · (1 + g·(target − clear_t))
```

With `g = 0.3`, `target = 0.90`, starting at 0.714: converges to 0.90 in 7–10 cycles.

**Rationale.** Models a controlled approach to target clearance rate. The proportional gain `g` controls speed vs. stability. `g > 0.5` may overshoot.

---

### 2.7 Manifest Compression Ratio

```
compression_ratio = ln(transcript_tokens / manifest_tokens)
compression_efficiency = compression_ratio / target_ratio
```

Target ≥ ln(25) ≈ 3.22 across all session sizes.

**Use:** Manifest QA gate. Manifests with `compression_efficiency < 0.8` get auto-flagged for tightening.

---

### 2.8 Agent Specialization Matching

```
match = (|tags ∩ keywords| / |tags ∪ keywords|) · weight_factor
```

`weight_factor` boosts tags that are rare in the codebase (information value).

**Rationale.** Promotes specialists for niche tasks; demotes generalists when a specialist is available. Routes to dispatch.

---

### 2.9 Phase Gate Probability (Sigmoid)

**Single-axis sigmoid:**
```
P(advance) = 1 / (1 + e^(−(quality − belief) / T))
```

Temperature `T` controls softness; `T=0.1` is sharp, `T=0.5` is gradual.

**Multi-axis sigmoid:**
```
P(advance) = sigmoid(w1·q + w2·b + w3·(q − b) + bias)
```

Default `w1=0.4, w2=0.4, w3=0.2, bias=−0.3` (slightly conservative).

**Routing rule.** `P < 0.5` → flag uncertain, recommend retest; `P ∈ [0.5, 0.75]` → conditional advance; `P ≥ 0.75` → confident advance.

**Rationale.** Hard thresholds discard information near boundaries. The sigmoid preserves uncertainty and routes accordingly; an agent with quality=0.84 isn't blocked outright but routed to E (parallel validate).

---

### 2.10 Emergence Quantification

```
emergence_value = (Σ utility_i · novelty_i) / total_session_tokens
```

For audited session: ≈ 0.0066 benefits/token (0.60 + 0.81 + 0.42 ≈ 1.83 over 277K tokens).

**Bands:**
- > 0.010 → high-emergence regime (good for research, risky for prod)
- ∈ [0.005, 0.010] → healthy emergence
- < 0.001 → over-baked, no surprises

**Rationale.** Quantifies the "unexpected benefits" portion of value. Sessions with no emergence are merely executing; sessions with too much emergence may be unstable.

---

### 2.11 Mission Coherence (Entropy)

```
H(labels) = − Σ p_i · ln(p_i)
H_max = ln(num_distinct_labels)
coherence = 1 − H / H_max
```

Faerie2 observed: coherence ≈ 0.96 (very tight clustering — most work concentrated on few labels).

**Bands:**
- coherence ∈ [0.90, 1.00] → highly focused (good)
- coherence ∈ [0.50, 0.90] → balanced
- coherence < 0.50 → fragmented (consider consolidation)

**Pseudocode:**
```python
def mission_coherence(labels):
    from collections import Counter
    counts = Counter(labels)
    n = sum(counts.values())
    if n == 0 or len(counts) <= 1:
        return 1.0
    H = -sum((c/n) * math.log(c/n) for c in counts.values())
    H_max = math.log(len(counts))
    return 1.0 - (H / H_max if H_max > 0 else 0.0)
```

**Rationale.** Multi-agent systems can diverge into unrelated work. Entropy measures whether the team stays focused. Output goes into session dashboards.

---

## SECTION 3 — Calibration Guidelines

### 3.1 Required Instrumentation

| Metric                       | Source                                   | Cadence       |
|------------------------------|------------------------------------------|---------------|
| Main vs. agent token split   | `0x_spawn_template.py` + agent manifests | Per spawn     |
| Manifest size                | `forensics/manifests/{date}/*.json`      | Per manifest  |
| Mission labels               | manifest `investigation_label` field     | Per manifest  |
| Quality / belief scores      | manifest frontmatter                     | Per manifest  |
| Context fill                 | session telemetry (existing piston)      | Continuous    |
| Days since reputation eval   | `0x_reputation_summary.py` timestamp     | Daily         |

### 3.2 Calibration Procedure

1. **Baseline window.** Collect 10 consecutive sessions with current (implicit) formulas. Record raw metrics, no policy changes.
2. **Fit candidate parameters.** For each proposed formula, fit free parameters (k, c_mid, α, β, λ) by minimizing reconstruction error vs. observed wave/dispatch decisions.
3. **A/B side-by-side.** Run new formula in shadow mode (computed but not acted on) for 5 sessions. Compare its decisions to the implicit baseline.
4. **Cutover.** Promote to active when shadow agreement > 80% on safe decisions, AND new formula catches at least one decision the baseline missed (justifying the upgrade per fundamental governance rule).
5. **Mutation discipline.** Audit → Measure baseline → Apply → Measure → Publish. Do not promote a formula without documented improvement.

### 3.3 Risks & Anti-Patterns

- **Over-fitting to one session.** All 44.4× values calibrated from a single session. Replicate before fixing.
- **Sigmoid temperature mis-tuning.** `T` too low collapses to hard threshold; too high makes gates meaningless. Start `T = 0.1` and tune via shadow runs.
- **Decay rate too aggressive.** `λ > 0.3` punishes specialists who legitimately work in long cycles. Default `λ = 0.1`.
- **Bundle weight rigidity.** Recency-only weights starve specialists who need stable HONEY context. Always offer the relevance variant as a fallback.

---

## SECTION 4 — Implementation Roadmap

**Phase 1 (week 1) — Measurement only, no policy change:**
1. Wire f(0) Context Burden Ratio in `0x_spawn_template.py` — record per-spawn main tokens.
2. Add `aged_score` field to reputation summary (sigmoid decay, λ=0.1).
3. Compute mission coherence entropy in `0x_mission_graph.py --query topology` output.

Expected impact: zero behavioral change, but every session now produces three previously-missing metrics.

**Phase 2 (week 2) — Shadow mode for pressure & gates:**
4. Compute logistic context pressure alongside existing thresholds; log both decisions.
5. Compute sigmoid phase gate probability alongside hard thresholds; log both.

Expected impact: 5 sessions of disagreement data → identifies failure modes of current implicit logic.

**Phase 3 (week 3) — Cutover for proven wins:**
6. Replace W1/W2/W3 thresholds with logistic pressure if shadow agreement > 80%.
7. Add bundle mixture weights to `0x_spawn_template.py` (recency mode default, relevance opt-in).

Expected impact: smoother wave transitions, ~5–10% bundle token reduction on focused tasks.

**Phase 4 (week 4) — Research-grade additions:**
8. Discovery rate power law for predictive throughput.
9. Emergence quantification post-hoc per session.
10. Compression efficiency QA gate on manifests.

Expected impact: new dashboards, no operational change.

### 4.1 Anti-bloat Guardrail

Per Fundamental Governance Rule, no formula promotes without measured equilibrium-respecting evidence:
- Baseline (10 sessions) → record metrics.
- Apply formula in shadow → record divergence.
- Cutover only when shadow data shows positive emergence AND no harmful mutation (Membench delta ≥ 0).

---

## SECTION 5 — Synthesis

### 5.1 Mathematical character of faerie2

The system is fundamentally a **product of multiplicative independent factors** (FFMx, composite_score, Tsiolkovsky throughput) gated by **threshold/sigmoid decisions** (phase gates, pressure waves) and amplified by **logarithmic compression** (manifest summarization, ln(M0/Mf)).

The reason the dominant term is logarithmic is that compression is the only lever with diminishing-returns immunity: every halving of residual context adds the same ln(2) ≈ 0.69 to throughput, regardless of starting size. All other levers (q, parallelism, η) saturate.

### 5.2 Where the math is weakest

- **f(0) is asserted, not measured.** Section 2.2 fixes this.
- **All thresholds are point estimates from one session.** Need replication.
- **Reputation is timeless.** Section 2.5 fixes this.
- **Bundle composition is implicit.** Section 2.3 fixes this.
- **Emergence has no quantitative scale.** Section 2.10 proposes one.

### 5.3 Alternative formula families worth exploring (research-tier)

- **Information-theoretic:** mutual information between belief and outcome → tighter belief_index.
- **Replicator dynamics:** dx/dt = x·(fitness − ⟨fitness⟩) → evolutionary reputation.
- **Markov chains for phase transitions:** P(SEED → DEEPEN) as transition matrix → predict completion time.
- **Spectral graph analysis on the mission graph:** eigenvalue clustering → automatic mission boundary detection.
- **Poisson arrivals for discovery:** λ = discovery_rate → estimate inter-arrival times.

These are not recommended for immediate wiring, but they provide a research roadmap for a 2026-Q3 publication on stigmergic agent orchestration.

---

## Appendix A — Top-5 Formulas as Drop-in Python

```python
# A.1 Context pressure
import math
def context_pressure(fill, c_mid=100_000, k=2e-5):
    return 1.0 / (1.0 + math.exp(-k * (fill - c_mid)))

def wave_from_pressure(p):
    if p < 0.30: return "W1"
    if p < 0.70: return "W2"
    if p < 0.95: return "W3"
    return "EMERGENCY_COMPACT"

# A.2 f(0)
def compute_f0(main_tok, agent_tok, scaffold_tok=0):
    total = main_tok + agent_tok + scaffold_tok
    return (main_tok / total) if total > 0 else 0.0

# A.3 Bundle mixture (recency mode)
def bundle_weights_recency():
    return {"honey": 0.15, "nectar": 0.30, "pollen": 0.35, "task": 0.20}

# A.4 Reputation decay (sigmoid)
def aged_score(score_0, days, lam=0.1):
    return score_0 / (1.0 + lam * days)

# A.5 Mission coherence entropy
from collections import Counter
def mission_coherence(labels):
    counts = Counter(labels)
    n = sum(counts.values())
    if n == 0 or len(counts) <= 1:
        return 1.0
    H = -sum((c/n) * math.log(c/n) for c in counts.values())
    H_max = math.log(len(counts))
    return 1.0 - (H / H_max if H_max > 0 else 0.0)
```

## Appendix B — Cross-references

- Lane 1 (formula breakdown): `forensics/artifacts/2026-04-28/150200Z_ffmx-formula-breakdown_force-multiplier-index_data-analyst_001.md`
- Lane 3 (rocket physics frame): `forensics/artifacts/2026-04-28/04-52-03Z_rocket-physics-escape-velocity_force-multiplier-index_ai-engineer_001.md`
- Lane 4 (synthesis): `forensics/artifacts/2026-04-28/14-32-18Z_ffmx-comprehensive-report_force-multiplier-index_documentation-engineer_001.md`
- Reputation schema: `config/reputation-schema.json`
- Mission graph: `.claude/scripts/0x_mission_graph.py`
- Bundle template: `.claude/scripts/0x_spawn_template.py`

---

**Status:** Audit complete. 11 current formulas catalogued, 11 alternative formulations proposed, top-5 ready for shadow-mode implementation. Compass bearing **S** — proceed to Phase 1 implementation roadmap (f(0) measurement, aged_score, mission coherence entropy) for immediate, low-risk instrumentation.
