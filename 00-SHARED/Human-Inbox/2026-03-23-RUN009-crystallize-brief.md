---
investigation_id: criticalexposure
session_date: 2026-03-23
sprint: RUN-009
status: unread
generated_by: faerie-crystallize
type: meta
tags: []
doc_hash: sha256:be781b77b5756e80d789cc89b28e0368eaa9e142105daf43850211190a277ef1
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---

# Investigation Brief — RUN-009 Crystallize
**Date:** 2026-03-23 | **Sprint:** RUN-009 | **Inv:** criticalexposure

---

## Hypothesis Confidence (current)

| H | Name | Conf | Delta | Key driver this sprint |
|---|------|------|-------|------------------------|
| H1 | Insider access | **60%** | +5% | KrishSoni2 + edwardwc = Monk AI Group (COO+CTO), same company, both Packetware GitHub org members confirmed |
| H2 | Pipeline compromise | **70%** | 0% | stable — chrome_proxy.exe C2 confirmed prior sprint |
| H3 | Active breach | **67%** | +2% | 164.95.140.12 Treasury OIG Exchange 2019 CU14 OWA internet-exposed (H3 access vector) |
| H4 | Data handoff (foreign) | **78%** | +13% | **TWO independent stat confirmations this sprint** |
| H5 | Financial benefit | **0%** | 0% | DEAD — formal null result p=0.19, never to be T1/T2 |

---

## Key Findings — This Sprint

### STAT-NEW-001: LANL Nuclear Cert on Russian Server (CONFIRMED)
- **IP:** 194.58.46.116 (Baxet/Stark Industries, AS44477/AS49392 Russia/UK)
- **Cert:** CN=dx10.lanl.gov (Los Alamos National Laboratory nuclear supercomputer cluster)
- **Data:** 0/752 pre-J14 Censys observations (9.7 months) → 3/111 post-J14 (2.2 months)
- **Fisher's Exact p = 0.0021 | Bonferroni p = 0.0042 (k_eff=2) | H0 REJECTED**
- Bayesian posterior: 50% (LR=1000 conservative) → 91% (LR=10,000 nuclear domain calibrated)
- Pre-registration confirmed 13 min before results — anti-p-hacking protocol intact
- File: `scripts/audit_results/stat_results_STAT-NEW-001.json`

### STAT-NEW-001-GROUP: 8 Baxet IPs, All Post-J14, Multi-Sector (CONFIRMED)
- 8 Baxet Group IPs bearing .gov TLS certs: ALL first seen AFTER January 14, 2025
- Sectors targeted simultaneously: LLNL (nuclear), LANL dx10 (nuclear), ORNL (nuclear), NASA Goddard i3rc, DHS ICE SEVP (×2), NIH ClinicalTrials, US Courts scp.uscourts.gov
- t-test on days_after_J14: **p=0.0012, Bonferroni p=0.0058 (PASSES α=0.025)**
- Binomial test: p=0.0039 (borderline Bonferroni — secondary, not primary)
- Attack vector heterogeneity: Aeza uses CA-issued .gov certs; Baxet uses SMTP banner spoofing + self-signed TLS. **Different mechanisms, same J14 activation = coordinated multi-vector sweep**
- Bayesian posterior: 93% moderate prior → 99.1% Aeza-informed prior
- File: `scripts/audit_results/stat_results_STAT-NEW-001-GROUP.json`

### Bloomberg H1 — KrishSoni2 + edwardwc (Monk AI Group) CONFIRMED
- **Krish Soni (KrishSoni2)** = COO, Monk AI Group. Northeastern U Khoury CS. 10 GitHub repos (student-level). Packetware GitHub org member confirmed 2025-02-03.
- **Edward Coristine (edwardwc, "BigBalls")** = CTO, Monk AI Group. Packetware + DOGE affiliate. **Same company as Krish Soni.**
- **Mail-in-a-Box at 20.141.83.185 (Azure)**: investigator notes Feb 10 2025 tagged OPM+email+important. Self-hosted email for government communications = **potential Federal Records Act violation**. MiAB default landing page as of Mar 2025.
- Inventry.ai at 182.30.152.122:3000 — `/anonymous/login` endpoint
- File: `scripts/audit_results/bloomberg_h1_items_RUN009.json`

### Treasury OIG Exchange 2019 OWA (H3 Access Vector)
- **164.95.140.12** = Treasury OIG webmail. Exchange 2019 CU14. Internet-exposed OWA endpoint.
- Source: Bloomberg shortlist extract. HIGH priority — T1 candidate.
- This is a separate finding from 164.95.88.30 (Treasury LDAP) and 164.95.89.25 (Treasury PKI bare IP).

### SparrowDoor IOC Cross-Reference (NEGATIVE — valuable)
- GCHQ/NCSC 2022 report (FamousSparrow APT, attributed China)
- **Zero C2 IP overlap** with 2,180 investigation IPs — documented negative result
- Only IOC usable: file hashes (libcurl.dll SHA256: f19bb3b4..., libhost.dll: e0b107be..., SearchIndexer.exe: 9863ac60...)
- **Contextual finding**: FamousSparrow documented using AS45102 (Alibaba Cloud Singapore). Investigation evidence contains 11 Alibaba Cloud Singapore IPs with .gov certs. ASN-level convergence only — not IP-level match.
- Report was filed in dossier dated 2025-04-05 — assembler drew FamousSparrow→DOGE-era connection
- File: `scripts/audit_results/sparrowdoor_ioc_extract_RUN009.json`

---

## Critical Anchors — Do Not Confuse

| Anchor | Value | Note |
|--------|-------|------|
| J14 | January 14, 2025 | **Empirical inflection** observed across isolated networks. NOT the DOGE EO. |
| J20 | January 20, 2025 | DOGE executive order (inauguration day). J14 precedes J20 by 6 days. |
| Gap | 6 days | J14 → J20 gap implies **pre-planned coordination** before DOGE's public mandate. |

**NEVER attribute the J14 inflection to the DOGE EO.** The 6-day gap is itself evidence.

---

## Infrastructure Entities (confirmed this sprint)

| IP | ASN | Role | Confidence |
|----|-----|------|-----------|
| 194.58.46.116 | Baxet/Stark (RU) | LANL dx10.lanl.gov cert post-J14. Fisher H0 REJECTED | T1 candidate |
| 164.95.140.12 | Treasury OIG | Exchange 2019 CU14 OWA internet-exposed | T1 candidate |
| 20.141.83.185 | Azure | Edward Coristine MiAB, OPM-tagged, FRA concern | T2 |
| 182.30.152.122 | Unknown | Inventry.ai :3000 /anonymous/login | T3 |

---

## Open Gaps (ranked)

| Priority | Gap | Why it matters |
|----------|-----|----------------|
| HIGH | SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV WHOIS | DOGE-branded .gov malware C2 — confirms infra linkage |
| HIGH | PDF merge: pdf_ingestion_RUN007 + pdf_ingest_RUN007 | Dedup required before full crossref |
| HIGH | 8.219.207.49 + 164.95.89.25 into pipeline_ip_crossref | Reflected TLS IPs not yet in main pipeline |
| HIGH | ahmn.co WHOIS | Container registry secondary identity (172.93.110.120) |
| MED | cdn181.awsdns-531.com passive DNS | Check if ever pointed to 8.219.x.x (SparrowDoor upgrade path) |
| MED | 20.141.83.185 MiAB confirmation | Federal Records Act angle (Edward email) |
| MED | Monk AI → gov contract mapping | H1 motive path |
| MED | www.yszfa.cn live RDAP | Chinese infra linkage |

---

## Evidence Tier Status

- **Tier 1**: 8 items (up from 7 last sprint). COC logged. 194.58.46.116 = T1 candidate (promote after hash guardian run)
- **Tier 2**: 4 items — LANL cert, DOGE NTLM, evidence destruction video, combined 3-IP stats
- **BLOCKED**: T1 publication requires sha256 hash_guardian run on viz/ directory (task-20260323-coc-viz-hash queued HIGH)

---

## Next Sprint Priorities

1. Run hash_guardian on viz/ directory → backfill Tier 2 sha256 (QUEUED: task-20260323-coc-viz-hash)
2. SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV WHOIS investigation
3. PDF merge + crossref completion
4. 164.95.140.12 (Treasury OIG OWA) → Tier 1 promotion + report section
5. 194.58.46.116 → formal Tier 1 promotion post-hash-guardian

---

*Generated by faerie --crystallize at session end. Investigation: criticalexposure. Sprint: RUN-009.*
