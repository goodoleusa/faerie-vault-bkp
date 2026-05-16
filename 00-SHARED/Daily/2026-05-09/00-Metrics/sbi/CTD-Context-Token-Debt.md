---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, ctd]
metric_id: CTD
suite: SBI
target: "< 8K tokens"
flag_threshold: "> 20K tokens"
weight_in_composite: 0.10
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[MTC-Main-Token-Cost]]", "[[TDR-Token-Delegation-Ratio]]"]
child: []
doc_hash: sha256:085739ad88c1aeafa2ca88a5fe7e0e700219b60958e16cc654d062d61149f0ed
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# CTD — Context Token Debt

## Definition

Tokens accumulated in the main session context since the last Agent call. Measures how much context weight is building between spawns.

## Formula

```
CTD = tokens_since_last_agent_call  (sampled per turn)
```

## Target

- **Target:** < 8K tokens (main context stays lean between spawns)
- **Flag threshold:** > 20K tokens (main has accumulated 2–3 full turns of agent-level work)
- **Composite weight:** 0.10

## Why It Matters

CTD is the "lean main" monitor. Even if faerie spawns frequently, if each spawn is preceded by a long preamble, context builds up. At 20K+ tokens between spawns, the main session is effectively doing a full agent run inline before delegating — the delegation is symbolic at that point.

In MaA terms: lean main = infinitely scalable. As long as CTD stays below 8K, 100+ agent spawns in a session remain theoretically possible without context pressure.

## Collection

**Data source:** Token counter on main session, sampled per turn. Reset on each `Agent(...)` call.
**Sampling:** Per turn.
**Report:** `CTD_max` (worst-case per session) and `CTD_avg` (typical).

## Failure Modes

- **Legitimate high CTD:** Long context reads (HONEY.md, SPAWN-BOILERPLATE.md) at session start inflate CTD before first spawn. Record but flag `session_start_read: true` to discount.
- **Cascade read inflation:** Reading multiple agent manifests at once can inflate CTD transiently. These are coordination-necessary reads; distinguish from inline reasoning.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "CTD"
SORT created DESC
LIMIT 10
```

## Related

- [[MTC-Main-Token-Cost]]
- [[TDR-Token-Delegation-Ratio]]
- [[../SBI-Switchboard-Index]]
