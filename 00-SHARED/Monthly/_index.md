---
type: dir-index
title: "Monthly digests — 90d+ crystallization tier"
emoji: "📆"
N: ['[../Weekly/_index](../Weekly/_index.md)']
S: ['[../Anchors/_index](../Anchors/_index.md)']
E: ['[../Honey/_index](../Honey/_index.md)']
W: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
tags: [dir-index, crystallization, monthly]
---

# 📆 Monthly — `{YYYY-MM}` digests

Deep crystallization tier. Weekly digests older than ~90 days condense
into a single monthly digest. Charter ribbons preserved; manifest clusters
collapse to one droplet per mission. Forensic chain holds via
`superseded_by:` pointers — nothing is deleted.

**Retention:** indefinite. Promoted to `Anchors/` at 1 year if a principle
has held continuously. See [[RETENTION]].

## Contents

```dataviewjs
const pages = dv.pages('"00-SHARED/Monthly"')
  .where(p => p.file.folder !== '00-SHARED/Monthly')
  .sort(p => p.file.path, 'desc');
dv.table(['Month', 'Note'], pages.map(p => [p.file.folder.split('/').pop(), dv.fileLink(p.file.path)]));
```
