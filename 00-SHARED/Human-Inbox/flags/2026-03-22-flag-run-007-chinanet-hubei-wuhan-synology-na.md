---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: data-engineer
ts: 2026-03-22T16:45:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:9b3410f6faee7dbda2713a2be748ac327277a92b29d6f61c9d4c85402c43fed4
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# RUN-007: CHINANET Hubei (Wuhan) Synology NAS literally named "doge" — T1 candidate

IP `111.172.10.170`, CHINANET Hubei, HTTP title literally "doge - Synology DiskStation". TLS cert
`ming.wanip.ch`. Second Wuhan IP `111.172.8.240` same device. First seen Aug 16 2025. "doge" branding
on a Chinese NAS is direct naming evidence of H2/H4 connection — not circumstantial.
Files: scripts/audit_results/tabular_ingestion_RUN007_new.json
Next: Verify via current Shodan, check cert for org name, promote to T1 if confirmed

---
*Source: REVIEW-INBOX · Agent: data-engineer · 2026-03-22*
