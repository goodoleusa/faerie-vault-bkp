---
type: design-narrative
status: final
date: 2026-03-29
scope: faerie2 skills — evolutionary history and supersession
purpose: forensic record of skill innovation, obsolescence, and architectural learning
---

# Skills Evolution Narrative — Why Old Ideas Got Replaced

## Preamble

This is a forensic record of skills that no longer serve the faerie system. Each skill was born to solve a real problem at the time. Each was replaced because a more elegant architecture emerged that solved the same problem *and* adjacent ones. Understanding why they mattered helps us understand what the current system learned.

---

## Phase 1: The Training Multiplicity Era (2025–2026 Q1)

### The Problem They Solved

**Context:** Early faerie sessions had no way to measure or improve agent performance. Agents would run once per session; if they succeeded, great. If they failed, their failures weren't systematized. There was no feedback loop.

### Three Skills Emerged

#### `/autotune` — Time-Boxed Iterative Drills (v0.1.0, DEPRECATED)

**What it was:** Spawn an agent with artificial constraints (time limit, citation budget, evidence cap), run N iterations in a hard budget, score each iteration, feed scores back. If iteration N scored better than N-1, lock that improvement and try again.

**Why it was cool:**
- Brought **constraint-driven improvement** to agent training — not just "run the agent," but "run it under adversarial pressure"
- Separated training (constrained lab) from deployment (real sessions) — agents learned differently under pressure
- **Measurable feedback loop:** score → feedback → retry. Concrete proof of improvement.
- Built-in **early-stopping** (plateau detection, budget exhaustion, target hit)

**The Innovation:** Framing agent training as iterative constraint satisfaction, not just parameter tuning.

**What Was Missing:**
- No connection to real deployment metrics
- Training scores didn't predict deployment performance
- Time budget didn't account for actual session context demand
- Standalone — training happened in isolation, learnings didn't flow back into normal sessions

#### `/training-roster` — Batch Agent Improvement (v0.1.0, DEPRECATED)

**What it was:** Run `/autotune` on 5–8 agents sequentially, re-using insights from previous runs (e.g., "evidence-curator improved on prioritization → data-scientist can learn same lesson"). Batch training pipeline.

**Why it was cool:**
- **Cross-agent learning** — improvements in one agent inform the next
- **Roster thinking** — treat agents as a team, not individuals
- **Batch economies** — train multiple agents in one session, amortizing context cost

**The Innovation:** Team-level skill acquisition, not individual agent islands.

**What Was Missing:**
- No integration with `/run` or `/faerie` — training happened separately from real work
- Learnings lived in `.md` cards but didn't flow into active sessions
- No way to know if trained agents actually performed better in real deployment

#### `/continual-learning` — Post-Session Integration (v2.0.0, DEPRECATED)

**What it was:** At session end, run a synthesis pass: extract learnings from agent streams, rank them by impact, decide which are "permanent" enough for HONEY, promote to agent cards, update team knowledge base.

**Why it was cool:**
- **Closed-loop feedback:** real deployment → insights → agent cards → next session
- **Anti-evaporation:** without this, insights from complex sessions would die with the session
- **Evolutionary pressure:** system improved naturally over multiple sessions
- **Memetic richness:** team knowledge deepened with each cycle

**The Innovation:** Multi-session learning as a **system property**, not a one-off training event.

**What Was Missing:**
- Lived at session boundary (expensive, context-heavy)
- No notion of **training vs. deployment** — couldn't isolate what real deployment taught vs. what training drills taught
- Ran *after* session, so couldn't affect that session's work
- Memory promotion rules were brittle (what counts as "permanent"?)

### Why They Mattered But Aren't Anymore

Together, these three skills created the first **agent feedback ecosystem.** Before them, agents were static. After them, agents could improve.

**But:** They were built as three separate things, not one unified system. Training happened separately from deployment. Learnings moved through brittle heuristics. The architecture had seams.

---

## Phase 2: The Unified Training Hub Era (2026 Q2 → NOW)

### The Architectural Insight

**The core realization:** Separating training from deployment was artificial. Real improvement happens in real work, *informed by constrained practice.*

The new model:
- **Training** (`/train`) is optional, explicit, happens when you want it
- **Deployment** (`/run`, `/faerie`) is the default
- **OTJ Learning** (on-the-job) is always on — every deployment session automatically streams insights, agents read their own `.md` cards before work, learnings accumulate in NECTAR, memory-keeper promotes to REVIEW-INBOX
- **Crystallization** (`/crystallize`) is intentional pressure-driven, not automated

### What Replaced the Three Skills

#### `/train` — Unified Training Hub (v1.0.0, ACTIVE)

**What it does:**
```
/train [--run AGENT | --prep CATEGORY | --roster CATEGORY]
```

Merged the best of all three:
- **Constraint drills** (`/train --run`) — the `/autotune` idea, now integrated into the training hub
- **Batch training** (`/train --roster`) — the `/training-roster` idea, but with real deployment context feeding back
- **Continuous integration** — training doesn't live in isolation; it reads the agent's deployment history, compares training scores to real performance, flags regressions, recommends focus areas

**Why it's better:**
1. **One command.** User doesn't need to know about autotune vs. training-roster vs. continual-learning. Just `/train`.
2. **Training-deployment equivalence.** Training runs look exactly like deployment runs (same memory protocol, same stream format, same OTJ learning). A trained agent sees no distinction.
3. **Feedback loop is automatic.** After training, `/faerie` picks up learnings in the next roundup. Real deployment follows. `session_metrics.py` compares training vs. deployment. Gaps feed back to training-queue.json.
4. **Optional, not forced.** Training is explicit; deployment happens always. But deployment *informs* training via metrics.
5. **Roster thinking is native.** `/train --prep CATEGORY` reads agent cards for the whole category, plans complementary training runs, builds roster skill maps.

**The genius move:** Training and deployment are now **two modes of the same process.** The agent runs the same code, reads the same memory, streams the same insights. Training is just deployment under artificial pressure.

### What Got Absorbed

- **Constraint drills** → `--constraint` flag in `/train --run`
- **Batch rosters** → `--roster` and `--prep` in `/train`
- **Continuous learning** → OTJ loop that runs every session automatically; `/train` lets you be explicit about it

### Why Consolidation Worked

The insight was: **training and deployment want the same infrastructure.** Once you build that unified pipeline, you don't need separate training skills. You just need `/train` as the explicit lever and `/run`/`/faerie` as the background evolution.

---

## Phase 3: The Context Roundup Era → Faerie (2025–2026)

### `/context-roundup` — Pre-Session Roundup (v1.0.0, DEPRECATED)

**What it was:** Before starting work, read all active project memories, queue state, hypotheses, recent findings. Print a brain-dump to help you orient.

**Why it was cool:**
- **Anti-disorientation.** Without it, you'd start a session lost.
- **Cross-project awareness.** Multiple investigations running? This showed what's hot in each.
- **Queue visibility.** See all pending work before choosing what to focus on.

**The Innovation:** Explicit memory handoff as a session ritual.

**What Was Missing:**
- Passive — it just printed info; didn't launch work
- Stateless — context roundup didn't know what you'd pick next
- Sequential — "read context, then decide, then launch" meant two turns minimum

### Why It's Absorbed Into `/faerie`

`/faerie` didn't replace `/context-roundup` by doing the same thing better. It replaced it by doing *more* in one turn:

1. **Read context** (what context-roundup did)
2. **Check queue** (same)
3. **Launch HIGH tasks immediately** (new — no delay)
4. **Show dashboard** (new — not just a brain-dump)
5. **Continue supporting work** (new — agents already in flight when user reads the output)

The key: `/faerie` is **action-biased.** Roundup was passive ("here's the context"). `/faerie` is active ("here's the context, and here's what's already moving").

---

## Phase 4: The Shortcut Era → Deprecated Aliases (2025–2026)

### The Aliases: `/done`, `/end`, `/new`, `/sprint`, `/investigation`

**What they were:** User-friendly shortcuts.

**Why they existed:**
- Muscle memory — users get used to typing one thing
- Domain language — `/investigation` sounds more natural than `/data-ingest` in investigation context
- Verb brevity — `/done` faster than `/handoff`

**The Problem:**
- **Cognitive overhead.** "Should I use `/done` or `/handoff`? Are they the same?"
- **Discoverability.** Looking at skill list, two commands do the same thing.
- **Maintenance burden.** Fix a bug in one, have to fix it in the alias.
- **Clarity loss.** New users see `/investigation` and `/data-ingest` and don't know which to use.

**Why they're gone:**
Not because the shortcuts were bad, but because **a clean model (one canonical command) is worth the context-switching cost.** Users get used to `/faerie`, `/handoff`, `/data-ingest` quickly. The cognitive benefit of clarity exceeds the cost of learning the "official" names.

**Alternative approach** (preserved for power users):
- Shell aliases: `alias end='faerie /handoff'`
- Don't make them first-class skills.

---

## Phase 5: Unclear/Stale Utilities → Pending Clarification

### `/swap` (Status: UNCLEAR)

**Hypothesis:** This was meant for swapping agents mid-session or swapping branches (Git side). Purpose unclear; last known use ~3 months ago. Either clarify or archive.

### `/dynamo` (Status: UNCLEAR)

No clear record of purpose. Recommend investigation before keeping.

### `/clean-gone` (Status: DEPRECATED)

Possibly for doc consolidation (cleaning "gone" i.e. deleted docs). Purpose murky; recommend removal unless active use is found.

---

## Forensic Ledger: What We Learned

### From the Training Multiplicity Era

**Lesson:** Constraint-driven improvement works. Agents *do* improve under pressure differently than in free-form deployment. But training and deployment need unified infrastructure, not separate pipelines.

**Applied to current system:** OTJ learning is always on (implicit training), `/train` is optional explicit training (constraint drills), same memory protocol and stream format for both.

---

### From the Context Roundup Era

**Lesson:** Passive information display is not enough. Users want context *and action* — the "what should I do next" question answered in the same turn.

**Applied to current system:** `/faerie` reads context *and* launches HIGH tasks immediately. Dashboard is the main interface, not a side effect.

---

### From the Shortcut/Alias Era

**Lesson:** Muscle memory is real, but clarity of model is more valuable for a system meant to be shared and maintained. One canonical name per function.

**Applied to current system:** Skills have single canonical names. Shell aliases can be added for power users without cluttering the skill namespace.

---

### From the Unified Hub Insight

**Lesson:** When two processes want the same infrastructure (training and deployment both need memory, streaming, learning, team orchestration), they should *be* the same process with different parameters, not separate systems.

**Applied to current system:** `/train` and `/run` run the same agent code with the same memory protocol. The only difference is context (artificial constraints vs. real work).

---

## Recommendation for Preservation

**Archive these skills as historical reference in:**
```
00-SHARED/Hive/SKILLS-ARCHIVE-{skill}.md
```

Each file documents:
- Original purpose
- Innovation at the time
- Why it was superseded
- Link to what replaced it
- Example usage (for archaeology)

This lets future maintainers understand *why* the current system is structured as it is.

---

## The Design Principle Underneath

**Convergence through iteration:**

Each generation of skills solved real problems. Each generation had seams and redundancies. The next generation didn't throw away the insights — it unified the infrastructure.

- Gen 1 (autotune/training-roster/continual-learning): Training exists. It's inefficient and isolated.
- Gen 2 (/train): Training and deployment unified. Same protocol, same memory, same learning loop. Training is optional, deployment is default.
- Gen 1.5 (context-roundup): Roundup exists. It's passive.
- Gen 2 (/faerie): Roundup *and* launch in one turn. Action-biased orchestration.
- Gen 1.5 (aliases): Shortcuts exist. Users get confused about canonical names.
- Gen 2: One canonical name per function. Aliases at shell level if needed.

The pattern: **merge seams, unify infrastructure, make the default case strong enough that you don't need multiple ways to do the same thing.**

---

**Status:** Final. Ready for vault publication and archive creation.
