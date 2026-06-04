---
type: reference
status: active
created: 2026-04-21
tags: [commands, reference, faerie]
up: README.md
prev: FOUNDER-GUIDE.md
next: SETUP-CHECKLIST.md
---

> [↑ Readme](README.md) · [← Founder Guide](FOUNDER-GUIDE.md) · [→ Setup Checklist](SETUP-CHECKLIST.md) · [⌂ Home](../README.md)

# Faerie Command Guide

Power-user reference for the faerie orchestration system. Read this after `ARCHITECTURE.md`.

---

## When to use what

| Command | Use when | Don't use when |
|---------|----------|----------------|
| `/faerie` | Session START — read HONEY.md, orient from memory, launch HIGH queue | Mid-session (wastes cold-start overhead — just keep working) |
| `/faerie focus on {topic}` | Session start with a known topic filter | You want the full queue |
| `/faerie --train` | Autotune agents, skip real investigations | Active investigation sessions |
| `/faerie --queue` | Shape/reorder tasks without running them | You want to actually execute |
| `/run` | Claim and execute the next queued task | Orienting — do /faerie first |
| `/queue` | View task state, check what's queued/claimed | Actually running tasks |
| `/handoff` | Session END — wind-down, promote memory, snapshot | Mid-session (it's the inverse of /faerie — use only at day end) |
| `/data-ingest` | Running the full investigation pipeline | Light one-off tasks |
| `/memory` | View scratchpad, write observations, promote flags | — |
| `/memory learn` | After promoting items — runs continual-learning to update HONEY.md | Every turn (expensive, run once at session end) |
| `/crystallize` | Human-triggered memory compression round | Automatic/scheduled (human only, gauntlet required) |
| `/audit-equilibrium` | After adding scripts | Every session |
| `/audit-coc` | After pipeline runs | Every session |
| `/dev-eval` | System eval snapshot — ALWAYS re-runs eval_harness (never reads cached system-eval.json) | Real investigation work |
| `/dev-status` | All-in-one snapshot — eval + queue + memory health | — |
| `/suggest` | Get next high-value task proposals | You already know what to do |
| `/memory-audit` | Audit routing violations — case data in global HONEY, over-budget files | — |
| `/collab-export` | Share crystallized process knowledge with a collaborator | Sharing findings or evidence (NEVER leaves) |

---

## The session lifecycle

```
SESSION START
  /faerie
    ├── reads ~/.claude/HONEY.md (crystallized prefs)
    ├── reads ~/.claude/memory/NECTAR.md tail-30 (recent findings)
    ├── reads faerie-brief.json (if fresh — cold-start fuel)
    ├── scans sprint-queue.json for HIGH tasks
    ├── launches Wave 1+2 inline, Wave 3 background
    └── returns dashboard (one response)

DURING SESSION
  /run              ← claim + execute tasks
  /queue            ← view state
  /memory write     ← flag observations
  [agents spawn, work, return manifests]

SESSION END
  /handoff
    ├── collect scratch files from all repos
    ├── promote HIGH flags → REVIEW-INBOX
    ├── write validated findings → NECTAR.md
    ├── crystallize prefs/methods → HONEY.md
    ├── write last-session-handoff.md
    ├── spawn membot (mechanical promotion)
    └── brief, exit
```

---

## Queue flow in detail

```
/task "description"         ← add to sprint-queue.json
/faerie                     ← reads queue, launches HIGH tasks
/run                        ← claims next queued task, spawns agents
  agent → writes manifest → ~/.claude/hooks/state/wave2-{type}-result.json
  faerie reads manifest on TaskNotification
/handoff                    ← session end, memory promotion
```

**Sprint queue location:** `~/.claude/hooks/state/sprint-queue.json` — always global, single source of truth across repos.

**Project scoping:** Tasks in the queue include a `project` field. `/run` filters by `PROJECT` env var if set.

---

## Memory topology

```
HONEY.md         ~/.claude/HONEY.md           ← global prefs/methods/identity
                  {repo}/.claude/memory/HONEY.md   ← project-specific facts (rare)
NECTAR.md        ~/.claude/memory/NECTAR.md   ← validated findings (append-only forever)
REVIEW-QUEUE     ~/.claude/memory/REVIEW-QUEUE.json   ← atomic claim state (fcntl.flock)
REVIEW-HOT       ~/.claude/memory/REVIEW-HOT.md       ← lean active-flags hotlist (~2K tokens)
pollen           {repo}/.claude/memory/pollen-{SID}.md ← working notes (ephemeral, gitignored)
```

**Read order at session start:**
1. `~/.claude/HONEY.md` (always — crystallized wisdom)
2. `~/.claude/memory/NECTAR.md` tail-30 (if investigation)
3. `~/.claude/memory/REVIEW-HOT.md` (~2K tokens active flags)

**Memory routing test for HONEY.md:**
> "Would this line mean anything to an agent on a completely different investigation?"
> YES → global HONEY (`~/.claude/HONEY.md`)
> NO → investigation HONEY (`{repo}/.claude/memory/HONEY.md`) or NECTAR

---

## Environment setup

### Required env vars

```bash
# In ~/.bashrc or ~/.zshrc:
export SPRINT_QUEUE_FILE="$HOME/.claude/hooks/state/sprint-queue.json"
export CT_VAULT="/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED"

# Per-repo (or auto-detected by claim_task.py):
export PROJECT="cybertemplate"
```

**The global queue is the single source of truth.** Each repo's `.claude/settings.json` must NOT override `SPRINT_QUEUE_FILE`.

### Per-repo settings.json

`~/.claude/hooks/state/sprint-queue.json` is the canonical queue path. Never override this in repo-level settings.

### B2 backup credentials

```
~/.b2/faerie.env   — your B2 credentials (never committed)
```

See `scripts/0b_b2_provision.py` in an investigation repo to set up backups.

---

## Investigation pipeline: /data-ingest flow

```
/data-ingest
  ├── Wave 1: data-engineer (ingest CSV/XLSX/JSON)
  ├── Wave 2: evidence-curator (tier + curate)
  ├── Wave 3: data-scientist (statistical analysis)
  ├── Wave 4: security-auditor (hash verification)
  └── outputs → scripts/audit_results/{slug}_RUN{N}.json
```

Run standalone (no faerie session required):
```bash
python3 scripts/run_data_ingest.py \
  --repo /path/to/cybertemplate \
  --rawdata /path/to/rawdata \
  --phase all
```

---

## Crystallization rules (HONEY.md)

**Budget:** 200 lines hard cap. Warn at 150.

**Crystallization is not append — it integrates:**
1. Read ALL related existing entries
2. What does the new fact mean in light of what's already known?
3. Semantic dedup — same content, different wording → merge
4. Supersedure — new fact replaces existing → update old, remove it
5. Already implied → skip entirely
6. Genuinely novel → write in most compressed form

**Crystallization is a human choice.** Agents never queue or trigger it. Only `/crystallize` (human-invoked) and membot's final descent step.

**Gauntlet before any HONEY.md write:**
- Recurrence (3+ faerie cycles)
- Multi-agent validation
- Human review
- Proven impact
- Universality (true across all future sessions, all projects)

---

## Agent self-improvement loop

```
agent completes task
  → performance-eval scores output
  → beat_last_verifier.py compares to baseline
  → IF beat_last: agent self-updates ~/.claude/agents/{type}.md (## Last Training)
  → IF not beat: appended to training-queue.json (on_the_job_eligible: true)
  → OTJ redemption: next real task where agent beats target → self-update + log redemption
```

Training-aware commands:
- `/faerie --train` — autotune agents in training mode
- `/dev-eval` — view current eval scores
- `/train --otj` — list agents eligible for on-the-job redemption

---

## Subagent categories (quick reference)

| Flag | Category | Default team |
|------|----------|--------------|
| `-data` | data | data-engineer → security-auditor → data-scientist |
| `-evidence` | evidence | evidence-curator → code-reviewer → security-auditor |
| `-analysis` | analysis | data-scientist → research-analyst → knowledge-synthesizer |
| `-publish` | publish | report-writer → fullstack-developer → ipfs-publisher |
| `-memory` | memory | memory-keeper → context-manager → knowledge-synthesizer |
| `-ingest` | ingest | Full 10-agent data-ingest pipeline |

Full registry: `~/.claude/hooks/state/subagent-options.json`

---

## Common patterns

### Start a new session
```bash
cd /mnt/d/0LOCAL/gitrepos/{repo}
claude
# Then:
/faerie
```

### Add a task and run it
```bash
/task "research AS400495 BGP routing changes"
/run
```

### Flag something for human review
```bash
/memory write FLAG HIGH -- found anomaly in cert rotation timing
```

### End a session
```bash
/handoff
```

### Check system health
```bash
/dev-status
```

---

*See also: `ARCHITECTURE.md`, `rules/agent-lifecycle.md`, `rules/memory-routing.md`*
