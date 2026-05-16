---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, bpr]
metric_id: BPR
suite: SI
target: "≥ 0.70"
flag_threshold: "< 0.30"
weight_in_composite: 0.10
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[CMR-Coordination-Message-Ratio]]", "[[CSS-Cross-Session-Signal-Survival]]"]
child: []
doc_hash: sha256:cc40df84094394bcd00802451bfb831e99ea6887bd85602ffa935c673474f61e
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# BPR — Broadcast Propagation Rate

## Definition

Fraction of `#shared` droplets written by agents that are read by at least one sibling agent in the same or following wave.

## Formula

```
BPR = #shared_droplets_read_by_at_least_one_sibling / #shared_droplets_written
```

## Target

- **Target:** ≥ 0.70 (70% of broadcast signals reach at least one sibling)
- **Flag threshold:** < 0.30 (broadcast system mostly non-functional)
- **Composite weight:** 0.10

## Why It Matters

The broadcast mechanism (`#shared` droplet → `broadcast.jsonl` → sibling reads at curiosity checkpoints) enables cross-pollination between parallel agents. When it works, agent A's insight can redirect agent B without either going through the main session. When BPR is low, parallel agents work in informational isolation — each discovering the same things independently, or missing each other's blockers.

BPR is the only metric that directly measures whether the lateral coordination channel is live.

## Collection

**Data source:** `broadcast.jsonl` for written signals; sibling agent `manifest.files_read` or `broadcast_scan` hook logs for reads.
**Sampling:** Per session where parallel agents (same-wave) exist.
**Requires:** At least 2 concurrent agents in the session. If single-agent: metric is undefined.

## Failure Modes

- **Timing:** Sibling B may complete before sibling A writes its broadcast droplet. This is not a BPR failure — it's a timing issue. Distinguish by checking wave start times. If sibling B finished before sibling A wrote the droplet, exclude from BPR denominator.
- **Curiosity checkpoint frequency:** Agents that never call `9x_broadcast_scan.py` can't receive broadcasts. Low BPR may diagnose checkpoint discipline rather than broadcast infrastructure.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "BPR"
SORT created DESC
LIMIT 10
```

## Related

- [[CMR-Coordination-Message-Ratio]]
- [[CSS-Cross-Session-Signal-Survival]]
- [[../SI-Stigmergy-Index]]
