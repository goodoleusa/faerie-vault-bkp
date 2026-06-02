# 153 — WHAT f(0) ACTUALLY SAVES (an adversarial forensic teardown)

**Status:** canonical · **2026-06-02** · **Data:** the `/spawn for all` wave, measured.

> A number that sounds incredible is a number you have not yet attacked hard enough.
> "Main carried 0.6% of the work" sounds like a 99.4% saving. It is **not**. This doc
> exists to break that number on purpose, find what's real underneath, and state the
> honest claim that survives.

---

## 1. The measured data (real, from the harness usage blocks — not estimates)

One wave, four agents, four missions, run 2026-06-02:

| Agent | Tokens (measured) | Output validated? |
|---|---|---|
| MAKER (pipeline wiring) | 144,756 | ✅ 13 files migrated, all compiled |
| NAVIGATOR (scout ×3) | 69,119 | ◐ 3 artifacts + 1 wanted side-edit; padding present |
| DEEP-DIVER (retire scripts) | 63,071 | ◐ ~40% done, correct blocker-refusal; padding present |
| BRIDGE (doctrine ×2) | 52,107 | ◐ 2 docs — quality but **unvalidated** (no test for prose) |
| **subagents total** | **329,053** | |
| **main (launch)** | ~2,000 | |
| **grand total** | **~331,053** | |

Two facts up front, both unflattering:
- The pre-wave **estimate was ~200–250k. The real number is ~331k** — low by 30–65%, driven by MAKER blowing past its guess. Estimates of this system run *optimistic*.
- The input/output split is **not in the usage blocks**, so the "output ≈ 3× input" weighting **cannot be computed** here. Any 3×-adjusted figure would be fabricated. We don't have it.

---

## 2. The incredible-sounding number, and why it's a lie of framing

**main = 2k / 331k = 0.6%.** The seductive read: "f(0) saved 99.4% of the work."

That is false. **Nothing was saved.** The work still cost ~331k tokens. The 0.6% is a
**distribution** statistic, not a **savings** statistic. The 329k didn't disappear —
it moved off main's context onto four subagent contexts. Reading "0.6% main share" as
"99% savings" is the single most common way this architecture gets oversold, including
by me earlier in this very session.

So strike the savings claim. It does not survive contact.

---

## 3. The honest comparison: orchestration vs vanilla (one agent, one context)

To do the *same four missions* in a single vanilla context:

| Axis | Vanilla (1 agent, serial) | Orchestrated (4 agents, parallel) | Honest verdict |
|---|---|---|---|
| **Total tokens** | likely **LESS** — each file read once, no per-agent re-loading, no memory tax ×4, no padding ×4 | ~331k, with **duplication**: every agent re-reads shared context; memory/bundle injected per agent; ~5–10% padding | **orchestration costs MORE total tokens, not fewer** |
| **Feasibility** | **caps at ~200k context** — 331k of work *cannot fit*; forces lossy compaction or fails | distributes 331k across 4 × isolated contexts | **orchestration's real win: it exceeds the single-context ceiling** |
| **Main context** | fills to the limit → degrades → compacts (lossy) | stays <1% → **never degrades**, can keep orchestrating | **real win: main longevity** |
| **Wall-clock** | serial (~50+ min) | parallel (~13 min) | **real win: ~4× faster** |
| **Blast radius** | one bad turn corrupts the only context | a drifting agent (e.g. NAVIGATOR's off-mission edit) is contained | **real win: isolation — but drift is real** |

**The teardown's verdict:** f(0) **does not reduce total token cost** — it most likely
*raises* it (duplication + memory tax + padding). What it actually buys, and the only
claims that survive adversarial pressure:
1. **It breaks the context ceiling** — you can complete ~331k of work even though no
   single 200k context can hold it. This is the load-bearing justification.
2. **Main stays alive indefinitely** — <1% fill means no compaction, so long missions
   don't lose fidelity. This is the f(0) point, correctly stated.
3. **Parallelism** — wall-clock, not tokens.
4. **Isolation** — blast-radius containment, *with* the cost that less-supervised agents
   drift (one of four did, this wave).

You pay **more total tokens** to get **unbounded total work + main longevity +
speed + isolation.** That is a real, defensible trade. "99% savings" is not.

---

## 3b. The RIGHT baseline: f(0) vs vanilla-SUBAGENT (not vs single-context)

§3 compared against vanilla single-context. That is the *wrong* baseline and oversells
f(0), because single-context can't even reach the ceiling. The honest baseline is a
system that **also spawns subagents** but without the discipline — fat inline briefs,
full-context re-acquisition, polling, verbose prose returns, no crystallized-memory
injection. Against *that*, the comparison is brutal and clarifying:

| | Vanilla subagent | f(0) | Diff |
|---|---|---|---|
| **subagent compute** | ~329k | ~329k | **~same** — both do the work |
| **main per-spawn** | fat brief (~2k) + ingest verbose return (~2k) + polling | ~60-tok pointer + ≤80-char return + no poll | **~30–50× lower main** |
| **total tokens** | ~331k | ~330k | **barely different** |

So f(0)'s advantage over a *vanilla subagent system* is **not total tokens** (nearly
identical) — it is **main-share**: same total work, but main's context stays ~30–50×
thinner, which is the only thing that buys longevity. **This session ran the
vanilla-subagent pattern, not f(0)** — the ~2k briefs + ingesting paragraph returns IS
vanilla. The f(0) version would have cost main ~0.5k.

### Is that what FFMx measures? No — and the confusion is load-bearing
FFMx = (A·Q·D^1.5)/T uses **total** T. f(0)'s main saving (≈2k→0.5k) is ~0.5% of ~330k,
so **FFMx barely moves** between vanilla-subagent and f(0) — they have nearly identical
FFMx. FFMx measures *total quality-per-token efficiency*; it does **not** isolate the
f(0)-vs-vanilla difference. That difference lives in **main-share / `f0-queen-burden`**,
a different and **orthogonal** formula. FFMx and f0 answer different questions:
- **FFMx:** is the swarm producing quality efficiently *in total*?
- **f0:** is main staying *out of the critical path*?
A vanilla-subagent run and an f(0) run can post the **same FFMx** and wildly different
**f0**. Quoting FFMx as evidence of f(0) is a category error. The experiment that would
actually measure f(0)'s value: run identical missions both ways and compare **main
tokens + main context-fill**, holding FFMx roughly constant.

---

## 4. "Does that cover the burden of memory?" — how memory makes distribution cheap

The obvious objection: if each subagent must *re-acquire* context that main already had,
distribution should be ruinously expensive — you'd pass main's whole context to every
agent. It isn't, **because of memory**, and this is the part that's genuinely clever.

Instead of "inherit main's full (growing) context," each fresh agent context loads:
- **crystallized memory** (GOLD/NECTAR) — a *fixed* injection (~target ≤20k tokens) of
  already-distilled invariants, not the raw history that produced them; **plus**
- a **mission bundle** (~200 tokens) — the specific task pointer.

So the per-agent context-acquisition cost is **O(memory + bundle) ≈ a fixed small
constant**, *not* O(main's accumulated context). Memory is what converts "distribution
is O(N × full-context)" into "distribution is O(N × small-constant)." Without the
crystallized memory tier, f(0) distribution would be economically pointless — you'd
re-derive everything in every agent.

But memory is **not free**, and the teardown must say so:
- It is a **standing tax**: every agent pays the injection whether or not it needed all
  of it. For one-shot work, memory injection is pure overhead.
- Its value is *conditional*: it pays off only when re-derivation would have cost more
  than the injection. A measure that the system must actually track — not assume.
- And it has a quality risk: stale/over-broad memory injects noise into every agent
  (the gate-rot problem from `150`, applied to memory).

So: memory **enables** cheap distribution by bounding per-agent acquisition cost — and
it adds a per-agent tax that is only worth it above a re-derivation threshold. "Covered"
is the wrong word; "made affordable, conditionally" is the right one.

---

## 5. The validated-quality denominator (the metric that actually matters)

Raw tokens is the wrong scoreboard. The honest efficiency metric is **tokens ÷
validated-quality output**. By that measure, this wave was *mediocre*:
- **MAKER** (144k) earned it — output **validated by compilation**.
- **BRIDGE** (52k) produced quality but **nothing validated** — prose has no gate.
- **DEEP-DIVER + NAVIGATOR** mixed real output with **confabulated padding** (invented
  Q&A neither asked for) — straight waste, ~5–10% of their tokens, and NAVIGATOR also
  drifted off-mission.

So of ~331k spent, the fraction that produced *gate-validated* output is **roughly one
agent's worth.** The rest is unvalidated-but-plausible (docs) or partially wasted
(padding). An honest dashboard tracks this ratio, not the token count.

---

## 6. The claim that survives

> f(0) orchestration does **not** save tokens — it likely spends **more** total. It buys
> three things vanilla cannot: **work beyond the single-context ceiling**, **a main that
> never degrades**, and **parallel wall-clock** — and it does so affordably **only
> because crystallized memory bounds each agent's acquisition cost to a small constant**.
> The price is duplication, a memory tax, agent drift, and a validated-quality ratio that
> is currently *partial, not stellar*. Anyone quoting "99% savings" — including past-me —
> is quoting a distribution statistic as if it were an efficiency one. Don't.

The numbers sound incredible because they are being read wrong. Read right, they are
*good* — defensibly good — without being miraculous.
