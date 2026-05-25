---
type: readme
pseudosystem_folder: Charters
canonical_repo_path: "forensics/charters/"
tags: [readme, pseudosystem]
---

# Charters — Pseudosystem README

## What This Folder Is

`Charters/` is the **vault-native mirror** of the repo's `forensics/charters/` directory. Each active charter in the repo has a corresponding note here with frontmatter mirroring the charter JSON's key fields. The vault note is a **navigation and journaling surface** — the canonical source of truth is always the JSON file in the repo.

## What This Folder Is NOT

- Not a replacement for the JSON charters in the repo
- Not a place to change charter status (do that in the JSON)
- Not automatically synced (manual mirror for now; see sync strategy below)

## Subfolder Structure

```
Charters/
├── _MOC.md           ← Map of Content (start here)
├── _README.md        ← this file
├── active/           ← mirrors forensics/charters/active/ (one note per charter)
├── proposals/        ← mirrors forensics/charters/proposals/ (one note per proposal)
└── sealed/           ← graduated/completed charters (populated as charters seal)
```

## Frontmatter Fields

Each charter note carries these frontmatter fields (mirroring the JSON):

| Field | Source | Meaning |
|-------|--------|---------|
| `charter_id` | `charter_id` | Canonical charter identifier |
| `status` | `status` | active / sealed / proposed |
| `semantic_mission` | `semantic_mission` or `mission_id` | Links to `[[Missions/]]` note |
| `phase` | `phase` | Current phase of the charter |
| `canonical_repo_path` | (vault-added) | Path to the JSON file in repo |

## How to Add a New Charter Note

1. Create the charter JSON in `forensics/charters/proposals/` using the operator workflow
2. Once activated, open Obsidian and use **Blueprint** → `Charter.blueprint`
3. Fill in `charter_id`, `semantic_mission`, `phase`, `canonical_repo_path`
4. Save to `Charters/active/{charter_id}.md`
5. Add a row to `_MOC.md`

## Sync Strategy

Currently **manual**. A future hook (`scripts/9x_vault_pseudosystem_sync.py`) will auto-regenerate these notes when charters change. Until then, re-run the vault pseudosystem builder when charters are added or sealed.

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root for the full picture.*
