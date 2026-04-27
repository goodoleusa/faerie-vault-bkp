---
type: agent-review-item
cat: HEADLINE
priority: HIGH
agent: data-engineer
ts: 2026-03-20T18:15:00Z
review_status: unreviewed
tags: [review, headline, human-inbox]
doc_hash: sha256:dbe776e8616adef8841d6af43d1ae6102020dd1c1a30089325e8735da0899bf0
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# Hunchly scan — Stark-Aeza-Russia graph captured + 400yaahc.gov in DomainProfiler panel

H4 (conf 0.55 → likely higher now):
- Stark-Aeza-Russia Graph Commons entity map captured Oct 30 2025: graphcommons.com/graphs/671b8cb6-77e7-4a6a-b18a-7f8f4e97b131
- Shodan Monitor watching 45.38.46.0/24 (Aeza) — 256-IP range
- 138.124.123.3 cert CSVs in Google Colab notebook

H3 gap: 400yaahc.gov confirmed in Aegis DomainProfiler scan panel (page 520), grouped with bigballs.one + anchored.host + 194.58.46.116

Void confirmed: registry2 = 0 hits (expected gap)

Output: scripts/audit_results/hunchly_keyword_hits.json (2,751 hits, 3,990 files scanned)

---
*Source: REVIEW-INBOX · Agent: data-engineer · 2026-03-20*
