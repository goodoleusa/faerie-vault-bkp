---
type: readme
title: Vault Pseudosystem
tags: [pseudosystem, navigation, readme]
created: "2026-05-25"
repo: "faerie2"
canonical_substrate_docs:
  - "docs/100-HIVE-ARCHITECTURE-CANONICAL.md"
  - "docs/35-FOUR-LAYER-ENFORCEMENT-CANONICAL.md"
---

# Vault Pseudosystem

The Vault Pseudosystem is the operator's **navigable mirror** of the repo's forensic substrate — presented in vault-native conventions (frontmatter, MoCs, wiki-links, Blueprints) so the operator has the same mental model in Obsidian as in the repo, without the vault becoming load-bearing for production.

---

## What It Is

The repo (`faerie2/`) has a canonical substrate:

| Repo Structure | Contains |
|----------------|----------|
| `forensics/charters/active/` | Active charter JSONs (governance contracts for work) |
| `forensics/charters/proposals/` | Proposed charters awaiting activation |
| `forensics/manifests/<date>/` | Signed manifest JSONs (agent completion records) |
| `forensics/coc.jsonl` | Hash-linked Chain of Custody |
| `forensics/mission-graph.json` | DAG of missions, bearings, and task linkages |
| `_meta/shapes.json` | Measurement probe registry |
| `.agents/skills/*/SKILL.md` | Agent skill definitions |

The Pseudosystem mirrors each of these with an Obsidian-friendly equivalent:

| Vault Folder | Mirrors | Format |
|--------------|---------|--------|
| `Charters/` | `forensics/charters/` | One `.md` per charter; frontmatter = charter JSON fields |
| `Manifests/` | `forensics/manifests/` | One `.md` per manifest; organized by date |
| `Missions/` | `forensics/mission-graph.json` | One `.md` per mission (top 20 by activity) |
| `Shapes/` | `_meta/shapes.json` | One `.md` per shape with history table |
| `Forensics/` | `forensics/` (structural) | Navigation notes; COC/sessions/waves subfolders |

---

## What It Is NOT

The Pseudosystem is **optional and non-load-bearing**. Production deployments of swarmy have no vault at all and operate identically. The vault is purely for the operator's cognitive benefit:

- Not a replacement for any repo file
- Not a place to edit charter status or manifest data (the repo JSON is authoritative)
- Not automatically synced (manual for now; future automation planned)
- Not a duplicate of evidence-class data (`coc.jsonl` entries, raw manifests, session logs)

Consult `docs/24-CRYSTAL-AND-SPRAY-WRITING-DISCIPLINE.md` (in repo) for the canonical discipline on what is vault-appropriate vs. repo-canonical.

---

## How to Navigate

**Start at the MoC for the area you want to explore:**

- Charters → `Charters/_MOC.md` → click any charter note → frontmatter links to mission + canonical repo path
- Manifests → `Manifests/_MOC.md` → `Manifests/2026-05-25/` → individual manifest notes
- Missions → `Missions/_MOC.md` → click any mission dossier → backlinks to charters + manifests
- Shapes → `Shapes/_MOC.md` → click any shape → history table + detector script reference
- Forensics → `Forensics/_MOC.md` → navigate COC chain structure, session summaries, wave dossiers

**In Obsidian's graph view:** All notes use `[[wiki-links]]` so the graph naturally shows the charter → mission → manifest → shape relationships. Enable the `type:` frontmatter filter to isolate pseudosystem note types.

**Ctrl-Click navigation:** Every vault note has a `canonical_repo_path` frontmatter field containing the exact repo-relative path to the source JSON. This lets you jump from vault note → canonical source with a path lookup.

---

## How to Add New Notes

When new charters, manifests, missions, or shapes appear in the repo, mirror them in the vault using the matching Blueprint:

| Note Type | Blueprint | Save Location |
|-----------|-----------|---------------|
| Active charter | `Charter.blueprint` | `Charters/active/{charter_id}.md` |
| Proposal charter | `Charter.blueprint` | `Charters/proposals/{charter_id}.md` |
| Sealed/completed charter | `Charter.blueprint` | `Charters/sealed/{charter_id}.md` |
| Manifest | `Manifest.blueprint` | `Manifests/{YYYY-MM-DD}/{task_id}.md` |
| Mission dossier | `Mission.blueprint` | `Missions/{mission-id}.md` |
| Shape dossier | `Shape.blueprint` | `Shapes/{shape_id}.md` |
| Wave dossier | `Wave.blueprint` | `Forensics/waves/{YYYY-MM-DD}-{label}.md` |

Blueprints live in `Blueprints/` — in Obsidian, open the Template picker and select the matching blueprint to get the correct frontmatter skeleton.

After adding a note, update the relevant `_MOC.md` to include it in the navigation table.

---

## Sync Strategy

Currently **manual**. The pseudosystem was built once (2026-05-25) from a repo snapshot. To refresh it after significant changes:

1. Re-run the vault pseudosystem builder (future: `scripts/9x_vault_pseudosystem_sync.py`)
2. Or manually: add/update individual notes when you notice the repo has diverged

**Proposed automation hook** (not yet built): `scripts/9x_vault_pseudosystem_sync.py` — watches `forensics/charters/`, `forensics/manifests/`, `_meta/shapes.json` for changes and regenerates the corresponding vault notes. This would be wired as a PostToolUse hook so it fires after any charter or manifest write. Tracked as `discovered_work` in the pseuodosystem builder's manifest.

When `9x_vault_pseudosystem_sync.py` is built, the sync becomes:
1. Charter added → vault note auto-generated in `Charters/active/`
2. Manifest sealed → vault note auto-generated in `Manifests/{date}/`
3. Shape count updated → vault note `current_count` frontmatter refreshed

---

## Design Principles (Summary)

1. **Vault-optional in prod** — the substrate operates without the vault
2. **Frontmatter mirrors repo JSON** — same fields, YAML syntax, for Dataview queries
3. **Wiki-links over hard paths** — `[[mission-id]]` not `forensics/manifests/...`
4. **No duplication of source-of-truth data** — vault summarizes + links, never replicates
5. **MoC pattern** — each subfolder root has `_MOC.md` as the top-level navigation surface
6. **Blueprint-driven note creation** — hive plugin's bundled `.njk` templates (Nunjucks) ensure consistent structure. Templates live in `/mnt/d/0local/gitrepos/swarmy-hive-plugin/Blueprints/` (87 templates). The vault `Blueprints/` directory is now an empty stub — all templates come from the hive bundle.

---

## Blueprint Engine (post-unification 2026-05-25)

As of 2026-05-25, all vault blueprints run on the hive plugin's Nunjucks (`.njk`) engine. The François Vaux `.blueprint` plugin is no longer used for swarmy templates.

**How to apply a blueprint:**
1. Open any note in Obsidian
2. Run `Swarmy: apply blueprint to current note` (Cmd/Ctrl+P)
3. Select from the fuzzy-search list (87 templates available)

**Template source:** `swarmy-hive-plugin/Blueprints/*.njk` (configured via Settings → Hive → `swarmyRepoBlueprintsDir`)

**New substrate primitives added (2026-05-25):** `Mission.njk`, `Shape.njk`, `Wave.njk` — these replace the vault-only `.blueprint` versions and are now canonical in the hive bundle.

See `Blueprints/_README.md` for the full migration notice and archive location.

---

*Pseudosystem built: 2026-05-25. Repo: `faerie2`. Vault: `faerie-vault`.*
*Canonical architecture docs: `docs/100-HIVE-ARCHITECTURE-CANONICAL.md` in repo.*
*Blueprint unification: 2026-05-25. Archive: `_archive/Blueprints-20260525-pre-unification/`.*
