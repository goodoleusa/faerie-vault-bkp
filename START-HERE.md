---
type: onboarding
status: active
created: 2026-04-27
tags: [start-here, vault-orientation, onboarding, new-users]
---

# faerie-vault: START HERE

Welcome! This vault is the **human interface** to faerie2 orchestration. Before you start investigating, read this (takes ~10 minutes).

---

## What Is This Vault?

**faerie-vault** is an Obsidian vault that **connects to faerie2 orchestration** via live Dataview dashboards.

### What It Does
- **Live dashboards** auto-update as agents run (Dataview queries)
- **Evidence organization** — folder structure for findings (30-Evidence/, 40-Intelligence/, etc.)
- **Async reading** — browse findings while agents work (no polling, no main context burden)
- **Crystallized memory** — HONEY.md and Droplets preserve insights across sessions

### What It Doesn't Do
- **Does NOT** run agents. That's faerie2's job (Claude backend)
- **Does NOT** require you to understand code. Everything is point-and-click or Markdown
- **Does NOT** enforce any workflow. Structure is optional; note-taking is free-form

---

## Folder Structure (Quick Tour)

### 00-SHARED/ (Collaboration)
**For team investigations.** Contains:
- `ONBOARDING/` — Team context + shared investigation rules
- `Droplets/` — Preserved insights from prior sessions (read-only)
- `Coordination/` — Meeting notes, decisions, blockers

**When to use:** Collaborative investigations. Solo? Skip this folder.

---

### 01-Memories/ (Session Output)
**Where faerie2 writes your findings.** Contains:
- `HONEY.md` — Crystallized memory from `/handoff` (read at session start)
- `pollen-{session_id}.md` — Raw observations from last session
- `Training-Insights/` — Agent learnings + reputation trends

**When to read:** Every session start. HONEY.md loads automatically in Claude context.

---

### 02-Skills/ (Command Reference)
**Cheat sheet for faerie2 skills.** Contains:
- `/faerie` — Dashboard + orchestration status
- `/run` — Mission-aware agent spawning
- `/data-ingest` — Multi-agent ingest pipeline
- `/handoff` — Session wrap-up (crystallize findings)
- `[...other skills]` — Documented in individual files

**When to use:** When you forget a skill's syntax. Copy-paste command from here.

---

### 03-Agents/ (Agent Cards)
**Agent profiles + reputation tracking.** Contains:
- `Agent-Reputation.md` — Live dashboard of all agents (Dataview)
- `Agent-[name].md` — Individual agent training log, issues, strengths
- `training-events/` — Timestamped training records

**When to check:** When an agent fails, check their card to see recent issues.

---

### 10-Investigations/ (Case Work)
**Your investigation cases.** Contains:
- One subfolder per case (e.g., `treasury-ip-origins/`)
- Within each: tasks, progress, blockers

**When to use:** Active investigations. Each case gets a dated subfolder.

---

### 30-Evidence/ (Findings Dashboard)
**MOST IMPORTANT FOLDER.** Contains:
- `Agent-Output-Dashboard.md` — Live table of all agent findings (Dataview)
- `Dashboards/` — Organized queries by investigation
- `Tier-1-Raw.md` — Unverified, raw findings
- `Tier-2-Verified.md` — Cross-checked findings
- `Tier-3-Conclusions.md` — Synthesized insights
- `Tier-4-Court-Ready.md` — Court-admissible proofs

**When to use:** Every session. Start here to see what's already known.

---

### 40-Intelligence/ (Analysis)
**Hand-curated analysis.** Contains:
- Attack trees, actor profiles, infrastructure maps
- Analyst notes (you and team)
- Competitor/threat intelligence

**When to use:** Building narrative or synthesizing complex evidence.

---

### 50-Financial/ (Financial Findings)
**Financial data, when relevant.** Contains:
- Transaction flows, account analysis, payment chains
- Analyst notes on money trails

**When to use:** If investigation involves financial traces.

---

### 60-Chronology/ (Timeline)
**Temporal organization.** Contains:
- Timeline.md — Dataview query showing events chronologically
- Dated logs of key events

**When to use:** Understanding sequence of events or causality.

---

### 70-Sources/ (Citations)
**Source tracking for court admissibility.** Contains:
- URLs, document hashes, access logs
- Collector metadata (who found it, when, how)

**When to use:** Before submitting findings to court or external parties.

---

### 99-Archives/ (Completed)
**Finished cases + historical work.**

**When to use:** When closing a case, move to 99-Archives/.

---

## Pre-Session Checklist (Before Starting Investigation)

- [ ] faerie2 is cloned (at `/mnt/d/0local/gitrepos/faerie2` or your `$FAERIE_REPO`)
- [ ] This vault is open in Obsidian
- [ ] Obsidian shows "Dataview plugin enabled" (Settings → Community plugins)
- [ ] Read [DUAL-REPO-SETUP.md](../faerie2/docs/DUAL-REPO-SETUP.md) (understand two-repo architecture)
- [ ] Read [../faerie2/SEMANTIC-INTENT.md](../faerie2/SEMANTIC-INTENT.md) Part 1-2 (understand skills + intent)
- [ ] Environment variables are set: `echo $FAERIE_REPO $FAERIE_VAULT` (both should print paths)

---

## First Session Flow (10 min)

### Step 1: Understand Current State (2 min)
```bash
# Open this vault in Obsidian
# Click: 30-Evidence/Agent-Output-Dashboard.md
# This shows all findings produced so far (empty on first run)

# Click: 01-Memories/HONEY.md
# This is crystallized memory from prior sessions (empty on first run)
```

### Step 2: Start faerie2 Session (3 min)
```bash
# In Claude Code:
cd $FAERIE_REPO
claude

# Load dashboard
/faerie
# Shows: context snapshot, queue status, next tasks
```

### Step 3: Queue or Run Missions (3 min)
```bash
# Option A: Queue a new task
/queue
# Follow prompts: goal, priority, agent type, investigation_label

# Option B: Run existing queued missions
/run --missions
# faerie2 discovers tasks and spawns agents
```

### Step 4: Watch Results Appear (2 min)
```bash
# In vault (keep Obsidian open):
# 30-Evidence/Agent-Output-Dashboard.md auto-updates as Dataview refreshes
# No polling. Just watch it populate.

# Agents produce manifests → vault reads forensics/ → Dataview queries fire
# 1-2 min typical latency
```

### Step 5: Session Wrap-Up (optional)
```bash
# End of session (optional, helps next session):
/handoff
# Synthesizer agent crystallizes findings to HONEY.md + Droplets
# Next session starts ~11K tokens ahead (not cold at 61K)
```

---

## Key Concepts (Read Before Investigating)

### Investigation Label
**What:** A tag grouping related tasks into a mission cluster.

**Example:** `treasury-ip-origins` groups all tasks investigating IP ownership patterns for a company.

**Why:** Agents coordinate by label. Related tasks run together, increasing context + speed.

**When to set:** Every time you `/queue` a task or run `/run --missions`.

---

### Compass Edge (N/S/E/W Routing)
**What:** A compass direction indicating the next task bearing.

**Meanings:**
- **N (North)** → Unblock prerequisites (missing input data)
- **S (South)** → Proceed (high quality + confidence, move forward)
- **E (East)** → Parallel investigation (good output, low confidence, validate separately)
- **W (West)** → Return to HQ (honest work failed, reframe task)

**When to care:** Advanced usage. Beginners can ignore; agents handle routing.

---

### Dashboard Line
**What:** A ≤80 character outcome summary from an agent.

**Example:** `"Found 42 active AWS regions; 8 risky; identified 3 account anomalies"`

**Why:** Lets you scan many agent results quickly without reading full artifacts.

**Where:** Visible in 30-Evidence/Agent-Output-Dashboard.md (Dataview query).

---

### Phase Gates (SEED → DEEPEN → EXTEND → FULL)
**What:** Quality thresholds that determine when to advance investigation.

**Meanings:**
- **SEED** (50% quality) — Initial hypothesis, rough scope
- **DEEPEN** (70% quality) — Focused ingest, higher confidence
- **EXTEND** (80% quality) — Cross-validation, edge cases
- **FULL** (85% quality) — Production ready, court admissible

**When to care:** When reading dashboard_line or reviewing agent reputation.

---

## Live Dataview Dashboards

Dataview queries auto-populate as agents produce findings. No manual refresh needed.

### Agent-Output-Dashboard.md
Shows all agent findings with:
- Task ID
- Agent name + model
- Dashboard line (outcome)
- Timestamp
- Status

**Click:** `30-Evidence/Agent-Output-Dashboard.md`

**Troubleshooting:** If empty and agents have run, see [DUAL-REPO-SETUP.md → Troubleshooting → Dataview](../faerie2/docs/DUAL-REPO-SETUP.md#troubleshooting-dataview-no-results).

---

### Agent-Reputation.md
Shows agent performance metrics:
- Composite score (0.0–1.0)
- Success rate
- Manifest truthfulness
- Recent training

**Click:** `03-Agents/Agent-Reputation.md`

**What it means:** Agents ≥0.5 are healthy. <0.5 are in recovery. System naturally improves good agents, phases out poor ones.

---

## Glossary (Vault Context)

| Term | Meaning |
|------|---------|
| **faerie2** | Orchestration engine (spawns agents, writes forensics/) |
| **forensics/** | Immutable artifact folder (in faerie2, not vault) |
| **manifest** | Agent outcome (task_id, dashboard_line, compass_edge) |
| **Dataview** | Obsidian plugin (auto-populating queries) |
| **HONEY.md** | Crystallized memory (readable + tagged) |
| **Droplets** | Preserved insights (hand-curated, long-lived) |
| **investigation_label** | Tag grouping related tasks |
| **dashboard_line** | ≤80 char outcome summary from agent |
| **phase gate** | Quality threshold (SEED/DEEPEN/EXTEND/FULL) |
| **compass edge** | Next task bearing (N/S/E/W routing) |

---

## Common Workflows

### Workflow 1: Start Fresh Investigation
```bash
1. Create subfolder in 10-Investigations/ (e.g., "treasury-ip-origins")
2. /queue to add first task (set investigation_label = "treasury-ip-origins")
3. /run --missions to spawn agents
4. Watch 30-Evidence/ dashboards populate
5. At session end: /handoff to crystallize findings
```

### Workflow 2: Continue Prior Investigation
```bash
1. Open 01-Memories/HONEY.md (load prior session context)
2. Click 30-Evidence/Agent-Output-Dashboard.md (review what's known)
3. Read 01-Memories/Droplets/ (preserved insights)
4. /faerie to check orchestration status
5. /run --missions to spawn next round of agents
```

### Workflow 3: Review Evidence for Court
```bash
1. Go to 30-Evidence/Tier-4-Court-Ready.md
2. Check 70-Sources/ for documentation + hashes
3. Verify manifests in forensics/ (chain-of-custody proof)
4. Use 6x_forensic_recovery.py to bundle artifacts for legal
```

### Workflow 4: Collaborate (Team Investigation)
```bash
1. One person runs setup.sh + forks faerie-vault to shared repo
2. Team members clone faerie2 + fork faerie-vault
3. Everyone mounts shared forensics/ (NFS, SMB, or S3)
4. Everyone syncs vault via Git
5. Coordinate in 00-SHARED/Coordination/ notes (async)
6. Dataview dashboards auto-update for all (near-real-time)
```

---

## Troubleshooting in Vault

### Dataview Queries Show "No Results"
**Fix:** See [DUAL-REPO-SETUP.md → Troubleshooting → Dataview](../faerie2/docs/DUAL-REPO-SETUP.md#problem-dataview-no-results--blank-dashboards).

**Quick check:**
```bash
# Verify faerie2 has produced manifests
ls $FAERIE_REPO/forensics/manifests/$(date +%Y-%m-%d)/
# Should list files like: 14-35-22Z_manifest_*.json

# If empty: agents haven't run yet (expected on first run)
# If exists: Dataview should show results within 1-2 min
```

---

### Vault Won't Open
**Fix:** See [DUAL-REPO-SETUP.md → Troubleshooting → Obsidian](../faerie2/docs/DUAL-REPO-SETUP.md#problem-obsidian-wont-open-faerie-vault-or-shows-errors).

**Quick check:**
```bash
# Verify vault path
echo $FAERIE_VAULT
# Should print: /mnt/d/0local/gitrepos/faerie-vault (or your path)

# Verify vault exists
ls $FAERIE_VAULT
# Should list: 00-SHARED/, 01-Memories/, 02-Skills/, etc.
```

---

### Can't Find a Finding
**Use the global search:**
- Obsidian: Cmd+Shift+F (Mac) or Ctrl+Shift+F (Windows/Linux)
- Search term (IP, domain, finding name, investigation label)
- Results show matching files + line numbers

---

## Next Steps

### After Reading This (Now)
1. Verify vault opens without errors
2. Check `30-Evidence/Agent-Output-Dashboard.md` (see what's known)
3. Read `01-Memories/HONEY.md` (load context)

### After First Setup
1. Read [DUAL-REPO-SETUP.md](../faerie2/docs/DUAL-REPO-SETUP.md) (two-repo architecture)
2. Read [SEMANTIC-INTENT.md](../faerie2/SEMANTIC-INTENT.md) Part 1-2 (skills + intent)

### After First Session
1. Run `/faerie` to check orchestration status
2. Queue a task via `/queue` or run `/run --missions`
3. Watch dashboards populate in real-time
4. Read `/handoff` output (see what agents found)

### Advanced (After 2-3 Sessions)
1. Read [IDEA-COMPASS-ARCHITECTURE.md](../faerie2/docs/IDEA-COMPASS-ARCHITECTURE.md) (compass navigation)
2. Read [FORENSIC-INTEGRITY.md](../faerie2/docs/FORENSIC-INTEGRITY.md) (court-ready proofs)
3. Set up collab (see [COLLAB-GUIDE.md](../faerie2/docs/COLLAB-GUIDE.md))

---

## Quick Reference: Common Commands

| Command | What It Does |
|---------|------|
| `/faerie` | Show orchestration dashboard + status |
| `/run --missions` | Discover tasks, spawn agents by investigation_label |
| `/queue` | Queue a new task interactively |
| `/handoff` | Session wrap-up: crystallize findings, sync vault |
| `/crystallize` | Promote NECTAR → HONEY (on demand) |
| `/compass` | View compass graph (task routing visualization) |

**For full reference:** See `02-Skills/` folder or [SEMANTIC-INTENT.md](../faerie2/SEMANTIC-INTENT.md) Part 2.

---

## Questions?

- **"How do I start an investigation?"** → See [Workflow 1](#workflow-1-start-fresh-investigation) above
- **"Something looks broken"** → See [Troubleshooting](#troubleshooting-in-vault) section
- **"I don't understand the two repos"** → Read [DUAL-REPO-SETUP.md](../faerie2/docs/DUAL-REPO-SETUP.md) "Why Two Repos"
- **"How do agents find my task?"** → Read [SEMANTIC-INTENT.md](../faerie2/SEMANTIC-INTENT.md) Part 2 (skills + routing)
- **"Can I use this vault with other tools?"** → Yes. Vault is pure Markdown. Sync to Git, S3, or sync via Obsidian Sync.

---

## Final Note

**You are not responsible for orchestration.** faerie2 handles agent spawning, coordination, memory. You just:
1. Open this vault
2. Queue tasks or read dashboards
3. Review findings (Evidence/ folders)
4. Read HONEY.md at session start

That's it. The rest is async. Agents work while you're offline. Dashboards update automatically. Memory evolves.

**Start by reading the [Pre-Session Checklist](#pre-session-checklist-before-starting-investigation), then jump into [First Session Flow](#first-session-flow).**

Good luck investigating!

---

**Related docs:**
- [DUAL-REPO-SETUP.md](../faerie2/docs/DUAL-REPO-SETUP.md) — Two-repo setup + troubleshooting
- [SEMANTIC-INTENT.md](../faerie2/SEMANTIC-INTENT.md) — Skills + intent setting
- [../faerie2/README.md](../faerie2/README.md) — Architecture overview
- [HOW-SYNC-WORKS.md](./HOW-SYNC-WORKS.md) — Vault ↔ forensics/ mechanics
