---
type: reference
status: active
created: 2026-04-21
tags: [business, novelty, competitive-analysis]
up: README.md
prev: SURVIVAL_LAUNCH_PLAN.md
---

> [↑ Readme](README.md) · [← Survival Launch Plan](SURVIVAL_LAUNCH_PLAN.md) · [⌂ Home](../../README.md)

# faerie — Novelty Assessment

> What's truly new here vs. what builds on known art.

---

## The Core Differentiator: Work Memory, Not User Memory

Every AI memory product remembers things **about the user** — their name, preferences,
past conversations. faerie is different: it remembers the user's **work** and **process**.

| What competitors remember | What faerie remembers |
|--------------------------|----------------------|
| User preferences, name, style | Investigation state, entity relationships, dead ends |
| Past conversation topics | What was tried, what failed, what to try next |
| User's role and context | Active hypotheses, confidence scores, hot leads |
| How to talk to this user | How to **work** — which agent configs produce better results |

**Why this matters:** The user's biggest cognitive tax isn't "AI doesn't know my name."
It's context-switching, re-explaining background, retrying dead ends, and losing
momentum when the system breaks flow. faerie eliminates these **speed bumps**:

- **Context switching** → SEED loads full investigation context in <2K tokens
- **Re-explaining background** → HONEY already has it; agent is briefed before it starts
- **Retrying dead ends** → Dead-end map prevents duplicate work across sessions
- **Breaking flow** → Flow detection goes quiet, auto-approves, extends commit window
- **Boring work** → faerie handles crystallization, memory promotion, queue management
- **Missing connections** → Cross-investigation entity matching surfaces relevant findings

**The result:** faerie takes the boring, repetitive, flow-breaking work and handles it
silently. What's left for the user is the fun stuff — following leads, making connections,
having insights.

**Process memory is the second axis.** faerie doesn't just remember the work — it
remembers how to do the work better. Agent configs that produce higher I/F ratios get
promoted. Crystallization patterns that preserve more knowledge get refined. The system's
*process* improves through continual-learning, not just its *knowledge*.

---

## Crystallization vs Summarization

| Property | LLM Summarization | Mem0/Zep Accumulation | **faerie Crystallization** |
|----------|------------------|----------------------|--------------------------|
| **Source** | Single document | All past interactions (growing) | All existing durable entries |
| **Gate** | None | None | Merge-check: already known? Supersedes? Implied? |
| **Result** | Shorter version of A | A + new facts (grows forever) | Denser truth — same knowledge, fewer tokens |
| **Budget enforcement** | No | No | Hard token ceiling — file **cannot** grow past budget |
| **Confidence integration** | No | No | High-confidence cross-thread facts upgrade entry status |
| **Over time** | N/A | Memory grows → API costs rise | Memory densifies → API costs fall |
| **Failure mode** | Loses edge cases | Bloat, retrieval noise | Rejects redundancy before it enters |

**The geological metaphor:** Salt crystals form only from saturation — impure inputs don't form crystal lattice. Existing crystals restructure when new compatible material bonds. faerie's HONEY works the same way: every write is a phase transition, not an accumulation.

---

## Full Novelty Table

| Feature | What exists | What's novel | Evidence of gap |
|---------|-------------|--------------|-----------------|
| **Prompt transformation (not augmentation)** | Mem0/Zep/Letta all *append* memory to the original prompt | faerie *rewrites* the user's prompt using HONEY — original question is replaced, not supplemented | No memory product currently transforms the input prompt |
| **Hard memory token budget** | All products let memory grow indefinitely | faerie enforces a hard ceiling per file — system physically cannot exceed it | Mem0/Zep roadmaps have no token budget concept |
| **Merge-before-write gate** | Products store new facts by appending or overwriting | faerie checks: already known? supersedes? implied? — rejects before writing | No known product treats the memory store as an append-reject system |
| **Crystallization as first-class operation** | Recursive summarization in MemGPT (closest prior art) | MemGPT compresses the *conversation window*; faerie crystallizes the *knowledge artifact* itself | Different scope, different artifact, different protocol |
| **Crystallization + cross-thread confidence boost** | No prior art | High-confidence facts from related investigation threads can promote a crystallized entry's status | Novel combination |
| **Insight-to-Friction (I/F) ratio as product metric** | NPS, DAU, engagement metrics | Measures ratio of "click moments" to friction points — continuous signal from every session | Not named or formalized in any product or research |
| **Forensic reasoning log (cross-session, cross-project)** | Per-session transcripts, per-project context | ONE append-only `.jsonl` per investigation, spanning any number of sessions/projects/agents, with chain-of-custody for data transforms | OSINT/investigation tools have no AI-native forensic reasoning record |
| **SEED — generated at dispatch, not stored** | Context files read at session start (growing overhead) | SEED is generated fresh at task-claim time from HONEY — agents receive a <2K token custom-compiled brief, never read files | No known system compiles a task-specific bootstrap context at dispatch time |
| **Salience tags on memory entries** | Plain metadata (date, source) | SURPRISE, VISCERAL, DREAD, INTUITION, PERIPHERAL, CONFIRMATION — affect retrieval priority and flow detection | Emotional salience as retrieval signal not found in any memory system |
| **VOID layer (expected-but-absent signals)** | Memory records what happened | VOID records what was expected but *didn't* happen — negative space as first-class investigation data | Novel in AI memory; exists in human intelligence tradecraft (absence of signal as signal) |
| **Flow state detection and quiet-mode** | No AI tool does this | Infers flow from LOG signal density (SURPRISE rate, I/F, turn cadence) → reduces friction, extends auto-approve, dims UI | No AI tool currently detects user flow state and adapts behavior |
| **Proactive pain routing (no user action)** | User must report problems | Detects PAIN patterns → silently routes, expands SEED, queues fix tasks | Current AI tools wait for user to describe the problem |
| **Failure as first-class contribution** | Failed tasks are retried silently or dropped | Failing agent writes structured handoff: what I tried, dead ends, high-value leads not yet tried — this *feeds* the next agent's SEED | Failure handoff that maximizes value for successor not found in any agent framework |
| **Investigation DAG with heat scoring** | Task queues (linear, priority-based) | Tasks are graph nodes with `heat = confidence × recency × spawn_rate × cross_hive_interest` — hot leads auto-elevate, dead ends propagate to hive | Dynamic heat formula for investigation leads not found in task management or AI agent frameworks |
| **Bayesian confidence with independence check** | Sources cited or counted | Independence is the signal — 3 independent sources → conf ~0.89; derivative sources only add +0.05; contradicting source cuts by 45% | Bayesian memory updating with independence premium not in any current AI memory product |
| **Reconsolidation with cooling period** | Memory updated on new evidence | 3 updates in 48h → cooling period: new evidence queued for human review, not auto-applied — prevents confirmation bias spiral | Reconsolidation cooling inspired by human memory research; not implemented in AI systems |
| **State as reconstructible hypothesis (not fact)** | Memory stores facts | STATE is an agent's *working model* — versioned, allowed to be wrong, reconstructed by reading fresh evidence against prior assumptions | Treating agent state as hypothesis rather than ground truth is novel |
| **Federation (4-layer: LOCAL/HIVE/FEDERATION/SWARM)** | Cloud sync (Notion, Obsidian) or single-machine | Fully offline-capable federation via dead-drop messaging (Syncthing/git/IPFS) — hives communicate without real-time connection | Offline-first federated AI memory not in any current product |
| **Hive splitting (like biological swarms)** | Team accounts are fixed | A hive can split: child inherits global HONEY + methods, starts fresh on project HONEY — investigation continues in both | Organizational splitting as a first-class operation not in any AI tool |
| **Dead-end sharing across hives** | Each investigation is siloed | Dead ends propagate to federation — 3+ hives independently marking same entity → convergence signal | Collective intelligence via negative result sharing not in current tools |
| **ASSUMPTION_VIOLATION as special LOG category** | Contradictions logged generically | When new evidence contradicts a prior STATE assumption → auto-bump STATE version, immediate FLAG, optional federation broadcast | Structured assumption violation tracking not found in AI reasoning systems |
| **Semantic prompt compression using personal knowledge** | LLMLingua compresses context generically | faerie compresses the *user's specific query* using *their accumulated HONEY* — the compression is personalized, not generic | Combining personal memory with input prompt compression: novel per competitive research |
| **Zero memory tax — "always on"** | Memory must be invoked or managed | Background processes: SEED freshness, entity matching, HONEY crystallization, pain aggregation — user never thinks about memory | The goal (not the mechanism) — no current product achieves true zero-management memory |

---

## Honest Novelty Summary

**Known art (not novel, build on top of):**
- Prompt compression techniques (LLMLingua, ACON)
- LLM memory injection (Mem0, Zep, Letta)
- RAG-based context retrieval
- Recursive summarization (MemGPT)
- OSINT investigation tools (Maltego, Palantir)

**Novel combinations (not done together, but pieces exist):**
- Prompt compression + personal memory injection in a single pre-API transformation step
- Bayesian confidence + memory retrieval priority
- Forensic audit trail + AI reasoning (investigation tools have one or the other, not both)

**Genuinely novel (not in current literature or products):**
- Crystallization law: merge-before-write + hard token budget + density-over-time
- I/F ratio as primary AI product metric
- SEED generated at dispatch time from HONEY
- VOID layer: absent-signals as first-class data
- Flow state detection → adaptive AI behavior
- Investigation DAG with heat formula
- Failure handoff protocol as value contribution (not just retry)
- Reconsolidation cooling (prevents confirmation bias in AI reasoning)
- Offline-first federated hive architecture with splitting
- Zero memory tax as design north star
