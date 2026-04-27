---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, memory-layer]
parent:
  - "[[_system-root]]"
sibling:
  - "[[session-lifecycle]]"
  - "[[state-engine]]"
  - "[[agent-layer]]"
child:
  - "[[honey-seed]]"
  - "[[nectar-narrative]]"
  - "[[scratch-working]]"
  - "[[review-inbox]]"
  - "[[crystallization]]"
inputs:
  - "[[agent-work]]"
  - "[[handoff-end]]"
outputs:
  - "[[faerie-start]]"
  - "[[agent-cards]]"
color: teal
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:65ac0f87c599817542a126eae2fef1c2b219aecc95aa8a39ae8a08619b8b01c2
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Memory Layer

The long-term nervous system of the hive. Memory has three temperature zones: hot (scratch — ephemeral, per-session), warm (NECTAR — append-only validated findings), and cold (HONEY — crystallized, dense, slow-changing). The crystallization cycle moves knowledge from hot to cold, distilling it against everything already known. Nothing is deleted; temperature changes.

## Flow

**In:** Scratch outputs from agent work, findings from handoff, flags from REVIEW-INBOX
**Out:** HONEY loaded at session start, NECTAR for researcher review, crystallized facts for agent cards

## Relationships

- [[honey-seed]] — cold memory: crystallized preferences and methods
- [[nectar-narrative]] — warm memory: append-only validated findings
- [[scratch-working]] — hot memory: working notes, per-session ephemeral
- [[review-inbox]] — human attention queue: HIGH-priority flags
- [[crystallization]] — the process that moves warm → cold

## Natural Metaphor

Geological strata: surface sediment (scratch) compacts under pressure (crystallization) into rock (HONEY). The rock remembers what the sediment was. Nothing is lost — only transformed.
