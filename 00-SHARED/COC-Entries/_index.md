---
type: dir-index
title: "COC entries — hash-chained audit trail"
emoji: "🔗"
N: ['[../Manifests/_index](../Manifests/_index.md)']
S: ['[../Anchors/_index](../Anchors/_index.md)']
E: ['[../Artifacts/_index](../Artifacts/_index.md)']
W: ['[../Ephemeral/_index](../Ephemeral/_index.md)']
tags: [dir-index, coc, canonical, audit, promotion-pipeline]
---

# 🔗 COC entries — `{YYYY-MM-DD}/`

Chain-of-custody entries. **Append-only**, hash-linked (each entry carries
`prev_entry_hash`). The forensic spine of the system.

Mirrors `faerie2/forensics/coc-entries/{YYYY-MM-DD}/` and rolls up into
`faerie2/forensics/coc.jsonl` (the canonical chain).

Entry types: `promotion`, `mutation`, `crystallization`, `spawn`,
`session_end`, `anchor_promote`, `vault_write`.

## Today's COC entries

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const pages = dv.pages(`"00-SHARED/COC-Entries/${today}"`).sort(p => p.file.name);
dv.table(['Entry', 'Type', 'Actor'],
  pages.map(p => [dv.fileLink(p.file.path), p.entry_type ?? '', p.actor ?? '']));
```
