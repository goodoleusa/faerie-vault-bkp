# data/timelines/_CHANGELOG.md — COC-style migration trail

Every move and data transform that produced this hierarchy is logged in `forensics/coc.jsonl` (the canonical chain-of-custody ledger). This file is the human-readable cross-reference.

## 2026-05-21 — Initial creation

**Task:** `timeline-hierarchy-master-to-actor-01`
**Mission:** `timeline-canonicalization`
**Bearing:** S (ship to staging — meeting tomorrow on timeline + map viz)
**Builder script:** `forensics/ephemeral/2026-05-21/timeline-hierarchy-master-to-actor-01/build_timeline_hierarchy.py`

### What was created

- `data/timelines/_INDEX.md` (canonical map + decision matrix)
- `data/timelines/00-master/master-timeline.csv` (392 rows, UNION of curated sources)
- `data/timelines/00-master/master-timeline.json` (same data, JSON array)
- `data/timelines/00-master/_sources.md` (provenance + dedup methodology)
- `data/timelines/00-master/_schema.md` (column definitions)
- `data/timelines/00-master/_stats.json` (row counts, date range, breakdowns)
- `data/timelines/00-master/_dedup-drops.json` (audit log of dedup decisions)
- `data/timelines/10-by-actor/{russia,china,doge,foreign-unknown,federal-victim,observation}/` with per-actor source copies + master-derived subsets + READMEs
- `data/timelines/20-by-topic/{cve-exploitation,federal-exposure,network-topology,prisma-anomalies}/` with topic source copies + master-derived subsets + README
- `data/timelines/30-viz-ready/{timelinejs-knightlab,vis-network-timeline,d3-force-graph}/` with library-specific shapes + README
- `data/timelines/20-by-topic/cve-exploitation/cve-window.csv` (NEW — curated from `rawdata/Treasury Commvault China Article/sharepoint-vuln-timeline.md`; only new content created in this consolidation)

### What was preserved (legacy paths untouched)

All originals at their pre-consolidation paths remain in place — this consolidation is **agglomerative**, not destructive. The git history is the lineage record; the COC entries in `forensics/coc.jsonl` are the per-file audit trail.

### Files NOT moved this pass

- `data/TIMELINE_citations.csv` — superset of `data/timeline.csv`; superseded by `00-master/` content
- `data/timeline.csv` / `data/timeline.json` — duplicates of TIMELINE_citations
- `data/TIMELINE_argument.json` — argument scaffold, not events
- `data/4-viz/PRISMA_timeline.csv` — duplicate of TIMELINE_prisma-user-accounts
- `data/4-viz/ACTOR_*.csv` — `ACTOR_prisma-*` were copied; `ACTOR_doge-personnel-network` is a graph, not a timeline
- `data/master/investigation-timeline/*.json` — auto-generated from data/TIMELINE_*.csv; consolidation focuses on CSV originals
- `data/cybertemplate-october-2025-normalized/viz-october-2025-timeline.json` — superseded by 4-viz/unified-timeline.json
- `data/viz/normalized/operational-timeline-master.csv` — exact duplicate of `data/TIMELINE_operational-master.csv`

### Promotion criteria (future passes)

- Foreign-unknown rows promote to `russia/` or `china/` when attribution ≥ 0.85 confidence
- Observation-tier rows promote into the master when individually narratively important (manual decision)
- New source files: add to the builder's `builders` list + run; do NOT hand-edit master outputs

### COC chain entries

See `forensics/coc.jsonl` — every move + transform listed in this changelog has a corresponding `type=data_move`, `type=data_transform`, `type=doc_create`, or `type=script_create` entry chained from the prior tail. Run `python3 scripts/9x_coc_verifier.py --coc-file forensics/coc.jsonl` to verify chain continuity.
