---
type: faerie-internal
subtype: index
last_synced: '2026-05-19T15:24:06+00:00'
N: '[Faerie System Internals Home](../00-Home.md)'
tags: ['internal', 'index', 'formulas', '#path/transparency']
---

# Formulas Index

Every formula that drives swarm behavior + health scoring, in one place.

```dataview
TABLE formula_id AS "ID", category AS "Category", formula_text AS "Formula"
FROM "00-SHARED/Faerie-System-Internals/Formulas"
WHERE subtype = "formula"
SORT category ASC, formula_id ASC
```

## Categories

- **emergence** — f(0) queen burden, swarm health
- **physics** — osmotic potential, piston dynamics
- **leverage** — subagent vs main token ratio
- **evolution** — mutation fitness
- **velocity** — piston spawn rate
- **memory** — T+1 retention, NECTAR/HONEY recall
- **eval-dimension** — daily A–G system health dimensions (`scripts/eval_harness.py`)
- **membench** — M12–M15 memory-system metrics (`/mnt/d/0local/gitrepos/membench`)
