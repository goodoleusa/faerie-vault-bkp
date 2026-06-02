# /faerie f(0) Startup Protocol — Lean Edition

**Context budget at startup: <5K chars overhead**

## What System-Reminder Already Loads
- `~/.claude/rules/core/agents.md` (5.1K)
- `~/.claude/rules/core/memory.md` (2.9K)
- `~/.claude/rules/core/core.md` (2.8K)
- Project `CLAUDE.md` and `.claude/HONEY.md` (if repo scoped)

**Do NOT re-read these in /faerie.**

---

## Ideal /faerie Startup Sequence (Lean)

### 1. Print Brief Header (user-facing)
```bash
echo "FAERIE ──────────────────────────────────"
echo "Orienting..."  # Let user know work is happening
```
**Cost: ~0.1K**

### 2. Run Startup Scripts with --silent
```bash
# Each of these returns 1-2 lines, not full JSON output
python3 ~/.claude/scripts/eval_harness.py --silent  # Output: "eval:0.36→"
python3 ~/.claude/hooks/state/piston.py --silent    # Output: "piston:W1" 
python3 ~/.claude/scripts/9x_f0_efficiency_tracker.py --record-startup $(wc -c < ~/.claude/hooks/state/piston-checkpoint.json)
```
**Cost: ~0.5K** (3 lines of output)

### 3. Get Dynamic Wave Spec (silent)
```bash
# Read only the critical fields, not full JSON
WAVE_SUMMARY=$(python3 ~/.claude/scripts/7x_piston_orchestrator.py --output-json 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"W1:{len(d['waves']['W1']['agents'])} W2:{len(d['waves']['W2']['agents'])} W3:{len(d['waves']['W3']['agents'])}\")")
echo "Waves: $WAVE_SUMMARY"
```
**Cost: ~0.1K** (1 line of summary)

### 4. Print Lean Status + Spawn Agents
```bash
echo "────────────────────────────────────────"
echo "Executing W1+W2..."
# Spawn agents here (silent, blocking)
```
**Cost: ~0.1K**

### 5. Collect & Report Results (after waves complete)
```bash
# Print W1/W2 results from manifests (1-2 lines per agent)
# Then return to user
```
**Cost: ~0.5K**

---

## Total Startup Cost (Lean Protocol)
- System-reminder pre-load: ~30K (rules)
- /faerie startup: ~1K (header + status + wave summary)
- **Total: ~31K chars** (acceptable for f(0))

---

## Current Session (Bad Example)
- System-reminder: ~30K
- Read BODY.md: ~2K
- Bash outputs (full JSON): ~40K
- Eval harness output: ~10K
- Piston orchestrator full spec: ~5K
- **Total: ~85K chars** (bad)

---

## Conversion Steps

1. ✓ Add `--silent` flag to eval_harness.py (DONE)
2. ☐ Add `--silent` flag to piston.py
3. ☐ Add `--silent` flag to droplet_cadence.py
4. ☐ Update BODY.md to use --silent flags
5. ☐ Update BODY.md to skip faerie-brief.json if >10K
6. ☐ Add PostToolUse hook to f0_efficiency_tracker (record startup chars)

---

## Flag Definitions

**--silent:** Output only 1-line summary, no explanatory text.
- eval_harness.py --silent → "eval:0.36→"
- piston.py --silent → "piston:W1"
- droplet_cadence.py --silent → "droplets:0"

**--brief:** Return only essential fields of JSON (for JSON outputs).
- piston_orchestrator.py --brief → {"waves": {W1: [agents], W2: [], W3: []}} (no metric details)

