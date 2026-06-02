# mth00087 — Faerie2 Mutation Cycle — Semantic Formula Tuning

**Tier:** 0x (setup/governance)  
**REPLACES:** Ad-hoc formula changes, unmeasured system adjustments  
**METRIC:** mutation_iteration_time, emergence_detection_accuracy

## Quick Start: Test a Formula Change

All formulas are parameterized in `~/.claude/faerie2-formulas.json` with semantic variable names.

### 🔬 Step 1: Measure Baseline (3 Sessions)

```bash
/dev-eval --measure-baseline WAVE_1_SPAWN_MAX_CONTEXT_PCT
```

This measures:
- `cache_hit_rate` (how often do we hit prompt cache?)
- `agents_parallelism` (how many W1 agents spawned?)
- `compact_frequency` (how often does auto-compact fire?)

**Output:** Baseline metrics recorded in `piston-checkpoint.json` + `metrics-ledger.jsonl`

### 🔧 Step 2: Propose Mutation

Edit `~/.claude/faerie2-formulas.json`:

```json
"WAVE_1_SPAWN_MAX_CONTEXT_PCT": {
  "current": 70,        ← Current baseline
  "baseline": 70,       ← Original (for REVERT)
  "min": 50,
  "max": 90,
  "unit": "%"
}
```

Change `current` to test value:

```json
"WAVE_1_SPAWN_MAX_CONTEXT_PCT": {
  "current": 75,        ← Test: more aggressive W1 spawning
  ...
}
```

**Document your hypothesis in the commit message:**
```
mutation: WAVE_1_SPAWN_MAX_CONTEXT_PCT 70→75 (aggressive parallelism)

Hypothesis: Higher threshold catches cache TTL more often.
Expected: cache_hit_rate ↑, compact_frequency same, agents_parallelism ↑
Equilibrium: ✓ Does not violate f(0) principles (just timing adjustment)
```

### 📊 Step 3: Measure Mutation (3 Sessions)

```bash
/dev-eval --measure-mutation WAVE_1_SPAWN_MAX_CONTEXT_PCT
```

This measures the same metrics under the new threshold.

**Output:** Post-mutation metrics + delta (post - baseline)

### 🧪 Step 4: Analyze Results

```bash
/metrics --formula-tracking --show WAVE_1_SPAWN_MAX_CONTEXT_PCT --graph 7d
```

This shows:
- Baseline trend (3 sessions before change)
- Mutation trend (3 sessions after change)
- Delta per metric
- Positive/negative emergence signals

### ✅ Step 5: Decision

Based on results:

**ACCEPT** — Positive emergence detected
```
Example: cache_hit_rate +2%, agents_parallelism +15%, no regressions
→ Update baseline: baseline = 75 in faerie2-formulas.json
→ Commit: "mutation-accept: WAVE_1_SPAWN_MAX_CONTEXT_PCT 70→75"
```

**REVERT** — Negative emergence detected
```
Example: compact_frequency +40% (bad), agents_quality ↓
→ Revert: current = 70 (back to baseline)
→ Commit: "mutation-revert: WAVE_1_SPAWN_MAX_CONTEXT_PCT 75→70 (regressed)"
```

**ITERATE** — Mixed results, need refinement
```
Example: cache_hit_rate ↑, but agents_quality ↓ marginally
→ Try middle value: current = 72 (between 70 and 75)
→ Re-measure with 3 more sessions
→ Commit: "mutation-iterate: WAVE_1_SPAWN_MAX_CONTEXT_PCT 70→72 (tuning)"
```

---

## Available Mutable Parameters

All from `faerie2-formulas.json`:

### Wave Thresholds
- `WAVE_1_SPAWN_MAX_CONTEXT_PCT` (default 70) — Parallelism vs cache TTL
- `WAVE_2_SPAWN_MAX_CONTEXT_PCT` (default 80) — Precision vs speed
- `WAVE_3_SPAWN_MAX_CONTEXT_PCT` (default 87) — Residual context squeeze
- `RED_ALERT_CONTEXT_PCT` (default 93) — Safety margin

### Compass Quality Gates
- `COMPASS_GATE_SEED_QUALITY_MIN` (default 0.50) — Hypothesis speed vs rigor
- `COMPASS_GATE_DEEPEN_QUALITY_MIN` (default 0.70) — Investigation depth
- `COMPASS_GATE_EXTEND_QUALITY_MIN` (default 0.80) — Cross-validation coverage
- `COMPASS_GATE_FULL_QUALITY_MIN` (default 0.85) — Production readiness

### Compass Belief Gates
- `COMPASS_GATE_DEEPEN_BELIEF_MIN` (default 0.50) — Honesty tolerance
- `COMPASS_GATE_EXTEND_BELIEF_MIN` (default 0.75) — Edge case safety

### Reputation Weights
- `REPUTATION_WEIGHT_TRUTHFULNESS` (default 0.35) — Reward honest agents
- `REPUTATION_WEIGHT_KNOWLEDGE_DEPTH` (default 0.30) — Reward deep work
- `REPUTATION_WEIGHT_WISDOM` (default 0.20) — Reward collaboration
- `REPUTATION_WEIGHT_EFFICIENCY` (default 0.15) — Reward token efficiency
- `AGENT_RECOVERY_MODE_THRESHOLD` (default 0.50) — Quarantine cutoff

### Memory Loading
- `CLAUDE_MD_LOAD_TOKENS` (default 13300) — ⚠️ VIOLATES f(0), should split into 1.5K core + 8K on-demand

### Emergence Tuning
- `EMERGENCE_MULTIPLIER_BASE` (default 1.0) — Collaboration bonus scaling

---

## Equilibrium Check: Before Every Mutation

**Ask yourself:**

1. **Does this mutation change what gets measured?**
   - If yes: it's likely f(0)-compliant (metrics-driven)
   - If no: it's infrastructure change (requires equilibrium justification)

2. **Does this mutation create new work for main context?**
   - If yes: f(0) VIOLATION! Revert.
   - If no: continue.

3. **Is the measurement phase part of the test, not added overhead?**
   - If yes: f(0)-compliant
   - If no: VIOLATION! Don't add new telemetry.

4. **Does the mutation respect the 5 f(0) principles?**
   ```
   1. Stigmergy-only (no SendMessage) — ✓
   2. Artifacts-in-forensics (results live in forensics/) — ✓
   3. Task_id-in-filename (every metric tagged) — ✓
   4. Cascading summarization (dashboard_line discipline) — ✓
   5. Pressure-responsive streaming (mutate based on context%) — ✓
   ```

---

## Example: Mutation That Violates f(0)

**BAD:** "Add a new rule that checks X every spawn"
- ❌ Creates new work (checking)
- ❌ New telemetry (extra logging)
- ❌ Main context burden increases
- ❌ Violates f(0): orchestration burden ≠ 0

**GOOD:** "Raise WAVE_1_SPAWN_MAX_CONTEXT_PCT from 70 to 75"
- ✓ No new work (just a number)
- ✓ Uses existing metrics (no new telemetry)
- ✓ Zero main burden (piston reads value, decides gate)
- ✓ f(0)-compliant: mutation is data, not code

---

## Reading Results: /metrics Dashboard

Example output after running both baseline + mutation:

```
METRIC: cache_hit_rate
  Baseline (3 sessions avg):  42.3%
  Mutation (3 sessions avg):  44.8%
  Delta:                      +2.5%
  Trend:                      ↑ (consistent improvement)
  Confidence:                 HIGH (low variance)
  Verdict:                    POSITIVE EMERGENCE ✓

METRIC: agents_parallelism
  Baseline:                   4.2 agents avg per W1
  Mutation:                   4.9 agents avg per W1
  Delta:                      +0.7 agents (+16%)
  Trend:                      ↑ (consistent)
  Confidence:                 HIGH
  Verdict:                    POSITIVE EMERGENCE ✓

METRIC: compact_frequency
  Baseline:                   1.3 compacts per session
  Mutation:                   1.2 compacts per session
  Delta:                      -0.1 compacts (-8%)
  Trend:                      ↓ (slightly less)
  Confidence:                 MEDIUM (within variance)
  Verdict:                    NEUTRAL (acceptable)

OVERALL: ✓ ACCEPT mutation
  Multiple metrics improved, no regressions.
  Recommendation: Update baseline to 75, commit change.
```

---

## Batch Mutations (Advanced)

Run multiple mutations in parallel:

```bash
# Test 3 different wave threshold values simultaneously
/dev-eval --batch \
  --param WAVE_1_SPAWN_MAX_CONTEXT_PCT:70,75,80 \
  --measure-baseline --measure-mutation \
  --duration-sessions 2 \
  --compare-across-variants
```

This measures baseline + mutation for all 3 values and ranks them by emergence score.

---

## Committing Mutations

Always include formula context in commit:

```
mutation: WAVE_1_SPAWN_MAX_CONTEXT_PCT 70→75 (aggressive parallelism) ✓ ACCEPT

Baseline (3 sessions):
  cache_hit_rate:    42.3%
  agents_parallelism: 4.2
  compact_frequency:  1.3

Mutation (3 sessions):
  cache_hit_rate:    44.8% (+2.5%)
  agents_parallelism: 4.9 (+16%)
  compact_frequency:  1.2 (-8%)

Emergence: POSITIVE (multi-metric improvement, no regressions)
Equilibrium: ✓ (no new work, metrics-driven, f(0) compliant)

Co-Authored-By: Faerie Mutation Cycle <faerie@f0.ai>
```

---

## See Also

- `~/.claude/faerie2-formulas.json` — All formula definitions
- `/dev-eval --help` — Baseline + mutation measurement
- `/metrics --help` — Dashboard + graphing
- `docs/MUTATION-DISCIPLINE.md` — Full protocol
