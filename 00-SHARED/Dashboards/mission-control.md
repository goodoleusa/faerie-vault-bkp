---
type: dashboard
date: 2026-05-18
status: draft
promotion_state: capture
created: 2026-05-18T00:00:00Z
updated: 2026-05-18T00:00:00Z
tags:
  - faerie
  - mission-control
  - dashboard
  - mission-graph
parent: "[[00-SHARED/Dashboards]]"
blueprint: ""
source_path: forensics/mission-graph.json
source_hash: "sha256:"
cloud_path: ""
doc_hash: "sha256:"
hash_ts: 2026-05-18T00:00:00Z
hash_method: body-sha256-v1
promoted_to: ""
promoted_at: ""
---

# Mission Control

> Live view of the active mission graph. Missions are the primary routing unit — agents read `mission` fields and self-assign to frontier nodes.

---

## Active Missions

```dataview
TABLE bearing, status, length(tasks) AS "Tasks"
FROM "forensics/manifests"
WHERE type = "faerie-manifest" OR type = "manifest"
SORT date DESC
LIMIT 20
```

---

## Mission Graph Diagram

![[mission-graph.excalidraw.md]]

---

## Hive Status — Today's Agent Activity

```dataview
TABLE archetype, mission, status
FROM "00-SHARED/Daily"
WHERE date = date(today)
SORT file.mtime DESC
LIMIT 10
```

---

## Agent Continuation Choices

> What agents chose to do after their primary mission — and why.

![[agent-choices-report.md]]

---

> [!tip] Refresh
> Run `python3 scripts/9x_vault_sync.py sync --with-graph --with-choices` to pull today's manifests, update the diagram, and regenerate the choices report.

---

## Bearing Legend

> Bearing = **final vector course** — where the agent concluded, not where it started.

| Bearing | Colour | Meaning |
|---------|--------|---------|
| N | 🔵 Blue | Concluded by unblocking upstream — prerequisite resolved |
| S | 🟢 Green | Concluded by shipping — deliverable reached next milestone |
| E | 🟡 Yellow | Concluded in parallel — sister work at same DAG level |
| W | 🔴 Red | Concluded at baseline — re-validated assumptions, returned to HQ |
