---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: negative-space-graph-analysis
status: synthesis-log
canon_candidate: true
---

# Negative space analysis — where things AREN'T, where things DIED

User stated (verbatim):

> "similar to negative space analysis on the graph, where are things
>  not? where did things die? shld we devote hive resources or let it
>  fizzle?"

This is the natural follow-up to doctrine 21 (distress signals).
Once we have a measurement substrate (shapes), a failure recovery
mechanism (distress bundles + scouts), and a forensic ledger
(charter accretion), the next analytical step is:

**Read the mission graph for what's MISSING, not just what's there.**

Where are the gaps? Which regions have no manifests? Which charters
opened and quietly died? Which missions emerged once and never came
back? And — most importantly — **should the hive devote resources
to fill any of those gaps, or recognize that some negative space is
legitimately empty?**

## Three classes of negative space

### 1. Uncharted gaps — work being done with no charter

Manifests exist; their `mission` field has a cluster_prefix; no
active charter covers that w3w address. The work is happening but
has no bounding region.

How to find them: walk recent manifests, group by `mission`, filter
to those whose cluster_prefix has no ≥2-term overlap with any
active charter's cluster_prefix.

Today: the genesis script's mission-clustering surface (the
`MISSION-CLUSTERS.md` sidecar — doctrine 11) already does this. It
surfaces uncharted clusters as "candidate for new charter."

Negative-space reading: a cluster of 5+ manifests around a w3w
address with no charter signals either:
- Real emergent work that deserves bounding (resource: open a charter)
- Drift that should be reabsorbed into an adjacent charter (resource: claim)
- One-off work that's done and doesn't need a charter (resource: nothing)

### 2. Dead-end zones — work that started then stopped

A mission first appeared N days ago, accumulated K manifests, then
silence. No new manifests; no distress bundle; no seal. Just
fizzled out.

How to find them: walk mission-graph nodes, compute
`(last_manifest_ts - first_manifest_ts)` + days since last_manifest.
Sort by silence duration descending.

Three readings of a dead-end zone:

| Pattern | Interpretation | Resource decision |
|---|---|---|
| 2-3 manifests, fizzled within a day | exploration didn't pan out | LET FIZZLE |
| 8-12 manifests, fizzled after a week | real attempt, no closure | INVESTIGATE — write a synthesis pass; either revive or formally retire |
| 1 manifest with distress kind, no scout response | failure never picked up | URGENT — assign a scout |
| Many manifests, multiple agents, no completion_choice=seal | scope blown, no exit ritual | RECONCILE — likely needs explicit close + retroactive charter |

### 3. Unmapped territory — bearings with no manifests

The mission graph DAG has nodes (missions) connected by N/S/E/W
bearings. Where the bearings point but no manifests landed there,
the territory is mapped (we know it should exist) but unmade.

How to find them: walk every manifest's `discovered_work[]`, count
how many proposed-next-tasks were never claimed (no downstream
manifest cites them as predecessor). Each unclaimed
discovered_work entry is a node on the DAG that was named but
never reached.

Negative-space reading: a high ratio of "discovered but unclaimed"
work to "discovered and claimed" work signals the swarm is
proposing more than it can absorb. Either the spawn rate is too
low for the discovery rate, or the discovered tasks are themselves
low-quality (vague, off-mission, premature).

## The resource-allocation question

User's question — *"shld we devote hive resources or let it
fizzle?"* — turns on three signals about each negative space:

### Signal 1 — Connection density

A dead-end zone connected to active charters by ≥2 shared
cluster_prefix terms is HIGH-VALUE NEGATIVE SPACE — completing it
would feed an active charter. Worth devoting resources.

A dead-end zone with no connections to active work is ORPHAN
NEGATIVE SPACE — completing it produces a standalone artifact with
no downstream consumers. Let fizzle UNLESS the artifact has
intrinsic value (e.g. a one-shot publication).

### Signal 2 — Distress evidence

A dead-end zone with a distress bundle that no scout picked up is
ALWAYS worth resources. The signal was honest; the swarm just
failed to route. Critical to address.

A dead-end zone with no distress signal but observed silence might
be a SILENT GIVE-UP — agents abandoned the work without flagging
distress. This is a discipline failure (per doctrine 21, agents
should flag distress, not just stop). Investigation + reputation
penalty for the abandoning agent.

### Signal 3 — Shape trajectory

If completing the negative space would push a TRACKED SHAPE toward
its target direction, resources are clearly worth it (mechanical
verdict: beneficial). If completing it has no shape impact, the
case for resources weakens.

Example: a dead-end mission about consolidating MCP tools is HIGH
PRIORITY if `mcp.tools.granular` is still above target. The same
mission would be LOW PRIORITY if `mcp.tools.granular` has already
hit target.

## The negative-space audit (proposed)

Script: `scripts/shapes/audit-negative-space.py`. Outputs:

```markdown
# Negative-Space Audit — {date}

## Uncharted gaps (manifests with no covering charter)
{cluster, manifest_count, oldest, newest, charter_overlap_score, recommendation}

## Dead-end zones (missions that fizzled)
{cluster, last_activity_days_ago, manifest_count, has_distress, resource_recommendation}

## Unmapped territory (high unclaimed:claimed ratio)
{discovering_manifest, unclaimed_count, claimed_count, ratio, recommendation}

## Resource allocation matrix
| zone | shape_lift | connection_density | distress_present | recommendation |
| ...  | ...       | ...                | ...              | DEVOTE / LET FIZZLE / INVESTIGATE |
```

This becomes a new shape: `mission-graph.negative-space.coverage`
— measures fraction of mission-graph regions with EXPLICIT
disposition (either covered by active work, or formally
acknowledged as "let fizzle"). Target: increasing toward 1.0.
Negative space without a disposition is ambiguous; explicit
disposition (even "let fizzle") is preferable.

## The four-layer enforcement

### Structural

`forensics/schemas/shape/negative-space-zone.schema.json` — defines
a zone entry: {cluster_prefix, kind: uncharted|dead-end|unmapped,
first_seen, last_activity, manifest_ids[], distress_bundle_ids[],
disposition: investigate|devote-resources|let-fizzle|retroactive-seal,
disposition_rationale, disposition_signer}.

### Cognitive

Extend `mission-emergence-w3w/SKILL.md` (don't sprawl) with a new
section: *Negative space — read what's missing*. Triggers: "where
did this die", "what gaps", "what's not happening".

### Reactive

`.openhands/hooks/9x_hook-distress-route.py` — when a distress
bundle is written, surface it loudly (high-priority log entry,
record into a `distress.open.count` shape). The hook doesn't
block; it prevents distress signals from getting silently buried.

### Recovery

`scripts/shapes/audit-negative-space.py` — nightly cron + on-demand
CLI. Emits the negative-space audit report + records the
`mission-graph.negative-space.coverage` shape.

## Why this matters operationally

The hive currently rewards positive signal: shipping, completing,
synthesizing. Failures and gaps are invisible.

Negative-space analysis flips that. A hive that watches its gaps
as carefully as its outputs:

- Catches drift faster (silence is a measurable signal)
- Routes scouts to abandoned work (the failures we learn most from)
- Makes explicit "let fizzle" decisions instead of implicit
  abandonment (forensic clarity)
- Surfaces systemic issues (5 missions on the same shape all
  fizzled → that shape's territory has a structural blocker)

It's the same pattern that made the shape registry valuable:
making the implicit measurable. The shape registry made
"problems" measurable. Negative-space analysis makes
"non-problems-that-might-be-problems" measurable.

## Single-line summary

**Read the mission graph for what's NOT there. Three classes of
negative space: uncharted gaps (work without a charter), dead-end
zones (missions that fizzled), unmapped territory (bearings that
proposed work nobody claimed). For each, the swarm decides:
devote resources, let fizzle, or investigate. The decision becomes
an explicit disposition signed into the negative-space audit;
implicit abandonment is no longer acceptable — every gap gets a
verdict.**

---

*Closes a 15-doctrine arc for 2026-05-22 (08-22). Implementation
needs: new schema + audit script + cron + skill extension (NOT
new skill — fold into mission-emergence-w3w per 'dont sprawl'
discipline). Should follow distress-signals (doctrine 21) since
the distress signal IS the most actionable kind of negative space.*
