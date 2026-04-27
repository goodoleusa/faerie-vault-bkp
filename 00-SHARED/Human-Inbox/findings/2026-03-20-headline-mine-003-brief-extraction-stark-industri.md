---
type: agent-review-item
cat: HEADLINE
priority: HIGH
agent: data-engineer
ts: 2026-03-20T18:10:00Z
review_status: unreviewed
tags: [review, headline, human-inbox]
doc_hash: sha256:8b26ff0e74bb71b1062015a821991715ec0e28a827273453bebee8632de2db6a
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# MINE-003 brief extraction: Stark Industries (AS44477) + Aeza International same Russian entity — H4 upgrade

Brief-general.pdf + Cert Brief new.pdf explicitly document: Stark Industries (AS44477) and Aeza International (AS210644) registered to same Russian address. IP 138.124.123.3 transferred Stark→Aeza while holding 3 US Gov TLS certs (Jan15–Mar5 2025). AS51659 (LLC Baxet) peered with both via Melbikomas UAB (AS56630). Nuclear brief: 194.58.46.116 (Aeza) served LANL + DOE certs. DOE LDAP unauthenticated at 205.254.131.127.

New ASNs: AS44477, AS210644, AS51659, AS56630 — none in HONEY.md yet.
Output: scripts/audit_results/brief_extractions.json
Files: none
Next: Crystallize AS44477/Aeza=Stark into HONEY.md fnd entries; check 205.254.131.127 DOE LDAP; OCR bigballs PDF

---
*Source: REVIEW-INBOX · Agent: data-engineer · 2026-03-20*
