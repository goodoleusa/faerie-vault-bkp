# Durable State Loader — Minimal File Reads for Piston Momentum

**Problem:** To solve ephemeral state loss on auto-compact, agents need access to durable state. But reading too many files bloats context and violates equilibrium.

**Solution:** Load ONLY essential durable state. Everything else flows via stigmergy (streaming, filesystem signals).

---

## What to Read (Bare Minimum)

### Must Read (Always)
- **Agent's own card:** `~/.claude/agents/{agent_type}.md` (≤80 lines, ~300 tokens)
  - Contains: KPIs, techniques, recent training
  - When: At agent startup (HONEY.md Step Zero pattern)
  - Why: Agents need to know their own training context

### Conditional Read (Only if recovering)

**If resuming from auto-compact:**
- **Piston checkpoint:** `~/.claude/hooks/state/piston-checkpoint.json` (≤10 lines, ~100 tokens)
  - Contains: Wave state, agents in-flight, resume plan
  - When: Only if agent is resuming mid-session (detect via shell/context summary)
  - Why: Tells agent which wave/task to pick up next

**If investigation task:**
- **NECTAR tail-30:** `~/.claude/memory/NECTAR.md` (last 1K chars, ~250 tokens)
  - Contains: Recent validated findings
  - When: Only if task explicitly asks for context on prior findings
  - Why: Investigation agents need to know what's been discovered

### DO NOT READ (Let /run provide)
- ❌ **Full sprint-queue.json** — Too large (68KB, unbounded)
  - Instead: Claimed task provides metadata in return object
  - Agent receives: `{task_id, goal, context_bundle, source_files, ...}` from claim
  - Pattern: `python3 queue_ops.py claim` returns ONE task object, not whole queue
- ❌ **All agent cards** — Load only your own type
- ❌ **All NECTAR.md** — Load tail-30 only, and only if investigation
- ❌ **REVIEW-INBOX** — Not agent responsibility; membot handles at /handoff

---

## Piston Checkpoint Format

File: `~/.claude/hooks/state/piston-checkpoint.json` (written by pre_compact_hook)

```json
{
  "checkpoint_ts": "2026-03-30T01:45:00Z",
  "compact_trigger": "context_heavy",
  "current_wave": 2,
  "agent_state": {
    "in_flight": [
      {"agent_id": "a541145f", "task_id": "OSINT-BREADCRUMB-001", "claimed_at": "2026-03-30T01:30:00Z"},
      {"agent_id": "ac3acefe", "task_id": "INGEST-DAE-001", "claimed_at": "2026-03-30T01:35:00Z"}
    ],
    "next_fast": "INGEST-SPIDERFOOT-VERIFY",
    "next_medium": null,
    "next_deep": null
  },
  "next_action": "LAUNCH_WAVE_2_MEDIUM"
}
```

At startup: If this file exists and agent sees its task_id in `in_flight[]`, it's resuming. Read the whole file.

---

## Code Pattern: Minimal Startup

```python
import os
import json
from pathlib import Path

# Step 1: Read own agent card (always)
agent_type = "data-engineer"  # or read from env
agent_card_path = Path.home() / ".claude" / "agents" / f"{agent_type}.md"
if agent_card_path.exists():
    with open(agent_card_path) as f:
        agent_context = f.read()  # ~300 tokens
    print(f"Loaded agent card: {len(agent_context)} chars")

# Step 2: Check if resuming from auto-compact
piston_checkpoint = Path.home() / ".claude" / "hooks" / "state" / "piston-checkpoint.json"
if piston_checkpoint.exists():
    with open(piston_checkpoint) as f:
        checkpoint = json.load(f)

    # Check if this agent is in flight
    in_flight = checkpoint.get("agent_state", {}).get("in_flight", [])
    my_task = None
    for agent in in_flight:
        if agent.get("agent_id") == MY_AGENT_ID:
            my_task = agent
            break

    if my_task:
        print(f"Resuming task: {my_task['task_id']}")
        # Resume logic here
    else:
        print("Not in flight; proceeding normally")

# Step 3: Get task metadata from /run (not from queue file!)
# When /run spawns agent, it passes task object:
# {
#   "task_id": "OSINT-BREADCRUMB-001",
#   "goal": "...",
#   "context_bundle": "...",
#   "source_files": ["file1", "file2"],
#   ...
# }
# This comes from the TASK OBJECT claim returns, NOT from reading sprint-queue.json

# Step 4: Optional — read NECTAR tail if investigation
if is_investigation_task:
    nectar_path = Path.home() / ".claude" / "memory" / "NECTAR.md"
    if nectar_path.exists():
        with open(nectar_path) as f:
            lines = f.readlines()
            nectar_tail = "".join(lines[-50:])  # Last ~1K chars
        print(f"Loaded NECTAR tail: {len(nectar_tail)} chars")
```

**Total startup cost:**
- Agent card: ~300 tokens
- Piston checkpoint (if resuming): ~100 tokens
- NECTAR tail (if investigation): ~250 tokens
- **Total: ≤650 tokens per agent startup** (budget-safe)

---

## Anti-Pattern: What NOT to Do

❌ Read full sprint-queue.json on startup
  - Queue is 68KB, unbounded growth
  - Agent gets task metadata from claimed task object instead
  - Reading queue at startup = wasted context

❌ Load all of ~/.claude/agents/ to understand team
  - Each agent card is ~300-800 tokens
  - If you load 10 agent cards = 3-8K tokens gone
  - Instead: Read only your own card

❌ Load all of NECTAR.md
  - Could be 50K+ tokens (unbounded)
  - Instead: Load tail-30 (250 tokens) if investigation

---

## When /run Claims a Task

The `/run` command (or equivalent queue claim mechanism) returns task object:

```json
{
  "id": "task-20260330-145901-xyz",
  "task_id": "OSINT-BREADCRUMB-001",
  "goal_one_line": "OSINT investigation with breadcrumb trail...",
  "context_bundle": "Highest value: ... Done looks like: ... Source files: [...]",
  "source_files": ["targets.txt", "config.json"],
  "recommended_agent": "data-engineer",
  "category": "investigation",
  "priority": "HIGH",
  ...
}
```

**Agent does NOT need to:**
- Re-read sprint-queue.json to get this task
- Search the queue for their task
- Parse context from template files

**Agent does:**
- Receive task object as parameter/env from /run
- Extract context_bundle, source_files, goal from the object
- Load source_files if needed (not the template)

---

## Equilibrium Budget

| File | Size | Tokens | When | Load? |
|------|------|--------|------|-------|
| Agent card | ≤80L | ≤300 | Always | ✓ |
| Piston checkpoint | ≤30L | ≤100 | If resuming | ✓ |
| NECTAR tail | ≤50L | ≤250 | If investigation | ✓ |
| HONEY | ≤200L | ≤500 | N/A (membot loads) | ✗ |
| Full sprint-queue.json | 68KB+ | unbounded | N/A (task obj) | ✗ |
| Full NECTAR.md | ≤50K | unbounded | N/A (use tail) | ✗ |
| All agent cards | multiple | ≤3K | N/A (load own) | ✗ |

**Agent startup stays ≤650 tokens** when following this pattern.

---

## Summary

1. **Always read:** Agent's own card (~300T)
2. **Conditionally read:** Piston checkpoint if resuming (~100T), NECTAR tail if investigation (~250T)
3. **Never read:** Full queue, full NECTAR, all agent cards
4. **Get task metadata from:** Claimed task object returned by queue_ops.py, not from queue file
5. **For source context:** Load source_files list if needed (provided in task object), not template

This keeps equilibrium intact while ensuring piston momentum doesn't evaporate on auto-compact.
