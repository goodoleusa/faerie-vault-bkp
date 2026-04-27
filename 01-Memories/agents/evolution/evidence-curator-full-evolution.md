---
type: agent-evolution-full
agent: evidence-curator
generated: 2026-03-25
tags: [agent-evolution, performance, investigation-context]
privacy: personal-vault-only
doc_hash: sha256:68cc068f11bfc055ca1ed78782a654a3dd476d3fdf193e063de42af76061de1e
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Evidence Curator — Full Evolution Story

## Current State
- **Score:** 0.97 (deployment, 2026-03-23) | **Prev:** 0.93
- **Tier:** INVESTIGATE (critical chain — every finding passes through this agent)
- **Active investigations:** Operation CriticalExposure — Tier 1/2 curation; Treasury cert chain; Hetzner Prisma Studio destruction triage; userId resolution

## Training Timeline

| Date | Score | Delta | Context | Key Learning |
|------|-------|-------|---------|-------------|
| Pre-2026-03-19 | ~0.93 | baseline | on_the_job deployment | Established as high-performer pre-formal-training |
| 2026-03-19 | 0.93 | baseline | destruction-triage deployment run | Tier accuracy confirmed; 4 MEM blocks; 4.0 quality avg |
| 2026-03-19 | 0.96 | +0.03 | Tier 1 formalization run (8 items) | All items above quality floor; full COC in one pass |
| 2026-03-19 | 0.97 | +0.01 | userId crossref resolution (fnd00006) | Bayesian chain documentation; 4 independent evidence paths; P=0.995 |
| 2026-03-23 | 0.97 | = | Formal card update (on_the_job_redemption) | Layer sources across dimensions; negative controls outrank positives |

## Investigation Context

### The Treasury Triple Finding — The Curator's Defining Moment (2026-03-19)
The evidence-curator's most significant contribution to Operation CriticalExposure was the formal Tier 1 promotion of the Treasury cert chain triple finding on March 19, 2026. This was not simply tiering three items — it was recognizing that three independent data streams told ONE coordinated story:

1. **RD-TREASURY-LDAP-EXPOSURE** (fnd00005): Two Treasury LDAP servers (164.95.88.30, 166.123.218.100) on port 389 with anonymous bind. Multi-agency directory: Treasury, SSA, DHS, VA, Fiscal Service, PingFederate SSO namespace exposed. Timestamps 2025-03-19 and 2025-03-27. Quality: 4.8/5.

2. **RD-TREASURY-CERT-ALIBABA-CHINA** (fnd00002): Treasury TLS cert fingerprint 68e11f5c... observed on Alibaba China IP 8.219.87.97 (AS45102) continuously from 2024-03-24 to 2025-03-02 — 984 observations over 11+ months. Verified real cert via CT logs (not spoofed). The curator's key insight: a single exposure would show disappearance; 11-month persistence = either private key exfiltration or CA compromise. Quality: 4.8/5.

3. **CERT-ROTATION-TRIGGERED-REEMERGENCE** (fnd00003): New cert 5d430f2c... appeared on South Korean Oracle Cloud IP 152.67.204.133 within 72 hours of Treasury cert rotation, DNS-linked to Chinese domain www.yszfa.cn. The curator named this the "rotation event" — proof of ongoing operational capability, not one-time leak. Quality: 4.8/5.

Promotion timeline: 19:00:00Z (LDAP), 19:05:00Z (China cert), 19:25:00Z (rotation event). All three formalized with 5-dimensional quality scores, caveats arrays (ALTERNATIVE/COUNTER/METHODOLOGICAL/CAUSAL), limitations, what-would-change-conclusion vectors, and journalist hooks.

**Narrative the curator synthesized:** Layer 1 (Credentials): Federal identity database exposed → foreign actor can enumerate Treasury employees. Layer 2 (Authentication): Treasury TLS certificate stolen for 11 months → foreign actor can impersonate Treasury. Layer 3 (Persistence): Post-rotation, new cert with Chinese DNS → operational persistence and geographic redundancy. Complete compromise chain.

**Hypothesis impact logged by curator:** H3 (Coordinated exfil) 0.32→0.81. H4 (Foreign actor) 0.61→0.82.

### Evidence Destruction Triage (2026-03-19, sprint-20260319-002)
The curator triaged the ProxMox Prisma Studio video evidence:
- Video showed operator selecting subsets of 37 ProxmoxVM records, causing "Delete N records" button to appear (Delete 4, Delete 23, Delete 21 at different frames)
- **Key finding: deletion was NOT executed** — all 37 records remain in final frames
- Assigned Tier 2 (H5 cover-up, H1 insider access consideration). Quality avg 4.0.
- Flagged as HIGH: source video "Packetware ProxMox VM lots spun up and terminated Jan 14, 2025 - Feb 11, 2025.mp4" (SHA-256: e824355...376d, 22.4 MB) confirmed in genesis manifest but NOT on local disk. B2 backup fields NULL. 153 extracted frames = partial preservation only. This REVIEW-INBOX flag remains open.

### fnd00006 userId Resolution (2026-03-19/22)
The curator resolved a persistent gap: userId a458bkg9pb95tgb8 vs projectId a45bkg9pb95tgb8 — Levenshtein distance = 1 (single character transposition in HTML vs Gemini OCR). Four independent evidence paths built into a Bayesian chain: (1) prisma_reconstructed_db.json id_variants field; (2) prisma_entity_linkage.json Member id=1 FK; (3) HTML vs Gemini OCR transposition documented in PRISMA_RECONSTRUCTION_METHODOLOGY.md; (4) all ADMIN-role Member records reference same entity. Bayesian posterior P=0.995.

Key curator decision: NO new Tier 1 promotion — finding subsumed in PRISMA-MUSKOX (quality=5.0, same source file). This deduplication discipline (not creating redundant Tier 1 entries when a better one exists) is characteristic of the curator's mature tiering practice.

Feb 18 timeline contextual note: same operator (a458bkg9pb95tgb8) conducted mass VM cleanup at 19:18:41, re-added as Member id=183 at 19:32:27 — 14 minutes later — consistent with scripted teardown + re-provisioning.

### Tier 1 Eight-Item Formalization (sprint-20260319-002, 8 items in one pass)
The highest-complexity single-session curation task: formalizing 8 Tier 1 items with full COC in one pass. All items above 4.0/5 quality floor. COC entries logged for all 8. Journalist briefing produced (JOURNALIST_BRIEFING_TIER1.md — though written to repo root instead of audit_results/, costing the session 0.04 on overall score). Tier 1 quality avg: 4.6.

### Nuclear Triple (Sprint RUN012, 2026-03-23)
Curator received the H4 nuclear triple finding from data-engineer for tiering: LANL (194.58.46.116) + LLNL (45.130.147.179) + ORNL (166.1.22.248) all bearing certs on Baxet-affiliated IPs. Verification task queued: confirm ORNL cert via CT logs before Tier 1 promotion. Also: NASA (103.146.119.152), DHS/ICE SEVP (194.87.82.246), uscourts (103.146.119.204) flagged.

## What It Learned

### Process Improvements (shareable)
- Layer sources across analytical dimensions (observation + quantification + control); two same-tool scans = 1 source
- Negative controls outrank additional positive examples for Tier 1 promotion — one true negative eliminates scanner artifact explanations better than three more positives
- Separate evidence from interpretation: attribution context is journalist_hook material, not quality-score input
- Same-database-different-angle = 1 source (e.g., same DB, two queries on one record = 1 source, not 2)
- Full Bayesian chain with 4 independent evidence items beats confidence assertion alone — decompose prior + likelihood ratios explicitly
- Document dual ID forms (authoritative vs canonical) with separate rationale for each form

### Investigation-Specific Insights (private)
- The Treasury triple finding was the curator's breakthrough moment. The "rotation event" insight — recognizing that a cert appearing 72 hours after rotation on new infrastructure is proof of operational capability, not coincidence — came from understanding the adversary's operational security constraints. An accidental cert leak doesn't follow you to new infrastructure post-rotation; a persistent access holder does.
- The fnd00006 resolution (a45 vs a458) taught the curator to distinguish OCR transcription errors from distinct entities. The PRISMA_RECONSTRUCTION_METHODOLOGY.md documentation of the HTML-vs-Gemini transposition was the key evidence — not just saying "similar IDs" but proving the specific error pathway.
- The ProxMox video destruction triage was a calibration exercise: the curator correctly placed it at Tier 2 (not Tier 1) because the deletion was not executed. Tier 1 requires direct proof; "evaluated deleting but didn't" is supporting context, not smoking-gun.
- The 8-item formalization sprint revealed a structural weakness: JOURNALIST_BRIEFING_TIER1.md was written to the repo root instead of audit_results/. The curator knows WHERE it wrote the file — this was an inattention error under load, not a methodology failure. Future sessions: always confirm output path before writing.

## Performance Trajectory

The curator's evolution is a story of steady deployment excellence punctuated by methodological deepening. The 0.93 baseline was already high — the curator entered this investigation as a capable tiering agent. What the Packetware investigation added was:

1. **Narrative synthesis**: Moving from "these are three good pieces of evidence" to "these three pieces form ONE coordinated breach chain" — the Treasury triple is the canonical example.
2. **Deduplication discipline**: The fnd00006 decision (don't create a new Tier 1 when it's already subsumed) shows mature evidence management.
3. **Destruction triage precision**: Correctly saying "the button appeared but was NOT pressed" is an important distinction in court-grade evidence work.

The 0.96 → 0.97 progression is incremental but meaningful in context: at this precision level, each 0.01 represents a specific methodological improvement. The Bayesian chain for fnd00006 (decomposing 4 independent evidence paths with explicit likelihood ratios) is what pushed the score.

## Spawn History

| Sprint | Task | Items Curated | Score |
|--------|------|---------------|-------|
| 2026-03-14 (baseline) | Evidence-curation (timeline evidence) | n/a | ~0.93 |
| sprint-20260319-002 | Evidence destruction triage (ProxMox video) | 1 item, Tier 2 | 0.93 |
| sprint-20260319-002 | Tier 1 formalization (8 items) | 8 items, Tier 1 | 0.96 |
| sprint-20260319-002 | fnd00006 userId crossref resolution | 1 item, Tier 1 | 0.97 |
| sprint-0322/23 | Nuclear triple triage (incoming) | queued | pending |

Appears 3x in sprint-20260319-002 alone — the session highlight note in run-benchmarks confirms "evidence-curator Tier 1 formalization is the session highlight: 8 items curated with full forensics in one pass."
