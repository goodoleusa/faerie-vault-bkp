---
type: dashboard
tier: anchors
title: "Anchors — Proposed / Promoted / Rejected"
status: live
derived_from:
  - "CyberOps-UNIFIED/00-SHARED/Dashboards/.claude-garbage-Mission-Control.md"
tags: [dashboard, anchors, governance]
---

# Anchors

All anchors with status (proposed/promoted/rejected) and the system-prompt patch they suggest.

```dataview
TABLE WITHOUT ID
  file.link AS "Anchor",
  status AS "Status",
  mission AS "Mission",
  suggested_patch AS "Patch"
FROM #anchor
SORT status ASC, file.mtime DESC
```

## Promoted (active in system prompt)

```dataview
LIST file.link + " — " + default(suggested_patch, "(no patch text)")
FROM #anchor
WHERE status = "promoted"
SORT file.mtime DESC
```

## Awaiting review

```dataview
LIST file.link + " — proposed " + dateformat(file.mtime, "MMM dd")
FROM #anchor
WHERE status = "proposed"
SORT file.mtime ASC
```

## Rejected (kept for audit)

```dataview
LIST file.link + " — " + default(rejection_reason, "(no reason)")
FROM #anchor
WHERE status = "rejected"
```
