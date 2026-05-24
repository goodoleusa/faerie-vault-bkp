# EVAL-AUTOMATION-DESIGN.md

Eval system audit and automation design for faerie2.
Generated: 2026-04-06 | Agent: performance-eval

---

## 1. Current State — What Runs, When, and Gaps

### 1.1 Trigger Map (audited from settings.json + SKILL.md)

| Trigger | What runs | Notes |
|---|---|---|
| `Stop` hook | `eval_harness.py --auto` | `--auto` flag is unrecognized; falls through to full eval path (same as `--json`). Side effect: writes system-eval.json every session stop. |
| `Stop` hook | `write_eval_mirror.py` | Secondary eval mirror writer (unknown output path — not audited) |
| `/faerie` Wave 0 bash | `eval_harness.py --quick` | Reads cached `system-eval.json`, prints statusline snippet. Does NOT recompute. Safe. |
| `UserPromptSubmit` | `health_check.py --brief` | Generic health; does NOT read eval-alerts or blockages. |
| Manual / on-demand | `eval_harness.py --report` or `--json` | Full recompute + auto-queue improvements. Only path that writes auto-queued tasks. |
| `SubagentStop` | `scratch_collector.py --brief` | Collects agent scratch — feeds eval indirectly. |
| Never (gap) | `eval_harness.py --check-blockages` | Does not exist. |
| Never (gap) | eval-alerts.json write | Not wired anywhere. |
| Never (gap) | eval-blockages.json write | Not wired anywhere. |
| Never (gap) | training-queue auto-update from eval score | Manual only — no script wired between eval score and training-queue. |
| Never (gap) | performance-eval agent auto-spawn | Manual only. Faerie does not spawn it automatically. |

### 1.2 How `--quick` Works

`--quick` reads the cached `system-eval.json` and prints `statusline_snippet`. It does NOT recompute scores. This is correct: it is fast (<100ms), suitable for Wave 0 injection. The statusline snippet (`eval:0.41→`) appears in the faerie dashboard if faerie reads it.

Gap: faerie's Wave 0 bash runs `--quick` and captures the output, but the SKILL.md does not explicitly surface it as a HIGH-alert section in the dashboard. It is printed but may be visually buried.

### 1.3 Regression Detection — Exists but Not Surfaced

`detect_regression()` in `eval_harness.py` computes regression alerts against a 3-entry rolling average of `eval-history.jsonl`. Regressions are injected into `system-eval.json` under `alerts[]` and `regression_alerts[]`. However:

- `faerie` Wave 0 reads `system-eval.json` via `--quick` (which reads `alerts[]`)
- But `alerts[]` is not listed as a HIGH-alert source in faerie's SKILL.md Step 0 parsing
- No file named `eval-alerts.json` exists — regressions are embedded in `system-eval.json` only
- No task is auto-queued when a regression is detected (the `auto_queue_improvements()` path handles below-target dimensions, not regressions)

### 1.4 Training Queue Integration — Manual Only

When an agent beats its prior score, the protocol in the agent card and SKILL.md says to:
1. Run `beat_last_verifier.py` (does not exist — prop-20260319-002 is pending)
2. Update agent card manually
3. Remove from training-queue.json manually

There is no automated link between `eval_harness.py` scoring a run and updating `training-queue.json`. It is fully manual.

### 1.5 `--auto` Flag — Unrecognized

The Stop hook calls `eval_harness.py --auto`. This flag is not implemented in the script. It falls through to the full eval path (writes system-eval.json, appends eval-history.jsonl, but does NOT auto-queue since `--report` and `--json` are not in args). This is a latent bug: the intent was likely `--json` behavior at stop time.

### 1.6 Overnight Batch Eval — Not Wired

The `batch_dispatcher.py --submit` runs at Stop. There is no mechanism to queue eval computations to the Batch API for overnight execution.

---

## 2. Gaps Summary (prioritized)

| # | Gap | Impact | Priority |
|---|---|---|---|
| G1 | Regression alerts not surfaced to faerie dashboard | Regressions silently accumulate | HIGH |
| G2 | `eval-blockages.json` does not exist — blockage detection absent | Stale evals go unnoticed | HIGH |
| G3 | `--auto` flag unrecognized in eval_harness — auto-queue improvements never fire at Stop | Dimension failures not auto-queued | HIGH |
| G4 | `eval-alerts.json` not written — no machine-readable alert file for downstream consumers | Faerie can't parse alerts reliably | HIGH |
| G5 | Training-queue not auto-updated from eval scores | Beat-last goes unrecorded until human notices | MED |
| G6 | `beat_last_verifier.py` missing | Agent self-update is error-prone | MED |
| G7 | `/faerie` dashboard does not explicitly surface eval alerts as HIGH section | Alerts buried in statusline | MED |
| G8 | Overnight batch eval not wired | Cost savings opportunity missed | LOW |
| G9 | `--quick` not re-running on first UserPromptSubmit if eval is >24h stale | Stale statusline served to dashboard | LOW |

---

## 3. Recommended Automation (by priority)

### HIGH — Wire These First

#### G3 Fix: Recognize `--auto` in eval_harness.py

In `main()`, add:
```python
if "--auto" in args:
    # Alias: behave like --json but also auto-queue improvements
    args = [a if a != "--auto" else "--json" for a in args]
    # Fall through to full eval + auto_queue path
```

This makes Stop hook `eval_harness.py --auto` actually write auto-queued tasks. Currently the most impactful single fix.

#### G4 + G1 Fix: Write `eval-alerts.json` from eval_harness

After computing regressions and alerts, write a separate machine-readable file:

**Path:** `~/.claude/hooks/state/eval-alerts.json`

**Format:**
```json
{
  "generated_at": "ISO8601",
  "composite_score": 0.41,
  "composite_delta": 0.0,
  "trend": "flat",
  "alerts": [
    {
      "type": "REGRESSION",
      "dimension": "THROUGHPUT",
      "severity": "HIGH",
      "drop_pct": -18,
      "avg_baseline": 0.45,
      "new_value": 0.37,
      "action": "queue investigation",
      "ts": "ISO8601"
    }
  ],
  "dimensions_below_target": ["throughput", "quality"],
  "last_eval_ts": "ISO8601",
  "eval_age_hours": 2.1,
  "stale": false
}
```

Write location: after `SYSTEM_EVAL.write_text(...)` in `main()`.

#### G2 Fix: Implement `eval_harness.py --check-blockages`

A blockage is defined as any of:
- Last eval is >24h old (`eval_age_hours > 24`)
- Last 3 evals all errored or have `composite_score == null`
- Any dimension has been in bootstrap_mode for >7 days with no data improvement
- `eval-history.jsonl` has not been updated in >3 sessions

**Output path:** `~/.claude/hooks/state/eval-blockages.json`

**Format:**
```json
{
  "generated_at": "ISO8601",
  "has_blockages": true,
  "blockages": [
    {
      "type": "stale_eval",
      "description": "Last eval ran 31h ago — exceeded 24h threshold",
      "severity": "HIGH",
      "action": "run eval_harness.py --json immediately",
      "auto_task": true
    },
    {
      "type": "bootstrap_stuck",
      "dimension": "throughput",
      "description": "THROUGHPUT in bootstrap mode for 8 days — instrumentation broken",
      "severity": "HIGH",
      "action": "fix session-metrics.jsonl tasks_completed field",
      "auto_task": true
    }
  ],
  "auto_queued_tasks": ["task-20260406-eval-unblock-001"]
}
```

Wire `--check-blockages` into the Stop hook BEFORE the main eval call:
```json
{
  "type": "command",
  "command": "python3 /mnt/c/Users/amand/.claude/scripts/eval_harness.py --check-blockages 2>/dev/null || true",
  "timeout": 5
}
```

When `has_blockages=true` and `auto_task=true`, call `queue_ops.py add` with `priority=HIGH`:
```bash
python3 ~/.claude/hooks/state/queue_ops.py add \
  --goal "Unblock eval: {blockage.description}" \
  --priority HIGH \
  --project faerie \
  --category eval \
  --recommended_agent performance-eval
```

### MED — Wire Within Next Sprint

#### G7 Fix: Faerie Wave 0 — Surface Eval Alerts as HIGH Section

In faerie SKILL.md Step 0, add after the `--quick` call:

```bash
cat ~/.claude/hooks/state/eval-alerts.json 2>/dev/null
cat ~/.claude/hooks/state/eval-blockages.json 2>/dev/null
```

Dashboard rendering rule: if `eval-alerts.json` has `alerts[]` with any `severity=HIGH`:
- Add to dashboard under `## ALERTS (HIGH)` section
- Format: `EVAL REGRESSION: {dimension} dropped {drop_pct}% — action: {action}`

If `eval-blockages.json` has `has_blockages=true`:
- Add to dashboard under `## BLOCKED` section
- Format: `EVAL BLOCKED: {blockage.description} — task queued: {auto_queued_tasks[0]}`

#### G5 + G6 Fix: Auto-update training-queue from eval scores

After `detect_regression()` in eval_harness `main()`, add a `_update_training_queue()` call:

1. Read `training-queue.json`
2. For each agent in the roster with a run in the last session:
   - Compare current score to agent card's last training score
   - If beat: set `status="redeemed_on_the_job"`, append redemption entry to `training-log.jsonl`
   - If not beat and `on_the_job_eligible=true`: update score, log miss
3. Write updated `training-queue.json`

This requires `beat_last_verifier.py` (G6) to be created first (prop-20260319-002).

### LOW — Opportunistic

#### G8: Overnight Batch Eval

At Stop hook, if session ran >20 turns (heavy session), append an eval task to `overnight-queue.json`:
```json
{
  "task": "eval_harness --json --report",
  "session_id": "...",
  "queued_at": "ISO8601",
  "reason": "heavy session — full eval deferred to batch"
}
```

Morning `/faerie` Wave 0 reads `batch_collect.py` (already wired) and includes overnight eval results in dashboard.

#### G9: Stale Eval Detection at UserPromptSubmit

In `UserPromptSubmit` hook (pre-session.py or health_check.py), check `eval-alerts.json.eval_age_hours`. If >24, inject a brief to the statusline: `eval:STALE(31h)` instead of cached snippet.

---

## 4. Blockage Detection Protocol

A "blockage" is a condition where the eval system cannot produce reliable scores.

### Blockage Types

| Type | Detection | Severity | Auto-action |
|---|---|---|---|
| `stale_eval` | Last eval >24h ago | HIGH | Queue eval run |
| `consecutive_errors` | Last 3 evals all null composite | HIGH | Queue eval debug |
| `bootstrap_stuck` | Dimension in bootstrap >7 days with no data points added | HIGH | Queue instrumentation fix |
| `history_stalled` | eval-history.jsonl not updated in >3 sessions | MED | Queue eval run |
| `score_below_floor` | composite < 0.30 for 2+ consecutive evals | HIGH | Queue investigation |
| `alerts_unread` | eval-alerts.json has HIGH severity alerts >48h old | MED | Queue human review |

### Detection Script: `eval_harness.py --check-blockages`

Run: at Stop hook, before main eval. Also runnable manually.
Output: `eval-blockages.json` (always written, even if empty).
Side effect: if `auto_task=true` blockages found, calls `queue_ops.py add`.

---

## 5. Faerie Dashboard Integration Points

### Wave 0 additions (Step 0 bash block in SKILL.md)

```bash
# Add these two lines to Wave 0:
cat ~/.claude/hooks/state/eval-alerts.json 2>/dev/null
cat ~/.claude/hooks/state/eval-blockages.json 2>/dev/null
```

### Dashboard rendering rules

```
IF eval-blockages.json has has_blockages=true:
  Add to ## HIGH ALERTS section:
    EVAL BLOCKED: {blockage.description}
    Auto-task: {auto_queued_tasks[0] or "none queued"}

IF eval-alerts.json has alerts[].severity=HIGH:
  Add to ## WATCH section:
    EVAL REGRESSION [{dimension}]: -{drop_pct}% vs 3-run avg
    Action: {action}

IF eval_age_hours > 12:
  Add to ## STALE section:
    EVAL STALE: last ran {eval_age_hours}h ago
```

### Statusline enhancement

Current: `eval:0.41→`
Proposed: `eval:0.41→ !REGRESSION:THROUGHPUT` (when `alerts[]` non-empty in system-eval.json)

The `--quick` path already reads `alerts[]` and appends the first alert. This is already implemented. The gap is only in faerie's rendering of it.

---

## 6. Implementation Order

| Step | Action | File(s) | Effort |
|---|---|---|---|
| 1 | Fix `--auto` flag in eval_harness.py | `eval_harness.py` | 15 min |
| 2 | Add `eval-alerts.json` write after main eval | `eval_harness.py` | 20 min |
| 3 | Implement `--check-blockages` with auto-queue | `eval_harness.py` | 45 min |
| 4 | Wire `--check-blockages` into Stop hook | `settings.json` | 5 min |
| 5 | Add eval-alerts + eval-blockages reads to faerie Wave 0 | `skills/faerie/SKILL.md` | 10 min |
| 6 | Create `beat_last_verifier.py` | new script | 30 min |
| 7 | Wire training-queue auto-update from eval scores | `eval_harness.py` | 45 min |
| 8 | Overnight batch eval queue | `eval_harness.py`, `overnight-queue.json` | 30 min |

Total estimated: ~3.5 hours for HIGH+MED gaps (steps 1-7).

---

## 7. Files Referenced

| File | Role | Exists? |
|---|---|---|
| `~/.claude/scripts/eval_harness.py` | Main eval engine | Yes |
| `~/.claude/hooks/state/system-eval.json` | Cached eval output | Yes |
| `~/.claude/hooks/state/eval-history.jsonl` | Hash-chained eval history | Yes (presumed) |
| `~/.claude/hooks/state/eval-alerts.json` | Machine-readable alert file | No — to create |
| `~/.claude/hooks/state/eval-blockages.json` | Blockage detection output | No — to create |
| `~/.claude/hooks/state/eval-rule-proposals.json` | Rule change proposals | Yes |
| `~/.claude/hooks/state/training-queue.json` | Agent training queue | Yes |
| `~/.claude/hooks/state/beat_last_verifier.py` | Beat-last score checker | No — to create |
| `~/.claude/hooks/state/training-log.jsonl` | Redemption log | Yes (presumed) |
| `~/.claude/skills/faerie/SKILL.md` | Faerie orchestrator skill | Yes |
| `~/.claude/settings.json` | Hook configuration | Yes |
