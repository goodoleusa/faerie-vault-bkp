---
type: faerie-internal
subtype: formula
formula_id: emergence-health
formula_text: EH = mean( cohort_eval_scores ) × (1 + cognitive_diversity_bonus)
category: emergence
canonical_source: /mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js
canonical_sha256: f347ccf6dbe377616207fcc9d24032d7c550d95657537dc25901ed59b8778fec
last_synced: '2026-05-19T15:24:06+00:00'
used_in: ['deploy/chat-mvp MissionSteer dashboard', 'session evals']
performance_window: 7d
N: '[Formulas Index](00-Formulas-Index.md)'
E: ['[f0](f0.md)']
tags: ['internal', 'formula', '#category/emergence', '#path/transparency']
---

# Emergence Health

**ID:** `emergence-health`  **Category:** `emergence`

## Plain English

Average eval across the most recent cohort, with a bonus for multi-bearing teams.

## Formula

```
EH = mean( cohort_eval_scores ) × (1 + cognitive_diversity_bonus)
```

## Output interpretation

≥0.87 = healthy swarm (validated baseline)

## Pilot tip

> Below 0.87? Spawn more bearings. Add a DEEP-DIVER if too many MAKERs.

## Live performance

```dataviewjs
const fs = require('fs');
const path = require('path');
const root = '/mnt/d/0local/gitrepos/faerie2/forensics';
let latest = null;
try {
  const dirs = fs.readdirSync(root).filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d)).sort().reverse();
  for (const d of dirs) {
    const f = path.join(root, d, 'system-eval.json');
    if (fs.existsSync(f)) { latest = JSON.parse(fs.readFileSync(f, 'utf-8')); latest._date = d; break; }
  }
} catch (e) { dv.paragraph('eval read error: ' + e.message); }
if (latest) dv.paragraph('Latest eval ' + latest._date + ' — see system-eval.json for `emergence-health`-related signals.');
else dv.paragraph('No system-eval.json found in forensics/');
```

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
