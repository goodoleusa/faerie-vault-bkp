---
type: system-changelog
date: 2026-03-22
tags: [system, vault, sync, hooks, env]
session: faerie-20260322
doc_hash: sha256:c7d83fc791d65376807c20e2c541bc46907dc244d877627c6e1d3224705aafb1
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---

# System Change — Vault Sync Wiring + Env Var Rename

*What changed in this session, in plain language. Use this if something breaks.*

---

## What Was Changed

### 1. New env var: `CT_VAULT` (replaces `DAE_VAULT`)

The vault environment variable was renamed from `DAE_VAULT` to `CT_VAULT` because:
- `DAE` (data-analysis-engine) is a generic template repo that gets shared/open-sourced — it shouldn't have an investigation-specific vault
- `CT` = CyberTemplate (the investigation-specific repo) — this is the one that writes to the vault

**In settings.json:** `DAE_VAULT` → `CT_VAULT`. Also added `CT_VAULT_SHARED` (the `00-SHARED/` write zone).

**In scripts:** `vault_narrative_sync.py` reads `CT_VAULT` first, falls back to `FAERIE_VAULT` (legacy) for compatibility.

---

### 2. New Stop hook: `vault_narrative_sync.py`

**File:** `~/.claude/scripts/vault_narrative_sync.py`

**What it does:** Runs automatically at the end of every Claude session. Reads `REVIEW-INBOX.md` and `NECTAR.md` for new HIGH-priority findings (those you haven't seen yet) and writes them to `00-SHARED/Agent-Outbox/{date}-findings.md`.

**Why:** So you don't have to ask "write findings to vault" every session — it happens automatically.

**State tracking:** `~/.claude/hooks/state/vault-sync-state.json` tracks the last line synced in INBOX and NECTAR, so each run only processes new content.

**Wired into:** `settings.json` → `Stop` hook array (runs after `session_stop_hook.py`).

---

### 3. New script: `vault_manifest.py`

**File:** `~/.claude/scripts/vault_manifest.py`

**What it does:** SHA-256 hashes vault files and writes a timestamped manifest to `~/.claude/memory/forensics/vault-manifests/`. Also appends a COC (chain-of-custody) entry to the investigation's `master-coc.jsonl`.

**Why:** Court-readiness. The agent hashes files when it writes them. You hash files when you annotate them. The difference between the two hashes proves which parts are agent-written vs. human-annotated.

**How to seal your annotations:**
```bash
python3 ~/.claude/scripts/vault_manifest.py \
  --vault /mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED \
  --sign-only --author human
```

---

### 4. New rule file: `vault-safety.md`

**File:** `~/.claude/rules/vault-safety.md`

Defines what agents can and can't do to the vault:
- Never `rsync --delete`
- `00-PROTECTED/` = absolute no-touch zone
- Write zone = `00-SHARED/` only
- Backup before bulk writes
- Agents never overwrite the `## Your Annotations` section of any note

---

### 5. Skill vs command disambiguation

**Problem:** `/faerie` was listed in both `commands/` (user slash command) and the Skill tool's list (programmatic invocation). This caused confusion about which mechanism to use.

**Fix:** Rule added to `vault-safety.md` and `HONEY.md`: if a name is in `~/.claude/commands/`, it is always a COMMAND. The Skill tool listing is informational — never call a command/ entry via the Skill tool. When user types `/faerie`, it ALWAYS uses the command, not the skill.

---

### 6. Investigation narratives written to vault

Four wave narratives created in `10-Investigations/criticalexposure/`:
- `WAVE-01-The-Emergence.md` — the Jan 14 inflection
- `WAVE-02-The-Infrastructure.md` — Packetware/Prometheus/Hetzner
- `WAVE-03-The-Foreign-Fingerprints.md` — Aeza/Baxet, reflected TLS, Fisher tests
- `WAVE-04-The-Malware.md` — chrome_proxy.exe, DOGE C2

`Annotation-Dash.md` at vault root — court prep dashboard with 6 smoking guns in plain prose.

All files hashed and COC-logged in `master-coc.jsonl`.

---

## If Something Breaks

| Symptom | Check |
|---|---|
| Vault sync not running on session end | Check Stop hook in `settings.json` — look for `vault_narrative_sync.py` |
| "Vault not found" error | Check `CT_VAULT` env var in `settings.json` points to correct path |
| Old code still using `DAE_VAULT` | `vault_narrative_sync.py` has fallback: `CT_VAULT → FAERIE_VAULT → hardcoded default` |
| Files written outside 00-SHARED/ | Check permissions in `settings.json` — Write is restricted to `00-SHARED/**` |
| COC manifest missing | Check `~/.claude/memory/forensics/vault-manifests/` — should have one per session |

---

## Previous System (Deprecated)

This setup deprecates the previous vault sync approach which:
- Used `FAERIE_VAULT` env var (now `CT_VAULT`)
- Had no automated Stop hook sync (required manual request)
- Had no COC hashing of vault files
- Wrote to vault root instead of `00-SHARED/`

The previous approach is still partially functional (fallback chain maintained) but this is the canonical setup going forward.
