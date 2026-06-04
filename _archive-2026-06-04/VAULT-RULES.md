---
type: policy
status: active
created: 2026-03-22
updated: 2026-03-24
tags:
  - vault-safety
  - policy
  - coc
doc_hash: sha256:21c121102c1b5336f4c277b244324e8aec5455a5f6e05e68f59ce738e8eab2cb
hash_ts: 2026-03-29T16:10:54Z
hash_method: body-sha256-v1
---

# VAULT-RULES — Read This First (Agents + Humans)

**Any agent or automation touching this vault MUST read this file before writing anything.**

---

## Folder numbering (current policy)

**Do not require `NN-` numeric prefixes on new folders the human creates** for investigations or partners. Use plain names (`Cases/`, `Fieldwork/`) if you like.

**Exceptions (keep obvious in listings & permissions):**

- **`01-PROTECTED/`** — private / sensitive / human-gated; treat as **protected**.
- **`00-SHARED/`** — **agent write zone**; hooks and `CT_VAULT_SHARED` assume this path — **do not rename** without updating tooling.

Legacy template roots (`10-Investigations/`, `20-Entities/`, …) may stay numbered for this repo; they are **not** a mandate for your additions.

---

## Communication Model (CyberOps-UNIFIED)

Paths below are under **`00-SHARED/`** in this vault layout.

```
FOLDER                           DIRECTION           WHO WRITES      WHO READS
──────────────────────────────────────────────────────────────────────────────────
00-SHARED/Agent-Inbox/        humans → agents     Humans          Agents poll/claim
00-SHARED/Agent-Outbox/       agents → humans     Agents          Humans review
00-SHARED/Human-Inbox/       agents → humans     Agents (flags)  Humans (REVIEW-INBOX)
00-SHARED/Human-Outbox/      humans → agents     Humans          Agents read (instructions)
00-SHARED/Inbox/             humans → agents     Humans + agents Task drop (match runner config)
00-SHARED/Hive/              anyone → anyone     Anyone          Anyone (casual, informal)
──────────────────────────────────────────────────────────────────────────────────
01-PROTECTED/                    PRIVATE             Humans          Anyone read (no agent writes)
──────────────────────────────────────────────────────────────────────────────────
00-SHARED/Memories/human/    human memories      Humans only     Agents read
```

**Hive** (`00-SHARED/Hive/`) = beehive / hangout. Drop anything interesting — links, ideas, weird finds, questions. No format, no rules, nothing deleted.

**Kickstart (where to put tasks first):** [[00-SHARED/00-META/KICKSTART-COLLAB]]

**Async bridge (same note for agents + humans):** [[00-SHARED/00-META/12-ASYNC-HUMAN-AGENT-BRIDGE]] — YAML for machines, markdown sections for human read/reply, optional `vault_path` / `source` / `sha256` for traceability.

---

## Hard Rules for Agents

1. **NEVER write to `01-PROTECTED/`** unless the human has explicitly expanded permissions for a scoped task — default is **human-only**.
2. **NEVER write to `00-SHARED/Memories/human/`** — human-only memory space.
3. **NEVER wholesale replace index files** (VAULT-INDEX.md, KNOWLEDGE-BASE.md, etc.) — read the current version first, then MERGE/INSERT your section. Check if the file is newer than your launch time.
4. **NEVER overwrite `*-FULL-*.md` or `*-BACKUP-*.md`** — these are verbatim locked snapshots.
5. **When in doubt:** write to `00-SHARED/Agent-Outbox/` and let the human decide where it belongs.

---

## Promoting Content to Protected

1. Agent writes draft to `00-SHARED/Agent-Outbox/`
2. Agent flags it in `00-SHARED/Human-Inbox/` (or tells human directly)
3. Human reviews and approves
4. Human copies to `01-PROTECTED/` and sets immutability (e.g. `chmod 444` on Unix) if that is your policy — immutable from that point forward

---

## Settings.json Permissions Pattern

For any agent/session working with this vault, **narrow Write** to the shared zone; **Read** may be broader:

```json
"allow": [
  "Read(/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/**)",
  "Write(/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/**)"
]
```

Tighten further if you use subpaths only (e.g. `00-SHARED/Agent-Outbox/**`). Adjust drive/path for Windows vs WSL.

**Reconstruction agents** need a temporary `Write(/vault/**)` override — not a permanent permission. Remove it after the reconstruction run.

---

## Multi-User / Shared Vault Pattern

If this vault is shared via Syncthing or IPFS between multiple people:

- Each person's **`01-PROTECTED/`** is their own — only they promote content there
- **`00-SHARED/Agent-Inbox/`** and **`00-SHARED/Agent-Outbox/`** are shared (any node's agents write there per rules)
- **`00-SHARED/Hive/`** is fully shared — everyone's casual drops land here
- Investigation findings surface through **`00-SHARED/Human-Inbox/`** → human review → promotion
- Agents from any node must not corrupt another person's protected content

---

## Why This Exists (Incident 2026-03-22)

A background vault reconstruction agent completed while the main session was updating VAULT-INDEX.md. The agent's wholesale replacement of the index file lost additions made during the intervening time — including a pointer to the ON-RESISTANCE document (5,828 chars, SHA256: befe6cdf...). Recovery required checking 4 backup locations.

**Root cause:** background agents cannot know what the main session has done since they launched. Time-separated writes to the same file will always conflict.

**Solution:** agents write to dedicated zones, humans gate what reaches the protected archive. Index files are always merged, never replaced.
