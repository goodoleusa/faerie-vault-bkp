# TERMINOLOGY.md — Strict Definitions for faerie2 System

## Core Concept: Four Orthogonal Dimensions

The faerie2 system uses four distinct dimensions to describe work. **They are NOT interchangeable.** Each has precise boundary conditions, measurement criteria, and usage context.

---

## 1. SPRINT — Human Time Window

**Definition:**
A continuous human interaction session where a user opens Claude Code and works toward a goal.

**Boundary Conditions:**
- **Starts:** Human opens Claude Code, begins task entry
- **Ends:** Human manually runs `/end` command OR auto-compact fires (natural session conclusion)
- **Duration:** 5 minutes (quick fix) to 120+ minutes (intensive problem-solving)

**Measurement:**
- Success = user achieves their goal OR receives clear next step (no rage-quit)
- Failure = user gives up mid-sprint without actionable next step
- **Key metric:** Did the user feel their time was well-spent? (satisfaction, not just velocity)

**What SPRINT measures:**
- Human agency + satisfaction
- Alignment between user intent and agent outcomes
- Clarity of handoff (if work continues to next sprint)

**Examples:**
- "Quick sprint to fix the GLOSSARY section" (15 min) ✅
- "Investigation sprint: map treasury-cert origins" (90 min) ✅
- "User opens session, runs one command, closes" (2 min) ✅
- "User works for 40 min and still confused" (❌ negative sprint)

**Anti-Patterns — What NOT to Call a SPRINT:**
- Do NOT call W1/W2/W3 a "sprint" (that's WAVE)
- Do NOT measure SPRINT by token count (that's SESSION)
- Do NOT confuse SPRINT with "iteration" (SPRINT is time, iteration is phase)
- Do NOT say "the sprint is at 80% complete" (use SESSION % for token progress)

---

## 2. SESSION — Token Consumption Window

**Definition:**
A continuous token budget consumption cycle within Claude's inference model. One or more SPRINTs may fit within a single SESSION.

**Boundary Conditions:**
- **Starts:** Context fresh at 0 tokens (after previous auto-compact or session reset)
- **Ends:** Auto-compact fires naturally (triggered by context-fill % or time-based policy)
- **Duration:** Varies by token budget and consumption rate (~1–2 hours typical, 200K tokens)

**Measurement:**
- Token burn rate (tokens/minute)
- Artifact production (FFMx = Forensic artifacts, Findings, Manifests per token spent)
- Context fill % (tokens used / total budget)
- **Key metric:** Yield = (artifact count + manifest quality) / tokens_consumed

**What SESSION measures:**
- Model efficiency + cost-benefit
- How much work can be packed before compaction
- Quality gates per remaining-context-budget

**Examples:**
- One large sprint that fits within 150K tokens = 1 SESSION ✅
- Two small sprints in sequence, total 180K tokens = 1 SESSION ✅
- Sprint exceeds 200K tokens → auto-compact fires → 2 SESSIONs ✅
- "We completed the sprint in 40 minutes, one session" ✅

**Anti-Patterns — What NOT to Call a SESSION:**
- Do NOT conflate SESSION with SPRINT (SPRINT is user-driven; SESSION is model-driven)
- Do NOT say "SESSION took 2 hours" (use SPRINT for time)
- Do NOT call each agent spawn a separate "session" (agents run within host SESSION)
- Do NOT measure SESSION quality by "did user like it?" (that's SPRINT satisfaction)

---

## 3. WAVE — Agent Return Cycle

**Definition:**
A discrete cycle of parallel agent dispatch, execution, and manifest return. **Waves are triggered by pressure, not time.**

**Wave Types:**

### W1 — LIFTOFF (Max Burn)
- **Trigger:** Session start OR context_fill > 50% OR infrastructure work OR >3 bundles ready
- **Agents:** 4–5 parallel (burn hot, hit 5-min cache TTL)
- **Model:** haiku (cheap, fast)
- **Quality Gate:** ≥0.60 acceptable (hypothesis formation OK)
- **Duration:** ~15 minutes (wall-clock)
- **Purpose:** Max discovery, broad search, parallel routing
- **Measurement:** Count unique compass edges found; map open bearings

### W2 — CRUISE (Selective Dispatch)
- **Trigger:** W1 complete OR context_fill > 80%
- **Agents:** 2–3 sequential or lightly parallel
- **Model:** sonnet (higher quality, feature-focused)
- **Quality Gate:** ≥0.75 required (refine; don't explore)
- **Duration:** ~10 minutes (wall-clock)
- **Purpose:** Feature execution, focused work, quality consolidation
- **Measurement:** Artifact completeness; manifest truthfulness

### W3 — INSERTION (Deep Synthesis, Background)
- **Trigger:** W2 complete OR time > 20 minutes into session
- **Agents:** 1–2 async background
- **Model:** sonnet (synthesis, reflection)
- **Quality Gate:** ≥0.80 required (publish-ready)
- **Duration:** background, no wait
- **Purpose:** Cross-correlation, synthesis, deep write
- **Measurement:** Signal quality + belief_index for next bearing

**Measurement:**
- Wave completion = all agents return manifests
- Success = compass_edge valid + quality_score ≥ gate + belief_index solid
- **Key metric:** How many high-quality bearings did this wave produce?

**Examples:**
- Session start + 5 bundles ready → W1 LIFTOFF (4 scouts, 1 researcher) ✅
- W1 returns 3 manifests, context now at 75% → trigger W2 CRUISE ✅
- W2 finishes, 20 min elapsed → trigger W3 INSERTION async ✅
- One agent writes manifest with quality_score 0.92 = W2-grade bearing ✅

**Anti-Patterns — What NOT to Call a WAVE:**
- Do NOT conflate WAVE with PHASE (WAVE is agent cycle; PHASE is investigation scope)
- Do NOT say "W1, W2, W3 are the project phases" (those are SEED/DEEPEN/EXTEND/FULL)
- Do NOT trigger wave by time alone (trigger by pressure + context_fill)
- Do NOT run W2 before W1 completes (waves are sequential by design)
- Do NOT measure WAVE success by "how fast it ran" (measure by compass edges found + quality)

---

## 4. PHASE — Investigation/Project Scope (NOT Session Flow)

**Definition:**
A semantically coherent stage within a long-running investigation or project. **Phases describe investigation maturity, NOT session timing.**

**Phase Types:**

### SEED (Hypothesis Formation)
- **Quality Gate:** ≥0.50, belief ≥0.50
- **Purpose:** Frame problem, gather initial signals, form hypothesis
- **Artifacts:** Rough scoping documents, initial findings, open questions
- **Duration:** Variable (could span multiple SPRINTs or SESSIONs)
- **Success Criteria:** Hypothesis is clear; enough evidence to proceed to DEEPEN

### DEEPEN (Focused Ingest)
- **Quality Gate:** ≥0.70, belief ≥0.50
- **Purpose:** Targeted data collection, hypothesis refinement, reduce ambiguity
- **Artifacts:** Organized findings, evidence clusters, refined scope
- **Duration:** Variable
- **Success Criteria:** Evidence is strong enough for EXTEND validation

### EXTEND (Cross-Validation & Edges)
- **Quality Gate:** ≥0.80, belief ≥0.75
- **Purpose:** Validate findings against edge cases, find contradictions, strengthen confidence
- **Artifacts:** Validated datasets, edge case analyses, exception reports
- **Duration:** Variable
- **Success Criteria:** Findings survive challenge; belief_index is high

### FULL (Production-Ready)
- **Quality Gate:** ≥0.85, belief ≥0.75
- **Purpose:** Final publication, artifact polish, court-ready formatting
- **Artifacts:** Publishable reports, forensically-logged work, final manifests
- **Duration:** Variable
- **Success Criteria:** Artifact is ready for stakeholder use; COC chain is complete

**Measurement:**
- Phase progression = quality + belief gates passed
- Can skip phases if early gates already met (rare)
- **Key metric:** Has this investigation reached the maturity required for its use case?

**Examples:**
- Treasury investigation: SEED (Q1) → DEEPEN (Q2) → EXTEND (Q3) → FULL (Q4) ✅
- Quick security audit: might jump SEED → EXTEND (if initial data is strong) ✅
- Small sprint task: might stay in SEED/DEEPEN, never reach FULL ✅
- "Our findings are DEEPEN-phase; we need more edge-case validation before publication" ✅

**Anti-Patterns — What NOT to Call a PHASE:**
- Do NOT say "we're in the W2 phase" (W2 is WAVE, not phase)
- Do NOT use PHASE for session/sprint timing (PHASE is scope maturity)
- Do NOT conflate PHASE with "this investigation is 50% done" (gates are yes/no, not %)
- Do NOT skip PHASE gates (gates exist for good reason; don't bypass them)

---

## QUALITY-GATES (Auxiliary Dimension: Agent Maturity)

**Definition:**
Numeric thresholds (quality_score + belief_index) that gate work progression. **Independent of PHASE/SPRINT/SESSION/WAVE.**

**Gate Structure:**
```
quality_score: 0.0–1.0 (data/output quality: raw signal value)
belief_index:  0.0–1.0 (honesty in self-reporting: honest ≥ false confidence)
```

**Gating Logic:**
- Each PHASE has a minimum gate
- Agent writes manifest with quality_score + belief_index
- Work advances only if BOTH metrics meet gate
- **Key insight:** Honest 0.65 belief > false-confident 0.95 belief

**Measurement:**
- belief_index computed from 4 signals: truthfulness, method_confidence, uncertainty_admission, evidence_grounding
- quality_score self-assigned by agent (with explanation)
- **Audit:** manifest truthfulness = (expected outcome vs. actual outcome) / reported confidence

**Examples:**
- Agent reports: quality=0.78, belief=0.82 → gates EXTEND ✅
- Agent reports: quality=0.45, belief=0.90 (overconfident) → blocked, reframed ❌
- Agent reports: quality=0.92, belief=0.55 ("good output but I'm unsure of method") → gates DEEPEN, not EXTEND (belief too low for EXTEND)

---

## Cross-Dimensional Map: How They Interact

```
SPRINT (Human time window)
  ├─→ Contains multiple W* agents (WAVE)
  └─→ Fits within SESSION (token budget)
        ├─→ Contains W1 → W2 → W3 (sequential wave cycles)
        └─→ Measures artifact yield

PHASE (Investigation maturity)
  ├─→ Independent of SPRINT/SESSION timing
  ├─→ Gated by QUALITY-GATES (numeric thresholds)
  └─→ Progress = multiple W* cycles across multiple SPRINTs
        across multiple SESSIONs (slow accumulation)

WAVE (Agent cycle)
  ├─→ Triggered by context pressure + PHASE gates
  ├─→ Occurs within a SESSION (uses tokens)
  ├─→ Occurs during a SPRINT (human watching)
  └─→ Produces manifests that advance PHASE
```

---

## Discovery Compass Integration

**How TERMINOLOGY Connects to Compass Navigation:**

1. **Manifest Bearing (N/S/E/W)** encodes next WAVE direction:
   - **S** (South) = PHASE gate passed; proceed to next phase
   - **N** (North) = PHASE gate blocked; unblock prerequisites first
   - **E** (East) = Parallel PHASE-equivalent work discovered; batch together
   - **W** (West) = PHASE gate failed; reframe or return to HQ

2. **investigation_label** groups work across multiple SPRINTs/SESSIONs:
   - Label links semantic coherence, NOT timing
   - All tasks with label="treasury-cert-origins" advance same PHASE together

3. **quality_score + belief_index** in manifest determine if WAVE output is:
   - Good enough to gate current PHASE (continue south)
   - Too weak to advance (go north, unblock dependencies)
   - Uncertain but directional (go east, get parallel validation)

---

## FFMx — Force Multiplier Metric

**Definition:**
Artifact yield per token spent. Measures SESSION efficiency.

```
FFMx = (Manifests + Quality-Artifacts + Findings) / Tokens-Consumed
```

**Examples:**
- Session burns 150K tokens, produces 12 manifests + 3 reports + 47 forensic artifacts = high FFMx ✅
- Session burns 120K tokens, produces 2 manifests = low FFMx ❌

**Why It Matters:**
- Drives wave dispatch: high-FFMx sessions spawn more agents (W1 LIFTOFF)
- Low-FFMx sessions spawn fewer agents (W2/W3 conservative)
- Encourages artifact production over exploration

---

## Quick Reference: When to Use Each Term

| When You Want to Say... | Use This Term | Example |
|--------------------------|---------------|---------|
| "User's continuous interaction time" | SPRINT | "The 45-minute sprint was productive" |
| "Token consumption cycle" | SESSION | "We're at 75% context fill in this session" |
| "Agent dispatch round" | WAVE | "W1 LIFTOFF deployed 5 scouts in parallel" |
| "Investigation maturity level" | PHASE | "We've completed DEEPEN; ready for EXTEND" |
| "Numeric quality thresholds" | QUALITY-GATES | "This work meets EXTEND gates: quality 0.83, belief 0.79" |
| "Agent output quality" | quality_score | "Agent reports quality_score 0.92 for this manifest" |
| "Agent honesty in reporting" | belief_index | "High belief_index means agent admitted limitations" |

---

## Mutation & Emergence Application

**How Terminology Enables Rigorous Mutation Discipline:**

1. **Measure BASELINE** (before mutation):
   - FFMx per SESSION
   - PHASE gate pass-rate (what % of work reaches EXTEND/FULL?)
   - WAVE completion time (how fast do agents return?)

2. **Audit MUTATION** (classify change):
   - Does it affect SPRINT satisfaction? (human experience)
   - Does it change SESSION FFMx? (token efficiency)
   - Does it speed up WAVE cycles? (agent dispatch pressure)
   - Does it unlock earlier PHASE advancement? (investigation speed)

3. **Fix HARMFUL mutations only**:
   - Beneficial mutation: WAVE latency drops 20%, FFMx rises → KEEP
   - Harmful mutation: PHASE gates bypass, work quality plummets → FIX
   - Neutral mutation: cosmetic changes, no metric impact → TOLERATE

4. **Measure POST-FIX**:
   - Re-baseline FFMx, PHASE pass-rate, WAVE latency
   - Compare to T0 baseline (forensics/mutation-baselines/)
   - Document in manifest discovery_field

---

## Living Definition: How to Update This Document

This document is **orthogonal dimension descriptors**, not prescriptive rules. Update when:

1. **A new orthogonal dimension emerges** (e.g., "MISSION = semantic cluster of phases")
   - Add dimension definition
   - Map to existing dimensions
   - Document examples + anti-patterns

2. **A term is overloaded** (e.g., "phase" used for both PHASE and wave cycle)
   - Disambiguate with italic emphasis: *investigation phase* vs. *session phase*
   - Update all references in codebase

3. **A mutation challenges a definition** (e.g., "W2 agents are now parallel, not sequential")
   - Measure impact (does FFMx improve? do manifests get better?)
   - Update definition to reflect observed behavior
   - Document why old definition was incomplete

---

**Last Updated:** 2026-04-28  
**Status:** STRICT DEFINITIONS LOCKED (unless mutation observed + measured + published)  
**Maintained By:** faerie2 Scout (mth00101 compass navigation protocol)
