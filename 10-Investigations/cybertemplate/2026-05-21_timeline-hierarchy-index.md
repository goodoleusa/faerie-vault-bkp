# data/timelines/ — Canonical Timeline Hierarchy

**Generated:** 2026-05-21
**Mission:** timeline-canonicalization
**task_id:** timeline-hierarchy-master-to-actor-01

---

## ORIENTATION (60-second card)

Timelines used to be scattered across `data/`, `data/master/`, `data/4-viz/`, `data/viz/normalized/`, and `rawdata/`. This folder is the **one canonical place to start**. Pick by use case:

- **"Show me everything in one file."** → `00-master/master-timeline.csv` (392 rows, 2011-11-01 → 2026-05-20)
- **"Show me events by who did them."** → `10-by-actor/<russia|china|doge|foreign-unknown|federal-victim|observation>/`
- **"Show me events about a topic (CVE, Prisma, federal-exposure, network-topology)."** → `20-by-topic/<topic>/`
- **"I'm wiring this into a viz library (TimelineJS / vis.js / D3 / Mapbox)."** → `30-viz-ready/<library>/`

Originals remain at their legacy paths — this hierarchy is **agglomerated, not destructive**. See `_CHANGELOG.md` for the migration table.

---

## HIERARCHY

```
data/timelines/
├── _INDEX.md                            ← you are here
├── _CHANGELOG.md                        ← migration / move history (COC-style)
├── 00-master/
│   ├── master-timeline.csv              ← 392 rows, all curated sources union'd
│   ├── master-timeline.json             ← same data, JSON array
│   ├── _sources.md                      ← what was joined, dedup methodology
│   ├── _schema.md                       ← column definitions
│   ├── _stats.json                      ← row counts, date range, actor breakdown
│   └── _dedup-drops.json                ← which rows the dedup removed
├── 10-by-actor/
│   ├── _README.md                       ← actor-cluster taxonomy
│   ├── russia/                          ← AEZA + Baxet + STARK-INDUSTRIES
│   ├── china/                           ← ChinaNet + Alibaba + Treasury cert obs
│   ├── doge/                            ← Packetware + Prisma + DOGE personnel
│   ├── foreign-unknown/                 ← foreign-IP+gov-cert crossover, unresolved
│   ├── federal-victim/                  ← NLRB, Treasury, OPM, NNSA, FEMA
│   └── observation/                     ← 44k+18k+14k bulk scan rows + aggregates
├── 20-by-topic/
│   ├── _README.md                       ← topic taxonomy
│   ├── cve-exploitation/                ← SharePoint ToolShell + Commvault CVE
│   ├── federal-exposure/                ← federal cert/credential exposure events
│   ├── network-topology/                ← Packetware container starts + Shodan
│   └── prisma-anomalies/                ← suspicious users / VMs / billing
└── 30-viz-ready/
    ├── _README.md                       ← library compatibility matrix
    ├── timelinejs-knightlab/            ← Knightlab schema (voldemort firing arc)
    ├── vis-network-timeline/            ← vis.js Timeline JSON
    └── d3-force-graph/                  ← D3 force-graph nodes+links
```

---

## DECISION MATRIX — "If you need X, look at Y"

| You need | Go to | Why |
|---|---|---|
| Every timestamped event in one place | `00-master/master-timeline.csv` | Union of all curated sources, deduped |
| Events grouped by who caused them | `10-by-actor/<actor>/<actor>-timeline-from-master.csv` | Pre-filtered master subset |
| Full raw scan / cert / activity rows for an actor | `10-by-actor/<actor>/*.csv` (non-`from-master`) | Original source CSVs copied here |
| Topic-chapter for a report (e.g. CVE chapter) | `20-by-topic/<topic>/` | Curated single-purpose files |
| Curated narrative arc | `30-viz-ready/timelinejs-knightlab/voldemort-data-and-firing.csv` | Already Knightlab-schema |
| Dense event scatter | `30-viz-ready/vis-network-timeline/*.json` | vis.js shape |
| Actor relationship network | `30-viz-ready/d3-force-graph/*.json` | nodes + edges |
| Geo heatmap of events | `00-master/master-timeline.csv` + join with IP-geo | Need IP enrichment, see schema.md |

---

## VISUALIZATION LIBRARY COMPATIBILITY MATRIX

| Library | Best for | Source file | Schema notes |
|---|---|---|---|
| **TimelineJS (Knightlab)** | Curated narrative timeline w/ media + captions | `30-viz-ready/timelinejs-knightlab/voldemort-data-and-firing.csv` | Strict column names: `year,month,day,time,end_year,...,headline,text,media,...` |
| **vis.js Timeline** | Dense event scatter, zoom + group | `30-viz-ready/vis-network-timeline/timeline-curated.json` (and siblings) | Array of `{id, content, start, end?, group?, type?}` |
| **vis.js Network** | Actor relationship graph (force layout) | `30-viz-ready/vis-network-timeline/mega-timeline-config.json` | `{nodes: [...], edges: [...]}` |
| **D3 force-graph** | Cert-and-IP relationship clustering | `30-viz-ready/d3-force-graph/cert-timeline-d3.json` | `{nodes: [{id,group}], links: [{source,target,value}]}` |
| **Mapbox / Leaflet** | Geo cluster of events by actor | `00-master/master-timeline.csv` joined to IP-geo enrichment | Filter `lat,lon` non-empty, color by `actor_cluster` |
| **plain HTML table** | Quick scan for analysts | `00-master/master-timeline.csv` | Sort by `ts_iso`, filter by `hypothesis_tags` or `actor_cluster` |

---

## QUICK STATS

| Metric | Value |
|---|---|
| Master rows (deduped) | **392** |
| Dedup drops | 4 |
| Date range | 2011-11-01 → 2026-05-20 |
| Actor breakdown | observation 196 · doge 160 · federal-victim 27 · russia 5 · china 4 · foreign-unknown 0 |
| Hypothesis breakdown | NONE 155 · H2 82 · H1 54 · H3 32 · H1\|H2 28 · H4 11 · H5 9 · H1\|H3 7 · H2\|H4 6 · H1\|H4 4 · H3\|H4 4 |
| Topic row counts | prisma-anomalies 73 · federal-exposure 69 · cve-exploitation 25 · network-topology 6 |

> Note on `foreign-unknown=0`: the foreign-actor source CSVs (CERT_foreign-servers-with-gov-cert.csv, CROSSOVER_foreign-ips-with-gov-certs.csv, C_foreign-adversary.csv) are NOT in the curated narrative master — they are full IP-observation datasets and live in `10-by-actor/foreign-unknown/` as standalone files. They can be promoted into the master in a future pass if individual rows become narratively important.

---

## MIGRATION TABLE — legacy paths → canonical paths

| Legacy path | Canonical new path | Status |
|---|---|---|
| `data/TIMELINE_events.csv` | `00-master/master-timeline.csv` (joined) | agglomerated (original retained) |
| `data/TIMELINE_operational-master.csv` | `00-master/master-timeline.csv` (joined) | agglomerated |
| `data/TIMELINE_doge-media-events.csv` | `10-by-actor/doge/doge-media-events.csv` | copied |
| `data/TIMELINE_prisma-user-accounts.csv` | `10-by-actor/doge/doge-packetware-personnel-events.csv` + `20-by-topic/prisma-anomalies/prisma-user-accounts.csv` | copied (2x) |
| `data/TIMELINE_prisma-vm-lifecycle.csv` | `10-by-actor/doge/doge-packetware-vm-lifecycle.csv` + `20-by-topic/prisma-anomalies/prisma-vm-lifecycle.csv` | copied (2x) |
| `data/prisma/investigation_timeline.csv` | `10-by-actor/doge/doge-prisma-investigation.csv` | copied |
| `data/TIMELINE_daily-counts.csv` | `00-master/master-timeline.csv` (joined as DAILY_AGGREGATE) | agglomerated |
| `data/TIMELINE_citations.csv` | (kept at legacy path — superset of timeline.csv, no new info) | not copied |
| `data/timeline.csv` | (kept at legacy path — superseded by TIMELINE_citations) | not copied |
| `data/TIMELINE_argument.json` | (kept at legacy path — argument scaffold, not events) | not copied |
| `data/C--russia-aeza-cert-timeline.csv` | `10-by-actor/russia/russia-aeza-cert.csv` + 1 catalog row in master | copied + cataloged |
| `data/CERT_russia-aeza-gov-cert-timeline.json` | `10-by-actor/russia/russia-aeza-cert.json` | copied |
| `data/master/foreign-actor-proximity-russia/organization-cert-russia-aeza-gov-cert-timeline.json` | `10-by-actor/russia/russia-baxet-and-aeza-master-record.json` | copied |
| `data/C--china-alibaba-cert-observations.csv` | `10-by-actor/china/china-alibaba-cert.csv` | copied |
| `data/C--china-gov-certs.csv` | `10-by-actor/china/china-gov-certs.csv` | copied |
| `data/CERT_treasury-cert-ip-observations.csv` | `10-by-actor/china/china-treasury-cert-observations.csv` | copied |
| `data/CERT_treasury-cert-ip-observations-all.csv` | `10-by-actor/china/china-treasury-cert-observations-all.csv` | copied |
| `data/CERT_foreign-servers-with-gov-cert.csv` | `10-by-actor/foreign-unknown/foreign-actor-unknown-attribution.csv` | copied |
| `data/CROSSOVER_foreign-ips-with-gov-certs.csv` | `10-by-actor/foreign-unknown/foreign-crossover-gov-certs.csv` + `20-by-topic/federal-exposure/federal-foreign-ips-with-gov-certs.csv` | copied (2x) |
| `data/C_foreign-adversary.csv` | `10-by-actor/foreign-unknown/foreign-adversary-observations.csv` | copied |
| `data/A--treasury-dept.csv` | `10-by-actor/federal-victim/federal-treasury-dept-events.csv` + `20-by-topic/federal-exposure/federal-treasury-dept-events.csv` | copied (2x) |
| `data/A--treasury-hosts-same-fingerprint.csv` | `10-by-actor/federal-victim/federal-treasury-fingerprint-collisions.csv` | copied |
| `data/NETWORK_fema-foreign-sightings.csv` | `10-by-actor/federal-victim/federal-fema-foreign-sightings.csv` | copied |
| `data/viz/normalized/packetware-shodan-...csv` | `10-by-actor/doge/doge-packetware-shodan-scrape.csv` + master catalog row | copied + cataloged |
| `rawdata/packetware-shodan-...csv` | (kept at rawdata — `rawdata/` is immutable) | cataloged only |
| `data/viz/normalized/shodan-monitor-timeline.csv` | `10-by-actor/observation/observation-shodan-monitor.csv` + master catalog row | copied + cataloged |
| `data/viz/normalized/run008_timeline_index_...csv` | `10-by-actor/observation/observation-run008-index.csv` + master catalog row | copied + cataloged |
| `data/4-viz/TIMELINE.csv` | `10-by-actor/observation/observation-4viz-joined.csv` + master catalog row | copied + cataloged |
| `data/4-viz/EVIDENCE_bundle-doge-access-timeline.csv` | `10-by-actor/doge/doge-evidence-bundle-tier1.csv` (joined into master) | copied + joined |
| `data/4-viz/PRISMA_timeline.csv` | (duplicate of TIMELINE_prisma-user-accounts — not re-copied) | already represented |
| `data/4-viz/MAP_TIMELINE_DATA.json` | `30-viz-ready/vis-network-timeline/map-timeline-data.json` | copied |
| `data/4-viz/MEGA_TIMELINE_CONFIG.json` | `30-viz-ready/vis-network-timeline/mega-timeline-config.json` | copied |
| `data/4-viz/unified-timeline.json` | `30-viz-ready/vis-network-timeline/unified-timeline.json` | copied |
| `data/4-viz/timeline-curated.json` | `30-viz-ready/vis-network-timeline/timeline-curated.json` | copied |
| `data/4-viz/timeline-full.json` | `30-viz-ready/vis-network-timeline/timeline-full.json` | copied |
| `data/4-viz/cert_timeline_d3.json` | `30-viz-ready/d3-force-graph/cert-timeline-d3.json` | copied |
| `data/NETWORK_d3-graph.json` | `30-viz-ready/d3-force-graph/network-d3-graph.json` + `20-by-topic/network-topology/network-d3-graph.json` | copied (2x) |
| `data/NETWORK_packetware-container-starttimes.csv` | `20-by-topic/network-topology/network-packetware-container-starttimes.csv` | copied |
| `data/ACTOR_prisma-billing-anomalies.csv` | `20-by-topic/prisma-anomalies/prisma-billing-anomalies.csv` | copied |
| `data/ACTOR_prisma-suspicious-accounts.csv` | `20-by-topic/prisma-anomalies/prisma-suspicious-accounts.csv` | copied |
| `data/normalized/ev-commvault-cve-federal-window-...json` | `20-by-topic/cve-exploitation/cve-commvault-federal-window.json` | copied |
| `data/viz/normalized/knightlab_timeline_voldemort_...csv` | `30-viz-ready/timelinejs-knightlab/voldemort-data-and-firing.csv` (joined into master as NARRATIVE_BEAT) | copied + joined |

**`data/master/investigation-timeline/` JSON variants** — those files are auto-generated from the `data/TIMELINE_*.csv` sources by the existing data pipeline. They are not directly copied into the new hierarchy because their CSV originals already are. Keep them at the legacy path for now.

---

## REGENERATION

To rebuild from sources (idempotent):

```bash
cd /mnt/d/0local/gitrepos/cybertemplate
python3 forensics/ephemeral/2026-05-21/timeline-hierarchy-master-to-actor-01/build_timeline_hierarchy.py
```

The script reads from all source paths listed in `00-master/_sources.md` and writes master + actor-subsets + topic-subsets. To add a new source, edit the builder's `builders` list. To add a new actor cluster, extend the `VALID_ACTORS` constant AND `actor_from_event()` — do NOT introduce ad-hoc actor names outside that vocabulary.
