---
type: dashboard
tier: daily
title: "Today — Manifests by Mission Cluster"
status: live
cssclasses: [wide-page]
N: '[00-Home](00-Home.md)'
E: ['[02-Missions-Emergent](02-Missions-Emergent.md)', '[03-Anchors](03-Anchors.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)', '[05-Stigmergy](05-Stigmergy.md)']
W: '[00-Home](00-Home.md)'
tags: [dashboard, daily]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Today — Manifests by Mission Cluster

Today's manifests grouped by `cluster_prefix` (first 3 w4w slots per dead-reckoning ontology).
Each row shows trail summary + displacement + alignment.

```dataview
TABLE WITHOUT ID
  file.link AS "Manifest",
  cluster_prefix AS "Cluster",
  bearing AS "Bearing",
  trail_summary AS "Trail"
FROM "00-SHARED/session-manifests"
WHERE file.cday = date(today)
SORT cluster_prefix ASC
```
