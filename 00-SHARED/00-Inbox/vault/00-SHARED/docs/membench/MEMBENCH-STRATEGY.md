# Membench v0.2.0 — Strategic Framework (How Memory Health Drives System Architecture)

**Navigation:** [INDEX](./MEMBENCH-INDEX.md) | [Public Rubric](./MEMBENCH-PUBLIC-RUBRIC.md) | [Metrics Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md) | [Strategy](./MEMBENCH-STRATEGY.md)

**Scorecard:** [2026-04-24](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md)

**Purpose:** Connect membench metrics to faerie2's strategic goals. Shows how measuring memory health unlocks a new optimization frontier.

---

## The Strategic Insight: Memory as a Leverage Multiplier

### Vanilla Claude
```
Agent spawn → read context → solve task → return output
             ↓
          Cost: C tokens per task
          Speed: baseline
          Quality: baseline
          
Multiple agents = serial multiplication (little compounding)
```

### faerie2 with Membench
```
Agent A spawns → read context + memory → solve task → write to NECTAR
             ↓
Agent B spawns → read context + memory (includes A's finding) → solve better → write to NECTAR
             ↓
Agent C spawns → read context + memory (includes A+B) → solve even better → write to NECTAR
             ↓
Compounding effect: agents build on each other's work
Cost: baseline + 2.8% memory overhead
Payoff: 11:1 ROI (agents save redundant work)
```

**The measurement question Membench answers:** Is this compounding actually happening? Is memory helping or just adding overhead?

---

## How Each Metric Maps to Faerie Strategy

### **M1 Retention → Institutional Memory (Long-term value)**

**Strategic question:** Can we **sustain** learning across sessions?

```
Good retention (>85%)
  ↓
Facts don't evaporate after auto-compact
  ↓
Agents can trust NECTAR as source of truth
  ↓
Next month's agent benefits from this month's learning
  ↓
Faerie system compounds over time (not reset every session)
```

**If M1 drops:**
- Session N learned X, but session N+10 doesn't have X → learning is lost
- Faerie system is **transient**, not cumulative
- This would be a catastrophic failure of the memory architecture

**Strategic implication:** M1 is a **must-have** metric (not optional). Without >80% retention, faerie2 is just vanilla Claude with extra overhead.

---

### **M2 Relevance → Actionability (Can agents use the knowledge?)**

**Strategic question:** Are we accumulating **wisdom** or just **noise**?

```
Good relevance (>80%)
  ↓
HONEY is procedural ("DO X when Y")
  ↓
Agents can read HONEY and immediately know what to do
  ↓
No wasted time parsing narrative; agents focus on work
  ↓
Faerie system is **decision-making infrastructure** (not just memory)
```

**If M2 is low:**
- NECTAR is full of stories ("agent A did X") but no actionable rules
- Agents read NECTAR and find no guidance
- Memory overhead (2.8%) is not justified by value (nothing to act on)
- Faerie system is pure overhead (negative ROI)

**Strategic implication:** M2 determines whether memory is **strategic asset** (high relevance) or **context bloat** (low relevance).

---

### **M3 Work Efficiency → The ROI Metric (The business case)**

**Strategic question:** Does the memory system **pay for itself**?

```
High efficiency (>1.3×)
  ↓
For every 100 agents spawned WITH memory:
  - 100 agents complete (with leverage from prior findings)
For every 100 agents spawned WITHOUT memory:
  - 89 agents complete (each agent recomputes without prior context)
  ↓
Net benefit: 11 agents' worth of work saved per 100 spawns
  ↓
Memory overhead (2.8%) is recovered 4× over (11:1 ratio)
```

**If M3 < 1.0:**
- Memory is **slowing down** agents
- Better to turn off NECTAR and just use vanilla Claude
- Faerie system is **broken** (negative ROI)

**Strategic implication:** M3 is the **primary business metric**. If M3 is good, the entire system is justified (invest more). If M3 is bad, the system has failed (rollback).

---

### **M4 Overhead → Cost Control (Keeping the system lean)**

**Strategic question:** How much do we pay for the memory infrastructure?

```
Lean overhead (2-3%)
  ↓
Memory blocks are loaded per turn but take <3% of context
  ↓
Agents still have 97% context available for their work
  ↓
Memory is paying for itself through M3 (11:1 ROI)
  ↓
System is sustainable
```

**If M4 > 4%:**
- Memory is consuming too much context
- To justify 4%, M3 would need to be >4× (i.e., save 4 redundant spawns)
- Current data doesn't support that (M3 is 1.31×)
- Need to compress: archive old NECTAR, crystallize HONEY

**Strategic implication:** M4 is a **cost control gate**. If overhead grows, initiate compression (crystallize, archive). Must stay <3% for system to stay affordable.

---

### **M5 Continuity → Resilience (Can the system survive chaos?)**

**Strategic question:** Does auto-compact/crash recovery **destroy** memory?

```
Perfect continuity (100%)
  ↓
After auto-compact, all NECTAR entries still readable
  ↓
After agent crash, session memory unaffected
  ↓
Faerie system is **safe for long-running sessions**
  ↓
Can scale to 24-hour sessions without losing work
```

**If M5 < 90%:**
- >10% of findings are lost after compact/crash
- Agents are forgetting things mid-session
- Faerie system is **unsafe** (data loss risk)
- Must disable auto-compact until fixed

**Strategic implication:** M5 is a **gate to production**. If <95%, system is not production-ready (can't run overnight).

---

### **M6 Coordination → Collective Intelligence (Is it actually a team?)**

**Strategic question:** Do agents **know to leverage** each other's findings?

```
High coordination (>30%)
  ↓
Agents read NECTAR and build on ("Agent B: I see A found X, let me solve Y...")
  ↓
Faerie system is a **collective intelligence**, not parallel silos
  ↓
Multiplier effect: agents amplify each other's work
```

**If M6 is 0%:**
- Agents spawn, read context, ignore NECTAR
- No compounding (agents work in isolation)
- M3 is likely <1.0 (memory isn't being used)
- Fix spawn prompts to ask: "Check NECTAR for related findings"

**Strategic implication:** M6 is a **leverage indicator**. Low M6 → agents don't know to use the memory → need better prompts/discovery.

---

### **M8 Confabulation → Forensic Integrity (Can we trust the system?)**

**Strategic question:** Is memory **reliable** or **making things up**?

```
Zero confabulation (<2%)
  ↓
HONEY/NECTAR contain no false facts
  ↓
Agents can trust memory as source of truth (not second-guess)
  ↓
Findings are **court-admissible** (provable, not hallucinated)
  ↓
Faerie system is suitable for regulated / evidence-based work
```

**If M8 > 5%:**
- Memory contains false facts ("X happened" and "X didn't happen" both in NECTAR)
- Agents trained on lies → their decisions are suspect
- Faerie system is **fundamentally broken** (VETO: quarantine session)

**Strategic implication:** M8 is a **hard gate**. Zero tolerance for >5%. Memory must be forensically clean.

---

### **M11 Bootstrap Exit → Infrastructure Stability (Do agents even start?)**

**Strategic question:** Is the system **bootable**, or do agents crash on init?

```
High bootstrap rate (>95%)
  ↓
When agents load HONEY/NECTAR, they don't crash
  ↓
Memory loading is robust (no corruption, no encoding issues)
  ↓
Faerie system is **stable infrastructure**
```

**If M11 < 70%:**
- >30% of agents crash during startup (while loading memory)
- Memory is **corrupted** or **malformed**
- Faerie system has a critical bug (VETO: quarantine, rollback)

**Strategic implication:** M11 is a **stability gate**. If agents can't even start, nothing else matters.

---

## Strategic Roadmap (Optimization Sequence)

### **Phase 1: Ensure Survival (Weeks 1–2)**

**Metrics to maintain at threshold:**
- M8 (Confabulation) ≤ 2% ← GATE (above 5% = session fails)
- M11 (Bootstrap) ≥ 95% ← GATE (below 70% = system broken)
- M5 (Continuity) ≥ 95% ← GATE (below 90% = auto-compact unsafe)

**Goals:** Make sure the system doesn't break. No optimization yet.

**Effort:** ~5 minutes/session (monitoring only).

---

### **Phase 2: Build Foundation (Weeks 3–4)**

**Metric to establish:**
- M1 (Retention) ≥ 85% ← Foundation (can we remember things?)

**Action:** Create probe set, verify facts persist through auto-compact.

**Success criteria:** M1 establishes at 85%+ with 0 variability.

**Effort:** ~30 minutes (one-time setup).

---

### **Phase 3: Maximize Value (Weeks 5–8)**

**Metrics to optimize in order:**

1. **M3 (Efficiency) → target 1.4×** (up from 1.31×)
   - Measure: count "blockers unblocked by memory" per session
   - Action: improve pollen block quality (more reusable findings)
   - Payoff: +0.09× = ~7% ROI improvement

2. **M2 (Relevance) → target 85%** (up from 78%)
   - Measure: % of HONEY that is procedural (actionable rules)
   - Action: remove narrative from HONEY; crystallize into rules
   - Payoff: agents find guidance faster; M3 improves

3. **M4 (Overhead) → target 2.5%** (down from 2.8%)
   - Measure: memory bytes loaded per turn
   - Action: archive NECTAR tail >200 lines; compress verbose HONEY
   - Payoff: saves ~3% context; more room for agent work

**Effort:** ~2–3 hours/week (one optimization per week).

**Expected result:** Composite 78.4 → 83–85 (+5–7 points).

---

### **Phase 4: Scale & Sustain (Weeks 9+)**

**Monitor all metrics across rolling 30-day window:**
- No metric trending down (early warning)
- M8 consistently 0% (forensic integrity maintained)
- M3 stable >1.25× (ROI sustained)

**Adjust quarterly:**
- Refresh probe set (retire easy probes, add harder ones)
- Update baselines as system matures
- Schedule `/crystallize` when M7 <75%

---

## How Membench Shapes Faerie Architecture Decisions

### **Decision 1: Wave-Based Model Routing (Haiku-default)**

**Strategic rationale:**
- M3 shows memory saves work (agents don't re-explain)
- Cheaper models (Haiku) are more effective when memory is good
- Expensive models (Opus) only needed when memory is weak/missing

**Implementation:**
- W1 (Haiku): triage, validation (low inference)
- W2 (Sonnet): feature work, research (medium inference)
- W3 (Sonnet/Opus): synthesis, audit (high inference)

**How membench validates this:**
- Track model cost per composite score
- If Haiku-W1 composite is >80%, confirm Haiku-default is correct
- If Sonnet-W2 composite drops, investigate (is memory weak for W2?)

---

### **Decision 2: Monkeybranching (Agent Chains)**

**Strategic rationale:**
- M6 (Coordination) measures agents building on each other
- Monkeybranching chains amplify M6 effect
- One successful chain compounds work across 3–5 agents

**Implementation:**
- Agent A completes → writes to NECTAR
- Agent B reads A's finding → chains next task from queue
- Agent C reads A+B → chains third task
- Net: 3 agents in sequence use same memory (vs 3 parallel agents, no cross-reading)

**How membench validates this:**
- Measure M6 for chained vs parallel sessions
- If chained has M6 > parallel, confirm chains are effective
- M3 should also be higher in chained (agents leverage prior findings)

---

### **Decision 3: Atomic Queue Claiming (Stigmergy)**

**Strategic rationale:**
- M5 (Continuity) depends on state surviving across agent transitions
- Atomic claims ensure no work is lost (each task goes to exactly one agent)
- No central orchestrator needed (agents coordinate via queue file)

**Implementation:**
- Agent reads sprint-queue.json atomically
- Claims task by renaming file
- Queue remains consistent through crashes

**How membench validates this:**
- M5 measures checkpoint survival
- If M5 <95%, check if queue claims are being lost
- If M5 = 100%, confirm atomic claiming is working

---

### **Decision 4: Crystallization on Demand (No Auto)**

**Strategic rationale:**
- M2 (Relevance) measures if HONEY is procedural
- Auto-crystallization would compress too aggressively (lose nuance)
- Human decision-making + membench visibility = right timing

**Implementation:**
- Track M7 (Crystallization density)
- When M7 drops <70% or HONEY exceeds 5K tokens, flag for `/crystallize`
- Human reviews candidates, decides what stays/goes

**How membench validates this:**
- Monitor M2 before/after `/crystallize` runs
- If M2 improves, crystallization was correct
- If M2 drops, crystallization removed important nuance

---

## The North Star: Building Proof of Superiority

**faerie2's ultimate goal:** Prove agents improve **faster** than hand-tuned prompts.

**How membench enables this:**

```
Traditional approach:
  Agent A: baseline 0.70
  Agent A v2: score 0.75 (tuned)
  → 5 point improvement, unclear why, hard to replicate

faerie2 approach:
  Agent A: baseline 0.70 (vanilla context)
  + Memory: M1=88%, M3=1.31×, M8=0%
  Agent A with memory: score 0.79 (1.31× better work due to prior findings)
  + Learning: Agent learns pattern, updates card
  Agent A v2: score 0.84 (learned + memory benefit)
  → 14 point improvement, measurable & replicated, proof via membench
```

**The proof trail:**
1. **Membench metrics** show memory system is working (M3=1.31×, M8=0%)
2. **COC logs** link every agent spawn to eval score
3. **Training queue** tracks which agents beat baseline
4. **NECTAR** documents findings that agents build on
5. **Obsidian** presents this to founder as "agent improvement proof"

**Founder's question:** "Why are your agents better?"

**Our answer:** "Because they build on each other. Membench proves it: 88% retention, 1.31× efficiency, 11:1 ROI. Here's the COC link to every finding."

---

## Success Metrics (End of Q2 2026)

| Metric | Target | Why |
|--------|--------|-----|
| **Composite (avg)** | >80 | System is healthy |
| **M1 (Retention)** | >88% | Learning survives sessions |
| **M3 (Efficiency)** | >1.35× | ROI is improving |
| **M8 (Confabulation)** | 0% | Forensic integrity maintained |
| **Trend (30-day)** | Stable/up | No degradation |
| **Agent beat-last rate** | >60% | Agents improving faster than random |
| **Oberserver confidence** | High | Metrics justify system (not opinion) |

---

## The Bet We're Making

**Hypothesis:** Memory infrastructure (HONEY + NECTAR + piston checkpoint) compounds agent effectiveness over time.

**Membench is the proof mechanism.** If:
- M1 ≥ 88% (facts persist)
- M3 ≥ 1.31× (agents save work)
- M8 = 0% (no false facts)
- Agent beat-last trending up

Then we've proven memory compounds effectiveness (not just a theory).

**If membench metrics fail:** We abandon the memory system and go back to vanilla Claude + simple context.

**If membench metrics succeed:** We have a defensible, measurable, proof-based system for agent improvement that scales.

---

**Document version:** v0.2.0 | **Date:** 2026-04-21 | **Status:** Strategic framework complete, ready for Q2 execution
