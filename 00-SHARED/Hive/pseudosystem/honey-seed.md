---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, honey-seed]
parent:
  - "[[memory-layer]]"
sibling:
  - "[[nectar-narrative]]"
  - "[[scratch-working]]"
child: []
inputs:
  - "[[crystallization]]"
outputs:
  - "[[faerie-start]]"
  - "[[agent-work]]"
color: pistachio
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:7071d28e293cf45f07d0b842b2569e7f4a2a55ac737f019306ae80b81a57c4e2
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# HONEY Seed

HONEY is the crystallized long-term memory of the system: preferences, methods, agent identity, and durable patterns of operation. It is read at the start of every session and updated only through crystallization — never by raw append. Budget: 200 lines. Every fact in HONEY has survived integration against everything else known; nothing redundant survives. It is dense by design.

## Flow

**In:** Crystallized output from the crystallization cycle (NECTAR → HONEY distillation)
**Out:** Loaded context for faerie-start and every spawned agent; shapes all decisions

## Relationships

- [[crystallization]] — the only process that writes to HONEY
- [[nectar-narrative]] — the source material that crystallization distills from
- [[faerie-start]] — reads HONEY at session open
- [[agent-cards]] — agent-specific HONEY equivalent (per-type crystallized state)
- [[debloat-cycle]] — enforces the 200-line budget

## Natural Metaphor

Honeycomb: each hexagonal cell holds a single concentrated unit of knowledge, maximum nutrition per gram. The comb is finite; filling a new cell requires checking if an existing cell already holds that nectar.
