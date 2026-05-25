---
type: shape
shape_id: hook.coverage.gap
target_direction: decreasing
current_count: 0
baseline_ts: "2026-05-23T00:00:00Z"
membench_probe: true
cluster_prefix: ["hook", "coverage", "gap"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — hook.coverage.gap

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `hook.coverage.gap`)
> Target direction: **decreasing** | Current count: **0** | Membench probe: **True**

---

## Description

PostSpawn / PreSpawn lifecycle boundaries where a hook SHOULD fire (per .openhands/hooks.json contract) but no hook script is wired. Each gap is one missing observer in the swarmy lifecycle. Target: zero gaps = full closure of the evolve↔spawn feedback loop.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 0 |
| Baseline timestamp | 2026-05-23T00:00:00Z |
| Noise threshold | 0 |
| Detector script | `.openhands/hooks/8x_hook-roster-update.py` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-23T23:30:00 | 0 | bulkheads-impl-w1: wired 2x_hook-sanitize-{outgoing,incoming}.py | beneficial |

## Interpretation

<!-- What a count of 0 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
