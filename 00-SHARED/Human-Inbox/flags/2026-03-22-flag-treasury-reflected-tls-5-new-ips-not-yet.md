---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: orchestrator-inline
ts: 2026-03-22T23:32Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:5aa1879e79a703b1cfaa10fe311f081c486aa40978e0790444dfc37a27059078
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# Treasury Reflected TLS: 5 new IPs not yet in pipeline_ip_crossref

New IPs: 5.180.24.192 (Stark/AS44477), 217.142.144.30, 8.219.147.118 (Alibaba/AS45102), 164.95.89.25 (Treasury bare PKI, no SNI). Reflected TLS attack technique via socat documented. | Files: `scripts/audit_results/treasury_tls_certs_extract_RUN009.json` | Next: evidence-curator T1 review; add all 5 to pipeline_ip_crossref

---
*Source: REVIEW-INBOX · Agent: orchestrator-inline · 2026-03-22*
