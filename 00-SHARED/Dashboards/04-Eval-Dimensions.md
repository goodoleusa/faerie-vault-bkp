---
type: dashboard
tier: eval
title: "Eval Dimensions — A through G (last 7d)"
status: live
N: '[00-Home](00-Home.md)'
E: ['[01-Today](01-Today.md)', '[02-Missions-Emergent](02-Missions-Emergent.md)', '[03-Anchors](03-Anchors.md)', '[05-Stigmergy](05-Stigmergy.md)']
W: '[00-Home](00-Home.md)'
tags: [dashboard, eval, metrics]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Eval Dimensions

Last 7 days of dimension A-G scores. Treat trends as sparkline-equivalent.

External HTML view: [membench-eval-dashboard.html](file:///mnt/d/0local/gitrepos/faerie2/forensics/dashboards/dashboard/membench-eval-dashboard.html)

```dataview
TABLE A, B, C, D, E, F, G
FROM "00-SHARED/review"
WHERE file.cday >= date(today) - dur(7 days)
SORT file.cday DESC
```
