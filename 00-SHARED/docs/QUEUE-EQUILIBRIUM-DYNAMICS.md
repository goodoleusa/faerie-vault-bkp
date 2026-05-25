# Queue Equilibrium Dynamics — Balancing Drain, Spawn, and Context Pressure

## Overview

The faerie queue operates under pressure from three competing forces: **inbound task creation**, **outbound agent spawning**, and **context saturation**. When these forces balance, the system drains efficiently. When they mismatch, bottlenecks emerge. This document explains the dynamics and the control mechanisms that maintain equilibrium.

**Key principle:** Queue equilibrium is not about speed — it's about sustainable work distribution. A queue that drains fast but explodes context is unstable; one that stays shallow but hoards context for agents is starved. The equilibrium point is where **drain rate = spawn rate** and **context allocation per agent = context recovery rate** (via agent returns and manifest compression).

---

## Three Pressure Forces

### Force 1: Inbound — Task Creation Rate

Tasks enter the queue via:
- `/task` commands (explicit queueing)
- Chained tasks from agent manifests (`next_task_queued` field)
- Blocked-task resolution (when a `blockedBy` dependency completes, downstream tasks auto-unblock and become claimable)

**Measurement:** `sprint-queue.json` total task count (`len(tasks)`) and unclaimed count (`sum(status=="queued" AND claim_state=="unclaimed")`).

**Pressure signal:** Queue depth growing; if unclaimed > 50 and drain_rate < 2 tasks/min, the system is intake-heavy.

### Force 2: Outbound — Agent Spawn Rate

Agents claim and consume tasks via:
- Faerie wave dispatch (W1, W2, W3 each spawn agents)
- Monkeybranching — single agent chains multiple unblocked tasks before returning (Phase 1.5 Queue-Claiming feature)
- Manual claims via `7x_queue_ops.py claim` (e.g., development/testing)

**Measurement:** `piston-checkpoint.json` `agents_in_flight` list (count) and `agents_returned` counter (cumulative).

**Pressure signal:** Many agents spawned but few returning (high in-flight count, low return rate) → context bloat or task slowdown.

### Force 3: Context Pressure — Resource Saturation

Main context fills as:
- Agents are spawned (each spawn costs 15-25K tokens for boot)
- Manifests return (50-100 tokens per manifest)
- Wave summaries accumulate (dashboard_lines compress but bulk output stays in forensics)
- Inference layers perform synthesis (cross-agent reasoning)

**Measurement:** Altimeter reading (context_pct from piston-checkpoint.json or lean_query output). Context gates at 70% (W2 deferred until drop), RED alert at 85%.

**Pressure signal:** Context % climbing; if >80%, intake should throttle (spawn fewer agents) until context drops.

---

## Equilibrium Condition

**Stable state:** The queue depth oscillates in a narrow band (e.g., 5–15 tasks queued) as intake matches drain.

### Math Model

```
Let:
  T_create = inbound task creation rate (tasks/minute)
  T_drain  = outbound consumption rate (tasks/minute)
  A_spawn  = agent spawn rate per minute
  A_return = agent return rate per minute
  C_used   = context tokens burned per spawn
  C_avail  = context tokens available per cycle

Equilibrium holds when:
  1. T_drain ≥ T_create  (queue depth is stable or shrinking)
  2. A_return ≥ A_spawn  (in-flight agent count is stable or shrinking)
  3. Context pressure is GREEN (context_pct < 70%) or stable in YELLOW (70–85%)
```

### Failure Modes

**Mode 1: Intake Outpaces Drain (Queue Bloat)**
- T_create > T_drain for sustained period
- Queue depth grows unbounded
- Unclaimed tasks accumulate; agents cannot keep pace
- **Cause:** Faerie spawn rate too low, or agents returning too fast without sufficient work queued
- **Signal:** unclaimed > 50, altimeter YELLOW but queue not shrinking
- **Fix:** Increase spawn rate (more agents, or lower W-gate thresholds) OR queue more work upfront

**Mode 2: Spawn Outpaces Return (Context Bloat)**
- A_spawn > A_return for sustained period
- Agents in-flight count climbs
- Context fills rapidly; wave gates trigger; W2/W3 defer
- **Cause:** Tasks are slow (high latency per agent), or context allocated per agent is excessive
- **Signal:** agents_in_flight > 5, context_pct climbing to YELLOW/RED
- **Fix:** Return agents faster (set lower context budgets, or split large tasks), OR defer next spawn wave until returns catch up

**Mode 3: Premature Gate Closure (W-Gate Stale State)**
- Context gate recorded at 85% (deferring W2)
- Compact fires, context resets to 0%
- Deferral condition is now stale, but no mechanism re-evaluates
- W2 never launches despite ample context
- **Cause:** Gate state not re-checked post-compact; piston-checkpoint fields (`current_wave`, `deferred_reason`) inconsistent with reality
- **Signal:** context_pct is now 20%, but `deferred_reason` still says "W2 deferred at 85%"; wave stuck
- **Fix:** Re-evaluate gate conditions after compact; store gate state as a declarative condition, not a frozen snapshot

---

## Pre-Computation at Write-Time (mth00083)

The key to sustainable equilibrium is **shifting aggregation work from read-time to write-time**.

### The Problem

When faerie needs to route next wave, it runs:
```python
queue = json.load(sprint-queue.json)  # parse 500-2000 tasks
unclaimed = [t for t in queue if t["claim_state"] == "unclaimed"]  # O(N) filter
next_claimable = [t for t in unclaimed if t.get("blockedBy") == []]  # O(N) filter
drain_rate = count_completed_last_5_min(queue)  # O(N) scan
```

This is O(N) per decision, with N = queue length. At 100 tasks, this is milliseconds; at 500 tasks, it's multiple seconds of JSON parsing + filtering. Main context is burned on aggregation, not routing.

### The Solution

Maintain a tiny **queue summary file** (≤200 bytes) that faerie consults instead:

**File:** `~/.claude/hooks/state/queue-summary.json` (updated atomically on every queue mutation)

**Contents:**
```json
{
  "ts": "2026-04-25T12:34:56Z",
  "total_tasks": 47,
  "unclaimed_count": 23,
  "unblocked_claimable": 19,
  "in_progress_count": 2,
  "completed_last_5_min": 4,
  "drain_rate_per_min": 0.8,
  "next_unblocked_task_id": "task-20260425-001",
  "queue_bottleneck": "none",
  "altimeter_context_pct": 42.5,
  "wave_state": "W2_in_flight",
  "agents_in_flight": 3
}
```

**Maintenance:** Every write to `sprint-queue.json` (task creation, claim, release, completion) triggers an atomic update of this summary. Scripts that write queue do the aggregation once at write-time; readers consume the summary at O(1).

**Faerie's decision loop becomes:**
```python
summary = json.load(queue-summary.json)  # O(1), ≤1ms
if summary["unblocked_claimable"] > 10 and summary["agents_in_flight"] < 3:
  spawn_next_wave()
```

No JSON parsing, no filtering, no O(N) scans.

---

## Atomic Queue Mutations (7x_queue_ops.py)

The queue state machine is driven by three atomic operations. Each updates both the raw `sprint-queue.json` AND the `queue-summary.json` summary:

### Operation 1: Create Task

```
Input: task_id, goal, priority, category, blockedBy []
Output: task appended to sprint-queue.json, status="queued", claim_state="unclaimed"
Side effect: queue-summary.json updated (total_tasks++, unclaimed_count++)
COC entry: "task_created: {task_id} | priority={priority}"
```

### Operation 2: Claim Task (Atomic Rename)

```
Input: agent_id, task_id (first unblocked task in queue)
Output: 
  - New sentinel file: ~/.claude/hooks/state/claimed-{task_id}
  - queue entry: claim_state="claimed", claimed_by=agent_id, claimed_at=now
  - Piston-checkpoint.json: agents_in_flight += agent_id
Side effect: queue-summary.json updated (unblocked_claimable--, in_progress_count++)
COC entry: "task_claimed: {task_id} | by={agent_id}"
Precondition: blockedBy == [] (no dependencies pending)
```

**Failure mode:** If sentinel file already exists, claim failed (another agent claimed first). Pick next unblocked task.

### Operation 3: Complete Task (Release + Unblock)

```
Input: task_id (agent calls this after writing manifest with status="final")
Output:
  - Queue entry: status="completed", claim_state="released"
  - Sentinel file deleted
  - Any tasks with task_id in blockedBy list: blockedBy list updated
  - Piston-checkpoint.json: agents_in_flight -= agent_id, agents_returned++
Side effect: queue-summary.json updated (completed_last_5_min++, drain_rate recalc)
COC entry: "task_completed: {task_id} | agent_returned | unblocked={downstream_ids}"
```

---

## Monkeybranching — Momentum Chains

When an agent completes a task with ample context remaining (>30K tokens), it can **chain-claim** the next unblocked task without returning to faerie. This reduces spawn overhead and increases throughput during high-velocity periods.

### Decision at Task Boundary

```
Agent completes task_N:
  1. Check context_remaining > 30K? 
     → No: return normally (faerie will spawn next agent)
     → Yes: continue
  2. Lookahead(depth=5) at next unblocked tasks
     → None found: return normally
     → Found: proceed to chain
  3. Atomically claim next task via claim_atomic()
  4. If claim succeeds: jump back to task execution (no faerie re-plan)
     If claim fails (another agent claimed it): return normally
```

### Effect on Equilibrium

Monkeybranching creates **temporary decoupling** between task consumption and agent spawning:
- One agent claims N tasks in sequence
- Faerie sees only 1 agent in-flight (the initial spawn)
- But queue depth drops by N tasks
- Context per agent is distributed across N tasks (50-75K per task × N)

**Stability implication:** Equilibrium equations still hold (T_drain increases because one agent chains), but the signal (agents_in_flight count) lags behind actual consumption (queue_depth drops faster). Faerie must use queue_depth and drain_rate as the primary signals, not agent count.

---

## Wave Gates — Context-Responsive Throttling

When context pressure climbs, faerie defers later waves to prevent overflow.

### Gate Mechanism

```
piston-checkpoint.json:
  wave_state: "W1_in_flight" | "W1_complete" | "W2_deferred" | "W2_in_flight" | ...
  context_gate_at_wave: { "W1": 0, "W2": 70, "W3": 50 }  (% threshold to defer next wave)
  deferred_reason: string (if wave deferred)
```

### Problem: Gate Staleness

Early design (2026-04-24 diagnosis): Gate state is a snapshot.
- W1 completes, context at 85% → "W2 deferred at 85%"
- Compact fires (context reset to 0%)
- Faerie re-evaluates but `deferred_reason` still says "deferred at 85%"
- Decision logic: "reason says 85%, current is 0%, therefore defer" (OR "reason says 85%, that's > 85% now false, undefer") — CONTRADICTION

### Solution: Declarative Gates

Store gate conditions as **predicates**, not snapshots:

```json
{
  "wave_state": "W2_deferred",
  "deferral_condition": {
    "wave": "W2",
    "reason_type": "context_pressure",
    "threshold_pct": 70,
    "deferred_at": "2026-04-24T13:45:00Z"
  },
  "re_evaluate_trigger": "post_compact | every_5_min | on_agent_return"
}
```

Faerie checks the **condition**, not the snapshot:
```python
if wave_state == "W2_deferred":
  current_context = get_altimeter()["context_pct"]
  threshold = deferral_condition["threshold_pct"]
  if current_context < threshold:
    wave_state = "W2_pending"  # ready to launch when queue fills
  else:
    # keep deferred
```

---

## Zombie Claim Recovery

**Problem:** Agent crashes mid-task. Sentinel file `claimed-{task_id}` persists with TTL=300s. If the claim expires and no cleanup runs, the sentinel lingers and the queue record is stuck at `claim_state="claimed"`.

**Signal:** Dashboard shows 1 in-progress task, but drain_rate=0; the agent is not running.

**Recovery:** Cleanup task runs periodically (via SubagentStop hook or cron) and calls `cleanup_expired_claims()`:

```python
def cleanup_expired_claims():
  for sentinel in glob("claimed-*"):
    age = now - sentinel.mtime()
    if age > 300s:
      task_id = sentinel.stem  # "claimed-task-001" → "task-001"
      release_atomic(task_id)  # resets queue entry to queued
      delete(sentinel)
      log_coc("zombie_claim_recovered: {task_id} | age={age}s")
```

**Enforcement:** Add this to SubagentStop hooks (runs on every agent return). Cost: O(N) sentinel scan, but N is small (<10 live claims typically).

---

## Equilibrium Checklist

To maintain a healthy queue:

1. **Pre-computation:** Queue summary file updated atomically with every mutation ✓
2. **Atomic claims:** Rename-based claiming, sentinel TTL, cleanup on expiration ✓
3. **Gate predicates:** Wave deferral conditions re-evaluated post-compact, not frozen ✓
4. **Monkeybranching:** Agents can chain-claim when context allows (Phase 1.5) ✓
5. **Drain rate monitoring:** Track completed_last_5_min and flag if <1 task/min with unclaimed>10 ✓
6. **Context pressure routing:** Altimeter feedback to wave-gate thresholds; W2 gate = 70%, W3 gate = 50% ✓
7. **Visibility:** Faerie reads queue-summary.json only, not raw sprint-queue.json (O(1) reads) ✓
8. **COC integrity:** Every queue mutation logged to forensic COC; no silent state changes ✓

---

## Operational Tuning

### Symptoms → Tuning Table

| Symptom | Root Cause | Tuning |
|---------|-----------|--------|
| Queue depth growing (unclaimed > 50) | Spawn rate too low | Lower W-gate thresholds (e.g., W2 gate from 70% → 60%) or spawn more agents per wave |
| Context RED (>85%) but queue shallow | Agents holding too much context | Reduce context budget per agent (e.g., Sonnet from 200K → 150K) or shorten task timeout |
| Agents stuck in-flight (return rate low) | Tasks are slow/blocked | Inspect manifest for blockedBy dependencies; unblock upstream tasks; or decompose large tasks |
| Zombie claims detected | Cleanup not running | Verify `cleanup_expired_claims()` is in SubagentStop hooks; or add a cron job |
| Wave never launches (stuck deferred) | Gate state stale post-compact | Ensure gate condition is re-evaluated after compact; implement declarative predicates |

---

## Summary

Queue equilibrium is a **dynamic steady-state**, not a static condition. Three forces (intake, spawn, context) must balance for the system to be stable. The mechanisms that enforce equilibrium are:

1. **Pre-computed summaries** — shift aggregation from read-time (faerie decisions) to write-time (queue mutations)
2. **Atomic operations** — rename-based claims, sentinel TTLs, cleanup on expiration
3. **Context-responsive gates** — wave deferral thresholds that respond to altimeter readings
4. **Monkeybranching momentum** — agents chain tasks when possible to reduce spawn overhead
5. **Forensic visibility** — every queue state change logged to COC; no silent mutations

When these mechanisms work together, the queue drains smoothly and context stays healthy. When one breaks (e.g., cleanup stops running, or gate state goes stale), the system drifts toward bottleneck. Monitoring the queue-summary file is the fastest way to detect equilibrium loss.

---

**Forensic reference:** Queue bottleneck diagnosis at `/mnt/d/0local/gitrepos/faerie2/forensics/diagnosis-queue-bottleneck.md` (2026-04-24, detailed root-cause analysis). Queue-claiming architecture at `/mnt/d/0local/gitrepos/faerie2/docs/QUEUE-CLAIMING-ARCHITECTURE.md` (agent-level claiming and monkeybranching design).

