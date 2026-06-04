# Current Formulas — Inventory of 11 Formulations in Use

## 1. Force Multiplier Index (FFMx = 44.4×)

**Decomposed form (current):**
```
FFMx = (Discovery × Depth × Parallelization × Blockers) / Cost
     = (7.78 × 2.20 × 3.30 × 0.714) / 0.54 ≈ 44.4
```

**Closed form via Tsiolkovsky:**
```
FFMx = q_ratio · parallel_factor · ln(M₀ / Mf) · η_staging
     ≈ 1.85 · 2.20 · 3.22 · 0.78 ≈ 44.4
```

| Variable | Meaning | Calibrated |
|----------|---------|-----------|
| q_ratio | Agent quality (Isp analogue) | 1.85 |
| parallel_factor | W1 parallel spawn count | 2.20 |
| ln(M₀/Mf) | Log compression ratio (200K→8K) | **3.22** |
| η_staging | Manifest compression efficiency | 0.78 |

**Key insight:** `ln(M₀/Mf) ≈ 3.22` dominates (>70% of multiplier). Compression is the leverage point.

**Limitation:** Single-point calibration from one session. Needs replication across N≥30 sessions.

---

## 2. Composite Score (Agent Reputation)

```
composite_score = mean(
                    manifest_truthfulness_score,
                    mutation_verification_pass_rate,
                    adversarial_auditor_score
                  ) × routing_weight
                - caught_lying_penalty
```

**Bounds:** `[0.0, 1.0]`. Threshold 0.5 separates Healthy from Recovery.

**Penalty:** `caught_lying = min(0.05 × lie_count, 0.30)`

**Rationale:** Three independent signals prevent gaming. No single metric can be faked in isolation.

**Limitation:** Static. No temporal decay. Six-month-old score treated same as fresh score. See Section 2.5 for fix.

---

## 3. Membench Composite (Memory Health)

```
membench = (M1·0.25 + M2·0.20 + M3·0.30 + (100−M4)·0.10 + M5·0.15) · M10
```

**Metrics:**
- M1 = Retention (% prior signals surviving compaction)
- M2 = Relevance (Bleu score vs. task spec)
- M3 = Work Efficiency (output value per token) — **DOMINANT (30% weight)**
- M4 = Overhead (% scaffolding, inverted)
- M5 = Continuity (% manifests with valid routing)
- M10 = Instrumentation (0.0–1.0 multiplier; honesty governor)

**Rationale:** M3 weighted highest because tokens are the binding cost. M10 prevents false confidence from incomplete measurement.

**Limitation:** Diagnostic metrics (M6–M9) don't enter composite. Either fold them in or formally declare auxiliary.

---

## 4. Tsiolkovsky Equation (Mapped to Faerie)

```
discovery_throughput = q · μ · ln(C₀ / C_resid)
```

For 200K→8K: `ln(25) ≈ 3.22`

Doubling compression adds `ln(2) ≈ 0.69` to throughput (diminishing-returns immunity).

**Rationale:** Log dominates. Most engineering effort → compression, not Isp (quality).

---

## 5. Phase Gate Thresholds

| Phase | Quality ≥ | Belief ≥ | Purpose |
|-------|-----------|----------|---------|
| SEED | 0.50 | 0.50 | Hypothesis formation |
| DEEPEN | 0.70 | 0.50 | Focused ingest |
| EXTEND | 0.80 | 0.75 | Cross-validation |
| FULL | 0.85 | 0.75 | Production ready |

**Compass routing from gates:**
- Both ≥ → S (proceed)
- Both < → N (block)
- Quality ≥, belief < → E (parallel validate)
- Quality <, belief ≥ → W (retreat)

**Limitation:** Hard thresholds. Quality=0.84 vs. 0.86 produce different routing despite same epistemic state. See Section 2.9 for sigmoid softening.

---

## 6. Crystallization Quality (M7)

```
M7 = coverage · fidelity · log(density)
```

**Rationale:** Linear + linear + log. Prevents token bloat from inflating the score.

---

## 7. Belief Index

```
belief_index = (b₁ + b₂ + b₃ + b₄) / 4

b₁ = dashboard_line truthfulness
b₂ = next_bearing accuracy
b₃ = assumption validity
b₄ = failure honesty
```

**Rationale:** Four-component mean prevents single-axis gaming. Each falsifiable from forensics.

---

## 8. Prescan Staleness Gate

```
if mtime(target) > now − 24h: SKIP
else: PROCEED
```

**Rationale:** 24h empirically reasonable for task freshness.

**Limitation:** Constant. Different artifact types have different half-lives (HONEY weeks, pollen hours).

---

## 9. Cache TTL Economics

5-minute Anthropic prompt cache. Spawning within 300s gives ~10× input savings; outside, full cost.

---

## 10. Context Pressure (Implicit Thresholds)

| Context fill | Wave | Spawns | Model |
|--------------|------|--------|-------|
| > 60K | W1 LIFTOFF | 4–5 | haiku |
| > 80K | W2 CRUISE | 2–3 | sonnet |
| > 100K | W3 INSERTION | 1–2 | sonnet |

**Limitation:** Discrete jumps. See Section 2.1 for logistic alternative.

---

## 11. Emergence Classification

Qualitative four-bucket: Positive ✨ | Neutral 🌌 | Negative 🔴 | Shadow 🌑. No formula; post-hoc.

---

**Next:** See Proposed Formulas (Section 2) for alternatives and calibration procedures.
