# Time-Tracking Schema & Feedback Loop Design

## Overview
Closed-loop system: **Prediction → Execution → Measurement → Accuracy Analysis → Refined Prediction**.

Agents estimate task duration at spawn. After completion, actual elapsed time is recorded. Accuracy curves computed per (agent_type, task_category) enable future prediction adjustment.

---

## 1. Manifest Enhancement: Time-Tracking Fields

Add to every manifest JSON output:

```json
{
  "task_id": "string",
  "investigation_label": "string",
  "agent_type": "string",
  "task_category": "string (audit|design|implementation|synthesis|discovery)",
  
  // NEW TIME-TRACKING FIELDS
  "predicted_duration_minutes": 15,
  "actual_duration_minutes": 14.3,
  "accuracy_percent": 95.3,
  "time_tracking": {
    "estimate_source": "agent_prompt|historical_baseline|wave_adjusted",
    "wave": "W1|W2|W3",
    "model": "haiku|sonnet|opus",
    "agent_run_start_utc": "2026-04-28T04:52:00Z",
    "agent_run_end_utc": "2026-04-28T04:54:18Z",
    "elapsed_seconds": 138,
    "notes": "Overestimate by 2 min; task simpler than expected"
  },
  
  // EXISTING FIELDS
  "dashboard_line": "...",
  "compass_edge": "S",
  "quality_score": 0.91,
  "belief_index": 0.93,
  ...
}
```

### Field Definitions

| Field | Type | Range | Meaning |
|-------|------|-------|---------|
| `predicted_duration_minutes` | float | 1–1200 | Agent's estimate in prompt ("estimate 15 min") |
| `actual_duration_minutes` | float | 0.1–1200 | Clock time from agent_run_start to agent_run_end |
| `accuracy_percent` | float | -∞ to +∞ | `(predicted - actual) / predicted * 100`. Positive = underestimate (good). Negative = overestimate (bad). 100 = perfect. |
| `estimate_source` | enum | agent_prompt, historical_baseline, wave_adjusted | Where estimate came from |
| `task_category` | enum | audit, design, implementation, synthesis, discovery | Extracted from task_id or investigation_label prefix |
| `wave` | enum | W1, W2, W3 | Spawn wave (LIFTOFF, CRUISE, INSERTION) |

### Accuracy Percent Interpretation

- **+50%** = Estimated 10 min, took 5 min → Agent overestimated by 50%. Very good (conservative). Add slack to future estimates.
- **+5%** = Estimated 10 min, took 9.5 min → Nearly perfect prediction.
- **0%** = Estimated 10 min, took 10 min → Exact match.
- **-20%** = Estimated 10 min, took 12 min → Agent underestimated by 20%. Bad (missed deadline). Add buffer.
- **-50%** = Estimated 10 min, took 20 min → Agent severely underestimated. Critical (risky).

---

## 2. Task Category Detection

Extract category from task_id prefix or investigation_label:

| Prefix | Category | Examples |
|--------|----------|----------|
| `audit-*` `validate-*` `review-*` `qa-*` | **audit** | `audit-sdk-contracts`, `validate-manifest-integrity`, `qa-bundle-serialization` |
| `design-*` `plan-*` `spec-*` `architecture-*` | **design** | `design-time-tracking-w1`, `plan-data-ingest`, `spec-mcp-server` |
| `impl-*` `build-*` `code-*` `fix-*` | **implementation** | `impl-coc-writer`, `build-reputation-service`, `fix-task-id-injection` |
| `synthesis-*` `weave-*` `document-*` `narrative-*` | **synthesis** | `synthesis-and-narrative-weaving`, `document-sdk-api` |
| `discovery-*` `scan-*` `frontier-*` | **discovery** | `discovery-unblocking-work`, `frontier-scan-24h` |
| (none) | **other** | Fall back to generic bucketing |

---

## 3. Agent Type Roster

Standard agent types for bucketing:

```
general-purpose
ai-engineer
python-pro
code-reviewer
data-scientist
data-analyst
fullstack-developer
documentation-engineer
knowledge-synthesizer
research-analyst
security-engineer
devops-engineer
product-manager
```

---

## 4. Storage Location

Manifest + time-tracking data stored in existing forensics hierarchy:

```
forensics/
  manifests/
    2026-04-28/
      04-52-03Z_manifest_task-ffmx-lane3_ai-engineer_001.json  ← TIME FIELDS ADDED HERE
  
  time-tracking/  ← NEW ARTIFACT TYPE
    2026-04-28/
      14-00-00Z_accuracy-curves_summary_main_001.json          ← AGGREGATED ANALYSIS
      14-00-00Z_time-estimate-baseline_historical_main_001.json ← FUTURE PREDICTION BASELINE
```

---

## 5. Accuracy Curves Artifact

Computed daily via `8x_time_estimate_analyzer.py --generate-curves`:

```json
{
  "generated_at": "2026-04-28T14:00:00Z",
  "analysis_window_days": 7,
  "manifests_analyzed": 142,
  
  "by_agent_type": {
    "general-purpose": {
      "audit": {
        "avg_accuracy_percent": 92.3,
        "stddev": 8.1,
        "min_accuracy": 45.0,
        "max_accuracy": 156.0,
        "sample_size": 23,
        "prediction_recommendation": "Multiply baseline estimate by 0.92 (agents overestimate by 8%)"
      },
      "design": {
        "avg_accuracy_percent": 78.4,
        "stddev": 15.2,
        "min_accuracy": 23.0,
        "max_accuracy": 124.0,
        "sample_size": 12,
        "prediction_recommendation": "Multiply baseline estimate by 0.78 (agents underestimate by 22%)"
      },
      "implementation": {
        "avg_accuracy_percent": 85.1,
        "stddev": 12.4,
        "sample_size": 34,
        "prediction_recommendation": "Multiply baseline estimate by 0.85 (agents underestimate by 15%)"
      },
      "synthesis": {
        "avg_accuracy_percent": 65.3,
        "stddev": 22.7,
        "sample_size": 8,
        "prediction_recommendation": "Multiply baseline estimate by 0.65 (agents severely underestimate by 35%)"
      },
      "discovery": {
        "avg_accuracy_percent": 71.2,
        "stddev": 19.3,
        "sample_size": 5,
        "prediction_recommendation": "Multiply baseline estimate by 0.71 (add 40% buffer)"
      }
    },
    
    "code-reviewer": {
      "audit": {
        "avg_accuracy_percent": 97.8,
        "stddev": 3.2,
        "sample_size": 45,
        "prediction_recommendation": "Trust estimate at face value (±3%)"
      },
      "implementation": {
        "avg_accuracy_percent": 89.4,
        "stddev": 7.1,
        "sample_size": 31,
        "prediction_recommendation": "Add 10% buffer"
      }
    },
    
    "data-scientist": {
      "synthesis": {
        "avg_accuracy_percent": 58.7,
        "stddev": 25.4,
        "sample_size": 18,
        "prediction_recommendation": "Add 70% buffer (high variance; prefer range estimates)"
      }
    }
  },
  
  "by_wave": {
    "W1": {
      "avg_accuracy_percent": 110.2,
      "stddev": 18.3,
      "interpretation": "W1 scouts overestimate by 10% (conservative, thorough). Good for discovery phase."
    },
    "W2": {
      "avg_accuracy_percent": 98.1,
      "stddev": 5.4,
      "interpretation": "W2 fixers nearly perfect (±5%). Experienced, focused work."
    },
    "W3": {
      "avg_accuracy_percent": 52.3,
      "stddev": 28.1,
      "interpretation": "W3 synthesizers underestimate by 48% (open-ended synthesis). Always add 50% buffer."
    }
  },
  
  "correlation_matrix": {
    "accuracy_vs_quality_score": 0.34,
    "accuracy_vs_belief_index": 0.41,
    "accuracy_vs_artifact_size_bytes": -0.28,
    "accuracy_vs_citations_count": -0.19,
    "interpretation": "Belief_index has modest positive correlation with accuracy (honest agents estimate better). Large artifacts tend toward underestimation."
  }
}
```

---

## 6. Integration into Future Spawning

When `/spawn` or `/run` is invoked:

1. **Read latest accuracy_curves.json** from `forensics/time-tracking/{today}/`
2. **Extract baseline estimate** from agent prompt or task spec
3. **Look up prediction_recommendation** for (agent_type, task_category, wave)
4. **Apply adjustment factor** to baseline
5. **Inject adjusted estimate** into manifest prescan_decision or agent prompt metadata

Example:

```python
# Baseline estimate from agent prompt: "estimate 20 minutes"
baseline_estimate_minutes = 20

# Historical accuracy for general-purpose agents doing design work in W2
accuracy_curve = accuracy_curves['general-purpose']['design']
factor = accuracy_curve['avg_accuracy_percent'] / 100.0  # 0.78

# Adjusted estimate
adjusted_estimate_minutes = baseline_estimate_minutes * factor  # 20 * 0.78 = 15.6 minutes

# Inject into manifest metadata
manifest['time_tracking']['estimate_source'] = 'historical_baseline'
manifest['predicted_duration_minutes'] = round(adjusted_estimate_minutes, 1)
```

---

## 7. Wave-Specific Pressure Curves

Manifest can apply wave-specific corrections:

| Wave | Pattern | Recommendation |
|------|---------|-----------------|
| **W1 (LIFTOFF)** | Agents overestimate by 10–15% | Accuracy ~110%. Multiply baseline by **0.92** (subtract 8%). Scouts are thorough; discount their estimates slightly. |
| **W2 (CRUISE)** | Agents estimate accurately ±5% | Accuracy ~98%. Multiply baseline by **1.0** (trust estimate). Experienced, focused work. |
| **W3 (INSERTION)** | Agents underestimate by 40–50% | Accuracy ~52%. Multiply baseline by **1.5** (add 50% buffer). Synthesis is open-ended; always expect overruns. |

---

## 8. Manifest-Writing Implementation

Every agent manifest MUST include time-tracking fields:

```python
def write_manifest(task_id, dashboard_line, compass_edge, **kwargs):
    """Write manifest with time-tracking fields."""
    
    agent_run_start = kwargs.get('agent_run_start_utc')  # Set at spawn
    agent_run_end = datetime.utcnow().isoformat() + 'Z'
    
    elapsed_seconds = (agent_run_end - agent_run_start).total_seconds()
    actual_duration_minutes = elapsed_seconds / 60.0
    
    predicted_duration_minutes = kwargs.get('predicted_duration_minutes', 0)
    
    if predicted_duration_minutes > 0:
        accuracy_percent = (predicted_duration_minutes - actual_duration_minutes) / predicted_duration_minutes * 100
    else:
        accuracy_percent = 0  # Unknown estimate; skip accuracy calc
    
    manifest = {
        'task_id': task_id,
        'dashboard_line': dashboard_line,
        'compass_edge': compass_edge,
        'predicted_duration_minutes': predicted_duration_minutes,
        'actual_duration_minutes': round(actual_duration_minutes, 1),
        'accuracy_percent': round(accuracy_percent, 1),
        'time_tracking': {
            'estimate_source': kwargs.get('estimate_source', 'unknown'),
            'wave': kwargs.get('wave', 'unknown'),
            'model': kwargs.get('model', 'unknown'),
            'agent_run_start_utc': agent_run_start,
            'agent_run_end_utc': agent_run_end,
            'elapsed_seconds': int(elapsed_seconds),
            'notes': kwargs.get('time_notes', '')
        },
        # ... other fields
    }
    
    # Write to forensics/manifests/{date}/
    return manifest
```

---

## 9. Next Phase (W2 Implementation)

1. **Modify manifest schema** — add time-tracking fields to all 0x_* scripts
2. **Inject agent_run_start_utc** into bundle at spawn time (set by main)
3. **Collect historical data** — run analyzer on past 7 days of manifests
4. **Wire into /spawn** — read accuracy_curves, apply adjustments
5. **Display in dashboard** — accuracy trends per agent_type + task_category
6. **Alert on anomalies** — if agent's estimate is 2x stddev off baseline, flag for review

---

## References

- **Manifest Format:** `forensics/manifests/{YYYY-MM-DD}/{HH-MM-SS}Z_manifest_{task_id}_{agent}_{counter}.json`
- **Analyzer Script:** `scripts/8x_time_estimate_analyzer.py`
- **Integration Point:** Manifest writing via `0x_coc_writer.py` or agent ManifestWriter class
- **Historical Baseline:** `forensics/time-tracking/{date}/accuracy-curves.json`
