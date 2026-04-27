---
type: system-component
component_type: cycle
status: active
created: 2026-03-27
tags: [system, pseudosystem, debloat-cycle]
parent:
  - "[[equilibrium]]"
sibling:
  - "[[context-budget]]"
  - "[[crystallization]]"
child: []
inputs:
  - "[[honey-seed]]"
  - "[[agent-cards]]"
outputs:
  - "[[crystallization]]"
color: pistachio
concurrency: iterative
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:ac2e1502b327409d267238f64a0fd68f8b5e4e13ff439bfdc0c284b61f58889e
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Debloat Cycle

The budget enforcement cycle. `debloat.py --scan` runs at faerie startup and before committing session work. It counts lines in every durable file and reports which are over budget. Over-budget files block new content — they must be crystallized before any addition. The cycle: detect → crystallize → verify budget → allow write. This is not deletion; over-budget content is not discarded. It is integrated, densified, and re-written at budget.

## Flow

**In:** Durable files that may be at or over budget (HONEY, agent cards, rules files)
**Out:** Crystallization request for over-budget files; cleared budget that allows new content

## Relationships

- [[context-budget]] — the budget numbers that debloat enforces
- [[crystallization]] — what debloat triggers; the resolution for over-budget
- [[honey-seed]] — primary monitored file (200-line budget)
- [[agent-cards]] — monitored per-card (80-line budget; 120 for trained)
- [[equilibrium]] — parent layer; debloat is the enforcement arm of equilibrium

## Natural Metaphor

A river's flood control system: when the water level (file size) rises above the spillway (budget), the overflow gate opens (crystallization triggers). Water doesn't disappear — it's routed to the reservoir (denser storage).
