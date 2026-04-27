---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: orchestrator
ts: 2026-03-23T01:00:01Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:2271bea604fed4b1396a4327461a98b032c75f9c6c3b0ed679163def9eebce33
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# Edward Coristine mail-in-a-box at 20.141.83.185 (Azure) — OPM-tagged self-hosted email = potential FRA violation H1

IP 20.141.83.185 shows Mail-in-a-Box default landing page as of March 2025.
Investigator note at time of capture (2025-02-10): "like bigballs uses" — direct attribution to Edward.
Raindrop tags: edward, email, OPM, important.
Mail-in-a-Box = self-hosted email server. If used for government/OPM communications:
- Bypasses official .gov email infrastructure  
- Federal Records Act violation (gov communications must be on gov systems)
- Content not subject to FOIA if never on gov servers
- ASN: 20.x.x.x = Azure. If running gov-tagged email here = evading retention requirements.
Contrast: Official Treasury OIG uses Exchange 2019 at 164.95.140.12. Edward appears to use MiAB in parallel.
Source: bloomberg_h1_items_RUN009.json. Next: WHOIS/PTR for 20.141.83.185, confirm MiAB still active, subpoena-ready.

---
*Source: REVIEW-INBOX · Agent: orchestrator · 2026-03-23*
