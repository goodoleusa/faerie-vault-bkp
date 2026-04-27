---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, handoff-snapshot]
parent:
  - "[[state-engine]]"
sibling:
  - "[[brief-atoms]]"
  - "[[sprint-queue]]"
child: []
inputs:
  - "[[handoff-end]]"
  - "[[emergency-handoff]]"
outputs:
  - "[[faerie-start]]"
color: pistachio
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:2aee56291acefc2892a720197b23f4c8723b4215669e4e411121b4b4aad1af8f
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Handoff Snapshot

The handoff snapshot is the single artifact that enables session continuity. Written at session close by [[handoff-end]] (or in minimal form by [[emergency-handoff]]), it packages: what was done, what is next, what is blocked, key decisions, files touched, and the brief context for the incoming session. It is not a log — it is an orientation document. Every snapshot overwrites the previous; history lives in brief-atoms.

## Flow

**In:** Session summary from handoff-end, or minimal state from emergency-handoff
**Out:** Opening context for faerie-start — the first thing read at session open

## Relationships

- [[handoff-end]] — primary writer; produces the full-form snapshot
- [[emergency-handoff]] — fallback writer; produces minimal snapshot at 1% context
- [[faerie-start]] — primary reader; unpacks snapshot to orient the new session
- [[brief-atoms]] — the historical record; snapshot is the current view
- [[state-engine]] — parent layer managing all state artifacts

## Natural Metaphor

A shift-change note at a hospital: the outgoing nurse writes what happened, what's pending, what to watch. The incoming nurse doesn't need to re-examine every chart — the note tells them where to start.
