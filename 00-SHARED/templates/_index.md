---
type: dir-index
title: "Templates — Obsidian core templates (no Templater)"
emoji: "🧩"
N: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
S: ['[../Daily/_index](../Daily/_index.md)']
E: ['[../Snippets](../Snippets)']
W: ['[../HELP/crystallization-workflow](../HELP/crystallization-workflow.md)']
tags: [dir-index, templates]
---

# 🧩 Templates

Basic frontmatter shells for the core Obsidian Templates plugin. **No
Templater syntax** — these are pure markdown stubs so they survive both
core-Templates and Templater installs.

Each file ending in `-basic.md` is a copy-paste seed: open, replace
placeholders, save into the right canonical folder (Daily/, Charters/,
Honey/, etc).

## Available templates

```dataviewjs
const pages = dv.pages('"00-SHARED/Templates"')
  .where(p => p.file.name !== '_index')
  .sort(p => p.file.name);
dv.table(['Template', 'Purpose'],
  pages.map(p => [dv.fileLink(p.file.path), p.summary ?? '']));
```
