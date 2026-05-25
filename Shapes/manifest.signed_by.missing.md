---
type: shape
shape_id: manifest.signed_by.missing
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: true
cluster_prefix: ["manifest", "signed_by", "missing"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — manifest.signed_by.missing

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `manifest.signed_by.missing`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **True**

---

## Description

Manifests written without signer + signed_by — the basic agent-lifecycle violation.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/audit-unsigned-manifests.py` |
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
