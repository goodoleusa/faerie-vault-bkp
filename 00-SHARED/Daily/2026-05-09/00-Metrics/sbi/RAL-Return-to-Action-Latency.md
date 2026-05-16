---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, ral]
metric_id: RAL
suite: SBI
target: "< 500 tokens"
flag_threshold: "> 2K tokens"
weight_in_composite: 0.10
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[STL-Spawn-Turn-Latency]]", "[[MPL-Manifest-Pickup-Latency]]"]
child: []
doc_hash: sha256:931f1974ae84fa166280b6a5ad4a982aa15e43e80c2af73e05e3f9fcefd1feb2
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# RAL — Return-to-Action Latency

## Definition

Tokens generated in the main session between receiving a TaskNotification and taking the next substantive action (spawning an agent, writing a file, or returning to the user).

## Formula

```
RAL = tokens_from_TaskNotification_to_next_action
```

## Target

- **Target:** < 500 tokens (brief acknowledgment + immediate action)
- **Flag threshold:** > 2K tokens (main session re-synthesizing the returned work before acting)
- **Composite weight:** 0.10

## Why It Matters

A notification arrives: agent has returned. The correct response is to glance at `dashboard_line`, decide next action, and act — typically another spawn or a brief user update. At < 500 tokens this is a 2–3 sentence acknowledgment plus tool call. At > 2K tokens, faerie is re-reading the full manifest, summarizing it, evaluating it, and writing an analysis before deciding what to do — work that belongs inside the downstream agent.

RAL and STL form a pair: STL measures latency on the input side (user message → spawn), RAL measures latency on the output side (agent return → next action).

## Collection

**Data source:** Session transcript; token delta from TaskNotification event to next tool call.
**Sampling:** Per notification.

## Failure Modes

- **Large manifest reading:** If the notification is from a W3 deep-synthesis agent, reading its full output before acting is appropriate. Flag `agent_tier: W3` and apply a looser threshold (< 2K for W3 returns).
- **User turn between notification and action:** If the user sends a message that intercepts the notification acknowledgment, the latency is not faerie's fault — discount.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "RAL"
SORT created DESC
LIMIT 10
```

## Related

- [[STL-Spawn-Turn-Latency]]
- [[../si/MPL-Manifest-Pickup-Latency]]
- [[../SBI-Switchboard-Index]]
