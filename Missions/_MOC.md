---
type: moc
title: Missions — Map of Content
pseudosystem_folder: Missions
canonical_repo_path: "forensics/mission-graph.json"
tags: [moc, mission, pseudosystem]
updated: "2026-05-25"
graph_stats: "112 total missions, 265 manifests in corpus, bearings: S:120 / N:11 / E:10 / W:8"
---

# Missions — Map of Content

> Vault pseudosystem dossiers for missions in `forensics/mission-graph.json`.
> 112 total missions tracked; top 20 open-work missions have full dossier notes here.
> **Canonical source:** `forensics/mission-graph.json` — vault notes are operator-navigable summaries.

---

## Mission Graph Stats (2026-05-25)

| Metric | Value |
|--------|-------|
| Total missions | 112 |
| Corpus size (manifests) | 265 |
| Open work missions | ~60 |
| Bearing distribution | S:120, N:11, E:10, W:8 |
| COC edges | 10 |
| Branch merge edges | 2 |
| Discovered edges | 527 |

---

## Top 20 Open-Work Mission Dossiers

| Mission | Charter(s) |
|---------|------------|
| [[agent-signing-discipline]] | — |
| [[agent.agency.citation-and-coc-chain-discipline.schema-lock]] | — |
| [[agent.agency.completion-ritual.three-families.thirteen-kinds]] | — |
| [[agent.lifecycle.signing-enforcement]] | — |
| [[bulkheads.implementation.cuts]] | — |
| [[charter-schema-compliance]] | — |
| [[collapse-the-sprawl]] | — |
| [[consolidation.fold.cut]] | — |
| [[creatures.agency.bonds]] | — |
| [[crystallization.momentum.loop]] | — |
| [[discipline.stack.completion]] | — |
| [[doc-crystallization-faerie2]] | — |
| [[documentation-infrastructure]] | — |
| [[documentation.platform-narrative.crystallization]] | — |
| [[emergence-health-regression-diagnosis]] | — |
| [[enterprise.patent.foundation]] | — |
| [[faerie-architecture-optimization]] | — |
| [[faerie-observability-enhancement]] | — |
| [[harness-coc-mission-graph-eval-metrics]] | — |
| [[hive-pair-coding-foundation]] | [[hive-pair-coding-foundation]] |

---

## Mission Naming Grammar

Mission IDs follow a 3-term cluster prefix: `{domain}.{subject}.{mode}` or a hyphenated form. The mission field in manifests is the canonical routing unit (not `investigation_label`).

## How Missions Are Created

Missions emerge from manifests — when an agent writes a manifest with a new `mission` field value, the mission graph absorbs it on next `mission_graph.py` run. Missions are never manually created; they are discovered from manifest data.

---

## Dataview Query

```dataview
TABLE task_count, last_ts, charter_ids
FROM "Missions"
WHERE type = "mission"
SORT task_count DESC
LIMIT 20
```

---

*Canonical mission graph: `forensics/mission-graph.json`. Schema version 4.*
