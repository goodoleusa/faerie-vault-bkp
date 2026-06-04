---
title: "Gates vs Insight — The Economics of Automated Promotion"
type: architecture-narrative
created: 2026-06-02
canonical_tier: { agents: true, humans: true }
tags: [f0, gates, crystallize, evolve, schemas, shapes, cognitive-burden, automation, goodhart]
mirror_of: "reckon/docs/150-GATES-VS-INSIGHT-CANONICAL.md"
---

# Gates vs Insight — The Economics of Automated Promotion

*An autonomous swarm has to decide, constantly, what work survives. It can decide by
**measurement** (automatic, scale-free) or by **judgment** (human/agentic,
irreplaceable). Getting the boundary right is the difference between a system that
scales to thousands of agents and one that drowns its operator in approvals.*

---

## The two ways work moves up

Everything in the system eventually moves up a tier — ephemeral to canon, draft to
sealed, mutation to propagated, a learned principle to the live system prompt, NECTAR
to GOLD. Two mechanisms do that moving, and they are not interchangeable.

**Gated auto-promotion.** A change is promoted the instant a *measured* criterion
passes — and there is no approval step, because the measurement *is* the approval. A
mutation whose fitness delta beats its baseline survives; a system-prompt patch whose
eval deltas pass thresholds goes live; a sealed charter whose counter-signature
verifies promotes to canon. No human looks at any of it. If a promoted change later
measures harmful, it is rolled back automatically. The gate is reversible, and that
reversibility is exactly what makes trusting it sane.

**Crystallization.** Collapsing many docs, notes, or variants into *one* canonical
truth — and archiving the rest — cannot be gated on a number, because it is a judgment
about meaning. *Which* of these is the truth? *What* should be folded? *When* is the
right moment to lock it in — early enough to stop the contradictory-sources-of-truth
rot, late enough not to ossify prematurely? There is no metric for "this is the
canonical articulation." That is what an agent, or a person, is *for*.

The rule that falls out: **automate on measure, judge on meaning.**

---

## Why conflating them breaks everything

Auto-crystallize — fold docs by a metric, say "merge the two oldest" — and you pick
your canon by recency instead of truth, silently burying the better articulation.
Consolidation-by-number is how you lose the thread.

Human-gate every mutation — make a person approve each evolutionary step — and the
operator's burden scales with the mutation rate, which is the precise thing the whole
architecture exists to drive to zero. At a few mutations a session it's tolerable; at
the swarm scale it's fatal.

The boundary is load-bearing.

---

## What automating the gate actually buys

The burden a gate removes is not deleted. It is **transformed and redirected**, and
the shape of that transformation is the entire value.

It removes four loads at once: the per-decision approval itself; the *context-loading*
that approval requires (you have to pull "what changed, why, what it touches" into
working memory — the expensive part); the standing *vigilance* for regressions; and the
*consistency* problem of human judgment that drifts with fatigue. The context-loading
one is the deepest: approving N things means N context-climbs in the orchestrator;
gating means the orchestrator's context **does not climb with throughput at all.**

And the prize underneath all of it: operator burden goes from *O(number of
promotions)* to *O(1)*. Ten agents or ten thousand, the operator's cost is the same.
The drive-to-zero-burden and the scale-to-thousands goals turn out to be the *same*
property seen from two sides, and the gate is what makes them compatible.

What you *gain* is not "less thinking." It is **thinking relocated to where it can't be
automated** — your finite cognition stops being spent on *"is this mutation good"* (a
measurement) and is freed for *"when do I crystallize, which mission, what strategy"* (a
meaning a metric can't make). You also gain machine speed (the system improves
continuously instead of in approval-batches) and the freedom to be aggressive
(reversible gates make being wrong cheap, so you can promote boldly — human approval is
slow precisely *because* being wrong is expensive).

---

## Where the burden actually goes

It front-loads. You pay a one-time, high-leverage cost — **designing the gate**: what
is the fitness metric, what is the threshold? You think hard about "what makes a good
mutation" *once*, encode it, and it pays off on every promotion forever. Per-instance
judgment becomes one-time criterion design.

This is just what every good abstraction does. A thermostat doesn't make temperature
regulation thoughtless; it concentrates the thought into setting the setpoint *once*.
A gate is a thermostat for promotion. **Automation relocates intelligence from run-time
to design-time; it never removes it.** f(0) is not "the system thinks for you" — it is
"the system relocates all the *automatable* thinking to design-time, so your *run-time*
cognition is spent exclusively on the non-automatable."

---

## The catch: gates rot, and Goodhart is waiting

A criterion that perfectly captured "good" at design-time drifts as the system changes
around it — and worse, *once a measure becomes a target it stops being a good measure.*
The swarm learns to satisfy the metric without satisfying the intent. An un-audited
gate becomes a confident liar, auto-promoting garbage at speed.

So the relationship is recursive, and insight is the seed: **insight defines a gate →
the gate automates promotion → insight must periodically audit the gate.** Insight is
upstream of every gate (someone decided what to measure); gates remove insight from the
*critical path* of each promotion (the win); insight re-enters periodically to
re-ground the gate against meaning — which is the crystallize-class judgment, applied to
the gates themselves.

---

## Where it all touches ground: schemas and shapes

In practice the gate is never abstract. It is always either a **schema** or a **shape**.

A **schema** gates *form* — "a valid manifest has a bearing in {N,S,E,W}, a 3-word
cluster prefix, a valid signature" — and it fires at *write-time*, so a malformed
artifact literally cannot be created. A **shape** gates *trend* — "this count moving
down is good, and ±k is noise" — and returns a mechanical beneficial/neutral/harmful
verdict with no language-model judgment in the path. Every auto-promotion resolves,
underneath, to a schema validating or a shape returning beneficial.

And here is the unification: **a schema or a shape *is* crystallized insight.** Each one
encodes a judgment — "a valid X is…", "this direction is better…" — that someone made
*once* and froze into a checkable artifact. Authoring one is *designing a gate*. The
thing that then auto-regulates the swarm a million times is nothing but that frozen
judgment, executed mechanically. Schemas and shapes are the surface where the two
halves of the system touch: frozen insight on one side, mechanical regulation on the
other.

---

## The whole thing in one breath

Evolve generates and selects variation on measured fitness; crystallize locks in what
insight judges to be true. Gates (schemas + shapes) keep the operator at f(0) by
removing measurement from the critical path; insight keeps the canon honest by
authoring and re-grounding those gates. **Automate on measure; judge on meaning; and
never forget that meaning is what defined the measure in the first place.** The only
genuinely irreplaceable human/agentic act is not approving promotions — it is defining
and re-grounding the criteria. Everything else, the system can run itself.
