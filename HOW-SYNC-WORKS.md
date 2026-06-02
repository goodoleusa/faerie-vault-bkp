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
