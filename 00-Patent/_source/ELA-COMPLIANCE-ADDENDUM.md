# ELA Compliance Recitals — Addendum to Enterprise License Agreement

> **This document contains the six compliance recital sections that overlay onto
> ELA-DRAFT.md. Insert this addendum as a new section titled "Section [X]:
> Regulatory Compliance, Data Sovereignty, and Privacy Architecture" in the ELA.**

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a privacy + compliance attorney before any USPTO filing,
contract signature, or customer-facing publication.
Jurisdiction-specific requirements may differ.

---

## Section [X]: Regulatory Compliance, Data Sovereignty, and Privacy Architecture

### Recital X.0 — Framing

The parties acknowledge that Licensor's technology platform is designed to provide compliance with applicable data protection and privacy regulations by architectural construction rather than by organizational policy alone. The provisions in this Section describe the technical architecture through which Licensor achieves data sovereignty on behalf of Licensee, and establish the respective regulatory roles, obligations, and indemnification responsibilities of each party.

---

### Recital X.1 — Data Sovereignty and Customer as Canonical Data Controller

**X.1.1** Upon execution of this Agreement and completion of Licensee's initial payment, Licensor shall provision a dedicated object storage namespace (hereinafter "Licensee Namespace") for Licensee's exclusive use. The Licensee Namespace is isolated from all other customer namespaces via independent access credentials.

**X.1.2** Licensor shall generate a cryptographic encryption keypair and a cryptographic signing keypair on Licensor's server infrastructure. The private components of both keypairs shall be delivered to Licensee's designated email address at provisioning time and shall be irrevocably erased from Licensor's systems upon confirmed delivery. Licensor shall retain no copy of either private key in any storage medium after the delivery-and-erasure step completes.

**X.1.3** All Licensee content stored in the Licensee Namespace shall be encrypted using Licensee's public encryption key before being written to durable storage. Licensor's infrastructure shall hold no plaintext Licensee content at any time.

**X.1.4** Licensee is the sole and exclusive controller of all data stored in the Licensee Namespace. Licensor neither holds nor has technical access to any cryptographic key required to decrypt or modify Licensee's stored content. By virtue of this architecture:

(a) For purposes of the European Union General Data Protection Regulation (Regulation (EU) 2016/679, "GDPR"), Licensee is the Data Controller as defined in Article 4(7), and Licensor is at most a Data Processor as defined in Article 4(8), processing only ciphertext on behalf of Licensee.

(b) For purposes of the United States Health Insurance Portability and Accountability Act (45 CFR Parts 160 and 164, "HIPAA"), Licensee is the Covered Entity or primary Business Associate, and Licensor's role as a cloud storage provider of exclusively encrypted data is governed by the Business Associate Agreement attached hereto as Exhibit BAA-1, if applicable.

(c) For purposes of the Ontario Personal Health Information Protection Act, 2004 ("PHIPA"), Licensee is the Health Information Custodian, and Licensor is Licensee's agent processing personal health information in encrypted form without access to plaintext.

(d) For purposes of the Canadian Personal Information Protection and Electronic Documents Act ("PIPEDA"), Quebec Act Respecting the Protection of Personal Information in the Private Sector ("Law 25"), and the California Consumer Privacy Act ("CCPA"), Licensor's role is that of a service provider processing encrypted data on behalf of Licensee.

**X.1.5** This data sovereignty posture is a technical property of Licensor's architecture, not merely a contractual commitment. Licensor's technical inability to access Licensee's plaintext content is established at provisioning time and is maintained for the duration of this Agreement.

---

### Recital X.2 — Cryptographic Key Custody

**X.2.1** LICENSOR DOES NOT RETAIN COPIES OF LICENSEE'S PRIVATE ENCRYPTION KEY OR PRIVATE SIGNING KEY AFTER THE PROVISIONING DELIVERY STEP. This is a technical property of the system. Licensor cannot produce Licensee's private keys in response to any request, including compelled legal disclosure, court order, regulatory demand, or government subpoena, because Licensor does not hold them.

**X.2.2** Licensee is solely responsible for:
(a) Safekeeping and backup of the private keys delivered at provisioning;
(b) All access to Licensee's encrypted content (Licensor cannot assist with decryption if Licensee loses the private key);
(c) Key rotation, if Licensee elects to re-encrypt content with new keys in the future; and
(d) Decisions regarding key destruction for purposes of permanent data erasure.

**X.2.3** LICENSOR MAKES NO WARRANTY REGARDING THE RECOVERY OF LICENSEE'S PRIVATE KEYS OR LICENSEE'S ENCRYPTED CONTENT IN THE EVENT OF KEY LOSS. Key loss by Licensee results in permanent and irrecoverable loss of access to all content encrypted under those keys, and Licensor has no obligation or technical ability to restore such access.

---

### Recital X.3 — Conduit-Style Operator Role

**X.3.1** For purposes of applicable regulatory analysis, Licensor's operational relationship to Licensee's encrypted content is analogous to a conduit or transmission intermediary: Licensor provides the technical infrastructure for encrypted-at-rest storage and signed-data integrity verification but has no access to the semantic content of Licensee's data.

**X.3.2** The parties acknowledge that, notwithstanding the conduit-analogy characterization above, current HHS guidance (FAQ 2076, 2026) classifies a Cloud Service Provider storing encrypted ePHI without a decryption key as a HIPAA Business Associate, not a conduit exempt from Business Associate obligations. Accordingly:

(a) Healthcare Licensees whose use case involves Protected Health Information (PHI) as defined in 45 CFR § 160.103 shall execute the Business Associate Agreement attached hereto as Exhibit BAA-1.

(b) The BAA does not alter Licensor's technical inability to access plaintext PHI. It formalizes the parties' HIPAA compliance relationship for audit and reporting purposes.

(c) Licensee shall not submit PHI to the platform without first executing the BAA.

**X.3.3** For GDPR purposes, Licensor's status as a Data Processor (Art. 4(8)) processing only ciphertext on behalf of Licensee as Data Controller (Art. 4(7)) is the operative characterization. The Data Processing Agreement attached hereto as Exhibit DPA-1 governs this relationship for EU/UK Licensees.

---

### Recital X.4 — Business Associate Agreement

**X.4.1** For healthcare Licensees requiring formal HIPAA Business Associate Agreement coverage, the Business Associate Agreement template is attached hereto as Exhibit BAA-1 (incorporated by reference from the separately executed document titled "Business Associate Agreement — [LICENSOR] and [LICENSEE]").

**X.4.2** The BAA does not modify Licensor's technical architecture or expand Licensor's access to PHI. Licensor's technical inability to access plaintext PHI is maintained regardless of BAA execution status.

**X.4.3** Licensee represents and warrants that it will execute the BAA before submitting any PHI to the platform.

---

### Recital X.5 — Data Processing Agreement and Standard Contractual Clauses

**X.5.1** For EU/UK Licensees processing personal data subject to GDPR (Regulation (EU) 2016/679) or UK GDPR, the Data Processing Agreement is attached hereto as Exhibit DPA-1 (incorporated by reference from the separately executed document titled "Data Processing Agreement — [LICENSOR] and [LICENSEE]").

**X.5.2** Where Licensee's personal data physically resides on Licensor's US-based storage infrastructure (Backblaze B2 US regions), and such data originates from EU/EEA data subjects, the parties agree that Commission Implementing Decision (EU) 2021/914 Standard Contractual Clauses (Module 2: Controller to Processor, or Module 3: Processor to Sub-Processor, as applicable) are incorporated by reference into the DPA as the lawful transfer mechanism under GDPR Article 46.

**X.5.3** Licensor shall make reasonable efforts to provision EU/EEA Licensee Namespaces in Backblaze B2 EU-region infrastructure (currently `eu-central-003`) upon Licensee's request, to minimize cross-border transfer exposure. This regional provisioning option is best-effort and subject to Licensor's infrastructure availability at the time of provisioning.

---

### Recital X.6 — Records Retention Schedule

**X.6.1** Licensee is the data controller and is solely responsible for ensuring that its retention of data in the Licensee Namespace complies with all applicable jurisdiction-specific record retention obligations, including but not limited to:

| Jurisdiction / Framework | Applicable Retention Obligation |
|---|---|
| HIPAA (US) | 6 years from creation or last effective date (45 CFR § 164.530(j)) |
| PHIPA (Ontario — adults) | 10 years after last transaction (Reg. 329/04, s. 13) |
| PHIPA (Ontario — minors) | Until age of majority + 10 years (Reg. 329/04, s. 13) |
| PIPEDA (Canada federal) | No fixed period — no longer than necessary for the identified purposes (Schedule 1, Principle 4.5) |
| CCPA (California) | No fixed minimum retention — but must disclose retention practices per Cal. Civ. Code § 1798.130 |
| Quebec Law 25 | No fixed period — only as long as the purposes for which the information was collected require, or as required by law |
| GDPR (EU/EEA) | No fixed period — no longer than necessary per Art. 5(1)(e) storage limitation principle |

**X.6.2** Licensor's role is the technical operation of the encrypted storage infrastructure. Licensor does not independently monitor, enforce, or audit Licensee's compliance with the above retention obligations. Licensee is solely responsible for managing the lifecycle of data in the Licensee Namespace, including scheduled deletion, anonymization, or key destruction for permanent erasure.

**X.6.3** Licensor shall retain Licensee provisioning records, billing records, and infrastructure access logs (not content) for a period of 7 years from the date of account creation or last transaction, consistent with general US business record retention practice, unless a shorter or longer period is required by applicable law.

---

### Recital X.7 — Reverse Indemnification for Regulatory Violations

**X.7.1** LICENSEE INDEMNIFIES LICENSOR FOR REGULATORY COMPLIANCE VIOLATIONS ARISING FROM LICENSEE'S DATA PRACTICES.

Licensee shall defend, indemnify, and hold harmless Licensor and its officers, agents, employees, and successors from and against any and all claims, demands, losses, damages, fines, penalties, and expenses (including reasonable attorneys' fees) arising out of or related to:

(a) Licensee's failure to comply with applicable privacy, data protection, and healthcare regulations, including GDPR, HIPAA, PHIPA, PIPEDA, CCPA, and Quebec Law 25, with respect to data Licensee stores or processes using the platform;

(b) Licensee's failure to execute required data processing agreements (BAA, DPA) before submitting regulated data to the platform;

(c) Licensee's failure to maintain adequate retention, deletion, or erasure schedules for data stored in the Licensee Namespace;

(d) Licensee's submission of data to the platform in violation of applicable data subject consent requirements;

(e) Any claim by a data subject against Licensor arising from Licensee's data controller obligations, where such claim arises from Licensee's instructions or failures rather than from Licensor's technical operations; and

(f) Regulatory investigations, audits, or enforcement actions triggered by Licensee's data practices, to the extent such actions name or impose obligations on Licensor.

**X.7.2** This Section X.7 reverse indemnification is in addition to, and not in lieu of, the general reverse indemnification provisions of Section [Y] of the Agreement.

**X.7.3** Licensor's maximum aggregate liability to Licensee for any regulatory compliance matter arising from Licensor's own technical operations (as opposed to Licensee's data practices) shall not exceed the limitation set forth in Section [Z] of the Agreement (twelve-month-paid-fees ceiling).

---

## Vancouver Bibliography

1. European Parliament and Council of the European Union. Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation). Off J Eur Union. 2016 Apr 27;L 119:1-88. Available from: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng **✅ VERIFIED**

2. European Commission. Commission Implementing Decision (EU) 2021/914 of 4 June 2021 on standard contractual clauses for the transfer of personal data to third countries pursuant to Regulation (EU) 2016/679. Off J Eur Union. 2021 Jun 7;L 199:31-61. Available from: https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj/eng **✅ VERIFIED**

3. US Government Publishing Office. 45 CFR § 164.530(j) — Documentation retention. Electronic Code of Federal Regulations. Available from: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.530 **✅ VERIFIED** — text confirmed: "must retain documentation...for six years from the date of its creation or the date when it last was in effect, whichever is later."

4. US Department of Health and Human Services. FAQ 2076: CSP stores encrypted ePHI without decryption key — HIPAA business associate status. HHS.gov. Available from: https://www.hhs.gov/hipaa/for-professionals/faq/2076/if-a-csp-stores-only-encrypted-ephi-and-does-not-have-a-decryption-key-is-it-a-hipaa-business-associate/index.html **✅ VERIFIED**

5. Ontario. Ontario Regulation 329/04 (PHIPA General), s. 13. e-Laws Ontario. Available from: https://www.ontario.ca/laws/regulation/040329 **✅ VERIFIED**

6. Office of the Privacy Commissioner of Canada. PIPEDA fair information principles — Principle 4.5 (Limiting Use, Disclosure, and Retention). OPC. Available from: https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/ **✅ VERIFIED** — text confirmed: "Personal information shall be retained only as long as necessary for the fulfilment of those purposes."

7. California Legislative Information. California Civil Code § 1798.130 (CCPA). Available from: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.130. **✅ VERIFIED** — confirmed: no fixed minimum retention period; disclosure obligations on retention practices.

8. Legis Quebec. Act respecting the protection of personal information in the private sector, CQLR c P-39.1 (Quebec Law 25). Available from: https://www.legisquebec.gouv.qc.ca/en/document/cs/p-39.1 **⚠️ AMBIGUOUS** — official text confirmed at legisquebec.gouv.qc.ca; retention language confirmed as "no longer than necessary for the purposes" with one-year minimum for decision-basis data; brain-dump phrasing "as long as serves the purposes" is an accurate paraphrase but not verbatim statutory text. Use: "no longer than necessary for the purposes for which it was collected, or as required by law."

9. Internal Revenue Service. Publication 583: Starting a Business and Keeping Records (Rev. December 2024). IRS.gov. Available from: https://www.irs.gov/publications/p583 **✅ VERIFIED** — confirmed IRS.gov publication; the general 3-year standard applies; 7 years applies specifically to bad-debt and worthless-securities claims (IRC § 6501(e)(1)(A)). Note: the "7-year general business records" figure in the brain-dump is conservative guidance, not a hard statutory mandate. See RETENTION-PERIODS-VERIFIED.md for full discussion.
