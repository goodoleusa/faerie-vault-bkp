---
type: shape
shape_id: manifest.cognitive_blindspot.missing
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-24T00:00:00Z"
membench_probe: false
cluster_prefix: ["manifest", "cognitive-blindspot", "missing"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — manifest.cognitive_blindspot.missing

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `manifest.cognitive_blindspot.missing`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Manifests from overhauled specialist agent types (post-2026-05-24) that lack the cognitive_blindspot_acknowledged field. This field is the mutual grooming signal — it tells peer agents where to apply scrutiny. Archetypes (bridge/maker/navigator/deep-diver) have this in their manifest contract but as free-form prose, not as a named field. Specialist types (python-pro, data-scientist, etc.) must emit it explicitly.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-24T00:00:00Z |
| Noise threshold | 3 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_manifest_cognitive_blindspot_missing` |
| Membench probe | False |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-24T00:00:00 | 0 | shape declared by agent-type-overhaul knowledge-synthesizer | None |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
