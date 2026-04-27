---
type: index
tags: [index, memory, dataview]
parent: "[[01-Memories/_index|01-Memories]]"
up: "[[HOME]]"
sibling:
  - "[[00-SHARED/00-META/AGENT-INDEX|Agent Index]]"
  - "[[00-SHARED/00-META/QUEUE-INDEX|Queue Index]]"
  - "[[00-SHARED/00-META/DASHBOARD-INDEX|Dashboard Index]]"
status: active
doc_hash: sha256:badbea84ee592e173a561ab94543e553d705a9d10f15cc39266910cddb82ff36
hash_ts: 2026-04-07T02:49:23Z
hash_method: body-sha256-v1
---

> [[HOME]] > **01-Memories** > **Memory Index**

# Memory Index

Recent memory entries across all memory layers, most recently updated first.

```dataview
TABLE file.mtime as "Updated", file.tags as "Tags"
FROM "01-Memories"
WHERE file.name != "_index"
SORT file.mtime DESC
LIMIT 30
```

---

## Agent Knowledge Base

```dataview
TABLE WITHOUT ID
  file.link AS "File",
  dateformat(file.mtime, "MMM dd HH:mm") AS "Updated",
  file.size AS "Size"
FROM "01-Memories/agents"
WHERE file.name != "_index"
SORT file.mtime DESC
```

---

## By Subfolder

```dataview
TABLE WITHOUT ID
  file.folder AS "Folder",
  length(rows) AS "Files",
  dateformat(max(rows.file.mtime), "MMM dd HH:mm") AS "Latest"
FROM "01-Memories"
WHERE file.name != "_index"
GROUP BY file.folder
SORT max(rows.file.mtime) DESC
```

---

*[[01-Memories/agents/KNOWLEDGE-BASE|Knowledge Base]] · [[00-SHARED/00-META/INDEX|00-META]] · [[HOME]]*
