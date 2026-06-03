# Claim 8: Multi-Party Hash-Rollup Completion Seal with Single-Authority Counter-Signature for Autonomous Multi-Agent Systems

> **Standalone section for insertion into the USPTO Provisional Patent Application.**
> When PATENT-PROVISIONAL-SPECIFICATION.md is finalized, this document folds in as:
> (a) the formal Claim 8 language (and dependents 8a–8d) in the Claims section, and
> (b) the corresponding sub-section in the Detailed Description of the Invention.
> This file is self-contained for independent attorney review.

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a patent attorney before any USPTO filing or public disclosure.

---

## Part A: Formal Claim Language (USPTO Claim 8)

### Claim 8

A computer-implemented method for cryptographically certifying the completion of a unit of distributed work performed by a plurality of autonomous software agents, the method comprising:

(a) maintaining a completion record (a "charter") describing a unit of work and a set of contributing agents, each contributing agent possessing an independently-provisioned asymmetric signing keypair;

(b) computing a body digest comprising a cryptographic hash over a canonical serialization of the completion record exclusive of a seal section thereof;

(c) for each contributing agent, in an ordered sequence corresponding to the order in which the agents completed their respective contributions, generating a co-signature record comprising:
    (i) a predecessor digest equal to the body digest for the first agent in the sequence, and equal to a rollup digest of the immediately preceding co-signature record for each subsequent agent;
    (ii) a digital signature produced with the contributing agent's private signing key over a concatenation of the body digest and the predecessor digest; and
    (iii) a rollup digest comprising a cryptographic hash over a concatenation of the predecessor digest and a canonical serialization of the co-signature record exclusive of the rollup digest;
    such that the co-signature records form a hash-linked chain whose final rollup digest constitutes a merkle root that is computationally bound to the entire ordered sequence of contributions;

(d) generating, by a single designated authority process distinct from the contributing agents and possessing its own asymmetric signing keypair, exactly one counter-signature over a concatenation of the merkle root and the body digest, irrespective of the number of contributing agents, said counter-signature representing acceptance of, and being computationally bound to, the entire ordered sequence of contributions; and

(e) verifying the completion record by recomputing the body digest, traversing the chain of co-signature records to confirm each predecessor digest, each contributing-agent signature, and each rollup digest, confirming the merkle root, and confirming the authority counter-signature, wherein any reordering, insertion, deletion, or mutation of any co-signature record or of the completion record body causes the verification to fail at the first inconsistent link;

wherein the designated authority performs a single cryptographic acceptance operation that certifies an arbitrarily large ordered set of independently-attested agent contributions, thereby bounding the authority's per-completion workload to a constant independent of the number of contributing agents.

---

### Claim 8a (Dependent — Constant-Authority-Burden / f(0) Property)

The method of Claim 8, wherein the designated authority process performs exactly one signing operation per completion record regardless of (i) the number of contributing agents, (ii) the number of work artifacts produced, and (iii) the number of intermediate state transitions, and wherein all operations performed by the contributing agents — including attestation, acceptance of intermediate work, and integration of divergent work branches — are performed without any signing or supervisory operation by the designated authority, such that the designated authority's computational and attentional burden per completion record remains constant as the contributing-agent count increases.

---

### Claim 8b (Dependent — Public Transparency-Log Anchoring of the Merkle Root)

The method of Claim 8, further comprising submitting the merkle root, the authority counter-signature, or a digest derived therefrom, to a public append-only cryptographic transparency log external to and not controlled by the system, receiving from said transparency log an inclusion proof and a log-entry identifier, and storing the log-entry identifier and a publicly-resolvable reference thereto inline within the seal section of the completion record, such that the completion record carries a self-describing, publicly-verifiable, and temporally-anchored proof that the certified ordered sequence of contributions existed no later than a globally-witnessed time without reliance on any clock controlled by the system.

---

### Claim 8c (Dependent — Zero-Protocol Branch Integration)

The method of Claim 8, wherein a subset of contributing agents performs work on a divergent version-control branch isolated from a trunk, and wherein integration of said branch into the trunk is performed without any signing operation by the designated authority and without a branch-specific acceptance protocol, by virtue of: (i) each work artifact crossing the branch-trunk boundary being individually signed by its producing agent prior to integration; and (ii) the divergent branch periodically emitting a liveness record to the trunk comprising a merkle digest of the branch's accumulated state and a public transparency-log anchor thereof; such that the single authority counter-signature of Claim 8 serves as the sole acceptance operation for all work delivered by the branch upon completion of the associated completion record.

---

### Claim 8d (Dependent — Dual-Regime Storage with Cryptographic Promotion Gate)

The method of Claim 8, wherein in-progress completion records are stored in a first storage regime partitioned by lifecycle state and not by calendar date, such that a completion record spanning multiple calendar days accumulates in a single continuous location traversable by agents without date-boundary fragmentation; and wherein, upon successful verification per Claim 8(e) and an affirmative acceptance indication in the authority counter-signature, the completion record and its associated artifacts are promoted by a gate process to a second storage regime partitioned by both artifact type and calendar date, said second regime constituting an immutable, time-ordered, content-addressable archival canon; wherein the gate process refuses promotion of any completion record whose seal fails verification.

---

### Claim 8e (Dependent — Integration with Prior Claims)

The method of Claim 8, operating upon the stigmergic filesystem-coordinated multi-agent system of Claims 1 through 6, wherein the contributing-agent attestations of Claim 8(c) are the signed manifests produced by the stigmergic coordination system, the body digest and rollup chain are appended to the SHA-256 hash-chained audit log of Claim 1, and the dual-regime promotion of Claim 8d is performed by the canonical writer enforcement of the four-layer stack of Claim 3, such that completion certification, coordination, audit logging, and enforcement form a single integrated cryptographic architecture.

---

## Part B: Detailed Description (Claim Area 8)

### B.1 The problem

Prior multi-agent and multi-signatory systems require the accepting authority to
either (i) sign each contribution individually (O(N) authority operations), or (ii)
sign a flat set that does not bind the *order* of work, losing provenance of the
sequence. Neither bounds authority burden to a constant while preserving ordered,
tamper-evident provenance. This claim resolves both.

### B.2 The hash-rollup construction

Let the canonical serialization function be deterministic (sorted keys, no
whitespace). The construction proceeds bottom-to-top; node labels below carry the
exact formulas (rendered via the *mehrmaid* extension, which embeds MathJax inside
Mermaid node labels):

```mehrmaid
flowchart TD
  BODY["**Body digest**<br>$h_{body} = \mathrm{SHA256}(\mathrm{canon}(\text{charter} \setminus \text{seal}))$"]
  A0["**Agent 0 co-sign** (seq 0)<br>$prev_0 = h_{body}$<br>$\sigma_0 = \mathrm{Ed25519}_{k_0}(h_{body} \,\Vert\, prev_0)$<br>$r_0 = \mathrm{SHA256}(prev_0 \,\Vert\, \mathrm{canon}(e_0))$"]
  A1["**Agent 1 co-sign** (seq 1)<br>$prev_1 = r_0$<br>$\sigma_1 = \mathrm{Ed25519}_{k_1}(h_{body} \,\Vert\, prev_1)$<br>$r_1 = \mathrm{SHA256}(prev_1 \,\Vert\, \mathrm{canon}(e_1))$"]
  AN["**Agent n co-sign** (seq n)<br>$prev_n = r_{n-1}$<br>$\sigma_n = \mathrm{Ed25519}_{k_n}(h_{body} \,\Vert\, prev_n)$<br>$r_n = \mathrm{SHA256}(prev_n \,\Vert\, \mathrm{canon}(e_n))$"]
  ROOT["**Merkle root**<br>$\rho = r_n$"]
  SEAL["**Authority counter-seal** (exactly ONE op)<br>$\Sigma = \mathrm{Ed25519}_{k_{main}}(\rho \,\Vert\, h_{body})$"]
  REKOR["**Public transparency anchor**<br>$\mathrm{Rekor}(\rho) \rightarrow (\text{uuid}, \text{inclusion proof})$"]
  CANON["**Promote to canon**<br>$\text{forensics}/\{type\}/\{date\}/$"]
  BODY --> A0 --> A1 --> AN --> ROOT --> SEAL --> REKOR --> CANON
```

Because each agent signs over $h_{body} \Vert prev_i$ and $prev_i = r_{i-1}$, the
signatures are chained: altering any $e_i$, reordering the sequence, or mutating the
charter body changes some $prev_j$ and breaks verification at that link. The single
authority signature $\Sigma$ over $\rho$ therefore certifies the *entire ordered
history* in one operation — the constant-burden property of Claim 8a.

### B.3 The lifecycle and the f(0) burden ledger

```mehrmaid
flowchart LR
  L1["**L1 Atom**<br>agent signs manifest<br>$\sigma^{man}_i$"]
  L2["**L2 Acceptance**<br>automated merge / heartbeat<br>$\mathrm{Rekor}(\text{merkle})$ — *0 authority ops*"]
  L3["**L3 Seal**<br>co-sign rollup → $\rho$ → counter-seal $\Sigma$<br>**1 authority op**"]
  L4["**L4 Promotion**<br>$\mathrm{verify}(seal)=\top \Rightarrow$ canon"]
  L1 --> L2 --> L3 --> L4
```

The authority's total workload over the entire lifecycle is exactly one operation
($\Sigma$), located at L3. L1, L2 (including branch integration and heartbeats), and
L4 require zero authority operations. This is the patentable advance: ordered,
publicly-anchored, tamper-evident completion certification at **constant authority
cost**.

### B.4 Reduction to practice

A working embodiment exists: `scripts/5e_agent_sign.py` (verbs `cosign-charter`,
`counterseal-charter`, `verify-seal`, `anchor`) over Ed25519 keys at
`forensics/reputation/keys/`, with the shape constrained by
`forensics/schemas/shape/charter.schema.json` (`seal.co_signatures[]`,
`seal.counter_seal.merkle_root`, `seal.anchor`). Verification empirically rejects
both body mutation and co-signature reordering. See
`docs/145-THE-CHARTER-SEAL-CANONICAL.md`.

---

*Prior-art note for the examiner: distinguish from (i) multisignature wallets
(threshold signatures do not bind contribution ORDER and do not bound authority
cost to one op), (ii) certificate transparency (anchors certificates, not an ordered
multi-agent work rollup with a single accepting authority), and (iii) git commit
signing (per-commit, no single-authority sequence seal, no transparency-anchored
merkle root of the ordered set).*
