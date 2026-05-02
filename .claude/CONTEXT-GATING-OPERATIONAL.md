# mth00106 — Context Gating & Wave Auto-Selection (Operational)

**Tier:** 0x (governance)  
**REPLACES:** Manual wave selection (--wave flag), context violation warnings (presend)  
**METRIC:** context_gate_violations_per_session (target: 0), RED_ALERT_avoided_per_week, w1_cache_hit_rate

---

## The Problem

Before: `/spawn --wave 1` allowed agents to launch at 85% context (violates WAVE_1_SPAWN_MAX_CONTEXT_PCT=70%). No presend gate. Users could spawn blind into compact zone.

After: `/spawn` reads altimeter.json (current context %), reads faerie2-formulas.json wave thresholds, auto-gates wave, prevents RED ALERT spawns.

---

## How It Works

1. **User invokes:** `/spawn "analyze this" --wave 2`
2. **read_altimeter()** fetches ~/.claude/altimeter.json → context_pct (live measurement)
3. **read_formulas()** fetches faerie2-formulas.json → WAVE_*_SPAWN_MAX_CONTEXT_PCT thresholds
4. **auto_determine_wave()** applies gates:
   - If context < 70% → W1 LIFTOFF (cheap parallel haiku)
   - If 70% ≤ context < 80% → W2 CRUISE (selective haiku)
   - If 80% ≤ context < 87% → W3 INSERTION (deep sonnet, background)
   - If context ≥ 87% → 🔴 RED ALERT, refuse spawn
5. **Override check:** If user provided --wave flag, validate it doesn't violate gates. Force appropriate wave if needed.
6. **Log decision** to manifest prescan_decision field (transparent to agents)

---

## Implementation

**File:** `0x_spawn.py` (mth00106 implementation)  
**Called by:** `/spawn` skill at invocation  
**Read-only dependencies:** altimeter.json (Claude CLI metrics), faerie2-formulas.json (governance)  
**Output:** Wave selected, presend warning if violated, RED ALERT if imminent

---

## Formulas Used

| Formula | Current | Min | Max | Meaning |
|---------|---------|-----|-----|---------|
| WAVE_1_SPAWN_MAX_CONTEXT_PCT | 70 | 50 | 90 | Max context for W1 (LIFTOFF cheap parallel) |
| WAVE_2_SPAWN_MAX_CONTEXT_PCT | 80 | 70 | 88 | Max context for W2 (CRUISE selective) |
| WAVE_3_SPAWN_MAX_CONTEXT_PCT | 87 | 80 | 92 | Max context for W3 (INSERTION background) |
| RED_ALERT_CONTEXT_PCT | 93 | 85 | 93.4 | Hard limit; prevent compact zone spawning |

---

## Mutation Protocol

To adjust wave thresholds (e.g., test WAVE_1_SPAWN_MAX_CONTEXT_PCT = 75 instead of 70):

1. **Measure baseline** (3 sessions at current 70%): cache_hit_rate, agents_parallelism, compact_frequency
2. **Edit:** faerie2-formulas.json, change WAVE_1_SPAWN_MAX_CONTEXT_PCT.current to 75
3. **Measure mutation** (3 sessions at new 75%): collect same metrics
4. **Analyze:** Did cache_hit_rate improve? Did parallelism increase? Did compacts decrease?
5. **Decision:** ACCEPT (update baseline to 75) | REVERT (baseline stays 70) | ITERATE (try 72%)
6. **Commit:** `git commit -m "mutation: WAVE_1_SPAWN_MAX_CONTEXT_PCT 70→75 (cache_hit +7%, parallelism +14%)"`

---

## See Also

- `faerie2-formulas.json` — All mutable parameters + baselines
- `0x_bundle_emission_pressure.sh` — Incentivizes agents to emit bundles when context >30% (paired equilibrium mechanism)
- `/spawn` skill — User-facing interface
- `MUTATION-CYCLE-GUIDE.md` (mth00087) — Framework for safe formula mutations
