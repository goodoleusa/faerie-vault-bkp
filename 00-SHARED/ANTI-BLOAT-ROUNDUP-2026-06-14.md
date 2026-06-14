# Anti-Bloat Roundup — 2026-06-14

> Canonical audit of stray content across `/mnt/d`. Lands in both vaults.
> Companion: `CyberOps-UNIFIED/00-SHARED/ANTI-BLOAT-ROUNDUP-2026-06-14.md`

---

## Stray Vault Copies

| Path | Size | Status | Action |
|---|---|---|---|
| `/mnt/d/0LOCAL/faerie-vault/` | 5.0M | TOMBSTONED 2026-06-03 — 141 files migrated to canonical, TOMBSTONE.md confirms | **DELETE** — migration confirmed complete |
| `/mnt/d/mnt/d/0LOCAL/gitrepos/faerie-vault/` | ~5M | Doubled/nested path — agent went wrong on path resolution | **DELETE** entire `/mnt/d/mnt/` tree |

**Canonical vault (renamed this session):** `/mnt/d/0LOCAL/gitrepos/reckon-vault/`
GitHub: `goodoleusa/reckon-vault`

---

## Stray CT_VAULT Content

| Path | Size | Contents | Action |
|---|---|---|---|
| `/mnt/d/0LOCAL/CT_VAULT/` | 264K | Forensic governance docs (investigation architecture, MCP design, settings sync), dated dirs 2026-04-28/29 | **CONSOLIDATE** ct-vault/ docs → `CyberOps-UNIFIED/10-Investigations/`; check if already in canonical cybertemplate repo |
| `/mnt/d/0LOCAL/CT_VAULT/ct-vault/` | — | 9 governance docs (forensic-governance, mcp-architecture, vault-architecture, etc.) | **REVIEW** — may duplicate reckon docs |

---

## Stray Forensics (Outside Repos)

| Path | Size | Contents | Action |
|---|---|---|---|
| `/mnt/d/0LOCAL/0forensics/` | 9.1M | `coc.jsonl`, `cybertemplate/` subdir, dated dirs 2026-05-02 to 2026-05-04, `FORENSICS-MANIFEST.md` | **REVIEW before delete** — dated dirs may have unique session metrics; coc.jsonl may need merging into reckon/forensics |
| `/mnt/d/0LOCAL/0forensics/cybertemplate/` | — | Investigation forensics written to wrong path | **CONSOLIDATE** → canonical path in `gitrepos/cybertemplate/forensics/` |
| `/mnt/d/0LOCAL/.openhands/forensics` | — | OH session wrote forensics outside reckon repo | **REVIEW** — likely safe to archive to reckon/forensics/_archive |

---

## Session Metrics — Stray / Missing

| Path | Status |
|---|---|
| `/mnt/d/0LOCAL/.claude-backup/forensics/session-metrics.jsonl` | Backup copy — intentional; canonical is reckon/forensics/main-metrics.jsonl |
| `/mnt/d/0LOCAL/0forensics/` (dated dirs 05-02 to 05-04) | May contain session metrics from wrong-path writes; **verify against reckon/forensics/_archive** for gaps |

**Canonical session metrics:** `/mnt/d/0LOCAL/gitrepos/reckon/forensics/main-metrics.jsonl`
Archived series: `/mnt/d/0LOCAL/gitrepos/reckon/forensics/_archive/{date}/main-metrics.jsonl`

---

## Stray Cybertemplate / CriticalExposure Content

| Path | Size | Action |
|---|---|---|
| `/mnt/d/0LOCAL/cybertemplate/` | 216K | Scripts dir only — check if duplicates `gitrepos/cybertemplate/scripts/`; delete if so |
| `/mnt/d/0LOCAL/cybertemplatedeprecated/` | — | Deprecated — **DELETE** after confirming nothing unique |
| `/mnt/d/0LOCAL/0forensics/cybertemplate/` | — | Wrong-path forensics — **CONSOLIDATE** → `gitrepos/cybertemplate/forensics/` |
| `/mnt/d/0LOCAL/cybertemplate-rawdata-b2.log` | — | B2 upload log — archive to cybertemplate repo or delete |
| `/mnt/d/0LOCAL/InvestigationData/` | — | Jan 2025 OPM emails investigation data — **MOVE** → `CyberOps-UNIFIED/30-Evidence/` or `gitrepos/0-CriticalRAWDATA/` |

---

## Loose Files at /mnt/d/0LOCAL Root

| File | Action |
|---|---|
| `NECTAR_MIGRATION_MANIFEST.md` | Archive to `gitrepos/reckon/forensics/_archive/` |
| `NECTAR_MIGRATION_PATCHES.json` | Same |
| `NECTAR_QUICK_APPLY.sh` | Same |

---

## Stray Ghost Sync Trees (ALREADY ARCHIVED)

Caught in 2026-06-04 anti-bloat consolidation — moved to `_archive-2026-06-04/`:
- `00-Inbox/_archive-2026-06-04/faerie-vault-ghost-sync/`
- `00-SHARED/_archive-2026-06-04/00-SHARED-ghost-sync/faerie-vault/`

Status: **DONE** — tracked in VAULT-CANONICAL-INDEX.md

---

## Vault Rename (this session)

- **Old name:** `faerie-vault` → **New name:** `reckon-vault`
- Local: `/mnt/d/0LOCAL/gitrepos/faerie-vault/` → `/mnt/d/0LOCAL/gitrepos/reckon-vault/`
- GitHub: `goodoleusa/faerie-vault` → `goodoleusa/reckon-vault` (user renamed on GitHub)
- `.git/config` remote URL updated to `git@github.com:goodoleusa/reckon-vault.git`
- Update `RECKON_VAULT_PATH` in `reckon/.env` if pointing to sibling `../faerie-vault` → `../reckon-vault`

---

## Recommended Execution Order

```
1. DELETE /mnt/d/0LOCAL/faerie-vault/                    (TOMBSTONED, safe)
2. DELETE /mnt/d/mnt/d/                                  (doubled path artifact)
3. REVIEW /mnt/d/0LOCAL/0forensics/ dated dirs           (check for unique session metrics)
4. CONSOLIDATE 0forensics/cybertemplate → gitrepos/cybertemplate/forensics/
5. REVIEW /mnt/d/0LOCAL/CT_VAULT/ct-vault/ docs         (check for duplication)
6. DELETE /mnt/d/0LOCAL/cybertemplatedeprecated/          (after uniqueness check)
7. ARCHIVE NECTAR_MIGRATION_* files → reckon/forensics/_archive/
8. UPDATE reckon/.env: RECKON_VAULT_PATH=../reckon-vault
```
