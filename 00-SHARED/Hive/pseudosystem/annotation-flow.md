---
type: system-component
component_type: cycle
status: active
created: 2026-03-27
tags: [system, pseudosystem, annotation-flow]
parent:
  - "[[vault-layer]]"
sibling:
  - "[[agent-outbox]]"
  - "[[human-evidence]]"
child: []
inputs:
  - "[[agent-outbox]]"
  - "[[review-inbox]]"
outputs:
  - "[[human-evidence]]"
color: coral
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:472b2540b3e661614b7fda028b201f335fd63652b64586d35e68b1ad03b83be9
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Annotation Flow

The cycle of human review. When an agent deposits a draft in the outbox, or a HIGH flag lands in REVIEW-INBOX, a human enters the loop: reads the finding, applies the blueprint-FINDING-review.md template (adding Review Assessment, Annotations, Court Prep Notes), and decides whether to promote to 30-Evidence/. This is not a rubber stamp — human judgment is required at every step. Obsidian Blueprints facilitate the template; no Templater syntax, compatible with mobile.

## Flow

**In:** Agent outbox drafts awaiting review, HIGH-priority flags from review-inbox
**Out:** Promoted, annotated findings in human-evidence (30-Evidence/)

## Relationships

- [[agent-outbox]] — primary input: where drafts wait
- [[review-inbox]] — secondary input: HIGH flags trigger annotation attention
- [[human-evidence]] — output: what survives human review
- [[vault-layer]] — parent layer
- [[forensic-layer]] — forensic provenance attaches to promoted findings; the two systems are synchronized at promotion

## Natural Metaphor

A photo darkroom: the developer (agent) prepares the negative (draft); the photographer (human) decides which prints to enlarge and mount. The darkroom is process; the gallery wall is judgment.
