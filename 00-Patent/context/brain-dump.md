---
expedition: enterprise-patent-foundation
mission_id: enterprise.patent.foundation
type: brain-dump
status: captured-not-fact-checked
captured_at: 2026-05-23
operator: goodoleusa
co_collaborator: claude-opus-4-7 (capture-mode, no synthesis)
source_research: LUMO AI Memory Orchestration Patent and Legal Contract Kit (operator-curated)
next_step: spawn agent to produce polished + cited + URL-verified deliverables in ../polished-deliverables/
---

# 🧭 Brain Dump — Enterprise Patent Foundation Expedition

> **This is the raw operator-curated notes.** None of the URLs below have been verified yet. None of the legal language has been reviewed by an attorney. None of the patent claims have been refined. This document is the INPUT to the polished-deliverables spawn, not the output. Read it as a captured snapshot of intent, not as legal advice.

## The strategic context

Company is exploring its **first serious enterprise contract**. This both:
1. Validates the technology + business viability
2. **Starts the window** on USPTO provisional patent application deadlines (12-month clock to non-provisional)

So we need three interlocking products ready (or at least drafted) when the contract conversation matures:

1. **Enterprise License Agreement (ELA)** — indemnifies the company from future liability + all liability + maintenance obligations, while granting the licensee a license to tweak / modify / customize / resell their own versions of the system sold. Within the ELA the company asserts due-diligence done (no obvious or serious harm), and the language establishes the company as the **progenitor / ancestor / inventor of the entire complete system** — using multiple overlapping and intervolving modules / components in a complex ecosystem. Even if individual modules/subproducts/repositories are open-sourced, the company holds patent + associated IP rights for the overall larger system design using a **unique and novel combinations of techniques** to solve several common problems and limitations currently in the AI space.

2. **USPTO Provisional Patent Application** — clear, well technically documented specification, demonstrating novelty + specific problems solved + implementation of multiple concepts / technologies in unique novel ways.

3. **Patent Assignment Agreement (template)** — for the future case where IP is transferred (acquisition, spin-off, asset purchase). Includes future-liability waiver + no-future-support clause + indemnification shift to assignee.

---

## The novel-combination claim — the heart of the patent

The operator is the **progenitor / inventor of the OVERALL multi-module AI ecosystem**, not just any single module. The patent should claim:

- **Each individual technique** (where novel)
- **And especially the novel combination** of these techniques into a coherent integrated system

This combination claim is what survives even when individual modules are open-sourced.

### The five claim areas operator selected (with operator emphasis flagged)

1. **Memory orchestration hierarchy** — HONEY ↔ NECTAR ↔ pollen ↔ forensics with mechanical promotion gates. Hierarchical memory with formal verification gates between layers. ⭐ **OPERATOR EMPHASIS** — explicitly called out as load-bearing.

2. **Stigmergic agent coordination via filesystem manifests** — no message-passing; w3w mission addressing (3 atomic dotted terms); compass bearings (N/S/E/W) for inter-mission edges; flat-folder filename grammar enabling O(1) frontier-scan lookup; agents discover each other via shared substrate, not via orchestrator/router.

3. **Four-shields enforcement (🛡 structural / 🧠 cognitive / ⛓ reactive / 🪞 recovery)** — cheaper-earlier discipline stack applied to AI safety + integrity. Each shield is cheaper to deploy than the next; together they form a biological-immune-system-style defense. Prevents drift propagation by closing structural gaps before reactive whack-a-mole.

4. **Shape-registry mechanical verdict classification** — count-based shapes with `target_direction` drive mechanical good/bad classification. No LLM judgement in the verdict path. Quality signal is integer-comparable across sessions; enables genetic-algorithm-style improvement loops.

5. **Membench-related quality measurement substrate** — quality probes ARE shapes; mechanical eval substrate that ties memory architecture to measurable quality outputs. ⭐ **OPERATOR EMPHASIS** — explicitly added beyond the four core claims, emphasizing **memory as architecture** rather than memory as feature.

6. **The overall-system claim** — the novel combination of (1)–(5) into a single coherent AI orchestration ecosystem.

---

## ELA design intent (operator's stated requirements)

- **Indemnification direction:** REVERSE — licensee indemnifies licensor (not the other way around)
- **Warranty posture:** AS-IS, no warranties — including explicit no-warranty against AI hallucination outputs
- **Liability cap:** 12-month-paid-fees ceiling
- **IP retention:** licensor retains all patent + IP rights for the overall system; license grants licensee right to **modify + customize + resell their own versions** of the licensed product
- **Due-diligence language:** company has done reasonable due-diligence to ensure no obvious or serious harm will come from using or modifying the product
  - ⚠️ This language must be drafted carefully — not too strong a guarantee (creates liability), not too weak a disclaimer (looks reckless)
- **Progenitor assertion:** contract language explicitly establishes company as progenitor / ancestor / inventor of the overall larger system using a unique novel combination of techniques solving specific common problems in the AI space
- **Open-source compatibility:** even if specific modules / subproducts / repositories are open-sourced, company retains patent + associated IP rights for the overall larger system design

## OSS boundary

**Strategy chosen:** Core engine proprietary, everything else open-source. (Option 1 in the interview.)

- **Closed (proprietary, patent-protected):** orchestration kernel + memory pipeline = the patentable core
- **Open (community-building + adoption):** skills + agents + hooks + vault patterns
- **Enterprise license sells access to the kernel** — open-source pieces remain freely available

**Module disposition matrix:** TODO in polished pass — needs concrete per-module enumeration so the patent's novel-combination claim covers the IP boundary cleanly.

---

## Patent Assignment Agreement design intent

For the future case where IP transfers (acquisition, spin-off, asset purchase):

- **Future Liability Waiver:** explicit Release-and-Waiver clause; Assignee assumes all future liabilities + indemnifies Assignor
- **No-future-support clause:** Assignor has no obligation to provide future updates / bug fixes / security patches / technical support; tech transferred AS-IS in current state
- **USPTO recordation:** any actual transfer recorded via USPTO Assignment Center

---

## 🔐 Regulatory compliance + data sovereignty architecture (CRITICAL ADDITION 2026-05-23)

> **This is the architectural pattern that makes regulatory compliance tractable. It is ALSO a 7th patent novelty claim — the "Zero-Knowledge Customer-Key-Custody Architecture for AI Services in Regulated Industries". Polished-deliverables agent must incorporate this into BOTH the patent spec AND the ELA AND add a new compliance recitals section.**

### The architectural pattern (the "we don't hold the keys" property)

When a customer pays:
1. The system **provisions a Backblaze B2 bucket for customer use** (per-customer isolation; customer-scoped storage namespace)
2. The system **issues a decryption keypair AND a signing keypair directly to the customer's email** at payment time
3. **The vendor (our company) NEVER retains a copy of either private key.** Keys are generated server-side, delivered to customer, and erased from vendor-side memory
4. All customer data is encrypted with the customer's public key before storage in their B2 bucket
5. All customer data is signed with the customer's signing key for forensic chain-of-custody integrity

**Functional effect:**
- Vendor **cannot decrypt customer data** even if compelled by court order, breach, or insider threat
- Vendor **cannot impersonate customer signatures** for any forensic record
- **Customer is the canonical data controller** in every regulatory sense; vendor is at most a technical operator of the encrypted-at-rest storage

This is **data sovereignty by architecture, not by policy**.

### GDPR (EU General Data Protection Regulation) implications

| GDPR Concept | Our Architecture | Compliance Status |
|---|---|---|
| **Data Controller (Art. 4(7))** | The CUSTOMER is the controller — they hold the keys, decide what's encrypted, control the bucket | Customer holds controller role |
| **Data Processor (Art. 4(8))** | Vendor processes ciphertext only — never plaintext PII | Vendor is at most a processor with technical inability to access |
| **Security of Processing (Art. 32)** | Encryption at rest with customer-managed keys = strongest possible measure | ✅ Strong |
| **Right to Erasure (Art. 17)** | Customer controls deletion — vendor has no way to read content; customer can revoke bucket access + destroy their keys = data unrecoverable | ✅ Customer-self-served erasure |
| **Right of Access (Art. 15)** | Customer has direct access; vendor cannot provide content even if requested (no keys) | ✅ Customer-self-served access |
| **Data Portability (Art. 20)** | Customer can extract their ciphertext + use their keys to decrypt → fully portable | ✅ Customer-self-served portability |
| **Records of Processing (Art. 30)** | Vendor maintains processing logs (which buckets exist, which customers, when provisioned) but NO content logs | ✅ Maintained without exposing PII |
| **Breach Notification (Art. 33-34)** | Encrypted-at-rest data with customer-held keys = breach notification thresholds dramatically reduced (ciphertext exposure ≠ data breach in most analyses) | ✅ Substantially de-risked |

**Open question:** Does the per-customer B2 bucket cross EU borders (B2 is US-based)? If EU customer data physically resides on US infrastructure, need to address via **Standard Contractual Clauses (SCC)** or alternative transfer mechanism in the ELA.

### HIPAA (US Health Insurance Portability and Accountability Act) implications

| HIPAA Concept | Our Architecture | Compliance Status |
|---|---|---|
| **Covered Entity** | Customer (healthcare provider, plan, or clearinghouse) | Customer holds covered-entity role |
| **Business Associate** | Vendor handles PHI on behalf of CE → likely BA in formal sense | Likely BAA required for formal compliance |
| **Conduit Exception** | The vendor's role is closer to a CONDUIT (like a phone carrier transmitting calls) — vendor stores ciphertext, has no access to PHI content | Conduit exception may apply (but case-by-case; conservative path is BAA) |
| **Security Rule § 164.312(a)(2)(iv) — Encryption** | Customer-managed encryption at rest = strong addressable safeguard | ✅ Strong |
| **Breach Notification Rule (§ 164.402)** | Encrypted PHI under HHS guidance = "unreadable, unusable, or indecipherable" → exempt from breach notification | ✅ De-risked (with proper guidance compliance) |
| **Minimum Necessary Rule (§ 164.502(b))** | Vendor sees nothing → trivially minimum-necessary | ✅ Architecturally enforced |
| **Audit Controls (§ 164.312(b))** | Vendor maintains access logs (bucket creation, key delivery events) without content | ✅ Maintained |
| **Retention (45 CFR § 164.530(j))** | **6 years** for HIPAA-required documentation | Customer responsibility primarily; vendor retains provisioning/billing records |

**Open question:** Even with zero-knowledge architecture, a BAA is conventionally signed. The polished-deliverables ELA should include a **BAA template addendum** that healthcare customers can attach when needed.

### PHIPA (Ontario Personal Health Information Protection Act, 2004) implications

| PHIPA Concept | Our Architecture | Compliance Status |
|---|---|---|
| **Health Information Custodian (HIC, s. 3)** | Customer (provider, hospital, etc.) | Customer holds custodian role |
| **Agent of a Custodian (s. 2)** | Vendor as agent processing on behalf of custodian | Vendor is agent with technical inability to access |
| **Reasonable Steps to Protect (s. 12)** | Customer-managed encryption at rest = reasonable steps in any modern analysis | ✅ Strong |
| **Retention Periods (Regulation 329/04, s. 13)** | **10 years** for adult health records (longer for minors — until age of majority + 10 yrs) | Customer responsibility primarily |
| **Right of Access (Part V)** | Customer-self-served (vendor cannot provide) | ✅ Architecturally provided |
| **Information Practices Statement (s. 16)** | Customer publishes; vendor's role is documented as "encrypted-at-rest agent with no access" | Documented in ELA |
| **Breach Notification (s. 12.3, IPC guidelines)** | Encrypted ciphertext breach has dramatically reduced notification obligations | ✅ De-risked |

### North American Documentation Retention Periods (summary)

| Jurisdiction / Regulation | Period | Source |
|---|---|---|
| **HIPAA** (US — covered entities) | 6 years from creation OR last effective date | 45 CFR § 164.530(j) |
| **HIPAA** (US — BA documentation) | 6 years (same as CE) | 45 CFR § 164.530(j) by reference |
| **PHIPA** (Ontario — adult HIC records) | 10 years after the last transaction or interaction | Reg. 329/04, s. 13 |
| **PHIPA** (Ontario — records of minors) | Until age of majority + 10 years | Reg. 329/04, s. 13 |
| **PIPEDA** (Canada federal — personal info) | No fixed period — principle of "no longer than necessary" + retention schedule documented | PIPEDA Principle 4.5 |
| **CCPA** (California — personal info) | No fixed period — but disclosure obligations on retention practices | Cal. Civ. Code § 1798.130 |
| **General US business records (IRS, tax)** | 7 years (tax records) | IRC § 6501 + business custom |
| **Quebec Law 25** | "As long as serves the purposes... or required by law" | Act respecting the protection of personal information |

⚠️ **The polished-deliverables agent must verify each of these with WebFetch to authoritative sources (HHS.gov, Ontario.ca, Justice Laws Website Canada, IRS.gov) before printing in the patent + ELA.**

### Implications for the patent claims

**ADD a 7th claim to the patent spec:**

```
Claim 7: Zero-Knowledge Customer-Key-Custody Architecture for AI Services
  in Regulated Industries

  - Per-customer cryptographic isolation via customer-controlled keys never
    retained by the vendor
  - Customer-managed encryption at rest with vendor-provisioned storage
  - Cryptographic separation of vendor-side technical operation from
    customer-side data controllership
  - Compliance posture by architectural construction rather than by
    organizational policy
  - Specific application to multi-tenant AI systems handling PII, PHI, or
    other regulated information

  Technical effect:
  - Eliminates vendor-side data breach exposure (vendor cannot leak what
    it cannot read)
  - Reduces regulatory compliance burden (vendor's technical inability to
    access is stronger than any policy commitment)
  - Enables single SaaS deployment to serve HIPAA, PHIPA, GDPR customers
    simultaneously without per-jurisdiction infrastructure
```

This is a substantial novelty claim and synergizes with the orchestration architecture — together they form a coherent "compliance-by-construction" AI orchestration ecosystem.

### Implications for the ELA

**ADD a "Regulatory Compliance Recitals" section** with:

1. **Data Sovereignty Recital** — "Licensee is the sole and exclusive controller of all data stored in the customer-provisioned B2 bucket. Licensor neither holds nor has direct access to any cryptographic keys required to decrypt or modify said data. Customer is the canonical data controller for purposes of GDPR Article 4(7), HIPAA Privacy Rule, PHIPA, and analogous jurisdictional frameworks."

2. **Cryptographic Key Custody Recital** — "Upon contract activation, Licensor provisions a dedicated Backblaze B2 bucket for Licensee's use, and issues a decryption keypair and signing keypair to Licensee's designated email address. Licensor does not retain copies of the private keys after delivery and has no technical ability to access encrypted customer content thereafter."

3. **Conduit-Style Operator Recital** — "Licensor's role is analogous to a conduit (cf. HIPAA Conduit Exception, 45 CFR § 164.502 commentary): Licensor provides encrypted-at-rest storage and signed-data integrity verification but has no access to plaintext customer content."

4. **BAA Template Addendum** — For healthcare customers requiring formal Business Associate Agreement coverage, attach the BAA template addendum. The BAA does NOT modify Licensor's technical inability to access PHI — it formalizes the relationship for HIPAA reporting purposes.

5. **Data Processing Addendum (DPA)** — For EU/UK customers under GDPR. Standard Contractual Clauses (SCC) for international transfers (if customer data crosses EU borders to B2 US infrastructure).

6. **Records Retention Schedule** — Recital documenting that LICENSEE controls retention of customer data per applicable jurisdiction; Licensor's role is technical storage operation only.

### Implications for the brain-dump / planning

Open question added: **B2 bucket regional residency strategy**. If EU customer data MUST stay in EU per GDPR, vendor needs:
- B2's EU region option (B2 has EU buckets in `eu-central-003`) — provision per-customer in customer's required region
- OR alternative storage backends with sovereign regions
- OR SCC-based cross-border transfer with customer informed consent

This is a tactical follow-up charter to the expedition, not solved here.

---

## Open questions (for polished pass + operator follow-up)

- Co-founder / co-inventor name + identity for filing
- Company entity legal name + state of incorporation
- First enterprise customer name + industry + deal size class (informs ELA jurisdiction + scope)
- Per-module OSS-vs-proprietary disposition matrix
- Patent attorney engagement timing + budget (must engage before 12-month non-provisional conversion)
- Jurisdiction strategy (US-only first vs PCT international filing)
- Existing prior art operator is aware of (helps inventor draft novelty narrative defensively)
- Timeline for first enterprise contract signature
- Whether the overall-system patent should also cover the **forensic-coc-v2** architecture (separate but coupled charter `forensic-coc-v2-rekor`)

---

## ⬇️ LUMO AI Research — verbatim capture (NOT verified)

> The following is LUMO's research output as provided by the operator. It is captured here AS-IS, without URL verification or hallucination check. The polished-deliverables spawn must triple-fact-check every URL printed below via WebFetch and replace any dead/hallucinated references.

### LUMO Part 1: Successful Provisional Patent Examples

LUMO cited the following as case studies of provisional-originated patents:

- **Apple Multi-Touch Interface** — U.S. Patent No. 7,469,381; key was specific multi-touch gesture descriptions (pinch-to-zoom, scrolling mechanics) distinguishing from single-touch prior art
- **Amazon 1-Click Ordering** — U.S. Patent No. 5,960,411; key was precise method description (stored payment/shipping info linked to single-action button)
- **Google PageRank** — early provisional described algorithmic link-analysis ranking; mathematical/logical description of link-weight concept was the novelty
- **Tesla EV Powertrain** — provisionals covered high-efficiency motor designs + battery management; detailed engineering diagrams + specific circuit descriptions established priority

**LUMO's claim:** in all these cases, success = high-quality written description in provisional was detailed enough to support broader claims later filed in non-provisional. ⚠️ Polished-deliverables spawn should fact-check these patent numbers + verify the "originated from provisional" claim for each.

### LUMO Part 2: Free Official Templates & Forms

**Form SB/16** — USPTO Provisional Application for Patent Cover Sheet (mandatory). LUMO claims URL: `https://www.uspto.gov/sites/default/files/documents/sb0016.pdf` ⚠️ VERIFY.

**Recommended Specification Structure (LUMO):**
1. Title (clear + technical, 2–7 words)
2. Cross-Reference to Related Applications (optional)
3. Background of the Invention
4. Summary of the Invention
5. Brief Description of Drawings (note: drawings not strictly required if text enables; highly recommended for mechanical/electrical)
6. Detailed Description of the Invention (the core "Novelty Document")
7. (Optional) claims — formal claims NOT required in provisional, but describing as-if-claiming is good practice

**Critical rule (LUMO):** cannot add new matter later — what's in the provisional is the priority date ceiling.

### LUMO Part 3: Submission

- Combine Cover Sheet + Specification into a single PDF (or separate files via EFS-Web)
- File online via **USPTO Patent Center** (formerly EFS-Web)
- File-by-mail option: Commissioner for Patents, P.O. Box 1450, Alexandria, VA 22313-1450
- **Micro entity fee:** ~$70-$150 (verify current rates)
- **Small entity fee:** roughly double micro

### LUMO Part 4: Critical advice

- **Enablement is king** — a skilled engineer must be able to build the invention from the description alone
- **Drawings matter** — even simple sketches help
- **Timing** — 12 months from provisional to non-provisional; miss = lose priority date

### LUMO Part 5: USPTO eligibility for software/AI patents

LUMO cites the **August 2025 USPTO Guidance** as clearer path if invention is framed as "technical improvement" not "abstract idea":

- Don't say: "A system that remembers things better for AI" (abstract)
- Do say: "A distributed memory orchestration layer that dynamically allocates vector database shards based on real-time inference latency thresholds, reducing context-switching overhead by 40%" (concrete technical improvement)

**Key sections LUMO recommends for our provisional:**
1. **The Problem (Symptoms)** — describe specific technical failures in current AI systems (context window overflow, hallucination due to stale memory retrieval, latency spikes during multi-agent handoffs)
2. **The Solution (Orchestration Logic)** — architecture diagram, algorithm, data structures
3. **The "Technical Effect"** — explicitly state how this improves the computer (RAM reduction %, token-generation speed Y%)

**Critical tip (LUMO):** under 2025 guidance, tie AI steps to hardware or high-level runtime interactions (accessing specific memory buffer, modifying cache pointer) — prevents "abstract idea" rejection.

### LUMO Part 6: The "Unique Combination" defense

For combining existing technologies (AI + Memory + Orchestration), novelty lies in the **synergy**. Don't list components — describe the interaction:

> "A system comprising [Component A] and [Component B], wherein [Component A] modifies the input parameters of [Component B] in real-time based on [Specific Metric], resulting in [Technical Outcome]."

### LUMO Part 7: ELA Boilerplate — VERBATIM with clauses highlighted

> **Captured verbatim from LUMO's research. Highlighted clauses are the load-bearing ones operator must preserve in any drafted ELA. Polished-deliverables agent should refine wording for swarmy-specific context but MUST keep the highlighted protection patterns intact.**

```
SECTION X: DISCLAIMER OF WARRANTIES AND LIMITATION OF LIABILITY

X.1 "As-Is" Basis.   ⭐ LOAD-BEARING — the foundational disclaimer
    THE SOFTWARE, INCLUDING ALL MEMORY ORCHESTRATION LOGIC, RUNTIME
    ENVIRONMENTS, AND MATHEMATICAL FORMULAS, IS PROVIDED "AS IS" AND
    "AS AVAILABLE," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-
    INFRINGEMENT, AND ANY WARRANTIES ARISING FROM COURSE OF DEALING
    OR USAGE OF TRADE. LICENSOR DOES NOT WARRANT THAT THE SOFTWARE
    WILL BE UNINTERRUPTED, ERROR-FREE, OR FREE FROM SECURITY
    VULNERABILITIES, OR THAT THE AI OUTPUTS GENERATED WILL BE
    ACCURATE, LEGAL, OR SAFE FOR ANY SPECIFIC USE CASE.

X.2 Limitation of Liability.   ⭐ LOAD-BEARING — the indirect-damages shield
    IN NO EVENT SHALL LICENSOR, ITS AFFILIATES, OR ITS LICENSORS BE
    LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR
    PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS,
    DATA, USE, GOODWILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM
    (A) YOUR ACCESS TO OR USE OF OR INABILITY TO ACCESS OR USE THE
    SOFTWARE; (B) ANY CONDUCT OR CONTENT OF ANY THIRD PARTY ON THE
    SOFTWARE; (C) ANY CONTENT OBTAINED FROM THE SOFTWARE; AND (D)
    UNAUTHORIZED ACCESS, USE, OR ALTERATION OF YOUR TRANSMISSIONS OR
    CONTENT, WHETHER BASED ON WARRANTY, CONTRACT, TORT (INCLUDING
    NEGLIGENCE), OR ANY OTHER LEGAL THEORY, EVEN IF LICENSOR HAS BEEN
    ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

X.3 Cap on Liability.   ⭐ LOAD-BEARING — the financial ceiling
    LICENSOR'S TOTAL AGGREGATE LIABILITY FOR ANY CLAIMS ARISING UNDER
    THIS AGREEMENT SHALL NOT EXCEED THE TOTAL AMOUNT PAID BY LICENSEE
    TO LICENSOR IN THE TWELVE (12) MONTHS PRECEDING THE EVENT GIVING
    RISE TO THE CLAIM.

X.4 No Liability for AI Outputs.   ⭐ LOAD-BEARING — the AI-specific carve-out
    LICENSEE ACKNOWLEDGES THAT THE SOFTWARE UTILIZES ARTIFICIAL
    INTELLIGENCE AND MAY GENERATE OUTPUTS THAT ARE INACCURATE,
    OFFENSIVE, OR IN VIOLATION OF THIRD-PARTY RIGHTS. LICENSOR ASSUMES
    NO RESPONSIBILITY FOR ANY SUCH OUTPUTS OR ANY DAMAGES ARISING FROM
    LICENSEE'S RELIANCE UPON THEM. LICENSEE SOLELY BEARS THE RISK OF
    DEPLOYMENT AND USE.
```

**Additional clauses operator wants added in polished pass (not in LUMO):**

- **Reverse Indemnification** — Licensee indemnifies Licensor against third-party claims arising from licensee's use, customization, third-party data integration, or deployment errors
- **License to Customize + Resell** — explicit grant: Licensee may modify + customize + resell their own versions of the licensed product, subject to retained patent + IP rights
- **Due-Diligence Affirmation** — Licensor has performed reasonable due-diligence to ensure no obvious or serious harm will come from using the product (carefully scoped, not over-promising)
- **Progenitor Assertion** — explicit recital that Licensor is the progenitor / ancestor / inventor of the overall larger system, with novel-combination claim retained even when individual modules are open-sourced
- **OSS Compatibility Recital** — even when modules are open-sourced, the overall-system patent + IP rights remain with Licensor

### LUMO Part 8: Patent Assignment Agreement Boilerplate — VERBATIM with clauses highlighted

> **Captured verbatim from LUMO. Highlighted clauses are the load-bearing ones for the future-IP-transfer scenario. Polished-deliverables agent refines wording but MUST keep the protection patterns intact.**

```
SECTION Y: TRANSFER OF RIGHTS AND RELEASE OF LIABILITY

Y.1 Assignment.   ⭐ LOAD-BEARING — the actual IP transfer
    ASSIGNOR hereby assigns, transfers, and conveys to ASSIGNEE all
    right, title, and interest in and to the Patent Application/Patent
    identified in Exhibit A (the "Assigned Rights"), including all
    rights to sue for past, present, and future infringements.

Y.2 Assumption of Liabilities.   ⭐ LOAD-BEARING — assignee takes ALL liability going forward
    EFFECTIVE AS OF THE CLOSING DATE, ASSIGNEE HEREBY ASSUMES ALL
    LIABILITIES, OBLIGATIONS, AND RISKS ASSOCIATED WITH THE OPERATION,
    MAINTENANCE, SUPPORT, AND FUTURE USE OF THE ASSIGNED TECHNOLOGY.
    ASSIGNEE AGREES TO INDEMNIFY, DEFEND, AND HOLD HARMLESS ASSIGNOR
    FROM ANY AND ALL CLAIMS, DEMANDS, LOSSES, DAMAGES, OR EXPENSES
    (INCLUDING ATTORNEYS' FEES) ARISING OUT OF OR RELATED TO THE
    ASSIGNED TECHNOLOGY AFTER THE CLOSING DATE.

Y.3 Release and Waiver of Future Claims.   ⭐ LOAD-BEARING — the legal "shield"
    ASSIGNOR AND ASSIGNEE MUTUALLY AGREE THAT, EXCEPT FOR BREACHES OF
    THIS AGREEMENT OCCURRING PRIOR TO THE CLOSING DATE, ASSIGNOR IS
    HEREBY RELEASED AND DISCHARGED FROM ANY AND ALL CLAIMS,
    LIABILITIES, OR OBLIGATIONS (KNOWN OR UNKNOWN) ARISING FROM THE
    FUTURE USE, MODIFICATION, DEPLOYMENT, OR COMMERCIALIZATION OF THE
    ASSIGNED TECHNOLOGY BY ASSIGNEE OR ITS SUCCESSORS. ASSIGNEE WAIVES
    ANY RIGHT TO ASSERT CLAIMS AGAINST ASSIGNOR REGARDING THE
    PERFORMANCE, SAFETY, OR LEGAL COMPLIANCE OF THE TECHNOLOGY POST-
    TRANSFER.

Y.4 No Future Support Obligation.   ⭐ LOAD-BEARING — no implied warranty of support
    ASSIGNOR HAS NO OBLIGATION TO PROVIDE FUTURE UPDATES, BUG FIXES,
    SECURITY PATCHES, OR TECHNICAL SUPPORT FOR THE ASSIGNED TECHNOLOGY.
    ASSIGNEE ACKNOWLEDGES THAT THE TECHNOLOGY IS TRANSFERRED IN ITS
    CURRENT STATE WITHOUT ANY FUTURE GUARANTEES.
```

**Legal caveats from LUMO (operator must internalize):**

- ⚠️ **Liability waivers are NOT magic shields.** Courts will often void liability waivers for: (a) known defects sold knowingly, (b) fraud, (c) past negligence
- ⚠️ **Forward-only waiver works; backward waiver often fails.** You generally can waive liability for FUTURE operations but not PAST ones
- ⚠️ **Operator usually liable, not developer.** If the AI violates laws (e.g., generates CSAM, violates privacy), the OPERATOR is usually liable, but regulators MIGHT still investigate the developer if the tool was designed for illegal use — Terms-of-Use must explicitly prohibit illegal use

### LUMO Part 9 (additional research reference): share.note.sx encrypted note

Operator shared additional research via encrypted note at:

```
https://share.note.sx/xyjlsmzd#yOf7fYmiC6qLhW4kHDi3uPpst9+YRt2pnEfWJ32FnTo
```

⚠️ **share.note.sx uses client-side encryption** — the fragment after `#` is the decryption key. A plain HTTP GET will only retrieve the encrypted blob; decryption happens in the browser. The polished-deliverables agent should:
1. WebFetch the URL — if the response is the encrypted blob (which it likely will be), flag this in OPEN-QUESTIONS.md
2. Best fallback: operator copies-paste decrypted content from a browser visit, OR the agent uses a share.note.sx-aware fetcher if available
3. If decryption isn't available to the agent, note that this is a known limitation; operator will provide the decrypted content in a follow-up

### LUMO Part 9: Vancouver Bibliography (LUMO-claimed)

⚠️ **EVERY URL BELOW MUST BE VERIFIED by the polished-deliverables spawn via WebFetch. Mark VERIFIED / DEAD / HALLUCINATED next to each.**

1. **USPTO Provisional Cover Sheet SB/16** — `https://www.uspto.gov/sites/default/files/documents/sb0016.pdf`
2. **deftio Provisional Patent Template** — `https://github.com/deftio/provisional-patent-template`
3. **Git.Law Free EULA Template** — `https://git.law/templates/doc/free-end-user-license-agreement-template-your-essential-eula-resource-AoyrQ3`
4. **USPTO Assignment Center** — `https://assignmentcenter.uspto.gov`
5. **GitHub Customer Agreement** — `https://assets.ctfassets.net/8aevphvgewt8/luAPHjODK4vAYIpwisJfC/88a1961a9c7fcbb8d02a86d5d4635295/GCA_-_2025_03_-_GitHub_Customer_Agreement_General_Terms_-_FINAL_locked.pdf`
6. **USPTO Subject-Matter Eligibility (August 2025 memo)** — `https://www.uspto.gov/patents/apply/patent-eligibility`
7. **Martensen IP commentary on 2025 USPTO memo** — `https://www.martensenip.com/blog/2025/october/uspto-memo-2025-brings-breakthrough-for-software`

### LUMO Part 10: Mermaid Diagrams (LUMO drafts)

LUMO provided two Mermaid diagrams that should be refined in the polished pass:

- **Diagram A:** High-Level Architecture Flow — VPS environment → Custom Runtime Layer → Memory Orchestration Engine → Mathematical Formula Engine → Disk I/O Scheduler → Virtual Disk → AI Inference Engine
- **Diagram B:** "Math-to-Action" Loop — sequence diagram showing how the formula (`Score = (Freq * Recency) / Time`) drives the physical disk write (proves it's not just abstract idea per USPTO guidance)

⚠️ Polished spawn should: (a) verify Mermaid renders cleanly; (b) adapt the diagrams to swarmy's ACTUAL architecture (HONEY/NECTAR/pollen/forensics + manifest hooks + shape registry), not LUMO's generic stand-in.

---

## What the polished-deliverables agent must produce

Per operator's directive: "fully polished, cited and triple-fact-checked for hallucinations on all urls printed in vancouver bibliography style at end".

**Output set** (lands in `./polished-deliverables/`):

1. `PATENT-PROVISIONAL-SPECIFICATION.md` — the technical novelty document, structured per USPTO recommended sections, adapted to swarmy's ACTUAL architecture (not LUMO's stand-in), demonstrating "technical improvement" framing per 2025 USPTO guidance. Includes refined Mermaid diagrams.

2. `ELA-DRAFT.md` — Enterprise License Agreement boilerplate with the reverse-indemnification + as-is + liability cap + IP retention + due-diligence + progenitor-assertion language. Marked DRAFT for attorney review.

3. `ASSIGNMENT-AGREEMENT-DRAFT.md` — Patent Assignment Agreement template with the future-liability waiver + no-future-support + indemnification-shift language. Marked DRAFT for attorney review.

4. `BIBLIOGRAPHY-VERIFIED.md` — Vancouver-style bibliography with EVERY URL marked ✅ VERIFIED (responded with expected content) / ❌ DEAD (URL doesn't resolve) / ⚠️ HALLUCINATED (URL resolves but content doesn't match claim). Replacement URLs provided where LUMO's were dead/hallucinated. Each entry includes WebFetch evidence of verification (status code + first 200 chars of response).

5. `OPEN-QUESTIONS.md` — Questions surfaced during the polished pass that operator must answer before USPTO filing or attorney engagement.

**Hard requirements:**
- Triple-fact-check ALL URLs via WebFetch before printing them in any bibliography
- Use Vancouver style (numbered, journal-citation format)
- Mark all legal language as DRAFT — operator engages attorney for review before any USPTO filing or signature
- Adapt LUMO's generic templates to swarmy's ACTUAL system (don't ship LUMO's stand-in language as final)
- If a LUMO claim cannot be verified, flag it and provide the closest verified alternative
