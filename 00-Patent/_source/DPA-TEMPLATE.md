# Data Processing Agreement — Template

> **Exhibit DPA-1 to the Enterprise License Agreement**
> For EU/UK customers under GDPR.
> Incorporates Standard Contractual Clauses (Commission Implementing Decision (EU) 2021/914)
> for international data transfers where Licensee data crosses EU borders to US-based
> Backblaze B2 infrastructure.

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
This document is generated draft language for operator review.
Engage a privacy + compliance attorney before any USPTO filing,
contract signature, or customer-facing publication.
Jurisdiction-specific requirements may differ.

---

## DATA PROCESSING AGREEMENT

This Data Processing Agreement ("DPA") is entered into as of the Effective Date specified below, by and between:

**DATA CONTROLLER ("Controller"):** [LICENSEE ENTITY NAME], a [Country] [entity type]; hereinafter "Controller."

**DATA PROCESSOR ("Processor"):** [LICENSOR ENTITY NAME], a [State, US] [entity type], holding an exclusive license from joint individual inventors [INVENTOR 1 NAME] and [INVENTOR 2 NAME] and operating the licensed technology as a sublicensor; hereinafter "Processor."

*(Note on entity structure: Per the patent filing structure, the two individual inventors hold the patent. The entity signing this DPA operates under an exclusive license from those inventors. Confirm this structure with legal counsel before execution.)*

**Effective Date:** [DATE]

---

### RECITALS

A. Controller is established in the European Union / European Economic Area / United Kingdom and processes personal data of EU/EEA/UK data subjects in connection with its use of Processor's AI platform services.

B. Processor provides a zero-knowledge customer-key-custody architecture: Processor generates cryptographic keypairs at provisioning, delivers private keys to Controller, and irrevocably erases private keys from Processor's systems. Processor thereafter stores only ciphertext on Controller's behalf and has no technical ability to access plaintext personal data.

C. The parties enter into this DPA to comply with the requirements of Regulation (EU) 2016/679 (GDPR) and, where applicable, the UK GDPR.

D. Where Controller's personal data is stored on Processor's US-based infrastructure (Backblaze B2 US regions), the parties agree that Commission Implementing Decision (EU) 2021/914 Standard Contractual Clauses (SCCs) apply as the lawful transfer mechanism under GDPR Article 46, incorporated herein as Annex SCC.

---

### ARTICLE 1 — DEFINITIONS

1.1 "GDPR" means Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data.

1.2 "UK GDPR" means the GDPR as it forms part of the law of England and Wales, Scotland and Northern Ireland by virtue of section 3 of the European Union (Withdrawal) Act 2018.

1.3 "Personal Data," "Processing," "Data Subject," "Data Controller," "Data Processor," "Personal Data Breach," and "Supervisory Authority" have the meanings given in GDPR Article 4.

1.4 "Zero-Knowledge Architecture" means Processor's technical practice of: (a) generating cryptographic keypairs server-side at provisioning; (b) delivering private keys to Controller; (c) irrevocably erasing private keys from Processor's systems; and (d) storing only ciphertext personal data in Controller's isolated storage namespace, such that Processor has no technical means to access plaintext personal data at any time after provisioning.

1.5 "SCCs" means the Standard Contractual Clauses for international transfers of personal data to third countries under Commission Implementing Decision (EU) 2021/914 of 4 June 2021.

---

### ARTICLE 2 — SCOPE AND ROLES

2.1 **Controller Role.** Controller is the Data Controller as defined in GDPR Article 4(7): Controller determines the purposes and means of processing personal data stored in Controller's isolated namespace. Controller's exclusive private-key custody is the technical basis for this controller role.

2.2 **Processor Role.** Processor is the Data Processor as defined in GDPR Article 4(8): Processor processes personal data (in ciphertext form only) on behalf of Controller, pursuant to Controller's instructions. Processor's inability to access plaintext personal data is a technical property of the Zero-Knowledge Architecture.

2.3 **Instructions.** Processor shall process personal data only on Controller's documented instructions. The provision of the platform services described in the Enterprise License Agreement constitutes Controller's ongoing instruction to Processor. Processor shall immediately inform Controller if, in Processor's opinion, an instruction infringes GDPR.

---

### ARTICLE 3 — OBLIGATIONS OF PROCESSOR

3.1 **Confidentiality.** Processor shall ensure that persons authorized to process personal data on behalf of Processor are bound by appropriate confidentiality obligations.

3.2 **Security of Processing.** Processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, in accordance with GDPR Article 32. Processor's Zero-Knowledge Architecture — ciphertext-only storage with Controller-held keys — constitutes the highest practical technical safeguard available.

3.3 **Sub-processors.** Processor shall not engage a sub-processor without prior written authorisation from Controller. Processor shall enter into sub-processing agreements with authorised sub-processors (including Backblaze Inc. as infrastructure provider) that impose on them data protection obligations equivalent to those in this DPA. Current authorised sub-processors are listed in Annex A. Processor shall inform Controller of any intended changes to sub-processors with reasonable advance notice.

3.4 **Data Subject Rights.** Processor shall assist Controller, by appropriate technical and organisational measures, to fulfil Controller's obligations to respond to requests from data subjects exercising their rights under GDPR (Articles 15-22), recognising that Processor's ability to assist is limited to its administrative records; Processor holds no plaintext content and cannot itself provide content in response to Subject Access Requests.

3.5 **Data Protection Impact Assessment.** Processor shall provide reasonable assistance to Controller in conducting data protection impact assessments (GDPR Article 35) and prior consultation with supervisory authorities (Article 36), where required.

3.6 **Deletion and Return.** Upon termination of the Enterprise License Agreement or upon Controller's request, Processor shall delete or return all personal data to Controller. Under the Zero-Knowledge Architecture, Processor shall make available all ciphertext objects for download and shall delete them from the Licensee Namespace upon instruction. Controller retains the ability to render data permanently inaccessible by destroying its private keys before or after deletion.

3.7 **Audit.** Processor shall make available to Controller all information necessary to demonstrate compliance with the obligations in this DPA, and shall allow for and contribute to audits, including inspections, conducted by Controller or a mandated auditor, subject to reasonable advance notice and Processor's confidentiality obligations to other customers.

3.8 **Breach Notification.** Processor shall notify Controller of any Personal Data Breach without undue delay and, where feasible, within 72 hours of becoming aware, as required by GDPR Article 33. Under the Zero-Knowledge Architecture, any breach of Processor's storage infrastructure that exposes only ciphertext — where the encryption key held by Controller has not been compromised — substantially reduces the risk to data subjects under the GDPR risk assessment required by Article 33(1). Processor and Controller shall jointly assess the severity of any such event.

3.9 **Records of Processing Activities.** Processor shall maintain records of all categories of processing activities carried out on behalf of Controller, in accordance with GDPR Article 30(2).

---

### ARTICLE 4 — INTERNATIONAL DATA TRANSFERS

4.1 **Basis for Transfer.** Where personal data of EU/EEA/UK data subjects is transferred from the EEA/UK to Processor's US-based storage infrastructure, the parties agree that Commission Implementing Decision (EU) 2021/914 Standard Contractual Clauses apply as the lawful transfer mechanism under GDPR Article 46(2)(c).

4.2 **Applicable Module.** The SCCs apply in their Module 2 form (Controller to Processor), or Module 3 form (Processor to Sub-Processor) for transfers from Processor to Backblaze Inc. as sub-processor, as appropriate.

4.3 **SCC Annex.** The SCCs are incorporated by reference herein as Annex SCC. The Annex I (parties, description of transfers), Annex II (technical and organisational measures), and Annex III (list of sub-processors) to the SCCs are set out in the corresponding Annexes to this DPA.

4.4 **EU Region Alternative.** Processor shall, upon Controller's written request and subject to availability, provision Controller's Licensee Namespace in Backblaze B2's EU-sovereign region (currently `eu-central-003`), which would reduce or eliminate the cross-border transfer basis for the SCCs. The availability of EU-region provisioning is not guaranteed and should be confirmed at contract execution.

4.5 **UK Transfers.** For transfers involving UK personal data to US infrastructure, the parties agree to apply the UK Information Commissioner's Office International Data Transfer Agreement (IDTA) or UK Addendum to the SCCs, as appropriate under UK GDPR. *(Note for attorney: The UK IDTA replaced the EU SCCs for UK-to-third-country transfers. Confirm current UK ICO requirements at time of contract execution.)*

---

### ARTICLE 5 — GDPR-SPECIFIC ARCHITECTURE ANALYSIS

5.1 **Storage Limitation (GDPR Art. 5(1)(e)).** GDPR requires that personal data be kept "in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed." Controller is solely responsible for ensuring that retention of data in the Licensee Namespace complies with this principle. Processor does not monitor retention periods on Controller's behalf.

5.2 **Right to Erasure (GDPR Art. 17).** Controller's exclusive private-key custody enables a technically complete implementation of the Right to Erasure: Controller may destroy its private key, rendering all stored ciphertext permanently and irrecoverably inaccessible, without any cooperation required from Processor. This key-destruction mechanism constitutes a valid erasure measure under GDPR Art. 17, provided no other copies of the data or keys exist.

5.3 **Right of Access (GDPR Art. 15).** Processor holds no plaintext content. Where a data subject requests access to their personal data from Controller, Controller must use its private keys to decrypt the relevant ciphertext objects. Processor can provide Controller with the ciphertext objects on request.

5.4 **Data Portability (GDPR Art. 20).** Controller may export all ciphertext objects from the Licensee Namespace and use its private keys to decrypt and migrate the data to any alternative platform or storage. Processor shall provide reasonable technical assistance for such export.

5.5 **Breach Notification De-risking.** Ciphertext stored under the Zero-Knowledge Architecture constitutes personal data in encrypted form. Under the GDPR breach notification risk analysis (Art. 33(1)), a breach exposing only ciphertext where the encryption key has not been compromised is unlikely to "result in a risk to the rights and freedoms of natural persons," substantially reducing or potentially eliminating notification obligations. The parties shall conduct the required risk assessment jointly in the event of any such breach.

---

### ARTICLE 6 — TERM AND TERMINATION

6.1 This DPA is effective as of the Effective Date and shall remain in effect for the duration of the Enterprise License Agreement.

6.2 Upon termination, Processor shall fulfill the deletion/return obligations of Article 3.6.

---

### ANNEX A — AUTHORISED SUB-PROCESSORS

| Sub-Processor | Country | Processing Purpose |
|---|---|---|
| Backblaze, Inc. | United States (and EU region `eu-central-003`) | Object storage — Licensee Namespace encrypted storage |
| [Additional sub-processors to be listed] | — | — |

---

### ANNEX B — DESCRIPTION OF PROCESSING (SCC Annex I)

**A. List of Parties:** As specified in the preamble of this DPA.

**B. Description of Transfer:**
- Categories of data subjects: As determined by Controller (may include end users, employees, healthcare patients, etc.)
- Categories of personal data: As submitted by Controller to the platform (encrypted at rest before storage; Processor has no visibility into categories)
- Sensitive data: May include special category data (Art. 9 GDPR) if Controller submits such data; Controller bears sole responsibility for ensuring appropriate legal basis and safeguards
- Frequency of transfer: Continuous during the term of the Agreement
- Subject-matter of processing: Encrypted storage of Controller's data; metadata processing (bucket creation, access logs, billing records)
- Duration: Duration of the Agreement
- Purpose of transfer: Providing platform services to Controller per the Enterprise License Agreement

---

### ANNEX C — TECHNICAL AND ORGANISATIONAL MEASURES (SCC Annex II / GDPR Art. 32)

1. Zero-Knowledge Architecture: ciphertext-only storage with Controller-held private keys — see Article 2 and Recital B
2. Isolated per-customer storage namespace (logical and credential isolation)
3. Transport Layer Security (TLS 1.2 minimum) for all data in transit
4. Cryptographic signing of stored records for tamper detection (forensic chain-of-custody)
5. Access controls to Processor's management plane limited to authorized personnel
6. Incident response and breach notification procedures per Article 3.8
7. Sub-processor contractual obligations per Article 3.3

---

## Vancouver Bibliography

1. European Parliament and Council of the European Union. Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation). Off J Eur Union. 2016 Apr 27;L 119:1-88. Available from: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng **✅ VERIFIED** — Art. 4(7), 4(8), 5(1)(e), 15, 17, 20, 30, 32, 33, 35, 46 confirmed.

2. European Commission. Commission Implementing Decision (EU) 2021/914 of 4 June 2021 on standard contractual clauses for the transfer of personal data to third countries pursuant to Regulation (EU) 2016/679. Off J Eur Union. 2021 Jun 7;L 199:31-61. Available from: https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj/eng **✅ VERIFIED** — Full title confirmed; OJ L 199, pp. 31-61; entered into force 27 June 2021.

3. UK Information Commissioner's Office. International Data Transfer Agreement (IDTA). ICO.org.uk. Available from: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/ **⚠️ NOT INDEPENDENTLY VERIFIED VIA SEARCH** — Attorney should confirm current UK IDTA form at contract execution. This reference is included for completeness; the EU SCCs 2021/914 are independently verified.

4. European Commission. Data protection: Frequently asked questions — What is a data controller or a data processor? Available from: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/controllerprocessor/what-data-controller-or-data-processor_en **✅ VERIFIED** — confirmed via search; Art. 4(7) and 4(8) definitions confirmed.
