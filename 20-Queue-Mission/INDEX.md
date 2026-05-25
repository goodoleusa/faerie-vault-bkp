---
doc_hash: sha256:pending
created: 2026-04-25
type: playground-index
folder: 20-Queue-Mission
breadcrumb: "vault / 20-Queue-Mission / INDEX"
---

# 20-Queue-Mission — How Tasks Become Missions

The sprint queue (`sprint-queue.json`) is faerie2's nervous system. Tasks enter as seeds, survive claiming wars, mutate through state transitions, and exit as completed manifests. No message broker. No database. A JSON file with atomic file-lock claiming.

---

## Task Lifecycle

```
PENDING → in_progress → completed
               │
               └→ released (if session dies before completing)
```

A task object in the queue looks like:

```json
{
  "id": "task-20260425-152144-a4e5",
  "title": "Merge vault folders into playground",
  "status": "pending",
  "claim_state": "pending",
  "priority": "HIGH",
  "created_at": "2026-04-25T15:21:44Z",
  "blockedBy": [],
  "tags": ["synthesis-heavy"],
  "agent_type_hint": "documentation-engineer",
  "estimated_effort": "L",
  "criteria_emergent_v2": {
    "seeded": ["5 explainer folders with INDEX.md", "deprecated folders archived"],
    "augmented": [],
    "confidence": 0.85,
    "permission_to_leap": "v2.1 permission granted"
  }
}
```

---

## Claim Atomicity

Two sessions cannot claim the same task. The mechanism:

```python
# O_CREAT | O_EXCL = atomic "create if not exists" — OS-level atomicity
fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
```

1. Session A: `claim-atomic task-20260425-152144-a4e5` → creates `claimed-task-20260425-152144-a4e5` sentinel file
2. Session B: same call → `FileExistsError` → claim fails → B picks next unclaimed task
3. TTL: 300 seconds. If session A dies without completing, stale sentinel auto-expires.

This works on a single machine with multiple concurrent sessions. No coordinator. No message queue. The filesystem IS the lock.

---

## Claim Modes

```bash
# Depth mode (default): focus on one project, claim up to --max tasks
python 7x_queue_ops.py claim --session $SID --project faerie2 --mode depth --max 3

# Breadth mode: clear the highest-priority tasks regardless of project
python 7x_queue_ops.py claim --session $SID --mode breadth
```

Two concurrent sessions draining the same queue:
```
Session A: claims 3 faerie2 tasks  (depth mode)
Session B: claims 3 cybertemplate tasks (depth mode)
→ zero overlap, zero collision
```

---

## Monkeybranch Claim — Momentum Chains

When a session completes a task, it can look ahead at what that task unblocks and claim the next link in the chain — before releasing the lock, while it still has momentum context.

```
Task A completes
  → lookahead finds Task B (blockedBy: [A]) is now unblocked
  → monkeybranch_claim grabs B atomically
  → session transitions directly A→B without returning to main
```

This is chain-claiming. It reduces round-trips to main context: the subagent chains without surfacing. The system calls it monkeybranch because the agent swings from branch to branch without touching the ground (main context).

---

## Smart Prerequisites (blockedBy)

`blockedBy` is a list of task IDs that must reach `completed` before this task becomes claimable. The queue ops script skips blocked tasks during `claim`:

```json
{
  "id": "task-20260425-vault-phase2",
  "blockedBy": ["task-20260425-vault-phase1"],
  "status": "pending"
}
```

Phase 1 completes → phase 2 automatically becomes claimable on the next `claim` call. No human intervention. No message sent. The queue's own state is the trigger.

---

## Premise-Stale Detection

A task seeded when the codebase was in state X may be stale when the codebase has moved to state Y. The queue schema includes `source` (what observation triggered the task) and `criteria_emergent_v2.seeded` (what done looks like). An agent that finds the premise already satisfied marks the task `completed` with `completion_reason: "premise-already-satisfied"` — not a skip, not a failure. This is honest bookkeeping.

---

## Priority Sort + Recency Boost

Tasks are not pure FIFO. The sort key combines static priority with recency decay:

```
effective_priority = pri_int - recency_boost

where:
  recency_boost = max(0.0, 0.9 × (1.0 - hours_ago / 48.0))

Examples:
  fresh HIGH  → (0 - 0.90) = -0.90   ← top of queue
  old   HIGH  → (0 - 0.00) =  0.00
  fresh MED   → (1 - 0.90) =  0.10   ← below any HIGH
  old   MED   → (1 - 0.00) =  1.00
```

A fresh MED task never outranks an old HIGH task. The cap of 0.9 enforces this.

---

## Queue Health Compass

```
                    BLOCKED
                  (waiting on deps)
                       │
    LOW priority ──────┼────── HIGH priority
                       │
                  IN_PROGRESS
                  (being worked)
                       │
           COMPLETED ──┴── RELEASED (session died)
```

Healthy queue: HIGH tasks draining, LOW tasks accumulating (normal backpressure). Unhealthy: HIGH tasks stuck in_progress for >TTL (session died without cleanup). Fix: `python 7x_queue_ops.py cleanup-claims`.

---

## The `claimed_by_agent_reputation_at_claim_time` Proposal

Currently the claim record captures `session_id` and `claimed_at`. A proposed extension would capture the claiming agent's reputation score at claim time:

```json
{
  "claimed_by_session": "1c0c5ef4",
  "claimed_at": "2026-04-25T15:21:44Z",
  "claimed_by_agent_type": "documentation-engineer",
  "claimed_by_agent_reputation_at_claim_time": {
    "baseline": 0.82,
    "last_score": 0.87,
    "tasks_completed": 14
  }
}
```

This enables post-hoc analysis: do higher-reputation agents produce better outcomes on the same task type? It also creates a reputation audit trail — you can see what the system believed about an agent when it trusted them with a task. Not yet implemented; proposal captured here.

---

[[00-Welcome/INDEX]] | [[10-Processes/INDEX]] | [[30-Dashboards/INDEX]] | [[40-Roster-Routing/INDEX]] | [[50-Honesty-System/INDEX]]

*sha256:pending*
