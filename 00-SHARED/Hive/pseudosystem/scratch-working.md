---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, scratch-working]
parent:
  - "[[memory-layer]]"
sibling:
  - "[[honey-seed]]"
  - "[[nectar-narrative]]"
  - "[[review-inbox]]"
child: []
inputs:
  - "[[agent-work]]"
outputs:
  - "[[handoff-end]]"
  - "[[nectar-narrative]]"
  - "[[review-inbox]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:762af00425df9dd1bb72d9ccf7a0c757eb7bd71360b8cbe2d5b5f88d332ca623
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Scratch Working

Scratch is the ephemeral working memory of a session — one file per session ID, gitignored, written by agents as they work. It holds MEM blocks: observations, flags, technique discoveries, first impressions, open questions. At session end, memory-keeper promotes high-value entries to NECTAR and REVIEW-INBOX. What is not promoted evaporates. Scratch is intentionally disposable; only the crystallized extract survives.

## Flow

**In:** MEM blocks written by agents during work — observations, flags, techniques, first impressions
**Out:** Promoted findings to NECTAR (via memory-keeper), HIGH flags to REVIEW-INBOX, context for handoff-end

## Relationships

- [[agent-work]] — every agent writes here during execution
- [[handoff-end]] — reads scratch to prepare the session summary
- [[nectar-narrative]] — destination for promoted findings
- [[review-inbox]] — HIGH-priority flags routed here immediately
- [[otj-learning]] — reflection MEM blocks land here after each work unit

## Natural Metaphor

River water: always fresh, always moving, carrying sediment downstream. Tomorrow's river doesn't hold today's specific water molecules — but the river bed remembers where they flowed.
