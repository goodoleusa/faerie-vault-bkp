---
type: system-component
component_type: process
status: active
created: 2026-03-27
tags: [system, pseudosystem, subagent-spawning]
parent:
  - "[[agent-layer]]"
sibling:
  - "[[agent-cards]]"
  - "[[otj-learning]]"
child: []
inputs:
  - "[[sprint-queue]]"
  - "[[agent-cards]]"
  - "[[honey-seed]]"
outputs:
  - "[[agent-work]]"
  - "[[coc-hash-chain]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:986ef3e094dcb2ee71354901e7da363f0514a8073f0b22c0367cf7144b8fc4bd
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Subagent Spawning

Spawning is how agents come into existence. Work assigned to a specialist type MUST be executed by spawning that agent via the Agent tool — never simulated inline. The spawning protocol: match task to subagent_type from subagent-options.json, build a context bundle (task + HONEY + prior findings + agent card), include the OTJ training block, call Agent tool. Multiple independent tasks spawn in parallel in the same message. The roster is updated after each spawn.

## Flow

**In:** Task assignments from sprint queue, agent identity from cards, crystallized context from HONEY
**Out:** Active agents executing in parallel (agent-work); spawn events logged to COC chain

## Relationships

- [[sprint-queue]] — source of task assignments
- [[agent-cards]] — source of agent identity loaded into context bundle
- [[honey-seed]] — crystallized context included in every bundle
- [[agent-work]] — what spawning produces
- [[coc-hash-chain]] — spawn events are logged with agent version
- [[agent-layer]] — parent layer

## Natural Metaphor

A queen bee laying eggs: each egg is genetically encoded with its specialist role. The egg (context bundle) contains everything the hatching bee (agent) needs to know who it is and what it does.
