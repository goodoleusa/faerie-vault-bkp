---
type: shape
shape_id: manifest.discovered_work.shape_missing
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: false
cluster_prefix: ["manifest", "discovered-work", "shape"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — manifest.discovered_work.shape_missing

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `manifest.discovered_work.shape_missing`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Entries in manifest._evolution_log[] that target a shape but lack the `shape` field (or shape doesn't resolve to a registered shape).

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_evolution_log_shape_missing` |
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
