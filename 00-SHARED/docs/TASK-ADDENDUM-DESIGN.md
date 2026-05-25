# Task Addendum Stigmergy Channel — Design Document

**Task:** task-20260424-stigmergy-addendums-1  
**Status:** Complete  
**Date:** 2026-04-24

## North Star

Enable main to send corrected or new instructions to a running agent **without restarting or replacing the agent**. Pattern: append-only channel + per-agent cursor tracking + checkpoint polling.

## Architecture

### Storage Layer

**Addendum files** (append-only, JSONL):
```
~/.claude/hooks/state/task-addendums/{task_id}.jsonl
```

Each line is a JSON object:
```json
{
  "ts": "ISO8601 timestamp",
  "from": "main",
  "addendum": "Text of correction or new instruction (1-500 chars)",
  "priority": "urgent|normal",
  "source_context": "Optional: pipeline change, user correction, etc"
}
```

**Cursor files** (per-agent read position):
```
~/.claude/hooks/state/task-addendums/.cursors/{agent_id}_{task_id}.pos
```

Content: single integer (last-read line number, 0-indexed).

### CLI Operations (Main Side)

**Write addendum:**
```bash
python3 scripts/7x_queue_ops.py addendum \
  --task-id task-xyz \
  --text "New instruction: focus on X instead of Y" \
  --priority urgent \
  --source "pipeline change discovered"
```

Response:
```json
{
  "success": true,
  "task_id": "task-xyz",
  "priority": "urgent",
  "line_number": 0,
  "file": "/path/to/task-addendums/task-xyz.jsonl",
  "message": "Addendum added (priority=urgent)"
}
```

### Agent Operations (Agent Side)

**Check for new addendums** (at each checkpoint):
```bash
python3 ~/.claude/scripts/9x_addendum_reader.py check \
  --task-id task-xyz \
  --agent-id $AGENT_RUN_ID
```

Response:
```json
{
  "new_count": 1,
  "cursor_was": 3,
  "cursor_now": 4,
  "addendums": [
    {
      "ts": "2026-04-24T15:30:42Z",
      "from": "main",
      "addendum": "Skip section 2.3; focus on X instead",
      "priority": "urgent",
      "source_context": "downstream contradiction"
    }
  ],
  "any_urgent": true
}
```

**Get all addendums** (no cursor update):
```bash
python3 ~/.claude/scripts/9x_addendum_reader.py get-all --task-id task-xyz
```

**Reset cursor** (force re-read from line 0):
```bash
python3 ~/.claude/scripts/9x_addendum_reader.py reset \
  --task-id task-xyz \
  --agent-id $AGENT_RUN_ID
```

### Spawn Template Integration

**Partial:** `.claude/spawn-templates/common-boilerplate/task-addendum-protocol.md`

Instructions injected into all agent prompts via the spawn template system. Agents are told to:
1. Call the reader at each checkpoint
2. If `any_urgent == true`, stop and re-read immediately
3. If `new_count > 0` and `priority == normal`, incorporate at next checkpoint
4. Fail gracefully if the reader script is unavailable

**Usage in templates:** Simply reference the partial to include it. The partial uses `{{task_id}}` which is automatically in the context.

## Design Decisions

### Why Append-Only?

- **Immutability:** Once written, addendums never change. Chain of command is clear.
- **Forensics:** Every instruction change is logged; no overwriting.
- **Concurrent Safety:** Multiple addendums can be added in parallel; no locking needed for reads.

### Why Per-Agent Cursors?

- **Isolation:** Agent A doesn't interfere with Agent B's reading; each tracks independently.
- **Idempotency:** Calling `check` twice with the same agent_id returns different results (cursor advances).
- **Efficiency:** Agents don't re-read old addendums they already processed.

### Why Two Priority Levels?

- **Urgent:** Stop work immediately, re-plan based on correction. Used for critical pivots discovered downstream.
- **Normal:** Incorporate at next checkpoint. Used for minor clarifications or context additions.

### Why Not Messaging or SendMessage?

- **Stigmergy-first:** No bidirectional coupling; main writes to a location, agents discover passively.
- **Parallel agents:** Multiple agents reading the same task's addendums doesn't race.
- **Simplicity:** No queue management, no message delivery guarantees — pure filesystem.

### Why Not Replace the Agent?

- **Context preservation:** Agent keeps working context, memory, partial results.
- **Efficiency:** Re-spawning costs 15–50 tokens + restart overhead; addendum is <1 token.
- **Autonomy:** Agent chooses when to check (at checkpoints); not reactive interrupts.

## Limitations

1. **No acknowledgment:** Main doesn't know when agent reads an addendum. Best-effort delivery.
2. **No bidirectional messaging:** Agents can't ask follow-up questions via the channel.
3. **Text-only:** Addendums are small strings (≤500 chars). For large context, use manifest paths.
4. **Weak ordering:** If main sends addendums A, B, C in quick succession, agent may see them out of order (file append isn't instantaneous across all processes). In practice, this is rare; agents check infrequently.

## Example Workflows

### Mid-Flight Pivot

1. **Agent starts** task-xyz: broad research phase
2. **Downstream task** completes, finds contradiction
3. **Main calls** `addendum --task-id task-xyz --priority urgent --text "Stop broad search; focus on X"`
4. **Agent polls** at next checkpoint, sees urgent flag
5. **Agent stops current work**, re-reads the addendum, and pivots

### Minor Clarification

1. **Agent running** task-abc: needs minor context
2. **Main calls** `addendum --task-id task-abc --priority normal --text "See updated file at /path/..."`
3. **Agent continues** until next checkpoint
4. **Agent reads** the addendum, checks the file, and adjusts if needed

## Testing

See `/mnt/d/0local/gitrepos/faerie2/tests/` for automated test suite (when added).

Manual test:
```bash
# 1. Write an addendum
python3 scripts/7x_queue_ops.py addendum test-task --text "test" --priority normal

# 2. Read it (should show new_count=1)
python3 scripts/9x_addendum_reader.py check --task-id test-task --agent-id agent-001

# 3. Read again (should show new_count=0, cursor advanced)
python3 scripts/9x_addendum_reader.py check --task-id test-task --agent-id agent-001

# 4. Write another
python3 scripts/7x_queue_ops.py addendum test-task --text "test2" --priority urgent

# 5. Read (should show new_count=1)
python3 scripts/9x_addendum_reader.py check --task-id test-task --agent-id agent-001
```

## Future Extensions

1. **Batch addendums:** Send multiple addendums in one command for efficiency.
2. **Addendum TTL:** Auto-expire old addendums after N days.
3. **Selective read:** Agents filter by priority or age.
4. **Acknowledgment beacon:** Agent writes a marker after reading urgent addendum.
5. **Rollback:** Retract an addendum if mistake discovered.

## Files

- **Scripts:** 
  - `scripts/7x_queue_ops.py` (added `cmd_addendum` + CLI parser)
  - `scripts/9x_addendum_reader.py` (new utility)
- **Boilerplate:**
  - `.claude/spawn-templates/common-boilerplate/task-addendum-protocol.md` (partial)
- **Docs:**
  - This file: `docs/TASK-ADDENDUM-DESIGN.md`
