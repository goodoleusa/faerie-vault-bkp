---
title: "Supporting Documents — Patent Expedition"
subtitle: "Open Questions + Assignment Agreement Template + Marketing Blurbs"
date: 2026-05-23
authors: [Operator + claude-opus-4-7 agent]
document_type: supporting-reference
status: DRAFT — for operator + attorney internal reference
citation_style: Mixed; endnotes where applicable
---

> **⚠️ DRAFT — operator + attorney internal reference**
>
> Consolidates the supporting materials operator + attorney pair will need alongside the patent-application + service-license-agreement drafts. Not for external sharing without further curation.
>
> **Ancestor sources** (originals preserved verbatim at `business/patent/_source/`):
>
> 1. `OPEN-QUESTIONS.md` — 20 operator questions across 4 priority tiers; what blocks USPTO filing and ELA signature
> 2. `ASSIGNMENT-AGREEMENT-DRAFT.md` — Patent Assignment Agreement template (future IP transfer; Sections Y.1-Y.4)
> 3. `BLURBS-BRAINSTORM.md` — 70+ semantic-density blurbs across 12 audiences/tones for patent title, abstract, recital openings, marketing
>
> **Promoted to `business/patent/` 2026-05-23** from `forensics/charters/expeditions/enterprise-patent-foundation/polished-deliverables/`.

---

# Open Questions — what blocks filing + signature

> *Cited as ancestor: *
# OPEN QUESTIONS
## Operator Must Answer Before USPTO Filing or Attorney Engagement

**Status:** Compiled from `charter.json` open_questions + discoveries during the polished-deliverables research pass.
**Date compiled:** 2026-05-23
**Agent:** research-analyst (expedition-w1)

---

### CRITICAL — Required Before USPTO Filing

These questions block the provisional filing. The provisional cannot be filed until they are answered.

**OQ-001: Co-inventor name and identity**
- What is the co-inventor's full legal name (as it will appear on the USPTO cover sheet)?
- What is their current mailing address (required on Form SB/16)?
- What is their citizenship / country of residence (required for USPTO filing)?
- Are there any ownership agreements between the two inventors regarding the patent rights (e.g., a co-inventor agreement specifying ownership split)?

**OQ-002: Lead inventor (first named inventor) information**
- Full legal name as it will appear on the USPTO cover sheet
- Current mailing address
- Citizenship / country of residence

**OQ-003: Entity status for fee calculation**
- Do BOTH inventors qualify for micro entity status?
  - Micro entity gross income qualification: as of 2025, maximum qualifying gross income is $251,190/year (confirmed from USPTO fee schedule search)
  - Micro entity filing limit: no more than 4 previous patent applications filed as inventor (provisional applications do not count toward this limit)
  - If either inventor does not qualify, the filing fee tier drops to small entity ($130) or regular ($325)
- Recommendation: confirm micro entity qualification with a patent attorney before filing

**OQ-004: Provisional patent title**
- The draft title in this specification is: "Autonomous Multi-Agent Orchestration System with Hierarchical Memory Promotion, Stigmergic Filesystem Coordination, Four-Layer Enforcement Stack, and Mechanical Quality Classification"
- USPTO recommends titles that are 2–7 words but this is a recommendation, not a requirement for provisionals
- Operator should confirm or adjust this title

---

### HIGH PRIORITY — Required Before ELA Execution

These questions block the ELA from being signed.

**OQ-005: Company entity legal name and state of incorporation**
- What is the full legal name of the company entity that will sign as Licensor?
- What state is it (or will it be) incorporated/formed in?
- If the company does not yet exist: the ELA Option A (company as exclusive sublicensee from inventors, then sublicenses to enterprise customer) requires a separate Exclusive License Agreement between the Inventors and the Company entity. The company must exist before this can be executed.

**OQ-006: ELA structure decision (Section 14 of ELA-DRAFT.md)**
- **Option A (recommended):** Inventors grant exclusive license to Company entity; Company sublicenses to Licensee. Provides liability shield but requires Exclusive License Agreement between Inventors and Company.
- **Option B (fallback):** Inventors license directly to Licensee. Simpler but exposes inventors personally.
- Which structure does the operator choose? Attorney should advise on tax and liability implications before selecting.

**OQ-007: First enterprise customer information**
- Customer legal name and state of formation (affects governing law selection and jurisdiction)
- Industry vertical (affects due-diligence affirmation scope and acceptable use provisions)
- Deal size class (affects fee schedule structure — flat fee vs. usage-based vs. revenue share)
- Timeline for contract signature (drives ELA finalization deadline)

**OQ-008: Governing law jurisdiction**
- The ELA and Assignment Agreement both have [STATE — OPEN QUESTION] placeholders.
- Most common choices for software companies: Delaware (company law alignment), California (where many enterprise customers are based), or the operator's home state.
- Attorney should advise based on company formation state and enterprise customer's jurisdiction.

**OQ-009: Dispute resolution mechanism**
- ELA Section 10.2 has a placeholder for arbitration provider (AAA or JAMS) and seat (city/state).
- Attorney should advise on which arbitration forum is appropriate for the deal size and customer type.

---

### MEDIUM PRIORITY — Required Before Non-Provisional Filing or Patent Attorney Engagement

**OQ-010: Patent attorney engagement**
- The provisional establishes the priority date. The 12-month clock to non-provisional conversion begins on the filing date.
- A registered patent attorney must: (a) review and refine the provisional specification; (b) draft formal independent and dependent claims for the non-provisional; (c) advise on claim scope vs. prior art; and (d) handle USPTO prosecution.
- Recommended timeline: engage attorney within 6 months of provisional filing, before the 12-month clock expires.
- Budget note: non-provisional patent prosecution typically costs $8,000–$20,000+ including attorney fees and USPTO fees. Provisional filing itself (DIY, no attorney) costs $65 (micro entity) + Form SB/16 + specification PDF.

**OQ-011: Prior art disclosure**
- Are the inventors aware of any prior art systems that describe similar techniques?
  - Stigmergic agent coordination systems (e.g., swarm intelligence papers, ACO — ant colony optimization systems)?
  - Hierarchical memory systems for AI agents (e.g., MemGPT, Reflexion, generative agents)?
  - Mechanical verdict classification systems in software engineering (e.g., mutation testing frameworks)?
  - Four-layer enforcement stacks in computer security (e.g., defense-in-depth frameworks)?
- Full prior art disclosure is required for USPTO examination. Inventors have a duty to disclose material prior art they are aware of.

**OQ-012: Jurisdiction strategy**
- US-only first (provisional + US non-provisional)?
- PCT international filing (covers 150+ countries, must file within 12 months of provisional)?
- Direct national phase in specific jurisdictions (EU, UK, China, Japan) without PCT?
- PCT route preserves maximum international options but adds significant cost ($5,000–$15,000+ for PCT filing, then national phase fees).
- Attorney should advise based on where the operator expects commercial activity.

---

### MEDIUM PRIORITY — Module Disposition Matrix

**OQ-013: Per-module OSS vs. proprietary disposition**
- The operator selected "core-engine-proprietary-rest-open" strategy.
- A concrete per-module decision matrix is needed to ensure the patent's novel-combination claim covers the IP boundary cleanly.
- Draft matrix (operator must confirm or revise):

| Module / Component | Proposed Disposition | Notes |
|---|---|---|
| `scripts/1a_manifest_writer.py` | Proprietary | Core memory promotion gate |
| `scripts/2d_frontier_scanner_indexed.py` | Proprietary | Core stigmergic coordination |
| `scripts/2a_spawn_pressure.py` | Proprietary | Core spawn formula |
| `scripts/shapes/_shapes_lib.py` | Proprietary | Core mechanical verdict classifier |
| `scripts/3f_membench_probes.py` | Proprietary | Core membench substrate |
| `scripts/3k_membench_scorer.py` | Proprietary | Core evaluation substrate |
| `forensics/schemas/formulas/*.formula.json` | Proprietary | Core formula definitions |
| `_meta/shapes.json` | Proprietary | Core shape registry |
| `.openhands/hooks/9x_hook-*.py` | Proprietary | Core reactive enforcement |
| `HONEY.md`, `NECTAR.md` (format/protocol) | Proprietary | Core memory protocol |
| `.agents/skills/*/SKILL.md` | Open source (OSS) | Community building |
| `.agents/skills/forage/SKILL.md` | Open source (OSS) | Community building |
| `AGENTS.md` (doctrine) | Open source (OSS) | Community building |
| Agent archetypes (NAVIGATOR, MAKER, etc.) | Open source (OSS) | Community building |
| Vault patterns, Obsidian structure | Open source (OSS) | Community building |

**OQ-014: forensic-coc-v2-rekor integration decision**
- The `forensic-coc-v2-rekor` charter covers a Merkle-tree + Sigstore Rekor witnessing architecture for the forensic chain-of-custody.
- Decision needed: (a) fold it into the current provisional as an additional claim area (requires adding Section 7 to the patent spec before filing); or (b) file a separate provisional for that architecture?
- The current provisional spec describes the SHA-256 hash chain (`forensics/coc.jsonl`) but does not claim the Rekor witnessing layer.
- Attorney should advise on whether combining or separating provides stronger protection.

---

### LOWER PRIORITY — For Later Planning

**OQ-015: share.note.sx encrypted note content**
- The operator referenced additional research at `https://share.note.sx/xyjlsmzd#yOf7fYmiC6qLhW4kHDi3uPpst9+YRt2pnEfWJ32FnTo`
- This note uses client-side encryption; the agent could not decrypt it in this session.
- Action: operator opens the URL in a browser, copies the decrypted content, and provides it for the next research pass.
- The decrypted content may contain additional patent claim language, ELA clauses, prior art references, or other material that should be incorporated into the polished deliverables.

**OQ-016: Multi-signature ed25519 notary key strategy**
- The `forensic-coc-v2-rekor` charter cross-references a notary key strategy for the company's overall identity.
- This may affect how the patent's forensic chain-of-custody claims are framed and how the company's IP ownership is established in a legally defensible way.
- No action required for the provisional filing, but should be resolved before the non-provisional.

**OQ-017: Post-assignment IP landscape**
- If the company is acquired or the IP is assigned (triggering the Assignment Agreement), what happens to:
  - Existing enterprise licensees under the ELA?
  - Open-source community users of the OSS modules?
  - Any employees or contractors who contributed to the system after the provisional filing?
- The Assignment Agreement draft (Y.2) transfers "all liabilities" to Assignee, but the scope of "liabilities" relative to existing ELA licensees should be confirmed with an attorney.

---

### NOTES FROM THE RESEARCH PASS

**On the LUMO hallucinated URL (OQ-018):**
- LUMO cited `https://www.uspto.gov/patents/apply/patent-eligibility` as the August 2025 USPTO guidance URL. This URL does not match the confirmed USPTO site structure. The correct resources are:
  - Canonical SME page: `https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility`
  - August 4, 2025 memo PDF: `https://www.uspto.gov/sites/default/files/documents/memo-101-20250804.pdf`
- The hallucinated URL has been corrected in BIBLIOGRAPHY-VERIFIED.md. Any attorney communications should use the corrected URLs.

**On LUMO's micro entity fee claim (OQ-019):**
- LUMO claimed micro entity fees of "$70-$150" and advised to "verify current rates." The verified current rate (from USPTO fee schedule, effective January 19, 2025, last revised May 1, 2026) is $65 for micro entity provisional filing. LUMO's range was slightly off; the current rate is $65.

**On patent numbers cited by LUMO (OQ-020):**
- LUMO cited Apple 7,469,381, Amazon 5,960,411, and Google PageRank as examples of provisional-originated patents.
- These patent numbers are in the public record.
- The "originated from provisional" claim was not independently verified in this session.
- Before citing these in any attorney communication or patent marketing material, verify via https://ppubs.uspto.gov/pubwebapp/ that the provisional origin claim is accurate for each patent.



---

# Patent Assignment Agreement Template (future IP transfer)

> *Cited as ancestor: *
```
⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a patent attorney before executing any patent assignment.
Assignments must be recorded with the USPTO Assignment Center
(https://assignmentcenter.uspto.gov) to be effective against third-party
purchasers. This draft is not a substitute for legal counsel.
```

---

# PATENT ASSIGNMENT AGREEMENT
## DRAFT — For Attorney Review and Red-Line

**Agreement date:** [DATE]
**Assignor:** [INVENTOR 1 NAME] and [INVENTOR 2 NAME], individuals, joint owners of the Patent Rights described herein ("Assignor")
**Assignee:** [ACQUIRING ENTITY LEGAL NAME] ("Assignee")
**Consideration:** [DOLLAR AMOUNT] USD, receipt of which is hereby acknowledged, plus the mutual covenants herein

---

### RECITALS

WHEREAS, Assignor is the joint inventor and owner of the Patent Rights described in Exhibit A, covering a novel autonomous multi-agent AI orchestration system;

WHEREAS, Assignee desires to acquire all right, title, and interest in the Patent Rights;

WHEREAS, Assignor is willing to assign the Patent Rights on the terms and conditions set forth herein, including the express conditions that: (a) Assignee assumes all future liabilities associated with the Patent Rights; (b) Assignor is released from all future obligations; and (c) Assignor has no obligation to provide future support, updates, or technical assistance for the assigned technology;

NOW, THEREFORE, in consideration of the mutual covenants and the consideration paid hereunder, the parties agree as follows:

---

### SECTION Y: TRANSFER OF RIGHTS AND RELEASE OF LIABILITY

**Y.1 Assignment.** Assignor hereby irrevocably assigns, transfers, and conveys to Assignee, its successors and assigns, all right, title, and interest worldwide in and to:

(a) The patent application(s) identified in Exhibit A (the "Assigned Patent Rights"), including U.S. Provisional Patent Application No. [TBD], any subsequent non-provisional applications claiming priority thereto, and all patents issuing therefrom;

(b) All rights to sue for past, present, and future infringements of the Assigned Patent Rights;

(c) All rights to collect royalties, damages, and other monetary relief for infringement of the Assigned Patent Rights;

(d) All counterpart patent rights in all foreign jurisdictions;

(e) All goodwill associated with the Assigned Patent Rights.

**Y.2 Assumption of Liabilities.** Effective as of the Closing Date, Assignee hereby assumes all liabilities, obligations, and risks associated with the operation, maintenance, support, prosecution, enforcement, and future use of the Assigned Patent Rights and the underlying technology. Assignee agrees to indemnify, defend, and hold harmless Assignor from any and all claims, demands, losses, damages, or expenses (including reasonable attorneys' fees) arising out of or related to the Assigned Patent Rights after the Closing Date.

**Y.3 Release and Waiver of Future Claims.** Assignor and Assignee mutually agree that, except for breaches of this Agreement occurring prior to the Closing Date:

(a) Assignor is hereby released and discharged from any and all claims, liabilities, or obligations (known or unknown, matured or contingent) arising from the future use, modification, deployment, licensing, enforcement, or commercialization of the Assigned Patent Rights by Assignee or its successors, licensees, or assigns;

(b) Assignee waives any right to assert claims against Assignor regarding the performance, safety, legal compliance, validity, enforceability, or scope of the Assigned Patent Rights after the Closing Date;

(c) This release applies to claims arising under patent law, contract, tort, or any other legal theory;

(d) THIS RELEASE DOES NOT APPLY TO FRAUD, KNOWING MISREPRESENTATION, OR INTENTIONAL MISCONDUCT BY ASSIGNOR OCCURRING PRIOR TO THE CLOSING DATE. [Note to attorney: some jurisdictions void releases for known defects sold knowingly; confirm scope with local counsel.]

**Y.4 No Future Support Obligation.** Assignor has no obligation, after the Closing Date, to provide:

(a) future updates, patches, or improvements to the assigned technology;

(b) bug fixes, security patches, or vulnerability remediation;

(c) technical support, documentation updates, or training;

(d) consultation regarding the technology's operation, architecture, or licensing;

(e) assistance with patent prosecution beyond the obligations set forth in Section Z.4.

Assignee acknowledges that the Assigned Patent Rights and underlying technology are transferred in their current state on the Closing Date, without any future guarantees of any kind.

---

### SECTION Z: ADDITIONAL TERMS

**Z.1 Representations and Warranties of Assignor.** Assignor represents and warrants, as of the Closing Date, that:

(a) Assignor is the sole legal and beneficial owner of the Assigned Patent Rights, free and clear of all liens, encumbrances, and adverse claims known to Assignor;

(b) Assignor has full right and authority to execute this Agreement and make this assignment;

(c) To Assignor's knowledge, no third party has made a written claim challenging the validity or ownership of the Assigned Patent Rights;

(d) The provisional application identified in Exhibit A was filed with the USPTO and is in good standing as of the Closing Date.

**Z.2 As-Is Transfer.** EXCEPT AS EXPRESSLY SET FORTH IN SECTION Z.1, THE ASSIGNED PATENT RIGHTS ARE TRANSFERRED "AS IS" AND "AS AVAILABLE," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, VALIDITY, ENFORCEABILITY, OR SCOPE OF THE ASSIGNED PATENT RIGHTS.

**Z.3 Limitation of Liability.** IN NO EVENT SHALL ASSIGNOR BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATED TO THIS AGREEMENT OR THE ASSIGNED PATENT RIGHTS, REGARDLESS OF THE THEORY OF LIABILITY. ASSIGNOR'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL NOT EXCEED THE CONSIDERATION PAID BY ASSIGNEE.

**Z.4 Cooperation for Prosecution.** Assignor agrees to execute, at Assignee's expense, such additional documents and take such further actions as may be reasonably necessary to perfect, record, or enforce the assignment, including executing formal USPTO Assignment Cover Sheets and providing declarations of inventorship for patent prosecution purposes. Assignor's obligation under this Section is limited to actions that can be accomplished without significant time investment; Assignor may charge Assignee for time at a reasonable rate if cooperation required exceeds [N] hours.

**Z.5 USPTO Recordation.** Assignee is responsible for recording this assignment with the USPTO Assignment Center (https://assignmentcenter.uspto.gov) within thirty (30) days of the Closing Date. Recording is required to be effective against subsequent purchasers and mortgagees. [Note: 35 U.S.C. § 261 governs patent assignment recordation.]

**Z.6 Governing Law.** This Agreement is governed by the laws of [STATE — OPEN QUESTION], without regard to conflict of laws principles. Federal patent law governs the validity, scope, and enforceability of the Assigned Patent Rights.

**Z.7 Entire Agreement.** This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, and agreements.

**Z.8 Counterparts; Electronic Signatures.** This Agreement may be executed in counterparts (including electronic signatures); each is an original; together they constitute one agreement.

---

### EXHIBIT A — ASSIGNED PATENT RIGHTS

1. U.S. Provisional Patent Application No. [TBD — complete upon filing], entitled "[TITLE — use same title as provisional specification]", filed [DATE], by inventors [INVENTOR 1] and [INVENTOR 2].

2. Any and all non-provisional applications, continuations, continuations-in-part, and divisionals of the foregoing, and all patents issuing therefrom.

3. All foreign counterpart applications and patents.

---

### SIGNATURE BLOCK

**ASSIGNOR:**

_____________________________ Date: _______________
[INVENTOR 1 NAME]
[Address]

_____________________________ Date: _______________
[INVENTOR 2 NAME]
[Address]

**ASSIGNEE:**

_____________________________ Date: _______________
[Authorized Signatory Name]
[Title]
[ACQUIRING ENTITY NAME]
[Address]

---

**Note to Attorney:** This draft includes Sections Y.1 (Assignment), Y.2 (Assumption of Liabilities), Y.3 (Release and Waiver), and Y.4 (No Future Support) from LUMO's verbatim boilerplate, adapted with swarmy-specific content (Assigned Patent Rights referencing the provisional specification, technology described in chart.json). The release scope in Y.3 should be carefully reviewed: U.S. courts frequently void liability waivers for (a) known defects sold knowingly, (b) fraud, and (c) pre-closing negligence. The forward-looking release (post-Closing Date) is generally enforceable; the backward release for pre-closing conduct may be challenged. The carve-out in Y.3(d) for fraud/intentional misconduct is included to reduce the risk of the entire release being voided.



---

# Blurbs Brainstorm — semantic-density picks for patent title + abstract + recitals + marketing

> *Cited as ancestor: *
---
type: brainstorm-sidecar
status: draft
sibling_to: PATENT-PROVISIONAL-SPECIFICATION.md
created: 2026-05-23
authors:
  - tier: agent
    id: agent:claude-opus-4-7-run-289dd044
    contribution: "brainstorm sweep of 10-word semantic-density blurbs across audiences + tones"
  - tier: human
    id: "human:goodoleusa (curation pending)"
    contribution: "selection + refinement of preferred blurbs for patent title / abstract / marketing"
---

# 🎯 Blurbs Brainstorm — 10-Word Semantic-Density Captures

> **Purpose:** the patent application's cover sheet title is constrained to ~2-7 words; the abstract is ~150 words; the marketing one-liner is whatever density you choose. This sidecar mines the system's identity at maximum semantic density, grouped by audience + tone, so the human curator can select / refine for each use surface.
>
> **System being described:** multi-agent AI orchestration platform with (1) hierarchical memory promotion (HONEY/NECTAR/pollen), (2) stigmergic filesystem coordination (w3w mission addressing, compass bearings), (3) four-shields enforcement (🛡🧠⛓🪞), (4) shape-registry mechanical verdicts, (5) membench quality substrate, (6) four-bulkheads cyber defense, (7) zero-knowledge customer-key-custody (encryption + signing), (8) customer-side runtime + customer-held cryptographic primitives end-to-end.

---

## A. Patent-language density-max (jargon-heavy, technical attorneys)

A1. "Stigmergic multi-agent AI orchestration with zero-knowledge customer-side cryptographic sovereignty."

A2. "Mechanical-verdict shape-registry AI orchestration on hash-chained forensic substrate."

A3. "Forensically-grounded multi-agent AI with four-bulkhead cyber defense and zero-knowledge custody."

A4. "Hierarchical memory promotion + stigmergic coordination + zero-knowledge customer-controlled signing."

A5. "Cryptographically-sovereign multi-agent AI orchestration with mechanically-verified forensic chain-of-custody."

A6. "Multi-tenant AI orchestration with customer-sovereign cryptographic primitives end-to-end."

A7. "Forensically-sound AI swarm orchestration via four-shields + four-bulkheads + zero-knowledge custody."

A8. "Zero-vendor-cryptographic-surface AI orchestration with mechanical verdict classification and forensic chain integrity."

→ A1, A6, A8 are the densest semantic packs. A2 captures the measurement substrate angle most cleanly.

---

## B. Plain-language operator-friendly (marketing one-liners)

B1. "Multi-agent AI orchestration where customers own the keys, the audit trail, and the substrate."

B2. "Verifiable AI agents on customer infrastructure with customer-held cryptographic sovereignty."

B3. "AI agents that coordinate via filesystem, sign via customer keys, and never leak customer data."

B4. "Compliance-by-construction multi-agent AI: customer-held keys, hash-chained audits, zero vendor cryptographic surface."

B5. "AI orchestration where the customer holds every key — encryption AND signing — and the vendor holds nothing."

B6. "The AI you run, on infrastructure you own, with keys YOU hold and audits YOU can verify."

B7. "Multi-agent AI for regulated industries: customer-sovereign, forensically-grounded, mechanically-verifiable."

→ B1, B4, B6 are the strongest. B6 reads like a tagline; B4 reads like a sales sheet.

---

## C. Metaphor-driven (the storytelling angle)

C1. "An AI swarm with watertight bulkheads, mechanical verdicts, and the customer holding the keys."

C2. "Bee-pattern AI orchestration on a forensic substrate the customer cryptographically owns."

C3. "AI agents that work like a beehive: stigmergic coordination, hierarchical memory, customer-held seals."

C4. "Hive-architecture AI for regulated industries: every agent watertight, every action witnessed by customer signatures."

C5. "Multi-agent AI where the swarm coordinates by leaving marks, and the customer holds every key."

→ C1 + C2 carry the swarmy/bee identity well. C3 lands the metaphor + the value prop together.

---

## D. Patent-claim-shaped (formal, USPTO-cover-sheet candidates)

D1. "Multi-agent AI orchestration with hierarchical promotion gates, stigmergic coordination, and customer-sovereign forensic signing."

D2. "Forensically-sound AI orchestration via four-shields enforcement, four-bulkheads defense, and customer-held cryptographic primitives."

D3. "Autonomous multi-agent orchestration system with hierarchical memory promotion, stigmergic filesystem coordination, four-layer enforcement stack, and zero-knowledge customer cryptographic sovereignty." [the current PATENT-PROVISIONAL-SPECIFICATION title — 24 words; possibly the formal one but long]

D4. "Multi-agent AI orchestration platform with mechanically-verified forensic chain-of-custody and customer-held cryptographic primitives."

D5. "Stigmergic AI orchestration system with zero-knowledge customer-key custody for forensic integrity operations."

→ Cover sheet title prefers 2-7 words; these are abstract-grade. For cover sheet, consider:
- "Stigmergic Multi-Agent AI with Customer-Sovereign Signing" (7 words)
- "Forensically-Sovereign Multi-Agent AI Orchestration" (5 words)
- "Zero-Knowledge Multi-Agent AI Orchestration" (5 words)

---

## E. Compliance / business-development blurbs (CTO / GC / Privacy Officer audience)

E1. "Multi-jurisdiction-ready AI: customer-controlled keys, machine-verifiable audit trail, zero vendor-side cryptographic surface."

E2. "Customer-sovereign AI: encrypted data + signed audit + bulkhead-protected execution = compliance-by-construction."

E3. "AI orchestration that satisfies GDPR + HIPAA + PHIPA by architectural construction, not by policy."

E4. "Compliance-by-construction AI: every cryptographic primitive belongs to the customer, every action is mechanically auditable."

E5. "The first multi-agent AI platform with ZERO vendor-side cryptographic surface — encryption + signing both customer-held."

→ E4 + E5 are the privacy-officer pitches. E5 is the marketing-grade differentiator.

---

## F. Punchy / catchy / branding-ready (1-sentence theses)

F1. "AI that proves its own work — and YOU prove the AI."

F2. "Stigmergic AI orchestration. Zero vendor cryptographic surface. Hash-chained forensic record."

F3. "Multi-agent AI orchestration where every cryptographic operation belongs to the customer."

F4. "The AI swarm that signs everything — with YOUR keys, not ours."

F5. "Hive-architecture AI: customer-sovereign, forensically-grounded, mechanically-verifiable."

F6. "Sovereign AI. Customer-held keys. Verifiable on every operation."

F7. "Multi-agent AI on a forensic substrate the customer cryptographically owns."

F8. "The first AI orchestration platform with zero vendor cryptographic surface."

→ F1 is the punchiest tagline (8 words). F4 is the operator-emotion pitch. F8 is the "we got there first" claim — historically defensible IF the patent + prior-art search support it.

---

## G. Title candidates (2-7 words — USPTO cover sheet)

G1. "Stigmergic Multi-Agent AI Orchestration" (4 words)

G2. "Customer-Sovereign Multi-Agent AI" (4 words)

G3. "Zero-Knowledge AI Orchestration System" (4 words)

G4. "Forensically-Sound Multi-Agent AI Platform" (5 words)

G5. "Hive-Pattern AI Orchestration Architecture" (4 words)

G6. "Customer-Held Cryptographic AI Orchestration" (4 words)

G7. "Stigmergic AI with Customer-Sovereign Signing" (5 words)

G8. "Multi-Agent AI Orchestration with Zero Vendor Cryptographic Surface" (8 words — over budget but tells the whole story)

→ G3, G6, G7 are the strongest cover-sheet candidates. G7 captures the most-novel angle in 5 words. G3 is the cleanest single-claim summary.

---

## H. Abstract opening sentences (~150 word abstract starts with one of these)

H1. "Disclosed is a multi-agent artificial intelligence orchestration system in which the customer holds every cryptographic primitive used to operate the system — both encryption keys for data confidentiality and signing keys for forensic chain-of-custody integrity — yielding a system with zero vendor-side cryptographic surface and architectural compliance with GDPR, HIPAA, PHIPA, and analogous regulatory frameworks by construction rather than by policy."

H2. "The present invention provides a multi-agent AI orchestration platform combining hierarchical memory promotion with mechanical verification gates, stigmergic filesystem-based agent coordination, four-layer cheaper-earlier discipline enforcement, mechanical shape-registry quality verdicts, and customer-sovereign cryptographic operations end-to-end — producing an AI system whose forensic record is verifiable by the customer, whose discipline is mechanically enforced, and whose data sovereignty is a technical property rather than a contractual commitment."

H3. "Disclosed is an autonomous multi-agent AI orchestration system characterized by (1) zero-knowledge customer-key custody for both data encryption and forensic signing operations, (2) stigmergic filesystem-mediated agent coordination eliminating orchestrator/router bottlenecks, (3) mechanical shape-registry quality classification replacing LLM-judgment evaluation, and (4) four-shields plus four-bulkheads defense-in-depth providing court-discovery-ready audit trails."

→ H1 is the strongest opener — leads with the zero-knowledge claim that's the most-novel-combination element. H2 covers the full surface but reads dense. H3 is the structured technical opener for the formal abstract section.

---

## I. Working candidates for human curator

The human curator (operator) should review + pick + refine. My picks across surfaces:

- **USPTO cover sheet title:** G7 "Stigmergic AI with Customer-Sovereign Signing" (5 words; captures most-novel angle)
- **Patent abstract opener:** H1 (leads with zero-knowledge, the strongest novelty claim)
- **ELA recital opening line:** D1 "Multi-agent AI orchestration with hierarchical promotion gates, stigmergic coordination, and customer-sovereign forensic signing."
- **Marketing one-liner:** F1 "AI that proves its own work — and YOU prove the AI."
- **Privacy-officer pitch:** E5 "The first multi-agent AI platform with ZERO vendor-side cryptographic surface — encryption + signing both customer-held."
- **Operator-friendly tagline:** B6 "The AI you run, on infrastructure you own, with keys YOU hold and audits YOU can verify."
- **Compliance pitch:** E2 "Customer-sovereign AI: encrypted data + signed audit + bulkhead-protected execution = compliance-by-construction."
- **Storytelling / blog post hook:** C3 "AI agents that work like a beehive: stigmergic coordination, hierarchical memory, customer-held seals."

## J. Density grammar — what made the strongest blurbs work

The patterns to mine across all 8 groups:

1. **Triadic structure** — "X + Y + Z = W" reads like a thesis (E2, F2, F5). The brain loves three.
2. **Customer-held / customer-sovereign / YOU** — the second-person ownership claim does immense work; B-, E-, F- groups lean on it heavily.
3. **ZERO X** as anchor — "zero vendor-side cryptographic surface" is the strongest specific differentiator; appears in A8, B4, E1, F2, F8.
4. **"By construction" / "architectural" not "by policy"** — collapses the regulatory-compliance argument into one phrase (E2, E3, E4, H1).
5. **Compound architectural terms in series** — "encryption AND signing both customer-held" or "stigmergic + zero-knowledge + mechanically-verified" — high jargon density but the technical reader parses fast (A4, A5, D2).
6. **Verbs over nouns where possible** — "the AI proves," "the customer signs," "the system verifies" — more energetic than passive description.

## K. What to AVOID

- "Revolutionary," "groundbreaking," "next-generation" — patent application style guides explicitly recommend against, plus they're empty
- Acronyms without expansion — assume nothing
- "Best-in-class" — unverifiable
- Trademark conflicts — verify any "Hive" or "Swarm" branding against existing AI products before settling on it for the patent (operator action; outside agent scope)

## L. Final selection workflow (for the human curator)

1. **Pick the cover-sheet title** from G3 / G6 / G7 (or refine)
2. **Pick the abstract opener** from H1 / H2 / H3
3. **Pick the marketing one-liner** from F1 / B6 / E5
4. **Curate the rest** — at least 3 of these will end up in ELA recitals, BAA preamble, DPA preamble, and the company's public-facing materials. The brainstorm catalog above is the source.
5. **Commit the final selections** back into PATENT-PROVISIONAL-SPECIFICATION.md as the formal title + abstract + recital openings.


---

(continued from _source/OPEN-QUESTIONS.md)

# OPEN QUESTIONS
## Operator Must Answer Before USPTO Filing or Attorney Engagement

**Status:** Compiled from `charter.json` open_questions + discoveries during the polished-deliverables research pass.
**Date compiled:** 2026-05-23
**Agent:** research-analyst (expedition-w1)

---

### CRITICAL — Required Before USPTO Filing

These questions block the provisional filing. The provisional cannot be filed until they are answered.

**OQ-001: Co-inventor name and identity**
- What is the co-inventor's full legal name (as it will appear on the USPTO cover sheet)?
- What is their current mailing address (required on Form SB/16)?
- What is their citizenship / country of residence (required for USPTO filing)?
- Are there any ownership agreements between the two inventors regarding the patent rights (e.g., a co-inventor agreement specifying ownership split)?

**OQ-002: Lead inventor (first named inventor) information**
- Full legal name as it will appear on the USPTO cover sheet
- Current mailing address
- Citizenship / country of residence

**OQ-003: Entity status for fee calculation**
- Do BOTH inventors qualify for micro entity status?
  - Micro entity gross income qualification: as of 2025, maximum qualifying gross income is $251,190/year (confirmed from USPTO fee schedule search)
  - Micro entity filing limit: no more than 4 previous patent applications filed as inventor (provisional applications do not count toward this limit)
  - If either inventor does not qualify, the filing fee tier drops to small entity ($130) or regular ($325)
- Recommendation: confirm micro entity qualification with a patent attorney before filing

**OQ-004: Provisional patent title**
- The draft title in this specification is: "Autonomous Multi-Agent Orchestration System with Hierarchical Memory Promotion, Stigmergic Filesystem Coordination, Four-Layer Enforcement Stack, and Mechanical Quality Classification"
- USPTO recommends titles that are 2–7 words but this is a recommendation, not a requirement for provisionals
- Operator should confirm or adjust this title

---

### HIGH PRIORITY — Required Before ELA Execution

These questions block the ELA from being signed.

**OQ-005: Company entity legal name and state of incorporation**
- What is the full legal name of the company entity that will sign as Licensor?
- What state is it (or will it be) incorporated/formed in?
- If the company does not yet exist: the ELA Option A (company as exclusive sublicensee from inventors, then sublicenses to enterprise customer) requires a separate Exclusive License Agreement between the Inventors and the Company entity. The company must exist before this can be executed.

**OQ-006: ELA structure decision (Section 14 of ELA-DRAFT.md)**
- **Option A (recommended):** Inventors grant exclusive license to Company entity; Company sublicenses to Licensee. Provides liability shield but requires Exclusive License Agreement between Inventors and Company.
- **Option B (fallback):** Inventors license directly to Licensee. Simpler but exposes inventors personally.
- Which structure does the operator choose? Attorney should advise on tax and liability implications before selecting.

**OQ-007: First enterprise customer information**
- Customer legal name and state of formation (affects governing law selection and jurisdiction)
- Industry vertical (affects due-diligence affirmation scope and acceptable use provisions)
- Deal size class (affects fee schedule structure — flat fee vs. usage-based vs. revenue share)
- Timeline for contract signature (drives ELA finalization deadline)

**OQ-008: Governing law jurisdiction**
- The ELA and Assignment Agreement both have [STATE — OPEN QUESTION] placeholders.
- Most common choices for software companies: Delaware (company law alignment), California (where many enterprise customers are based), or the operator's home state.
- Attorney should advise based on company formation state and enterprise customer's jurisdiction.

**OQ-009: Dispute resolution mechanism**
- ELA Section 10.2 has a placeholder for arbitration provider (AAA or JAMS) and seat (city/state).
- Attorney should advise on which arbitration forum is appropriate for the deal size and customer type.

---

### MEDIUM PRIORITY — Required Before Non-Provisional Filing or Patent Attorney Engagement

**OQ-010: Patent attorney engagement**
- The provisional establishes the priority date. The 12-month clock to non-provisional conversion begins on the filing date.
- A registered patent attorney must: (a) review and refine the provisional specification; (b) draft formal independent and dependent claims for the non-provisional; (c) advise on claim scope vs. prior art; and (d) handle USPTO prosecution.
- Recommended timeline: engage attorney within 6 months of provisional filing, before the 12-month clock expires.
- Budget note: non-provisional patent prosecution typically costs $8,000–$20,000+ including attorney fees and USPTO fees. Provisional filing itself (DIY, no attorney) costs $65 (micro entity) + Form SB/16 + specification PDF.

**OQ-011: Prior art disclosure**
- Are the inventors aware of any prior art systems that describe similar techniques?
  - Stigmergic agent coordination systems (e.g., swarm intelligence papers, ACO — ant colony optimization systems)?
  - Hierarchical memory systems for AI agents (e.g., MemGPT, Reflexion, generative agents)?
  - Mechanical verdict classification systems in software engineering (e.g., mutation testing frameworks)?
  - Four-layer enforcement stacks in computer security (e.g., defense-in-depth frameworks)?
- Full prior art disclosure is required for USPTO examination. Inventors have a duty to disclose material prior art they are aware of.

**OQ-012: Jurisdiction strategy**
- US-only first (provisional + US non-provisional)?
- PCT international filing (covers 150+ countries, must file within 12 months of provisional)?
- Direct national phase in specific jurisdictions (EU, UK, China, Japan) without PCT?
- PCT route preserves maximum international options but adds significant cost ($5,000–$15,000+ for PCT filing, then national phase fees).
- Attorney should advise based on where the operator expects commercial activity.

---

### MEDIUM PRIORITY — Module Disposition Matrix

**OQ-013: Per-module OSS vs. proprietary disposition**
- The operator selected "core-engine-proprietary-rest-open" strategy.
- A concrete per-module decision matrix is needed to ensure the patent's novel-combination claim covers the IP boundary cleanly.
- Draft matrix (operator must confirm or revise):

| Module / Component | Proposed Disposition | Notes |
|---|---|---|
| `scripts/1a_manifest_writer.py` | Proprietary | Core memory promotion gate |
| `scripts/2d_frontier_scanner_indexed.py` | Proprietary | Core stigmergic coordination |
| `scripts/2a_spawn_pressure.py` | Proprietary | Core spawn formula |
| `scripts/shapes/_shapes_lib.py` | Proprietary | Core mechanical verdict classifier |
| `scripts/3f_membench_probes.py` | Proprietary | Core membench substrate |
| `scripts/3k_membench_scorer.py` | Proprietary | Core evaluation substrate |
| `forensics/schemas/formulas/*.formula.json` | Proprietary | Core formula definitions |
| `_meta/shapes.json` | Proprietary | Core shape registry |
| `.openhands/hooks/9x_hook-*.py` | Proprietary | Core reactive enforcement |
| `HONEY.md`, `NECTAR.md` (format/protocol) | Proprietary | Core memory protocol |
| `.agents/skills/*/SKILL.md` | Open source (OSS) | Community building |
| `.agents/skills/forage/SKILL.md` | Open source (OSS) | Community building |
| `AGENTS.md` (doctrine) | Open source (OSS) | Community building |
| Agent archetypes (NAVIGATOR, MAKER, etc.) | Open source (OSS) | Community building |
| Vault patterns, Obsidian structure | Open source (OSS) | Community building |

**OQ-014: forensic-coc-v2-rekor integration decision**
- The `forensic-coc-v2-rekor` charter covers a Merkle-tree + Sigstore Rekor witnessing architecture for the forensic chain-of-custody.
- Decision needed: (a) fold it into the current provisional as an additional claim area (requires adding Section 7 to the patent spec before filing); or (b) file a separate provisional for that architecture?
- The current provisional spec describes the SHA-256 hash chain (`forensics/coc.jsonl`) but does not claim the Rekor witnessing layer.
- Attorney should advise on whether combining or separating provides stronger protection.

---

### LOWER PRIORITY — For Later Planning

**OQ-015: share.note.sx encrypted note content**
- The operator referenced additional research at `https://share.note.sx/xyjlsmzd#yOf7fYmiC6qLhW4kHDi3uPpst9+YRt2pnEfWJ32FnTo`
- This note uses client-side encryption; the agent could not decrypt it in this session.
- Action: operator opens the URL in a browser, copies the decrypted content, and provides it for the next research pass.
- The decrypted content may contain additional patent claim language, ELA clauses, prior art references, or other material that should be incorporated into the polished deliverables.

**OQ-016: Multi-signature ed25519 notary key strategy**
- The `forensic-coc-v2-rekor` charter cross-references a notary key strategy for the company's overall identity.
- This may affect how the patent's forensic chain-of-custody claims are framed and how the company's IP ownership is established in a legally defensible way.
- No action required for the provisional filing, but should be resolved before the non-provisional.

**OQ-017: Post-assignment IP landscape**
- If the company is acquired or the IP is assigned (triggering the Assignment Agreement), what happens to:
  - Existing enterprise licensees under the ELA?
  - Open-source community users of the OSS modules?
  - Any employees or contractors who contributed to the system after the provisional filing?
- The Assignment Agreement draft (Y.2) transfers "all liabilities" to Assignee, but the scope of "liabilities" relative to existing ELA licensees should be confirmed with an attorney.

---

### NOTES FROM THE RESEARCH PASS

**On the LUMO hallucinated URL (OQ-018):**
- LUMO cited `https://www.uspto.gov/patents/apply/patent-eligibility` as the August 2025 USPTO guidance URL. This URL does not match the confirmed USPTO site structure. The correct resources are:
  - Canonical SME page: `https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility`
  - August 4, 2025 memo PDF: `https://www.uspto.gov/sites/default/files/documents/memo-101-20250804.pdf`
- The hallucinated URL has been corrected in BIBLIOGRAPHY-VERIFIED.md. Any attorney communications should use the corrected URLs.

**On LUMO's micro entity fee claim (OQ-019):**
- LUMO claimed micro entity fees of "$70-$150" and advised to "verify current rates." The verified current rate (from USPTO fee schedule, effective January 19, 2025, last revised May 1, 2026) is $65 for micro entity provisional filing. LUMO's range was slightly off; the current rate is $65.

**On patent numbers cited by LUMO (OQ-020):**
- LUMO cited Apple 7,469,381, Amazon 5,960,411, and Google PageRank as examples of provisional-originated patents.
- These patent numbers are in the public record.
- The "originated from provisional" claim was not independently verified in this session.
- Before citing these in any attorney communication or patent marketing material, verify via https://ppubs.uspto.gov/pubwebapp/ that the provisional origin claim is accurate for each patent.



---

(continued from _source/ASSIGNMENT-AGREEMENT-DRAFT.md)

```
⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a patent attorney before executing any patent assignment.
Assignments must be recorded with the USPTO Assignment Center
(https://assignmentcenter.uspto.gov) to be effective against third-party
purchasers. This draft is not a substitute for legal counsel.
```

---

# PATENT ASSIGNMENT AGREEMENT
## DRAFT — For Attorney Review and Red-Line

**Agreement date:** [DATE]
**Assignor:** [INVENTOR 1 NAME] and [INVENTOR 2 NAME], individuals, joint owners of the Patent Rights described herein ("Assignor")
**Assignee:** [ACQUIRING ENTITY LEGAL NAME] ("Assignee")
**Consideration:** [DOLLAR AMOUNT] USD, receipt of which is hereby acknowledged, plus the mutual covenants herein

---

### RECITALS

WHEREAS, Assignor is the joint inventor and owner of the Patent Rights described in Exhibit A, covering a novel autonomous multi-agent AI orchestration system;

WHEREAS, Assignee desires to acquire all right, title, and interest in the Patent Rights;

WHEREAS, Assignor is willing to assign the Patent Rights on the terms and conditions set forth herein, including the express conditions that: (a) Assignee assumes all future liabilities associated with the Patent Rights; (b) Assignor is released from all future obligations; and (c) Assignor has no obligation to provide future support, updates, or technical assistance for the assigned technology;

NOW, THEREFORE, in consideration of the mutual covenants and the consideration paid hereunder, the parties agree as follows:

---

### SECTION Y: TRANSFER OF RIGHTS AND RELEASE OF LIABILITY

**Y.1 Assignment.** Assignor hereby irrevocably assigns, transfers, and conveys to Assignee, its successors and assigns, all right, title, and interest worldwide in and to:

(a) The patent application(s) identified in Exhibit A (the "Assigned Patent Rights"), including U.S. Provisional Patent Application No. [TBD], any subsequent non-provisional applications claiming priority thereto, and all patents issuing therefrom;

(b) All rights to sue for past, present, and future infringements of the Assigned Patent Rights;

(c) All rights to collect royalties, damages, and other monetary relief for infringement of the Assigned Patent Rights;

(d) All counterpart patent rights in all foreign jurisdictions;

(e) All goodwill associated with the Assigned Patent Rights.

**Y.2 Assumption of Liabilities.** Effective as of the Closing Date, Assignee hereby assumes all liabilities, obligations, and risks associated with the operation, maintenance, support, prosecution, enforcement, and future use of the Assigned Patent Rights and the underlying technology. Assignee agrees to indemnify, defend, and hold harmless Assignor from any and all claims, demands, losses, damages, or expenses (including reasonable attorneys' fees) arising out of or related to the Assigned Patent Rights after the Closing Date.

**Y.3 Release and Waiver of Future Claims.** Assignor and Assignee mutually agree that, except for breaches of this Agreement occurring prior to the Closing Date:

(a) Assignor is hereby released and discharged from any and all claims, liabilities, or obligations (known or unknown, matured or contingent) arising from the future use, modification, deployment, licensing, enforcement, or commercialization of the Assigned Patent Rights by Assignee or its successors, licensees, or assigns;

(b) Assignee waives any right to assert claims against Assignor regarding the performance, safety, legal compliance, validity, enforceability, or scope of the Assigned Patent Rights after the Closing Date;

(c) This release applies to claims arising under patent law, contract, tort, or any other legal theory;

(d) THIS RELEASE DOES NOT APPLY TO FRAUD, KNOWING MISREPRESENTATION, OR INTENTIONAL MISCONDUCT BY ASSIGNOR OCCURRING PRIOR TO THE CLOSING DATE. [Note to attorney: some jurisdictions void releases for known defects sold knowingly; confirm scope with local counsel.]

**Y.4 No Future Support Obligation.** Assignor has no obligation, after the Closing Date, to provide:

(a) future updates, patches, or improvements to the assigned technology;

(b) bug fixes, security patches, or vulnerability remediation;

(c) technical support, documentation updates, or training;

(d) consultation regarding the technology's operation, architecture, or licensing;

(e) assistance with patent prosecution beyond the obligations set forth in Section Z.4.

Assignee acknowledges that the Assigned Patent Rights and underlying technology are transferred in their current state on the Closing Date, without any future guarantees of any kind.

---

### SECTION Z: ADDITIONAL TERMS

**Z.1 Representations and Warranties of Assignor.** Assignor represents and warrants, as of the Closing Date, that:

(a) Assignor is the sole legal and beneficial owner of the Assigned Patent Rights, free and clear of all liens, encumbrances, and adverse claims known to Assignor;

(b) Assignor has full right and authority to execute this Agreement and make this assignment;

(c) To Assignor's knowledge, no third party has made a written claim challenging the validity or ownership of the Assigned Patent Rights;

(d) The provisional application identified in Exhibit A was filed with the USPTO and is in good standing as of the Closing Date.

**Z.2 As-Is Transfer.** EXCEPT AS EXPRESSLY SET FORTH IN SECTION Z.1, THE ASSIGNED PATENT RIGHTS ARE TRANSFERRED "AS IS" AND "AS AVAILABLE," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, VALIDITY, ENFORCEABILITY, OR SCOPE OF THE ASSIGNED PATENT RIGHTS.

**Z.3 Limitation of Liability.** IN NO EVENT SHALL ASSIGNOR BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATED TO THIS AGREEMENT OR THE ASSIGNED PATENT RIGHTS, REGARDLESS OF THE THEORY OF LIABILITY. ASSIGNOR'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL NOT EXCEED THE CONSIDERATION PAID BY ASSIGNEE.

**Z.4 Cooperation for Prosecution.** Assignor agrees to execute, at Assignee's expense, such additional documents and take such further actions as may be reasonably necessary to perfect, record, or enforce the assignment, including executing formal USPTO Assignment Cover Sheets and providing declarations of inventorship for patent prosecution purposes. Assignor's obligation under this Section is limited to actions that can be accomplished without significant time investment; Assignor may charge Assignee for time at a reasonable rate if cooperation required exceeds [N] hours.

**Z.5 USPTO Recordation.** Assignee is responsible for recording this assignment with the USPTO Assignment Center (https://assignmentcenter.uspto.gov) within thirty (30) days of the Closing Date. Recording is required to be effective against subsequent purchasers and mortgagees. [Note: 35 U.S.C. § 261 governs patent assignment recordation.]

**Z.6 Governing Law.** This Agreement is governed by the laws of [STATE — OPEN QUESTION], without regard to conflict of laws principles. Federal patent law governs the validity, scope, and enforceability of the Assigned Patent Rights.

**Z.7 Entire Agreement.** This Agreement constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, and agreements.

**Z.8 Counterparts; Electronic Signatures.** This Agreement may be executed in counterparts (including electronic signatures); each is an original; together they constitute one agreement.

---

### EXHIBIT A — ASSIGNED PATENT RIGHTS

1. U.S. Provisional Patent Application No. [TBD — complete upon filing], entitled "[TITLE — use same title as provisional specification]", filed [DATE], by inventors [INVENTOR 1] and [INVENTOR 2].

2. Any and all non-provisional applications, continuations, continuations-in-part, and divisionals of the foregoing, and all patents issuing therefrom.

3. All foreign counterpart applications and patents.

---

### SIGNATURE BLOCK

**ASSIGNOR:**

_____________________________ Date: _______________
[INVENTOR 1 NAME]
[Address]

_____________________________ Date: _______________
[INVENTOR 2 NAME]
[Address]

**ASSIGNEE:**

_____________________________ Date: _______________
[Authorized Signatory Name]
[Title]
[ACQUIRING ENTITY NAME]
[Address]

---

**Note to Attorney:** This draft includes Sections Y.1 (Assignment), Y.2 (Assumption of Liabilities), Y.3 (Release and Waiver), and Y.4 (No Future Support) from LUMO's verbatim boilerplate, adapted with swarmy-specific content (Assigned Patent Rights referencing the provisional specification, technology described in chart.json). The release scope in Y.3 should be carefully reviewed: U.S. courts frequently void liability waivers for (a) known defects sold knowingly, (b) fraud, and (c) pre-closing negligence. The forward-looking release (post-Closing Date) is generally enforceable; the backward release for pre-closing conduct may be challenged. The carve-out in Y.3(d) for fraud/intentional misconduct is included to reduce the risk of the entire release being voided.



---

(continued from _source/BLURBS-BRAINSTORM.md)

---
type: brainstorm-sidecar
status: draft
sibling_to: PATENT-PROVISIONAL-SPECIFICATION.md
created: 2026-05-23
authors:
  - tier: agent
    id: agent:claude-opus-4-7-run-289dd044
    contribution: "brainstorm sweep of 10-word semantic-density blurbs across audiences + tones"
  - tier: human
    id: "human:goodoleusa (curation pending)"
    contribution: "selection + refinement of preferred blurbs for patent title / abstract / marketing"
---

# 🎯 Blurbs Brainstorm — 10-Word Semantic-Density Captures

> **Purpose:** the patent application's cover sheet title is constrained to ~2-7 words; the abstract is ~150 words; the marketing one-liner is whatever density you choose. This sidecar mines the system's identity at maximum semantic density, grouped by audience + tone, so the human curator can select / refine for each use surface.
>
> **System being described:** multi-agent AI orchestration platform with (1) hierarchical memory promotion (HONEY/NECTAR/pollen), (2) stigmergic filesystem coordination (w3w mission addressing, compass bearings), (3) four-shields enforcement (🛡🧠⛓🪞), (4) shape-registry mechanical verdicts, (5) membench quality substrate, (6) four-bulkheads cyber defense, (7) zero-knowledge customer-key-custody (encryption + signing), (8) customer-side runtime + customer-held cryptographic primitives end-to-end.

---

## A. Patent-language density-max (jargon-heavy, technical attorneys)

A1. "Stigmergic multi-agent AI orchestration with zero-knowledge customer-side cryptographic sovereignty."

A2. "Mechanical-verdict shape-registry AI orchestration on hash-chained forensic substrate."

A3. "Forensically-grounded multi-agent AI with four-bulkhead cyber defense and zero-knowledge custody."

A4. "Hierarchical memory promotion + stigmergic coordination + zero-knowledge customer-controlled signing."

A5. "Cryptographically-sovereign multi-agent AI orchestration with mechanically-verified forensic chain-of-custody."

A6. "Multi-tenant AI orchestration with customer-sovereign cryptographic primitives end-to-end."

A7. "Forensically-sound AI swarm orchestration via four-shields + four-bulkheads + zero-knowledge custody."

A8. "Zero-vendor-cryptographic-surface AI orchestration with mechanical verdict classification and forensic chain integrity."

→ A1, A6, A8 are the densest semantic packs. A2 captures the measurement substrate angle most cleanly.

---

## B. Plain-language operator-friendly (marketing one-liners)

B1. "Multi-agent AI orchestration where customers own the keys, the audit trail, and the substrate."

B2. "Verifiable AI agents on customer infrastructure with customer-held cryptographic sovereignty."

B3. "AI agents that coordinate via filesystem, sign via customer keys, and never leak customer data."

B4. "Compliance-by-construction multi-agent AI: customer-held keys, hash-chained audits, zero vendor cryptographic surface."

B5. "AI orchestration where the customer holds every key — encryption AND signing — and the vendor holds nothing."

B6. "The AI you run, on infrastructure you own, with keys YOU hold and audits YOU can verify."

B7. "Multi-agent AI for regulated industries: customer-sovereign, forensically-grounded, mechanically-verifiable."

→ B1, B4, B6 are the strongest. B6 reads like a tagline; B4 reads like a sales sheet.

---

## C. Metaphor-driven (the storytelling angle)

C1. "An AI swarm with watertight bulkheads, mechanical verdicts, and the customer holding the keys."

C2. "Bee-pattern AI orchestration on a forensic substrate the customer cryptographically owns."

C3. "AI agents that work like a beehive: stigmergic coordination, hierarchical memory, customer-held seals."

C4. "Hive-architecture AI for regulated industries: every agent watertight, every action witnessed by customer signatures."

C5. "Multi-agent AI where the swarm coordinates by leaving marks, and the customer holds every key."

→ C1 + C2 carry the swarmy/bee identity well. C3 lands the metaphor + the value prop together.

---

## D. Patent-claim-shaped (formal, USPTO-cover-sheet candidates)

D1. "Multi-agent AI orchestration with hierarchical promotion gates, stigmergic coordination, and customer-sovereign forensic signing."

D2. "Forensically-sound AI orchestration via four-shields enforcement, four-bulkheads defense, and customer-held cryptographic primitives."

D3. "Autonomous multi-agent orchestration system with hierarchical memory promotion, stigmergic filesystem coordination, four-layer enforcement stack, and zero-knowledge customer cryptographic sovereignty." [the current PATENT-PROVISIONAL-SPECIFICATION title — 24 words; possibly the formal one but long]

D4. "Multi-agent AI orchestration platform with mechanically-verified forensic chain-of-custody and customer-held cryptographic primitives."

D5. "Stigmergic AI orchestration system with zero-knowledge customer-key custody for forensic integrity operations."

→ Cover sheet title prefers 2-7 words; these are abstract-grade. For cover sheet, consider:
- "Stigmergic Multi-Agent AI with Customer-Sovereign Signing" (7 words)
- "Forensically-Sovereign Multi-Agent AI Orchestration" (5 words)
- "Zero-Knowledge Multi-Agent AI Orchestration" (5 words)

---

## E. Compliance / business-development blurbs (CTO / GC / Privacy Officer audience)

E1. "Multi-jurisdiction-ready AI: customer-controlled keys, machine-verifiable audit trail, zero vendor-side cryptographic surface."

E2. "Customer-sovereign AI: encrypted data + signed audit + bulkhead-protected execution = compliance-by-construction."

E3. "AI orchestration that satisfies GDPR + HIPAA + PHIPA by architectural construction, not by policy."

E4. "Compliance-by-construction AI: every cryptographic primitive belongs to the customer, every action is mechanically auditable."

E5. "The first multi-agent AI platform with ZERO vendor-side cryptographic surface — encryption + signing both customer-held."

→ E4 + E5 are the privacy-officer pitches. E5 is the marketing-grade differentiator.

---

## F. Punchy / catchy / branding-ready (1-sentence theses)

F1. "AI that proves its own work — and YOU prove the AI."

F2. "Stigmergic AI orchestration. Zero vendor cryptographic surface. Hash-chained forensic record."

F3. "Multi-agent AI orchestration where every cryptographic operation belongs to the customer."

F4. "The AI swarm that signs everything — with YOUR keys, not ours."

F5. "Hive-architecture AI: customer-sovereign, forensically-grounded, mechanically-verifiable."

F6. "Sovereign AI. Customer-held keys. Verifiable on every operation."

F7. "Multi-agent AI on a forensic substrate the customer cryptographically owns."

F8. "The first AI orchestration platform with zero vendor cryptographic surface."

→ F1 is the punchiest tagline (8 words). F4 is the operator-emotion pitch. F8 is the "we got there first" claim — historically defensible IF the patent + prior-art search support it.

---

## G. Title candidates (2-7 words — USPTO cover sheet)

G1. "Stigmergic Multi-Agent AI Orchestration" (4 words)

G2. "Customer-Sovereign Multi-Agent AI" (4 words)

G3. "Zero-Knowledge AI Orchestration System" (4 words)

G4. "Forensically-Sound Multi-Agent AI Platform" (5 words)

G5. "Hive-Pattern AI Orchestration Architecture" (4 words)

G6. "Customer-Held Cryptographic AI Orchestration" (4 words)

G7. "Stigmergic AI with Customer-Sovereign Signing" (5 words)

G8. "Multi-Agent AI Orchestration with Zero Vendor Cryptographic Surface" (8 words — over budget but tells the whole story)

→ G3, G6, G7 are the strongest cover-sheet candidates. G7 captures the most-novel angle in 5 words. G3 is the cleanest single-claim summary.

---

## H. Abstract opening sentences (~150 word abstract starts with one of these)

H1. "Disclosed is a multi-agent artificial intelligence orchestration system in which the customer holds every cryptographic primitive used to operate the system — both encryption keys for data confidentiality and signing keys for forensic chain-of-custody integrity — yielding a system with zero vendor-side cryptographic surface and architectural compliance with GDPR, HIPAA, PHIPA, and analogous regulatory frameworks by construction rather than by policy."

H2. "The present invention provides a multi-agent AI orchestration platform combining hierarchical memory promotion with mechanical verification gates, stigmergic filesystem-based agent coordination, four-layer cheaper-earlier discipline enforcement, mechanical shape-registry quality verdicts, and customer-sovereign cryptographic operations end-to-end — producing an AI system whose forensic record is verifiable by the customer, whose discipline is mechanically enforced, and whose data sovereignty is a technical property rather than a contractual commitment."

H3. "Disclosed is an autonomous multi-agent AI orchestration system characterized by (1) zero-knowledge customer-key custody for both data encryption and forensic signing operations, (2) stigmergic filesystem-mediated agent coordination eliminating orchestrator/router bottlenecks, (3) mechanical shape-registry quality classification replacing LLM-judgment evaluation, and (4) four-shields plus four-bulkheads defense-in-depth providing court-discovery-ready audit trails."

→ H1 is the strongest opener — leads with the zero-knowledge claim that's the most-novel-combination element. H2 covers the full surface but reads dense. H3 is the structured technical opener for the formal abstract section.

---

## I. Working candidates for human curator

The human curator (operator) should review + pick + refine. My picks across surfaces:

- **USPTO cover sheet title:** G7 "Stigmergic AI with Customer-Sovereign Signing" (5 words; captures most-novel angle)
- **Patent abstract opener:** H1 (leads with zero-knowledge, the strongest novelty claim)
- **ELA recital opening line:** D1 "Multi-agent AI orchestration with hierarchical promotion gates, stigmergic coordination, and customer-sovereign forensic signing."
- **Marketing one-liner:** F1 "AI that proves its own work — and YOU prove the AI."
- **Privacy-officer pitch:** E5 "The first multi-agent AI platform with ZERO vendor-side cryptographic surface — encryption + signing both customer-held."
- **Operator-friendly tagline:** B6 "The AI you run, on infrastructure you own, with keys YOU hold and audits YOU can verify."
- **Compliance pitch:** E2 "Customer-sovereign AI: encrypted data + signed audit + bulkhead-protected execution = compliance-by-construction."
- **Storytelling / blog post hook:** C3 "AI agents that work like a beehive: stigmergic coordination, hierarchical memory, customer-held seals."

## J. Density grammar — what made the strongest blurbs work

The patterns to mine across all 8 groups:

1. **Triadic structure** — "X + Y + Z = W" reads like a thesis (E2, F2, F5). The brain loves three.
2. **Customer-held / customer-sovereign / YOU** — the second-person ownership claim does immense work; B-, E-, F- groups lean on it heavily.
3. **ZERO X** as anchor — "zero vendor-side cryptographic surface" is the strongest specific differentiator; appears in A8, B4, E1, F2, F8.
4. **"By construction" / "architectural" not "by policy"** — collapses the regulatory-compliance argument into one phrase (E2, E3, E4, H1).
5. **Compound architectural terms in series** — "encryption AND signing both customer-held" or "stigmergic + zero-knowledge + mechanically-verified" — high jargon density but the technical reader parses fast (A4, A5, D2).
6. **Verbs over nouns where possible** — "the AI proves," "the customer signs," "the system verifies" — more energetic than passive description.

## K. What to AVOID

- "Revolutionary," "groundbreaking," "next-generation" — patent application style guides explicitly recommend against, plus they're empty
- Acronyms without expansion — assume nothing
- "Best-in-class" — unverifiable
- Trademark conflicts — verify any "Hive" or "Swarm" branding against existing AI products before settling on it for the patent (operator action; outside agent scope)

## L. Final selection workflow (for the human curator)

1. **Pick the cover-sheet title** from G3 / G6 / G7 (or refine)
2. **Pick the abstract opener** from H1 / H2 / H3
3. **Pick the marketing one-liner** from F1 / B6 / E5
4. **Curate the rest** — at least 3 of these will end up in ELA recitals, BAA preamble, DPA preamble, and the company's public-facing materials. The brainstorm catalog above is the source.
5. **Commit the final selections** back into PATENT-PROVISIONAL-SPECIFICATION.md as the formal title + abstract + recital openings.
