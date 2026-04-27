---
type: index
tags: [index, queue, dataview]
parent: "[[INDEX]]"
up: "[[00-SHARED/Queue/_index|Queue]]"
sibling:
  - "[[AGENT-INDEX]]"
  - "[[MEMORY-INDEX]]"
  - "[[DASHBOARD-INDEX]]"
status: active
doc_hash: sha256:cb5ec71d122efdb0713940b7579dd873f32b25219b7b663ad2dc2be2743409ab
hash_ts: 2026-04-07T02:49:17Z
hash_method: body-sha256-v1
---

> [[HOME]] > [[INDEX|00-META]] > **Queue**

# Queue Index

Active tasks by priority. Archived tasks excluded.

```dataview
TABLE status, priority, file.link as "Task"
FROM "00-SHARED/Queue"
WHERE status != "archived" AND file.name != "_index"
SORT choice(priority = "HIGH", 0, choice(priority = "MED", 1, 2)) ASC, file.mtime DESC
```

---

## Sprint Board

```dataview
TABLE WITHOUT ID
  file.link AS "Item",
  status AS "Status",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Updated"
FROM "00-SHARED/Queue"
WHERE file.name != "_index"
SORT file.mtime DESC
LIMIT 15
```

---

*[[00-SHARED/Queue/_index|Browse Queue]] · [[00-SHARED/Queue/sprint-queue|Sprint Queue]] · [[INDEX|Back to Meta]]*
