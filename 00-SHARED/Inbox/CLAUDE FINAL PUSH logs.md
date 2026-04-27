---
type: meta
tags: []
doc_hash: sha256:ef2fdf3a135292691c6118c9db4456c7df50d2545d8f8fd036b76f41e2879706
hash_ts: 2026-03-29T16:16:41Z
hash_method: body-sha256-v1
---
 Backgrounded agent
  ⎿  Prompt:
       You are the Process Orchestrator for the CyberTemplate investigation pipeline. Your specific task: ensure the recent Prisma DB vision extraction outputs are properly COC'd
       (chain of custody) and integrated into the reconstructed Prisma database with annotations.

       Working directory: /mnt/d/0local/gitrepos/cybertemplate

       What just happened (context)

       A vision extraction agent (ai-engineer) just processed the remaining 35 screenshots of Packetware's Prisma DB (65.108.96.185:5555 — exposed database management interface).
       These screenshots show VM tables, user tables, billing data, activity logs, and service tables.

       Previous extraction state:
       - scripts/audit_results/prisma_screenshots_visual_extraction.json — contained 6 screenshots previously processed
       - The agent was instructed to append findings to an "additional_extraction" key in this file
       - scripts/audit_results/prisma_entity_linkage.json — consolidated entity relationships
       - scripts/audit_results/prisma_html_extraction.json — HTML-based extraction of 14/181 OAuthAccounts + tables
       - pinata/data/gemini_merged_extraction.json — Gemini Vision extraction (4144 rows from video frames)

       Your task

       Coordinate 3 subagents to do the following in sequence:

       Agent 1: HASH GUARDIAN (security-auditor)

       Hash all Prisma screenshot source files and the new extraction output. Update scripts/audit_results/hash_manifest.json with:
       - SHA-256 of every file in rawdata/Screenshots/Packetware Prisma Screenshots/
       - SHA-256 of every file in rawdata/Packetware Prisma Screenshots/
       - SHA-256 of scripts/audit_results/prisma_screenshots_visual_extraction.json (current state)
       - SHA-256 of pinata/data/gemini_merged_extraction.json
       - Entry for the vision extraction run: {"run_id": "prisma_visual_20260313", "timestamp": "2026-03-13T23:00:00Z", "screenshots_processed": 41, "method": "Claude Opus 4.6
       multimodal direct screenshot reading"}

       This establishes the chain of custody for the vision extraction.

       Agent 2: INGESTOR/CLEANER (data-engineer)

       Read the current state of scripts/audit_results/prisma_screenshots_visual_extraction.json and:
       1. Check if the additional_extraction key was successfully added by the vision agent
       2. If yes: merge all extracted data into a unified prisma_reconstructed_db.json that combines:
         - Findings from the original 6 screenshots (existing tables_extracted)
         - Findings from the 35 new screenshots (additional_extraction)
         - Cross-reference with prisma_entity_linkage.json (link found entities)
       3. The unified file should have sections:
         - vm_table: all VM records found across screenshots
         - user_table: all user/account records found
         - activity_table: all activity/audit log entries
         - service_table: all service records
         - oauth_table: any OAuthAccount records found
         - billing_table: billing entries
         - annotations: key findings with citation IDs
       4. Add annotations for:
         - Edward Coristine account(s) found: "CRITICAL: edward@packetware.net created 2025-02-20, same session as tempf.gov"
         - tempf.gov: "CRITICAL: Has 1 session — someone logged in. Created 2025-02-20T06:57:58"
         - interim-muskox VM: "HIGH: Musk reference, cleaned 2025-02-18T19:18:41"
         - mass cleanup: "CRITICAL: All VMs updated 2025-02-18T19:18:41 same second"
         - mrcomq: "HIGH: Known The Com handle, registered Aug 1 2025"
         - GitHub OAuth: "OPEN: Edward's GitHub provider_user_id not found in 14/181 OAuth sample"
       5. Write to scripts/audit_results/prisma_reconstructed_db.json

       Agent 3: EVIDENCE CURATOR (evidence-curator)

       After the reconstructed DB is written:
       6. Review the Prisma evidence bundle for tier promotion
       7. The following items should be in Tier 1 (smoking gun):
         - prisma_reconstructed_db.json — the reconstructed database itself
         - tempf.gov / tempdf.gov accounts (created same second as edward, 9 min after his account)
         - The Feb 18 2025 19:18:41 UTC mass cleanup (same-second VM update)
         - $6.74 total billing / Stripe null = funded front operation
       8. Add to scripts/audit_results/evidence_tiers/tier1_smoking_gun.json if it exists, or create it
       9. Log all promotions to scripts/audit_results/evidence_tiers/promotion_log.json
       10. Write a COC entry to scripts/audit_results/prisma_coc_log.json:
       {
         "event": "vision_extraction_completed",
         "timestamp": "2026-03-13T23:00:00Z",
         "screenshots_processed": 41,
         "new_findings": ["...list key new finds..."],
         "output_file": "scripts/audit_results/prisma_reconstructed_db.json",
         "source_hashes": {"...": "..."},
         "chain": "rawdata/Screenshots → vision_extraction → prisma_reconstructed_db"
       }

       Key things to look for

       Edward's GitHub OAuth ID — Throughout the reconstructed data, look for any OAuthAccount table row where userId matches edward's ID patterns (cm7cze9b70000rr614w25...,
       cx7cze9h70000rr814w254ant, cn7cze9h700000rr614w25..., kahh, or any variant). If found, extract the provider_user_id field — that's his GitHub numeric ID.

       New suspicious accounts — Any account not previously documented that registered in Jan-Feb 2025.

       Service pricing anomalies — Confirm stripePriceId: null on all services.

       Output files

       After all 3 agents complete:
       11. scripts/audit_results/hash_manifest.json — updated with vision extraction files
       12. scripts/audit_results/prisma_reconstructed_db.json — unified Prisma DB reconstruction
       13. scripts/audit_results/evidence_tiers/tier1_smoking_gun.json — updated tiers
       14. scripts/audit_results/evidence_tiers/promotion_log.json — COC promotion log
       15. scripts/audit_results/prisma_coc_log.json — chain of custody for this run

       After completion

       Write a plain-language summary (2-3 paragraphs) that explains:
       16. What the Prisma DB is and how we got access to it
       17. What the reconstruction found (key numbers: VMs, users, billing)
       18. Why this matters (the most significant findings)

       This summary goes in launch/PRISMA-RECONSTRUCTION-SUMMARY.md — it will be used by journalists.