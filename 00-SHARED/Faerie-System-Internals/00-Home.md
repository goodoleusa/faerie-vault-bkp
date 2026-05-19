---
type: faerie-internal
subtype: home
tier: internals-home
last_synced: '2026-05-19T15:24:06+00:00'
N: '[Vault Root](../00-SHARED.md)'
S: ['[Templates](Templates/)', '[Formulas](Formulas/00-Formulas-Index.md)', '[Spawn-Bundles](Spawn-Bundles/00-Overview.md)', '[System-Prompts](System-Prompts/queen-system-prompt.md)']
tags: ['internal', 'home', '#path/transparency']
---

# Faerie System Internals

## Why this exists

The faerie AI's inner workings are normally opaque — templates buried in `.njk` files, formulas locked inside `formulas.js`, spawn bundles hidden under `forensics/bundles/`, system prompts that only the agent ever sees.

This section makes them **legible**. Every template, every formula, every spawn bundle pattern, every system prompt is mirrored here in plain Markdown, with explanations, raw source, and live performance pointers.

> [!info] Read-only display
> This tree is a regenerable mirror. Edit the canonical sources (paths shown on every page); re-run `scripts/dev/vault/09-internals-sync.py` to refresh.

## Three things to read first

1. **[Queen system prompt](System-Prompts/queen-system-prompt.md)** — what the AI is told
2. **[Formulas Index](Formulas/00-Formulas-Index.md)** — how it's measured
3. **[Spawn bundles overview](Spawn-Bundles/00-Overview.md)** — how it's invoked

## Sections

- [Templates/](Templates/) — every Nunjucks system prompt + agent archetype definition
- [Formulas/](Formulas/) — f(0), Emergence Health, Osmotic Potential, eval dims A–G, membench M12–M15
- [Spawn-Bundles/](Spawn-Bundles/) — bundle schema, archetypes, real anonymized samples
- [System-Prompts/](System-Prompts/) — the queen's brief as rendered

## Freshly synced

```dataview
TABLE WITHOUT ID
  file.link AS "Page",
  subtype AS "Kind",
  last_synced AS "Synced"
FROM "00-SHARED/Faerie-System-Internals"
WHERE type = "faerie-internal"
SORT last_synced DESC
LIMIT 15
```
