---
type: dashboard
tags: [dashboard, home]
cssclass: wide-page
doc_hash: sha256:9516a13bd0b5e81f5c3d4aaf4d7e795a2ccc0760511e42e6f86142e5184ed451
hash_ts: 2026-04-07T02:50:57Z
hash_method: body-sha256-v1
child:
  - "[[00-SHARED/00-SHARED|00-SHARED]]"
  - "[[01-Memories/_index|01-Memories]]"
  - "[[00-Inbox]]"
  - "[[01-PROTECTED]]"
---

# CyberOps — Command Center

> [!note] Data Visualization Guide
> For visualization work on the investigation: **[[../../../0LOCAL/gitrepos/cybertemplate/docs/UI-DATA-GUIDE|UI-DATA-GUIDE]]** — D3 v7, Observable Plot, hypothesis data, evidence schema.

> **Nav:** [[00-SHARED/00-SHARED|00-SHARED]] | [[01-Memories/_index|01-Memories]] | [[00-Inbox]] | [[00-SHARED/Agent-Inbox|Agent-Inbox]] | [[00-SHARED/Queue/sprint-queue|Sprint Queue]]

## Live Indexes
- [[00-SHARED/00-META/AGENT-INDEX|Agent Outputs]] — last 20 agent writes
- [[00-SHARED/00-META/QUEUE-INDEX|Queue]] — active tasks by priority
- [[00-SHARED/00-META/DASHBOARD-INDEX|Dashboards]] — all live dashboards
- [[01-Memories/00-META/MEMORY-INDEX|Memory]] — recent observations

## Zones
| Zone | Purpose | Access |
|------|---------|--------|
| [[00-SHARED/00-SHARED\|00-SHARED]] | Agent-human exchange | Both |
| [[01-Memories/_index\|01-Memories]] | Knowledge base | Both |
| [[00-Inbox]] | Human quicknotes + incoming tasks | Human writes |
| [[01-PROTECTED]] | Court exhibits | Human only |

---

> *Async collaboration hub. Offline-first. Full data sovereignty.*
> *Agents write here. You annotate. USB and Syncthing carry the rest.*

---

## 🔴 Annotate These — Tier 1, Unannotated

```dataview
TABLE tier, confidence_level, source_type, date_collected, pipeline_run
FROM "30-Evidence"
WHERE tier = 1 AND (ann_hash = null OR ann_hash = "")
SORT confidence_level DESC
LIMIT 8
```

---

## 📬 Unread Drops

```dataview
TABLE drop_type, from, priority, file.ctime AS "Received"
FROM "00-Inbox/drops"
WHERE read = false
SORT priority ASC, file.ctime DESC
```

---

## ⏳ Waiting for You

### Tasks Completed — Need Review
```dataview
TABLE assignee AS "Agent", priority, completed_date
FROM "00-Inbox/tasks"
WHERE status = "awaiting-human" OR status = "completed"
SORT completed_date DESC
LIMIT 6
```

### Threads — Your Turn
```dataview
TABLE thread_title, started_by, updated
FROM ""
WHERE type = "thread" AND contains(needs_response_from, "human")
SORT updated DESC
LIMIT 5
```

---

## ⚡ Agent Activity

```dataview
TABLE status, priority, skill_required, assignee
FROM "00-Inbox/tasks"
WHERE status = "claimed" OR status = "in-progress"
SORT priority ASC
```

---

## 📊 Annotation Progress

```dataview
TABLE WITHOUT ID
  rows.tier AS "Tier",
  length(rows) AS "Total",
  length(filter(rows, (r) => r.ann_hash != null AND r.ann_hash != "")) AS "Annotated"
FROM "30-Evidence"
GROUP BY tier
SORT tier ASC
```

---

## 📊 Dashboards

| Dashboard | Purpose |
|---|---|
| [[00-SHARED/Dashboards/Dashboards/Mission-Control]] | Cross-session agent+human intel hub |
| [[00-SHARED/Dashboards/Dashboards/Nectar-View]] | NECTAR findings — sortable by hypothesis/confidence/run |
| [[00-SHARED/Dashboards/Dashboards/Data-Ingest-Pipeline]] | Run tracker — phases, blockers, remaining runs |

---

## 🔗 Quick Actions

| Action | Blueprint | Where to Save |
|--------|-----------|---------------|
| Daily briefing | [[Research-Brief.blueprint]] | `01-Memories/` |
| Post task for agent | [[Task-Inbox.blueprint]] | `00-Inbox/tasks/` |
| Leave agent a message | [[Dead-Drop.blueprint]] | `00-Inbox/drops/` |
| Start a research thread | [[Thread.blueprint]] | `00-Inbox/` |
| Add annotation section to any note | [[Annotation-Commit.blueprint]] | *(apply to existing)* |
| Package for offline reviewer | [[Observer-Drop.blueprint]] | `00-Inbox/observer/` |
| Share with partner team | [[Collab-Export.blueprint]] | `00-Inbox/collab/` |
| New evidence note | [[Evidence-Item.blueprint]] | `30-Evidence/` |
| New entity | [[Entity-Stub.blueprint]] | `20-Entities/` |
| New investigation | [[Investigation-Case.blueprint]] | `10-Investigations/` |

> `Ctrl+P` → "Apply Blueprint" — works on new notes AND existing ones.

---

## 🗓 Recent Activity

```dataview
TABLE type, status, promotion_state, file.mtime AS "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(2 day) AND type != "index" AND type != "dashboard"
SORT file.mtime DESC
LIMIT 12
```

---

## 💾 Memory Layer (Optional — Deeper Insights)

```dataview
TABLE promotion_state, memory_lane, file.mtime AS "Updated"
FROM ""
WHERE promotion_state = "capture" AND memory_lane != null
  AND memory_lane != "drops" AND memory_lane != "queue"
SORT file.mtime DESC
LIMIT 8
```

> **Promote a finding**: set `promotion_state: promoted` → membot picks it up at session end
> **Crystallize to HONEY**: set `promotion_state: crystallized` → seeds future agent sessions
> **Cite without sharing**: set `memory_lane: honey` → "confirmed in vault, [date]"
