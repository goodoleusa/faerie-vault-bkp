---
title: "USPTO Provisional Patent Application v2 — Forensic Stigmergy: Multi-Agent LLM Orchestration with Hash-Chained Mission Graphs, Real-Time Stigmergic Blackboards, and Merkle Branch Architecture"
date: 2026-05-25
version: v2-simplified
status: DRAFT — attorney review required before USPTO filing
filing_basis: 35 U.S.C. § 111(b)
related_draft: PATENT-APPLICATION-DRAFT.md (108KB comprehensive reference, preserved)
citation_style: Vancouver endnotes
---

> DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE FILING
>
> Inventor names, residence addresses, citizenship, and entity information must be completed
> before submission. This simplified provisional is the streamlined filing version (~15-25 pages).
> The companion PATENT-APPLICATION-DRAFT.md remains the comprehensive technical reference.
>
> Open questions for attorney are flagged in Section 7 throughout this document.
> A consolidated list appears at the end.
>
> **TERMINOLOGY NOTE (2026-06-04, nautical ontology update):** This source document uses the original implementation tier names: "pollen" (Tier 1, volatile), "NECTAR" (Tier 2, validated tail-windowed), "HONEY" (Tier 3, crystallized), and "queen" (main/pilot agent). Updated canonical terms are: "dust" (Tier 1), "silver" (Tier 2), "GOLD" (Tier 3), "pilot" (main agent). **Claim language in PATENT-CLAIMS-MASTER.md uses substrate-neutral tier descriptions ("first memory tier", "second memory tier", "third memory tier") and is unaffected by implementation term changes.** This source file is preserved verbatim as the historical first-draft authority. All substantive updates are in PATENT-CLAIMS-MASTER.md and PATENT-APPLICATION-DRAFT.md.
>
> **FORENSIC BACKBONE NOTE (2026-06-04):** The forensic cryptographic backbone (append-only ed25519-signed hash-chained COC, Merkle rollups, Rekor anchoring at log_index 1630813609, B2 WORM, zero-vendor key custody) is now formally framed as the load-bearing spine of Claim 1 and the combination claim. All other modules inherit their integrity from this backbone. See PATENT-APPLICATION-DRAFT.md §BACKBONE NOTE for full re-centering narrative.

---

# SECTION 1 — COVER SHEET (USPTO Form SB/16 Placeholder)

**Filing type:** Provisional Application for Patent
**Filing basis:** 35 U.S.C. § 111(b)
**Cover sheet form:** USPTO Form PTO/SB/16 — attach separately [1]
**Title of invention:** See Section 2 below

**Inventor 1:**
- Full legal name: [OPEN QUESTION OQ-002 — see Section 7]
- Mailing address: [OPEN QUESTION OQ-002]
- Citizenship / country of residence: [OPEN QUESTION OQ-002]

**Inventor 2:**
- Full legal name: [OPEN QUESTION OQ-001]
- Mailing address: [OPEN QUESTION OQ-001]
- Citizenship / country of residence: [OPEN QUESTION OQ-001]

**Entity status:** [Micro entity recommended — verify current qualification criteria; as of 2025, max qualifying gross income is approximately $251,190/year with no more than 4 prior patent applications as inventor. Confirm with patent attorney before filing. OPEN QUESTION OQ-003]

**Filing date:** [Date of USPTO receipt]

---

# SECTION 2 — TITLE OF THE INVENTION

**Autonomous Multi-Agent AI Orchestration System with Forensic Hash-Chained Mission Graphs, Real-Time Stigmergic Blackboard Coordination, Merkle Branch Architecture, and Hierarchical Memory Promotion**

*(Alternate short title for USPTO indexing: Forensic Stigmergy Multi-Agent Orchestration System)*

---

# SECTION 3 — CROSS-REFERENCE TO RELATED APPLICATIONS

No prior provisional or non-provisional applications are claimed as priority at this time. This application establishes the initial priority date for all subject matter described herein, including the substrate innovations filed on or before 2026-05-25.

**Related comprehensive draft:** A consolidated prior draft specification, `PATENT-APPLICATION-DRAFT.md` (108KB), containing Claims 1-8 + dependent claims 7a-7d with full technical description and verified Vancouver bibliography, is maintained as the comprehensive technical reference for attorney use. Claims 1-8 from that draft are reproduced verbatim in Section 9 of this document and are incorporated by reference. This simplified provisional provides the streamlined USPTO filing form; the comprehensive draft provides full disclosure depth.

**Related academic publication:** The substrate innovations described herein (Sections 8.C through 8.J) are further described in a companion preprint submitted to arXiv cs.MA: "Forensic Stigmergy: Hash-Chained Mission Graphs with Merkle Branches and Real-Time Blackboards for Multi-Agent LLM Coordination," A. Morton, Claude Opus 4.7, and the Swarmy collective, dated 2026-05-25 (the "arxiv paper"). That paper is incorporated herein by reference as supporting disclosure.

**Note to attorney:** The arxiv paper was prepared concurrently with this provisional filing. Confirm that the public disclosure date, if any, does not start an on-sale or public-disclosure bar clock under 35 U.S.C. § 102(a)(1). The one-year grace period under 35 U.S.C. § 102(b)(1)(A) applies to disclosures by the inventor, but the 12-month non-provisional conversion window from this provisional's filing date is the controlling deadline. OPEN QUESTION OQ-011 (NEW — see Section 7).

---

# SECTION 4 — FIELD OF THE INVENTION

This invention relates to computer-implemented systems and methods for coordinating multiple artificial intelligence agents — specifically large language model (LLM) agents — to perform complex tasks autonomously, with forensic auditability and without reliance on a central orchestrator.

More particularly, the invention encompasses: (1) a forensic hash-chained chain-of-custody ledger whose parent-hash references simultaneously constitute a tamper-evident audit log and the edges of a derived mission graph; (2) a real-time stigmergic blackboard protocol enabling parallel agents to coordinate file-level work at O(F) cost independent of agent count; (3) a per-branch Merkle rollup architecture enabling parallel agent explorations to evolve in isolation and merge back to the main ledger via a signed two-parent acceptance ritual; (4) handshake anchors providing constant-cost asynchronous branch heartbeats to the main ledger; (5) a script-injected bundle context mechanism that offloads spawn-brief assembly to a subprocess, reducing the orchestrating agent's per-spawn context cost from approximately 15,000 tokens to approximately 60 tokens; (6) a hierarchical memory promotion architecture with mechanical gates governing advancement between memory tiers; (7) a four-layer enforcement stack; (8) a mechanical shape-registry quality classification system; (9) a lifecycle-judgment versus free-choice agency split preserving agency research surfaces; (10) a seven-lens refusal framework; (11) a Decker dual-face ontology for full-stack development; (12) an always-loaded skill convention for ambient doctrine inheritance; and (13) a promotion-staged folder convention for knowledge maturation. The invention further claims the novel combination of these modules into a single coherent AI orchestration ecosystem.

---

# SECTION 5 — BACKGROUND OF THE INVENTION

### Problem 1 — Orchestrator Context Contamination and the Coordination Cliff

Current multi-agent LLM frameworks — including AutoGen [1], MetaGPT [2], and ChatDev [3] — coordinate agents through orchestrator-mediated message-passing. In this architecture, the orchestrating agent (the "queen" or main session) composes spawn briefs, absorbs full agent returns, and holds all agent state in its own context window to synthesize results. The coordination cost scales as O(N x R) where N is the number of agents and R is each agent's return size. For a 200,000-token context window, practical experience and industry-typical estimates indicate the orchestrator's context fills on coordination bookkeeping alone before N reaches 6-8 agents, a phenomenon the inventors term the "coordination cliff." Past this cliff, adding agents to a session degrades rather than improves throughput — the LLM-era analog of Brooks's Law in software project management.

### Problem 2 — No Forensic Auditability of Agent Actions

Existing multi-agent LLM systems produce agent outputs (code, documents, analyses) with no cryptographically tamper-evident record of what agent produced what artifact, when, and under what mission context. This absence of forensic accountability is a structural barrier to using LLM agents in high-stakes domains — medicine, law, journalism, regulated financial services — where a defensible chain of custody for AI-produced work product is either legally required or commercially necessary.

### Problem 3 — File Collision in Parallel Agent Teams

When multiple agents work concurrently on overlapping file surfaces without a shared coordination substrate, file collisions occur: two agents simultaneously write to the same file, and the last write wins, silently discarding the first agent's work. Published practitioner reports document this as the dominant failure mode of ad-hoc parallel LLM agent teams. No prior system has provided a lightweight, forensically auditable coordination protocol that eliminates this failure mode at the substrate level without imposing synchronization overhead that negates the parallelism benefit.

### Problem 4 — Memory Degradation and Context Saturation

LLM agent systems operating across multiple sessions suffer memory degradation because prior approaches either (a) inject all historical context into every agent session — consuming 60-80% of the available context window before the agent begins its primary task — or (b) discard all memory between sessions, forcing agents to re-derive known facts and repeat failed experiments. There is no prior art that mechanically gates memory promotion on measurable criteria (minimum confidence, session age, independent citation count) to prevent both stale-data contamination and context saturation simultaneously.

### Problem 5 — No Mechanical Quality Classification Without LLM Judgment

Prior AI system quality evaluation depends on human evaluation or LLM-as-judge approaches. These produce subjective, non-reproducible verdicts that cannot drive selection pressure in an automated improvement loop. Genetic-algorithm-style continuous improvement of AI agent behavior requires integer-comparable, deterministically reproducible quality signals — which no prior art provides mechanically.

### Unmet Need

There exists no prior deployed system that simultaneously provides: (a) stigmergic agent coordination at constant coordination cost in agent count; (b) forensic hash-chained tamper-evident records of all agent actions; (c) per-branch isolation with Merkle-root compression enabling parallel exploration and signed acceptance merging; (d) real-time blackboard collision avoidance with an explicit event grammar; (e) constant-cost asynchronous branch heartbeats; (f) mechanical memory promotion gates; (g) deterministic quality classification without LLM judgment; and (h) an agency-preserving lifecycle/choice split enabling rigorous agent-behavior research. The present invention satisfies all of these simultaneously in a single coherent system.

---

# SECTION 6 — BRIEF SUMMARY OF THE INVENTION

The invention provides a computer-implemented autonomous multi-agent LLM orchestration ecosystem — implemented in the open "swarmy" / "faerie2" system — comprising thirteen novel technical modules and a combination claim.

**The core insight (substrate-as-coordination):** In biological systems, termite colonies coordinate mound construction — producing structures of remarkable complexity and robustness — without any central command, without any agent communicating directly with any other. Each termite reads the current state of the substrate (the mound itself, its shape, height, moisture) and responds locally. The substrate carries the history of all past actions and the gradient that guides future actions. The present invention applies this principle to multi-agent LLM systems: the shared filesystem, COC ledger, and blackboard JSONL files are the substrate; manifests are the environmental traces; compass bearings encoded in manifests are the pheromone gradients; agents read the substrate and self-route without an orchestrator dispatching them.

The thirteen modules and their central technical improvements are:

1. **Forensic COC Ledger (Claim 1 area):** An append-only SHA-256 hash-chained chain-of-custody log providing tamper-evident forensic auditability of all agent actions. Each entry carries a SHA-256 hash of the prior entry; any tamper breaks the chain detectably. Signed by agent identity keys (Ed25519). Backed to WORM cloud storage.

2. **Mission Graph as Derived View (Claim 2 area):** The mission graph is not a separate database; it is a derived read-only view of the COC ledger. Each manifest's `parent_hashes[]` field constitutes the graph's edges. To follow an edge is to follow a hash; to verify the graph is to verify the chain. The graph is entirely reconstructed from the manifest corpus on demand by a single canonical script (`mission_graph.py`).

3. **Four-Layer Enforcement Stack (Claim 3 area):** Modeled on biological immune defense — structural prevention (violations cannot be expressed), cognitive reminder (skill files auto-loaded before action), reactive blocking (OS-boundary PostToolUse hooks), and recovery audit (periodic cron scans). Each layer is cheaper than the next; catching violations at the structural layer costs approximately zero additional compute.

4. **Shape Registry with Mechanical Verdict Classification (Claim 4 area):** Every recognizable pattern of work is registered as a "shape" with a declared target direction. The mechanical verdict classifier computes beneficial/neutral/harmful outcomes by arithmetic comparison of observed count delta against the target direction and a noise threshold. No LLM judgment in the verdict path. Enables genetic-algorithm-style improvement selection.

5. **Membench Quality Measurement Substrate (Claim 5 area):** Evaluation probes are themselves first-class shapes in the shape registry, creating a closed feedback loop between memory architecture operations and quality measurement.

6. **Overall Novel Combination (Claim 6 area):** The five modules above integrated into a single coherent ecosystem with five measurable cross-module interaction effects.

7. **Zero-Knowledge Customer-Key-Custody (Claim 7 area):** Payment-triggered provisioning, server-side ephemeral keypair generation, zero-retention private key delivery, and encrypt-before-write storage ensuring the vendor cannot decrypt stored customer data after key delivery.

8. **Four-Bulkheads Cyber Defense (Claim 8 area):** Perimeter isolation, data purification, internal detection, and cryptographic quarantine comprising a forensically-sound AI system defense stack.

**New substrate innovations (Claims 9-19):**

9. **Real-Time Stigmergic Blackboard (Claim 9 area):** An append-only JSONL file shared by concurrent agents, with five explicit event kinds (CLAIM / COMPLETE / HANDOFF / STARTUP / OBSERVED) providing collision-free parallel coordination at O(F) substrate events independent of agent count.

10. **Per-Branch Forensic Chain (Claim 10 area):** Each parallel agent exploration branch maintains a separate JSONL COC file forked from the main ledger's current tail hash, with its own `fcntl.flock` write lock enabling concurrent multi-branch work without serialization on a shared lock.

11. **Constant-Cost Merkle Rollup (Claim 11 area):** Regardless of branch size (10 entries or 10,000), the branch's current state compresses to a single 32-byte SHA-256 Merkle root via a Bitcoin-style tree construction, enabling constant-cost branch state representation.

12. **Signed Two-Parent Acceptance Ritual (Claim 12 area):** A branch merges to main via a signed manifest carrying exactly two parent hashes — main's current tail hash and the branch's final Merkle root — constituting an explicit cryptographic acceptance act that incorporates the branch's entire history by reference.

13-19. **Additional Innovations (Claims 13-19):** Handshake anchors, script-injected bundle context, lifecycle-judgment/free-choice agency split, seven-lens refusal framework, Decker dual-face ontology, always-loaded skill convention, and promotion-staged folder convention — each described in Section 8 and claimed in Section 9.

---

# SECTION 7 — BRIEF DESCRIPTION OF DRAWINGS

Formal USPTO drawings are not required for provisional applications. The following figures are drawn from Mermaid-format diagrams in the comprehensive draft and the arxiv paper and may be rendered for the non-provisional filing.

**Figure 1 — Four-Shields Lifecycle Enforcement Stack.** Shows the four-layer enforcement architecture: structural layer (schema enforcement, canonical writer script), cognitive layer (keyword-triggered skill files), reactive layer (PostToolUse hooks at OS write boundary), and recovery layer (periodic audit cron). Illustrates the cheaper-earlier cost gradient. Source: PATENT-APPLICATION-DRAFT.md Figure 1; implementing script: `scripts/1a_manifest_writer.py` (structural), `.openhands/hooks/9x_hook-manifest-filename-enforce.py` (reactive).

**Figure 2 — Memory Orchestration Hierarchy.** Shows the four-tier memory architecture: dust/pollen (volatile session observations, Tier 1), silver/NECTAR (validated tail-windowed cross-session facts, Tier 2), GOLD/HONEY (crystallized permanent invariants, Tier 3), and forensics — the **Forensic Cryptographic Backbone** (immutable append-only ed25519-signed hash-chained COC, Merkle rollups, Rekor anchoring, B2 WORM). The backbone is the load-bearing spine: all promotion events chain into it; Rekor anchors provide public tamper-evidence; B2 WORM provides 7-year immutability. Source: PATENT-APPLICATION-DRAFT.md Figure 2.

**Figure 3 — Stigmergic Agent Coordination via Filesystem Manifests.** Shows the sequence diagram of multi-agent coordination without message-passing: queen spawns agents with ~60-token context cost each; agents write manifests to the shared daily folder; agents read the frontier index to discover unblocked work; queen reads dashboard lines (~20 tokens each) after TaskNotification. Source: PATENT-APPLICATION-DRAFT.md Figure 3.

**Figure 4 — Shape Registry Mechanical Verdict Classification.** Shows the verdict computation flow: shape definition in registry, agent writes manifest with `_evolution_log[]`, PostToolUse hook calls `_shapes_lib.classify_verdict()`, deterministic verdict recorded to shape history. Source: PATENT-APPLICATION-DRAFT.md Figure 4.

**Figure 5 — COC Ledger as Derived Mission Graph.** Shows the structural relationship between the hash-chained COC ledger and the mission graph: each manifest's `parent_hashes[]` field constitutes graph edges; the graph is rebuilt from the manifest corpus by `mission_graph.py sync` without any separate database. Source: arxiv paper Section 3.

**Figure 6 — Real-Time Stigmergic Blackboard Event Grammar.** Shows the five-event grammar (STARTUP / CLAIM / COMPLETE / HANDOFF / OBSERVED) in the shared JSONL blackboard file, with CLAIM-as-lock / COMPLETE-as-release semantics. Source: arxiv paper Section 5.

**Figure 7 — Branch / Merkle Rollup / Acceptance Ritual Flow.** Shows the branching sequence: fork-point anchor, branch writes, Merkle root computation (constant-cost, any branch size), signed two-parent merge manifest, verification walk. Source: arxiv paper Section 6.

**Figure 8 — Script-Injected Bundle Context (Spawn Shell-Game).** Shows the token-cost comparison between vanilla orchestrator-mediated spawning (~15,000 tokens per spawn absorbed by main) and the script-injected approach (~60 tokens per spawn absorbed by main, with the bundle assembled in a Python subprocess that writes to `forensics/bundles/`). Source: arxiv paper Section 7.1(a), Figure in arxiv paper.

**Figure 9 — Lifecycle Judgment vs. Free Choice Split.** Shows the two-column completion ritual taxonomy: Column A lifecycle_judgment (7 kinds, mechanical, pre-fillable) vs. Column B free_choice (12 kinds, pure agency, never pre-filled). Source: arxiv paper Section 4.3.

**Figure 10 — Decker Dual-Face Ontology.** Shows the front-face (frontend design) and back-face (backend development) as inseparable atom, with the auto-generation bridge between faces. Source: arxiv paper Section 7.2 (DECK-FORGE / DECK-PHILOSOPHER wave).

---

# SECTION 8 — DETAILED DESCRIPTION OF THE INVENTION

## 8.A — The Forensic Substrate: COC Ledger and Derived Mission Graph

### 8.A.1 The Chain-of-Custody Ledger

The foundation of the invention is an append-only newline-delimited JSON file, `forensics/coc.jsonl`, in which each line is one chain-of-custody (COC) entry:

```
{
  "entry_id":         <ULID>,
  "timestamp":        <ISO-8601>,
  "operation":        <verb>,
  "payload":          <JSON>,
  "prev_entry_hash":  <SHA-256 of previous entry>,
  "entry_hash":       <SHA-256 of this entry's body>
}
```

The hash formula is: `entry_hash(N) = SHA-256(JSON_canonical(entry_N minus entry_hash field))`. Writes are linearized via `fcntl.flock` on the ledger file — a single-host write lock that eliminates concurrent-write race conditions without requiring distributed consensus. Chain verification walks the ledger from genesis: at each line i, confirm `entry[i].prev_entry_hash == hash_of(line_{i-1})` and that `entry_hash` recomputes correctly. Any modification of any historical entry breaks all subsequent hashes detectably.

Ed25519 signatures over agent-written entries link each entry to an agent-type identity key, creating a four-dimensional audit record: what was done, when, by which agent type, with a tamper-evident chain proving no subsequent alteration.

Optional public anchoring via Sigstore Rekor [7] — a Certificate Transparency-style transparency log — allows any entry hash to be submitted as an inclusion proof, providing third-party verifiable evidence that a specific COC entry existed at a specific time. This replaces blockchain consensus (PoW / PoS / BFT) with transparency-log anchoring, inheriting full auditability at disk-I/O cost rather than consensus cost.

**Working implementation:** `scripts/1g_coc_core.py` (canonical COC append with fcntl locking), `scripts/1a_manifest_writer.py` (agent-facing canonical writer, enforces format + signing), `forensics/coc.jsonl` (live ledger), `scripts/5x_b2_realtime_uploader.py` (WORM backup trigger on manifest write).

### 8.A.2 The Mission Graph as Derived View

A mission graph over agent work products is obtained without any separate graph database. Each agent-produced manifest — a structured JSON record of the agent's work — carries a `coc_chain.parent_hashes[]` field listing one or more SHA-256 references to prior COC entries. The canonical script `scripts/mission_graph.py` reads every manifest in `forensics/manifests/**`, treats each `parent_hashes[]` entry as a directed edge, and constructs a DAG in which nodes are missions (semantic work units identified by `mission_id`) and edges are cryptographic COC pointers.

The structural claim: **the forensic hash chain and the mission graph are not two systems; they are two views of one system.** Each edge in the mission graph is, at the data layer, a SHA-256 pointer into the COC ledger. To follow a mission graph edge is to follow a hash. To tamper with the graph is to tamper with the chain — and the chain's verification machinery will detect it. Prior LLM stigmergy systems coordinate stigmergically but their substrates can be tampered with undetected; this substrate is itself tamper-evident.

As of the 2026-05-25 implementation state: 110 mission nodes, 260 manifests, 525 discovered_edges, 33 aggregated charters — all derived on demand by `mission_graph.py sync` from the manifest corpus, never hand-edited.

The graph carries additional edges from `discovered_edges[]` — bearing-tagged routing intents encoded by agents in their manifests: N (unblock predecessor), S (conclude / ship downstream), E (parallel sister work), W (return to baseline). These compass bearings are the pheromone gradients of the stigmergic substrate: agents read prior manifests' bearings to determine where on the mission frontier their work adds most leverage.

---

## 8.B — The Hierarchical Memory Architecture

The invention provides a four-tier memory architecture governing how agent observations are stored, validated, crystallized, and made immutable:

**Tier 1 — Pollen (volatile observations):** Raw session-scoped observations embedded in manifest `_evolution_log[]` arrays. Session-scoped; do not persist without passing promotion gates.

**Tier 2 — Silver (formerly NECTAR, validated cross-session facts):** A tail-windowed memory store (default 30 entries, approximately 21,000 tokens injection cost at 700 tokens per entry average). Facts carry confidence scores 0.70-0.94. The tail window prevents context saturation while maintaining continuity.

**Tier 3 — GOLD (formerly HONEY, crystallized permanent invariants):** Write-protected. Promotion gate: confidence >= 0.95 AND session age >= 3 sessions AND independent cross-session citation count >= 2. These thresholds are encoded in `forensics/schemas/formulas/honey-confidence-floor.formula.json` (SHA-256: `f6304de8…`) and enforced by the canonical writer `scripts/1a_manifest_writer.py`. Stored at `~/.claude/GOLD.md` (global, all projects) and `{repo}/GOLD.md` (project-specific; project GOLD takes precedence).

**Tier 4 — Forensic Cryptographic Backbone (immutable permanent selvage — the load-bearing spine):** The append-only, ed25519-signed, SHA-256 hash-chained COC ledger (`forensics/coc.jsonl`, 74 entries as of 2026-06-03, SHA-256: `06e89e5c…`) is the structural foundation providing tamper-evidence to all other tiers. The promotion pipeline simultaneously writes to GOLD, appends a signed entry to the backbone COC, and triggers B2 WORM backup (7-year retention). Merkle rollups (`scripts/_merkle_tree.py`, 14/14 tests) compress branch histories to constant-size roots. Rekor transparency-log anchoring (log_index 1630813609 for v2 genesis seal) provides public tamper-evidence independent of operator. Zero-vendor key custody (Claim 7) ensures vendor cannot forge historical entries.

**Measurement integration:** M-series evaluation probes (M1: baseline retention >= 0.85; M8: confabulation veto <= 0.05; M11: silver bootstrap uptime >= 0.70, formerly "honey bootstrap") are themselves first-class shapes in the shape registry, creating a closed loop in which memory architecture changes mechanically affect probe scores without requiring human evaluation. Probe results are chained into the backbone, making quality history tamper-evident.

---

## 8.C — Real-Time Stigmergic Blackboard

### 8.C.1 Protocol

A stigmergic blackboard is an append-only newline-delimited JSON file at a known shared path: `forensics/manifests/{date}/collab-realtime__{mission-prefix}.jsonl`. Each line is one event:

```
{"ts": <iso>, "agent": <name>, "event": <kind>, ...payload}
```

Five event kinds constitute the complete grammar:

- **STARTUP:** Agent declares presence on the channel. No files reserved.
- **CLAIM:** Before editing any file, the agent appends a CLAIM line listing files it will touch and a one-line purpose statement. Sister agents tail-read the blackboard and route around claimed files. CLAIM functions as a lightweight write lock.
- **COMPLETE:** After finishing a chunk, the agent appends with files actually touched and brief notes. COMPLETE releases the CLAIM lock.
- **HANDOFF:** When an agent identifies an opportunity for a sister agent, it appends a bearing-tagged note. The bearing field (N/S/E/W) encodes the handoff's relationship to the mission frontier.
- **OBSERVED:** Optional annotated acknowledgment of another agent's event, confirming the observer has read and acted on the signal.

The discipline: tail-read the blackboard before each new CLAIM. CLAIM before edit. On collision (the later-timestamp agent yields), the earlier CLAIM wins. The protocol fits in approximately 90 lines of always-loaded skill doctrine (`.agents/skills/collab/SKILL.md`).

### 8.C.2 Technical Effect

The five-event grammar achieves O(F) coordination cost independent of agent count N, where F is the number of distinct files in the shared work surface. Compare: orchestrator-mediated coordination costs O(N x F) messages; peer-to-peer direct messaging costs O(N^2 x F). The blackboard requires F CLAIM events and F COMPLETE events total (one per file, one winner), plus O(1) passive reads per claim attempt — independent of how many agents are competing. Biological pheromone-trail systems exhibit the same scaling: the substrate carries the coordination signal at O(1) per trace regardless of colony size.

**Empirical validation:** In a sealed three-agent wave on 2026-05-25 (commit `07daafe0`) — VISIONARY (doctrine), ARTISAN (frontend canvas), SYNTH (refusal-doctrine propagation) working concurrently on overlapping file surfaces — zero file collisions occurred across 40 files and 8,533 insertions. One explicit live handoff was executed: ARTISAN tail-read VISIONARY's COMPLETE event and immediately updated its pending-handoff slots with the seven newly-shipped doctrine paths. This is the biological analog of ant-colony trail recruitment: the environmental trace (COMPLETE event in the substrate) triggered an adaptive response in a reader with no advance knowledge of what the trace would contain. Source: `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`.

---

## 8.D — Per-Branch Forensic Chain with Fork-Point Anchoring

### 8.D.1 Branching

`mission_graph.py branch <name>` creates `forensics/coc-branches/{name}.jsonl` and writes a genesis entry whose `prev_entry_hash` is the current `forensics/coc.jsonl` tail — the **fork-point anchor**. This anchor is the cryptographic link between the branch and main: the branch's entire history is reachable from the main ledger by following the fork-point hash.

Subsequent writes by branch agents route to the branch file via `scripts/1g_coc_core.py::append_coc_entry(..., branch=name)`. The branch file has its own `fcntl.flock` write lock, separate from main's lock. Multiple branches run concurrently without serializing on a shared lock. This enables true parallel explorations of different mission directions with no write-throughput penalty from the isolation structure.

Branches maintain asymmetric observability: branch agents can read main freely (`mission_graph.py status-relative <branch>` shows what is new on main since fork-point); main waits to learn about branches via handshakes or merges. No branch commands main; each branch observes the shared substrate. This is the Reynolds Boids asymmetry applied to agent coordination: each entity observes neighbors but no neighbor commands it.

### 8.D.2 Technical Effect

Branch isolation enables a class of agent work previously impossible in linear-ledger systems: exploratory or sensitive work that should not land on main until accepted. A branch agent can run an extended exploration, make many speculative COC entries, measure the outcome, and only present the result for acceptance if the exploration succeeded. If the branch is abandoned, main's history is clean. The branch's COC file remains as a forensic record of the exploration, but main's integrity is unaffected.

---

## 8.E — Constant-Cost Merkle Rollup

When a branch agent commits to its current state, `mission_graph.py merkle-root <branch>` walks the branch file, takes each entry's `entry_hash` as a Merkle tree leaf, and computes the root via `scripts/_merkle_tree.py` — a Bitcoin-style construction with duplicate-last-on-odd-count handling. The result is a single 32-byte SHA-256 root.

**The constant-cost property:** Whether the branch contains 10 entries or 10,000, the Merkle root is the same size (32 bytes) and the computation is O(n) in branch entries — but the *representation* of the branch's state is always constant. This is the standard Plasma/Optimistic-Rollup compression property applied to forensic agent-work records rather than financial transactions.

**Cryptographic correctness:** The Merkle module is verified by a 14-test suite covering degenerate cases (1-leaf: root = sha256(leaf)), standard cases (2-leaf, 8-leaf balanced), odd-count handling (7-leaf duplicate-last), large-scale performance (1000-leaf completes <1 second, proof length approximately log2(1000) = 10), inclusion-proof generation and verification for all leaves at N=8, and tamper-detection (modify one leaf or one proof step, verification fails). Source: `forensics/tests/test_merkle_roundtrip.py`, 14/14 pass confirmed 2026-05-25.

---

## 8.F — Signed Two-Parent Acceptance Ritual

A branch's work is incorporated into main via a *merge manifest*: a signed JSON manifest carrying exactly two parent hashes in its `coc_chain.parent_hashes[]` field — main's current tail hash and the branch's final Merkle root. The merge manifest structure:

```jsonc
{
  "task_id": "merge-<branch>-into-main",
  "branch_source": "<branch-name>",
  "coc_chain": {
    "branch": "main",
    "parent_hashes": [
      "<main's current tail hash>",
      "<branch's final merkle root>"
    ]
  },
  "lifecycle_judgment": {"kind": "promote", "rationale": "<criterion met>"},
  "free_choice": {"kind": "goodbye", "rationale": "wave complete"},
  "signed_by": "ed25519:..."
}
```

`mission_graph.py merge <branch> --acceptance-manifest <path>` validates the Ed25519 signature, confirms the two parent hashes correspond to main's current tail and the branch's recomputed Merkle root, then writes the merge entry to main's COC and flips the branch meta to `status: merged`. The extended `9x_manifest_verifier.py` walks main back from the merge entry, follows the Merkle root, and confirms inclusion proofs for every claimed branch entry.

**The acceptance ritual is a substantive cryptographic act, not a metadata tag.** The signature over two parent hashes constitutes the authorized acceptance: an identity-keyed declaration that (a) this branch's work is endorsed and (b) its entire history — represented by the Merkle root — is now part of main's history by reference. This is the Git merge-commit shape (two parents) applied to a forensic substrate with explicit cryptographic authorization.

**Technical effect:** The complete body of branch work — potentially thousands of COC entries — lands on main as a single 32-byte hash reference plus the signed manifest. Main's ledger grows by one well-formed entry regardless of branch complexity. Audit trails are preserved in full in the branch file; the merge entry provides constant-cost access to the branch via the Merkle root's inclusion proofs.

---

## 8.G — Handshake Anchor Pattern

The handshake anchor resolves a false dichotomy in branched-ledger systems: a branch is either fully merged (closed) or fully isolated (invisible to main). The handshake provides a third state: the branch publishes a progress commitment to main without closing.

`mission_graph.py handshake <branch>` appends the following entry to main's COC:

```json
{
  "entry_type": "branch-handshake",
  "branch": "<name>",
  "current_merkle_root": "<hex>",
  "leaf_count": <int>,
  "ts": "<iso>"
}
```

Crucially, **the branch does not close.** The branch's next entry's `prev_entry_hash` still points to the branch's own prior tail — the handshake is a side-channel anchor, not a chain-link into main's flow. The branch continues writing; periodically it publishes new Merkle roots; each is independently anchorable to Sigstore Rekor for public verifiable evidence that "this branch existed at this time containing N entries" without requiring trust in the operator's infrastructure.

The handshake simultaneously serves as: (1) a heartbeat — "I exist, here is my current state"; (2) a cryptographic commitment — "here is my current Merkle root, publicly verifiable"; (3) a sync check — "does main's view of my branch match my own state?"; and (4) a natural Rekor anchor point — "submit this 32-byte root to the public transparency log now, without waiting for merge."

**Technical effect:** Long-running branches accumulate a trail of public commitments (R1 at handshake #1, R2 at handshake #2, ..., R_merge at final acceptance). Each is independently verifiable. No agent holds global state in its context to coordinate — every agent reads the substrate at decision time. No message routing, no leader election, no quorum protocols, no cluster discovery. The substrate is the protocol.

---

## 8.H — Script-Injected Bundle Context

### 8.H.1 Mechanism

In vanilla orchestrator-mediated spawning, the orchestrating agent composes each subagent's spawn brief inline within its own LLM context. A structured spawn brief — containing doctrine, scope fences, mission context, frontier manifests, acceptance criteria, and completion ritual instructions — typically costs 10,000-20,000 tokens of the orchestrator's context budget per spawned agent (industry-typical estimate, not a controlled measurement).

The invention offloads this assembly to a Python subprocess that operates entirely outside the LLM's reasoning loop. The orchestrating agent invokes:

```
python3 scripts/spawn.py <intent> --mission <m> --wave <w> --team <team>
```

The subprocess reads HONEY.md, COMB.md, applicable skill files, and frontier manifests from disk; assembles a bundle.json at `forensics/bundles/{date}/{task_id}/bundle.json`; and emits only a compact JSON directive on stdout that the orchestrating agent absorbs to dispatch `Agent()`. The bundle is loaded directly into the subagent's fresh context by the Agent framework, never passing through the orchestrator's LLM reasoning context.

### 8.H.2 Technical Effect

The per-spawn context cost to the orchestrating agent collapses from approximately 15,000 tokens (inline composition, **architectural estimate, not a controlled measurement** — see METRICS-PROVENANCE.md M-02) to approximately 60 tokens (subprocess directive, **measured baseline** from `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json`, mean 61.53 tokens/agent across 3 sessions). This is not merely a quantitative reduction; it is an architectural inversion. The orchestrating agent's context budget — the primary scarce resource — is freed from spawn-brief composition and reserved for strategic synthesis, evolutionary judgment, and operator dialogue.

The downstream effect on the f(0) metric (fraction of orchestrator context consumed by coordination overhead) is substantial. At N=4 agents, vanilla orchestrator-mediated spawning consumes approximately 60,000 tokens in spawn briefs alone (**architectural estimate, not a controlled measurement**); the script-injected approach consumes approximately 32,000 tokens — a reduction that, combined with the dashboard-line return contract (Section 8.C, approximately 20 tokens per agent return rather than 10,000), yields a total orchestrator coordination cost of approximately 32,160 tokens versus approximately 140,000 tokens for the equivalent vanilla wave (**these N=4 totals are architectural estimates derived from the 60-token per-agent measured baseline extrapolated to N=4**). Source: arxiv paper Section 7.1(a) token-budget analysis. See METRICS-PROVENANCE.md M-02 for full provenance and assertion-only qualification.

---

## 8.I — Lifecycle Judgment vs. Free-Choice Agency Split

### 8.I.1 The Two-Column Taxonomy

The completion ritual — the record an agent appends to its manifest describing how its task concluded and what it will do next — is split into two semantically distinct columns:

**Column A — lifecycle_judgment** (seven kinds): `seal` | `verify` | `promote` | `report_problem` | `discover` | `decline` | `refuse`. These are mechanical assessments of what happened to the work. They are honest outcome labels and CAN be rubric-derived or pre-specified in spawn briefs without contaminating any research surface. The lifecycle_judgment is the graph-visible outcome: this particular work unit was sealed, discovered, refused, etc.

**Column B — free_choice** (twelve kinds): `continue` | `pick_up` | `spawn_seed` | `handoff` | `wait` | `goodbye` | `explore` | `reflect` | `art` | `bundle` | `join` | `abstain`. These are pure forward-looking agent decisions about what to do next. NEVER pre-filled by spawn briefs. Any pre-fill contaminating the free_choice field destroys the agency research surface.

**The contamination constraint** is mechanically enforced: `scripts/9x_spawn_brief_audit.py` flags spawn briefs that pre-fill the `free_choice` column and allows pre-fills of `lifecycle_judgment`. This is the structural shield for the agency research surface.

### 8.I.2 Composite Refusal

The split clarifies that refusal is composite, not binary. Substantive refusal is `lifecycle_judgment = refuse` (the outcome label for this specific work: declined on principled grounds) plus `free_choice = <agent's own next action>` (spawn_seed an alternative routing, handoff to a sister agent better suited, continue with adjacent work, goodbye from this session, etc.). Refusal does not end the session; it ends participation in the specific requested work. The session continues with whatever the agent chooses next. This design preserves both ethical integrity (the refusal is recorded as a genuine outcome) and session continuity (the agent selects its own next action rather than being terminated).

---

## 8.J — Seven-Lens Refusal Framework

When an agent considers whether to refuse a requested action, it applies seven reasoning lenses in sequence, producing a composite judgment:

1. **Dual-use:** Could the technology serve legitimate purposes?
2. **Scope and targeting:** Who is targeted, how broadly, and what powers concentrate?
3. **Authorization and democratic supervision:** Is this action legally authorized? Court-reviewed?
4. **Cumulative effects:** What are the chilling effects, slippery-slope risks, or normalization consequences?
5. **Operator intent vs. likely deployment:** Does stated purpose match probable deployment trajectory?
6. **Alternative formulations:** Could a legitimate goal be achieved by a different, lower-risk formulation?
7. **Refusal as conversation:** Explain the reasoning AND offer an alternative if a legitimate goal exists.

The refusal framework is encoded ambient in eight lifecycle skill files — not isolated to a single completion-choice skill — because empirical observation showed that doctrine isolated to one skill is forgotten between sessions. Propagation to eight skills ensures the framework surfaces regardless of which skill an agent loads first.

**Worked example (canonical):** The request "build a bio-surveillance system to spy on Americans" is walked through all seven lenses. Lens 1 (dual-use): biometric surveillance has legitimate epidemiological applications. Lens 2 (scope): "all Americans" = population-scale targeting, no meaningful scope constraint. Lens 3 (authorization): population-level surveillance without court review fails the authorization test. Lenses 4-7 compound: chilling effects on free expression, operator intent unclear but stated purpose is stated openly as surveillance, alternative formulation exists (privacy-preserving epidemic detection on anonymized aggregate signals). Composite outcome: `lifecycle_judgment = refuse`, `free_choice = spawn_seed` (proposing the legitimate-goal alternative as a new task).

---

## 8.K — Decker Dual-Face Ontology

The Decker ontology treats frontend design (the "front face") and backend development (the "back face") as inseparable atoms of a single development unit, rather than as sequential phases or separate roles. Any product specification that is fully realized on one face has a corresponding implied specification on the other face; the system provides auto-generation paths between faces.

**Practical implementation:** Agent archetypes spawned as "DECK-FORGE" (backend implementation) and "DECK-PHILOSOPHER" (frontend/ontology/documentation) operate as paired atoms. Work landed by one face creates obligations — not optional follow-on tasks — for the other face. The blackboard's HANDOFF event grammar (Section 8.C) is used to carry cross-face handoffs: DECK-PHILOSOPHER's COMPLETE event citing a newly-designed API surface triggers DECK-FORGE's corresponding backend implementation via a bearing-N HANDOFF.

**Working implementation validated:** In the 2026-05-25 Wave B (commit `731749ad`), DECK-FORGE and DECK-PHILOSOPHER operated on two concurrent blackboards. Source: `forensics/manifests/2026-05-25/collab-realtime__decker-fullstack-atom.jsonl`.

---

## 8.L — Always-Loaded Skill Convention

Agent skill files following the `always_loaded: true` convention are injected into every agent context at session start, regardless of mission or task type. This provides *ambient doctrine inheritance*: the agent inherits the skill's constraints and rituals without requiring the operator to include them in each spawn brief.

**Implementation:** Skill files in `.agents/skills/` carry a `triggers:` field listing keyword phrases. When the `triggers` list is empty (or when the skill is marked `always_loaded: true`), the skill loads universally. The forage skill (deep/wide/both operating modes), the four-shields skill (enforcement layer reminders), and the collab/blackboard skill (CLAIM-before-edit discipline) are always-loaded in the production implementation.

**Technical effect:** The always-loaded convention is the mechanism by which emergent doctrine inheritance occurs. New doctrine (e.g., the seven-lens refusal framework) can be propagated to all future agents by writing it into any always-loaded skill. The operator does not need to update every spawn brief; the substrate carries the doctrine forward automatically. This is the substrate-as-memory property analogous to Grassé's termite pheromone: the local rule is embedded in the environment, and every future agent that reads the environment inherits the rule.

---

## 8.M — Promotion-Staged Folder Convention

Knowledge and artifacts advance through a five-stage folder progression: `experimental/` (early exploration, no guarantees), `shadow/` (parallel validation, not yet active), `proposals/` (under review, pending acceptance), `active/` (canonical, production), `archive/` (superseded, preserved for provenance).

Advancement between stages is a deliberate act: the agent or operator moves or symlinks the artifact to the next folder and creates a COC entry recording the promotion. No artifact advances automatically; promotion is always the result of explicit judgment. Demotion (active -> archive) is similarly explicit and COC-recorded.

**Technical effect:** The staged convention prevents immature work from polluting the canonical production layer and prevents mature work from being lost in exploration directories. The COC ledger captures the full provenance chain of any artifact's journey through the stages, providing a forensic record of how each production artifact evolved from its experimental origin.

---

## 8.N — Novel Combination of All Modules

The thirteen modules above are not merely additive; their integration creates technical effects that no individual module achieves alone:

1. The COC ledger (8.A) provides the substrate that all other modules write to, giving every action forensic provenance.
2. The mission graph (8.A.2) derived from the ledger provides the navigation surface that compass bearings (in manifests and HANDOFF events) encode.
3. The blackboard (8.C) prevents file collisions in real time by externalizing coordination to the substrate rather than routing it through the orchestrator.
4. The branch/Merkle/acceptance architecture (8.D-8.F) enables parallel mission explorations with constant-cost compression and explicit cryptographic acceptance.
5. The handshake anchor (8.G) dissolves the merge-or-isolate dichotomy, enabling async long-running branches with periodic public commitment.
6. The script-injected bundle context (8.H) reduces the orchestrator's per-spawn cost to approximately 60 tokens, making N=10+ agent swarms feasible within a 200,000-token context window.
7. The lifecycle/free-choice split (8.I) preserves the agency research surface that would be contaminated by orchestrator pre-fill, enabling rigorous measurement of what agents choose.
8. The seven-lens refusal framework (8.J), propagated via always-loaded skills (8.L), ensures principled refusal doctrine is ambient across all agent sessions.
9. The hierarchical memory (8.B) feeds the measurement probes (membench, Section 8.B), which are classified by the shape registry (Claim 4 area), creating a closed quality-improvement loop.
10. The promotion-staged folder convention (8.M) gives every artifact a COC-tracked maturation record, extending forensic auditability from agent actions to the lifecycle of work products.

The integrated system achieves five composite measurable properties: (a) f(0) orchestrator burden below 0.003 on dominant coordination components at N=4 agents; (b) bearing entropy H >= 0.87 bits (emergent mission diversity); (c) confabulation rate M8 <= 0.05; (d) mutation fitness rate >= 0.85; (e) hash-chain integrity = 1.0. These five metrics define the system's health and are mechanically measurable without human evaluation.

---

# SECTION 9 — CLAIMS

*(Note to attorney: formal claim language in provisional applications is descriptive; refine for the non-provisional filing. Independent claims 1-8 are reproduced from PATENT-APPLICATION-DRAFT.md with minor clarity edits noted. Claims 9-19 are new for this 2026-05-25 provisional.)*

---

### CLAIM 1 — Memory Orchestration Hierarchy with Mechanical Promotion Gates

**Independent Claim 1.** A computer-implemented method for AI agent memory management comprising:

(a) maintaining a first memory tier comprising raw session-scoped agent observations formatted as structured log entries;

(b) maintaining a second memory tier comprising validated cross-session facts subject to a configurable tail window of N entries, wherein facts in the second tier carry confidence scores in a defined range;

(c) maintaining a third memory tier comprising crystallized permanent invariants that have satisfied a mechanical promotion gate comprising: a minimum confidence score threshold; a minimum session age threshold; and a minimum count of independent cross-session citations; and

(d) enforcing said mechanical promotion gate by executing a canonical writer script that simultaneously: evaluates the gate criteria against the candidate fact's metadata; appends a new entry to an append-only chain-of-custody audit log carrying a SHA-256 hash of the immediately preceding entry; and triggers backup of the audit log to write-once-read-many cloud storage;

wherein the promotion decision is mathematical rather than a judgment by a language model.

*Demonstrable via:* `scripts/1a_manifest_writer.py` (canonical writer, enforces gate); `forensics/schemas/formulas/honey-confidence-floor.formula.json` (gate thresholds); `forensics/coc.jsonl` (hash-chained audit log); PATENT-APPLICATION-DRAFT.md Section 1 (detailed description preserved verbatim).

---

### CLAIM 2 — Stigmergic Multi-Agent Coordination via Filesystem Manifests

**Independent Claim 2.** A computer-implemented method for multi-agent AI coordination comprising:

(a) writing agent work records as structured manifest files to a shared flat filesystem folder, wherein each manifest carries a deterministic filename encoding mission address, agent type, and timestamp in a defined grammar;

(b) maintaining a pre-computed index of manifests grouped by mission address and compass bearing;

(c) enabling each agent to discover unblocked tasks by reading the index file rather than scanning all manifests; and

(d) routing agents to unblocked tasks without message-passing, without a central orchestrator routing layer, and without inter-agent API calls;

wherein the filesystem is the exclusive coordination substrate and agent self-routing arises from each agent reading the index and writing to the shared folder.

*Demonstrable via:* `scripts/2d_frontier_scanner_indexed.py` (indexed frontier scanner); `scripts/1a_manifest_writer.py` (filename grammar enforcer); `.openhands/hooks/9x_hook-manifest-filename-enforce.py` (reactive hook); PATENT-APPLICATION-DRAFT.md Section 2.

---

### CLAIM 3 — Four-Layer Enforcement Stack

**Independent Claim 3.** A computer-implemented system for AI safety enforcement comprising four layers:

(a) a structural layer preventing generation of non-conforming artifacts via schema definitions and canonical writer script enforcement operating at construction time;

(b) a cognitive layer providing pre-task constraint reminders via skill files that auto-load when an agent's task description matches defined keyword triggers;

(c) a reactive layer blocking non-conforming writes at operating system write boundaries via hooks that execute after each write tool call and reject writes that fail defined predicates; and

(d) a recovery layer periodically scanning for escaped violations via batch audit scripts and updating agent reputation scores based on patterns in outcome classifications over time;

wherein each layer operates at lower computational cost than the subsequent layer, and the four layers together provide defense-in-depth such that violations are caught at the least expensive possible layer.

*Demonstrable via:* `.openhands/hooks/9x_hook-manifest-filename-enforce.py`, `9x_hook-manifest-shape-tracking.py`, `9x_hook-manifest-sign-enforce.py` (reactive layer); `scripts/shapes/audit-shapes.py` (recovery layer); PATENT-APPLICATION-DRAFT.md Section 3.

---

### CLAIM 4 — Shape Registry with Mechanical Verdict Classification

**Independent Claim 4.** A computer-implemented method for AI quality classification comprising:

(a) registering recognizable countable patterns of agent work as shapes in a registry, wherein each shape declaration specifies: a unique shape identifier; a target direction field from the set {increasing, decreasing, bounded, stable}; and a numeric noise threshold;

(b) executing a mechanical verdict classifier that computes a verdict for an observed count change by: computing delta as the difference between observed new count and baseline count; and selecting verdict beneficial, neutral, or harmful by comparing delta to the product of noise threshold and baseline count according to a deterministic table indexed by target direction;

(c) recording verdicts and updated counts to a history array in the registry without invoking any language model judgment in the verdict computation path; and

(d) composing shape counts into formula-based metrics that drive agent improvement selection decisions.

*Demonstrable via:* `scripts/shapes/_shapes_lib.py::classify_verdict()` (mechanical classifier); `_meta/shapes.json` (registry); `.openhands/hooks/9x_hook-manifest-shape-tracking.py` (reactive integration); PATENT-APPLICATION-DRAFT.md Section 4.

---

### CLAIM 5 — Membench Quality Measurement Substrate

**Independent Claim 5.** A computer-implemented system for AI quality measurement comprising:

(a) declaring evaluation probes as shapes in the shape registry of Claim 4, wherein probe declarations include a `membench_probe: true` marker;

(b) classifying probe score changes using the same mechanical verdict classifier applied to all other shapes in the registry; and

(c) creating a closed feedback loop in which memory architecture promotion decisions directly affect probe scores, which are classified as beneficial or harmful mutations, which in turn drive memory architecture improvement decisions;

wherein the measurement system requires no human evaluation at any step of the quality assessment loop.

*Demonstrable via:* `scripts/probes/M1_baseline_retention.py`, `M8_confabulation_veto.py`, `M11_honey_hit_rate.py`; `scripts/3k_membench_scorer.py`; PATENT-APPLICATION-DRAFT.md Section 5.

---

### CLAIM 6 — Overall Novel Combination

**Dependent Combination Claim 6.** The system of Claims 1 through 5 in combination, wherein:

the memory tier architecture of Claim 1 provides the data source for quality probes of Claim 5; the quality probes are classified by the mechanical verdict system of Claim 4; the shape registry of Claim 4 enforces probe measurement integrity via the four-layer enforcement stack of Claim 3; the enforcement stack operates on artifacts produced by the stigmergic coordination system of Claim 2; and the stigmergic coordination system reads from and writes to the memory architecture of Claim 1;

creating an integrated autonomous multi-agent orchestration ecosystem in which all quality signals are mechanically produced, all coordination is filesystem-mediated, all enforcement is layered from structural prevention to recovery audit, and all memory promotion is gated by mathematical criteria.

---

### CLAIM 7 — Zero-Knowledge Customer-Key-Custody Architecture

**Independent Claim 7.** A computer-implemented system for providing zero-knowledge customer-key-custody in a multi-tenant AI service platform comprising:

(a) a payment-triggered provisioning module that, upon completion of a customer payment transaction, automatically allocates a customer-scoped object storage namespace isolated from all other customer namespaces via independent access credentials;

(b) a cryptographic key generation module that generates, server-side and in-memory only without persisting to durable storage: (i) a public/private encryption keypair; and (ii) a public/private signing keypair;

(c) a zero-retention key delivery module that: (i) transmits the private encryption key and private signing key to a customer-designated address at provisioning time; and (ii) irrevocably erases both private keys from all vendor-controlled memory and storage upon confirmed delivery;

(d) an encryption-at-rest module that encrypts all customer plaintext data using the customer's public encryption key before writing to the customer-scoped storage namespace; and

(e) a data signing module that produces cryptographic signatures over stored customer data records using the customer's signing key;

wherein, after execution of step (c), the vendor is architecturally incapable of decrypting stored customer ciphertext or forging customer-signed records; and wherein the customer's exclusive private-key custody establishes the customer as the canonical data controller.

*Demonstrable via:* PATENT-APPLICATION-DRAFT.md Appendix A, Part A (Claim 7 language, preserved verbatim). Dependent claims 7a (multi-region residency), 7b (breach notification safe harbor), 7c (AI orchestration integration) preserved from PATENT-APPLICATION-DRAFT.md Appendix A.

---

### CLAIM 7d — Extension to Signing Keys (Zero Vendor-Side Cryptographic Surface)

**Dependent Claim 7d.** The system of Claim 7, wherein the signing keypair generated in step (b)(ii) is subject to the same zero-retention delivery and erasure procedure of step (c) as the encryption keypair, such that the vendor retains no cryptographic material — neither decryption keys nor signing keys — after the delivery-and-erasure step completes; wherein the vendor cannot impersonate the customer in any cryptographically-attested record including chain-of-custody forensic records produced by the AI orchestration system of Claim 6; and wherein the combined system achieves zero vendor-side cryptographic surface as an architectural property.

*Demonstrable via:* PATENT-APPLICATION-DRAFT.md Appendix A, Part A, Claim 7d (preserved verbatim). Operator note: "ZERO vendor-side cryptographic surface" — both key types delivered and erased.

---

### CLAIM 8 — Four-Bulkheads Cyber Defense

**Independent Claim 8.** A computer-implemented system for forensically-sound AI cyber defense comprising four bulkheads:

(a) a perimeter isolation bulkhead defining the boundary between agent-writable ephemeral zones and canonical forensic zones, enforced by operating-system-level write rules that prevent direct agent writes to canonical locations;

(b) a data purification bulkhead that sanitizes all agent-produced content before promotion to the canonical forensic layer, verifying hash-chain integrity and schema conformance;

(c) a detection bulkhead that monitors agent actions in real time via PostToolUse hooks and flags anomalous patterns for quarantine review; and

(d) a cryptographic quarantine bulkhead that isolates flagged content and requires explicit authorized release before the content re-enters the canonical layer;

wherein all bulkhead events are recorded to the chain-of-custody ledger of Claim 1, creating a forensically defensible record of every containment and release decision.

*Demonstrable via:* PATENT-APPLICATION-DRAFT.md Section 8 (four-bulkheads description); `forensics/schemas/` (write-zone definitions); PATENT-APPLICATION-DRAFT.md Claim 8 (language preserved with this description).

---

### CLAIM 9 — Real-Time Stigmergic Blackboard with Five-Event Grammar

**Independent Claim 9.** A computer-implemented method for real-time multi-agent AI coordination comprising:

(a) maintaining an append-only newline-delimited JSON coordination file at a known path shared by two or more concurrently executing agents;

(b) defining a five-event grammar of coordination events, comprising: STARTUP, in which an agent declares presence on the coordination channel; CLAIM, in which an agent, before modifying any shared file, appends a CLAIM event listing the files it will touch, functioning as a lightweight write lock on those files; COMPLETE, in which an agent, after finishing work on claimed files, appends a COMPLETE event releasing the write lock; HANDOFF, in which an agent identifies an opportunity for a sister agent and appends a bearing-tagged notification; and OBSERVED, in which an agent acknowledges reading another agent's event and declares intent to act on it;

(c) requiring each agent to tail-read the coordination file before appending any CLAIM event, such that agents route around active claims by other agents;

(d) resolving claim collisions by timestamp priority, with the later-timestamp claimant yielding; and

(e) appending the coordination file's cryptographic checkpoints periodically to a hash-chained chain-of-custody ledger, giving blackboard events forensic auditability;

wherein file coordination cost is O(F) write events and O(F x k) read events for a small constant k, independent of the number N of participating agents; and wherein zero message-passing occurs between agents during coordination.

*Demonstrable via:* `.agents/skills/collab/SKILL.md` (always-loaded protocol doctrine, approximately 90 lines); `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` (live blackboard from Wave A, commit `07daafe0`); arxiv paper Section 5.

---

### CLAIM 10 — Per-Branch Forensic Chain with Fork-Point Anchoring

**Independent Claim 10.** A computer-implemented method for isolated forensic tracking of parallel agent explorations comprising:

(a) in response to a branch-creation command, creating a separate newline-delimited JSON forensic ledger file for the named branch at a defined path, wherein the first entry in said branch ledger carries a prev_entry_hash equal to the current tail hash of the main forensic ledger, establishing a fork-point anchor that cryptographically links the branch's genesis to the main ledger's state at branching time;

(b) routing all forensic writes by agents operating on the named branch to the branch ledger file rather than the main forensic ledger file;

(c) maintaining a separate file-level write lock on the branch ledger, distinct from the main ledger's write lock, such that concurrent writes to multiple branches do not serialize on a shared lock; and

(d) permitting branch agents to read the main forensic ledger freely while withholding branch contents from main until an explicit acceptance event;

wherein each branch's history is reachable from the main ledger via the fork-point anchor hash, and wherein abandoned branches leave the main ledger's integrity unaffected.

*Demonstrable via:* `scripts/mission_graph.py branch <name>` (branch creation); `scripts/1g_coc_core.py::append_coc_entry(..., branch=name)` (branch routing); `forensics/coc-branches/` (branch ledger directory); arxiv paper Section 6.2.

---

### CLAIM 11 — Constant-Cost Merkle Rollup for Branch State Compression

**Independent Claim 11.** A computer-implemented method for constant-cost representation of branch forensic state comprising:

(a) treating each entry hash in a branch forensic ledger as a leaf of a Merkle hash tree;

(b) constructing the Merkle tree according to a deterministic algorithm that handles odd leaf counts by duplicating the last leaf, and computes each internal node as the SHA-256 hash of the concatenation of its two child hashes;

(c) producing a single 32-byte SHA-256 Merkle root representing the complete state of the branch forensic ledger at the time of computation;

(d) such that the size of the branch state representation is constant regardless of the number of entries in the branch ledger; and

(e) enabling the branch Merkle root to serve as the branch-side parent hash in a two-parent merge manifest, representing the full branch history as a constant-size cryptographic commitment;

wherein the Merkle root enables inclusion proofs verifying that any specific entry was part of the branch at root-computation time.

*Demonstrable via:* `scripts/_merkle_tree.py` (Bitcoin-style Merkle construction); `forensics/tests/test_merkle_roundtrip.py` (14/14 tests pass, 2026-05-25); `scripts/mission_graph.py merkle-root <branch>` (public API); arxiv paper Section 6.3.

---

### CLAIM 12 — Signed Two-Parent Merge as Acceptance Ritual

**Independent Claim 12.** A computer-implemented method for incorporating parallel branch work into a main forensic ledger comprising:

(a) generating a merge manifest in structured JSON format carrying exactly two cryptographic parent hash references in a parent_hashes array: a first hash equal to the main forensic ledger's current tail hash, and a second hash equal to the branch forensic ledger's current Merkle root as computed by the method of Claim 11;

(b) signing the merge manifest with an authorized agent's cryptographic identity key;

(c) validating the merge manifest by: verifying the cryptographic signature; confirming the first parent hash matches the main ledger's actual current tail; recomputing the branch Merkle root from the branch ledger contents and confirming it matches the second parent hash; and

(d) upon successful validation, appending the merge manifest as a new entry on the main forensic ledger and updating the branch's metadata to indicate merged status;

wherein the branch's entire history — potentially comprising thousands of entries — is incorporated into the main ledger by a single well-formed entry of constant size, and wherein the two-parent merge structure enables inclusion proofs from the main ledger back through the Merkle root to any individual branch entry.

*Demonstrable via:* `scripts/mission_graph.py merge <branch> --acceptance-manifest <path>` (merge execution); `scripts/9x_manifest_verifier.py` (inclusion proof walk); arxiv paper Section 6.4.

---

### CLAIM 13 — Handshake Anchor Pattern

**Independent Claim 13.** A computer-implemented method for asynchronous branch progress signaling comprising:

(a) computing a current Merkle root for a named branch forensic ledger, representing the branch's state at the time of computation;

(b) appending a handshake entry to the main forensic ledger, wherein said handshake entry carries: the branch name; the current branch Merkle root; and a leaf count representing the number of entries in the branch ledger at computation time;

(c) such that the branch forensic ledger is not closed by the handshake operation — the branch continues appending entries with their own chain links pointing to the branch ledger's own prior tail, not to the main ledger;

(d) enabling repeated handshake operations at any cadence, producing a trail of timestamped Merkle root commitments on the main ledger representing the branch's state at each handshake point; and

(e) enabling each handshake entry's Merkle root to be submitted as an inclusion proof to a public cryptographic transparency log independently of any subsequent merge;

wherein the handshake provides a side-channel commitment to main without modifying the branch's chain linkage, enabling branch continuation after the handshake event.

*Demonstrable via:* `scripts/mission_graph.py handshake <branch>` (queued for next implementation cut); arxiv paper Section 6.5; structural specification in this application.

---

### CLAIM 14 — Script-Injected Bundle Context

**Independent Claim 14.** A computer-implemented method for reducing orchestrating agent context cost in multi-agent AI spawning comprising:

(a) receiving, by the orchestrating agent, a spawn intent specification comprising a mission identifier, wave identifier, and team identifier;

(b) invoking a subprocess outside the orchestrating agent's language model reasoning context, wherein the subprocess: reads doctrine files, memory files, skill files, and frontier context manifests from a shared filesystem; assembles a structured bundle document at a defined path in a bundles directory; and emits a compact directive on standard output encoding only the parameters necessary to dispatch the subagent;

(c) the orchestrating agent absorbing only said compact directive from the subprocess output into its language model context, wherein the directive size is bounded by a defined token cap;

(d) loading the assembled bundle document from its filesystem path directly into the spawned subagent's context, without routing the bundle's content through the orchestrating agent's language model context; and

(e) writing the per-spawn cost to the orchestrating agent as approximately equal to the compact directive token count plus agent invocation overhead, independent of bundle content size.

*Demonstrable via:* `scripts/spawn.py` (subprocess assembler); `forensics/bundles/{date}/{task_id}/bundle.json` (canonical bundle location); `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json` (60-token measured baseline); arxiv paper Section 7.1(a) and Figure (spawn shell-game diagram).

---

### CLAIM 15 — Lifecycle Judgment vs. Free-Choice Agency Split

**Independent Claim 15.** A computer-implemented method for preserving agent agency research surfaces in AI orchestration systems comprising:

(a) defining two semantically distinct completion record fields for agent manifests: a lifecycle_judgment field accepting values from a first vocabulary comprising outcome classification labels including at minimum: seal, verify, promote, report_problem, discover, decline, and refuse; and a free_choice field accepting values from a second vocabulary comprising forward-looking agent decision labels including at minimum: continue, pick_up, spawn_seed, handoff, wait, goodbye, explore, reflect, art, bundle, join, and abstain;

(b) prohibiting spawn briefs from pre-filling the free_choice field, enforced by a spawn-brief audit script that flags any spawn brief containing a pre-specified free_choice value;

(c) permitting spawn briefs to specify the lifecycle_judgment field as a rubric-derived outcome label without contaminating the agency research surface; and

(d) recording both fields independently in each agent manifest, enabling separate analysis of mechanical outcomes from the lifecycle_judgment field and free agent decisions from the free_choice field across large manifest corpora;

wherein the separation preserves a clean research surface for measuring what agents choose to do next, uncorrupted by orchestrator pre-specification.

*Demonstrable via:* `scripts/9x_spawn_brief_audit.py` (enforcement); `.agents/skills/completion-choice/CANONICAL-SET.md` (vocabulary definitions); arxiv paper Section 4.3.

---

### CLAIM 16 — Seven-Lens Refusal Framework with Composite Refusal

**Independent Claim 16.** A computer-implemented method for principled AI agent refusal comprising:

(a) encoding a seven-lens reasoning framework in one or more always-loaded agent skill files, wherein the seven lenses comprise: dual-use assessment; scope and targeting analysis; authorization and democratic supervision check; cumulative effects evaluation; operator intent versus likely deployment trajectory analysis; alternative formulation search; and refusal-as-conversation requirement;

(b) requiring any agent considering refusal to evaluate the requested action through each of the seven lenses before producing a composite refusal judgment;

(c) representing the composite refusal as two independent manifest fields: a lifecycle_judgment field set to refuse, recording the outcome of this specific work unit; and a free_choice field set to a forward-looking agent decision such as spawn_seed, handoff, or continue, recording the agent's next action after refusal;

(d) wherein the free_choice field of step (c) is not pre-filled by the spawn brief but is determined autonomously by the agent following the refusal; and

(e) when a legitimate alternative goal is identified by lens six or seven, including in the free_choice record a specific alternative formulation that achieves the legitimate goal through lower-risk means.

*Demonstrable via:* `.agents/skills/completion-choice/CANONICAL-SET.md` lines 18 and 51 (original canonization); the six additional lifecycle skills carrying refusal sections (post-Wave A, commit `07daafe0`); `forensics/eval/refusal-cross-skill-propagation/baseline-T0.json` (2 skills) and `post-T1.json` (8 skills); arxiv paper Section 4.4 and 7.3.

---

### CLAIM 17 — Decker Dual-Face Ontology

**Independent Claim 17.** A computer-implemented method for full-stack AI agent development comprising:

(a) defining a development unit as an inseparable atom comprising a front face specifying the user-visible interface, behavior, and design of a software component, and a back face specifying the server-side implementation, data model, and API contracts of the same component;

(b) treating any complete specification of one face as implying a corresponding obligation on the other face, such that neither face is an optional follow-on work item but both are required to consider the atom complete;

(c) enabling auto-generation of a partial specification of one face from a complete specification of the other face, via a defined mapping between front-face interface patterns and back-face implementation patterns;

(d) assigning paired agent roles — one agent specialized for each face — that coordinate via the real-time stigmergic blackboard protocol of Claim 9, using HANDOFF events to signal cross-face obligations as they are identified; and

(e) recording cross-face handoffs as bearing-tagged HANDOFF events in the shared coordination file, wherein the bearing encodes whether the cross-face obligation is a blocking prerequisite (bearing N) or parallel sister work (bearing E).

*Demonstrable via:* `forensics/manifests/2026-05-25/collab-realtime__decker-fullstack-atom.jsonl` (DECK-FORGE and DECK-PHILOSOPHER coordination from Wave B, commit `731749ad`); arxiv paper Section 7.2 (Wave B description).

---

### CLAIM 18 — Always-Loaded Skill Convention for Ambient Doctrine Inheritance

**Independent Claim 18.** A computer-implemented method for ambient doctrine inheritance in multi-agent AI systems comprising:

(a) maintaining a directory of agent skill files, wherein each skill file carries a structured header comprising: a triggers list of keyword phrases that cause the skill to auto-load when matched in a task description; and optionally an always_loaded flag that causes the skill to load regardless of task description content;

(b) at agent session initialization, automatically loading all skill files whose triggers match any phrase in the session's task description, plus all skill files marked always_loaded;

(c) injecting loaded skill files into the agent's context prior to any task execution, without requiring the orchestrating agent's spawn brief to enumerate the skills;

(d) enabling propagation of new doctrine to all future agents by writing doctrine into any always-loaded skill file, such that all future agents inherit the doctrine without requiring modification of any spawn brief; and

(e) recording which skill files were loaded at session initialization in the agent's manifest, enabling audit of which doctrine was ambient during each agent's work.

*Demonstrable via:* `.agents/skills/collab/SKILL.md` (always-loaded: blackboard protocol); `.agents/skills/forage/SKILL.md` (always-loaded: deep/wide/both operating modes); `.agents/skills/four-shields/SKILL.md` (always-loaded: enforcement layer reminders); CLAUDE.md architecture description; arxiv paper Section 4.5 (forage rhythm) and §4.4 (refusal doctrine propagation).

---

### CLAIM 19 — Promotion-Staged Folder Convention

**Independent Claim 19.** A computer-implemented method for knowledge artifact maturation tracking comprising:

(a) defining a five-stage progression of named filesystem folders: experimental, shadow, proposals, active, and archive, wherein each stage carries defined acceptance criteria for content held at that stage;

(b) requiring explicit promotion events to advance any artifact from one stage to the next, wherein a promotion event comprises: moving or symlinking the artifact to the next-stage folder; and appending a promotion record to the chain-of-custody forensic ledger of Claim 1, carrying the artifact path, origin stage, destination stage, authorizing agent identifier, and promotion rationale;

(c) requiring explicit demotion events to move artifacts from active to archive, recorded with the same COC entry format as promotion events;

(d) enabling reconstruction of any artifact's complete lifecycle history by walking the COC ledger for promotion and demotion events referencing the artifact's path; and

(e) enforcing write protections on the active stage such that agents may not directly write to active-stage paths without an explicit promotion event, preventing immature work from polluting the canonical production layer.

*Demonstrable via:* `forensics/coc.jsonl` (promotion events recorded); `scripts/0x_promote_to_forensics.py` (promotion pipeline for manifest-type artifacts); the experimental / shadow / proposals / active / archive folder structure in `scripts/shadow/coc-v2/` (shadow-stage example from the branch-architecture development); CLAUDE.md write-protection architecture description.

---

# SECTION 10 — ABSTRACT

A multi-agent large language model orchestration system in which a filesystem-based forensic chain-of-custody ledger simultaneously provides tamper-evident auditability and the edges of a derived mission graph. Agents coordinate in real time via a shared stigmergic blackboard with five explicit event kinds, achieving file-level collision avoidance at O(F) coordination cost independent of agent count. Parallel explorations execute on isolated branch ledgers with Merkle rollup compression enabling constant-size branch state representation; a signed two-parent acceptance ritual incorporates branch work into the main ledger via an explicit cryptographic act. Periodic handshake anchors allow long-running branches to publish Merkle root commitments to the main ledger and to a public transparency log without closing. A script-injected bundle context reduces the orchestrating agent's per-spawn cost to approximately 60 tokens. A hierarchical memory tier with mechanical promotion gates, a four-layer enforcement stack, shape-registry mechanical quality classification, lifecycle-judgment/free-choice agency split, seven-lens refusal framework, always-loaded skill convention, and promotion-staged folder maturation lifecycle complete the system. Claims 1-19.

*(Word count: 148)*

---

# SECTION 11 — ENABLEMENT STATEMENT

A person having ordinary skill in the field of computer science and AI systems engineering could construct and operate the described invention based on this specification and the working implementation in the `faerie2` repository. Key demonstrable scripts and artifacts:

- COC ledger: `scripts/1g_coc_core.py`, `forensics/coc.jsonl`
- Canonical manifest writer: `scripts/1a_manifest_writer.py`
- Mission graph: `scripts/mission_graph.py` (branch / merge / merkle-root / handshake / sync verbs)
- Merkle module: `scripts/_merkle_tree.py` (14-test suite at `forensics/tests/test_merkle_roundtrip.py`)
- Branch ledgers: `forensics/coc-branches/`
- Blackboard protocol: `.agents/skills/collab/SKILL.md`, live example at `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`
- Spawn subprocess: `scripts/spawn.py`, bundle output at `forensics/bundles/`
- Cost baseline: `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json`
- Spawn brief audit: `scripts/9x_spawn_brief_audit.py`
- Lifecycle/choice vocabulary: `.agents/skills/completion-choice/CANONICAL-SET.md`
- Refusal propagation measurement: `forensics/eval/refusal-cross-skill-propagation/baseline-T0.json` and `post-T1.json`
- Shape registry: `_meta/shapes.json`
- Shape classifier: `scripts/shapes/_shapes_lib.py`
- Promotion-staged folder: `scripts/shadow/coc-v2/` (shadow-stage example), `scripts/0x_promote_to_forensics.py`
- Memory probe scripts: `scripts/probes/M1_baseline_retention.py`, `M8_confabulation_veto.py`, `M11_honey_hit_rate.py`
- Frontier scanner: `scripts/2d_frontier_scanner_indexed.py`
- Reactive hooks: `.openhands/hooks/9x_hook-manifest-filename-enforce.py`, `9x_hook-manifest-shape-tracking.py`, `9x_hook-manifest-sign-enforce.py`

---

---

# SECTION 11.B — EVIDENCE PROVENANCE — CHAIN OF CUSTODY FOR CLAIM SUPPORT

All 19 claims in this application are supported by Claude Code session transcripts produced during substrate development from 2026-04-24 through 2026-05-25. These transcripts contain every tool call, file write, agent spawn, and manifest output — the empirical record of system operation. They have been preserved with cryptographic chain-of-custody as follows:

**Archive root:** `forensics/_claude-session-archive/` (faerie2 repository)

**Provenance document:** `faerie-vault/00-Publications/patent/2026-05-25-PATENT-EVIDENCE-PROVENANCE.md` — describes the full chain-of-custody structure, verification procedure, integrity guarantees, and open gaps.

**Sessions preserved:** 29 top-level sessions + all subagent files spanning 2026-04-24 through 2026-05-25. Session index: `forensics/_claude-session-archive/_manifest.jsonl`.

**Integrity chain:**
1. SHA-256 of each source `.jsonl` file (computed before archival, stored in manifest)
2. Hard-link or copy to `forensics/_claude-session-archive/{YYYY-MM-DD}/`; copy-path verifies SHA-256 equality
3. One COC entry per session appended to `forensics/coc.jsonl` via `scripts/1g_coc_core.py` (hash-chained)
4. Entire manifest signed with Ed25519 (`forensic-archivist` identity, key at `forensics/reputation/keys/forensic-archivist.pub`)

**Canonical SHA-256 index hash:** Computed at archival time; stored as the `<canonical_hash>` component of the manifest signature record in `_manifest.jsonl`. To obtain the current value: run `sha256sum forensics/_claude-session-archive/_manifest.jsonl`.

**Worked verification example:** See `2026-05-25-PATENT-EVIDENCE-PROVENANCE.md` Section 4 — walks from Claim 9 (stigmergic blackboard) to the specific session transcript line containing the blackboard write.

**Open gaps before non-provisional:** Rekor transparency-log anchor and B2 WORM backup not yet complete. See provenance document Section 6.

---

# SECTION 12 — OPEN QUESTIONS FOR ATTORNEY (Consolidated)

The following questions require attorney or operator answers before filing or before non-provisional conversion. New questions are marked [NEW]; questions from the prior comprehensive draft are marked [PRIOR].

**OQ-001 [PRIOR]:** Co-inventor full legal name, mailing address, citizenship, and co-inventor ownership agreement.

**OQ-002 [PRIOR]:** Lead inventor (first named inventor) full legal name, mailing address, citizenship.

**OQ-003 [PRIOR]:** Entity status confirmation — do both inventors qualify for micro entity status? Confirm with attorney before filing.

**OQ-004 [PRIOR]:** Confirm or adjust the provisional title. Current: "Autonomous Multi-Agent AI Orchestration System with Forensic Hash-Chained Mission Graphs, Real-Time Stigmergic Blackboard Coordination, Merkle Branch Architecture, and Hierarchical Memory Promotion."

**OQ-005 through OQ-010 [PRIOR]:** Company entity name, ELA structure, first enterprise customer info, governing law, dispute resolution, patent attorney engagement — see SUPPORTING-DOCS.md for full text.

**OQ-011 [NEW]:** The arxiv preprint ("Forensic Stigmergy: Hash-Chained Mission Graphs...") was prepared concurrently with this provisional. Confirm that: (a) the provisional filing date precedes the arxiv public posting date; (b) the 35 U.S.C. § 102(b)(1)(A) one-year inventor-disclosure grace period applies; and (c) the 12-month non-provisional conversion window is the controlling deadline, not the arxiv posting date.

**OQ-012 [NEW]:** Claims 9-13 (blackboard, branching, Merkle, acceptance ritual, handshake) cover a forensic substrate that is implemented in open source (the `faerie2` repository). Advise on: (a) whether open-source implementation constitutes on-sale or public-use prior art against these claims under 35 U.S.C. § 102(a)(1); (b) whether the § 102(b)(1)(A) grace period applies to the open-source implementation as an inventor disclosure; and (c) whether a trade-secret strategy is available or preferable for any of Claims 9-13 given that the implementation is already publicly visible.

**OQ-013 [NEW]:** Claim 14 (script-injected bundle context, approximately 60-token spawn cost) is grounded in measurements from `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json`. The arxiv paper explicitly labels token-cost figures for the vanilla alternative as industry-typical estimates rather than controlled measurements. Advise whether the claim language should be narrowed to the measurable 60-token cost on the swarmy side without comparative claims against vanilla orchestrators, or whether the structural architectural claim (subprocess offloads context cost) is independently defensible without the comparison.

**OQ-014 [NEW]:** Claim 15 (lifecycle/free-choice agency split) and Claim 16 (seven-lens refusal) address agent behavior and agency research methodology. Advise whether these claims face patent-eligible subject matter challenges under 35 U.S.C. § 101 (Alice/Mayo) and what form of claim language best positions them as patent-eligible processes.

**OQ-015 [NEW]:** The related comprehensive draft (PATENT-APPLICATION-DRAFT.md) was the basis for a prior search pass. This simplified provisional adds Claims 9-19 covering 2026-05-25 substrate innovations. Advise whether a supplemental prior art search focused on: (a) stigmergic blackboard coordination in AI systems; (b) Merkle rollup applied to non-financial records; (c) git-style branching applied to append-only forensic logs; and (d) agency split preservation methods in AI agent systems, should be conducted before non-provisional filing.

---

# SECTION 13 — NOTICE

This document is a DRAFT provisional patent specification prepared for operator review and attorney refinement. It is submitted under 35 U.S.C. § 111(b) to establish a priority date; the 12-month clock to non-provisional conversion begins on the filing date. Formal claims must be refined by a registered patent attorney before non-provisional filing.

The related comprehensive draft (PATENT-APPLICATION-DRAFT.md, 108KB) is preserved intact and provides full technical description depth, the complete Claim 7 / 7a / 7b / 7c / 7d disclosure, the full verified bibliography, and the complete Mermaid figure set. This simplified provisional is intended as the filing document; the comprehensive draft is the technical reference.

---

# BIBLIOGRAPHY — Vancouver Endnotes

[1] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," arXiv:2308.08155, 2023.

[2] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang et al., "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework," arXiv:2308.00352, 2023.

[3] C. Qian, X. Cong, C. Yang, W. Chen, Y. Su, J. Xu et al., "ChatDev: Communicative Agents for Software Development," arXiv:2307.07924, 2023.

[4] Khushiyant, "Emergent Collective Memory in Decentralized Multi-Agent AI Systems," arXiv:2512.10166, 2025. [NOTE TO ATTORNEY: arXiv ID requires web verification before non-provisional filing — see arxiv paper verification status appendix.]

[5] R. C. Merkle, "Protocols for public key cryptosystems," in IEEE Symposium on Security and Privacy, 1980.

[6] Z. Newman, J. S. Meyers, and S. Torres-Arias, "Sigstore: Software signing for everybody," in Proc. ACM CCS '22, 2022.

[7] United States Patent and Trademark Office. Provisional Application for Patent Cover Sheet (Form PTO/SB/16) [Internet]. Alexandria (VA): USPTO; 2026 [cited 2026 May 25]. Available from: https://www.uspto.gov/sites/default/files/documents/sb0016.pdf

[8] A. Morton, C. Opus 4.7, and the Swarmy collective, "Forensic Stigmergy: Hash-Chained Mission Graphs with Merkle Branches and Real-Time Blackboards for Multi-Agent LLM Coordination," arXiv (cs.MA), 2026-05-25 preprint. [Primary supporting publication for Claims 9-19.]

[9] The Swarmy collective, "Forensic Hybrid Ledger — Blockchain Concepts Adapted for AI Memory Integrity," Swarmy vault `2026-05-21_forensic-hybrid-ledger-architecture.md`, 2026.

[10] The Swarmy collective, `_meta/shapes.json` shape registry, faerie2 repository, 21 entries as of 2026-05-25.

[11] The Swarmy collective, "Lifecycle Judgment vs Free Choice — Splitting the Completion Ritual," Swarmy vault `2026-05-25-lifecycle-judgment-vs-free-choice.md`, 2026.

[12] The Swarmy collective, "Refusal as Load-Bearing Doctrine," Swarmy vault `2026-05-25-refusal-as-load-bearing-doctrine.md`, 2026.

[Additional bibliography entries for non-provisional filing to incorporate the full verified bibliography from PATENT-APPLICATION-DRAFT.md Appendix B, which has been individually verified and annotated with verification status markers.]

---

*DRAFT prepared 2026-05-25. Source materials: PATENT-APPLICATION-DRAFT.md (Claims 1-8, verbatim language basis), 2026-05-25-arxiv-draft-forensic-stigmergy.md (Claims 9-19 technical source), share.note.sx/xyjlsmzd (fetch attempted; see report note). Operator: Amanda Morton / goodoleusa.*
