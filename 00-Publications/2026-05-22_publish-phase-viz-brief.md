# TERMINAL PUBLISH PHASE — TIMELINE + MAP VIZ BRIEF

**Meeting:** 2026-05-22 with UI dev team
**Goal:** pick visuals + datasets that best illustrate each report claim
**Outcome:** iteration roadmap + 3 prototype targets the dev team starts immediately
**Read time:** ~10 min cold. Page 1 is the whole picture; rest is detail.

---

## Page 1 — Index Card

### Core claims the report needs to visualize

| # | Hypothesis | Confidence | One-line |
|---|---|---|---|
| H1 | DOGE Insider Access via Credential Misuse | **0.95** | Access happened — timestamps prove it. Foundation of the report. |
| H2 | Packetware/Prometheus as Data Exfiltration Pipeline | 0.78 | Infrastructure was wired to move data through Packetware. |
| H3 | Federal Systems Exposed During DOGE Access Window | 0.78 | Sensitive federal systems were reachable during the access window. |
| H4 | Foreign Actor Proximity (statistical signal) | 0.55 | Foreign infrastructure proximate to the event cluster — suggestive only. |
| H5 | Financial Benefit | **0.00** | Empty result. Must be disclosed, NOT visualized as a finding. |

### The 3 prototypes to build this week

- **A. Master narrative timeline** — Knightlab TimelineJS, 18-25 hand-curated events from `data/timelines/30-viz-ready/timelinejs-knightlab/` (sister agent is preparing). Colored by hypothesis (H1/H2/H3/H4). Executive-summary entry point.
- **B. Geo + actor cluster map** — Mapbox GL JS (or Leaflet + CartoDB dark_all if API-key-free is required per mth00025). Plots Packetware/Hetzner/ChinaNet/Treasury/Vultr endpoints with cluster overlay + hypothesis filter.
- **C. Actor → asset network graph** — D3 force-directed, source `data/timelines/30-viz-ready/d3-force-graph/`. Nodes = actors (Aidan Perry, Member #278, Coristine, etc.) + assets (65.108.96.185, GameServerKings AS26863, Treasury IPs). Edges = activity events.

### One-sentence pitch for each prototype

A grabs the reader (story). B locates the threat (geography). C names the network (relationships). Together they cover the three reading modes journalists actually use.

---

## Section 1 — The story arc the visuals must support

For each hypothesis, the primary viz must land its strongest evidence. Confidence numbers below are CANONICAL from `cybertemplate/NECTAR.md`; do not invent new figures.

### H1 — DOGE Insider Access (conf 0.95) — FOUNDATION

- **Statement:** Edward Coristine + Aidan Perry (STAFF role, GitHub `UltraSive`) held Packetware credentials during the access window. Timestamps tie credential events to firewall + admin operations.
- **Best illustrated by:** Prototype A (TimelineJS) — narrative arc of 5-8 credential events (Jan 20 inauguration → clearance grant → first login → admin escalations → Feb 18 bulk-account event). H1 is the "open chapter."
- **Why this works:** Timestamps are the strongest evidence in the entire investigation. Prisma Activity table (18/19 events tied to Aidan Perry, Member #1) is itself a timeline — the data IS the chart.
- **Supporting datasheet:** `scripts/audit_results/unified_evidence_H1.json` (1,271 entities) + `data/ACTOR_doge-personnel-network.csv`.
- **Backup viz:** Vega-Lite cumulative-count chart of credential events vs. baseline access patterns. Less narrative, more "wow that's a step function."

### H2 — Packetware/Prometheus Exfiltration Pipeline (conf 0.78)

- **Statement:** Packetware infrastructure (single-peer ASN: GameServerKings AS26863) was wired as a data-handling pipeline; behavioral signal: 82 → 0 cessation on Feb 06 (H2 corroboration, confidence 0.82).
- **Best illustrated by:** Prototype C (D3 network graph) — Packetware as hub node, GameServerKings as upstream chokepoint, 65.108.96.185 + 65.108.96.158 as Hetzner management. Visual shows the single-peer fragility.
- **Why this works:** "Single upstream peer = single point of control" is a structural claim only a graph makes legible. Tables flatten it.
- **Supporting datasheet:** `data/B_doge-packetware.csv` + `data/ACTOR_prisma-billing-anomalies.csv`.
- **Backup viz:** vis.js timeline showing the 82→0 cessation event as a dense activity drop.

### H3 — Federal Systems Exposed (conf 0.78)

- **Statement:** Treasury + DOE/NNSA + Air Force systems showed exposure during the DOGE access window. Treasury cert cluster: 164.95.88.80, 164.95.204.27, 164.95.10.134 (LDAP exposure 164.95.88.30).
- **Best illustrated by:** Prototype B (Mapbox) — federal endpoints geolocated, exposure type as marker color, time-window slider showing only events during the access window.
- **Why this works:** Geography matches the claim shape ("federal systems" = government buildings + agency hosting); map is the natural argument.
- **Supporting datasheet:** `data/A--treasury-dept.csv`, `data/A--nnsa-doe-pan-vpn.csv`, `data/A--satods-air-force-rdp.csv`, `data/A--critical-defense-all.csv`.
- **Backup viz:** vis.js timeline of exposure events grouped by agency (rows = agency, marks = exposure events).

### H4 — Foreign Actor Proximity (conf 0.55) — SUGGESTIVE ONLY

- **Statement:** ChinaNet AS4134 endpoints (218.81.98.54 Shanghai, 111.172.x.x Wuhan "DOGE NAS"), Baxet/Aeza Russia infrastructure observed proximate to the cluster. **Proximity, not proof.**
- **Best illustrated by:** Prototype B (Mapbox) — secondary layer (dimmer, dashed-outline markers) over H3 endpoints. The visual treatment must encode "weaker confidence."
- **Why this works:** Geography is the only honest framing — "look how close they sit, draw your own line." Avoids overclaiming.
- **Supporting datasheet:** `data/C--baxet-aeza-russia.csv`, `data/C--china-alibaba-cert-observations.csv`, `data/C--china-gov-certs.csv`.
- **Backup viz:** Static map figure (no interactivity) with hand-drawn caveat block per NECTAR mandate ("consistent with" not "proves").
- **Visual discipline:** H4 markers MUST visually differ from H1-H3 (lower opacity, dashed border, "0.55" badge). If the dev cannot encode confidence visually, drop H4 from the map and keep it text-only.

### H5 — Financial Benefit (conf 0.00) — DO NOT VISUALIZE

- **Statement:** Empty. Examined across RUN-001 through RUN-008. No bank records, crypto wallets, or instrument transfers found.
- **Treatment:** One disclosure paragraph in the published report. NO viz. NO empty chart, NO "we looked here and found nothing" decoration. Showing absence as a visual lends it false weight.
- **Meeting question for dev team:** make sure no one is building H5 viz "for completeness."

---

## Section 2 — Visualization library decision matrix

| Library | Best for | Trade-offs | Datasheet | Recommendation |
|---|---|---|---|---|
| **TimelineJS (Knightlab)** | Curated narrative — 10-30 events with rich media (image, caption, link) | Slow with 100+ events; not interactive filtering; Google Sheets ingestion is the default but local JSON works | `data/timelines/30-viz-ready/timelinejs-knightlab/*.csv` (sister agent preparing) | **YES** — Prototype A (exec timeline) |
| **vis.js Timeline** | Dense event scatter, 100s-1000s of events, zoom + pan + grouping by lane | Visual hierarchy harder; needs custom CSS to look publication-grade | `data/timelines/30-viz-ready/vis-network-timeline/*.json` | **YES** — full-evidence backup timeline (Section 6 of report) |
| **D3 force-graph** | Actor → asset relationship; clustering; structural arguments (single-peer ASN) | Layout instability across reloads; needs label nudging; mobile painful | `data/timelines/30-viz-ready/d3-force-graph/*.json` | **YES** — Prototype C (actor network) |
| **Mapbox GL JS** | Geo hotspots, vector tiles, smooth zoom, layer toggling | Requires API key + token rotation; budget cost at high traffic | `data/timeline.csv` (needs lat/lon enrichment) + `data/A--*.csv` | **YES** — Prototype B preferred. Fallback below if key-free required. |
| **Leaflet + CartoDB dark_all** | Same as Mapbox but no API key (per mth00025); dark theme matches report aesthetic | Fewer style controls; raster tiles only | same as above | **YES** — drop-in fallback for Prototype B |
| **Plotly Sankey** | Money/data flow between actors | Hard to read with >10 sources/sinks; H5 is empty so no funds-flow story | n/a | **NO** — H5 is empty; skip |
| **Vega-Lite** | Statistical charts (timeline density, cumulative count, Bonferroni-corrected p-value plot) | Less storytelling, more analysis; small footprint, embeds anywhere | `data/timeline.csv` + `scripts/audit_results/*.json` | **YES** — H1 backup + the statistical spine sidebar |
| **Custom React + d3** | Anything specifically tailored | High dev time; no community templates | any | **LAST RESORT** — pick a library first, customize second |

**Rule for the meeting:** if a viz cannot be built in TimelineJS, vis.js, D3, Mapbox/Leaflet, or Vega-Lite, it gets dropped from this iteration. No custom React unless one of the prototypes proves blocking.

---

## Section 3 — The 3 prototypes — concrete specs for the dev team

### Prototype A — Master Narrative Timeline (TimelineJS)

- **Purpose:** Executive entry point. Reader scrolls through 18-25 events and understands the arc without reading the report.
- **Source data file:** `data/timelines/30-viz-ready/timelinejs-knightlab/master-timeline.csv` (sister agent's output)
- **Required fields:** `start_date, end_date, headline, text, media_url, media_caption, media_credit, group (=hypothesis H1/H2/H3/H4), background_color`
- **Visual style:**
  - Color by hypothesis: H1 magenta, H2 teal, H3 cyan, H4 gold (bearing palette per CLAUDE.md). Bearing colors = N=magenta, S=teal, E=cyan, W=gold; mapping to H1-H4 keeps continuity with system-wide language.
  - Font: Space Grotesk (headlines) + Inter (body) — matches faerie storefront design system.
  - Background: dark (#1a1a2e or similar) to match the dark report theme.
  - Interactivity: scroll-through, click to expand, no filter chips (TimelineJS doesn't filter natively).
- **Acceptance criteria:**
  - Shows H1 access events (Jan 20 → Feb 18) as a clear narrative spine.
  - Shows H2 Packetware infrastructure events.
  - Shows H3 federal exposure events (Treasury, NNSA, Air Force).
  - Shows H4 events with visual de-emphasis (lower saturation, "suggestive" tag).
  - Renders on mobile (TimelineJS responsive mode).
  - Loads in <3s on 4G.
- **Iteration order:** static CSV → render → review event selection → tune copy → add media → review again.

### Prototype B — Geo + Actor Cluster Map (Mapbox or Leaflet+CartoDB)

- **Purpose:** Locate the threat. Reader sees "this is where the federal systems are; this is where the foreign infrastructure sits; this is the overlap."
- **Source data file:** `data/timeline.csv` (76 events, enriched with lat/lon) + `data/A--*.csv` (federal) + `data/C--*.csv` (foreign)
- **Required fields:** `lat, lon, ts_iso, agency, actor_cluster (federal|packetware|china|russia|doge), event_type, hypothesis (H1|H2|H3|H4), evidence_id`
- **Visual style:**
  - Tile layer: CartoDB dark_all (no API key required per mth00025) OR Mapbox dark-v11 if key is approved.
  - Marker color by `actor_cluster`: federal=cyan, packetware=teal, china=gold, russia=red, doge=magenta.
  - H4 markers: lower opacity (0.5), dashed border, "0.55" badge in popup.
  - Aggregate cluster markers (per mth00025) when zoomed out.
  - Dark popups (per mth00025).
  - Time-window slider: highlight only events within the DOGE access window.
- **Acceptance criteria:**
  - Treasury cert cluster (164.95.88.80, .204.27, .10.134) visible as DC-area dots.
  - Packetware Hetzner endpoints (65.108.96.185, .158) in Helsinki.
  - ChinaNet Wuhan + Shanghai endpoints visible with H4 visual treatment.
  - Filter by hypothesis works (toggle H1/H2/H3/H4).
  - No API key required in fallback mode.
- **Iteration order:** ingest CSV → render dots → cluster markers → popup styling → time slider → hypothesis filter.

### Prototype C — Actor → Asset Network Graph (D3 force-directed)

- **Purpose:** Name the network. Reader sees who connects to what, and the GameServerKings-AS26863 single-peer fragility becomes visually obvious.
- **Source data file:** `data/timelines/30-viz-ready/d3-force-graph/network.json` (sister agent's output)
- **Required fields:**
  - `nodes[]`: `id, label, type (actor|asset|asn|agency), confidence, hypothesis, size_metric (activity_count or similar)`
  - `links[]`: `source, target, kind (credential|hosts|peers|connects), weight, ts_iso`
- **Visual style:**
  - Force-directed layout, charge -300, link distance 80.
  - Node color by `type`: actor=magenta, asset=teal, asn=gold, agency=cyan.
  - Node size by activity_count (Aidan Perry = largest among actors per Prisma Activity 18/19 events).
  - Edge thickness by weight.
  - Hover: show node details + outgoing edges highlighted.
  - Click: pin node + show all evidence_ids in side panel.
- **Acceptance criteria:**
  - Aidan Perry, Member #278, Edward Coristine visible as actor nodes.
  - GameServerKings AS26863 visible as upstream node with only Packetware peering (single-peer claim legible).
  - 65.108.96.185 + .158 as Hetzner management cluster.
  - Treasury IP cluster grouped.
  - China/Russia infrastructure visually separated (H4 lower opacity).
- **Iteration order:** ingest JSON → render force layout → label nudging → color + size encoding → hover/click → side panel.

---

## Section 4 — Iteration plan with the dev team

| Day | Activity | Output |
|---|---|---|
| **Day 1 (2026-05-22 meeting)** | Walk the dev team through Sections 1-3. Assign one owner per prototype. Lock data file paths. Lock library choices. Identify the 5-8 H1 events for Prototype A. | Owner assignments + locked data paths in meeting notes |
| **Day 2-3** | Dev builds Prototype A (TimelineJS narrative). Hourly feedback loop: screenshot share + pair review on event selection, copy, color encoding. | Working TimelineJS at staging URL |
| **Day 4-5** | Dev builds Prototype B (map). Hourly feedback loop on marker style + H4 visual treatment + cluster behavior. | Working map at staging URL |
| **Day 6-7** | Dev builds Prototype C (network). Hourly feedback loop on layout stability + labeling + side-panel content. | Working network at staging URL |
| **Week 2** | Integrate all 3 into the report's HTML/landing page. Cross-link from prose sections to specific viz events (e.g. "see Timeline event H1-04"). | Integrated report draft |
| **Week 2-3** | Editorial review pass + caveat audit (H4 visual de-emphasis, H5 disclosure paragraph). | Editorial sign-off |

**Iteration cadence:** 1-2 hour review cycles during dev days. Screenshot-share in shared channel, pair-review on the hardest 2-3 decisions per cycle. No daily standups — the screenshot stream IS the standup.

---

## Section 5 — Critical questions for the meeting

Walk in prepared to answer or ask:

1. Which 3-5 events MUST be in the executive timeline? (TimelineJS works best with ≤25 events; over that, readers bounce.)
2. Which audience are we publishing for first — journalists, infosec community, or policymakers? Affects viz density, technical-jargon level, and whether we lead with timeline or with map.
3. What's the deadline for the published report? (Drives whether Week 2 integration is realistic or whether we ship prototypes serially.)
4. Who owns the dev for each prototype? One owner per prototype is faster than committee dev; can the team commit?
5. Are we using TimelineJS verbatim (embed) or building on top of it (custom layer)? Embed is 2 hours; custom is 2 weeks. Default to embed.
6. Do we want filter-by-hypothesis interactivity on every viz, or static narrative? Recommendation: TimelineJS static, Map filterable, Network filterable.
7. H4 visual de-emphasis — does the dev team have a strong opinion on opacity vs. dashed border vs. badge? Pick one in the meeting; don't iterate later.
8. Mapbox API key approval status? If not approved by Day 4, fallback to Leaflet + CartoDB is mandatory (no scrambling mid-iteration).
9. Mobile-first or desktop-first? Report readers (journalists, policymakers) skew desktop; mobile must work but desktop wins ties.
10. Who has final editorial approval on H4 caveats, H5 disclosure paragraph, and "consistent with" vs "proves" language? Lock the editor in the meeting.

---

## Section 6 — Risks + open questions

- **Data gaps.** The sister agent's work on `data/timelines/30-viz-ready/` is in flight; if those files aren't ready by Day 2, Prototype A is blocked. Mitigation: have raw `data/timeline.csv` ready as fallback ingestion source.
- **H4 overclaim risk.** Foreign-actor proximity is statistical only. If the dev team builds a map that visually equates H1 and H4 marker styles, the report's caveat collapses. Lock visual de-emphasis in the meeting; do not defer.
- **H5 absence-of-evidence trap.** If anyone proposes an "empty chart" or "we searched here" viz for H5, refuse it. Disclosure paragraph only.
- **IP/legal review for hosting evidence.** Lat/lon of state-actor endpoints + named individuals (Aidan Perry full identifiers in NECTAR) need legal sign-off before publication. Add to meeting agenda; do not assume.
- **Compute cost of heavy D3 in browser.** Network graph with 200+ nodes can melt low-end mobile. Set a node-count budget (≤150 visible at default zoom).
- **Mobile responsiveness expectations.** TimelineJS is responsive. vis.js is OK. D3 force-graph is brittle on mobile. Decide acceptable mobile degradation in the meeting (e.g. "show static PNG fallback on <768px").
- **Mapbox API key budget.** If usage exceeds free tier during launch traffic, swap to Leaflet+CartoDB mid-publication. Have the fallback wired Day 4.
- **Library version pinning.** TimelineJS, vis.js, D3, Mapbox — pin versions in the report's HTML. Live CDN refs break two years from now; the report needs to survive.
- **Citation linkage.** Every viz event must carry `evidence_id` so readers can trace to `cybertemplate/scripts/audit_results/unified_evidence_H*.json`. Non-negotiable; check in every review cycle.

---

## Appendix — Quick reference

- **Hypotheses + confidence:** H1=0.95, H2=0.78 (behavioral 0.82), H3=0.78, H4=0.55, H5=0.00. From `cybertemplate/NECTAR.md`. Do not adjust.
- **Bearing color palette (system-wide):** N=magenta, S=teal, E=cyan, W=gold. Used for H1/H2/H3/H4 mapping in all three prototypes.
- **Canonical timeline source:** `data/timeline.csv` (76 events, May 2024 → Nov 2025).
- **Viz-ready outputs (sister agent):** `data/timelines/30-viz-ready/{timelinejs-knightlab,vis-network-timeline,d3-force-graph}/`
- **Evidence backing each hypothesis:** `scripts/audit_results/unified_evidence_H{1,3}.json` (H2/H4 use Amanda's analysis files referenced in NECTAR).
- **Methodology canonical:** `docs/200-METHODOLOGY-CANONICAL.md`.
- **Disclosure timeline:** `docs/DISCLOSURE-TIMELINE.md`.

**This brief is the meeting agenda. Walk through Page 1 in the first 5 minutes. Sections 1-3 in the next 20. Sections 4-6 in the last 15. Done.**
