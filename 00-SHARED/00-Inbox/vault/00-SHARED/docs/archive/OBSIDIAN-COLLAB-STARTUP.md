# Obsidian Collaboration Setup — LEGACY (See Current Docs)

> **STATUS:** LEGACY — This document predates the 2026-04-05 overhaul.
>
> **For current setup instructions, see:**
> - **New user?** [README.md#obsidian-vault--quick-start](../README.md#obsidian-vault--quick-start) or [INSTALL.md#obsidian-vault-5-minutes](../INSTALL.md#obsidian-vault-5-minutes)
> - **Multi-machine sync?** [docs/VAULT-SYNC-GUIDE.md](VAULT-SYNC-GUIDE.md)
> - **Inside the vault?** [ObsidianVault/00-SHARED/LAUNCH/](../ObsidianVault/00-SHARED/LAUNCH/)
>
> This file is kept for historical reference only.

Canonical **vault files** live in-repo: **`ObsidianVault/`** (this repo). **START-COLLAB** and **COLLAB-FOOTER** are the operator entrypoints.

## Local vault vs `00-SHARED`

- Each machine keeps a **full local vault**. **Only `00-SHARED/`** is replicated via **Syncthing**; remote collaborators **only** receive that subtree. The rest of the vault is **not** shared — others don’t see it, and anything agents need cross-machine should be written under **`00-SHARED/`** (or via terminal hooks targeting it).

## Do this in order

1. **Syncthing** — Point shared sync at **`ObsidianVault/00-SHARED`** only (see **`ObsidianVault/00-SHARED/_README.md`**). Remote users watch **that** folder for changes.
2. **Set env on the workstation:**
   - **`FAERIE_VAULT_SHARED`** = absolute path to `…/ObsidianVault/00-SHARED`
   - Optional **`CLAUDE_HOOKS_STATE`** for one shared `sprint-queue.json` across machines — see **`hooks/state/SPRINT_QUEUE.md`**
   - Optional **`VAULT_DROPS`** = e.g. `…/00-SHARED/inbox/drops` for human-readable dead-drop mirrors
3. **Open Obsidian** at the vault root (folder that contains **`00-SHARED/`**).
4. **Read** **`ObsidianVault/START-COLLAB.md`** (or `[[START-COLLAB]]` inside Obsidian).
5. **Queue mirror vs live:** JSON is **truth**; **`export_queue_to_vault.py`** writes **`00-SHARED/queue/`** (mirror). **Prefer** a hook, git hook, or OS scheduler to re-run export after queue mutations; **manual** re-run only when no automation. **Live** queue UI: hooks / Turn 1 may spawn **`dashboard.py`**; **`dashboard.py --watch`** is the **operator fallback** if no frame appears ([`docs/DESIGN-QUESTIONS.md`](DESIGN-QUESTIONS.md)).
6. **Append footer to long notes:** embed **`[[COLLAB-FOOTER]]`** or `![[COLLAB-FOOTER]]`.

## Do not

- Edit **`queue/SPRINT-QUEUE-LIVE.md`** expecting the JSON queue to change — use **`queue_ops`**, **`/faerie`**, **`/run`**, **`REVIEW-INBOX`**, or **drops**.

## See also

- **`docs/DESIGN-QUESTIONS.md`** — hooks vs scripts, token budget map, hot files to crystallize first.
- **`docs/CONTEXT-CRYSTALLIZATION.md`** — stub; points to `memory-routing.md` + DESIGN-QUESTIONS.
