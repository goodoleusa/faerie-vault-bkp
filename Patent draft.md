
# PATENT PROVISIONAL SPECIFICATION

## Autonomous Multi-Agent Orchestration System with Forensic Cryptographic Backbone, Append-Only Hash-Chained Chain-of-Custody, Stigmergic Filesystem Coordination, Four-Layer Enforcement Stack, and Mechanical Quality Classification

Jessica Terry and Amanda Morton

**Filing type:** Provisional Application for Patent  
**Filing basis:** 35 U.S.C. § 111(b)  
**Cover sheet:** USPTO Form SB/16 (PTO/SB/16) — attach separately  
**Entity status:** Individual inventors (micro entity filing recommended — verify current qualification criteria at USPTO fee schedule)  
**Filed by:** Amanda Morton and Jessica Terry, joint inventors  
**Note:** This is a DRAFT specification prepared for attorney review. Inventor names, residence addresses, and entity information must be completed before filing.

### CROSS-REFERENCE TO RELATED APPLICATIONS

No prior provisional or non-provisional applications are claimed as priority. This application establishes the initial priority date for all subject matter described herein.

The inventors note that a related technical charter (`forensic-coc-v2-rekor`) covering a Merkle-tree-based forensic chain-of-custody architecture may be subject to a separate or combined provisional filing — this is an open question recorded in Section 7 (Open Questions for Attorney).

### FIELD OF THE INVENTION

This invention relates to multi-agent artificial intelligence orchestration systems, and more particularly to:

(1) a forensic cryptographic backbone comprising an append-only ed25519-signed hash-chained chain-of-custody ledger (COC), Merkle rollups providing constant-cost branch state compression, Rekor transparency-log anchoring for public tamper-evidence, B2 WORM immutable cloud backup, and zero-vendor customer-key custody — this backbone is the foundational spine from which all other system properties derive their integrity;

(2) a hierarchical memory architecture with mechanical promotion gates between memory tiers, whose tamper-evident auditability is provided by the forensic backbone;

(3) a stigmergic agent coordination system using filesystem manifests as the sole coordination substrate, all manifest writes chained into the forensic backbone;

(4) a four-layer enforcement stack modeled on biological immune system defense, whose recovery audit layer reads the forensic backbone; and

(5) a mechanical quality classification system using shape registries with declared target directions, whose measurement substrate is grounded in the backbone's tamper-evident records.

The invention further claims the novel combination of all five modules into a single coherent AI orchestration ecosystem whose trustworthiness derives architecturally from the forensic backbone rather than from organizational policy.

### BACKGROUND OF THE INVENTION

**1. Problems in current AI agent memory systems**

Current large language model (LLM) agent systems suffer from memory degradation and hallucination caused by undifferentiated memory storage. Systems that store all observations in a single flat memory layer (e.g., a single vector database or a monolithic context window) fail to distinguish between raw unverified observations, validated cross-session facts, and immutable invariants. This causes several specific technical failures:

(a) **Stale memory contamination**: Observations that were valid in one session but later invalidated by new evidence continue to surface in retrieval, causing agents to act on outdated or contradictory beliefs. Current systems provide no mechanical gate between raw observations and the long-term memory store.

(b) **Hallucination amplification**: Without a promotion gate that requires minimum confidence score and cross-session citation count, low-confidence observations propagate into long-term memory and generate compounding errors across future sessions.

(c) **Context window saturation**: Flat memory architectures inject all historical observations into every agent's context at startup, consuming large fractions of the available token budget before any new work begins. A 200,000-token context window with naive memory injection may be 60-80% consumed by historical data before the agent performs its first action.

(d) **No measurement substrate**: Current systems lack a mechanical substrate linking memory operations to measurable quality outputs. There is no programmatic way to assert "memory promotion improved agent quality" without manual evaluation.

**2. Problems in current multi-agent coordination systems**

Current multi-agent AI systems rely on one of two coordination patterns, both of which introduce serious bottlenecks:

(a) **Orchestrator/router pattern**: A central orchestrator LLM receives all agent requests, routes them to worker agents, and aggregates results. This creates a single point of failure, a throughput bottleneck, and imposes LLM inference cost on every inter-agent communication. Scaling to N agents scales the orchestrator linearly.

(b) **Message-passing pattern**: Agents communicate via message queues or direct API calls. This requires agents to maintain awareness of each other's addresses and availability, creating tight coupling. Cost of each message to N agents scales quadratically, not just linearly. Message-passing systems fail silently when an agent is unavailable, and produce race conditions when multiple agents attempt to update shared state concurrently. Main reason for bugginess and failure of Claude's Agent Teams feature.

Neither pattern enables true emergent coordination — the ability for agents to discover each other's work and self-route to unblocked tasks without explicit scheduling.

**3. Problems in current AI safety enforcement systems**

Current AI safety systems apply enforcement reactively — monitoring outputs after they are produced and flagging violations. This reactive-only approach has two fundamental problems:

(a) **Cost at the wrong layer**: Catching a harmful output after generation is maximally expensive in terms of compute, latency, and potential damage. Prevention before generation is orders of magnitude cheaper but current systems rarely achieve structural prevention.

(b) **Whack-a-mole without immune memory**: Reactive systems catch specific known violations but do not build up a structural immune response. The same class of violation recurs in new forms because the underlying structural gap was never closed. Current systems have no analog to the biological immune system's memory T-cell mechanism that produces faster, stronger responses to previously-seen threats.

**4. Problems in current AI quality measurement**

Current AI system quality evaluation relies on human judgment or LLM-as-judge approaches. Both suffer from:

(a) **Vibe-based verdicts**: Human and LLM evaluators produce subjective assessments ("this looks better") that are not reproducible across sessions, not comparable across agents, and cannot drive automated improvement loops.

(b) **No genetic algorithm substrate**: Without integer-comparable, mechanically-produced quality signals, it is impossible to implement selection pressure that reliably improves agent behavior over time. Genetic algorithm-style improvement requires fitness functions that are deterministic, comparable, and not dependent on human judgment for each evaluation.

### SUMMARY OF THE INVENTION

The present invention provides an autonomous multi-agent orchestration system built on a **Forensic Cryptographic Backbone** that is the foundational load-bearing spine from which all other system properties inherit their integrity. Five technical modules compose on top of this backbone:

**Forensic Cryptographic Backbone — The Load-Bearing Spine**  
An append-only, ed25519-signed, SHA-256 hash-chained chain-of-custody ledger (`forensics/coc.jsonl`) in which each entry carries a `parent_hashes[]` DAG array linking to its predecessor(s), enabling both linear chain and two-parent merge structures. The backbone provides:

(1) **append-only tamper-evidence** — modifying any historical entry invalidates all subsequent hashes, mechanically detectable by `scripts/manifest_verifier.py`;

(2) **Merkle rollups** — per-branch forensic trees compressed to a constant 32-byte root via `scripts/_merkle_tree.py` (14/14 tests pass, SHA-256: `79d22d9e…`), enabling branch history of arbitrary depth to be represented in a single COC entry;

(3) **Rekor transparency-log anchoring** — handshake Merkle roots submitted to Sigstore Rekor (log_index 1630813609 for v2 genesis seal, entry_hash `80f56b10…`, commit `6890b4ab`), creating a public tamper-evident timestamp independent of the operator;

(4) **B2 WORM immutable backup** — 7-year WORM retention via `scripts/b2_realtime_uploader.py` triggered on every manifest write, making historical records irrecoverable from tampering;

(5) **zero-vendor customer-key custody** — ed25519 signing keys generated server-side, delivered to customer via zero-retention pipeline, and erased from vendor storage, such that vendor cannot forge chain-of-custody signatures (Claim 7 architecture). This backbone is not a feature of the system — it is the foundation every other module writes into and reads from for its integrity guarantees.

**Module 1 — Hierarchical Memory Architecture with Mechanical Promotion Gates (inherits backbone)**  
A three-tier memory system (dust → silver → GOLD) with a separate immutable forensic layer (forensics/), in which promotion between tiers is governed by mechanical rules: minimum confidence score (≥0.95), minimum session age (≥3 sessions), and minimum independent cross-session citation count (≥2). Promotion is executed by a canonical script (`scripts/manifest_writer.py`) that simultaneously evaluates gate criteria and appends an entry to the forensic backbone's append-only COC (`forensics/coc.jsonl`) with SHA-256 hash linking between entries and ed25519 signature. The backbone provides the tamper-evident audit trail that makes the promotion decision legally and technically defensible.

**Module 2 — Stigmergic Filesystem Coordination (inherits backbone)**  
A multi-agent coordination architecture in which agents discover each other's work and self-route to unblocked tasks exclusively through shared filesystem artifacts (manifests). No message-passing, no central orchestrator, no inter-agent API calls. Agents write manifests to a flat daily folder (`forensics/ephemeral/{YYYY-MM-DD}/`) following a deterministic filename grammar. A frontier scanner (`scripts/2d_frontier_scanner_indexed.py`) enables O(1) lookup of unblocked tasks by reading an 8KB daily index rather than scanning all manifests, reducing context cost by approximately 80% versus naive full-manifest scanning. Every manifest write is chained into the forensic backbone via PostToolUse hooks, so coordination history is tamper-evident.

**Module 3 — Four-Layer Enforcement Stack, Four-Shields (inherits backbone)**  
A discipline enforcement architecture modeled on biological immune system defense, comprising: (a) structural prevention (wrong behavior cannot be expressed, enforced by schema and canonical writer scripts); (b) cognitive reminder (skill files auto-loaded before action); (c) reactive blocking (PostToolUse hooks reject violations at OS write boundary); and (d) recovery audit (periodic batch scans that surface escaped violations and update reputation scores). The recovery layer reads the forensic backbone's COC chain to audit enforcement history. Each layer is cheaper to operate than the next, and the four layers together provide defense-in-depth that no single layer can provide alone.

**Module 4 — Shape Registry with Mechanical Verdict Classification (inherits backbone)**  
A quality classification system in which every recognizable, countable pattern of work ("shape") is declared in a registry (`_meta/shapes.json`) with a `target_direction` field (increasing/decreasing/bounded/stable). A reactive hook classify_verdict computes mutation verdicts (beneficial/neutral/harmful/uncertain) by comparing the observed count delta to the target direction and a noise threshold. No LLM judgment in the verdict path. Quality signals are integer-comparable across sessions, enabling genetic-algorithm-style improvement selection. Verdict records are written to the forensic backbone, making the quality history tamper-evident.

**Module 5 — Membench Quality Measurement Substrate (inherits backbone)**  
A quality measurement architecture in which evaluation probes (M1 baseline retention, M8 confabulation veto, M11 silver bootstrap uptime, and their F-series internal mirrors) are themselves first-class shapes in the shape registry. This creates a closed loop between memory operations and quality measurement: memory promotion decisions directly affect probe scores, which are classified mechanically by the same shape-registry verdict system that classifies all other work patterns. The membench scorer (`scripts/3k_membench_scorer.py`) computes M3 (efficiency), SI (stigmergy index), and SBI (switchboard burden index) deterministically from fixed eval data, enabling reproducible T0 vs T1 comparison. Probe results are anchored to the backbone, providing a tamper-evident quality history.

**Combination Claim — Overall Novel System**

Info

The novel combination of the forensic cryptographic backbone and all five modules into a single coherent AI orchestration ecosystem where every claim of quality improvement, every coordination event, and every enforcement decision is backed by the same cryptographic substrate. Individual modules may be open-sourced; the combination claim retains patent protection over the integrated system design whose integrity derives architecturally from the forensic backbone rather than from organizational policy.

## Part C: Prior Art Search Guidance (for patent attorney)

Recommended search areas before filing:

1. AWS KMS / Google Cloud KMS / Azure Key Vault — CMK/BYOK patterns (distinguished in §7.4)
2. "Client-side encryption" in cloud storage literature (S3 client-side encryption SDK, etc.)
3. HIPAA-compliant zero-knowledge cloud storage (e.g., Tresorit, SpiderOak architecture)
4. Zero-knowledge proof protocols (separate technical domain — these are mathematical verification protocols, not data custody architectures; confirm claim language clearly distinguishes)
5. "Convergent encryption" / "client-side key management" in distributed storage literature
6. US Patent 10,992,464 (Microsoft Azure confidential computing) and related portfolio

 ## Bibliography
 
 "Provisional Application for Patent Cover Sheet," updated March 2026 (last revision date confirmed), mandatory form for provisional filings per 35 U.S.C. § 111(b) and 37 C.F.R. § 1.53(c).
1. United States Patent and Trademark Office. Provisional Application for Patent Cover Sheet (Form PTO/SB/16) [Internet]. Alexandria (VA): USPTO; 2026 [cited 2026 May 23]. Available from: https://www.uspto.gov/sites/default/files/documents/sb0016.pdf

   > Current filing fees confirmed:
   > -  micro entity $65, 
   > - small entity $130, 
   > - regular undiscounted $325. (Note: WebFetch of PDF directly was not attempted due to tool restrictions; URL confirmed via USPTO domain search result.)

2. Chatterjee M. deftio/provisional-patent-template [Internet]. GitHub; 2024 [cited 2026 May 23]. Available from: https://github.com/deftio/provisional-patent-template

> repository is a free, open-source provisional patent template for U.S. patents, created by Manu Chatterjee (deftio). Contains Word (.docx) template, RTF version, filled example (PDF), and tutorial article. 
> 
> Repository states it has been "used to generate dozens of granted patents" and is licensed under BSD-2. Content matches LUMO's description of "provisional patent template."

3. GitLaw. Free End-User License Agreement Template [Internet]. GitLaw Community Legal Library; [date unknown] [cited 2026 May 23]. Available from: https://git.law/templates/doc/free-end-user-license-agreement-template-your-essential-eula-resource-AoyrQ3

4. United States Patent and Trademark Office. Assignment Center [Internet]. Alexandria (VA): USPTO; [date unknown] [cited 2026 May 23]. Available from: https://assignmentcenter.uspto.gov

> USPTO Assignment Center is the active system for recording patent and trademark assignments, having replaced EPAS and ETAS. 
> 
> Supports Patent Assignment Recordation Cover Sheet filing + PDF/TIFF attachment.
> Contact email: AssignmentCenter@uspto.gov. Customer service: 571-272-3350. URL is active on USPTO's official domain.

5. GitHub Inc. GitHub Customer Agreement General Terms (March 2025) [Internet]. San Francisco (CA): GitHub Inc.; 2025 Mar [cited 2026 May 23]. Available from: https://assets.ctfassets.net/8aevphvgewt8/luAPHjODK4vAYIpwisJfC/88a1961a9c7fcbb8d02a86d5d4635295/GCA_-_2025_03_-_GitHub_Customer_Agreement_General_Terms_-_FINAL_locked.pdf
6.  United States Patent and Trademark Office. Subject Matter Eligibility (SME) Guidance — Memorandum to Patent Examining Corps re: AI and Software Claims (August 4, 2025) [Internet]. Alexandria (VA): USPTO; 2025 Aug 4 [cited 2026 May 23]. Available from: https://www.uspto.gov/sites/default/files/documents/memo-101-20250804.pdf (direct PDF); see also: https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility (canonical SME page).

7. Martensen IP. USPTO Memo 2025: New Guidance on Software Patent Eligibility and AI [Internet]. Martensen IP Blog; 2025 Oct [cited 2026 May 23]. Available from: https://www.martensenip.com/blog/2025/october/uspto-memo-2025-brings-breakthrough-for-software/