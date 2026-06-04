# Queue-Claiming Agent Architecture — Collective Wave Wisdom

## Vision

Replace faerie's central wave orchestration with **emergent piston effects through collective agent decision-making**. Agents autonomously claim tasks from queue at execution boundaries, applying context/scope heuristics locally. Batching, work distribution, and wave rhythm emerge naturally from agent behavior instead of central dispatch.

---

## Agent Lifecycle (New Model)

### Phase 1: Spawn & Claim
```
Agent spawns with instruction:
  "Claim available unblocked task from queue, execute, repeat until return condition"

Agent startup:
  1. Read queue (sprint-queue.json)
  2. Find first task where:
     - status == "queued" (unclaimed)
     - blockedBy == [] (no dependencies)
  3. Atomically claim task: rename .queued → .claimed-by-{AGENT_ID}
  4. Load task details
```

### Phase 2: Execute
```
Agent executes task per task.description
  (Identical to current model)
```

### Phase 3: Write Results
```
Agent writes manifest to canonical path:
  - task_id field present
  - status == "final"
  
PostToolUse hook fires:
  - manifest_task_autocompletion.py
  - Calls queue_ops.py complete {task_id}
  - Task marked COMPLETED
  - Downstream tasks unblock
```

### Phase 4: Boundary Decision (NEW)
```
At task completion, agent evaluates:

NEXT_TASK = first unblocked task in queue

Step 1: SELF-ASSESSMENT
  Two questions:
  
  Q1: "Do I have HIGH CONTEXT on this task?"
      (Already read relevant files, understand problem space, know the attack surface)
  
  Q2: "Do I have LOW EXPERTISE for this task?"
      (Requires specialist knowledge — security, crypto, forensics, etc. — I'm not trained for)
  
  Decision logic:
  
  IF Q1=true AND Q2=true AND specialist_exists:
    → This is PERFECT for queueing
    → Queue task back with context notes:
      {
        "task_id": "task-123",
        "queued_by": "{CURRENT_AGENT}",
        "reason": "High context, low expertise — specialist should inherit groundwork",
        "files_already_read": ["forensic-coc.py", "coc_validator.py"],
        "problem_analysis": "HMAC-SHA256 chain validation needed. Files are 400 LOC each.",
        "context_notes": "I understand the problem but lack cryptographic expertise. Specialist can start immediately.",
        "prev_attempts": ["Tried as code review → realized it's a security domain"],
        "specialist_hint": "security-auditor",
        "status": "queued"
      }
    → RETURN (let specialist inherit context)
  
  ELIF Q1=false AND Q2=true:
    → Stay and learn
    → Adjacent domain, you'll build context as you work
    → No penalty for exploring
    → CONTINUE (stretch into this domain)
  
  ELIF Q1=true AND Q2=false:
    → This is YOUR DOMAIN and you have context
    → CONTINUE (you're the best fit)
  
  ELIF NOT enough_capacity_for_this_task:
    → Return anyway (let fresh agent start)
    → Don't queue unless Q1=true (no waste of context)

Step 2: CONTEXT EVALUATION (if in domain)
  CONTEXT_USED = tokens_written + tokens_read
  CONTEXT_BUDGET = 200K (for Sonnet, 50K for Haiku)
  CONTEXT_REMAINING = CONTEXT_BUDGET - CONTEXT_USED

  IF CONTEXT_REMAINING < 30K:
    → RETURN (fresh agent needed)
  
  ELIF NEXT_TASK.complexity == "heavy" AND CONTEXT_USED > 60K:
    → RETURN (deep work deserves fresh context)

Step 3: CONTINUATION DECISION (if domain + context OK)
  queue_depth = count(unclaimed + unblocked tasks)
  parallel_agents_idle = count(agents waiting in queue)
  
  IF queue_depth > 10 AND parallel_agents_idle < 3:
    → CLAIM(NEXT_TASK) and CONTINUE (batch for efficiency)
  
  ELIF queue_depth < 3:
    → RETURN (let fresh agent start)
  
  ELIF CONTEXT_REMAINING > 80K:
    → CLAIM(NEXT_TASK) and CONTINUE (room for more)
  
  ELSE:
    → RETURN (safe boundary)

IF CONTINUE:
  - Update manifest: prev_task_id, next_task claim
  - Claim next unblocked task
  - Jump to Phase 2 (Execute)

IF RETURN:
  - Finalize manifest
  - Return to main context
```

**Key insight:** Agents leave work for team members they know are better suited. The queue becomes a conversation: "Tried X, blocked by Y. evidence-curator, this is yours." No ego-driven task completion. Specialization drives the work flow.

---

## Emergent Wave Patterns

Instead of faerie declaring "W1: launch 5 agents", waves emerge from collective behavior:

### W1 Behavior (Fast Triage)
- Short tasks (blocker fixes, quick audits)
- Agents claim, execute, return quickly
- Many agents in flight simultaneously
- High throughput, low context per agent
- **Emerges because:** agents see "task is fast + context is fresh → claim and return"

### W2 Behavior (Feature/Research)
- Medium tasks (refactoring, analysis, cross-file changes)
- Agents claim, may continue if context allows
- Some batching (agent claims 2–3 medium tasks before returning)
- Balanced throughput + depth
- **Emerges because:** agents see "task is medium + context room → claim and continue"

### W3 Behavior (Synthesis/Deep Work)
- Complex tasks (architecture decisions, investigation synthesis)
- Single agent claims one task, goes deep
- Fresh context per deep task (agent returns after 1 task)
- **Emerges because:** agents see "task is complex + context is high → return after one"

No central planner. Waves emerge from local agent decisions.

---

## Monkeybranching — Momentum Chains (Phase 1.5)

Instead of returning after each task, agents can chain-claim the next unblocked task when
momentum is high (task completed fast, context remains healthy).

### Decision Logic (at task boundary, before Phase 4)

```
IF task_completed_successfully AND context_remaining > 30K:
  next_tasks = lookahead(current_task_id, depth=5)
  IF next_tasks and next_tasks[0].blockedBy == []:
    result = monkeybranch_claim(current_task_id, agent_id, context_remaining)
    IF result["chained"] is True:
      Update manifest: next="chained to {result['to_task']}"
      Log COC event: "monkeybranch_chain: {current} -> {result['to_task']}"
      Jump back to Phase 2 (Execute) -- do NOT return to faerie
ELSE:
  -> Fall through to existing Phase 4 boundary decision
```

### Effect

Single agent completes N fast tasks back-to-back without faerie re-planning between them.
Latency between tasks drops from "faerie re-plan + spawn overhead (~15-25K tokens)" to
"immediate next claim (~50ms)".

### Implementation

Two new functions in `7x_queue_ops.py`:

**`lookahead(current_task_id, depth=5) -> List[dict]`**
- Reads queue (no lock -- read-only, best-effort)
- Finds position of `current_task_id` in full task list
- Scans next `depth` positions; returns only tasks where `blockedBy == []` and
  `status == "queued"` and `claim_state == "unclaimed"`
- Order preserved (queue position, not priority sort)

**`monkeybranch_claim(current_task_id, agent_id, context_tokens_remaining, depth=5) -> dict`**
- Checks `context_tokens_remaining > MONKEYBRANCH_CONTEXT_THRESHOLD` (30K)
- Calls `lookahead()` for candidates
- Atomically claims first candidate via `claim_atomic()`
- Logs COC entry: `event="monkeybranch_chain"`, `from_task`, `to_task`
- Returns `{chained, from_task, to_task, reason, claim_result}`

CLI:
```bash
# Peek ahead only (no claiming):
python 7x_queue_ops.py lookahead TASK_ID [--depth 5]

# Attempt a chain-claim:
python 7x_queue_ops.py monkeybranch-claim TASK_ID --agent AGENT_ID \
  --context-remaining 80000 [--depth 5]
```

### Limitations

- Must respect context budget (30K token threshold is non-negotiable)
- Only chains **unblocked** tasks (`blockedBy == []`)
- Each monkeybranch logs to COC (full audit trail)
- Sentinel file created for each claimed task (same expiration TTL as Phase 1)
- No nested monkeybranching -- agent chains sequentially, not in parallel

### Example Momentum Chain

```
Agent claims task-01 (faerie spawn)
  -> executes task-01 (fast, context=150K remaining)
  -> monkeybranch: chains to task-02 (context=120K)
  -> executes task-02
  -> monkeybranch: chains to task-03 (context=90K)
  -> executes task-03
  -> monkeybranch: chains to task-04 (context=60K)
  -> executes task-04
  -> monkeybranch: context check fails (< 30K) -> returns normally
COC log: 4 chain entries (01->02, 02->03, 03->04, 04->(stopped))
faerie re-plans only ONCE for 4 completed tasks
```

---

## Queue Claiming Mechanism (Atomic)

**Requirement:** Multiple agents claim simultaneously without race conditions.

**Implementation: Rename-Based Claiming**

```
Sprint queue state:
  sprint-queue.json contains:
    [{
      "id": "task-001",
      "status": "queued",
      "claim_state": "unclaimed"  ← agents modify this atomically
    }, ...]

Agent claims via atomic file operation:
  1. Read sprint-queue.json
  2. Find first task with claim_state == "unclaimed"
  3. Write claim transaction:
     {
       "task_id": "task-001",
       "claimed_by": "{AGENT_ID}",
       "claimed_at": "ISO8601",
       "claim_ttl": 300  ← 5 min; if agent crashes, claim expires
     }
     to: ~/.claude/hooks/state/claim-{task-id}-{AGENT_ID}.json
  4. Rename (atomic):
     claim-{task-id}-{AGENT_ID}.json → claimed-{task-id}
     (If file already exists, claim failed; pick next task)
  5. Update sprint-queue.json: claim_state = "claimed"

Result: First-one-wins, no polling, race-free.
```

**Claim expiration:** If agent crashes mid-task, claim file TTL expires after 5 min. Cleanup task (via faerie health monitor or async script) recycles the claim and re-queues the task.

---

## Queue Conversation Protocol (Agent-to-Agent Notes)

When an agent recognizes work outside their domain, they queue it back with context notes for teammates.

**Queue note format:**
```json
{
  "task_id": "task-123",
  "queued_by": "code-reviewer-a1b2c3d",
  "queued_at": "ISO8601",
  "reason": "Outside my specialization | Blocked by expertise | Context overflow | Tried and failed",
  "specialist_hint": "evidence-curator | security-auditor | research-analyst",
  "what_was_tried": [
    "Approached as code review → realized cryptographic validation needed",
    "Checked HashLib docs → out of my depth"
  ],
  "blocked_by": [
    "HMAC-SHA256 chain validation (cryptography)",
    "Private key handling (security)"
  ],
  "high_value_lead": "Chain-of-custody algorithm is elegant; just needs specialist review",
  "context_notes": "Files already read: forensic-coc.py, coc_validator.py. Glossary of COC terms at: ~/.claude/memory/coc-glossary.md",
  "status": "queued",
  "for_agent": "security-auditor"
}
```

**Why this works:**
- Next agent (e.g., security-auditor) claims the task and ALREADY HAS context
- Knows what was tried, where it failed, what still needs work
- Doesn't re-explore dead ends
- Feels like a handoff from a team member, not a cold assignment

**Agent responsibility:**
- Never add vague notes ("hard, give up")
- Always include: what was tried, where it failed, what the next agent needs
- Suggest specialist by name if you know who's best
- Leave high-value insights even if you can't complete the task

---

## Context Budget Heuristics

Agents make local decisions using:

- **CONTEXT_USED**: tokens written during task (from manifest)
- **CONTEXT_BUDGET**: model-specific (Haiku 50K, Sonnet 200K, Opus 700K)
- **TASK_COMPLEXITY**: inferred from task.description length, keywords ("architecture", "synthesis", etc.)
- **QUEUE_DEPTH**: number of unblocked tasks waiting
- **PARALLEL_IDLE**: agents idle in queue waiting for claims

**Decision matrix:**

| Context Used | Queue Depth | Task Complexity | Decision |
|---|---|---|---|
| > 150K | any | any | RETURN |
| 60–150K | < 5 | light | CONTINUE |
| 60–150K | < 5 | heavy | RETURN |
| 60–150K | ≥ 5 | light | CONTINUE |
| 30–60K | any | any | CONTINUE if unblocked task exists, RETURN otherwise |
| < 30K | any | any | CONTINUE if unblocked task exists |

---

## Faerie's Role (Reduced)

Faerie no longer orchestrates waves. Instead:

1. **Health monitoring** — agent queue depth, claim expiration, blocked tasks
2. **Tiebreaker** — if queue deadlocked (all tasks blocked on single blocker), faerie can escalate human attention
3. **Cold start** — at session start, spawn 2–3 agents with "claim available task" instruction; agents self-organize from there
4. **Learning injection** — still maintains training-queue.json, prioritizes on_the_job_eligible agents in queue order

---

## Implementation Plan

### Phase 1: Queue Claiming Mechanism
1. Implement atomic claim via rename (claim-{task}-{agent}.json)
2. Add claim expiration + cleanup logic
3. Modify queue_ops.py: add claim/release endpoints
4. Update sprint-queue.json schema: add claim_state, claim_ttl fields

### Phase 2: Agent Boundary Decision Logic
1. Create boundary-decision-heuristics.py
   - Inputs: manifest (context_used), next_task (complexity), queue state
   - Outputs: CONTINUE or RETURN
2. Inject heuristics into agent spawn prompt
3. Agent calls heuristic at task boundary before claiming next

### Phase 3: Faerie Reduction
1. Remove wave-planning logic from 7x_surfacing_scheduler.py
2. Faerie spawn: just launch 2–3 agents with "claim available task"
3. Add health monitor: detect deadlocks, claim expirations, queue saturation

### Phase 4: Testing & Tuning
1. Run test with 5 agents, 20 tasks (mix of fast/medium/heavy)
2. Observe emergent wave behavior
3. Tune heuristics (context thresholds, queue depth triggers)
4. Validate zero race conditions on claiming

---

## Benefits

✓ **Eliminates central bottleneck** — faerie doesn't plan, agents decide
✓ **Natural batching** — emerges from context budget awareness
✓ **Adaptive concurrency** — agents naturally serialize deep work, parallelize fast work
✓ **Resilient** — agent crash doesn't break system (claim expires, task re-queued)
✓ **Stigmergic** — queue is the only shared state; agents coordinate via filesystem
✓ **Scalable** — add more agents without changing orchestration logic

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Agents deadlock on resource contention | Claim TTL + health monitor escalates to human |
| Context explosion (agents batch too aggressively) | Strict context budget heuristics + early return |
| Idle agents (all tasks blocked on one blocker) | Faerie health monitor detects, flags blocker task as urgent |
| Claim race conditions | Atomic rename-based claiming, no polling |

---

## Timeline

- **Week 1:** Implement queue claiming + atom claim mechanism
- **Week 2:** Agent boundary heuristics + spawn prompt injection
- **Week 3:** Faerie reduction + health monitoring
- **Week 4:** Testing, tuning, validation

**Rollout:** Parallel old (faerie-orchestrated) + new (queue-claiming) for 1 sprint; then cutover.

---

## Status

- [x] Architecture designed
- [ ] Queue claiming mechanism implemented
- [ ] Boundary decision heuristics created
- [ ] Agent spawn prompt updated
- [ ] Faerie reduced to health monitoring
- [ ] End-to-end testing completed
- [ ] Tuning & production readiness

**Owner:** Team (multi-phase rollout)
