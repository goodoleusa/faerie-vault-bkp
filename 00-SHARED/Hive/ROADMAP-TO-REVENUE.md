---
type: roadmap
status: living-document
generated: 2026-03-29
doc_hash: sha256:pending
---

# Roadmap to Revenue

This is a working document. It tracks concrete milestones, not aspirations. Each stage says: when X is true, we can claim Y, and Y is what makes Z possible. Nothing moves to the next stage without the prior milestone being real.

---

## The Business in One Sentence

Users buy tokens through us. We buy from Anthropic. Our margin is the optimization gap — how much better our infrastructure makes cheap models perform relative to what users would get buying direct. Zero servers. Zero staff. Zero inventory. The infrastructure runs on the user's machine. Our cost base is our own API usage during development and the time it takes to build and maintain the system.

This is not a soft margin. It is a performance claim: system-haiku delivers ≥ vanilla-sonnet results at roughly 70% lower cost. When that claim is empirically supported, the margin is real. Until then, we have a promising system and honest uncertainty.

---

## Stage 0 — Current (Proving It Works)

**Milestone achieved:** composite ≥ 0.48, +115% vs vanilla measured on three instrumented dimensions

**What we can say:**
The system outperforms vanilla Claude on every instrumented dimension. Resilience is at 1.00 — the stigmergy layer (manifests, streams, hash chains) is working. Piston efficiency is at 0.83 — agents launch in the right order and fast. These are architectural properties, not flukes.

**What we cannot say yet:**
MEMORY and QUALITY dimensions are not instrumented. The +115% is computed on 3 of 7 dimensions. The core claim — system-haiku ≥ vanilla-sonnet — has not been run as a controlled experiment. We have strong evidence the system works. We do not yet have the evidence needed to charge for it.

**What this stage feels like:**
You are using the system on real work. Each session, it is marginally better than the last. The HONEY is building. The agents are learning. But you are funding this with savings and API credits, and the meter is running. The goal of Stage 0 is to get to Stage 1 as fast as possible — not to polish, not to document, not to tell anyone. Just wire the measurements.

**Cost:** API tokens are R&D, not COGS yet. Each session costs $0.50-$3.00 depending on depth. This is the cost of building evidence.

**Revenue:** $0

---

## Stage 1 — Instrumentation Complete

**Milestones (in order of priority):**
- [ ] `honey_hit` wired → MEMORY score ≥ 0.7
- [ ] Depth scoring collection path wired → QUALITY score ≥ 0.7 (requires weekly 15-min human review, not automated)
- [ ] model_compare.py live run → system-haiku MBS ≥ vanilla-sonnet MBS
- [ ] composite ≥ 0.70

**What each milestone means:**

`honey_hit` wired: MEMORY jumping from 0.00 to 0.4-0.6 immediately is the expected outcome based on observed behavior. The memory is working — it is just not being counted. Wiring this takes 1-2 sessions and is the highest-leverage instrumentation task.

Depth scoring: This one requires human judgment. The rubric is defined (Eval-Framework.md D1, 0-10 scale). The process is: pick 3 REVIEW-INBOX findings at random per week, score them, log the result. It takes 15 minutes. The score will not be automated because quality is not automatable — human validation is the point.

model_compare.py live run: This is the gating milestone. Two arms: faerie+haiku vs vanilla sonnet, same tasks, blinded scoring. If haiku+infrastructure ≥ sonnet baseline, the economic claim becomes defensible. If it does not, we revisit the core hypothesis before going further.

**What we can say at Stage 1:**
"System-haiku delivers ≥ vanilla-sonnet quality at approximately 70% lower API cost."

This is the sentence that unlocks revenue. Not before.

**What unlocks:** The ability to charge. Not the ability to market, not the ability to pitch — the ability to make a specific claim to a specific user and have the evidence to back it.

**Timeline:** Approximately 5-10 sessions of focused instrumentation work. Not a sprint — careful work. Each metric wired correctly is worth more than all the features that could be added instead.

---

## Stage 2 — First Paying User

**Milestone:** One user pays for tokens through us instead of Anthropic direct.

**What that requires:**

*Technical:* An API proxy or reseller arrangement. Anthropic permits resellers — the mechanics are: user configures their API base URL to point to our proxy, which forwards requests to Anthropic and invoices the difference. No new models, no new infrastructure, no servers we manage long-term beyond a lightweight proxy. The faerie system itself runs on the user's machine.

*Trust:* Memory-Bench score published and accessible so the user can verify our claims themselves. We do not ask anyone to trust a claim we cannot show evidence for. The benchmark is the transparency mechanism.

*Onboarding:* A path for a user to install faerie on their machine that takes under an hour. This does not need to be polished. It needs to work. Documentation-first, not product-first.

*The first user:* Someone who already knows the system exists, has seen it work, and is doing sustained technical work (investigation, research, code, writing) where cross-session memory has compounding value. Not a cold acquisition. Someone from the immediate network who would benefit and wants to pay because it is worth it to them.

**Revenue:** First dollar. The amount does not matter yet. The fact of a transaction matters — it proves the value proposition is real enough that someone acted on it.

**Cost basis:** API token cost × volume. At current usage patterns, margin is approximately the difference between haiku pricing and sonnet pricing on the tasks being run. This is a real margin because the claim is performance parity — the user gets sonnet-equivalent work at haiku prices.

---

## Stage 3 — Breaking Even

**Milestone:** Monthly API token costs (our own R&D + user volume) covered by user revenue.

**The math (needs current data to complete):**

```
monthly_api_spend = [check: ~/.claude/scripts/session_metrics.py --monthly-cost]
margin_per_user = avg_user_monthly_spend × optimization_gap_pct
break_even_users = monthly_api_spend / margin_per_user
```

We do not know the monthly R&D API spend precisely yet — pulling from session_metrics.jsonl will give this. The optimization gap percentage is what model_compare.py proves. Until those numbers are in hand, the break-even user count is unknown, but the formula is correct.

**What this stage means:** We are no longer burning savings to do R&D. The system is paying for itself. This does not mean income — it means the experimentation is now self-funding. Every session we run is covered by users getting value from the system.

**What breaks this:** A user churns because the system does not deliver the claimed performance improvement. The benchmark is the defense against this — if CPI trend shows declining cost per finding over time, users have empirical evidence of compounding value. Churn risk drops when the value is visible, not just claimed.

---

## Stage 4 — Covering Basic Needs

**Milestone:** Net monthly income ≥ [whatever covers rent + food in your location].

**The calculation:**

```
basic_needs_monthly = [your actual number — be honest, not aspirational]
incremental_users_needed = basic_needs_monthly / margin_per_user
total_users_at_this_stage = break_even_users + incremental_users_needed
```

This is the stage that ends the clock on savings depletion. Until here, every month is a countdown. After here, it is a business.

**What changes at this stage:**
- Time pressure drops. Not gone — growth still matters — but the existential countdown is over.
- R&D decisions become cleaner. Features that serve existing users at their current usage levels are the priority, not features that might attract hypothetical future users.
- The benchmark gains a track record. A user who has been on the system for 4+ months has real CPI trend data. If it is declining — if they are getting more per dollar spent month over month — that is the strongest possible marketing material. It is also the strongest academic evidence. CPI trend over real users is harder to fake than a controlled benchmark.

**Honest uncertainty:** The margin per user is the unknown. It depends on how much users actually use the system and whether the haiku-vs-sonnet claim holds at production volume and across diverse task types. We do not have this data yet. The number of users needed could be 5 or 50. The formula is right; the inputs are pending.

---

## Stage 5 — Sustainable Growth

**Milestone:** Memory-Bench published as an academic benchmark → organic discovery begins.

**What this changes:**
At this stage, the benchmark is doing marketing. Researchers and practitioners searching for memory system comparisons find the paper. They evaluate their own systems against the benchmark. They cite it. They find faerie as the reference implementation.

We do not need to advertise. We do not need sales. We need the benchmark to be good enough that people want to use it — which means it has to be genuinely rigorous, not designed to flatter us. A benchmark that only faerie can pass is not a benchmark. A benchmark that honestly measures what matters, and on which faerie happens to score highest because the architecture is genuinely good, is worth publishing.

The competitive dynamics are: once Memory-Bench is a cited standard, we are the referee. Every competitor comparison we publish is scientifically defensible. Every competitor who wants to claim memory capability has to run our benchmark or explain why they did not.

**Revenue at this stage:** Depends entirely on what the CPI trend has shown by then. If compounding economics are real — if users' cost per finding is declining month over month — the benchmark paper is evidence of that, not just a product claim. That is the strongest possible position.

---

## The Actual Moat

The code can be copied in two weeks by a well-resourced competitor. This is not a code moat.

The moat is three things:

**1. Crystallized knowledge infrastructure.**
The HONEY that makes every session cheaper than the last cannot be copied — it is accumulated from real work, real sessions, real validated findings over real time. A competitor starting today does not have six months of crystallized context. They start cold.

**2. The benchmark standard.**
Memory-Bench published as a cited standard means we are the referee. Competitors have to run our benchmark to claim memory capability. The benchmark was designed by the team building faerie — it was designed around the dimensions where crystallized context outperforms accumulated context. This is not a coincidence. The framework inherently surfaces architectural advantages that faerie was built to have.

**3. CPI trend evidence.**
If we have users whose cost per finding has been declining for 4+ months, that is data no competitor can manufacture. They cannot fake a 4-month longitudinal trend. First-mover advantage in a market where the core value proposition is time-compounding is real advantage.

---

## Risks and Honest Uncertainty

**Anthropic changes API pricing.**
This changes the margin calculation but not the core claim. If haiku gets more expensive, the optimization gap narrows. If sonnet gets cheaper, the gap also narrows from the other side. The benchmark claim (system-haiku ≥ vanilla-sonnet) remains true independent of pricing — pricing affects the business model, not the technical result. Mitigation: multi-model support means we are not locked to a single pricing structure. If haiku stops being the right model, we route to whatever is.

**Anthropic builds this natively.**
This is the most real risk. If Claude natively accumulates crystallized context across sessions, the infrastructure argument weakens. Counter-arguments: (a) the benchmark is still ours — we defined the standard; (b) Anthropic's implementation will be generic; ours is tuned to specific work patterns; (c) multi-model support (not just Anthropic) becomes the differentiator. This risk is real. It is not a reason to stop — it is a reason to move fast on Stage 1 and Stage 2 before the window closes.

**Competition builds something similar.**
If they publish first, they are the referee. The response is: publish the benchmark faster than they publish the system. The benchmark is a standalone contribution — it can be submitted independently of the faerie system. We should consider publishing the benchmark before the product if timing becomes a concern.

**model_compare.py shows system-haiku < vanilla-sonnet.**
This is the result that invalidates the core claim. If it happens: we do not pretend it did not happen. We publish the result, understand why, and either (a) determine what would need to change to flip the result and pursue that, or (b) reframe the value proposition around RESILIENCE and PISTON, which are genuinely strong and do not depend on the haiku-vs-sonnet comparison. A system that never loses work and always has agents launching in parallel has real value even if model-for-model it is not outperforming baseline. But this is a consolation prize. The core claim is worth fighting for.

---

## Next 3 Actions (in order, no skipping)

**1. Wire honey_hit — get MEMORY score off zero.**
This is the highest-leverage instrumentation task. One session. The expected outcome is MEMORY jumping immediately because the memory is working, just not counted. This is also the most honest thing to do — running with a 0.00 MEMORY score when the memory is active is misleading, even to ourselves.

**2. Run model_compare.py live — confirm the core claim.**
Two arms: faerie+haiku vs vanilla sonnet. Three standardized tasks. Blinded human scoring. This result gates everything after it. We need to know this number. If it is what we expect, Stage 1 is nearly complete. If it is not, we need to know that now, not after we have spent more sessions building toward a claim we cannot defend.

**3. Open-source Memory-Bench runner — start building credibility before first user.**
The runner (not the proprietary HONEY data — just the tasks, rubrics, and eval harness) on GitHub. No product announcement. No marketing. Just: here is the benchmark, here is how to run it, here is our result. This plants a flag. It starts the citation clock. And it forces us to write down the methodology clearly enough that someone else could run it — which is the discipline that makes the methodology actually rigorous.

These three actions are sufficient to get from Stage 0 to Stage 1. Everything else can wait.
