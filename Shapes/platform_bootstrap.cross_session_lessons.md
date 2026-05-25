---
type: shape
shape_id: platform_bootstrap.cross_session_lessons
target_direction: increasing
current_count: 9
baseline_ts: "2026-05-25T00:30:00Z"
membench_probe: true
cluster_prefix: ["platform", "bootstrap", "lessons"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — platform_bootstrap.cross_session_lessons

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `platform_bootstrap.cross_session_lessons`)
> Target direction: **increasing** | Current count: **9** | Membench probe: **True**

---

## Description

Distinct doctrinal lessons crystallized from session manifests that ALL future spawn briefs / agent cards / charter authoring should reference. Examples (from 2026-05-24 session): always-mounted drawers > conditional React mounts (SSE survives toggles); mockMode first-class on viz components; 2-tier loading (index + keyword trigger) for token efficiency; @mcp.tool() is factory call; SSE handles must precede /api/* catch-all in Caddy; HMAC + sha256 for zero-knowledge auth; charter status DERIVED from signed manifest count, not manually edited; spawn briefs use acceptance_criteria not pre-filled completion_choice; verb-dispatcher MCP pattern > many single-verb tools. Increases over time as the platform's institutional memory crystallizes into reusable patterns. Detector: count of references to .agents/skills/*/SKILL.md doctrinal sections from new spawn briefs + new agent cards + new charter pre-registrations.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | increasing |
| Current count | 9 |
| Baseline timestamp | 2026-05-25T00:30:00Z |
| Noise threshold | 1 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_platform_bootstrap_pattern_references` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| (no history entries yet) | | | |

## Interpretation

<!-- What a count of 9 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
