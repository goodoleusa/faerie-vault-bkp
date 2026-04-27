---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, review-inbox]
parent:
  - "[[memory-layer]]"
sibling:
  - "[[scratch-working]]"
  - "[[nectar-narrative]]"
child: []
inputs:
  - "[[agent-work]]"
  - "[[scratch-working]]"
outputs:
  - "[[human-evidence]]"
  - "[[annotation-flow]]"
color: coral
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:faf1638818250bea22ee2dafb4442d8d85baa3b2b5817f99b40fe1fd467f81db
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Review Inbox

The human attention queue. Agents append HIGH-priority flags here immediately when found — before scratch promotion, before session end. Items include HEADLINE findings, CONFIRMED evidence, and anything that requires a human decision before the system can proceed. Unbounded and append-only. The coral color signals: this is where the human layer begins.

## Flow

**In:** HIGH-priority MEM blocks from any agent during work; lengthy findings siphon to forensics/researcher-review/ with a pointer left here
**Out:** Human review triggers annotation flow; reviewed items promote to vault human-evidence

## Relationships

- [[agent-work]] — agents write HIGH flags here directly, not just to scratch
- [[scratch-working]] — lower-priority items live here; HIGH items are duplicated to inbox
- [[annotation-flow]] — what happens after a human reviews an item
- [[human-evidence]] — destination for promoted, human-validated findings
- [[vault-layer]] — REVIEW-INBOX mirrors to 00-Agent-Inbox/ in the vault

## Natural Metaphor

A physical inbox on a desk: agents drop notes in, the investigator picks them up. The inbox doesn't think — it holds. The thinking happens when the human reads it.
