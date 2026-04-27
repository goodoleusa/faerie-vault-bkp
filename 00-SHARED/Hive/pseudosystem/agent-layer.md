---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, agent-layer]
parent:
  - "[[_system-root]]"
sibling:
  - "[[session-lifecycle]]"
  - "[[memory-layer]]"
  - "[[forensic-layer]]"
child:
  - "[[agent-cards]]"
  - "[[otj-learning]]"
  - "[[subagent-spawning]]"
inputs:
  - "[[sprint-queue]]"
  - "[[honey-seed]]"
outputs:
  - "[[scratch-working]]"
  - "[[coc-hash-chain]]"
  - "[[agent-outbox]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:a5c91622f9fbc22dee5b26254071264bf30a011e83556907d730048c998480c4
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Agent Layer

The workforce. 23 specialist agent types, each with its own identity (agent card), KPIs, and OTJ learning protocol. Agents are spawned via the Agent tool — never simulated inline. Each agent receives a context bundle, executes its task, writes to scratch, logs to COC, and reflects before returning. The agent layer is parallel by default; specialists work simultaneously on independent tasks.

## Flow

**In:** Task context from sprint queue, crystallized knowledge from HONEY, identity from agent cards
**Out:** Scratch MEM blocks, forensic COC log entries, vault-facing drafts in agent outbox

## Relationships

- [[agent-cards]] — each agent's crystallized identity: KPIs, last training, methods
- [[otj-learning]] — the reflection cycle every agent runs after work
- [[subagent-spawning]] — the mechanism: Agent tool, subagent_type, context bundle
- [[honey-seed]] — read at spawn time for crystallized context
- [[scratch-working]] — primary write target during work
- [[coc-hash-chain]] — forensic log written automatically by PostToolUse hook

## Natural Metaphor

A beehive's worker population: diverse specialists (forager, nurse, builder, guard), each with instinctive protocols, working in parallel toward collective goals. No individual bee holds the whole plan — but the hive does.
