---
title: Shape Registry — Authoring + Integration Guide
date: 2026-05-22
related_doc: docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md
status: canonical
---

# Shape Registry (`_meta/shapes.json`) — The Measurement Substrate

A **shape** is a recognizable, countable, mechanically-detectable pattern
of work. The registry is the canonical home for every shape the swarm
measures — RAP cuts cite shapes for baseline + new_state; evolution +
mutation assessment classify verdicts against a shape's `target_direction`;
membench probes ARE shapes at the quality layer.

Where shapes COUNT, formulas COMPUTE — together they form the complete
measurement layer (see `inspiration/2026-05-22/14-formulas-static-and-dynamic.md`).

## Why this exists

Without an explicit registry, shapes are implicit — hand-written in
ad-hoc scripts, named inconsistently, never composed. Implicit shapes
make:

- Mutation verdicts subjective ("the code feels better")
- Cross-repo propagation impossible (no shared shape ID)
- Membench drift invisible (probes regress silently)
- RAP cuts uncomparable (different baselines per run)

The registry fixes all four. Every shape has a stable ID, a detector
script, a target direction, and a history of measurements.

## Shape schema

```json
{
  "shape_id": "{domain}.{subject}.{mode}",
  "cluster_prefix": ["term1", "term2", "term3"],
  "description": "What this shape recognizes; load-bearing one-liner.",
  "target_direction": "decreasing | increasing | bounded | stable",
  "detector_script": "scripts/<name>.py  OR  scripts/<name>.py::function_name",
  "membench_probe": true | false,
  "applicable_repos": ["faerie2", "..."],
  "current_count": int | null,
  "baseline_ts": "ISO8601",
  "noise_threshold": int  (delta < this = neutral verdict),
  "history": [
    {"ts": "...", "count": N, "mutation": "<slug or null>", "verdict": "..."}
  ]
}
```

### Field semantics

- **shape_id** — stable canonical name. Once published, NEVER renamed
  (would break the mutation history). Use `domain.subject.mode` as a
  w3w-style address.
- **target_direction**:
  - `decreasing` — count should trend toward 0 (e.g. unsigned manifests)
  - `increasing` — count should grow (e.g. tests added, missions claimed)
  - `bounded` — count should stay below a cap (e.g. active charters ≤ 15)
  - `stable` — count should not drift more than `noise_threshold`
    (regression-detection mode)
- **detector_script** — relative path from repo root. May include a
  function suffix `::fn_name`; in that case the audit script calls that
  named function. Otherwise the script must accept `--count` flag and
  emit a single integer to stdout.
- **noise_threshold** — `abs(delta) < threshold` → verdict=`neutral`.
  Above threshold + target_direction_aligned → `beneficial`. Above +
  violated → `harmful`. Detector failed → `uncertain`.

## Authoring a new shape (the recipe)

1. **Recognize the pattern.** A shape is something you can scan + count
   mechanically. If you find yourself eyeballing JSON files looking for a
   recurring problem, that's a shape candidate.
2. **Write the detector.** Add a function to `scripts/shapes/audit-shapes.py`
   (preferred — keeps detectors co-located) OR a stand-alone script.
   Returns int. No side effects (idempotent + fast — runs in the audit
   cron).
3. **Pick the shape_id.** Form `domain.subject.mode`. Examples:
   - `mcp.tools.granular` (domain=mcp, subject=tools, mode=granular)
   - `manifest.signed_by.missing` (domain=manifest, subject=signed_by, mode=missing)
4. **Declare it in `_meta/shapes.json`.** Append entry. Capture
   `baseline_ts` + initial `current_count` if known (use `null` if
   first-run; audit cron will populate).
5. **Wire RAP cuts.** When you run a fast-evo cut targeting this shape,
   cite it in `_evolution_log[].shape` so verdicts are mechanical.

## Integration with the four-layer pattern

| Layer | How shapes show up |
|---|---|
| **Structural** | Schema (`_meta/shapes.json`) — the registry IS the structure. |
| **Cognitive** | `.agents/skills/shape-registry/SKILL.md` — agents read the registry to find the right shape to target. |
| **Reactive** | Hooks (`9x_hook-manifest-shape-tracking.py`) update shape counts on manifest write. |
| **Recovery** | Nightly cron (`scripts/shapes/audit-shapes.py`) walks every shape's detector, appends history, surfaces regressions. |

## Cross-repo propagation

When `applicable_repos[]` lists multiple repos, the shape is portable
— the same detector logic + target_direction applies. A mission shaped
around the shape can ship the protocol once and propagate the
acceptance criteria to every repo carrying the shape.

This is the **killer property** doctrine 11 (`missions-as-emergent-cross-repo-shape.md`) describes: the shape comes first; the mission
emerges from shape recognition; the charter bounds the propagation;
the SAME mission ships across N repos because they share the shape.

## How shapes link to formulas

A shape returns a COUNT (raw int). A formula returns a SCORE (often
[0, 1]). Formulas compose shapes:

```
formula:mcp_consolidation_index =
    1 - (shape:mcp.tools.granular.current_count / baseline)

formula:signing_coverage =
    1 - (shape:manifest.signed_by.missing / total_manifests)

formula:swarm_vitality =
    weighted_sum(
      0.3 × signing_coverage,
      0.2 × charter_progression_rate,
      0.2 × mission_emergence_rate,
      0.2 × consolidation_index,
      0.1 × cross_repo_alignment
    )
```

The formula registry (`scripts/_formulas.py`) is the canonical home for
composition logic. Each formula MAY cite a shape ID as its primary
input.

## See also

- `docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` Part 4 — the canon
  doc this registry serves
- `inspiration/2026-05-22/13-shape-rap-evolution-membench.md` — the
  doctrine that produced this registry
- `inspiration/2026-05-22/14-formulas-static-and-dynamic.md` — formula
  composition layer
- `.agents/skills/shape-registry/SKILL.md` — author-time discipline
- `.openhands/hooks/9x_hook-manifest-shape-tracking.py` — reactive layer
- `scripts/shapes/audit-shapes.py` — recovery layer (nightly cron)
