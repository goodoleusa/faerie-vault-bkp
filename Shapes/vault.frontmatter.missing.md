---
type: shape
shape_id: vault.frontmatter.missing
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-22T12:00:00Z"
membench_probe: false
cluster_prefix: ["vault", "frontmatter", "missing"]
applicable_repos: ["faerie2", "faerie-vault"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — vault.frontmatter.missing

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `vault.frontmatter.missing`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **False**

---

## Description

Vault narrative .md files lacking a YAML frontmatter block (---...---) at line 1.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-22T12:00:00Z |
| Noise threshold | 1 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_vault_frontmatter_missing` |
| Membench probe | False |
| Applicable repos | faerie2, faerie-vault |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| (no history entries yet) | | | |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
