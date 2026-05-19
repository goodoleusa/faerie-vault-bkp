---
type: dir-index
title: "Honey droplets — crystallized memory"
emoji: "🍯"
N: ['[../Daily/_index](../Daily/_index.md)']
S: ['[../Anchors/_index](../Anchors/_index.md)']
E: ['[../Weekly/_index](../Weekly/_index.md)', '[../Monthly/_index](../Monthly/_index.md)']
W: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
tags: [dir-index, honey, crystallization]
---

# 🍯 Honey — `{YYYY-MM-DD}` droplets

Crystallized memory. When the crystallization pass detects sibling manifests
that converged on the same insight, the survivors get distilled into a single
HONEY droplet here. Each droplet is canonical once written — read it as
ambient memory on future sessions.

Mirrors `faerie2/forensics/honey/{YYYY-MM-DD}/{slug}.md` (the system of record).

**Retention:** indefinite (droplets are canonical). See [[RETENTION]].

## Droplets by day

```dataviewjs
const pages = dv.pages('"00-SHARED/Honey"')
  .where(p => p.file.name !== '_index' && p.file.name !== 'RETENTION')
  .sort(p => p.file.path, 'desc');
dv.table(['Day', 'Droplet'],
  pages.map(p => [p.file.folder.split('/').pop(), dv.fileLink(p.file.path)]));
```
