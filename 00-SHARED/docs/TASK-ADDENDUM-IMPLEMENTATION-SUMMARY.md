# Task Addendum Stigmergy Channel — Implementation Summary

**Task:** task-20260424-stigmergy-addendums-1  
**Completed:** 2026-04-24T21:04:00Z  
**Status:** Production-Ready

## Overview

Implemented a **stigmergy-based mid-flight instruction channel** allowing main to send corrected or new instructions to running agents without restarting them. Agents poll at checkpoints for addendums; urgent priorities trigger immediate re-read.

## Components Implemented

### 1. Agent-Side Reader Utility (NEW)

**File:** `scripts/9x_addendum_reader.py` (7.6 KB, executable)

- **Purpose:** Agents call this at each checkpoint to read new instructions
- **Commands:**
  - `check --task-id X --agent-id Y` — Get new addendums since last read (updates cursor)
  - `get-all --task-id X` — Get all addendums (no cursor update)
  - `reset --task-id X --agent-id Y` — Reset cursor to 0 for full re-read
- **Per-agent cursor tracking:** `.cursors/{agent_id}_{task_id}.pos` — isolates each agent's read state
- **Output:** JSON with `new_count`, `cursor_was/now`, `addendums[]`, `any_urgent` flag

### 2. CLI Command (MODIFIED)

**File:** `scripts/7x_queue_ops.py`

**New subcommand:** `addendum`
```bash
python3 scripts/7x_queue_ops.py addendum TASK_ID \
  --text "instruction text" \
  [--priority urgent|normal] \
  [--source "reason"]
```

- **Validation:** Text must be 1-500 characters
- **Priority:** `urgent` (immediate) or `normal` (at checkpoint)
- **Storage:** Append-only JSONL at `~/.claude/hooks/state/task-addendums/{task_id}.jsonl`
- **Output:** JSON success/error response with line number

### 3. Spawn Template Boilerplate (NEW)

**File:** `.claude/spawn-templates/common-boilerplate/task-addendum-protocol.md` (1.2 KB)

- **Purpose:** Instructions injected into all agent spawn prompts
- **Content:** Tells agents to call the reader at checkpoints, handle urgent/normal priorities
- **Usage in templates:** Reference via partial name; `{{task_id}}` injected automatically
- **Fail-safe:** Graceful degradation if reader unavailable

## Architecture

### Data Flow

```
Main                        Filesystem                Agent
─────────────────────────────────────────────────────────────
Write addendum    ─→   task-addendums/{task_id}.jsonl
                          (append-only, JSON lines)
                                                    ←─  Poll at checkpoint
                                              Check if new since cursor
                                              Read addendums[]
                                              Update .cursors/{agent}_{task}.pos
```

### Storage Locations

| Path | Purpose | Format |
|------|---------|--------|
| `~/.claude/hooks/state/task-addendums/{task_id}.jsonl` | Addendum queue | JSONL (one object per line) |
| `~/.claude/hooks/state/task-addendums/.cursors/{agent}_{task}.pos` | Read cursor | Integer (line number) |

### JSON Schema

**Addendum object (one per line in .jsonl):**
```json
{
  "ts": "ISO8601 timestamp",
  "from": "main",
  "addendum": "Text 1-500 chars",
  "priority": "urgent|normal",
  "source_context": "optional reason"
}
```

**Reader response (check command):**
```json
{
  "new_count": N,
  "cursor_was": N,
  "cursor_now": N,
  "addendums": [...],
  "any_urgent": bool
}
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Append-only .jsonl** | Immutability + forensics + concurrent safety |
| **Per-agent cursors** | Isolates independent agents; prevents read-ahead issues |
| **Two priority levels** | Urgent = stop+re-read; normal = incorporate at next checkpoint |
| **No SendMessage** | Stigmergy-first: passive discovery, no bidirectional coupling |
| **Text-only (≤500 chars)** | Small fixes/pivots; large context goes via manifest paths |
| **Fail-safe** | Optional optimization layer; absence degrades gracefully |

## Testing Results

All manual tests passed:

- ✓ Write normal addendum → agent reads once → cursor advances → no re-read
- ✓ Write urgent addendum → agent sees `any_urgent=true`
- ✓ Multiple agents on same task → independent cursor tracking
- ✓ Reset cursor → agent re-reads from beginning
- ✓ CLI validation → rejects >500 char text, invalid priority

## Integration Points

### For Template Authors

Templates can include the addendum protocol by adding to `body_partials`:

```json
{
  "body_partials": ["task-addendum-protocol.md", ...]
}
```

The partial will automatically inject checkpoint-polling instructions using `{{task_id}}` from context.

### For Agents at Runtime

At each checkpoint, agents call:
```bash
RESULT=$(python3 ~/.claude/scripts/9x_addendum_reader.py check \
  --task-id "$TASK_ID" \
  --agent-id "$AGENT_RUN_ID")

# Parse JSON, check any_urgent, read addendums array
```

### For Main / Orchestrators

Send an addendum:
```bash
python3 scripts/7x_queue_ops.py addendum task-xyz \
  --text "Focus on X instead of Y" \
  --priority urgent \
  --source "downstream contradiction found"
```

## Limitations

1. **No acknowledgment:** Main doesn't know when agent reads
2. **No bidirectional messaging:** Agents can't ask questions
3. **Eventually consistent:** If agent already reading at the moment addendum is written, it may miss one (rare)
4. **Text-only:** For large context, use manifest files

## Future Extensions

- Batch addendums (write multiple at once)
- TTL (auto-expire old addendums)
- Rollback (retract an addendum)
- Acknowledgment beacon (agent marks read)
- Selective filtering (agents filter by tag)

## Files Changed

### Created
- `scripts/9x_addendum_reader.py`
- `docs/TASK-ADDENDUM-DESIGN.md` (detailed design)
- `.claude/spawn-templates/common-boilerplate/task-addendum-protocol.md`

### Modified
- `scripts/7x_queue_ops.py` — added `cmd_addendum()` function + CLI parser + handler

### Manifest
- `/mnt/d/0LOCAL/.claude/hooks/state/wave2-stigmergy-addendums.json` — final result

## Verification Commands

```bash
# 1. Write
python3 scripts/7x_queue_ops.py addendum test-verify --text "test" --priority normal

# 2. Agent reads
python3 scripts/9x_addendum_reader.py check --task-id test-verify --agent-id agent-1

# 3. Verify cursor advanced
python3 scripts/9x_addendum_reader.py check --task-id test-verify --agent-id agent-1

# 4. Write urgent
python3 scripts/7x_queue_ops.py addendum test-verify --text "URGENT" --priority urgent

# 5. Different agent sees all
python3 scripts/9x_addendum_reader.py check --task-id test-verify --agent-id agent-2
```

Expected: All commands succeed; cursor tracking works; agents see urgent flag.

## Context Cost

- **Spawn injection cost:** ~50 tokens per agent (static boilerplate partial)
- **Runtime cost:** ~15 tokens per checkpoint poll (reader script invocation)
- **Storage cost:** ~100 bytes per addendum (JSON + timestamp)

## Phase Classification

**Phase 3 of Queue Operations** — Completes the stigmergy layer:
- Phase 1: Atomic agent-level claiming (2026-04-21)
- Phase 1.5: Monkeybranching (2026-04-21)
- Phase 2: Piston checkpoint sync (2026-04-24)
- **Phase 3: Task addendum channel (2026-04-24)** — THIS TASK

## Related Work

- Queue claiming: `scripts/7x_queue_ops.py`
- Agent orchestration: `scripts/7x_spawn_template.py`
- Stigmergy tracking: `scripts/9x_stigmergy_tracker.py`
- Task droplet discovery: `scripts/9x_task_droplet_discovery_bootstrap.py`

## Conclusion

The task-addendum channel provides a **lightweight, stigmergic way to correct running agents in-flight** without restart overhead. Append-only storage ensures forensic integrity; per-agent cursors enable safe concurrent reads; two priority levels allow nuanced flow control.

Ready for production integration into spawn templates and agent workflows.
