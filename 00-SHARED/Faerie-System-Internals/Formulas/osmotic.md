---
type: faerie-internal
subtype: formula
formula_id: osmotic
formula_text: OP = (1 - context_fill_pct) × W1_capacity
category: physics
canonical_source: /mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js
canonical_sha256: f347ccf6dbe377616207fcc9d24032d7c550d95657537dc25901ed59b8778fec
last_synced: '2026-05-19T15:24:06+00:00'
used_in: ['deploy/chat-mvp MissionSteer dashboard', 'session evals']
performance_window: 7d
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', '#category/physics', '#path/transparency']
---

# Osmotic Potential

**ID:** `osmotic`  **Category:** `physics`

## Plain English

How much "fuel" is left for parallel spawn. High OP = cold tank, burn hot.

## Formula

```
OP = (1 - context_fill_pct) × W1_capacity
```

## Output interpretation

OP > 0.7 = W1 LIFTOFF; 0.35-0.7 = W2 CRUISE; <0.35 = W3 INSERTION

## Pilot tip

> Don't conserve OP in turn 1 — it never recovers without a /compact.

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
if (latest) dv.paragraph('Latest eval ' + latest._date + ' — see system-eval.json for `osmotic`-related signals.');
else dv.paragraph('No system-eval.json found in forensics/');
```

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
