---
title: "swarmy-ui ↔ faerie2 — Term Comparison"
subtitle: "A term-by-term comparison of two halves of one system"
investigation_label: glossary-merge
mission: swarmy-faerie-vocabulary-alignment
lane: 1
agent: documentation-engineer
task_id: comparison-2026-05-25-swarmy-ui-faerie2
date: 2026-05-25
status: draft
compass_edge: E
next_task_queued: architectural-merge-plan-businesss-vps
quality_score: 0.82
belief_index: 0.85
tags:
  - glossary
  - comparison
  - swarmy-ui
  - faerie2
  - vocabulary
  - merge-planning
sources:
  - swarmy-ui/docs/COMPARISON.md
  - swarmy-ui/docs/GLOSSARY.md
  - swarmy-ui/CLAUDE.md
  - faerie2/citations/glossary/02-CANONICAL-GLOSSARY.md
  - faerie2/CLAUDE.md
artifacts:
  pdf: ./comparison.pdf
  diagrams: ./diagrams/
related:
  - swarmy-ui/docs/GLOSSARY.md
  - faerie2/citations/glossary/02-CANONICAL-GLOSSARY.md
dashboard_machine_readable:
  aligned_terms: 8
  partial_overlap_terms: 7
  swarmy_ui_only_terms: 9
  faerie2_only_terms: 12
  hierarchy: "expedition ⊇ flight ⊇ mission ⊇ batch ⊇ worker_task"
  key_tensions:
    - term: crystallize
      severity: medium
      recommendation: "adopt swarmy-ui's tight definition"
    - term: honey_scope
      severity: low
      recommendation: "disambiguate per-flight vs system-wide"
    - term: nectar_scope
      severity: low
      recommendation: "disambiguate per-flight vs system-wide"
  merge_actions:
    keep_separate:
      - compass_bearings_nsew
      - cognitive_archetypes
      - mutation_discipline
      - ffmx
      - genotype_fitness
      - worker_role_taxonomy
    port_upstream:
      - flight
      - cap_uncapped_state_machine
      - ambrosia_name
    port_downstream:
      - charter
      - mission_graph_dag
      - rap
      - reputation
---

# What each repo is, in one line

- **swarmy-ui** — user-facing UI layer. Beekeeping metaphor is the *product mental model*; 9 named worker roles, 4 substances, hive / apiary / comb / cell as visible structures.
- **faerie2** — internal orchestration substrate. Beekeeping metaphor is *operational shorthand*; 4 cognitive archetypes routed by compass bearings, mission-graph DAG, forensics + COC chain, mutation discipline.

Different layers of the same stack: swarmy-ui is the **show**, faerie2 is the **engine room**. Most divergence is "swarmy-ui has no analog" or "faerie2 has no analog" rather than head-to-head conflict.

![Layer architecture](diagrams/01-layers.png)

# The scale hierarchy

The two repos have *nested* dispatch concepts. They sound like rivals only because the relationship was never written down.

![Scale hierarchy](diagrams/02-hierarchy.png)

`expedition ⊇ flight ⊇ mission ⊇ batch ⊇ worker_task`

# Term overlap at a glance

![Term overlap](diagrams/04-overlap.png)

---

## Aligned — same term, same meaning {#aligned}

| Term | swarmy-ui | faerie2 | Notes |
|:---|:---|:---|:---|
| **Mission** | Project goal in `swarm/mission.md`; queen re-emits when swarm drifts | Primary semantic routing unit in manifests; clusters related work | Identical load-bearing concept |
| **Queen** | Holds mission; doesn't execute; one per hive | Queen announces bearing decision via signal file; never polls | Same role, different surface |
| **Stigmergy** | Coordination emerges without messages | No SendMessage. Ever. Stigmergic routing via filesystem | Same principle, identically named |
| **Manifest** | Structured JSON output from one completed worker | Carries `mission`, `dashboard_line`, `next_mission_node`, `discovered_work[]` | Identical contract |
| **Discovered work** | Cells the swarm wants to fill next | `discovered_work[]` drives emergent mission formation | Same field, same semantics |
| **COC** | Append-only, hash-linked log | Hash-chained in `{repo}/forensics/` with full provenance | Identical architecture |
| **HONEY** | Final user-facing artifact crystallized from capped ambrosia | Crystallized memory + invariants — `HONEY.md` | Aligned but at different altitudes |
| **NECTAR** | Raw unstructured source material | Observation → pollen → promotion flow | Same metaphor, different scope |

## Partial overlap — shared term, drifted meaning {#partial}

| Term | swarmy-ui | faerie2 | Drift |
|:---|:---|:---|:---|
| **Flight** | One user-initiated arc, mission-start → finalized honey | Closest match is **Expedition** — 9+ missions cluster | Same family, **different scale** |
| **Crystallize** | Reserved verb: many capped cells → one honey artifact | Used loosely as `canon-crystallization` skill | swarmy-ui has stricter semantics |
| **Cap / Capped** | Reviewer's exclusive verb; binary state | RAP (Retroactive Anchor Promotion) | Same intent, different mechanism |
| **Batch** | One internal wave of workers; not user-facing | W1/W2/W3 piston waves | Same concept; UI avoids piston metaphor |
| **Ambrosia** | Intermediate work product packed in cells | Not a top-level concept; closest is `forensics/ephemeral/` | swarmy-ui formalized this |
| **Comb** | Visual substrate; hex-cell grid | `COMB.md` — repo map, deploy status | Genuinely different |
| **Worker / Bee** | 9 named roles, self-selected at runtime | Generic "agent" with archetype tag | swarmy-ui has rich taxonomy |

## swarmy-ui only {#swarmy-ui-only}

| Term | Meaning |
|:---|:---|
| **Guard · Scout · Forager · Prober · Mason · Cartographer · Reviewer · Crystallizer** | Named worker roles with apiculture pairings |
| **Pollen** | Structured / atomic source material (separate from nectar) |
| **Hive** | One kind of work (FlowSearch / Survey / Investigate / Build) |
| **Apiary** | Top-level container; multiple hives |
| **Cell / Capped cell / Uncapped cell** | Atomic storage unit + state |
| **Waggle, Pack, Ripen, Forage, Swarm in** | Verbs for coordination events |
| **Hive philosophy (HIVE.md)** | Per-hive decomposition + crystallization guidance |
| **Project types** | FlowSearch / DPA / Investigation / Build |
| **Fill level** | Visual property (0–1) separate from capped state |

## faerie2 only — kept internal {#faerie2-only}

| Term | Meaning |
|:---|:---|
| **Compass bearings N/S/E/W** | Routing edges in mission graph |
| **NAVIGATOR / MAKER / BRIDGE / DEEP-DIVER** | 4 cognitive archetypes |
| **f(0)** | "Queen burden ≈ 0" north-star metric |
| **Charter** | Formal mission declaration |
| **RAP** | Retroactive Anchor Promotion |
| **Reputation** | Agent quality score |
| **Mission-graph DAG** | Bearing-edge navigation |
| **Piston waves (W1/W2/W3)** | Wave dispatch with context-pressure sigmoid |
| **Mutation discipline** | Measure → pause → fix → measure → publish |
| **FFMx** | Force multiplier index |
| **Genotype-fitness** | Variants compete on fitness |
| **Four shields / Four bulkheads** | Defense-in-depth |

## Substance flow {#substance-flow}

![Substance chain](diagrams/03-substance-chain.png)

## Merge implications {#merge-implications}

![Merge flows](diagrams/05-merge-flows.png)

### Keep separate (working as intended)

- N/S/E/W compass and the four archetypes stay inside faerie2
- Mutation discipline, FFMx, genotype-fitness, piston waves
- swarmy-ui's nine worker roles stay inside swarmy-ui

### Align (would reduce drift)

- **Crystallize** — pick the tight definition (swarmy-ui's)
- **HONEY scope** — disambiguate per-flight vs system-wide
- **NECTAR scope** — same pattern
- **Scale hierarchy** — write down `expedition ⊇ flight ⊇ mission ⊇ batch ⊇ task`

### Port upstream (swarmy-ui → faerie2)

- **Flight** as the named mid-level unit
- **Cap / Uncapped** as a clean binary state machine
- **Ambrosia** as the name for ephemeral artifacts

### Port downstream (faerie2 → swarmy-ui future phases)

- **Charter** as the formal mission declaration
- **Mission-graph DAG** with bearing-edge navigation
- **RAP** as an additional durability signal
- **Reputation** as a worker-quality metric

---

## Companion artifact

- **PDF (typeset):** [`comparison.pdf`](./comparison.pdf)
- **Diagram sources:** `./diagrams/*.mmd` (Mermaid)
- **Diagram renders:** `./diagrams/*.png` (mermaid.ink)
- **Skill that built this:** `faerie2/.agents/skills/pdf/`
