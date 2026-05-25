---
type: shape
shape_id: charter.cluster_prefix.violations
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: false
cluster_prefix: ["charter", "cluster-prefix", "schema"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — charter.cluster_prefix.violations

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `charter.cluster_prefix.violations`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Active charters whose cluster_prefix is not exactly 3 atomic terms (length != 3 OR kebab-stack masquerade).

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_charter_cluster_prefix_violations` |
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
