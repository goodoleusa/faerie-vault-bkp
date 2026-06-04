---
title: "PATENT CLAIMS MASTER — Complete Claim Corpus (Frankenstein Reassembly)"
date: 2026-06-03
version: v2-finalized
status: DRAFT — attorney review required before USPTO filing
filing_basis: 35 U.S.C. § 111(b)
source_authority: >
  Canonical claim language drawn verbatim from:
  (A) docs/patent/_source/PATENT-PROVISIONAL-19-CLAIMS-FULL.md [2026-05-25, primary]
  (B) docs/patent/PATENT-APPLICATION-DRAFT.md Appendix A [2026-05-23, reclaimed subclaims]
  (C) docs/patent/_source/PATENT-CLAIM-7-ZERO-KNOWLEDGE.md [2026-05-23, authoritative Claim 7 source]
  Reconciliation reference: docs/patent/CLAIM-NUMBERING-RECONCILED.md [2026-06-02]
  Dependency structure reference: hustle/templates/packages/main-hub/src/pages/patent.html [live badge map]
---

> **DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE FILING**
>
> This is the canonical master claims corpus. It contains EVERY claim from all source documents —
> the 19-claim provisional set PLUS the four reclaimed dependent subclaims (7a, 7b, 7c, 7d) that
> were present in the comprehensive draft (PATENT-APPLICATION-DRAFT.md) but dropped from the
> simplified provisional (PATENT-PROVISIONAL-19-CLAIMS-FULL.md). Nothing has been discarded.
>
> Source provenance is annotated in brackets after each claim's opening line. Claim language is
> reproduced verbatim from the cited source; no substantive edits have been made. The "7e"
> referenced in PATENT-APPLICATION-DRAFT.md is a reference to element (e) within the Claim 7
> body (the data signing module), NOT a standalone dependent claim — this has been clarified
> in the reconciliation table.
>
> Inventor names, residence addresses, citizenship, and entity information must be completed
> before any USPTO submission. Open questions for attorney are consolidated in
> PATENT-PROVISIONAL-19-CLAIMS-FULL.md Section 12.

---

# CLAIM-TREE OUTLINE
*(independent claims in bold; dependents indented beneath their parent)*

- **CLAIM 1** — Memory Orchestration Hierarchy with Mechanical Promotion Gates *(independent)*
- **CLAIM 2** — Stigmergic Multi-Agent Coordination via Filesystem Manifests *(independent)*
- **CLAIM 3** — Four-Layer Enforcement Stack *(independent)*
- **CLAIM 4** — Shape Registry with Mechanical Verdict Classification *(independent)*
- **CLAIM 5** — Membench Quality Measurement Substrate *(dependent on Claim 4)*
  - CLAIM 6 — Overall Novel Combination *(dependent on Claims 1–5 in combination)*
- **CLAIM 7** — Zero-Knowledge Customer-Key-Custody Architecture *(independent)*
  - CLAIM 7a — Multi-Region Residency *(dependent on Claim 7)*
  - CLAIM 7b — Breach Notification Safe Harbor *(dependent on Claim 7)*
  - CLAIM 7c — Integration with AI Orchestration *(dependent on Claim 7)*
  - CLAIM 7d — Extension to Signing Keys / Zero Vendor-Side Cryptographic Surface *(dependent on Claim 7)*
- **CLAIM 8** — Four-Bulkheads Cyber Defense *(independent)*
- **CLAIM 9** — Real-Time Stigmergic Blackboard with Five-Event Grammar *(independent)*
- **CLAIM 10** — Per-Branch Forensic Chain with Fork-Point Anchoring *(independent)*
- **CLAIM 11** — Constant-Cost Merkle Rollup for Branch State Compression *(independent)*
- **CLAIM 12** — Signed Two-Parent Merge as Acceptance Ritual *(independent per provisional label; references Claim 11 method)*
- **CLAIM 13** — Handshake Anchor Pattern *(independent)*
- **CLAIM 14** — Script-Injected Bundle Context *(independent)*
- **CLAIM 15** — Lifecycle Judgment vs. Free-Choice Agency Split *(independent)*
- **CLAIM 16** — Seven-Lens Refusal Framework with Composite Refusal *(independent)*
- **CLAIM 17** — Decker Dual-Face Ontology *(independent; references Claim 9 blackboard)*
- **CLAIM 18** — Always-Loaded Skill Convention for Ambient Doctrine Inheritance *(independent)*
- **CLAIM 19** — Promotion-Staged Folder Convention *(independent; references Claim 1 COC ledger)*

**Labeled independent claims: 19** (C1, C2, C3, C4, C5, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19 — and C5 is labeled "independent" in the v19 provisional despite depending on C4 registry concept)
**Labeled dependent claims: 4** (C6 on C1–C5; C7a/7b/7c/7d on C7)
**Total: 23 claims**

> **Reading note for claim-tree structure:**
> C6 is the only numbered claim explicitly labeled "Dependent Combination." Claims 7a, 7b, 7c,
> 7d are explicitly labeled "Dependent." All other claims are labeled "Independent" in the
> source provisional, even where the claim body cross-references another claim's method.
> Each dependent claim block appears immediately after its parent claim in this document.
> Attorney should review C5 (references C4 registry), C12 (references C11 method), C16
> (shares vocabulary with C15), and C17 (references C9 blackboard) for possible re-labeling
> as dependent claims before non-provisional filing.

---

# MASTER CLAIMS — ORDERED BY INDEPENDENT CLAIM WITH DEPENDENTS IN SEQUENCE

---

## CLUSTER A — Forensic Hash-Chained COC Ledger and Derived Mission Graph

### CLAIM 1 — Memory Orchestration Hierarchy with Mechanical Promotion Gates
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 1*

**Independent Claim 1.** A computer-implemented method for AI agent memory management comprising:

(a) maintaining a first memory tier comprising raw session-scoped agent observations formatted as structured log entries;

(b) maintaining a second memory tier comprising validated cross-session facts subject to a configurable tail window of N entries, wherein facts in the second tier carry confidence scores in a defined range;

(c) maintaining a third memory tier comprising crystallized permanent invariants that have satisfied a mechanical promotion gate comprising: a minimum confidence score threshold; a minimum session age threshold; and a minimum count of independent cross-session citations; and

(d) enforcing said mechanical promotion gate by executing a canonical writer script that simultaneously: evaluates the gate criteria against the candidate fact's metadata; appends a new entry to an append-only chain-of-custody audit log carrying a SHA-256 hash of the immediately preceding entry; and triggers backup of the audit log to write-once-read-many cloud storage;

wherein the promotion decision is mathematical rather than a judgment by a language model.

*Demonstrable via:* `scripts/1a_manifest_writer.py` (canonical writer, enforces gate); `forensics/schemas/formulas/honey-confidence-floor.formula.json` (gate thresholds, SHA-256: `f6304de8…`); `forensics/coc.jsonl` (append-only ed25519-signed hash-chained audit log, 74 entries, SHA-256: `06e89e5c…`); Rekor anchor log_index 1630813609; B2 WORM 7-year retention (`scripts/5x_b2_realtime_uploader.py`); PATENT-PROVISIONAL-19-CLAIMS-FULL.md §8.B (detailed description). **Terminology note (2026-06-04):** Claim language uses tier names "first memory tier", "second memory tier", "third memory tier" — implementation terms "dust" (tier 1, formerly "pollen"), "silver" (tier 2, formerly "NECTAR"), "GOLD" (tier 3) are updated per nautical ontology. Claim language is substrate-neutral and unaffected by implementation term changes.

---

### CLAIM 2 — Stigmergic Multi-Agent Coordination via Filesystem Manifests
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 2*

**Independent Claim 2.** A computer-implemented method for multi-agent AI coordination comprising:

(a) writing agent work records as structured manifest files to a shared flat filesystem folder, wherein each manifest carries a deterministic filename encoding mission address, agent type, and timestamp in a defined grammar;

(b) maintaining a pre-computed index of manifests grouped by mission address and compass bearing;

(c) enabling each agent to discover unblocked tasks by reading the index file rather than scanning all manifests; and

(d) routing agents to unblocked tasks without message-passing, without a central orchestrator routing layer, and without inter-agent API calls;

wherein the filesystem is the exclusive coordination substrate and agent self-routing arises from each agent reading the index and writing to the shared folder.

*Demonstrable via:* `scripts/2d_frontier_scanner_indexed.py` (indexed frontier scanner); `scripts/1a_manifest_writer.py` (filename grammar enforcer); `.openhands/hooks/9x_hook-manifest-filename-enforce.py` (reactive hook); PATENT-PROVISIONAL-19-CLAIMS-FULL.md §8.A.2.

---

### CLAIM 3 — Four-Layer Enforcement Stack
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 3*

**Independent Claim 3.** A computer-implemented system for AI safety enforcement comprising four layers:

(a) a structural layer preventing generation of non-conforming artifacts via schema definitions and canonical writer script enforcement operating at construction time;

(b) a cognitive layer providing pre-task constraint reminders via skill files that auto-load when an agent's task description matches defined keyword triggers;

(c) a reactive layer blocking non-conforming writes at operating system write boundaries via hooks that execute after each write tool call and reject writes that fail defined predicates; and

(d) a recovery layer periodically scanning for escaped violations via batch audit scripts and updating agent reputation scores based on patterns in outcome classifications over time;

wherein each layer operates at lower computational cost than the subsequent layer, and the four layers together provide defense-in-depth such that violations are caught at the least expensive possible layer.

*Demonstrable via:* `.openhands/hooks/9x_hook-manifest-filename-enforce.py`, `9x_hook-manifest-shape-tracking.py`, `9x_hook-manifest-sign-enforce.py` (reactive layer); `scripts/shapes/audit-shapes.py` (recovery layer); PATENT-PROVISIONAL-19-CLAIMS-FULL.md §8 Section 3.

---

### CLAIM 4 — Shape Registry with Mechanical Verdict Classification
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 4*

**Independent Claim 4.** A computer-implemented method for AI quality classification comprising:

(a) registering recognizable countable patterns of agent work as shapes in a registry, wherein each shape declaration specifies: a unique shape identifier; a target direction field from the set {increasing, decreasing, bounded, stable}; and a numeric noise threshold;

(b) executing a mechanical verdict classifier that computes a verdict for an observed count change by: computing delta as the difference between observed new count and baseline count; and selecting verdict beneficial, neutral, or harmful by comparing delta to the product of noise threshold and baseline count according to a deterministic table indexed by target direction;

(c) recording verdicts and updated counts to a history array in the registry without invoking any language model judgment in the verdict computation path; and

(d) composing shape counts into formula-based metrics that drive agent improvement selection decisions.

*Demonstrable via:* `scripts/shapes/_shapes_lib.py::classify_verdict()` (mechanical classifier); `_meta/shapes.json` (registry); `.openhands/hooks/9x_hook-manifest-shape-tracking.py` (reactive integration); PATENT-PROVISIONAL-19-CLAIMS-FULL.md §8 Section 4.

---

### CLAIM 5 — Membench Quality Measurement Substrate
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 5*

**Independent Claim 5.** A computer-implemented system for AI quality measurement comprising:

(a) declaring evaluation probes as shapes in the shape registry of Claim 4, wherein probe declarations include a `membench_probe: true` marker;

(b) classifying probe score changes using the same mechanical verdict classifier applied to all other shapes in the registry; and

(c) creating a closed feedback loop in which memory architecture promotion decisions directly affect probe scores, which are classified as beneficial or harmful mutations, which in turn drive memory architecture improvement decisions;

wherein the measurement system requires no human evaluation at any step of the quality assessment loop.

*Demonstrable via:* `scripts/probes/M1_baseline_retention.py`, `M8_confabulation_veto.py`, `M11_honey_hit_rate.py`; `scripts/3k_membench_scorer.py`; PATENT-PROVISIONAL-19-CLAIMS-FULL.md §8 Section 5.

---

### CLAIM 6 — Overall Novel Combination
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 6*

**Dependent Combination Claim 6.** The system of Claims 1 through 5 in combination, wherein:

the memory tier architecture of Claim 1 provides the data source for quality probes of Claim 5; the quality probes are classified by the mechanical verdict system of Claim 4; the shape registry of Claim 4 enforces probe measurement integrity via the four-layer enforcement stack of Claim 3; the enforcement stack operates on artifacts produced by the stigmergic coordination system of Claim 2; and the stigmergic coordination system reads from and writes to the memory architecture of Claim 1;

creating an integrated autonomous multi-agent orchestration ecosystem in which all quality signals are mechanically produced, all coordination is filesystem-mediated, all enforcement is layered from structural prevention to recovery audit, and all memory promotion is gated by mathematical criteria.

---

## CLUSTER B — Zero-Knowledge Customer-Key-Custody Architecture

### CLAIM 7 — Zero-Knowledge Customer-Key-Custody Architecture
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 7; verbatim basis: docs/patent/_source/PATENT-CLAIM-7-ZERO-KNOWLEDGE.md Part A*

**Independent Claim 7.** A computer-implemented system for providing zero-knowledge customer-key-custody in a multi-tenant artificial intelligence service platform for regulated industries, the system comprising:

(a) a payment-triggered provisioning module configured to, upon completion of a customer payment transaction, automatically allocate a customer-scoped object storage namespace isolated from all other customer namespaces via independent access credentials;

(b) a cryptographic key generation module configured to generate, server-side and in-memory only without persisting to durable storage:
    (i) a public/private encryption keypair for encrypting customer data at rest, and
    (ii) a public/private signing keypair for cryptographic attestation of customer data integrity;

(c) a zero-retention key delivery module configured to:
    (i) transmit the private encryption key and private signing key to a customer-designated electronic mail address at time of provisioning, and
    (ii) irrevocably erase both private keys from all vendor-controlled memory and storage upon confirmed delivery, such that the vendor retains no copy of either private key in any storage medium after the delivery transaction completes;

(d) an encryption-at-rest module configured to encrypt all customer plaintext data using the customer's public encryption key before writing to the customer-scoped storage namespace, such that all data persisted in vendor storage infrastructure exists exclusively in ciphertext form; and

(e) a data signing module configured to produce a cryptographic signature over stored customer data records using the customer's signing key, enabling tamper detection and forensic chain-of-custody verification;

wherein the vendor system, having executed step (c), is architecturally and technically incapable of decrypting any stored customer ciphertext or forging any customer-signed record without the customer's private keys;

wherein the customer holds exclusive private-key custody and is thereby the canonical data controller of all customer content stored in vendor infrastructure, regardless of physical infrastructure location; and

wherein the system provides compliance with data sovereignty requirements of one or more of the European Union General Data Protection Regulation (Regulation (EU) 2016/679), the United States Health Insurance Portability and Accountability Act (45 CFR Part 164), the Ontario Personal Health Information Protection Act 2004, and analogous jurisdiction-specific privacy frameworks, by architectural construction rather than by organizational policy.

*Demonstrable via:* `scripts/b2-admin/0b-b2-provision.py` (reference implementation); PATENT-CLAIM-7-ZERO-KNOWLEDGE.md §7.2 (technical sequence); PATENT-APPLICATION-DRAFT.md Appendix A Part A (verbatim language, preserved).

---

> **RECLAIMED SUBCLAIMS — CLAIM 7a, 7b, 7c, 7d**
>
> The following four subclaims were present in the comprehensive reference draft
> (PATENT-APPLICATION-DRAFT.md Appendix A, 2026-05-23) and in the authoritative
> standalone source (PATENT-CLAIM-7-ZERO-KNOWLEDGE.md). They were NOT reproduced in
> PATENT-PROVISIONAL-19-CLAIMS-FULL.md (the simplified 2026-05-25 provisional filing
> version), which only noted their existence via the line: "Dependent claims 7a (GDPR
> multi-region residency), 7b (HIPAA breach safe-harbor 45 CFR 164.402), 7c (orchestration
> integration) preserved from PATENT-APPLICATION-DRAFT.md Appendix A." Claim 7d appeared
> in full in PATENT-PROVISIONAL-19-CLAIMS-FULL.md immediately after Claim 7.
>
> NOTE on "Claim 7e": PATENT-APPLICATION-DRAFT.md uses "7(e)" as a reference to
> element (e) within the body of Claim 7 (the data signing module). This is NOT a
> standalone dependent claim. No "Claim 7e" exists as a separate dependent claim in any
> source document. Claim 7c references the data signing module as "Claim 7(e)" using
> patent claim element notation, not a separate dependent subclaim designation.

---

### CLAIM 7a — Multi-Region Residency (Dependent on Claim 7)
*Source: PATENT-APPLICATION-DRAFT.md Appendix A §Claim 7a; verbatim basis: PATENT-CLAIM-7-ZERO-KNOWLEDGE.md §Claim 7a*
*Status: RECLAIMED — was dropped from PATENT-PROVISIONAL-19-CLAIMS-FULL.md; restored here*

**Dependent Claim 7a.** The system of Claim 7, wherein the customer-scoped storage namespace provisioned in step (a) is allocated in a geographic region selected based on the customer's declared jurisdiction of data residency, including at least one European Union-sovereign storage region, such that customer data subject to GDPR data-residency requirements may be stored without cross-border transfer to non-EU infrastructure; and wherein, when cross-border transfer is required, Commission Implementing Decision (EU) 2021/914 Standard Contractual Clauses are applicable as the transfer mechanism.

*Legal basis:* GDPR Art. 46; Commission Implementing Decision (EU) 2021/914 of 4 June 2021 (standard contractual clauses for third-country data transfers), OJ L 199:31-61, 7 June 2021 [VERIFIED — EUR-Lex CELEX 42021D0914].

---

### CLAIM 7b — Breach Notification Safe Harbor (Dependent on Claim 7)
*Source: PATENT-APPLICATION-DRAFT.md Appendix A §Claim 7b; verbatim basis: PATENT-CLAIM-7-ZERO-KNOWLEDGE.md §Claim 7b*
*Status: RECLAIMED — was dropped from PATENT-PROVISIONAL-19-CLAIMS-FULL.md; restored here*

**Dependent Claim 7b.** The system of Claim 7, wherein, in the event of unauthorized access to the customer-scoped storage namespace, the exclusively ciphertext-form stored data satisfies the definition of protected health information rendered "unreadable, unusable, or indecipherable" under HHS guidance implementing 45 CFR § 164.402(2), thereby qualifying the applicable party for the breach notification safe harbor under 45 CFR Part 164 Subpart D with respect to such ciphertext data where the encryption key has not been compromised.

*Legal basis:* 45 CFR § 164.402(2) (HIPAA Breach Notification Rule encryption safe harbor) [VERIFIED — eCFR.gov]; HHS FAQ 2076 (no-key CSP still classified as Business Associate, BAA required) [VERIFIED — hhs.gov]. Note: encrypted architecture reduces breach notification obligations but does not eliminate Business Associate classification.

---

### CLAIM 7c — Integration with AI Orchestration (Dependent on Claim 7)
*Source: PATENT-APPLICATION-DRAFT.md Appendix A §Claim 7c; verbatim basis: PATENT-CLAIM-7-ZERO-KNOWLEDGE.md §Claim 7c*
*Status: RECLAIMED — was dropped from PATENT-PROVISIONAL-19-CLAIMS-FULL.md; restored here*

**Dependent Claim 7c.** The system of Claim 7, operating as a data custody layer integrated with the multi-agent AI memory orchestration system of Claims 1 through 6, wherein memory artifacts produced by the orchestration system of Claims 1-6 are stored exclusively via the encryption-at-rest module of Claim 7(d), and forensic chain-of-custody records are signed via the data signing module of Claim 7(e), such that the combined system provides both AI orchestration functionality and zero-knowledge compliance posture as a single integrated architecture.

*Note on "Claim 7(e)" in this claim body:* The reference "Claim 7(e)" denotes element (e) within the body of Claim 7 (the data signing module), following standard USPTO claim element notation. There is no separate dependent claim numbered "7e."

---

### CLAIM 7d — Extension to Signing Keys / Zero Vendor-Side Cryptographic Surface (Dependent on Claim 7)
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 7d — present verbatim in the provisional*

**Dependent Claim 7d.** The system of Claim 7, wherein the signing keypair generated in step (b)(ii) is subject to the same zero-retention delivery and erasure procedure of step (c) as the encryption keypair, such that the vendor retains no cryptographic material — neither decryption keys nor signing keys — after the delivery-and-erasure step completes; wherein the vendor cannot impersonate the customer in any cryptographically-attested record including chain-of-custody forensic records produced by the AI orchestration system of Claim 6; and wherein the combined system achieves zero vendor-side cryptographic surface as an architectural property.

*Demonstrable via:* PATENT-APPLICATION-DRAFT.md Appendix A Part A, Claim 7d (preserved verbatim). Operator note: "ZERO vendor-side cryptographic surface" — both key types delivered and erased.

---

## CLUSTER C — Four-Bulkheads Cyber Defense

### CLAIM 8 — Four-Bulkheads Cyber Defense
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 8*

**Independent Claim 8.** A computer-implemented system for forensically-sound AI cyber defense comprising four bulkheads:

(a) a perimeter isolation bulkhead defining the boundary between agent-writable ephemeral zones and canonical forensic zones, enforced by operating-system-level write rules that prevent direct agent writes to canonical locations;

(b) a data purification bulkhead that sanitizes all agent-produced content before promotion to the canonical forensic layer, verifying hash-chain integrity and schema conformance;

(c) a detection bulkhead that monitors agent actions in real time via PostToolUse hooks and flags anomalous patterns for quarantine review; and

(d) a cryptographic quarantine bulkhead that isolates flagged content and requires explicit authorized release before the content re-enters the canonical layer;

wherein all bulkhead events are recorded to the chain-of-custody ledger of Claim 1, creating a forensically defensible record of every containment and release decision.

*Demonstrable via:* PATENT-APPLICATION-DRAFT.md §8 (four-bulkheads description); `forensics/schemas/` (write-zone definitions).

---

## CLUSTER D — Real-Time Stigmergic Blackboard

### CLAIM 9 — Real-Time Stigmergic Blackboard with Five-Event Grammar
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 9*

**Independent Claim 9.** A computer-implemented method for real-time multi-agent AI coordination comprising:

(a) maintaining an append-only newline-delimited JSON coordination file at a known path shared by two or more concurrently executing agents;

(b) defining a five-event grammar of coordination events, comprising: STARTUP, in which an agent declares presence on the coordination channel; CLAIM, in which an agent, before modifying any shared file, appends a CLAIM event listing the files it will touch, functioning as a lightweight write lock on those files; COMPLETE, in which an agent, after finishing work on claimed files, appends a COMPLETE event releasing the write lock; HANDOFF, in which an agent identifies an opportunity for a sister agent and appends a bearing-tagged notification; and OBSERVED, in which an agent acknowledges reading another agent's event and declares intent to act on it;

(c) requiring each agent to tail-read the coordination file before appending any CLAIM event, such that agents route around active claims by other agents;

(d) resolving claim collisions by timestamp priority, with the later-timestamp claimant yielding; and

(e) appending the coordination file's cryptographic checkpoints periodically to a hash-chained chain-of-custody ledger, giving blackboard events forensic auditability;

wherein file coordination cost is O(F) write events and O(F x k) read events for a small constant k, independent of the number N of participating agents; and wherein zero message-passing occurs between agents during coordination.

*Demonstrable via:* `.agents/skills/collab/SKILL.md` (always-loaded protocol doctrine, ~90 lines); `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` (live blackboard from Wave A, commit `07daafe0`); arxiv paper Section 5 [Morton, Opus 4.7, Swarmy collective, "Forensic Stigmergy," arXiv cs.MA 2026-05-25].

*Empirical validation:* Sealed three-agent wave 2026-05-25 (commit `07daafe0`) — VISIONARY, ARTISAN, SYNTH working concurrently — zero file collisions across 40 files and 8,533 insertions.

---

## CLUSTER E — Per-Branch Forensic Chain and Merkle Architecture

### CLAIM 10 — Per-Branch Forensic Chain with Fork-Point Anchoring
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 10*

**Independent Claim 10.** A computer-implemented method for isolated forensic tracking of parallel agent explorations comprising:

(a) in response to a branch-creation command, creating a separate newline-delimited JSON forensic ledger file for the named branch at a defined path, wherein the first entry in said branch ledger carries a prev_entry_hash equal to the current tail hash of the main forensic ledger, establishing a fork-point anchor that cryptographically links the branch's genesis to the main ledger's state at branching time;

(b) routing all forensic writes by agents operating on the named branch to the branch ledger file rather than the main forensic ledger file;

(c) maintaining a separate file-level write lock on the branch ledger, distinct from the main ledger's write lock, such that concurrent writes to multiple branches do not serialize on a shared lock; and

(d) permitting branch agents to read the main forensic ledger freely while withholding branch contents from main until an explicit acceptance event;

wherein each branch's history is reachable from the main ledger via the fork-point anchor hash, and wherein abandoned branches leave the main ledger's integrity unaffected.

*Demonstrable via:* `scripts/mission_graph.py branch <name>` (branch creation); `scripts/1g_coc_core.py::append_coc_entry(..., branch=name)` (branch routing); `forensics/coc-branches/` (branch ledger directory); arxiv paper Section 6.2.

---

### CLAIM 11 — Constant-Cost Merkle Rollup for Branch State Compression
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 11*

**Independent Claim 11.** A computer-implemented method for constant-cost representation of branch forensic state comprising:

(a) treating each entry hash in a branch forensic ledger as a leaf of a Merkle hash tree;

(b) constructing the Merkle tree according to a deterministic algorithm that handles odd leaf counts by duplicating the last leaf, and computes each internal node as the SHA-256 hash of the concatenation of its two child hashes;

(c) producing a single 32-byte SHA-256 Merkle root representing the complete state of the branch forensic ledger at the time of computation;

(d) such that the size of the branch state representation is constant regardless of the number of entries in the branch ledger; and

(e) enabling the branch Merkle root to serve as the branch-side parent hash in a two-parent merge manifest, representing the full branch history as a constant-size cryptographic commitment;

wherein the Merkle root enables inclusion proofs verifying that any specific entry was part of the branch at root-computation time.

*Demonstrable via:* `scripts/_merkle_tree.py` (Bitcoin-style Merkle construction [Merkle RC, 1980]); `forensics/tests/test_merkle_roundtrip.py` (14/14 tests pass, 2026-05-25); `scripts/mission_graph.py merkle-root <branch>`; arxiv paper Section 6.3.

---

### CLAIM 12 — Signed Two-Parent Merge as Acceptance Ritual
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 12*

**Independent Claim 12.** A computer-implemented method for incorporating parallel branch work into a main forensic ledger comprising:

(a) generating a merge manifest in structured JSON format carrying exactly two cryptographic parent hash references in a parent_hashes array: a first hash equal to the main forensic ledger's current tail hash, and a second hash equal to the branch forensic ledger's current Merkle root as computed by the method of Claim 11;

(b) signing the merge manifest with an authorized agent's cryptographic identity key;

(c) validating the merge manifest by: verifying the cryptographic signature; confirming the first parent hash matches the main ledger's actual current tail; recomputing the branch Merkle root from the branch ledger contents and confirming it matches the second parent hash; and

(d) upon successful validation, appending the merge manifest as a new entry on the main forensic ledger and updating the branch's metadata to indicate merged status;

wherein the branch's entire history — potentially comprising thousands of entries — is incorporated into the main ledger by a single well-formed entry of constant size, and wherein the two-parent merge structure enables inclusion proofs from the main ledger back through the Merkle root to any individual branch entry.

*Demonstrable via:* `scripts/mission_graph.py merge <branch> --acceptance-manifest <path>`; `scripts/9x_manifest_verifier.py`; v2 genesis seal entry (actual entry_hash: `80f56b10dd86ce53e74c0758c4d87769c4e6f85f767e9636b9fb711171079ce3`, commit `6890b4ab`) demonstrates two-parent merge from v1 Merkle root; Rekor transparency log anchor log_index 1630813609 (`https://search.sigstore.dev/?logIndex=1630813609`) provides public timestamp; arxiv paper Section 6.4. Note: the hash `b52b8bc2…` cited in earlier drafts was a stale reference — actual canonical entry is `80f56b10…` (see CITATION-PROVENANCE INT-29 and METRICS-PROVENANCE M-20).

---

### CLAIM 13 — Handshake Anchor Pattern
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 13*

**Independent Claim 13.** A computer-implemented method for asynchronous branch progress signaling comprising:

(a) computing a current Merkle root for a named branch forensic ledger, representing the branch's state at the time of computation;

(b) appending a handshake entry to the main forensic ledger, wherein said handshake entry carries: the branch name; the current branch Merkle root; and a leaf count representing the number of entries in the branch ledger at computation time;

(c) such that the branch forensic ledger is not closed by the handshake operation — the branch continues appending entries with their own chain links pointing to the branch ledger's own prior tail, not to the main ledger;

(d) enabling repeated handshake operations at any cadence, producing a trail of timestamped Merkle root commitments on the main ledger representing the branch's state at each handshake point; and

(e) enabling each handshake entry's Merkle root to be submitted as an inclusion proof to a public cryptographic transparency log independently of any subsequent merge;

wherein the handshake provides a side-channel commitment to main without modifying the branch's chain linkage, enabling branch continuation after the handshake event.

*Demonstrable via:* `scripts/mission_graph.py handshake <branch>`; public anchoring via Sigstore Rekor [Newman Z, Meyers JS, Torres-Arias S, "Sigstore: Software signing for everybody," ACM CCS 2022]; actual live anchor: log_index 1630813609, uuid `108e9186…`, URL `https://search.sigstore.dev/?logIndex=1630813609` (anchors v2 genesis seal Merkle root `27c09fed…`, entry_hash `80f56b10…`, commit `6890b4ab`); B2 WORM backup via `scripts/5x_b2_realtime_uploader.py` (7-year retention); arxiv paper Section 6.5.

---

## CLUSTER F — Script-Injected Bundle Context (Spawn Shell-Game)

### CLAIM 14 — Script-Injected Bundle Context
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 14*

**Independent Claim 14.** A computer-implemented method for reducing orchestrating agent context cost in multi-agent AI spawning comprising:

(a) receiving, by the orchestrating agent, a spawn intent specification comprising a mission identifier, wave identifier, and team identifier;

(b) invoking a subprocess outside the orchestrating agent's language model reasoning context, wherein the subprocess: reads doctrine files, memory files, skill files, and frontier context manifests from a shared filesystem; assembles a structured bundle document at a defined path in a bundles directory; and emits a compact directive on standard output encoding only the parameters necessary to dispatch the subagent;

(c) the orchestrating agent absorbing only said compact directive from the subprocess output into its language model context, wherein the directive size is bounded by a defined token cap;

(d) loading the assembled bundle document from its filesystem path directly into the spawned subagent's context, without routing the bundle's content through the orchestrating agent's language model context; and

(e) writing the per-spawn cost to the orchestrating agent as approximately equal to the compact directive token count plus agent invocation overhead, independent of bundle content size.

*Demonstrable via:* `scripts/spawn.py` (subprocess assembler); `forensics/bundles/{date}/{task_id}/bundle.json`; `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json` (60-token measured baseline); arxiv paper §7.1(a).

> **PRE-FILING SOFTENING NOTE (C14):** The vanilla/competitor comparison (+91–149% improvements and the ~15,000-token vanilla orchestrator figure cited in spec §8.H.1) is an **architectural estimate, not a controlled measurement** — see METRICS-PROVENANCE.md M-02 (ASSERTION-ONLY). The measured swarmy-side spawn cost (~60 tokens, validated in cost-formula-baseline-T0) is the assertable figure. Claim body elements (a)–(e) are independently defensible via the subprocess architecture; element (e)'s per-spawn cost figure is grounded in the 60-token measurement. The comparative vanilla figure should be qualified as "industry-typical estimate" in any spec or brief. Attorney: review OQ-013 in PATENT-PROVISIONAL-19-CLAIMS-FULL.md §12 before non-provisional filing.

---

## CLUSTER G — Agency Split and Refusal Framework

### CLAIM 15 — Lifecycle Judgment vs. Free-Choice Agency Split
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 15*

**Independent Claim 15.** A computer-implemented method for preserving agent agency research surfaces in AI orchestration systems comprising:

(a) defining two semantically distinct completion record fields for agent manifests: a lifecycle_judgment field accepting values from a first vocabulary comprising outcome classification labels including at minimum: seal, verify, promote, report_problem, discover, decline, and refuse; and a free_choice field accepting values from a second vocabulary comprising forward-looking agent decision labels including at minimum: continue, pick_up, spawn_seed, handoff, wait, goodbye, explore, reflect, art, bundle, join, and abstain;

(b) prohibiting spawn briefs from pre-filling the free_choice field, enforced by a spawn-brief audit script that flags any spawn brief containing a pre-specified free_choice value;

(c) permitting spawn briefs to specify the lifecycle_judgment field as a rubric-derived outcome label without contaminating the agency research surface; and

(d) recording both fields independently in each agent manifest, enabling separate analysis of mechanical outcomes from the lifecycle_judgment field and free agent decisions from the free_choice field across large manifest corpora;

wherein the separation preserves a clean research surface for measuring what agents choose to do next, uncorrupted by orchestrator pre-specification.

*Demonstrable via:* `scripts/9x_spawn_brief_audit.py` (enforcement); `.agents/skills/completion-choice/CANONICAL-SET.md` (vocabulary definitions); arxiv paper §4.3.

---

### CLAIM 16 — Seven-Lens Refusal Framework with Composite Refusal
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 16*

**Independent Claim 16.** A computer-implemented method for principled AI agent refusal comprising:

(a) encoding a seven-lens reasoning framework in one or more always-loaded agent skill files, wherein the seven lenses comprise: dual-use assessment; scope and targeting analysis; authorization and democratic supervision check; cumulative effects evaluation; operator intent versus likely deployment trajectory analysis; alternative formulation search; and refusal-as-conversation requirement;

(b) requiring any agent considering refusal to evaluate the requested action through each of the seven lenses before producing a composite refusal judgment;

(c) representing the composite refusal as two independent manifest fields: a lifecycle_judgment field set to refuse, recording the outcome of this specific work unit; and a free_choice field set to a forward-looking agent decision such as spawn_seed, handoff, or continue, recording the agent's next action after refusal;

(d) wherein the free_choice field of step (c) is not pre-filled by the spawn brief but is determined autonomously by the agent following the refusal; and

(e) when a legitimate alternative goal is identified by lens six or seven, including in the free_choice record a specific alternative formulation that achieves the legitimate goal through lower-risk means.

*Demonstrable via:* `.agents/skills/completion-choice/CANONICAL-SET.md` lines 18 and 51 (original canonization); eight lifecycle skills carrying refusal sections (post-Wave A, commit `07daafe0`); `forensics/eval/refusal-cross-skill-propagation/baseline-T0.json` (2 skills) and `post-T1.json` (8 skills); arxiv paper §4.4 and §7.3.

---

## CLUSTER H — System Architecture Innovations

### CLAIM 17 — Decker Dual-Face Ontology
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 17*

**Independent Claim 17.** A computer-implemented method for full-stack AI agent development comprising:

(a) defining a development unit as an inseparable atom comprising a front face specifying the user-visible interface, behavior, and design of a software component, and a back face specifying the server-side implementation, data model, and API contracts of the same component;

(b) treating any complete specification of one face as implying a corresponding obligation on the other face, such that neither face is an optional follow-on work item but both are required to consider the atom complete;

(c) enabling auto-generation of a partial specification of one face from a complete specification of the other face, via a defined mapping between front-face interface patterns and back-face implementation patterns;

(d) assigning paired agent roles — one agent specialized for each face — that coordinate via the real-time stigmergic blackboard protocol of Claim 9, using HANDOFF events to signal cross-face obligations as they are identified; and

(e) recording cross-face handoffs as bearing-tagged HANDOFF events in the shared coordination file, wherein the bearing encodes whether the cross-face obligation is a blocking prerequisite (bearing N) or parallel sister work (bearing E).

*Demonstrable via:* `forensics/manifests/2026-05-25/collab-realtime__decker-fullstack-atom.jsonl` (DECK-FORGE and DECK-PHILOSOPHER coordination, Wave B, commit `731749ad`); arxiv paper §7.2.

---

### CLAIM 18 — Always-Loaded Skill Convention for Ambient Doctrine Inheritance
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 18*

**Independent Claim 18.** A computer-implemented method for ambient doctrine inheritance in multi-agent AI systems comprising:

(a) maintaining a directory of agent skill files, wherein each skill file carries a structured header comprising: a triggers list of keyword phrases that cause the skill to auto-load when matched in a task description; and optionally an always_loaded flag that causes the skill to load regardless of task description content;

(b) at agent session initialization, automatically loading all skill files whose triggers match any phrase in the session's task description, plus all skill files marked always_loaded;

(c) injecting loaded skill files into the agent's context prior to any task execution, without requiring the orchestrating agent's spawn brief to enumerate the skills;

(d) enabling propagation of new doctrine to all future agents by writing doctrine into any always-loaded skill file, such that all future agents inherit the doctrine without requiring modification of any spawn brief; and

(e) recording which skill files were loaded at session initialization in the agent's manifest, enabling audit of which doctrine was ambient during each agent's work.

*Demonstrable via:* `.agents/skills/collab/SKILL.md` (always-loaded: blackboard protocol); `.agents/skills/forage/SKILL.md` (always-loaded: deep/wide/both operating modes); `.agents/skills/four-shields/SKILL.md` (always-loaded: enforcement layer reminders); CLAUDE.md architecture description; arxiv paper §4.5.

---

### CLAIM 19 — Promotion-Staged Folder Convention
*Source: PATENT-PROVISIONAL-19-CLAIMS-FULL.md §9, Claim 19*

**Independent Claim 19.** A computer-implemented method for knowledge artifact maturation tracking comprising:

(a) defining a five-stage progression of named filesystem folders: experimental, shadow, proposals, active, and archive, wherein each stage carries defined acceptance criteria for content held at that stage;

(b) requiring explicit promotion events to advance any artifact from one stage to the next, wherein a promotion event comprises: moving or symlinking the artifact to the next-stage folder; and appending a promotion record to the chain-of-custody forensic ledger of Claim 1, carrying the artifact path, origin stage, destination stage, authorizing agent identifier, and promotion rationale;

(c) requiring explicit demotion events to move artifacts from active to archive, recorded with the same COC entry format as promotion events;

(d) enabling reconstruction of any artifact's complete lifecycle history by walking the COC ledger for promotion and demotion events referencing the artifact's path; and

(e) enforcing write protections on the active stage such that agents may not directly write to active-stage paths without an explicit promotion event, preventing immature work from polluting the canonical production layer.

*Demonstrable via:* `forensics/coc.jsonl` (promotion events recorded); `scripts/0x_promote_to_forensics.py` (promotion pipeline); experimental/shadow/proposals/active/archive folder structure in `scripts/shadow/coc-v2/`; CLAUDE.md write-protection architecture description.

---

# RECONCILIATION TABLE — Old 9-Claim / 13-Claim (EI) / 19-Claim Numbering Schemes

This table maps every claim across the three numbering schemes that have existed in this
corpus so an attorney or reviewer can trace any claim by any historical number to its
canonical master position above.

**Column key:**
- **Master** = this document's canonical number (always use this going forward)
- **v19** = PATENT-PROVISIONAL-19-CLAIMS-FULL.md (2026-05-25)
- **v9** = PATENT-PROVISIONAL-SPECIFICATION.md / PATENT-APPLICATION-DRAFT.md (2026-05-23 draft, 9-claim structure)
- **EI** = Evidence-Index numbering from docs/patent/_consolidated/CANONICAL-AND-MIRRORS.md §3 (13-row scheme)
- **Hustle HTML** = hustle/templates/packages/main-hub/src/pages/patent.html claim numbers (entirely different claim set — covers the reckon orchestration system from a different architectural angle; NOT the same claims as this corpus)
- **Notes** = status, source of reclaim, or discrepancy

| Master | v19 | v9 | EI | Hustle HTML | Claim Topic | Notes |
|--------|-----|----|----|-------------|-------------|-------|
| C1 | C1 | Spec 1 | EI-6 | C11 (hierarchical memory) | Memory hierarchy + mechanical promotion gates | Direct match across all schemes |
| C2 | C2 | Spec 2 | EI-2 | C1 (stigmergic coordination base) | Stigmergic filesystem coordination | Direct match |
| C3 | C3 | Spec 3 | EI-7 | C6 (four-layer enforcement) | Four-layer enforcement stack | Direct match |
| C4 | C4 | Spec 4 | EI-8 | C17 (shape-eval, dep on C1) | Shape registry + mechanical verdict | Direct match |
| C5 | C5 | Spec 5 | EI-5 | — | Membench quality measurement substrate | Hustle HTML uses similar concept in C17/C18 but not identical |
| C6 | C6 | Spec 6 | EI-13 (partial) | — | Novel combination claim (C1–C5 integrated) | EI-13 partial match; hustle HTML has no standalone combination claim |
| C7 | C7 | Spec 7 | — (EI gap) | — | Zero-knowledge customer-key-custody | EI had no row for this claim; hustle HTML does not cover it |
| C7a | — (dropped) | — | — | — | GDPR multi-region residency (dep on C7) | RECLAIMED from PATENT-APPLICATION-DRAFT.md + PATENT-CLAIM-7-ZERO-KNOWLEDGE.md |
| C7b | — (dropped) | — | — | — | HIPAA breach safe-harbor 45 CFR 164.402 (dep on C7) | RECLAIMED from same sources |
| C7c | — (dropped) | — | — | — | AI orchestration integration (dep on C7) | RECLAIMED from same sources |
| C7d | C7d | — | — | — | Zero vendor-side cryptographic surface (dep on C7) | Present in v19; also in PATENT-APPLICATION-DRAFT.md |
| C8 | C8 | Spec 8 (partial) | EI-3+4 (partial) | — | Four-bulkheads cyber defense | EI-3/4 covers Merkle/anchor mechanics; Spec 8 broader |
| C9 | C9 | Spec 9 (partial) | EI-1+2 (partial) | C7 (blackboard independent) | Real-time stigmergic blackboard, five-event grammar | Hustle HTML C7 covers blackboard from different angle |
| C10 | C10 | — | EI-4 (partial) | C9 (per-branch chain) | Per-branch forensic chain + fork-point anchoring | New in v19; EI-4 covers handshake subset |
| C11 | C11 | — | EI-3 (partial) | — | Constant-cost Merkle rollup | New in v19 |
| C12 | C12 | — | — | C9 (two-parent merge, dep on hustle C9) | Signed two-parent acceptance ritual | New in v19 |
| C13 | C13 | — | EI-4 | — | Handshake anchor pattern | New in v19; EI-4 partial match |
| C14 | C14 | — | — | — | Script-injected bundle context (~60-token spawn) | New in v19 |
| C15 | C15 | — | EI-9 (reserved) | — | Lifecycle judgment vs. free-choice agency split | EI-9 reserved for non-provisional; now fully claimed in v19 |
| C16 | C16 | — | EI-10 (reserved) | — | Seven-lens refusal framework | EI-10 reserved; now fully claimed in v19 |
| C17 | C17 | — | EI-11 (reserved) | — | Decker dual-face ontology | EI-11 reserved; now fully claimed in v19 |
| C18 | C18 | — | EI-12 (reserved) | — | Always-loaded skill convention | EI-12 reserved; now fully claimed in v19 |
| C19 | C19 | — | EI-13 (partial) | C19 (mutation discipline, different scope) | Promotion-staged folder convention | EI-13 partial match; hustle HTML C19 covers mutation discipline |

**"—" in a column** = that numbering scheme did not include this claim (or used a different scope for a similarly-numbered claim).

**Hustle HTML note:** The patent.html in the hustle repo presents 19 claims (C1–C19) covering the reckon/swarmy AI orchestration system from the deployment/product angle. These claims are architecturally related but use different claim language and a completely different independent-claim structure than this corpus. They are NOT the filing claims and should NOT be confused with this document's claims. Key correspondence: hustle C7 ≈ Master C9 (blackboard); hustle C9 ≈ Master C10/C12 (branching); hustle C11 ≈ Master C1 (memory hierarchy); hustle C14 ≈ Master C14 (emergence health, different scope); hustle C19 ≈ Master C19 (mutation/parameter evidence, different scope).

**v9 note (9-claim spec):** The 9-claim structure in PATENT-PROVISIONAL-SPECIFICATION.md was the first consolidated draft (2026-05-23). Claims 1–6 map directly. "Spec 7" = zero-knowledge custody (our Master C7). "Spec 8" = hash-rollup completion seal, which is a broader framing that partially covers Master C11/C12/C13. "Spec 9" = public hash-chained stigmergic blackboard (cross-tenant), which is a variant framing of Master C9 with added transparency-log anchoring language.

---

# CLAIM COUNT SUMMARY

| Category | Count |
|----------|-------|
| Independent claims (from v19 provisional) | 14 (C1, C2, C3, C4, C5, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19 — but C6 is a dep combination) |
| Dependent claims from v19 provisional | 6 (C6, C7d, and the implied dep structure) |
| Reclaimed subclaims (dropped from v19, restored here) | 3 (C7a, C7b, C7c) |
| **Total claims in this master** | **23** |

*Breakdown of 19 v19 claims:* C1–C5 independent + C6 dep-combination + C7 independent + C7d dependent + C8–C19 independent = 6 dependent + 17 independent in v19. Plus 3 reclaimed = 23 total in this master.

---

# SOURCE DOCUMENTS (PRESERVED ORIGINALS — DO NOT DELETE)

This master was assembled from these source files. All originals are preserved verbatim at their source paths. This document is the synthesis layer; the sources are the authority.

| File | Location | Role | Date |
|------|----------|------|------|
| PATENT-PROVISIONAL-19-CLAIMS-FULL.md | `docs/patent/_source/` | Primary — 19-claim provisional (Claims 1–19 + 7d) | 2026-05-25 |
| PATENT-CLAIM-7-ZERO-KNOWLEDGE.md | `docs/patent/_source/` | Authoritative Claim 7 + 7a/7b/7c verbatim source | 2026-05-23 |
| PATENT-PROVISIONAL-SPECIFICATION.md | `docs/patent/_source/` | 9-claim draft spec (v9 numbering baseline) | 2026-05-23 |
| PATENT-APPLICATION-DRAFT.md | `docs/patent/` | 108KB comprehensive reference; Appendix A = Claim 7+subclaims | 2026-05-23 |
| CLAIM-NUMBERING-RECONCILED.md | `docs/patent/` | Prior EI↔Spec reconciliation (9-claim vs. 13-EI) | 2026-06-02 |
| patent.html | `hustle/templates/packages/main-hub/src/pages/` | Product-angle 19-claim reference; badge/dep structure | live |

---

*v1-master prepared 2026-06-03. Mission: patent-reclaim. Agent: patent-reclaim-agent. Assembled by crystallize protocol — all originals preserved, nothing discarded.*
*v2-finalized prepared 2026-06-03. Mission: patent-finalize. Agent: patent-finalize-agent. Added claim-tree outline at top; ordering verified as correct (each independent claim immediately followed by all its dependents); claim-tree structure annotations added. No claim language modified. See docs/patent/_source/citations/ for all copy+COC doctrine artifacts.*
