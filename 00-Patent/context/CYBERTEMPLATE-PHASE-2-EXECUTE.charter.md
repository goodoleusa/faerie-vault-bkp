---
type: charter
status: declared
created: 2026-05-19
promoted_from: docs/_human-inbox/CYBERTEMPLATE-PHASE-2-EXECUTE.mission
bearing: S
ship_gate: yes
---

# Mission — Execute cybertemplate Phase 2 + 3 (six-script refinement chain)

## Scope expanded 2026-05-19

Per user directive "JUST EXECUTE" + agent-B's refinement-order, this mission produces **all six scripts** from the agent-B refinement sequence — authored together because they share inputs (the stage-manifest JSON) and depend on each other sequentially.

## ⚠ PRESERVATION RULE (operator directive 2026-05-19)

**"everything on these pages is important, just needs refinement. comprehensive, not reductive. no IMPORTANT CASE WRITING OR EVIDENCE OR CONCLUSIONS lost."**

Before ANY script in this mission runs, the **TC-PRE forensic snapshot** documented in `forensics/2026-05-19-ui-inbound-link-map.md` MUST complete: every retired-slug page snapshotted byte-faithful to `data/_archive/2026-05-19-pre-consolidation/{slug}.html` with SHA256SUMS + a `pre_consolidation_snapshot` COC entry. The snapshot is the recovery substrate and the audit baseline.

Every script in this mission MUST:
- Be **comprehensive, not reductive** — when consolidating content, every paragraph survives byte-faithful in a `<section id="from-{slug}">` block.
- Refuse to run if `data/_archive/2026-05-19-pre-consolidation/SHA256SUMS` doesn't exist.
- Compare its proposed changes against the TC-PRE snapshot when applicable, and emit a `content_preservation_check` COC entry confirming byte-faithfulness. Original three deliverables (`build-timeline.py` + `_redirects` + 17-page port checklist) remain; four additional scripts added below.

The six scripts (in execution order, all authored by this mission):

| # | Script | Reads | Writes | COC entry kind |
|---|---|---|---|---|
| 1 | (already produced) `forensics/2026-05-19-timeline-stage-manifest.json` | spec-agent's analysis | n/a | n/a (data) |
| 2 | `scripts/coc_tag_timeline_stages.py` | stage-manifest.json | COC entries only (no file moves) | `data_transform` (operation: `stage_tag`) |
| 3 | `scripts/rename_data_stage_folders.py` | charter Phase-2 rename map | `git mv` + COC entries | `promotion` |
| 4 | `scripts/refine_timeline_master.py` | stage-1 normalized CSVs | `data/3-master/timeline/*.csv` (schema-conformant) | `data_normalize` |
| 5 | `scripts/build-timeline.py` | `data/3-master/timeline/*.csv` | `data/4-viz/timeline/*.json` | `data_transform` (operation: `viz_build`) |
| 6 | `scripts/snapshot_for_public.py` | stages 2+3 | public-repo `data/` mirror + `published-{date}.coc.jsonl` + `SHA256SUMS` | `promotion` (operation: `publish_snapshot`) |

Each script is idempotent. Each emits one COC entry per file it touches via the data-ingest skill's `CocChain`. Each accepts `--dry-run` and `--verify` flags. Each refuses to run if its prereq stage isn't satisfied (e.g., refine_timeline_master refuses if stage-manifest.json reports any L1 file still missing schema-conformance prereqs).

## Prereqs (must exist before claiming)

- `cybertemplate/forensics/2026-05-19-timeline-centralization-plan.md` (spec-agent output)
- `cybertemplate/forensics/2026-05-19-ui-inbound-link-map.md` (audit-agent-C output)
- `cybertemplate/forensics/2026-05-19-timeline-stage-manifest.json` (agent-B's stage-routing-table — to be authored as part of spec-agent's work or this mission's first sub-task)
- Branch `dev/astro-consolidation-2026-05-19` pushed to `origin` (astro-branch-agent output)

Check all four; if any missing, leave a `.blocked` file naming which and stop.

## Goal — three artifacts the user asked for literally

### Artifact 1: `scripts/build-timeline.py` (Layer 1 → Layer 2 generator)

Reads the 7 canonical CSVs from `data/3-master/timeline/`, writes the 5 L2 artifacts to `data/4-viz/timeline/`. Specifically:
- Concatenate all 7 L1 sources, dedupe by `(ts, source, event_type)` tuple, sort by `ts` → `unified-timeline.json`
- Filter `unified-timeline.json` to `confidence >= 0.7` AND `event_type IN (story-grade enum)` → `timeline-curated.json`
- Geo-join `cert-observations.csv` + `shodan-monitor.csv` with `data/3-master/ips/` lookup → `MAP_TIMELINE_DATA.json`
- Reshape cert events for D3 → `cert_timeline_d3.json`
- Leave `MEGA_TIMELINE_CONFIG.json` untouched (hand-edited config)
- Emit one `data_transform` COC entry per output via the data-ingest skill's `CocChain` shim

CLI:
```
python3 scripts/build-timeline.py [--verify] [--dry-run]
```

### Artifact 2: `web/public/_redirects` (Cloudflare Pages redirect table)

Authored from audit-agent-C's `forensics/2026-05-19-ui-inbound-link-map.md`. ~35 entries mapping retired slugs → canonical anchors:
```
/timeline.html       /timeline-master.html#from-timeline       301
/evidence.html       /evidence-hub.html#from-evidence          301
/report.html         /investigation-report.html                301
...
```
Plus any explicit overrides for `map.html` (KEEP — never redirected).

### Artifact 3: `forensics/2026-05-19-17-page-port-checklist.md`

Line-by-line port checklist for the 17 canonical pages from Jess's preserved `site/` folder onto Astro. Format per page:
```
## site/timeline-master.html

- [ ] git checkout preserved/defenders-main-2026-05-19 -- site/timeline-master.html
- [ ] mv site/timeline-master.html web/src/pages/timeline-master.astro
- [ ] Wrap in <Layout title="Timeline">...</Layout>
- [ ] Replace fetch('data/...') with build-time `import data from '../../../data/4-viz/timeline/unified-timeline.json'`
- [ ] Verify `npm run build` succeeds with this page included
- [ ] Add `<link rel="canonical">` to /timeline-master
- [ ] Smoketest: `curl -sf http://localhost:4321/timeline-master | grep -q <title>`
- [ ] Commit message: `astro-port: timeline-master.html → web/src/pages/timeline-master.astro`
```

## Order of execution

1. Verify prereqs.
2. Author `web/public/_redirects` (smallest deliverable, no dependencies beyond agent-C).
3. Author `scripts/build-timeline.py` (uses the L1 schema from the spec doc).
4. Author the 17-page port checklist (uses both inputs).
5. Run `python3 scripts/build-timeline.py --dry-run` to validate the L2 schema before any actual file writes.
6. Append a single `phase2_artifacts_ready` COC entry referencing all three deliverables by sha256.

## Constraints

- DO NOT execute the 17-page port itself. The checklist is for a later session/agent. This mission produces the *checklist*, not the ports.
- DO NOT write the `_redirects` if agent-C's inbound-link map is empty or malformed — drop a `.blocked` file naming the issue.
- DO NOT modify Jess's preserved tags or `defenders` branches.
- Bash heredocs for all writes. Verify each with `ls -la`.
- Append the same COC chain that prior session entries use.

## Bearing
S (ship — these three are the gate to Phase 3, which is the actual ports).

## See also
- `forensics/charters/2026-05-19/consolidate.data-pipeline.cybertemplate.rawdata-to-ui.md` — parent
- `forensics/2026-05-19-timeline-centralization-plan.md` — spec for build-timeline.py
- `forensics/2026-05-19-ui-data-dependency-map.md` — outbound deps (agent-B)
- `forensics/2026-05-19-ui-inbound-link-map.md` — inbound deps (agent-C)
- `forensics/2026-05-19-cybertemplate-data-audit.md` — whole-repo inventory (agent-A)
