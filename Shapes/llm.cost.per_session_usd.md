---
type: shape
shape_id: llm.cost.per_session_usd
target_direction: bounded
current_count: null
baseline_ts: "2026-05-25T22:00:00Z"
membench_probe: true
cluster_prefix: ["llm", "cost", "session"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — llm.cost.per_session_usd

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `llm.cost.per_session_usd`)
> Target direction: **bounded** | Current count: **None** | Membench probe: **True**

---

## Description

Rolling 7-day windowed median USD cost per Claude Code session. Derived from forensics/api-usage/claude-code/{date}/session-*.json rollups produced by 9x_claude_token_aggregator.py. Target: bounded — operator sets a cost ceiling; sessions above the P90 are flagged for context efficiency review. A rising median signals increasing session complexity or reduced cache efficiency. Reference baseline: ~$262/session for heavy sonnet-4 sessions (98% cache reads), ~$1,558 for the largest observed session.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | bounded |
| Current count | None |
| Baseline timestamp | 2026-05-25T22:00:00Z |
| Noise threshold | 5 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_llm_cost_per_session_usd` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-25T22:00:00 | None | shape declared by token-instrumentor agent (collab wave: pdf-tokens-wandb) | None |

## Interpretation

<!-- What a count of None means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
