---
type: shape
shape_id: pair_session.viewer_token_class
target_direction: increasing
current_count: 0
baseline_ts: "2026-05-25T00:00:00Z"
membench_probe: true
cluster_prefix: ["pair-session", "viewer", "token"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — pair_session.viewer_token_class

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `pair_session.viewer_token_class`)
> Target direction: **increasing** | Current count: **0** | Membench probe: **True**

---

## Description

Viewer tokens minted and shared for a pair session. Each token represents a measurable read-only engagement event — someone consuming a live session without write access. Increasing count = more audience-mode usage of pair sessions.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | increasing |
| Current count | 0 |
| Baseline timestamp | 2026-05-25T00:00:00Z |
| Noise threshold | 0 |
| Detector script | `find forensics/users/*/pair-sessions/*/viewer-tokens.jsonl 2>/dev/null | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}'` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-25T00:00:00 | 0 | first-registration: viewer-mode shipped (ViewerModeContext + SessionTopBar viewer_token_mint). Canvas-voxel Cut G. | beneficial |

## Interpretation

<!-- What a count of 0 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
