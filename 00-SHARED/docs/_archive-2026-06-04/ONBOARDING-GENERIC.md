---
type: guide
status: active
created: 2026-04-21
tags: [onboarding, getting-started]
up: ONBOARDING.md
prev: ONBOARDING-COLLAB.md
---

> [↑ Onboarding](ONBOARDING.md) · [← Onboarding Collab](ONBOARDING-COLLAB.md) · [⌂ Home](../README.md)

# Onboarding — Using Faerie

A step-by-step guide to setting up faerie for the first time.

---

## Prerequisites

- Claude CLI v2.1.70+ (`claude --version`)
- Python 3.10+ (`python3 --version`)
- Git (`git --version`)
- WSL2 on Windows (Claude CLI runs only in WSL; use `/mnt/d/` paths)

---

## Step 1: Install Faerie

See [INSTALL.md](../INSTALL.md) or [QUICKSTART.md](../QUICKSTART.md) for installation instructions.

If you've already completed the install, you should have:
- `~/.claude/agents/`, `~/.claude/hooks/`, `~/.claude/skills/` populated
- `~/.claude/settings.json` configured with hook paths
- `CT_VAULT` pointing to your Obsidian vault

---

## Step 2: Understand the Memory System

Faerie's memory works in three tiers:

| File | Path | Purpose | Lifecycle |
|------|------|---------|-----------|
| **Pollen** | `{repo}/.claude/memory/pollen-{sessionID}.md` | Session scratch notes | Per-session, gitignored |
| **NECTAR** | `~/.claude/memory/NECTAR.md` | Validated findings | Append-only forever |
| **HONEY** | `~/.claude/HONEY.md` | Crystallized wisdom | Loaded at every session start |

**The pipeline:** During a faerie cycle, you write observations to pollen. At `/handoff` (session end), memory-keeper promotes high-confidence findings to NECTAR. When patterns repeat across 3+ sessions, the `/crystallize` skill distills them into HONEY.

**Why this matters:** Each session, Claude's context starts at zero. HONEY.md loads automatically (≤200 lines), carrying crystallized knowledge forward. This is what lets faerie sessions compound — you're not starting from scratch every time.

---

## Step 3: Launch Your First Session

```bash
cd /path/to/any/repo
claude
```

This starts the Claude CLI. Now type:

```
/faerie
```

What you'll see:
- **Dashboard:** Current context, queued tasks, agent state
- **HONEY summary:** Crystallized wisdom from prior sessions
- **Wave status:** W1 (triage) and W2 (research) agents launching

---

## Step 4: Essential Commands

| Command | When to use | What happens |
|---------|------------|--------------|
| `/faerie` | At session start (or after `/handoff`) | Orient + launch HIGH-priority agent teams |
| `/run` | Anytime | Claim next task from queue, watch agents work |
| `/queue` | To see what's queued | Show tasks: blockers → critical → breadth |
| `/handoff` | At session end (before exiting) | Promote findings, snapshot, prepare for next session |
| `/crystallize` | When NECTAR feels dense | Distill patterns → HONEY (manual, human-triggered) |
| `/memory` | To view/edit scratchpad | Read/write session notes |

Full reference: [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

---

## Step 5: First Task

After `/faerie` shows the dashboard:

```
/queue
```

This lists queued work. Pick the first HIGH-priority task:

```
/run
```

Now watch agents work. They'll:
1. Read task requirements
2. Complete the work (usually 2-5 minutes)
3. Write findings to a manifest file
4. Return to idle, waiting for the next task

You can run multiple `/run` cycles in a session.

---

## Step 6: End-of-Session Handoff

Before you exit the Claude CLI:

```
/handoff
```

This:
1. Promotes high-confidence observations to NECTAR.md
2. Bundles context for cold-start next time
3. Syncs vault with your knowledge base
4. Logs session metadata

After `/handoff` completes, you can safely exit. Next session, when you run `/faerie`, you'll pick up where you left off.

---

## WSL Path Convention (Critical)

Always launch from a WSL path:

```bash
✓ cd /mnt/d/0LOCAL/gitrepos/myrepo && claude
✗ cd D:\gitrepos\myrepo && cmd.exe && claude   # WRONG
```

Reason: Claude's auto-memory system detects project folders by path. Dual-path access creates fragmented memory folders. Use WSL paths exclusively.

---

## Day 1 Checklist

- [ ] Complete install (or [QUICKSTART.md](../QUICKSTART.md))
- [ ] Check that `~/.claude/` has agents/, hooks/, skills/ subdirectories
- [ ] Verify `CT_VAULT` env var is set: `echo $CT_VAULT`
- [ ] Open Claude CLI: `claude && /faerie`
- [ ] Read the HONEY summary (crystallized wisdom from prior sessions)
- [ ] Run `/queue` to see available tasks
- [ ] Run `/run` to claim and start a task
- [ ] After 5 minutes, run `/handoff` to end the session

Done. Next time you `claude`, you'll start from context that carries forward.

---

## Troubleshooting

**Q: `/faerie` shows no dashboard**
- A: Hooks may not be wired. Check `~/.claude/settings.json` — hooks block should reference your actual paths. See [INSTALL.md Step 3](../INSTALL.md).

**Q: `CT_VAULT` not found**
- A: Export it in `~/.bashrc`: `export CT_VAULT="/path/to/vault"`

**Q: Agents are very slow**
- A: Depends on queue size and model (W1=Haiku 45s, W2=Sonnet 3min, W3=Sonnet 10min background). Check `/queue` to see how many tasks are ahead.

**Q: I see "WSL path required" error**
- A: You're launching from a Windows path. Switch to WSL: `cd /mnt/d/...` instead of `D:\...`

For more help, see [ARCHITECTURE.md](../ARCHITECTURE.md) or post an issue on GitHub.

---

*Next: Read [ARCHITECTURE.md](../ARCHITECTURE.md) to understand the design. Or jump to [COMMAND-GUIDE.md](COMMAND-GUIDE.md) for a full command reference.*
