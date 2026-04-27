---
type: system-component
component_type: cycle
status: active
created: 2026-03-27
tags: [system, pseudosystem, otj-learning]
parent:
  - "[[agent-layer]]"
sibling:
  - "[[agent-cards]]"
  - "[[crystallization]]"
child: []
inputs:
  - "[[agent-work]]"
outputs:
  - "[[scratch-working]]"
  - "[[agent-cards]]"
color: teal
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:fd9c51b543a912f67407d518dc902f44485016dfda768437609d52581a5ee020
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# OTJ Learning

On-the-job learning is the reflection protocol that fires after every agent work unit — 2K tokens, not optional. Every agent reflects before returning: what worked, what was harder than expected, what would I do differently. The output is 1-2 MEM blocks written to scratch. If a reusable technique was discovered, it is tagged `cat=TECHNIQUE` for cross-agent promotion. If a new high deployment score was achieved, the agent card is updated. Failure outputs are also learning material.

## Flow

**In:** Completed work unit from agent-work
**Out:** OBSERVATION and TECHNIQUE MEM blocks to scratch; agent card update if score beat; training-queue entry if score missed

## Relationships

- [[agent-work]] — triggers OTJ at completion; every agent, every run
- [[scratch-working]] — receives the reflection MEM blocks
- [[agent-cards]] — updated when deployment score is beaten (never on training score alone)
- [[crystallization]] — TECHNIQUE blocks eventually reach AGENTS.md via crystallization
- [[coc-hash-chain]] — the forensic record includes the agent version at time of learning

## Natural Metaphor

A surgeon's post-operative debrief: not optional, not performative. The team reflects on what happened, what was harder than expected, what they'd do differently. The learning accumulates into better technique.
