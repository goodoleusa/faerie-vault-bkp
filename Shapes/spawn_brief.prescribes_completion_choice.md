---
type: shape
shape_id: spawn_brief.prescribes_completion_choice
target_direction: decreasing
current_count: 50
baseline_ts: "2026-05-25T00:30:00Z"
membench_probe: true
cluster_prefix: ["spawn", "brief", "prescribes"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — spawn_brief.prescribes_completion_choice

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `spawn_brief.prescribes_completion_choice`)
> Target direction: **decreasing** | Current count: **50** | Membench probe: **True**

---

## Description

Spawn briefs (Agent() prompts written by main, dispatcher, or peer agents) that include a pre-filled `free_choice` field or a `completion_choice` blob prescribing the agent's NEXT ACTION (e.g., 'completion_choice: { kind: "seal", ... }' or 'free_choice: { kind: "goodbye", ... }') instead of leaving the forward-looking choice to the agent. NOTE (2026-05-25 doctrine update): only `free_choice` pre-fills are violations. Pre-filling `lifecycle_judgment` (seal/verify/promote/refuse/decline/report_problem/discover) is ALLOWED — that is bookkeeping, not agency contamination. The 14-kind taxonomy distinguishes lifecycle_judgment (what happened — pre-fillable) from free_choice (what's next — never pre-fillable). Replace free_choice pre-fills with `acceptance_criteria` or `done_looks_like` prose. Decreases as authors adopt the corrected pattern.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 50 |
| Baseline timestamp | 2026-05-25T00:30:00Z |
| Noise threshold | 2 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_spawn_brief_prescribes_completion_choice` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| (no history entries yet) | | | |

## Interpretation

<!-- What a count of 50 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
