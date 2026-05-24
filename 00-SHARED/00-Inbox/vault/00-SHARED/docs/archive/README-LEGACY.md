# Long-form README (deprecated)

**Superseded:** The repo entry point is now the root **[README.md](../README.md)** — quickstart-first, with Windows / macOS / Linux paths.

This file keeps the **full narrative** (novelty table, orbit model, use cases, Obsidian vault, contributing, contracts) for deep dives. It is frozen as of the README swap; for the latest single source of truth on behavior, prefer `.claude/commands/faerie.md` and [ARCHITECTURE.md](ARCHITECTURE.md).

---

<!-- BEGIN legacy body (formerly root README.md) -->

# faerie

**faerie transforms you from a passenger to a pilot.**

**Product scope:** faerie targets **Claude Code** — the terminal `claude` CLI and editors (Cursor, VS Code) that use the same project hooks, `~/.claude`, Agent tool, and slash commands. It is **not** designed for Claude Desktop, mobile, or web chat: those surfaces do not expose the same hook pipeline, repo-local `.claude` layout, or real subagent spawns this stack depends on.

Without faerie, you're managing Claude one conversation at a time — re-explaining context, watching sessions end, losing work when windows close. With faerie, you open one terminal and watch a mission control dashboard while specialized agents run parallel work streams in fresh 200K-token windows. You intervene to redirect. faerie handles everything else.

---

## What Makes It Novel

| Problem | Conventional approach | What faerie does |
|---|---|---|
| Sessions start from nothing | Paste context manually | Stop hook writes `faerie-brief.json` on every exit — next `/faerie` reads one file and launches in one turn |
| Main session fills up fast | Summarize and compact | Orbit model: main session stays at ~500 tokens; subagents do the heavy work in fresh windows |
| Memory grows stale and heavy | Delete old notes | Crystallization: HONEY.md at cycle 100 is the same size as cycle 1, but every entry carries more meaning |
| Collaboration exposes private work | Separate repos or manual sharing | HONEY-filtered sharing: review your crystallized insights, copy only what you choose to `00-SHARED/` |
| Multi-session coordination requires tab-switching | Manual checks | Fixed-frame dashboard + session heartbeats show all sessions, queue, hypotheses, blockers in one view |

**Token savings from scripts and hooks:**
- `session_stop_hook.py` writes a complete `faerie-brief.json` on every clean exit → startup reads **1 file instead of 5+**, saving ~40K input tokens per session
- `dashboard.py` renders as a subprocess → dashboard costs **zero tokens** in the main session context
- `session_heartbeat.py` tracks multi-session presence as a lightweight script → **no agent spawn** needed to know who else is working
- HONEY.md crystallization enforces a hard line budget → context cost of memory **never grows** even as knowledge depth increases

---

## What Changes

Without faerie, Claude Code is a conversation. You type, it responds, you type again. Context fills up. Sessions end. The next session starts from nothing.

With faerie, Claude Code becomes a **workstation**. You open one terminal, type `/faerie`, and watch a dashboard of tasks flowing through specialized agents -- each with a fresh 200K context window, each writing insights that survive the session. Pain points auto-queue as tasks. Agents that struggled last time perform better this time. Two sessions can split work without you alt-tabbing between windows.

The experience shifts from "talking to an AI" to "directing a team from mission control."

## Core Ideas

### Flow

Everything in faerie is designed to keep you in flow. No switching between windows and tabs. No re-explaining context. No wondering what happened last session.

You see one dashboard. Tasks move from QUEUED to RUNNING to DONE with output files attached. Insights surface as they are discovered -- not buried in agent transcripts you will never read. When an agent hits a wall, the pain point auto-queues as a new task with context attached. The work never stops moving.

Subagents coordinate through a shared queue and dead-drop messaging. Session A does not need to know what Session B is doing -- faerie tracks it. When an agent in Session B discovers something relevant to Session A, it shows up in the dashboard on the next turn.

### Equilibrium

The system maintains itself. Every addition removes something of equal waste. New command absorbs a redundant one. New memory entry supersedes a stale one. The token budget for faerie's own startup read has gone down even as capability has gone up -- because crystallization makes knowledge denser, not larger.

This is not just file hygiene. It is an architectural invariant. HONEY.md at cycle 100 is the same size as at cycle 1, but every entry carries more meaning. The system gets smarter without getting heavier.

### Maximizing Potential

faerie turns your normal workstation into an AI/ML engineering environment. Agent training uses `/autotune` -- essentially prompt tuning through constrained practice runs with scoring. Agents that beat their benchmarks self-update their cards with what they learned. Agents that miss get queued for on-the-job redemption: the next time they run a real task and succeed, the improvement is captured automatically.

This is the same feedback loop as model fine-tuning, but it operates at the prompt/agent level, on your machine, during your work. No GPUs. No training data pipelines. Just agents getting measurably better at their jobs through structured practice and crystallized learnings.

---

## How It Works

```
/faerie                         You type this once.
  |
  +-- Read brief/HONEY/queue    Orient in 1 turn (~500 tokens)
  +-- Launch HIGH tasks         Background subagents, fresh 200K each
  +-- Output DASHBOARD          Everything at a glance
  |
  |   ORBIT: main stays lean while subagents work
  |   Each return: process result -> commit output -> update dashboard
  |   Pain points auto-queue. Insights auto-surface.
  |
  +-- /handoff                  Crystallize memory for next session
```

### The Dashboard

Your single view into everything happening across all sessions:

```
FAERIE                                                           2 sessions active
============================================================================================
 ID       | STATUS      | TYPE  | GOAL                           | AGENT              | OUTPUT
----------|-------------|-------|--------------------------------|--------------------|-------------------
 task-044 | RUNNING     | work  | draft findings section         | report-writer      |
 task-043 | RUNNING     | work  | tier evidence bundle           | evidence-curator   |
 task-042 | RUNNING     | work  | ETL pipeline clean             | data-engineer      |
 train-02 | RUNNING     | train | tiering drill (max 3 src)      | evidence-curator   |
 task-041 | DONE        | work  | data cleaned                   | data-engineer      | cleaned.csv
          |             |       |   12 dupes removed, schema OK  |                    |
 task-040 | DONE        | work  | security audit                 | security-auditor   | audit_report.md
          |             |       |   3 new IPs -> queued WHOIS    |                    |
 task-045 | QUEUED HIGH | work  | WHOIS 45.38.46.0/24            | research-analyst   |
 task-046 | QUEUED HIGH | work  | Fisher test .gov cert          | data-scientist     |
 task-047 | QUEUED MED  | work  | AS400495 BGP peers [auto]      | research-analyst   |
 train-03 | QUEUED MED  | train | stat rigor drill               | data-scientist     |
 train-04 | QUEUED LOW  | train | clarity scoring (on-the-job)   | report-writer      |
============================================================================================
 REVIEW: Foreign .gov cert on adversary IP -- needs attribution decision
 OTHER SESSION: B | T5 ctx 35K | researching 45.38.46.0/24
 Queue clearing fast -- pull forward MED tasks?
```

One table. Work and training unified. The TYPE column distinguishes them, but they share the same queue because agent time is agent time -- whether the agent is doing real work or practicing, it is improving. Training tasks marked `on-the-job` (like train-04) run real work with autolearn enabled: the agent does the task AND tracks its score. If it beats its benchmark during real work, the improvement is captured as the most valuable kind of learning.

The table refreshes on natural events: a subagent returns (row moves from RUNNING to DONE, OUTPUT fills in, insight line appears), a new task is auto-queued (row added), or you ask. No polling. No wasted turns.

No window switching. No tab hunting. Insights surface inline under DONE rows. Pain points auto-queue as new rows. You see everything flowing.

### The Orbit Model

The main session is air traffic control. It stays lean -- never doing heavy work inline.

1. **Spawn early.** Turn 1 launches all HIGH tasks as background subagents. Each gets a fresh 200K context window. The main session uses maybe 500 tokens to orient.

2. **Stay lean.** While subagents work, the main session barely grows. It is waiting for returns, checking drops from other sessions, refreshing the dashboard.

3. **Commit on return.** When a subagent finishes, the orchestrator processes the result immediately: extract output files, capture insights, commit to git. Work is persisted before anything can be lost.

4. **Auto-queue follow-ups.** If a subagent found something that needs investigation, it queued a follow-up task with full context. If it hit a dead end, the failure context is stacked into the retry task so the next agent does not repeat the mistake.

This means your session extends naturally through subagent windows. A 15-turn main session that launches 5 subagents effectively has 15 + (5 x 50) = 265 turns of useful work, most of it in fresh context.

---

## Use Cases

### Research Pipeline
`/faerie` launches source-ingest, cross-reference, and report-assembly agents in parallel. You watch the dashboard as sources are processed, cross-references found, and the report assembles itself. Output files appear in DONE with insights attached as each agent finishes.

### Plan and Execute (two sessions)
Session A: `/faerie` plans the sprint, queues tasks with rich context bundles.
Session B: `/run` claims tasks, spawns specialist teams, executes.
Dead-drops keep both sessions aware. You see both sessions' progress in one dashboard.

### Adversarial Review
Session A writes a report. Session B spawns adversarial-reviewer to stress-test every conclusion -- finding confirmation bias, flagging weak sources, proposing alternative explanations. A's output is B's input. The queue connects them.

### Statistical Analysis
Queue a stats task. faerie routes it to data-scientist with an anti-p-hacking protocol (pre-registered hypotheses, Bonferroni correction, effect sizes). Results flow back with structured outputs. Significant findings auto-queue follow-ups. Non-significant results auto-queue alternative approaches.

### Agent Training
`/autotune` trains agents through constrained practice -- like giving a junior analyst progressively harder assignments with scoring. evidence-curator might train with a "max 3 sources" constraint to sharpen prioritization. Results go to `training/` with full score history. Agents that improve update their own playbooks. Agents that struggle get another chance during real work -- and when they succeed there, the redemption is captured as the most valuable kind of learning, because it was proven in production.

### Investigation Pipeline
`/data-ingest` spawns 10+ specialists: ingestor, hash guardian, cleaner, transformer, stat analyst, evidence curator. Each writes structured observations. Insights promote through scratch -> NECTAR -> HONEY. Evidence gets tiered (Tier 1 = smoking guns, Tier 2 = strong, Tier 3 = contextual). Chain of custody is court-grade: append-only JSONL with SHA256 hash chains.

---

## Quickstart (generic)

```bash
# 1. Get the faerie branch
git clone -b faerie https://github.com/Persistech/flowsearch.git

# 2. Copy .claude/ to your repo (or symlink to ~/.claude/)
cp -r flowsearch/.claude/ your-repo/.claude/

# 3. Initialize your preferences
cp .claude/memory/HONEY.md ~/.claude/memory/HONEY.md
# Edit HONEY.md: Python path, WSL setup, your role, how you like to work

# 4. Start
cd your-repo && claude
# Type: /faerie
```

**Two-window dashboard (per-OS commands):** see root [README.md](../README.md).

To end a session: `/handoff` -- crystallizes memory so the next `/faerie` picks up exactly where you left off.

---

## Obsidian Vault

flowsearch includes an Obsidian vault at `ObsidianVault/`. It is your private investigation workspace. **Only one folder syncs** — `ObsidianVault/00-SHARED/` — via Syncthing. Everything else stays local.

### 00-SHARED — the collaboration bus

```
ObsidianVault/
  00-SHARED/              ← Syncthing target (this subfolder only, not the vault root)
    sessions/             ← auto: who is working, on what investigation
    inbox/                ← shared task drops (agents pick these up)
    cybersecurity/        ← shared findings by role, not by person
    financial/
    socmint/
    legal/
  00-Inbox/               ← your private inbox (local only)
  10-Investigations/      ← private
  30-Evidence/            ← private ...
```

Role folders are named by contribution angle, not by person. A new collaborator sees `financial/` and immediately knows what is there. Add new roles as needed (`geospatial/`, `medical/`, etc.).

**Two phases.** Drop notes flat in role folders while informal. Once you agree on an `investigation_id`, nest under `{role}/{investigation_id}/`. New collaborators join by adding their role subfolder to the same investigation. Spin-offs use `parent_investigation:` in frontmatter — Obsidian graph shows the lineage.

### HONEY → selective sharing

Your crystallized insights in `~/.claude/memory/HONEY.md` are dense and hard-won. Before sharing, open it and choose what to reveal. Copy selected entries into `00-SHARED/{role}/` as `shared-finding` notes.

```
HONEY.md (private)  →  you review  →  you choose  →  00-SHARED/{role}/{inv-id}/finding.md
```

Share conclusions. Keep methods. People cooperate more when sharing is high-value and low-risk. HONEY makes the value visible; you control what goes across.

### Syncthing setup

```
Syncthing folder:  ObsidianVault\00-SHARED     ← subfolder only, not vault root
Share with:        collaborator's device
```

Session heartbeats auto-write to `00-SHARED/sessions/`. The dashboard `--watch` pane shows all collaborators' active sessions in real time.

---

## Commands

| Command | What it does |
|---|---|
| `/faerie` | Orient + launch + dashboard. The only command most sessions need. |
| `/faerie --train` | Training mode — autotune agents, skip investigation tasks |
| `/faerie --review` | Adversarial mode — red-team findings, no tasks launched |
| `/faerie --queue` | Queue manager — add/reorder/reprioritize only |
| `/faerie --crystallize` | Intentional close — promote to HONEY/NECTAR, queue open threads |
| `/team` | View/modify active agent team |
| `/roster` | List all available agents by category |

## Memory

```
HONEY.md          Crystallized preferences, methods, identity.
                  Read at startup. Enriched every cycle. Same size, richer meaning.

NECTAR.md         Validated findings, sprint summaries.
                  Additive only. Feeds HONEY on crystallize.

training/         Agent improvement history.
  index.json      Agent -> last score, benchmark, learnings (read on demand).
  runs/           Detailed per-agent training reports.

scratch-*.md      Per-session working notes. Promoted to NECTAR at session end.

REVIEW-INBOX.md   Items needing human judgment. HIGH flags auto-promote here.
```

## Design Principles

1. **Flow over friction.** One terminal, one dashboard. No window switching. No re-explaining.
2. **Orbit.** Main session directs. Subagents execute with fresh context. Work extends through their windows.
3. **Commit on return.** Outputs persist to disk the moment subagents finish. No crash landings.
4. **Equilibrium.** Every addition removes something. The system never grows without pruning.
5. **Crystallization > compression.** Memory gets richer, not just smaller.
6. **Act first.** faerie launches without asking. You intervene to redirect, not to approve.
7. **Agents improve.** Training, on-the-job redemption, and self-updating cards create a feedback loop that makes every cycle better than the last.

---

## Contributing

faerie is infrastructure, not an app. Contributing means improving the contracts between the pieces — memory, queue, hooks, agents, vault — without breaking the equilibrium invariant: **every addition must remove something of equal waste.**

### Architecture at a glance

```
~/.claude/
  dashboard.py                    ← fixed-frame ANSI dashboard (subprocess, zero session tokens)
  commands/faerie.md              ← the /faerie skill (read this first)
  commands/handoff.md             ← deprecated; use /faerie --crystallize
  hooks/
    session_stop_hook.py          ← writes faerie-brief.json + heartbeat cleanup on every exit
    agent_state.json              ← session role, turn count, ctx estimate (read by dashboard)
  hooks/state/
    session_heartbeat.py          ← multi-session presence (write/read/clean)
    faerie-dashboard-launcher.py  ← called at end of faerie Turn 1
    sprint-queue.json             ← task queue (O_CREAT|O_EXCL locked, concurrent-safe)
    queue_ops.py                  ← atomic queue operations
    faerie-brief.json             ← complete session context bundle (12h TTL)
    faerie-recovery.json          ← needs_membot_rebuild flag (False = fast launch)
  memory/
    HONEY.md                      ← crystallized prefs/methods (hard 200-line budget)
    NECTAR.md                     ← additive findings log (never compressed)
    REVIEW-INBOX.md               ← human review queue (HIGH flags land here)

ObsidianVault/
  00-SHARED/                      ← Syncthing target (subfolder only)
    sessions/                     ← session heartbeat presence notes
    inbox/                        ← shared task drops
    {role}/                       ← contribution folders (cybersecurity/, financial/, etc.)
      {investigation_id}/         ← formal investigation subfolder
```

### Key contracts

| Contract | Where enforced | Why it matters |
|---|---|---|
| faerie-brief.json ≤ 12h TTL | `session_stop_hook.py` + `faerie.md` Turn 1 | Stale brief causes membot rebuild |
| HONEY.md ≤ 200 lines | `memory-routing.md` crystallization law | Loaded every session — must stay cheap |
| sprint-queue.json writes are atomic | `queue_ops.py` O_CREAT\|O_EXCL | Two sessions can run /run safely |
| 00-SHARED/ is the only Syncthing target | README + `_README.md` | Private vault never exposed |
| Stop hook exits 0 always | `session_stop_hook.py` | Never block session close |
| Dashboard is a subprocess | `dashboard.py` entry point | Zero tokens in main session |

### Adding a new agent

1. Create `~/.claude/agents/{name}.md` with the agent card (role, tools, KPIs, Last Training section)
2. Add to `~/.claude/hooks/state/subagent-options.json` under the appropriate category
3. Follow the lifecycle in `~/.claude/rules/agent-lifecycle.md` — startup reads HONEY, writes scratch, optional mini-learning pass
4. If it produces investigation findings, add a beat-last KPI to `run-benchmarks.json`

### Adding a new role folder to 00-SHARED

```bash
mkdir -p ObsidianVault/00-SHARED/{role-name}
# Create _index.md with type, role, tags frontmatter and a Dataview query
```

Keep names lowercase, one word or hyphenated. Announce in `ObsidianVault/00-SHARED/_README.md`.

### What NOT to touch

- `NECTAR.md` — additive only, never compress, never rewrite history
- `sprint-queue.json` — always use `queue_ops.py`, never write directly
- `00-SHARED/sessions/` — managed by `session_heartbeat.py`, never edit manually
- Any `*-coc.jsonl` or `hash_manifest*.json` — append-only forensic logs

<!-- END legacy body -->
