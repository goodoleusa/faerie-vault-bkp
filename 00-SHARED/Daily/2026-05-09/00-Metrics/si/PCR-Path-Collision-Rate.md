---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, pcr]
metric_id: PCR
suite: SI
target: "0"
flag_threshold: "> 0.05"
weight_in_composite: 0.05
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[CD-Cascade-Depth]]", "[[SDR-Stigmergic-Discovery-Rate]]"]
child: []
doc_hash: sha256:54b56052c7c2f22fe2b20dc7a1a952d19bb40364ff4627ddc4028ab3ba6d6d7d
hash_ts: 2026-04-20T21:59:35Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# PCR — Path Collision Rate

## Definition

Fraction of agent writes that land on a path already written by a different agent in the same session. A collision means two agents claimed the same file — a race condition and a coordination failure.

## Formula

```
PCR = writes_to_overlapping_paths / total_agent_writes
```

## Target

- **Target:** 0 (zero collisions — file ownership is disjoint)
- **Flag threshold:** > 0.05 (more than 5% of writes are contested)
- **Composite weight:** 0.05

## Why It Matters

The stigmergic model requires that file ownership is exclusive. Two agents writing to the same manifest path corrupt each other's output — the second write overwrites the first, and the chain-walk that reads `triggered_by` may see the wrong ancestor. PCR = 0 is not aspirational; it's a correctness requirement. Any nonzero PCR is a bug in spawn orchestration.

## Collection

**Data source:** All manifest `files_written` arrays across all agents in session.
**Sampling:** Per session.
**Parser:** Group by path; any path in 2+ different agents' `files_written` = collision.

## Failure Modes

- **Progressive manifest writes:** Same agent writes its manifest multiple times (in-progress → draft → final). These are NOT collisions — same agent, same path.
- **Intentional overwrite pattern:** Some workflows have agent B explicitly replacing agent A's intermediate file (e.g., upgrading a draft). This should be modeled as a `triggered_by` chain, not a collision. If `triggered_by` relationship exists between the agents, exclude from PCR.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "PCR"
SORT created DESC
LIMIT 10
```

## Related

- [[CD-Cascade-Depth]]
- [[SDR-Stigmergic-Discovery-Rate]]
- [[../SI-Stigmergy-Index]]
