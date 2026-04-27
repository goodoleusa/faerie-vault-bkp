---
type: agent-review-item
cat: CONNECTION
priority: HIGH
agent: evidence-curator
ts: 2026-03-22T22:00:00Z
review_status: unreviewed
tags: [review, connection, human-inbox]
doc_hash: sha256:77e9fed41d1c3320cf2e7167578e20e5785a408cbb4c1f58a2db7a5bb6572bcb
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:36Z
hash_method: body-sha256-v1
---

# ProxMox projectId a45bkg9pb95tgb8 == Prisma userId a458bkg9pb95tgb8 == Aidan Perry confirmed P=0.995

4 independent evidence paths: (1) prisma_reconstructed_db.json id_variants field; (2) prisma_entity_linkage.json Member id=1 FK; (3) HTML vs Gemini OCR transposition documented in PRISMA_RECONSTRUCTION_METHODOLOGY.md line 110; (4) All ADMIN-role Member records in primary project reference same entity. Feb 18 timeline: same operator (a458bkg9pb95tgb8) conducted mass VM cleanup at 19:18:41 and was re-added as Member id=183 at 19:32:27 — 14 minutes later — consistent with scripted teardown + re-provisioning. NO NEW TIER 1 promotion — finding subsumed in PRISMA-MUSKOX (quality=5.0, same source file).
Files: scripts/audit_results/userid_crossref.json, scripts/audit_results/prisma_reconstructed_db.json, scripts/audit_results/prisma_entity_linkage.json
Next: Cross-ref a458bkg9pb95tgb8 membership (ids 183, 184, 188, 189) against project table to identify additional project contexts operator accessed.

---
*Source: REVIEW-INBOX · Agent: evidence-curator · 2026-03-22*
