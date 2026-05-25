---
type: shape
shape_id: charter.active.over_cap
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: false
cluster_prefix: ["charter", "active", "cap"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — charter.active.over_cap

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `charter.active.over_cap`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Excess active charters beyond max_active_charters (15). Measured as max(0, active_count - cap).

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_charter_active_over_cap` |
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
