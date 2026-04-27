---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, equilibrium]
parent:
  - "[[_system-root]]"
sibling:
  - "[[memory-layer]]"
  - "[[session-lifecycle]]"
child:
  - "[[debloat-cycle]]"
  - "[[context-budget]]"
inputs:
  - "[[agent-work]]"
  - "[[crystallization]]"
outputs:
  - "[[honey-seed]]"
  - "[[agent-cards]]"
color: pistachio
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:045ba772bbacda4cbb6d01206ec825a3d0c298c7f8955db0211737bb8828315d
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Equilibrium

The regulating force. The system maintains balance between what flows in and what flows out: context consumed equals knowledge crystallized; energy in equals work out; file size is held at budget through crystallization. Equilibrium is not stasis — it is dynamic balance. A file at budget is not frozen; it is continuously renewed as new knowledge displaces older, less relevant knowledge through the crystallization cycle.

## Flow

**In:** Over-budget files detected by debloat scan; context usage metrics; agent outputs
**Out:** Crystallized files at budget; renewed HONEY; density-maximized agent cards

## Relationships

- [[debloat-cycle]] — the enforcement mechanism: detects over-budget files, triggers crystallization
- [[context-budget]] — the quantified rules: 300L for rules files, 200L for HONEY, 80L for agent cards
- [[crystallization]] — the resolution: over-budget triggers crystallization, not deletion
- [[honey-seed]] — primary target of equilibrium maintenance
- [[agent-cards]] — secondary target: 80-line budget enforced per card

## Natural Metaphor

A living ecosystem: inputs and outputs balance over time. Too much nutrient in a lake causes algae bloom (over-budget files). The system self-regulates through decomposition (crystallization) and uptake — returning to clarity.
