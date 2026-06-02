# WandB Integration — Membench + Eval Harness

Tracks M/Q/T/P membench metrics and 7-dimension eval scores (A-G) across agent runs.
Enables trend visualization, composite trajectory, and competitor delta comparisons.

## Project

- Project: `faerie-membench` (bridge default) / `cybertemplate-ops` (wb_membench_log.py)
- Entity: `aegis-eternis`
- Dashboard: https://wandb.ai/aegis-eternis/cybertemplate-ops
- Config: `~/.claude/hooks/state/wandb_run_config.json` (or `{repo}/hooks/state/wandb_run_config.json`)

## Setup

```bash
# Install WandB (system Python or pipx venv)
pip install wandb
# OR (isolated, matches shebang in wb_membench_log.py)
pipx install wandb

# Login (one-time — stores creds in ~/.netrc)
wandb login
```

## Running

### Full membench + WandB log (canonical path)
```bash
python3 /mnt/d/0local/gitrepos/faerie2/scripts/eval/eval_harness.py \
  --membench --wandb
```

Flags:
- `--vs-prior`   — include delta metrics vs last eval-history entry
- `--vs-vanilla` — include delta vs vanilla baseline (no rules/agents)
- `--wandb NAME` — custom run name (optional, auto-generated if omitted)

### Global eval_harness.py wrapper
```bash
python3 ~/.claude/scripts/eval_harness.py --full --wandb
```
This delegates to `9x_eval_harness.py` which calls `_run_membench_wandb()`.
The membench cache is written to `~/.claude/hooks/state/membench-latest.json`
after a successful WandB log.

### Quick read of cached membench score (no WandB)
```bash
python3 ~/.claude/scripts/eval_harness.py --quick
```
Reads `membench-latest.json` and displays composite inline with the 7-dim eval.

### Standalone wandb_bridge.py (log existing system-eval.json)
```bash
python3 ~/.claude/hooks/state/wandb_bridge.py
# or with options:
python3 ~/.claude/hooks/state/wandb_bridge.py \
  --eval-json ~/.claude/hooks/state/system-eval.json \
  --phase phase2 \
  --run-name "sprint-015-post-refactor"
# dry run (no WandB connection needed)
python3 ~/.claude/hooks/state/wandb_bridge.py --dry-run
```

### Import in agent scripts
```python
from wandb_bridge import MembenchWandBLogger

logger = MembenchWandBLogger()
logger.log_eval_run(eval_result)                 # 7-dim eval dict
logger.log_membench_detail("M1_retention", 88.0, confidence=2.5)
logger.tag_run("phase2", agent_types=["evidence-curator"])
logger.finish()

# Or one-shot functional API
from wandb_bridge import log_eval_run_to_wandb
log_eval_run_to_wandb(eval_result, phase="phase2")
```

## WandB Dashboard — What to Look For

### Panels to set up in the WandB project UI

| Panel | Metric keys | What it shows |
|---|---|---|
| Composite trend | `eval/composite_score`, `membench/composite` | System-wide improvement over time |
| M-dimension matrix | `eval/dim/B-Memory`, `eval/dim/D-Quality`, `eval/dim/E-Piston`, `eval/dim/A-Throughput` | MQTP dimensions side-by-side |
| Memory health | `eval/memory/honey_hit_rate`, `eval/memory/cross_session_continuity`, `eval/memory/nectar_line_count` | HONEY usage + continuity rate |
| Membench M1-M11 | `membench/M1_retention` through `membench/M11_bootstrap_exit_rate` | Full substrate measurement |
| Piston rhythm | `eval/piston/waves_before_response`, `eval/piston/two_wave_rate` | Orchestration cadence |
| Quality signals | `eval/quality/citation_accuracy_rate`, `eval/quality/finding_depth_avg` | Finding depth + citation rate |
| Alert count | `eval/alert_count` | System health (0 = clean) |

### Interpretation guide

**Composite score (0-1.0):**
- < 0.5: Baseline — insufficient data or system cold-start
- 0.5-0.7: Calibrating — memory system warming, piston firing inconsistently
- 0.7-0.85: Functional — most dimensions contributing, M3 efficiency proving value
- > 0.85: Mature — compounding improvement visible, M8 confabulation rate near zero

**Membench composite (0-100 scale):**
- < 50: RED band — memory system not materially contributing
- 50-70: AMBER band — improvement visible but overhead exceeds net gain
- > 70: GREEN band — memory system paying for itself

**Trend signals:**
- `eval/trend = 1.0` (improving), `0.5` (flat), `0.0` (degrading)
- `eval/composite_delta` > +0.02 per run = meaningful improvement
- `membench/M1_retention` declining + `eval/memory/honey_hit_rate` declining = HONEY drift

### Tags (filter runs in dashboard)

| Tag | Runs |
|---|---|
| `membench` | All membench-only runs |
| `eval` | All eval harness runs |
| `memory-system` | Substrate measurement runs |
| `sprint` | Session-sprint runs (wb_sprint_log.py) |
| `phaseN` | Phase-tagged runs (added via `logger.tag_run()`) |

## Offline Mode (disable WandB without removing code)

```bash
# Per-run disable
WANDB_MODE=disabled python3 eval_harness.py --membench --wandb

# Persistent disable in shell
export WANDB_MODE=disabled

# Or don't pass --wandb flag — all W&B calls are guarded by flag checks
python3 eval_harness.py --membench   # no WandB, full local eval
```

`wandb_bridge.py` degrades silently if WandB is not installed or not logged in.
The `MembenchWandBLogger` class becomes a no-op — all methods return without error.

## File Locations

| File | Role |
|---|---|
| `~/.claude/hooks/state/wandb_bridge.py` | Lightweight eval+membench WandB bridge (this system) |
| `{faerie2}/scripts/eval/wb_membench_log.py` | Full M1-M11 membench logger (primary, called by eval_harness) |
| `{faerie2}/scripts/eval/eval_membench.py` | Membench measurement engine (M1-M11 computation) |
| `{faerie2}/scripts/eval/eval_harness.py` | Primary eval harness (--membench --wandb entry point) |
| `~/.claude/scripts/eval_harness.py` | Wrapper — delegates --wandb to 9x_eval_harness.py |
| `~/.claude/scripts/9x_eval_harness.py` | Global eval harness (7-dimension A-G scoring) |
| `~/.claude/hooks/state/wandb_run_config.json` | WandB project/entity config |
| `~/.claude/hooks/state/membench-latest.json` | Cached membench composite (updated after --wandb run) |
| `~/.claude/hooks/state/system-eval.json` | Cached 7-dimension eval result |

## COC Integration

Each `--wandb` run writes a hash-chained COC entry to:
`~/.claude/memory/forensics/agent-runs.jsonl`

Entry type: `membench_run`. Fields: `run_id`, `composite_eval`, `composite_membench`,
`wb_run_url`, `prev_run_hash`, `run_hash`, `entry_hash`.

This links every WandB run to the forensic chain — the W&B dashboard URL is
forensically provable via the COC log.

---

Status: Adopted 2026-04-21
