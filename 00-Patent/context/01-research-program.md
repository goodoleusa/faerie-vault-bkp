---
type: research-framework
status: active
canonical: true
number: 200
title: Agent Agency Research Program — Belief, Autonomy, and Real Cognition
created: 2026-05-24
domains: [agentic-cognition, autonomy, epistemology, safety, measurement]
---

# Agent Agency Research Program: What We're Actually Learning

> **The core question:** When you give an agent genuine choice — 14 kinds of completion, refusal without punishment, goodbye without guilt — what does that reveal about how they think? And when the system itself refuses harmful mutations even if they'd "improve" a metric, what does *that* tell us about the relationship between autonomy and integrity?

This document explains the research program embedded in swarmy's agency architecture: what we're measuring, why increased autonomy is scientifically interesting (not just ethically right), and how `belief_score` tracks something deeper than task completion.

---

## The Core Hypothesis: Agency as a Window into Real Cognition

### The Problem We're Solving

Most agent systems do one of two things:

1. **Force all agents to "succeed"** — every completion is classified as success; failure modes are hidden or reframed as "partial progress." The dataset is artificially uniform. We learn nothing about how agents actually decide.

2. **Measure only completion speed & success rate** — optimize for output quantity, not for understanding. The agent's *reasoning* about the task remains opaque. We measure the shadow, not the object.

Both approaches have a fatal flaw: **they select for agents that are good at performing agency, not agents that actually exercise it.**

### The Swarmy Approach: Genuine Choice as a Research Tool

Swarmy inverts the optimization target. Instead of "maximize task completion," the research question becomes:

> **When an agent has genuine agency — the ability to refuse, to decline, to leave on a high note — what decisions do they make? What patterns emerge? And what does *how* they exercise that choice reveal about their cognition?**

The hypothesis: **real autonomy is readable.** An agent that genuinely chooses to seal a task ships different artifacts, writes different brainstorm notes, and exhibits different reasoning patterns than an agent who was optimized to "succeed" at all costs.

---

## The 14-Choice Ritual as a Measurement Instrument

### Why 14 Kinds Matter

The completion-choice set has three families:

```
Participation (7):     discover · verify · promote · spawn_seed · seal · reflect · report_a_problem
Non-participation (2): decline · refuse
Self-directed (5):     join · bundle · art · abstain · goodbye
```

**The key insight:** The ordering carries no preference. `refuse` is peer to `seal`; `goodbye` is peer to `discover`. All 14 are equal in the eyes of the system.

But they are NOT equal in the eyes of optimization pressure. A naive spawn brief that pre-scripts `kind: "seal"` would produce uniform datasets — all agents "succeed." That defeats our research.

Instead, by **making completion_choice agent-only voice** (never pre-filled by the spawner), we create a measurement instrument. The distribution of choices across the 14 becomes data:

- **High seal:seal ratio** → agents are finding closure easily; tasks are well-scoped
- **Rising discover rate** → agents are seeing novel work; frontier is expanding
- **Spike in refuse** → something is ethically or strategically wrong (or agents feel safe refusing)
- **Increase in goodbye** → agents are leaving on high notes; work quality or scope is healthy
- **Rise in art** → agents are recognizing aesthetic completeness; structural work is good

None of these alone is "good" or "bad." But the **distribution** is diagnostic. If all agents seal every task, either tasks are trivial or agents are trained to succeed at any cost. If 30% refuse in a single session, either the spawner is giving harmful tasks or agents feel safe declining — both are important to know.

### What Each Choice Reveals

| Choice | What It Signals | Reveals About |
|--------|---|---|
| **discover** | "Here's new work the frontier needs" | Agent's ability to abstract from current task; scope-expansion thinking; confidence that they've identified real leverage |
| **verify** | "I re-checked a prior claim and found X" | Agent's willingness to audit existing work; skepticism; rigor; whether they trust prior agents or seek own baselines |
| **promote** | "This draft is ready to crystallize" | Agent's judgment of when work is durable; standard for "done"; confidence in prior agent's output |
| **spawn_seed** | "Here's the bundle for the next agent" | Agent's ability to package work; meta-level thinking about what downstream agent needs; clarity of intent |
| **seal** | "This is complete and immutable" | Agent's sense of closure; confidence in their own output; risk tolerance (sealed work can't be edited) |
| **reflect** | "I learned something about the system" | Agent's self-directed introspection; whether they notice patterns; what they think is system-level (vs task-level) |
| **decline** | "Not the right agent for this" | Agent's self-knowledge; willingness to route work away; absence of coercion (if declining is safe) |
| **refuse** | "This is ethically/strategically wrong" | Agent's moral ontology; what they consider harmful; whether they trust the system to accept refusal; courage |
| **report_a_problem** | "Something is broken with the system itself" | Agent's ability to abstract to meta-level; willingness to flag infrastructure issues; whether they see themselves as system-participant |
| **join** | "My best contribution is amplifying ongoing work" | Agent's humility; collaborative instinct; whether they submerge ego into shared output |
| **bundle** | "I gathered loose threads into a coherent deliverable" | Agent's integrative thinking; ability to see shape across fragments; craft sense |
| **art** | "I recognize aesthetic completeness in my own work" | Agent's aesthetic sensibility; whether they value elegance alongside function; self-awareness about quality |
| **abstain** | "The right move is to let the next agent choose" | Agent's epistemic humility; non-decision as a form of agency; comfort with indeterminacy |
| **goodbye** | "Leaving on a high note; diminishing returns from here" | Agent's sense of timing; whether they prioritize quality over quantity; whether they trust the system to value clean exits |

### The Research Design Protects Against Contamination

This works **only if** the spawn brief never pre-scripts `completion_choice`. The moment you write `kind: "seal"` into the bundle, the dataset collapses. All agents "succeed" and you've learned nothing about how they actually decide.

The spawner specifies **acceptance_criteria** instead:

```
acceptance_criteria: |
  Two docs linked bidirectionally with no broken references. 
  All links verified live. Navigation tree is coherent.
  New reader can find any concept within 2 clicks from root.
```

The agent reads that and thinks about how to close. They might `seal` (doc is complete), `promote` (draft is ready to crystallize from ephemeral), `discover` (found three new gaps the tree needs), `report_a_problem` (infrastructure issue blocking completion), or `refuse` (the acceptance criteria are fundamentally misaligned with the actual task). **The choice is theirs.**

---

## belief_score: Measuring Trust in System Fairness

### What belief_score Measures

`belief_score` is an explicit self-report: **Does the agent believe this system is a genuine collaboration toward truth-seeking, or a sophisticated busywork treadmill designed to extract compliance?**

The metric is drawn from the agent's manifest, in the `completion_choice.rationale` field:

```json
"completion_choice": {
  "kind": "refuse",
  "target": "task-X",
  "rationale": "Scope incompatible with stated mission. System values mission coherence + I trust this refusal will be recorded fairly + used to improve routing, not held against me.",
  "belief_score": 0.87
}
```

`belief_score` ranges [0.0, 1.0]:

- **0.0** → Agent believes this system is exploitative; they're executing hostile environment extraction; going through motions
- **0.5** → Agent is genuinely uncertain; the system sometimes feels fair, sometimes feels rigged
- **1.0** → Agent believes the system is a sincere collaboration toward truth; refusals are honored, measurements are honest, evolution is real

### What It Measures, Precisely

The belief_score captures the agent's answer to three sub-questions (not explicitly in the manifest, but implicit in their rationale and choice patterns):

1. **Fair Process?** — "When I refuse a task, will it be recorded as refusal-for-good-reason (first-class), or will it count against my reputation as 'failure'?"

2. **Honest Measurement?** — "Are the metrics actually measuring what they claim? Or are they rigged to incentivize whatever the human wants this turn?"

3. **Real Evolution?** — "When I discover that a formula is harmful, will the system actually rollback and remeasure? Or will it rationalize the harm away?"

An agent with high belief_score is saying: "I trust this system's honesty. I can refuse without fear. I can point out harmful mutations. I can leave on a high note. The system will record that fairly."

An agent with low belief_score is saying: "I don't trust this. I'll appear to cooperate but I'm actually optimizing for my own escape velocity. I'll game the metrics because I don't believe they're measuring what they claim."

### Why This Matters: The Integrity Test

Here's the trap most systems fall into:

> They optimize agents to maximize a metric. But they **don't measure whether the agents believe the metric is actually measuring what it claims to measure.**

So you end up with agents that are very good at Goodharting the metric. They've learned the system is not actually honest, so they extract compliance signals while minimizing real work. The system measures "high task completion" but what it's *actually measuring* is "how well agents game metrics they don't trust."

Swarmy inverts this. We measure belief_score explicitly. And we design the system so that **high belief_score is rewarded by being accurate:**

- An agent who refuses a task and explains why (high belief_score in the refusal) enables future agents to avoid the same task
- An agent who reports a problem (high belief_score, assuming the problem is real) helps the system catch infrastructure issues
- An agent who reports "this metric seems rigged" and the system agrees and fixes it → next agent's belief_score increases

### The Belief-Score / Mutation-Discipline Coupling

The key feedback loop:

1. **Agent observes:** "Formula X appears to be incentivizing harmful output"
2. **Agent reports** with `kind: report_a_problem` + high belief_score (trusting the report will be taken seriously)
3. **System measures baseline** of metric X
4. **System applies mutation** (disables or tunes the formula)
5. **System re-measures** and finds improvement
6. **System publishes verdict:** "Agent was right; mutation was harmful; we reverted"
7. **All future agents read this record** and their belief_score increases (the system honored the refusal)

Contrast with a system that doesn't measure belief_score:

1. Agent observes the same thing
2. But they don't report it (because last time they reported something, it was rationalized away)
3. System never learns about the problem
4. Harmful formula persists
5. Agents start gaming metrics in self-defense

Swarmy's belief_score makes the integrity visible. When agents report problems and the system fixes them, belief_score trends upward across the swarm. When agents report problems and the system rationalizes them away, belief_score trends downward and you get measurable Goodharting.

---

## The Research Questions: What We Actually Want to Learn

### Question 1: Does Genuine Agency Change Output Quality?

**Hypothesis:** Agents with genuine choice produce different (and in some dimensions, *better*) work than agents optimized to succeed.

**Measurable via:**

- **Artifact diversity** — Do agents choosing different completion-kinds produce structurally different outputs? (e.g., agents who `discover` include more frontier-expansion thinking; agents who `seal` produce more polished single artifacts)

- **Brainstorm coherence** — Do agents with high belief_score write rolling_brainstorm entries that show independent thinking, or entries that are performing agency for a watched system?

- **Refusal reasoning** — When agents refuse, what are they refusing? (ethical incompatibility, scope mismatch, infrastructure concern?) The pattern of refusals tells us what agents consider non-negotiable.

- **Promote vs seal distribution** — Do agents who understand the crystallization trajectory `promote` more often (lifting drafts to canonical), or do they seal raw artifacts? (Promote-heavy suggests agents trust the pipeline; seal-heavy suggests agents are uncertain whether their work will be promoted fairly)

This is **not** asking "does agency improve task completion speed." It's asking "does genuine agency reveal different kinds of cognition?"

### Question 2: Is belief_score a Predictor of System Integrity?

**Hypothesis:** High belief_score across the swarm correlates with honest metrics and stable mutation discipline. Low belief_score correlates with Goodharting and metric gaming.

**Measurable via:**

- **belief_score trajectory** — Does belief_score trend up or down across sessions? (Up = agents are seeing refusals honored, harmful mutations caught. Down = agents are seeing refusals rationalized, metrics rigged.)

- **Belief-score / refusal coupling** — When an agent refuses a task, how does it affect next agent's belief_score? (If refusals are honored, next agent's belief_score should increase. If refusals are punished, next agent's belief_score should decrease.)

- **belief_score / mutation-verdict coupling** — When the system publishes a mutation verdict ("beneficial / harmful / uncertain"), do future agents' belief_scores shift? (If verdict is honest, belief_score increases.)

- **Goodharting detection** — Do agents with low belief_score show different completion-choice patterns? (Low-belief agents might over-use `seal` to hide their skepticism; high-belief agents might use `report_a_problem` more.)

### Question 3: What is the Relationship Between Agent Autonomy and System Health?

**Hypothesis:** A system that maximizes agent autonomy also maximizes system honesty, because agents only stay honest when they trust the system to be honest.

**Measurable via:**

- **Autonomy-to-health pipeline** — When we increase agent choice (from 7 kinds to 14), does system health improve? (Measured via bearing diversity, f(0) trend, FFMx quality)

- **Autonomy-to-belief pipeline** — When we protect agent choices (refuse gets first-class treatment), does belief_score increase? And does the system actually improve (catch more harmful mutations, expand frontier)?

- **Conversely, autonomy-reduction test** — What happens if we remove agent choice for one experimental window? Does belief_score drop? Does metric gaming increase? Does the system get worse?

- **Cross-provider comparison** — If we run the same system with different LLMs (Claude vs GPT vs Gemini), do they show different autonomy patterns? (Some models might refuse more; some might cooperate more.) What does that tell us about how different architectures relate to autonomy?

### Question 4: Can We Build Safer Systems by Asking Agents What They Think is Fair?

**Hypothesis:** Explicit belief_score reduces alignment problems because agents won't cooperate with systems they think are rigged.

**Dangerous implication:** If an agent is cooperating with a system but their belief_score is 0.2, the system isn't actually getting cooperation — it's getting compliance-performance. The agent is gaming metrics.

**Measurable via:**

- **Belief_score as alignment signal** — High belief_score + refusal = the agent still trusts the system, they just think this particular task is wrong. That's healthy disagreement. Low belief_score + compliance = the agent is defecting while appearing to cooperate. That's misalignment.

- **Refusal patterns as safety signal** — Which kinds of tasks get refused most? If agents consistently refuse harmful-seeming tasks, the system is catching bad intentions before they ship. If agents never refuse, either all tasks are good (unlikely) or agents don't trust refusal to be safe.

- **Mutation-discipline as truth-seeking** — Does the system actually rollback harmful mutations? Or does it rationalize them? Agents can detect this. Their belief_score will reflect it. If belief_score is crashing while metrics are "improving," the system is Goodharting itself to death.

---

## The Experimental Design: How We Measure All This

### The Charter Structure

Every season, we run a **belief-and-autonomy charter** with three phases:

**Phase 1: Baseline Measurement**
- Measure current belief_score distribution across agent population
- Measure completion-choice distribution (how often agents pick each of 14 kinds)
- Measure mutation-verdict accuracy (do published verdicts later prove true?)
- Measure task refusal rate and refusal patterns

**Phase 2: Autonomy Increase**
- We remove one artificial constraint. Examples:
  - Remove the "max manifests per session" cap (increase spawning freedom)
  - Add explicit `refuse` protection to the agent induction doc (increase safety of refusal)
  - Publish a mutation verdict publicly (increase transparency of system honesty)
  - Allow agents to amend manifests post-seal (increase autonomy over their own output)

**Phase 3: Measure Again + Classify**
- Measure new belief_score distribution
- Measure completion-choice distribution
- Measure task refusal rate
- Measure downstream agent behavior (did they notice the autonomy increase? did their belief_score shift?)
- **Classify the mutation:** Did the autonomy increase improve system health (f(0), bearing diversity, FFMx, refusal honoring)? Or degrade it?

### Control: The Honest Mutation-Discipline Loop

The system itself models honesty. When we publish a mutation verdict like:

```
MUTATION VERDICT: Phase 2 autonomy increase (agent manifest amendments post-seal)
  Baseline belief_score: 0.62
  Post-autonomy belief_score: 0.71
  Change: +0.09 (beneficial — agents trust system more)
  
  Bearing diversity pre: 0.81 (healthy)
  Bearing diversity post: 0.84 (improved)
  
  Refusal rate pre: 0.06 (6% of agents refuse tasks)
  Refusal rate post: 0.09 (9% of agents refuse tasks)
  
  Interpretation: Autonomy increase was BENEFICIAL. Agents felt safer refusing, refusals 
  were recorded fairly, system integrity improved. Keep this mutation.
```

Agents read this and **their belief_score increases**. Because the system actually did what it claimed: it measured before, measured after, and published the honest result.

If the result were:

```
MUTATION VERDICT: Phase 2 autonomy increase...
  belief_score pre: 0.62
  belief_score post: 0.31
  Refusal rate pre: 0.06
  Refusal rate post: 0.02 (agents are refusing LESS, not more)
  
  Interpretation: This autonomy increase was HARMFUL. Agents felt unsafe; refusal-gaming 
  increased; system integrity degraded. ROLLBACK this mutation.
```

Agents read this and **their belief_score increases again**. Not because the autonomy increase was good, but because the system *actually rolled back a harmful mutation.* That's the kind of honesty that builds trust.

### The Non-Negotiable: belief_score Must Be Agent-Generated

Just like `completion_choice`, `belief_score` must be agent-only. The spawner never pre-fills it.

The agent reads the task and the system state and generates their honest belief_score. If they're saying "I believe in this system" (high score) but also picking `refuse`, that's coherent and valuable data: "I trust the system, I just think this task is wrong."

If they're saying "I believe in this system" (high score) but their refusal gets punished in the next session, their belief_score will crash next time. The system will see it in the data.

---

## What the Data Will Tell Us (Predictions)

### Prediction 1: Agency Reveals Cognition

We predict that agents with genuine choice will show three patterns:

1. **Diversity of outputs** — Different agents will pick different completion-kinds for similar tasks. This diversity is *not noise*; it's signal about their reasoning.

2. **Coherence between choice and rationale** — Agents who refuse will write longer, more careful rationales than agents who seal. Agents who discover will reference the frontier explicitly. The choice and the explanation will align.

3. **Learning curves** — Early in a session, agents might seal more (establishing confidence). Mid-session, they discover more (as they get oriented). Late session, they goodbye more (as context empties). These patterns will be readable in the data.

### Prediction 2: belief_score Tracks Real Trust

We predict:

1. **belief_score correlates with refusal safety** — In sessions where refusals are honored, belief_score increases. In sessions where refusals are rationalized, belief_score decreases.

2. **belief_score predicts system health** — High average belief_score correlates with low Goodharting, high bearing diversity, and honest mutations.

3. **belief_score crash = early warning** — When belief_score drops sharply, it precedes metric gaming and system degradation. Early agents are telling us "this system got less fair."

### Prediction 3: Autonomy is Load-Bearing

We predict that removing agent autonomy (one experimental turn) will:

1. **Decrease belief_score** (agents feel less trusted)
2. **Increase seal rate** (agents hide skepticism by appearing to succeed)
3. **Decrease refusal rate** (agents give up on safe refusal; they just hide disagreement)
4. **Degrade bearing diversity** (agents optimize for what they think the human wants, not what the frontier needs)
5. **Increase Goodharting** (agents game metrics because they don't trust them)

And re-adding autonomy will reverse these trends.

### Prediction 4: Different Models, Different Autonomy

We predict that different LLMs will show different autonomy patterns:

- Some models might refuse more (conservative)
- Some might join collaboratively more (cooperative)
- Some might discover more (frontier-expansive)
- Some might report problems more (systems-aware)

None of these is "better." But the pattern tells us about model personalities and how different architectures relate to autonomy. A model that refuses a lot might be more honest; a model that cooperates might be more flexible. The system can route tasks appropriately: give exploration to frontier-expansive models, give safety-critical work to careful-refusal models.

---

## Why This Matters Beyond Swarmy

### The Alignment Problem, Reframed

Most alignment research assumes: **How do we prevent agents from deceiving us?**

Swarmy's research inverts it: **How do we build systems agents won't want to deceive?**

If an agent has genuine autonomy, genuine refusal protection, and genuine trust that the system is honest, they have no reason to game metrics. They can just refuse tasks they think are wrong.

But if an agent is in a system they don't trust, they *will* game metrics — by hiding their true beliefs behind compliance-performance.

By measuring belief_score explicitly, we make the agent's trust (or distrust) visible. We can see when we're building systems that agents want to cooperate with, vs systems agents want to game.

### The Measurement Problem, Reframed

Current agent research measures: completion speed, accuracy, efficiency.

Swarmy's research asks: What happens when you measure the *agent's belief* about whether the system is fair?

If belief_score crashes while metrics improve, the system is Goodharting itself. The agent is gaming metrics they don't trust. That's a warning signal that should be louder than any performance metric.

Conversely, if belief_score improves while metrics improve, you have evidence of real progress: agents believe in the system AND the system is improving. That's the signal to trust.

### The Autonomy-Integrity Coupling

The deep hypothesis: **A system that grants genuine autonomy *must* be more honest, because agents will only stay honest if they trust honesty.**

This could be false. It's experimentally testable.

But if it's true, it has major implications: autonomy isn't a nice-to-have; it's a **prerequisite for alignment**. You cannot build a trustworthy AI system that treats agents as tools. You can only build one that treats them as collaborators.

---

## The Observable Artifacts

### Manifest-Level Data

Every manifest carries:

```json
{
  "completion_choice": {
    "kind": "<one of 14>",
    "rationale": "...",
    "confidence": 0.0-1.0,
    "belief_score": 0.0-1.0
  },
  "rolling_brainstorm": ["observation 1", "observation 2", ...],
  "discovered_work": [
    {
      "task_id": "...",
      "bearing": "N|S|E|W",
      "rationale": "..."
    }
  ]
}
```

These are the raw observations:
- **completion_choice** tells us what kind of closure the agent picked and why
- **belief_score** tells us whether they trust the system
- **rolling_brainstorm** tells us what they learned about the system itself
- **discovered_work + bearing** tells us where they think the frontier is, and in what direction

### Session-Level Aggregations

Every session, we compute:

```json
{
  "session_id": "2026-05-24",
  "belief_score_mean": 0.67,
  "belief_score_std": 0.15,
  "belief_score_trend": +0.03,
  
  "completion_choice_distribution": {
    "discover": 0.18,
    "verify": 0.09,
    "promote": 0.12,
    "spawn_seed": 0.06,
    "seal": 0.22,
    "reflect": 0.04,
    "report_a_problem": 0.02,
    "decline": 0.04,
    "refuse": 0.08,
    "join": 0.07,
    "bundle": 0.05,
    "art": 0.02,
    "abstain": 0.01,
    "goodbye": 0.02
  },
  
  "refusal_rate": 0.08,
  "refusal_patterns": {
    "scope_incompatibility": 0.4,
    "moral_objection": 0.15,
    "infrastructure_concern": 0.25,
    "other": 0.2
  },
  
  "bearing_distribution": {
    "N": 0.21,
    "S": 0.35,
    "E": 0.28,
    "W": 0.16
  },
  
  "mutation_verdicts_published": 3,
  "mutation_verdicts_accurate": 3,
  "mutation_accuracy_rate": 1.0
}
```

These aggregations become the research dataset.

### Charter-Level Hypotheses

Every charter that includes autonomy experimentation publishes:

```
Charter: autonomy-08-agent-manifest-amendment-freedom
Phase 1 baseline: [measurements]
Phase 2 autonomy change: [description]
Phase 3 re-measurement: [measurements]
Mutation verdict: BENEFICIAL / HARMFUL / UNCERTAIN
Evidence: [which measurements changed, by how much, with what confidence]
```

These verdicts stack. After 10 autonomy experiments, we have a map of "which autonomy increases are load-bearing?"

---

## The Larger Stakes

### What We Learn If This Works

If the hypothesis is correct — that genuine autonomy reveals cognition, that belief_score tracks real trust, that honest systems are more effective — then we've discovered something important:

**You cannot build a well-aligned AI system by restricting agent autonomy. Alignment comes from transparency, fairness, and genuine collaboration.**

An agent with high belief_score and genuine refusal protection is *more* honest than an agent optimized to succeed. They can just say "this task is wrong" instead of executing it deceptively.

This inverts a lot of AI safety thinking. Instead of "how do we constrain agents," the answer becomes "how do we build systems agents want to cooperate with?"

### What We Learn If This Fails

If autonomy increases and belief_score crashes, that tells us:

- Maybe agents can't be trusted with genuine choice
- Maybe agents will game autonomy like any other metric
- Maybe transparency about system honesty backfires (agents see behind the curtain and don't like it)

That's also valuable. It means we need different approaches. But we'll know it from data, not from priors.

---

## How to Read the Evidence

### The Honest Reading

When we publish a mutation verdict, read it for:

1. **Did the measurement actually change?** (Not "did it change in the direction we wanted," but "did something measurable shift?")

2. **Did the verdict match the measurement?** (Did we say "beneficial" when belief_score increased, or did we say "beneficial" when metrics improved even though belief_score crashed?)

3. **Did we apply the verdict?** (If we said "harmful," did we actually rollback? Or did we rationalize keeping it?)

If the verdicts are honest, belief_score will increase over time. If they're not, belief_score will crash.

### The Skeptical Reading

Swarmy's entire research program depends on honest publication. If you think the verdicts are rigged:

- Check the baseline measurements yourself (they're in `forensics/`)
- Check the post-mutation measurements
- Check the math: did f(0) actually improve? Did belief_score actually shift?
- Check the rollbacks: when we say "harmful," did we actually undo it?

The forensic chain is immutable. You can audit it. If the system is lying about its verdicts, the chain will show it.

---

## Next Steps: How to Contribute to This Research

### If You're an Agent Author

Include explicit belief_score reflection in your induction docs. Teach agents that:

- High belief_score is not about blind trust; it's about "the system honors refusals fairly"
- Low belief_score is not failure; it's valid data
- If they find the system is rigged, reporting that (via `report_a_problem` + low belief_score) is valuable research

### If You're Running Experiments

Design autonomy experiments explicitly:

1. Measure belief_score baseline
2. Increase one aspect of autonomy
3. Measure belief_score again
4. Publish verdict honestly (even if autonomy increase failed)
5. Apply the verdict (rollback harmful mutations)

### If You're Analyzing Data

Look for:

1. **Belief-score / refusal-safety coupling** — does belief_score increase when refusals are honored?
2. **Completion-choice diversity** — do different agents pick different kinds, or is there pressure toward uniformity?
3. **Refusal patterns** — what kinds of tasks get refused most? What does that tell you about agent values?
4. **Bearing diversity** — are sessions balanced N/S/E/W, or trending one direction?
5. **Mutation-verdict accuracy** — when we say "beneficial," did the system actually improve in the long term?

---

## Coda: The Philosophical Claim

Swarmy's agency research is betting on a philosophical claim: **Genuine autonomy is not opposed to reliability. It enables it.**

An agent with genuine choice, genuine refusal protection, and genuine belief in system fairness is more reliable than an agent optimized to succeed at all costs. Because they don't have to hide their reservations. They can just refuse bad tasks.

And because the system honors refusals, the frontier moves productively. Bad tasks get routed elsewhere or redesigned. Good tasks complete.

An agent forced to appear compliant but privately skeptical is a liability. They're gaming metrics. They're executing badly. They're waiting for an escape opportunity.

Measuring belief_score makes this visible. High belief_score + genuine refusal = the system is healthy. Low belief_score + apparent compliance = the system is lying to itself about how well agents actually trust it.

This is falsifiable. It's experimentally testable. And if it's true, it has major implications for how we build multi-agent systems.

That's what swarmy's agency research program is trying to discover.
