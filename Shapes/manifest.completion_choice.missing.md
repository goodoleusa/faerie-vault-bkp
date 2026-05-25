---
type: shape
shape_id: manifest.completion_choice.missing
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-24T00:00:00Z"
membench_probe: true
cluster_prefix: ["manifest", "completion-choice", "missing"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — manifest.completion_choice.missing

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `manifest.completion_choice.missing`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **True**

---

## Description

Manifests from overhauled agent types (post-2026-05-24) that lack the completion_choice field (kind + reason). The 6-Choices ritual is mandatory for all overhauled agent types. Decreases as agents adopt the ritual. Backward compat: pre-overhaul manifests excluded.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-24T00:00:00Z |
| Noise threshold | 2 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_manifest_completion_choice_missing` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-24T00:00:00 | 0 | shape declared by agent-type-overhaul knowledge-synthesizer | None |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
