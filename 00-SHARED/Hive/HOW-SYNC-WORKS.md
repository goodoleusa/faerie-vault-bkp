---
type: system-doc
tags: [system, sync, how-to]
last_updated: 2026-03-24
deprecates: [FAERIE_VAULT manual sync, DAE_VAULT env var]
parent:
  - "[[00-SHARED/00-SHARED]]"
sibling:
  - "[[00-SHARED/Dashboards/Annotation-Dash]]"
child:
  - "[[00-SHARED/Hive/system-changes/2026-03-22-vault-sync-wiring]]"
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:43a24c5bd10c50b89d504b1f05be92f76b77f3190ac5637d6f40d3c7c4b0d674
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:16:21Z
hash_method: body-sha256-v1
---

# How Vault Sync Works

*Plain English. Read this if you're confused about what's automatic vs manual, or if sync breaks.*

---

## What this vault is for

**Three-layer mental model** (full detail: [[00-META/00-OVERVIEW]] — *Data sovereignty*):

| Layer | Role |
|-------|------|
| **This vault (Obsidian)** | **Conceptual home** — how humans and agents **collaborate**: readable notes, graph, inbox, queue, promoted narrative. |
| **Investigation repo + COC** | **Forensic masters** — original runs, audit outputs, manifests, hashes; managed by your **chain-of-custody** system (e.g. CyberTemplate + `scripts/audit_results/`, `~/.claude/memory/forensics/`). |
| **Managed memory (optional)** | **Hosted processor** — only **slices you approve** may go to a provider; never a substitute for COC originals. |

**Kickstart collaboration:** [[00-META/KICKSTART-COLLAB]] — where to put your first task, briefs, and reviews under `00-SHARED/`, and **folder naming** (no new numeric prefixes except protected / tooling).

**This Obsidian vault is not the forensic evidence archive.** It is:

1. **A readable surface for Claude CLI output** — reports, findings, flags, and summaries land here (mostly under `00-SHARED/`) so you can **review** them like normal notes.
2. **Your investigator dashboard** — case stubs, graph, Dataview boards, scratch thinking: how you think, link, and prioritize. Not every note must participate in COC.
3. **The handoff layer for sync-back** — corrections, promotions, review checkoffs, and priorities are what the next agent run **reads** as steering: **human judgment → back into the pipeline**.

Heavy artifacts, audit matrices, and bundles you would defend under **COC** stay in the **repo** paths above; the vault **summarizes and coordinates**.

**Data sovereignty (short):** You hold **operational custody** in the vault (what the team sees) and **forensic custody** in the **COC repo** (masters). You decide what exits your machines — including **if** a **managed memory** service receives **HONEY-class** or other approved bundles.

**Faerie / file-backed handoff** turns ephemeral chat into **durable, reviewable state** so investigations **compound**; partners using the **same vault + repo conventions** can **swap investigation folders** and share expertise with less re-training. See [[00-META/11-FAERIE-IMPACT-AB]].

---

## The Short Version

Every time a Claude session ends, an automatic script can push new investigation material from Claude’s working memory into this vault. You don’t have to ask — it just happens.

**What gets pushed:** High-priority findings, smoking guns, statistical results, and flagged items from the investigation.

**Where they go:** `00-SHARED/Agent-Outbox/{investigation-id}/{date}-findings.md`

**System changes go to:** `00-SHARED/Hive/system-changes/YYYY-MM-DD-*.md`

---

## What's Automatic (Zero Action Required)

| What | When | Where in vault |
|---|---|---|
| New HIGH findings | Every session end | `00-SHARED/Agent-Outbox/{inv}/{date}-findings.md` |
| System changes (hooks/rules/settings) | When agent writes `cat=SYSTEM_CHANGE` MEM blocks | `00-SHARED/Hive/system-changes/` |
| Delivery hash file | Same run as above | `note.md.sha256` next to each agent-delivered file — **one line**, 64 hex chars = SHA-256 of that file’s bytes on disk |

---

## What's Manual (You Run It)

| What | Command | Why |
|---|---|---|
| Force a sync now (don't wait for session end) | `python3 ~/.claude/scripts/vault_narrative_sync.py` | Pull latest findings into the vault immediately |
| Optional bulk hash audit (not required for daily use) | `python3 ~/.claude/scripts/vault_manifest.py --vault ... --files path/to/file.md` | Extra record under `~/.claude/memory/forensics/` if you want it |

---

## CyberTemplate repo (where hooks and audit outputs live)

Investigation automation, `scripts/audit_results/`, and `.claude` hooks live in the **CyberTemplate** git repo — not inside this Obsidian vault.

| Environment | Typical path |
|---|---|
| Windows | `D:\0LOCAL\gitrepos\cybertemplate` |
| WSL (same machine) | `/mnt/d/0LOCAL/gitrepos/cybertemplate` |

Set `CT_REPO` or `CYBERTEMPLATE_REPO` if your clone lives elsewhere.

---

## Environment Variables

| Var | Value | Purpose |
|---|---|---|
| `CT_VAULT` | e.g. `D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED` or WSL path | Vault root for CyberTemplate investigation |
| `CT_VAULT_SHARED` | `CT_VAULT/00-SHARED` | Agent write zone |
| `CT_REPO` / `CYBERTEMPLATE_REPO` | e.g. `D:\0LOCAL\gitrepos\cybertemplate` | CyberTemplate clone (hooks, audit_results → vault sync) |

**Deprecated (kept as fallback):** `FAERIE_VAULT`, `DAE_VAULT`, `VAULT_ROOT` — all point to same place. Use `CT_VAULT` going forward.

**DAE repo:** Does NOT have a vault env var. DAE is a generic template and doesn't write to this vault.

---

## Agent Write Zone

Agents (Claude) can only write to `00-SHARED/`. This is enforced in `settings.json` permissions.

**Agents cannot write to:** vault root, `00-PROTECTED/`, `10-Investigations/`, `30-Evidence/`, or any other folder.

**Exception:** User can grant temporary expanded permissions for specific tasks (like writing wave narratives).

---

## Investigation Routing

Each push is tagged with an investigation ID (from `investigation-active.json`). Currently: `criticalexposure`.

Output structure:
```
00-SHARED/
  00-Agent-Outbox/
    criticalexposure/
      2026-03-22-findings.md
      2026-03-23-findings.md
    future-investigation/
      ...
  00-Hive/
    system-changes/
      2026-03-22-vault-sync-wiring.md
```

When you add a new investigation, update `investigation-active.json` and findings will route to the new folder automatically.

---

## If Sync Breaks

1. **Check the state file:** `~/.claude/hooks/state/vault-sync-state.json` — shows last synced line numbers
2. **Run manually:** `python3 ~/.claude/scripts/vault_narrative_sync.py`
3. **Check the Stop hook** in `settings.json` — look for `vault_narrative_sync.py` in the Stop hooks array
4. **Reset state** (re-sync from beginning): delete `vault-sync-state.json` — next run will sync all history (may produce large output)

See also: [[00-SHARED/Hive/system-changes/2026-03-22-vault-sync-wiring]] for what changed and why.

---

## Delivery proof — `*.sha256` (simple)

For each agent-delivered file in the vault, the sync scripts write a **sibling hash file**:

- Name: **same as the document + `.sha256`** — e.g. `2026-03-23-findings.md` → `2026-03-23-findings.md.sha256`
- Contents: **one line**, 64 hex characters (SHA-256 of the **exact bytes** of that `.md` on disk right after delivery)

**Check:** Recompute SHA-256 of the note in Obsidian’s folder. If it still matches the line in `*.sha256`, you have the **same starting document** the agent gave you. If you edited the note, the hash will **not** match — that’s your evidence you changed it after delivery.

PowerShell example:

```powershell
Get-FileHash -Algorithm SHA256 ".\path\to\note.md" | Select-Object Hash
Get-Content ".\path\to\note.md.sha256"
```

### Scripts (`~/.claude/scripts/`)

| Script | Role |
|---|---|
| `vault_sync.py` | Copy into `00-SHARED/`; writes `filename.sha256` for each delivered file |
| `vault_narrative_sync.py` | Session-end memory → vault; refreshes `*.sha256` for files it touched |
| `vault_manifest.py` | Optional — bulk forensics under `~/.claude/memory/forensics/` if you run it by hand |

CyberTemplate: `launch/VAULT-OBSIDIAN-COC-SYNC.md` in your clone.
