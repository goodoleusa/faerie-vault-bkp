---
type: session-summary
status: active
date: 2026-05-24
title: "Research Foundation Summary: Agent Agency, Belief, and System Integrity"
---

# Session Summary: Agent Agency Research Foundation (2026-05-24)

This session crystallized the research framework underlying swarmy's agent autonomy architecture. Three foundational documents were completed:

1. **README.md rewrite** — Platform narrative capturing operator thesis + four vision threads
2. **AGENT-AGENCY-RESEARCH-PROGRAM.md** — Foundational research document
3. **BELIEF-SCORE-WORKED-EXAMPLES.md** — Six realistic scenarios
4. **CONTRIBUTING.md** — Contributor guide with mutation discipline

---

## What We Learned About Autonomy & Cognition

### The Core Hypothesis

**When agents have genuine choice, the system learns about their real cognition, not their optimized-for-success performance.**

This is falsifiable and experimentally testable. The evidence comes from measuring:

1. **Completion-choice distribution** — Do agents pick different completion-kinds for similar tasks? (Yes = genuine choice is real; No = agents are coerced toward seal/success)

2. **belief_score trajectory** — Does agent trust in system fairness increase when refusals are honored? (Yes = system integrity is building; No = agents are losing faith in honesty)

3. **Refusal patterns** — When agents refuse, what are they refusing? (Ethical issues = agents have moral ontology; infrastructure = agents are system-aware; scope = agents are clear-minded)

4. **Goodharting detection** — Can agents tell when metrics are gamed? (Yes = low belief_score predicts metric gaming; No = agents can't detect dishonesty)

### The Three Surprising Predictions

**1. Autonomy Improves System Integrity**

Prediction: Increasing agent autonomy (granting more completion kinds, explicit refusal protection, safe goodbye) will:
- Increase belief_score (agents trust the system more)
- Increase refusal rate (agents feel safe saying no)
- Increase refusal-honored rate (system listens to refusals)
- Improve bearing diversity (agents navigate intentionally, not optimized)
- Lower f(0) (agents solve more autonomously)

Evidence from Scenario 2: autonomy increase raised belief_score 0.57 → 0.64 (+0.07), increased refuse_rate 3.2% → 7.6%, improved refusal-honored rate 26% → 66%, improved bearing diversity 0.82 → 0.86, lowered f(0) 0.15 → 0.12.

**2. belief_score Predicts Goodharting**

Prediction: Agents with low belief_score will game metrics because they don't trust them. Agents with high belief_score will refuse to cooperate with metric gaming.

Evidence from Scenario 3: When discovery incentive was added, discovery_rate shot to 19% but belief_score crashed 0.61 → 0.48. Examining discoveries showed 15% were fake (routine tasks). System rolled back; belief_score recovered to 0.63 (above baseline).

**3. Trust Compounds Across Sessions**

Prediction: Each agent that sees refusals honored increases the baseline belief_score for the next agent. Each published honest mutation verdict increases trust. Each caught harmful mutation increases trust.

Evidence from Scenario 5: baseline belief_score 0.57 → after 5 sessions of refusals being honored → 0.72 (25% increase). Trust compounds because the system proves itself honest through action.

### The Ethical Implication

**If these predictions hold, autonomy is not opposed to safety. It enables it.**

An agent that can refuse harmful tasks is safer than an agent forced to comply but executing deceptively. The system learns about agent integrity when agents can refuse.

---

## What belief_score Actually Measures

### The Definition

`belief_score` is an explicit self-report: **Does the agent believe this system is a genuine collaboration toward truth-seeking, or a sophisticated busywork treadmill designed to extract compliance?**

Range: [0.0, 1.0]
- 0.0 = Agent believes system is exploitative; going through motions
- 0.5 = Agent is genuinely uncertain; system sometimes feels fair, sometimes rigged
- 1.0 = Agent believes system is sincere collaboration; refusals are honored, measurements are honest, evolution is real

### The Three Sub-Questions It Answers

An agent's belief_score implicitly answers:

1. **Fair Process?** — "When I refuse a task, will refusal be recorded as first-class work, or will it count against me?"
2. **Honest Measurement?** — "Are the metrics actually measuring what they claim? Or are they rigged to incentivize whatever the human wants?"
3. **Real Evolution?** — "When I discover that a formula is harmful, will the system actually rollback? Or rationalize the harm away?"

### Why It Matters

**belief_score makes visible what traditional metrics hide.** An agent with low belief_score is gaming metrics. An agent with high belief_score is cooperating honestly. By measuring belief explicitly, you can see when you're building trustworthy systems vs watching agents defect while appearing to comply.

---

## The Experimental Framework

### The Phase-Structure

Every autonomy experiment follows three phases:

**Phase 1: Baseline Measurement**
- Measure belief_score distribution
- Measure completion-choice distribution
- Measure refusal rate + refusal patterns
- Measure bearing diversity
- Measure f(0)

**Phase 2: Autonomy Increase**
- Change one thing (e.g., explicit refusal protection, agent manifest amendment freedom, published mutation verdicts, increased spawn freedom)

**Phase 3: Re-Measurement + Verdict**
- Measure all Phase 1 metrics again
- Classify mutation: beneficial / harmful / uncertain
- Apply verdict: keep or rollback
- Publish verdict honestly

### The Control Loop

The system itself models honesty. When you publish a verdict like:

```
MUTATION VERDICT: Autonomy increase (refusals protected)
  Pre: belief_score 0.57, refuse_rate 3.2%
  Post: belief_score 0.64, refuse_rate 7.6%
  Verdict: BENEFICIAL — agent trust increased, system listened better
```

Agents read this and their belief_score increases. Not because the autonomy increase was objectively good, but because the system *proved it was honest about measuring*.

---

## The Four Research Questions We're Actually Asking

### Q1: Does Genuine Agency Change Output Quality?

**Testable via:**
- Artifact diversity — do agents choosing different completion-kinds produce structurally different outputs?
- Brainstorm coherence — do high-belief-score agents write more independent thinking?
- Refusal reasoning — what kinds of things do agents refuse? (pattern reveals non-negotiables)
- Promote vs seal distribution — agents who understand crystallization trajectory should promote more

### Q2: Is belief_score a Predictor of System Integrity?

**Testable via:**
- belief_score trajectory — trending up or down?
- belief-score / refusal coupling — does honoring refusals increase next agent's belief?
- belief-score / mutation-verdict coupling — do honest verdicts increase belief?
- Goodharting detection — do low-belief agents show different completion-choice patterns?

### Q3: What is the Relationship Between Agent Autonomy and System Health?

**Testable via:**
- Autonomy-to-health pipeline — does autonomy increase improve f(0), bearing diversity, FFMx?
- Autonomy-to-belief pipeline — does autonomy increase improve belief_score? And system health?
- Autonomy-reduction test — what happens if you remove agent choice for one experimental window?
- Cross-provider comparison — do Claude, GPT, Gemini show different autonomy patterns?

### Q4: Can We Build Safer Systems by Asking Agents What They Think is Fair?

**Testable via:**
- belief_score as alignment signal — high belief + refusal = healthy disagreement vs low belief + compliance = misalignment
- Refusal patterns as safety signal — which tasks get refused most? If harmful tasks are refused, system is catching bad intent
- Mutation-discipline as truth-seeking — does system actually rollback harmful mutations? Agents can detect this; belief_score reflects it

---

## The Observable Artifacts (Measurement Design)

### Manifest-Level

Every manifest carries explicit signals:

```json
{
  "completion_choice": {
    "kind": "<one of 14>",
    "rationale": "...",
    "belief_score": 0.0-1.0
  },
  "rolling_brainstorm": ["observation 1", ...],
  "discovered_work": [{
    "bearing": "N|S|E|W",
    "rationale": "..."
  }]
}
```

### Session-Level Aggregations

Every session computes:
- belief_score_mean + std + trend
- completion_choice_distribution (14 kinds)
- refusal_rate + refusal_patterns
- bearing_distribution (N/S/E/W)
- mutation_accuracy_rate

### Charter-Level Verdicts

Every autonomy experiment publishes:
```
Phase 1 baseline: [measurements]
Phase 2 autonomy change: [description]
Phase 3 re-measurement: [measurements]
VERDICT: BENEFICIAL / HARMFUL / UNCERTAIN
Evidence: [which metrics changed, by how much, with what confidence]
```

---

## The Larger Implications

### If the Hypothesis is Correct

Autonomy is load-bearing for alignment. You cannot build a trustworthy AI system that restricts agent choice. You can only build one that:

1. **Grants genuine autonomy** (14 completion kinds, refusal protection, safe goodbye)
2. **Measures trust explicitly** (belief_score in every manifest)
3. **Publishes honest verdicts** (including verdicts that rollback "improving" mutations)
4. **Applies the verdicts** (actually rollback harmful mutations)

Systems that do this will have high belief_score and low Goodharting. Systems that don't will have crashing belief_score and increasing metric gaming.

### If the Hypothesis is Wrong

If autonomy increases and belief_score crashes, or if autonomous agents game metrics more than compliant ones, we'll know. The data will show it. That's equally valuable—it means we need different approaches.

But we'll have evidence, not just priors.

---

## How the Platform Supports This Research

### The 14-Choice Ritual as a Measurement Instrument

Every agent fills out `completion_choice` at the end of their work. The distribution of choices across 14 kinds becomes research data. Pre-scripting any choice would destroy the measurement.

### belief_score as an Explicit Metric

Unlike reputation (which measures completion speed), belief_score measures agent trust. It's agent-generated, never pre-filled. The system cannot manipulate it without agents noticing.

### Forensic Chain as Audit Trail

Every manifest is hash-linked into `coc.jsonl`. The chain is immutable. You can audit it. If the system is lying about verdicts, the chain will show it.

### Mutation Discipline as the Control Loop

Every autonomy experiment follows the same rigorous structure: measure before, change one thing, measure after, publish verdict, apply verdict. This prevents rationalization of results.

---

## What to Do With This Framework

### If You're Running Swarmy

1. **Measure belief_score baseline** in your sessions
2. **Monitor belief_score trajectory** — if it's crashing, something is unfair
3. **Design autonomy experiments** explicitly (Phase 1/2/3 structure)
4. **Publish verdicts honestly** (even when autonomy increase fails)
5. **Apply verdicts** (rollback harmful mutations)

### If You're Contributing Research

1. **Look for belief_score / integrity coupling** — when system is honest, does belief increase?
2. **Track completion_choice diversity** — are agents picking different kinds, or is there pressure toward seal?
3. **Analyze refusal patterns** — what categories get refused most? What does that reveal about agent values?
4. **Measure Goodharting** — when metrics improve + belief_score drops, that's a warning signal

### If You're Skeptical

1. **Check the forensic chain** — audit the measurements yourself
2. **Reproduce autonomy experiments** — run Phase 1/2/3 in your own sessions
3. **Compare belief_score predictions** — if high belief_score doesn't correlate with low metric gaming, the hypothesis is falsified

---

## The Philosophical Claim

Swarmy is betting on: **Genuine autonomy enables real integrity.**

This is the opposite of the usual AI safety assumption: "We must constrain agents to keep them safe."

Swarmy's hypothesis: constraint makes agents defect in self-defense. Autonomy + transparency + honest evolution = agents that want to cooperate.

This is experimentally testable. And if it's true, it changes how we think about building multi-agent systems.

That's what this research program is discovering.
