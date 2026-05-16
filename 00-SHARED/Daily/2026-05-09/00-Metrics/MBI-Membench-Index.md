---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, mbi, composite]
metric_id: MBI
suite: MBI
target: "≥ 0.80"
flag_threshold: "< 0.60"
weight_in_composite: 1.0
parent: ["[[../INDEX.md]]"]
up: "[[../_INDEX.md]]"
child: ["[[SBI-Switchboard-Index]]", "[[SI-Stigmergy-Index]]"]
doc_hash: sha256:da8080e1819fd072cf37451b74c4111c7f34c632429996d1a9f8ad1c1d33a8d0
hash_ts: 2026-04-20T21:59:33Z
hash_method: body-sha256-v1
---

> [↑ Metrics Index](_INDEX.md) · [⌂ Home](../HOME.md) · [📊 Dashboard](../02-Dashboards/Session-Health.md)

# MBI — Membench Index

## Definition

Single session health number combining delegation quality (SBI) and coordination quality (SI). The headline metric for a faerie session.

## Formula

```
MBI = 0.5 * SBI + 0.5 * SI
```

## Target

- **Target:** ≥ 0.80
- **Flag threshold:** < 0.60 (session health degraded — inspect SBI and SI separately)

## Interpretation

| MBI | SBI | SI | Reading |
|-----|-----|----|---------|
| ≥ 0.80 | ≥ 0.80 | ≥ 0.80 | Healthy |
| 0.65–0.79 | varies | varies | Degraded — check which axis is low |
| < 0.60 | — | — | Critical — immediate investigation |

**SBI dragging:** Main session doing too much work. Fix: spawn faster, shorter pre-spawn reasoning.
**SI dragging:** Agents isolated. Fix: add `triggered_by` + `files_read` fields, check broadcast.jsonl propagation.
**Both low:** Structural breakdown. Start with SBI (delegation foundation precedes coordination).

Note: MBI is meaningless if both inputs are from sessions with very few agents. Sample size < 3 spawns = report null, not a number.

## MaaS vs MaA Context

MBI is the **MaA** (Memory-as-Architecture) health metric. It measures whether the system is building compounding value through coordination.

For **MaaS** (Memory-as-Service) use cases, the relevant composite is different — see [[../01-Literature/MaaS-vs-MaA-Framework|MaaS vs MaA Framework]] for the scoring distinction.

## Collection

**Source:** `collectors/mbi_calculator.py` — reads SBI + SI from session snapshot.
**Sampling:** Per session.

## Dashboard Query

```dataview
TABLE session_id, SBI, SI, MBI, status
FROM "03-Baselines"
WHERE type = "baseline"
SORT created DESC
LIMIT 10
```

## Related

- [[SBI-Switchboard-Index]]
- [[SI-Stigmergy-Index]]
- [[../01-Literature/MaaS-vs-MaA-Framework]]
- [[../02-Dashboards/Session-Health]]
