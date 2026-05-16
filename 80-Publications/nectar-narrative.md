---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, nectar-narrative]
parent:
  - "[[memory-layer]]"
sibling:
  - "[[honey-seed]]"
  - "[[scratch-working]]"
child: []
inputs:
  - "[[handoff-end]]"
  - "[[agent-work]]"
outputs:
  - "[[crystallization]]"
  - "[[honey-seed]]"
color: teal
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:9d97bd22bd337a76dc12ae8613d9856f0654e71c3e1b73c0c9d1b6925490b6d0
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# NECTAR Narrative

NECTAR is the append-only validated findings log — the investigation's permanent record. It is never compressed, never crystallized, never overwritten. Findings are promoted here by the memory-keeper agent after validation. NECTAR is the forensic truth of what the system has discovered and when. Unbounded by design; the only durable file with no line budget.

## Flow

**In:** Validated findings from handoff-end, promoted scratch entries from memory-keeper
**Out:** Source material for crystallization cycles that distill HONEY; tail-30 loaded for investigation sessions

## Relationships

- [[scratch-working]] — upstream source; memory-keeper promotes scratch → NECTAR
- [[handoff-end]] — triggers NECTAR promotion at session close
- [[crystallization]] — reads NECTAR as source material; extracts to HONEY
- [[honey-seed]] — downstream destination; NECTAR's essence lives there
- [[coc-hash-chain]] — forensic parallel: NECTAR is findings, COC is provenance

## Natural Metaphor

A river: always flowing forward, never reversing. Each session adds volume. The crystallization cycle is where river water evaporates and falls as rain on HONEY — the same water, transformed.
