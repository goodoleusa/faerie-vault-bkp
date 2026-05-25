---
type: readme
title: Blueprints — Unified Engine Notice
created: "2026-05-25"
tags: [blueprints, unification, hive]
---

# Blueprints — Unified Engine Notice

**As of 2026-05-25, vault Blueprints have been unified onto the swarmy-hive plugin's bundled Nunjucks (`.njk`) engine.**

This directory is now empty (stub only). All templates live in the hive plugin's bundled `Blueprints/` directory.

---

## Where Blueprints Now Live

**Source of truth:** `/mnt/d/0local/gitrepos/swarmy-hive-plugin/Blueprints/`

87 templates available (84 original + 3 new substrate primitives: `Mission.njk`, `Shape.njk`, `Wave.njk`).

**Configure via:** Obsidian → Settings → Hive → `swarmyRepoBlueprintsDir`

Current setting in `data.json`:
```
"swarmyRepoBlueprintsDir": "/mnt/d/0local/gitrepos/swarmy-hive-plugin/Blueprints"
```

---

## Engine

The hive plugin uses a vendored micro-Nunjucks renderer (`src/vendor/micro-njk.ts`). Supported syntax:
- `{{ variable }}` — interpolation with dotted paths
- `{{ var | default("x") }}` — pipe filters (default, upper, lower, length, join, replace, date, etc.)
- `{% if %}...{% endif %}` — conditionals
- `{% for x in xs %}...{% endfor %}` — loops
- `{% set x = ... %}` — assignment
- `{% section "name" %}...{% endsection %}` — passes through as literal text (used for human-readable section markers)

---

## Pre-Unification Archive

The original 39 `.blueprint` files (François Vaux plugin format) are preserved at:

`_archive/Blueprints-20260525-pre-unification/`

They are retained for audit purposes only. The François Vaux `blueprint` plugin is now functionally unused for swarmy templates (see D6 note in migration report).

---

## Migration Audit

Full 41-pair audit at:
`/mnt/d/0local/gitrepos/swarmy-hive-plugin/Blueprints/_AUDIT-2026-05-25.md`

Summary: 30 EQUIVALENT, 2 HIVE-SUPERSET, 1 HIVE-MISSING-FEATURES (ported), 7 DIFFERENT-PURPOSE (documented).

---

*Migration performed: 2026-05-25 by blueprint-unifier agent.*
