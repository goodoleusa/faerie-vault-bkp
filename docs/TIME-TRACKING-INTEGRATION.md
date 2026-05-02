# Time-Tracking Integration Guide — W2 Implementation Roadmap

## Overview

The time-tracking feedback loop closes the estimate → execution → measurement → refinement cycle. This guide walks through implementation steps for W2 (CRUISE) execution phase.

---

## Phase 1: Manifest Enhancement (W2 Week 1)

### Step 1: Update ManifestWriter Class

All manifest-writing code must capture time data. Typical locations:

- `scripts/0x_coc_writer.py` — if agents use this for atomic manifest writes
- SDK harness `agent_sdk/manifest_writer.py` — if building faerie SDK
- Agent subclass implementations — if agents override write methods

**Implementation pattern:**

```python
class ManifestWriter:
    def __init__(self, agent_run_start_utc: str):
        self.agent_run_start_utc = agent_run_start_utc  # Injected at spawn
        self.manifest_data = {}

    def write(self, task_id: str, dashboard_line: str, compass_edge: str, **kwargs):
        """Write manifest with time-tracking fields."""
        
        from datetime import datetime
        
        agent_run_end = datetime.utcnow().isoformat() + 'Z'
        
        # Parse ISO timestamps
        start_dt = datetime.fromisoformat(self.agent_run_start_utc.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(agent_run_end.replace('Z', '+00:00'))
        elapsed_seconds = (end_dt - start_dt).total_seconds()
        actual_minutes = elapsed_seconds / 60.0
        
        predicted_minutes = kwargs.get('predicted_duration_minutes', 0)
        
        # Calculate accuracy
        if predicted_minutes > 0:
            accuracy_percent = (predicted_minutes - actual_minutes) / predicted_minutes * 100
        else:
            accuracy_percent = 0
        
        # Extract task category
        task_category = self._extract_task_category(task_id, kwargs.get('investigation_label', ''))
        
        self.manifest_data = {
            'task_id': task_id,
            'investigation_label': kwargs.get('investigation_label', 'unknown'),
            'agent_type': kwargs.get('agent_type', 'unknown'),
            'task_category': task_category,
            'dashboard_line': dashboard_line,
            'compass_edge': compass_edge,
            'predicted_duration_minutes': round(predicted_minutes, 1),
            'actual_duration_minutes': round(actual_minutes, 1),
            'accuracy_percent': round(accuracy_percent, 1),
            'time_tracking': {
                'estimate_source': kwargs.get('estimate_source', 'unknown'),
                'wave': kwargs.get('wave', 'unknown'),
                'model': kwargs.get('model', 'unknown'),
                'agent_run_start_utc': self.agent_run_start_utc,
                'agent_run_end_utc': agent_run_end,
                'elapsed_seconds': int(elapsed_seconds),
                'notes': kwargs.get('time_notes', '')
            },
            # ... other manifest fields
        }
        
        # Write atomically to forensics/manifests/{date}/
        return self._write_to_forensics()

    @staticmethod
    def _extract_task_category(task_id: str, investigation_label: str) -> str:
        """Extract task category from task_id or investigation_label."""
        # Use same logic as 8x_time_estimate_analyzer.py
        prefixes = {
            'audit': ['audit-', 'validate-', 'review-', 'qa-'],
            'design': ['design-', 'plan-', 'spec-', 'architecture-'],
            'implementation': ['impl-', 'build-', 'code-', 'fix-'],
            'synthesis': ['synthesis-', 'weave-', 'document-', 'narrative-'],
            'discovery': ['discovery-', 'scan-', 'frontier-'],
        }
        
        full_text = (task_id + ' ' + investigation_label).lower()
        
        for category, prefix_list in prefixes.items():
            for prefix in prefix_list:
                if prefix in full_text:
                    return category
        
        return 'other'
```

### Step 2: Inject agent_run_start_utc at Spawn

When spawning agents, the main must inject the start timestamp. Update spawn logic:

```python
# In main spawn flow (0x_mission_graph.py --spawn or /run)

from datetime import datetime

agent_run_start_utc = datetime.utcnow().isoformat() + 'Z'

# For SDK-based spawning:
result = agent_sdk.spawn(
    subagent_type='general-purpose',
    prompt=bundle,
    metadata={
        'agent_run_start_utc': agent_run_start_utc,
        'predicted_duration_minutes': 20,  # From agent prompt estimate
        'estimate_source': 'agent_prompt',  # or 'historical_baseline' or 'wave_adjusted'
        'wave': 'W2',
        'model': 'haiku'
    }
)

# Manifest writer receives this in kwargs
manifest_writer = ManifestWriter(agent_run_start_utc=agent_run_start_utc)
manifest_writer.write(
    task_id='design-time-tracking-w1',
    dashboard_line='Time tracking schema designed; ...',
    compass_edge='S',
    predicted_duration_minutes=20,
    estimate_source='agent_prompt',
    wave='W2',
    **metadata
)
```

### Step 3: Parse Estimate from Agent Prompt

Agents include time estimates in their spawning prompt. Parse pattern:

```
"estimate 15 minutes" or "~20 min" or "expect 30–40 min"
```

**Regex pattern:**

```python
import re

def extract_estimate_from_prompt(prompt: str) -> float:
    """Extract time estimate in minutes from prompt."""
    
    # Pattern: "estimate X minutes" or "~X min" or "X–Y min"
    patterns = [
        r'estimate\s+(\d+(?:\.\d+)?)\s+minutes?',
        r'~\s*(\d+(?:\.\d+)?)\s+min',
        r'(\d+(?:\.\d+)?)\s*–\s*(\d+(?:\.\d+)?)\s+min',  # Range: use midpoint
        r'expect\s+(\d+(?:\.\d+)?)\s+(?:to\s+)?(\d+(?:\.\d+)?)?\s+min',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            groups = match.groups()
            if pattern.endswith('min'):  # Range pattern
                start = float(groups[0])
                end = float(groups[1]) if groups[1] else start
                return (start + end) / 2.0
            else:
                return float(groups[0])
    
    return 0  # No estimate found
```

---

## Phase 2: Historical Data Collection (W2 Week 1–2)

### Step 1: Backfill Time Data

Run analyzer on past manifests. Since time fields are new, you'll need to estimate elapsed time from manifest timestamp patterns:

```bash
# If manifests don't yet have time_tracking fields, backfill with proxy:
# Use file mtime difference between spawning and manifest creation

python3 scripts/8x_time_estimate_analyzer.py --generate-curves --days 14
```

This will:
1. Parse all manifests from past 14 days
2. Extract (agent_type, task_category, accuracy) tuples
3. Compute mean/stddev per bucket
4. Output: `forensics/time-tracking/2026-04-28/accuracy-curves.json`

### Step 2: Review Initial Curves

Manually inspect output to ensure sanity:

```bash
cat forensics/time-tracking/2026-04-28/accuracy-curves.json | jq '.by_agent_type | keys'
# Should see: ["code-reviewer", "data-scientist", "general-purpose", ...]

cat forensics/time-tracking/2026-04-28/accuracy-curves.json | jq '.by_wave'
# Should see: {"W1": {...}, "W2": {...}, "W3": {...}}
```

---

## Phase 3: Integration into Spawning (W2 Week 2–3)

### Step 1: Update Spawn Bundle

When building agent bundles, read latest accuracy curves and inject adjusted estimates:

```python
# In bundle rendering logic (0x_spawn_template.py or /run)

import json
from pathlib import Path
from datetime import datetime

def render_spawn_bundle(task_id, agent_type, baseline_estimate_minutes, wave, model):
    """Render bundle with time-tracking metadata."""
    
    # Read latest accuracy curves
    today = datetime.utcnow().strftime("%Y-%m-%d")
    curves_file = Path(f"forensics/time-tracking/{today}/accuracy-curves.json")
    
    if curves_file.exists():
        with open(curves_file) as f:
            curves = json.load(f)
    else:
        curves = {}
    
    # Predict adjusted estimate
    task_category = extract_task_category(task_id)
    
    if agent_type in curves.get('by_agent_type', {}):
        if task_category in curves['by_agent_type'][agent_type]:
            curve = curves['by_agent_type'][agent_type][task_category]
            factor = curve.get('prediction_factor', 1.0)
            adjusted_estimate = baseline_estimate_minutes * factor
            estimate_source = 'historical_baseline'
        else:
            adjusted_estimate = baseline_estimate_minutes
            estimate_source = 'agent_prompt'
    else:
        adjusted_estimate = baseline_estimate_minutes
        estimate_source = 'agent_prompt'
    
    # Apply wave-specific pressure curve
    if wave in curves.get('by_wave', {}):
        wave_curve = curves['by_wave'][wave]
        wave_factor = wave_curve.get('prediction_factor', 1.0)
        adjusted_estimate *= wave_factor
        estimate_source = 'wave_adjusted'
    
    bundle = {
        'task_id': task_id,
        'agent_type': agent_type,
        'wave': wave,
        'model': model,
        'predicted_duration_minutes': round(adjusted_estimate, 1),
        'estimate_source': estimate_source,
        'goal': f"...",
        # ... other bundle fields
    }
    
    return bundle
```

### Step 2: Wire into /spawn and /run

Modify skill logic to use time-adjusted bundles:

```bash
# In skills/run/BODY.py or spawn orchestration

# Before Agent() spawn:
bundle = render_spawn_bundle(...)

# Inject into agent prompt + metadata
metadata = {
    'agent_run_start_utc': datetime.utcnow().isoformat() + 'Z',
    'predicted_duration_minutes': bundle['predicted_duration_minutes'],
    'estimate_source': bundle['estimate_source'],
    'wave': wave,
    'model': model
}

agent_result = Agent(
    subagent_type=official_agent_type,
    prompt=bundle['goal'],  # Task description
    metadata=metadata
)
```

---

## Phase 4: Monitoring & Refinement (W2 Week 3–4)

### Step 1: Daily Accuracy Digest

Add cron job to generate curves daily + alert on anomalies:

```bash
# In .claude/hooks/post_spawn.sh or similar

#!/bin/bash

python3 scripts/8x_time_estimate_analyzer.py --generate-curves --days 7

# Check for anomalies
python3 - <<'EOF'
import json
from pathlib import Path
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
curves_file = Path(f"forensics/time-tracking/{today}/accuracy-curves.json")

if curves_file.exists():
    with open(curves_file) as f:
        curves = json.load(f)
    
    # Alert if stddev > 30% (high variance)
    for agent_type, categories in curves['by_agent_type'].items():
        for cat, stats in categories.items():
            if stats['stddev'] > 30:
                print(f"ALERT: {agent_type}/{cat} high variance ({stats['stddev']}%)")
EOF
```

### Step 2: Weekly Review Dashboard

Create a simple accuracy dashboard:

```python
#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime

def show_accuracy_dashboard():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    curves_file = Path(f"forensics/time-tracking/{today}/accuracy-curves.json")
    
    if not curves_file.exists():
        print("No curves available")
        return
    
    with open(curves_file) as f:
        curves = json.load(f)
    
    print("\n=== ACCURACY BY WAVE ===")
    for wave, stats in curves['by_wave'].items():
        acc = stats['avg_accuracy_percent']
        status = "👍 Good" if 95 <= acc <= 105 else "⚠️ Caution" if acc < 50 else "⚠️ Over"
        print(f"{wave:3s} {acc:6.1f}% ± {stats['stddev']:5.1f}  {status}")
    
    print("\n=== TOP 3 CATEGORIES (by sample size) ===")
    all_cats = []
    for agent_type, categories in curves['by_agent_type'].items():
        for cat, stats in categories.items():
            all_cats.append((agent_type, cat, stats))
    
    all_cats.sort(key=lambda x: x[2]['sample_size'], reverse=True)
    
    for agent_type, cat, stats in all_cats[:3]:
        print(f"{agent_type:20s} {cat:15s} {stats['avg_accuracy_percent']:6.1f}% (n={stats['sample_size']})")

if __name__ == '__main__':
    show_accuracy_dashboard()
```

### Step 3: Agent Feedback Loop

Include accuracy feedback in agent reputation system. Update `0x_reputation_summary.py`:

```python
# In reputation calculation

# Time-tracking accuracy correlates with belief_index
# If agent estimates consistently (low stddev), raise belief_index
# If agent estimates poorly (high bias), lower score

def compute_time_tracking_signal(manifests):
    """Extract time-tracking quality as reputation signal."""
    
    if not manifests:
        return 0.0
    
    # Compute mean absolute error in estimates
    errors = []
    for m in manifests:
        if m.get('predicted_duration_minutes') and m.get('actual_duration_minutes'):
            error = abs(m['accuracy_percent'])
            errors.append(error)
    
    if not errors:
        return 0.0
    
    # Low error = high score
    mean_error = sum(errors) / len(errors)
    
    # Cap at 50% error; normalize to 0–1
    time_tracking_score = max(0, 1 - (mean_error / 50))
    
    return round(time_tracking_score, 2)
```

---

## Phase 5: Advanced Features (Future)

Once basic loop is running smoothly:

### Confidence Intervals

Instead of point estimates, return ranges:

```python
def predict_with_confidence(agent_type, task_category, baseline_estimate, accuracy_curves):
    """Return (lower, best, upper) 68% confidence interval."""
    
    curve = accuracy_curves[agent_type][task_category]
    factor = curve['prediction_factor']
    stddev_factor = curve['stddev'] / 100.0
    
    best = baseline_estimate * factor
    lower = best * (1 - stddev_factor)
    upper = best * (1 + stddev_factor)
    
    return (round(lower, 1), round(best, 1), round(upper, 1))

# Example output:
# "estimate 12–18 min (best 15 min)"
```

### Anomaly Detection

Flag estimates that are >2σ away from historical mean:

```python
def check_estimate_anomaly(agent_type, task_category, baseline_estimate, accuracy_curves):
    """Return True if estimate is anomalously different."""
    
    if agent_type not in accuracy_curves:
        return False
    
    if task_category not in accuracy_curves[agent_type]:
        return False
    
    curve = accuracy_curves[agent_type][task_category]
    
    # Compute expected range: ±2σ
    mean_accuracy = curve['avg_accuracy_percent']
    stddev = curve['stddev']
    
    lower_bound = mean_accuracy - 2 * stddev
    upper_bound = mean_accuracy + 2 * stddev
    
    # Is our estimate outside expected range?
    estimate_accuracy = ...  # TODO: compute
    
    return not (lower_bound <= estimate_accuracy <= upper_bound)
```

### Wave-Specific Pressure Adjustments

Automatically apply wave corrections at spawn time:

```python
def apply_wave_pressure_curve(baseline_estimate, wave, accuracy_curves):
    """Apply pressure-curve adjustment based on piston wave."""
    
    wave_curves = accuracy_curves.get('by_wave', {})
    
    if wave not in wave_curves:
        return baseline_estimate
    
    wave_factor = wave_curves[wave]['prediction_factor']
    adjusted = baseline_estimate * wave_factor
    
    return round(adjusted, 1)
```

---

## Testing Checklist (W2)

- [ ] Manifest time fields captured for 50+ agents
- [ ] Analyzer parses manifests without errors
- [ ] Accuracy curves generated daily
- [ ] Curves show expected W1 > 100%, W2 ≈ 100%, W3 < 100%
- [ ] Adjustment factors applied to 5+ new spawns
- [ ] Agent accuracy feedback visible in reputation dashboard
- [ ] No manifests missing time data
- [ ] Correlations computed (accuracy vs. quality_score, belief_index, etc.)

---

## Success Metrics (W2 Exit Criteria)

1. **Data completeness** — 95%+ of new manifests have time fields
2. **Prediction accuracy** — Phase 2 curves ≤30% stddev per bucket
3. **Agent adoption** — 3+ agent types using adjusted estimates
4. **Feedback loop** — accuracy trends visible in weekly dashboard
5. **No regressions** — manifest write latency unchanged (<500ms)

---

## Files Modified / Created

- **New:** `scripts/8x_time_estimate_analyzer.py` (analyzer)
- **New:** `forensics/time-tracking/` (results directory)
- **New:** `docs/TIME-TRACKING-INTEGRATION.md` (this file)
- **Modified:** `scripts/0x_coc_writer.py` (or equivalent) — time fields
- **Modified:** `scripts/0x_spawn_template.py` — prediction logic
- **Modified:** `skills/run/BODY.py` — spawn metadata injection
- **Modified:** `scripts/0x_reputation_summary.py` — time-tracking signal

---

## References

- Schema: `forensics/time-tracking/time-tracking-schema.md`
- Analyzer: `scripts/8x_time_estimate_analyzer.py`
- Manifest format: `forensics/manifests/{YYYY-MM-DD}/{HH-MM-SS}Z_manifest_*.json`
