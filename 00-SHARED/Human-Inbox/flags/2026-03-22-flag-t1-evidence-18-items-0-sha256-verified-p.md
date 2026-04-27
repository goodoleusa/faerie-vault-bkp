---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: evidence-curator
ts: 2026-03-22T00:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:07c15afb62c0db261c4e9270ab69d74a0bff93f5bd624cd1287947af95861ae4
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# T1 evidence: 18 items, 0 sha256-verified — publication BLOCKED until hash_guardian run

Chain-of-custody requirement: NEVER promote T1 item without hash verification. Critical files include: rawdata/Treasury Commvault China Article metadata.json files, prisma_reconstructed_db.json, gov_cert_inflection_stats.json, operational-timeline-master.csv. | Files: `scripts/audit_results/evidence_tiers/tier1_smoking_gun.json` | Next: Run hash_guardian.py on all 18 T1 source files; security-auditor priority

---
*Source: REVIEW-INBOX · Agent: evidence-curator · 2026-03-22*
