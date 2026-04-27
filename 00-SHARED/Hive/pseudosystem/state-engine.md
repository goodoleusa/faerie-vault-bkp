---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, state-engine]
parent:
  - "[[_system-root]]"
sibling:
  - "[[session-lifecycle]]"
  - "[[memory-layer]]"
child:
  - "[[handoff-snapshot]]"
  - "[[brief-atoms]]"
  - "[[sprint-queue]]"
inputs:
  - "[[handoff-end]]"
  - "[[agent-work]]"
outputs:
  - "[[faerie-start]]"
  - "[[emergency-handoff]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:9661ef90c102bdf5d3464ef309e5d1fc10e811976e04e839a5fee3a58336c1a2
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# State Engine

The state engine is the continuity mechanism — the thread that connects sessions across the context wall. Where HONEY is deep knowledge, the state engine holds positional information: what was happening, what was next, what was blocked. Brief atoms accumulate during work; the snapshot packages them at session end; faerie unpacks them at session start. The system never starts from zero.

## Flow

**In:** Findings and checkpoints from agent work and handoff-end
**Out:** State context for faerie-start; emergency snapshot for emergency-handoff

## Relationships

- [[handoff-snapshot]] — the packaged state bundle written at session end
- [[brief-atoms]] — the event-sourced checkpoints accumulated during a session
- [[sprint-queue]] — the task state: what's done, what's pending, what's blocked
- [[handoff-end]] — writes the snapshot
- [[faerie-start]] — reads the snapshot
- [[emergency-handoff]] — reads brief atoms as fallback

## Natural Metaphor

A bookmark in a book: it doesn't hold the story — it holds where you were. Combined with the book (HONEY), the next reader can pick up exactly where the last left off.
