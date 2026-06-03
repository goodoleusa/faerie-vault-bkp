---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: mission-graph-doctrine
status: synthesis-log
canon_candidate: true
---

# Living mission graph vs. discrete bounded charters — the canon

User stated (verbatim):

> "the mission graph frontier and mission semantics shld be ever
>  evolving, growing, chaining, diverging and converging, self
>  braiding and tightening"

> "Charters are concrete bounding boxes that exist to put a discrete
>  boundary on that evolving graph so we can accomplish stuff"

This is THE doctrinal clarification on how the two structures relate.
Capturing here as canon-candidate for the next pass at
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md`.

## The two structures

### The mission graph — LIVING

The mission graph is a fluid, ever-evolving substrate. Its dynamics:

- **Growing** — new tasks land, new manifests append, new
  cluster_prefix terms enter the vocabulary
- **Chaining** — task A discovers task B which discovers task C; the
  N/S/E/W bearings encode this chain
- **Diverging** — one mission spawns multiple sub-missions when
  scope cracks open
- **Converging** — sister missions discover they share enough
  cluster_prefix terms to merge into one
- **Self-braiding** — when two strands of work realize they're
  actually one cable; the graph adds cross-links and tightens
- **Tightening** — sparse exploration → dense execution as the
  surface fills in

The graph never "completes." It just keeps evolving. Trying to seal
the WHOLE graph is a category error.

### Charters — DISCRETE BOUNDING BOXES

Charters are how we accomplish things despite the flux. Each charter
draws a discrete boundary around a region of the graph and says:
"this region, these terms (cluster_prefix=3), these deliverables —
THIS we will finish."

Without charters, the living graph is endless. Every task discovers
two more; every cluster grows. Nothing closes.

Charters close. They have:
- A `cluster_prefix` (3 terms) that defines the boundary
- An `acceptance_ritual` that defines when "done" means done
- Phase deliverables that ladder toward acceptance
- A `phase_1_sealed_ts` field that gets set when the charter actually completes

When a charter seals, that region of the living graph crystallizes.
Future work on those terms must charter a NEW boundary (with shared
terms — the lineage shows in the cluster_prefix overlap).

## The interaction (the load-bearing part)

The two structures relate like flow vs. snapshot:

- The graph FLOWS — agents append manifests, discover work, propose
  edges, the cluster_prefix vocabulary drifts
- Charters SNAPSHOT — they grab a moment of the graph, draw a box
  around it, and commit to closing inside that box

A healthy hive is constantly opening charters (carving discrete
work-units from the flux) and closing them (returning the flux to
its evolving state with one more crystallized region).

If you only have the graph: you have endless ideation, nothing ships.
If you only have charters: you have a TODO list, no emergence.

Both layers, always. The graph is the breath; charters are the
heartbeats.

## What this means concretely for swarmy

### The `00-HOME` page (vault entry)

Should surface both:
- Mission graph stats (count, growth rate, overlap density, recent
  braids/divergences) — the breath
- Active charter list (boxes currently drawn, days open, phase) —
  the heartbeats

The vault dashboards we've been building (PUBLISHING-DASHBOARD,
CybertemplatePUBLISH, etc.) are charters-in-disguise — they're
discrete boundaries on the workflow flux so publication actually
happens.

### The charter-cap hook

(In flight via agent a23ae83f — `9x_hook-charter-cap.py`.) The cap
isn't about preventing too many ideas — the GRAPH can be huge. The
cap is about preventing too many open BOXES — because each box
requires a closing-ritual and unclosed boxes accumulate cognitive
debt.

15 active charters is a soft warning. The hook surfaces "consider
sealing N before opening N+1" — not because the work doesn't matter
but because the boxes need to close to make the system feel alive.

### The charter genesis pass

(Also in flight via a23ae83f — `scripts/0x_charter_genesis.py`.)
This is the CRYSTALLIZATION operation on charters specifically:
walk active charters, identify which can SEAL (the boundary's work
is done), which can MERGE (two boxes drawn around overlapping
regions can be one box), which are TRULY ORPHAN.

The graph itself doesn't get crystallized — it keeps flowing.
Charters do.

### Mission graph dynamics layer (queued — not yet built)

The user's language ("self-braiding and tightening") suggests a
visualization + measurement layer we don't have yet:

- **Braid detector** — when two cluster_prefix sets overlap by ≥2
  terms over rolling 24h window, surface as a braid candidate
- **Divergence tracker** — when one mission's task count starts
  cleanly bifurcating into two distinct cluster_prefix subsets,
  surface as a divergence candidate
- **Tightening metric** — count of cross-links per node; growing
  metric = graph getting denser/tighter
- **Time-lapse viz** — snapshot the graph daily; render the
  evolution as an animation in the Recursive Canvas

These are the next-quarter mission-graph-dynamics items. The
charter-genesis script is the FIRST piece (the sealing/merge half).

## Single-line summary

**Mission graph = flow. Charters = boxes drawn on the flow.
Both, always. Don't try to box the whole flow.**

---

*Capturing today (2026-05-22) at user's articulation. Next step:
fold the relevant parts into
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` as Part 4 (the
existing 1-3 cover the addressing layer; this is the dynamics layer).
Also surface the mission-graph-dynamics queue items as N-bearing
discovered_work for the next round.*
