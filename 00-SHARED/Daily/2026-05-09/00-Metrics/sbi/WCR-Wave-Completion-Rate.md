---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, wcr]
metric_id: WCR
suite: SBI
target: "≥ 0.90"
flag_threshold: "< 0.70"
weight_in_composite: 0.10
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[ARD-Agent-Return-Density]]", "[[SPX-Switchboard-Purity-Index]]"]
child: []
doc_hash: sha256:73c260714a709f432e8ec9cb108d03adf5a5a335c0ef9c88d8483cd0544631e3
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# WCR — Wave Completion Rate

## Definition

Fraction of spawned agents that produced a manifest reaching `"status": "final"` within the session (or within a reasonable timeout window for background agents).

## Formula

```
WCR = manifests_with_final_status / agents_spawned
```

## Target

- **Target:** ≥ 0.90 (≤ 10% of spawned agents stall or fail silently)
- **Flag threshold:** < 0.70 (nearly a third of spawns are waste)
- **Composite weight:** 0.10

## Why It Matters

WCR measures whether the pipeline is actually delivering. Spawning agents is only valuable if they complete. A low WCR means spawn overhead is being paid without getting the work — agents stalled, ran out of context, or returned with incomplete manifests. It also indicates the stigmergy tracker is needed (agents that stall without manifest updates should trigger re-queuing).

## Collection

**Data source:** `wave*-result.json` glob at session end.
**Sampling:** Per wave, per session.
**Edge cases:** Background W3 agents should be checked at next `/faerie` start, not at session end. WCR for W3 uses a 24h window.

## Failure Modes

- **Missing manifest vs genuinely incomplete:** An agent that writes a manifest with status "in-progress" and never updates it is incomplete (WCR denominator++, numerator--). An agent that never writes any manifest is also incomplete. Both count the same way.
- **Re-spawns from stall recovery:** If error-coordinator respawns a stalled agent and it completes, count as 1 completion for 1 spawn (not 2 spawns).

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "WCR"
SORT created DESC
LIMIT 10
```

## Related

- [[ARD-Agent-Return-Density]]
- [[SPX-Switchboard-Purity-Index]]
- [[../SBI-Switchboard-Index]]
