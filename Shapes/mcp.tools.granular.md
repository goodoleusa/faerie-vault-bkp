---
type: shape
shape_id: mcp.tools.granular
target_direction: decreasing
current_count: 75
baseline_ts: "2026-05-22T11:00:00Z"
membench_probe: true
cluster_prefix: ["mcp", "tools", "granular"]
applicable_repos: ["faerie2", "swarmy-hive-plugin"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — mcp.tools.granular

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `mcp.tools.granular`)
> Target direction: **decreasing** | Current count: **75** | Membench probe: **True**

---

## Description

MCP tools that should be verb-dispatcher-merged. Each instance is a stand-alone @mcp.tool() that could fold into a verb-dispatch wrapper.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 75 |
| Baseline timestamp | 2026-05-22T11:00:00Z |
| Noise threshold | 1 |
| Detector script | `deploy/scripts/lint-mcp-tools.sh` |
| Membench probe | True |
| Applicable repos | faerie2, swarmy-hive-plugin |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-22T16:41:36 | 60 | 1 | beneficial |
| 2026-05-22T16:41:42 | 75 | test-rollback | None |

## Interpretation

<!-- What a count of 75 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
