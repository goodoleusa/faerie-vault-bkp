---
type: index
tags: [index, agent-outbox, dataview]
parent: "[[INDEX]]"
up: "[[00-SHARED/00-SHARED|00-SHARED]]"
sibling:
  - "[[QUEUE-INDEX]]"
  - "[[MEMORY-INDEX]]"
  - "[[DASHBOARD-INDEX]]"
status: active
doc_hash: sha256:ca51812beff730f570361d417cda0e84ac84002e23425297ca767bf98277e8af
hash_ts: 2026-04-07T02:49:09Z
hash_method: body-sha256-v1
---

> [[HOME]] > [[INDEX|00-META]] > **Agent Outputs**

# Agent Output Index

Last 20 files written to Agent-Outbox, most recent first.

```dataview
TABLE file.mtime as "Last Updated", file.size as "Size"
FROM "03-Agents"
WHERE file.name != "_index"
SORT file.mtime DESC
LIMIT 20
```

---

## By Subfolder

```dataview
TABLE WITHOUT ID
  file.folder AS "Folder",
  length(rows) AS "Files",
  dateformat(max(rows.file.mtime), "MMM dd HH:mm") AS "Latest"
FROM "00-SHARED/Agent-Outbox"
WHERE file.name != "_index"
GROUP BY file.folder
SORT max(rows.file.mtime) DESC
```

---

*[[00-SHARED/Agent-Outbox/_index|Browse Agent-Outbox]] · [[QUEUE-INDEX|Queue]] · [[INDEX|Back to Meta]]*
