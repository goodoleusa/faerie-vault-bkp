---
type: dashboard
status: active
created: 2026-04-20
tags: [dashboard, session-health, mbi, sbi, si]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Metric-Trends]]", "[[Flag-Table]]"]
child: []
doc_hash: sha256:d1ddaf3ce8dd77664e2bbef2c6666e1a4eef0fede504e0b4f02aad5680a97cfb
hash_ts: 2026-04-20T21:59:41Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](_INDEX.md) · [→ Trends](Metric-Trends.md) · [⌂ Home](../HOME.md)

# Session Health Dashboard

Latest SBI, SI, MBI readings per session. Live via Dataview.

## Composite Scores (Recent Sessions)

```dataview
TABLE session_id, SBI, SI, MBI, status, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 5
```

## MaA vs MaaS Composites (Recent Sessions)

```dataview
TABLE session_id, SBI, SI, MBI, MaaS_Score, MaA_Score, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 5
```

## SBI Sub-Metric Breakdown

```dataview
TABLE session_id, IRR, STL, MTC, ARD, CTD, WCR, SPX, TDR, RAL
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 5
```

## SI Sub-Metric Breakdown

```dataview
TABLE session_id, OMR, MPL, SDR, CMR, CSS, BPR, CD, PCR
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 5
```

## MaA Extended Metrics

```dataview
TABLE session_id, ISR, FPR, "COC-WORM-AR"
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 5
```

## Status Legend

| Status | MBI Range | Meaning |
|--------|-----------|---------|
| healthy | ≥ 0.80 | All systems nominal |
| degraded | 0.60–0.79 | One axis dragging — check SBI vs SI |
| critical | < 0.60 | Immediate investigation required |

## Notes

Baselines are populated by running `/membench baseline` after a session. First measurement pending.

See [[../03-Baselines/baseline-2026-04-20|Baseline placeholder]] for schema reference.
See [[../04-Methods/Collection-Procedure|Collection Procedure]] for how values are measured.
