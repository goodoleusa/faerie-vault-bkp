---
type: agent-review-inbox
updated: 2026-03-15
tags: [agents, review, inbox]
doc_hash: sha256:73db760eb2786dbee46d7ced5165731cdbd7b9b84c0968c96920645a2e7e3a2e
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---

# Agent Review Inbox

Items flagged by agents for human review. Synced from `~/.claude/memory/REVIEW-INBOX.md` via `vault_push.py`.

Review items below. Mark completed items with `[x]` — agents will pick up your responses on next /faerie run.

---


---

## RUN-008 Broad Rawdata Sweep — 2026-03-22

<!-- MEM agent=data-engineer ts=2026-03-22T18:03:48Z session=18b341db cat=HEADLINE pri=HIGH av=baseline -->
**[HEADLINE]** RUN-008 broad sweep: 347,720 records, 2,082 unique IPs across 5 evidence categories

**Summary:**
- Treasury H3: 942 records (treasurychina JSONL, treasuryLDAP, cert-spoofing timelines)
- Shodan DOGE H2/H4: 4,408 records (China/Russia/DOGE queries)
- Threat Assessment H1-H4: 282,847 records from 128 files (largest category — AzureGov master XLSX, Baxet US gov spoofs, Russia-AEZA cert spoofing)
- Packetware-spreadsheets H2: 37,143 records from 28 files (container metrics, node configs)
- Misc/Ukraine/Raindrop H4: 22,380 records (investigator bookmarks, Ukraine/Russia exports)

**Key findings for review:**
1. IP `20.159.179.121` (MS-SQL 2016, port 1433, AzureGov AS8070) — cross-validated against investigator-flagged "bd one" in pipeline_ip_crossref_RUN007
2. AzureGov SQL exposure first timestamp: 2025-01-14 (6 days before inauguration) — 37.4% of 14,013 records from Jan-Feb 2025
3. treasurychina.json and treasuryLDAP.json.gz are JSONL format — need line-by-line re-parsing for full extraction
4. Threat Assessment sheets contain 15K+ Baxet US gov spoof records and China-Treasury cert timelines

Files: `scripts/audit_results/broad_*_RUN008.json`, `azuregov_sql_*_RUN008.json`, `packetware_*_RUN008.json`
Next: TRANSFORM phase — cross-reference and deduplicate across all RUN-008 extracts; produce normalized CSVs for site data viz
<!-- /MEM -->
