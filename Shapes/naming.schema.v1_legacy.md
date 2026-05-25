---
type: shape
shape_id: naming.schema.v1_legacy
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: false
cluster_prefix: ["naming", "schema", "legacy"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — naming.schema.v1_legacy

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `naming.schema.v1_legacy`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Manifest filenames still using v1 schema ({ts}__{task_id}_{agent}_{mission}_{sid}.json) instead of v2 ({ts}__{w3w}__{charter-slug}__{task_id}_{agent}.json). Decreases as agents migrate to v2 writer.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 5 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_naming_schema_v1_legacy` |
| Membench probe | False |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| (no history entries yet) | | | |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
