# Piston DAG — Zero-Burden Task Orchestration

**Goal:** Task dependencies resolved entirely by queue metadata + agent manifests. Main session does only: claim → spawn → wait → mark complete. No orchestration logic, no DAG analysis, no chunking.

---

## Pattern: Push-Based Self-Orchestration

Instead of main analyzing dependencies, **agents read their own deps from queue metadata**.

### 1. Queue Metadata (Sprint-Queue-JSON)

Each task declares its own critical dependencies:

```json
{
  "task": {
    "id": "task-20260407-publish-commit",
    "goal_one_line": "Final commit + push H1+H3 narratives",
    "depends_on": ["task-20260407-publish-citations"],
    "blocks": [],
    "blocks_critical_path": true,
    "wave_target": "W3",
    "priority": "HIGH"
  }
}
```

**Fields:**
- `depends_on`: list of task IDs that MUST complete before this task can start
- `blocks`: list of task IDs waiting on this one (informational; used by next claim sweep)
- `blocks_critical_path`: if true, this task is a blocker for the publication/release path
- `wave_target`: W1/W2/W3/background (optional; affects scheduling but not deps)

### 2. Claim Returns Dependency Metadata

When main calls `claim_batch(4)`, it gets:

```json
{
  "status": "claimed",
  "count": 4,
  "tasks": [
    {
      "id": "task-1",
      "goal_one_line": "...",
      "depends_on": [],
      "manifest_path": "~/.claude/hooks/state/wave2-agent-task-1-result.json",
      "ready": true
    },
    {
      "id": "task-2",
      "depends_on": ["task-1"],
      "manifest_path": "~/.claude/hooks/state/wave2-agent-task-2-result.json",
      "ready": false,
      "waiting_on": ["task-1"]
    }
  ]
}
```

**The claim logic itself is f(0) to main**: it's just filtering queue.json for `depends_on.length == 0 || all_deps_completed`.

### 3. Agent Reads Deps From Manifest Path

Spawn prompt includes:

```
TASK DEPENDENCIES:
This task depends on: {depends_on list}
This task blocks: {blocks list}

MANIFEST PATH (for your output + dependency signaling):
~/.claude/hooks/state/wave2-{agent_type}-{task_id}-result.json

When you write your manifest, INCLUDE:
{
  "completed_task": "task-20260407-publish-citations",
  "now_unblocks": ["task-20260407-publish-commit"],
  "dashboard_line": "..."
}
```

### 4. Main Session Loop (Literally This Simple)

```python
while True:
    claimed = claim_batch(4)  # f(0): just reads queue.json, filters on depends_on
    if claimed['status'] == 'empty':
        break
    
    # Sort by depends_on.length (zero deps first) — agents will wait if needed
    claimed['tasks'].sort(key=lambda t: len(t.get('depends_on', [])))
    
    # Spawn all 4 in parallel — agents self-orchestrate
    for task in claimed['tasks']:
        spawn_agent(task)
    
    # Wait for all manifests to appear
    for task in claimed['tasks']:
        wait_for_manifest(task['manifest_path'])
    
    # Mark complete
    for task in claimed['tasks']:
        mark_complete(task['id'])
```

**That's it. Zero analysis. Zero chunking logic. Zero dependency graph.**

---

## Agent Self-Orchestration (Inside Agent)

When an agent starts, it:

1. **Read depends_on list from spawn prompt**
2. **If depends are pending**: poll manifest paths (`~/.claude/hooks/state/wave2-{dep_type}-{dep_id}-result.json`) until they exist
3. **Read dep manifests**: extract data you need from prior agents
4. **Do your work**
5. **Write manifest with `now_unblocks` field**: signals which tasks you just unblocked

```python
# Agent startup code (same in all spawns)
def wait_for_dependencies(depends_on_list):
    """Poll dependency manifests until ready."""
    for dep_id in depends_on_list:
        manifest_path = find_manifest_for_task(dep_id)  # uses pattern matching
        deadline = time.time() + 600  # 10 min timeout
        while time.time() < deadline:
            if Path(manifest_path).exists():
                return json.loads(Path(manifest_path).read_text())
            time.sleep(2)
        raise TimeoutError(f"Dep {dep_id} never completed: {manifest_path}")

# At agent start:
deps = json.loads(os.environ.get('TASK_DEPENDS_ON', '[]'))
if deps:
    dep_data = wait_for_dependencies(deps)
    # Use dep_data to contextualize your work
```

---

## Scaling: Why f(0)?

**Main session overhead per agent:**
- Claim: O(n) where n = queue size (can be parallelized; not main's problem)
- Spawn: O(1) — just call Agent tool
- Wait: O(1) — file polling, not coordination
- Mark complete: O(1) — update queue.json

**Adding agent 100?** Same O(1) per agent. No new logic, no new coordination.

**Dependency resolution:** Happens in
1. **Queue metadata** (static, pre-written, O(1) to read)
2. **Agent manifest polling** (async, each agent self-waits)
3. **Next claim sweep** (filters `depends_on.length == 0`, O(n) but batched)

**Zero discovery, zero graph traversal, zero consensus protocol.**

---

## Implementation Checklist

- [ ] **claim_task.py**: Add `depends_on`, `blocks`, `ready`, `waiting_on` fields to claimed task JSON
- [ ] **claim_task.py**: Filter for `ready: true` (all deps completed) when collecting claim batch
- [ ] **Spawn prompt**: Include TASK DEPENDENCIES section with depends_on list + manifest_path
- [ ] **Agent code**: Add wait_for_dependencies() + manifest polling at startup
- [ ] **Manifest format**: Agents write `now_unblocks: [...]` field when done
- [ ] **Main loop**: Replace "chunking logic" with simple batch-claim → spawn → wait → complete loop

---

## Example: Concrete DAG

```
B2 forensic flush (no deps)  →  ready: true
    ↓
H1 narrative (depends: B2)  →  ready: false (waits for B2 manifest)
    ↓
Citations (depends: H1)  →  ready: false
    ↓
Publish commit (depends: Citations)  →  ready: false
```

**First batch claim:**
```json
[
  {"id": "b2-flush", "depends_on": [], "ready": true},
  {"id": "h1-narrative", "depends_on": ["b2-flush"], "ready": false},
  {"id": "citations", "depends_on": ["h1-narrative"], "ready": false},
  {"id": "pub-commit", "depends_on": ["citations"], "ready": false}
]
```

**Main spawns all 4:**
- B2 runs immediately
- H1 polls B2 manifest, waits 30s, then starts when B2 writes manifest
- Citations waits for H1 manifest
- Pub-commit waits for Citations manifest

**Main does nothing while agents wait.** No polling, no orchestration, no analysis.

---

## Key Properties

| Property | How | Cost |
|----------|-----|------|
| **Scalability** | f(0) overhead per agent | No orchestration, agents self-coordinate |
| **Flexibility** | Task metadata is extensible | Add fields to task JSON, agents read them |
| **Atomicity** | Manifest is single source of truth | No consensus, no coordination protocol |
| **Observability** | Manifests in shared path | All agent outputs immediately visible |
| **Resilience** | Deps polled by agents, not main | Agent timeout ≠ main blocked |
| **Simplicity** | Main loop is 10 lines | All complexity pushed to queue metadata |

---

## Next Steps

1. Extend `claim_task.py` to track `depends_on` + `ready` fields
2. Implement `find_manifest_for_task()` — maps task_id to manifest path pattern
3. Add agent startup code to every spawn prompt
4. Replace chunking logic in main with simple batch loop
5. Test: spawn 4-agent chain, verify self-orchestration works
