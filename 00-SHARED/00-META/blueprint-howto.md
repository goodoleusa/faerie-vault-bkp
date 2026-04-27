---
type: meta
status: active
created: 2026-04-06
tags: [meta, blueprints, howto]
doc_hash: sha256:37514cba968d97d1e4d63598ae4752c3b8afa284aabdee865ed19ea5b738ee44
hash_ts: 2026-04-06T05:36:41Z
hash_method: body-sha256-v1
---

# Blueprint Quick Reference

Blueprints live in `Blueprints/` at vault root. Each `.blueprint` file is a frontmatter + section template.

## Create a new note from a blueprint
Cmd palette → **"Templater: Create new note from template"** or **"Blueprint: Create note from blueprint"** → pick blueprint → note appears with frontmatter pre-filled and section scaffolding in place.

## Apply/re-apply a blueprint to an existing note
Open the note → Cmd palette → **"Blueprint: Apply blueprint"**. Adds any missing frontmatter fields and section markers. Will not overwrite fields you have already set.

**Why "Apply blueprint" is greyed out:** The note must have `blueprint: "[[Blueprints/Name.blueprint]]"` in its frontmatter. Add that line first, then the command becomes available.

## Update all notes using a blueprint
Open the `.blueprint` file → Cmd palette → **"Blueprint: Update notes using this blueprint"**. Pushes changed fields to every note whose `blueprint:` field links to that blueprint.

## The `blueprint:` frontmatter field
Declares which blueprint a note was created from. Required for:
- "Apply blueprint" and "Update notes" commands to find the note
- `vault_hash_sync.py` to link annotation hashes to their originating blueprint
- Dataview queries that filter by blueprint type

## Annotating a note (COC workflow)
Write in the `## Your Annotations` section → **Ctrl+Alt+C** (QuickAdd: Commit Annotation) → `ann_hash` + `ann_ts` fill in frontmatter → `ann_synced` fills when `vault_annotation_sync.py` runs next session.
