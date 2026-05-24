---
type: system-sidecar
subtype: data-file
status: active
date: 2026-05-20
tags: [system, mission, graph, dag, compass, sidecar]
memory_lane: system
promotion_state: permanent
N:
  - "[[00-Home]]"
  - "[[Flow-Orchestration]]"
E:
  - "[[manifest-index]]"
  - "[[coc]]"
S:
  - "[[Flow-Memory]]"
  - "[[Flow-Evolution]]"
---

# mission-graph.json

System sidecar for `forensics/mission-graph.json`.

**Role:** Compass DAG (directed acyclic graph) of all missions and their bearing-edge relationships.  
**Format:** JSON — nodes are missions, edges carry bearing direction (N/S/E/W).  
**Location:** `{repo}/forensics/mission-graph.json`

## Structure

```json
{
  "nodes": [
    { "id": "mission-id", "label": "Human-readable name", "status": "active" }
  ],
  "edges": [
    { "from": "mission-a", "to": "mission-b", "bearing": "S", "rationale": "..." }
  ]
}
```

## Compass bearing semantics

| Bearing | Meaning | Example |
|---|---|---|
| **N** | Unblock predecessor — A needs B cleared | Auth blocker → downstream feature |
| **S** | Conclude / deliver into — A ships into B | Feature → staging deploy |
| **E** | Parallel sister work at same DAG level | Doc update ↔ API update |
| **W** | Return to baseline / re-seat assumptions | Failed assumption → re-validate |

## Navigation

Used by `/run --missions` to cluster and route agents. Agents declare `next_mission_node` in their manifests to extend this graph.

## Related

- [[manifest-index]] — tracks in-flight tasks per mission node
- [[Flow-Orchestration]] — piston wave diagram
- [[coc]] — forensic audit trail
