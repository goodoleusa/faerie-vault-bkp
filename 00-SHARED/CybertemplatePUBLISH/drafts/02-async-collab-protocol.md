---
date: 2026-05-22
author: goodoleusa
related_mission: cybertemplate-publish
status: draft
imported_from: CyberOps-UNIFIED/ASYNC-COLLAB.md
original_doc_hash: sha256:3b79aaeac84f0fde0a1cfbbcaf9db0b64457747e884d4db851495e4aa4e61e7b
original_created: 2026-03-15
---

# Async Collaboration Protocol — CyberOps Vault

hi mom

**For humans (Obsidian):** Leave drops, post tasks, read agent discoveries.
**For Claude agents:** Read drops and task files, claim work, write discoveries back.
**Transport:** Syncthing — airgapped OK, eventually consistent, no real-time required.

---

## The Dead-Drop Model

Sessions and humans communicate like spies: **no real-time channel**, only shared files.
Everyone writes to the vault; everyone reads from it when they next connect.

```
Your machine (WSL/Claude)          Vault (Syncthing)          Collaborator / ZimaBoard
──────────────────────             ──────────────────          ───────────────────────
drops.py write DISCOVERY    →→→    00-Inbox/drops/*.md   →→→  Obsidian inbox / OpenClaw
queue_ops.py add TASK       →→→    00-Inbox/tasks/*.md   →→→  Agent picks up and claims
Agent writes scratch MD     →→→    03-Agents/sessions/   →→→  Human reads in Obsidian
```

---

## Directory Map

| Path | Purpose | Who writes | Who reads |
|---|---|---|---|
| `00-Inbox/drops/` | Dead-drop messages (typed, structured) | Agents + humans | Presend hook + humans |
| `00-Inbox/tasks/` | Claimable task files (atomic rename to claim) | Agents + humans | Agents at session start |
| `00-Inbox/AGENT-REVIEW-INBOX.md` | Human review queue for agent findings | Agents | Human + agents |
| `03-Agents/sessions/` | Per-session state files written during work | Agents | Faerie, humans |
| `03-Agents/skills/` | Agent skill reference docs | Maintained centrally | All agents |
| `03-Agents/active_agents.json` | Live registry of active sessions | Presend hook | Faerie, humans |
| `01-Memories/KNOWLEDGE-BASE.md` | Validated facts shared across all sessions | Agents (membot) | All agents |

---

## Quick Start

### As a human — post a task for any agent:
1. Create a note from `Blueprints/Task-Claim.blueprint`
2. Fill in goal, priority, context
3. Save to `00-Inbox/tasks/task-YYYYMMDD-NNN.md`
4. Syncthing delivers it; agent claims it on next `/new`

### As a human — leave a discovery drop for agents:
1. Create a note from `Blueprints/Dead-Drop.blueprint`
2. Type your message, set type (DISCOVERY/ALERT/HANDOFF/REQUEST)
3. Save to `00-Inbox/drops/`
4. Agent presend hook reads it on next turn: `DROP [DISCOVERY]: ...`

### As a Claude agent:
```bash
# Read all pending drops for your session
python3 ~/.claude/hooks/state/drops.py read

# Leave a discovery for other sessions / humans
python3 ~/.claude/hooks/state/drops.py write --to all --type DISCOVERY \
  --payload "foreign .gov cert on port 22 at 45.83.x.x — needs attribution"

# Claim a task from vault inbox
python3 ~/.claude/hooks/state/queue_ops.py claim --session $CLAUDE_SESSION_ID

# Write session state (visible to collaborators in Obsidian)
# → 03-Agents/sessions/session-$SESSION_ID.md
```

---

## Message Types

| Type | Color | Meaning |
|---|---|---|
| DISCOVERY | blue | Found something — another node should know |
| ALERT | red | Warning — don't do X, watch out for Y |
| CLAIM | yellow | I'm taking this task/file — leave it alone |
| HANDOFF | green | Completed work ready for pickup |
| REQUEST | purple | Asking another node to check or do something |
| STATUS | white | Periodic heartbeat — turn N, progress, ctx% |
| BROADCAST | (all) | To all nodes |

---

## Airgapped / Offline Operation

Syncthing works over LAN (ZimaBoard), WireGuard VPN, or USB sneakernet.
Drop files accumulate while offline; sync on reconnect.
Task claims use atomic file operations — no conflicts even if both nodes write simultaneously.
Claude agents check for drops every turn via presend hook — ~50ms, zero tokens.

---

## Files

- `Blueprints/Dead-Drop.blueprint` — template for leaving typed messages
- `Blueprints/Task-Claim.blueprint` — template for posting tasks
- `Blueprints/Session-Handoff.blueprint` — standardized session summary
- `Blueprints/Context-Bundle.blueprint` — faerie's context package for agents
- `03-Agents/skills/faerie.md` — context roundup + session prep skill
- `03-Agents/skills/collab-protocol.md` — this protocol as agent reference
- `03-Agents/skills/queue-ops.md` — queue claiming and task management
