---
type: shape
shape_id: sanitization.audit.coverage
target_direction: increasing
current_count: 7
baseline_ts: "2026-05-23T23:30:00Z"
membench_probe: true
cluster_prefix: ["sanitization", "audit", "coverage"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — sanitization.audit.coverage

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `sanitization.audit.coverage`)
> Target direction: **increasing** | Current count: **7** | Membench probe: **True**

---

## Description

Count of distinct (direction, source-class) tuples covered by sanitization audit log on the most-recent day. Target=increasing: more coverage = more places where bidirectional sanitization is observable + provable. Bulkhead 2 instrumentation health.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | increasing |
| Current count | 7 |
| Baseline timestamp | 2026-05-23T23:30:00Z |
| Noise threshold | 0 |
| Detector script | `scripts/shapes/audit-shapes.py::detect_sanitization_audit_coverage` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-23T23:30:00 | 0 | shape declared by bulkheads-impl-w1 MAKER-B | None |
| 2026-05-23T23:56:29 | 7 | audit-shapes-cron | neutral |
| 2026-05-23T23:57:46 | 7 | audit-shapes-cron | neutral |

## Interpretation

<!-- What a count of 7 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
