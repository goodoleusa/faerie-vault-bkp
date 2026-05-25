---
type: shape
shape_id: cluster_prefix.length_violation
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: false
cluster_prefix: ["cluster-prefix", "length", "violation"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — cluster_prefix.length_violation

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `cluster_prefix.length_violation`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Any artifact carrying a cluster_prefix array whose length is not exactly 3. Schema mandate.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_cluster_prefix_length_violation` |
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
