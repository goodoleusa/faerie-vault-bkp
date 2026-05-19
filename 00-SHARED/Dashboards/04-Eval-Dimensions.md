---
type: dashboard
tier: eval
title: "Eval Dimensions — A through G (last 7d)"
status: live
derived_from:
  - "CyberOps-UNIFIED/00-SHARED/Dashboards/system/metrics-dashboard-20260425.md"
  - "CyberOps-UNIFIED/00-SHARED/Daily-Dashboards/2026-05-09/02-Dashboards/Metric-Trends.md"
  - "faerie2/forensics/dashboards/dashboard/membench-eval-dashboard.html"
tags: [dashboard, eval, metrics]
---

# Eval Dimensions

Last 7 days of dimension A-G scores. Dataview tables; treat trends as sparkline-equivalent.

External HTML view: [membench-eval-dashboard.html](file:///mnt/d/0local/gitrepos/faerie2/forensics/dashboards/dashboard/membench-eval-dashboard.html)

---

## Composite (last 10 runs)

```dataview
TABLE session_id, composite AS "Composite", created AS "Date"
FROM "forensics" AND #eval-run
WHERE composite != null
SORT created DESC
LIMIT 10
```

## Dim A — Throughput

```dataview
TABLE session_id, dim_A AS "A: Throughput", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_A != null
SORT created DESC
LIMIT 10
```

## Dim B — Memory

```dataview
TABLE session_id, dim_B AS "B: Memory", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_B != null
SORT created DESC
LIMIT 10
```

## Dim C — Resilience

```dataview
TABLE session_id, dim_C AS "C: Resilience", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_C != null
SORT created DESC
LIMIT 10
```

## Dim D — Quality

```dataview
TABLE session_id, dim_D AS "D: Quality", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_D != null
SORT created DESC
LIMIT 10
```

## Dim E — Piston

```dataview
TABLE session_id, dim_E AS "E: Piston", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_E != null
SORT created DESC
LIMIT 10
```

## Dim F — Model Routing

```dataview
TABLE session_id, dim_F AS "F: Routing", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_F != null
SORT created DESC
LIMIT 10
```

## Dim G — Emergence

```dataview
TABLE session_id, dim_G AS "G: Emergence", created AS "Date"
FROM "forensics" AND #eval-run
WHERE dim_G != null
SORT created DESC
LIMIT 10
```
