---
type: system-guide
status: current
created: 2026-03-27
updated: 2026-03-27
tags:
  - system
  - state-files
  - guide
  - human-readable
  - faerie
parent:
  - "[[system-rules-guide]]"
sibling:
  - "[[AGENT-SYSTEM-ARCHITECTURE-ZIMA]]"
child: []
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:8fc605d28af4c7a87ccdb172cd43c452661ced26f90b8a42580277da428de441
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# State Files: How Faerie Tracks System State

All state files live at `C:\Users\amand\.claude\hooks\state\` (WSL: `~/.claude/hooks/state/`).

---

## Core State Files

### handoff-snapshot.json (~700KB)
**What:** Complete roundup of all memory sources — every project memory, scratch file, HIGH flag, queue state, hypothesis confidence. The "brain dump" at session end.
**Written by:** `emergency_handoff.py` (at /handoff Step Zero)
**Read by:** `/faerie` at next session start (replaces 15+ scattered file reads)
**Forensic link:** SHA256 of snapshot logged in `memory-collection-coc.jsonl`

### faerie-brief.json (~5KB)
**What:** Lightweight cold-start pointer. Contains: last session summary, queue snapshot, list of fragmented memory files to process, pointer to `brief-atoms/` directory.
**Written by:** `emergency_handoff.py`, `session_stop_hook.py`
**Read by:** `/faerie` (fallback if handoff-snapshot.json missing or stale)
**Not the source of truth** — just a pointer. The atoms collection IS the truth.

### sprint-queue.json (~77KB currently, needs archiving)
**What:** Task queue with priorities. Each task has: goal, done-looks-like, source_files, team assignment, context_bundle, status, timestamps.
**Written by:** `queue_ops.py` (add, claim, complete, fail, reorder)
**Read by:** `/faerie` (what to launch), `/run` (what to claim), `/queue` (display)
**Investigation link:** Tasks tagged with `investigation_id` and `hypothesis` fields

### handoff-checkpoint.json
**What:** Tracks which handoff steps completed. If auto-compact fires mid-handoff, re-invoking `/handoff` reads this and skips completed steps.
**Written by:** `emergency_handoff.py`
**Read by:** `/handoff` (idempotent re-entry)

### pending-hash-snapshot.json
**What:** Marker file requesting deferred hash_tracker work. Written by `/handoff` at 1% context (when running hash_tracker would be too slow). Next `/faerie` detects this and runs the snapshot when context is fresh.
**Written by:** `emergency_handoff.py`
**Read by:** `/faerie` Step 0
**Deleted after:** hash snapshot completes

---

## Memory Collection COC

### memory-collection-coc.jsonl
**What:** Hash-chained Chain of Custody log for every memory file collected by `emergency_handoff.py`. Each entry contains:
- `timestamp` — when collected
- `source_path` — where the file was
- `source_sha256` — hash BEFORE reading/moving
- `dest_path` — where it was nested
- `prev_entry_hash` — hash chain link to previous entry
- `entry_hash` — this entry's HMAC-SHA256

**Purpose:** Proves that memory collection didn't alter files. If a defense attorney asks "did your agent modify this memory file during collection?", the hash chain proves it didn't.

---

## Brief Atoms (accumulating checkpoints)

### brief-atoms/ directory
**What:** Each file is a JSON checkpoint — a snapshot of system state at a natural boundary (handoff, pipeline phase, sprint completion). Files accumulate; never overwritten.
**Written by:** `emergency_handoff.py` (handoff atoms), `briefgen.py` (pipeline atoms)
**Read by:** `/faerie` (reads latest N atoms to build context)
**Obsidian:** Rendered via Dataview queries + Blueprints templates

---

## Performance & Agent State

### run-benchmarks.json
**What:** Agent performance KPIs from recent runs. Agents read this to know baselines.
**Written by:** `performance-eval` agent
**Read by:** All agents at T2 (so they know what to beat)

### subagent-options.json
**What:** Maps task categories to agent teams. `"statistical_analysis" → ["data-scientist", "evidence-analyst"]`
**Read by:** All agents when spawning subagents

### task-states/{task_id}-{type}.json
**What:** Per-task state for resume capability. If an agent crashes mid-task, the next attempt reads this to continue.

---

## How State Links to Investigations

State files are **system-level** (they serve all investigations). Investigation-specific state lives in:
- `~/.claude/memory/investigations/{inv_id}/` — investigation index, hypotheses, forensics
- `{repo}/.claude/memory/scratch-*.md` — session-level working notes tagged with investigation

The bridge: `handoff-snapshot.json` contains a `per_investigation` section that groups memories, findings, and queue tasks by investigation ID. `/faerie` reads this to know which investigation threads are active.

---

*Source: emergency_handoff.py, session_stop_hook.py, queue_ops.py. Updated 2026-03-27.*
