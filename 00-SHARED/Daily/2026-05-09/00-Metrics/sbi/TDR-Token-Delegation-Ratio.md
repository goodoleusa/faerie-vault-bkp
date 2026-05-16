---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, tdr]
metric_id: TDR
suite: SBI
target: "≥ 0.85"
flag_threshold: "< 0.60"
weight_in_composite: 0.10
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[MTC-Main-Token-Cost]]", "[[SPX-Switchboard-Purity-Index]]"]
child: []
doc_hash: sha256:f5b8c079db6daf17ed4689b30fc68f6f4b19e895cc87ddb0c9fe7cff3a75f8e2
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# TDR — Token Delegation Ratio

## Definition

Fraction of total session tokens spent in subagents rather than the main session. Measures whether expensive inference is happening in agents (correct) or inline (wrong).

## Formula

```
TDR = subagent_tokens / (main_tokens + subagent_tokens)
```

## Target

- **Target:** ≥ 0.85 (85% of token spend is in agents)
- **Flag threshold:** < 0.60 (main session accounts for more than 40% of token spend)
- **Composite weight:** 0.10

## Why It Matters

Token spend is a proxy for work. If main is spending 40%+ of total tokens, it is doing 40%+ of the work inline — reasoning, synthesizing, analyzing. The faerie model says this work belongs in agents. TDR is the economic accountability metric: it measures where the inference budget is actually going.

This is also the primary MaaS metric. A system optimizing for cost should show TDR → 1.0 (all expensive work delegated to cheapest capable agent). A system showing TDR < 0.60 is billing the customer for expensive main-session inference that should have been Haiku.

## Collection

**Data source:** `session_metrics.py` subagent token totals vs main session totals.
**Sampling:** Per session.

## Failure Modes

- **W3 Opus agents:** Very long W3 runs inflate subagent tokens correctly — TDR looks high even if main was doing too much. Both can be true simultaneously; check MTC and CTD alongside TDR.
- **Short sessions:** Sessions with 1–2 agents may have genuinely high main-session fraction (turn-0 context load). Note `session_type: short` and discount.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "TDR"
SORT created DESC
LIMIT 10
```

## Related

- [[MTC-Main-Token-Cost]]
- [[SPX-Switchboard-Purity-Index]]
- [[../SBI-Switchboard-Index]]
- [[../MBI-Membench-Index]]
