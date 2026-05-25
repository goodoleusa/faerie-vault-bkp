---
type: shape
shape_id: jsx.closure_leak_to_sibling_component
target_direction: decreasing
current_count: 0
baseline_ts: "2026-05-25T01:30:00Z"
membench_probe: true
cluster_prefix: ["jsx", "closure", "leak"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — jsx.closure_leak_to_sibling_component

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `jsx.closure_leak_to_sibling_component`)
> Target direction: **decreasing** | Current count: **0** | Membench probe: **True**

---

## Description

A top-level React function component references an identifier (state, prop, callback, derived value) that is only in lexical scope inside a SIBLING function component — not the current one. Visually plausible because both components live in the same source file; structurally broken because each function has its own closure. Dev mode + HMR + non-minified bundles often hide the bug (the helper is rarely re-rendered with the offending branch active, or React preserves the name via fast-refresh state). Production minification ships the code unchanged, and the browser surfaces it as `ReferenceError: <name> is not defined` the first time the bad render path runs. Worked example (commit e75e8af5, 2026-05-25): TableGridGraph.jsx defined ColHeaders as a sibling component whose JSX read `colMode` — a state variable declared inside TableGridGraph's body. Vite build emitted the bundle clean; users hit the ReferenceError on first mission render. Fix: pass the identifier as an explicit prop. Decreasing target: every new instance is a regression and should fail pre-commit.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 0 |
| Baseline timestamp | 2026-05-25T01:30:00Z |
| Noise threshold | 1 |
| Detector script | `scripts/9x_chat_mvp_no_undef_gate.sh` |
| Membench probe | True |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| (no history entries yet) | | | |

## Interpretation

<!-- What a count of 0 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
