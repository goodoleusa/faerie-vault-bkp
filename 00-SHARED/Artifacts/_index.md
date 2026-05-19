---
type: dir-index
title: "Artifacts — promotion-only canonical work products"
emoji: "⬡"
N: ['[../Manifests/_index](../Manifests/_index.md)']
S: ['[../Honey/_index](../Honey/_index.md)']
E: ['[../Bundles/_index](../Bundles/_index.md)']
W: ['[../Ephemeral/_index](../Ephemeral/_index.md)']
tags: [dir-index, artifacts, canonical, promotion-pipeline]
---

# ⬡ Artifacts — `{YYYY-MM-DD}/`

Canonical work products (the "what was made"). **Promotion-only** symlink
overlay onto Ephemeral originals. Mirrors
`faerie2/forensics/artifacts/{YYYY-MM-DD}/`.

## Today's artifacts

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const pages = dv.pages(`"00-SHARED/Artifacts/${today}"`).sort(p => p.file.name, 'desc');
dv.table(['Artifact', 'Task', 'Type'],
  pages.map(p => [dv.fileLink(p.file.path), p.task_id ?? '', p.type ?? '']));
```
