---
type: dir-index
title: "Anchors — durable principles"
emoji: "⚓"
N: ['[../Monthly/_index](../Monthly/_index.md)']
S: ['[../Charters/_index](../Charters/_index.md)']
E: ['[../Honey/_index](../Honey/_index.md)']
W: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
tags: [dir-index, anchors, crystallization, permanent]
---

# ⚓ Anchors — load-bearing principles

The selvage edge of the tapestry. Anchors are principles the system rests
on; they only land here after surviving the full crystallization ladder
(Daily → Weekly → Monthly → Anchor) and a year of continuous holding.

Question an anchor only via **W-bearing** work (baseline re-seating). Read
the chain inward to the evidence manifests that crystallized it.

**Retention: PERMANENT.** Retired only by an explicit charter. See [[RETENTION]].

## Anchor set

```dataviewjs
const pages = dv.pages('"00-SHARED/Anchors"')
  .where(p => p.file.name !== '_index' && p.file.name !== 'RETENTION')
  .sort(p => p.file.name);
dv.table(['Anchor', 'Bearing', 'Crystallized'],
  pages.map(p => [dv.fileLink(p.file.path), p.bearing ?? '', p.crystallized_on ?? '']));
```
