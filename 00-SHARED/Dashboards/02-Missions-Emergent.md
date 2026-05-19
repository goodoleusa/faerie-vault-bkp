---
type: dashboard
tier: emergent
title: "Missions — Emergent Clusters (30d)"
status: live
derived_from:
  - "CyberOps-UNIFIED/00-SHARED/Dashboards/system/metrics-dashboard-20260425.md"
tags: [dashboard, missions, emergent]
---

# Missions — Emergent Clusters

Distinct `cluster_prefix` across the last 30 days where ≥2 manifests share the prefix.
Click through to see all manifests in that cluster.

```dataview
TABLE WITHOUT ID
  cluster_prefix AS "Cluster",
  length(rows) AS "Manifests",
  length(filter(rows.bearing, (b) => b = "N")) AS "N",
  length(filter(rows.bearing, (b) => b = "S")) AS "S",
  length(filter(rows.bearing, (b) => b = "E")) AS "E",
  length(filter(rows.bearing, (b) => b = "W")) AS "W",
  dateformat(max(rows.file.mtime), "MMM dd") AS "Latest"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today) - dur(30 days) AND cluster_prefix
GROUP BY cluster_prefix
WHERE length(rows) >= 2
SORT length(rows) DESC
```

## Distinct missions (last 30d, all sizes)

```dataview
TABLE WITHOUT ID
  mission AS "Mission",
  length(rows) AS "Count"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today) - dur(30 days) AND mission
GROUP BY mission
SORT length(rows) DESC
LIMIT 30
```
