---
type: agent-review-item
cat: HEADLINE
priority: HIGH
agent: data-engineer
ts: 2026-03-22T17:35:00Z
review_status: unreviewed
tags: [review, headline, human-inbox]
doc_hash: sha256:8346b30c9dfbbb43ddb85f919289a0f13faecd5a270467bd1a97364a04ba4311
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# Reflected TLS Attack — C2 proxies Treasury PKI TLS handshake via socat

Treasury-and-USPTO-and-usadotgov-TLS-certs-Russia-China.pdf (never previously extracted) contains mechanistic explanation for H4 T1 Fisher test (p=3.82e-16): C2 server 8.219.207.49 uses socat to proxy TLS from Treasury PKI IP 164.95.89.25 (pki.treasury.gov, no SNI enforcement). C2 appears as legitimate Treasury HTTPS to Shodan/Censys without possessing private key. Akamai peering ruled out via RIPEstat. Aeza IP 138.124.123.3 first appeared bearing .gov certs January 15, 2025 — one day after DOGE EO signed. Confirmed by 4 independent PDFs.
Files: rawdata/1-Packetware-Prometheus.../National Cybersecurity Crisis Briefs/Treasury-and-USPTO...pdf; scripts/audit_results/pdf_ingestion_RUN007.json
Next: Pre-register + run STAT-NEW-001 (Baxet Fisher test) — data now in hand

---
*Source: REVIEW-INBOX · Agent: data-engineer · 2026-03-22*
