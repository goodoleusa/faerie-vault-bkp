---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-23T14:04:11Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:7d2729261cff8ba7ccbf48c9def89d7e25ddd70d7c47923586cf752451ce286d
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:46Z
hash_method: body-sha256-v1
---

# ORNL nuclear triple arm: icons.ornl.gov hostname on Baxet IP CONFIRMED but cert is NOT ornl.gov

166.1.22.248 (AS26383, Baxet Group Inc., Lelystad NL) — Shodan hostname=icons.ornl.gov, HTTP title="Coming Soon - icons.ornl.gov", port 8181 TLS cert=CN=BlurbStudio.cr (self-signed, Version 1, RSA-1024, sha1, Not Before 2025-02-24). CT log queries for IP and %ornl% domain — 0 results for IP, 120 results for %ornl% all from DigiCert/InCommon, zero Baxet IP associations. Nuclear triple: LANL=cert confirmed, LLNL=unverified (need 45.130.147.179 Shodan), ORNL=hostname impersonation only. Verdict: HOSTNAME_CONFIRMED_CERT_DENIED. Tier 2. BlurbStudio.cr (.cr TLD, manually-generated) is an unresolved pivot — investigate WHOIS.
Files: archives/990935009_166122248-baxet-iconsornlgov.html, scripts/audit_results/ornl_cert_verification_RUN012.json
Next: Check 45.130.147.179 Shodan archive for LLNL cert; revise nuclear triple framing in report.html; WHOIS BlurbStudio.cr

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-23*
