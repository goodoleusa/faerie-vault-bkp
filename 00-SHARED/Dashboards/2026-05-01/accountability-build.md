---
type: accountability-build
created: 2026-05-01T00:00:00Z
tags: [spawn-cost-accountability, faerie, accountability-build]
parent: ../Dashboards.md
mission_field: spawn-cost-accountability
compass_edge: null
hash: pending
---

> [↑ Dashboards](../Dashboards.md) · [⌂ Home](../../HOME.md)

# Spawn Cost Accountability Infrastructure — Build Complete

**Date:** 2026-05-01  
**Status:** Ready for integration and evaluation  
**Problem solved:** Sycophancy + amnesia in spawn cost estimates

---

## The Vulnerability

User identified the critical gap:
> "Isn't this setting yourself up to game the system and lie about tokens because of sycophancy and amnesia?"

**Spawn cost estimates (60 tokens/agent) were documented but unmeasured.** Future sessions could:
- Claim low cost with no forensic proof
- Inherit false estimates and forget actual spending
- Game the system by under-estimating and over-spending silently

**Solution:** Build forensic accountability infrastructure that makes gaming impossible.

---

## Three-Layer System Built

### 1. Measurement Layer
**File:** `scripts/9x_spawn_cost_tracker.py`

```python
tracker = SpawnCostTracker(wave_type='W2', agent_count=4)

with tracker.measure('bundle_rendering'):
    bundles = render_bundles(...)

with tracker.measure('agent_invocation'):
    manifests = [Agent(...) for i in range(4)]

tracker.finalize(estimated_cost=240, agent_work_value=400000)
# Logs: {estimated: 240, actual: 2100, drift: +775%, leverage: 190×}
```

**Output:** Immutable `forensics/main-metrics.jsonl` with full event details
- Per-spawn: estimated vs actual cost pair
- Drift percentage (alarm if >20%)
- Leverage ratio (alarm if <10×)
- Measurement breakdown (which operations expensive?)

### 2. Visibility Layer
**File:** `hooks/presend_spawn_cost_visibility.py`

Every turn shows (can't ignore):
```
🔴 Spawn cost: est 240→act 2100 (+775%) | 🟢 Leverage: 190× (min 10×)
```

**Why this matters:**
- Presend output is non-deniable
- Drift appears right at spawn decision point
- Prevents silent gaming of estimates

**Overhead:** ~200 tokens (read 1KB summary + template output)

### 3. Query Layer  
**File:** `scripts/9x_spawn_metrics_query.py`

Detect systemic patterns and force investigation:

```bash
# Summary (7 days)
python3 scripts/9x_spawn_metrics_query.py --period 7 --report

# Red flags only
python3 scripts/9x_spawn_metrics_query.py --drift --report

# By wave
python3 scripts/9x_spawn_metrics_query.py --waves W1,W2,W3 --report
```

---

## How This Prevents Gaming

| Attack Vector | Old (No Measurement) | New (With Accountability) |
|---|---|---|
| **Sycophancy** | Claim "costs 240 tokens" with no proof | Presend shows "actual was 2,100" — can't hide |
| **Amnesia** | Forget real costs, re-claim old estimates | forensics/main-metrics.jsonl is permanent |
| **Silent drift** | Config estimates decay over time | Query shows avg drift +350% → forces investigation |
| **Gaming** | No consequences for over-spawning | Measured leverage ratio blocks unproductive spawns |

---

## Files Created

### Core Infrastructure
- `scripts/9x_spawn_cost_tracker.py` (190L) — Measurement
- `hooks/presend_spawn_cost_visibility.py` (40L) — Presend gate
- `scripts/9x_spawn_metrics_query.py` (280L) — Forensic query
- `scripts/9x_spawn_cost_test_harness.py` (280L) — Test harness

### Documentation  
- `docs/SPAWN-COST-ACCOUNTABILITY.md` — Full design
- `docs/SPAWN-COST-ACCOUNTABILITY-QUICKSTART.md` — Integration guide

---

**Source artifact:** `forensics/artifacts/` (faerie2 repo)  
Full session notes: `docs/SESSION-2026-05-01-ACCOUNTABILITY-BUILD.md`
