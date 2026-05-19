---
type: faerie-internal
subtype: overview
canonical_source: /mnt/d/0local/gitrepos/faerie2/scripts/spawn.py
canonical_sha256: ddaf8744071979f342c81cb95aa91ec9b1e95f135f607ec9b50fb86d4840414c
last_synced: '2026-05-19T15:24:06+00:00'
N: '[Faerie System Internals Home](../00-Home.md)'
E: []
tags: ['internal', 'spawn-bundle', 'overview', '#path/transparency']
---

# Spawn Bundles — What & How

A **spawn bundle** is the pre-spawn context envelope handed to each subagent. It is written to `forensics/bundles/{date}/{ts}_bundle_{task_id}_{archetype}_{seq}.json` BEFORE the agent is invoked, so the chain-of-custody starts the instant the queen lays the egg.

## Bundle structure

| Field | Meaning |
|-------|---------|
| `task_id` | 8-char deterministic ID; appears in every downstream filename |
| `mission` | Canonical routing signal — **mandatory**. Spawn refuses without it. |
| `goal` | One-line semantic intent |
| `done_looks_like` | Concrete success criterion |
| `priority` | LOW / MED / HIGH / CRITICAL |
| `agent_type` | Archetype key (navigator, maker, bridge, deep-diver, …) |
| `compass_edge` | N / S / E / W bearing |
| `constraints` | Free-text guardrails |
| `investigation_label` | Legacy compat alias (prefer `mission`) |
| `status` | charted → in-flight → returned |

## Read-bundle assembly (from `scripts/spawn.py` `read_bundle()`)

When an agent is invoked the bundle is rendered by concatenating:

1. Global `HONEY.md` (crystallized prefs)
2. Project `.claude/HONEY.md` (repo-specific context)
3. `NECTAR.md` tail-50 (recent HIGH/CRITICAL findings)
4. `0x_spawn_bundle_template.md` (self-describing context format)
5. Mission + investigation-label header + frontier-reading instructions

## Archetypes (the four bearings)

| Archetype | Bearing | Job |
|-----------|---------|-----|
| **NAVIGATOR** | N | Unblock predecessors |
| **MAKER** | S | Ship deliverables |
| **BRIDGE** | E | Sync parallel sister tracks |
| **DEEP-DIVER** | W | Re-seat baseline assumptions |

Canonical definitions in [`../Templates/agents/`](../Templates/agents/).

## Spawn flow

```mermaid
flowchart LR
  C[Charter / Mission] --> B[bundle.py write]
  B --> F[forensics/bundles/{date}/]
  F --> S[spawn.py]
  S --> A{archetype?}
  A -->|N| NAV[NAVIGATOR]
  A -->|S| MAK[MAKER]
  A -->|E| BR[BRIDGE]
  A -->|W| DD[DEEP-DIVER]
  NAV & MAK & BR & DD --> M[forensics/manifests/{date}/]
```

## MCP entry points

- `faerie_bundle` — any agent can write a bundle (free tier)
- `faerie_spawn` — Main only; uses `0a_spawn-pressure.py` + `0b_spawn-executor.py` (pro tier)
- `faerie_internals_sync` — regenerate this internals tree (admin)

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/scripts/spawn.py`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
