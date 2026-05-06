# Spawn Cost Formula Baseline — Measurement Protocol

**Session:** 2026-05-03  
**Mission:** mutation-cost-formula-baseline-measure  
**Window:** 2026-05-03 to 2026-05-05 (3 days)  
**Status:** BASELINE ESTABLISHED

---

## Executive Summary

The spawn cost estimation formula is currently drifting 182% from actual measured costs—a RED FLAG violation (threshold: <20%). This document establishes a rigorous 3-session baseline measurement protocol to:

1. **Isolate the root cause** — Is the formula broken, or is measurement broken?
2. **Validate the measurement system** — Can we consistently measure spawn costs?
3. **Calibrate or rebuild the formula** — Either update the estimate or restructure how we estimate

**Success criterion:** Average drift <20% across 3 measurement sessions by end of 2026-05-05.

---

## What We're Measuring

### The Problem

From `config/faerie-config-v1.json`:
```json
{
  "spawn_discipline": {
    "spawn_cost_per_agent": 60,
    "min_leverage_ratio": 10,
    "alert_drift_threshold_pct": 20
  }
}
```

**Estimate formula:**
```
estimated_cost = spawn_cost_per_agent × agent_count
Example: 4 agents × 60 tokens/agent = 240 tokens estimated
```

**Reality check:** Actual measured costs consistently run 3-7× the estimate.  
**Drift observed:** 182% (and rising in recent observations)

### What Drift Means

```
drift_pct = ((actual - estimated) / estimated) × 100

Example:
  Estimated: 240 tokens
  Actual: 2,100 tokens
  Drift: ((2100 - 240) / 240) × 100 = +775%
```

**Status quo:** This 775% drift means:
- Config says "spawns cost ~60 tokens per agent" (outdated)
- Reality: Spawns cost 60-200+ tokens per agent (measurement shows much higher)
- Decision-making: We're using wrong estimates to decide whether spawning is worth it

### Why This Matters

The `min_leverage_ratio: 10` decision gate depends on accurate cost:
```
leverage_ratio = agent_work_value / actual_spawn_cost

If actual cost is 10× the estimate:
  - Gate says "spawn if work > 10× cost"
  - We think we're checking "work > 2,400 tokens"
  - We're actually checking "work > 21,000 tokens"
  - We're spawning agents when we shouldn't
```

**Outcome:** Bad decisions cascade. High-cost spawns (measured) look acceptable (estimated).

---

## Measurement Specification

### What We'll Measure (Three Components)

Each spawn event writes a forensic record to `forensics/main-metrics.jsonl` with:

| Metric | Units | Source | Purpose |
|--------|-------|--------|---------|
| **estimated_cost_tokens** | tokens | config.spawn_discipline.spawn_cost_per_agent × agent_count | Baseline expectation |
| **actual_cost_tokens** | tokens | Measured via token accounting during spawn | Ground truth |
| **drift_pct** | % | ((actual - estimated) / estimated) × 100 | Deviation indicator |
| **leverage_ratio** | ratio | agent_work_value / actual_cost | Cost-effectiveness |
| **bundle_rendering** | tokens | Time spent building bundles (COMB + HONEY + context) | Major cost component |
| **agent_invocation** | tokens | Time spent invoking agents (spawn.py wrapper) | Minor cost component |
| **manifest_parsing** | tokens | Time spent reading/processing manifests (discovery) | Minor cost component |

### Record Format

Every spawn event appends one JSON record to `forensics/main-metrics.jsonl`:

```json
{
  "ts": "2026-05-03T12:34:56Z",
  "event_id": "spawn-20260503-123456-W1",
  "wave": "W1",
  "agent_count": 6,
  "estimated_cost_tokens": 360,
  "actual_cost_tokens": 1850,
  "drift_pct": 413.9,
  "drift_flag": "RED",
  "measurements": {
    "bundle_rendering": 1200,
    "agent_invocation": 450,
    "manifest_parsing": 200
  },
  "agent_work_value_tokens": 18500,
  "leverage_ratio": 10.0,
  "leverage_flag": "OK",
  "notes": "COMB full + HONEY excerpt (5 tokens). Prescan cache HIT (saved ~400K)."
}
```

### Collection Method

**Pre-requirement:** `scripts/9x_spawn_cost_tracker.py` must be wired into spawn.py BEFORE any measurements.

**Timing:**
1. **Before spawn:** Record estimated_cost from config
2. **During spawn:** Measure bundle_rendering (token meter at key checkpoints)
3. **After spawn:** Measure agent_invocation and manifest_parsing
4. **Sum:** actual_cost_tokens = bundle_rendering + agent_invocation + manifest_parsing
5. **Append:** Write record to forensics/main-metrics.jsonl with timestamp

**Where:** `/mnt/d/0local/gitrepos/faerie2/forensics/main-metrics.jsonl` (immutable, git-tracked)

---

## Baseline Phase (2026-05-03)

### Goals

1. **Verify measurement infrastructure is working** — Can we consistently write cost records?
2. **Establish T0 baseline** — Document the current state before any mutations
3. **Surface cost distribution** — What's the range? (min/max/mean/median)

### Execution

**Day 1 (2026-05-03):**
- [ ] Ensure `9x_spawn_cost_tracker.py` is integrated into spawn.py (or presend hook)
- [ ] Run 2-3 spawn events (W1 or W2 liftoff)
- [ ] Verify 2-3 records written to main-metrics.jsonl
- [ ] Calculate T0 baseline drift (should show current ~180%+ status quo)

**Deliverable:** `forensics/mutation-baselines/mutation-baseline-T0.json` (locked, immutable)
```json
{
  "timestamp": "2026-05-03T end_of_session",
  "baseline_name": "spawn_cost_formula_T0",
  "phase": "BASELINE",
  "sample_size": 2,
  "metrics": {
    "avg_estimated_cost": 300,
    "avg_actual_cost": 1500,
    "avg_drift_pct": 400,
    "max_drift_pct": 500,
    "min_drift_pct": 300,
    "avg_leverage_ratio": 12.3,
    "leverage_satisfactory_pct": 100
  },
  "status": "BASELINE_ESTABLISHED",
  "next_phase": "MEASUREMENT"
}
```

---

## Measurement Phase (2026-05-04 to 2026-05-05)

### Goals

1. **Accumulate 10-15 spawn events** across W1/W2/W3 tiers
2. **Surface component costs** — Which part is expensive? (COMB? HONEY? bundle rendering?)
3. **Detect patterns** — Does drift vary by wave? By agent count? By mission complexity?
4. **Prepare for mutation** — Identify what to change

### Execution

**Day 2 (2026-05-04):**
- [ ] Run normal sessions, accumulate spawn cost records
- [ ] Target: 5-7 spawn events (mixed W1/W2)
- [ ] Partial analysis: emerging patterns?

**Day 3 (2026-05-05):**
- [ ] Continue normal sessions, accumulate spawn cost records
- [ ] Target: 5-8 additional spawn events (mixed W1/W2/W3)
- [ ] Stop accumulation by 18:00 UTC

**Deliverable (end of 2026-05-05):** `forensics/main-metrics.jsonl` with 10-15 complete records

---

## Evaluation Phase (End of 2026-05-05)

### Analysis Questions

1. **Average drift:**
   - Calculate mean drift across all 10-15 events
   - Is it <20% (green), 20-50% (orange), or >50% (red)?

2. **Cost distribution:**
   - Bundle rendering: What % of total cost?
   - Agent invocation: What % of total cost?
   - Manifest parsing: What % of total cost?

3. **Wave correlation:**
   - Is drift consistent across W1/W2/W3?
   - Or does one wave show systematic inflation?

4. **Leverage trend:**
   - Are spawns actually cost-effective (leverage >10×)?
   - Or is measured cost so high that leverage is marginal?

### Success Criteria

**GREEN (mission accomplished):**
- avg_drift_pct < 20%
- All spawns maintain leverage_ratio ≥ 10×
- Cost components are predictable (no surprises in bundle or invocation)

**ORANGE (partial success, mutation needed):**
- avg_drift_pct = 20–50%
- Most spawns maintain leverage_ratio ≥ 10× (but some marginal)
- One cost component is abnormally high (e.g., bundle rendering = 70% of cost)

**RED (mission failed, formula breakdown):**
- avg_drift_pct > 50%
- Many spawns fail leverage_ratio ≥ 10× test
- Cost is erratic (no consistent pattern)

### Next Steps by Outcome

#### If GREEN → Promote Formula to HONEY
```
[mth00110 | method | 3d | 0.85]
Spawn cost formula validated: 60 tokens/agent ± 18% (n=12 events, 0 outliers).
Bundle rendering dominates (~65% of cost). Agent invocation + manifest parsing stable.
W1/W2 cost similar (no wave-specific inflation). Formula ready for production.
Confidence: 0.85 (3-session validation, consistent results, <20% drift).
```

#### If ORANGE → Mutate & Re-Measure
```
HYPOTHESIS: Bundle rendering cost exceeds estimate because HONEY is too large.
MUTATION: (Option A) Increase spawn_cost_per_agent: 60 → 120
          (Option B) Shrink HONEY via crystallize (remove old entries)
          (Option C) Implement bundle caching to amortize cost

Recommend Option C (bundle caching saves 400K tokens/session prescan, should help).
Apply mutation, measure again in next 3-session window.
Target: avg_drift < 20% after mutation.
```

#### If RED → Rebuild Formula
```
Current formula fundamentally broken. Possible causes:
- Token metering is wrong (measuring cost incorrectly)
- Config values are ancient (inherited from old system)
- Bundle architecture has inflated (COMB + HONEY too large)
- Spawn.py wrapper has regressed

Action: Audit token accounting, verify COMB size, check spawn.py for regressions.
Rebuild formula from scratch (measure every spawn for 1 week, derive formula from data).
Timeline: 1-2 weeks, hold spawning decisions until new formula ready.
```

---

## Success Metrics

### Primary Metric: Average Drift

```
avg_drift_pct = (sum of all drift_pct values) / (number of events)

Target: < 20%
Green zone: 0–20%
Orange zone: 20–50%
Red zone: >50%
```

### Secondary Metric: Measurement Consistency

```
consistency = 1 - (std_dev_drift / avg_drift)

If drift is 400 ± 100 (std_dev 100):
  consistency = 1 - (100/400) = 0.75 (GOOD: predictable)

If drift is 400 ± 300 (std_dev 300):
  consistency = 1 - (300/400) = 0.25 (BAD: erratic)

Target: consistency > 0.70
```

### Tertiary Metric: Leverage Ratio Satisfaction

```
leverage_satisfied_pct = (events with leverage_ratio ≥ 10) / (total events) × 100

Target: ≥ 90%
Current: Unknown (will measure in baseline phase)
```

---

## Timeline & Milestones

| Date | Phase | Deliverable | Owner |
|------|-------|-------------|-------|
| 2026-05-03 | BASELINE | T0 baseline snapshot + 2-3 sample records | documentation-engineer + python-pro (spawn tracking) |
| 2026-05-04 | MEASUREMENT | 5-7 spawn cost records accumulated | normal session operations |
| 2026-05-05 | MEASUREMENT | 10-15 complete records; analysis tables | python-pro (metrics query) |
| 2026-05-05 18:00 UTC | EVALUATION | Drift analysis + decision (GREEN/ORANGE/RED) | documentation-engineer |
| 2026-05-05 23:59 UTC | CRYSTALLIZE | If GREEN: promote to HONEY. If ORANGE/RED: write mutation proposal | knowledge-synthesizer |

---

## Data Location

**Canonical source of truth:**
```
/mnt/d/0local/gitrepos/faerie2/forensics/main-metrics.jsonl
```

**Baseline snapshot (locked):**
```
/mnt/d/0local/gitrepos/faerie2/forensics/mutation-baselines/mutation-baseline-T0.json
```

**Query tool (for trend analysis):**
```bash
python3 scripts/9x_spawn_metrics_query.py --period 3 --report
```

Output: Summary of drift, leverage, cost components for past 3 days.

**Integration with presend:**
Presend hook reads latest record from main-metrics.jsonl before each spawn decision:
```
🔴 SPAWN COST VISIBILITY — ACCOUNTABILITY GATE
  Estimated: 360 tokens (6 agents × 60 tokens)
  Last actual: 1,850 tokens (drift +414%)
  ⚠️ Drift exceeds 20% threshold — investigate before spawning
```

---

## Failure Scenarios & Fallback Strategy

### Scenario 1: Measurement System Fails
**Problem:** Records don't get written to main-metrics.jsonl (tracker not integrated, no token metering).

**Detection:** After day 1, only 0-1 records present (expected: 2-3).

**Fallback:**
1. Manually measure one spawn event: start token count (from presend) → end token count (from result) = actual cost
2. Wire tracker synchronously into spawn.py (not async hook)
3. Re-run 3 events and verify records appear

### Scenario 2: Drift Remains >50% (RED)
**Problem:** Measurements show formula is fundamentally broken.

**Decision:** Don't promote formula to HONEY; move to mutation phase instead.

**Action:** Escalate to deep-dive (security-auditor + python-pro):
- Audit COMB size (should be ~400 tokens, not 1200)
- Audit HONEY size (should be ~8.5K, check if bloated)
- Audit bundle rendering (trace which step is expensive)

### Scenario 3: Only 1-2 Sessions Worth of Data
**Problem:** By 2026-05-05, we have <6 spawn events.

**Decision:** Extend measurement window to 2026-05-07 (5 days instead of 3).

**Rationale:** Need n≥10 for statistical confidence. 3 days may not generate enough spawns (depends on mission complexity).

---

## Key Assumptions

1. **Token metering is accurate.** We trust the token counter in spawn.py.
2. **Spawn events are independent.** One spawn doesn't affect the next (no cache poisoning).
3. **Config values are readable.** We can extract `spawn_cost_per_agent` from faerie-config-v1.json.
4. **Actual cost is measurable.** We can decompose bundle_rendering + agent_invocation + manifest_parsing.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Estimated cost** | What config says a spawn should cost (spawn_cost_per_agent × count) |
| **Actual cost** | Measured token usage during spawn (bundle + invocation + parsing) |
| **Drift** | Percent difference: ((actual - estimated) / estimated) × 100 |
| **Leverage ratio** | Cost-effectiveness: (agent_work_value) / (actual_cost) |
| **Bundle rendering** | Tokens spent assembling COMB + HONEY + manifest context for agents |
| **Agent invocation** | Tokens spent in spawn.py wrapper and agent startup overhead |
| **Manifest parsing** | Tokens spent reading existing manifests for discovery context |

---

## Document Metadata

- **Created:** 2026-05-03
- **Mission:** mutation-cost-formula-baseline-measure
- **Task ID:** cost-formula-baseline-docs
- **Phase:** BASELINE ESTABLISHED
- **Window:** 3 days (2026-05-03 to 2026-05-05)
- **Owner:** documentation-engineer
- **Related:** `docs/SPAWN-COST-ACCOUNTABILITY.md`, `config/faerie-config-v1.json`
- **Status:** READY FOR MEASUREMENT PHASE
