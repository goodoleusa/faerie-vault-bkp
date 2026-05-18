# Mathematical Formulas — faerie2 System Audit (2026-04-28)

> **Audit thesis:** Every operational claim in faerie2 reduces to measurable mathematical relationships. This directory catalogs 11 current formulas, 11 alternative formulations, and a 4-phase implementation roadmap.

## Quick Links

- **Current Formulas Inventory** (Section 1): 11 formulas with rationale, calibrated values, limitations
- **Alternative Formulations** (Section 2): 11 proposed formulas with pseudocode and calibration guidelines
- **Implementation Roadmap** (Section 4): 4 phases, shadow-mode discipline, anti-bloat guardrail
- **Python Drop-ins** (Appendix A): Top-5 formulas ready for immediate implementation

## Top-5 Implementation Priorities (Phase 1, Week 1)

These are **measurement-only** (zero behavioral change) and have highest ROI:

1. **Context Pressure Logistic Sigmoid** — Replace 3 hardcoded thresholds (W1/W2/W3 at 60K/80K/100K) with continuous curve
   - Formula: `p = 1 / (1 + e^(-k·(c - c_mid)))`
   - Eliminates discontinuities at threshold crossings
   - Expected impact: smoother wave transitions

2. **f(0) Context Burden Ratio** — **CRITICAL GAP.** Currently asserted ("f(0) ≈ 0"), never measured.
   - Formula: `f0 = main_tokens / total_tokens`
   - Target: ≤ 0.05 (5% orchestration overhead)
   - Expected impact: converts slogan to covenant

3. **Spawn Bundle Mixture Weights** — Currently implicit ("paste all sections at full size")
   - Formula: `bundle = 0.15·HONEY + 0.30·NECTAR + 0.35·pollen + 0.20·task`
   - Auditable weights, token caps per layer
   - Expected impact: ~5–10% bundle token reduction on focused tasks

4. **Reputation Decay Sigmoid** — Currently static (no temporal decay)
   - Formula: `score_aged(t) = score_0 / (1 + λ·days)` where λ=0.1
   - Prevents permanent reputation caste system
   - Expected impact: meritocratic agent selection

5. **Mission Coherence Entropy** — Currently implicit ("we feel focused")
   - Formula: `coherence = 1 - H(labels) / H_max`
   - Target: ≥ 0.90 (tight clustering on few investigation_labels)
   - Expected impact: quantifies team focus

## Key Finding

**FFMx 44.4× dominant term is `ln(M₀/Mf) = 3.22`**, contributing **>70% of the multiplier**.

Engineering attention should target **compression ratio**, not agent quality. Compression is the only lever with diminishing-returns immunity: every halving adds the same ln(2) ≈ 0.69 to throughput regardless of starting size.

## The Biggest Gap

**f(0) is asserted, not measured.** The claim "orchestration burden on main ≈ 0" is not currently instrumented. Section 2.2 of the audit proposes:

```python
f0 = main_tokens / total_tokens
```

Without measurement, f(0) is marketing. With the formula, it becomes an enforceable target.

## Files in This Directory

- **formulas-current-11.md** — Inventory of 11 formulas currently in use (with calibrated values, rationale, limitations)
- **formulas-proposed-11.md** — 11 alternative formulations with pseudocode and research-grade alternatives
- **calibration-procedure.md** — How to fit parameters, shadow-mode testing, cutover criteria
- **implementation-roadmap.md** — 4-phase rollout plan (Phase 1: measurement, Phase 2: shadow, Phase 3: cutover, Phase 4: research)
- **python-drop-ins.md** — Top-5 formulas as production-ready code

## Related Artifacts

- Full audit: `/mnt/d/0local/gitrepos/faerie-vault/forensics/artifacts/2026-04-28/04-59-44Z_mathematical-formula-audit_faerie-system_ai-engineer_001.md` (631 lines)
- Manifest routing: `/mnt/d/0local/gitrepos/faerie-vault/forensics/manifests/2026-04-28/04-59-44Z_manifest_task-formula-audit_ai-engineer_001.json`
- FFMx comprehensive report: `/mnt/d/0local/gitrepos/faerie-vault/forensics/artifacts/2026-04-28/14-32-18Z_ffmx-comprehensive-report_force-multiplier-index_documentation-engineer_001.md` (now integrated with formula audit findings)

## Anti-Bloat Guardrail

Per **Fundamental Governance Rule**, no formula promotes without measured equilibrium-respecting evidence:

```
Baseline (10 sessions) 
  → measure raw metrics
Propose formula + fit parameters
  → run in shadow mode (5 sessions)
Cutover only when:
  → shadow agreement > 80% on safe decisions
  → AND new formula catches ≥1 decision baseline missed
  → AND Membench delta ≥ 0 (no harm)
```

This prevents formula churn and respects system equilibrium.

---

**Audit date:** 2026-04-28  
**Compass bearing:** S (proceed to Phase 1 implementation)  
**Quality/Belief:** 0.92 / 0.88 (EXTEND-phase pass)  
**Next task:** implementation-roadmap-context-pressure-and-f0-measurement
