---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, maa, fpr]
metric_id: FPR
suite: MaA
target: "≥ 0.90"
flag_threshold: "< 0.70"
weight_in_composite: 0.10
parent: ["[[MBI-Membench-Index]]"]
up: "[[_INDEX.md]]"
sibling: ["[[ISR-Insight-Surfacing-Rate]]", "[[../sbi/ARD-Agent-Return-Density]]"]
child: []
doc_hash: sha256:538add6ecdcf33bf35072e35c0c9431321f1b20b9427ddc8cbc05f63daaeae01
hash_ts: 2026-04-20T21:59:32Z
hash_method: body-sha256-v1
---

> [↑ MBI](MBI-Membench-Index.md) · [⌂ Metrics Index](_INDEX.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# FPR — Flow Preservation Rate

## Definition

Fraction of sessions where the human never hit a stall — defined as waiting more than 60 seconds with no agent return visible, no progress message, no faerie acknowledgment.

## Formula

```
FPR = sessions_without_stall / total_sessions
```

A "stall" = human in active session, 60+ seconds elapsed, no agent return event, no user-visible output from faerie.

## Target

- **Target:** ≥ 0.90 (stalls are rare events)
- **Flag threshold:** < 0.70 (nearly one in three sessions includes a stall — human flow is regularly broken)
- **Composite weight:** 0.10 (in MaA composite)

## Why It Matters

The human's flow state is the scarcest resource in the system. When the system stalls, the human either disengages or starts asking "what's happening?" — both are context-switching costs. FPR measures how reliably the piston keeps output visible. A well-functioning MaA session should feel continuous: something is always returning, always visible, always moving forward. The human never needs to wonder if the system is stuck.

FPR is a lagging indicator — it captures the felt experience of the session, not intermediate mechanics. It integrates WCR (agents completing), ARD (throughput), and the async discipline (no polling, no silence-then-flood pattern).

## Collection

**Data source:** Session telemetry timestamps; agent return event timestamps vs human turn timestamps.
**Sampling:** Per session.
**Stall detection:** If `time_since_last_agent_return > 60s AND human_sent_no_message_in_window`, record stall.

## Failure Modes

- **Background W3 agents:** Long W3 runs legitimately take minutes. Flag sessions with active W3 background runs; a 60s stall during W3 execution is not a flow failure if faerie communicated "W3 is running."
- **Session type:** Short sessions (< 15 min) may have no agents at all — FPR is trivially high. Report only for substantive sessions (≥ 3 agent spawns or ≥ 30 min active).

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "FPR"
SORT created DESC
LIMIT 10
```

## Related

- [[ISR-Insight-Surfacing-Rate]]
- [[../sbi/ARD-Agent-Return-Density]]
- [[../01-Literature/MaaS-vs-MaA-Framework]]
