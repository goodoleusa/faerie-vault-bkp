---
type: dir-index
title: "Ephemeral — agent scratch space (unrestricted writes)"
emoji: "🌼"
N: ['[../Dashboards/00-Home](../Dashboards/00-Home.md)']
S: ['[../Manifests/_index](../Manifests/_index.md)', '[../Artifacts/_index](../Artifacts/_index.md)', '[../Bundles/_index](../Bundles/_index.md)', '[../COC-Entries/_index](../COC-Entries/_index.md)']
E: ['[../Daily/_index](../Daily/_index.md)']
W: ['[../HELP/crystallization-workflow](../HELP/crystallization-workflow.md)']
tags: [dir-index, ephemeral, promotion-pipeline]
---

# 🌼 Ephemeral — `{YYYY-MM-DD}/{task_id}/`

**Mirrors `faerie2/forensics/ephemeral/{YYYY-MM-DD}/{task_id}/`** — the only
place agents are allowed to write freely. Zero friction. Agents are unaware
of promotion; the hooks do it ambient to them.

Filenames carry a type marker (`_manifest_`, `_artifact_`, `_bundle_`,
`_coc-entry_`) so `0f_promote-to-forensics.py` can infer destination from
the name alone.

## Promotion pipeline (PostToolUse + STOP + SESSION_END)

```
ephemeral/{date}/{task_id}/file              ← agent writes here
        │
        ▼  0f_promote-to-forensics.py
        ├──► Manifests/{date}/      (symlink)
        ├──► Artifacts/{date}/      (symlink)
        ├──► Bundles/{date}/        (symlink)
        ├──► COC-Entries/{date}/    (append to coc.jsonl)
        └──► B2 WORM queue          (best-effort)
```

**Retention:** indefinite (original payloads live here; canonical dirs are
pure symlinks back). See [[RETENTION]].

## Today's ephemeral

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const pages = dv.pages(`"00-SHARED/Ephemeral/${today}"`).sort(p => p.file.path, 'desc');
dv.table(['Task', 'File', 'Type-hint'],
  pages.map(p => [p.file.folder.split('/').pop(), dv.fileLink(p.file.path),
    (p.file.name.match(/_(manifest|artifact|bundle|coc-entry)_/)||[,'?'])[1]]));
```
