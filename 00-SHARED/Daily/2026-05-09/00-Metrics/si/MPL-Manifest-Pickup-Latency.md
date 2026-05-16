---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, mpl]
metric_id: MPL
suite: SI
target: "< 1 turn"
flag_threshold: "> 3 turns"
weight_in_composite: 0.15
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[OMR-Orphaned-Manifest-Rate]]", "[[SHL-Signal-Half-Life]]"]
child: []
doc_hash: sha256:65bd35ce7c076a14028b71f4ec5a411f763cb9b07968986c82ff5ec48b984610
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# MPL — Manifest Pickup Latency

## Definition

Number of turns between a manifest reaching `"status": "final"` and the next Agent call that cites it. Measures how quickly downstream work reacts to upstream output.

## Formula

```
MPL = downstream_turn_index - manifest_final_turn_index
```

## Target

- **Target:** < 1 turn (faerie reads manifest and spawns in the same turn or immediately following)
- **Flag threshold:** > 3 turns (3+ turns of session activity before the manifest is acted on)
- **Composite weight:** 0.15

## Why It Matters

In the ideal case, a manifest appears and faerie picks it up in the very next turn — zero thinking time, immediate propagation. Every turn of latency is a turn where the human is waiting, the main session is using context on something other than acting on the available signal, or the manifest is sitting idle. MPL captures the "hot path" responsiveness of the piston.

Note: MPL and [[../sbi/RAL-Return-to-Action-Latency|RAL]] are related but different. RAL measures main-session token overhead on the return; MPL measures turn latency. A session can have good RAL (lean acknowledgment) but bad MPL (waits several turns before spawning downstream work).

## Collection

**Data source:** Session transcript turn index + manifest `ts` field.
**Sampling:** Per manifest completion.

## Failure Modes

- **User interruption:** If the user sends a message between manifest completion and downstream spawn, the latency is partially user-driven. Flag `user_interruption: true` on affected samples.
- **Deliberate batching:** Faerie may intentionally wait for multiple manifests before launching the next wave (wave batching). This is architecturally correct but shows as high MPL for early returners. Discount manifests that were batched with later returners before the next wave was launched.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "MPL"
SORT created DESC
LIMIT 10
```

## Related

- [[OMR-Orphaned-Manifest-Rate]]
- [[SHL-Signal-Half-Life]]
- [[../sbi/RAL-Return-to-Action-Latency]]
- [[../SI-Stigmergy-Index]]
