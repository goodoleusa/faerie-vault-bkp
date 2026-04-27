---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-23T00:46:05.597518+00:00
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:08796fa6a1cc593772cb8d071674393c1cd9813f43f5942b8d5b58107792fc96
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:46Z
hash_method: body-sha256-v1
---

# Edward Coristine self-hosted Mail-in-a-Box for gov-tagged email comms; IP 20.141.83.185 active March 2025

Investigator explicitly labeled Mail-in-a-Box (self-hosted SMTP/IMAP) as what 'edward' uses for gov emails.
Raindrop tagged: edward, email, opm, important (Feb 10 2025).
March 2025 finding: IP 20.141.83.185 shows MiAB default landing page.
Official treasury OIG email runs Microsoft Exchange 2019 at 164.95.140.12 (MAIL.oig.treas.gov) with DigiCert cert.
IMPLICATION: If Coristine used self-hosted MiAB for OPM/gov communications, this bypasses official .gov email
infrastructure and records retention - significant FOIA/records compliance issue.
NEXT: Look up 20.141.83.185 in Shodan/cert evidence; check if this IP appears in any .gov DNS or cert data.

Files: scripts/audit_results/bloomberg_h1_items_RUN009.json

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-23*
