---
date: 2026-03-23
sprint: RUN009-011
status: complete
type: meta
tags: []
doc_hash: sha256:d7f59f85843694d704751db71f52949ee406892a60e209c55a3bf075bef5f64c
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:16:31Z
hash_method: body-sha256-v1
---

# Sprint Close — data/ Directory Finalized

## What was accomplished

### COC — RUN011 (viz/ hash sweep)
- 585 files in viz/ hashed (263 MB) → `hash_manifest_RUN011_viz.json`
- GAP-1 (viz/ excluded from all manifests) RESOLVED
- Tier 1: 4 viz/ items verified (sha256=fac79bbb confirmed)
- Tier 2: 33 null sha256 fields filled, 2 verified (35 total viz/ refs)

### data/ as canonical site product
| File | Description | Rows |
|------|-------------|------|
| TIMELINE_events.csv | Master narrative event timeline (tier-ranked) | 61 |
| TIMELINE_citations.csv | Archive-tracked citation record (site source) | 76 |
| TIMELINE_daily-counts.csv | Daily IP counts A/B/C | 153 |
| TIMELINE_argument.json | D3-ready with key dates + stats | 153+7 |
| SECTOR_risk-summary.csv | Per-sector evidence + tier counts | 7 |
| METHODS.md | Data provenance + limitations | — |

### Evidence tier ranking in TIMELINE_events.csv
New columns: `evidence_tier` (1/2/blank), `evidence_tier_label` (smoking_gun/strong_support/untiered), `quality_score`, `evidence_bundle`

Distribution: 32 Tier 1 events, 21 Tier 2, 8 untiered

### Key stats confirmed this sprint
- Fisher exact: OR=123.7, p<10⁻¹⁰⁰ (cert multi-country overlap)
- LANL cert: Fisher p=0.0021, Bonferroni p=0.0042 (Tier 2, STAT-NEW-001)
- ahmn.co = Packetware-operated (P=0.78, Tier 2 update)
- TIMELINE_events.csv: Tier 1 events span PRISMA-MUSKOX (5.0/5) through BGP/cert findings (4.4/5)

## Open items for next session
- `timeline.html` still fetches `viz/timeline.csv` — should be updated to `data/TIMELINE_citations.csv`
- 8 untiered events in TIMELINE_events.csv need curation (CORUNA-GTIG-2025, PRISMA-MRCOMQ, etc.)
- Tier 2 sha256 backfill for scripts/audit_results/ files still pending (GAP-2)
- Live WHOIS for ahmn.co registrant (needs WebFetch)
- report.html cert language update pending: "certificates appeared" → more precise language
