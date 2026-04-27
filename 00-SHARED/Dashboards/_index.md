---
type: index
status: active
cssclasses:
  - wide-page
  - dashboard-home
tags: [dashboard, index, command-center]
parent:
  - "[[00-SHARED/00-SHARED|00-SHARED]]"
sibling:
  - "[[00-SHARED/Human-Inbox/_index|Human Inbox]]"
  - "[[00-SHARED/Queue/_index|Queue]]"
  - "[[00-SHARED/Agent-Outbox/_index|Agent Outbox]]"
child:
  - "[[HOME]]"
doc_hash: sha256:d15d2e473d3319e201f7a4f9b6633ee7b111f0d479cd97851997d43e40ddca99
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|HOME]] · **All Dashboards** · [[00-SHARED/Hive/SYSTEM-GUIDE|System Guide]] · [[00-SHARED/Hive/_index|Hive]] · [[00-SHARED/Queue/_index|Queue]]

# Dashboard Command Center

Start at [[HOME]] for the investigation. Come here for everything else.

---

## Investigation Dashboards

> [!abstract]- Investigate (Phase 1 — agent-driven)
> | Dashboard | Purpose |
> |---|---|
> | [[Phase1-AgentSync]] | Command center — agent queue, findings, gaps |
> | [[Hypothesis-Tracker]] | Per-hypothesis evidence + confidence over time |
> | [[Pipeline-Gates]] | Scientific rigor gates for /data-ingest |
> | [[Data-Ingest-Pipeline]] | Pipeline run tracker — raw data to curated evidence |

> [!check]- Review (human annotation & promotion)
> | Dashboard | Purpose |
> |---|---|
> | [[Annotation-Dash]] | Smoking guns, court prep, your annotation space |
> | [[Agent-Insights]] | 24h agent insight feed — validate & promote |
> | [[Chain-of-Custody]] | Forensic audit trail — what you signed, when |
> | [[Unprocessed-Stubs]] | Entity stubs and evidence needing review |

> [!tip]- Publish (Phase 2 — writing)
> | Dashboard | Purpose |
> |---|---|
> | [[Phase2-Publication]] | Section editing, website mirror, pre-publish checklist |

---

## System Dashboards

> [!gear]- System Architecture & Design
> | Dashboard | Purpose |
> |---|---|
> | [[System-Architecture]] | Full system architecture — 10 Mermaid diagrams |
> | [[00-SHARED/Hive/SYSTEM-GUIDE\|System Guide]] | Clickable learning guide to every component |
> | [[00-SHARED/Hive/15-MODULAR-SECRET-SAUCE\|Modular Architecture]] | Secret sauce: paid tier vs open build |
> | [[00-SHARED/Hive/PISTON-MODEL-DESIGN\|Piston Model]] | Three-speed agent wave engine |
> | [[Session-Manifests]] | Cross-repo session manifests |
> | [[Nectar-View]] | NECTAR finding explorer |

---

## Live Feeds

### Recently Modified Dashboards

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Dashboard",
  type AS "Type",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Modified"
FROM "00-SHARED/Dashboards"
WHERE type = "dashboard" OR type = "kanban"
SORT file.mtime DESC
LIMIT 10
```

### Latest Session Briefs

```dataview
TABLE WITHOUT ID
  link(file.link, regexreplace(file.name, "brief", "")) AS "Brief",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Time"
FROM "00-SHARED/Dashboards/session-briefs"
SORT file.name DESC
LIMIT 8
```

### Recent Droplets (pre-compact captures)

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Droplet",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Captured"
FROM "00-SHARED/Dashboards/Droplets"
WHERE file.name != "_index"
SORT file.mtime DESC
LIMIT 5
```

### Recent Condensation

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Condensation",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Crystallized"
FROM "00-SHARED/Dashboards/condensation"
SORT file.mtime DESC
LIMIT 5
```

---

## All Dashboards (auto-populated)

Every file in this folder tree with `type: dashboard` or `type: kanban`:

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Dashboard",
  type AS "Type",
  default(status, "—") AS "Status",
  join(file.tags, ", ") AS "Tags"
FROM "00-SHARED/Dashboards"
WHERE (type = "dashboard" OR type = "kanban") AND file.name != "_index"
SORT file.folder ASC, file.name ASC
```

---

## Design Docs (Hive)

System design, architecture narratives, and the pseudosystem component library:

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Doc",
  type AS "Type",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Modified"
FROM "00-SHARED/Hive"
WHERE (type = "system-design" OR type = "design-narrative" OR type = "system-guide" OR type = "narrative")
  AND file.name != "_index"
SORT file.mtime DESC
LIMIT 10
```

---

## Folder Map

| Folder | What's in it | Count |
|--------|-------------|-------|
| `investigate/` | Phase 1 agent-driven dashboards | 4 |
| `review/` | Human annotation + promotion | 4 |
| `publish/` | Phase 2 writing dashboards | 1 |
| `system/` | Architecture, manifests, NECTAR view | 3 |
| `session-briefs/` | Auto-generated session state snapshots | ~90 |
| `Droplets/` | Real-time captures before auto-compact | live |
| `condensation/` | Stream-of-consciousness crystallization | live |

---

*[[HOME|HOME]] · [[00-SHARED/Hive/_index|Hive (design hub)]] · [[00-SHARED/Hive/SYSTEM-GUIDE|System Guide]] · [[00-SHARED/00-SHARED|00-SHARED]]*
