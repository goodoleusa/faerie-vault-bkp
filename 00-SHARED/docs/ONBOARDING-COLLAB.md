---
type: guide
status: active
created: 2026-04-21
tags: [onboarding, collaboration, getting-started]
up: ONBOARDING.md
next: ONBOARDING-GENERIC.md
---

> [↑ Onboarding](ONBOARDING.md) · [→ Onboarding Generic](ONBOARDING-GENERIC.md) · [⌂ Home](../README.md)

# Onboarding — Investigation Collaborator

Step-by-step setup for team members joining an active investigation.

This guide assumes you're joining a project like `cybertemplate` that uses faerie for evidence management and collaborative analysis. If you're just using faerie solo, see [ONBOARDING-GENERIC.md](ONBOARDING-GENERIC.md) instead.

---

## Prerequisites

- Claude CLI v2.1.70+ (`claude --version`)
- Python 3.10+ (`python3 --version`)
- Git (`git --version`)
- WSL2 on Windows (Claude CLI runs only in WSL; use `/mnt/d/` paths)
- Access to the investigation repo (e.g., `cybertemplate`)
- Backblaze B2 account (for evidence backups) — optional but recommended

---

## Step 0: Clone and Configure Environment

```bash
# Clone the investigation repo (example: cybertemplate)
git clone git@github.com:Persistech/cybertemplate.git /mnt/d/0LOCAL/gitrepos/cybertemplate
cd /mnt/d/0LOCAL/gitrepos/cybertemplate

# Set environment variables (add to ~/.bashrc)
export SPRINT_QUEUE_FILE="$HOME/.claude/hooks/state/sprint-queue.json"
export CT_VAULT="/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED"
export PROJECT="cybertemplate"   # or your investigation repo name
export PATH="$HOME/.local/bin:$PATH"
```

### WSL SSH Configuration (for YubiKey / Hardware Keys)

If you're using a hardware security key (YubiKey) on Windows, bridge SSH from WSL to the Windows SSH agent:

```bash
# Per-repo configuration
git config core.sshCommand "/mnt/c/Windows/System32/OpenSSH/ssh.exe"
```

This allows WSL git commands to use your Windows-side SSH agent (YubiKey, etc.).

---

## Step 1: Install Faerie

If you haven't already, install faerie:

```bash
cd /mnt/d/0LOCAL/gitrepos/faerie2
bash scripts/install.sh
```

See [INSTALL.md](../INSTALL.md) or [QUICKSTART.md](../QUICKSTART.md) for details.

---

## Step 2: Load Investigation Context

From your investigation repo (e.g., cybertemplate):

```bash
cd /mnt/d/0LOCAL/gitrepos/cybertemplate
python3 scripts/0a_setup_collab.py
```

This script:
- Merges investigation HONEY.md + NECTAR.md into your global `~/.claude/HONEY.md` and `~/.claude/memory/NECTAR.md`
- Writes `~/.claude/hooks/state/faerie-brief.json` (cold-start context for `/faerie`)
- Configures `DAE_SCRIPTS` paths for evidence analysis
- Takes ~30 seconds, safe to re-run

---

## Step 3: Set Up B2 Backup (Recommended)

To enable automatic evidence backups to Backblaze B2:

```bash
cd /mnt/d/0LOCAL/gitrepos/cybertemplate
python3 scripts/0b_b2_provision.py
```

This prompts for your B2 application key and writes `~/.b2/faerie.env`. All evidence backups then run automatically at the cadence defined in your repo's `ARCHITECTURE.md`.

**Not ready to set up B2?** Skip this step. You can run it later — it's idempotent.

---

## Step 4: Start Your First Investigation Session

```bash
cd /mnt/d/0LOCAL/gitrepos/cybertemplate
claude
```

Once in the Claude CLI:

```
/faerie
```

This reads your investigation context and shows:
- **Dashboard:** Current tasks, agent state, queued work
- **HONEY + NECTAR:** Prior findings and crystallized insights
- **Wave launchers:** W1 (triage), W2 (research) agents beginning

---

## Step 5: Essential Investigation Commands

| Command | When to use | What happens |
|---------|------------|--------------|
| `/faerie` | At session start | Orient + launch agent teams on HIGH-priority evidence work |
| `/run` | Anytime | Claim next task from queue (analysis, evidence review, findings synthesis) |
| `/queue` | To see what's queued | Show tasks: evidence gaps → critical analyses → breadth |
| `/handoff` | At session end | Promote findings, sync vault, snapshot investigation state |
| `/stat` | For statistical analysis | Run hypothesis tests, cross-correlation analysis |
| `/memory` | To view/edit scratchpad | Read/write session notes |

Full reference: [COMMAND-GUIDE.md](COMMAND-GUIDE.md)

---

## Step 6: Understand the Investigation Memory System

This extends the generic faerie memory system with investigation-specific context:

| File | Path | Purpose |
|------|------|---------|
| Investigation HONEY | `~/.claude/HONEY.md` | Merged: global faerie prefs + investigation facts (loaded at every session start) |
| Investigation findings | `~/.claude/memory/NECTAR.md` | Validated findings across all sessions (append-only) |
| Session scratch | `{investigation}/.claude/memory/pollen-{SID}.md` | Working notes for this session (gitignored) |
| Vault | `$CT_VAULT/` | Obsidian vault with evidence, findings, agent outputs |
| Backup | `~/.b2/` | B2 WORM backup of all investigation artifacts (immutable) |

---

## Step 7: First Task — Investigation Workflow

After `/faerie` shows the dashboard:

```
/queue
```

This lists evidence gaps, critical analyses, and synthesis work. Pick the first HIGH-priority task:

```
/run
```

This spawns an agent (or agent team) to work on:
- **Evidence review** — analyze logs, artifacts, timelines
- **Findings synthesis** — cross-correlate sources, resolve contradictions
- **GAP analysis** — identify missing evidence, recommend next steps

Watch agents work. They'll write findings to the vault (`$CT_VAULT/00-SHARED/ONBOARDING/`). When done, they return findings for you to review.

---

## Step 8: End-of-Session Handoff

Before exiting the Claude CLI:

```
/handoff
```

This:
1. Promotes high-confidence findings to NECTAR.md
2. Syncs vault with your knowledge base
3. Updates the sprint queue for next session
4. Logs session metadata

After `/handoff`, you can exit. Next session, your findings will be remembered.

---

## Day 1 Checklist

- [ ] Clone investigation repo, set env vars in `~/.bashrc`
- [ ] Install faerie (or verify `~/.claude/agents/`, `~/.claude/hooks/` exist)
- [ ] Run `python3 scripts/0a_setup_collab.py`
- [ ] (Optional) Run `python3 scripts/0b_b2_provision.py` for B2 backup
- [ ] Start Claude CLI: `cd /mnt/d/0LOCAL/gitrepos/cybertemplate && claude && /faerie`
- [ ] Read the HONEY + NECTAR summary (investigation context)
- [ ] Run `/queue` to see available evidence work
- [ ] Run `/run` to claim and start an analysis task
- [ ] After 10-20 min, run `/handoff` to end the session
- [ ] Review findings in vault (`$CT_VAULT/00-SHARED/ONBOARDING/`) — promote key findings to `30-Evidence/` if evidentiary

Done. Next time you `claude`, you'll start from investigation context that carries forward.

---

## Investigation-Specific Topics

**Read these to understand the investigation:**
- `docs/UI-DATA-GUIDE.md` — data paths, evidence browser, D3 examples
- `context/HONEY.md` — investigation seed (key entities, hypotheses, prior work)
- `ARCHITECTURE.md` — phases, milestones, evaluation criteria
- `launch/PUBLICATION_BLOCKERS.md` — what needs to be resolved before publication

**For vault navigation:**
- `$CT_VAULT/INDEX.md` — vault structure and navigation
- `$CT_VAULT/30-Evidence/` — finalized findings (human-curated)
- `$CT_VAULT/00-SHARED/ONBOARDING/{date}/` — agent-generated findings (this session's work)

---

## Troubleshooting

**Q: `/faerie` shows no investigation context**
- A: Check that `python3 scripts/0a_setup_collab.py` completed successfully. If it failed, see the error message and re-run it.

**Q: B2 backup failing to start**
- A: Run `python3 scripts/0b_b2_provision.py` again to re-configure credentials. Check that your B2 account is active.

**Q: Vault sync is slow**
- A: Vault is eventually consistent (Syncthing-based). Wait a few minutes or check Syncthing logs at `$CT_VAULT/.sync/`.

**Q: Agents keep asking for evidence I think already exists**
- A: File may not be in `$CT_VAULT/30-Evidence/` (agent-curated zone). Check `00-SHARED/ONBOARDING/` or the raw `/Artifacts/` folder. If it's not in vault, file a GitHub issue or add it to the vault manually.

For more help, see [ARCHITECTURE.md](../ARCHITECTURE.md), [COMMAND-GUIDE.md](COMMAND-GUIDE.md), or post an issue.

---

*Next: Read [docs/UI-DATA-GUIDE.md](UI-DATA-GUIDE.md) for evidence browser + data analysis workflows. Or dive into [ARCHITECTURE.md](../ARCHITECTURE.md) to understand investigation phases.*
