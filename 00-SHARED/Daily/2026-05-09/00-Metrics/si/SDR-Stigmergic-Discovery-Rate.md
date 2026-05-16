---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, sdr]
metric_id: SDR
suite: SI
target: "≥ 0.80"
flag_threshold: "< 0.50"
weight_in_composite: 0.20
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[OMR-Orphaned-Manifest-Rate]]", "[[CMR-Coordination-Message-Ratio]]"]
child: []
doc_hash: sha256:38c09e260b2fd266a6332c4d859cd601e67c26491fa3211d61f87ffb6162a922
hash_ts: 2026-04-20T21:59:35Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# SDR — Stigmergic Discovery Rate

## Definition

Fraction of agent tasks where the agent self-discovered at least one input file rather than being explicitly told every path in its spawn prompt. Measures whether agents are navigating the filesystem autonomously.

## Formula

```
SDR = tasks_where_agent_self_discovered_inputs / total_scoreable_tasks
```

A task is "scoreable" only when the manifest includes a `files_read` field (schema v2+).

## Target

- **Target:** ≥ 0.80 (80% of tasks include at least one self-discovered read)
- **Flag threshold:** < 0.50 (majority of agents were fully told where to look)
- **Composite weight:** 0.20 (tied with OMR for highest SI weight — core stigmergy behavior)

## Why It Matters

If every agent is told exactly where to find its inputs, the spawn prompt is doing the coordination that the filesystem should be doing. Agents become dependent on the spawning session knowing and enumerating all relevant paths at spawn time — which doesn't scale. True stigmergy means agents know the conventions (where wave*-result.json files live, where broadcast.jsonl lives, where their upstream sibling's manifest will be) and navigate there without being directed.

SDR is the self-sufficiency metric: can agents find their own food?

## Collection

**Data source:** `wave*-input.json` (prompt paths) vs `manifest.files_read` (actual reads). See `collectors/sdr_collector.py`.
**Sampling:** Per agent run where `files_read` is present.
**Requires:** Manifest schema v2 (`files_read` field). Schema v1 manifests are excluded (not penalized).

**Proxy limitation:** Self-discovery is inferred from path comparison, not from reading the agent's reasoning. An agent directed to a directory and navigating within it counts as told (the directory hint directed discovery). A strict reading of "self-discovery" would require zero path hints — but that bar is too high for practical measurement.

## Failure Modes

- **False negative (SDR deflated):** Agent was given a hint ("check wave results from today") that isn't a literal path, navigated to the right files. This reads as self-discovered (no literal path in prompt matches the file found). Acceptable — the navigation was non-trivial.
- **False positive (SDR inflated):** Agent was given directory A and read files under directory A. Technically not in prompt paths but not "discovered" either. Mitigate: if read path is a child of any prompted path, count as told.
- **Schema v1 blind spot:** Sessions before schema v2 was adopted will show `SDR = null`. Do not impute; report null with note.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "SDR"
SORT created DESC
LIMIT 10
```

## Related

- [[OMR-Orphaned-Manifest-Rate]]
- [[CMR-Coordination-Message-Ratio]]
- [[../../04-Methods/Manifest-Schema-v2]]
- [[../SI-Stigmergy-Index]]
