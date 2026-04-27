---
type: daily-master-brief
date: undated
blueprint: "[[Blueprints/Faerie-Brief.blueprint]]"
agent_type: python-pro
session_id: w2-brief-summary
doc_hash: sha256:61578a1f95fdf31025796796b4bfdbb31eed54aea46428682ec9d7aa929abea7
status: final
sources:
  - 00-META.md
  - 00-README.md
  - 01-LEARNINS.md
  - 01-MEMORY-EDIT.md
  - 02-QUICKADD-SETUP.md
  - 05-OBSIDIAN-SETTINGS.md
  - AGENT-OBSIDIAN-INTEGRATION.md
  - FRONTMATTER-WIKILINKS.md
  - HOW-SYNC-WORKS.md (last_updated: 2026-03-24, captured in 2026-03-24 brief)
  - KICKSTART-COLLAB.md (updated: 2026-03-24, captured in 2026-03-24 brief)
  - VAULT-SCHEMA.md
  - README.md
  - _index.md
  - Color/
  - blueprints/
  - collected-memories/
  - design-coc.jsonl
  - design-hash-track.py
  - design-ip-manifest.json
  - forensic/
  - honey-dev/
  - memory-bench-business-context.md
  - pseudosystem/
  - system-changes/
hash_ts: 2026-04-06T22:35:47Z
hash_method: body-sha256-v1
---

# Undated Hive Files — Reference Brief

Files in the Hive directory with no date in their name and no `created:` frontmatter date that
clearly assigns them to a specific day. These are reference documents, configuration guides,
scaffolding files, or support assets that are maintained as living references rather than
dated session records.

## Document Index

### Navigation and Onboarding
- **`00-META.md`** — empty placeholder; exists as an index anchor for the 00-META namespace
- **`00-README.md`** — doc index and reading order for the Hive; links to OVERVIEW, KICKSTART-COLLAB, ASYNC-HUMAN-AGENT-BRIDGE; suggests reading order by topic
- **`README.md`** — Hive folder README: "Drop anything here. Not work-related, not formal, just interesting." Informal hangout marker.
- **`_index.md`** — vault-level index anchor

### Configuration and Setup Guides
- **`02-QUICKADD-SETUP.md`** — step-by-step guide to wiring QuickAdd + Blueprint in Obsidian; no `created:` date in frontmatter (hashed 2026-03-29)
- **`05-OBSIDIAN-SETTINGS.md`** — opinionated baseline Obsidian settings for the vault; covers every settings category that matters; some defaults actively fight the agent pipeline and need overriding
- **`VAULT-SCHEMA.md`** — vault schema reference; `created: YYYY-MM-DD` placeholder suggests it was created as a template stub not yet filled in
- **`FRONTMATTER-WIKILINKS.md`** — YAML frontmatter and Obsidian wikilinks conventions; `updated: 2026-03-23`, captured under the March 24 update wave

### Redirect / Moved Documents
- **`AGENT-OBSIDIAN-INTEGRATION.md`** — redirect notice: "Agent-Obsidian integration (moved)"; content relocated elsewhere; acts as a tombstone/pointer

### Scratch and Working Files
- **`01-LEARNINS.md`** — empty (no content); likely a scratch placeholder for learnings accumulation
- **`01-MEMORY-EDIT.md`** — empty (no content); likely a scratch placeholder for memory edit tracking

### Support Assets and Subdirectories
- **`Color/`** — color palette assets for the vault (theme/styling support)
- **`blueprints/`** — Blueprint template files for agent output types (referenced by 18-blueprint-system-design.md)
- **`collected-memories/`** — collected memory artifacts, likely HONEY/NECTAR extracts
- **`design-coc.jsonl`** — design-phase chain-of-custody JSONL log for Hive documents
- **`design-hash-track.py`** — hash tracking script for design documents; likely the source of the `hash_ts` / `doc_hash` fields on Hive files
- **`design-ip-manifest.json`** — design-phase IP manifest (document inventory with hashes)
- **`forensic/`** — forensic artifacts for the Hive itself (COC log, hash manifests)
- **`honey-dev/`** — HONEY.md development working files; drafts and candidates before promotion to global HONEY
- **`memory-bench-business-context.md`** — business context document for the memory-bench project; companion to `MEMORY-BENCH-README.md`
- **`pseudosystem/`** — pseudosystem component notes; atomic design units referenced by System-Architecture.md Dataview queries
- **`system-changes/`** — system change log entries (e.g., `2026-03-22-vault-sync-wiring`); changelog for vault infrastructure changes

## Key Notes

- Most of these files were hashed in the bulk pass on `2026-03-29` (`hash_ts: 2026-03-29T16:10:*`) but may have been created earlier
- `design-hash-track.py` is likely the script that performed the bulk hashing pass
- Empty files (`00-META.md`, `01-LEARNINS.md`, `01-MEMORY-EDIT.md`) are placeholders awaiting content
- `honey-dev/` is the staging area for HONEY candidates — content there is pre-crystallization
- `pseudosystem/` is a critical dependency for `System-Architecture.md` Dataview queries — needs population

## Open Threads

- `VAULT-SCHEMA.md` has a placeholder `created: YYYY-MM-DD` — needs the actual creation date filled in
- `pseudosystem/` component notes need to be written for the Dataview queries in `System-Architecture.md` to resolve
- `honey-dev/` candidates need review for promotion through the crystallization gauntlet
- Empty placeholder files (`01-LEARNINS.md`, `01-MEMORY-EDIT.md`) need either content or deletion
