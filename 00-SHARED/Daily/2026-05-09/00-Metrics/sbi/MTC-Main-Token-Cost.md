---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, mtc]
metric_id: MTC
suite: SBI
target: "< 2K tokens/return"
flag_threshold: "> 8K tokens/return"
weight_in_composite: 0.10
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[CTD-Context-Token-Debt]]", "[[TDR-Token-Delegation-Ratio]]"]
child: []
doc_hash: sha256:45204d6ce93917e7890fcbb6af9e48fa394abc256bf5122c0e8cc455753a3cba
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# MTC — Main Token Cost / Return

## Definition

Average main-session tokens spent between consecutive agent returns. Measures the overhead the main session pays per unit of agent output received.

## Formula

```
MTC = main_tokens_between_returns / returns_received
```

## Target

- **Target:** < 2K tokens per return
- **Flag threshold:** > 8K tokens per return (main is spending 4× more than healthy)
- **Composite weight:** 0.10

## Why It Matters

A lean main session coordinates agent returns with minimal overhead. If the main session is consuming 8K+ tokens between each return, it is doing substantial work inline — reasoning, synthesizing, re-reading context — that should be delegated. MTC is the budget metric: it measures the token economy of orchestration.

In MaaS vs MaA terms: MaaS optimizes MTC aggressively (cost reduction). MaA accepts higher MTC when it enables richer coordination and longer agent chains.

## Collection

**Data source:** `session_metrics.py` main token totals; agent return event timestamps.
**Sampling:** Per agent return.
**Parser:** Token delta from last return event to current return event; divide by return count in window.

## Failure Modes

- **False positive:** Session start (faerie turn-0 context load) inflates MTC for first return. Exclude the turn-0 context initialization from MTC calculation.
- **False negative:** Main session is lean but each return is trivial (e.g., "file exists: true"). High return count with low MTC can still be a coordination problem — check ARD and WCR together.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "MTC"
SORT created DESC
LIMIT 10
```

## Related

- [[CTD-Context-Token-Debt]]
- [[TDR-Token-Delegation-Ratio]]
- [[../SBI-Switchboard-Index]]
