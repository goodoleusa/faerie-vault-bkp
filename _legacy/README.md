---
type: legacy-shelf-readme
status: archived
last_updated: 2026-05-22
purpose: forensic archive of pre-2026-05-22 vault conventions
---

# `_legacy/` — Pre-2026-05-22 Vault Conventions

This shelf holds folders that predate the canonical daily-folder
convention set on **2026-05-22**:

  Canonical:  `00-SHARED/Daily/{YYYY-MM-DD}/`

Everything here is **forensic archive, not an active surface**. Do
not write new content into these folders. Do not delete them either
— they preserve session history that COC entries and earlier
narratives may reference by path.

## What's shelved here

| Folder | Why it's here |
|---|---|
| `2026-04-28/` | Old top-level dated session folder (Vault Ops Dashboard + 15 tracked files). Last touched ~Apr 30. |
| `2026-05-10/` | Empty top-level dated folder leftover from older convention. Kept for path-history continuity. |
| `DAILYFOLDERS/` | Older daily-folder convention under `00-SHARED/`. Contained `agents/2026-05-04/test-agent/` only (2 files). |

## Why shelve instead of delete

1. **History preservation** — git history is preserved via `git mv`
   for the tracked `2026-04-28/` tree
2. **Path-reference safety** — any COC entries, manifests, or
   narratives that linked to the old paths still resolve via the
   shelf prefix
3. **Top-level decluttering** — keeps the active vault root focused
   on the new canonical surfaces (`00-Welcome/`, `10-Charters/`,
   `80-Publications/`, `00-SHARED/Daily/`)

## Looking for something here?

If you came in via an old link, that's fine — read what you need.
For active work, return to `00-HOME.md` and use the current
dashboards listed there.
