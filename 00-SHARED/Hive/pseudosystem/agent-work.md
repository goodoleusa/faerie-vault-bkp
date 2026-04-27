---
type: system-component
component_type: process
status: active
created: 2026-03-27
tags: [system, pseudosystem, agent-work]
parent:
  - "[[session-lifecycle]]"
sibling:
  - "[[faerie-start]]"
  - "[[handoff-end]]"
child:
  - "[[subagent-spawning]]"
  - "[[otj-learning]]"
inputs:
  - "[[sprint-queue]]"
  - "[[honey-seed]]"
  - "[[agent-cards]]"
outputs:
  - "[[scratch-working]]"
  - "[[review-inbox]]"
  - "[[coc-hash-chain]]"
  - "[[agent-outbox]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:ac7a2b64889dac585c7344601caceb338570234f7b24c8cc4e65208139d1b567
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Agent Work

The productive middle of every session. Multiple specialist agents execute in parallel, each with their own context bundle, task assignment, and OTJ learning protocol. Agents write to scratch, flag findings to REVIEW-INBOX, log to the COC chain, and deposit drafts to the agent outbox. Work is parallel by design — the system does not serialize unnecessarily.

## Flow

**In:** Task assignments from sprint queue, crystallized context from HONEY, agent identity from agent cards
**Out:** Scratch notes, HIGH-priority flags, forensic COC log entries, agent outbox drafts

## Relationships

- [[subagent-spawning]] — how agents are instantiated (Agent tool, never inline)
- [[otj-learning]] — reflection protocol that fires after every work unit
- [[scratch-working]] — primary write target during work
- [[review-inbox]] — HIGH-priority findings routed here immediately
- [[coc-hash-chain]] — every tool call logged automatically
- [[agent-outbox]] — vault-facing drafts deposited here

## Natural Metaphor

River water: always moving, branching into parallel channels, carrying sediment (findings) downstream. Never stagnant, never looping back upstream.
