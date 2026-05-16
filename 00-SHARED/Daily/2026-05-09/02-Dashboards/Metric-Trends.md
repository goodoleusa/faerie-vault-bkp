---
type: dashboard
status: active
created: 2026-04-20
tags: [dashboard, trends, metrics]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Session-Health]]", "[[Flag-Table]]"]
child: []
doc_hash: sha256:f3fd774755d2d54e0b93f4f563f17120ba7a1f5d7189f32562c1a8037b2eb8fa
hash_ts: 2026-04-20T21:59:41Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](_INDEX.md) · [← Health](Session-Health.md) · [→ Flags](Flag-Table.md) · [⌂ Home](../HOME.md)

# Metric Trends Dashboard

Per-metric last-10-session tables. Dataview cannot render charts natively — use these tables as inputs for external visualization if needed.

## SBI Composite Trend

```dataview
TABLE session_id, SBI, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND SBI != null
SORT created DESC
LIMIT 10
```

## SI Composite Trend

```dataview
TABLE session_id, SI, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND SI != null
SORT created DESC
LIMIT 10
```

## MBI Composite Trend

```dataview
TABLE session_id, MBI, status, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND MBI != null
SORT created DESC
LIMIT 10
```

## IRR Trend

```dataview
TABLE session_id, IRR, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND IRR != null
SORT created DESC
LIMIT 10
```

## SDR Trend

```dataview
TABLE session_id, SDR, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND SDR != null
SORT created DESC
LIMIT 10
```

## OMR Trend

```dataview
TABLE session_id, OMR, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND OMR != null
SORT created DESC
LIMIT 10
```

## CD Trend

```dataview
TABLE session_id, CD, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND CD != null
SORT created DESC
LIMIT 10
```

## ISR Trend (MaA)

```dataview
TABLE session_id, ISR, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND ISR != null
SORT created DESC
LIMIT 10
```

## FPR Trend (MaA)

```dataview
TABLE session_id, FPR, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND FPR != null
SORT created DESC
LIMIT 10
```
