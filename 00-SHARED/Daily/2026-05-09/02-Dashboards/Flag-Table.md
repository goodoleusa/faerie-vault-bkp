---
type: dashboard
status: active
created: 2026-04-20
tags: [dashboard, flags, alerts]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Session-Health]]", "[[Metric-Trends]]"]
child: []
doc_hash: sha256:936180374929d2b1f5a162291c3c0d656f08bfa58f5b4157633d27ef4cc58664
hash_ts: 2026-04-20T21:59:41Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](_INDEX.md) · [← Trends](Metric-Trends.md) · [⌂ Home](../HOME.md)

# Flag Table

Metrics currently in flag zone in the most recent session. A flag means the metric has crossed its threshold and requires attention.

## Current Session Flags

```dataview
TABLE session_id, IRR, "IRR > 0.30?" as IRR_flag, OMR, "OMR > 0.30?" as OMR_flag, SDR, "SDR < 0.50?" as SDR_flag
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 1
```

## All Flag Thresholds Reference

| Metric | Suite | Flag When |
|--------|-------|-----------|
| IRR | SBI | > 0.30 |
| STL | SBI | ≥ 2 turns |
| MTC | SBI | > 8K tokens |
| ARD | SBI | < 1/hr |
| CTD | SBI | > 20K tokens |
| WCR | SBI | < 0.70 |
| SPX | SBI | < 0.50 |
| TDR | SBI | < 0.60 |
| RAL | SBI | > 2K tokens |
| SBI | SBI | < 0.60 |
| OMR | SI | > 0.30 |
| MPL | SI | > 3 turns |
| SDR | SI | < 0.50 |
| CMR | SI | > 0.60 |
| CSS | SI | < 0.50 |
| BPR | SI | < 0.30 |
| CD | SI | = 0 |
| PCR | SI | > 0.05 |
| SFE | SI | < 0.65 |
| SHL | SI | > 12h |
| SI | SI | < 0.55 |
| MBI | MBI | < 0.60 |
| ISR | MaA | < 0.5/hr |
| FPR | MaA | < 0.70 |
| COC-WORM-AR | MaA | < 0.80 |

## Historical Flags

```dataview
TABLE session_id, SBI, SI, MBI, status, created as "Date"
FROM "03-Baselines"
WHERE type = "baseline" AND status != "healthy"
SORT created DESC
LIMIT 20
```

## What to Do When a Metric Flags

1. Read the metric's deep-dive page (linked from [[../00-Metrics/_INDEX|Metrics Index]])
2. Check the "Failure Modes" section for likely causes
3. Review the session transcript for the specific behavior that drove the flag
4. If systemic, create a task in the queue to address the root cause

Flags are observations, not verdicts. A single-session flag in a metric with low sample size (e.g., CDr in a session with 2 agents) should be noted but not acted on. Three consecutive flags require action.
