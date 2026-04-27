---
type: analysis
tags: [gaps, investigation-priorities, evidence]
status: draft
created: 2026-03-29T16:50:00Z
agent_type: evidence-curator
blueprint: [[Blueprints/Research-Brief]]
---

# Evidence Gaps and Investigative Priorities

## Executive Summary

**Gap A (Exfilled Data Forensics)** blocks all three hypotheses from confident determination. Closing this gap is the highest-ROI activity — it directly answers whether Packetware was the exfil vector (H2) or a side effect of an independent Treasury breach (H3). **Investigation priority: CRITICAL.**

**Gaps B-D** (Credential provenance, Packetware ownership, CVE timeline) are hypothesis-specific differentiators. They determine which of the three competing narratives is most consistent with the evidence.

**Gaps E-F** are confirmatory/refinement — they validate the leading hypothesis once the top three gaps are closed.

---

## Gap Impact Matrix

```
                     Impact on H1    Impact on H2    Impact on H3    Effort    Priority
Gap A (Exfil data)       LOW          CRITICAL        CRITICAL        HARD      CRITICAL
Gap B (Cred source)      CRITICAL     LOW             CRITICAL        MEDIUM    HIGH
Gap C (Pkg ownership)    LOW          CRITICAL        LOW             HARD      HIGH
Gap D (CVE timeline)     MEDIUM       HIGH            CRITICAL        HARD      MEDIUM
Gap E (Frankfurt SSH)    LOW          HIGH            MEDIUM           MEDIUM    MEDIUM
Gap F (Baxet coord)      LOW          MEDIUM          LOW              LOW       LOW
```

---

## Gap A: Exfilled Data Forensics (CRITICAL)

### Current State
- 45 TB data burst detected exiting Packetware infrastructure at ~1 Gbps sustained over 12 hours
- Destination IPs detected include Alibaba (8.219.87.97) and Frankfurt SSH cluster (23.133.104.0/24)
- DOGE dataset confirmed in Linen Typhoon hands per NPR/Daniel Berulis whistleblower report
- Timing: data burst observed, but exact date not clearly stated in STAT-H-RATIO-014

### What's Missing
1. **Data format identification:** Was the 45 TB exfil actual Treasury database dumps (SQL exports, LDAP directory, file archives)? Or only DOGE data?
   - **How to close:** Obtain Packetware host logs (syslog, bash history, application logs) or ISP packet capture (DPI analysis of exfil payload)
   - **Expected output:** MIME type, schema signature, table structures, archive format
   - **Confidence boost:** 20% (if Treasury data confirmed in 45 TB)

2. **Temporal alignment:** When exactly did 45 TB leave Packetware? Does it correlate with:
   - Treasury LDAP exposure discovery date?
   - Citrix CVE exploitation attempts?
   - ToolShell SharePoint exploitation by Linen Typhoon?
   - **How to close:** ISP flow logs (NetFlow v5/v9), Packetware egress firewall logs
   - **Expected output:** Timestamp, source IPs, destination IPs, byte count
   - **Confidence boost:** 25% (if correlation is strong)

3. **Destination mapping:** Did 45 TB go to Alibaba, Frankfurt, or elsewhere? Multi-hop or direct?
   - **How to close:** ISP BGP logs, Alibaba/OVH incident response, Frankfurt SSH server access logs
   - **Expected output:** Reverse-path trace, intermediate hops, final destination
   - **Confidence boost:** 15% (if chain is unbroken)

### Why It Matters
- **If 45 TB = Treasury database → H2 + H3 unified chain wins** (Packetware + CVE breach converged into single exfil path)
- **If 45 TB = only DOGE data → H3 independent vector wins** (Packetware is a red herring; CVE breach is the actual vector)
- **If unknown → all hypotheses remain equidistant** (no discriminating evidence)

### Investigation Owner
**Data-engineer** (log extraction + forensics) + **Data-scientist** (statistical correlation of timestamps)

### Estimated Effort
- Packetware logs: 4-8 hours (if available), 0 hours (if destroyed or unavailable)
- ISP packet capture reconstruction: 8-16 hours (if available from ISP)
- Data format analysis: 2-4 hours
- **Total: 14-28 hours IF logs exist; 4 hours if confirmed destroyed**

### Expected Output
JSON manifest with fields:
```
{
  "exfil_event_id": "EX-20250218-001",
  "timestamp": "2025-02-18T19:18:41Z",
  "source_ips": ["192.168.1.1"],
  "destination_ips": ["8.219.87.97", "23.133.104.0/24"],
  "byte_count": 45000000000000,
  "data_format": "PostgreSQL_logical_backup | LDAP_LDIF | unknown",
  "data_schema_signature": "hash_of_first_100_MB_payload",
  "confidence": 0.85
}
```

---

## Gap B: Treasury Credential Provenance (HIGH Impact on H1 + H3)

### Current State
- tempf.gov and tempdf.gov accounts created in Packetware DB at 2025-02-20T06:57:58
- Created by Edward Coristine (Packetware admin, DOGE contractor, GitHub ID 76141700)
- These .gov accounts are **not legitimate Treasury accounts** (tempf/tempdf are non-standard domain patterns for federal agencies)
- **Hypothesis:** E.C. created fake .gov addresses to stage exfil or impersonate federal agencies

### What's Missing
1. **Did E.C. obtain real Treasury credentials first?**
   - Scenario A: E.C. stole valid Treasury credentials (from leaked breach, social engineering, insider network access)
   - Scenario B: E.C. never touched Treasury; tempf/tempdf are entirely fake, used for impersonation only
   - **How to close:** Packetware logs showing whether tempf.gov / tempdf.gov credentials were used to authenticate to any Treasury systems
   - **Expected output:** Authentication logs, source IPs, timestamp, success/failure
   - **Confidence boost:** 25% (if E.C. authenticated to Treasury)

2. **Where did the tempf.gov / tempdf.gov credentials come from originally?**
   - Scenario A: Leaked from previous Treasury breach (check: Equifax, MOVEit, SolarWinds, OWA compromise, etc.)
   - Scenario B: Social engineering attack on Treasury employee
   - Scenario C: E.C. created as completely fake credentials (no real identity behind them)
   - **How to close:** Treasury Active Directory logs for account creation (creation date, creator, originating system); cross-reference against known credential leak timelines
   - **Expected output:** Treasury AD account creation timestamp, creator account, originating system (which IdP or domain controller)
   - **Confidence boost:** 20% (if match to known breach); 30% (if created by Treasury admin under duress)

3. **Which Treasury systems accepted these credentials?**
   - **How to close:** Treasury access logs for all systems accepting tempf.gov or tempdf.gov logins (VPNs, web portals, databases, file shares)
   - **Expected output:** Access logs showing: timestamp, system accessed, data accessed, actions performed
   - **Confidence boost:** 35% (if E.C. accessed Treasury data; this directly proves H1)

### Why It Matters
- **If tempf/tempdf came from leaked Treasury breach → H3 wins** (Treasury was compromised earlier; E.C. reused leaked creds)
- **If tempf/tempdf created by E.C. as fake with no Treasury login → H1 + H2 wins** (E.C. is staging in Packetware, not accessing Treasury directly)
- **If tempf/tempdf authenticated to real Treasury systems and E.C. exfilled data → H1 CRITICAL WIN** (insider confirmed)

### Investigation Owner
**Data-engineer** (Treasury identity logs, authentication logs) + **Evidence-analyst** (breach timeline correlation)

### Estimated Effort
- Treasury Active Directory logs: 2-4 hours (requires Treasury cooperation, may be restricted)
- Treasury system access logs (VPN, web, database): 4-8 hours
- Credential breach correlation (Equifax, MOVEit, etc.): 2-4 hours
- **Total: 8-16 hours IF Treasury cooperates; higher if legal/FOIA required**

### Expected Output
JSON manifest:
```
{
  "credential_id": "tempf.gov",
  "created_in_packetware": "2025-02-20T06:57:58Z",
  "created_by_edward_coristine": true,
  "source_breach": "none_detected | leaked_breach_name | treasury_internal",
  "authenticated_to_treasury_systems": false | true,
  "treasury_systems_accessed": ["LDAP", "Citrix", "unknown"],
  "data_exfil_confirmed": false | true,
  "data_exfil_volume_gb": 0,
  "confidence": 0.XX
}
```

---

## Gap C: Packetware Funding + Command Authority (HIGH Impact on H2)

### Current State
- Packetware is definitively a dark operation: $6.74 revenue, 37 VMs, 270 "users" with zero legitimate customers
- No Stripe integration (no real payment processing)
- Likely operational since 2024 or early 2025
- Baxet + AEZA + Alibaba IPs co-occur at extreme statistical significance (p=6.54e-101)
- **Hypothesis:** Packetware was funded by state actor or criminal syndicate as intentional exfil pipeline

### What's Missing
1. **Who registered packetware.com / packetware domain?**
   - **How to close:** WHOIS historical records, registrar domain data, DNS registrar trails
   - **Expected output:** Registrant name, email, phone, registrar history, date registered
   - **Confidence boost:** 15% (if registrant is known threat actor); 10% (if behind privacy service); -5% (if legitimate shell company used)

2. **Who owns AS13506 (if Packetware operates its own AS)?** Or which hosting provider hosts Packetware IPs?
   - **How to close:** WHOIS AS lookup, BGP history, historical traceroutes, peering registry
   - **Expected output:** AS owner legal entity, founding date, peering partners, geographic location
   - **Confidence boost:** 20% (if AS owner is known adversary)

3. **What is the payment infrastructure behind Packetware?** (Who paid OVH, Alibaba, Digital Ocean, etc. for these VMs?)
   - **How to close:** Financial subpoena to cloud providers (OVH, Alibaba, DigitalOcean, Hetzner, etc.); obtain payment records (credit card, cryptocurrency, wire transfer)
   - **Expected output:** Invoice/receipt records, payment account owner, payment method
   - **Confidence boost:** 30% (if payment traces to known adversary); 15% (if cryptocurrency payment, confirms intent to obfuscate)

4. **When was Packetware actually established? When did it start operating?**
   - **How to close:** Domain creation date, first BGP announcement, first Shodan observation, first SSL certificate issuance
   - **Expected output:** Timeline of infrastructure deployment, correlation with Treasury LDAP exposure and data burst dates
   - **Confidence boost:** 10% (if timeline aligns with H2 planning period)

### Why It Matters
- **If Packetware funded by state actor (China/Russia) → H2 CRITICAL WIN** (confirms state-backed exfil pipeline)
- **If Packetware funded by criminal syndicate (Baxet, Prometheus) → H2 wins differently** (criminal-grade exfil, not state-grade)
- **If Packetware funded by unknown entity → H2 remains open** (could be state actor hiding identity, or criminal syndicate)

### Investigation Owner
**Evidence-analyst** (OSINT: WHOIS, DNS, registrar records) + **Data-engineer** (cloud provider subpoena coordination with law enforcement)

### Estimated Effort
- WHOIS + DNS history: 1-2 hours
- BGP historical analysis: 2-4 hours
- Cloud provider subpoena coordination: 4-8 hours (subject to legal process)
- Payment record analysis: 4-8 hours
- **Total: 11-22 hours IF legal subpoena authority available; 3-6 hours for OSINT-only**

### Expected Output
JSON manifest:
```
{
  "packetware_domain": "packetware.com",
  "registered_date": "2024-XX-XX or unknown",
  "registrant_name": "privacy_redacted | known_threat_actor_alias | legitimate_shell_co",
  "whois_email": "email@domain.com",
  "registered_with_privacy_service": true | false,
  "asn_if_applicable": "AS13506",
  "asn_owner": "unknown | known_adversary",
  "hosting_providers": ["OVH", "Alibaba", "DigitalOcean"],
  "payment_method": "credit_card | crypto | wire_transfer | unknown",
  "payment_account_owner": "unknown | known_adversary",
  "establishment_date_confidence": 0.XX
}
```

---

## Gap D: CVE Exploitation Timeline (MEDIUM-HIGH Impact on H3)

### Current State
- Treasury LDAP at 164.95.88.30:389 is publicly exposed and vulnerable to anonymous DSE query (unencrypted, unauthenticated)
- Treasury Citrix Gateway at domaxm.treasury.gov is vulnerable to known RCE exploits (CVE-2023-4966, CVE-2024-9496, etc.)
- Linen Typhoon + Violet Typhoon actively exploit ToolShell SharePoint (NSA-attributed)
- **Hypothesis:** Treasury was breached via one or more of these CVEs, independent of Packetware

### What's Missing
1. **When was LDAP first accessed from external IPs?**
   - **How to close:** Treasury network logs, Shodan historical scans (to determine when LDAP became public)
   - **Expected output:** First observed external access date, source IPs, success/failure
   - **Confidence boost:** 15% (if exploitation confirmed)

2. **Did Linen Typhoon or other state actors successfully exploit ToolShell against Treasury SharePoint?**
   - **How to close:** Treasury IIS logs, SharePoint audit logs, CISA advisories, NSA intelligence reporting
   - **Expected output:** Exploitation timestamp, source IP, success/failure, data accessed
   - **Confidence boost:** 30% (if successful exploitation confirmed)

3. **Did Citrix RCE exploits succeed against domaxm.treasury.gov?**
   - **How to close:** Citrix audit logs, NetScaler logs, Citrix AAA logs, incident response forensics
   - **Expected output:** Exploitation timestamp, source IP, shell access, commands executed
   - **Confidence boost:** 25% (if RCE success confirmed)

4. **Which CVE exploitation (if any) correlates temporally with 45 TB data burst?**
   - **How to close:** Timeline correlation: CVE exploitation date ↔ Packetware 45 TB burst date ↔ Alibaba/Frankfurt activity date
   - **Expected output:** Timeline sequence showing which event preceded others
   - **Confidence boost:** 20% (if strong temporal alignment); -10% (if CVE exploitation post-dated data burst)

### Why It Matters
- **If ToolShell / LDAP / Citrix exploitation occurred BEFORE 45 TB burst → H3 independent vector wins** (CVE breach precedes Packetware exfil)
- **If CVE exploitation occurred AFTER 45 TB burst → H2 unified pipeline wins** (Packetware exfil precedes foreign actor grab-and-go)
- **If no exploitation detected → H3 weakens, H2 strengthens** (Packetware may be primary vector, not CVE)

### Investigation Owner
**Data-engineer** (Treasury logs) + **Security-auditor** (Citrix/SharePoint forensics) + **Research-analyst** (timeline correlation)

### Estimated Effort
- Treasury IIS/SharePoint/LDAP logs: 4-8 hours
- Citrix audit log analysis: 2-4 hours
- Timeline correlation: 2-3 hours
- **Total: 8-15 hours IF Treasury cooperates; higher if FOIA required**

### Expected Output
JSON manifest:
```
{
  "cve_exploitation_events": [
    {
      "cve_id": "CVE-2023-29357",
      "product": "SharePoint",
      "timestamp": "2025-02-XX or unknown",
      "source_ip": "IP_of_attacker",
      "success": true | false,
      "data_accessed": ["unknown", "list_of_docs"],
      "confidence": 0.XX
    }
  ],
  "ldap_external_access_date": "2025-02-XX or unknown",
  "citrix_rce_success": true | false | unknown,
  "timeline_sequence": "ToolShell → LDAP → Citrix → Packetware_burst | Packetware_burst → ToolShell | unknown"
}
```

---

## Gap E: Frankfurt SSH Infrastructure Attribution (MEDIUM Priority, H2 + H3)

### Current State
- 32 SSH servers deployed 2025-02-23 on OVH 23.133.104.0/24 (BGP-63141380)
- Timing aligns with Packetware cleanup (2025-02-18), suggesting coordinated operations
- Operator unknown: could be Prometheus, Linen Typhoon, or independent contractor

### What's Missing
1. **SSH server deployment forensics:** Who allocated the IP block? When was BGP announced?
2. **SSH key material:** Are deployed keys linked to known threat actor sets (Baxet? Linen Typhoon)?
3. **SSH access logs:** Who logged in? From where? What commands? When?
4. **Data exfil through Frankfurt:** Did 45 TB pass through Frankfurt SSH servers?

### Investigation Owner
**Security-auditor** (SSH key analysis) + **Evidence-analyst** (OSINT: WHOIS/BGP) + **Data-engineer** (netflow analysis)

### Estimated Effort
- WHOIS/BGP: 1-2 hours
- SSH key analysis: 2-4 hours
- Netflow/packet analysis: 4-8 hours
- **Total: 7-14 hours**

---

## Gap F: Prometheus / Baxet Coordination (LOW Priority, Confirmatory)

### Current State
- Baxet and Alibaba IPs co-occur at 123.7x higher odds (p=6.54e-101)
- Suggests coordinated threat actor infrastructure, but lacks direct command/control evidence

### What's Missing
1. Shared C2 infrastructure
2. Shared tooling or malware signatures
3. Campaign coordination timeline

### Investigation Owner
**Evidence-analyst** (tool signature correlation) + **Research-analyst** (campaign timeline)

### Estimated Effort
- Tool signature correlation: 2-4 hours
- Campaign timeline: 2-3 hours
- **Total: 4-7 hours**

---

## Investigation Roadmap (Phased Approach)

### Phase 1: Gap A (Week 1) — Exfilled Data Forensics
**Goal:** Determine if 45 TB is Treasury data or DOGE data only.
**Owner:** Data-engineer + Data-scientist
**Deliverables:**
- Packetware logs forensics report (or destruction confirmation)
- ISP packet capture analysis (if available)
- Data format signature and destination mapping
**Success criteria:** Confidence ≥0.80 on data source and destination

### Phase 2: Gaps B + C (Week 2) — Credential Provenance + Packetware Ownership
**Goal:** Determine if H1 (insider) or H2 (unified pipeline) is primary vector.
**Owner:** Data-engineer (logs) + Evidence-analyst (OSINT)
**Deliverables:**
- Treasury credential provenance report
- Packetware ownership and funding investigation
- Payment infrastructure analysis
**Success criteria:** Identify Packetware funder or prove E.C. Treasury access

### Phase 3: Gap D (Week 2-3) — CVE Exploitation Timeline
**Goal:** Determine if H3 (CVE breach) is independent or downstream of H2 (Packetware).
**Owner:** Data-engineer + Security-auditor + Research-analyst
**Deliverables:**
- Treasury CVE exploitation forensics report
- Timeline correlation analysis
- Causal chain determination
**Success criteria:** Establish which event (CVE vs. Packetware) occurred first with ≥0.80 confidence

### Phase 4: Gaps E + F (Week 3-4) — Infrastructure Attribution + Coordination
**Goal:** Validate the leading hypothesis with infrastructure evidence.
**Owner:** Security-auditor + Evidence-analyst
**Deliverables:**
- Frankfurt SSH attribution report
- Prometheus/Baxet coordination analysis
- Final threat actor topology
**Success criteria:** Confirm Frankfurt operator and coordination level

### Phase 5: Timeline Synthesis (Week 4) — Final Narrative
**Goal:** Produce unified timeline showing which hypothesis is most consistent.
**Owner:** Research-analyst + Report-writer
**Deliverables:**
- Comprehensive timeline with confidence scores
- Hypothesis confidence updates (H1/H2/H3)
- Final determination and caveats
**Success criteria:** All three hypotheses ranked with ≥0.80 confidence, narrative is defensible

---

## Effort Estimates and Parallelization

**Total effort (sequential):** ~60-80 hours
**Total effort (maximum parallelization):** ~25-35 hours

**Parallelizable groups:**
- **Group 1 (Week 1):** Gap A (Packetware logs) + Gap C OSINT (WHOIS/DNS/BGP) = 8-10 hours
- **Group 2 (Week 2):** Gap B (Treasury logs) + Gap D (CVE timeline) + Gap C financials (subpoenas) = 15-20 hours
- **Group 3 (Week 3):** Gap E (Frankfurt SSH) + Gap F (Baxet coordination) = 10-15 hours
- **Group 4 (Week 4):** Timeline synthesis + final report = 5-8 hours

**Critical path:** Gap A (Packetware logs) + Gap D (CVE timeline) + Timeline synthesis = 18-25 hours

---

## Dependency Graph

```
Gap A (Exfil data) ──→ Gap D (CVE timeline) ──→ Phase 5 (Timeline synthesis)
                       ↗                        ↗
Gap B (Creds)  ──────────────────────────────→ 
                       ↗
Gap C (Ownership) ───→ Phase 5 (Confidence update)

Gap E (Frankfurt) ──→ Phase 4 (Infrastructure validation)
Gap F (Baxet) ──────→ Phase 4
```

**Critical path:** A → D → Phase 5 (minimum 18-25 hours to reach final determination)

---

## Recommended Task Queuing

```
IMMEDIATELY:
1. Data-engineer: Extract Packetware logs or ISP packet captures (Gap A)
2. Evidence-analyst: WHOIS/DNS/BGP historical research on Packetware (Gap C OSINT)

WEEK 2 (parallel):
3. Data-engineer: Request Treasury credential/access logs (Gap B)
4. Data-engineer: Request Treasury CVE exploitation logs (Gap D)
5. Security-auditor: Analyze SSH keys on Frankfurt servers (Gap E)

WEEK 3 (dependent on outputs from Week 2):
6. Research-analyst: Correlate timestamps and build timeline
7. Evidence-analyst: Identify Packetware funder via payment records (Gap C financials)

WEEK 4:
8. Research-analyst: Final timeline synthesis
9. Report-writer: Produce final narrative with confidence scores
```

---

## Risk Factors

**High risk:**
- Packetware logs may be destroyed (anti-forensics)
- Treasury logs may be classified or restricted from access
- Cloud provider subpoenas may require DOJ coordination

**Mitigation:**
- If Packetware logs destroyed, rely on ISP packet capture (if available) or statistical reconstruction
- If Treasury logs restricted, escalate to DOJ/IG for legal access
- Parallel: use OSINT (Shodan, DNS history, BGP) as supplementary evidence

---

**Status:** DRAFT - awaiting approval for Phase 1 launch
**Next:** Assign Data-engineer to Gap A (Packetware logs extraction) and Evidence-analyst to Gap C OSINT.
