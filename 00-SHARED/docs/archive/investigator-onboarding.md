# Investigator Onboarding — Joining Mid-Investigation

Quick-start for new investigators. Five reads, one launch, then you're oriented.

---

## 1. Read HONEY.md first (crystallized system knowledge)

`~/.claude/memory/HONEY.md` — the distilled brain of the system. Covers environment paths,
established methods, investigator preferences, key decisions, and cross-project patterns.
Read it in full on first join. It's kept under 200 lines by design — read it all.

What you'll find: env vars (env00001–env00013), vault root, agent routing rules, active
project status, crystallized lessons from prior sessions.

---

## 2. Read NECTAR.md tail (recent findings)

`~/.claude/memory/NECTAR.md` — forensic append-only truth log. Never edited, only appended.
Read the last 30 lines for recent findings:

    tail -30 ~/.claude/memory/NECTAR.md

What you'll find: confirmed findings, agent outputs promoted from scratch, session handoff
notes, blocker flags, open questions requiring human resolution.

---

## 3. Orient with /faerie

Type `/faerie` at session start. It reads HONEY + NECTAR, scans the HIGH queue, and prints
a live dashboard: active tasks, open blockers, recent decisions, sprint status.

Faerie IS the session orchestrator. Run it first, every session.

---

## 4. How the queue works

Queue lives at `~/.claude/hooks/state/`. Operations via queue_ops.py:

    # See what needs doing
    python3 ~/.claude/hooks/state/queue_ops.py list

    # Claim a task (marks it in-progress, prevents double-pickup)
    python3 ~/.claude/hooks/state/queue_ops.py claim TASK_ID

    # Mark done after completing work
    python3 ~/.claude/hooks/state/queue_ops.py complete TASK_ID

    # Mark failed with reason (creates retry context)
    python3 ~/.claude/hooks/state/queue_ops.py fail TASK_ID --reason "blocked on X"

Tasks have categories (meta, analysis, infra) and priorities (HIGH/MED/LOW). Pick HIGH first.
Claim before starting — unclaimed tasks can be grabbed by parallel agents.

---

## 5. Vault structure

Vault root: `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/`

| Folder            | Who writes  | What goes there               |
|-------------------|-------------|-------------------------------|
| `00-SHARED/`      | Agents      | Outbox drafts, techniques, inbox flags |
| `00-SHARED/Agent-Outbox/` | Agents only | Finding drafts (never final) |
| `30-Evidence/`    | Humans only | Promoted, reviewed findings   |
| `10-Investigations/` | Humans   | Wave narratives               |
| `20-Entities/`    | Humans      | Entity notes                  |
| `60-Chronology/`  | Humans      | Timeline entries              |
| `00-PROTECTED/`   | Nobody      | Absolute dead zone — never touch |

Agents write to `00-SHARED/` only. Humans promote to `30-Evidence/` after review.
Never `rsync --delete`, never `rm -rf` on vault. Additive writes only.

---

## 6. Key commands

| Command        | When to use                                          |
|----------------|------------------------------------------------------|
| `/faerie`      | Session START — orient, dashboard, launch HIGH queue |
| `/run`         | Claim and execute next queued task                   |
| `/handoff`     | Session END — crystallize, queue threads, wind down  |
| `/crystallize` | Mid-session memory round — crystallize scratch, integrate into HONEY |
| `/queue`       | Show sprint task queue status                        |
| `/memory`      | View/write shared memory, review inbox               |

---

## Quick-start sequence

    1. tail -30 ~/.claude/memory/NECTAR.md
    2. /faerie
    3. python3 ~/.claude/hooks/state/queue_ops.py list
    4. /run

Scratch notes go to `{repo}/.claude/memory/scratch-{SESSION_ID}.md`.
HIGH-priority flags also append to `~/.claude/memory/REVIEW-INBOX.md`.

---

## B2 Backup Setup (optional but recommended)

Forensics and memory files auto-upload to Backblaze B2 at session end. Zero effort once configured.

**You need:** A B2 Application Key. Either create your own at [Backblaze Console](https://secure.backblaze.com/app_keys.htm), or ask the project lead for a restricted key (read+write on your prefix only — you never see the master key).

**Setup (2 minutes):**

    python3 scripts/0b_b2_provision.py

The script prompts for your key, tests the connection, creates the bucket if needed,
and writes `~/.b2/faerie.env`. After that, backups happen automatically at every session end.

**Verify at any time:**

    python3 scripts/0b_b2_provision.py --test-only

**Upload manually:**

    python3 ~/.claude/hooks/b2_backup_hook.py --force

**What gets backed up automatically:**
- `{repo}/forensics/` — full forensic COC log (rclone sync, incremental)
- `~/.claude/memory/NECTAR.md` — validated findings
- `~/.claude/HONEY.md` — crystallized system knowledge

**Getting a restricted key from the project lead:**

The project lead runs:

    python3 scripts/b2_provision_user.py provision --user-slug <yourname>

This creates a WORM bucket + three scoped keys (write/read/detonate). The write key
is placed in `~/.b2/ct-<yourname>-forensics.env` and shared with you. You use that
key ID + key when prompted by `0b_b2_provision.py`.
