---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, omr]
metric_id: OMR
suite: SI
target: "< 0.10"
flag_threshold: "> 0.30"
weight_in_composite: 0.20
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[MPL-Manifest-Pickup-Latency]]", "[[SDR-Stigmergic-Discovery-Rate]]"]
child: []
doc_hash: sha256:1f0f9e76aca90b3de485d59446b082452c65c2b0eef7d827377886771e9d77fc
hash_ts: 2026-04-20T21:59:35Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# OMR — Orphaned Manifest Rate

## Definition

Fraction of agent manifests that were written but never cited by any downstream agent or spawn prompt. An orphaned manifest is a signal emitted into the filesystem that no one listened to.

## Formula

```
OMR = (manifests_written - manifests_read_by_downstream) / manifests_written
```

## Target

- **Target:** < 0.10 (≤ 10% of manifests are orphaned)
- **Flag threshold:** > 0.30 (nearly a third of agent outputs are wasted)
- **Composite weight:** 0.20 (highest weight in SI — most direct measure of stigmergy failure)

## Why It Matters

In a stigmergic system, manifests are the coordination medium. An orphaned manifest is equivalent to a pheromone trail that no ant followed — the signal degraded without effect. High OMR means the filesystem-as-message-bus is broken: agents are writing output but nothing downstream is reading it. This is the most direct indicator that coordination is happening through direct messaging or human brokering rather than through shared state.

## Collection

**Data source:** `~/.claude/hooks/state/wave*-result.json` glob. Citation detection via string-match in subsequent spawn prompts.
**Sampling:** Per session.
**Parser:** See `collectors/omr_collector.py`.

## Failure Modes

- **Proxy limitation:** Citation = path appears as string in later prompt. A path mentioned but not acted on counts as "read." This inflates OMR denominator, making OMR slightly optimistic.
- **Cross-session manifests:** A manifest written in session N read in session N+1 appears orphaned by session-scope counting. These feed into CSS instead.
- **Terminal manifests (by design):** A final-wave manifest may legitimately have no downstream — it's the end of the chain. Distinguish by checking CD; if CD ≥ 1, the manifest had downstream work; if CD = 0, terminal manifests should be excluded from OMR.

## Dashboard Query

```dataview
TABLE session_id, value, target, (value - 0.10) as delta
FROM "03-Baselines"
WHERE metric_id = "OMR"
SORT created DESC
LIMIT 10
```

## Related

- [[MPL-Manifest-Pickup-Latency]]
- [[CD-Cascade-Depth]]
- [[../SI-Stigmergy-Index]]
