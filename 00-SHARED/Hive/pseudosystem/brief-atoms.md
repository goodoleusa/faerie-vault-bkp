---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, brief-atoms]
parent:
  - "[[state-engine]]"
sibling:
  - "[[handoff-snapshot]]"
  - "[[sprint-queue]]"
child: []
inputs:
  - "[[faerie-start]]"
  - "[[agent-work]]"
  - "[[handoff-end]]"
outputs:
  - "[[handoff-snapshot]]"
  - "[[emergency-handoff]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:0f917912183e247d3bd73efad84e3dc0ca9efb32ab94bb5fb6af8886765e17a4
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Brief Atoms

Brief atoms are the event-sourced checkpoint log of the system — small, timestamped state snapshots written throughout a session. They are never overwritten; only appended. At session open (faerie), a new atom is written. At key transitions (major finding, task completion, context warning), another. At session close (handoff), another. Together they form a complete event trace. The emergency handoff uses the most recent atom as its recovery point.

## Flow

**In:** Checkpoint events from faerie-start, agent-work milestones, and handoff-end
**Out:** Recovery state for emergency-handoff; history context for handoff-snapshot construction

## Relationships

- [[faerie-start]] — writes an atom at session open
- [[handoff-end]] — writes a closing atom and reads atoms to build the snapshot
- [[emergency-handoff]] — reads the latest atom as the recovery anchor
- [[handoff-snapshot]] — constructed from atoms; snapshot is the synthesis, atoms are the evidence
- [[state-engine]] — parent layer

## Natural Metaphor

Event sourcing in software: every state change is an immutable event in the log. Current state is derived by replaying the log. The log is the truth; derived state is convenience.
