---
type: faerie-internal
subtype: formula
formula_id: M14
formula_text: 
category: membench
canonical_source: /mnt/d/0local/gitrepos/membench/scoring_definitions.json
canonical_sha256: e69a062ee613d3b9ca53d89ec6b98e860aecb38c9d8297b3ce9d06dc8a11b350
last_synced: '2026-05-19T15:24:06+00:00'
performance_window: session
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', 'membench', '#metric/M14', '#path/transparency']
---

# M14 — Spawn Leverage Ratio

**Category:** operational-efficiency  
**Weight in composite:** 0.08

## What it measures

The cost-benefit ratio of spawning agents: how many tokens of value (measured by manifest work output) are produced per token spent on spawn overhead (bundle rendering, agent invocation, manifest parsing, coordination). High ratio = efficient spawn. Low ratio = overhead exceeds benefit.

## Formula

```

```

### Components

- **agent_work_value_tokens** — Estimated value produced by agents: sum of (task_complexity × task_count) for completed work. Baseline: 50K-100K tokens per agent (measured from manifest outputs). Conservative estimate: count unique discovered_work[] items × 10K tokens each.
- **spawn_overhead_tokens** — Total tokens consumed by spawn machinery: bundle rendering (manifest context injection, HONEY loading, frontier snapshot) + agent invocation (API call overhead, context window negotiation) + manifest parsing (agent reading manifests to discover work) + coordination (agent cross-referencing manifests). Measured directly from spawn.py metrics + Agent API logs.

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/membench/scoring_definitions.json`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
