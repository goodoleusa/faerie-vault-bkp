---
type: hub
status: active
tags: [onboarding, faerie2, vault, setup]
created: 2026-05-06T00:00:00Z
updated: 2026-05-06T00:00:00Z
doc_hash: ""
---

# Onboarding: faerie2 + Vault

Welcome. This guide explains what faerie is, how the vault works, and how to operate it day-to-day.

---

## What Is faerie? What Is This Vault?

**faerie2** is a multi-agent AI orchestration system. You give it a mission. It spawns teams of Claude agents that work in parallel — each agent writes its findings as manifest files. The system is modeled on a hive: you are the queen. You spawn eggs (agents) and read the honey (findings).

**This vault** is your reading surface. It is also the stigmergic substrate — agents leave traces here as notes, and those notes guide subsequent agents. Obsidian renders the output in a navigable, searchable, linked format.

There are two vaults:

| Vault | Purpose |
|-------|---------|
| `faerie-vault` | Publications, synthesis, onboarding. What you read first. |
| `ct-vault` | Investigation data, evidence, entities, raw agent outputs. |

---

## Where to Find Agent Outputs

Agents write to `faerie2/forensics/` (canonical, git-tracked). A sync hook renders final manifests into vault notes.

| Vault Location | What Is Here |
|----------------|-------------|
| `00-SHARED/Agent-Outbox/` | Raw agent writes (fresh, not yet reviewed) |
| `00-SHARED/Human-Inbox/findings/` | Synthesized findings routed for human review |
| `00-SHARED/Human-Inbox/flags/` | Items flagged as needing your attention |
| `00-SHARED/Human-Inbox/connections/` | Entity connection discoveries |
| `00-SHARED/Human-Inbox/narratives/` | Narrative synthesis outputs |
| `00-SHARED/Droplets/` | Crystallized memory drops (persistent distillations) |
| `10-Investigations/` | Active investigation notes |

> Note: "Agent-Outbox" is named from the agent's perspective. From your perspective it is an inbox. Check it daily.

The daily ingest flow:

1. Agents finish tasks and write final manifests to `forensics/ephemeral/{date}/`
2. `0x_manifest_to_vault_sync.py` (PostToolUse hook) converts them to vault notes
3. Notes land in `00-SHARED/Agent-Outbox/`
4. You open Obsidian, review, and move findings to `Human-Inbox/` or archive

---

## How to Capture Mission Choice

At the start of each session:

1. Create a daily note via `Cmd/Ctrl+P → QuickAdd: Daily Note`
2. Fill in the `mission_choice` frontmatter field:

```yaml
---
type: hub
status: active
tags: [daily, faerie2]
mission_choice: "vault-infrastructure-overhaul"
---
```

Agents read this field on session start to cluster their work under your chosen mission. If you leave it blank, agents default to their last known active mission.

**Mission names** come from the manifest `mission` field. Look at recent manifests in `forensics/manifests/` to see current active missions, or ask faerie2: `/run --missions` lists all active mission clusters.

---

## How to Make Edits

- Use `[[wikilinks]]` to link notes — **never** `[markdown links](file.md)`.
- Vault is configured for relative wikilinks (set in `.obsidian/app.json`).
- Every vault note must have frontmatter with these fields:

```yaml
---
type: hub          # see type taxonomy below
status: active     # draft | active | deprecated | archived
tags: [tag1, tag2] # minimum 2 tags
created: 2026-05-06T00:00:00Z
updated: 2026-05-06T00:00:00Z
doc_hash: ""       # filled by hash hook automatically
---
```

**Type taxonomy:**

| Type | Use For |
|------|---------|
| `hub` | Entry points, daily notes, index files |
| `narrative` | Synthesis documents, mission notes |
| `droplet` | Crystallized memory (permanent) |
| `dashboard` | Dataview query pages |
| `publication` | Finished research outputs |
| `entry-point` | Navigation landing pages |
| `skill-ref` | Documentation for agent skills |
| `glossary` | Terminology definitions |

**Compass frontmatter** (for mission-graph navigation):

```yaml
north: "[[predecessor-task]]"    # what must complete before this
south: "[[downstream-task]]"     # what this unblocks
east:  "[[parallel-sister]]"     # parallel work at same level
west:  "[[genesis-anchor]]"      # return to baseline if needed
bearing: "S"                     # dominant bearing (N/S/E/W)
mission: "vault-infrastructure-overhaul"
```

---

## How to Sync

Sync is **automatic** via hooks — no action needed for routine operations.

The sync pipeline:
1. Agent writes final manifest → `forensics/ephemeral/{date}/{task_id}/`
2. `0x_promote_to_forensics.py` (PostToolUse hook) creates canonical symlink
3. `0x_manifest_to_vault_sync.py` (PostToolUse hook) renders note to vault
4. `5x_vault_mutation_tracker.py` (PostToolUse hook) updates `doc_hash` in frontmatter
5. `5x_b2_realtime_uploader.py` queues WORM backup

**Manual sync** (when hooks are not running):
```bash
cd ~/Obsidian/faerie2
python3 scripts/0x_vault_sync_test.py --vault ../faerie-vault --faerie2 .
```

**Force full sync:**
```bash
cd ~/Obsidian/faerie2
python3 .claude/scripts/0x_manifest_to_vault_sync.py --all --vault ../faerie-vault
```

---

## Troubleshooting

### Broken links (orange in Obsidian)
- Cause: file was moved or renamed without using Obsidian's rename.
- Fix: use Obsidian's "Rename" (right-click file → Rename) — updates all backlinks.
- Bulk check: `grep -r "\[\[" . --include="*.md" | grep -v ".obsidian"` then manually verify targets.
- Never use OS-level mv/rename on vault files — always rename through Obsidian.

### Sync stuck / new manifests not appearing in vault
1. Verify hooks are active: `ls ~/.claude/hooks/` — should list `0x_manifest_to_vault_sync.py`
2. Check hook log: `cat ~/.claude/logs/post-tool-use.log | tail -20`
3. Restart Claude Code (`claude` CLI) — reinitializes hooks on SessionStart
4. Manual trigger: `python3 .claude/scripts/0x_manifest_to_vault_sync.py`
5. If still stuck, check environment: `echo $CT_VAULT && echo $FAERIE_VAULT` — both paths must be non-empty.

### Plugin not loading in Obsidian
1. Settings → Community Plugins → verify toggle is ON for the plugin.
2. Check Obsidian version: Help → About — must be ≥ 1.12.0.
3. Reload plugin: Settings → Community Plugins → find plugin → Reload (circular arrow icon).
4. Full reload: Cmd/Ctrl+P → "Reload app without saving".
5. Open developer console (Ctrl+Shift+I) — check Console tab for error messages.
6. Nuclear option: delete `~/.obsidian/plugins/{plugin-id}/` and reinstall from Community Plugins browser.

### Dataview queries return "Dataview: failed to query"
- Ensure `enableInlineDataview: true` in Dataview settings.
- Frontmatter field names are case-sensitive — `Status` != `status`.
- Wait 5–10 seconds after opening vault for Dataview to index.
- Force reindex: Dataview settings → "Re-index vault".
- Reduce `maxRecursiveRenderDepth` to 2 if performance is slow.

### Frontmatter validation errors
- The `8x_vault_frontmatter_validator.py` hook enforces schema on Write/Edit.
- Error format: `[FRONTMATTER VIOLATION] missing field: doc_hash in /path/to/file.md`
- Fix: add the required field. Required fields: `type`, `status`, `tags` (≥2), `created`, `updated`, `doc_hash`.
- `doc_hash` is auto-populated by hooks — if empty, it means the hash hook hasn't fired yet. Save the file again.

### QuickAdd template not creating file in correct folder
1. Settings → QuickAdd → find your template → gear icon → verify "Folder" is set correctly.
2. Verify `templateFolderPath` in QuickAdd settings points to `Templates/`.
3. Verify the template file exists at the configured path.
4. Check template syntax — Eta engine: use `{{VALUE:prompt text}}` and `{{DATE:format}}`.

### Mission choice not recognized by agents
- Verify the `mission_choice` field is in the **frontmatter** block (between the `---` markers), not in note body.
- Value must exactly match a known mission name (case-sensitive). Check: `cat forensics/manifests/*/manifest*.json | grep '"mission"'` for valid names.
- Re-open the Claude session after updating `mission_choice` — hooks read it on SessionStart.

---

## Quick Reference

| Action | Command |
|--------|---------|
| Create daily note | `Cmd/Ctrl+P` → `QuickAdd: Daily Note` |
| Create mission note | `Cmd/Ctrl+P` → `QuickAdd: Mission Note` |
| Search all notes | `Cmd/Ctrl+Shift+F` |
| Open breadcrumb trail | Sidebar → Breadcrumbs icon |
| Force sync | `python3 scripts/0x_vault_sync_test.py` |
| List active missions | `/run --missions` (in Claude Code) |
| Check frontmatter | `python3 .claude/scripts/8x_vault_frontmatter_validator.py <file>` |

---

*This document is part of the vault-infrastructure-overhaul mission. Generated 2026-05-06.*
