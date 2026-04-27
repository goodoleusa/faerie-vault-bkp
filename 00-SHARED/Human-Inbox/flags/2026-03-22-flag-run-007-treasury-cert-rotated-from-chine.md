---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: data-engineer
ts: 2026-03-22T16:45:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:d67a22c73b9953f242b3660d19604f5ba0ffb2de6bc2b81b32f189b583918465
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# RUN-007: Treasury cert rotated from Chinese IP to South Korean Oracle Cloud — T1 candidate

Treasury cert fingerprint `68e11f5c` confirmed on Chinese Alibaba IP `8.219.87.97`, then rotated to
two South Korean Oracle Cloud IPs: `152.67.204.133` (Gangwon-do) and `217.142.144.30`. Domain
`www.yszfa.cn` directly linked in cert trail. 90 new IPs from this XLSX alone. This IS a new T1 item —
cert rotation to S.Korea suggests multi-hop relay or secondary exfil path beyond China.
Files: scripts/audit_results/tabular_ingestion_RUN007_new.json, rawdata/1-Treasury-cert-South-Korea-China.xlsx
Next: Add `152.67.204.133` and `217.142.144.30` to T1 as new entries; update fnd00009 H4 crossref

---
*Source: REVIEW-INBOX · Agent: data-engineer · 2026-03-22*
