---
type: system-component
component_type: layer
status: active
created: 2026-03-27
tags: [system, pseudosystem, index]
parent:
  - "[[_system-root]]"
sibling: []
child: []
inputs: []
outputs: []
color: gold
concurrency: parallel
memory_lane: reference
promotion_state: crystallized
doc_hash: sha256:d10b365d24344e6bbb20e99aca4d9e799b36acbd52cc0206d9f0d474ab38dfec
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# Faerie System — Component Index

This note is the navigable index of the pseudosystem graph. Every note in this folder represents a component of the faerie agent architecture. Explore via Obsidian graph view or ExcaliBrain for the interactive relationship map.

## Color Key

| Color | Meaning | Components |
|---|---|---|
| gold | Boundary / gateway — inputs mirror outputs | faerie-start, handoff-end, emergency-handoff, context-budget, _index |
| teal | Flowing / active state — water in motion | agent-work, scratch-working, nectar-narrative, sprint-queue, brief-atoms, state-engine, memory-layer, agent-layer, agent-outbox, subagent-spawning, otj-learning |
| pistachio | Settled / crystallized — crystal formed | honey-seed, crystallization, handoff-snapshot, agent-cards, debloat-cycle, equilibrium |
| dark | Immutable / bedrock — never changes | forensic-layer, coc-hash-chain, hash-integrity |
| coral | Human layer — warmth, attention required | review-inbox, vault-layer, human-evidence, annotation-flow |

## Layer Map

```
_system-root (The Hive)
├── session-lifecycle  →  faerie-start · agent-work · handoff-end · emergency-handoff
├── memory-layer       →  honey-seed · nectar-narrative · scratch-working · review-inbox · crystallization
├── state-engine       →  handoff-snapshot · brief-atoms · sprint-queue
├── agent-layer        →  agent-cards · otj-learning · subagent-spawning
├── forensic-layer     →  coc-hash-chain · hash-integrity
├── vault-layer        →  agent-outbox · human-evidence · annotation-flow
└── equilibrium        →  debloat-cycle · context-budget
```

## All Components

```dataviewjs
const pages = dv.pages('"00-SHARED/00-META/pseudosystem"')
  .where(p => p.type === "system-component")
  .sort(p => p.file.name);

dv.table(
  ["Component", "Type", "Color", "Concurrency", "Inputs", "Outputs"],
  pages.map(p => [
    p.file.link,
    p.component_type || "-",
    p.color || "-",
    p.concurrency || "-",
    (p.inputs || []).join(", "),
    (p.outputs || []).join(", ")
  ])
);
```

## Core Insight

The system is conservative: energy in equals energy out. Context consumed in one session crystallizes into knowledge that makes the next session more effective. The equilibrium is not metaphor — it is architecture. Budgets enforce it. Crystallization maintains it. The forensic layer proves it was always so.
