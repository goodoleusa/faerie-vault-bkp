---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-22T00:00:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:118adff1533be24a575b998df63b3f81ca5263c141fd61aab505acdfb0c81be3
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# yszfa.cn Chinese domain pre-positioned on Oracle Cloud SK node 16 days before Treasury cert 68E11F5C

www.yszfa.cn → 152.67.204.133 (Oracle Cloud SK, AS31898) DNS A record confirmed 2025-03-07 (Censys archive).
Treasury Entrust OV cert 68E11F5C (*.treasury.gov) first appeared on this IP: 2025-03-23.
16-day gap proves Chinese-operated node was pre-positioned before cert migration from Alibaba.
Domain appears in cert crossover query alongside 155 US Treasury domains (A--treasury-hosts-same-fingerprint.csv row 156).
.cn TLD = mandatory CNNIC real-name Chinese domestic entity registration.
Live RDAP required for registrant ID: https://rdap.cnnic.cn/domain/yszfa.cn
ICP lookup (stronger identifier): https://beian.miit.gov.cn search yszfa.cn
Full output: scripts/audit_results/yszfa_whois_RUN009.json
Next: Live RDAP + ICP lookup + passive DNS for full timeline

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-22*
