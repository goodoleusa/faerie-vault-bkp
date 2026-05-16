---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, spx]
metric_id: SPX
suite: SBI
target: "≥ 0.80"
flag_threshold: "< 0.50"
weight_in_composite: 0.15
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[IRR-Inline-Reasoning-Ratio]]", "[[TDR-Token-Delegation-Ratio]]"]
child: []
doc_hash: sha256:c33b34ab69b38047a0ccd133a6cb26efc00d606c31fd79e17f8ad645ca653d39
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# SPX — Switchboard Purity Index

## Definition

Fraction of main-session turns that are "spawn events" — turns whose primary action is an Agent call — weighted by output length (longer turns that aren't spawns count against SPX more).

## Formula

```
SPX = spawn_turns / total_turns  (weighted by output length)
```

## Target

- **Target:** ≥ 0.80 (80% of session activity by weight is spawning)
- **Flag threshold:** < 0.50 (half or more of session weight is non-spawn activity)
- **Composite weight:** 0.15

## Why It Matters

SPX is the broadest measure of switchboard discipline. IRR catches pre-spawn deliberation, STL catches slow first spawn, but SPX catches everything: long analytical responses, extended planning turns, verbose result summaries — any turn where the main session is doing work rather than spawning. At SPX ≥ 0.80, the session feels like a dispatcher. Below 0.50, it's a research assistant.

## Collection

**Data source:** Session transcript turn classification.
**Sampling:** Per session.
**Parser:** Classify each turn as spawn (primary action = Agent call) or non-spawn. Weight by output token count. SPX = sum(spawn_turn_tokens) / total_tokens.

## Failure Modes

- **Manifest-reading turns:** After a W3 return, faerie reads a long manifest and writes a summary. This is coordination-necessary but shows as a non-spawn turn. Consider a "coordination read" turn category that doesn't penalize SPX.
- **Context-load turns:** Session start (HONEY.md + NECTAR.md reads) inflate non-spawn weight. Flag and discount.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "SPX"
SORT created DESC
LIMIT 10
```

## Related

- [[IRR-Inline-Reasoning-Ratio]]
- [[TDR-Token-Delegation-Ratio]]
- [[../SBI-Switchboard-Index]]
