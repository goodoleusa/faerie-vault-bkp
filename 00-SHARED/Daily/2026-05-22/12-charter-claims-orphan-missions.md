---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: charter-mission-claim-dynamics
status: synthesis-log
canon_candidate: true
---

# Charters claim orphan missions — the dynamic relationship

User said (verbatim, the final clarification on charter↔mission
dynamics):

> "and the relationship between charters and missions evolves,
>  because missions can arise or be added to the frontier of the
>  mission graph and they can then be 'claimed' by a charter that
>  fits it"
>
> "that way the charter isnt just creeping and expanding, its
>  following its own rules but it can also subsume an orphaned
>  mission that naturally emerged"

This is the dynamic-claim mechanism — the last piece needed to make
the charter↔mission relationship LIVING rather than static.

## The mechanism in one paragraph

A mission can emerge in the frontier (an agent recognizes a shape,
declares a w3w cluster_prefix) without a charter. It sits as an
**orphan mission** — visible in the mission graph, contributing to
its evolution, but uncommissioned. A charter, following its OWN
rules (the 3-question scope fence), can choose to **claim** that
orphan mission — subsume it under the charter's bounding box if
the orphan's cluster_prefix overlap legitimately fits. The charter
doesn't creep — it absorbs aligned work that arose naturally.

## Two failure modes this prevents

### Failure 1: forced commission → creep
If charters had to be authored BEFORE work could begin, and work
discovered new shapes, the charter had to be edited to add them.
This is the creep pattern — charters expanding past their original
scope.

### Failure 2: orphan work → invisibility
If only-charter-bound work counted, emergent shapes would be
invisible. Agents discovering a recurring problem couldn't surface
it as a mission until a human authored the charter.

The claim mechanism gives both: orphans CAN exist (no charter
needed to recognize a shape); charters CAN absorb (when scope
genuinely matches); neither side has to creep.

## The claim rule (precise + enforceable)

A charter `C` may CLAIM an orphan mission `M` iff:

1. **Cluster_prefix overlap is structural** —
   `|C.cluster_prefix ∩ M.cluster_prefix| >= 2`
   (≥2 of the 3 w3w terms shared)

2. **Mission shape serves charter goal** —
   Apply the 3-question scope fence to M as if M were a candidate
   deliverable:
   a. Does M's shape serve C's summary line?
   b. Does M share any cluster_prefix term with C? (already satisfied by rule 1)
   c. Will completing M move a declared KPI in C?
   If ANY answer is "no" → claim is invalid; M stays orphan or
   gets its OWN charter.

3. **Charter is in a claimable phase** —
   Phase must be `phase_X active` (not sealed; not draft). Sealed
   charters don't claim; they're closed.

4. **Active charter cap honored** —
   The claim doesn't COUNT toward the cap (it's absorbed work, not
   a new charter). But the charter's `manifests_received[]` grows,
   so the cap stays at the charter-count level.

If all four hold, the charter writes a `claimed_missions[]` entry
referencing `M.cluster_prefix` + `M.first_seen_ts`. The mission's
mission-graph node is annotated `claimed_by: C.charter_id`.

## How claim differs from MERGE

Both reduce graph fragmentation but are operationally different:

| Operation | What it does | When |
|---|---|---|
| **CLAIM** (charter ← orphan mission) | Charter subsumes a mission with no charter yet. Mission stays addressable; gains a bounding box. | Mission EMERGED FIRST, charter exists |
| **MERGE** (charter ← charter) | Two charters with high cluster_prefix overlap consolidate. One sealed → the other absorbs its deliverables. | Both charters PRE-EXISTED, scope drifted to convergence |

Claim is forward-emergence-friendly (asynchronous). Merge is
charter-deduplication.

## Where claim shows up in the data

### In the charter file

```json
{
  "charter_id": "agents-as-bonded-creatures",
  "cluster_prefix": ["creatures", "agency", "bonds"],
  "claimed_missions": [
    {
      "cluster_prefix": ["creatures", "naming", "memorial"],
      "first_seen_ts": "2026-05-22T08:14:00Z",
      "first_seen_manifest": "ephemeral/.../creatures-phase1-foundation-01_maker.json",
      "claimed_ts": "2026-05-22T10:22:00Z",
      "claim_rationale": "naming + memorial work emerged inside phase 1 deliverables; cluster_prefix shares 'creatures' term and serves the 'bonded' acceptance ritual",
      "claimed_by_signer": "goodoleusa"
    }
  ]
}
```

### In the mission graph

```json
{
  "missions": {
    "creatures.naming.memorial": {
      "first_seen": "2026-05-22T08:14:00Z",
      "manifest_count": 3,
      "claimed_by": "agents-as-bonded-creatures",
      "claimed_ts": "2026-05-22T10:22:00Z"
    }
  }
}
```

## Genesis script integration

`scripts/0x_charter_genesis.py` already does mission clustering (the
`_cluster_missions_from_manifests` function). Adding **claim
detection**:

For each uncharted mission cluster from the genesis pass:
- Compute cluster_prefix overlap with every active charter
- If max overlap is ≥2 terms → propose CLAIM (surface in
  MISSION-CLUSTERS.md as "claim candidate")
- If max overlap is ≤1 term → surface as "new charter candidate"
- Operator/agent reviews + confirms

Then `--apply` mode could (with caution) execute:
- New charter creation for uncharted clusters with low overlap
- Claim writes for clusters with high overlap (charter's
  `claimed_missions[]` gets the entry + signed COC chain)

## How this prevents "missions can keep arising forever" anxiety

Without the claim mechanism, every emergent shape would seem to
demand a new charter — explosion. With it:

- Many emergent shapes land inside existing charters' clusters
  (claim absorbs them)
- Only genuinely-orthogonal shapes get new charters
- The active-charter-count stays bounded by the cap

The MISSION graph keeps growing (good — it's the breath, per
`08-living-graph-vs-bounded-charters.md`). The CHARTER count stays
bounded (good — they're heartbeats, not constantly multiplying).

## The closure pattern

When a charter SEALS, its `claimed_missions[]` decision becomes
historical. Future manifests still tagged with that mission's
cluster_prefix become NEW orphans — they don't auto-route to the
sealed charter. The shape can be:

a) **Re-claimed** by an adjacent active charter
b) **Charter-promoted** if the shape recurs strongly (new charter
   authored)
c) **Left orphan** if the shape is one-off

This keeps the lifecycle clean: sealed = sealed (no zombie claims).

## Single-line summary

**Charters follow their own rules but CAN claim emergent orphan
missions that fit. The cluster_prefix overlap (≥2 terms) + the
3-question fence are the claim test. Mission graph grows freely;
charter count stays bounded; neither creeps.**

---

*Final piece of the dynamics doctrine (08+09+10+11+12). Together:
- 08: dynamics (graph flows, charters bound)
- 09: types + commission rule (parent N / child S)
- 10: naming schema (w3w mission, kebab charter, lineage in filename)
- 11: emergence (missions arise from shape, not assignment)
- 12: claim (charters absorb orphan missions that fit)

These 5 documents together describe the COMPLETE mission-charter
lifecycle. Should be crystallized into Part 4 of
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` in a focused
synthesis pass.*
