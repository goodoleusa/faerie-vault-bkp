---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-23T14:30:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:913de69fd8ba49022a7152e4e3ae8be769f6fdee7c37f1e230b7fbb5f53b57d9
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# cdn181.awsdns-531.com C2 confirmed FamousSparrow; AS45102 link NOT yet established

cdn181 = SparrowDoor C2 confirmed per UK NCSC MAR 2022-02-28 + Trend Micro Earth Estries IOC archive.
Passive DNS: 103.15.28.228 → AS55639 (HK VPS, Asia Web Service Ltd) — NOT AS45102 (Alibaba Cloud).
Cross-validated: 103.15.28.228 in OTX passive DNS AND Trend Micro IOC independently. Confidence: 0.9.
Packetware IPs (8.219.87.97, 8.219.147.118) remain AS45102-confirmed independently.
GAP OPEN: 5 sibling awsdns-531.com domains (ssl3, ns101, llnw-dd, cas04, c11r) — all confirmed FamousSparrow IOCs — passive DNS NOT checked. Any 8.219.x.x resolution = AS45102 link confirmed for FamousSparrow C2 cluster.
Files: scripts/audit_results/virustotal_cdn181_RUN012.json
Next: OTX passive DNS sweep for 5 sibling awsdns-531.com subdomains

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-23*
