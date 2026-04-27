---
type: meta
tags: []
doc_hash: sha256:de9f2e5e7f877baab6fdb8f6488d7cc50ed002f1bc94f77d90c5d6395a8d4180
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:33Z
hash_method: body-sha256-v1
---
# HONEY.md — CyberTemplate Project Memory
# Canonical investigation state. Last updated: 2026-03-20
# Format: crystallized facts organized by domain

---

## Investigation Overview

**Project:** Defenders-of-Democracy/cybertemplate
**Mission:** Document and publish evidence of infrastructure misuse, credential abuse, and potential foreign data handoff involving DOGE-connected entities and Packetware/Prometheus.
**Status:** Active (Tier 1: 90% ready, Tier 2: 82%, Tier 3: 28%)

---

## Active Hypotheses (Confidence by Evidence)

| ID | Hypothesis | Evidence Strength | Current Confidence | Status |
|----|-----------|--------------------|-------------------|--------|
| H1 | DOGE insider access via credential misuse | CRITICAL (Prisma DB + .gov domains) | 0.95 | CONFIRMED — Tier 1 |
| H2 | Packetware/Prometheus as data exfiltration pipeline | HIGH (Prometheus + BGP + SSH cluster) | 0.78 | SUPPORTED — evidence accumulating |
| H3 | Treasury/federal systems breached via known vulns | HIGH (LDAP exposure + cert matches) | 0.78 | SUPPORTED — LDAP confirmed |
| H4 | Data handoff to foreign actors | MEDIUM (Linen Typhoon NNSA, Wuhan) | 0.55 | SUGGESTIVE — needs 2nd source |
| H5 | Financial benefit to connected parties | NONE publishable | 0.00 | DO NOT PUBLISH — zero Tier 1 evidence |

**Movement:** H1 stable (critical), H3 ↑ (Treasury LDAP confirmation), H2/H4 accumulating support

---

## Evidence Inventory (Briefing Readiness)

- **Tier 1 (Smoking Gun):** 18/20 items (90%) ✅
  - Prisma DB records (.gov accounts + DOGE operators in same transaction)
  - .gov cert inflection Jan 14 2025 (p=8.88e-16)
  - Treasury LDAP exposure (164.95.88.30, DSE + SASL PLAIN)
  - ProxMox bulk update Feb 18 (P=1.0 programmatic)

- **Tier 2 (Strong):** 41/50 items (82%) ⏳
  - H-TEMPORAL (Feb 5 Cilium 6.28TB burst same-day DOGE, 89.5% Bayesian)
  - H-GOV-CERT per-IP (138.124.123.3 individually Bonferroni-significant)
  - China 12-month continuous cert hold (8.219.87.97, Alibaba)
  - 72h cert rotation (Treasury → Korea Oracle)

- **Tier 3 (Contextual):** 28/100 items (28%) ⏳
  - BGP announcements (63.141.38.0/24 hijacked from Continental)
  - Infrastructure enumeration (23 IPs across 5 ASNs)
  - Personnel links (Aidan Perry, Edward Coristine, Dylan High)
  - Timeline correlation (Jan 14 inflection across multiple signals)

---

## Critical Blockers (Stopping Publication)

- **B2 backup verification** — ProxMox video file recovery (cost+time unknown, URGENT)
- **Feb 18 motive determination** — deployment logs OR Prisma migration history to distinguish programmatic vs manual tampering
- **400yaahc.gov agency link** — congressional/IG attribution missing for credibility
- **H5 financial evidence** — Perry/Coristine account corroboration (if pursuing)

---

## Key Infrastructure Findings

**Packetware/AS400495 Core:**
- `63.141.38.0/24` — New Canaan CT (253 IPs, BGP HIJACKED, RPKI INVALID)
- `23.133.104.0/24` — Frankfurt OVH (70 IPs, SSH+HTTP, WITHDRAWN after use)
- `103.195.102.0/24` — APNIC, NOT in public WHOIS, $200/hr hourly billing
- AS400495 listed as "Reserved AS" — GameServerKings (AS26863) only peer

**Confirmed Packetware Nodes:**
- `65.108.96.185` — Hetzner Helsinki (mgmt: Coolify + Prisma unauth:5555)
- `172.93.110.120` — AS23470/ReliableSite Miami (container_registry_secondary, now ahmn.co)
- `8.219.87.97` — Alibaba China, Treasury wildcard cert 12 months continuous

**Treasury/Federal Exposure:**
- `164.95.88.80`, `164.95.204.27`, `164.95.10.134` — Treasury cert IPs
- `164.95.88.30`, `166.123.218.100` — LDAP PingFederate (unauthenticated DSE + SASL PLAIN, port 389, AS13506)
- Certs on adversary IPs: p=8.88e-16 (combined), p=1.53e-15 per-IP
- 8.219.87.97 NOT in Prisma entity graph — cert access is network-level, not via Packetware platform
- Post-rotation cert appeared on SK IPs (152.67.204.133, 217.142.144.30) linked to www.yszfa.cn

---

## Pending Gaps to Close (Before Publication)

- **ahmn.co registrant identity** — currently hostname of 172.93.110.120; WHOIS + MX needed
- **www.yszfa.cn registrant** — Chinese domain linked via DNS to SK IP 152.67.204.133 holding rotated Treasury cert; WHOIS needed
- **AS400495↔AS23470 BGP peering** — confirms infrastructure link
- **mrcomq identity** — needs second independent source (currently "The Com", unverified)
- **deployments logs access** — Feb 18 motive clarification (Prisma ORM vs manual update)
- **Congressional contact authority** — agency link for 400yaahc.gov classification

---

## Open Threads / Investigation Continuity

1. **registry2.anchored.host hostname rotation** — ahmn.co appeared 2026-03-12, mail.ahmn.co identity unknown. SSH fingerprint persists. H2+H4 hypothesis.
2. **China-Treasury cert connection** — 8.219.87.97 held wildcard cert continuously Mar 2024-Mar 2025. Why 12 months? Payment? State actor control?
3. **BGP peering topology** — 2 upstreams, 2 peers to AS400495. Confirm AS23470 peering for infrastructure link validation.

---

## Personnel Confirmed

- **Aidan Perry** — Primary technical operator, STAFF in Prisma, Google OAuth 100020367607980102252, aidanjperry@gmail.com, GitHub UltraSive
- **Edward Coristine** — CLIENT role, edward@packetware.net, WHOIS registrant packetware.net
- **Dylan High** — Systems Engineer (Prisma user table)
- **userId a45bkg9pb95tgb8** — Primary admin (35/37 VMs), 24 activity events, ADMIN memberships, Feb 18 mass account creation (IDENTITY RESOLVED post-typo)

---

## Next Session Actions

**IMMEDIATE (do first):**
1. Verify B2 bucket ProxMox video recovery status + cost
2. Retrieve ahmn.co WHOIS registrant + MX records
3. Confirm deployment logs for Feb 18 motive

**FOLLOW-UP:**
4. AS400495↔AS23470 BGP peering query (Hurricane Electric, RIPE)
5. mrcomq second-source search (Congressional/IG filings)
6. Tier 1 quality audit (18/20 items @4.0+)

**IF TIME:**
7. Financial evidence for H5 (if pursuing — currently DO NOT PUBLISH)
8. Perplexity/45.32.65.224 DOGE China link confirmation

---

## RUN016 — c5isr.dev Army DEVCOM Impersonation (2026-03-23)
- Domain: c5isr.dev — impersonates U.S. Army DEVCOM C5ISR Center
- git.c5isr.dev → 20.141.83.185 (Azure AS8070)
- mail.c5isr.dev → 20.141.187.124 (Azure AS8070)
- MiAB CONFIRMED: port 4190 (ManageSieve) open + self-hosted DNS (ns1/ns2 on same IP)
- Full parallel platform: Matrix, SSO, MDM, wiki, artifacts, cloud storage. Active Dec 2023+
- H1 support: Army impersonation infra = insider credential abuse vector
- Task: task-20260323-185306-e019 (registrant ID pending)

---

# Crystallization Notes
- Migrated from AGENTS.md (2026-03-20) to canonical HONEY.md format
- All findings with timestamps, confidence scores, and publication status
- Open threads link to queued sprint tasks automatically via `/handoff`
- Updates pushed to global HONEY.md findings on session crystallization
- Case data (IPs, domains, entities) lives HERE — never in global ~/.claude/memory/HONEY.md
