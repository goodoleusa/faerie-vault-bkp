---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: ffmx-emergence-formula
status: synthesis-log
canon_candidate: true
supersedes_partial: 17-compression-vs-crystallization-emergence-driver.md
---

# Correction: the compression-emergence formula is FFMx

User correction (verbatim):

> "crystallize (per doctrine 17 — meaning compression), thats not what
>  crystallize means, i was asking you to search for the term
>  compression in relation to emergence eval metrics because you
>  mentioned theres a formula that seems to perfectly predict certain
>  emergence"

Doctrine 17 was directionally right (crystallization vs naive
compression are opposites with the same shape) but I missed the
specific formula the user remembered. **That formula is FFMx.**

## The formula

```
FFMx = (A × Q × D^1.5) / T
```

Where:
- **A** = artifact count (manifests sealed, deliverables shipped)
- **Q** = quality (citation rate, validation density)
- **D** = discovery depth (novel terms / patterns surfaced)
- **T** = tokens spent

Source: `/mnt/d/0local/gitrepos/membench/EMERGENCE-METRICS.md`
line 226 (canonical spec, just shipped today by agent ab1e8cfe as
part of the E-series split).

## Why it predicts emergence

Think of it as **information density per token** — but with a
non-linear boost for discovery:

- High A·Q means lots of high-quality work
- ÷ T normalizes for cost
- **D raised to 1.5** is the kicker: linear discovery gets linear
  credit, but a system that finds PATTERNS (recurring shapes,
  cross-cutting connections) gets super-linear credit

Emergence is precisely the moment when the system finds patterns
faster than it spends tokens. FFMx captures that turning point as
a single number.

## The compression connection

`/mnt/d/0local/gitrepos/membench/docs/ICON-METRICS-CROSSWALK.md`
line 350 names the icon:

```
⚡ Efficiency = tokens_per_finding = f(0) compression
```

So **f(0) compression** is the icon's name for the underlying ratio
that FFMx maximizes. "f(0)" reads "the queen approaches zero
direct work" — the swarm produces the meaning, the queen just
crystallizes it; the smaller the queen's token spend per finding,
the better the system is compressing meaning into output.

This is NOT text compression. This is **information-theoretic
compression**: how much signal does the system produce per token of
context burned. High FFMx = the system gets a lot of meaning out of
each token of compute.

## Baseline + target

- **Baseline (faerie2, 2026-04-23):** FFMx = 44.4
- **Target (3-month):** FFMx ≥ 66.6 (= 1.5× baseline)
- **Today (2026-05-03 measurement):** FFMx = 52.1 (above baseline,
  below target, trending in the right direction)

These are the actual numbers from the swarmy seed submission
landed in the membench OSS prep agent's work today.

## Why FFMx is E6, not in the M-composite

FFMx is unbounded scale (can grow arbitrarily large). The
M-composite is bounded [0, 1]. They can't share an axis.

Today's resolution (agent ab1e8cfe's follow-up): split into the
**E-series** (Emergence metrics, experimental):
- E1 Emergence Structural — edge_density + clustering + linearity
- E2 Emergence Qualitative — novelty + evidence + cross_domain
- E3 Spawn Leverage avg
- E4 Spawn Leverage Distribution
- E5 Emergence Trajectory — rolling-window E1 delta
- **E6 FFMx Composite — the f(0) compression formula**
- E_composite — provisional weighted combination

E-series gets its own leaderboard table, separate from the M-core
and the MaaS_Score / MaA_Score composites. This is the right
architectural call: M-core compares all memory systems on a bounded
axis; E-series compares emergence depth on an unbounded axis;
neither mixes.

## What this corrects in doctrine 17

Doctrine 17 (`compression-vs-crystallization-emergence-driver.md`)
made the FOLLOWING claims that were directionally right but
imprecise:

| Doctrine 17 claim | Status |
|---|---|
| Naive compression destroys emergence | ✓ Right (text compression of HONEY) |
| Crystallization (LLM-mediated meaning compression) drives emergence | ✓ Right (the MECHANISM) |
| M7 Crystallization is THE load-bearing emergence indicator | ⚠ Partial — M7 is diagnostic only; **FFMx (E6) is the actual indicator** |
| The driver metric is "meaning-per-token" | ✓ Right — and that's exactly what FFMx measures (A·Q·D / T) |

So doctrine 17's MECHANISM (crystallization, not naive compression)
remains correct. The METRIC isn't M7 — it's FFMx (E6). Doctrine 17
should be read as: "crystallization is the LEVER; FFMx is the
GAUGE that tells you whether the lever is working."

## How this connects to the rest of the doctrine arc

| Doctrine | Layer | Role |
|---|---|---|
| 13 Shape-RAP-evolution-membench | Concept | Shape = countable patterns |
| 14 Formulas static + dynamic | Concept | Formula = compute over shapes |
| 17 Compression vs crystallization | Mechanism | Crystallization > naive compression |
| **18 FFMx** | **Measurement** | **FFMx scores how well the mechanism works** |

The full chain:
- An agent **CRYSTALLIZES** memory (the mechanism)
- This produces **DENSER MEANING PER TOKEN** (the property)
- Which **INCREASES FFMx** = (A·Q·D^1.5) / T (the measurement)
- Which **PREDICTS EMERGENCE** (the outcome)

## Operational implication

When the memory-pressure-relief tool (peer agent a54ebbec, in flight)
runs, the right success metric is **FFMx delta**, not just F4
delta. F4 measures memory burden ratio; FFMx measures whether the
relief move actually preserved emergence.

If a relief move drops F4 but ALSO drops FFMx → the move was naive
compression. Roll back.

If a relief move drops F4 AND maintains/improves FFMx → the move
was real crystallization. Keep it.

## Single-line summary

**FFMx = (A·Q·D^1.5)/T is the formula that predicts emergence via
information density per token. It's E6 in the new E-series. The
1.5 exponent on discovery depth is what makes it predictive: linear
work gets linear credit; pattern-finding gets super-linear credit.
Crystallization is the mechanism that raises FFMx; FFMx is the
gauge that tells you crystallization worked. Doctrine 17 had the
mechanism right; this doctrine names the gauge.**

---

*Closes the doctrine arc 08-18 for this session. Source:
`/mnt/d/0local/gitrepos/membench/EMERGENCE-METRICS.md` (the
canonical E-series spec). Companion charts:
`/mnt/d/0local/gitrepos/membench/docs/ICON-METRICS-CROSSWALK.md`
(efficiency icon = tokens_per_finding = f(0) compression);
`forensics/schemas/formulas/ffmx-emergence-quality-score.formula.json`
(schema). Folds into Part 5 of
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` when next pass
crystallizes the measurement layer.*
