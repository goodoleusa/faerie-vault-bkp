---
type: dashboard
tier: stigmergy
title: "Stigmergy — discovered_work flow & cross-citation"
status: live
N: '[00-Home](00-Home.md)'
E: ['[01-Today](01-Today.md)', '[02-Missions-Emergent](02-Missions-Emergent.md)', '[03-Anchors](03-Anchors.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)']
W: '[00-Home](00-Home.md)'
tags: [dashboard, stigmergy, compass]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Stigmergy

`discovered_work[]` flow visualization: which agents cited which, cross-citation rate,
bearing distribution N/S/E/W.

## Bearing distribution (last 7d)

```dataview
TABLE WITHOUT ID
  bearing AS "Bearing",
  length(rows) AS "Count"
FROM "00-SHARED/session-manifests"
WHERE file.cday >= date(today) - dur(7 days)
GROUP BY bearing
```
