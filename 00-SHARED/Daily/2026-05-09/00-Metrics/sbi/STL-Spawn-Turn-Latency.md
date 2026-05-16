---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, stl]
metric_id: STL
suite: SBI
target: "0 turns"
flag_threshold: "≥ 2 turns"
weight_in_composite: 0.10
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[IRR-Inline-Reasoning-Ratio]]", "[[RAL-Return-to-Action-Latency]]"]
child: []
doc_hash: sha256:1897775b12477d6d78b8604cbf3716144683030a49eeb429cdb3b86913837a11
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# STL — Spawn Turn Latency

## Definition

Number of turns between a substantive user message and the first Agent call made in response to it. Ideal is 0 — spawn is the first action.

## Formula

```
STL = turn_index_of_first_agent_call - turn_index_of_user_message
```

## Target

- **Target:** 0 turns (spawn is the first action after user message)
- **Flag threshold:** ≥ 2 turns (two or more turns of non-spawn activity before delegating)
- **Composite weight:** 0.10

## Why It Matters

When faerie encounters a substantive request, spawn should be the first response — not a clarifying question, not a summary of what it's about to do, not an analysis of options. Each turn before the first spawn is a turn where the human is waiting and the main session is consuming tokens it doesn't need to. STL = 0 is the switchboard ideal.

## Collection

**Data source:** Session transcript turn index.
**Sampling:** Per user message.
**Parser:** Find `Agent(...)` tool call turn index; subtract user message turn index. If no Agent call follows the message, STL = ∞ (flag separately as "no-delegation session").

## Failure Modes

- **False positive:** User sends a message that genuinely requires a clarifying question before delegation is possible — STL = 1 here is correct, not a failure. Heuristic: if the clarifying question is answered in the next turn and spawn follows, discount.
- **False negative:** Faerie spawns but the spawn is a trivial "check if file exists" that doesn't represent actual delegation — MTC and TDR will catch this.
- **Common cause:** Faerie starts explaining its plan before executing it. Fix: "do, don't ask."

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "STL"
SORT created DESC
LIMIT 10
```

## Related

- [[IRR-Inline-Reasoning-Ratio]]
- [[RAL-Return-to-Action-Latency]]
- [[../SBI-Switchboard-Index]]
