---
type: shape
shape_id: crystallization.discipline.violations
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-23T00:00:00Z"
membench_probe: false
cluster_prefix: ["crystallization", "discipline", "violations"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — crystallization.discipline.violations

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `crystallization.discipline.violations`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Daily count of manifests violating spray->tighten->crystallize discipline (>3 files in files_created[], scratch/draft in production filenames, non-canonical filenames)

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-23T00:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_crystallization_violations` |
| Membench probe | False |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-23T23:55:00 | 0 | shape declared by bulkheads-impl-w1 MAKER-CRYSTAL | None |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
