# Vanilla-Baseline Protocol

How to capture defensible "this is what vanilla Claude Code does on the same task"
data so faerie's ROI claims are falsifiable and honest.

> If you have never measured vanilla on your own tasks, any delta you report for
> faerie is unverifiable. This protocol exists so you can **prove** faerie is better
> (or learn that it is not, and adjust).

---

## Why vanilla baselines matter

Faerie's value claim rests on "faerie makes Claude Code measurably better at
complex real-world work than vanilla Claude Code."

Without vanilla numbers, every ROI report is hand-waving. With vanilla numbers,
every ROI report is a checkable diff.

Today (pre-protocol), the eval harness falls back to a **hardcoded approximation**
of vanilla performance (see `scripts/eval/eval_harness.py` — the `vanilla_approx_dims`
dict in `record_vanilla_baseline`). That is an acceptable starting point, **not** an
acceptable ending point. You need real runs.

---

## What vanilla HAS

Vanilla Claude Code is still powerful. The vanilla template does NOT strip:

| Feature | Why it stays | Notes |
|---------|-------------|-------|
| `Agent` tool | Claude Code native | Full subagent dispatch |
| `Task` tool | Claude Code native | Task tracking within session |
| `TeamCreate` / `SendMessage` | Native experimental feature | Enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — kept in the vanilla template |
| Standard `subagent_type` roster | Shipped with Claude Code | general-purpose, data-engineer, documentation-engineer, code-reviewer, evidence-curator, security-auditor, fullstack-developer, etc. |
| Built-in skills (official plugins) | Ship with Claude Code | `/init`, `/review`, `/security-review`, `/simplify`, etc. |
| Basic tool permissions | User controls | Bash/Read/Write/Edit/WebFetch/WebSearch |
| Model routing | Claude-side | `model: sonnet` by default |

## What vanilla LACKS (on purpose)

| Feature | Why it goes | Where it lives in faerie |
|---------|-------------|--------------------------|
| `memory_bridge.py --stream` | faerie sauce | `~/.claude/scripts/memory_bridge.py` |
| SPAWN-BOILERPLATE auto-injection | faerie sauce | `~/.claude/rules/spawn-boilerplate.md` + hook |
| `pollen-{SID}.md` working notes | faerie sauce | `{repo}/.claude/memory/` |
| `NECTAR.md` / `HONEY.md` | faerie crystallization pipeline | `~/.claude/NECTAR.md` / `~/.claude/HONEY.md` |
| `evalbot` / `eval_harness.py` agent scoring | faerie sauce | `faerie2/scripts/eval/eval_harness.py` |
| Forensic COC hooks (`forensic_coc.py`, `vault_mutation_tracker.py`) | faerie sauce | `~/.claude/hooks/` |
| Piston wave orchestration (`surfacing_scheduler`, piston-checkpoint) | faerie sauce | `~/.claude/scripts/` |
| Session lifecycle hooks (`session_stop_hook`, `pre_compact_hook`, `memory_collector`) | faerie sauce | `~/.claude/hooks/` |
| Stigmergy tracker, broadcast scan, droplet register | faerie sauce | `~/.claude/scripts/9x_*` |
| Custom skills (`/faerie`, `/handoff`, `/crystallize`, `/data-ingest`, etc.) | faerie skills | `~/.claude/skills/` |
| Custom agent cards (`report-writer`, `membot`, `memory-keeper`, etc.) | faerie-trained | `~/.claude/agents/` |
| Custom agent-proxy registry | faerie sauce | `~/.claude/hooks/state/custom-agent-registry.json` |
| `enabledPlugins` (cybertemplate-investigation, claude-md-management, etc.) | faerie add-ons | cleared in vanilla template |

The vanilla template is deliberately minimal. This is what a new user would get on day one
of installing Claude Code with no faerie and no plugins, plus the teams flag which is a
Claude Code feature anyone can enable.

---

## Activation / deactivation procedure

### Activate (flip faerie OFF)

```bash
cd /mnt/d/0LOCAL/gitrepos/faerie2
python3 scripts/install/vanilla_baseline.py --activate
```

What happens:
1. `settings.json` is SHA-256-hashed and backed up to
   `settings.json.faerie-on.{UTC-timestamp}`. Existing backups are never clobbered
   (timestamp-suffixed; collision-proof).
2. The vanilla template at `scripts/install/vanilla_settings_template.json` is written
   to `settings.json`. Your `ANTHROPIC_API_KEY` is preserved from the live settings so
   you don't have to re-paste it.
3. A flag file `~/.claude/state/VANILLA_BASELINE_ACTIVE` (or `/mnt/d/0LOCAL/.claude/state/`
   on WSL) records the activation timestamp and backup path.
4. A COC entry appends to `faerie2/forensics/baseline-runs-coc.jsonl` with before/after
   SHA-256 hashes, chained to the previous entry's hash.

Safety guard: if your live `settings.json` has `ANTHROPIC_API_KEY` overridden to
anything containing `test` or starting `sk-ant-test`, activation refuses. This prevents
accidentally burning prod quota on vanilla runs when you clearly meant to use a test
env — or vice versa, running prod tasks on what you thought was a test key.

### Run the task (new terminal)

```bash
# In a NEW terminal (faerie session already closed):
claude                       # starts vanilla Claude Code

# In the Claude CLI:
# Paste the prompt from a baseline task file. For example:
cat baseline-tasks/task-01-code-audit.md
# Copy the "Task prompt" block, paste into Claude, let it work.
```

Copy-paste helper:

```bash
python3 scripts/install/vanilla_baseline.py --run-task task-01-code-audit
# Prints the entire task file to stdout. Grab the prompt section.
```

### Deactivate (flip faerie ON)

```bash
python3 scripts/install/vanilla_baseline.py --deactivate
```

What happens:
1. Settings.json is restored from the backup recorded in the flag file (fallback:
   most-recent `.faerie-on.*` file).
2. Any Claude CLI transcript JSONLs under `~/.claude/projects/**/*.jsonl` that were
   modified AFTER activation_ts are copied to `faerie2/baseline-runs/{session_id}/`.
3. For each copied transcript, a `metadata.json` is extracted:
   ```json
   {
     "session_id": "...",
     "mode": "vanilla",
     "activation_ts": "...",
     "deactivation_ts": "...",
     "start_ts": "...",
     "end_ts": "...",
     "tasks_attempted": N,
     "tool_use_counts": {"Agent": 2, "Read": 15, "Write": 3, ...},
     "subagent_spawns": 2,
     "total_tokens": 48231,
     "completion_status": "completed",
     "transcript_path": "...",
     "transcript_sha256": "..."
   }
   ```
4. A COC entry appends with `action: "deactivate"`, archived count, and restored
   backup path.
5. The flag file is removed.

### Status

```bash
python3 scripts/install/vanilla_baseline.py --status
```

Shows: current mode, settings.json hash, flag file path, how long vanilla has been
active (if applicable), last 5 archived runs with token/spawn counts, last COC event.

---

## Recommended cadence

- **1-2 full vanilla sessions per month**, working through all three `baseline-tasks/`.
- Record a **faerie session on the same three tasks** within the same week for a paired
  comparison.
- Each quarter, run `--collect` to refresh `baseline-runs/SUMMARY.json`. Trend lines
  over time tell you whether faerie's ROI is steady, growing, or eroding.

**Rule of thumb for claims:**
- 0 vanilla runs: you cannot claim faerie is better. You can say "subjectively feels
  better, unmeasured."
- 1 vanilla run: directional evidence only. Report as "n=1 pilot."
- 2+ vanilla runs: you can report mean/median/p95 deltas with a sample-size caveat.
- 5+ vanilla runs per task: the deltas begin to be statistically defensible.

---

## Metrics captured per run

From the transcript JSONL parser:

| Metric | Source | Meaning |
|--------|--------|---------|
| `tasks_attempted` | Count of user-role events | How many prompts the user sent (≈ tasks worked) |
| `tool_use_counts` | Sum per `tool_use` block name | Which tools the session reached for, how often |
| `subagent_spawns` | Count of `Agent` + `Task` tool uses | Team-dispatch behavior |
| `total_tokens` | Sum of `input_tokens + output_tokens` | Cost proxy |
| `start_ts` / `end_ts` | First / last event timestamp | Duration |
| `completion_status` | Inferred from end_ts presence | Did the session close cleanly? |
| `transcript_sha256` | Hash of archived JSONL | Tamper-evidence in the COC |

From `--collect` aggregation (SUMMARY.json):

- `aggregates.total_tokens`: mean/median/p95/min/max/n
- `aggregates.subagent_spawns`: same stats
- `aggregates.duration_s`: derived from ISO timestamps
- `aggregates.tool_use_totals`: totals across all runs by tool name
- `aggregates.completion_rate`: fraction of runs that ended cleanly

---

## How `eval_harness.py --vs-vanilla` consumes this

`scripts/eval/eval_harness.py` has two vanilla-related entry points:

1. **`--vs-vanilla`** — reads `~/.claude/hooks/state/vanilla-baseline.json` and diffs
   the current system-eval's composite + per-dimension scores against it. Output is
   a ROI table showing `delta` per dimension.

2. **`--ab-vanilla`** — the paired A/B task-level harness. Expects a
   `vanilla-run-result.json` and a `faerie-run-result.json` with matching task IDs,
   then writes a vault diff report and updates `vanilla-baseline.json`.

`vanilla_baseline.py --collect` is the **upstream producer** for both:

- `baseline-runs/{session_id}/metadata.json` → aggregated into `baseline-runs/SUMMARY.json`
- `SUMMARY.json.aggregates` gives the denominators (tokens, duration, spawns) that
  contextualize the composite-score deltas from `vanilla-baseline.json`.

Future work: wire `eval_harness.py --vs-vanilla` to read
`baseline-runs/SUMMARY.json` directly for overhead/ROI metrics. Today it reads
only `vanilla-baseline.json` (composite score). The SUMMARY adds the "at what cost"
side of the ROI equation.

---

## Forensic guarantees

Every activate/deactivate/collect event appends one line to
`faerie2/forensics/baseline-runs-coc.jsonl`:

```json
{
  "ts": "2026-04-20T...Z",
  "action": "activate|deactivate|run_collected",
  "session_id": "...",
  "settings_hash_before": "sha256:...",
  "settings_hash_after":  "sha256:...",
  "operator": "system",
  "prev_entry_hash": "...",
  "entry_hash": "sha256 of body"
}
```

- **Append-only.** Never rewrite. Verification = walk the chain.
- **Hash-chained.** Each entry's `prev_entry_hash` must match the previous entry's
  `entry_hash`. Break = tampered.
- **Transcript SHA-256.** Archived transcripts are hashed at copy time; the hash
  lives in `metadata.json`. Re-hash later to verify the archive is untampered.

Run a chain-verification pass with:

```bash
python3 - << 'EOF'
import hashlib, json, pathlib
p = pathlib.Path("forensics/baseline-runs-coc.jsonl")
prev = ""
for i, line in enumerate(p.read_text().splitlines(), 1):
    if not line.strip(): continue
    rec = json.loads(line)
    recorded = rec.pop("entry_hash")
    recomputed = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
    ok_self  = recorded == recomputed
    ok_chain = rec["prev_entry_hash"] == prev
    print(f"{i:3d} {rec['action']:16s} self={ok_self} chain={ok_chain}")
    prev = recorded
EOF
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `--activate` says "already active" | A prior run didn't deactivate cleanly. Remove the flag manually: `rm ~/.claude/state/VANILLA_BASELINE_ACTIVE` (after confirming you aren't in an unintended vanilla session). |
| `--deactivate` finds no transcripts | Claude CLI writes transcripts to `~/.claude/projects/` by default. On WSL your `$HOME` may differ between shells — check `echo $HOME` in the vanilla shell. If transcripts are on `/mnt/c/`, the deactivator already scans there. |
| "No backup found" | Look in `~/.claude/` for `settings.json.faerie-on.*`. If none exists, the activate step never fired — your settings.json is already your real faerie config. |
| Safety refusal ("test key") | Your `ANTHROPIC_API_KEY` in settings.json contains `test` or starts `sk-ant-test`. Remove the override or use a prod key before activating. |
| `baseline-runs/SUMMARY.json` shows 0 runs | You've activated/deactivated but the transcript archive step found no JSONLs post-dating activation. Check `~/.claude/projects/*/` mtimes. |
