---
type: faerie-internal
subtype: formula
formula_id: piston-velocity
formula_text: PV = (W1_spawns + W2_spawns + W3_spawns) / session_minutes
category: velocity
canonical_source: /mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js
canonical_sha256: f347ccf6dbe377616207fcc9d24032d7c550d95657537dc25901ed59b8778fec
last_synced: '2026-05-19T15:24:06+00:00'
used_in: ['deploy/chat-mvp MissionSteer dashboard', 'session evals']
performance_window: 7d
N: '[Formulas Index](00-Formulas-Index.md)'
E: []
tags: ['internal', 'formula', '#category/velocity', '#path/transparency']
---

# Piston Velocity (flywheel)

**ID:** `piston-velocity`  **Category:** `velocity`

## Plain English

Total spawn rate. The faster the flywheel spins, the more momentum.

## Formula

```
PV = (W1_spawns + W2_spawns + W3_spawns) / session_minutes
```

## Output interpretation

Spawns/min — feed this directly into the flywheel speedometer.

## Pilot tip

> PV plateauing? Either you've hit a context wall (compact!) or the swarm is busy synthesizing (let it).

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
if (latest) dv.paragraph('Latest eval ' + latest._date + ' — see system-eval.json for `piston-velocity`-related signals.');
else dv.paragraph('No system-eval.json found in forensics/');
```

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/deploy/chat-mvp/src/config/formulas.js`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
