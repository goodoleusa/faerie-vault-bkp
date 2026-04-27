---
date: 2026-03-23
sprint: RUN009/010
status: unread
investigation: criticalexposure
hypothesis_codes: [H1, H2, H3, H4]
type: meta
tags: []
doc_hash: sha256:e86623e28b4f6ebd785c1688c3116e673c5a43c3170d0ef28f07cc2388eeec7b
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:16:31Z
hash_method: body-sha256-v1
---

# Sprint RUN009/010 — Key Findings

## LANL Nuclear Cert — SIGNIFICANT ⚠️

**dx10.lanl.gov** certificate (Los Alamos National Laboratory) detected on **Baxet/Stark** foreign bulletproof hosting infrastructure after January 14, 2025.

- Fisher exact p = 0.0021
- Bonferroni-corrected p = 0.0042 ← **crosses significance threshold**
- Cert quality score: 3.6/5 (Tier 2 — below 4.0 Tier 1 floor; CT-unlogged federal internal CA)
- Timing: first detected Feb 8, 2025 — one day after DOE Secretary publicly denied DOGE nuclear access

**Required action:** LANL IT Security inquiry — determine whether this certificate issuance was authorized. If unauthorized: Tier 1 promotion.

Source: `scripts/audit_results/stat_results_STAT-NEW-001.json`, `scripts/audit_results/evidence_tiers/tier2_strong_support.json` (STAT-GOV-CERT-LANL-019)

---

## Edward Coristine — Mail-in-a-Box at 20.141.83.185

- **Self-hosted email server** (Mail-in-a-Box) at IP 20.141.83.185 (Azure, Microsoft)
- Used for .gov-tagged communications
- Bypasses federal records retention requirements — email outside official .gov systems is not captured by FOIA
- H1 hypothesis: insider access facilitated by communications that left no federal record

**Action:** Cross-reference 20.141.83.185 against cert/IP investigation base. Check if this IP appears in Treasury, GSA, or DOGE infrastructure context.

Source: `scripts/audit_results/bloomberg_h1_items_RUN009.json`

---

## report.html — Cert Language Fix Required

Current text says: "certificates appeared on adversary infrastructure"

Must change to: **"legitimate US government certificates were detected serving from adversary-linked foreign infrastructure beginning after January 14, 2025, having been absent from those IPs during 9–11 months of continuous prior scanning."**

**Why this matters:** CT verification (`ct_log_verification.json`) confirms all three target certs were issued **before** Jan 14. Pre-issuance rules out forgery — the certs are genuine. This actually strengthens the finding: a real, legitimate government cert appearing on foreign adversary infra is more anomalous than a potentially fake one.

---

## ahmn.co Infrastructure — Packetware Confirmed (P=0.78)

- ahmn.co = Packetware-operated (same entity as packetware.net, anchored.host)
- Evidence: `packetware-verification` TXT on anchored.host + CNAME to packetware.net + shared 65.108.96.185 (Hetzner Helsinki)
- 172.93.110.120 = **decommissioned container registry** (`registry2.anchored.host`)
  - Now SSH-only (port 22, March 2026)
  - Was on AS23470 (ReliableSite.Net) — separate from primary Packetware AS400495 block
  - `mail.ahmn.co` PTR hostname = label only, no mail services running

Source: `scripts/audit_results/ahmn_co_research_RUN010.json`

---

## COC Status — PARTIAL → 14/15 Tier 1 Hashed

- All 15 Tier 1 items now have sha256 (STAT-BAXET-FISHER-014 backfilled)
- Chain 0-741 VERIFIED intact (RUN-009 + RUN-010 reconciliation)
- **GAP-1 [HIGH]**: `viz/` directory excluded from all hash manifests — 4 Tier 1 items and 33+ Tier 2 items reference viz/ files with no manifest-backed COC
- Next task: hash viz/ directory → `hash_manifest_RUN011_viz.json`

---

## New Public Pages

- **`disclosure.html`** — OSINT investigator methodology + responsible disclosure record
  - "I am not a hacker. Everything was open-source."
  - Scale: 658+ evidence items, 259 datasets, p<10⁻¹⁰⁰
  - First documented disclosure: DOE (2025-02-21) re: plain HTTP VPN portals
  - Linked in nav: About → Disclosure

- **`docs/DISCLOSURE-TIMELINE.md`** — COC-grade tracking for all disclosure attempts to authorities (CISA, FBI, Congress, IGs, journalists)
