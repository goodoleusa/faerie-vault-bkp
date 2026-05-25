---
type: shape
shape_id: llm.tokens.uninstrumented_call
target_direction: decreasing
current_count: null
baseline_ts: "2026-05-25T22:00:00Z"
membench_probe: true
cluster_prefix: ["llm", "tokens", "uninstrumented"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — llm.tokens.uninstrumented_call

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `llm.tokens.uninstrumented_call`)
> Target direction: **decreasing** | Current count: **None** | Membench probe: **True**

---

## Description

Count of LLM completion calls in production that did NOT produce a forensic token log entry. Measured by comparing call counts in the MCP request log (api-usage/calls.jsonl) against token log entries (forensics/api-usage/openhands/{date}/llm-calls.jsonl). A non-zero count means token cost data is missing for those calls. Target: decreasing toward zero — every production call should have a forensic entry. Gap can arise if llm_token_logger.py is not wired, litellm version mismatch, or async exception in callback.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | None |
| Baseline timestamp | 2026-05-25T22:00:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_llm_tokens_uninstrumented_call` |
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
