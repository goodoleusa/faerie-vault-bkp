---
type: system-component
component_type: process
status: active
created: 2026-03-27
tags: [system, pseudosystem, handoff-end]
parent:
  - "[[session-lifecycle]]"
sibling:
  - "[[faerie-start]]"
child: []
inputs:
  - "[[scratch-working]]"
  - "[[brief-atoms]]"
  - "[[agent-outbox]]"
outputs:
  - "[[handoff-snapshot]]"
  - "[[nectar-narrative]]"
  - "[[brief-atoms]]"
color: gold
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:2cefc0f36e795c6138127ccf8840c3e4850308d634d8b3dcf851078a784dfe5d
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Handoff End

The session-closing mirror of [[faerie-start]]. Handoff crystallizes scratch into NECTAR, writes the handoff snapshot, appends a brief atom, and prepares the context bundle for the next session's faerie call. It is the exhale of the breath cycle. Its inputs are exactly the outputs of [[faerie-start]], and its outputs are exactly the inputs to the next [[faerie-start]]. This symmetry is not accidental — it is the architectural proof that the system is conservative.

## Flow

**In:** Session scratch notes, accumulated brief atoms, agent outbox drafts
**Out:** Handoff snapshot (next session's starting state), NECTAR promotions, fresh brief atom

## Relationships

- [[faerie-start]] — exact mirror; together they form a closed loop
- [[handoff-snapshot]] — primary artifact produced
- [[nectar-narrative]] — validated findings promoted here by memory-keeper
- [[brief-atoms]] — checkpoint appended at close
- [[crystallization]] — may trigger a crystallization cycle before writing

## Natural Metaphor

A conductor stepping off the podium: annotates the score (snapshot), files the performance notes (NECTAR), leaves a note for tomorrow's conductor (brief atoms). The music lives on.
