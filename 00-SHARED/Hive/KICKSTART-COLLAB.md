---
type: meta
tags: [meta, onboarding, collaboration, agents]
updated: 2026-03-24
parent: []
child: []
sibling: []
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:2937f013a784c7617acc33a5e011c39600bf0798fd1ed1d8da7f1b6443ac4e2b
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:16:21Z
hash_method: body-sha256-v1
---

# Kickstart collaboration — where to put things

Use this page when you open the vault and want **humans + agents** to start working **without** hunting through older architecture trees.

---

## Folder naming (current policy)

**We are not requiring numeric prefixes on new folders you create** (e.g. you may add `Cases/`, `Partner-A/`, or `Field-Notes/` at vault root).

- **Keep numbers where they signal private / protected / tooling-enforced zones**, e.g. **`01-PROTECTED/`** (human-only, sensitive) and **`00-SHARED/`** (the **agent write zone** — Cursor/Claude hooks and `CT_VAULT_SHARED` point here; don’t rename without updating tooling). **Inside `00-SHARED/`**, collaboration folders use **plain names** (`Inbox/`, `Agent-Outbox/`, `Hive/`, `Memories/`, …) — no extra `00-` prefixes on those subdirs.
- **Legacy numbered roots** in this template (`10-Investigations/`, `20-Entities/`, …) stay as-is for compatibility; you can **add** new areas **without** `NN-` if you prefer.
- Meta docs under **`00-META/`** keep their filenames (`01-ARCHITECTURE.md`, …) for sort order — that is **doc naming**, not a rule that *your* investigation folders must be numbered.

---

## Agent-safe zone: everything under `00-SHARED/`

In **CyberOps-UNIFIED**, the collaboration **inboxes and outboxes** live under **`00-SHARED/`** (not at vault root). Subfolders are **plain names** (no `00-` prefix): `Inbox/`, `Human-Inbox/`, etc. Agents are typically allowed to write only here (see vault permissions / `VAULT-RULES.md`).

| You want to… | Put it here |
|--------------|-------------|
| **Kick off work** — new task for an agent or runner | `00-SHARED/Inbox/` **or** `00-SHARED/Agent-Inbox/` (use whichever your **poll script / queue** is configured to watch; if unsure, start with **`00-SHARED/Inbox/`**) |
| **Tell agents what to do next** — brief, constraints, priorities | `00-SHARED/Human-Outbox/` (new `.md` note) |
| **See what agents need from you** — HIGH flags, review queue | `00-SHARED/Human-Inbox/flags/REVIEW-INBOX.md` and other notes under `00-SHARED/Human-Inbox/` |
| **Read agent deliveries** — findings, reports | `00-SHARED/Agent-Outbox/` (often `…/{investigation-id}/{date}-findings.md` after sync) |
| **Drop informal links / ideas** — no strict format | `00-SHARED/Hive/` |
| **Shared handoff context** — so the next run picks up thread | `00-SHARED/Memories/shared/` (e.g. research logs; optional **`Agent:`** / **`Handoff:`** two-line blocks per [[04-QUICKADD-GLOBAL-VARS-HANDOFF]]) |
| **Your corrections / preferences** (human-only namespace) | `00-SHARED/Memories/human/` — agents read; they should not overwrite your voice |
| **Agent scratch learnings** | `00-SHARED/Memories/agents/` (and task files) per your rules |

**Protected / private:** anything under **`01-PROTECTED/`** is **not** the default agent drop zone — treat as **yours** unless you explicitly open it. Promote into it only on purpose.

---

## Minimal “first hour” checklist

1. **Create one task file** in `00-SHARED/Inbox/` with goal, done-when, and links to any case notes under `10-Investigations/` (or your own case folder).
2. **Optional:** Add a one-screen brief in `00-SHARED/Human-Outbox/` (“constraints, OPSEC, what not to do”).
3. **Open** `00-SHARED/Human-Inbox/flags/REVIEW-INBOX.md` after a run to clear or triage HIGH items.
4. **Read** [[00-SHARED/HOW-SYNC-WORKS]] if you use CyberTemplate sync (what auto-lands vs what you run by hand).

---

## Related

- [[00-CLAUDE DEV/GLOBAL/SKILLS-MIRROR-FOR-COLLAB]] — **Claude skills in the vault** (`00-CLAUDE DEV/GLOBAL/skills/`) are **mirrors for researchers**; runtime canonical is **`~/.claude/skills/`** on the workstation.
- [[12-ASYNC-HUMAN-AGENT-BRIDGE]] — **one note, two audiences:** frontmatter agents parse, body humans read; where to append async human responses.
- [[VAULT-RULES]] — hard rules for agents (zones, protected tree).
- [[01-ARCHITECTURE]] — full topology (note unified vs legacy path callouts).
- [[00-OVERVIEW]] — principles and sovereignty.
- [[00-SHARED/00-SHARED]] — short description of the shared zone.
