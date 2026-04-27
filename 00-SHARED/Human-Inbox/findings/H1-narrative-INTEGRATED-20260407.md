---
type: report
blueprint: [[Blueprints/Report.blueprint]]
agent_type: report-writer
session_id: task-20260407-h1-narrative
doc_hash: sha256:pending
status: draft
promotion_state: awaiting-annotation
---

# H1 Hypothesis Narrative: DOGE Insider Threat Investigation

**Classification:** DRAFT — Awaiting human annotation gate  
**Sprint Task:** task-20260407-h1-narrative  
**Vault copy:** Human-Inbox/findings — for annotation  
**Primary file:** scripts/audit_results/H1-narrative-INTEGRATED-20260407.md  

This file is the vault copy of the H1 narrative for human annotation. Primary evidentiary file
is at `/mnt/d/0local/gitrepos/faerie2/scripts/audit_results/H1-narrative-INTEGRATED-20260407.md`.

Annotate via `.ann.md` sibling file. Use decision markers:
- `approve-promote` → finding moves to NECTAR on next memory-keeper run
- `crystallize-to-honey` → finding queued for /crystallize
- `reject` → finding archived, not promoted
- `needs-context` → finding held pending additional evidence

---

## Summary for Human Review

Eight findings support H1. Five are Tier 1 (confidence 4.3–5.0/5.0). Two are Tier 2 secondary
indicators with confidence caveats. One is a null result (p = 0.294) disclosed per pre-registration.

**Overall H1 confidence: 0.95** (HONEY.md canonical value, per faerie-executive decision 2026-04-07.)

**Key claims requiring annotation:**
1. Coristine = Packetware admin (GitHub ID 76141700, PRISMA-MUSKOX) — 5.0/5.0
2. .gov accounts in Packetware (tempf.gov + tempdf.gov created same second, PRISMA-GOV-ACCOUNTS) — 5.0/5.0
3. Certificate inflection Jan 14 (p = 6.54e-101, STAT-GOV-CERT-INFLECTION-019) — 5.0/5.0
4. Dark entity ($6.74 revenue, 37 VMs, 0 customers, PRISMA-MUSKOX) — 5.0/5.0
5. Anti-forensics (29 VMs wiped same second, PRISMA-MUSKOX) — 4.8/5.0
6. Traffic anomaly (26,411:1, Montreal Z=7.03, p=1.06e-12, STAT-H-RATIO-014) — 4.5/5.0
7. Baxet/Alibaba co-occurrence (p=6.54e-101, OR=123.7, STAT-BAXET-FISHER-014) — 4.3/5.0
8. Whistleblower disclosures — NLRB Berulis + Treasury (RD-1017279346) — 3.8/5.0

**Secondary indicators (annotation can defer):**
- c5isr.dev domain (0.42 confidence — IP link absent)
- ORNL/LLNL hostname targeting (reconnaissance only, not compromise)

**Null result disclosed:** p = 0.294 for DOGE access vs. Treasury breach temporal simultaneity.
Non-significant. Disclosed per pre-registration. Does not weaken Tier 1 evidence.

**Publication deadline:** 2026-04-08 12:00 UTC

---

See primary file for full section text, citations, and evidence paths.
