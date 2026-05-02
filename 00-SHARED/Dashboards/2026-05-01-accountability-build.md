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

**Reveals:**
- Systemic drift (broken config or broken measurement?)
- Wave-by-wave efficiency (W1 always expensive?)
- Trend over time (is system improving?)
- Red flag clustering (multiple problems or one root cause?)

---

## Test Harness
**File:** `scripts/9x_spawn_cost_test_harness.py`

Simulate spawn events and demo the full accountability flow:

```bash
# Basic simulation
python3 scripts/9x_spawn_cost_test_harness.py --wave W2 --agents 4

# Scenario: HONEY bloated (high drift)
python3 scripts/9x_spawn_cost_test_harness.py --scenario high-drift

# Scenario: Small tasks (low leverage, blocks spawn)
python3 scripts/9x_spawn_cost_test_harness.py --scenario low-leverage

# Scenario: Prescan cache benefit (negative drift = optimization)
python3 scripts/9x_spawn_cost_test_harness.py --scenario prescan-benefit
```

Each scenario shows:
1. Tracker output (actual measurements)
2. Forensic event logged
3. Presend gate output (what user sees)
4. Query analysis (trending + patterns)

---

## Documentation

### For Integration
- `docs/SPAWN-COST-ACCOUNTABILITY-QUICKSTART.md` — Integration checklist, test commands
- Implementation sections added to global `CLAUDE.md`

### For Understanding
- `docs/SPAWN-COST-ACCOUNTABILITY.md` — Full design, problem/solution, workflows, mutation discipline integration

### For This Session
- `docs/SESSION-2026-05-01-ACCOUNTABILITY-BUILD.md` — Detailed build notes, what was created, next steps

---

## Global CLAUDE.md Updates

**New sections:**
1. **Bundle Architecture (COMB + HONEY)** — Immutable structure vs crystallizing wisdom
2. **Configuration System (Faerie V1)** — Centralized tweakable formulas
3. **SPAWN COST Accounting — Measured, Not Guessed** — Honest about estimates vs forensic measurement

**Key change to SPAWN COST:**
- FROM: "Per-agent cost ~60 tokens (gospel)"
- TO: "Per-agent cost ~60 tokens (TARGET ESTIMATE). Actual measured in forensics. Drift >20% is RED FLAG."

---

## How This Prevents Gaming

| Attack Vector | Old (No Measurement) | New (With Accountability) |
|---|---|---|
| **Sycophancy** | Claim "costs 240 tokens" with no proof | Presend shows "actual was 2,100" — can't hide |
| **Amnesia** | Forget real costs, re-claim old estimates | forensics/main-metrics.jsonl is permanent |
| **Silent drift** | Config estimates decay over time | Query shows avg drift +350% → forces investigation |
| **Gaming** | No consequences for over-spawning | Measured leverage ratio blocks unproductive spawns |

---

## Integration Next Steps

1. **Wire tracker into spawn.py**
   - Import `SpawnCostTracker`
   - Add `with tracker.measure(...)` around operations
   - Call `tracker.finalize()` at end

2. **Wire presend gate into presend hook**
   - Call `presend_spawn_cost_visibility.py`
   - Output goes to presend stream

3. **Evaluate in real session**
   - Run spawns
   - Check `forensics/main-metrics-summary.json` created
   - Next spawn: presend shows drift from prior spawn
   - Run query: `python3 scripts/9x_spawn_metrics_query.py --report`

4. **Measurement validation**
   - Confirm overhead <5% of spawn cost
   - Confirm drift correlates with real inefficiency
   - Adjust config estimates based on measured reality

5. **Mutation discipline integration**
   - Feed drift data into /metrics and /dev-eval
   - Use as signal: beneficial (negative drift) vs harmful (positive drift) mutations
   - Auto-update config if estimates consistently wrong

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
- `docs/SESSION-2026-05-01-ACCOUNTABILITY-BUILD.md` — Build notes

### Global Updates
- `/mnt/d/0LOCAL/.claude/CLAUDE.md` — New sections on bundles, config, spawn cost accountability

---

## Evaluation Criteria

**Measure:**
- Tracker overhead (should be <5% of spawn cost)
- Presend overhead (should be <200 tokens/turn)
- Drift accuracy (does it correlate with real inefficiency?)
- Noise vs signal (do red flags point to fixable problems?)

**Success:**
- Drift >20% always has investigable root cause
- Presend gate blocks inappropriate spawns
- Query tool reveals actionable patterns
- Sycophancy becomes impossible (math is non-deniable)

---

**Ready:** Integration can begin whenever. Test harness available for smoke tests first.

Full session notes: `docs/SESSION-2026-05-01-ACCOUNTABILITY-BUILD.md`
