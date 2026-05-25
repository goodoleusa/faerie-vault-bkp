---
type: moc
title: Shapes — Map of Content
pseudosystem_folder: Shapes
canonical_repo_path: "_meta/shapes.json"
tags: [moc, shape, measurement, pseudosystem]
updated: "2026-05-25"
total_shapes: 27
schema_version: "1.0"
---

# Shapes — Map of Content

> Vault pseudosystem mirror of `_meta/shapes.json` in the repo.
> A shape is a recognizable, countable, mechanically-detectable pattern of work.
> RAP / evolution / mutation assessment / membench all ground measurements here.
> **Canonical source:** `_meta/shapes.json` — vault notes are navigable dossiers.

---

## Shape Grammar

`{domain}.{subject}.{mode}` — e.g. `mcp.tools.granular`, `manifest.signed_by.missing`

Target directions: **decreasing** (reduce this count) | **increasing** (grow this count) | **bounded** (keep within range) | **stable**

---

## Decreasing Shapes (20) — want fewer of these

| Shape | Current | Membench | Description |
|-------|---------|----------|-------------|
| [[mcp.tools.granular]] | 75 | yes | MCP tools that should be verb-dispatcher-merged. Each instan |
| [[manifest.signed_by.missing]] | None | yes | Manifests written without signer + signed_by — the basic age |
| [[charter.cluster_prefix.violations]] | None |  | Active charters whose cluster_prefix is not exactly 3 atomic |
| [[charter.active.over_cap]] | None |  | Excess active charters beyond max_active_charters (15). Meas |
| [[charter.stale.no_progress]] | None | yes | Active charters open >7 days with no new manifests_received[ |
| [[manifest.orphan_mission]] | 0 | yes | Recent (rolling 24h) manifests whose mission field doesn't r |
| [[vault.frontmatter.missing]] | None |  | Vault narrative .md files lacking a YAML frontmatter block ( |
| [[cluster_prefix.length_violation]] | None |  | Any artifact carrying a cluster_prefix array whose length is |
| [[naming.schema.v1_legacy]] | None |  | Manifest filenames still using v1 schema ({ts}__{task_id}_{a |
| [[manifest.discovered_work.shape_missing]] | None |  | Entries in manifest._evolution_log[] that target a shape but |
| [[hook.coverage.gap]] | 0 | yes | PostSpawn / PreSpawn lifecycle boundaries where a hook SHOUL |
| [[crystallization.discipline.violations]] | None |  | Daily count of manifests violating spray->tighten->crystalli |
| [[manifest.rolling_brainstorm.missing]] | None | yes | Manifests written by overhauled agent types (post-2026-05-24 |
| [[manifest.completion_choice.missing]] | None | yes | Manifests from overhauled agent types (post-2026-05-24) that |
| [[manifest.cognitive_blindspot.missing]] | None |  | Manifests from overhauled specialist agent types (post-2026- |
| [[spawn_brief.prescribes_completion_choice]] | 50 | yes | Spawn briefs (Agent() prompts written by main, dispatcher, o |
| [[jsx.closure_leak_to_sibling_component]] | 0 | yes | A top-level React function component references an identifie |
| [[llm.tokens.uninstrumented_call]] | None | yes | Count of LLM completion calls in production that did NOT pro |
| [[patent.evidence.unanchored_session]] | 29 |  | Count of sessions/conversations that do NOT have a correspon |
| [[coc.schema.versions_in_play]] | 1 | yes | Number of distinct COC schemas being actively walked. v1 (le |

## Increasing Shapes (5) — want more of these

| Shape | Current | Membench | Description |
|-------|---------|----------|-------------|
| [[sanitization.audit.coverage]] | 7 | yes | Count of distinct (direction, source-class) tuples covered b |
| [[crystallization.discipline.clean_rate]] | None | yes | Daily fraction of manifests passing crystallization discipli |
| [[platform_bootstrap.cross_session_lessons]] | 9 | yes | Distinct doctrinal lessons crystallized from session manifes |
| [[multi_agent.realtime_collab.blackboard]] | 1 | yes | Parallel agents coordinate via append-only JSONL blackboard  |
| [[pair_session.viewer_token_class]] | 0 | yes | Viewer tokens minted and shared for a pair session. Each tok |

## Bounded Shapes (2) — keep within range

| Shape | Current | Membench | Description |
|-------|---------|----------|-------------|
| [[llm.cost.per_session_usd]] | None | yes | Rolling 7-day windowed median USD cost per Claude Code sessi |
| [[openhands.agent.tool_set_completeness]] | 5 | yes | Count of Tool(name=X) entries in sdk_chat.py's agent_kwargs  |

---

## Dataview Query

```dataview
TABLE current_count, target_direction, membench_probe
FROM "Shapes"
WHERE type = "shape"
SORT target_direction ASC, current_count DESC
```

---

*Canonical registry: `_meta/shapes.json` (schema v1.0). Shape detector scripts are referenced in each note.*
