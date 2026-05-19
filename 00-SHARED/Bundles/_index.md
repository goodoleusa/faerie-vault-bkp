---
type: dir-index
title: "Bundles — spawn context packages"
emoji: "📦"
N: ['[../Charters/_index](../Charters/_index.md)']
S: ['[../Manifests/_index](../Manifests/_index.md)']
E: ['[../Artifacts/_index](../Artifacts/_index.md)']
W: ['[../Ephemeral/_index](../Ephemeral/_index.md)']
tags: [dir-index, bundles, canonical, promotion-pipeline]
---

# 📦 Bundles — `{YYYY-MM-DD}/`

Spawn context packages (input data for agents). **Promotion-only** symlink
overlay. Mirrors `faerie2/forensics/bundles/{YYYY-MM-DD}/`.

A bundle carries: charter_ref, mission, frontier context, NSEW links —
everything an agent needs at spawn time to autonomously route.

## Today's bundles

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const pages = dv.pages(`"00-SHARED/Bundles/${today}"`).sort(p => p.file.name, 'desc');
dv.table(['Bundle', 'Mission', 'Charter'],
  pages.map(p => [dv.fileLink(p.file.path), p.mission ?? '', p.charter_ref ?? '']));
```
