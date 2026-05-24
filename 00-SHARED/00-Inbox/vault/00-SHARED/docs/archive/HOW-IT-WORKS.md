# How This System Works — A Plain-Language Guide

> **LEGACY:** This document predates the 2026-04-05 overhaul.
> For current docs, see [README.md](../README.md) or the vault LAUNCH/ folder.
> Kept for historical reference.

This is a system for making AI sessions **remember**, **learn**, and **coordinate**.
Out of the box, every Claude session starts from zero — no memory of what happened
yesterday, no idea what another session is working on, no way to improve over time.
This system fixes all three.

---

## Memory Read Architecture — The Queen & The Hive

**The flow is one-way:** Pollen (scratch) → Nectar (validated) → Honey (crystallized)

```
SESSION WORK
  └── agents write observations to scratch (pollen)
        ↓
SESSION END (memory-keeper)
  └── promotes scratch → NECTAR.md (validated findings, append-only)
        ↓
HUMAN REVIEW (faerie, /crystallize)
  └── integrates NECTAR → HONEY.md (crystallized wisdom, ≤200 lines)
        ↓
NEXT SESSION (faerie reads at startup)
  └── reads HONEY.md (dense seed, 30 seconds)
  └── reads NECTAR.md tail-30 (recent findings, context)
  └── reads agent cards (KPIs, capabilities)
  └── curates context bundles for each task
```

**Who reads what:**

| Reader | Files | When | Why |
|--------|-------|------|-----|
| **Faerie** (orchestrator) | HONEY + NECTAR tail + agent cards | Session start | Curate context bundles |
| **Subagents** (workers) | Context bundle (in prompt) | Task start | Everything they need |
| **memory-keeper** (promotion) | scratch files | Session end | Elevate findings |
| **Human** (reviewer) | NECTAR, REVIEW-INBOX | Anytime | Decide what crystallizes |

**Subagents do NOT read:**
- HONEY.md (faerie already excerpted relevant parts into bundle)
- NECTAR.md (faerie included findings in bundle if relevant)
- Their own agent cards (faerie excerpted KPIs into bundle)

---

## Investigation narrative (session end)

**`session_stop_hook`** spawns **`scripts/4a_narrative_auto_update.py`** (background, best-effort) so **`docs/narrative/INVESTIGATION-NARRATIVE.md`** gains **pointers**: **Tier 1** promotions; **HIGH** MEM; **MED** MEM with gap/question **`cat`**; **HONEY Critical Blockers**; **`docs/gaps.md`** / investigation **`gaps.md`** edits. First run **bootstraps** dedupe state. Disable with **`NARRATIVE_AUTO=0`** (or **`DAE_NARRATIVE_AUTO`** / **`FAERIE_NARRATIVE_AUTO`**). Project root = **`REPO_ROOT`** / **`DAE_REPO_ROOT`** or Claude’s cwd when the script exists under **`scripts/`**. Keep manual sections for **blockers**, **major questions**, and **evidence gaps / progressive disclosure**; merge auto bullets on **`/handoff`**.

After editing **`.claude/hooks/`**, rebuild release trees: **`python scripts/0b_build_release_bundles.py`**.

---

## v2.1 Modular Runtime (Orchestration + Memory)

- Orchestration runtime is centered on:
  - `.claude/hooks/state/s3a_faerie_turn1.py`
  - `.claude/hooks/state/s3b_dynamo_orchestrator.py`
  - `.claude/hooks/state/dynamo_dashboard.py`
  - `.claude/hooks/state/queue_ops.py`
- Memory runtime is centered on:
  - `.claude/memory/HONEY.md` (crystallized)
  - `.claude/memory/NECTAR.md` (additive)
  - `.claude/rules/memory-routing.md` (canonical routing)
  - `.claude/hooks/forensic_coc.py` (append-only COC stream)
- Packaging boundary:
  - public orchestration manifest: `modules/orchestration/manifest.json`
  - private memory manifest: `modules/memory/manifest.private.json`

---

## The Core Ideas (and What They Mean in Practice)

### 1. The Hive Memory System — Pollen → Nectar → Honey

The bee hive has three memory layers that flow one direction: raw material → validated → crystallized.

**Faerie's job (the queen bee):**
- Reads HONEY.md (≤200 lines of crystallized wisdom from all prior sessions)
- Reads NECTAR.md tail-30 (recent validated findings from the investigation)
- Reads agent cards (know thy workers' capabilities)
- Curates a context bundle for each task: exactly what that worker needs, nothing more

**Subagent's job (the worker bee):**
- Receives a context bundle (faerie already did the reading and synthesis)
- Does specialized work
- Writes observations to scratch (pollen — raw, session-scoped)
- Returns results

**memory-keeper's job (the nurse bee):**
- Promotes scratch → NECTAR (validates findings, makes them permanent)
- Syncs to vault (other sessions can read what was found)

**Human's job (the beekeeper):**
- Reads NECTAR when inspired
- Decides what crystallizes (what's durable enough for HONEY)
- /crystallize integrates NECTAR → HONEY (integration, not compression)
- Next faerie reads the crystallized HONEY and the cycle continues

```
Pollen (scratch)         Nectar (findings)         Honey (wisdom)
session work       ──►    validated facts    ───►   crystallized seed
MEM blocks               append-only              ≤200 lines
ephemeral                forever                  read at every startup
```

**Why this matters:** Subagents don't re-read 10K of HONEY and NECTAR every session.
Faerie does the reading once and curates a 2-4K bundle per task. Total session startup
cost dropped from 61K tokens to 11K.

**Real files:** `~/.claude/memory/HONEY.md` (seed), `~/.claude/memory/NECTAR.md` (lab
notebook), context bundles in `hooks/state/sprint-queue/`, `/faerie` and `/handoff` skills

---

### 2. Rocket Liftoff — Every session has a trajectory

A rocket doesn't cruise at the same altitude forever. It launches, reaches orbit,
does its work, and lands. Every Claude session follows the same arc:

```
T1-2   🚀 LAUNCH        Spawn specialists — they get fresh 200K windows each
T3-7   ⚡ ORBIT          Agents working; parent session stays lean
T8-10  📦 CONSOLIDATE   Agents return; integrate their outputs
T11-13 ⚠️ COMMIT         Write everything to disk — git commit + push
T14+   📦 DESCENT        Auto-compact fires; session lands gracefully
```

The status footer on every response tells you where you are in the trajectory.
Early turns are cheap (cache warming). Middle turns are the work. Late turns are
expensive (context is heavy) — that's when you commit outputs and let the system
compress itself.

**Why it matters:** Without this model, people work until context runs out and lose
everything. The rocket trajectory means outputs are committed before fuel runs out.

**Real files:** `rules/token-optimization.md` (footer format, stages, alerts)

---

### 3. Dead Reckoning — Agents estimate their position without GPS

Sailors navigated by estimating speed and direction from their last known position.
No GPS — just "I was here, going this fast, so I must be about here."

**Every agent does this with context.**

```
Baseline: ~20-25K tokens (system prompt + rules)
Per turn: ~6K (normal) / ~11K (heavy with images/agents)
Position: baseline + (turns × rate) = estimated context used
```

The correction factor (`context-calibration.json`) updates from real observations —
like a sailor updating their charts. When auto-compact fires, that's ground truth.

**Real files:** `hooks/state/context-calibration.json`, `hooks/presend_estimate.py`

---

### 4. Exposing Connections — The web between threads, not just the threads

Most AI work produces long, isolated threads. Session 1 finds X. Session 2 finds Y.
Nobody notices that X and Y are connected.

**This system surfaces connections across sessions, projects, and machines.**

```
Session A: finds unusual SSH certs on German servers
  └── writes <!-- MEM cat=CONNECTION --> to scratch

Session B: finds BGP anomalies pointing to same IP range
  └── writes <!-- MEM cat=CONNECTION --> to scratch

Memory-keeper: promotes both CONNECTION entries to REVIEW-INBOX
Faerie (next session): reads both, spots the link, briefs the user:
  "Sessions A and B both touched the same IP range from different angles"
```

The `CONNECTION` category exists specifically for this. Agents are trained to tag
observations that link to other projects or threads. These auto-promote to the
global REVIEW-INBOX where faerie can cross-reference them.

The evaluator (performance-eval) also compares patterns across repos and task types,
surfacing which investigation approaches are most efficient.

**Real files:** `rules/agent-memory.md` (CONNECTION category), `rules/memory-routing.md`
(cross-project routing), `rules/agent-lifecycle.md` (Section 6 — agent matrix with
faerie integration for every agent type)

---

### 5. Permaculture — Nothing is wasted

In permaculture, every output is an input to something else. Chicken manure feeds
the garden. Garden scraps feed the chickens. Nothing leaves the system as waste.

**This system treats every agent session the same way.**

```
Agent does work
  └── produces output (the deliverable)
  └── produces observations (<!-- MEM --> blocks in scratch)
  └── produces pain points and ideas (also in scratch)
        │
        ▼
Memory-keeper promotes:
  └── FLAGS → REVIEW-INBOX (human reviews in Obsidian)
  └── validated facts → NECTAR.md (append-only lab notebook)
  └── durable patterns → agent cards (via continual-learning)
        │
        ▼
Faerie (next session) reads all of it:
  └── reads HONEY.md (crystallized wisdom from past sessions)
  └── reads NECTAR.md tail-30 (recent findings)
  └── curates into context bundles for new agents
  └── shows performance delta (did we improve?)
  └── suggests next tasks based on what's unfinished
        │
        ▼
New agents start with yesterday's learnings built in
  └── and the cycle continues
```

Nothing is thrown away. Scratch notes become reviewed items. Reviewed items become
validated findings in NECTAR. Validated findings get crystallized into HONEY by faerie.
HONEY becomes context for future agents. Even "null results" (tests that found nothing
significant) get recorded — because knowing what DOESN'T work is as valuable as knowing what does.

The training system (`/autotune`) takes this further: agents literally update their
own definition files when they discover techniques that improve their scores. The
system evolves.

**Real files:** `.claude/memory/HONEY.md` (crystallized wisdom), `.claude/memory/NECTAR.md`
(lab notebook), `.claude/agents/` (agent cards), `skills/autotune/` (self-improvement loops)

---

### 6. Dead Reckoning Queue — Self-Navigating Task Chains

The sprint queue uses **dead reckoning**: each task auto-tees the next one without human coordination.

```
Task A completes
  ├── context from A's work → bundled into Task B's prompt
  └── Task B auto-queues with full context
        ↓
Task B runs
  ├── if success → Task C auto-queues
  ├── if failure → Task B' (retry) queues with "what failed + what to try next"
  └── no human needed to hand off between tasks
```

**Key fields on queue entries:**
- `--next-on-success TASK_ID` — if this task completes, queue that one
- `--next-on-failure TASK_ID` — if this task fails, queue a retry with failure context
- Failure context baked in: "What was tried? What didn't work? Why?"

**Why it matters for async collaboration:**
Two people (or two sessions) can work the same queue without coordination overhead.
Person A finishes task 1. Task 2 auto-queues with A's findings. Person B (or session B)
picks up task 2 while A is offline. When B finishes, task 3 is ready. The queue navigates itself.

Combined with soft affinity (multi-session piston), the shared queue becomes the coordination surface.
Edit in Obsidian (vault), sync via Syncthing, consumed by any `/run`.

**Real files:** `hooks/state/queue_ops.py` (manages next-on-success/failure),
`hooks/state/sprint-queue.json` (the actual queue with next-task fields)

---

### 7. Async Stateless Collaboration — Sessions coordinate without talking

Two Claude sessions can't send messages to each other in real-time. They're stateless —
each one is an isolated process. But they CAN read and write to shared files.

**This is like a team of scientists sharing a lab notebook.**

```
SESSION A                    SHARED FILES                   SESSION B
─────────                    ────────────                   ─────────
writes agent_state.json  →   agent_state.json    ←  reads on startup
writes drops.json        →   drops.json          ←  reads on startup
claims task from queue   →   sprint-queue.json   ←  claims different task
writes to scratch        →   scratch-A.md            scratch-B.md ← writes
                             REVIEW-INBOX.md
                             KNOWLEDGE-BASE.md
```

Neither session knows the other is running. But faerie's "live bridge" (Step 0)
reads `agent_state.json` at startup and tells you: "Another session is on turn 12,
working on evidence tiering. Don't duplicate that work."

The dead-drop system (`drops.py`) lets sessions leave messages for each other:
"I finished the hash audit — pick up the evidence curation." The next session's
faerie reads the drop and includes it in the briefing.

**Real files:** `hooks/agent_state.json` (updated every turn by presend hook),
`hooks/state/drops.py` (dead-drop messaging), `hooks/state/queue_ops.py` (task queue),
`hooks/state/sprint-queue.json` (the actual queue)

---

## Relationship to Claude CLI — The Layering

Faerie is built **on top of** Claude CLI, not replacing it. The layering is:

```
CLAUDE CLI (platform — maintained by Anthropic)
  ├── CLAUDE.md              → project bootstrap (~300 tokens, loaded every turn)
  ├── auto-compact           → context management + summarization
  ├── settings.json          → hook registration (Pre/PostToolUse, Stop)
  ├── Agent tool             → subagent spawning mechanism
  └── .claude/projects/*/memory/ → auto-memory system (overridden by faerie)

FAERIE (our layer — built on Claude CLI, mission-specific)
  ├── HONEY.md               → crystallized wisdom (replaces auto-memory)
  ├── NECTAR.md              → validated findings, audit trail (no CLI equivalent)
  ├── Piston model           → RIDES auto-compact as exhaust stroke (doesn't fight it)
  ├── Context bundles        → curated task prompts for Agent tool
  ├── Sprint queue           → dead-reckoning task chains
  ├── Hooks                  → Python scripts registered in CLI's settings.json
  └── Vault sync             → stigmergy via vault paths + progressive output
```

**Key relationships:**

- **CLAUDE.md is the BOOTSTRAPPER.** It says "read HONEY.md, follow these rules." It's tiny (≤300 tokens)
  because the CLI loads it every turn. It points to faerie's system, doesn't contain the system.

- **HONEY.md is the ACTUAL BRAIN.** Rich crystallized context, loaded once at session start by faerie
  (not by the CLI). Claude CLI doesn't know it exists; faerie reads and curates it.

- **Auto-compact is the EXHAUST STROKE.** Faerie's piston model treats auto-compact as a natural beat,
  not an error. Pre-compact hook saves checkpoint. Post-compact hook resumes. Piston absorbs compaction.

- **settings.json hooks are how faerie WIRES IN.** PostToolUse → forensic_coc.py.
  Stop → session_stop_hook.py. The CLI executes faerie's infrastructure code at natural points.

- **Agent tool is how faerie SPAWNS WORKERS.** Faerie builds context bundles and passes them as prompts
  to the Agent tool. The tool handles subagent isolation and 200K fresh windows.

- **.claude/projects/*/memory/ auto-memory is OVERRIDDEN.** MEMORY.md there is an index only.
  Canonical memory lives in HONEY/NECTAR at global level + in memory-routing rules.

**Why this layering matters:** Faerie can evolve independently from Claude CLI updates. A Claude CLI
upgrade doesn't require changes to faerie. Faerie just keeps using the platform as intended.

---

## How a Real Session Works (Start to Finish)

### You type: `/faerie`

```
Step 0 — LIVE BRIDGE (5 seconds)
  Reads: agent_state.json, sprint-queue.json, scratch files, last handoff
  Reports: "No other sessions active. Last session ended 2h ago,
           completed evidence gap sweep, left 3 items in queue."

Step 1 — ROUNDUP + LEARN
  Reads: HONEY.md (crystallized wisdom), NECTAR.md (recent findings), REVIEW-INBOX
  Runs continual-learning: extracts durable facts from scratch → agent cards
  Reports: "12 items in REVIEW-INBOX, 3 HIGH priority. Agent cards updated."

Step 1b — PERFORMANCE BRIEF
  Reads: run-benchmarks.json
  Reports: "Last run scored 0.92. Tier1 count up 3 vs prior run.
           Context usage 20% lower — cache optimization working."

Step 2 — BRIEF + FILL TEMPLATE
  Summarizes: top priorities, hottest areas, what's unfinished
  Asks: "What's your goal for this session?"
  Fills: session template with context bundle

Step 3 — BUILD CONTEXT BUNDLE
  Creates: dense task-specific packet for each queued task
  Includes: goal, key facts, prior run, open flags, queue state

Step 4 — QUEUE OR HAND OFF
  Either: adds task to queue (run /run to consume)
  Or: outputs paste-ready prompt for /new
```

### Agents work (turn 2 onwards)

```
/run claims next task from queue (atomic — no double-claiming)
  → reads context bundle
  → spawns specialist agents with the bundle
  → agents work in fresh 200K windows
  → agents write observations to scratch
  → agents return output to parent

If mini-learning is enabled:
  → each agent reflects before returning
  → writes 1-2 <!-- MEM --> blocks
  → conditionally updates its own agent.md (only if improvement is durable)
```

### Session ends

```
Memory-keeper (or membot):
  → promotes scratch observations to REVIEW-INBOX
  → promotes validated facts to NECTAR.md
  → runs performance-eval (score, delta, proposals)
  → logs to W&B (memorable name: "sprint-0315-evidence-gap-sweep")
  → updates agent cards with continual-learning
  → writes handoff for next session

Everything survives. Next faerie picks up exactly where this one left off.
```

---

## The Parts List

### Three Plugins (the core system)

| Plugin | What it does | Key skills |
|--------|-------------|------------|
| **cyberops-memory** | Remember across sessions | faerie, memory, handoff, context-roundup, continual-learning |
| **cyberops-orchestration** | Coordinate work | queue, task, run, suggest, sprint-prep, subagent-spawn |
| **cyberops-investigation** | Analyze evidence | data-ingest, stat, vision-ingest, audio-ingest, workflows |

### Rules (auto-loaded, every session)

| Rule | What it enforces |
|------|-----------------|
| `agent-lifecycle.md` | Universal startup, memory, self-update, and mini-learning protocol |
| `agent-memory.md` | Structured `<!-- MEM -->` format, vault sync protocol |
| `memory-routing.md` | Three canonical memory locations, prevents fragmentation |
| `token-optimization.md` | Rocket lifecycle, footer format, commit cadence |
| `subagent-enforce.md` | Real spawning (not inline simulation), mini-learning + training blocks |
| `subagent-categories.md` | Category-based team assembly (-data, -evidence, -analysis, etc.) |
| `script-writing.md` | PID files, signal handlers, timeouts (prevents zombie processes) |
| `wsl-usage.md` | WSL path rules, memory fragmentation prevention |

### Hooks (fire automatically)

| Hook | When | What |
|------|------|------|
| `presend_estimate.py` | Every user message | Estimates cost, shows status line |
| `agent_tracker.py` | Agent start/stop | Tracks active agents in agent_state.json |
| `session_stop_hook.py` | Session end | Consolidates memory, logs session |
| `notification_handler.py` | System events | Handles auto-compact signals |
| `statusline.sh` | Continuous | Shows context/cost in terminal status bar |

### Memory Locations (three, never more)

| Location | What lives here | Committed to git? |
|----------|----------------|-------------------|
| `{repo}/.claude/memory/` | Project scratch, session notes | Yes |
| `~/.claude/memory/` | REVIEW-INBOX, KNOWLEDGE-BASE | No (local) |
| `~/.claude/hooks/state/` | Queue, handoffs, agent state | No (operational) |

### Evaluation + Self-Improvement

| Component | What it does |
|-----------|-------------|
| `run-benchmarks.json` | Last-run KPIs per task type |
| `performance-eval` agent | Compares runs, proposes rule updates |
| `wb_sprint_log.py` | Logs to W&B with memorable names |
| `training-queue.json` | Agents queued for improvement training |
| `/autotune` skill | Iterative agent improvement under constraints |
| `TRAINING_MODE.md` | Strict constraints for evolution sessions |
| Mini-learning | Lightweight learning during real deployment |

---

## For Someone New

1. Copy this `claude-cli/` folder to your machine
2. Run `claude` from a WSL terminal (always WSL path, never Windows path)
3. Type `/faerie` — it reads everything and briefs you
4. Tell it your goal — it builds a context bundle and queues the task
5. Type `/run` — it claims the task and spawns agents automatically
6. When done, memory-keeper promotes learnings for next time

That's it. The champagne pyramid fills the glasses. The rocket follows its trajectory.
The agents dead-reckon their position. Connections surface between threads. Nothing
is wasted. And sessions coordinate through shared files without ever talking directly.

The system gets better every time you use it.

---

## Command Cheat Sheet

### Use

```text
/faerie
/dynamo
/dynamo --watch 2
/new
/run
/task "goal"
/queue
/handoff
```

### Dev / Build

```powershell
python "scripts/0b_build_release_bundles.py" --profile full
python "scripts/0b_build_release_bundles.py" --profile orchestration
python "C:\Users\amand\.claude\hooks\state\s3a_faerie_turn1.py"
python "C:\Users\amand\.claude\hooks\state\s3b_dynamo_orchestrator.py"
python "C:\Users\amand\.claude\hooks\state\s3b_dynamo_orchestrator.py" --watch 2
```
