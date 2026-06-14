# VAULT-REORG-PLAN.md — Claude Code Execution Reference

> **Mission:** vault.authority.plane · Bearing: S (ship deliverable)
> **Canonical date:** 2026-06-14
> **Companion:** `reckon/chart/active/vault-authority-plane/brief.md` (phases P1–P5 source)

---

## Current State vs Target State

| Dimension | Current | Target |
|---|---|---|
| Sync mechanism | Syncthing sidecar (NOT-YET-DEPLOYED) | Git-only; operator pushes signed commits |
| VPS Obsidian | Planned Docker/Electron container | None — Obsidian runs on operator machine only |
| Human authority signal | None | Signed commit = authoritative human edit |
| Vault↔OH watcher | Polling / Syncthing | Thin debounced event-driven watcher |
| Settings-push gate | None | Valid operator ed25519 sig required |
| Key backup | None | Encrypted private keys → B2 WORM |
| Annotation sync | Manual | vault annotation → corpus/session async |

---

## DO NOT TOUCH

- `forensics/` tree in any reckon repo — immutable, COC-chained
- `coc.jsonl` and any COC entry files
- `00-Patent/` and patent draft files (`Patent draft.md`, `PATENT DRAFT 2.md`)
- `_archive-2026-06-04/` and `_archive/` trees — archived, do not modify
- `scripts/_archive/` — deprecated scripts, leave in place
- `HOW-SYNC-WORKS.md` — keep for three-store architecture context; update Syncthing section only (add deprecation notice)
- `.obsidian/` config — Obsidian manages this; do not restructure

---

## Interop Contract: faerie-vault ↔ reckon

| Contract point | Detail |
|---|---|
| `RECKON_VAULT_PATH` | Set in `reckon/.env`; defaults to `../faerie-vault`; single env-var controls all vault resolution |
| `RECKON_VAULT_ROOT` | Absolute override for VPS paths |
| MCP server gate | `server.py::_resolve_vault_roots` — vault writes gated to `_VAULT_ALLOWED_ROOTS` |
| Signed commit authority | `vault_sign.py` writes ed25519 sig → reckon MCP verifies sig before accepting settings-push |
| Dataview → forensics | `30-Dashboards/` queries `$RECKON_REPO/forensics/` live; no copy, no sync |
| Manifest reading | Via Dataview queries against symlinked or mounted forensics path |
| Watcher trigger | `reckon/scripts/vault_watcher.py --profile vault-sidecar` (P3 deliverable) |

---

## P0 — CLEANUP (Prerequisites)

**WHAT:** Retire Syncthing references; add deprecation notices; verify three-store docs intact.

**WHERE:**
- `.sync/VAULT-SIDECAR-SYNC.md` — prepend deprecation banner
- `HOW-SYNC-WORKS.md` — replace Syncthing section with "Syncthing sidecar superseded — see VAULT-REORG-PLAN.md P3"
- Remove any `docker compose --profile vault-sync` references from operator runbooks

**HOW TO DO:**
1. Edit `.sync/VAULT-SIDECAR-SYNC.md` — add at top: `> ⚠️ SUPERSEDED 2026-06-14. Git-sync replaces Syncthing. This file retained for historical reference only.`
2. Edit `HOW-SYNC-WORKS.md` — in "Three-Store Architecture" section, note Syncthing path deprecated; keep three-store table and env-var table intact
3. `git add -p` → sign commit (operator key)

**VERIFY DONE:**
- `grep -r "syncthing\|Syncthing\|vault-sidecar" . --include="*.md" | grep -v "_archive\|SUPERSEDED\|VAULT-REORG-PLAN"` returns nothing actionable
- `HOW-SYNC-WORKS.md` still contains three-store table and env-var table

---

## P1 — SIGNING (Human COC / Citable Authority)

**WHAT:** `vault_sign.py` — operator signs vault documents with ed25519 key. Signed vault docs become forensic-grade citable artifacts.

**WHERE (reckon repo):**
- Deliverable: `reckon/scripts/vault_sign.py`
- Key storage: `~/.vault/operator.key` (ed25519 private, chmod 600)
- Signature sidecar: `{vault_doc}.sig` next to signed file, or manifest sidecar in `OH-System-Prompts/`
- COC entry: written to `reckon/forensics/coc.jsonl` on each sign operation

**HOW TO DO:**
1. Generate operator ed25519 keypair: `python -c "from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey; k=Ed25519PrivateKey.generate(); ..."`
2. Write `vault_sign.py`:
   - Input: vault doc path
   - Sign: ed25519(doc_bytes) → base64 sig
   - Write `.sig` sidecar
   - Append COC entry: `{ts, file, sha256, sig, signer: "operator"}`
3. Register public key in `reckon/.env` as `VAULT_OPERATOR_PUBKEY`

**VERIFY DONE:**
- `python vault_sign.py OH-System-Prompts/main.md` exits 0, `.sig` file created
- COC entry appears in `reckon/forensics/coc.jsonl`
- `reckon/scripts/vault_verify.py OH-System-Prompts/main.md` returns VALID

---

## P2 — KEY BACKUP (Identity Preservation)

**WHAT:** Encrypt operator private key → B2 WORM backup. Restore path documented. Re-clone identity preserved.

**WHERE:**
- `~/.vault/operator.key` (source)
- B2 bucket: `faerie-vault-keys/` prefix (WORM-locked, deletion-proof)
- `reckon/docs/KEY-RESTORE.md` — restore procedure

**HOW TO DO:**
1. Encrypt: `age -p ~/.vault/operator.key > ~/.vault/operator.key.age` (passphrase in operator password manager)
2. Upload: `b2 file upload faerie-vault-keys operator.key.age operator.key.age`
3. Enable B2 Object Lock on `faerie-vault-keys/` bucket
4. Write `reckon/docs/KEY-RESTORE.md`:
   - Download `.age` from B2
   - `age -d operator.key.age > ~/.vault/operator.key && chmod 600 ~/.vault/operator.key`
   - Re-register `VAULT_OPERATOR_PUBKEY` in `reckon/.env`

**VERIFY DONE:**
- `b2 file info faerie-vault-keys/operator.key.age` shows object-lock retention
- Full restore drill: delete local key → restore from B2 → `vault_verify.py` returns VALID

---

## P3 — LIGHTWEIGHT SYNC (Replace Syncthing Sidecar)

**WHAT:** Replace Syncthing/Docker sidecar with git-synced-dir + thin debounced file watcher. VPS has zero Obsidian/Electron. Near-zero CPU.

**Architecture:**
```
Operator machine:
  Obsidian edits → git commit (signed) → git push

VPS:
  git pull (triggered by watcher or cron) → vault updated
  vault_watcher.py detects change → reconciles relevant files only

VPS → Operator:
  reckon crystallize → writes to vault/ → git commit → operator pulls
```

**WHERE:**
- Watcher: `reckon/scripts/vault_watcher.py`
- Reconcile handlers (in watcher):
  - `OH-System-Prompts/*.md` changed → call `init_oh_settings()`
  - `.agents/agents/*.md` or `.claude/agents/*.md` changed → reload agent cards
  - `Human/*.md` changed → `reckon_corpus annotate --source vault`
- Git pull hook: `reckon/scripts/vault_git_pull.sh` (called by watcher on push event or via cron fallback)

**HOW TO DO:**
1. Write `vault_watcher.py` using `watchdog` (Python):
   - Watch `$RECKON_VAULT_PATH` recursively
   - Debounce: 2s settling window
   - On `OH-System-Prompts/` change → `init_oh_settings()`
   - On `.agents/agents/` or `.claude/agents/` change → reload agent registry
   - On `Human/` change → `reckon_corpus annotate --source vault --file {changed}`
2. Write `vault_git_pull.sh`:
   - `git -C $RECKON_VAULT_PATH pull --ff-only`
   - Verify signature of HEAD commit: `git verify-commit HEAD` (requires operator GPG/SSH key registered)
   - If sig invalid: abort pull, log to COC, alert
3. Register watcher as `--profile vault-sidecar` in reckon docker-compose (optional, up/down at will)
4. Remove Syncthing service definition from `reckon/deploy/vault-sidecar/docker-compose.yml` (or archive it)

**Reconciliation map (canonical):**

| Vault path changed | Action |
|---|---|
| `OH-System-Prompts/*.md` | `init_oh_settings()` |
| `.agents/agents/*.md` | Reload agent registry |
| `.claude/agents/*.md` | Reload agent registry |
| `Human/*.md` | `reckon_corpus annotate --source vault` |
| `Charters/*.md` | Log to COC only (no auto-action) |
| Anything else | Log only |

**VERIFY DONE:**
- Edit `OH-System-Prompts/main.md` on operator machine → push → VPS pulls → `init_oh_settings()` called within 5s
- `ps aux | grep syncthing` returns nothing on VPS
- `docker stats` shows vault-sidecar profile idle when not in use

---

## P4 — SETTINGS-PUSH (Signed Operator Authority)

**WHAT:** Operator edits system-prompt or agent-card in vault → signs → pushes → reckon accepts with valid operator sig. Invalid sig = rejected (no effect).

**WHERE:**
- Gate: `reckon/scripts/vault_settings_gate.py`
- Called by: `vault_watcher.py` reconcile handlers (wraps `init_oh_settings` and agent reload)
- Key: `VAULT_OPERATOR_PUBKEY` in `reckon/.env`

**HOW TO DO:**
1. Wrap each reconcile handler with sig check:
   ```python
   if not vault_verify(changed_file, pubkey=VAULT_OPERATOR_PUBKEY):
       log_coc(event="SETTINGS_PUSH_REJECTED", file=changed_file)
       return  # no effect
   ```
2. On valid sig: proceed with reconcile action + append COC entry with `{sig_verified: true, signer: "operator"}`
3. On invalid sig: COC entry with `{sig_verified: false, reason: "sig_mismatch"}` + alert operator

**VERIFY DONE:**
- Unsigned edit to `OH-System-Prompts/main.md` pushed → reconcile logs `SETTINGS_PUSH_REJECTED`, no settings change
- Signed edit → reconcile logs `SETTINGS_PUSH_ACCEPTED`, `init_oh_settings()` executes

---

## P5 — ASYNC ANNOTATION (Vault → Corpus)

**WHAT:** Vault annotations in `Human/` sync to `reckon_corpus` session/thread. Operator drops annotation in Obsidian → appears in corpus for agent retrieval.

**WHERE:**
- Drop zone: `Human/` (vault folder, monitored by watcher)
- Target: `reckon_corpus annotate --source vault --file {path} --thread {thread_id}`
- Thread ID: parsed from filename convention `{thread_id}_{title}.md` or frontmatter `thread_id:` field

**HOW TO DO:**
1. Confirm `Human/` exists in vault (create if absent)
2. In `vault_watcher.py` `Human/` handler:
   - Parse `thread_id` from filename or frontmatter
   - Call `reckon_corpus annotate --source vault --file {path} --thread {thread_id}`
   - On success: append COC entry `{event: "ANNOTATION_SYNCED", file, thread_id}`
3. Annotation format convention (document in `Human/README.md`):
   - Filename: `{YYYYMMDD}_{thread_id}_{slug}.md`
   - Frontmatter: `thread_id`, `tags`, `author: operator`

**VERIFY DONE:**
- Create `Human/20260614_test-thread_hello.md` → push → `reckon_corpus thread list` shows annotation
- COC entry written for annotation sync event

---

## Vault Key Folders (Reference)

| Folder | Purpose | Watcher action |
|---|---|---|
| `OH-System-Prompts/` | System prompt source | → `init_oh_settings()` on change (P4 gated) |
| `00-SHARED/Hive/` | Agent cards, session artifacts | Log only (agent cards in `.agents/` or `.claude/agents/`) |
| `Human/` | Annotation drop zone | → `reckon_corpus annotate` (P5) |
| `Charters/` | Charter lifecycle docs | Log + COC only |
| `30-Dashboards/` | Dataview over forensics | Read-only; queries live forensics path |
| `.agents/agents/` | Agent card definitions | → Reload agent registry (P4 gated) |
| `.claude/agents/` | Claude Code agent cards | → Reload agent registry (P4 gated) |

---

## Execution Order

```
P0 (cleanup) → P1 (signing) → P2 (key backup) → P3 (watcher) → P4 (gate) → P5 (annotation)
```

P1 must complete before P4 (gate requires signing infrastructure).
P3 must complete before P4 and P5 (watcher is the delivery vehicle).
P0 and P2 are independent; run in parallel if desired.
