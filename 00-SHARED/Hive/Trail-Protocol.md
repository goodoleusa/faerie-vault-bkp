---
type: design-narrative
status: final
created: 2026-03-29
topic: Trail Protocol — DAE Stigmergy Layer
tags: [architecture, trail, stigmergy, recovery, pipeline, orchestration]
parent: "[[00-SHARED/Hive/Hive-Index]]"
doc_hash: sha256:8af0738b0438ba00e62a9571519efb0c9655094190a4dff512a5542eef08a80d
hash_ts: 2026-03-29T16:10:29Z
hash_method: body-sha256-v1
---

# Trail Protocol — DAE Stigmergy Layer

## The Problem It Solves

Before this protocol existed, the DAE pipeline had no persistent record of what had run. All state — which stages completed, what they produced, how many rows passed through, what failed and why — lived in the orchestrating agent's context window or in the human's memory. When a session ended or an agent crashed, that state evaporated. There was no machine-readable answer to "where did we leave off?"

This created three failure modes that happened repeatedly:

1. **Session restart = cold start.** Every new agent invocation required the human to reconstruct pipeline state through back-and-forth: "Did stage 3a finish? How many rows did 2f ingest?" Even when the human remembered, the reconstruction took turns and tokens. When the human didn't remember, analysis could be re-run unnecessarily or skipped silently.

2. **Crash = lost work.** If 3a failed mid-run, the only record was an error in a terminal session that had since closed. A resuming agent had no way to know: did it fail before or after writing its outputs? Were the partial outputs trustworthy? Which column caused the failure? This was all context the human had to manually re-provide.

3. **Agent-to-agent handoff required human relay.** If Agent A completed stage 2f and Agent B needed to run stage 3a, B had to be told by the parent prompt that A was done and where A's outputs lived. There was no environment state B could query directly. Every handoff was a verbal relay — fragile, context-dependent, impossible to automate.

---

## Before: How Recovery Worked (the painful way)

1. Human notices pipeline is stopped.
2. Human checks their own notes or terminal history to figure out which stage last ran.
3. Human opens a new session and types something like: "Stage 2f finished — it ingested 1420 rows. Stage 3a failed with a column error. Please fix the column issue and re-run 3a, then continue with 3b through 6a."
4. Agent does the work. State evaporates again at session end.
5. Next session: repeat from step 1.

Every recovery path went through the human. The pipeline could not self-describe. An agent landing in the middle of a run had no way to assess the situation without interrogating a person.

---

## After: How Recovery Works (trail-first)

1. Agent starts. Runs `python lib/trail_reader.py RUN-007` — takes 200ms.
2. Trail shows: 0a final, 2a final, 2f final, 3a failed (error: missing column 'ip_dst'), 3b pending.
3. Agent fixes the column, reruns 3a via `stage_run("3a", ...)`, trail updates automatically.
4. Agent runs `trail_reader.py RUN-007 --next` → returns `3b`.
5. Session ends. Trail persists to disk. Next session: step 1 again, zero reconstruction needed.

The trail is truth. The trail is the handoff note. Agents only ask a human if the trail is empty AND no run directory exists — meaning the investigation genuinely hasn't started yet.

---

## Principle

Every pipeline stage writes a manifest on completion (or failure). `trail_reader.py` reads
all manifests for a run and produces a machine-readable + human-readable trail summary.
Orchestrators and resuming agents read the trail first — they never ask a human or parent
agent what ran unless the trail is empty.

## Layout

```
scripts/audit_results/
  runs/
    RUN-007/
      manifests/
        0a-manifest.json
        2a-manifest.json
        3a-manifest.json    <- failed: missing column 'ip_dst'
        3b-manifest.json    <- pending (written by orchestrator as placeholder)
```

Run IDs follow the existing convention: `RUN-001`, `RUN-002`, etc. (uppercase).
Stage IDs match script prefixes: `0a`, `2a`, `2b`, `2c`, `2d`, `2e`, `2f`,
`3a`, `3b`, `3c`, `3d`, `4a`, `4b`, `5a`, `6a`.

## Manifest Schema (`lib/manifest_schema.py`)

Each manifest is a JSON file with these fields:

| Field | Type | Description |
|---|---|---|
| `run_id` | str | e.g. `"RUN-007"` |
| `stage` | str | e.g. `"3a"` |
| `script` | str | script filename |
| `status` | str | `pending` / `in_progress` / `partial` / `final` / `failed` |
| `started_at` | str | ISO8601 or null |
| `completed_at` | str | ISO8601 or null |
| `outputs` | list[str] | file paths written by this stage |
| `input_from` | str | which stage fed this one, e.g. `"2f"` |
| `next_stage` | str | recommended next stage, or null |
| `error` | str | error message if failed, null otherwise |
| `row_counts` | dict | e.g. `{"ingested": 1420, "cleaned": 1387}` |
| `sha256` | str | hash of primary output file (COC anchor) |
| `notes` | str | free-text for trail readers |

## Key Functions

### manifest_schema.py
```python
from lib.manifest_schema import write_manifest, read_manifest, update_status, StageManifest

m = StageManifest(run_id="RUN-007", stage="3a", script="3a-pipeline-orchestrator.py", ...)
write_manifest(m, run_dir)
m = read_manifest(run_dir, "3a")
update_status(run_dir, "3a", "failed", error="missing column 'ip_dst'")
```

### stage_wrapper.py
```python
from lib.stage_wrapper import stage_run

with stage_run("3a", run_id=args.run_id) as stage:
    stage.set_input("2f")
    stage.add_output("scripts/audit_results/runs/RUN-007/3a/cleaned.csv")
    stage.set_rows(ingested=1420, output=1387)
    stage.set_next("3b")
    # clean exit: status=final  |  exception: status=failed, error captured
```

### trail_reader.py
```bash
python lib/trail_reader.py RUN-007           # full trail
python lib/trail_reader.py RUN-007 --next    # machine-readable next stage
python lib/trail_reader.py RUN-007 --failed  # failed stages only
python lib/trail_reader.py RUN-007 --resume  # shell snippet to continue
python lib/trail_reader.py --list            # all runs with status summary
```

## Stage Ordering

Stages sort numerically then alphabetically: `0a < 1f < 1g < 1h < 2a < 2b < ... < 2f < 3a < ... < 6a`.
Sort key: `(int(numeric_prefix), alpha_suffix)` — never lexicographic.

## Trail Output Example

```
RUN-007 trail:
  v 0a   coc-genesis-ledger      final      2026-03-29 14:22   rows: in=1420
  v 2a   ingest-rawdata          final      2026-03-29 14:23   rows: in=1420
  v 2f   build-manifest          final      2026-03-29 14:29   rows: in=1420 out=1420
  x 3a   pipeline-orchestrator   failed     2026-03-29 14:31   error: missing column 'ip_dst'
  o 3b   pipeline-clean          pending    --

  NEXT: fix 3a (missing column 'ip_dst'), then run 3b
```

## Atomic Write Safety

All manifest writes use temp file + `os.replace()` rename:
- Crash mid-write cannot corrupt a previously completed manifest.
- Parallel stage writes cannot corrupt each other.
- Readers always see a complete JSON file or the previous version.

## Agent Resume Protocol

1. `python lib/trail_reader.py {RUN_ID}` — read the trail.
2. Find last `final` and first non-`final` stage.
3. Check `--failed` — fix before proceeding.
4. Use `--next` for machine-readable routing.
5. Only ask parent if trail is empty AND no run directory exists.

The trail is truth. The trail is the handoff note. The trail IS the stigmergy.

---

## What Breaks If You Skip This

Skipping the trail protocol doesn't cause an immediate failure — it causes silent degradation.

| Skipped component | What stops working |
|---|---|
| `stage_wrapper.py` on a stage | That stage produces no manifest. Trail shows a gap. `trail_reader --next` cannot route past it. Orchestrators and resuming agents treat the gap as "not run" even if it completed. |
| `manifest_schema.py` (write_manifest) | No persistent record of what the stage produced. Row counts, output paths, and SHA-256 anchors go unrecorded. Future stages cannot verify their input came from a completed upstream stage. |
| `trail_reader.py` at resume | Agent goes back to asking the human. All the recovery work described above comes back. One missed trail read = one human relay. Multiplied across sessions = constant interruption. |
| Trail directory (`runs/RUN-NNN/manifests/`) not created | trail_reader returns "no trail" and the protocol degrades to manual reconstruction. The manifest writes fail silently unless the directory exists first. |
| Stage status update after failure (`update_status(..., "failed", error=...)`) | The trail shows the stage as `in_progress` forever. Resuming agents see it as active and skip it. The failure goes unrecorded. Diagnosis requires reading raw output files instead of the trail. |

The trail protocol is cheapest to adopt at stage write time (add `stage_wrapper` context manager, costs ~10 lines) and most expensive to recover without (costs human reconstruction time, session turns, and pipeline restart risk). Adopt it at the time of writing or rewriting each stage script.

*Written 2026-03-29. Extends Trail-Protocol.md technical spec with problem narrative and failure mode documentation.*
