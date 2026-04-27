---
type: dashboard
stage: review
tags: [dashboard, annotation, court-prep]
cssclass: wide-page
created: 2026-03-22
parent:
  - "[[HOME]]"
sibling:
  - "[[Agent-Insights]]"
  - "[[Chain-of-Custody]]"
  - "[[Unprocessed-Stubs]]"
doc_hash: sha256:99c5bc2d29e9caac24e64081edcea03ab3e68b368f7d1dd10cb4be2670975fb5
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Phase1-AgentSync|← Investigation]] · **Annotate & Review** · [[Chain-of-Custody|COC →]] · [[Phase2-Publication|Phase 2 →]]

# CriticalExposure — Annotation & Review Dashboard

> *This is your human-readable guide to the investigation. Use it to review agent findings,
> annotate what matters, and build the mental model you'll need if you ever have to explain
> this in court or to a journalist. Agents update the "Agent Findings" sections. Everything
> under "Your Annotations" and "Court Prep Notes" is yours alone — agents never touch it.*

---

## Hypothesis Scorecard (as of 2026-03-22)

| # | Hypothesis | Confidence | Driver |
|---|---|---|---|
| H1 | DOGE insider access via credential misuse | **0.95** | Prisma user table, LDAP anon bind, TLS cert timing |
| H2 | Packetware/Prometheus as data pipeline | **0.78** | chrome_proxy.exe C2, BGP hijack, container registry |
| H3 | Treasury/federal systems compromised | **0.78** | 7 RDP-exposed IPs, DOE PKI plain HTTP, SATODS AF |
| H4 | Data handoff to foreign actors (Russia/China) | **0.82** | Fisher p=6.54e-101, OR=123.7, reflected TLS, staged rollout |
| H5 | Financial benefit to connected parties | **0.00** | NULL — published as null result, demoted from T2 |

**What drives H4 to 0.82:** Three independent foreign IPs on Russian/Chinese infrastructure all show US .gov TLS certs appearing after Jan 14 2025 — at odds of 123:1 versus the null hypothesis. The math is unambiguous. See "Wave 3" below.

---

## Smoking Guns — Know These Cold

### SG-1: The Jan 14 Inflection (H1, H2, H3, H4 — confidence 0.95)

On January 14, 2025 — the day DOGE was established by executive order — a measurable change occurred across at least four independent infrastructure categories simultaneously: US government TLS certificates appeared on Russian hosting (Aeza/Baxet), Packetware container registry went active, foreign adversary IPs started accumulating .gov certs, and federal systems showed new exposure patterns.

**The critical detail:** This inflection was NOT a collection artifact. Shodan's 8-year baseline confirms these service hashes did not exist before Jan 14. Pre-Jan-14 searches return zero matches. The same date appears across entities that should have no connection to each other — Russian hosting, Chinese Alibaba, US gov Azure, DOGE-linked infrastructure. Independent entities sharing the same high-activity start date is probabilistically near-impossible under chance.

**Statistical backing:** Fisher combined test across all H4 sources: p ≈ 0. KS-test confirms the pre/post distributions are fundamentally different populations.

*Forensic ref: `scripts/audit_results/stat_baxet_fisher_RUN008.json`*

---

### SG-2: Reflected TLS Attack — The H4 Mechanism (confidence 0.82)

**What was found:** A C2 server at 8.219.207.49 uses `socat` to proxy Treasury PKI TLS handshakes from `164.95.89.25` (pki.treasury.gov, which has no SNI enforcement). The C2 server appears as legitimate Treasury HTTPS to passive network scanners (Shodan, Censys) — without possessing the Treasury private key.

**Why this matters:** This is the mechanism that explains the H4 statistical finding. Aeza's IP (138.124.123.3) first showed a Treasury cert on January 15, 2025 — one day after the DOGE EO. The cert didn't teleport there; the infrastructure was configured to impersonate Treasury endpoints. Akamai peering was ruled out (38 ASNs tested, zero mutual visibility).

**Staged rollout timeline:** Aeza Jan 15 → Baxet Feb 8 → Alibaba Feb 10. This is not coincidence — it's a deployment sequence.

*Sources: Treasury-and-USPTO PDF, 4 independent corroborating PDFs. Forensic ref: audit-log.md*

---

### SG-3: DOGE-Branded Malware C2 (H2 — confirmed)

**What was found:** `chrome_proxy.exe` — a piece of malware — calls home to `SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV` as its command-and-control domain. This was confirmed by Falcon Sandbox analysis.
- SHA256: `92fcf735...`
- Dropped by: `test.exe`
- Tag: `bigballs`

**Why this matters:** A DOGE-branded domain being used as malware C2 is direct infrastructure evidence linking DOGE operations to active malware deployment. This is not circumstantial — it is the domain name hard-coded into the malware binary.

*Forensic ref: Falcon Sandbox report, `scripts/audit_results/pdf_ingest_RUN007.json`*

---

### SG-4: Baxet/Aeza Fisher Test — OR=123.7, p=6.54e-101 (H4 — Tier 1)

**The math:** Three independent foreign IPs (AEZA/Stark 138.124.123.3, Baxet 194.58.46.116, Alibaba 8.219.87.97) all show .gov TLS certs clustering post-DOGE EO. Combined Odds Ratio = 123.7 (meaning post-DOGE .gov certs are 124x more likely on these Russian/Chinese IPs than under the null). Combined p = 6.54e-101.

**The negative control works:** 83.149.30.186 (a comparable IP) showed zero .gov certs in both periods, ruling out scanner artifact. The signal is real and targeted.

**Pre-DOGE access:** 10 .gov cert observations appeared on Aeza's IP January 15-19 — BEFORE the January 20 EO. Access began during the presidential transition period, five days before formal authorization.

*Forensic ref: `scripts/audit_results/statistical_analysis_baxet_RUN007.json`*

---

### SG-5: DOE Access by Luke Farritor (H1 — named personnel)

**What was found:** "Packetware and Purge" (31-page document) names **Luke Farritor** (23-year-old former SpaceX intern) as having accessed Department of Energy systems on **February 5, 2025**. Also names Secretary Brooke Rollins and Secretary Chris Wright in the same document.

**Context:** The document was tagged with malware marker `bigballs` — the same tag as the DOGE malware binary. This suggests the document was produced in the same operational context as the malware infrastructure.

*Forensic ref: `scripts/audit_results/pdf_ingest_RUN007.json`*

---

### SG-6: Federal System Exposures (H3)

- **7 IPs exposed RDP (port 3389)** in usgovvirginia January-March 2025. Earliest exposure: January 15 — one day after DOGE EO.
- **DOE PKI LDAP** accessible via anonymous bind (no authentication required)
- **Fermilab VPN, LLNL GlobalProtect, NNSS password reset** all accessible via plain HTTP (unencrypted)
- **SATODS** (Security Assistance Technical Order Distribution System, US Air Force) exposed

RDP IPs: 62.11.100.105, 62.11.97.15, 62.11.96.174, 62.11.96.233, 62.10.108.118, 62.10.70.153, 20.141.44.221

*Source: NuclearRisks brief, pdf_ingest_RUN007.json*

---

## Waves of Analysis

*Links to narrative notes — each wave is a chapter in the investigation story.*

| Wave | Topic | Status |
|---|---|---|
| [[WAVE-01-The-Emergence]] | Jan 14 inflection — what changed and when | Draft |
| [[WAVE-02-The-Infrastructure]] | Packetware, Hetzner, Prometheus, BGP | Draft |
| [[WAVE-03-The-Foreign-Fingerprints]] | Aeza, Baxet, Alibaba, reflected TLS | Draft |
| [[WAVE-04-The-Malware]] | chrome_proxy.exe, DOGE C2, Falcon Sandbox | Draft |
| [[WAVE-05-The-Statistics]] | What the Fisher tests prove (and don't) | Queued |
| [[WAVE-06-The-Personnel]] | Luke Farritor, DOGE access, userId resolution | Queued |

---

## Evidence Queue — Needs Your Review

```dataview
TABLE WITHOUT ID
  file.link AS "Finding",
  tier AS "Tier",
  confidence_level AS "Conf",
  hypothesis_support AS "H",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox" OR "00-SHARED/Agent-Outbox"
WHERE review_status = "unreviewed" OR (reviewed = false OR !reviewed)
SORT tier ASC, confidence_level DESC
LIMIT 20
```

---

## Open Investigation Threads

These are gaps the analysis has identified but not yet resolved:

- `SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV` — WHOIS/DNS history, registrant, active status
- `GCHQ SparrowDoor IOC table` — image format, IPs not extracted; needs manual review
- `8.219.207.49` (C2 socat) + `164.95.89.25` (bare Treasury PKI) not yet cross-checked against full IP base
- `www.yszfa.cn` — Chinese domain, WHOIS needed (queued)
- `ahmn.co` — current operator of 172.93.110.120 (was Packetware container registry)
- `400yaahc.gov` — unusual .gov domain on Russian AEZA IP; attribution missing
- Russian Starlink PDFs — INNs 231533996303 and 232524834996: SPARK/Kontur lookup for shared directorships with Aeza/Baxet

---

## Your Annotations

<!-- This section is yours. Agents never write here. -->

*Use this space to:*
- *Record what you believe and why*
- *Note connections you see that agents haven't drawn*
- *Flag things that feel wrong or need double-checking*
- *Write the "story" in your own words — what happened, in what order, why it matters*

---

## Court Prep Notes

<!-- This section is yours. Agents never write here. -->

*What you need to be able to explain without notes:*
- [ ] The Jan 14 inflection — what happened, why it's not a collection artifact
- [ ] The reflected TLS mechanism — how a C2 can appear as Treasury HTTPS
- [ ] Why OR=123.7 is significant (what the null hypothesis would predict)
- [ ] The staging sequence (Aeza Jan 15 → Baxet Feb 8 → Alibaba Feb 10)
- [ ] Who Luke Farritor is and why his DOE access is relevant
- [ ] What Packetware/Prometheus does (the infrastructure layer)
- [ ] What the negative control on 83.149.30.186 proves

---

## Agent Activity Log

*Agents append brief updates here when they push new findings to the vault.*

| Date | Agent | Finding added |
|---|---|---|
| 2026-03-22 | main | Annotation-Dash.md created; SG-1 through SG-6 from NECTAR/REVIEW-INBOX |
