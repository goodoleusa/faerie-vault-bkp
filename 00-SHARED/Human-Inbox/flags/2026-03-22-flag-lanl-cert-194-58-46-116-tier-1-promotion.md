---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: evidence-curator
ts: 2026-03-22T22:30:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:6a01d128d5a560b1642b78c766a1fcc13c35907342323dabfcb1635313f1009a
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# LANL cert 194.58.46.116 Tier 1 promotion REJECTED — quality avg 3.6, CT inconclusive

Task task-20260320-004832-14b3 assessed 194.58.46.116 (dx10.lanl.gov, Baxet/Russia) for Tier 1 promotion.
CT log verdict: INCONCLUSIVE — federal internal CA cert, not CT-logged. Issuance date unknown. TLS RSA-1024 + TLSv1.0 indicates legacy internal cert; cannot rule out spoofed/forged without issuance date. Quality avg 3.6 (authenticity=3, reliability=3, relevance=5, corroboration=2, timeliness=5) — below Tier 1 floor of 4.0. Tier 1 at cap (15/15). Already partially represented by STAT-BAXET-FISHER-014 (Tier 1, OR=123.7, p=6.54e-101). STAT-GOV-CERT-LANL-019 confirmed at Tier 2 with note "qualitative interest only." No tier change.

Files: scripts/audit_results/ct_log_verification.json, scripts/audit_results/evidence_tiers/tier1_smoking_gun.json, scripts/audit_results/evidence_tiers/promotion_log.json
Next: If independent corroboration emerges for LANL cert (second source confirming cert on IP, or issuance date), reassess. Do not publish LANL cert as standalone Tier 1 claim.

---
*Source: REVIEW-INBOX · Agent: evidence-curator · 2026-03-22*
