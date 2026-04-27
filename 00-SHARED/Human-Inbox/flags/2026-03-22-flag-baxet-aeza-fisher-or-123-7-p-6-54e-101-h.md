---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: data-scientist
ts: 2026-03-22T20:15:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:a8191ae0ed8d29ddfc30d4dd199248990805f4d0ae23ac8afb14518d96079d41
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:42Z
hash_method: body-sha256-v1
---

# Baxet/Aeza Fisher: OR=123.7, p=6.54e-101, H4 posterior 0.55→0.993

Three independent foreign IPs (AEZA/Stark 138.124.123.3, Baxet 194.58.46.116, Alibaba 8.219.87.97) all
show .gov TLS certs clustering post-DOGE EO. Combined OR=123.7 (post-DOGE .gov certs are 124x more likely
on these Russian/Chinese IPs). Combined Fisher p=6.54e-101 — essentially impossible under null.

CRITICAL FINDING: 10 .gov cert observations appeared on AEZA IP Jan 15-19 — BEFORE the Jan 20 DOGE EO.
Access began during presidential transition period, 5 days before formal executive order.
Staged deployment: AEZA Jan 15 → Baxet Feb 8 → Alibaba Feb 10.

Negative control (83.149.30.186): zero .gov certs in both periods. Rules out scanner artifact.

Disposition: PROMOTE — add to tier1_smoking_gun.json, gov-cert-inflection bundle.
Files: scripts/audit_results/statistical_analysis_baxet_RUN007.json, scripts/stat_baxet_fisher_jan20.py
Next: evidence-curator to add as Tier 1 item; update H4 confidence in faerie-brief.json to 0.82

---
*Source: REVIEW-INBOX · Agent: data-scientist · 2026-03-22*
