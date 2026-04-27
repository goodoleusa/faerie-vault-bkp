---
type: index
tags: [hive, color, css, themes, design]
parent:
  - "[[00-SHARED/Hive/_index|Hive]]"
doc_hash: sha256:4cfed2ed22fdfede817b52f55b2d85b0430480aa660147e280e11cb113dbda4b
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:23Z
hash_method: body-sha256-v1
---

> [!nav]
> [[00-SHARED/Hive/_index|← Hive]] · **Color Palette Lab** · [[00-SHARED/Dashboards/HOME|HOME]]

# Color Palette Lab

CSS themes designed for this vault. Reusable for web dev — swap Obsidian selectors for your own HTML classes.

## Active Theme

**`theme-palette-lab.css`** — Prism extension layer. Lets Prism handle the base palette via Style Settings, adds investigation-specific callouts, Kanban columns, Mermaid diagrams, evidence tiers, and FFFF colors.

Toggle in: Settings > Appearance > CSS Snippets

## Theme Options

| File | Aesthetic | Use for |
|---|---|---|
| `theme-palette-lab.css` | Prism-compat — pistachio/teal/purple investigation layer | **Current active snippet** |
| `02-vaporwave-jewel-FULL.css` | Full vaporwave override (standalone, overrides Prism) | Rollback if Prism-compat doesn't feel right |
| `01-mission-control.css` | Original mission control | Dark ops, dense data |
| `03-penpot-brutalist.css` | Penpot-inspired brutalism — zero radius, heavy type, neon on black | Bold, geometric, developer aesthetic |
| `02-vaporwave-jewel.css` | Copy of the current vaporwave (pre-Prism-compat) | Backup/web dev reference |

## How to Switch

1. Settings > Appearance > CSS Snippets
2. Toggle OFF current snippet
3. Toggle ON the one you want
4. Only one should be active at a time

## Web Dev Reuse

These are standard CSS with custom properties. To reuse:
- Replace `.theme-light` / `.theme-dark` with your own selectors (e.g. `body`, `[data-theme="dark"]`)
- Replace `.markdown-preview-view h2` with `h2`
- Replace `.callout[data-callout="..."]` with your own component classes
- The `--lab-*` custom properties work in any CSS context
