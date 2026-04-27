---
type: vault-status
created: 2026-03-22
status: unified
obsidian_target: CyberOps-UNIFIED
tags: []
doc_hash: sha256:06579d23b8cfb893cff1d6641944632312dc73edf8e09b4f260d756412b10f73
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---
# Vault Status — Reconstruction Log

## Summary

CyberOps-UNIFIED was reconstructed on 2026-03-22 by merging three vault copies:

| Source | Files | Last modified | Role in merge |
|--------|-------|--------------|--------------|
| CyberOps2/ | 18,945 | Mar 15 2026 | **BASE** — most recent living content |
| CyberOps3/ | 72 | Mar 10-11 2026 | Supplement — design docs + design narrative |
| CyberOps1/ | 116 | Mar 10 2026 | Supplement — human memory skeleton |
| CyberOps/ | 357 | contaminated | **NOT MERGED** — Windows plugin repo embedded as literal directory |

## What Was Merged

### From CyberOps3 (00-META supplements)
Files merged because CyberOps3 had a larger or unique version:

| File | Decision | CyberOps3 size | CyberOps2 size |
|------|----------|---------------|---------------|
| 00-DESIGN-NARRATIVE-2026-03-22.md | **ADDED** (unique to CyberOps3) | 10,946 bytes | — |
| 00-OVERVIEW.md | **REPLACED** (CyberOps3 larger) | 10,719 bytes | 10,700 bytes |
| 00-README.md | **REPLACED** (CyberOps3 larger) | 3,108 bytes | 3,094 bytes |

All other 00-META files were identical in CyberOps2 and CyberOps3 — CyberOps2 version kept.

### From CyberOps1 (human memory)
All files from CyberOps1/01-Memories/human/ and CyberOps1/01-Memories/shared/ were
compared against CyberOps2 equivalents. CyberOps2 had equal or larger versions in all cases,
so no replacements were needed. The CyberOps1 files confirm CyberOps2 is authoritative.

| File | Decision | Reason |
|------|----------|--------|
| corrections.md | KEPT CyberOps2 | Same size (636 bytes) |
| user-preferences.md | KEPT CyberOps2 | Same size (1,700 bytes) |
| project-history.md | KEPT CyberOps2 | Same size (1,319 bytes) |
| world-state.md | KEPT CyberOps2 | Same size (1,134 bytes) |

## What Was NOT Merged

### CyberOps/ (contaminated)
This folder is contaminated — it contains the Windows plugin marketplace repo
(`claude-plugins-official/`) as a literal directory tree embedded inside the vault.
This makes it appear to have 357 files but the vast majority are plugin repo files.
The actual vault content is minimal and predates CyberOps2.
**Do not point Obsidian at CyberOps/.**

### Large dump files in 00-Inbox
These files were identified as raw unprocessed dumps and excluded from CyberOps-UNIFIED/00-Inbox:
- `Dail.md` (55KB) — raw dump
- `Untitled.md` (150KB) — raw dump
- `Untitled 4.md` (20KB) — raw dump
- `Untitled 5.md` (22KB) — raw dump

## What the "Last Night" Session Was Working On

Based on the Mar 15 handoff sessions in `03-Agents/sessions/`:
- **Dead-drop + DAE integration** with the vault
- The `ASYNC-COLLAB.md` protocol was the primary design output
- `03-Agents/skills/collab-protocol.md`, `queue-ops.md`, `faerie.md` were written
- `01-Memories/agents/KNOWLEDGE-BASE.md` was updated with validated findings

The Mar 15-16 sessions were the most recent active work. The `handoff--2026-03-15.md`
and `handoff--2026-03-16.md` files in `03-Agents/sessions/` contain the session summaries.

## Recommended Configuration

### Obsidian
Point Obsidian at: `D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED`

Do NOT open: `CyberOps/` (contaminated), `CyberOps1/`, `CyberOps2/`, `CyberOps3/`
(source vaults — preserve but don't use as working vault).

### Environment Variable
Update `DAE_VAULT` env var:
```bash
# In ~/.bashrc or .claude/settings.json env block:
export DAE_VAULT=/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED
```

Windows path: `D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED`

### Claude Code CLAUDE.md / HONEY.md
Update any hardcoded references to `CyberOps/` or `CyberOps2/` vault paths
to point at `CyberOps-UNIFIED/`.

## File Count
- Total files in CyberOps-UNIFIED: ~849 (excluding .git/)
- Markdown files: ~120+
- Scripts: 12
- Agent card backups (00-CLAUDE DEV/): 40+
