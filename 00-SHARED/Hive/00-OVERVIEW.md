---
type: meta
tags: [meta, overview, philosophy, onboarding]
created: 2026-03-11
updated: 2026-03-24
doc_hash: sha256:163d45a9dfba100db77e19d46a270fbd4a14c5366a655934f79167f206f2dcfa
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

# CyberOps Vault — Overview

Start here for the big picture. This vault is the **collaboration and memory surface** for agentic investigation — the **conceptual home** where humans and agents read, write, and promote. **Original forensic masters** belong in your **investigation repo** under **chain-of-custody (COC)**; see *Data sovereignty* below. The **problem** statement and **design principles** are here so the rest of the docs stay easy to follow.

---

## The problem (multi-fold)

**(a) Compute divide + missing orchestration**  
The gap between Big Tech AI labs (evals, alignment research) and the average person is **diminishing for the first time ever**. What we’re missing now is not raw compute but the **orchestration layer** — how to route work, share context, and collaborate at scale.

**(b) Research isolation vs diverse perspectives**  
Research is isolating but is **always better with diverse perspectives and new ideas**. People digging stuff up need a way to combine viewpoints without needing to be in the same room or org.

**(c) Institutional burden**  
The work of getting money, assembling a team, parceling out collections, and validating results is **arduous** and usually needs institutional support. An async AI swarm gives you the team; you focus on high-level direction and promotion.

**(d) AI-specific fears**  
- **Unsure of AI costs before send** — you don’t know what a run will cost.  
- **Unsure what’s happening to your data** — where it goes, who sees it.  
- **Sensitive topics** — if you research sensitive topics you miss the benefits of AI because you don’t want to give your data away.

**(e) OSINT coordination and understanding**  
Not enough coordination in the online OSINT community. OSINT is not well understood by casual users who like researching online — it’s not just some tools, it’s a **whole methodology of validating reality with evidence**.

---

We make it as simple as possible: here are the design principles and metaphors that address this. Everything else follows.

---

## Core design principles

- **One shared collaboration record:** Agent handoffs, promoted narrative, and human steering live in **this vault** (no hidden “model-only” reasoning for work that matters). **COC originals** (audit matrices, raw run artifacts) live in the **investigation repo** — the vault links and summarizes; masters stay under chain-of-custody.
- **Human gates change:** Nothing the swarm does alters the shared record until a human promotes it. *Human promotes, AI executes.*
- **Reproducible by design:** Same inputs + same pipeline → same outputs. Steps are logged; runs are tagged; you can replay how a conclusion was reached.
- **Cost visible before it happens:** Model routing, caching, and batching are explicit; you can estimate (or cap) cost per run or per task.
- **Compartmentalization:** Tasks and collections don’t leak into each other. One thread of work doesn’t contaminate another (dead reckoning).
- **Asynchronous by default:** Researchers and agents don’t have to be online at once. The vault is the meeting point.

---

## Values and metaphors

- **Bee metaphor:** *“Scout bees don’t report to a manager. They fly out, find something, come back, and dance. The hive listens. The best dance wins.”* — Agents write to the shared vault (the dance floor). Humans observe the dances and approve which findings become part of the story.
- **Dead reckoning:** Each collection (or task batch) is self-contained. You can hand 50 collections to 50 volunteers; each has everything needed to run. No silent dependency on “what the main agent had in context.”
- **Vault as waggle dance:** The vault is the only place agents “speak.” No direct agent-to-agent chats; no disappearing context. If it mattered, it’s in the vault — readable, archivable, auditable.
- **Queen protocol:** Humans set direction and approve; the swarm proposes. Automation doesn’t replace judgment; it extends it.

---

## Solving the black box problem

| Fear | How the design addresses it |
|------|-----------------------------|
| **“I don’t know how the agent decided.”** | Every material step is written into the vault: hypotheses, data used, conclusions, handoffs. No reasoning lives only in chat history. You read the same record the next agent (or human) reads. |
| **“I can’t reproduce their steps.”** | Pipeline is deterministic: same inputs + same run spec → same outputs. Runs are tagged; logs and manifests are kept. Reproducibility is a design goal. |
| **“I don’t know how much a run will cost.”** | Model routing (Haiku/Sonnet/Opus by task type), prompt caching, and batch discounts are built in. Cost is predictable and visible; you can estimate or cap before running. |
| **“Automation will create more problems and ruin important data.”** | Raw agent output never overwrites the shared record. Humans promote what’s good; the rest stays in staging. Data is immutable once promoted; hashes and chain of custody support integrity. |
| **“I don’t want to give my data away — especially on sensitive topics.”** | Your **forensic originals** stay in **your** investigation repo under **chain-of-custody (COC)**; the **vault** is your readable collaboration home. Local-first and offline-capable; no requirement to send raw evidence to third-party clouds. You choose what gets promoted, what syncs to a managed service, and where it goes. |

**These principles and metaphors exist so you don’t have to trust a black box.**

---

## Data sovereignty — three layers: vault, COC repo, optional managed service

**The promise of sovereignty.** **Data sovereignty** means you hold **custody, inspectability, and promotion authority** over your work: you see **how** conclusions were reached (trails, hashes, COC where it applies); you decide **what** leaves your machines and **when**. Vendors and hosted layers are **tools**, not owners of your case.

---

### 1) The vault — conceptual *home* (collaboration & memory surface)

The **Obsidian vault** is the **conceptual home** for how you and agents **think together**: wikilinks, dashboards, human review, inbox flags, queue stubs, and promoted narrative you actually *read* every day. It is the **shared language** of the investigation — the place partners open to stay aligned.

It is **not** where **original forensic masters** are required to live. Treat the vault as **operational and narrative custody** (what the team sees and steers), not as the sole chain-of-custody archive.

---

### 2) The investigation repo — *original* forensic copies under COC

**Authoritative forensic originals** (raw extracts, audit matrices, run manifests, hashes, pipeline outputs you would defend in review) should live in your **investigation / CyberTemplate repo** (or equivalent) and be governed by your **chain-of-custody (COC)** rules: versioning, manifests, `scripts/audit_results/`, `~/.claude/memory/forensics/` (or your org’s path), and explicit promotion from agent staging.

The vault **mirrors, summarizes, and hands off**; the **repo + COC system** holds the **masters** you rely on for reproducibility and defensibility.

---

### 3) Managed memory / hosted service — *optional* processor

**Managed memory** (or a similar hosted offering) is **optional**. If you enable it, it exists to **deepen synthesis, routing, and continuity** on **slices you explicitly allow** — never to replace your repo masters or your promotion discipline.

**Model APIs** (every prompt to a frontier model) are separate: they process **that request’s** text; design prompts so case-breaking secrets stay local unless you intend otherwise.

---

### What lives where (quick map)

| Kind of data | Typical home | Notes |
|--------------|--------------|--------|
| Original runs, audit JSON/CSVs, bulk hashes, court-grade bundles | **COC repo** (e.g. CyberTemplate) | Masters for reproducibility and review |
| Human-readable findings, flags, queue, `HONEY` / `NECTAR` narrative, dashboards | **Local vault** (often `00-SHARED/` for agent writes) | Collaboration and steering surface |
| Chat-only scratch | **Ephemeral** unless you paste or sync | Compaction loses it; file-backed memory fixes that |

---

### If you use a **hosted managed memory** service — what may cross the wire

*Exact categories depend on your product settings and agreement; defaults should minimize exposure.*

| Usually **stays on your disk** | **May** be sent **only if you opt in** to hosted memory / sync |
|--------------------------------|------------------------------------------------------------------|
| Raw evidence files and full forensic masters in the **COC repo** | **HONEY-class** or similarly **crystallized** workflow packs (methods, preferences, non-sensitive patterns) you approve for sync |
| Full **NECTAR** / case narrative unless you export it | Redacted summaries or embeddings **you** choose to upload |
| Vault copies of sensitive notes | Routing metadata, session structure, or queue state **if** the product sends them — **read the service’s data handling** |

**Rule of thumb:** COC originals stay in the **repo**; the vault holds **what humans and agents coordinate on**; the **managed service** sees only **policy-allowed, user-approved** slices — never “the whole disk” by default.

---

### Why a **custom file-backed memory** (faerie-style) is worth it

- **Beyond a single session:** Promoted intelligence survives compaction; queues and inbox survive overnight and handoffs.
- **Individuals and small teams:** One person gets **continuity** like a lab notebook; a team gets a **shared surface** without everyone re-briefing the model.
- **Crystallized intelligence:** **HONEY** (how to work) and **NECTAR** (what you validated) separate **process** from **substance** so both stay maintainable and teachable.
- **Same system, portable folders:** Partners who use the **same vault layout + COC repo conventions** can **swap investigation folders**, **drop in a shared `00-SHARED` handoff**, or **sync via Syncthing / dead-drop** and understand the structure immediately — **shared expertise without shared logins**.
- **Overcoming blockers:** When you’re stuck, aligning on **one vault + one repo contract** lowers friction to **join a research network**: you contribute a slice, others contribute theirs, promotion and COC keep quality legible.

**HONEY vs the rest of the hive.** **HONEY** = crystallized **process** (methods, gates, preferences). **NECTAR** and case bodies = promoted **substance** tied to investigations — still **your** files until you export. See [[00-SHARED/HOW-SYNC-WORKS]] for sync boundaries and delivery hashes.

**Faerie / file-backed memory — what you gain.** `HONEY`, `NECTAR`, inbox, queue, and agent cards turn **opaque chat** into **inspectable, linkable state**; improvement is **reproducible** (same inputs + pipeline + promotion) and **compatible with COC** when originals stay in the repo.

**Bottom line:** **Vault** = conceptual collaboration home. **COC repo** = forensic masters. **Managed memory** = optional depth on approved slices. Sovereignty = **you** define that split and **you** promote across it.

---

## Why this exists: OSINT, public intelligence, and the crossroads

OSINT is changing intelligence collection. This project believes intelligence should be **shared with and easily understood by the public** — and that the public should be **able to participate**. As we joke: this is an example of a **decentralized intelligence agency**. Lots of people are digging stuff up and want to do something with it; they need a way to collaborate without a central authority.

- **Crossroads:** A meeting point for researchers who need help **safely distributing work to anonymous collaborators**. You don’t have to know who ran which task; the vault and pipeline let you **check the quality of work** (reproducible runs, review, promoted findings) without knowing who did it.
- **Era of political repression:** Not knowing your collaborator is a **protective factor** — **security by deniability**. Compartmentalization and dead reckoning mean each contributor can work on a slice without exposing others; the lead researcher can still assess and promote results. The design supports: public-facing, participatory intelligence *and* safe, anonymous collaboration with verifiable quality.

---

## Why 2026: orchestration and optimization

One model, one context worked until the work got bigger. By 2026 the bottleneck is **orchestration and prompt discipline**, not model size.

- **2023:** One context, quadratic cost — same tokens rebilled every turn.
- **2024:** Specialized models (RLHF), but still one-context-by-default; cost and bias scale with conversation length.
- **2026:** Models are as capable as ever; **orchestration and optimization** decide outcomes. Scalability, zero-waste, immutability, self-evolution, decentralization, async, truth-seeking, and active archiving become the design goals.

---

## [entity-name]: the 2026 standard

Self-evolving swarm; vault as waggle dance; human–AI dyad. Philosophy:

- **Scalability** — Linear cost growth via parallel, isolated agents.
- **Immutability** — All findings archived in a tamper-evident vault.
- **Zero-waste** — Prompt caching and model routing reduce token costs.
- **Self-evolving** — The system iterates its own workflow from friction logs (PAIN/IDEA → Memory-Keeper).
- **Decentralized** — No single point of failure or bias; consensus emerges from the swarm.
- **Asynchronous** — Work continues while humans sleep; collaboration across time zones.
- **Active archiving** — The process of discovery is preserved as a living knowledge base.

---

## Human–AI dyad

AI as partner, not replacement. Cross-dyad collaboration: your AI partner can meet with a colleague’s AI partner in the vault to synthesize findings and challenge assumptions. **Queen protocol:** humans retain final authority. The swarm proposes; the human disposes.

---

## Key features (compact)

- **Epistemic integrity:** Hypothesis agent (blind to results) → Analysis agent (blind to hypothesis) → Adversarial reviewer. Reduces p-hacking and recency bias.
- **The vault:** Single channel, immutable. Agents communicate only through the vault; no direct handoffs.
- **Cost engine:** Model routing, prompt caching, batch discounts.
- **Self-evolution:** PAIN/IDEA logs → Memory-Keeper reviews → improvement proposals.

---

## What this vault is

This vault is the **shared knowledge engine** for OSINT investigations where humans and AI agents collaborate asynchronously. It is the **collaboration surface** — agents read and write within policy (mostly **`00-SHARED/`**); **forensic masters** stay in your **COC repo**. See [[KICKSTART-COLLAB]] to start dropping tasks and briefs in the right folders. It embodies **public, participatory intelligence** and serves as a **crossroads** for researchers distributing work to anonymous collaborators: **security by deniability**, **quality by design** (you can verify work via the vault and review without knowing who did it). Dead reckoning, compartmentalization, scaling without losing control, human at the center, integrity, reproducibility, offline-first.

---

## Where to go next

| Next step | Doc |
|-----------|-----|
| **Kickstart collab** | [[KICKSTART-COLLAB]] — task/inbox paths under `00-SHARED/`, naming (no new numbering except protected/private). |
| **Technical architecture** | [[01-ARCHITECTURE]] — topology, folder layout, task lifecycle, memory, pipelines. |
| **QuickAdd + Blueprint setup** | [[02-QUICKADD-SETUP]] — step-by-step setup. |
| **QuickAdd global vars (handoff)** | [[04-QUICKADD-GLOBAL-VARS-HANDOFF]] — HandoffBlock, ResearchFolder, contract. |
| **Full doc index** | [[00-README]] — suggested topic order; meta filenames keep numbers for sort only. |

---

## Legal and compliance

UNCLASSIFIED // FOR PUBLIC RELEASE. All evidence from publicly available sources or authorized disclosures. No autonomy/replacement claims — data stays in your vault; orchestration framework; users responsible for data sources. Audit-ready: immutable, timestamped records of the investigative process.

---

## Business value (short)

- **Cost predictability** — Reduce AI inference costs through model routing and prompt caching; variable API bills become fixed, scalable operational expenses.
- **Complementary cognition** — Human strategic oversight + AI speed and data processing; reduced cognitive bias, better accuracy in high-stakes investigations.
- **Audit-ready intelligence** — Immutable, timestamped records of hypothesis, data, and counter-arguments; defensible audit trail for compliance and regulatory review.
