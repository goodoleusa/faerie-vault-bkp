---
type: faerie-internal
subtype: formula
formula_id: M13
formula_text: 
category: membench
canonical_source: /mnt/d/0local/gitrepos/membench/scoring_definitions.json
canonical_sha256: e69a062ee613d3b9ca53d89ec6b98e860aecb38c9d8297b3ce9d06dc8a11b350
last_synced: '2026-05-19T15:24:06+00:00'
performance_window: session
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', 'membench', '#metric/M13', '#path/transparency']
---

# M13 — Emergence Scoring (Qualitative Depth)

**Category:** autonomy  
**Weight in composite:** 0.08

## What it measures

The depth of reasoning and cross-domain understanding in discovered work: insight_density (unique concepts per discovery), cross_domain_ratio (fraction of discoveries that bridge multiple domains), novelty_score (whether discovery represents new thinking vs. rote assignment execution). Extended formula: 65% structural (M12) + 35% qualitative (M13) = complete Emergence Scoring.

## Formula

```

```

### Components

- **insight_density** — Number of distinct actionable concepts encoded per discovered work item, normalized to [0, 1]. Measured via LLM rubric or human review. Each discovery scored 0-5; normalized to [0, 1].
- **cross_domain_ratio** — Fraction of discovered work items that reference or integrate across 2+ knowledge domains (e.g., 'refactor database schema (backend) to support new UI layout (frontend)'). Range [0, 1]. Domain boundary: architectural layer shift (frontend/backend/infra/security/etc.).
- **novelty_score** — Does the discovery represent original thinking (novel synthesis of existing knowledge, new approach to known problem) vs. rote extension of assignment? LLM-scored [0, 1] via rubric: 0=rote execution, 0.5=incremental, 1.0=genuinely novel synthesis.

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/membench/scoring_definitions.json`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
