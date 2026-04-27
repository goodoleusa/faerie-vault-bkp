---
type: dashboard
stage: review
tags: [dashboard, stubs, entity-review]
parent:
  - "[[HOME]]"
sibling:
  - "[[Annotation-Dash]]"
  - "[[Agent-Insights]]"
  - "[[Chain-of-Custody]]"
doc_hash: sha256:d025d830be1a179e346d9c5bd7f5c2145c41e647937933792fc0e764b9a4a17b
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Annotation-Dash|← Annotate]] · **Unprocessed Stubs** · [[Phase1-AgentSync|Investigation →]]

# Unprocessed Stubs

## Needs Review
```dataview
TABLE status, type, entity_type, confidence_level, created
FROM "20-Entities" or "30-Evidence"
WHERE status = "stub" OR status = "needs-review" OR needs_processing = true
SORT created ASC
```

## By Entity Type
```dataview
TABLE entity_type, confidence_level, priority
FROM "20-Entities"
WHERE status = "stub"
GROUP BY entity_type
```

## Overdue Reviews
```dataview
TABLE next_review, entity_name, priority
FROM "20-Entities"
WHERE next_review AND date(next_review) < date(today)
SORT next_review ASC
```

## Processing Progress
```dataview
TABLE length(rows) AS "Count"
FROM "20-Entities" or "30-Evidence"
WHERE contains(tags, "osint")
GROUP BY status
```
