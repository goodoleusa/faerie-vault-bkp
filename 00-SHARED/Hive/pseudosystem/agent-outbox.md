---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, agent-outbox]
parent:
  - "[[vault-layer]]"
sibling:
  - "[[human-evidence]]"
  - "[[annotation-flow]]"
child: []
inputs:
  - "[[agent-work]]"
outputs:
  - "[[annotation-flow]]"
color: teal
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:d242727fdf33c9d67334461bea1eed73fe2ea6a6c61a7bf2f240503f66c43afe
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Agent Outbox

The staging area for agent-drafted vault content. Located at `00-SHARED/Agent-Outbox/` — the only vault folder agents may write to. Drafts follow the FINDING-template.md format: frontmatter with run_id, confidence, source_agent, sha256_source, and git_commit; body with What Was Found, Why It Matters, The Numbers, Evidence Chain, Open Questions. Agents never touch 30-Evidence/. The human promotion step is the trust boundary.

## Flow

**In:** Completed finding drafts from agent-work, following the FINDING-template.md standard
**Out:** Drafts waiting for human review in annotation-flow; human may promote to 30-Evidence/

## Relationships

- [[agent-work]] — agents write here at the end of a finding-producing run
- [[annotation-flow]] — the human review cycle that processes outbox drafts
- [[human-evidence]] — destination after human promotion; agents never see this
- [[vault-layer]] — parent layer; outbox is the agent write zone
- [[hash-integrity]] — every draft includes sha256_source linking to the evidence file

## Natural Metaphor

An editor's submission inbox: writers (agents) deposit manuscripts, the editor (human) decides what to publish. The magazine (30-Evidence/) is not the inbox; it is what survives the editorial process.
