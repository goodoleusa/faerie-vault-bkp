---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, maa, isr]
metric_id: ISR
suite: MaA
target: "≥ 2/hour"
flag_threshold: "< 0.5/hour"
weight_in_composite: 0.10
parent: ["[[MBI-Membench-Index]]"]
up: "[[_INDEX.md]]"
sibling: ["[[FPR-Flow-Preservation-Rate]]", "[[SI-Stigmergy-Index]]"]
child: []
doc_hash: sha256:42e9e4b2efd40c9c5a4c0bd0baf1209f870cb26ef42037aaf16ff157fa516895
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ MBI](MBI-Membench-Index.md) · [⌂ Metrics Index](_INDEX.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# ISR — Insight Surfacing Rate

## Definition

Number of droplets or findings per session hour that the human validates as useful — actively accepted, promoted, or acted upon rather than dismissed. Measures whether the anti-evaporation layer is delivering value.

## Formula

```
ISR = (droplets_validated_useful + findings_accepted) / session_hours_active
```

Validated = human explicitly accepts, promotes to NECTAR, creates a task from, or acts on the finding within the session.

## Target

- **Target:** ≥ 2 validated insights per hour
- **Flag threshold:** < 0.5/hour (the surfacing layer is mostly noise)
- **Composite weight:** 0.10 (in MaA composite)

## Why It Matters

The whole purpose of the pollen → NECTAR → HONEY pipeline is to surface insights that the human couldn't have articulated as a query. ISR measures the output of that system: not how many droplets are written (output metric) but how many the human finds genuinely valuable (outcome metric). High droplet count with low ISR means agents are writing noise. Low droplet count with high ISR means the write discipline is too conservative — insights are being lost.

ISR is exclusively a **MaA** metric. A MaaS system has no equivalent — it doesn't surface unsolicited insights; it answers explicit queries.

## Collection

**Data source:** Vault promotion logs, `/memory` command interactions, NECTAR append events from human sessions.
**Sampling:** Per session.
**Proxy:** When direct validation tracking isn't available, count droplets that receive a follow-on human action (linked task created, promoted to NECTAR, cited in a vault doc) within 2 sessions.

## Failure Modes

- **Validation tracking incomplete:** Most sessions don't have explicit "accept/reject" signals. The proxy (downstream action within 2 sessions) is imprecise.
- **ISR inflated by low quality bar:** If the human promotes everything to NECTAR indiscriminately, ISR is meaningless. Context: HONEY gauntlet requires recurrence — so HONEY ISR is more meaningful than raw NECTAR ISR.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "ISR"
SORT created DESC
LIMIT 10
```

## Related

- [[FPR-Flow-Preservation-Rate]]
- [[../01-Literature/MaaS-vs-MaA-Framework]]
- [[SI-Stigmergy-Index]]
