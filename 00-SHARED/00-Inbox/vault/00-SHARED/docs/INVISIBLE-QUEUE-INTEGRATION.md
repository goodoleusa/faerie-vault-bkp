# Invisible Queue Integration — TaskList ↔ Sprint Queue

**Goal:** Human creates tasks via TaskList. Agents autonomously claim from queue. Both layers stay synced. **Human never hears about the queue.**

---

## The Two Layers (Hidden from Human)

### Layer 1: TaskList (User-Facing)
```
Human: TaskCreate → Task #27 "Implement queue claiming"
Status: pending
Human: Sees task in TaskList, watches it progress
```

### Layer 2: Sprint Queue (Agent-Facing)
```
Faerie startup: auto-syncs pending tasks from TaskList
Queue entry: {id: "task-27", status: "queued", claim_state: "unclaimed"}
Agent: autonomously claims, executes, completes
Queue entry: {id: "task-27", status: "completed"}
```

### The Bridge (Invisible Sync)
```
TaskList → Queue (sync_pending_to_queue at faerie startup)
Queue ← TaskList (sync_complete_to_tasklist via PostToolUse hook)
Queue maintenance (prune_queue every 5 min)
```

---

## Integration Points (Where the Magic Happens)

### 1. Faerie Startup (Cold Start or /faerie)

**Old behavior:**
```
Faerie reads sprint-queue.json manually (stale)
Faerie plans waves based on stale queue
```

**New behavior:**
```
Faerie startup:
  1. Call: queue_sync.py --sync-pending
     → Reads TaskList (from task-list-cache.json)
     → Adds pending tasks to sprint-queue.json
     → Logs to COC: "N tasks synced"
  
  2. Proceed with wave planning
     → Queue now reflects latest human intent
```

**Implementation (in faerie_training_orchestrator.py):**
```python
def faerie_startup():
    # Sync TaskList → queue
    subprocess.run([
        "python3", "scripts/queue_sync.py",
        "--sync-pending"
    ])
    
    # Now read fresh queue
    queue = read_sprint_queue()
    piston_plan = recommend_waves(queue)
    spawn_agents(piston_plan)
```

---

### 2. Agent Completion (PostToolUse Hook)

**Trigger:** Agent returns manifest

**Old behavior:**
```
PostToolUse hook calls: queue_ops.py complete {task_id}
TaskList never updated (stale)
```

**New behavior:**
```
PostToolUse hook:
  1. Read agent manifest
  2. Call: queue_sync.py --sync-complete --task-id {id} --manifest-path {path}
     → Updates TaskList: status = "completed", stores manifest
     → Human sees task mark as done in TaskList
  
  3. Then call: queue_ops.py complete {task_id}
     → Marks in sprint-queue.json (already done by agent manifest)
```

**Implementation (in manifest_task_autocompletion.py hook):**
```python
def on_agent_complete(manifest_path):
    manifest = json.load(manifest_path)
    task_id = manifest.get("task_id")
    
    # Sync completion back to TaskList
    subprocess.run([
        "python3", "scripts/queue_sync.py",
        "--sync-complete",
        "--task-id", task_id,
        "--manifest-path", manifest_path
    ])
    
    # Mark in queue (optional, manifest already has status)
    subprocess.run([
        "python3", "scripts/queue_ops.py",
        "complete", task_id
    ])
```

---

### 3. Periodic Maintenance (Every 5 min or at checkpoint)

**Trigger:** Faerie checkpoint or scheduled maintenance

**Action:**
```
queue_sync.py --prune
  → Removes completed tasks from queue
  → Unblocks tasks whose dependencies are satisfied
  → Logs: "removed N, unblocked M"
```

---

## What the Human Sees (Only TaskList)

```
Turn 0:
  TaskCreate task #27 "Implement queue claiming"
  → Shows in TaskList: status=pending

Faerie activates:
  [Internal: syncs task #27 to sprint-queue.json]
  [Internal: spawns agents who claim from queue]

Agent completes:
  [Internal: updates TaskList via sync hook]
  → TaskList shows: status=completed, manifest_link

Result:
  Human sees clean TaskList progression
  Zero awareness of sprint-queue.json or claiming
  Everything "just works"
```

---

## What Agents See (Only Queue)

```
Agent startup:
  1. Read sprint-queue.json
  2. Claim first unblocked task
  3. Execute
  4. Write manifest with task_id
  5. Return

Queue updated by agent:
  status="completed"
  (Human never hears about this layer)

Next agent claims:
  Scans queue, finds next unblocked task
  Repeats
```

---

## The Three Scripts Work Together

| Script | Purpose | Integration Point |
|--------|---------|-------------------|
| `queue_sync.py` | Keep TaskList ↔ queue in sync | Faerie startup + PostToolUse hook |
| `queue_ops.py` | Atomic queue operations | Agent claiming + PostToolUse hook |
| `faerie_spawn.py` + `build_spawn_bundle.py` | Programmatic agent spawning | Faerie wave planning |

---

## Implementation Checklist

- [ ] **Update `manifest_task_autocompletion.py` hook:**
  - Add `queue_sync.py --sync-complete` call before `queue_ops.py complete`
  - Test: agent completes → TaskList auto-updated

- [ ] **Update `faerie_training_orchestrator.py` startup:**
  - Add `queue_sync.py --sync-pending` call at the top
  - Test: new TaskList tasks → queue auto-populated

- [ ] **Add scheduled maintenance:**
  - Cron or faerie checkpoint: call `queue_sync.py --prune` every 5 min
  - Test: completed tasks removed, blocked tasks unblocked

- [ ] **Verify human UX:**
  - Human only uses TaskCreate/TaskList
  - No mention of sprint-queue.json in documentation
  - All queue operations invisible

---

## Benefits

✅ **Seamless UX:** Human uses familiar TaskList interface  
✅ **Autonomous agents:** Agents autonomously claim from queue (no polling)  
✅ **Automatic sync:** All state stays consistent  
✅ **Transparent:** Human sees progress, agents see dispatch  
✅ **Scalable:** Adding agents doesn't change the workflow  

---

## FAQ

**Q: What if a human deletes a task from TaskList?**
A: Task remains in sprint-queue.json until completed. Next sync will see it gone from TaskList and mark it as "superseded" or "cancelled" in queue. Agent can continue or abandon gracefully.

**Q: What if an agent crashes mid-claim?**
A: Claim TTL expires (300s). Next prune_queue run releases the claim. Task re-queues for next agent.

**Q: What if TaskList and queue get out of sync?**
A: Call `queue_sync.py --status` to diagnose. Manual fix via `--sync-pending` or `--sync-complete`.

**Q: Do agents need to know about TaskList?**
A: No. Agents only read/write to sprint-queue.json. TaskList is hidden.

---

**Status:** Scripts ready. Integration hooks pending (manifest_task_autocompletion.py, faerie_training_orchestrator.py).
