---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-23T18:43:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:f23323d772106742f08b4a1c5650b032c4f1a92081baed3e964f50dbadfff9cc
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# c5isr.dev — Azure infrastructure impersonating U.S. Army DEVCOM C5ISR Center; Mail-in-a-Box CONFIRMED

Domain c5isr.dev (Azure AS8070, Boydton VA) impersonates U.S. Army DEVCOM C5ISR Center (c5isrcenter.devcom.army.mil). C5ISR Center works on cyberspace ops, EW, and tactical networks. Full parallel platform: git.c5isr.dev (20.141.83.185), Mail-in-a-Box on mail.c5isr.dev (20.141.187.124, ports 22/25/53/80/465/993/995/4190 + ManageSieve port 4190 = definitive MiAB fingerprint), Matrix chat, SSO, MDM, wiki, cloud, artifacts. Self-hosted DNS (ns1/ns2.mail.c5isr.dev). No PTR on git IP. Active since Dec 2023 per crt.sh. WHOIS privacy-protected. H1 confirmed.
Files: scripts/audit_results/mailinbox_20141_RUN016.json
Next: Identify c5isr.dev registrant (DNS history tools); cross-ref 20.141.187.124 against evidence corpus; check matrix/sso endpoints; attempt FOIA

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-23*
