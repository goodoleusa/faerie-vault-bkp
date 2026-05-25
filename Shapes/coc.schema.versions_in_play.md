---
type: shape
shape_id: coc.schema.versions_in_play
target_direction: decreasing
current_count: 1
baseline_ts: "2026-05-25T19:54:31Z"
membench_probe: true
cluster_prefix: ["coc", "schema", "unification"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — coc.schema.versions_in_play

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `coc.schema.versions_in_play`)
> Target direction: **decreasing** | Current count: **1** | Membench probe: **True**

---

## Description

Number of distinct COC schemas being actively walked. v1 (legacy hash/prev) + v2 (entry_hash/prev_entry_hash) = 2 pre-genesis. After genesis-seal: 1 (v2 only; v1 frozen + verified via archive walker). Target: 1.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 1 |
| Baseline timestamp | 2026-05-25T19:54:31Z |
| Noise threshold | 0 |
| Detector script | `` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-19T00:00:00 | 3 | initial v1 ledger: bare genesis entries + legacy hash/prev + entry_hash/prev_entry_hash all co-present | None |
| 2026-05-25T19:54:31 | 1 | genesis-seal (9x_coc_genesis_seal.py): v1 frozen read-only, v2 chain initialized with unified schema | beneficial |

## Interpretation

<!-- What a count of 1 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
