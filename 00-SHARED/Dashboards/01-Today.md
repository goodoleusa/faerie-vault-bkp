---
type: dashboard
tier: daily
title: "Today — Manifests by Mission Cluster"
status: live
cssclasses: [wide-page]
derived_from:
  - "CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-28/00-DASHBOARD.md"
  - "CyberOps-UNIFIED/00-SHARED/00-META/DASHBOARD-INDEX.md"
tags: [dashboard, daily]
---

# Today — Manifests by Mission Cluster

Today's manifests grouped by `cluster_prefix` (first 3 w4w slots per dead-reckoning ontology).
Each row shows trail summary + displacement + alignment.

> See [[00-Home]] for f(0) overview · [[02-Missions-Emergent]] for cross-day clusters.

---

## By cluster_prefix (today only)

```dataview
TABLE WITHOUT ID
  file.link AS "Manifest",
  bearing AS "→",
  displacement AS "Δ",
  alignment AS "Align",
  dashboard_line AS "Trail"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today)
GROUP BY cluster_prefix
SORT cluster_prefix ASC, file.mtime DESC
```

## Unclustered (no cluster_prefix field — legacy)

```dataview
LIST file.link + " — " + default(mission, "(no mission)")
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today) AND !cluster_prefix
SORT file.mtime DESC
LIMIT 20
```

## Bearing distribution (today)

```dataview
TABLE WITHOUT ID
  bearing AS "Bearing",
  length(rows) AS "Count"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today)
GROUP BY bearing
```
