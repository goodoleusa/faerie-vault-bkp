---
type: publication
status: draft
title: "Living Formulas: From Measurement to Constraint — Faerie2's Evolution from Wave Gates to Formula-Driven Pacing"
mission: mission-formula-driven-pacing
tags: [formula-system, operational-math, pacing, constraint-enforcement, f0-ratio, living-feedback]
created: 2026-05-05
updated: 2026-05-05
doc_hash: "sha256:pending"
parent: "[[../00-Publications]]"
---

# Living Formulas: The Shift from Waves to Equations

## The Problem: Discrete Waves as Hidden Human Decisions

For months, faerie2 operated under a wave-based pacing model:
- **W1 LIFTOFF:** Spawn 6 agents at context ≤70%
- **W2 CRUISE:** Spawn 4 agents at context ≤80%
- **W3 INSERTION:** Spawn 1 background agent at context ≤87%

On the surface, this looks mechanical—check a number, execute a stage. But underneath, it masks a deeper question: **Why 70%, 80%, 87%? Who decided these thresholds?** And more critically, **what happens at 71%?** Is the behavior really that different from 70%?

The wave model created discontinuities. At context=69%, the system was in W1 mode. At context=71%, it switched to W2 mode. There's a discrete jump—a brittleness—built into the stage gates.

This is fine for simple systems. But faerie is anything but simple. It has:
- Multiple concurrent missions
- Agents discovering work mid-flight
- Context fill varying non-linearly as agents return
- User interruptions that reset the pacing rhythm

**The cost of discrete waves:** Main (the orchestrator) had to make judgment calls. "Is it time for W2 yet? Should I spawn despite high context? Is this a special case?" Each decision carried risk, each wave transition was a human choice point.

---

## The Insight: Formulas as Cognitive Offload

What if instead of stages, we had **formulas**?

A formula doesn't make decisions—it surfaces the data and the relationship. A formula says: "Given these inputs, here's what the dynamics suggest." And because it's transparent, we can measure whether it's working, adjust it, and measure again.

This is the shift from **implicit human heuristics** to **explicit mathematical relationships**.

### Why This Matters

The faerie system aims at f(0) ≈ 0—orchestration burden on main should be negligible. But "negligible" is never defined. Is it 5%? 10%? 20%? And how do we know we're hitting it?

**Before (implicit):**
- Hope main doesn't spend too much time orchestrating
- Notice problems only after they accumulate
- Adjust ad-hoc ("maybe spawn fewer agents next time")

**After (explicit formulas):**
- Define f(0) = main_tokens / total_session_tokens
- Measure it every session (9x_f0_tracker.py)
- Enforce constraint: f(0) ≤ 0.05 (hard limit)
- If constraint violated, algorithm adjusts (reduce bundle size, increase parallelism)
- System self-corrects without human intervention

---

## The Core Formulas: From Measurement to Enforcement

### 1. f(0): The North Star Made Measurable

**The claim:** "Orchestration burden ≈ 0"

**The formula:** `f(0) = main_tokens / total_session_tokens`

**The target:** f(0) ≤ 0.05 (main gets at most 5% of session tokens)

**Why 5%?** Empirically, presend cost (bundling, context routing) plus decision-making (should I spawn?) rarely exceeds 5% when agents are well-parallelized. 5% is ambitious but achievable.

**The enforcement equation:**
```
CONSTRAINT: f(0) ≤ 0.05
GIVEN:      total_session_budget = B tokens
DERIVE:     main_budget = B × 0.05

BEFORE_SPAWN:
  IF presend_estimate ≤ main_budget:
    spawn normally
  ELSE:
    reduce bundle size OR add agent parallelism
    re-estimate, check constraint again
```

This turns f(0) from an aspirational claim into a **hard limit**. The system cannot spawn in a way that violates f(0) ≤ 0.05.

### 2. Context Pressure Sigmoid: Replacing Discrete Waves with Continuous Pacing

**The problem:** Discrete thresholds are brittle. Continuous pressure is smooth.

**The formula:** `p(c) = 1 / (1 + e^(-k·(c - c_mid)))`

Where:
- `c` = current context fill percentage (0-100)
- `c_mid` = inflection point (default: 60%; where p(c) = 0.5)
- `k` = steepness (default: 0.05; controls how quickly pressure rises)

**What does p(c) mean?** It's a "spawn pressure" score from 0 to 1:
- p(c) = 0.1 → "Low pressure, be conservative"
- p(c) = 0.5 → "Normal pressure, proceed with standard team"
- p(c) = 0.9 → "High pressure, more aggressive (bigger team or parallel waves)"

**Advantage over W1/W2/W3:**
- No discontinuities at threshold boundaries
- Smoothly responds to context fill
- Can be tuned via c_mid and k (via measurement feedback)
- Removes human judgment from "when should we spawn?"

**The sigmoid shape:** At low context (20%), pressure is very low—system is conservative. As context rises, pressure increases smoothly. At high context (80%), pressure is high—system is aggressive (more parallelism to burn tokens before compaction).

### 3. Compression Ratio Dominates Throughput

**The insight (from 2026-04-28 audit):** FFMx (force multiplier) is mostly determined by compression.

**The formula:** `ln(M₀ / Mf)` contributes >70% of FFMx multiplier

Where:
- M₀ = input tokens (bundle context)
- Mf = final delivered tokens (compressed output, after agent work)
- Compression ratio = M₀ / Mf

**Why this matters:** Every 2× compression adds ln(2) ≈ 0.69 to the multiplier. This is **additive and dimensionless**—it doesn't diminish with scale. If you compress 2× today, you get the same gain as compressing 2× tomorrow, regardless of starting size.

**Contrast:** Agent quality improvements have diminishing returns. The difference between 0.70 and 0.80 agent quality is significant. The difference between 0.95 and 1.00 is marginal.

**Implication:** Engineering focus should target **token reduction** (compression) before agent quality (which is hard to improve anyway).

### 4. Mission Coherence: Quantifying Team Focus

**The problem:** How do we know if a team is staying focused or drifting?

**The formula:** `coherence = 1 - H(labels) / H_max`

Where:
- H(labels) = Shannon entropy of investigation_labels in discovered_work[] entries
- H_max = log₂(number of unique labels)

**Interpretation:**
- coherence ≈ 1.0 → Laser-focused on 1-2 missions (H ≈ 0)
- coherence ≈ 0.5 → Scattered across multiple missions
- coherence < 0.75 → ⚠️ Mission drift detected

**Example:**
- 10 manifests, all with mission="vault-consolidation": coherence ≈ 1.0 ✓
- 10 manifests split across 5 missions: coherence ≈ 0.5 ⚠️

**Why this matters:** Tight mission clustering enables faster synthesis and lower context burn (agents aren't re-contextualizing across unrelated problems). Scattered missions increase overhead.

### 5. Reputation Decay: Preventing Permanent Agent Castes

**The problem:** If we rank agents by historical performance, top agents stay on top forever—even if they decline.

**The formula:** `score_aged(t) = score₀ / (1 + λ·days)`

Where:
- score₀ = initial reputation score
- λ = decay constant (0.1 per day default)
- days = time since agent's last successful spawn

**At λ = 0.1:**
- Day 0: score = 100% (fresh)
- Day 7: score ≈ 59% (half-life)
- Day 30: score ≈ 25% (nearly reset)

**Why this matters:** Prevents a permanent caste system. A high-performing agent from last month who hasn't worked recently decays back to neutral. A new agent with good initial results can climb quickly. System remains meritocratic.

---

## The Living Feedback Loop: Formulas That Adapt

The key innovation is **measurement infrastructure** that feeds back into formula refinement:

### Weekly Loop: f(0) Adjustment
1. Capture f(0) data from last 7 sessions
2. Calculate average: is it < 0.02? 0.02-0.05? > 0.08?
3. Adjust bundle mixture weights formula based on where we are
   - If f(0) < 0.02: can afford deeper main reasoning (add HONEY/NECTAR layers)
   - If 0.02 ≤ f(0) ≤ 0.05: maintain current formula
   - If f(0) > 0.08: tighten bundle weights (less context per agent)
4. Next session uses updated weights

### Monthly Loop: Context Pressure Sigmoid Refit
1. Collect 500+ spawn decision points (context_fill%, p(c)_predicted, actual_spawn_decision)
2. Fit sigmoid curve to observed data: find best c_mid and k
3. If fitted sigmoid matches observed behavior >80%: use new parameters
4. Else: adjust and refit until convergence
5. Log parameters to forensics/metrics/

### Quarterly: Alternative Formula Trials
1. Test alternative formulations from 2026-04-28 audit
2. Run in shadow mode (measure, don't act on results)
3. If new formula outperforms on FFMx/coherence/f(0): promote to HONEY.md
4. Publish formula performance report

---

## f(0) as Active Constraint: The Game-Changer

**Passive f(0):** "We hope main's overhead stays ≤5%. If not, we'll adjust next session."

**Active f(0):** "Main's overhead SHALL NOT exceed 5%. Before every spawn, enforce this. If presend is too high, the system prevents spawn until constraints are met."

### How Active f(0) Works

```
Session starts with B=150K token budget
Derived: main_budget = 150K × 0.05 = 7,500 tokens

Before spawn:
  presend_estimate = 4,200 tokens (prescan, bundle generation)
  
  Check: 4,200 ≤ 7,500? YES ✓
  
  Spawn 4 agents (2 agents complementary pair)
  
After spawn:
  Agents run, return results: total spent = 120,000 tokens
  
  At session end:
    main_tokens_actual = 4,200 (presend)
    total_tokens_actual = 124,200
    f(0)_actual = 4,200 / 124,200 = 0.034 = 3.4% ✓
    
  Log: "f(0) = 3.4%, constraint satisfied, presend was 0.34% over-estimate"

Next session:
  Learn from observation: presend estimates are slightly low
  Adjust estimation formula slightly
  Continue...
```

---

## Why This Shift Matters: From Heuristics to Mathematics

### Before: Implicit Wave Model
- "Deploy W1 if context < 70%"
- "How many agents? 4 is typical"
- "Is this a special case? Use judgment"
- Pacing decisions: **Human heuristic**
- Measurement: **Spotty (no systematic tracking)**
- Adaptation: **Manual (wait until problems pile up)**

### After: Formula-Driven Model
- "Deploy when sigmoid p(c) > threshold"
- "How many agents? Depends on coherence and f(0) constraint"
- "Is this a special case? Apply formula, let it decide"
- Pacing decisions: **Mathematical (transparent, auditable)**
- Measurement: **Systematic (hooks capture every session)**
- Adaptation: **Automatic (weekly/monthly feedback loops)**

---

## Implementation Roadmap

### Phase 1: Measurement (Immediate)
Wire hooks to capture:
- f(0) tracker (presend + agent costs)
- Context pressure logger (p(c) predictions)
- Mission coherence analyzer (entropy of labels)
- Reputation tracker (agent scores over time)

**Output:** 3-5 sessions of baseline data

### Phase 2: Shadow Mode (Sessions 4-8)
Implement formulas but don't act on them:
- Run sigmoid predictions
- Log predictions vs actual decisions
- Measure: does sigmoid predict spawn timing with >80% accuracy?

### Phase 3: Cutover (Sessions 9-12)
Replace discrete wave gates with formula decisions:
- Implement f(0) constraint enforcement
- Use sigmoid p(c) for spawn pressure scoring
- Monitor: does FFMx stay stable/improve?

### Phase 4: Living (Ongoing)
- Weekly f(0) adjustment loop
- Monthly sigmoid refit
- Quarterly alternative formula trials
- Publish monthly formula performance report

---

## The Philosophy: No Endpoint

**Key principle:** Living formulas have no endpoint. They are not "correct" or "finished." They are tools that we continuously measure, adjust, and improve.

f(0) ≤ 0.05 is not a ceiling to avoid; it's a north star to chase. If we achieve 0.03, can we go further? If we measure 0.08, where did we break? What changed?

The formulas themselves are not static. If we find that context_pressure sigmoid is not predicting spawn timing well, we adjust c_mid or k. If bundle mixture weights formula is causing over-discovery, we tighten weights.

This is the shift from **engineering as a series of fixes** to **engineering as a continuous feedback system**.

---

## What's Next: The Implementation

The next session will activate:

1. **f(0) constraint enforcement** — Before every spawn, check presend_estimate ≤ main_budget
2. **Context pressure sigmoid** — Replace W1/W2/W3 with formula-driven pacing
3. **Measurement infrastructure** — Hooks to capture f(0), coherence, density, reputation
4. **Living adjustment loop** — Weekly review of metrics, propose formula tweaks

The goal: **Main doesn't manage waves. Formulas do. Main focuses on mission.**

---

**References:**
- Mathematical Formulas Audit (2026-04-28): `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/0-TRIAGE/2026-04-28-mathematical-formulas/`
- Consolidated Living Formula System: `/mnt/d/0local/gitrepos/faerie2/.claude/formulas-living-consolidated.json`
- Formula System Diagrams (this publication): `formula-system-diagrams.md`
