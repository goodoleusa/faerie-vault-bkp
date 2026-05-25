# Stigmergic Recursion — f(0) Execution Pattern

**Why not nested Agent() calls?** Nested agents blow up call stack and context. **Why not polling?** Polling burns tokens and latency. **Solution:** filesystem-based recursion via manifest queuing.

## Problem: Nested Agent() is Blocked

The spawn protocol (agents.md §6) explicitly prohibits:
```python
# WRONG: nested team or Agent() inside an agent
Agent(subagent_type="child-agent", prompt="...")  # ← BLOCKED by PreToolUse hook
```

Why? Each Agent() call is:
- ~15 tokens to emit (spawn overhead)
- ~1.6K-1.9K tokens to receive (bundle size)
- ~100 tokens to return (manifest)

Nested chains explode: 2^depth overhead. A fan-out of 5 children × 3 grandchildren × 2 great-grandchildren = 30 agents, each with nested-stack burden.

## Solution: Queue-Write Pattern (next_task_queued)

Instead of spawning a child agent directly, **write the child's specification to the queue**.

**Agent A (parent):**
```python
# Agent does work, then writes manifest with next_task_queued field
manifest = {
  "task_id": "parent-task-123",
  "agent": "parent-agent-type",
  "status": "final",
  "findings": {...},
  
  # KEY: Tell the orchestrator about the next task
  "next_task_queued": {
    "id": "child-task-456",
    "title": "Analyze findings from parent",
    "description": "Parent found X, Y, Z. Analyze implications for Z.",
    "priority": "HIGH",
    "category": "analysis",
    "goal_one_line": "Deep-dive analysis of parent findings"
  }
}
# Write to manifest_path (e.g., ~/.claude/hooks/state/wave2-parent-result.json)
```

**PostToolUse Hook (4x_manifest_ingest_hook.py):**
```python
# Fires automatically after Agent() returns
# Reads manifest.next_task_queued
# Calls: python3 7x_queue_ops.py ingest-manifest {manifest_path}
# queue_ops auto-inserts the new task into sprint-queue.json
```

**Next /run Cycle:**
```python
# Later, when main calls /run again
# Orchestrator batch-claims the new HIGH task
# Spawns Agent B with the queued spec
# Agent B continues the work
```

## Data Flow Diagram

```
Agent A (W2) completes
       ↓
Agent A writes manifest with next_task_queued: {id: B, title: ..., priority: HIGH}
       ↓
4x_manifest_ingest_hook.py fires (PostToolUse)
       ↓
7x_queue_ops.py ingest-manifest {manifest_path}
       ↓
sprint-queue.json += {id: B, priority: HIGH, claim_state: unclaimed}
       ↓
Main session calls /run (immediately or later)
       ↓
7x_queue_ops.py batch-claim(1, HIGH) → claims task B
       ↓
run.py renders context bundle for B
       ↓
Agent B spawns, continues work
```

**Stack depth:** Constant O(1), regardless of chain length.

## Example: Fan-Out to 5 Children

**Parent agent finishes, writes manifest:**
```json
{
  "task_id": "task-A",
  "agent": "discovery-agent",
  "status": "final",
  "findings": {
    "entities": [
      {"name": "Entity-1", "risk": "high"},
      {"name": "Entity-2", "risk": "high"},
      {"name": "Entity-3", "risk": "medium"},
      {"name": "Entity-4", "risk": "medium"},
      {"name": "Entity-5", "risk": "low"}
    ]
  },
  "next_task_queued": {
    "id": "task-B1",
    "title": "Deep-dive: Entity-1",
    "priority": "HIGH",
    "category": "analysis"
  }
}
```

**4x_manifest_ingest_hook queues the child.** But agent can only write ONE `next_task_queued` field. To fan out to 5 children:

**Option 1: Sequential writes (preferred)**
Agent writes manifest #1 with B1. After ingest, when /run picks B1, agent B1 finishes and writes B2, etc. Linear chain of 5 tasks.

**Option 2: Multiple manifests (NEW)**
If a single manifest has `next_tasks_queued` (array instead of object):
```json
{
  "next_tasks_queued": [
    {"id": "B1", "title": "...", "priority": "HIGH"},
    {"id": "B2", "title": "...", "priority": "HIGH"},
    {"id": "B3", "title": "...", "priority": "HIGH"},
    {"id": "B4", "title": "...", "priority": "MED"},
    {"id": "B5", "title": "...", "priority": "MED"}
  ]
}
```

**Enhancement needed:** Update `4x_manifest_ingest_hook.py` to handle `next_tasks_queued` array (see ENHANCEMENT section below).

With this, parent fans out to 5 children in one manifest write.

## Full Example: 3-Level Fan-Out (1 + 5 + 15 = 21 agents)

**Wave 1: Parent (discovery-agent)**
- Reads raw data
- Identifies 5 entities of interest
- Writes manifest with next_tasks_queued: [B1, B2, B3, B4, B5]
- 4x_manifest_ingest_hook queues all 5 into sprint-queue.json

**Wave 2: 5 Children (analysis-agent × 5)**
- /run batch-claims 4 of the 5 (claims 4 max by default, rest on next cycle)
- Each B_i analyzes entity i, finds 3 sub-topics
- Each B_i writes next_tasks_queued: [C_i1, C_i2, C_i3] (3 per parent)
- All 5 manifests fire ingest hook → queue gets 15 grandchildren (5 × 3)

**Wave 3: 15 Grandchildren (deep-analysis-agent × 15)**
- /run claims 4 grandchildren per batch (or all 15 in one cycle if --max-count 15)
- Each C_ij performs deep synthesis, writes final manifest (no next_task_queued)
- All grandchildren complete

**Total agents spawned: 1 + 5 + 15 = 21**
**Stack depth: O(1) at all times**
**Call-stack burden: Zero (zero nested Agent() calls)**

Compare to nested Agent() pattern:
- Parent calls Agent(B1); B1 calls Agent(C1); C1 calls Agent(...) 
- Stack depth = 21; context paid per level
- Each Agent() call = ~2K tokens overhead on top of work

## Implementation Checklist

**VERIFIED (already in place):**
- [x] 4x_manifest_ingest_hook.py exists at /mnt/d/0local/gitrepos/faerie2/hooks/
- [x] 7x_queue_ops.py has `ingest-manifest` subcommand
- [x] should_ingest() checks for next_task_queued field
- [x] Atomic claiming with claim_state + claimed_at
- [x] Stale claim release (5-min TTL)

**ENHANCEMENT (next iteration):**
- [ ] Update 4x_manifest_ingest_hook.py to handle next_tasks_queued (array)
- [ ] Update 7x_queue_ops.py ingest-manifest to loop over array
- [ ] Document in manifest schema: both next_task_queued and next_tasks_queued valid

## Why This Works (f(0) Property)

**Orchestration burden on main = O(1):**
- Main calls /run once per batch (or in a loop)
- /run reads queue (O(N) where N = queue size)
- /run claims next task (O(1) with atomic lock)
- /run emits bundle (O(1) per task)
- Main spawns agents (constant per batch, not per agent)

**No SendMessage, no polling:** Agents can't talk to main. Next-task discovery happens via filesystem reads, not message queues.

**Fault-tolerant:** If an agent crashes, its manifest isn't written. The task stays claimed for 5 min, then is released and can be reclaimed by another session.

**Scales to arbitrary depth:** 1 parent → 100 children → 10,000 grandchildren, all via filesystem, zero call-stack overhead.

## Related

- Orchestrator CLI: `~/.claude/skills/run/run.py`
- Manifest hook: `/mnt/d/0local/gitrepos/faerie2/hooks/4x_manifest_ingest_hook.py`
- Queue ops: `/mnt/d/0local/gitrepos/faerie2/scripts/7x_queue_ops.py`
- Spawn contract: `faerie2/docs/SPAWN-CONTRACT.md`
- Design memo: `CLAUDE.md` (principle #1: stigmergy-only)

