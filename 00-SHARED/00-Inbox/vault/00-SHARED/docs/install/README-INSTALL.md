# One-click / one-path faerie + collab setup

These scripts bundle **module-separated** steps so you rarely run raw `queue_ops` / `export_queue_to_vault.py` / `dashboard.py` by hand for initial setup.

## Product bundles (installers)

| SKU | What gets copied to `~/.claude` | Path | Flag |
|-----|----------------------------------|------|------|
| **Core (open source)** | Orchestration only — queue, dashboard, hooks, agents, skills; **no** memory module | `releases/<os>/orchestration/.claude/*` | `-InstallCore` / `install-faerie.sh --core` |
| **Full (paid / licensed)** | **Combined** drop: orchestration **+ memory module** (single tree). Memory is **not** sold or installed separately. | `releases/<os>/.claude/*` (`s2 --profile full`) | `-InstallFull` / `install-faerie.sh --full` |

| Module | What | Flag / script |
|--------|------|-----------------|
| **Collab env** | `~/.claude/faerie-env.json` + shell helpers; `FAERIE_PROJECT_ROOT`, `FAERIE_VAULT_SHARED`, optional `CLAUDE_HOOKS_STATE`, `VAULT_DROPS` | `-CollabEnv` / `install-faerie.sh --env-only` |
| **Workstation** | Refresh vault mirror + start Mission Control | `~/.claude/start-faerie-workstation.ps1` or `.sh` |

**Maintainers:** `releases/<os>/memory/.claude/` still exists as an **s2** output for manual merges or packaging — it is **not** a customer-facing third installer; paid users get memory **only** inside **Full**.

**Prerequisite:** From repo root, build drops once:

```bash
python scripts/0b_build_release_bundles.py --profile all
```

That produces orchestration, memory, and full trees per OS.

---

## Windows (PowerShell)

From **flowsearch repo root** (or anywhere — scripts resolve `FlowsearchRoot` by default):

```powershell
cd D:\path\to\flowsearch\scripts\install
.\install-faerie.ps1 -Interactive
```

Or double-click **`install-faerie.cmd`** (repo `scripts\install\`) — runs the interactive installer (choose **O** = core OSS or **F** = full paid).

**Silent examples**

```powershell
# Open-source core (orchestration only)
.\install-faerie.ps1 -InstallCore -CollabEnv `
  -FaerieProjectRoot "D:\0LOCAL\gitrepos\cybertemplate" `
  -FaerieVaultShared "D:\path\to\flowsearch\ObsidianVault\00-SHARED" `
  -ReleaseTarget windows-native
```

```powershell
# Full combined (paid — includes memory)
.\install-faerie.ps1 -InstallFull -CollabEnv -ReleaseTarget windows-native
```

**Second window (queue mirror + dashboard):**

```powershell
& "$env:USERPROFILE\.claude\start-faerie-workstation.ps1"
```

Dot-source env in any PowerShell session (optional if User env was set):

```powershell
. "$env:USERPROFILE\.claude\faerie-env.ps1"
```

---

## macOS / Linux / WSL (bash)

```bash
cd /path/to/flowsearch/scripts/install
chmod +x install-faerie.sh start-faerie-workstation.sh
./install-faerie.sh
```

**Core (OSS):** `RELEASE_TARGET=macos ./install-faerie.sh --core`  
**Full (paid):** `RELEASE_TARGET=macos ./install-faerie.sh --full`  
**Env only:** `FAERIE_VAULT_SHARED=/path/to/00-SHARED ./install-faerie.sh --env-only`

**Second window:**

```bash
~/.claude/start-faerie-workstation.sh
```

---

## Config file

`~/.claude/faerie-env.json` is the single source for paths (see `faerie-env.example.json` in this folder). Installers generate:

- **Windows:** `faerie-env.ps1` (dot-source) + **User**-level env vars for new terminals
- **Unix:** `faerie-env.sh` (source)

**Syncthing** is not automated — point it at **`ObsidianVault/00-SHARED`** only; see **`ObsidianVault/START-COLLAB.md`**.

---

## No Obsidian app required

- **Claude Code / CLI:** **Core** or **Full** both give you **`sprint-queue.json`** + **`dashboard.py`** under `~/.claude`. You never need the Obsidian **app**.
- **`FAERIE_VAULT_SHARED`** is just a **folder** for optional markdown mirrors. If unset / missing, hooks **skip** vault writes (`resolve_vault_shared()` → `None`).
- **`start-faerie-workstation`** may log **SKIP** for export when vault is unset — dashboard still starts.

## Module separation (for maintainers)

- **Core installer** → `orchestration/.claude` only.
- **Full installer** → `.claude` at `releases/<os>/.claude` (includes memory per `s2` full profile).
- **Collab env** = paths only — safe to re-run.
- **Workstation launcher** = optional export + `dashboard.py --watch`.

---

## See also

- `docs/OBSIDIAN-COLLAB-STARTUP.md` — minimal collab narrative
- `releases/README.md` — manual copy paths if you skip the scripts
- `ObsidianVault/START-COLLAB.md` — vault + sync
