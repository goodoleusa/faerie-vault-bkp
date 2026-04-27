---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: orchestrator
ts: 2026-03-23T00:45:02Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:c49e298cf7b16329e8a3e60a4171771853d989a395d6ea4af66472b8cf61c464
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:46Z
hash_method: body-sha256-v1
---

# SparrowDoor (GCHQ/NCSC) negative crossref — file hashes only, no network IOCs

GCHQ/NCSC SparrowDoor report (2025-04-05, 25 pages) fully extracted via PyMuPDF.
Finding: ZERO C2 network IOCs (IPs/domains). Report contains only YARA detection rules + file hashes.
File hashes for SparrowDoor samples:
  SHA256: 9863ac60b92fad160ce88353760c7c4f21f8e9c3190b18b374bdbca3a7d1a3fb (SearchIndexer.exe = disguised GUP.exe Notepad++)
  SHA256: e0b107be8034976f6e91cfcc2bbc792b49ea61a071166968fec775af28b1f19c
  SHA256: f19bb3b49d548bce4d35e9cf83fba112ef8e087a422b86d1376a395466fdff2d
Conclusion: Cannot crossref SparrowDoor to investigation network infrastructure. Gap 17 closed (negatively).
Next: If any malware samples appear in investigation evidence, run YARA rules from this report for attribution.

---
*Source: REVIEW-INBOX · Agent: orchestrator · 2026-03-23*
