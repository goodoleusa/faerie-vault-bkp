---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, agent-cards]
parent:
  - "[[agent-layer]]"
sibling:
  - "[[otj-learning]]"
  - "[[subagent-spawning]]"
child: []
inputs:
  - "[[otj-learning]]"
  - "[[crystallization]]"
outputs:
  - "[[subagent-spawning]]"
  - "[[agent-work]]"
color: pistachio
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:14a1eeb2aaf2bb39e500bf65af3bfb1c3a9d923008949543b67e5e28e3593cfc
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Agent Cards

Agent cards are the crystallized identity of each specialist type: role definition, KPIs, last training score, deployment score, and durable process learnings. 23 types exist. Cards have a strict 80-line budget (120 for trained agents). They are court-defensible: cards may only contain process/methodology learnings, never case-specific data. A defense attorney test applies to every bullet: "Could this bias the analysis?" If yes, it does not belong in the card.

## Flow

**In:** OTJ learning reflections from post-work cycles; crystallization distillation
**Out:** Identity and method context loaded at agent spawn time; versioning anchors forensic provenance

## Relationships

- [[otj-learning]] — the cycle that updates cards when a new high score is achieved
- [[crystallization]] — may trigger card updates as part of a memory round
- [[subagent-spawning]] — reads the card to build the agent's context bundle
- [[honey-seed]] — cards are the agent-specific equivalent of HONEY
- [[coc-hash-chain]] — agent version (date_score) from card is embedded in every COC entry

## Natural Metaphor

A professional's CV with a legal constraint: it records only transferable skills and methodology, never client names or case specifics. The skill is durable; the case is not.
