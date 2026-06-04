# SOURCE-MIRROR-DIRECTION

**Direction:** Global canonical → Faerie2 shippable derivative (one-way export only)

## Context

G4 mutation (2026-04-24) inverted the source/mirror direction of `settings.json`. The global `/mnt/d/0LOCAL/.claude/settings.json` is the authoritative copy; faerie2 is a shippable mirror for reproducible builds.

## Truth

- **Global canonical:** `/mnt/d/0LOCAL/.claude/settings.json` (daily workflow, human edits)
- **Faerie2 derivative:** `/mnt/d/0local/gitrepos/faerie2/.claude/settings.json` (exported copy, shipped to reproducible builds)
- **Hook/script paths:** Both locations have full copies of all hooks and scripts; settings.json points to ONE location (the global one)

## Sync Flow

```
Human edits in global:
  /mnt/d/0LOCAL/.claude/settings.json
           ↓
  Export script (manual or periodic):
    python3 scripts/7x_export_settings.py --to-faerie2
           ↓
Faerie2 receives mirror:
  /mnt/d/0local/gitrepos/faerie2/.claude/settings.json
           ↓
Git commit + push (to ship reproducible build)
```

## Anti-Pattern

Never auto-sync from faerie2 → global. Never target settings.json hook paths at faerie2 (that makes runtime config point to the mirror, not the source).

## Implementation

- All hook commands in `/mnt/d/0LOCAL/.claude/settings.json` point to `/mnt/d/0LOCAL/.claude/hooks/` and `/mnt/d/0LOCAL/.claude/scripts/`
- Faerie2 has identical copies of all hooks/scripts in its own `/mnt/d/0local/gitrepos/faerie2/hooks/` and `scripts/` directories
- When settings.json is exported to faerie2, the path strings are NOT rewritten (they stay pointing at global), because faerie2 is a cold-start environment; it reads from global locations at runtime
- If faerie2 is cloned to a new machine, a bootstrap script patches settings.json paths to point at the local faerie2 paths

## Hooks & Scripts

Both locations remain complete:
- `/mnt/d/0LOCAL/.claude/hooks/` — working set, all files
- `/mnt/d/0LOCAL/.claude/scripts/` — working set, all files
- `/mnt/d/0local/gitrepos/faerie2/hooks/` — shipped copy, all files (for git history + audit)
- `/mnt/d/0local/gitrepos/faerie2/scripts/` — shipped copy, all files (for git history + audit)

Do not delete from one side when the other has the file.

## Recovery

If settings.json gets inverted again:
1. Read `/mnt/d/0LOCAL/.claude/settings.json`
2. Replace all `/mnt/d/0local/gitrepos/faerie2/hooks/` with `/mnt/d/0LOCAL/.claude/hooks/`
3. Replace all `/mnt/d/0local/gitrepos/faerie2/scripts/` with `/mnt/d/0LOCAL/.claude/scripts/`
4. Write atomically (tmp + rename)
5. Verify no faerie2 paths remain in hooks/scripts sections

---

**Status:** Adopted 2026-04-24 (post-G4 correction)  
**Related:** CLAUDE.md, agents.md spawn protocol  
**Mutation:** G4 (inverted direction, corrected same session)
