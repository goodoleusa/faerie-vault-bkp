---
type: index
tags: [index, memories, knowledge-base]
parent: "[[HOME]]"
sibling:
  - "[[00-SHARED/00-SHARED|00-SHARED]]"
child:
  - "[[agents/KNOWLEDGE-BASE|Agent Knowledge Base]]"
  - "[[00-META/MEMORY-INDEX|Memory Index]]"
status: active
doc_hash: sha256:c7c6079116728a6875fbd7b9af1eab6485f617f3f1e64bdfe3ce3543078ab1c4
hash_ts: 2026-04-07T02:51:18Z
hash_method: body-sha256-v1
---

> [[HOME]] > **01-Memories**

# Memories

Knowledge base and collected memory layers.

| Location | Purpose |
|----------|---------|
| [[agents/KNOWLEDGE-BASE]] | Validated cross-session facts (synced from NECTAR) |
| [[00-META/MEMORY-INDEX]] | Dataview index — all memory files by recency |

---

```dataview
TABLE file.mtime as "Updated", file.tags as "Tags"
FROM "01-Memories"
WHERE file.name != "_index"
SORT file.mtime DESC
LIMIT 15
```

---

*[[HOME]] · [[00-SHARED/00-SHARED|00-SHARED]] · [[00-META/MEMORY-INDEX|Full Memory Index]]*
