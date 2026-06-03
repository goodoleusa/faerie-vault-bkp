---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: type-ontology-doctrine
status: synthesis-log
canon_candidate: true
---

# Type ontology — parent/N vs child/S types in the swarmy graph

User stated (verbatim):

> "can we distinguish....? is there a way to connect ontology between
>  types for example charters are parent/N types and manifests are
>  child/S types because manifests can only come into being after
>  commissioned by a charter."

This is THE typed-graph clarification that completes the
living-graph-vs-bounded-charters doctrine
(`08-living-graph-vs-bounded-charters.md`).

## The two type families

Swarmy's forensic graph has artifacts in TWO families with a
parent→child commission relationship:

### PARENT TYPES (commissioning — bearing N affinity)

These COMMISSION downstream work. They can exist without prior
artifacts. They set the bounds:

| Type | What it commissions | Lives at |
|---|---|---|
| **Charter** | Manifests, sub-charters, missions | `forensics/charters/active/` |
| **Mission** (declared) | Manifests, sub-missions | `forensics/mission-graph.json` |
| **Skill** (`.agents/skills/{name}/SKILL.md`) | Agent behaviors via triggers | `.agents/skills/` |
| **Microagent** (legacy `.openhands/microagents/`) | Agent context | (migrating) |

A charter is sealed = no NEW manifests can be commissioned against
it (downstream manifests in flight finish; new ones need a new
charter, OR a charter merge).

Parent types carry **bearing affinity N** (unblock / commission).

### CHILD TYPES (commissioned — bearing S affinity)

These can ONLY exist AFTER a parent commissioned them. They cite
their parent + ladder to acceptance:

| Type | Commissioned by | Lives at |
|---|---|---|
| **Manifest** | Charter (via mission field) | `forensics/ephemeral/{date}/{task_id}/manifest.json` |
| **Artifact** | Manifest (cited in `artifacts_written[]`) | `forensics/ephemeral/.../`, promoted to `forensics/artifacts/{date}/` |
| **Bundle** | Charter / dispatcher (provides input context) | `forensics/bundles/{date}/` |
| **COC entry** | Manifest (signed body of) | `forensics/coc-entries/{date}/`, `forensics/coc.jsonl` |
| **Narrative** (vault daily) | Manifest OR charter (cited as `related_*`) | `$SWARMY_VAULT_DAILY/{date}/NN-slug.md` |
| **Memorial** (creature) | Creature lifecycle (the parent creature) | `forensics/creatures/memorial/` |

Child types carry **bearing affinity S** (ship / conclude).

## The commission rule (enforced)

**A child cannot exist before its parent.** Concretely:

1. Manifests MUST carry a `mission` field. That `mission` must point
   at a real declared mission OR exist in an active charter's
   cluster_prefix neighborhood. (Today: the `5x_hook-forensics-index.py`
   indexes mission fields; the validator could reject manifests with
   orphan missions — that's an open enhancement.)
2. Artifacts cited in a manifest's `artifacts_written[]` MUST be
   real files. The promotion pipeline verifies this.
3. COC entries chain to PRIOR entries (`parent_hashes[]`) — the
   parent is structural; you can't append without a chain root.
4. Vault narratives SHOULD carry `related_mission` + optionally
   `related_charter`. Without these, they're orphan synthesis (still
   valid — the user's pure reflection — but the dashboards can't
   route them).

## The bidirectional cite (what makes it a graph)

The parent→child commissioning is **one direction**. But the graph
needs BIDIRECTIONAL references:

- **Child cites parent** (mandatory): `manifest.mission`,
  `narrative.related_mission`, `artifact.manifest_id` (citing).
- **Parent reflects child** (accreting): `charter.manifests_received[]`,
  `mission.tasks[]`, `creature.manifests_authored[]`.

These accrete automatically via the promotion hooks. The 5x forensics
indexer reads each new manifest and updates the parent's reflection
fields. So parents grow over time as their children land — that's
the "tightening" in the living-graph doctrine.

## Type lifecycle (the unified view)

```
        N-bearing (commission)              S-bearing (conclude)
        ─────────────────────              ──────────────────────

   ┌── CHARTER ───────────────┐     ┌── MANIFEST ──────────┐
   │ cluster_prefix=3         │     │ mission              │
   │ acceptance_ritual        │ ──▶ │ artifacts_written[]  │ ──▶ ARTIFACT
   │ phase_*_deliverables[]   │     │ completion_choice    │       │
   │ manifests_received[]  ◀──┼─────┤ signer + signed_by   │       │
   └──────────────────────────┘     └──────────────────────┘       │
        ▲                                  │                       │
        │                                  │                       ▼
        │ (promotion via _charter_lib)      ▼                  COC ENTRY
        │                              VAULT NARRATIVE         (hash-chained)
        │                              (related_mission)
        │
   MISSION (declared in mission-graph.json) — parallel parent layer
```

The diagram reads: **CHARTER commissions → MANIFEST executes →
ARTIFACT lands → COC entry signs.** The arrow back from MANIFEST to
CHARTER (the `manifests_received[]` accretion) is the tightening
loop.

## Why this matters for the cold-start question

User asked: "the creation of any new charter at coldstart shld just
do this [convergence detection], right? so it never gets disjointed."

YES — that's now enforced as of this commit. The hook
`9x_hook-charter-discipline.py` now does a convergence check on
every active charter write:

- Reads the new charter's `cluster_prefix`
- Compares with every sister active charter
- ≥2 terms shared with a sister → WARN (soft nudge, not block)
- Surfaces the convergent sister name + shared terms
- Suggests merge or `breadcrumbs.same` linking

This is the cold-start gate. It prevents disjointed parent types
(charters) from accumulating without acknowledgment. The downstream
manifests stay aligned because they cite the parent — once parents
are clean, children inherit cleanliness.

## The third dimension: TIME (E/W bearings)

Beyond parent/N and child/S, the type ontology also flows in time:

- **E (parallel) artifacts** — multiple manifests in the same
  charter at the same DAG level. Sister artifacts. They cite the
  same parent.
- **W (backtrack) artifacts** — when a child manifest discovers
  the parent charter's assumptions are wrong. Triggers a re-baseline
  on the parent. The CHILD effectively commissions a parent-level
  revision (rare; structural debt signal).

So the full ontology:
- **N parents** commission **S children**
- **E parallels** within a parent
- **W backtracks** from child to parent-revision

Four bearings, two type families, one graph.

## What's auto-enforced today (the integrity story)

| Rule | Enforcement layer | Hook |
|---|---|---|
| Charter must have valid COC chain | structural | `9x_hook-charter-discipline.py` |
| Charter convergence warned at write | reactive | same hook (NEW today) |
| Manifest must be signed | reactive | `9x_hook-manifest-sign-enforce.py` |
| Active charter cap ≤15 (soft) | reactive | `9x_hook-charter-cap.py` |
| Signature verification on every write | reactive | `9x_hook-signature-verify.py` |
| Missing parent (orphan child) detection | (NOT YET) | open enhancement |

The "missing parent" enforcement is the next piece. A manifest with
a `mission` field that doesn't resolve to a declared mission OR an
active charter neighborhood should warn. Today it just lands silently
as orphan. Adding this would close the parent→child commission rule
at the write layer.

## Single-line summary

**N-bearing parent types (charters, missions, skills) commission
S-bearing child types (manifests, artifacts, COC entries, narratives).
Bidirectional cite makes it a graph. Convergence detection at
charter write prevents disjointed parents. Children stay aligned
because they always cite an extant parent.**

---

*Folds into the type-ontology dimension of
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md`. Companion to
`08-living-graph-vs-bounded-charters.md` (the dynamics layer). Both
are canon-candidates for Part 4 of the canonical doc.*
