---
type: dashboard
tier: anchors
title: "Anchors — Proposed / Promoted / Rejected"
status: live
N: '[00-Home](00-Home.md)'
E: ['[01-Today](01-Today.md)', '[02-Missions-Emergent](02-Missions-Emergent.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)', '[05-Stigmergy](05-Stigmergy.md)']
W: '[00-Home](00-Home.md)'
tags: [dashboard, anchors, governance]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Anchors

All anchors with status (proposed/promoted/rejected) and the system-prompt patch they suggest.

```dataview
TABLE WITHOUT ID
  file.link AS "Anchor",
  status AS "Status",
  mission AS "Mission",
  suggested_patch AS "Patch"
FROM #anchor
SORT status ASC
```
