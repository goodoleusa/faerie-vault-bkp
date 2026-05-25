---
type: shape
shape_id: crystallization.discipline.clean_rate
target_direction: increasing
current_count: null
baseline_ts: "2026-05-23T00:00:00Z"
membench_probe: true
cluster_prefix: ["crystallization", "discipline", "clean-rate"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — crystallization.discipline.clean_rate

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `crystallization.discipline.clean_rate`)
> Target direction: **increasing** | Current count: **None** | Membench probe: **True**

---

## Description

Daily fraction of manifests passing crystallization discipline (1.0 = perfect; 0.0 = nothing crystallized cleanly). Stored as integer percent 0-100 to fit non-negative-int schema; downstream consumers divide by 100.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | increasing |
| Current count | None |
| Baseline timestamp | 2026-05-23T00:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_crystallization_clean_rate` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-23T23:55:00 | 0 | shape declared by bulkheads-impl-w1 MAKER-CRYSTAL | None |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
