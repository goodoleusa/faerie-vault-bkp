---
type: narrative
status: active
created: 2026-04-20
tags: [literature, maas, maa, framework, scoring]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Equilibrium-Principle]]", "[[Switchboard-Principle]]"]
child: []
doc_hash: sha256:f196435f3799fb604bdbb016ae0e96d747da6061e3312406e47898f1f6e4bad7
hash_ts: 2026-04-20T21:59:39Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [← Equilibrium](Equilibrium-Principle.md) · [⌂ Home](../HOME.md)

# Memory-as-a-Service vs Memory-as-Architecture

## Two Fundamentally Different Use Cases

membench measures the same telemetry for two operators with incompatible optimization targets. Conflating them produces a metric suite that is mediocre for both. This document names the distinction so the composite scores can be applied correctly.

## Memory-as-a-Service (MaaS)

**Goal:** minimize cost per query. Financial incentive drives cheaper results.

The MaaS operator serves many thin clients — each session is independent, memory is retrieved and stuffed into prompts per-request, the system competes on price. Long-term learning is expensive and doesn't scale to millions of clients; so it doesn't happen. Every session starts cold.

**Primary metrics:** TDR (push work to cheapest agent), MTC (low main overhead), CTD (stay lean), CPI (cost per accepted output). Cache hit rate is king.

**Failure mode:** Agents refetch identical context every session. No compounding. Synthesis stays generic because deep inference isn't billable. The system provides answers, not understanding.

**What MaaS doesn't measure:** coordination depth, cross-session signal survival, emergent insight surfacing — these spend tokens and don't reduce per-query cost.

## Memory-as-Architecture (MaA)

**Goal:** context flows to perfectly fill agents; system continuously learns; insights surface before the human asks; forensic integrity is automatic; main session stays so lean it scales without limit.

The MaA operator serves one deep investigation or research team where losing session context means losing days of accumulated reasoning. Token cost is less important than flow preservation and compounding value.

**Primary metrics:** SI composite (OMR, MPL, SDR, CMR, CSS, BPR, CD, PCR), CTD (lean main = infinite scalability), WCR (wave completion), CD (cascade depth — autonomous chains), ISR (insight surfacing rate), FPR (flow preservation), COC-WORM-AR (forensic auto-upload).

**Failure mode:** none — agents crash-land but state survives in manifests and NECTAR. Each session builds on the last. The system gets smarter.

**What MaA doesn't optimize:** raw token minimization. Architecture spends tokens to preserve human time and context continuity. A deep-synthesis W3 agent costs 50K tokens and returns one insight that reshapes the investigation — MaaS would flag this as expensive; MaA reads it as the whole point.

## Comparison

| Dimension | MaaS | MaA |
|-----------|------|-----|
| Optimizes for | $/token | human flow + compounding context |
| Main session weight | minimize all reads | minimize writes (stays thin for routing) |
| Coordination | direct prompting | stigmergy |
| Learning | per-session | cross-session (NECTAR/HONEY pipeline) |
| Failure signature | generic answers, no learning | none (state survives crashes) |
| Metric stack | TDR, MTC, CTD, CPI | SI, CTD, WCR, CD, ISR, FPR, COC-WORM-AR |
| Dashboard headline | cost-per-query trend | session health (MBI) + flow rate (FPR) |

## Composite Formulas

Two separate composites from the same telemetry:

```
MaaS_Score = (1 - norm_CPI) * 0.40
           + TDR             * 0.30
           + (1 - CTD_norm)  * 0.20
           + cache_hit_rate  * 0.10

MaA_Score  = SI              * 0.35
           + (1 - CTD_norm)  * 0.25
           + WCR             * 0.15
           + min(CD/3, 1.0)  * 0.10
           + ISR_norm        * 0.10
           + FPR             * 0.05
```

Note: MBI (SBI + SI) is the **MaA** health metric. MaaS_Score is a separate composite for MaaS operators.

## Why Two Frameworks Matter

A system can be benchmarked against both. An honest vendor publishes both scores so buyers understand which product they're actually purchasing. A system with MaaS_Score = 0.92 and MaA_Score = 0.41 is an excellent query-answering service and a poor deep-investigation platform. Neither score is wrong; they measure different things.

Faerie is a MaA system by design. Its MBI is the correct health indicator. Applying MaaS scoring to faerie would penalize the deep synthesis and coordination behaviors that make it valuable.

## Related Metrics

- [[../00-Metrics/ISR-Insight-Surfacing-Rate|ISR]] — MaA surfacing
- [[../00-Metrics/FPR-Flow-Preservation-Rate|FPR]] — MaA flow health
- [[../00-Metrics/CPI-Cost-Per-Insight|CPI]] — MaaS efficiency
- [[../00-Metrics/COC-WORM-AR-Auto-Route-Rate|COC-WORM-AR]] — MaA forensic automation
- [[../00-Metrics/MBI-Membench-Index|MBI]] — MaA composite
