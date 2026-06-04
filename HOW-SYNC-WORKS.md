# How Sync Works — Vault ↔ Reckon Integration (canonical)

> Canonical as of 2026-06-02. Supersedes the faerie2-era doc. The engine repo
> is **`reckon`** (was `faerie2`). The vault root is **operator-configurable**
> via env vars so reorganizing the vault never breaks sync — see
> "Reorg-resilient sync" below.

## Three-Store Architecture

**faerie-vault** is part of a three-layer synchronization system:

1. **Git Canonical** — `faerie-vault/` (this repo)
   - Source of truth for vault structure
   - Investigation notes, findings, crystallized insights
   - Tracked in version control

2. **Forensics (Ephemeral)** — `reckon/forensics/`
   - Agent outputs, manifests, session metrics
   - Real-time events from active orchestration
   - Not in vault; accessed via Dataview queries

3. **B2 WORM Backup** — immutable cloud storage
   - Disaster-recovery backup of forensics
   - Timestamp-locked, deletion-proof
   - Referenced for audit trail

**Flow:**
```
Agent writes to forensics/ → Vault Dataview queries live data → User reviews in Obsidian
                         ↓
                    B2 WORM backup (async)
                         ↓
                  Periodic snapshot → git commit → this repo
```

## Reorg-resilient sync (the key folders are VARIABLES, not hardcoded)

The vault is always growing and contracting. Sync must survive you moving,
renaming, or restructuring folders. The rule: **a small set of key roots are
set by env vars; everything else is discovered relative to them.** Never
hardcode an absolute vault path in code.

### The variables (set in `reckon/.env`)

| Var | Meaning | Default |
|---|---|---|
| `RECKON_VAULT_PATH` | Vault root the MCP server may read/write (write-gated). Comma-separated for multiple roots. Relative paths resolve against the repo root. | `../faerie-vault` |
| `RECKON_VAULT_ROOT` | Alt/explicit absolute vault root (container/prod). | `/opt/reckon-vault` |
| `RECKON_REPO` | The reckon engine repo root (forensics live here). | walk-up autodetect |
| `RECKON_COC_DIR` | COC/forensics dir (defaults to `$RECKON_REPO/forensics`). | `$RECKON_REPO/forensics` |

The MCP server resolves these at startup (`server.py::_resolve_vault_roots`)
into `_VAULT_ALLOWED_ROOTS`. Write-mode vault ops are gated to those roots;
read-only audit works against any path under them. **Move the vault → change
ONE env var → restart. No code edit.**

### Keep sync from breaking when you reorganize

1. **Pin the ROOT, not the sub-folders.** Point `RECKON_VAULT_PATH` at the
   vault top. The plugin + tools address sub-folders by *relative* name
   (`Charters/`, `00-SHARED/SystemPrompts/`, `Human/`, `30-Dashboards/`), so
   moving notes within the vault doesn't break the contract — only renaming a
   *key* folder does.
2. **If you rename a key folder, change its setting — don't edit code.** The
   plugin settings (Reckon → settings) expose: blueprints dir, prompts dir,
   annotations (Human) dir, MCP URL. Dataview/Datacore queries point at
   `reckon/forensics/{date}/` by relative path.
3. **Dataview queries read forensics, not vault internals.** Because live
   tables read from `reckon/forensics/` (stable, append-only), reshuffling
   vault note folders never affects the dashboards.
4. **Run the dead-call audit after a big reorg.** It catches any path that
   drifted:
   `python3 reckon/.agents/skills/script-quarantine/scripts/audit_dead_calls.py`

## Live Metrics via Dataview

**Example query** (`30-Dashboards/Session-Metrics.md`):

```dataview
TABLE agent_type, reputation_score, task_count
FROM "reckon/forensics/evals"
WHERE contains(file.path, "agent-reputation") AND file.mtime > now - dur(1 hour)
SORT file.mtime DESC
```

**Requirements:**
- Dataview plugin enabled in Obsidian (the Reckon plugin vendors a subset)
- `RECKON_VAULT_PATH` set so the server resolves the vault root
- `reckon/forensics/evals/` contains recent JSON files

## Recommended vault folders for the round-trip loop

| Folder | Purpose | Who writes |
|---|---|---|
| `Human/{YYYY-MM-DD}/` | Annotation drop zone (plugin writes here; `reckon_collab` mirrors to `forensics/annotations/`) | human + plugin |
| `00-SHARED/SystemPrompts/<name>.md` | System-prompt mirror (frontmatter `prompt_file`) for the safe push-back loop (`reckon_prompt verb=update`, commit-only) | plugin import |
| `OH-System-Prompts/` | Canonical prompt source | reckon |
| `Charters/{active,proposals,sealed}/` | Charter lifecycle | reckon + plugin |
| `Blueprints/*.njk` | Output-formatting templates (charter/manifest writes render through these) | shared |
| `30-Dashboards/` | Live Dataview/Datacore tables over `forensics/{date}/` | shared |

## Committing Vault Changes

```bash
cd <vault-root>
git add -A
git commit -m "docs: investigation update"
git push origin main
```

## Sync Conflicts

- **Vault vs forensics:** Vault = collaboration source (human decisions);
  forensics = orchestration output. Vault is authoritative; forensics are input.
- **B2 vs vault:** B2 is immutable; vault takes precedence for ongoing work.
  Validate with `reckon/scripts/6e_forensics_index.py`.

## Standalone modes

- **Vault without reckon:** Dataview queries show "no results"; use as a
  normal Obsidian vault.
- **Reckon without vault:** agents write to `forensics/` normally; query via
  Python/bash. Add the vault later by cloning it and setting
  `RECKON_VAULT_PATH`.

---

See `reckon/INSTALL.md` for environment setup and `reckon/CHART.md` for the
repo map.

---

## [Source: VAULT-SYNC-GUIDE.md] Syncthing Setup for Cross-Platform Collaboration

> **TL;DR:**
> - Syncthing keeps the Obsidian vault in sync across Windows, WSL, and ZimaBoard.
> - Add both Windows path (`D:\...`) and WSL path (`/mnt/d/...`) as separate Syncthing folders.
> - Conflict resolution: Windows GUI wins; WSL is read-mostly.
> - See the Syncthing web UI at `http://127.0.0.1:8384` to monitor sync status.
> - ZimaBoard is the off-site backup node — always-on, runs headless Syncthing.

Two investigators, two vaults, one shared layer. This guide sets up bidirectional sync of `00-SHARED/` only — private folders (01-PROTECTED/, 30-Evidence/) stay local.

### Architecture Overview

```
Person A (Windows 11 + WSL2)          Person B (macOS / Linux)
─────────────────────────────          ──────────────────────────
CyberOps-UNIFIED\                      ~/CyberOps-Vault/
  01-PROTECTED\   ← local only           01-PROTECTED/  ← local only
  30-Evidence\    ← local only           30-Evidence/   ← local only
  00-SHARED\  ◄─── junction ───►  D:\Syncthing\CyberOps-SHARED\
                                         ▲
                                   Syncthing sync
                                         ▼
                               ~/Syncthing/CyberOps-SHARED/
                                         │
                                  symlink ▼
                               ~/CyberOps-Vault/00-SHARED/
```

**Why symlinks/junctions:** Syncthing syncs a flat folder. The junction/symlink lets Obsidian see `00-SHARED/` as part of its vault tree while Syncthing operates on it independently. Neither side's private folders are ever exposed to the sync layer.

### Person A Setup (Windows 11 + WSL2)

Syncthing runs natively on Windows — do not install it inside WSL.

```powershell
# Install via winget
winget install Syncthing.Syncthing

# Create sync folder
New-Item -ItemType Directory -Path "D:\0LOCAL\Syncthing\CyberOps-SHARED" -Force

# Create junction (run as Administrator)
New-Item -ItemType Junction `
  -Path "D:\0LOCAL\Syncthing\CyberOps-SHARED\00-SHARED" `
  -Target "D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED\00-SHARED"
```

Add folder in Syncthing UI (`localhost:8384`): Label=`CyberOps-SHARED`, Type=`Send & Receive`, Versioning=`Staggered (30 days)`. Ignore patterns: `.obsidian`, `.trash`, `*.sqlite*`, `__pycache__`, `*.pyc`, `.DS_Store`.

### Person B Setup (macOS / Linux)

```bash
# macOS
brew install syncthing && brew services start syncthing

# Linux
sudo apt install syncthing && systemctl --user enable syncthing

# Create directories and symlink
mkdir -p ~/CyberOps-Vault/00-SHARED ~/Syncthing/CyberOps-SHARED
ln -s ~/CyberOps-Vault/00-SHARED ~/Syncthing/CyberOps-SHARED/00-SHARED
```

Accept the shared folder from Person A in the Syncthing UI; set local path to `~/Syncthing/CyberOps-SHARED`.

### Ownership Protocol (Critical)

**One writer per file — eliminates most conflicts before they happen.**

| Files | Owner |
|-------|-------|
| `Agent-Outbox/`, `Human-Inbox/`, `Droplets/`, `Dashboards/` | Person A's agents (write); both humans (read) |
| `Queue/sprint-queue.md`, `00-Inbox/` | Humans write; agents read |
| `.ann.md` files | Designated human only |

Annotation convention: `network-map.md` → annotate as `network-map.ann.md` (sibling file). Agents never touch `.ann.md`.

### Conflict Prevention

Syncthing uses last-write-wins and surfaces conflicts as `.sync-conflict-YYYYMMDD-HHMMSS-deviceid` files. Conflicts are rare because agent outputs are write-once. If a conflict appears: open both, merge, save to original filename, delete the conflict file.

### WSL agents

The vault at `D:\0LOCAL\...` is accessible from WSL at `/mnt/d/0LOCAL/...`. Syncthing runs on Windows side, writes to `D:\`. WSL agents read/write at `/mnt/d/` — they see the same files.

### Syncthing Ports

- TCP 22000 — data sync
- UDP 21027 — local discovery

*Full setup guide with all 9 sections archived at `00-SHARED/docs/archive/VAULT-SYNC-GUIDE.md`.*
