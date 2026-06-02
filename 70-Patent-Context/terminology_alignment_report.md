# Terminology Alignment Report — MAP / COMPASS / CHARTER

**task_id:** mission-architecture-enforcement
**investigation_label:** mission-architecture-enforcement
**Reference model:** `docs/44-MISSION-NAVIGATION-MODEL.md`

## Three-Layer Model Alignment

### Layer 1: MAP — emergent territory of discovered work

| Property | Canonical Spec | Code Reality | Verdict |
|----------|----------------|--------------|---------|
| Storage | `forensics/mission-trails/{investigation_label}/{YYYY-MM-DD}/` | EXISTS — 35 trail directories | ALIGNED |
| Pheromone marker | investigation_label | 425 occurrences across scripts/hooks | ALIGNED |
| Compass edges (paths between missions) | discovered during work, in manifests | `compass_edge` field, 160 occurrences | ALIGNED (string form, not vector form) |
| Builder | mission-trails scanner | `0x_mission_trail_builder.py` (wired in settings.json:102) | ALIGNED |
| Crystallization | matures stalled trails | `1x_mission_crystallizer.py` (wired in settings.json:124) | ALIGNED |

**Layer 1 status: WORKING.** The MAP grows stigmergically, exactly as specified.

### Layer 2: COMPASS — bearing vectors for dead-reckoning

| Property | Canonical Spec | Code Reality | Verdict |
|----------|----------------|--------------|---------|
| Bearing direction | N/S/E/W string | string `compass_edge` | PARTIAL |
| Vector representation | `next_mission_node = {bearing, task_id, from_label, to_label}` | `next_task_queued` (string task_id) + `compass_edge` (string letter) | DRIFT |
| FROM mission | `from_label` field | implicit in agent's own `investigation_label` | DRIFT |
| TO mission | `to_label` field | NOT REPRESENTED | MISSING |
| Producer count | every manifest | 0 scripts produce dict form | MISSING |
| Consumer tolerance | dict + string fallback | only `0x_mission_graph_sync.py:118-124` accepts both | PARTIAL |

**Layer 2 status: SEMANTICALLY WORKING (string bearings preserved end-to-end), STRUCTURALLY DEGENERATE (no FROM→TO vectoring).**

The N/S/E/W concept is consistently used:
- North (N) → unblock prerequisites — preserved in `0x_mission_graph.py:212-222`, `1x_mission_crystallizer.py:121`, `compass_auto_infer.py`
- South (S) → conclude/proceed — preserved in `1x_mission_crystallizer.py:121-123` (south_edge_ratio threshold 0.60)
- East (E) → parallel/sister work — preserved in `0x_mission_graph_sync.py:159`, `8x_compass_native_bridge.py`
- West (W) → return to genesis — preserved in `8x_convergence_detector.py:140` (compass_w sibling synthesis), `8x_mission_completion_synthesizer.py:282`

**However**, the canonical model says agents must navigate as: "I'm at faerie2-shipping, came from X, going south to docs-consolidation." Without `from_label` and `to_label`, agents only know **where they are** (`investigation_label`) and **what direction they go** (`compass_edge`), not **where they came from** or **what mission they enter next**.

### Layer 3: CHARTER — bounded scope frame

| Property | Canonical Spec | Code Reality | Verdict |
|----------|----------------|--------------|---------|
| Storage | `genesis_manifest.json` + `crystallization_metrics.json` | NEITHER EXISTS | MISSING |
| `charter_id` | mandatory ID | 0 occurrences | MISSING |
| `investigation_labels` (charter scope) | array of in-scope labels | 0 occurrences | MISSING |
| `scope` | string description | 0 occurrences | MISSING |
| `deadline` | date | 0 occurrences (charter context) | MISSING |
| `map_boundary` | reachability rule | 0 occurrences | MISSING |
| `deliverables` | array of must-complete tasks | 0 occurrences | MISSING |
| `success_criteria` | manifest_count_min, avg_quality_score_min, blocking_issues | 0 occurrences | MISSING |
| `--charter` flag in `0x_spawn.py` | docstring example line 188-200 | NOT IMPLEMENTED in argparse | MISSING |

**Layer 3 status: DOCUMENTATION-ONLY.** The charter concept exists in canonical model and CLAUDE.md but is unenforced anywhere in code.

Without the charter:
- Spawn invocations are not bounded by deadline or deliverable list
- `0x_spawn.py` does not call any `load_current_charter()` function
- `discovery focuses on missions WITHIN charter boundary` (per doc 44 example) is not implementable
- "Charter completion / new charter" lifecycle is conceptual only

## Per-Field Terminology Cross-Reference

### Producers (write the field)

| Field | Producer Scripts | Field Type |
|-------|------------------|------------|
| `investigation_label` | `0x_spawn.py`, `0x_spawn_template.py`, `0x_bundle_factory.py`, `0x_mission_graph.py`, all manifest writers via spawn template | string |
| `compass_edge` | `0x_spawn.py`, `0x_mission_graph.py`, `0x_bundle_factory.py`, `compass_auto_infer.py`, `8x_compass_native_bridge.py`, `8x_mission_completion_synthesizer.py` | string (N/S/E/W) |
| `next_task_queued` | spawn template injects guidance; agents emit per docstring | string (task_id) |
| `next_mission_node` | NONE | (would be dict) |
| `from_label` | NONE | (would be string) |
| `to_label` | NONE | (would be string) |
| `charter_id` | NONE | (would be string) |
| `task_id` | universal | string |
| `dashboard_line` | universal (≤80 chars) | string |
| `quality_score` | spawn template guidance, eval harness | float 0–1 |
| `belief_index` | spawn template guidance, eval harness | float 0–1 |

### Consumers (read the field)

| Field | Consumer Scripts |
|-------|------------------|
| `investigation_label` | `0x_mission_trail_builder.py`, `1x_mission_crystallizer.py`, `0x_mission_graph_sync.py`, `0x_compass_query.py`, `9x_droplet_live_sync.py`, `9x_daily_dashboard_generator.py` |
| `compass_edge` | `0x_compass_query.py`, `1x_mission_crystallizer.py`, `0x_mission_graph_sync.py`, `0x_mission_graph.py`, `8x_manifest_first_guardian.py` (validates presence) |
| `next_task_queued` | `0x_compass_query.py`, `0x_mission_graph.py` (open-edges query), `1x_mission_crystallizer.py`, `9x_daily_dashboard_generator.py` |
| `next_mission_node` | `9x_daily_dashboard_generator.py` only (read as fallback) |

## Recommended Vocabulary Ladder

For internal consistency without breaking running code, use this ladder:

| Tier | Term | Use Case |
|------|------|----------|
| Layer-name (capitalized) | **MAP** | Documentation, ARCHITECTURE.md, when speaking about emergent territory as a concept |
| Concrete artifact | `forensics/mission-trails/` | Filesystem reference |
| Cluster ID | `investigation_label` | Field name in manifests, bundles, queries |
| Synonym | mission-graph | Allowed in prose; equivalent to MAP |
| Layer-name (capitalized) | **COMPASS** | Documentation, when speaking about navigation |
| Concrete field | `compass_edge` | Field name in manifests |
| Concrete bearings | N / S / E / W | string values |
| Vector (target schema) | `next_mission_node` (dict) | New target schema; produce alongside `next_task_queued` for transition |
| Layer-name (capitalized) | **CHARTER** | Documentation, when speaking about scope frame |
| Concrete artifact (target) | `genesis_manifest.json` | Filesystem path; not yet implemented |
| Field (target) | `charter_id`, `charter_boundary` | New fields to add to spawn |

## Consistency Findings

**STRONG (no action needed):**
- `investigation_label` field name and semantics
- `compass_edge` letter codes (N/S/E/W)
- `dashboard_line` length cap (≤80) and use as primary signal
- `task_id` placement in filenames (per Forensic Naming Standard)
- COC hash chain (`prev_entry_hash` + `entry_hash` schema)

**WEAK (terminology drift, low-risk to fix):**
- `next_task_queued` (legacy "queue" nomenclature contradicts Tesla-valve flow model migration)
- "queue" prefixes on hooks that operate on `mission-graph` semantics (e.g., `8x_queue_autorun.py` — but this is now superseded by `8x_mission_autorun.py` correctly)

**MISSING (high impact, requires baseline measurement before fix per FUNDAMENTAL GOVERNANCE RULE):**
- Charter layer artifacts (`genesis_manifest.json`, `crystallization_metrics.json` named explicitly)
- `next_mission_node` dict schema with `from_label` / `to_label`
- `--charter` flag implementation in `0x_spawn.py`
