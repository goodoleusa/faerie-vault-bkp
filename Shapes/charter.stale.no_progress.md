---
type: shape
shape_id: charter.stale.no_progress
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: true
cluster_prefix: ["charter", "stale", "progress"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — charter.stale.no_progress

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `charter.stale.no_progress`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **True**

---

## Description

Active charters open >7 days with no new manifests_received[] entries (heartbeat lost).

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 1 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_charter_stale_no_progress` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| (no history entries yet) | | | |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
