---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, session-lifecycle]
parent:
  - "[[_system-root]]"
sibling:
  - "[[memory-layer]]"
  - "[[state-engine]]"
child:
  - "[[faerie-start]]"
  - "[[agent-work]]"
  - "[[handoff-end]]"
  - "[[emergency-handoff]]"
inputs:
  - "[[handoff-snapshot]]"
  - "[[honey-seed]]"
  - "[[sprint-queue]]"
outputs:
  - "[[handoff-snapshot]]"
  - "[[scratch-working]]"
  - "[[brief-atoms]]"
color: teal
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:d1face60ee93a3fc696c20a688678a65fb05a973d9d73dec0d7022413cc2cc75
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Session Lifecycle

The session lifecycle is the heartbeat of the hive. Each session begins with faerie orienting on prior context, proceeds through parallel agent work, and closes with handoff preserving continuity. The pattern is: **orient → work → crystallize → hand off**. Sessions are finite; the system is not. Each cycle deepens the knowledge base.

## Flow

**In:** Handoff snapshot from prior session, HONEY seed, sprint queue tasks
**Out:** Updated handoff snapshot, new scratch notes, brief atoms, promoted findings

## Relationships

- [[faerie-start]] — session open: reads state, launches agents, builds dashboard
- [[agent-work]] — the productive middle: parallel specialist execution
- [[handoff-end]] — session close: crystallizes, writes snapshot, queues next sprint
- [[emergency-handoff]] — circuit breaker: fires at 1% context, preserves state in 1.5s
- [[handoff-snapshot]] — the artifact that bridges sessions
- [[sprint-queue]] — what work gets done this session

## Natural Metaphor

A single breath: inhale (faerie start, draw in context), hold (work, transform it), exhale (handoff, release crystallized knowledge). The lungs don't remember each breath — but the blood does.
