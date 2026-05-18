---
type: system-reference
title: Mutable System Parameters — Faerie2 Tuning Knobs
created: 2026-05-18
updated: 2026-05-18
tags: [emergence, mutable-parameters, tuning, wave-thresholds, compass-gates]
promotion_state: capture
source_path: ".claude/faerie2-formulas.json"
source_hash: "sha256:87b2df6bc77ca5a787b5d899a724078c92da7f300f56b4db9936c4dc1bfb5e6b"
doc_hash: "sha256:"
hash_ts: 2026-05-18T00:00:00Z
hash_method: body-sha256-v1
cloud_path: ""
promoted_to: ""
promoted_at: ""
---

# Mutable System Parameters — Faerie2 Tuning Knobs

**Source:** `.claude/faerie2-formulas.json` (MUTABLE_PARAMETERS section)  
**Status:** Active reference snapshot | **Last extracted:** 2026-05-18  
**Mutation discipline:** MEASURE baseline → AUDIT type → FIX formula → MEASURE post → PUBLISH

These parameters are tunable via mutation discipline. No change becomes permanent without measured equilibrium-respecting evidence. See [[03-CANONICAL-FAERIE-FORMULAS]] for the full formula context and 5-phase mutation protocol.

---

## Wave Thresholds (Piston / Context-Pressure Gates)

These thresholds gate spawn waves based on context fill percentage. The goal is to spawn hot early (W1) and conserve at high fill (W3).

| Wave | Parameter | Value | Meaning |
|------|-----------|-------|---------|
| W1 | WAVE_1_SPAWN_MAX_CONTEXT_PCT | 70% | Max context fill to allow W1 (liftoff) spawning |
| W2 | WAVE_2_SPAWN_MAX_CONTEXT_PCT | 80% | Max context fill to allow W2 (cruise) spawning |
| W3 | WAVE_3_SPAWN_MAX_CONTEXT_PCT | 87% | Max context fill to allow W3 (insertion) spawning |
| RED | RED_ALERT_CONTEXT_PCT | 93% | Auto-compact fires; no new spawns above this threshold |

**Note:** A continuous logistic sigmoid is proposed as a replacement for discrete thresholds (see 03-CANONICAL-FAERIE-FORMULAS → Context-Pressure Logistic Sigmoid). Shadow-mode validation in progress.

---

## Compass Quality Gates (Phase Exit Criteria)

Agents must meet minimum quality scores to advance from one compass phase to the next. These gates prevent low-confidence work from propagating.

| Gate | Parameter | Baseline | Current | Min | Max | Meaning |
|------|-----------|----------|---------|-----|-----|---------|
| SEED exit | SEED_QUALITY_MIN | 0.50 | 0.78 | 0.30 | 0.70 | Min quality to exit SEED phase (fast hypothesis) |
| DEEPEN exit | DEEPEN_QUALITY_MIN | 0.70 | 0.82 | 0.60 | 0.85 | Min quality to exit DEEPEN phase (focused ingest) |
| EXTEND exit | EXTEND_QUALITY_MIN | 0.80 | 0.89 | 0.70 | 0.90 | Min quality to exit EXTEND phase (cross-validation) |
| FULL exit | FULL_QUALITY_MIN | 0.85 | 0.92 | 0.80 | 0.95 | Min quality for production-ready artifact |

**Measurement source:** quality-gates-measurer (N=52, 2026-04-28). Recalibration based on pass-rate targets.

---

## Compass Belief Gates (Honesty / Self-Awareness)

Agents must demonstrate minimum self-awareness (belief index) before advancing. Low belief = agent hiding confidence.

| Gate | Parameter | Baseline | Current | Min | Max | Meaning |
|------|-----------|----------|---------|-----|-----|---------|
| DEEPEN | DEEPEN_BELIEF_MIN | 0.50 | 0.50 | 0.30 | 0.70 | Min honesty in DEEPEN phase |
| EXTEND | EXTEND_BELIEF_MIN | 0.75 | 0.75 | 0.65 | 0.90 | Min honesty for edge case exploration (safety gate) |

---

## Emergence Multiplier

Controls how strongly monkeybranching depth amplifies the mission_ffmx score.

| Parameter | Current | Min | Max | Meaning |
|-----------|---------|-----|-----|---------|
| EMERGENCE_MULTIPLIER_BASE | 1.0 | 0.5 | 2.5 | Emergence intensity knob |

**Formula:** `mission_ffmx = cross_citations × (1 + monkeybranching_depth × EMERGENCE_MULTIPLIER_BASE)`

- 0.5 = conservative (safe, low variation)
- 1.0 = balanced (current sweet spot)
- 2.5 = maximum (high risk/reward for large expeditions)

---

## Memory & Bundle Tuning

| Parameter | Baseline | Current | Min | Max | Unit | Meaning |
|-----------|----------|---------|-----|-----|------|---------|
| NECTAR_INJECTION_TOKENS | 1200 | 1200 | 800 | 3000 | tokens | Measured: 1,204 tokens (40-60% cheaper than theory) |
| HONEY_INJECTION_TOKENS | 200 | 200 | 50 | 1500 | tokens | Measured: ~200 tokens (7.5x cheaper via compression) |
| BUNDLE_EMISSION_THRESHOLD | 30 | 30 | 20 | 50 | % ctx remaining | When agents emit bundles for future scouts |

---

## Mutation Discipline Note

> **MEASURE baseline → AUDIT type → FIX formula → MEASURE post → PUBLISH**

No parameter in this table should be changed without:
1. Measuring 3-session baseline (M1–M12 + FFMx)
2. Classifying the mutation (beneficial / neutral / harmful / uncertain)
3. Pausing before reverting harmful mutations (preserve evidence)
4. Re-measuring post-fix
5. Publishing before/after deltas to HONEY.md

**Lock to HONEY only if confidence ≥ 0.80.**

---

## References

- [[03-CANONICAL-FAERIE-FORMULAS]] — Full formula context, 5-phase mutation protocol, sigmoid proposal
- [[canonical-emergence-metrics]] — FFMx formula and quality gate definitions
- [[membench-emergence-metrics]] — M1–M12 probe registry
- HONEY.md mth00420-422 — crystallized emergence formulas
