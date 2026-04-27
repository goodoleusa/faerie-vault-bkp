---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: orchestrator
ts: 2026-03-23T00:45:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:26ecd8d38f5eae828147b32fa0da8d473c1080d7fe8e273326f3b256f61b3e8a
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:46Z
hash_method: body-sha256-v1
---

# New H3 entity: 164.95.140.12 — Treasury OIG Exchange 2019 internet-exposed OWA

Treasury OIG email server. OWA (Outlook Web Access) at https://164.95.140.12/owa/auth/logon.aspx.
Exchange 2019 CU14 (Build 15.2.1544.11, April 2024). IIS 10.0. Hostnames: mail.oig.treas.gov,
autodiscover.oig.treas.gov, smtp.oig.treas.gov. Submitted to URLscan 2025-02-08 (investigator capture).
Significance: Internet-accessible OWA = candidate access vector for H3 (active foreign access to Treasury).
Org: United States Department of the Treasury, Washington DC (Shodan confirmed).
Source: bloomberg_shortlist_extract_RUN009.json. Not yet in CROSSOVER file (legitimate Treasury IP, different dataset).
Next: Check if this IP appears in any Baxet/Aeza/Stark observations or if any anomalous auth occurred around J14.

---
*Source: REVIEW-INBOX · Agent: orchestrator · 2026-03-23*
