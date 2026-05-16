---
type: metric-definition
status: active
created: 2026-04-20
tags: [metric, si, cd]
metric_id: CD
suite: SI
target: "≥ 2"
flag_threshold: "0"
weight_in_composite: 0.05
parent: ["[[../SI-Stigmergy-Index]]"]
up: "[[../_INDEX.md]]"
sibling: ["[[OMR-Orphaned-Manifest-Rate]]", "[[SDR-Stigmergic-Discovery-Rate]]"]
child: []
doc_hash: sha256:9d5d8b82fb44233707e44fb055e023d2987f8b7ff0d52cb52a5df53c9334433d
hash_ts: 2026-04-20T21:59:34Z
hash_method: body-sha256-v1
---

> [↑ SI](../SI-Stigmergy-Index.md) · [⌂ Metrics Index](../_INDEX.md) · [📊 Dashboard](../../02-Dashboards/Session-Health.md)

# CD — Cascade Depth

## Definition

Maximum agent chain length triggered by a single manifest file, measured via the `triggered_by` field chain-walk. A depth of 2 means: root manifest → agent A triggered → agent B triggered by A's manifest.

## Formula

```python
def cascade_depth(root_manifest_path, all_manifests):
    depth = 0
    current = root_manifest_path
    while True:
        children = [m for m in all_manifests if m.triggered_by == current]
        if not children: return depth
        depth += 1
        branch_depths = [cascade_depth(child.path, all_manifests) for child in children]
        return depth + max(branch_depths)
```

## Target

- **Target:** ≥ 2 (at least one two-step autonomous chain per session)
- **Flag threshold:** 0 (every agent chain was manually initiated — no autonomous propagation)
- **Composite weight:** 0.05 (low weight because CD = 0 is common early in adoption)

## Why It Matters

CD is the clearest evidence that stigmergy is doing real work. A cascade depth of 2 means a manifest not only triggered downstream work, but that downstream work triggered further work — without human intervention. This is the compounding behavior that justifies the whole architecture.

CD = 0 means the system is running as a flat sequence of manually-dispatched agents. The piston exists but it's hand-cranked.

## Collection

**Data source:** All `wave*-result.json` manifests with `triggered_by` field.
**Requires:** Manifest schema v2. See `collectors/cd_collector.py`.

## Failure Modes

- **Schema v1 sessions:** Before `triggered_by` was added, all manifests show CD = 0 by default. Do not interpret as "stigmergy broken"; flag as `schema_v1_session: true`.
- **Cycle guard:** Defend against circular `triggered_by` chains (should not occur architecturally, but can happen during debugging). `cd_collector.py` tracks visited set.

## Dashboard Query

```dataview
TABLE session_id, value, target
FROM "03-Baselines"
WHERE metric_id = "CD"
SORT created DESC
LIMIT 10
```

## Related

- [[OMR-Orphaned-Manifest-Rate]]
- [[SDR-Stigmergic-Discovery-Rate]]
- [[../../04-Methods/Manifest-Schema-v2]]
- [[../SI-Stigmergy-Index]]
