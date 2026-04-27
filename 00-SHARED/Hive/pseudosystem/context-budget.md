---
type: system-component
component_type: state
status: active
created: 2026-03-27
tags: [system, pseudosystem, context-budget]
parent:
  - "[[equilibrium]]"
sibling:
  - "[[debloat-cycle]]"
child: []
inputs:
  - "[[debloat-cycle]]"
outputs:
  - "[[crystallization]]"
  - "[[debloat-cycle]]"
color: gold
concurrency: sequential
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:c69bdf367337ea2431024c70bf0b1d7d4ade8dd8d5d477427344c02f3d69de31
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Context Budget

The quantified rules of equilibrium. Every durable file has a line budget: Rules files 300L, CLAUDE.md 30L, HONEY 200L, AGENTS.md 150L, agent cards 80L (120 trained), faerie.md 120L, LAUNCH.md 90L. NECTAR and REVIEW-INBOX are unbounded (append-only, never crystallize). The budget is not a suggestion — it IS the equilibrium mechanism. A budget forces crystallization; without budgets, files grow indefinitely and become unusable. The constraint creates quality.

## Flow

**In:** Line counts from debloat-cycle scans; budget definitions from this component
**Out:** Budget verdicts (under/over) that gate writes; crystallization triggers for over-budget files

## Relationships

- [[debloat-cycle]] — reads budget definitions to determine over/under status
- [[crystallization]] — triggered by over-budget verdicts; the resolution
- [[honey-seed]] — governed by 200L budget
- [[agent-cards]] — governed by 80L (120L trained) budget per card
- [[equilibrium]] — parent layer; budget is the quantified expression of equilibrium

## Natural Metaphor

The size of a honeycomb cell: fixed. You cannot add more honey than the cell holds. When the cell is full, you build a new cell — you do not enlarge the old one. The constraint is what makes honey storable.
