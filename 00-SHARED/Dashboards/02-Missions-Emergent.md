---
type: dashboard
tier: emergent
title: "Missions — Emergent Clusters (30d)"
status: live
N: '[00-Home](00-Home.md)'
E: ['[01-Today](01-Today.md)', '[03-Anchors](03-Anchors.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)', '[05-Stigmergy](05-Stigmergy.md)']
W: '[00-Home](00-Home.md)'
tags: [dashboard, missions, emergent]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Missions — Emergent Clusters

Distinct `cluster_prefix` across the last 30 days where ≥2 manifests share the prefix.

```dataview
TABLE WITHOUT ID
  cluster_prefix AS "Cluster",
  length(rows) AS "Manifests"
FROM "00-SHARED/session-manifests"
WHERE file.cday >= date(today) - dur(30 days)
GROUP BY cluster_prefix
WHERE length(rows) >= 2
SORT length(rows) DESC
```
