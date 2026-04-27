---
type: index
tags: [index, dashboards, dataview]
parent: "[[INDEX]]"
up: "[[00-SHARED/Dashboards/_index|Dashboards]]"
sibling:
  - "[[AGENT-INDEX]]"
  - "[[QUEUE-INDEX]]"
  - "[[MEMORY-INDEX]]"
status: active
doc_hash: sha256:1b3fd8832000f66df92af964f44b67e3fcb868a74fefdd88422b1b9a32e6cbbd
hash_ts: 2026-04-07T02:49:32Z
hash_method: body-sha256-v1
---

> [[HOME]] > [[INDEX|00-META]] > **Dashboards**

# Dashboard Index

All dashboards ordered by last refresh.

```dataview
TABLE file.mtime as "Last Refresh", default(status, "—") AS "Status"
FROM "00-SHARED/Dashboards"
WHERE (type = "dashboard" OR type = "kanban") AND file.name != "_index"
SORT file.mtime DESC
```

---

## Session Briefs

```dataview
TABLE WITHOUT ID
  file.link AS "Brief",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Generated"
FROM "00-SHARED/Dashboards/session-briefs"
SORT file.name DESC
LIMIT 10
```

---

## All Dashboard Files (by folder)

```dataview
TABLE WITHOUT ID
  file.folder AS "Folder",
  length(rows) AS "Files",
  dateformat(max(rows.file.mtime), "MMM dd HH:mm") AS "Latest"
FROM "00-SHARED/Dashboards"
WHERE file.name != "_index"
GROUP BY file.folder
SORT max(rows.file.mtime) DESC
```

---

*[[00-SHARED/Dashboards/_index|Dashboards Hub]] · [[HOME]] · [[INDEX|Back to Meta]]*
