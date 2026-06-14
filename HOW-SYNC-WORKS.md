# How Sync Works — Vault ↔ Reckon Integration (canonical)

> Canonical as of 2026-06-02. Updated 2026-06-14. Supersedes the faerie2-era doc
> and the syncthing-sidecar-model. The engine repo is **`reckon`** (was `faerie2`).
> The vault root is **operator-configurable** via env vars so reorganizing the vault
> never breaks sync — see "Reorg-resilient sync" below.

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

## Operator Sync — Git + Signed Commits

The vault syncs via git. No Syncthing. No Node or Electron on the VPS. The VPS
holds only the git-tracked markdown files; Obsidian runs client-side on the
operator's machine only.

### How it works

```
Operator edits in Obsidian (Windows)
        │
        ▼
git commit --gpg-sign -m "vault: <description>"
        │
        ▼
git push origin main
        │
        ▼
VPS: git pull   ← cron or inotify-triggered; no Obsidian process on VPS
```

**Signed commit = authoritative human edit.** The signing key is the operator's
identity signal: only commits bearing the operator's GPG/SSH signature are treated
as canonical human edits by the reckon vault-authority-plane charter. Unsigned
commits (e.g., agent writes promoted via hook) are distinguishable in `git log
--show-signature`.

### Cross-platform path note (Windows ↔ WSL)

The vault lives at `D:\0local\gitrepos\faerie-vault\` (Windows) which is the
same tree as `/mnt/d/0local/gitrepos/faerie-vault/` in WSL. The Windows git
client handles push; WSL agents read and write at `/mnt/d/` paths. They are the
same files — no Syncthing junction or symlink required.

### VPS side

- No Obsidian, no Node/Electron container on the VPS.
- The VPS mounts the vault as a plain directory (`git clone` or existing working
  tree at `RECKON_VAULT_PATH`).
- Pull is triggered by cron (`*/5 * * * * git -C /opt/reckon-vault pull --ff-only`)
  or by an inotify/webhook on push receipt — whichever is lighter for the stack.
- After pull, the thin debounced watcher (reckon chart/active/vault-authority-plane
  charter P3) reconciles changed files into the live OH session: system-prompt
  changes reload init-oh-settings, agent-card changes reload agent registry,
  annotation changes flow to corpus/session. Session crystallize outputs
  (NECTAR/HONEY/manifests) write back to the vault on the next commit cycle.

### --profile vault sidecar

The `--profile vault-sync` Docker Compose profile is optional and can be brought
up or down independently without affecting the main reckon stack. It is now
superseded by the git-pull model above; the old Syncthing sidecar docs are in
`.sync/VAULT-SIDECAR-SYNC.md` (retained as historical reference, marked
superseded).

### Conflict model

Because only one operator signs commits and agent writes go through the promotion
pipeline (hooks → forensics → vault commit), write contention is structurally
eliminated. If a fast-forward fails on VPS pull, the resolution is:
`git fetch && git rebase origin/main` — vault state is never force-pushed.
