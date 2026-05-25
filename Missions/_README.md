---
type: readme
pseudosystem_folder: Missions
canonical_repo_path: "forensics/mission-graph.json"
tags: [readme, pseudosystem]
---

# Missions — Pseudosystem README

## What This Folder Is

`Missions/` contains vault dossiers for missions tracked in `forensics/mission-graph.json`. A mission is the semantic routing unit — the `mission` field in manifests clusters work into coherent streams. Each note here is the operator's navigable history of one mission: which charters carry it, what manifests have been sealed under it, what open work remains.

## What This Folder Is NOT

- Not the canonical mission registry (that's `forensics/mission-graph.json`)
- Not a task queue (the compass bearing DAG in the repo is the routing substrate)
- Not exhaustive — 112 missions exist; vault notes cover the top 20 by open-work activity

## When to Create a Mission Note

When a new mission has accumulated 3+ manifests and you want a navigable dossier, use `Mission.blueprint` to create a note in this folder. Name the file `{mission-id}.md` (exact match to the `mission` field in manifests).

## Mission Lifecycle

1. **Emergence** — Mission ID appears in a manifest's `mission` field
2. **Growth** — Manifests accumulate; `mission-graph.py` tracks task_count, bearings, charter linkage
3. **Active** — Charters carry the mission; agents claim work via bearing edges
4. **Dormant** — No new manifests for 7+ days; shape `charter.stale.no_progress` fires
5. **Complete** — All bearing edges resolved; mission removed from open_work_missions

## Navigation

- Start at `_MOC.md` for the table of top missions
- Each mission note links back to `[[Charters/]]` notes that carry it
- Each mission note links forward to `[[Manifests/]]` notes that sealed under it

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root.*
