---
type: readme
pseudosystem_folder: Manifests
canonical_repo_path: "forensics/manifests/"
tags: [readme, pseudosystem]
---

# Manifests — Pseudosystem README

## What This Folder Is

`Manifests/` is the vault-native navigable mirror of `forensics/manifests/<date>/` in the repo. Each agent that completes a task writes a signed manifest JSON; these notes are navigable summaries of those manifests with frontmatter for Obsidian's graph view and Dataview queries.

## What This Folder Is NOT

- Not the canonical manifest record (that's the signed JSON in the repo)
- Not a replacement for the COC chain (the COC lives in `forensics/coc.jsonl`)
- Not automatically updated on each manifest write (manual mirror; future sync hook planned)

## Subfolder Structure

```
Manifests/
├── _MOC.md              ← Map of Content (top-level navigation)
├── _README.md           ← this file
└── {YYYY-MM-DD}/        ← one folder per day that had manifests
    └── {task_id}.md     ← one note per manifest JSON
```

## Manifest Note Frontmatter

| Field | Meaning |
|-------|---------|
| `task_id` | Matches the manifest's `task_id` field |
| `mission` | Links to `[[Missions/]]` dossier |
| `agent_type` | The agent archetype that wrote this manifest |
| `charter_id` | Links to `[[Charters/]]` note |
| `signed` | `true` if manifest carries a real ed25519 signature |
| `bearing` | N/S/E/W compass bearing |
| `canonical_repo_path` | Exact path to the JSON in repo |

## Naming Convention

Vault manifest notes use `{task_id}.md` as the filename. The full manifest filename in the repo follows the COC naming grammar: `{YYYYMMDD}T{HHMMSS}Z__{task_id}_{agent}_{mission}_{session_id}.json`.

## How to Add a Manifest Note

1. After an agent seals a manifest, open Obsidian
2. Blueprint → `Manifest.blueprint`
3. Save to `Manifests/{YYYY-MM-DD}/{task_id}.md`
4. Fill dashboard_line, signed_by, mission, charter_id from the JSON

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root.*
