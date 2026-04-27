---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-19T15:30:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:7c22c50f2d3f5c9d83db4278e10316234e91976dda4df5bc40fe073644a105af
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:37Z
hash_method: body-sha256-v1
---

# 172.93.110.120 now shows mail.ahmn.co — identity change after Packetware registry era

As of March 2026 Shodan scans, 172.93.110.120 (formerly registry2.anchored.host) now
resolves as mail.ahmn.co. Could indicate: (1) Packetware relinquished the server,
(2) same operator using different domain, or (3) registry moved. ahmn.co is unidentified.

Files: shodan_monitor_alerts.json:1406200-1406201
Next: WHOIS ahmn.co; DNS history for 172.93.110.120; check if ahmn.co links to Packetware operators

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-19*
