---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: evidence-curator
ts: 2026-03-19T18:48Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:17b74473a05ce942d93d1533964bf35a1aad2dca97ea42a7078e91e1df3113e1
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:41Z
hash_method: body-sha256-v1
---

# Source video file MISSING from local rawdata -- potential evidence loss -- `evidence-curator` @ 2026-03-19T18:48Z

"Packetware ProxMox VM lots spun up and terminated Jan 14, 2025 - Feb 11, 2025.mp4" (SHA-256: e824355...376d, 22.4 MB) exists in genesis hash manifest but NOT on disk. Only "Recording #55.mp4" (3.1 MB) present. B2 backup entry has NULL hash/size fields. 153 extracted frames serve as partial preservation. | Files: `forensic/provenance/hash_manifest_genesis_RUN004.json` (line 8701) | Next: `git log --diff-filter=D` for deletion history, verify B2 bucket, check .gitignore

---
*Source: REVIEW-INBOX · Agent: evidence-curator · 2026-03-19*
