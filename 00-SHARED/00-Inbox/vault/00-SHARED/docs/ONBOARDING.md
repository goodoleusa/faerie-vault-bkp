---
type: guide
status: active
created: 2026-04-21
tags: [onboarding, getting-started]
up: README.md
prev: SETUP-CHECKLIST.md
next: ONBOARDING-COLLAB.md
down: [ONBOARDING-COLLAB.md, ONBOARDING-GENERIC.md]
---

> [↑ Readme](README.md) · [← Setup Checklist](SETUP-CHECKLIST.md) · [→ Onboarding Collab](ONBOARDING-COLLAB.md) · [⌂ Home](../README.md)

# ⚠️ DEPRECATED — Onboarding Docs Reorganized

This file has been split into two new documents. **Please use one of these instead:**

| Your situation | Read this |
|---|---|
| **Solo user, fresh machine** | [ONBOARDING-GENERIC.md](ONBOARDING-GENERIC.md) |
| **Joining an investigation (e.g., cybertemplate)** | [ONBOARDING-COLLAB.md](ONBOARDING-COLLAB.md) |

This old file mixed both workflows into one, causing confusion. The new docs are separate and clearer.

---

**ARCHIVED CONTENT BELOW** (kept for reference, but use the new docs above)

---

## Step 0: Clone and configure

```bash
# Clone the repo
git clone git@github.com:Persistech/faerie.git /mnt/d/0LOCAL/gitrepos/faerie2
cd /mnt/d/0LOCAL/gitrepos/faerie2

# Set env vars (add to ~/.bashrc)
export SPRINT_QUEUE_FILE="$HOME/.claude/hooks/state/sprint-queue.json"
export CT_VAULT="/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED"
export PROJECT="cybertemplate"   # or your investigation repo name

# Install Claude CLI (WSL only)
curl -fsSL https://claude.ai/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### Git SSH (WSL + YubiKey)
```bash
# Per-repo — bridges WSL to Windows SSH agent (YubiKey):
git config core.sshCommand "/mnt/c/Windows/System32/OpenSSH/ssh.exe"
```

---

## Step 1: Run investigation setup script

From your investigation repo (e.g. cybertemplate):

```bash
cd /mnt/d/0LOCAL/gitrepos/cybertemplate
python3 scripts/0a_setup_collab.py
```

This script:
- Appends investigation context (HONEY.md + NECTAR.md from `context/`) to your global memory at `~/.claude/HONEY.md` and `~/.claude/memory/NECTAR.md`
- Writes `~/.claude/hooks/state/faerie-brief.json` so `/faerie` has cold-start fuel
- Wires `DAE_SCRIPTS` path into `ct-env.json`
- Takes ~30 seconds, idempotent (safe to re-run)

---

## Step 2: Set up B2 backup (investigation repos)

```bash
python3 scripts/0b_b2_provision.py
```

This prompts for your B2 application key, writes `~/.b2/faerie.env`, and configures rclone for WORM backups. All evidence backups then run automatically.

---

## Step 3: Start working

```bash
cd /mnt/d/0LOCAL/gitrepos/cybertemplate
claude
```

Once in the Claude CLI:
```
/faerie
```

This reads your memory, shows a dashboard, and launches queued HIGH-priority tasks.

---

## Three highest-impact first tasks

1. **Read `docs/UI-DATA-GUIDE.md`** (15 min) — data paths, D3 examples, evidence browser
2. **Claim a task from the queue** — run `/queue` to see what's ready, `/run` to claim one
3. **Check publication blockers** — `launch/PUBLICATION_BLOCKERS.md`

---

## Memory system overview

| File | Path | Purpose |
|------|------|---------|
| HONEY.md | `~/.claude/HONEY.md` | Crystallized prefs, methods, identity — read at every session start |
| NECTAR.md | `~/.claude/memory/NECTAR.md` | Validated findings, append-only forever |
| REVIEW-HOT.md | `~/.claude/memory/REVIEW-HOT.md` | Active flags hotlist (~2K tokens) |
| pollen | `{repo}/.claude/memory/pollen-{SID}.md` | Working notes for this session (gitignored) |

**Always launch from WSL path:**
```bash
cd /mnt/d/0LOCAL/gitrepos/{repo} && claude
```
Never from `D:\...` — this creates a fragmented auto-memory folder.

---

## Key commands

| Command | What it does |
|---------|-------------|
| `/faerie` | Session start — orient, dashboard, launch HIGH tasks |
| `/run` | Claim next queued task, spawn agents |
| `/queue` | View sprint queue |
| `/handoff` | Session end — promote memory, snapshot |
| `/memory` | View/write scratchpad |

Full reference: `docs/COMMAND-GUIDE.md`

---

## Day 1 checklist

- [ ] Clone repo, set env vars in `~/.bashrc`
- [ ] Run `python3 scripts/0a_setup_collab.py`
- [ ] Start http.server: `cd /mnt/d/0LOCAL/gitrepos/cybertemplate && python3 -m http.server 5000`
- [ ] Read `docs/UI-DATA-GUIDE.md`
- [ ] Open Claude CLI: `claude && /faerie`
- [ ] Claim one task from the queue: `/run`

---

*See also: `docs/COMMAND-GUIDE.md`, `ARCHITECTURE.md`, `context/HONEY.md` (investigation seed)*
