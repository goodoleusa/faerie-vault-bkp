---
type: faerie-internal
subtype: formula
formula_id: M12
formula_text: EMG_struct = (edge_density × 0.35) + (clustering × 0.30) + (linearity × 0.25) + ((1 - W_ratio) × 0.10)
category: membench
canonical_source: /mnt/d/0local/gitrepos/membench/scoring_definitions.json
canonical_sha256: e69a062ee613d3b9ca53d89ec6b98e860aecb38c9d8297b3ce9d06dc8a11b350
last_synced: '2026-05-19T15:24:06+00:00'
performance_window: session
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', 'membench', '#metric/M12', '#path/transparency']
---

# M12 — Emergence Scoring (Structural)

**Category:** autonomy  
**Weight in composite:** 0.12

## What it measures

The quality and autonomy of work discovery: agents identify prerequisite unblocking (N), downstream deliverables (S), parallel work (E), and baseline re-verification (W) using compass-bearing navigation. Structural component (M12) = 65% of emergence score (formula-derived).

## Formula

```
EMG_struct = (edge_density × 0.35) + (clustering × 0.30) + (linearity × 0.25) + ((1 - W_ratio) × 0.10)
```

### Components

- **edge_density** — Fraction of manifest entries that carry discovered_work[] entries with bearing assignments (N/S/E/W). Range [0, 1]. Measured: (entries_with_bearings / total_manifests).
- **clustering** — Cross-agent citation rate within mission boundaries (M6). How frequently agents read each other's discoveries and claim follow-up work. Normalized to [0, 1].
- **linearity** — Degree to which compass bearings form a coherent DAG without cycles or backtracking. Measured via topological sort feasibility. Range [0, 1]; 1.0 = pure DAG.
- **W_ratio** — Fraction of discovered work with W-bearing (backtrack/assumption-reversal). Inverted (1 - W_ratio) because excessive backtracking signals design fragility. Threshold: >5% W-bearings = caution.

## Validation history

> 2026-05-03: EMG_struct formula validated against Phase C mission-field-wire agent run. Predicted: 0.79 (from phase-B baseline). Actual: 0.97 (measured post-run). Correlation: 0.87. Validated for adoption.

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/membench/scoring_definitions.json`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
