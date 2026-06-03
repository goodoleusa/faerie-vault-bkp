---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: membench-comparator-doctrine
status: synthesis-log
canon_candidate: true
---

# Membench as comparator — MaaS vs MaA, shared core + system-specific surfaces

User stated (verbatim, accumulated):

> "using standard eval harnesses, common units, and best practices for
>  allowing friendly open competition between different close source ai
>  mem products"
> "also distinguishing between Memory-as-a-Service and Memory-as-
>  Architecture (swarmy) and they have different things they are
>  optimizing for and different business models altogether"
> "so this membench provides a harness to compare where MaaS and MaA
>  are comparable, and then offers metrics that are more specific to
>  their case that are not really comparable"

This crystallizes membench's role as a public benchmark: it
provides BOTH a shared comparable core AND honest system-specific
surfaces, with explicit guidance that cross-category comparisons
are NOT meaningful.

The canonical definition lives at
`/mnt/d/0local/gitrepos/membench/BENCHMARKS-MAAS-VS-MAA.md`.
This doc is the public-comm distillation.

## The two operator types

### MaaS — Memory-as-a-Service

**Business model:** API wrapper. Serve many independent client
sessions cheaply. Compete on per-query cost.

**Optimizes for:**
- Low cost per query
- High cache hit rate
- Minimum tokens per response
- Fast retrieval

**Examples (representative — not exhaustive):** mem0, Letta (in
its API-server mode), Zep (cloud), Pinecone-as-memory wrappers,
LangChain memory adapters.

**Failure signature:** identical context re-fetched every session;
no compounding; synthesis stays generic.

### MaA — Memory-as-Architecture

**Business model:** integrated platform. Serve one deep team or
investigation where losing session context loses days of reasoning.
Compete on compounding value + flow preservation.

**Optimizes for:**
- Cross-session signal survival
- Stigmergic coordination depth
- Synthesis insight (emergence)
- Forensic integrity (chain-of-custody)

**Examples:** swarmy (the canonical reference impl), other agent
orchestration platforms where memory IS the substrate (not a
service called).

**Failure signature:** unbounded token spend without commensurate
synthesis depth; "stigmergy is decorative."

## The membench comparison surface

```
                ┌──────────────────────────────────────┐
                │  SHARED CORE  (comparable across all │
                │   memory systems — M1-M11 canonical) │
                │                                       │
                │   M1  Retention                       │
                │   M2  Relevance                       │
                │   M3  Work Efficiency                 │
                │   M4  Overhead                        │
                │   M5  Continuity                      │
                │   M6  Coordination (diagnostic)       │
                │   M7  Crystallization (diagnostic)   │
                │   M8  Confabulation (VETO)            │
                │   M9  Ceiling-Hit (diagnostic)        │
                │   M10 Coverage (multiplier)           │
                │   M11 Bootstrap (VETO)                │
                └──────────────────────────────────────┘
                          │                  │
                          │                  │
                  ┌───────┴──────┐    ┌─────┴───────┐
                  │ MaaS surface │    │ MaA surface │
                  │ (not compa- │    │ (not compa- │
                  │  rable to   │    │  rable to   │
                  │  MaA)       │    │  MaaS)      │
                  │             │    │             │
                  │  CPI        │    │  SI         │
                  │  TDR        │    │  ISR        │
                  │  MTC        │    │  FPR        │
                  │  CTD        │    │  COC-WORM-AR│
                  │  cache_hit  │    │  MBI = ½SBI+│
                  │             │    │       ½SI   │
                  └─────────────┘    └─────────────┘

           MaaS_Score = composite of MaaS-surface metrics
           MaA_Score  = composite of MaA-surface metrics
           M-core     = comparable across both categories
```

**Two-layer reading rule for the leaderboard:**

1. **Core M-series (M1-M11)** is the universally comparable layer.
   Any system can be scored on the M-series. Cross-system
   comparisons of M-scores are meaningful.

2. **MaaS_Score AND MaA_Score** are surface-specific composites.
   Comparing a system's MaaS_Score to another system's MaA_Score
   is a CATEGORY ERROR. They optimize for different things.

3. Public leaderboard shows:
   - M-series scores (universal)
   - System's declared category (MaaS / MaA)
   - System's category-appropriate composite score
   - **Not** cross-category ranking

## Why this matters for OSS release

Without this distinction, membench becomes a popularity contest
that incentivizes the wrong thing:
- A MaaS system tuned for low cost gets dinged on coordination
  depth → misses its actual goal
- A MaA system tuned for synthesis depth gets dinged on cost-per-
  query → misses its actual goal

With the distinction:
- Both categories get a HONEST core comparison (M-series)
- Both categories get a category-specific composite that REWARDS
  the right optimization
- Public users can pick the system for their actual use case
  (price-sensitive batch jobs → MaaS leader; deep investigation
   → MaA leader)

## Standard eval harness — best practices for friendly open competition

For membench to serve open competition between closed-source AI
memory products, the harness needs:

1. **Common units** — every M-metric is a number in [0, 1] (or
   clearly bounded). System-specific composites also in [0, 1].
   No raw counts in leaderboard rows.

2. **Reproducibility** — submissions include enough metadata that
   another team could re-run them: system version, model used,
   probe set, dataset, environment. Sealed via signed manifest +
   hash chain.

3. **Probe canon** — the M-series probes are CANON. No team
   modifies the probe; they only provide an adapter that lets
   their system answer the probe. Probe ≠ adapter.

4. **Adapter interface** — minimal + clear: `read_memory()`,
   `inject_probe()`, `collect_response()`, `shutdown()`. Any
   closed-source system can be tested by anyone with API access.

5. **Audit trail** — every submission carries the raw probe
   responses + the hash chain over those responses. Disputes can
   be replayed.

6. **Category declaration** — each system MUST declare MaaS or MaA
   when submitting. Misdeclaration is grounds for moderator review.

7. **Versioning** — probes are versioned (M1-v1, M1-v2). When a
   probe changes, scores tagged with version. Historical comparisons
   are version-locked.

8. **No closed-source secrets required** — adapters operate via the
   target system's public API. If a system can only be tested with
   internal access, it doesn't get a public score (or gets a
   "self-reported" tag).

9. **Carry-forward responsibility** — submissions older than 90
   days get a "stale" tag. Systems should re-submit periodically.

10. **Friendly competition tone** — leaderboard celebrates
    improvements in BOTH categories. No "X system is bad at Y" —
    instead: "X system optimizes for {category-appropriate metrics}
    and scores {value}."

## How swarmy fits

Swarmy is the **MaA reference implementation**. Its role in the
membench OSS release:

- Provide the canonical adapter (`adapters/swarmy.py`)
- Be the first system on the leaderboard (with full M-series
  scores + MaA_Score)
- Sponsor the framework's hosting + governance (initial
  maintenance burden)
- Self-evaluate honestly — publish its own scores including
  metrics where it underperforms

Swarmy MUST NOT use membench as a marketing tool. Membench's
credibility depends on being neutral. Swarmy provides the
reference impl + the first scores; it doesn't WIN the framework.

## The F-series side (swarmy-internal)

Per doctrine 15, swarmy maintains F1-F15 (its internal
implementations of M1-M15). The F-series stays inside swarmy;
the M-series is what's published to the leaderboard. Alignment is
maintained so swarmy can DEBUG itself with F-series and PROVE its
M-series scores derive from the same probe logic.

## Single-line summary

**Membench scores every system on a shared M1-M11 core (universally
comparable) and offers two surface-specific composites (MaaS_Score
and MaA_Score) for category-honest optimization. Cross-category
ranking is a category error. Swarmy is the MaA reference impl;
mem0/letta/zep-style systems would be MaaS reference impls. Open
competition is friendly because each category rewards its own
right thing, and the core stays comparable.**

---

*Companion to canonical `/mnt/d/0local/gitrepos/membench/BENCHMARKS-MAAS-VS-MAA.md`.
Closes the doctrine arc 08-16 for this session. The membench OSS
prep agent (ab1e8cfe) is mid-flight building the adapter surface,
README, and submission format — this doc gives the operator the
WHY behind the framework's two-surface design.*
