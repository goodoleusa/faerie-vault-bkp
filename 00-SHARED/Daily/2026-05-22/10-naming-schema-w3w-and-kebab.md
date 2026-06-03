---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: filename-schema-w3w
status: synthesis-log
canon_candidate: true
---

# Naming schema — w3w for missions, kebab-toast for charters, lineage in filenames

User asked (verbatim):

> "is there a way to use what.three.words for missions and, what,
>  manifests?"
> "and charters get kebab-toast?"
> "how can we show the association between charter and manifest
>  naturally in the filename schema itself"

This proposal answers all three. It's a forward-only schema change
(old artifacts keep their existing names; new ones use the new
form).

## The naming distinction

| Type | Format | Example | Why this form |
|---|---|---|---|
| **Charter** | kebab-toast (single compound) | `agents-as-bonded-creatures` | Charter is a NAMED THING — a discrete bounded box. One memorable compound reads well to humans + sorts cleanly. |
| **Mission** (cluster_prefix-as-address) | w3w dotted (3 atomic terms) | `creatures.agency.bonds` | Mission is an ADDRESS in topic space. Three atomic terms preserve the adjacency property: two missions sharing `creatures` are neighbors, sharing 2 terms = same neighborhood, sharing 3 = same mission. |
| **Manifest** | timestamp + mission-w3w + charter-slug + task + agent | `20260522T120000Z__creatures.agency.bonds__agents-as-bonded-creatures__phase1-foundation_maker.json` | Lineage at a glance — see the parent charter AND the topic address without opening the file. |

## The proposed manifest filename

### Current schema

```
{YYYYMMDD}T{HHMMSS}Z__{task_id}_{agent_type}_{mission}_{session_id8}.json
```

`mission` is freely-formed; nothing enforces w3w form. Charter is
nowhere in the filename — you have to open the manifest to know
which bounding box it serves.

### Proposed schema

```
{YYYYMMDD}T{HHMMSS}Z__{mission-w3w}__{charter-slug}__{task_id}_{agent}.json
```

Where:
- `{mission-w3w}` — dot-separated 3 atomic terms: `term1.term2.term3`
  (matches `cluster_prefix=3` exactly; dots not dashes to disambiguate
  from kebab-toast slugs)
- `{charter-slug}` — the kebab-toast `charter_id` from the bounding
  charter (e.g., `agents-as-bonded-creatures`). If no charter (rare;
  freelance work), use `_no-charter_`.
- `{task_id}` — keep as-is (a stable identifier per task)
- `{agent}` — agent_type (maker / navigator / bridge / deep-diver
  / general-purpose / etc.)

### Concrete example

OLD:
```
20260522T120000Z__creatures-phase1-foundation-01_maker_creatures-phase1-foundation_phase1-fnd.json
```

NEW:
```
20260522T120000Z__creatures.agency.bonds__agents-as-bonded-creatures__phase1-foundation_maker.json
```

You can read THE WHOLE STORY off the filename:
- When: `2026-05-22 at 12:00 UTC`
- Topic neighborhood: `creatures × agency × bonds` (mission)
- Bounding box: `agents-as-bonded-creatures` charter
- Task: `phase1-foundation`
- By: `maker` archetype

## Why dots in the mission term, dashes in the charter

This is the load-bearing micro-decision. **Different separators
discriminate the two types unambiguously** in any tool that parses
filenames (jq, awk, frontier grep, etc.):

- `term1.term2.term3` → mission (split on `.`)
- `compound-multi-word-name` → charter (split on `-`)

If both used dashes, you couldn't tell where the mission ended and
the charter began. Dots vs dashes give a clean parser-friendly
boundary.

Side benefit: in conversations + URLs + Obsidian links, the
mission's dotted form is readable as a sentence
("creatures.agency.bonds" reads as a topic address; "agents-as-
bonded-creatures" reads as a project name).

## How this enforces the parent-child commission rule

(Companion to `09-type-ontology-parent-child.md`.)

A manifest filename now LITERALLY contains its parent charter's
slug. Three immediate wins:

1. **Frontier scan is grep-friendly.** "Find all manifests under
   charter X": `ls forensics/manifests/{date}/__*__X__*` — no
   JSON parsing needed.

2. **Orphan detection is mechanical.** A manifest with `_no-charter_`
   in its filename is explicitly orphan. The
   `9x_hook-manifest-sign-enforce.py` could extend to also warn on
   `_no-charter_` placement (soft nudge: "did you forget to declare
   the bounding charter?").

3. **Convergence is visually obvious.** Two missions claiming the
   same w3w address `creatures.agency.bonds` will sort adjacent in
   the filesystem listing. Convergence happens passively just by
   `ls`.

## How this interacts with the existing schema

Backwards compatibility:
- The CURRENT `0x_manifest_writer.py` produces the old form.
  Migration: introduce the new form as opt-in; once verified,
  flip the default; deprecation note for legacy parsers.
- Existing manifests on disk stay valid. The new filename pattern
  is forward-only.
- The COC chain doesn't care about filenames — it hashes content.
  Filename rename is forensically free (no chain invalidation).

Migration path:
1. Add `--schema-version=2` flag to `0x_manifest_writer.py`
2. Default agents to v2 for new manifests
3. Update the manifest-filename validator
   (`9x_hook-manifest-filename-enforce.py`) to accept BOTH v1 and v2
4. After 30 days: deprecation warning on v1 writes
5. After 60 days: hard-flip to v2-only (with `--legacy-v1` opt-out)

## Open questions / next-pass items

1. **What if a manifest serves multiple charters?** (rare — usually
   bridge work). Use the charter the agent was MOST-recently active
   on; or use a special `_multi-charter_` slug + a separate
   `charter_ids[]` field inside the manifest body.

2. **What if the mission has fewer than 3 terms?** (legacy data,
   pre-w3w-discipline). Pad with `_pad_` or refuse to write. The
   discipline says EXACTLY 3 — refuse is correct, but back-compat
   needs the padding-fallback.

3. **Charter slug max length?** The kebab-toast can grow ugly
   (`agents-as-bonded-creatures-phase-2-modding-community` is 51
   chars). Suggest hard cap at 40 chars for the slug component; if
   longer, hash-truncate with a stable hash suffix.

4. **Mission w3w vocabulary aliases?** `_meta/swarmy.config.json`
   already has `cluster_prefix_aliases`. Apply at write time so
   "gui.components.layout" → canonical "ui.components.layout"
   automatically.

## Single-line summary

**w3w (dotted, 3 atomic terms) for missions = topic address.
Kebab-toast (compound) for charters = named bounded box. The
manifest filename concatenates both: `{ts}__{w3w}__{charter}__{task_id}_{agent}.json`
— and you can read the entire lineage off the filename without
opening the file.**

---

*Proposes a schema change to `0x_manifest_writer.py` + the
`9x_hook-manifest-filename-enforce.py` validator. Should be folded
into the canonical manifest-naming section of
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md`. Companion docs:
`08-living-graph-vs-bounded-charters.md` (dynamics),
`09-type-ontology-parent-child.md` (commission rule).*
