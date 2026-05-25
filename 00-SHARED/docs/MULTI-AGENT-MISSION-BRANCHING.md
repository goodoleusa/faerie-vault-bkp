# Multi-Agent Mission Branching

**Phase 3 — Collaborative Workspace Substrate**
Introduced: 2026-04-25 | Task: task-20260425-153411-8f34

---

## Overview

Missions can now carry a `branches[]` field. Each branch is an independent work lane
that agents JOIN (not claim-the-whole-mission). Branches execute concurrently on different
subtasks; the convergence synthesizer fires only when every branch reaches `completed`.

This composes with existing mission-primary (step 3), worker ant colony, smart prereq,
sibling stigmergy, and reputation routing — it is additive, not a replacement.

---

## Web3 Parallels

| Web3 Concept | Faerie Equivalent | Why It Maps |
|---|---|---|
| **DAO proposal** | Mission | A DAO proposal defines a goal; token holders (agents) self-select into working groups |
| **Plasma chain** | Branch | Plasma chains run computation in parallel off the main chain; results are committed back when finalized |
| **Multi-sig threshold** | Convergence detector | The synthesizer task fires when `k-of-k` branches sign off (all must complete, not a quorum) |
| **Bonding curve / reputation** | `required_reputation` gate | Agents below a reputation threshold cannot join high-stakes branches — analogous to token staking for governance rights |
| **State channel** | Progressive manifest | A state channel lets two parties exchange signed state without on-chain txns; the branch manifest is the off-chain state visible to siblings |

### Key insight: plasma self-settlement without a coordinator

In Plasma, child chains settle to the root chain only at finalization. In faerie, branches
settle to the convergence synthesizer only when every branch writes `status=completed`. The
root (main context) never polls — it reads the heartbeat passively or waits for a
TaskNotification. This is **stigmergic plasma**: no SendMessage, no coordinator, no polling.

---

## Schema

### Mission object (missions dict value in sprint-queue.json)

```json
{
  "goal": "string",
  "member_task_ids": ["task-id", ...],
  "claim_state": "unclaimed | claimed",
  "branches": [
    {
      "branch_id": "branch-alpha",
      "name": "Human-readable lane name",
      "claimed_by": null,
      "status": "open | in_progress | completed | abandoned",
      "prereqs": ["branch-id", ...],
      "required_reputation": 0.0,
      "estimated_tokens": 20000,
      "agent_type": null,
      "progressive_manifest_path": null
    }
  ]
}
```

**Backward compatibility:** missions without `branches[]` continue to work exactly as before.
The convergence detector skips the branch check when `branches` is absent or empty.

### Branch fields

| Field | Type | Description |
|---|---|---|
| `branch_id` | str | Unique within this mission (e.g. `branch-alpha`) |
| `name` | str | Human-readable lane description |
| `claimed_by` | str \| null | Agent ID that joined this branch |
| `status` | enum | `open` → `in_progress` → `completed` \| `abandoned` |
| `prereqs` | list[str] | Branch IDs that must be `completed` before this branch is joinable |
| `required_reputation` | float | Min `reputation_score` for auto-join eligibility (default 0.0) |
| `estimated_tokens` | int | Estimated context cost; auto-join skips if remaining < this (default 20000) |
| `agent_type` | str \| null | If set, auto-join only matches agents of this type |
| `progressive_manifest_path` | str \| null | Path to per-branch live manifest; written on join and every update |

---

## Per-Branch Progressive Manifest

Location: `forensics/manifests/branches/{mission_id}/{branch_id}_progress.json`

Updated on every `mission join` and every `mission branch-update`. Sibling branches can
read this file at any time without coordination — stigmergy-first.

```json
{
  "mission_id": "mission-001",
  "branch_id": "branch-alpha",
  "branch_name": "Alpha: API design",
  "status": "in_progress",
  "claimed_by": "agent-007",
  "last_updated": "2026-04-25T15:00:00+00:00",
  "checkpoint": "schema-v2-done",
  "completions": 5
}
```

---

## Heartbeat

Location: `~/.claude/hooks/state/missions-heartbeat.json`

Updated on every `join`, `branch-update`, and `release`. Contains branch states + last
progress timestamp for all active missions. Auto-join scan reads this file (not the full
queue) for O(1) mission discovery.

---

## CLI Reference

### Join a branch (atomic, idempotent)

```bash
python3 scripts/7x_queue_ops.py mission join \
  --mission mission-001 \
  --branch branch-alpha \
  --agent agent-007
```

Returns `{success, mission_id, branch_id, claimed_by, progressive_manifest_path}`.
Idempotent: if the same agent calls again, `idempotent: true` is returned.

### Update branch progress

```bash
python3 scripts/7x_queue_ops.py mission branch-update \
  --mission mission-001 \
  --branch branch-alpha \
  --agent agent-007 \
  --status in_progress \
  --extra '{"checkpoint": "schema-v2", "completions": 5}'
```

### Auto-join scan (POST-EXEC in spawn template)

```bash
python3 scripts/7x_queue_ops.py mission auto-join-scan \
  --agent agent-007 \
  --type python-pro \
  --reputation 0.75 \
  --context-remaining 80000
```

Returns `{matched: true, mission_id, branch_id, branch_name, estimated_tokens}` or
`{matched: false, reason}`. Caller then calls `mission join` if matched.

---

## Convergence

`hooks/8x_mission_completion_synthesizer.py` fires when:

1. All `member_task_ids` have `status=completed`, AND
2. All `branches[].status == "completed"` (if `branches[]` is present and non-empty)

The synthesizer task is queued exactly once (idempotent via `_synth_already_queued`).
Missions without branches satisfy condition 2 trivially (backward compatible).

---

## Spawn Template POST-EXEC Integration

After an agent completes its primary task, the spawn template should run:

```python
scan = auto_join_scan(agent_id, agent_type, reputation_score, context_tokens_remaining)
if scan["matched"]:
    join_result = mission_join(scan["mission_id"], scan["branch_id"], agent_id)
    if join_result["success"]:
        # Execute branch work; update progress manifest periodically
        # Complete with: mission_branch_update(..., status="completed")
```

This is stigmergic self-assignment: agents find available work without any coordinator
broadcasting instructions. The heartbeat is the shared medium (analogous to pheromone trails).

---

## Queue Summary Marker

Missions with open branches are prefixed with `🔓` in queue-summary output, generated
by `_queue_summary_missions()` in `7x_queue_ops.py`. This allows main to instantly identify
collaborative work opportunities without reading mission details.

---

## Design Decisions

**Why per-branch not per-task claims?**
Task claims are all-or-nothing: one agent, one task. Branches model sub-lanes within a shared
goal where multiple agents contribute. Task claiming is exclusive; branch joining is concurrent.

**Why idempotent join?**
Network partitions and agent restarts are common. An agent that crashes mid-branch can rejoin
cleanly without intervention. The system treats re-joining the branch you already own as a no-op.

**Why heartbeat as a separate file?**
Agents should not read the full queue (contamination risk; queue lock contention). The heartbeat
is a distilled read surface — mission IDs + branch states — that auto-join scan can read without
touching the queue lock. It is eventually consistent (updated after every state change).

**Why prereqs as branch_ids not task_ids?**
Prereqs within a mission are naturally expressed as branch dependencies (plasma chain finality).
Task-level blocking is already handled by `blockedBy` in the queue. Two different mechanisms for
two different scopes.
