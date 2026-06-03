# Claim 7: Zero-Knowledge Customer-Key-Custody Architecture for AI Services in Regulated Industries

> **Standalone section for insertion into the USPTO Provisional Patent Application.**
> When PATENT-PROVISIONAL-SPECIFICATION.md is finalized, this document folds in as:
> (a) the formal Claim 7 language in the Claims section, and
> (b) the corresponding sub-section in the Detailed Description of the Invention.
> This file is self-contained for independent attorney review.

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a privacy + compliance attorney before any USPTO filing,
contract signature, or customer-facing publication.
Jurisdiction-specific requirements may differ.

---

## Part A: Formal Claim Language (USPTO Claim 7)

### Claim 7

A computer-implemented system for providing zero-knowledge customer-key-custody in a multi-tenant artificial intelligence service platform for regulated industries, the system comprising:

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

---

### Claim 7a (Dependent — Multi-Region Residency)

The system of Claim 7, wherein the customer-scoped storage namespace provisioned in step (a) is allocated in a geographic region selected based on the customer's declared jurisdiction of data residency, including at least one European Union-sovereign storage region, such that customer data subject to GDPR data-residency requirements may be stored without cross-border transfer to non-EU infrastructure; and wherein, when cross-border transfer is required, Commission Implementing Decision (EU) 2021/914 Standard Contractual Clauses are applicable as the transfer mechanism.

---

### Claim 7b (Dependent — Breach Notification Safe Harbor)

The system of Claim 7, wherein, in the event of unauthorized access to the customer-scoped storage namespace, the exclusively ciphertext-form stored data satisfies the definition of protected health information rendered "unreadable, unusable, or indecipherable" under HHS guidance implementing 45 CFR § 164.402(2), thereby qualifying the applicable party for the breach notification safe harbor under 45 CFR Part 164 Subpart D with respect to such ciphertext data where the encryption key has not been compromised.

---

### Claim 7c (Dependent — Integration with AI Orchestration)

The system of Claim 7, operating as a data custody layer integrated with the multi-agent AI memory orchestration system of Claims 1 through 6, wherein memory artifacts produced by the orchestration system of Claims 1-6 are stored exclusively via the encryption-at-rest module of Claim 7(d), and forensic chain-of-custody records are signed via the data signing module of Claim 7(e), such that the combined system provides both AI orchestration functionality and zero-knowledge compliance posture as a single integrated architecture.

---

## Part B: Detailed Description Sub-Section

### 7. Zero-Knowledge Customer-Key-Custody Architecture

#### 7.1 Technical Problem Addressed

Conventional multi-tenant AI services require vendor-side access to customer data in order to perform AI inference, memory retrieval, and storage operations. This structural requirement creates the following technical problems:

(i) A single vendor-side security breach exposes all customers' plaintext data simultaneously, creating correlated data loss risk at scale.

(ii) Under GDPR Article 4(7), a vendor with operational access to customer data content becomes at minimum a co-controller, creating joint regulatory liability that scales with each jurisdiction's enforcement posture.

(iii) Under HIPAA 45 CFR Part 164, a vendor maintaining PHI on behalf of covered entities is classified as a Business Associate (confirmed by HHS FAQ 2076, which clarifies this applies even when the CSP stores only encrypted ePHI and lacks the decryption key), requiring formal BAA execution with each healthcare customer.

(iv) Data-residency requirements (GDPR Art. 46, PHIPA) create per-jurisdiction infrastructure complexity when the vendor's AI processing infrastructure is centralized.

(v) Insider threats, compelled legal disclosure (subpoenas, court orders), and regulatory investigations create unavoidable access vectors that cannot be addressed by policy-layer commitments alone.

Prior art policy-layer solutions — contractual commitments, data processing agreements, organizational access policies — are inherently weaker than technical solutions because they depend on human compliance, ongoing enforcement, and third-party auditing. The disclosed system addresses these problems at the architectural level.

#### 7.2 Technical Solution

The disclosed system achieves data sovereignty by architectural construction through the following technically-specified sequence:

**Step 1 — Isolated Namespace Provisioning**
Upon payment transaction completion, the system provisions an isolated customer-scoped object storage namespace (reference implementation: Backblaze B2 bucket in region selected per customer jurisdiction). Each customer receives a dedicated namespace with independent access credentials, cryptographically isolated from all other customer namespaces.

**Step 2 — Ephemeral Server-Side Keypair Generation**
The system generates two cryptographic keypairs in server-side volatile memory, without persisting private components to any durable storage:
- Encryption keypair (e.g., RSA-4096, X25519, or post-quantum equivalent): public key retained by vendor for encrypt-before-write operations; private key delivered to customer.
- Signing keypair (e.g., Ed25519): public key retained by vendor for signature verification; private key delivered to customer.

**Step 3 — Zero-Retention Private Key Delivery and Erasure**
Both private keys are transmitted via encrypted transport (TLS) to the customer's designated email address. Upon confirmed delivery (or within a defined delivery confirmation window), the vendor's in-memory copies of both private keys are irrevocably overwritten using a cryptographic erasure procedure. After completion, the vendor holds no copy of either private key in any storage medium — volatile, persistent, or backup.

**Step 4 — Encrypt-Before-Write**
All customer content submitted for storage is encrypted using the customer's public encryption key before any write to durable storage. The vendor's storage infrastructure at no point contains plaintext customer content. All stored objects are ciphertext blobs from the vendor's operational perspective.

**Step 5 — Sign-All-Records**
Customer-supplied signing keys (provided at write time by authenticated customer sessions) are used to produce cryptographic signatures over stored records. These signatures constitute a chain-of-custody attestation enabling tamper detection and forensic audit.

#### 7.3 Technical Effects

**Architectural Breach Isolation:** Vendor infrastructure breach exposes only computationally infeasible ciphertext. Vendor cannot leak what it cannot read. This is a technical property, not a contractual claim.

**GDPR Controller/Processor Separation:** Customer holds exclusive key custody and thereby determines the means and purposes of data content processing per GDPR Art. 4(7). Vendor processes only ciphertext, placing vendor in processor role per Art. 4(8). This structural separation reduces vendor regulatory exposure compared to conventional multi-tenant architectures.

**HIPAA Encryption Safe Harbor:** Ciphertext-only storage satisfies 45 CFR § 164.402(2) technical standards for rendering ePHI "unreadable, unusable, or indecipherable" — the basis for breach notification safe harbor — provided the encryption key is not separately compromised. Note: HHS FAQ 2076 confirms a no-key CSP is still a Business Associate; BAA execution remains required for formal HIPAA compliance, but the encrypted architecture substantially reduces breach notification obligations.

**Cross-Jurisdictional Compliance by Single Deployment:** The architecture's compliance posture is jurisdiction-agnostic because it derives from technical properties (key custody, ciphertext-only storage) rather than per-jurisdiction policy reconfiguration. A single deployment simultaneously serves GDPR, HIPAA, PHIPA, CCPA, PIPEDA, and Quebec Law 25 customers.

**Right-to-Erasure by Key Destruction:** A customer destroys their private key, rendering all stored ciphertext permanently and irrecoverably inaccessible. This is a technically complete implementation of GDPR Art. 17 Right to Erasure.

#### 7.4 Distinction from Prior Art

Prior customer-managed encryption (CMK) and Bring-Your-Own-Key (BYOK) implementations — including AWS KMS, Google Cloud KMS, Azure Key Vault, and HashiCorp Vault — differ from the disclosed system in the following material respects:

- In CMK/BYOK patterns, the vendor operates the key management infrastructure. The vendor's systems retain computational access to the keys, even if indirect. The disclosed system places private keys exclusively outside vendor infrastructure after the delivery-and-erasure step.

- CMK/BYOK requires customers to operate and maintain key management infrastructure. The disclosed system automates key generation and delivery at payment time, requiring zero pre-existing PKI infrastructure from the customer.

- CMK/BYOK is a general-purpose infrastructure pattern not integrated with AI orchestration pipelines. The disclosed system specifically integrates zero-knowledge custody as a layer in the multi-agent AI memory orchestration architecture of Claims 1-6, enabling compliance-by-construction within AI-mediated data workflows.

- The disclosed system combines payment-triggered provisioning, server-side zero-retention key generation, automated delivery, and AI pipeline integration into a novel unified architecture.

#### 7.5 Implementation Variations

The architecture is substrate-agnostic. The claimed inventive concept applies to any object storage backend (AWS S3, Google Cloud Storage, Azure Blob Storage, self-hosted MinIO, Cloudflare R2). It applies to any asymmetric keypair scheme meeting the zero-retention property. It applies to key delivery channels other than email (API-endpoint delivery, HSM provisioning, secure messaging) provided the vendor-side erasure property of Step 3 is preserved. The architecture applies to any multi-tenant AI service handling regulated data, not limited to the specific swarmy implementation.

---

## Part C: Prior Art Search Guidance (for patent attorney)

Recommended search areas before filing:

1. AWS KMS / Google Cloud KMS / Azure Key Vault — CMK/BYOK patterns (distinguished in §7.4)
2. "Client-side encryption" in cloud storage literature (S3 client-side encryption SDK, etc.)
3. HIPAA-compliant zero-knowledge cloud storage (e.g., Tresorit, SpiderOak architecture)
4. Zero-knowledge proof protocols (separate technical domain — these are mathematical verification protocols, not data custody architectures; confirm claim language clearly distinguishes)
5. "Convergent encryption" / "client-side key management" in distributed storage literature
6. US Patent 10,992,464 (Microsoft Azure confidential computing) and related portfolio

---

## Part D: Vancouver Bibliography

1. European Parliament and Council of the European Union. Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation). Off J Eur Union. 2016 Apr 27;L 119:1-88. Available from: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng **✅ VERIFIED** — confirmed EUR-Lex canonical publication, CELEX 32016R0679. Art. 4(7) controller and 4(8) processor definitions confirmed.

2. European Commission. Commission Implementing Decision (EU) 2021/914 of 4 June 2021 on standard contractual clauses for the transfer of personal data to third countries pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council. Off J Eur Union. 2021 Jun 7;L 199:31-61. Available from: https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj/eng **✅ VERIFIED** — confirmed EUR-Lex, OJ L 199, 7.6.2021, pp. 31-61; entered into force 27 June 2021.

3. US Department of Health and Human Services, Office for Civil Rights. FAQ 2076: If a CSP stores only encrypted ePHI and does not have a decryption key, is it a HIPAA business associate? [Internet]. Washington (DC): HHS; [cited 2026-05-23]. Available from: https://www.hhs.gov/hipaa/for-professionals/faq/2076/if-a-csp-stores-only-encrypted-ephi-and-does-not-have-a-decryption-key-is-it-a-hipaa-business-associate/index.html **✅ VERIFIED** — confirmed HHS.gov. Key finding: no-view CSP storing encrypted ePHI is still classified as a Business Associate under HIPAA.

4. US Government Publishing Office. 45 CFR § 164.402 — Definitions [Breach Notification Rule]. Electronic Code of Federal Regulations [Internet]. [cited 2026-05-23]. Available from: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-D **✅ VERIFIED** — eCFR.gov confirmed; encrypted PHI safe harbor provision confirmed via HHS Breach Notification Guidance.

5. Ontario. Personal Health Information Protection Act, 2004, SO 2004, c 3, Sch A; Ontario Regulation 329/04 (General), s. 13. e-Laws Ontario [Internet]. [cited 2026-05-23]. Available from: https://www.ontario.ca/laws/regulation/040329 **✅ VERIFIED** — ontario.ca/laws confirmed via search; s. 13 retention provisions (10 years adults; age of majority + 10 years minors) confirmed via CanLII cross-reference.
