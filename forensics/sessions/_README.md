---
type: readme
pseudosystem_folder: Forensics/sessions
canonical_repo_path: "forensics/_claude-session-archive/"
tags: [readme, sessions, forensics, pseudosystem]
---

# Sessions — Navigation Notes

> **Canonical session archives live at `forensics/_claude-session-archive/` in the repo.**
> This folder contains prose summary notes for navigating archived sessions.
> Content here is orientation-level — NOT the raw session logs.

---

## What Is a Session Archive?

When a Claude Code session closes, the session archiver (`scripts/2x_session_archiver.py`) copies session artifacts to `forensics/_claude-session-archive/{date}/{session-uuid}/`. These include:
- Session manifest JSON
- Conversation context (if extracted)
- HONEY updates crystallized during the session
- Links to manifests produced during the session

## How to Add a Session Note Here

After a significant session (one that produced charters, manifests, or major HONEY entries), add a brief note:

1. Filename: `{YYYY-MM-DD}-{session-label}.md`
2. Frontmatter: `type: session`, `date`, `session_uuid`, `canonical_repo_path`
3. Body: 3–5 bullet points of what was accomplished, what emerged, what was crystallized

## Purpose

The sessions folder lets the operator navigate the history of working sessions in the vault's graph view — clicking through from a charter note → sessions where that charter was advanced → manifests produced → shapes moved.

## What NEVER Goes Here

- Raw JSONL conversation logs (evidence-class)
- API keys or authentication tokens
- Unhashed session IDs that could be reverse-engineered

---

*Part of the Vault Pseudosystem — see `PSEUDOSYSTEM-README.md` at vault root.*
