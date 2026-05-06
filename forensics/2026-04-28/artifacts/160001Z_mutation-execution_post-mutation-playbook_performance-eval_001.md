# Post-Mutation Measurement Playbook
**experiment_id:** EXP-2026-04-28-f0calA1
**investigation_label:** formula-calibration-measurement-2026-04-28
**authored_by:** performance-eval (W3 INSERTION)
**authored_at:** 2026-04-28T16:00:01Z
**parent_plan:** forensics/2026-04-28/artifacts/150000Z_mutation-experiment_formula-calibration-acceptance_knowledge-synthesizer_001.md
**baseline_artifact:** forensics/2026-04-28/artifacts/160000Z_mutation-execution_baseline-metrics_performance-eval_001.json

---

## Purpose

This playbook instructs the operator (or measurement agent) how to collect post-mutation metrics across 3 consecutive sessions and compute the delta vs baseline. Mutation is already live: NECTAR=1200 tokens, HONEY=200 tokens. This playbook closes the experiment loop.

---

## Collection Trigger

Execute this playbook at the **START** and **END** of each of the next 3 sessions that use the faerie2 system. Both checkpoints matter:
- **Session START:** Capture context state before agents spawn (pre-W1)
- **Session END / handoff:** Capture manifest chain depth, compass_edge distribution, prescan rates

Sessions do not need to be consecutive calendar days — consecutive working sessions is sufficient.

---

## Step-by-Step Collection Protocol

### Step 0: Lock Other Mutations (Before Session Starts)

Confirm no other formula parameters have changed since 2026-04-28. Check:
```bash
grep -E '"current"' /mnt/d/0local/.claude/faerie2-formulas.json | head -20
```
Expected:
- NECTAR_INJECTION_TOKENS.current = 1200
- HONEY_INJECTION_TOKENS.current = 200
- All other values unchanged from their 2026-04-28 baselines

If any other value changed, **pause collection** and note the confounding mutation before proceeding.

---

### Step 1: Capture Session-Start Context State

At the very start of each session (before any agent spawns), record:

```bash
# HONEY token estimate (session start)
HONEY_TOKENS=$(wc -w ~/.claude/HONEY.md /mnt/d/0local/gitrepos/faerie-vault/.claude/HONEY.md 2>/dev/null | tail -1 | awk '{printf "%.0f", $1 * 1.3}')
echo "HONEY_TOKENS: $HONEY_TOKENS"

# NECTAR token estimate (tail-50 equivalent)
NECTAR_TOKENS=$(tail -200 ~/.claude/NECTAR.md | wc -w | awk '{printf "%.0f", $1 * 1.3}')
echo "NECTAR_TOKENS: $NECTAR_TOKENS"

# Combined bundle injection cost
echo "BUNDLE_INJECTION_COST: $((HONEY_TOKENS + NECTAR_TOKENS))"

# Current date (for forensics folder lookup)
echo "SESSION_DATE: $(date +%Y-%m-%d)"
```

Record these values in the session log template below.

**NOTE on main_context_at_W2_start:** This metric currently has no instrumentation (see ANOMALY_1 in baseline artifact). Proxy: note the approximate turn number when W2 agents first spawn. This is a manual observation for now.

---

### Step 2: Capture Session-End Manifest Metrics

After all agents have returned for the session (or at /handoff), run:

```bash
SESSION_DATE=$(date +%Y-%m-%d)
MANIFEST_DIR="/mnt/d/0local/gitrepos/faerie-vault/forensics/${SESSION_DATE}/manifests"

# Compass edge S rate
TOTAL_MANIFESTS=$(ls "$MANIFEST_DIR"/*.json 2>/dev/null | wc -l)
S_MANIFESTS=$(grep -l '"compass_edge".*"S"' "$MANIFEST_DIR"/*.json 2>/dev/null | wc -l)
echo "TOTAL_MANIFESTS: $TOTAL_MANIFESTS"
echo "S_MANIFESTS: $S_MANIFESTS"
echo "COMPASS_S_RATE: $(echo "scale=2; $S_MANIFESTS * 100 / $TOTAL_MANIFESTS" | bc 2>/dev/null || echo 'N/A (no manifests)')%"

# Prescan pass rate
PRESCAN_PASSED=$(grep -l '"prescan_decision".*"passed"' "$MANIFEST_DIR"/*.json 2>/dev/null | wc -l)
echo "PRESCAN_PASSED: $PRESCAN_PASSED"

# Manifest chain depth (manifests with non-empty next_task_queued)
CHAINS=$(grep -l '"next_task_queued"' "$MANIFEST_DIR"/*.json 2>/dev/null | xargs grep -l '"next_task_queued".*"[a-z]' 2>/dev/null | wc -l)
echo "CHAINED_MANIFESTS: $CHAINS"

# Quality and belief index (average from manifest files)
python3 -c "
import json, os, glob
manifests = glob.glob('${MANIFEST_DIR}/*.json')
qs, bis = [], []
for m in manifests:
    try:
        d = json.load(open(m))
        if 'quality_score' in d: qs.append(d['quality_score'])
        if 'belief_index' in d: bis.append(d['belief_index'])
    except: pass
print(f'AVG_QUALITY_SCORE: {sum(qs)/len(qs):.3f} (N={len(qs)})' if qs else 'AVG_QUALITY_SCORE: N/A')
print(f'AVG_BELIEF_INDEX: {sum(bis)/len(bis):.3f} (N={len(bis)})' if bis else 'AVG_BELIEF_INDEX: N/A')
"

# Agent ramp-up efficiency: manifests with investigation_label field populated
LABEL_CORRECT=$(grep -l '"investigation_label"' "$MANIFEST_DIR"/*.json 2>/dev/null | wc -l)
echo "INVESTIGATION_LABEL_POPULATED: $LABEL_CORRECT / $TOTAL_MANIFESTS manifests"
```

---

### Step 3: Record in Session Log Template

For each of the 3 sessions, fill this template:

```
POST-MUTATION SESSION [1|2|3] — Date: ___________

START METRICS:
  bundle_injection_cost:           _____ tokens
  NECTAR_actual_tokens:            _____ tokens
  HONEY_actual_tokens:             _____ tokens
  other_mutations_locked:          Y/N (if N, PAUSE — confounding mutation present)

END METRICS:
  total_manifests_this_session:    _____
  compass_edge_S_rate:             _____% (S_manifests / total)
  prescan_pass_rate:               _____% (passed / total spawns)
  chained_manifests:               _____ (non-empty next_task_queued)
  avg_quality_score:               _____ (N=___)
  avg_belief_index:                _____ (N=___)
  investigation_label_populated:   _____% of manifests
  agents_per_wave_W1_estimate:     _____ (manual observation — count parallel spawns in W1)
  main_context_at_W2_start_proxy:  turn #___ (manual observation)

BEHAVIORAL OBSERVATIONS:
  Agent confusion from smaller NECTAR?  Y/N: ___
  Compass bearing errors from HONEY?    Y/N: ___
  Anomalous manifest structure?         Y/N: ___
  Token savings observed?               _____ tokens/session estimate vs theory
```

---

### Step 4: Delta Computation (After Session 3)

After collecting all 3 sessions, compute delta vs baseline:

**Baseline values (from 160000Z artifact):**
- bundle_injection_cost: 1,404 tokens
- compass_edge_S_rate: 100% (N=1, low confidence)
- prescan_pass_rate: 100% (N=1, low confidence)
- avg_quality_score: 0.82 (N=1)
- avg_belief_index: 0.88 (N=1)
- main_context_at_W2_start: UNKNOWN

**Delta formula:**
```
metric_delta = post_mutation_avg - baseline_value
pct_delta = (metric_delta / baseline_value) * 100
```

**Fill delta table:**
```
DELTA COMPUTATION (Post-Mutation Avg - Baseline):

bundle_injection_cost_delta:         _____ tokens (expected: 0 or negative)
compass_edge_S_rate_delta:           _____% points
prescan_pass_rate_delta:             _____% points
avg_quality_score_delta:             _____
avg_belief_index_delta:              _____
agent_ramp_up_efficiency_delta:      _____% points
```

---

### Step 5: Positive/Negative Emergence Check

For each metric, classify outcome:

| Metric | Baseline | Post-Mutation | Delta | Status |
|---|---|---|---|---|
| bundle_injection_cost | 1404 tok | ___ | ___ | PASS if <=1600 |
| compass_edge_S_rate | 100% (N=1) | ___ | ___ | PASS if >=60% |
| avg_quality_score | 0.82 | ___ | ___ | PASS if >=0.70 |
| avg_belief_index | 0.88 | ___ | ___ | PASS if >=0.70 |
| prescan_pass_rate | 100% (N=1) | ___ | ___ | PASS if >=80% |

**Negative emergence thresholds (trigger ITERATE or REVERT):**
- bundle_injection_cost increases >20% above 1,404 → INVESTIGATE
- compass_edge_S_rate drops below 50% → REVERT (HONEY compression degrading guidance)
- avg_quality_score drops below 0.65 → ITERATE (NECTAR insufficient for agent ramp-up)
- avg_belief_index drops below 0.65 → ITERATE
- prescan_pass_rate drops below 70% → INVESTIGATE (duplicate work increasing)

---

### Step 6: Recommendation

Based on delta computation and emergence check, select one:

**ACCEPT** — All metrics stable or improved. No negative emergence. Baselines at 1200/200 are confirmed correct. Downstream work (bundle cost model update, wave capacity recalculation) unlocked.

**ITERATE** — One or more metrics show degradation within acceptable range. Adjust NECTAR_INJECTION_TOKENS or HONEY_INJECTION_TOKENS incrementally (e.g., NECTAR → 1400 if emergence_signal_freshness degrades). Re-run 3 sessions.

**REVERT** — Multiple negative emergence signals. Restore NECTAR to 2000, HONEY to 1500 in faerie2-formulas.json. Root-cause analysis required before retry.

---

## Anomalies Requiring Wiring Before Session 3

The following gaps were discovered in baseline collection (see baseline artifact ANOMALY fields). These are recommended wiring tasks but do NOT block this experiment:

### Gap 1: main_context_at_W2_start capture (MEDIUM priority)
- **Problem:** No instrumentation captures context% at W2 start. All historical runs show "unknown".
- **Fix:** Wire a context% log call into the W2 spawn protocol (e.g., presend_estimate.py hook logs context% at each wave boundary).
- **Investigation label:** `context-capture-instrumentation` (spawn task if resourcing permits)

### Gap 2: wave_id in manifest schema (LOW priority)
- **Problem:** Manifests don't record which wave they were spawned in. Cannot compute agents_per_wave_W1.
- **Fix:** Add `wave_id` field to manifest schema (one line addition to spawn template).
- **Investigation label:** `manifest-schema-wave-id-wiring`

### Gap 3: manifest chain depth collection timing (LOW priority)
- **Problem:** Chain depth of 1 at session START is not meaningful (chains grow during session).
- **Fix:** Collect manifest_chain_depth at session END (after /handoff), not at session start.
- **Already addressed in this playbook:** Step 2 instructs end-of-session collection.

---

## Downstream Work (Unlocked on ACCEPT)

Per experiment plan section "Downstream Work (Next Bearing)":

1. **Bundle cost model update** — Update 0x_spawn_template.py to use new token budgets (1,400 instead of 4,500 per agent).
2. **Wave capacity recalculation** — (182,000 - per_task_instructions) / 1,404 per agent. W1 can support ~130 theoretical agents vs ~40 previously (practical limit: wave gates + task complexity).
3. **COMPASS_QUALITY_GATES experiment** — Unblocked once N>=20 sessions collected. Same template applies.
4. **NECTAR min/max bounds review** — min=800 now plausible as real operating point; max=3,000 likely obsolete.

---

## Experiment Summary (For Manifest)

**Pre-registration confirmed:**
- Hypothesis: NECTAR=1200, HONEY=200 reduces bundle cost ~3,096 tokens/agent with no behavioral degradation
- Primary KPI: bundle_injection_cost (target: <=1,600, achieved: 1,404 in session 1)
- Secondary KPIs: compass_edge_S_rate, avg_quality_score, avg_belief_index
- Measurement window: 3 post-mutation sessions (this document)

**Session 1 baseline result:** PASS on bundle_injection_cost (1,404 tokens, within 1,200-1,600 range); N=1 directional evidence for all other metrics.

**Expected ACCEPT path:** All metrics stable across 3 sessions → lock baselines → proceed to downstream work.
