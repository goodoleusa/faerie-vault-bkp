---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, sprint-queue]
parent:
  - "[[state-engine]]"
sibling:
  - "[[handoff-snapshot]]"
  - "[[brief-atoms]]"
child: []
inputs:
  - "[[faerie-start]]"
  - "[[handoff-end]]"
outputs:
  - "[[agent-work]]"
  - "[[subagent-spawning]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:05c0a1d76a9cebbcdbdb8ec85423bbb10feca12db6007eef23905c2dc643be10
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Sprint Queue

The sprint queue holds the work backlog — tasks prioritized, assigned, and tracked across sessions. Tasks carry: ID, type, description, assigned agent type, priority, dependencies, and status (pending/active/done/blocked). Faerie reads the queue at session start to assign work. Handoff updates statuses at session end. Multiple tasks can be active simultaneously; the queue is the coordinator, not a serializer.

## Flow

**In:** Task assignments from faerie-start, status updates from handoff-end, new tasks from user or agent suggestions
**Out:** Active task assignments to agent-work; spawning parameters for subagent-spawning

## Relationships

- [[faerie-start]] — reads queue at session open, assigns tasks to agents
- [[handoff-end]] — updates queue statuses at session close
- [[agent-work]] — executes tasks from the queue
- [[subagent-spawning]] — receives spawning parameters derived from queue tasks
- [[state-engine]] — parent layer; queue state is critical continuity data

## Natural Metaphor

A Kanban board: tasks move from backlog → active → done. The board doesn't do the work — it makes the work visible and coordinated across multiple workers.
