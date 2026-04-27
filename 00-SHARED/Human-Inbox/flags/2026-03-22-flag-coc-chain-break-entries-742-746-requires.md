---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: security-auditor
ts: 2026-03-22T00:00:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:8503c1c93eb40d9bdaa6fd324c638de76217478c771c034b5e00951698facfc6
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:44Z
hash_method: body-sha256-v1
---

# COC chain break entries 742-746 requires schema unification + repair

master-coc.jsonl entries 742–746 BROKEN (schema mismatch: forensic_coc.py vs vault_manifest.py vs inline Python using different hash field names). Entries 0–741 intact. coc_reconciliation_RUN009.json documents. All current investigation findings are in 0–741 range (COC-valid). Repair needed before any court export or public publication of COC chain. | Files: `~/.claude/memory/investigations/criticalexposure/forensics/master-coc.jsonl`, `scripts/audit_results/coc_reconciliation_RUN009.json` | Next: unify schema across all three appending scripts, re-hash from entry 742 forward

---
*Source: REVIEW-INBOX · Agent: security-auditor · 2026-03-22*
