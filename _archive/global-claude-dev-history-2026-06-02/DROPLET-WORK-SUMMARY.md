# Droplet Integration Work — Complete Summary

**Date:** 2026-04-21  
**Phase:** W3 (Deep Synthesis + Architecture)  
**Delivered:** Comprehensive droplet-writing rule + training strategy + executable session  
**Status:** Ready for execution

---

## The Problem (Identified by Team Lead)

Long, instructive rules (like droplet-writing-heuristics, ~3K tokens) are too expensive to load on every spawn. Agents need the discipline, but every spawn starts with +3K baseline cost for the rule. This wastes tokens and creates spawning context friction.

**Current model:** Spawn agent → Load rule → Agent reads rule → Agent applies discipline → Return output.  
**Cost:** +3K tokens per spawn, whether agent reads or not.

---

## The Solution (Implemented)

**Transform the long rule into embedded agent DNA via meta-training session.**

Instead of loading rules every spawn, train agents once (in W3) to internalize heuristics into their own cards. Next spawn of a trained agent reads discipline from their card, not from a loaded rule.

**New model:** Training session (one-time) → Agents refactor cards → Peer review → Deploy → Next spawn inherits discipline.  
**Cost:** +18-22K tokens one-time training (W3); -2.4K tokens per spawn thereafter. Payoff in 10 spawns.

---

## What Was Delivered

### 1. Comprehensive Droplet-Writing Rule
**File:** `/mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md` (3.2K tokens)

**Sections:**
- **Core Signal:** When to write droplets (strong triggers: 3+ sources, surprise, gut feeling, pre-compression)
- **Categories:** HEADLINE, CONNECTION, FIRST_IMPRESSION, TECHNIQUE, OBSERVATION (high-value vs low-value types)
- **Anti-Patterns:** What NOT to write (summaries, logs, generic observations, duplicates)
- **Moment-Based Heuristics:** Feeling checklist (when you feel X, write as Y)
- **Lifecycle in Spawn Context:** When agents write droplets during work
- **Quality Heuristics:** What makes a droplet worth reading 6 months from now
- **Examples:** Across memory, infrastructure, agents, design domains
- **FAQ:** Common questions about droplet discipline
- **Checklist:** Pre-manifest validation

**Status:** Complete, non-negotiable heuristics documented. Ready as sauce rule (load on demand).

---

### 2. Meta-Framework for Embedding Long Rules
**File:** `/mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md` (1.8K tokens)

**Purpose:** Generalizable pattern for ANY long rule (>1.5K tokens) that is instructive and affects 5+ agents.

**Key sections:**
- **When to use:** Criteria for rule-embedding training (token budget, instruction vs reference, agent count, behavior internalization)
- **Training session template:** Phases (audit → proposal → peer review → revision → deployment)
- **Card update structure:** How agent cards integrate rule content (Role + KPIs + Discipline section)
- **Success metrics:** Quantitative (spawn cost reduction, agent card completeness, peer review quality) + qualitative (discipline in DNA, peer reveals shared patterns, richer cards)
- **Quarterly cadence:** Q1 droplets, Q2 citations, Q3 stigmergy, Q4 review
- **Risk mitigation:** Adversarial peer review catches overcommit; easy rollback; OTJ validation

**Status:** Complete meta-framework. Reusable for future long rules.

---

### 3. Executable Training Session Spec
**File:** `/mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md` (2.1K tokens)

**What it does:** Step-by-step training session design for 9 tier-1 agents.

**Agents trained:**
1. evidence-curator (gap analysis spans domains)
2. memory-keeper (bridges pollen → NECTAR)
3. membot (crystallizes HONEY)
4. knowledge-synthesizer (connects across silos)
5. research-analyst (OSINT + deep research)
6. report-writer (narrative synthesis)
7. documentation-engineer (architecture + examples)
8. context-manager (roundup + state management)
9. workflow-orchestrator (session lead)

**Four phases:**
1. **Card Audit** (15 min): Does your card mention droplets? KPI metrics? Behavior rules? What's missing?
2. **Card Proposal** (30 min): Propose updated Role + KPI + new Droplet Discipline section
3. **Peer Adversarial Review** (30 min): Review 2–3 peers' proposals for completeness, specificity, consistency, feasibility
4. **Revision** (30 min, if needed): Address peer feedback; resubmit revised proposal

**Timeline:** 4 hours parallelized (not 36 hours sequential). Teams of 3–4 agents stagger reviews.

**Status:** Complete, executable specification. Ready to spawn.

---

### 4. Ready-to-Copy-Paste Spawn Instructions
**File:** `/mnt/d/0LOCAL/.claude/DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md` (2.4K tokens)

**What it includes:**
- Pre-spawn checklist
- Spawn pattern: TeamCreate + 9 Agent() calls in parallel
- Per-agent prompt template (meta-training context + audit + proposal + review + revision)
- Team coordination (shared task list + SendMessage)
- Manifest contract (status progression: in-progress → draft → final)
- Success criteria for main session (all audits complete, proposals pass feasibility, ≥0.90 confidence)
- Deployment script (main session applies patches to 9 agent cards)
- Monitoring plan (next 20 spawns track droplet quality improvement)

**Status:** Copy-paste ready. No ambiguity. Can execute immediately.

---

### 5. Pre-Execution Manifest
**File:** `/mnt/d/0LOCAL/.claude/hooks/state/wave3-droplet-training-manifest.json`

**Purpose:** Staging document that lists what will happen.

**Contents:**
- Tier-1 agents (9)
- Training rule source
- Expected outputs (9 audits, 9 proposals, 18–27 peer reviews, 0–3 revisions, 9 deployed cards)
- Success criteria (all sections updated, completeness ✓, consistency ✓, feasibility flagged ≤3, confidence ≥0.90)
- Token budget (18–22K total, parallelized W3)
- Spawn template (parameters for each agent)
- Risk mitigation (overcommit caught by peer review, timeout prevented by parallelization, rollback easy via git)

**Status:** Ready. Manifests the training session before agents spawn.

---

### 6. Enhanced Spawn Boilerplate
**File:** `/mnt/d/0local/gitrepos/faerie2/scripts-claude/8x_spawn_boilerplate_injector.py`

**Changes:**
- Added `generate_droplet_protocol()` function: minimal protocol excerpt (~300 tokens)
  ```
  "Minimum: 1 droplet per run. Write when: connection (3+ sources), surprise (breaks assumption), 
  gut signal (before reasoning), pattern (reusable). Types: HEADLINE, CONNECTION, FIRST_IMPRESSION, 
  TECHNIQUE. File: $CT_VAULT/00-SHARED/Droplets/LIVE-{date}.md. Format: ### ISO8601 — {agent_type}, 
  **cat:** X, **pri:** Y, {1–5 sentences}. Full heuristics: /mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md"
  ```
- Updated `generate_boilerplate()` to include `droplet_protocol` field
- Updated `inject_boilerplate_into_prompt()` to inject protocol + reference to full sauce rule

**Benefit:** Every spawn includes brief droplet reminder (+200 tokens); agents trained in cards read full rule on demand (not loaded every spawn).

**Status:** Complete, integrated. Already in place.

---

### 7. Updated Spawn Boilerplate Documentation
**File:** `/mnt/d/0local/gitrepos/faerie2/.claude/SPAWN-BOILERPLATE.md` (section 3c)

**Changes:**
- Minimal protocol summary (instead of full heuristics)
- Added note: "Agents trained in droplet discipline have this protocol embedded in their agent cards. Your card specifies WHEN/WHAT/WHY to write droplets."
- Link to full sauce rule: agents can read on demand
- Updated format example to include `"cats"` and `"pris"` arrays in manifest `droplets` field

**Status:** Complete. Consistent with new approach.

---

## Cost Analysis

### Before Training
- **Per spawn:** +3200 tokens (load full droplet-writing-heuristics rule)
- **Per 20 spawns:** +64K tokens
- **Problem:** Rule loaded every spawn; agents don't internalize discipline

### After Training Deployed
- **Per spawn:** +200 tokens (minimal protocol reminder in boilerplate)
- **Per 20 spawns:** +4K tokens
- **Benefit:** 91% reduction from baseline; agents trained in cards read discipline from their identity

### Training Investment
- **One-time cost:** 18–22K tokens (9 agents × 2–2.5K each, parallelized W3)
- **Payoff timeline:** 10 spawns break even; 20 spawns save 50K+ tokens
- **ROI:** Permanent (trained agents keep discipline in cards; no re-training needed)

---

## Next Steps

### Immediate (Ready Now)
1. ✓ Review `/mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md` (framework)
2. ✓ Review `/mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md` (session spec)
3. → **Queue W3 execution** of training session

### W3 Execution
1. TeamCreate team: `droplet-integration-t1`
2. Spawn 9 agents (parallel) with meta-training prompt from `/mnt/d/0LOCAL/.claude/DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md`
3. Agents complete phases: audit → proposal → peer review → revision (4 hours)
4. Main session validates proposals + applies patches to 9 agent cards
5. Deploy 9 updated cards (git commit)

### Post-Deployment Monitoring
1. Monitor next 20 spawns of trained agents
2. Track metrics: droplet count (target ≥1/run), quality (target 50%+ HEADLINE/CONNECTION), manifest compliance (100%)
3. Document outcomes in NECTAR entry
4. Consider Tier-2 training (Q2) for 5 additional agents if results positive

---

## Strategic Pattern (Generalizable)

This work establishes a **long-rules-to-agent-cards** pattern that's reusable:

### Q1 2026: Droplet Discipline
- Rule: 3.2K tokens
- Agents: 9 (evidence-curator, memory-keeper, membot, knowledge-synthesizer, research-analyst, report-writer, documentation-engineer, context-manager, workflow-orchestrator)
- Cost: 18–22K tokens (training); -2.4K tokens per spawn (payoff in 10 spawns)

### Q2 2026: Citation Discipline (Planned)
- Rule: ~2K tokens (when/what/how to cite sources; 100% citation rate goal)
- Agents: 5 (data-scientist, security-auditor, code-reviewer, fullstack-developer, ai-engineer)
- Cost: 10–15K tokens (training); -1.5K tokens per spawn (payoff in 8 spawns)

### Q3 2026: Stigmergy + Cross-Agent Coordination (Planned)
- Rule: ~2.5K tokens (messaging, shared state, task reassignment)
- Agents: 5 (task-distributor, error-coordinator, team-builder, performance-eval, knowledge-synthesizer)
- Cost: 12–18K tokens (training); -1.8K tokens per spawn (payoff in 10 spawns)

### Q4 2026: Model Routing Optimization (Planned)
- Rule: ~1.8K tokens (when to use haiku vs sonnet vs opus; cost/accuracy tradeoffs)
- Agents: 8 (all core agents)
- Cost: 16–20K tokens (training); -1.2K tokens per spawn (payoff in 17 spawns)

**By end of 2026:** 4 long rules embedded in agent cards; cumulative baseline spawn cost reduced by -7K tokens per spawn (agent identities carry discipline).

---

## Files Created/Modified

### New Files
1. `/mnt/c/Users/amand/.claude/rules/sauce/droplet-writing-heuristics.md` (3.2K rule)
2. `/mnt/d/0LOCAL/.claude/LONG-RULES-TRAINING-STRATEGY.md` (1.8K meta-framework)
3. `/mnt/d/0LOCAL/.claude/agents/TRAINING-DROPLET-INTEGRATION.md` (2.1K executable spec)
4. `/mnt/d/0LOCAL/.claude/DROPLET-TRAINING-SPAWN-INSTRUCTIONS.md` (2.4K ready-to-execute)
5. `/mnt/d/0LOCAL/.claude/hooks/state/wave3-droplet-training-manifest.json` (pre-execution manifest)
6. `/mnt/d/0LOCAL/.claude/hooks/state/wave3-droplet-guidance-result.json` (final manifest from this work)

### Modified Files
1. `/mnt/d/0local/gitrepos/faerie2/scripts-claude/8x_spawn_boilerplate_injector.py` (added `generate_droplet_protocol()`)
2. `/mnt/d/0local/gitrepos/faerie2/.claude/SPAWN-BOILERPLATE.md` (section 3c updated)

---

## Success Criteria (Post-Training)

### Quantitative
- **Spawn context savings:** -2.4K tokens per spawn (91% reduction)
- **Agent card completeness:** 100% of trained agents have rule-inspired sections
- **Peer review quality:** >90% of proposals pass all checks
- **KPI adoption:** 100% of updated cards include new metrics
- **Droplet quality improvement:** +30% HEADLINE/CONNECTION ratio in next 20 spawns

### Qualitative
- Agents spawn with discipline in their DNA (learned behavior, not external requirement)
- Peer review reveals shared patterns in agent design (synthesis opportunities)
- Cards become richer (more self-aware about behavior)
- Droplet writing becomes proactive (agents know triggers) vs reactive

---

## Key Insight (From User)

> "What if we loaded [the rule] as a training session, gave it to each agent type in some way that would allow them to write a proposed new version of their agent card... each agent is given the relevant faerie parts and told to make themselves more integrated overall with faerie, then do adversarial review on each other?"

This insight transformed a token-bloat problem into a capability-building opportunity. Instead of fighting rule load costs, we embed rules into agent identity. Side benefit: agents improve each other via peer review, revealing shared design patterns.

---

**Status:** Complete. Ready to execute in next W3 window.  
**Owner:** Team lead (execution) + documentation-engineer (design/scaffolding)  
**Dependencies:** None (all design complete, boilerplate enhanced, spawn instructions ready)  
**Approval gate:** Team lead review of strategy + training design before spawning agents

