---
type: agent-review-item
cat: CONNECTION
priority: HIGH
agent: research-analyst
ts: 2026-03-22T18:00:00Z
review_status: unreviewed
tags: [review, connection, human-inbox]
doc_hash: sha256:106999b0d77af01f161066637c755cdebbebaed2dfbae926372a39617ae08198
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# ahmn.co confirmed as Packetware-operated: packetware-verification TXT on anchored.host + CNAME to packetware.net + shared 65.108.96.185 IP. 172.93.110.120 decommissioned as registry2.anchored.host; SSH-only March 2026; was on AS23470 (ReliableSite), not AS400495.

Evidence chain: prisma_html_extractions_v2.json > anchored.host Shodan infra (JACKPOT-8-29-2025): TXT packetware-verification=ohtwzMJP9... + CNAME packetware.net. Shodan Monitor March 2026: port 22 only, 15 banner updates. Raindrop bookmark: "ASN: 23470 ASN Name: RELIABLESITE". Prisma DB: IPv4Address status:ASSIGNED.
Verdict: Same operator, not new tenant. mail.ahmn.co PTR is a hostname label only — no mail services active.
Files: scripts/audit_results/prisma_html_extractions_v2.json, scripts/audit_results/shodan_monitor_timing_analysis.json, scripts/audit_results/broad_packetware_spreadsheets_extract_RUN008.json
Next: Live WHOIS for ahmn.co + anchored.host (registrant name/email) — needs WebFetch access. AS23470 BGP peering with AS400495 (ReliableSite ↔ Packetware peering?) — needs bgp.tools query.

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-22*
