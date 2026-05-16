---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, sbi, ard]
metric_id: ARD
suite: SBI
target: "≥ 3 returns/hour"
flag_threshold: "< 1 return/hour"
weight_in_composite: 0.15
parent: ["[[../SBI-Switchboard-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[WCR-Wave-Completion-Rate]]", "[[MTC-Main-Token-Cost]]"]
child: []
doc_hash: sha256:92d1280ed481f8697d651d163f2162c798ec66453126edddec9c60954f26c053
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ SBI](../SBI-Switchboard-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# ARD — Agent Return Density

## Definition

Number of agent returns (manifests reaching final status) per hour of active session time. Measures throughput — how much agent work the session is processing.

## Formula

```
ARD = agent_returns / session_hours_active
```

## Target

- **Target:** ≥ 3 returns/hour
- **Flag threshold:** < 1 return/hour (session is stalled — agents not finishing or not being spawned)
- **Composite weight:** 0.15

## Why It Matters

ARD is the throughput signal. A well-orchestrated session dispatches W1 triage quickly (multiple returns in first few minutes), then sustains W2 feature work. Fewer than 1 return per hour means either agents aren't being spawned or they're stalling mid-run — both degrade session value.

## Collection

**Data source:** `len(task_notifications) / session_uptime_hours` from `session_metrics.py`.
**Sampling:** Per session.
**Edge case:** Background W3 agents may return after session end — count them at collection time.

## Failure Modes

- **Low ARD from long W3 runs:** A single W3 agent running for 45 minutes depresses ARD even if it's doing valuable work. Weight by wave type or report W1/W2/W3 ARD separately.
- **Inflated ARD from trivial spawns:** Many quick file-check agents inflate ARD without real throughput. Cross-check with TDR.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "ARD"
SORT created DESC
LIMIT 10
```

## Related

- [[WCR-Wave-Completion-Rate]]
- [[MTC-Main-Token-Cost]]
- [[../SBI-Switchboard-Index]]
