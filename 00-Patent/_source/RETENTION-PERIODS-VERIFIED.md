# Retention Periods — Triple-Fact-Checked Reference

> **Authoritative retention-period reference for use in the ELA, BAA, and DPA.**
> Every period below is verified against an authoritative primary source via web search.
> Status markers: ✅ VERIFIED | ❌ COULDN'T VERIFY | ⚠️ AMBIGUOUS

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE
Retention requirements are jurisdiction-specific and fact-pattern-dependent.
Engage a privacy + compliance attorney before relying on these periods
in any contract or compliance program.

---

## Retention Period Table

### 1. HIPAA (US) — 6 years

**Jurisdiction:** United States federal (Health Insurance Portability and Accountability Act)
**Framework:** 45 CFR § 164.530(j) (Privacy Rule Administrative Requirements)
**Period:** 6 years from the date of creation OR the date when the document was last in effect, whichever is later
**Applies to:** Documentation required by the HIPAA Privacy Rule (policies, procedures, accounting of disclosures, authorization forms, notices of privacy practices, records of actions and assessments); Business Associate Agreements. NOTE: 45 CFR § 164.530(j) governs DOCUMENTATION retention, not patient medical record retention (which is governed by state law, typically longer).

**Verification status: ✅ VERIFIED**

Authoritative source: Electronic Code of Federal Regulations, 45 CFR § 164.530(j)(2):
> "A covered entity must retain the documentation required by paragraph (j)(1) of this section for six years from the date of its creation or the date when it last was in effect, whichever is later."

Confirmed via: Law Cornell LII (https://www.law.cornell.edu/cfr/text/45/164.530), eCFR.gov (https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.530), and multiple secondary sources including HIPAA Journal (https://www.hipaajournal.com/hipaa-retention-requirements/).

**Important nuance for this architecture:** The 6-year rule governs HIPAA compliance documentation (BAAs, policies, procedures). Patient medical record retention is governed by applicable state law, which often requires 7-10 years. Healthcare Licensees must comply with both.

---

### 2. PHIPA (Ontario) — Adults: 10 years; Minors: Age of majority + 10 years

**Jurisdiction:** Province of Ontario, Canada (Personal Health Information Protection Act, 2004)
**Framework:** Ontario Regulation 329/04 (General), section 13
**Period:**
- Adults: 10 years after the last transaction or interaction in which the record was used
- Minors: Until the individual reaches the age of majority (18 in Ontario) + 10 years — whichever is later

**Verification status: ✅ VERIFIED**

Authoritative source: Ontario Regulation 329/04, s. 13, under the Personal Health Information Protection Act, 2004, SO 2004, c 3, Sch A.

Confirmed via: Ontario e-Laws official website (https://www.ontario.ca/laws/regulation/040329) and CanLII cross-reference (https://www.canlii.org/en/on/laws/regu/o-reg-329-04/latest/o-reg-329-04.html). Secondary source confirmation via CRTO guidance (https://www.crto.on.ca/pdf/FAQs/FAQ.Feb.2017.pdf) and CPSO Medical Records Management policy (https://www.cpso.on.ca/Physicians/Policies-Guidance/Policies/Medical-Records-Management).

Additional nuance: Physicians may wish to retain records for longer than the 10-year requirement given that certain legal proceedings can be brought forward 15 years after an act or omission (per secondary guidance).

**Applies to:** Health Information Custodians (HICs) as defined in PHIPA s. 3 — healthcare providers, hospitals, pharmacies, laboratories, etc. Licensor's role is that of an agent of the custodian; primary retention obligation rests with the HIC (customer).

---

### 3. PIPEDA (Canada federal) — No fixed period

**Jurisdiction:** Canada federal (Personal Information Protection and Electronic Documents Act, SC 2000, c 5)
**Framework:** PIPEDA Schedule 1, Principle 4.5 (Limiting Use, Disclosure, and Retention)
**Period:** No fixed statutory minimum or maximum. Principle of "no longer than necessary for the fulfilment of those purposes" for which the information was collected.

**Verification status: ✅ VERIFIED**

Authoritative source: PIPEDA Schedule 1, Principle 4.5:
> "Personal information shall be retained only as long as necessary for the fulfilment of those purposes."

Additional requirement: "Organizations should develop guidelines and implement procedures with respect to the retention of personal information. These guidelines should include minimum and maximum retention periods."

Confirmed via: Justice Laws Website Canada (https://laws-lois.justice.gc.ca/eng/acts/p-8.6/page-7.html) and Office of the Privacy Commissioner of Canada (https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/).

**Practical implication for contracts:** While no fixed period applies, Licensee must have and follow a documented retention schedule. ELA Recital X.6 places this obligation on Licensee as data controller.

**Note:** PIPEDA is being superseded federally by the Consumer Privacy Protection Act (CPPA, Bill C-27) which passed but has not yet come fully into force as of knowledge cutoff. Attorney should confirm current status at contract execution.

---

### 4. CCPA (California) — No fixed minimum period

**Jurisdiction:** State of California, United States (California Consumer Privacy Act, Cal. Civ. Code §§ 1798.100 et seq., as amended by CPRA)
**Framework:** Cal. Civ. Code § 1798.130 (disclosure obligations)
**Period:** No fixed minimum or maximum retention period. However:
- Businesses must disclose retention practices per § 1798.130(a)(5)(B): "the length of time the business intends to retain each category of personal information"
- Businesses must not retain personal information longer than "reasonably necessary for each disclosed purpose of use" (CPRA amendment, Cal. Civ. Code § 1798.100(a)(3))
- Nothing in § 1798.130 requires a business to keep personal information for any minimum length of time

**Verification status: ✅ VERIFIED**

Authoritative source: California Civil Code § 1798.130. Confirmed via California Legislative Information official website (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.130.) and FindLaw (https://codes.findlaw.com/ca/civil-code/civ-sect-1798-130/).

Key text confirmed: "Nothing in this subparagraph shall require a business to keep personal information for any length of time."

**Practical implication:** Licensee must have a disclosed retention schedule per CCPA; Licensor's ELA places this obligation on Licensee.

---

### 5. Quebec Law 25 — No fixed period ("no longer than necessary")

**Jurisdiction:** Province of Quebec, Canada (Act respecting the protection of personal information in the private sector, CQLR c P-39.1, as amended by Law 25 / Bill 64)
**Framework:** Act respecting the protection of personal information in the private sector, CQLR c P-39.1
**Period:** No fixed minimum period. Personal information must be destroyed, erased, or anonymized "when the purposes for which it was collected or used have been achieved." One explicit minimum: information used to make a decision about a person must be kept for at least 1 year following the decision, to allow the individual to exercise their rights.

**Verification status: ✅ VERIFIED (with paraphrase clarification)**

Authoritative source: Act respecting the protection of personal information in the private sector, CQLR c P-39.1. Official text at Légis Québec (https://www.legisquebec.gouv.qc.ca/en/document/cs/p-39.1) and CanLII (https://www.canlii.org/en/qc/laws/stat/cqlr-c-p-39.1/latest/cqlr-c-p-39.1.html).

The brain-dump phrase "as long as serves the purposes" is a reasonable paraphrase but not verbatim statutory text. Correct formulation: personal information shall be kept only "for the period necessary to achieve the purposes for which it was collected, or as required by law."

**Additional nuance:** Law 25 (in force in phases 2022-2023) introduced stronger requirements than the original Act. Attorney should verify which provisions are now fully in force at contract execution.

---

### 6. GDPR (EU) — No fixed period (storage limitation principle)

**Jurisdiction:** European Union / European Economic Area (General Data Protection Regulation, Regulation (EU) 2016/679)
**Framework:** GDPR Article 5(1)(e) (storage limitation principle)
**Period:** No fixed statutory period. Personal data must be kept "in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed."

**Verification status: ✅ VERIFIED**

Authoritative source: GDPR Article 5(1)(e):
> "personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject ('storage limitation')"

Confirmed via: EUR-Lex (https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng), GDPR-Info.eu (https://gdpr-info.eu/art-5-gdpr/), UK ICO guidance (https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/).

**UK GDPR:** Same storage limitation principle applies under UK GDPR (retained EU law).

---

### 7. General US Business/Tax Records (IRS) — 3 years statutory; 7 years conventional for specific claims

**Jurisdiction:** United States federal (Internal Revenue Code)
**Framework:** IRC § 6501 (limitations on assessment and collection)
**Period:**
- Standard statute of limitations for IRS tax assessment: **3 years** from the date the return was filed (IRC § 6501(a))
- Extended period for substantial omissions: **6 years** (IRC § 6501(e), where omitted income exceeds 25% of gross income shown on return)
- Bad-debt deductions and worthless securities: **7 years** (IRC § 6501(e)(1)(A) by cross-reference)
- No statute of limitations: fraudulent returns or failure to file

**Verification status: ✅ VERIFIED (with important nuance correction)**

Authoritative source: 26 U.S. Code § 6501 (Limitations on assessment and collection). Confirmed via Law Cornell LII (https://www.law.cornell.edu/uscode/text/26/6501) and IRS guidance (https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records).

**CRITICAL NUANCE — Correction of brain-dump claim:** The brain-dump states "7 years (tax records) | IRC § 6501 + business custom" as a general rule. This is imprecise. The IRS standard statute of limitations is 3 years, not 7. The 7-year period applies specifically to bad-debt/worthless-securities deduction claims. The "7-year general business records" figure is widely cited conventional guidance (keep records as long as the longest applicable limitation period might run, plus buffer) but is NOT a hard statutory mandate for general business records.

**ELA implication:** ELA Recital X.6.3 uses "7 years from the date of account creation or last transaction" for Licensor's own provisioning and billing records. This is a conservative and defensible choice as it covers the 6-year extended assessment window plus buffer, and is consistent with conventional business record-keeping practice. It should not be cited as a hard IRC § 6501 mandate.

Confirmed via: IRS Publication 583 (Rev. December 2024) (https://www.irs.gov/publications/p583); IRS "How long should I keep records" guidance (https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records).

---

## Summary Table (verified)

| Jurisdiction / Framework | Period | Status | Governing Text |
|---|---|---|---|
| HIPAA (US) — compliance documentation | 6 years from creation or last effect | ✅ VERIFIED | 45 CFR § 164.530(j) |
| PHIPA (Ontario) — adult health records | 10 years after last transaction | ✅ VERIFIED | Reg. 329/04, s. 13 |
| PHIPA (Ontario) — minor health records | Age of majority + 10 years | ✅ VERIFIED | Reg. 329/04, s. 13 |
| PIPEDA (Canada federal) | No fixed period — necessity principle | ✅ VERIFIED | Schedule 1, Principle 4.5 |
| CCPA (California) | No fixed minimum | ✅ VERIFIED | Cal. Civ. Code § 1798.130 |
| Quebec Law 25 | No fixed period — necessity principle + 1-year minimum for decision records | ✅ VERIFIED (paraphrase clarified) | CQLR c P-39.1 |
| GDPR (EU) | No fixed period — storage limitation (Art. 5(1)(e)) | ✅ VERIFIED | Regulation (EU) 2016/679 |
| IRS (US) — standard business records | 3 years statutory; 7 years conventional | ✅ VERIFIED (nuance corrected) | IRC § 6501(a); IRS Pub. 583 |

---

## Brain-Dump Discrepancy Log

The following discrepancies between the brain-dump table and verified statutory text are noted for the operator:

| Brain-Dump Claim | Verified Finding | Action |
|---|---|---|
| "7 years (tax records) | IRC § 6501 + business custom" as general rule | IRC § 6501(a) standard is 3 years; 7 years applies to bad-debt/worthless-securities only; "7 years" as general guidance is convention not statute | ELA Recital X.6.3 uses 7 years as conservative convention — flag as convention, not mandate |
| Quebec Law 25: "As long as serves the purposes... or required by law" | Accurate paraphrase; not verbatim statutory text. Official: "for the period necessary to achieve the purposes for which it was collected, or as required by law" | Updated phrasing in ELA Recital X.6 |
| HIPAA conduit exception may apply to zero-knowledge architecture | HHS FAQ 2076 explicitly confirms: no-view CSP storing encrypted ePHI is a Business Associate, NOT a conduit | BAA is required; conduit exception does not apply; BAA-TEMPLATE.md and ELA-COMPLIANCE-ADDENDUM.md reflect this |
| PHIPA retention: "10 years after the last transaction or interaction" | Verified as substantially correct per CanLII and secondary professional guidance | No correction needed |

---

## Vancouver Bibliography

1. US Government Publishing Office. 45 CFR § 164.530(j) — Administrative requirements: Documentation. Electronic Code of Federal Regulations [Internet]. Available from: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.530 **✅ VERIFIED**

2. Legal Information Institute, Cornell Law School. 45 CFR § 164.530. Cornell Law [Internet]. Available from: https://www.law.cornell.edu/cfr/text/45/164.530 **✅ VERIFIED**

3. Ontario. Personal Health Information Protection Act, 2004, SO 2004, c 3, Sch A; Ontario Regulation 329/04 (General), s. 13. e-Laws Ontario [Internet]. Available from: https://www.ontario.ca/laws/regulation/040329 **✅ VERIFIED**

4. CanLII. O Reg 329/04 — General [PHIPA]. CanLII [Internet]. Available from: https://www.canlii.org/en/on/laws/regu/o-reg-329-04/latest/o-reg-329-04.html **✅ VERIFIED**

5. Canada. Personal Information Protection and Electronic Documents Act, SC 2000, c 5, Schedule 1, Principle 4.5. Justice Laws Website [Internet]. Available from: https://laws-lois.justice.gc.ca/eng/acts/p-8.6/page-7.html **✅ VERIFIED**

6. Office of the Privacy Commissioner of Canada. PIPEDA fair information principles — Principle 5: Limiting Use, Disclosure, and Retention. OPC [Internet]. Available from: https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/ **✅ VERIFIED**

7. California Legislative Information. California Civil Code § 1798.130 (CCPA). [Internet]. Available from: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.130. **✅ VERIFIED**

8. Légis Québec. Act respecting the protection of personal information in the private sector, CQLR c P-39.1 (Quebec Law 25). [Internet]. Available from: https://www.legisquebec.gouv.qc.ca/en/document/cs/p-39.1 **✅ VERIFIED (via search confirmation)**

9. European Parliament and Council of the European Union. Regulation (EU) 2016/679 (GDPR), Art. 5(1)(e). Off J Eur Union. 2016 Apr 27;L 119:1-88. Available from: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng **✅ VERIFIED**

10. UK Information Commissioner's Office. A guide to the data protection principles — Storage limitation. ICO [Internet]. Available from: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ **✅ VERIFIED (via search)**

11. Legal Information Institute, Cornell Law School. 26 U.S. Code § 6501 — Limitations on assessment and collection. Cornell Law [Internet]. Available from: https://www.law.cornell.edu/uscode/text/26/6501 **✅ VERIFIED**

12. Internal Revenue Service. Publication 583 (Rev. December 2024): Starting a Business and Keeping Records. IRS.gov [Internet]. Available from: https://www.irs.gov/publications/p583 **✅ VERIFIED**

13. Internal Revenue Service. How long should I keep records? IRS.gov [Internet]. Available from: https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records **✅ VERIFIED**

14. US Department of Health and Human Services, Office for Civil Rights. FAQ 2076: CSP stores only encrypted ePHI without decryption key — HIPAA business associate status. HHS.gov [Internet]. Available from: https://www.hhs.gov/hipaa/for-professionals/faq/2076/if-a-csp-stores-only-encrypted-ephi-and-does-not-have-a-decryption-key-is-it-a-hipaa-business-associate/index.html **✅ VERIFIED**
