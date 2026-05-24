# 00-master — Source provenance + dedup methodology

**Generated:** 2026-05-21 by `forensics/ephemeral/2026-05-21/timeline-hierarchy-master-to-actor-01/build_timeline_hierarchy.py`
**Mission:** timeline-canonicalization
**task_id:** timeline-hierarchy-master-to-actor-01

`master-timeline.csv` is the UNION of all curated event-timeline sources, plus one CATALOG row per high-volume observation-tier source (Shodan / cert scans) so the master remains navigable without dumping 80k+ scan rows. The full observation rows live one folder deeper at `10-by-actor/observation/`.

## Sources joined into the master (curated events)

| Source file | Rows contributed | Notes |
|---|---|---|
| `data/TIMELINE_events.csv` | 61 | Primary curated event timeline (date, actor, hypothesis, evidence_tier) |
| `data/TIMELINE_operational-master.csv` | 61 | Operational-master view; overlaps TIMELINE_events but retained for citation_url parity |
| `data/TIMELINE_doge-media-events.csv` | 34 | Media-reported DOGE events by date (agency, link, additional_link) |
| `data/TIMELINE_prisma-user-accounts.csv` | 25 | Suspicious Prisma DB user accounts + flags |
| `data/TIMELINE_prisma-vm-lifecycle.csv` | 11 | VM CREATE/DELETE events from Prisma activity log |
| `data/prisma/investigation_timeline.csv` | 25 | Investigator-curated Prisma reconstruction timeline |
| `data/4-viz/EVIDENCE_bundle-doge-access-timeline.csv` | 12 | Tier-1 evidence bundles (smoking-gun + strong-support items) |
| `data/viz/normalized/knightlab_timeline_voldemort_data_and_firing.csv` | 8 | Narrative beats (Knightlab TimelineJS format — Voldemort/firing arc) |
| `data/TIMELINE_daily-counts.csv` | 153 | Per-day aggregate counts (A_usgov / B_doge / C_foreign) |

## Catalog rows (observation-tier sources referenced, not row-joined)

These files are too voluminous to fold into the master without drowning narrative events. One catalog row each is emitted with `event_type=OBSERVATION_SOURCE_CATALOG`; `raw_payload` holds the row count and byte size. Full data lives at the original path AND under `10-by-actor/observation/` or the relevant actor cluster.

| Source file | Cluster | Row count | Reason for catalog-only |
|---|---|---|---|
| `data/C--russia-aeza-cert-timeline.csv` | russia | ~1,914 | Cert observations — dense scan output |
| `data/viz/normalized/packetware-shodan-netrange-63_141_38_0-24-sept-4-2025-timeline-scrape_normalized.csv` | doge | ~501 | Packetware AS400495 Shodan scrape |
| `rawdata/packetware-shodan-netrange-63.141.38.0-24-sept-4-2025-timeline-scrape.csv` | doge | ~3,915 | Raw Packetware scrape (pre-normalization) |
| `data/viz/normalized/shodan-monitor-timeline.csv` | observation | ~14,817 | Broad Shodan monitor alerts |
| `data/viz/normalized/run008_timeline_index_20260322T185838Z.csv` | observation | ~18,683 | RUN008 cross-source index |
| `data/4-viz/TIMELINE.csv` | observation | ~44,346 | 4-viz master scatter (joined Shodan + PRISMA + cert obs) |

## Dedup methodology

Key: SHA-256 of `ts_iso | source_file | raw_payload` (truncated to first 16 hex chars).
Strategy: first-write-wins (the build order preserves curated narrative sources before catalog/aggregate). Drops are logged to `_dedup-drops.json` for auditability.

## Hypothesis tag mapping

Tags are normalized to a fixed vocabulary `{H1, H2, H3, H4, H5, NONE}` via case-insensitive substring extraction from each source's `hypothesis` / `hypothesis_support` / `hypothesis_tags` field. Multi-tag rows pipe-separate (e.g. `H1|H2`).

| Tag | Meaning |
|---|---|
| H1 | DOGE-staffed unauthorized federal access |
| H2 | DOGE automated infrastructure pipeline (Packetware-orchestrated) |
| H3 | Federal credential / data exposure (NLRB, Treasury, Commvault) |
| H4 | Foreign-actor proximity (Russia / China / state-sponsored APT) |
| H5 | Whistleblower retaliation / personnel firing arc |
| NONE | No hypothesis tagged (typically observation or aggregate rows) |

## Actor cluster mapping

Mapping is best-effort, conservative — uses keyword scan over `actor`, `description`, `source`, and `hypothesis` columns. Vocabulary fixed at `{russia, china, doge, foreign-unknown, federal-victim, observation}`. Rows that fail to attribute fall back to `observation`.
