# Architecture — claude-cli

> **LEGACY:** This document predates the 2026-04-05 overhaul and has been merged into [../ARCHITECTURE.md](../ARCHITECTURE.md).
> For current docs, see the root ARCHITECTURE.md.
> Kept for historical reference.

Full-featured Claude Code CLI configuration with persistent memory, multi-session orchestration, investigation pipelines, and self-improvement loops.

## 2026-03-19 Canonical Memory Contract

- **Global canonical:** `~/.claude/memory/HONEY.md`
- **Global additive:** `~/.claude/memory/NECTAR.md`
- **Project canonical (optional):** `{repo}/.claude/memory/HONEY.md`
- **Human review queue:** `~/.claude/memory/REVIEW-INBOX.md`
- **Deprecated:** `~/.claude/AGENTS.md` (stub only, replaced by HONEY/NECTAR)

All orchestration (`/faerie`, `/new`, lifecycle rules, memory routing) should read/write through this contract.

## 2026-03-20 Release Architecture (Cross-Platform + Modular Boundary)

- Added cross-platform release output folders:
  - `releases/windows/.claude`
  - `releases/linux/.claude`
  - `releases/macos/.claude`
- Added release builder:
  - `scripts/0b_build_release_bundles.py`
  - source baseline: repo `.claude`
  - per-OS templates: `releases/templates/*-settings.template.json`
- Added clean product boundary manifests:
  - orchestration public module: `modules/orchestration/manifest.json`
  - memory private module: `modules/memory/manifest.private.json`

Boundary intent:
- **Orchestration module** = queue, routing, Turn-1 state machine, dashboard, operational hooks.
- **Memory module** = crystallization policy, advanced memory stores, and forensics/memory governance.

## v2.1 Design Principles (Operational)

- **Brief-first, bounded fallback:** read compact artifacts first; deep reads only when freshness fails.
- **Execute on Turn 1:** orchestration launches HIGH-priority flow immediately after startup checks.
- **Script-heavy, prompt-light orchestration:** compute state in Python, pass compact summaries to model.
- **Dead-reckoning task contract:** each task carries rich context bundle fields for cold-start execution.
- **Separation by intent:** orchestration runtime is distributable, memory governance is independently packageable.
- **Cross-platform parity:** release bundles are generated per OS from a single `.claude` baseline + templates.

## v2.1 Benefits

- Reduces startup context burden and repeated narrative context.
- Improves session continuity when `/handoff` is forgotten.
- Makes queue/agent/project state visible in one terminal dashboard.
- Supports cleaner legal/forensic isolation with append-only COC.
- Enables OSS release of orchestration without disclosing private memory policy assets.

## Command Cheat Sheet

### Runtime / Operator

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

### Dev / Build / Packaging

```powershell
python "scripts/0b_build_release_bundles.py" --profile full
python "scripts/0b_build_release_bundles.py" --profile orchestration
python "C:\Users\amand\.claude\hooks\state\s3a_faerie_turn1.py"
python "C:\Users\amand\.claude\hooks\state\s3b_dynamo_orchestrator.py"
python "C:\Users\amand\.claude\hooks\state\s3b_dynamo_orchestrator.py" --watch 2
```

## Memory Read Architecture

**Faerie reads** (session start, orchestrator only):
1. `~/.claude/memory/HONEY.md` — crystallized wisdom, dense seed (≤200 lines)
2. `~/.claude/memory/NECTAR.md` tail-30 — recent validated findings
3. `~/.claude/agents/*.md` — agent cards (capabilities, KPIs, training history)
4. `~/.claude/memory/REVIEW-INBOX.md` — outstanding flags for human review

**Faerie curates** → **Context bundle** (2-4K tokens per task)
- Excerpts of HONEY relevant to the task
- Key facts from NECTAR if investigation
- Agent KPI/convention excerpts (not full cards)
- Relevant file paths and prior run state

**Subagents receive** → **Just the context bundle**
- Bundle is in the spawn prompt
- Agents do NOT independently read HONEY, NECTAR, or their own cards
- Agents read what they need for work (code, data, evidence files)
- Agents read prior task state if resuming

**Nothing is wasted:**
- Agent observations → scratch (per-session)
- memory-keeper promotes scratch → NECTAR (validated findings)
- faerie crystallizes NECTAR → HONEY (next session's seed)

## Directory Map

```
claude-cli/
├── AGENTS.md              — DEPRECATED (replaced by ~/.claude/memory/HONEY.md)
├── ARCHITECTURE.md        — THIS FILE (strategic map for all agents)
├── CLAUDE.md              — Session rules, footer format, context budget
├── CONSOLIDATION.md       — Migration history and dedup decisions
│
├── plugins/               — Official-format plugins (installable packages)
│   ├── PLUGINS-INDEX.md   — Quick reference for all plugins
│   ├── cyberops-memory/   — Memory + context + learning + faerie
│   ├── cyberops-orchestration/ — Queue + tasks + coordination + drops
│   ├── cyberops-investigation/ — Data pipelines + stats + evidence
│   └── claude-plugin-creator/  — Tool to create new plugins from skills
│
├── skills/                — All 31 skills (standalone, /skillname invocation)
├── agents/                — All 41 agent definitions (.md files)
├── commands/              — Slash commands (legacy format, still works)
├── rules/                 — Auto-loaded rules (every session, every agent)
├── hooks/                 — Event handlers (presend, PostToolUse, etc.)
├── memory/                — Shared memory layer
│   ├── REVIEW-INBOX.md    — Human review queue (flagged items)
│   ├── KNOWLEDGE-BASE.md  — Validated durable facts
│   └── scratch-*.md       — Per-session working notes
├── scripts/               — Python utilities (vault_push, usage_logger, etc.)
├── settings.json          — CLI settings
├── settings.local.json    — Local overrides (API keys — DO NOT COMMIT)
├── mcp.json               — MCP server configuration
└── essentials/            — Curated index of critical skills/agents
    └── ESSENTIALS.md
```

## Plugin Architecture

Plugins are the **recommended** way to package skills for sharing. Each plugin is self-contained:

```
plugin-name/
├── .claude-plugin/plugin.json   — metadata (name becomes namespace)
├── skills/                      — SKILL.md folders → /plugin-name:skill-name
├── agents/                      — agent .md files
├── commands/                    — slash commands
├── hooks/hooks.json             — event handlers
└── scripts/                     — supporting Python/Bash scripts
```

### Three Core Plugins

| Plugin | Skills | Agents | Purpose |
|--------|--------|--------|---------|
| **cyberops-memory** | memory, context-roundup, continual-learning, handoff, faerie | memory-keeper, membot, context-manager, knowledge-synthesizer, inbox-watcher | Persistent memory across sessions |
| **cyberops-orchestration** | sprint-prep, queue, task, run, suggest, subagent-spawn, token-optimizer | workflow-orchestrator, team-builder, task-distributor, performance-eval, performance-monitor, token-optimizer | Task management, multi-session coordination |
| **cyberops-investigation** | data-ingest, stat, vision-ingest, audio-ingest, workflows, memory-ingest | evidence-curator, data-scientist, data-engineer, research-analyst, security-auditor, data-analyst | Investigation data pipelines |

### How They Link Together

```
SESSION START
    │
    ▼
/faerie (cyberops-memory)
    ├── Step 0: Live bridge — reads agent_state.json + drops.json + queue
    ├── Step 1: Context roundup + continual-learning → HONEY.md
    ├── Step 2: Brief user on state
    ├── Step 3: Fill session template with context bundle
    └── Step 4: Add to queue or hand off to /new
                  │
                  ▼
/run (cyberops-orchestration)
    ├── Claims next task from queue (atomic, session-stamped)
    ├── Reads context bundle → spawns team
    ├── Agents execute with fresh 200K context windows
    └── Results committed + new tasks queued
                  │
                  ▼
DURING WORK
    ├── /memory write "observation" → scratch file → REVIEW-INBOX
    ├── /collab → dead-drop messages between sessions
    ├── /suggest → proposes next tasks from state
    └── /stat, /data-ingest, /workflows → investigation pipelines
                  │
                  ▼
SESSION END
    ├── membot promotes scratch → REVIEW-INBOX → KNOWLEDGE-BASE
    ├── /handoff → bundles for next session
    ├── run-eval → scores session → run-benchmarks.json
    └── W&B logging → wandb.ai/aegis-eternis/cybertemplate-ops
```

## Inter-Session Communication

Two concurrent sessions coordinate via shared files (no real-time needed):

| Mechanism | File | Updated by | Read by |
|-----------|------|-----------|---------|
| Agent state | `hooks/agent_state.json` | presend hook (every turn) | /faerie live bridge |
| Dead drops | `hooks/state/drops.json` | `/collab` command | presend hook (every turn) |
| Task queue | `hooks/state/sprint-queue.json` | `/task`, `/faerie` | `/run`, `/queue` |
| Session registry | `hooks/state/sessions-registry.json` | `/collab register` | `/faerie`, `/collab` |
| Scratch notes | `.claude/memory/scratch-*.md` | any agent during work | /faerie, membot |

## Obsidian CyberOps Vault Integration

Memory syncs bidirectionally with the CyberOps vault via Syncthing:

```
LOCAL                                    VAULT (Obsidian)
──────────────────────────              ─────────────────────────
memory/REVIEW-INBOX.md    ──sync──►    00-Inbox/AGENT-REVIEW-INBOX.md
memory/KNOWLEDGE-BASE.md  ──sync──►    01-Memories/agents/KNOWLEDGE-BASE.md
memory/scratch-*.md        ──flush──►   01-Memories/agents/
                                        03-Agents/active_agents.json
```

Vault root: `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps`

Humans review in Obsidian → agents pick up on next `/faerie` run.

## Evaluation & Self-Improvement

| Component | What it does |
|-----------|-------------|
| `run-benchmarks.json` | Scores each sprint (turns, agents spawned, items processed, cost) |
| `performance-eval` agent | Tracks recurring patterns, flags promotion candidates |
| W&B integration | `scripts/wb_sprint_log.py` → logs to wandb.ai/aegis-eternis/cybertemplate-ops |
| Training roster | `skills/training-roster/` → cross-pollinates learnings between agents |
| Autotune | `skills/autotune/` → 5-minute iterative agent improvement loops |
| Continual learning | Embedded in /faerie → promotes to NECTAR, crystallizes to HONEY |

**Self-improvement loop:**
1. Sprint runs → run-eval scores it → benchmarks updated
2. Performance-eval compares to prior runs → flags improvements/regressions
3. Training roster cross-pollinates learnings between agent types
4. Autotune runs targeted improvement on underperforming agents
5. Continual-learning promotes verified patterns to NECTAR → crystallizes to HONEY
6. W&B tracks all of this for longitudinal analysis

## Phases & Decision Log

### Phase 1-2: Audit & Measurement (✅ Complete — 2026-03-15)
- Audited full 8-stage faerie pipeline, identified 7 handoff points
- Measured self-correction effectiveness on 5 dimensions: feedback_closure, agent_adaptation, error_recovery, memory_promotion, route_optimization
- Baseline score: 0.156 (15.6% effective). Target: 0.45 (3× improvement)
- Root causes: (1) routing doesn't read scores, (2) training queue stranded, (3) beat-last unverified

### Phase 3: Design Fixes (✅ Complete — 2026-03-15)
- **Gap-1 Fix:** score-driven routing via `select_agent.py` (ranks team by effective_score, injects MINI_LEARNING for degraded agents)
- **Gap-2 Fix:** beat-last verification via `beat_last_verifier.py` (auto-updates agent cards when agents beat previous score)
- **Gap-3 Fix:** training queue consumption via `training_queue_manager.py` (on-the-job learning for agents with pending training)
- Decision: Integrate all 3 fixes into /faerie, /run, and performance-eval

### Phase 4: Integration & Loop (🔄 In Progress — 2026-03-18)
- ✅ Score-driven routing wired into faerie.md Step 1b (select_agent.py called during adaptive routing)
- ✅ Training queue check wired into /run pre-spawn (step 4.5, injects MINI_LEARNING for eligible agents)
- ✅ Beat-last verification wired into performance-eval (calls beat_last_verifier.py, auto-updates agent cards & training_queue.json)
- ✅ Continuous improvement loop created (6h interval, runs /run tasks, measures, auto-trains on stall, stops at 0.45)
- ✅ Loop monitoring added to /queue --loop flag
- **Next:** Validate loop is consuming training queue entries, measure actual score improvement, hit 0.45 target

### Phase 5: Validation & Release (📋 Pending)
- Run loop for 3-5 iterations to validate all fixes wired correctly
- Measure if baseline 0.156 → 0.45+ within 20 iterations
- Document any new learnings in agent cards
- Commit integration PR
- Success = Score reaches 0.45 with zero regressions on other dimensions

## Key Decisions

- **Skills vs Plugins**: Skills for quick personal use; plugins for sharing/distribution. Both work.
- **HONEY.md cap**: 200 lines max — crystallized, not accumulated. Faerie enforces this.
- **Memory is append-only**: Scratch → REVIEW-INBOX → KNOWLEDGE-BASE. Never overwrite.
- **Context bundles**: Every queued task gets a rich context bundle so agents start immediately.
- **Dead reckoning**: Agents estimate their context position each turn (Bayesian dead reckoning).
