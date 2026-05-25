---
type: shape
shape_id: manifest.orphan_mission
target_direction: decreasing
current_count: 0
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: true
cluster_prefix: ["manifest", "orphan", "mission"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — manifest.orphan_mission

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `manifest.orphan_mission`)
> Target direction: **decreasing** | Current count: **0** | Membench probe: **True**

---

## Description

Recent (rolling 24h) manifests whose mission field doesn't resolve to any active charter's cluster_prefix neighborhood (≥1-term overlap) OR an existing mission-graph node. Parent-commission rule violation.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 0 |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 2 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_manifest_orphan_mission` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-22T16:41:26 | 1 | orphan-detected | None |
| 2026-05-22T16:41:42 | 0 | test-rollback | None |

## Interpretation

<!-- What a count of 0 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
