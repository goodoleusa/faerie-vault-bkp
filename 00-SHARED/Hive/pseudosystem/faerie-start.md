---
type: system-component
component_type: process
status: active
created: 2026-03-27
tags: [system, pseudosystem, faerie-start]
parent:
  - "[[session-lifecycle]]"
sibling:
  - "[[handoff-end]]"
child:
  - "[[agent-work]]"
inputs:
  - "[[handoff-snapshot]]"
  - "[[honey-seed]]"
  - "[[sprint-queue]]"
outputs:
  - "[[agent-work]]"
  - "[[brief-atoms]]"
color: gold
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:1262f2f78b76effce499ae4a2963d1ebfc56ee0201d3c33c3a32b0b6ff505801
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Faerie Start

Faerie is the session-opening orchestrator. On invocation, it reads the prior handoff snapshot, loads HONEY for crystallized preferences, scans the sprint queue, assembles a context bundle, and launches the appropriate specialist agents. It produces a dashboard summary and hands off task assignments. Faerie is the gateway — everything enters through it and exits through [[handoff-end]], its mirror.

## Flow

**In:** Handoff snapshot (prior session state), HONEY seed (crystallized knowledge), sprint queue (pending tasks)
**Out:** Launched agents with context bundles, dashboard update, brief atom checkpoint

## Relationships

- [[handoff-end]] — mirror process; inputs and outputs are symmetric
- [[handoff-snapshot]] — primary input: where the last session left off
- [[honey-seed]] — crystallized preferences loaded at start
- [[sprint-queue]] — task list consumed and assigned
- [[agent-work]] — what faerie launches
- [[brief-atoms]] — checkpoint written at open

## Natural Metaphor

A conductor stepping onto the podium: reads the score (handoff), checks who is in the orchestra (agents), raises the baton (launches work). The performance begins.
