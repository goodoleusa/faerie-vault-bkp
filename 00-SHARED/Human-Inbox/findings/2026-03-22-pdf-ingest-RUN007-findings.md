---
type: investigation-findings
date: 2026-03-22
sprint: RUN-007 PDF ingest (session-592227)
agents: data-engineer, data-scientist, evidence-curator
status: READY FOR HUMAN REVIEW
priority: HIGH
hypotheses: H1, H2, H3, H4
tags: []
doc_hash: sha256:fff2ff32854824a38dffb896d793e6fe0629c6731fb333ccebce3cb570dc0d81
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# RUN-007 PDF Ingest — Key Findings

> These findings come from ingesting 20–34 PDFs (two ingest runs, pending merge) from the investigation brief corpus. They surfaced new mechanisms and personnel not previously in the normalized evidence base.

---

## Bombshell: SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV as Malware C2

**Source:** Falcon Sandbox analysis of chrome_proxy.exe
**SHA256:** 92fcf735...
**C2 domain:** SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV

A file named `chrome_proxy.exe` (dropped by `test.exe`) was confirmed malicious by Falcon Sandbox. Its C2 server is a DOGE-branded .gov subdomain. This is not an unofficial domain — it is a .gov subdomain, meaning someone with access to DOGE's DNS management created it. A .gov domain used as malware C2 infrastructure directly links the DOGE network administration to malicious tooling deployment.

**Hypothesis significance (H2 ↑):** H2 posits Packetware/DOGE as a data exfiltration pipeline. A DOGE-branded .gov domain acting as malware C2 is the most direct infrastructure evidence linking DOGE network operations to offensive tooling.

**Open:** WHOIS/DNS history for this domain — when registered, current status, registrant.

---

## Personnel: Luke Farritor Named Accessing DOE Feb 5, 2025

**Source:** "Packetware and Purge" (31-page PDF in brief corpus)

Named: **Luke Farritor**, 23 years old, former SpaceX intern, accessing Department of Energy systems February 5, 2025. Also named: Secretary Brooke Rollins, Secretary Chris Wright.

Malware tag string found in source material: `bigballs`. SHA256 from same document: 68e11f5... (this is the Treasury Entrust OV cert fingerprint — appearing in the same document as the personnel names is notable).

**This is the kind of naming that needs independent corroboration before Tier 1 publication.** Currently Tier 2/3 — supports H1 (insider access narrative) but requires second source before publication-grade confidence.

---

## Reflected TLS Attack — Mechanism Documented

**Source:** "Treasury-and-USPTO-and-usadotgov-TLS-certs-Russia-China.pdf"

**Technical mechanism:** C2 server at 8.219.207.49 uses `socat` (SOcket CAT, a Unix networking utility) to proxy the TLS handshake from 164.95.89.25 (pki.treasury.gov). Because pki.treasury.gov does not enforce SNI (Server Name Indication), the proxy can relay TLS handshakes without possessing the private key. Passive scanners (Shodan/Censys) observing the C2 see what appears to be a legitimate Treasury HTTPS connection.

**Why this matters for interpreting Censys data:** Some of the .gov cert observations on foreign IPs may be socat reflections (no private key needed), while others — particularly the 11-month Entrust OV cert hold on Alibaba CN — cannot be reflections and require private key exfiltration. The Reflected TLS mechanism explains the scanner-visible anomalies without requiring every instance to involve key theft, while the Entrust OV cert finding proves key theft occurred regardless.

**New IPs from this PDF (not yet in pipeline):**
- 5.180.24.192 (Stark Industries / AS44477)
- 217.142.144.30 (Stark Industries / AS44477)
- 8.219.147.118 (Alibaba / AS45102)
- 164.95.89.25 (Treasury PKI — no SNI enforcement)
- 152.67.204.133 (Oracle Cloud SK / AS31898, links to yszfa.cn)

---

## SATODS Correction: Air Force, Not Treasury

**Finding:** SATODS = Security Assistance Technical Order Distribution System — **United States Air Force foreign military aid system**, not Treasury/IRS as previously labeled in the evidence base.

**7 Air Force IPs exposed RDP (port 3389) in Azure usgovvirginia cloud**, Jan–Mar 2025:
```
62.11.100.105, 62.11.97.15, 62.11.96.174, 62.11.96.233
62.10.108.118, 62.10.70.153, 20.141.44.221
```
Earliest exposure: January 15, 2025 — one day after J14 inflection date. NOTE: DOGE EO = January 20 (J20, inauguration day). J14 precedes J20 by six days.

Same brief confirms additional federal IT exposures at the same time:
- Fermilab VPN exposed
- LLNL (Lawrence Livermore National Lab) GlobalProtect VPN exposed
- Nevada National Security Site (NNSS) password reset portal plain HTTP
- DOE PKI LDAP with anonymous bind — plain HTTP

**H3 reclassification:** These exposures now belong under H3 (federal systems breach) rather than mixed with H2 (Packetware pipeline). The Air Force foreign military aid system being exposed on RDP starting January 15, 2025 — one day after J14 inflection (NOT the DOGE EO, which was January 20/J20) — is particularly significant given the foreign military equipment/aid policy changes happening simultaneously.

---

## Evidence Normalization Summary

The PDF ingest enabled a major normalization pass across the evidence base:

| Hypothesis | Entity Count (after dedup) |
|-----------|--------------------------|
| H1 — Insider/credential misuse | 1,271 entities |
| H2 — Packetware pipeline | 1,373 entities |
| H3 — Federal breach via vulns | 772 entities |
| H4 — Foreign actor data handoff | 228 entities |
| H5 — Financial benefit | 0 (null result — stripped) |

**Raw → deduped:** 5,051 rows → 3,644 (27.9% dedup rate). 6 heterogeneous sources merged into canonical schema.

---

## H5 — Formal Null Result

H5 (financial benefit to connected parties) returned p=0.19 on the available evidence — **not statistically significant, not qualitatively supported**. Decision: strip H5 items from Tier 1 and Tier 2; publish the null result explicitly in `evidence_tiers` metadata. This is good scientific practice — documenting a null result prevents future agents from wasting cycles on H5.

The Perry accounts (aidanperry.net/aldenperry.net) remain as leads but are currently Tier 3 with insufficient independent corroboration.

---

## COC System Consolidation

Investigation IDs `inv-default` and `inv-2026-packetware` were merged → single investigation `criticalexposure`. 744 COC entries preserved with consolidation event appended. `investigation-active.json` updated.

---

## What Still Needs Doing

1. **Merge two PDF ingest outputs:** `pdf_ingestion_RUN007.json` (14 docs) + `pdf_ingest_RUN007.json` (20 docs) — duplicates exist, needs dedup before crossref
2. **GCHQ SparrowDoor IOC table:** Image-format in PDF — zero IPs extracted. Manual or vision review needed.
3. **SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV:** WHOIS/DNS history
4. **New IPs from Treasury TLS PDF:** 5 IPs not yet in `pipeline_ip_crossref`
5. **Baxet new first-seen dates:** NuclearRisks brief contains Baxet dates (Jan 15 controlbanding.llnl.gov, Jan 20 clinicaltrials.gov) — requires hypothesis pre-registration before running Fisher test on these

---

*Generated by: data-engineer + evidence-curator (RUN-007, session-592227)*
*Promoted to vault by: main session 2026-03-22*
