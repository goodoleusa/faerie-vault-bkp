---
type: faerie-internal
subtype: formula
formula_id: dim-G-emergence
category: eval-dimension
canonical_source: /mnt/d/0local/gitrepos/faerie2/scripts/eval_harness.py
canonical_sha256: 199bc6c6eba20ddb5057456253fbe9b4cafaed1f916096b8317e8c0a023d252d
last_synced: '2026-05-19T15:24:06+00:00'
used_in: ['scripts/eval_harness.py', 'forensics/{date}/system-eval.json']
performance_window: 7d
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', 'eval-dimension', '#dim/g', '#path/transparency']
---

# Dimension G — Emergence

One of seven daily system-health dimensions computed by `scripts/eval_harness.py`. Result lands in `forensics/{date}/system-eval.json` under a key starting with `G_`.

## Computation entrypoint

`compute_dimension_g_emergence(date)` in `eval_harness.py`.

## Where each input comes from

Inputs are read from manifest fields (forensics/manifests/{date}/), COC entries (forensics/coc.jsonl), and prior baselines (forensics/baselines/). See the source for the exact field paths.

## Live performance

Open `forensics/{latest-date}/system-eval.json` and look at the matching dimension key.

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/scripts/eval_harness.py`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
