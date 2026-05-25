---
type: readme
pseudosystem_folder: Forensics
canonical_repo_path: "forensics/"
tags: [readme, pseudosystem]
---

# Forensics — Pseudosystem README

## What This Folder Is

`Forensics/` is the vault-side companion to the repo's `forensics/` directory. It provides navigable summaries of the forensic infrastructure — COC chain entries, session archives, and wave dossiers — WITHOUT duplicating the canonical evidence-class data that must stay in the repo.

## Design Principle: Evidence Stays in Repo

The `forensics/coc.jsonl`, signed manifests, and session archives are **evidence-class artifacts** — they cannot be duplicated into the vault without creating a sync problem and potentially weakening their evidentiary standing. The vault folder contains **prose summaries + navigation aids only**.

Think of it as the difference between a court exhibit (stays in the record room, immutable) and your notes about the exhibit (in your notebook, for reference).

## Three-Store Architecture

The canonical forensics architecture has three stores:

1. **Repo `forensics/`** — git-tracked, hash-chained, COC-linked (canonical; vault never writes here)
2. **Vault `Forensics/`** (this folder) — navigable summaries for operator orientation
3. **B2 WORM backup** — immutable backup of repo forensics/ (automatic via hooks)

## Subfolder Structure

```
Forensics/
├── _MOC.md           ← Map of Content
├── _README.md        ← this file
├── coc/              ← COC chain structure notes (NOT coc.jsonl content)
│   └── _README.md
├── sessions/         ← summaries of Claude Code session archives
└── waves/            ← per-wave dossiers (one per multi-agent dispatch)
```

## What Goes in Each Subfolder

**`coc/`** — structural notes about the COC schema, entry types, and chain integrity metrics. Never paste raw coc.jsonl entries here (those are evidence-class).

**`sessions/`** — after a session ends and is archived to `forensics/_claude-session-archive/`, a brief prose summary note can be added here for navigation. Format: `{YYYY-MM-DD}-{session-label}.md`.

**`waves/`** — when a major multi-agent wave completes, create a Wave dossier note using `Wave.blueprint`. The wave note lists all agents dispatched, their task_ids, and what emerged. Links to individual Manifest notes.

## What NEVER Goes Here

- Raw `coc.jsonl` entries
- Full manifest JSON content
- Ed25519 key material
- Session logs or JSONL files
- Any file that would create a duplicate of repo canonical data

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root.*
