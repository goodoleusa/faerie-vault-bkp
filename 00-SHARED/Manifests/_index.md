---
type: dir-index
title: "Manifests — promotion-only canonical work cells"
emoji: "📌"
N: ['[../Ephemeral/_index](../Ephemeral/_index.md)']
S: ['[../Artifacts/_index](../Artifacts/_index.md)', '[../Honey/_index](../Honey/_index.md)']
E: ['[../Bundles/_index](../Bundles/_index.md)', '[../COC-Entries/_index](../COC-Entries/_index.md)']
W: ['[../Charters/_index](../Charters/_index.md)']
tags: [dir-index, manifests, canonical, promotion-pipeline]
---

# 📌 Manifests — `{YYYY-MM-DD}/`

Canonical work cells (hexagonal honeycomb tiles). **Promotion-only** —
this directory is a symlink overlay onto `Ephemeral/{date}/{task_id}/`
originals. Agents never write here directly; `0f_promote-to-forensics.py`
materializes the symlinks at promotion time.

Mirrors `faerie2/forensics/manifests/{YYYY-MM-DD}/` (system of record).

Filename contract:
`{YYYYMMDD}T{HHMMSS}Z__{task_id}_{agent_type}_{mission}_{session_id}.json`

## Today's manifests

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const pages = dv.pages(`"00-SHARED/Manifests/${today}"`).sort(p => p.file.name, 'desc');
dv.table(['Manifest', 'Mission', 'Bearing', 'Charter'],
  pages.map(p => [dv.fileLink(p.file.path), p.mission ?? '', p.bearing ?? '', p.charter_ref ?? '']));
```
