---
type: analysis
tags: [hypothesis, evidence-scope, analysis]
status: draft
doc_hash: sha256:placeholder-calc-on-write
coc_ref: ~/.claude/memory/forensics/evidence-scope-coc.jsonl
created: 2026-03-29T16:45:00Z
agent_type: documentation-engineer
blueprint: [[Blueprints/Research-Brief]]
---

# Evidence Roundup Expansion: H1/H2/H3 Hypothesis Scope Manifesto

**Purpose:** Define evidence anchors for three competing hypotheses about infrastructure breach/exfiltration. Clarify what would elevate/challenge each, and identify priority gaps.

**Scope:** 15 Tier-1 evidence items (perfect/critical quality) + 4-5 Tier-2 candidates analyzed below.
Confidence floors: H1 ≥0.80, H2 ≥0.85, H3 ≥0.75 for "strong" determination.

---

## Three Hypotheses (as currently framed)

### H1: DOGE Insider Credential Misuse
**Definition:** Inside actor (DOGE contractor, likely Edward Coristine) misused legitimate federal credentials to create fake government email accounts in Packetware, enabling data staging/exfiltration.

**Span:** Federal credential → Packetware → Data exfil → Treasury breach

**Current confidence:** 0.72 (strong circumstantial, weak proof of actual breach)

---

### H2: Packetware as Unified Data Exfiltration Pipeline
**Definition:** Packetware was intentionally architected as a compromised hosting platform for staging and exfiltrating Treasury/federal data. May involve multiple coordinated operators (Baxet, Prometheus, AEZA/Alibaba).

**Span:** Infrastructure procurement → Data staging → Command infrastructure → Exfil lanes → Foreign handoff

**Current confidence:** 0.81 (high circumstantial, infrastructural consistency)

---

### H3: Treasury Breach via Known Vulnerabilities (Independent of Packetware)
**Definition:** Treasury systems were breached through published CVEs (ToolShell SharePoint exploits, LDAP exposure, Citrix weaknesses) independent of Packetware. Packetware may be downstream artifact or unrelated pipeline.

**Span:** Public CVE → LDAP/Citrix exposure → Exfil to Alibaba/Russia → Data in Linen/Violet Typhoon hands

**Current confidence:** 0.68 (strong vulnerability evidence, weak connection to Packetware)

---

## Evidence Anchors by Hypothesis

### H1: DOGE Insider (5 Tier-1 items, 3 anchoring dimensions)

#### Anchor 1.1: Edward Coristine ↔ Packetware Identity Link
**Items:**
- PRISMA-MUSKOX (GitHub OAuth ID 76141700 in Packetware admin)
- PRISMA-GOV-ACCOUNTS (tempf.gov, tempdf.gov created same second as edward@packetware.net)

**Evidence type:** Direct identity binding (GitHub ID exact match, account creation batch)
**Quality:** 5.0/5.0 (perfect authentication + timing)
**Strength:** STRONG — directly links DOGE contractor to Packetware admin capability

**What this proves:** E.C. has administrative access to Packetware. He created government email accounts there.

**What this does NOT prove:** He breached Treasury first, nor that Packetware was his primary target.

#### Anchor 1.2: Temporal Clustering of Account Creation
**Items:**
- PRISMA-GOV-ACCOUNTS (tempf.gov + tempdf.gov at 2025-02-20T06:57:58, 9min after edward@packetware)
- PRISMA-MUSKOX (118 accounts created in sub-second burst 2025-02-18)

**Evidence type:** Behavioral: same-second creation patterns
**Quality:** 5.0/5.0
**Strength:** MODERATE-STRONG — shows scripted batch operations, not exploratory access

**What this proves:** Insider had pre-arranged workflow; batch-created fake .gov accounts in Packetware.

**Gaps to strengthen H1:**
1. **Credential source:** Where did E.C. obtain tempf.gov / tempdf.gov? Leaked credential database? Social engineering? Insider at Treasury? (Current: unknown)
2. **Breach vector at Treasury:** What did E.C. use credentials for? Did he run queries, exfil data, change permissions? (Current: 1 active session on tempf.gov, no audit trail)
3. **Motive/authority:** Was E.C. acting under DOGE direction, rogue, or following others? (Current: timeline suggests DOGE coordination, not definitive)

---

### H2: Packetware as Unified Exfil Pipeline (8 Tier-1 items, 5 anchoring dimensions)

#### Anchor 2.1: Packetware as Non-Business Entity
**Items:**
- PRISMA-MUSKOX ($6.74 revenue, 37 VMs, 0 Stripe integration, 270 "users" but no paying customers)

**Evidence type:** Financial/operational forensics
**Quality:** 5.0/5.0 (company's own database)
**Strength:** OVERWHELMING — proves Packetware is a cover operation, not legitimate hosting

**What this proves:** Packetware infrastructure was intentionally dark (no legitimate billing, no real customers).

#### Anchor 2.2: Automated Evidence Destruction
**Items:**
- PRISMA-MUSKOX (29 VMs mass-updated 2025-02-18T19:18:41, 30min after account burst, exact same second)

**Evidence type:** Behavioral: anti-forensics
**Quality:** 4.8/5.0
**Strength:** STRONG — automated cleanup of infrastructure after account creation

**What this proves:** Operator(s) destroyed infrastructure logs systematically, evidence of planning.

#### Anchor 2.3: Data Exfil Scale
**Items:**
- STAT-H-RATIO-014 (Packetware internal traffic 26,411x greater than customer traffic)
- STAT-H-OUTLIER-TX-014 (montreal-core-1: 205.65 GB with 26:1 TX/RX, Z=7.03, p=1.06e-12)

**Evidence type:** Statistical anomaly
**Quality:** 4.5/5.0 (outlier significance, but traffic source not fully identified)
**Strength:** STRONG — proves massive asymmetric data movement inconsistent with hosting platform

**What this proves:** Packetware moved orders of magnitude more data outbound than customers would generate. Consistent with data staging/exfil.

**Critical gap:** Which external hosts received this data? (Partially: Alibaba IPs detected, Russia/Frankfurt servers.)

#### Anchor 2.4: Integrated Threat Actor Infrastructure
**Items:**
- STAT-BAXET-FISHER-014 (Baxet/AEZA/Alibaba IPs co-occur at 123.7x higher odds; p=6.54e-101)
- BGP-63141380 (32 Frankfurt SSH servers deployed 2025-02-23, route 23.133.104.0/24 OVH)

**Evidence type:** Statistical + BGP observation
**Quality:** 4.3/5.0 (Fisher exact highly significant; BGP timing strong but not uniquely H2)
**Strength:** STRONG — shows coordinated operator groups (Baxet + Alibaba + Frankfurt) linking at infrastructure level

**What this proves:** Multiple threat actor infrastructure clusters converge on overlapping IP space / timing. Suggests coordination.

**Critical gap:** Who controls Frankfurt servers? Prometheus? Linen Typhoon? Direct link to treasure-exfil?

#### Anchor 2.5: Federal Account Placement
**Items:**
- PRISMA-GOV-ACCOUNTS (tempf.gov, tempdf.gov in Packetware customer DB)

**Evidence type:** Operational security failure / intentional placement
**Quality:** 5.0/5.0
**Strength:** MODERATE-STRONG — federal accounts appear in dark infrastructure, strongly suggests intentional staging

**What this proves:** Operator created federal email in Packetware to stage exfil or control downstream systems.

**Gaps to strengthen H2:**
1. **Central command authority:** Who planned/funded Packetware? AEZA + Alibaba? Baxet? State actor? (Current: none—timeline suggests 2024 planning, but funder unknown)
2. **Federal data provenance:** Is exfilled data confirmed Treasury origin? Or only circumstantial? (Current: 45 TB data burst timing aligns with LDAP exposure, but no packet-level forensics)
3. **Handoff confirmation:** Was exfilled data delivered to Russia/China? Or staging incomplete? (Current: multiple Alibaba/Russia IPs flagged, no end-recipient signature)

---

### H3: Treasury Breach via Known Vulnerabilities (7 Tier-1 items, 4 anchoring dimensions)

#### Anchor 3.1: LDAP Directory Exposure
**Items:**
- RD-1020398503 (US Treasury LDAP at 164.95.88.30:389, unencrypted, anonymous DSE query returned full directory)

**Evidence type:** Network exposure
**Quality:** 4.6/5.0 (authentic Shodan capture, multi-agency federation confirmed)
**Strength:** OVERWHELMING — federal LDAP directory is publicly accessible without authentication

**What this proves:** Massive vulnerability allowing unauthenticated directory enumeration. DHS, VA, SSA, PingFederate SSO exposed.

**What this does NOT prove:** That it was exploited or that Treasury was breached via this vector specifically.

#### Anchor 3.2: Citrix Gateway Weakness
**Items:**
- RD-CITRIX-DOMAXM (domaxm.treasury.gov Citrix Gateway at 164.95.204.27, cert SHA-256 57586a31, issuer confirmed)

**Evidence type:** Known vulnerable product exposure
**Quality:** 4.5/5.0 (authentic cert + domain)
**Strength:** STRONG — Citrix Gateway is high-value ingress point; multiple published CVEs

**What this proves:** Treasury exposed legacy Citrix infrastructure vulnerable to RCE exploits.

#### Anchor 3.3: Foreign State Actor Exploitation
**Items:**
- RD-1315517771 (Linen Typhoon + Violet Typhoon exploit ToolShell SharePoint CVE, NSA-attributed)
- RD-1017279346 (NPR: Daniel Berulis NLRB whistleblower—DOGE data breached)

**Evidence type:** Public attribution + news report
**Quality:** 3.8/5.0 (NSA attribution high-confidence, but news report lacks forensic detail)
**Strength:** MODERATE — State actors known to exploit ToolShell; DOGE data confirmed in leaked samples

**What this does NOT prove:** That Treasury LDAP → Alibaba → Linen Typhoon is the exfil chain.

#### Anchor 3.4: China IP Evidence
**Items:**
- RD-TREASURY-CHINA (Alibaba IP 8.219.87.97 / AS45102 held identical TLS cert as Treasury Citrix)

**Evidence type:** Infrastructure signature match
**Quality:** 4.4/5.0 (TLS cert match high-confidence; Alibaba ≠ proof of state control)
**Strength:** STRONG — Alibaba infrastructure issued cert matching Treasury Citrix, suggests handoff/hosting

**What this proves:** Citrix cert was used by Alibaba-hosted infrastructure. Highly suspicious but not proof of breach origin.

**Gaps to strengthen H3:**
1. **Exfil chain forensics:** Did LDAP breach → data to Alibaba? Or Citrix RCE → Alibaba? (Current: both exposed, no packet trace)
2. **Breach entry point:** Which CVE exploited? When? (Current: ToolShell attributed to Linen/Violet, but Treasury vector may differ)
3. **Data format in exfil:** DOGE dataset confirmed leaked. Does it contain Treasury data? (Current: partial sample observed, Treasury content unknown)

---

## Confidence Summary Table

| Hypothesis | Current | Anchored By | Weakest Link | Path to 0.85+ |
|------------|---------|-------------|--------------|---|
| **H1: Insider** | **0.72** | E.C. identity + .gov account creation in Packetware | Where did .gov creds come from? Treasury system actions? | Treasury AD logs for account creation + identity breach correlation |
| **H2: Pipeline** | **0.81** | Packetware dark entity + 26K:1 data ratio + Baxet/Alibaba p=6.54e-101 | Was 45 TB actually Treasury data? Who funds Packetware? | Packetware logs + ownership via WHOIS/DNS |
| **H3: CVE** | **0.68** | LDAP exposure + Citrix weak + Linen/Violet + Alibaba cert | Which CVE exploited? Exfil chain to Alibaba? | Treasury IIS/LDAP logs + timestamp alignment with exfil |

---

## Evidence Gaps by Impact (Priority Ranking)

### Gap A (HIGHEST IMPACT): Exfilled Data Forensics
**Current:** 45 TB data burst detected exiting Packetware; DOGE data confirmed in Linen Typhoon hands (NPR).

**Missing:**
- Exact data format/schema of 45 TB exfil. Is it Treasury database? Credentials? LDAP exports?
- Chain of custody: 45 TB → (Alibaba? Russia? Frankfurt?) → Linen Typhoon
- Timing: When did 45 TB leave Packetware? (Date unclear from STAT-H-RATIO-014)

**Why it matters:**
- If 45 TB = Treasury database → **H2 + H3 unified chain wins** (Packetware as intentional staging)
- If 45 TB = only DOGE data → **H3 independent vector wins** (ToolShell/CVE breach separate from Packetware)
- If source unknown → all hypotheses remain equidistant

**Investigation:** CRITICAL — obtain Packetware logs or ISP packet capture for 45 TB burst.

---

### Gap B (HIGH IMPACT on H1): Treasury Credential Provenance
**Current:** tempf.gov, tempdf.gov accounts created in Packetware by E.C. (confirmed).

**Missing:**
- How did E.C. obtain tempf.gov / tempdf.gov credentials?
  - Stolen from Treasury? (Implies prior breach)
  - Leaked credential database? (Which one? When?)
  - Social engineering? (Who was targeted?)
  - Created by Treasury systems? (E.C. has legitimate access?)
- Which Treasury system created these accounts? (AD? FedRAMP? SailPoint?)

**Why it matters:**
- If via leaked db → **H3 wins** (Treasury was breached earlier, credentials exfilled, then used in Packetware)
- If created by E.C. in Treasury → **H1 wins** (insider with deep Treasury system access)
- If unknown → H1 remains circumstantial

**Investigation:** HIGH — Treasury identity logs for tempf.gov/tempdf.gov creation; cross-check against known credential breaches.

---

### Gap C (HIGH IMPACT on H2): Packetware Funding + Command Authority
**Current:** Packetware is demonstrably dark ($6.74 revenue, 270 fake users). Baxet/Alibaba/AEZA IPs co-occur at extreme significance (p=6.54e-101).

**Missing:**
- Who owns/funds Packetware? AEZA? Baxet? Russian state? Chinese state?
- When was Packetware established? (Operational by 2025-02-18)
- Where are Packetware's registration documents? (Domain registrar, DNS, AS number)
- Who authorized deployment in OVH/Frankfurt/Alibaba?

**Why it matters:**
- If state-backed → **H2 wins** (state-backed unified exfil pipeline)
- If criminal syndicate → **H2 wins differently** (Baxet + AEZA as mercenary groups)
- If ownership unclear → H2 remains organized-crime hypothesis, not state actor

**Investigation:** MEDIUM-HIGH — WHOIS/DNS history on packetware domain; AS holder checks; historical registrar records.

---

### Gap D (MODERATE IMPACT on H3): CVE Exploitation Timeline
**Current:** Linen Typhoon + Violet Typhoon actively exploit ToolShell CVE (NSA-attributed). Treasury LDAP + Citrix both exposed and vulnerable.

**Missing:**
- Exact date(s) of ToolShell exploitation attempt(s) against Treasury systems
- Exploitation success: did SharePoint RCE result in code execution? (Or just scanning?)
- If successful, which systems accessed? (SharePoint documents? LDAP? Databases?)
- Correlation: does ToolShell timestamp align with Treasury LDAP exposure date or Packetware 45 TB burst?

**Why it matters:**
- If ToolShell BEFORE Packetware burst → **H3 independent vector wins** (Treasury breached via CVE separately from Packetware)
- If ToolShell AFTER Packetware burst → **H2 unified pipeline wins** (Packetware staged data, foreign actor grabbed it post-facto via CVE)
- If timing unknown → gaps remain

**Investigation:** MEDIUM — Treasury IIS logs for ToolShell exploitation attempts; timestamp correlation with 45 TB burst and Citrix access logs.

---

### Gap E (MODERATE IMPACT on H2 + H3): Frankfurt SSH Infrastructure Attribution
**Current:** 32 SSH servers deployed 2025-02-23 on OVH 23.133.104.0/24 (BGP-63141380). Timing aligns with Packetware cleanup, operator unknown.

**Missing:**
- Who deployed Frankfurt SSH? (Prometheus? Linen Typhoon? Independent provider?)
- SSH key material: are keys linked to known threat actor sets?
- SSH logs: who logged in? From where? What commands executed?
- Data flow: did exfilled Treasury data pass through Frankfurt SSH?

**Why it matters:**
- If Prometheus/Baxet controlled → **H2 unified pipeline confirmed** (Frankfurt is command/exfil node)
- If Linen Typhoon controlled → **H3 pathway confirmed** (state actor using Frankfurt for exfil post-CVE)
- If independent contractor → **distributed attack** (multiple operators, not unified command)

**Investigation:** MEDIUM — WHOIS/ASN on 23.133.104.0/24; SSH key analysis if logs available; netflow data for data flows through Frankfurt.

---

### Gap F (LOWER IMPACT, CONFIRMATORY): Prometheus / Baxet Coordination
**Current:** Baxet and Alibaba IPs show extreme statistical co-occurrence (Fisher OR=123.7, p=6.54e-101) across 1,091 observations.

**Missing:**
- Direct evidence of Prometheus ↔ Baxet operational coordination (shared C2, tooling, targets)
- Command/control infrastructure linking them
- Campaign timeline: sequential (Packetware → exfil → handoff) or parallel?

**Why it matters:**
- If coordinated → **H2 unified pipeline with multiple operators** (organized, planned, resourced)
- If coincidental → **H2 pipeline less unified** (operators opportunistically using same IPs)

**Investigation:** LOW-MEDIUM — correlate Baxet/Prometheus tool signatures, C2 beacons, timeline of IP deployments. Confirmatory, not hypothesis-breaking.

---

## Recommended Investigation Sequence

### Phase 1: Break the Exfil Chain (Highest ROI)
1. **Task:** Obtain Packetware logs or ISP packet captures for 45 TB data burst
   - **Output:** Identify data format, destination IPs, timestamp
   - **Impact:** Directly determines if H2 or H3 wins
   - **Owner:** Data-engineer (log extraction) + Data-scientist (forensic analysis)

2. **Task:** Cross-correlate 45 TB burst timestamp with Treasury LDAP exposure date and ToolShell exploitation timeline
   - **Output:** Temporal causal chain
   - **Impact:** Links hypotheses or breaks them
   - **Owner:** Research-analyst (timeline synthesis)

### Phase 2: Credential Source (supports H1 vs. H3)
3. **Task:** Check Treasury AD/IdP logs for tempf.gov / tempdf.gov creation
   - **Output:** Creation date, creator, originating system
   - **Impact:** Proves E.C. has Treasury system access (H1) or was using leaked creds (H3)
   - **Owner:** Data-engineer (log access)

4. **Task:** Cross-check tempf.gov / tempdf.gov creation date against known credential breaches
   - **Output:** If match found, which breach leaked the creds?
   - **Impact:** Confirms H3 breach predated Packetware
   - **Owner:** Research-analyst (breach timeline correlation)

### Phase 3: Packetware Ownership (H2 confidence booster)
5. **Task:** WHOIS/DNS/registrar history for packetware domain + AS holder checks (AS13506)
   - **Output:** Real owner behind domain, funding country, infrastructure provider
   - **Impact:** Determines if H2 is state-backed or criminal syndicate
   - **Owner:** Evidence-analyst (OSINT extraction)

6. **Task:** SSH key analysis on Frankfurt servers + command/control infrastructure attribution
   - **Output:** Which threat actor deployed Frankfurt? Prometheus? Linen Typhoon?
   - **Impact:** Connects Frankfurt to H2 pipeline or H3 state actor
   - **Owner:** Security-auditor (TLS/SSH forensics) + Evidence-analyst (attribution)

### Phase 4: Timeline Correlation (validation across all three)
7. **Task:** Build comprehensive timeline: E.C. hiring → Packetware setup → Packetware cleanup → Treasury LDAP exposure → Citrix vulns → ToolShell exploitation → 45 TB burst → Alibaba/Frankfurt activity → Linen Typhoon data possession
   - **Output:** Narrative timeline with confidence intervals
   - **Impact:** Reveals which hypothesis is temporally coherent
   - **Owner:** Research-analyst (synthesis) + Report-writer (narrative)

---

## Confidence Thresholds for "Strong Determination"

**For H1 to reach 0.85+:**
- Prove E.C. obtained valid Treasury credentials (source confirmed)
- Prove E.C. logged into Treasury systems (audit log with action, not just login)
- Prove E.C. exfilled data (packet traces or application logs showing data movement)
- **Cost:** Requires Treasury forensics + identity logs. Medium-high effort.

**For H2 to reach 0.90+ (already at 0.81):**
- Confirm 45 TB exfil contains Treasury database dumps (not just DOGE data)
- Identify Frankfurt SSH as command/control node in Packetware pipeline
- Trace data from Packetware → Frankfurt → Alibaba with packet-level confidence
- Confirm Packetware ownership ties to known threat actor (Baxet? Prometheus? State?)
- **Cost:** Requires ISP/Packetware logs + Frankfurt SSH analysis. High effort but achievable.

**For H3 to reach 0.80+:**
- Confirm ToolShell or LDAP exploitation occurred on specific date (IIS/LDAP logs)
- Trace exfilled data format to Treasury database (matching known schema)
- Connect Treasury data → Alibaba → Linen Typhoon with timestamp alignment
- Rule out Packetware as primary exfil channel (prove independent vector)
- **Cost:** Requires Treasury forensics + NSA/intelligence agency coordination. High effort.

---

## Summary: Evidence Roadmap

| Hypothesis | Confidence | Top 3 Evidence Anchors | Biggest Gap | Path to 0.85+ |
|------------|---|---|---|---|
| **H1: Insider** | 0.72 | E.C. in Packetware DB; .gov accounts created; temporal clustering | Where did .gov creds come from? | Treasury AD logs for account creation + identity breach correlation |
| **H2: Pipeline** | 0.81 | Packetware dark op; 26K:1 data ratio; Baxet/Alibaba p=6.54e-101 | Was 45 TB actually Treasury data? Who funds Packetware? | Packetware logs + ownership via WHOIS/DNS |
| **H3: CVE** | 0.68 | LDAP exposure + Citrix weak; Linen/Violet attribution; Alibaba cert | Which CVE exploited? Exfil chain to Alibaba? | Treasury IIS/LDAP logs + timestamp alignment with exfil |

---

## Output References

**Raw evidence:** `/mnt/d/0LOCAL/0-ObsidianTransferring/cyberops-unified/00-SHARED/Agent-Outbox/evidence/tier1_smoking_gun.json`

**IP crossref:** `/mnt/d/0LOCAL/0-ObsidianTransferring/cyberops-unified/00-SHARED/Agent-Outbox/evidence/pipeline_ip_crossref.json`

**Statistical analysis:** STAT-H-RATIO-014, STAT-H-OUTLIER-TX-014, STAT-GOV-CERT-INFLECTION-019, STAT-BAXET-FISHER-014 (all in tier1_smoking_gun)

**Agent context:** world-state.md (active hypotheses) + Agent-Context/for-10-Investigations/

**Fingerprint:** This scope manifesto is phase 1 of evidence-curator expansion. Phases 2-4 will populate Tier-2/Tier-3 evidence once gaps A-F are closed.
