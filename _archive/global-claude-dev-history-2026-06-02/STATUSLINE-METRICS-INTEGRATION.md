# Statusline Metrics Integration — Real-Time Session Guidance

**Purpose:** Pipe live eval metrics + membench data + agent health into Claude CLI statusline so the user sees system state intuitively without explicit queries.

## Architecture: Live Metrics Flow

```
Claude Code Statusline Hook (polling 5sec)
  ↓
  ~/.claude/hooks/statusline.sh reads:
    - piston-checkpoint.json (wave state, burn rate)
    - altimeter.json (context %, remaining)
    - metrics-ledger.jsonl (recent eval scores)
    - manifest stream (agent health)
  ↓
  Computes dashboard with:
    - Wave state (W1/W2/W3 + progress)
    - Eval score trend (trend arrow ↑↓)
    - Agent reputation histogram (health distribution)
    - Context burn rate (current + predicted time-to-compact)
    - F(0) compliance status (violations live-flagged)
  ↓
  Outputs JSON to Claude Code statusline
  ↓
  User sees integrated metrics WITHOUT prompting
```

## Statusline JSON Schema — What Claude CLI Renders

```json
{
  "statusLine": {
    "left": "W1 | eval:0.78↑ | agents:4/4 | ctx:68% → 89min",
    "center": "treasury-cert-ip-origins [■■■□□]",
    "right": "F0: ✓ | FFMx:1.04 ↑"
  }
}
```

### Interpretation

| Section | What It Shows | How to Read |
|---------|---------------|-----------|
| **W1** | Current wave | W1=parallel, W2=sequential, W3=synthesis, POST=after-compact |
| **eval:0.78↑** | Eval score + trend | Score 0-1, ↑=improving, ↓=declining, →=flat |
| **agents:4/4** | Agent capacity | 4 active / 4 requested (waiting means context pressure) |
| **ctx:68% → 89min** | Context fill + time-to-compact | Predicts when auto-compact fires |
| **[■■■□□]** | Mission progress | Filled=done phases, empty=remaining phases (5 phases max) |
| **F0: ✓** | F(0) compliance | ✓=no violations, ⚠=warning, ✗=critical violation |
| **FFMx:1.04↑** | Mission efficiency | Artifacts per token (>1.0 is good, ↑ means improving) |

## Input: metrics-ledger.jsonl

Agents write eval signals after each manifest:

```jsonl
{"ts":"2026-04-28T12:34:56Z","metric":"quality_score","agent":"scout-001","value":0.79,"task_id":"task-123"}
{"ts":"2026-04-28T12:35:01Z","metric":"eval_composite","agent":"scout-001","value":0.82,"task_id":"task-123"}
{"ts":"2026-04-28T12:35:05Z","metric":"ffmx","mission":"treasury-cert","value":1.04,"agents":3}
{"ts":"2026-04-28T12:40:22Z","metric":"eval_composite","agent":"auditor-002","value":0.71,"task_id":"task-124"}
...
```

## Computing Dashboard Values

### 1. Eval Score Trend

```python
def compute_eval_trend(minutes_window=10):
  now = time.time()
  cutoff = now - (minutes_window * 60)
  
  scores = [
    float(line.split('"value":')[1].split(',')[0])
    for line in open('~/.claude/hooks/metrics-ledger.jsonl')
    if (json.loads(line).get('ts') and
        time.fromisoformat(json.loads(line)['ts']) > cutoff and
        'eval_composite' in line)
  ]
  
  if len(scores) < 2:
    return None, '→'  # Not enough data
  
  current = scores[-1]
  previous = scores[0]
  delta = current - previous
  
  if delta > 0.02:
    trend = '↑'
  elif delta < -0.02:
    trend = '↓'
  else:
    trend = '→'
  
  return round(current, 2), trend
```

### 2. Agent Health Histogram

```python
def agent_health_distribution():
  """Return (active_agents, total_requested)"""
  manifest_dir = "forensics/manifests/$(date +%Y-%m-%d)"
  
  # Count recent manifests (created in last 5 min)
  recent = [f for f in os.listdir(manifest_dir)
            if time.time() - os.path.getmtime(manifest_dir+f) < 300]
  
  # Count how many agents are in-flight vs completed
  active = sum(1 for f in recent if 'in_progress' in open(manifest_dir+f).read())
  completed = len(recent) - active
  
  return active, len(recent)
```

### 3. Time-to-Compact

```python
def time_to_compact_minutes():
  """Predict when auto-compact fires (in minutes)"""
  altimeter = json.load(open('~/.claude/hooks/state/altimeter.json'))
  
  curr_pct = altimeter['pct']
  burn_rate_pct_per_min = altimeter.get('burn_rate_pct_per_min', 1.0)
  
  if burn_rate_pct_per_min <= 0:
    return '∞'
  
  minutes = (93.5 - curr_pct) / burn_rate_pct_per_min
  
  if minutes < 0:
    return 'NOW' # Already past threshold, compact may be firing
  elif minutes < 5:
    return f'{int(minutes)}min 🔴' # Red alert
  elif minutes < 15:
    return f'{int(minutes)}min 🟡' # Caution
  else:
    return f'{int(minutes)}min 🟢' # Safe
```

### 4. Mission Progress Bar

```python
def mission_progress_bar(investigation_label, width=5):
  """Return progress bar [■■□□□] for mission phases"""
  
  phases = ['SEED', 'DEEPEN', 'EXTEND', 'FULL', 'PUBLISH']
  
  # Find highest quality_score in manifests for this investigation
  completed_phases = 0
  quality_scores = [
    json.loads(line).get('quality_score', 0)
    for line in subprocess.check_output(
      f'grep -r "{investigation_label}" forensics/manifests/*/'.split()
    ).decode().split('\n')
  ]
  
  # Map quality_score to phases
  if max(quality_scores or [0]) >= 0.85:
    completed_phases = 5
  elif max(quality_scores or [0]) >= 0.80:
    completed_phases = 4
  elif max(quality_scores or [0]) >= 0.70:
    completed_phases = 3
  elif max(quality_scores or [0]) >= 0.50:
    completed_phases = 2
  elif len(quality_scores) > 0:
    completed_phases = 1
  
  filled = '■' * completed_phases
  empty = '□' * (width - completed_phases)
  
  return f'[{filled}{empty}]'
```

### 5. F(0) Compliance Check

```python
def f0_compliance_check():
  """Check for equilibrium violations"""
  violations = []
  
  # Check 1: CLAUDEMD load
  if os.path.getsize('/mnt/d/0local/.claude/CLAUDE.md') > 20000:
    violations.append('CLAUDE.md oversize (split needed)')
  
  # Check 2: NECTAR compaction
  if os.path.getsize('/mnt/d/0local/.claude/NECTAR.md') > 50000:
    violations.append('NECTAR.md not crystallized')
  
  # Check 3: SendMessage usage
  if 'SendMessage' in subprocess.check_output('grep -r "SendMessage" ./.claude/scripts/').decode():
    violations.append('SendMessage detected (stigmergy violation)')
  
  if not violations:
    return '✓'
  elif len(violations) == 1:
    return '⚠'
  else:
    return '✗'
```

### 6. FFMx Trend

```python
def mission_ffmx():
  """Read latest FFMx from metrics and compute trend"""
  
  ffmx_entries = [
    json.loads(line)
    for line in open('~/.claude/hooks/metrics-ledger.jsonl')
    if '"metric":"ffmx"' in line
  ]
  
  if not ffmx_entries:
    return None, '→'
  
  current = ffmx_entries[-1]['value']
  previous = ffmx_entries[-2]['value'] if len(ffmx_entries) > 1 else current
  
  delta = current - previous
  trend = '↑' if delta > 0.01 else ('↓' if delta < -0.01 else '→')
  
  return round(current, 2), trend
```

## Statusline Hook Implementation

**File:** `~/.claude/hooks/statusline.sh`

```bash
#!/bin/bash

# Called by Claude CLI every 5 seconds with:
# STDIN: JSON from Claude Code (window size, context%, rate limits, etc.)
# STDOUT: JSON to render in statusline

# Read input from Claude Code
INPUT=$(cat)

# Extract current metrics
CTX_PCT=$(echo "$INPUT" | jq '.context_window.used_percentage // 0')
REMAINING=$(echo "$INPUT" | jq '.context_window.remaining_percentage // 0')

# Read piston state
PISTON=$(cat ~/.claude/hooks/state/piston-checkpoint.json 2>/dev/null || echo '{}')
WAVE=$(echo "$PISTON" | jq '.wave // "?"' -r)

# Compute metrics
ALTIMETER=$(cat ~/.claude/hooks/state/altimeter.json 2>/dev/null || echo '{}')
BURN_RATE=$(echo "$ALTIMETER" | jq '.burn_rate_pct_per_min // 1.0')
TIME_TO_COMPACT=$(python3 << 'PYEOF'
import json
alt = json.load(open(os.path.expanduser('~/.claude/hooks/state/altimeter.json'), 'r')) rescue {}
pct = alt.get('pct', 50)
burn = alt.get('burn_rate_pct_per_min', 1.0)
if burn > 0:
  mins = (93.5 - pct) / burn
  if mins < 0:
    print('NOW 🔴')
  elif mins < 5:
    print(f'{int(mins)}min 🔴')
  elif mins < 15:
    print(f'{int(mins)}min 🟡')
  else:
    print(f'{int(mins)}min 🟢')
else:
  print('∞')
PYEOF
)

# Get eval score
EVAL_SCORE=$(tail -1 ~/.claude/hooks/metrics-ledger.jsonl 2>/dev/null | jq '.value // 0.5' -r)
EVAL_TREND=$(python3 << 'PYEOF'
# Simplified: if last score > previous, trend is up
import json
try:
  lines = [json.loads(l) for l in open(os.path.expanduser('~/.claude/hooks/metrics-ledger.jsonl')).readlines()[-2:]]
  if len(lines) >= 2:
    delta = lines[-1].get('value', 0) - lines[-2].get('value', 0)
    print('↑' if delta > 0.02 else ('↓' if delta < -0.02 else '→'))
  else:
    print('→')
except:
  print('→')
PYEOF
)

# Get agent count
AGENT_COUNT=$(ls forensics/manifests/$(date +%Y-%m-%d)/*.json 2>/dev/null | wc -l)

# Get F(0) compliance
F0_STATUS="✓"
if [ $(stat -c%s ~/.claude/CLAUDE.md 2>/dev/null || echo 0) -gt 20000 ]; then F0_STATUS="⚠"; fi
if [ $(stat -c%s ~/.claude/NECTAR.md 2>/dev/null || echo 0) -gt 50000 ]; then F0_STATUS="✗"; fi

# Get mission progress
MISSION=$(grep -h "investigation_label" forensics/manifests/$(date +%Y-%m-%d)/*.json 2>/dev/null | head -1 | jq '.investigation_label' -r)
PROGRESS="[■■■□□]"  # Placeholder

# Render statusline
cat << JSON
{
  "statusLine": {
    "left": "$WAVE | eval:${EVAL_SCORE}${EVAL_TREND} | agents:${AGENT_COUNT} | ctx:${CTX_PCT}% → ${TIME_TO_COMPACT}",
    "center": "${MISSION} ${PROGRESS}",
    "right": "F0: ${F0_STATUS}"
  }
}
JSON
```

## Enabling Statusline Metrics

Add to `settings.json`:

```json
{
  "hooks": {
    "statusline": {
      "type": "command",
      "command": "~/.claude/hooks/statusline.sh",
      "refreshInterval": 5
    }
  }
}
```

## Example Session Output

```
┌─────────────────────────────────────────────────────────────────┐
│                  W1 | eval:0.78↑ | agents:4 | ctx:68%→89min │
│     treasury-cert-ip-origins [■■■□□]    F0: ✓ | FFMx:1.04↑ │
└─────────────────────────────────────────────────────────────────┘
```

As context burns, statusline updates live:

```
T+5min:  W1 | eval:0.76→ | agents:3 | ctx:74%→45min | F0: ✓ | FFMx:1.04↑
T+10min: W2 | eval:0.81↑ | agents:2 | ctx:82%→22min | F0: ✓ | FFMx:1.09↑
T+15min: W3 | eval:0.85↑ | agents:1 | ctx:91%→2min 🔴 | F0: ✓ | FFMx:1.15↑
T+16min: [Auto-compact fires] → NEW SESSION STARTS → W1 | eval:0.85↑ | ... (fresh 191K tokens)
```

## Interpretation Guide for Users

**What Each Signal Means:**

- **W1/W2/W3 → eval:0.85↑** — "Good news: eval score improving, and we're in the right wave for this context level"
- **agents:4/4** — "All 4 agents I requested are running (not waiting)"
- **agents:2/4** — "Only 2 of 4 agents running (context pressure, W2 gating)"
- **ctx:68%→89min** — "68% full, 89 minutes until auto-compact (safe to spawn more)"
- **ctx:91%→2min🔴** — "91% full, 2 minutes to compact (enter RED ALERT, W3 background only)"
- **F0:✓** — "System is f(0) compliant, no violations"
- **F0:⚠** — "One violation detected (e.g., CLAUDE.md too large)"
- **FFMx:1.15↑** — "Mission efficiency improving (more artifacts per token)"

---

## Integrating with /metrics

The metrics dashboard (`/metrics --formula-tracking`) reads the same sources:

```bash
/metrics --show eval_trend --graph 24h
# Shows: Eval score over last 24 hours, with mutation events marked
```

Statusline is **real-time push**; `/metrics` dashboard is **historical analysis**.

Together: statusline guides **current session**, metrics dashboard guides **next mutation decision**.

---

## See Also

- `faerie2-formulas.json` — Parameters driving wave gating
- `MUTATION-CYCLE-GUIDE.md` — How to interpret eval trends and adjust
- `/dev-eval` — Measure baseline + mutation impact
