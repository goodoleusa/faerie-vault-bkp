---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, coc-hash-chain]
parent:
  - "[[forensic-layer]]"
sibling:
  - "[[hash-integrity]]"
child: []
inputs:
  - "[[agent-work]]"
  - "[[subagent-spawning]]"
  - "[[hash-integrity]]"
outputs: []
color: dark
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:82c915afcbb911ef492b69cc30fce38ef9db4cb86db2e2933f0b0588dc320602
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# COC Hash Chain

The chain-of-custody log. Every entry is HMAC-SHA256 signed, and each entry's hash references the previous entry's hash — forming an unbreakable chain. If any entry is tampered with, the chain breaks, and the tampering is detectable. Entries record: session ID, timestamp, agent type, agent version (from card), tool call type, tool call parameters, result hash, reasoning chain excerpt. Written by `forensic_coc.py` via PostToolUse hook — automatic, silent, never bypassed.

## Flow

**In:** Every PostToolUse event (automatic), spawn events, file operations
**Out:** Nothing flows out to agents. Immutable record. Researchers access via vault mirror.

## Relationships

- [[forensic-layer]] — parent layer; COC is the primary artifact
- [[hash-integrity]] — produces SHA256 proofs that COC embeds
- [[agent-cards]] — agent version (av= field) embedded in every entry
- [[agent-work]] — every tool call during work generates a COC entry automatically
- [[subagent-spawning]] — spawn events are logged with full context bundle hash

## Natural Metaphor

A geological core sample: each layer of sediment is identifiable, dateable, and in sequence. Drilling through it tells you exactly what happened when. You cannot reorder the layers without destroying the sample.
