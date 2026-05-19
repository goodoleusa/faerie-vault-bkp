---
type: dashboard
tier: home
title: "Faerie Home — f(0) Overview"
status: live
cssclasses: [wide-page, dashboard-home]
refresh_cadence: per-session
derived_from:
  - "CyberOps-UNIFIED/00-SHARED/Dashboards/01-SYSTEM-OVERVIEW.md"
  - "CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-04-28/00-DASHBOARD.md"
  - "faerie-vault/00-SHARED/templates/FFFF-dashboard-template.md"
tags: [dashboard, home, faerie]
---

# Faerie Home — f(0) Overview

> Sentence-trail summary of today's hive state. Mission clusters, recent anchors,
> eval dimension scores. FFFF structure: Findings · Flags · Friction · Flow.

Navigate: [[01-Today]] · [[02-Missions-Emergent]] · [[03-Anchors]] · [[04-Eval-Dimensions]] · [[05-Stigmergy]]

---

## Context Pressure Gauge

```
W1 LIFTOFF   [    ] ≤25% ctx — max burn, parallel spawns
W2 CRUISE    [    ] ≤65% ctx — autonomous dispatch
W3 INSERTION [    ] ≤95% ctx — deep synthesis, background
```

(Operator updates the bracket each session; auto-wiring TBD via `presend_estimate.py`.)

---

## Findings — What was discovered (last 24h)

```dataview
TABLE WITHOUT ID
  file.link AS "Manifest",
  mission AS "Mission",
  bearing AS "→",
  dashboard_line AS "Trail summary"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today) - dur(1 day)
SORT file.mtime DESC
LIMIT 15
```

## Flags — Needs attention

```dataview
LIST mission + " · " + dashboard_line
FROM "forensics/manifests"
WHERE contains(string(tags), "flag") OR priority = "HIGH"
SORT file.mtime DESC
LIMIT 8
```

## Friction — Blocked / discovered_work bearing=N

```dataview
TABLE WITHOUT ID
  file.link AS "Manifest",
  mission AS "Mission",
  rationale AS "Why blocked"
FROM "forensics/manifests"
WHERE bearing = "N"
SORT file.mtime DESC
LIMIT 10
```

## Flow — Concluded / shipped (bearing=S, last 7d)

```dataview
LIST mission + " — " + dashboard_line
FROM "forensics/manifests"
WHERE bearing = "S" AND date(file.mtime) >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```

---

## Recent Anchors

```dataview
TABLE status, suggested_patch AS "System-prompt patch"
FROM "forensics" AND #anchor
SORT file.mtime DESC
LIMIT 5
```

## Eval dimension snapshot (latest run)

See [[04-Eval-Dimensions]] for the trend tables. Latest composite + dim A-G live there.

---

## Today's mission clusters (cluster_prefix = first 3 w4w slots)

```dataview
TABLE WITHOUT ID
  cluster_prefix AS "Cluster",
  length(rows) AS "Manifests",
  dateformat(max(rows.file.mtime), "HH:mm") AS "Latest"
FROM "forensics/manifests"
WHERE date(file.mtime) >= date(today)
GROUP BY cluster_prefix
SORT length(rows) DESC
```

---

*Updated each session. Source files credited in `derived_from:` frontmatter.*
