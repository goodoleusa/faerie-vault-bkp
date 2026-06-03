# Business Associate Agreement — Template

> **Exhibit BAA-1 to the Enterprise License Agreement**
> Standalone template for healthcare (HIPAA) customers.

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a privacy + compliance attorney before any USPTO filing,
contract signature, or customer-facing publication.
Jurisdiction-specific requirements may differ.

---

## BUSINESS ASSOCIATE AGREEMENT

This Business Associate Agreement ("BAA" or "Agreement") is entered into as of the Effective Date specified below, by and between:

**COVERED ENTITY / BUSINESS ASSOCIATE ("CE/BA"):** [LICENSEE ENTITY NAME], a [State] [entity type], hereinafter "Covered Entity" (or "Business Associate" if Licensee is itself a BA of a Covered Entity).

**BUSINESS ASSOCIATE / SUB-BUSINESS ASSOCIATE ("BA"):** [LICENSOR ENTITY NAME], a [State] [entity type], holding an exclusive license from the joint individual inventors [INVENTOR 1 NAME] and [INVENTOR 2 NAME] and operating the licensed technology as a sublicensor to enterprise customers; hereinafter "Business Associate."

*(Note on entity structure: Per the patent filing structure, the patent is held by the two individual inventors. The entity signing this BAA operates under an exclusive license from those inventors. This structure should be confirmed with legal counsel before execution.)*

**Effective Date:** [DATE]

---

### RECITALS

A. Covered Entity is a "covered entity" as defined in 45 CFR § 160.103 (or is a Business Associate of a covered entity), and, in connection with its use of Business Associate's services, may disclose to Business Associate, or Business Associate may create, receive, maintain, or transmit on behalf of Covered Entity, Protected Health Information (PHI) as defined in 45 CFR § 160.103.

B. Business Associate's platform stores only encrypted PHI. Pursuant to HHS FAQ 2076, a Cloud Service Provider that stores encrypted ePHI without holding a decryption key is classified as a HIPAA Business Associate and must execute a BAA. Business Associate acknowledges this classification and enters into this Agreement to satisfy that requirement.

C. Business Associate's technology architecture provides zero-knowledge customer-key-custody: Business Associate generates cryptographic keypairs at provisioning, delivers private keys to Covered Entity, and irrevocably erases private keys from Business Associate's systems. Business Associate thereafter has no technical ability to access plaintext PHI. This BAA does not alter that technical architecture; it formalizes the regulatory relationship between the parties.

D. The parties desire to enter into this BAA to comply with the requirements of the HIPAA Privacy Rule (45 CFR Part 164 Subpart E), Security Rule (45 CFR Part 164 Subpart C), and Breach Notification Rule (45 CFR Part 164 Subpart D), as amended by the HITECH Act and the 2013 Omnibus Rule.

---

### ARTICLE 1 — DEFINITIONS

Capitalized terms used in this BAA have the meanings set forth in the HIPAA Rules (45 CFR Parts 160 and 164), unless otherwise defined herein.

1.1 "Protected Health Information" or "PHI" has the meaning set forth in 45 CFR § 160.103, including electronic PHI ("ePHI").

1.2 "HIPAA Rules" means the Privacy Rule, Security Rule, and Breach Notification Rule, collectively.

1.3 "Zero-Knowledge Architecture" means Business Associate's technical practice of: (a) generating cryptographic keypairs server-side at provisioning; (b) delivering private keys to Covered Entity at provisioning; (c) irrevocably erasing private keys from Business Associate's systems; and (d) storing only ciphertext PHI in Covered Entity's isolated storage namespace, such that Business Associate lacks the technical means to access plaintext PHI at any time after provisioning.

1.4 "Breach" has the meaning set forth in 45 CFR § 164.402.

1.5 "Unsecured PHI" has the meaning set forth in 45 CFR § 164.402. Under HHS guidance implementing 45 CFR § 164.402(2), PHI encrypted using NIST-validated processes and where the encryption key has not been compromised is "unreadable, unusable, or indecipherable" and constitutes a safe harbor from breach notification obligations.

---

### ARTICLE 2 — OBLIGATIONS OF BUSINESS ASSOCIATE

2.1 **Permitted Uses and Disclosures.** Business Associate shall not use or disclose PHI except: (a) as necessary to provide the services described in the Enterprise License Agreement; (b) as required by law; or (c) as otherwise permitted under this BAA.

2.2 **Safeguards.** Business Associate shall implement administrative, physical, and technical safeguards that reasonably and appropriately protect the confidentiality, integrity, and availability of ePHI it creates, receives, maintains, or transmits on behalf of Covered Entity, as required by 45 CFR Part 164, Subpart C (Security Rule).

2.3 **Zero-Knowledge Architecture as Safeguard.** The parties acknowledge that Business Associate's Zero-Knowledge Architecture provides a technical safeguard of the highest practical tier: ciphertext-only storage with customer-held keys. This architecture satisfies the "encryption" addressable implementation specification of 45 CFR § 164.312(a)(2)(iv) (encryption and decryption) and § 164.312(e)(2)(ii) (encryption in transit).

2.4 **Minimum Necessary.** Because Business Associate operates under the Zero-Knowledge Architecture and has no access to plaintext PHI, Business Associate trivially complies with the Minimum Necessary standard of 45 CFR § 164.502(b).

2.5 **Reporting.** Business Associate shall report to Covered Entity: (a) any use or disclosure of PHI not permitted under this BAA; (b) any Security Incident (as defined in 45 CFR § 164.304) that it becomes aware of; and (c) any Breach of Unsecured PHI, in accordance with 45 CFR § 164.410, without unreasonable delay and no later than sixty (60) calendar days after discovery.

2.6 **Breach Notification and Encrypted PHI Safe Harbor.** The parties acknowledge that, under HHS guidance implementing 45 CFR § 164.402(2), ciphertext PHI stored under the Zero-Knowledge Architecture — where Business Associate holds no decryption key — qualifies for the breach notification safe harbor in the event of unauthorized access to Business Associate's storage infrastructure, provided the encryption key held by Covered Entity has not been compromised. In such events, Business Associate shall notify Covered Entity of the access event, and the parties shall jointly assess whether the safe harbor applies based on whether the encryption key was compromised.

2.7 **Subcontractors.** Business Associate shall enter into agreements with its subcontractors (including infrastructure providers such as Backblaze B2) that provide the same protections for PHI as those provided under this BAA, to the extent such subcontractors create, receive, maintain, or transmit PHI on Business Associate's behalf.

2.8 **Access to PHI.** Upon Covered Entity's written request, Business Associate shall make available to Covered Entity any PHI in Business Associate's possession that is needed to fulfill Covered Entity's obligations under 45 CFR § 164.524 (access). Because Business Associate stores only ciphertext, Business Associate can make available only the encrypted ciphertext objects. Covered Entity must use its private keys to decrypt the content.

2.9 **Amendment of PHI.** Business Associate shall accommodate Covered Entity's requests to amend PHI to the extent applicable, recognizing that Business Associate's ability to amend content is limited to replacing encrypted objects with updated encrypted versions provided by or authorized by Covered Entity.

2.10 **Accounting of Disclosures.** Business Associate shall document and make available to Covered Entity any disclosures of PHI made by Business Associate, as required to enable Covered Entity to respond to requests under 45 CFR § 164.528.

2.11 **Records Retention.** Business Associate shall retain PHI-related documentation, including this BAA, for a minimum of six (6) years from the date of creation or the date when the document was last in effect, whichever is later, in accordance with 45 CFR § 164.530(j).

2.12 **HHS Access.** Business Associate shall make its internal practices, books, and records relating to PHI available to the Secretary of HHS for determining compliance with the HIPAA Rules, in accordance with 45 CFR § 164.504(e)(2)(ii)(I).

---

### ARTICLE 3 — OBLIGATIONS OF COVERED ENTITY

3.1 **Notice of Privacy Practices.** Covered Entity shall provide Business Associate with any changes to Covered Entity's Notice of Privacy Practices that affect Business Associate's permitted uses or disclosures under this BAA.

3.2 **Permission Changes.** Covered Entity shall promptly notify Business Associate of any restrictions on PHI uses or disclosures to which Covered Entity has agreed, to the extent such restrictions affect Business Associate's activities.

3.3 **Key Custody Responsibility.** Covered Entity acknowledges its sole responsibility for safekeeping of private decryption and signing keys delivered at provisioning. Covered Entity acknowledges that key loss results in permanent and irrecoverable loss of access to encrypted PHI, and that Business Associate has no obligation or ability to restore such access.

3.4 **Compliance Certification.** Covered Entity represents and warrants that it is either a Covered Entity or a Business Associate under HIPAA, and that it has appropriate authority to enter into this BAA.

3.5 **Regulatory Compliance.** Covered Entity is solely responsible for compliance with all provisions of the HIPAA Rules as they apply to Covered Entity's own operations, including as Data Controller of the PHI stored in the Licensee Namespace.

---

### ARTICLE 4 — TERM AND TERMINATION

4.1 **Term.** This BAA is effective as of the Effective Date and shall remain in effect until the Enterprise License Agreement is terminated or this BAA is otherwise terminated.

4.2 **Termination for Cause.** Either party may terminate this BAA if the other party materially breaches any provision and fails to cure such breach within thirty (30) days of written notice.

4.3 **Effect of Termination.** Upon termination, Business Associate shall, at Covered Entity's election: (a) return or destroy all PHI in Business Associate's possession; or (b) if return or destruction is infeasible, extend protections for such PHI and limit further use or disclosure to those purposes that make return or destruction infeasible. Under the Zero-Knowledge Architecture, Business Associate holds only ciphertext; return means making the encrypted objects available for download; destruction means deletion of the ciphertext objects from the Licensee Namespace.

---

### ARTICLE 5 — MISCELLANEOUS

5.1 **Conduit Exception — Not Applicable.** The parties acknowledge that, per HHS FAQ 2076 (2026), a CSP storing encrypted ePHI without a decryption key is classified as a Business Associate rather than a conduit exempt from Business Associate status. This BAA reflects and implements that classification. Business Associate does not rely on the conduit exception as the basis for any position under this BAA.

5.2 **Conduit Architecture as Risk Reduction.** Notwithstanding §5.1, the parties acknowledge that Business Associate's technical architecture — ciphertext-only storage with customer-held keys — substantially reduces Business Associate's operational PHI risk exposure compared to a conventional Business Associate that holds decryption keys, and provides the strongest practical compliance safeguard available.

5.3 **Governing Law.** This BAA shall be governed by the laws of [STATE], without regard to conflict-of-law principles, and by applicable federal law including the HIPAA Rules.

5.4 **Amendment.** This BAA may be amended by mutual written agreement of the parties. In the event of any change in the HIPAA Rules that affects the parties' obligations hereunder, the parties shall negotiate in good faith to amend this BAA accordingly.

5.5 **Entire Agreement (as to BAA subject matter).** This BAA, together with the Enterprise License Agreement of which it is an exhibit, constitutes the entire agreement between the parties with respect to the subject matter hereof.

---

**IN WITNESS WHEREOF**, the parties have executed this Business Associate Agreement as of the Effective Date.

**COVERED ENTITY / BUSINESS ASSOCIATE:**

Signature: ________________________
Name: ________________________
Title: ________________________
Entity: ________________________
Date: ________________________

**BUSINESS ASSOCIATE / SUB-BUSINESS ASSOCIATE:**

Signature: ________________________
Name: ________________________
Title: ________________________
Entity: ________________________
Date: ________________________

---

## Vancouver Bibliography

1. US Department of Health and Human Services. 45 CFR Part 164 — Security and Privacy (HIPAA Privacy Rule, Security Rule, Breach Notification Rule). Electronic Code of Federal Regulations. Available from: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164 **✅ VERIFIED** — eCFR.gov confirmed.

2. US Department of Health and Human Services, Office for Civil Rights. FAQ 2076: If a CSP stores only encrypted ePHI and does not have a decryption key, is it a HIPAA business associate? HHS.gov. Available from: https://www.hhs.gov/hipaa/for-professionals/faq/2076/if-a-csp-stores-only-encrypted-ephi-and-does-not-have-a-decryption-key-is-it-a-hipaa-business-associate/index.html **✅ VERIFIED** — HHS.gov confirmed. Authoritative statement that no-view CSP is a BA, not a conduit.

3. US Department of Health and Human Services, Office for Civil Rights. Guidance on HIPAA and Cloud Computing. HHS.gov. Available from: https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html **✅ VERIFIED** — HHS.gov confirmed via search.

4. US Department of Health and Human Services. Breach Notification Guidance — Safe Harbor for Encrypted PHI. HHS.gov. Available from: https://www.hhs.gov/hipaa/for-professionals/breach-notification/guidance/index.html **✅ VERIFIED** — HHS.gov confirmed.

5. US Government Publishing Office. 45 CFR § 164.530(j) — Retention of documentation. Electronic Code of Federal Regulations. Available from: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.530 **✅ VERIFIED** — 6-year retention requirement confirmed.
