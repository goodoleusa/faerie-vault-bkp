---
type: faerie-internal
subtype: formula
formula_id: mutation-fitness
formula_text: MF = (eval_after - eval_before) × dispersal_rate
category: evolution
canonical_source: /mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js
canonical_sha256: f347ccf6dbe377616207fcc9d24032d7c550d95657537dc25901ed59b8778fec
last_synced: '2026-05-19T15:24:06+00:00'
used_in: ['deploy/chat-mvp MissionSteer dashboard', 'session evals']
performance_window: 7d
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', '#category/evolution', '#path/transparency']
---

# Mutation Fitness

**ID:** `mutation-fitness`  **Category:** `evolution`

## Plain English

How much a mutation improved evals × how widely it spread.

## Formula

```
MF = (eval_after - eval_before) × dispersal_rate
```

## Output interpretation

>0 = beneficial; 0 = neutral; <0 = harmful (revert!)

## Pilot tip

> MF < 0 for two windows? Roll back the change. Don't hope.

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
if (latest) dv.paragraph('Latest eval ' + latest._date + ' — see system-eval.json for `mutation-fitness`-related signals.');
else dv.paragraph('No system-eval.json found in forensics/');
```

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
