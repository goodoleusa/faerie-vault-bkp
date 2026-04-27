---
type: narrative
status: living-document
created: 2026-03-21
updated: 2026-03-25
tags: [meta, evolution, changelog, process, creative]
parent:
  - "[[HOME]]"
sibling:
  - "[[00-DESIGN-NARRATIVE-2026-03-22]]"
  - "[[PIPELINE-DESIGN]]"
child:
  - "[[Session-Manifests]]"
  - "[[Pipeline-Gates]]"
  - "[[Faerie-Brief.blueprint]]"
  - "[[Gate-Review.blueprint]]"
  - "[[Session-Manifest.blueprint]]"
memory_lane: nectar
promotion_state: crystallized
doc_hash: sha256:17830f65e24c3ce6f40e3fed5e669f5e1322fea34940a380829f6b3de0938fa4
hash_ts: 2026-03-29T16:09:59Z
hash_method: body-sha256-v1
---

# The Data Analysis Engine — How It Got Here

> A personal narrative of the evolution of this tool. Written so future-me doesn't forget all the cool stuff.

---

## The Origin: A Year-Long Investigation Needed Better Tools

The Data Analysis Engine was born from necessity. A complex year-long investigation with varied data — financial records, network logs, certificates, WHOIS data, screenshots, audio recordings — needed a systematic approach. Manual analysis was hitting walls: too many data sources, too many threads to track, too easy to lose context between sessions.

The first version was simple: a single SKILL.md file (~430 lines) for Claude Desktop plugins. Everything was inline — all 8 subagent dispatch prompts, the phase list, statistical rules, even machine-specific Python paths. You invoked the skill, it walked you through phases. No queue, no hooks, no session continuity. Investigation state lived in your head.

**What survived from this era and never changed:** the pipeline itself. AUDIT → EXTRACT → CLEAN → TRANSFORM → ANALYZE → ASSESS → CURATE. The agent team: Evidence Curator, Data Engineer, Stat Analyst, Hash Guardian, Research Analyst, Report Writer. The chain-of-custody rules. The evidence tier system (Tier 1 = ≤15 smoking-gun items through Tier 4 = full catalog). The forensic principles: append-only logs, SHA-256 manifests, pre-registered hypotheses, Bonferroni correction. None of that changed. The *packaging* changed completely.

---

## Phase 1 — Plugin to CLI (the first rebuild)

Claude Code CLI arrived and the plugin SKILL.md was too fat — 430 lines loading into context every time. Split it into `SKILL.md` (entry) + `reference.md` (full dispatch prompts). Progressive disclosure: load less at startup, read reference when needed. Removed machine-specific paths. Added explicit `subagent_type` mapping for the Agent tool.

Still manual. Still no memory between sessions. Starting a new session meant 10-15 minutes of "where were we?" while agents re-discovered things already known.

---

## Phase 2 — The Session Bus (the breakthrough)

**The key realization:** Investigation state needs to outlive sessions. If you close the laptop mid-sprint, the next session should pick up exactly where you left off.

This is where the "faerie" framework entered the picture. Originally developed as a session orchestrator in a sibling repo (00-claude-faerie-cli-git), faerie introduced the concept of shared files as a communication bus between sessions. DAE imported these patterns wholesale.

Three files changed everything:
- `session-brief.json` (originally `faerie-brief.json`) — written at session end, read at session start. A compact snapshot: what was accomplished, what's next, what's hot.
- `sprint-queue.json` — the shared task list. Survives compaction, session restarts, context limits. Atomic claiming prevents two sessions from grabbing the same task.
- `session-context.json` — live session state (turn count, context estimate, active agents).

These files moved from "nice to have" to **the system**. Everything reads from files, not from chat history. The conversation can be compacted, the session can crash, the user can close the tab — and the next session picks up from the files.

This era also introduced:
- **Context roundup** — extract durable facts from scratch files into HONEY.md
- **Handoff protocol** — session end: write brief, promote findings, queue open threads
- **Session orchestration** — read brief → launch HIGH queue tasks → show dashboard → drain queue → close out

The faerie framework brought the foundational insight that made everything else possible: **state lives in files, not in the conversation.**

---

## Phase 3 — Hooks Absorb the Lifecycle (automation eats ceremony)

**Problem:** Session boundary actions (write brief, promote scratch, run autolearn) were forgettable. I closed sessions without running `/handoff` constantly. Context was lost.

**Solution:** Claude Code hooks. Move lifecycle actions from manual commands into automatic hook scripts:

- `session_stop_hook.py` (SessionEnd) — writes brief, promotes HEADLINE/THREAD MEM blocks to NECTAR, runs autolearn
- `pre-session.py` (SessionStart) — reads brief, writes session-context.json
- PostCompact hook — refreshes state after compaction

**Consequence:** The hooks do what the manual commands were doing. Three skills became redundant overnight:

- `/continual-learning` deprecated — learning is now OTJ (every agent reflects before returning output) plus autolearn on session end
- `/context-roundup` deprecated — pre-session hook reads brief + queue + HONEY automatically
- `/handoff` deprecated → `/crystallize` is the canonical explicit close-out. "Handoff" implied passing to someone else; "crystallize" describes what actually happens (durable facts distilled into HONEY/NECTAR)

---

## Phase 4 — Training Consolidation

Training started as three separate surfaces: `/autotune` (iterative improvement loop), `/training-roster` (batch view of which agents needed training), and ad-hoc `/train`. Unified into `/train --run AGENT`, `/train --roster CATEGORY`, `/train --prep CATEGORY`. Training had its own queue, its own KPIs, its own session mode — they belong together.

---

## Phase 5 — Queue Autonomy (the dynamo)

**The realization:** Agents were mentioning follow-up work in their output text instead of queuing it. Work got lost in scrollback.

**The rule:** anything that discovers actionable work appends to sprint-queue.json immediately. Never ask "should I queue this?"

The queue matured into a dynamo:
- `next_on_success` / `next_on_failure` fields — self-steering
- Priority ladder (HIGH/MED/LOW) — claim_task.py always takes HIGH first
- Auto-queue triggers: HANDOFF blocks, MEM blocks with `cat=THREAD|CONNECTION|FLAG`, open HONEY questions

`/data-ingest` became the primary command because it launches everything: pipeline, queue drain, hooks. One invocation kicks off the entire investigation session.

---

## Phase 6 — Doc Consolidation

~50+ docs in `docs/`. Every design decision had its own doc. New users had no entry point. Consolidated into 4 canonical docs: GUIDE.md, INVESTIGATION-PLAYBOOK.md, HOW-IT-WORKS.md, ADAPT-AND-EXTEND.md. Superseded docs moved to `docs/archive/`. Built `/debloat` skill to scan for remaining creep.

---

## Phase 7 — Agent Learning and First Impressions

Two insights that became system features:

**Process insights compound across agents.** When a data-scientist discovers that Bonferroni correction changes how evidence-analyst should profile data, that knowledge should flow. Added `cat=TECHNIQUE` MEM blocks that auto-promote to AGENTS.md Training section and sync to the Obsidian vault for human review. Agents learn from each other's techniques.

**First impressions are irreplaceable.** I kept getting lost in the sauce — tunnel vision kicks in and the naive-observer perspective evaporates forever. Added `cat=FIRST_IMPRESSION` as a MANDATORY MEM block for data-touching agents: write what stands out, what seems anomalous, what questions arise naturally — BEFORE deep analysis begins. These are gold for hypothesis generation.

---

## Phase 8 — The Obsidian Vault (the human command center)

The investigation needed a place where I could review agent findings, annotate evidence, and steer priorities without being in a live Claude session.

**Design decisions:**
- **Shared folder model:** Only `01-Memories/shared/` and `00-Inbox/` sync between researchers via Syncthing. Everything else stays local. Each researcher controls what to share. This would allow remote async collaboration — multiple researchers with their own Obsidian vaults, sharing a folder.
- **Human annotations are COC'd:** SHA-256 hashing into `annotation-coc.jsonl` with hash chains. Human corrections feed back to agents via vault_sync. Human expertise becomes part of the evidence chain.
- **Card aesthetic:** Navy headings (#1e3a5f), gold accents (#d4a843), card containers with shadows. Dataview-powered dashboards. Mermaid pipeline diagrams. ExcaliBrain for evidence-hypothesis graphs using parent/sibling/child ontology.
- **One-command sync:** `/vault-sync` from chat, or automatic at session start/end. No manual script running.
- **Mission Control:** HOME.md shows: what needs attention, pipeline progress, active tasks, fresh insights (first impressions + techniques), hypothesis strength, evidence gaps. The 30,000-foot view that keeps me from getting lost in the weeds.

---

## Phase 9 — Cutting the Cord (faerie → native DAE)

The session orchestration concepts came from the faerie framework in a sibling repo. For months, DAE imported these patterns — the session bus, the brief files, the queue loop, the crystallization protocol, even the naming conventions. But DAE had grown its own legs:

- `/data-ingest` handles everything the external orchestrator did, plus the investigation pipeline
- Hooks handle session lifecycle automatically
- The queue bus is repo-local (no global `~/.claude` dependency)
- Agent learning is OTJ (built into `rules/agents.md`)

**The decision:** Remove faerie as a named dependency. Keep every functional capability — just own it natively:

| Old (external framework) | New (DAE-native) | Why |
|--------------------------|------------------|-----|
| `/faerie` command | `/crystallize` | The only unique thing it did was AGENTS/HONEY merge |
| `faerie-brief.json` | `session-brief.json` | It's a session brief, not an import |
| `faerie_autolearn.py` | `autolearn.py` | It's autolearn, period |
| `background-faerie.py` | `background-orchestrator.py` | It orchestrates context retrieval |
| `FAERIE_VAULT` env var | `DAE_VAULT` env var | DAE owns the vault relationship |
| `docs/FAERIE-*.md` | `docs/archive/` | Content already in canonical docs |

Zero functionality lost. Zero concepts abandoned. The session bus, the queue dynamo, the crystallization law, the brief protocol, OTJ learning, the equilibrium rule — all the good ideas survived. DAE owns them now.

---

## The Pattern (the meta-lesson)

**Build separate → observe overlap → absorb into core → deprecate the spare.**

Every deprecated skill was a piece of the system that got absorbed. The session bus (brief + queue) is what makes `/data-ingest` work as one command: state lives in files, not in the conversation, so the system always knows where it is.

The faerie framework was essential scaffolding. It introduced the concepts that made DAE possible — session continuity, file-backed state, crystallization, the brief protocol. But once DAE internalized those concepts, the scaffolding could come down. The building stands on its own.

---

## The Cool Stuff (don't forget this)

Things worth remembering when you've been away from this project for a while:

1. **The session bus is everything.** `session-brief.json` + `sprint-queue.json` + `session-context.json`. Files are the communication channel. Sessions can crash, compact, restart — the bus survives.

2. **10+ specialized agents working in parallel.** Not one big model doing everything — an Evidence Curator that knows tiering, a Data Engineer that knows ETL, a Stat Analyst that knows Bonferroni. Each accountable for their domain.

3. **Chain of custody is real.** SHA-256 hash chains, PGP-signed snapshots, append-only forensic logs. Not "we have logs" — forensic-grade provenance that survives adversarial scrutiny.

4. **Anti-p-hacking is built in.** Pre-register hypotheses BEFORE running analysis. Bonferroni correction. Bayesian confidence. The system structurally prevents the most common statistical sins.

5. **Multi-session continuity.** `RUN-NNN` manifests. Pipeline sessions spanning days that never lose state. Start Tuesday, close laptop, pick up Friday — right where you left off.

6. **First impressions are captured.** Before the analyst dives deep, the naive-eye perspective is saved. This has already surfaced insights that tunnel-vision analysis missed.

7. **Agents learn on the job.** Every agent reflects before returning output. Techniques compound across agent types. Training happens during real work, not just in contrived drills.

8. **Human-in-the-loop via Obsidian.** Async collaboration without being in a live session. Annotate findings, correct agents, steer priorities — all through markdown files that sync automatically.

9. **Topic-agnostic.** Replace three files and the same forensic pipeline works for any domain. Financial fraud, surveillance infrastructure, environmental data, public records.

10. **Fully reproducible.** Any finding regenerable from base files by anyone, anywhere. Open science by design.

11. **Session manifests anchor scattered work.** Cross-repo artifact records written at session end — the glue between scattered commits, memory writes, and human comprehension. Auto-synced to vault.

12. **Human gates prevent runaway inference.** Cryptographic hypothesis pre-registration (sealed envelopes), factual-error-only corrections at phase boundaries, anti-coaching validation. The human stays in the loop without contaminating independence.

---

## Phase 10 — Workspace Consolidation + Human Gates (2026-03-25)

### Problems that emerged

**1. Path fragmentation.** WSL and Windows see the same repo as two different paths. `.claude/projects/` creates separate entries for each, scattering session memory. 32 memory files in one entry, 3 in another — for the same repo.

**2. Worktree orphans.** Claude Code creates worktrees for agent work. Four cybertemplate worktrees diverged 245-303 commits from main with 1 trivial commit each. Investigation evidence was trapped in these branches.

**3. Faerie repo drift.** Three separate repos (`faerie`, `faerie2`, `00-claude-faerie-cli-git`) drifted apart over weeks. Commands duplicated across repos — `/handoff` existed in 5 places, user didn't know which was firing.

**4. Hook double-nesting bug.** `_resolve_claude_home()` returns `~/.claude` but 10+ hooks did `HOME / ".claude" / "hooks"` — writing to `~/.claude/.claude/hooks`. Silent failure masked by `|| true` in settings.json.

**5. Session artifacts scatter.** A single session writes to 5+ locations (plans in `.claude/plans/`, memory in `.claude/projects/`, commits in multiple repos, HONEY globally). No unified record of "what happened."

**6. Runaway inference risk.** Progressive disclosure (15% → 50% → 75% → 100%) prevents HARKing, but if agents form incorrect first impressions at SEED, the error compounds through all subsequent phases with no correction mechanism.

### Solutions built

| Problem | Solution | How to monitor |
|---------|----------|----------------|
| Path fragmentation | `canonicalize_paths.py` + consolidated fragmented entries | `ls ~/.claude/projects/` — should show one entry per repo |
| Worktree orphans | Archive tags (`archive/*`), cherry-pick unique files, remove worktrees | `git worktree list` — should show main only |
| Faerie drift | Unified `00-claude-faerie-cli-git` → push to `faerie2` remote | `git -C faerie-cli remote -v` — should show faerie2 |
| Command duplication | Global = universal, repo = domain-specific only. 15 duplicates removed | `ls ~/.claude/commands/` vs `ls {repo}/.claude/commands/` — no overlap |
| Hook double-nesting | Renamed `HOME` → `CLAUDE`, removed `/ ".claude"` in 10+ files | `grep 'HOME.*\.claude' ~/.claude/hooks/*.py` — should return nothing |
| Session scatter | `session_manifest.py` — cross-repo artifact record at session end | Vault `Dashboards/session-manifests/` — should have latest |
| Runaway inference | `gate_pass.py` (4 human gates) + `hypothesis_seal.py` (sealed envelopes) | `python3 scripts/gate_pass.py status` |

### How to ensure it's improving

1. **Session manifests should grow richer.** Early manifests list commits + files. Mature manifests should link to plan phases, show hypothesis movement, and estimate sessions-to-phase-completion.

2. **Gate corrections should decrease over time.** If agents keep needing factual corrections at GATE 1, the SEED sampling or agent prompts need work. Track `corrections_count` across runs.

3. **Path fragmentation should be zero.** If new `.claude/projects/` entries appear with WSL paths when launching from Windows, `canonicalize_paths.py` isn't wired or isn't working.

4. **Command confusion should disappear.** If the user ever wonders "which `/handoff` is this?", a duplicate crept back in.

5. **Hypothesis seal/reveal comparison** is the ultimate validation. If sealed human hypotheses agree with agent conclusions after full analysis — independent convergence. If they diverge — the system caught something interesting either way.

---

## The Scope Hierarchy (the architecture that emerged)

```
Global (.claude/)          → identity, prefs, methods, agent cards
  └─ Investigation         → cross-session, cross-sprint findings
       └─ Sprint           → all work to enter next project phase
            └─ Pipeline Phase → AUDIT→...→PUBLISH (human gates between)
                 └─ Session → one CLI run, partial phase coverage
```

Pipeline Phase is above Session because a phase spans multiple sessions with human gates between stages. `/faerie` launch should always know: which investigation, which sprint, which phase, and estimate how many sessions remain.

The vault is the human annotation interface — the receipt layer. Sensitive forensic material stays local, gitignored. The vault shows "agent X produced this, I annotated that." Light COC (hashes, timestamps) links vault notes to the forensic store without exposing it.
