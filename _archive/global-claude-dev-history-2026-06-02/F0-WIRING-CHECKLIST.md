# f(0) Efficiency Wiring Checklist

## ✅ COMPLETED

- [x] Dimension H added to eval_harness.py (startup context efficiency metric)
- [x] `--silent` flag added to eval_harness.py (outputs "eval:0.36→" instead of full dump)
- [x] `9x_f0_efficiency_tracker.py` created (logs startup/task completion events)
- [x] Cold/Warm start detection template created (f0-startup-template.sh)
- [x] STARTUP-PROTOCOL.md written (ideal 31K vs actual 85K breakdown)
- [x] Audit completed: BODY.md fine, execution hygiene is the issue

## ⏳ IN PROGRESS

- [ ] Wire --silent into droplet_cadence.py → "droplets:N"
- [ ] Wire --silent into piston.py (doesn't exist yet, needs creation)
- [ ] Update BODY.md to detect cold vs warm start
- [ ] Update BODY.md to use --silent flags
- [ ] Update BODY.md to skip faerie-brief.json when warm

## 🚀 NEXT WAVE (After baseline wiring)

- [ ] Add PostToolUse hook to f0_efficiency_tracker (auto-record startup chars)
- [ ] Add context bloat alert to /faerie dashboard (RED if startup > 10K)
- [ ] Wire session heartbeat to reset checkpoint cleanly for warm starts
- [ ] Test: `/faerie` at T1, T5, T10 — should cost <2K each time after T1
- [ ] Establish f(0) SLA: no session starts >5K overhead

## 📊 EXPECTED RESULTS (After Wiring)

**Current (bad):**
- T1 /faerie: 85K chars, blocks agents
- Mid-session /faerie: can't run without context bloat

**After wiring (ideal):**
- T1 /faerie: 31K chars (system-reminder 30K + startup 1K)
- T5 /faerie: 1K chars (just status summary, skip faerie-brief)
- T10 /faerie: 1K chars (reusable control flow primitive)

**Dimension H tracking:**
- Session 1: eval startup=50K, tasks=0 → undefined (bloat case)
- Session 2: eval startup=5K, tasks=6 → ratio=120 (good)
- Session 3: eval startup=1K, tasks=6 → ratio=600 (ideal)

## 🔨 WIRING CODE

### 1. Add --silent to droplet_cadence.py
```python
if "--silent" in sys.argv:
    # Count droplets from past 3 days only
    recent = get_recent_droplets(days=3)
    print(f"droplets:{len(recent)}")
else:
    # Full output as before
    ...
```

### 2. Create piston.py (minimal, checkpoint-based)
```python
#!/usr/bin/env python3
"""Minimal piston status — reports current wave from checkpoint."""
import json
from pathlib import Path

CHECKPOINT = Path.home() / ".claude" / "hooks" / "state" / "piston-checkpoint.json"

if CHECKPOINT.exists():
    data = json.loads(CHECKPOINT.read_text())
    status = data.get("status", "unknown")
    current = data.get("current_wave", "?")
    print(f"piston:{current}" if not "--silent" in sys.argv else f"piston:{current}")
else:
    print("piston:unknown")
```

### 3. Update BODY.md startup to call cold/warm template
```bash
source ~/.claude/hooks/state/f0-startup-template.sh
# Sets COLD=true/false
if [ "$COLD" = "true" ]; then
    # Read faerie-brief for context bundle
else
    # Skip faerie-brief — it's already in context
fi
```

## 🎯 SUCCESS CRITERIA

- [ ] Dimension H appears in eval output
- [ ] /faerie at T5 costs <2K chars
- [ ] faerie-brief.json only read at T1
- [ ] Dashboard shows `[H:0.8→]` status
- [ ] Can run `/faerie` 3 times in one session without context bloat

