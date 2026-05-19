---
type: internals
title: "Promotion pipeline — Ephemeral → Canonical (mirror of faerie2)"
emoji: "🚇"
N: ['[README](README.md)']
S: ['[../../HELP/crystallization-workflow](../../HELP/crystallization-workflow.md)']
E: ['[../../Ephemeral/_index](../../Ephemeral/_index.md)', '[../../Manifests/_index](../../Manifests/_index.md)', '[../../COC-Entries/_index](../../COC-Entries/_index.md)']
W: ['[../../Dashboards/00-Home](../../Dashboards/00-Home.md)']
tags: [internals, promotion-pipeline, coc]
---

# 🚇 Promotion pipeline

This vault mirrors the faerie2 immutability architecture one-for-one.

## Architecture

```
                   AGENT WRITES (unrestricted)
                            │
                            ▼
            ┌─────────────────────────────┐
            │ 00-SHARED/Ephemeral/        │
            │   {date}/{task_id}/         │ ← only writable location
            │   file_manifest_*.json      │
            │   file_artifact_*.md        │
            │   file_bundle_*.json        │
            │   file_coc-entry_*.json     │
            └──────────────┬──────────────┘
                           │
            0f_promote-to-forensics.py
            (PostToolUse[Write] + STOP + SESSION_END)
                           │
        ┌──────────┬───────┼───────┬──────────┐
        ▼          ▼       ▼       ▼          ▼
   Manifests/  Artifacts/  Bundles/  COC-Entries/  B2 WORM
    {date}/     {date}/    {date}/    {date}/     (queue)
   (symlink)   (symlink)  (symlink)  (append)

                           │
              Daily/{date}/ ← human-readable mirror
              (06-daily-mirror.py, with NSEW frontmatter + canvas)
```

## Write-protection rules (mirror faerie2 settings.json deny list)

| Path | Agent writes? | Promotion writes? |
|---|---|---|
| `00-SHARED/Ephemeral/**` | ✅ yes | n/a (source) |
| `00-SHARED/Manifests/**` | ❌ deny | ✅ symlink only |
| `00-SHARED/Artifacts/**` | ❌ deny | ✅ symlink only |
| `00-SHARED/Bundles/**` | ❌ deny | ✅ symlink only |
| `00-SHARED/COC-Entries/**` | ❌ deny | ✅ append only |
| `00-SHARED/Anchors/**` | ❌ deny | ✅ via annual-anchor.py only |
| `00-SHARED/Charters/**` | ❌ deny (mirror) | ✅ mirror from faerie2 |
| `00-SHARED/Honey/**` | ❌ deny | ✅ via 10-crystallize.py only |
| `00-SHARED/Daily/**` | ❌ deny (mirror) | ✅ 06-daily-mirror.py only |

## Type inference (from filename)

`0f_promote-to-forensics.py` infers destination from filename markers:

- `*_manifest_*.json` → `Manifests/{date}/`
- `*_artifact_*.{md,json}` → `Artifacts/{date}/`
- `*_bundle_*.json` → `Bundles/{date}/`
- `*_coc-entry_*.json` → `COC-Entries/{date}/`
- `*_droplet_*.md` → `Artifacts/{date}/droplets/` (and later → `Honey/{date}/`)

## Why this respects f(0)

- Agents have **zero overhead** — unrestricted writes to one path.
- Infrastructure (hooks) enforces immutability **ambient to agents**.
- Canonical tree is **pure symlinks** — no duplicates, lineal traceability.
- COC chain is **complete + hash-linked** — forensically sound.
- The vault and `faerie2/forensics/` share the same shape — agents that
  know one know both.
