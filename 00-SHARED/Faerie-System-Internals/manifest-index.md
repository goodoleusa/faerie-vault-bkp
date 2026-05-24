---
type: system-sidecar
subtype: data-file
status: active
date: 2026-05-20
tags: [system, manifest, sidecar, stigmergy, in-flight]
memory_lane: system
promotion_state: permanent
N:
  - "[[00-Home]]"
  - "[[Flow-Orchestration]]"
E:
  - "[[mission-graph]]"
  - "[[coc]]"
S:
  - "[[Flow-Memory]]"
blueprint: "[[Session-Manifest.blueprint]]"
---

# manifest-index.jsonl

System sidecar for `forensics/ephemeral/{YYYY-MM-DD}/manifest-index-{date}.jsonl`.

**Role:** Single source of truth for all in-flight agent tasks in the current session.  
**Format:** newline-delimited JSON — one record per task.  
**Location:** `{repo}/forensics/ephemeral/{YYYY-MM-DD}/manifest-index-{date}.jsonl`

## Fields per record

| Field | Type | Description |
|---|---|---|
| `task_id` | string | Unique task identifier (deterministic) |
| `status` | enum | `in_progress` / `completed` / `failed` |
| `mission` | string | Semantic mission cluster |
| `bearing` | N/S/E/W | Compass direction |
| `agent_type` | string | Archetype spawned |
| `in_flight` | int | Count of running tasks |
| `dashboard_line` | string | ≤80 char summary for Queen |

## Queen reads this at spawn-time

Before any `Agent()` spawn the pre-spawn hook reads this file to enforce:  
`in_flight + agents_to_spawn ≤ 10` (prevents over-spawning).

## Related

- [[Flow-Orchestration]] — piston wave diagram showing manifest flow
- [[mission-graph]] — companion DAG file
- [[coc]] — hash-chained audit trail
