---
type: shape
shape_id: multi_agent.realtime_collab.blackboard
target_direction: increasing
current_count: 1
baseline_ts: "2026-05-25T00:00:00Z"
membench_probe: true
cluster_prefix: ["multi-agent", "realtime", "blackboard"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — multi_agent.realtime_collab.blackboard

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `multi_agent.realtime_collab.blackboard`)
> Target direction: **increasing** | Current count: **1** | Membench probe: **True**

---

## Description

Parallel agents coordinate via append-only JSONL blackboard with CLAIM/COMPLETE/HANDOFF event grammar instead of file-collision-prone independent claims. Increasing count = more waves successfully using the pattern.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | increasing |
| Current count | 1 |
| Baseline timestamp | 2026-05-25T00:00:00Z |
| Noise threshold | 0 |
| Detector script | `ls forensics/manifests/*/collab-realtime__*.jsonl 2>/dev/null | wc -l` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-25T00:00:00 | 1 | first-blackboard-instance: commit 07daafe0 VISIONARY+ARTISAN collab wave | beneficial |

## Interpretation

<!-- What a count of 1 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
