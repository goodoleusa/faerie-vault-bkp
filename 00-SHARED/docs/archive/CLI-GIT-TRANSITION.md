---
status: complete
archived_on: 2026-03-29
archived_by: fullstack-developer agent
---

# CLI-GIT to faerie2 Transition

> **LEGACY:** This document predates the 2026-04-05 overhaul.
> For current docs, see [README.md](../README.md) or the vault LAUNCH/ folder.
> Kept for historical reference.

## Summary

faerie2 (`/mnt/d/0LOCAL/gitrepos/faerie2/`) is now the **canonical dev repo** for the faerie system.
CLI-GIT (`/mnt/d/0LOCAL/gitrepos/00-claude-faerie-cli-git/`) is archived — do not merge new work there.

## What Was Ported

### Final commit from CLI-GIT: `5ac333e` (2026-03-25)

Both files are now in faerie2 at commit `9e5cc07`.

| File | CLI-GIT SHA256 | Lines |
|------|---------------|-------|
| `.claude/hooks/state/queue_ops.py` | `14f300c2...` | 598 |
| `.claude/skills/run/claim_task.py` | `98127713...` | 352 |

**Features ported:**
- 3-tier queue resolution: env var → repo-level → global fallback
- Task `category` field: investigation / infrastructure / training / publishing / review / meta
- Auto-inference of category from goal text keywords
- Recency boost in sort key (linear decay 0.9→0.0 over 48 hours; fresh tasks rank higher within tier)
- `.claude/.claude` double-nesting guard in path resolution
- `_resolve_claude_home()` handles WSL + Git Bash + Windows-native Python path mangling
- `--category` filtering in `/run` with aliases (infra, invest, train, pub)
- `task["status"] = "in_progress"` (was `"claimed:{session_id}"`) — cleaner state model

## What Was NOT Ported (intentionally)

| Item | Reason |
|------|--------|
| `plugins/cyberops-orchestration/hooks/` | Investigation-specific plugin; not part of faerie core |
| `ObsidianVault/` changes (unstaged) | Identical unstaged changes in both repos — Obsidian plugin manifests; not faerie code |
| Feature branches (business-plan, cognitive-architecture, evals, ui-concepts) | Already merged into faerie2 main via 703d8a9 and prior merges |

## CLI-GIT vs faerie2 Structure

| CLI-GIT | faerie2 | Notes |
|---------|---------|-------|
| `modules/memory/`, `modules/orchestration/` | `.claude/scripts/`, `.claude/hooks/` | Consolidated from brain/ + nervous-system/ (moved to .claude/garbage/ 2026-04-05) |
| `.claude/commands/` (deleted in CLI-GIT) | `.claude/skills/` | Commands to skills migration complete |
| `plugins/` | (not present) | Investigation-specific plugin |

## faerie2 Has (CLI-GIT Lacks)

- `LAYOUT.md` — repo layout doc
- `_paths.py` — path helpers
- `.claude/scripts/` — core runtime modules (consolidated from brain/)
- `.claude/hooks/` — hooks and state (consolidated from nervous-system/)
- `settings.json.portable` — portable settings variant
- `commands/` — slash commands layer (separate from skills)

## Remote Configuration

| Repo | Remote | URL |
|------|--------|-----|
| faerie2 | `origin` | `git@github.com:goodoleusa/faerie2.git` |
| CLI-GIT | `faerie2` | `git@github.com:goodoleusa/faerie2.git` (same upstream) |

## Archive Plan for CLI-GIT

CLI-GIT has 72 commits of history. Do NOT delete. Steps:
1. Add ARCHIVED.md at CLI-GIT root marking superseded date
2. Optionally rename dir to `00-claude-faerie-cli-git-ARCHIVED`
3. No further commits

Git history = provenance. Do not squash or delete.

## Next Tasks Unblocked

- Add ARCHIVED.md to CLI-GIT root
- Push faerie2 main to origin: `cd /mnt/d/0LOCAL/gitrepos/faerie2 && git push origin main`
- Vault sync / annotation wire-in (infrastructure task)

## Verification

```bash
cd /mnt/d/0LOCAL/gitrepos/faerie2
git log --oneline -3
grep "category" .claude/hooks/state/queue_ops.py | head -3
python3 -c "import ast; ast.parse(open('.claude/hooks/state/queue_ops.py').read()); print('OK')"
python3 -c "import ast; ast.parse(open('.claude/skills/run/claim_task.py').read()); print('OK')"
```
