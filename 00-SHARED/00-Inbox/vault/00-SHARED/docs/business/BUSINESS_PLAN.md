---
type: business
status: active
created: 2026-04-21
tags: [business, plan, strategy]
up: README.md
next: SURVIVAL_LAUNCH_PLAN.md
---

> [↑ Readme](README.md) · [→ Survival Launch Plan](SURVIVAL_LAUNCH_PLAN.md) · [⌂ Home](../../README.md)

# faerie — Business Plan & Market Analysis

> **North star product metric:** I/F ratio (Insight-to-Friction).
> Every feature ships to raise it. Every pricing tier reflects it.

---

## What We're Building

**faerie is a memory orchestration middleware layer** that sits between any Claude API application and the LLM. It does three things no existing product does together:

1. **Crystallizes** accumulated knowledge into compressed, prompt-injection-ready HONEY
2. **Transforms** the user's incoming prompt using that crystallized knowledge — not just appends to it
3. **Measures** the ratio of insights produced to friction encountered (I/F), using that signal to continuously improve itself

The result: users who use faerie for 6 months get better outputs from shorter prompts than new users get from longer ones — because the HONEY is the moat.

---

## Competitive Landscape

### Memory Management Middleware (primary competitive space)

| Product | Memory Model | Prompt Transform? | Crystallization? | Forensic Logging? | Open Source | Pricing |
|---------|-------------|------------------|-----------------|-------------------|-------------|---------|
| **Mem0** | Vector store; extracts facts, injects as appended context | No — appends, doesn't rewrite | No — stores raw extractions | No | Core OSS, cloud paid | ~$25/mo personal, enterprise custom |
| **Zep** | Temporal knowledge graph (Graphiti); episodic + semantic memory | No — injects alongside, doesn't rewrite | No — summarizes, doesn't crystallize | No | OSS community edition, cloud paid | ~$49/mo starter, enterprise custom |
| **Letta / MemGPT** | Two-tier (core/archival); OS-inspired; recursive summarization on eviction | No — manages window, doesn't rewrite input | Partial — recursive summarization is compression, but not knowledge crystallization | No | Fully OSS + cloud | OSS free, cloud ~$20/mo |
| **LangChain Memory** | ConversationBufferMemory, SummaryMemory, VectorStoreMemory | No | No | No | OSS | Free (framework) |
| **faerie** | SEED/LOG/HONEY/STATE/VOID — crystallized + prompt-transformed | **Yes — transforms user prompt using HONEY** | **Yes — hard token budgets, merge-before-write** | **Yes — append-only reasoning.jsonl, full chain of custody** | Yes (CLI), SDK planned | See pricing below |

### Prompt Compression Tools (adjacent space)

| Product | What it compresses | Personalized? | Memory-aware? | Pricing |
|---------|-------------------|---------------|---------------|---------|
| **LLMLingua / LLMLingua-2** | Long prompts, RAG chunks, document context | No — generic compression | No | Open source (Microsoft Research) |
| **ACON** | Conversation history | No | No | Research paper only |
| **Microsoft Prompt Flow** | Integrates LLMLingua | No | No | Azure-priced |
| **faerie** | User's natural language query using HONEY context | **Yes — personal knowledge drives compression** | **Yes — HONEY is the compression context** | See pricing below |

### Context Engineering Tools (emerging space)

| Product | Approach | Memory layer? | Prompt transform? |
|---------|----------|--------------|-------------------|
| **DSPy** | Offline prompt optimization via compilation | No | Template optimization only |
| **OPRO / promptim** | Iterative prompt improvement against dataset | No | Batch, not real-time |
| **LlamaIndex** | RAG orchestration + context construction | Vector store only | No |
| **faerie** | Real-time context engineering using accumulated HONEY | Yes (crystallized) | Yes (personal) |

### Investigation / OSINT Tools (vertical application space)

| Product | Memory | Collaborative? | AI-native? | Chain of custody? | Pricing |
|---------|--------|---------------|-----------|-------------------|---------|
| **Maltego** | No persistent AI memory | Limited (team licenses) | Partially | Partial | $999+/yr |
| **Palantir Gotham** | Proprietary graph | Enterprise | Yes | Yes | Enterprise (millions) |
| **Gephi** | No | No | No | No | Free |
| **i2 Analyst's Notebook** | No | Limited | No | Partial | Enterprise |
| **faerie** | Full HONEY + STATE + reasoning.jsonl | Multi-hive federation | **100% AI-native** | **Full forensic chain of custody** | See pricing below |

---

## The Three Gaps Faerie Fills

### Gap 1: Nobody transforms the user's prompt

Every memory product **appends** context to the user's message. Mem0 says: "here is what I remember — now go answer the user's original question." The original question arrives at the LLM unchanged.

Faerie **rewrites** the user's question using HONEY. "What's the deal with that domain cluster" becomes a precision-targeted 80-token prompt that the model can answer specifically. This is a qualitatively different product.

**Market evidence for the gap:** LLMLingua exists for compressing long context. Mem0 exists for injecting personal memory. Nobody is combining them — rewriting the user prompt using crystallized personal knowledge. The gap is between these two product categories.

### Gap 2: Nobody crystallizes — everyone accumulates

Mem0 grows as you use it. Zep's knowledge graph grows. Letta's archival memory grows. Every memory product gets larger over time, which means every API call gets more expensive over time.

Faerie applies the **crystallization law**: every write to a durable file must be a distillation, not an append. HONEY never grows past its token budget. The system gets denser, not larger. This means API costs decrease over time as the HONEY becomes more efficient, not increase.

**Market evidence for the gap:** No memory product currently measures token budget of its memory store or enforces a hard compression schedule. This is an unaddressed problem that every enterprise customer of Mem0/Zep/Letta will eventually face.

### Gap 3: Nobody has forensic-grade memory for professional investigators

Maltego and Palantir are built for enterprises. Free tools have no memory. Nothing in the market is designed for the independent investigator, journalist, or forensic researcher who needs:
- Full chronological chain of thought preserved across sessions
- Data transform audit trail with before/after hashes
- Multi-machine coordination without a central server
- Confidence-scored findings with provenance
- Dead-end mapping so work is never duplicated

This is a niche but high-value market: investigative journalists, human rights researchers, forensic accountants, compliance investigators, legal discovery teams. They currently use Maltego + spreadsheets + manual notes. No AI-native solution exists at their price point.

---

## Market Sizing

### Memory Middleware (addressable near-term)

- Claude API monthly active developers: est. 500K–1M (Anthropic has ~$500M ARR as of 2025)
- Fraction who would pay for memory middleware: est. 10–15% = 50K–150K
- Target: power users doing repeated domain work (legal, research, investigation, analysis)
- Willingness to pay: $20–$100/mo (comparable to Mem0/Zep pricing)
- Near-term TAM: $12M–$180M ARR

### Context Engineering Middleware (medium-term)

- Enterprise LLM deployments needing prompt optimization: large and growing
- Players: Salesforce, ServiceNow, enterprise legal/compliance → every domain that accumulates knowledge
- WTP: $500–$5,000/mo enterprise tier
- Medium-term SAM: difficult to size precisely; comparable to Zep's $10M+ ARR trajectory

### Professional Investigation Tools (vertical — best beachhead)

- Investigative journalists worldwide: ~50,000 professionals
- Human rights researchers, NGOs: ~10,000 orgs
- Forensic accountants/compliance: ~100,000 professionals
- Legal discovery teams: large enterprise market
- Beachhead TAM: ~160,000 potential users at $50–$200/mo = $96M–$384M ARR potential

---

## Pricing Model

### Personal (CLI, open source + cloud sync)
**Free / self-hosted** — full system, bring your own API key
- Full SEED/LOG/HONEY/STATE architecture
- Local crystallization
- Single-machine only
- Community support

**Pro: $29/mo**
- Hive sync (multi-machine via Obsidian/cloud)
- I/F ratio dashboard
- 5 investigation threads
- Up to 3 hive members

### Team (multi-hive federation)
**Team: $99/mo (up to 10 members)**
- Full federation protocol
- Shared HONEY with provenance
- Swarm task routing (human + AI)
- Priority support

### Professional Investigation
**Investigator: $199/mo**
- Unlimited investigation threads
- Full forensic reasoning log with export
- Chain of custody signatures
- Dead-drop multi-hive coordination
- Chain-of-evidence legal export format

### Enterprise / API SDK
**Custom pricing**
- Faerie as middleware in any Claude API application
- White-label
- SLA + support
- Volume discounts

---

## Go-to-Market: Beachhead Strategy

**Phase 1: Forensic investigator community (months 1–12)**

Why start here:
- High pain, high stakes — every friction point costs real investigation time
- Strong word of mouth (investigators talk to investigators)
- Pro-social OSINT creates organic press coverage
- Their use case is the hardest version of the problem — if faerie works for investigators, it works for everyone

Target channels:
- OSINT community (Bellingcat, OCCRP affiliates, investigative journalism networks)
- Academic human rights research (Amnesty Tech, Human Rights Data Analysis Group)
- Legal discovery teams at boutique law firms (large firms are too slow to adopt)

Positioning: *"The AI memory layer for serious investigators. Every insight preserved. Every dead end mapped. Every transform auditable. Chain of custody by default."*

**Phase 2: Knowledge workers using Claude for repeated domain work (months 12–24)**

Expansion via API SDK:
- Any Claude-powered application can embed faerie middleware
- Target: legal research tools, compliance platforms, medical literature tools, financial analysis
- Revenue model shifts from direct subscription to SDK licensing (per-API-call or flat monthly)

**Phase 3: Enterprise context engineering middleware (months 24+)**

At this point:
- HONEY crystallization and prompt transformation are proven at scale
- I/F ratio is a recognized product metric (we will have published on it)
- Enterprise customers are facing the "memory bloat" problem with Mem0/Zep
- Faerie positions as the crystallization layer that makes other memory products more efficient

---

## Moat Analysis

| Moat type | Strength | Notes |
|-----------|----------|-------|
| **Data flywheel** | Strong | HONEY compounds — 6 months of crystallized knowledge can't be copied |
| **Switching cost** | Medium | reasoning.jsonl contains years of investigation reasoning — hard to migrate |
| **Network effect (federation)** | Emerging | Dead-end sharing across hives → more hives = less duplicated work for everyone |
| **Brand in forensic/OSINT** | Achievable | Small community, high trust required — early mover advantage is real |
| **Technical** | Moderate | Crystallization law + prompt transformation is novel combination; copyable but time-to-implement is 6-12 months |

The primary moat is **the data flywheel**: a user's HONEY is worth more the longer they use faerie, and that accumulated HONEY produces compounding cost savings and output quality improvements that a new installation cannot replicate. The moat grows with usage.

---

## Novelty Assessment (from competitive research)

**Known art (not novel):**
- Prompt compression techniques (LLMLingua) — mature research
- LLM memory injection (Mem0, Zep, Letta) — active product category
- RAG as context retrieval — ubiquitous
- Friction metrics for digital products — established

**Novel combination (not done together):**
- Combining prompt compression with personal memory injection in a single pre-API transformation step
- Memory products append; faerie transforms. Small architectural distinction, large UX difference.

**Genuinely novel (not in current literature):**
- "Crystallized knowledge" as a distinct memory artifact: pre-distilled, token-budgeted, prompt-injection-ready — not raw retrieval chunks
- Insight-to-friction ratio as a first-class AI product metric (not named or formalized anywhere)
- The full chain: crystallize → transform user prompt → compressed API payload → measure I/F — as a unified system
- Forensic-grade reasoning log (investigation-scoped, cross-session, chain of custody) for AI investigation workflows

**Honest summary:** The closest prior art is Mem0 (personal memory injection) + LLMLingua (compression). Neither does the other's job. The specific combination — plus crystallization law, I/F ratio, and forensic logging — is a novel system-level architecture even if individual components have precedent.

---

## Key Risks

| Risk | Mitigation |
|------|-----------|
| Anthropic ships native memory | Faerie provides investigation-specific features (forensic log, COC, multi-hive) that Anthropic won't prioritize. Also: faerie is model-agnostic. |
| Mem0/Zep adds prompt transformation | They would need to add crystallization + compression in one step — 6-12 months to implement well. First-mover HONEY advantage still applies. |
| Small forensic market doesn't generate enough revenue | Forensic is the beachhead. API SDK opens the broader market in year 2. |
| Open source commoditization | Core is open. Moat is the data flywheel (HONEY) and the hosted sync service — not the code. |
| User doesn't understand value prop | I/F ratio dashboard makes value visible. "You found 9 insights and hit 1 friction point this week. Three months ago it was 3 insights and 7 friction points." |

---

## Key Metrics to Track (investors / founders)

| Metric | Target by month 6 | Target by month 12 |
|--------|------------------|--------------------|
| Weekly active investigators | 50 | 500 |
| Average I/F ratio across users | > 3.0 | > 5.0 |
| SEED compression ratio | > 8:1 | > 12:1 |
| Session return rate (weekly) | > 60% | > 75% |
| HONEY entries per user (density signal) | > 200 | > 500 |
| Paid conversion (free → pro) | > 10% | > 20% |
| NPS | > 50 | > 70 |

---

## The Pitch in One Paragraph

Every AI memory product today works the same way: it remembers things about you, then pastes those memories into the prompt alongside your question. The original question arrives at the model unchanged, the context window bloats over time, and API costs grow as memory grows. Faerie is different: it crystallizes accumulated knowledge into a compressed form that never grows past its token budget, then uses that knowledge to transform your question itself — not to augment it. The result is a smaller, smarter API call that produces better output than the original question could have. The longer you use faerie, the better your questions get, automatically. The moat is your HONEY. The metric is your I/F ratio. The market is everyone who uses AI to do serious repeated work — and doesn't want to start from scratch every session.
