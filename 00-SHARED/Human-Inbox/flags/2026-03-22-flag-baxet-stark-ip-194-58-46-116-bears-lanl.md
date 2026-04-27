---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: data-scientist
ts: 2026-03-22T00:00:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:44d4fa3b77d73276848176c9269091efca5ca8b6c99e6edf8b3abe2de2c42347
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:43Z
hash_method: body-sha256-v1
---

# Baxet/Stark IP 194.58.46.116 bears LANL nuclear cert (dx10.lanl.gov) post-J14 — Fisher p=0.0021, OR=infinity

Pre-registered Fisher exact test on 1-year Censys CSV series (863 rows):
- Pre-J14 (752 obs, 9.7 months): ZERO .gov TLS certs — 0/752 = 0.00%
- Post-J14 (111 obs, 2.2 months): 3 .gov TLS certs — 3/111 = 2.70%
- Certificate: CN=dx10.lanl.gov (Los Alamos National Laboratory nuclear supercomputer cluster dx10)
- Observations: Feb 8–9, 2025 (5–6 weeks after J14 inflection)
- Fisher p = 0.0021, Bonferroni-corrected p = 0.0042 (k_effective=2), alpha=0.025 — SIGNIFICANT
- MWU on daily series: p = 0.0030, Bonferroni-corrected p = 0.0061 — SIGNIFICANT (both tests agree)
- OR = infinity (zero pre-J14 gov certs — zero-cell table)
- Bayesian posterior: 50% (LR=1000 conservative), 91% (LR=10000 for nuclear domain)
- REPLICATES 138.124.123.3 pattern (Aeza/Ukraine, usa.gov cert, p=1.53e-15, 29 post-J14 rows)
- H4 (The Handoff) implication: Russian-linked Baxet/Stark infrastructure hosting LANL nuclear cert, same J14 inflection as across all investigation categories
- LANL IT VERIFICATION NEEDED: confirm dx10.lanl.gov cert was not legitimately issued to 194.58.46.116

Files: scripts/audit_results/stat_results_STAT-NEW-001.json, scripts/audit_results/stat_preregistration_STAT-NEW-001.json
Next: (1) LANL IT inquiry re cert legitimacy; (2) STAT-NEW-001-GROUP — group-level test across all Baxet IPs with .gov certs/hostnames; (3) Check cert chain/issuer for dx10.lanl.gov on this IP (self-signed vs real CA)

---
*Source: REVIEW-INBOX · Agent: data-scientist · 2026-03-22*
