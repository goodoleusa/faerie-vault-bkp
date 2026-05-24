# FFMx Forecast Function — Implementation Specification

**Task:** impl-ffmx-forecast-function (advance spec to unblock python-pro)
**Parent task:** wire-discovery-execution-pipeline
**Investigation:** terminology-cleanup-sprint
**Author:** fixer-architecture (max_velocity, in-flight discovery)
**Date:** 2026-04-28T18:48:48Z

---

## Purpose

Provide a fast (<50ms) forecast of FFMx for a candidate spawn so that `9x_discovery_promoter.py` can gate promotion at Stage 4 of the pipeline. This is **forecast**, not measurement; it runs *before* the spawn, with no actual artifacts to count.

---

## Function Contract

```python
def forecast_ffmx(
    parent_quality: float,           # parent manifest's quality_score (0.0–1.0)
    parent_belief: float,             # parent manifest's belief_index (0.0–1.0)
    parent_emergence_depth: int,      # depth of parent in DAG (0 if root)
    bearing: str,                     # "N" | "S" | "E" | "W"
    wave: str,                        # "W1" | "W2" | "W3"
    agent_type: str,                  # e.g. "python-pro", "stigmergy-scout"
    baseline_ffmx: float = 44.4,      # current locked T0 baseline
) -> ForecastResult:
    """
    Compute expected FFMx if this discovery is promoted to a spawn.

    Returns:
        ForecastResult with .score, .components, .gate_decision, .reason
    """
```

```python
@dataclass
class ForecastResult:
    score: float                      # forecast FFMx
    components: dict                  # {"A": ..., "Q": ..., "E": ..., "T": ...}
    ratio_to_baseline: float          # score / baseline_ffmx
    gate_decision: str                # "PROMOTE" | "BLOCK"
    gate_threshold: float             # 1.3 (configurable)
    reason: str                       # human-readable explanation
```

---

## Component Forecasts

### A — Artifact count forecast

```python
A_self = 1.0  # this spawn produces exactly 1 manifest

# expected number of further discoveries this spawn will emit
sub_discovery = {
    ("W1", "N"): 2.0,   # scouts that unblock prereqs spawn most
    ("W1", "S"): 1.5,   # scouts proceeding still find branches
    ("W1", "E"): 1.5,
    ("W1", "W"): 0.5,   # reframe scouts produce few children
    ("W2", "N"): 1.0,
    ("W2", "S"): 1.0,   # fixers proceed; modest follow-up
    ("W2", "E"): 1.0,
    ("W2", "W"): 0.5,
    ("W3", "N"): 0.0,   # synthesizers terminal
    ("W3", "S"): 0.0,
    ("W3", "E"): 0.5,
    ("W3", "W"): 0.0,
}.get((wave, bearing), 0.5)

A = A_self + sub_discovery
```

### Q — Quality forecast

Quality decays per generation (children inherit parent quality with a small loss):

```python
DECAY_FACTOR = 0.95
Q = parent_quality * DECAY_FACTOR
# Belief blends in to penalize promotions from low-belief parents:
Q = (Q + 0.3 * parent_belief) / 1.3
Q = max(0.0, min(1.0, Q))
```

### E — Emergence depth forecast

```python
E = parent_emergence_depth + 1
# Floor at 1 (single-spawn still has E=1)
E = max(1, E)
```

### T — Token cost forecast

Lookup table (calibrate post-30d):

```python
TOKEN_BUDGET = {
    ("W1", "haiku"): 30000,    # haiku scouts; small budget
    ("W2", "sonnet"): 80000,   # sonnet fixers; medium budget
    ("W3", "sonnet"): 60000,   # synthesizers; less than fixers because focused
    ("W1", "sonnet"): 50000,   # rare; mid-size
    ("W2", "haiku"): 40000,    # rare; cheap fixer
}
T = TOKEN_BUDGET.get((wave, _model_for(agent_type, wave)), 50000)
```

Helper:

```python
def _model_for(agent_type: str, wave: str) -> str:
    if wave == "W1": return "haiku"
    return "sonnet"
```

### Final composition

```python
k = 1.5  # FFMx exponent, locked per FFMX-EQUATION-SPECIFICATION.md
score = (A * Q * (E ** k)) / max(T, 1)  # divide-by-zero guard

# Rescale: T is in raw tokens (~50K). Multiply by token-scale to keep
# forecast on the same order of magnitude as the baseline (44.4).
# Baseline derivation used T in thousands; preserve that convention.
score_per_kt = score * 1000  # convert tokens-denominator to kilotokens
```

**Note:** the existing `7x_ffmx_calculator.py` should expose its T-units convention. If it uses raw tokens, do not multiply by 1000. **Implementation must read the calculator's convention and match it** — do not assume.

---

## Gate Logic

```python
GATE_THRESHOLD = 1.3   # 1.3x baseline forecast required for promotion
                       # NOT 1.5x — that's the publish threshold (FGR), not spawn-time

ratio = score / baseline_ffmx
if ratio >= GATE_THRESHOLD:
    gate_decision = "PROMOTE"
    reason = f"forecast {score:.2f} = {ratio:.2f}x baseline (>= {GATE_THRESHOLD}x)"
else:
    gate_decision = "BLOCK"
    reason = f"forecast {score:.2f} = {ratio:.2f}x baseline (< {GATE_THRESHOLD}x)"
```

---

## Edge Cases

| Case | Behavior |
|------|----------|
| `parent_emergence_depth` unknown | Default to 0 (treat as root spawn). Log to manifest. |
| `parent_quality` missing | Default to 0.5 (neutral). Penalizes via Q multiplier. |
| `bearing` unknown | Default to "S" (most common). Log warning. |
| `wave` unknown | Default to "W2". Log warning. |
| `agent_type` not in token table | Use 50000. Log warning. |
| `baseline_ffmx <= 0` | Raise ValueError. Calculator misconfigured. |
| `score == 0` (T saturated) | gate_decision = "BLOCK", reason = "zero forecast (T budget exhausted?)" |

**Critical override:** if the input record has `priority == "critical"`, gate returns PROMOTE regardless of forecast — but logs the override to ledger for audit.

---

## Unit Test Cases (mandatory before merge)

```python
def test_forecast_strong_parent():
    # Healthy parent, S bearing, W2 sonnet — should promote
    r = forecast_ffmx(0.92, 0.90, 0, "S", "W2", "python-pro")
    assert r.gate_decision == "PROMOTE"
    assert r.ratio_to_baseline >= 1.3

def test_forecast_weak_parent():
    # Low quality parent, W bearing, W3 — should block
    r = forecast_ffmx(0.40, 0.35, 0, "W", "W3", "general-purpose")
    assert r.gate_decision == "BLOCK"

def test_forecast_deep_emergence():
    # Depth 3 at S — exponential E should boost forecast
    r1 = forecast_ffmx(0.85, 0.80, 0, "S", "W2", "python-pro")
    r2 = forecast_ffmx(0.85, 0.80, 3, "S", "W2", "python-pro")
    assert r2.score > r1.score * 4  # E^1.5 effect

def test_forecast_unknown_bearing():
    # Should default and not crash
    r = forecast_ffmx(0.80, 0.80, 0, "?", "W2", "python-pro")
    assert r.gate_decision in ("PROMOTE", "BLOCK")  # didn't crash

def test_forecast_zero_baseline():
    with pytest.raises(ValueError):
        forecast_ffmx(0.80, 0.80, 0, "S", "W2", "python-pro", baseline_ffmx=0)
```

---

## Integration Surface

Caller in `9x_discovery_promoter.py`:

```python
from scripts.7x_ffmx_calculator import forecast_ffmx

for rec in records:
    forecast = forecast_ffmx(
        parent_quality=rec.parent_quality,
        parent_belief=rec.parent_belief,
        parent_emergence_depth=rec.parent_emergence_depth,
        bearing=rec.bearing,
        wave=rec.wave,
        agent_type=rec.agent_type,
    )
    rec.ffmx_forecast = forecast.score
    rec.gate_decision = forecast.gate_decision
    rec.gate_reason = forecast.reason
```

---

## Tuning Plan (post-deploy)

After 30 days of shadow + live data:

1. Compute *measured* FFMx for each promoted spawn (post-hoc).
2. Plot forecast vs measured. Compute calibration curve.
3. If forecasts are systematically high → raise GATE_THRESHOLD.
4. If forecasts are systematically low → recalibrate sub_discovery / TOKEN_BUDGET tables.
5. If correlation is poor (<0.3) → forecast model is wrong; redesign before tuning constants.

**Tuning is data-driven; do not hand-tune constants without the calibration data.**

---

## Honest Limits of This Forecast

- **Sub-discovery constants are educated guesses** — they encode "scouts spawn more than synthesizers" but the exact magnitudes are speculative until measured.
- **Token budget table is rough** — real burns vary 2–3x based on tool count and synthesis depth.
- **Quality decay (0.95) is uncalibrated** — could be 0.85 or 0.99; we just don't know.
- **The forecast is intentionally conservative on cost (T)** — if anything, tends to over-estimate T which under-forecasts FFMx. Bias toward fewer false-PROMOTEs is better than fewer false-BLOCKs early on.

These are explicit known unknowns; they do not invalidate the forecast as a *gate* (it still discriminates better than no gate at all = current state where 0% of discoveries promote).

---

**End of forecast function spec. Hands off to python-pro for impl-ffmx-forecast-function.**
