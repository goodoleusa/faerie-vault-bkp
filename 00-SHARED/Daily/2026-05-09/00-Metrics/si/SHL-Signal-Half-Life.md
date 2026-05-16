---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, shl]
metric_id: SHL
suite: SI
target: "< 2 hours"
flag_threshold: "> 12 hours"
weight_in_composite: null
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[MPL-Manifest-Pickup-Latency]]", "[[CSS-Cross-Session-Signal-Survival]]"]
child: []
doc_hash: sha256:b0ed5952fc39357337ea14960e895c4a5d849893e4ceec60c38fe103097d244b
hash_ts: 2026-04-20T21:59:35Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# SHL — Signal Half-Life

## Definition

Median age of manifests (from `"status": "final"` write time to first citation) in hours. Measures freshness of the coordination signal at pickup time.

## Formula

```
SHL = median(citation_timestamp - manifest_final_ts)  [in hours]
```

## Target

- **Target:** < 2 hours (manifests are acted on while the work context is still warm)
- **Flag threshold:** > 12 hours (manifests sitting idle through a full day cycle)
- **Composite weight:** null (informational; not in SI composite — cross-session cases make normalization unstable)

## Why It Matters

A manifest picked up immediately after writing carries maximum coordination value — the spawning context, the rationale, the findings are all fresh. A manifest picked up 24+ hours later is stale: the session context that created it is gone, the human may not remember why it mattered, and the downstream work is decoupled from the upstream reasoning. SHL is the staleness signal.

Note: SHL > 12h is common for cross-session cases and is separately captured by CSS. Within a session, SHL should be < 2h unless wave batching is intentional.

## Collection

**Data source:** Manifest `ts` field + session transcript timestamps.
**Sampling:** Per manifest with at least one citation.
**Excludes:** Orphaned manifests (no citation → undefined age, contributes to OMR instead).

## Failure Modes

- **Cross-session pickup:** SHL naturally exceeds 12h for manifests read in the next session. Flag separately; these are cross-session coordination events, not intra-session latency.
- **Wave batching:** Manifests intentionally batched before wave launch show high SHL for early returners. Distinguish by checking if the batch of manifests was read together in one turn.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "SHL"
SORT created DESC
LIMIT 10
```

## Related

- [[MPL-Manifest-Pickup-Latency]]
- [[CSS-Cross-Session-Signal-Survival]]
- [[../SI-Stigmergy-Index]]
