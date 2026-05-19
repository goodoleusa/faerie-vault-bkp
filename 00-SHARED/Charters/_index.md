---
type: dir-index
title: "Charters — declared intent"
emoji: "📜"
N: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
S: ['[../Daily/_index](../Daily/_index.md)']
E: ['[../Anchors/_index](../Anchors/_index.md)']
W: ['[../Honey/_index](../Honey/_index.md)']
tags: [dir-index, charters, intent]
---

# 📜 Charters — the cornerstone

Mirrors `faerie2/forensics/charters/{YYYY-MM-DD}/`. Every manifest must
`charter_ref` to a charter here. Charters are first-class declared intent —
the parchment scrolls that hold the comb frames together.

**Retention: PERMANENT.** Charters are retired via a `status:` field flip,
never deleted. See [[RETENTION]].

## Active charters

```dataviewjs
const pages = dv.pages('"00-SHARED/Charters"')
  .where(p => p.file.name !== '_index' && p.file.name !== 'RETENTION')
  .where(p => p.status !== 'retired')
  .sort(p => p.file.name, 'desc');
dv.table(['Charter', 'Status', 'Bearing'],
  pages.map(p => [dv.fileLink(p.file.path), p.status ?? 'active', p.bearing ?? '']));
```
