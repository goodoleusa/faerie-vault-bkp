---
title: "Executive Briefing — The Swarmy Substrate (1-Page)"
date: 2026-05-25
status: spray-D — executive distillation
authors: [Amanda Morton, Claude Opus 4.7, the Swarmy collective]
crystal: 2026-05-25-arxiv-draft-forensic-stigmergy.md
target_audience: customers, business development, investor due-diligence
length: one page (~800 words)
discipline: "Every claim cites a specific section in the crystal arxiv draft. No claim originates here."
sprays:
  - 2026-05-25-court-admissible-evidence-chain.md (legal architecture)
  - patent/2026-05-25-PROVISIONAL-PATENT-APPLICATION-v2-SIMPLIFIED.md (legal claims)
  - 2026-05-25-MEGA-REPORT-token-economics-and-real-numbers.md (financial)
---

# Swarmy — Executive Briefing

## The thesis (one sentence)

Swarmy is a coordination substrate for multi-agent LLM systems that ships **forensic-grade evidence chains** + **constant-cost coordination scaling** + **observation-driven design discipline** in one composition, validated empirically at production scale and engineered specifically for high-stakes adoption [arxiv §1].

## The three load-bearing properties

**1. The coordination cost is constant in agent count, not linear.** Vanilla multi-agent LLM systems (AutoGen, MetaGPT, ChatDev) consume ~140K orchestrator tokens for a 4-agent wave on the same task scope. Swarmy consumes ~400 measured tokens — a 99.7% reduction, structural not incremental. By N=10 agents, vanilla orchestrator architectures cannot run (exceed 200K context window on coordination alone). Swarmy runs cleanly at N=50+ because the bundle composition happens in subprocess, not in the orchestrator's LLM context [arxiv §7.1(a)].

**2. Every action is cryptographically tamper-evident.** Every agent execution writes three simultaneous evidence layers: raw session transcript (Claude Code session jsonl, archived), signed manifest (Ed25519 per agent_type), COC hash chain (SHA-256 prev_entry_hash linkage). 1,686 sessions / 11.3B tokens / 628.9 MB of evidence currently anchored. The mission graph's edges ARE cryptographic pointers into the COC ledger — tampering the graph requires tampering the chain, and chain verification catches it [arxiv §3, §7.7].

**3. Doctrine is observation-driven, not synthesized.** The substrate's canonical primitives (14-kind completion-choice taxonomy; seven-lens refusal framework; lifecycle-judgment vs free-choice agency split; mission-graph compass-bearing routing) emerged from actual agent behavior observed in production, not from designer guessing. Vanilla AI without the substrate has no equivalent observation source; reaching equivalent depth would take 5-15× more sessions of conjecture-correct cycles and may not converge to the same answer [arxiv §10 observation-driven design].

## What this means for adoption

In high-stakes domains (medicine, law, journalism, precision manufacturing, financial services), AI output is useless if it cannot be defended in adversarial proceedings. Swarmy's four-tier evidence chain (Tiers 1–3 operational today; Tier 4 public-anchor via Sigstore Rekor in the corresponding charter pre-reg) makes adoption defensible by construction — the customer's expert witness can walk the court through every agent tool call, every chain-of-thought chunk, every meaningful action, with hostile-counsel verification possible without trusting the customer or the substrate provider [court-admissible-evidence-chain doc + arxiv §3.4].

## Empirical validation (today, 2026-05-25)

- Two multi-agent waves: 4-agent VISIONARY+ARTISAN (40 files, 8,533 lines, zero file collisions, 1 explicit live handoff) and 5-agent branching/merkle (167 files, 23,463 lines, 14/14 cryptographic tests pass, zero collisions despite tight import dependencies)
- Sandwich-measured cross-skill doctrine propagation: refusal-doctrine reachability lifted from 2 to 8 lifecycle skills in 45 minutes, mechanically verified
- 97.3% cache-read fraction on the 32-day session corpus — saves ~$120,000 vs the same workload without prompt caching; this is the structural property that makes the substrate economically viable for single-operator deployment [mega-report §3]
- Operator coordination messages during the largest multi-agent wave: zero. The substrate carried the routing [arxiv §7.1(d)]

## What's shipped vs what's in-flight

| Shipped today | In-flight | Charter pre-reg |
|---|---|---|
| Ed25519 signing operational (pynacl installed both venvs); branching/Merkle/handshake; mission_graph consolidated 11→1 canonical script; OpenHands continuous archival cron (15-min cadence + PostToolUse hook); Claude Code session archive (1,686 sessions hash-anchored); doctrine refactor (lifecycle-judgment vs free-choice split + seven-lens refusal across 8 skills); patent provisional v2 (19 claims); arxiv draft with 49 verified citations | COC genesis-seal (closes mixed-schema gap; freezes v1, starts v2 clean); OH SDK tool perms (terminal+file_editor+grep+glob+task_tool_set) | court-admissible-evidence-chain (8 phases: signing, continuous capture, reproducibility manifest, Rekor anchoring, schema unification, WORM backup, discovery export tool, notarized operator attestation) |

## The honest disclosure

LLM output is non-deterministic at temperature > 0. The substrate captures what happened, not what would deterministically replay. Authorship is attributed at the agent_type level (the role), not the specific model instance — though model + version are captured per-message in transcripts. Cross-session memory consolidation is in active development; current membench composite scores 48 (operational dimensions strong: M3/M5/M6 ≈ 95; memory dimensions failing: M1/M2/M7 = 0). The orchestration substrate is mature; the memory substrate is still maturing. Both are reported with full transparency [arxiv §7.7, §8.2].

## What this isn't

Swarmy is not an LLM, not a model, not a foundation-layer training system. It is the **coordination + forensic-anchoring substrate** that sits on top of any LLM (Claude Code today; OpenHands SDK for prod; portable to other agentic runtimes). The substrate's value is independent of which model executes the agents.

## Who should care

- **Medical AI / clinical decision support** — every diagnostic suggestion needs malpractice-defensible provenance
- **Legal e-discovery / litigation tech** — chain-of-custody is the entire product
- **Investigative journalism** — source-protection + audit trail without exposing methods
- **Precision manufacturing / financial compliance** — regulator-defensible audit trails for AI-mediated decisions
- **Any startup building multi-agent LLM products** that hits the orchestrator-context cliff at N≈4–6 agents

## Where to read further

- **Crystal (full empirical paper, arxiv-target):** `2026-05-25-arxiv-draft-forensic-stigmergy.md` — every claim above derives from this document
- **Legal architecture:** `2026-05-25-court-admissible-evidence-chain.md` (court-admissibility 4-tier trust model)
- **Financial:** `2026-05-25-MEGA-REPORT-token-economics-and-real-numbers.md` ($14,939 measured vs $135K counterfactual)
- **Patent:** `patent/2026-05-25-PROVISIONAL-PATENT-APPLICATION-v2-SIMPLIFIED.md` (19 claims, 21pp)

---

*Spray-D executive distillation, 2026-05-25. Crystal-and-spray discipline: every claim above traces back to a specific anchor in `2026-05-25-arxiv-draft-forensic-stigmergy.md`. No claim originates in this document. If a claim feels novel, the spray is broken; check the crystal.*
