---
type: dir-index
title: "Weekly digests — 30d+ crystallization tier"
emoji: "🗓️"
N: ['[../Daily/_index](../Daily/_index.md)']
S: ['[../Monthly/_index](../Monthly/_index.md)']
E: ['[../Anchors/_index](../Anchors/_index.md)', '[../Honey/_index](../Honey/_index.md)']
W: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
tags: [dir-index, crystallization, weekly]
---

# 🗓️ Weekly — `{YYYY-Www}` digests

Mid-tier crystallization. Daily folders older than ~30 days are condensed
into a single weekly digest per ISO week (e.g. `2026-W20/`). Each weekly
digest preserves charter clusters + surviving HONEY droplets; sibling
manifests get retired-with-pointers back to `forensics/ephemeral/`.

**Retention:** indefinite. Rolled into `Monthly/` at 90 days. See [[RETENTION]].

## Contents

```dataviewjs
const pages = dv.pages('"00-SHARED/Weekly"')
  .where(p => p.file.folder !== '00-SHARED/Weekly')
  .sort(p => p.file.path, 'desc');
dv.table(['Week', 'Note'], pages.map(p => [p.file.folder.split('/').pop(), dv.fileLink(p.file.path)]));
```
