---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: data-engineer
ts: 2026-03-22T17:35:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:2db19806e88729bc5187b5e0eb20b3216b9e23ca0520822be3c5183e1327815c
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:45Z
hash_method: body-sha256-v1
---

# Requires manual visual inspection — no IPs extracted

SparrowDoor PDF's IOC table is an image, not text. pdfplumber returned 0 IPs. Manual review needed to check overlap with Baxet/Aeza infrastructure.
Files: rawdata/... SparrowDoor PDF
Next: Open PDF visually and manually extract IOC table, or use vision-ingest on that single PDF

---
*Source: REVIEW-INBOX · Agent: data-engineer · 2026-03-22*
