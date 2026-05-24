# 45 — Semantic Mission Emergence (Canonical)

**Status:** canonical · **Locked:** 2026-05-21 · **Charter:**
`2026-05-21_semantic-emergence-mission-graph`

> Charters are addresses. The neighbor graph is the map. Emergence is what
> appears when you stand back from the map and let the topic clusters tell
> you what the swarm is actually working on.

This doc is the load-bearing reference for the semantic-emergence layer of
the mission graph. If a future agent reads only one doc to understand why
charters carry an exactly-three-term `cluster_prefix` and how that
addressing turns into adjacency, this should be that doc.

---

## 1. The w3w semantic-addressing principle

A charter declares a mission. Missions need addresses — a stable handle by
which other charters, agents, and humans can refer to them. The swarmy
charter schema borrows the **what-three-words** convention: a charter's
semantic location in the topic space is a list of exactly three terms,
stored in `cluster_prefix`.

Three terms are enough to address every coherent mission a hive is likely
to run. They are short enough that humans can hold the full address in
working memory. They are concrete enough that overlap with another
charter's address has unambiguous meaning — two charters that share even
one term are unambiguously in the same neighborhood; two that share all
three are essentially the same mission and need a merge conversation.

The w3w analogy is not metaphor; it is mechanism. What.three.words tiles
the planet so that any 3m × 3m square has a unique three-word address; the
overlap pattern between addresses encodes spatial adjacency. Swarmy tiles
the topic space the same way: any coherent mission lives at a unique
three-term address; the overlap pattern between two charters' addresses
encodes topical adjacency.

This is the **addressing layer**. We have it. Schema-locked since
2026-05-19.

---

## 2. Why `cluster_prefix=3`, not 2 or 4

The 3-rule is load-bearing. It is not arbitrary. Each of 2 and 4 fails in
a different way:

- **Two-term addresses (cluster_prefix=2)** are under-specified. They
  collide too readily. `[gui, components]` plausibly fits a dozen
  charters; the address loses its discriminating power. The overlap
  signal goes from "this is meaningful adjacency" to "everything is
  adjacent to everything"; emergence collapses into a single giant
  cluster.

- **Four-term addresses (cluster_prefix=4)** are over-specified. Two
  charters that should be neighbors miss each other because a fourth
  refining term broke the overlap. The address gains specificity but
  loses the adjacency property. Emergence vanishes the other way:
  every charter becomes its own island.

- **Three-term addresses** sit at the sweet spot. They are specific
  enough that an overlap of even one term means real shared territory,
  and general enough that the natural mission clusters surface as
  connected components on the adjacency graph.

The 3-rule is enforced structurally by the schema validator, cognitively
by the `charter-discipline` skill, and reactively by the
`9x_hook-charter-discipline.py` write hook. The
`cluster_prefix_violators` helper in `_charter_term_index_lib.py` surfaces
any drift retroactively.

One legacy violator currently exists: `swarmy-rename-and-cleanup` carries
six terms. It was authored before the 3-rule was enforced; it is queued
for repair on the next charter-schema-compliance sweep.

---

## 3. Term hygiene — synonym deprecation, dead-term detection, canonical vocabulary

Address quality depends on vocabulary quality. If two charters use `gui`
and `ui` for the same concept, they will fail to be adjacent even though
they should be. The hygiene pass — `0c_charter_term_index.py --hygiene` —
surfaces three classes of vocabulary problem:

1. **Dead terms** (used fewer than 2x). A term that appears in only a
   single charter is either a unique specifier (legitimate) or a synonym
   for a more-used term (drift). The dead-terms list is the spot-the-drift
   tool.

2. **Hardcoded synonym candidates.** A small table in
   `_charter_term_index_lib._HARDCODED_SYNONYMS` knows about known
   alias pairs (`gui`↔`ui`, `docs`↔`documentation`, `workflow`↔`workflows`,
   `consolidate`↔`consolidation`, etc.). When a charter uses a non-canonical
   alias, the hygiene pass flags it.

3. **Stem collisions.** A naive stemmer reduces terms to roots; collisions
   surface candidates the synonym table doesn't yet know about (e.g.
   `signing` and `signoff` both stem to `sign`).

The hygiene pass **proposes**; it does not act. Humans approve merges.
This is intentional: the cost of a wrong auto-merge is higher than the
cost of a manual review.

The first run on the live 22-charter set surfaced 58 dead terms and 3
merge proposals — including a `gui→ui` canonicalization candidate that
would, if accepted, immediately reveal new adjacency between the GUI
charters and any future UI-focused mission.

---

## 4. Adjacency-as-emergence

The address gives you a point. Overlap gives you an edge. The set of
edges across all charter pairs gives you the **adjacency graph**, and
that graph is where mission emergence becomes visible.

**Overlap weights:**
- **1 shared term** — these charters touch the same topic at one slot
  of their address. Weak but real adjacency; the most common case.
- **2 shared terms** — strong adjacency. These charters likely
  collaborate on neighboring deliverables and should be aware of each
  other's frontier.
- **3 shared terms** — full overlap. These charters are functionally
  the same mission. They should either merge or one should narrow its
  third term to differentiate.

The adjacency graph for the current charter set has 23 nodes and 10
edges at `min_score=1`. Connected components of this graph are the
**emerging topic clusters**: the missions the swarm is collectively
weighting most.

Emergence here is in the literal complex-systems sense. No central
authority declared "GUI is a topic area"; the hive declared a GUI
charter, then a GUI-polish charter, and the overlap edge between them
made the GUI cluster visible. The cluster emerged from local addressing
decisions.

---

## 5. Three layers — addressing, adjacency, emergence

The full stack:

```
┌──────────────────────────────────────────────────────────────┐
│  EMERGENCE       — connected components, hub terms, dead-    │
│  (visible)         term flags. Synthesis: what is the swarm  │
│                    actually weighting?                       │
├──────────────────────────────────────────────────────────────┤
│  ADJACENCY       — overlap-weighted edges between charter    │
│  (computed)        pairs. Surface: which charters touch?     │
├──────────────────────────────────────────────────────────────┤
│  ADDRESSING      — cluster_prefix=3 per charter. Atom: where │
│  (declared)        does this mission sit in topic space?     │
└──────────────────────────────────────────────────────────────┘
```

Addressing has been in place since 2026-05-19 (schema lock).
Adjacency and emergence shipped together with the
`semantic-emergence-mission-graph` charter (this wave).

The crucial property: **all three layers are derivative from the same
substrate**. Address decisions ripple all the way up. Edit a charter's
`cluster_prefix`, rerun `0c_charter_term_index.py`, and the adjacency
graph + emergent clusters update deterministically. There is no
hand-maintained list of "topic areas"; the topic areas are emergent from
the addressing decisions.

---

## 6. Mission discovery via overlap — agent spawn injection pattern

The neighbor graph is most useful at **author time** — when a new
charter is being declared, or when an agent picks up a charter to work.

The intended pattern (queued for MCP integration in phase_2, once the
verifier-in-flight unblocks `server.py` edits):

1. Agent is dispatched on charter `X` (or proposes to author a new
   charter with cluster_prefix `[a, b, c]`).
2. Spawn-time hook runs
   `python3 scripts/0d_charter_neighbors.py X --json` (or, for a proposed
   new address, queries the index directly via
   `_charter_term_index_lib.find_neighbors`).
3. The 1-hop neighbor list is injected into the agent's bundle as a
   "topic neighborhood" hint.
4. Agent reads neighbors *before* authoring; can choose to (a) explicitly
   coordinate with a neighbor, (b) refine its own address to avoid
   overlap, or (c) reuse a neighbor's terms for tighter clustering.

Until that MCP integration lands, the neighbor lookup is invoked
manually by humans and any agent that knows to call the CLI. The
microagent skill at `.agents/skills/semantic-emergence/SKILL.md` fires
on relevant triggers so the pattern is at least cognitively reachable.

---

## 7. The fractal property — canvas of charters IS the same canvas as a brainstorm

The `CharterNeighborGraph` component is intentionally aligned with
`BrainstormCanvas`. Both use the same honey/cream palette, the same
SVG-first rendering approach, the same node-and-edge metaphor. This is
not coincidence; it is the **fractal vibe-coding pattern** identified
in the `2026-05-21_canvas-as-headwater` charter.

A card on a brainstorm canvas is a small charter (a captured intent).
A charter in the neighbor graph is a large card (an executed intent).
A connection in a brainstorm canvas is a soft adjacency (an arrow the
human drew). An edge in the neighbor graph is a hard adjacency (an
overlap the engine derived).

The two components could, in a future wave, share rendering primitives.
For now they are sibling components with shared design language. The
fractal property is: **zoom in or out at any scope, you get the same
node-graph substrate**.

This is also why the deliverable is a *graph*, not a *list*. A ranked
list would do the same job at less code, but a ranked list cannot show
the fractal. The graph CAN — and that's the load-bearing UX claim.

---

## 8. Anti-patterns

- **Inventing new terms when a synonym exists.** If `ui` is already in
  use by two charters, do not introduce `gui` in a new charter; reuse
  `ui`. The hygiene pass will catch you, but catching is post-hoc; the
  author has the easier fix.

- **cluster_prefix of length 2.** Under-specified address. Schema
  validator should reject; if you find one, repair the charter.

- **cluster_prefix of length 4 or more.** Over-specified. The fourth
  term is doing the work that should be done by the charter's `summary`
  or `deliverables_address_prefix`. Move it there.

- **Using charter-internal jargon as cluster_prefix terms.** A term
  that no other charter could plausibly use is a dead term by
  construction. Prefer broadly-applicable topic words.

- **Editing a charter's `cluster_prefix` after launch without rerunning
  the index.** The downstream adjacency graph goes stale silently. The
  index builder is idempotent; rerun it after every charter mutation.

- **Treating the graph as a TODO board.** It is not. It is a topic
  map. A charter on the graph without recent activity is not "stale";
  it is at rest. Mission cadence lives in synthesis logs and KPI
  status fields, not in graph topology.

---

## 9. Worked example — the current 22 (now 23) charter set

After the first full index build, the live state was:

- **23 charters indexed** (22 prior + this new one).
- **64 unique terms** across all `cluster_prefix` slots.
- **10 adjacency edges** at `min_score=1`.
- **Top hubs:** `rename` (3 charters), `vault` (3), `canonical` (2),
  `components` (2), `gui` (2).
- **One schema violator:** `swarmy-rename-and-cleanup` with 6 terms.

The `rename`-hub is the most legible emerging cluster — three charters
(`faerie-to-swarmy-rename`, `swarmy-rename-and-cleanup`,
`tool-namespace-redesign`) all touch the rename surface. They likely
want to coordinate on canonical-name choice; until the index was built
they had no surface to discover each other through.

The `vault`-hub is similarly emergent: `swarmy-production-runway`,
`swarmy-vault-template`, `vault-utils-bundling` all touch the vault
substrate. The neighbor graph makes this triplet visible at a glance,
where reading the charter list serially would never quite surface it.

`2026-05-21_canvas-as-headwater` is currently isolated — its address
`[canvas, fractal, platform-flow]` shares no terms with any other
charter. This is a signal: either the canvas vision is genuinely
greenfield (likely), or the charter is using terms that should
canonicalize toward an existing hub. Worth a human review.

---

## 10. Future — phase_2 and beyond

Sequenced work that this charter intentionally does **not** ship:

- **Real-time neighbor injection on agent spawn.** Requires MCP server
  changes; queued for after the verifier-in-flight (a6f0cb59) unblocks
  `server.py`. Will likely land as a new tool
  `swarmy_charter_neighbors(charter_id, depth)` plus a spawn-time hook
  that calls it and injects results into the bundle.

- **Brainstorm-card → charter promotion with neighbor preview.** When a
  card on `BrainstormCanvas` is promoted to a charter, surface the
  proposed `cluster_prefix`'s neighbors before committing. Lets the
  human refine the address before declaring.

- **Periodic term-merge ratchet.** Once a quarter (or after every N
  charter creations), the hygiene pass runs and proposes merges; humans
  approve a batch; charters get rewritten through a vetted migration
  script.

- **Hop-2 routing.** Currently the neighbor injection is 1-hop. Hop-2
  ("neighbors of my neighbors") may surface adjacent mission clusters
  even without direct term overlap. Worth experimenting with once we
  have 50+ charters and the graph has more interesting connectivity.

- **Temporal layer.** Charters carry a `created` date; adjacency edges
  could be annotated with "both active in same week" for time-aware
  emergence. Future, not now.

---

## Acceptance ritual (this doc)

This document passes its own orientation test if, on a cold read three
months from now, a new contributor can answer:

1. **Where were we?** Addressing layer shipped; adjacency layer missing.
2. **Where are we?** All three layers present; index + graph + viz + CLI
   + doctrine + skill all alive.
3. **Where are we headed?** MCP integration for spawn-time neighbor
   injection; canvas-card-to-charter promotion with neighbor preview.

If those answers are reachable in 60 seconds of reading, the doc has
done its job.

---

## Cross-references

- Charter: `forensics/charters/active/2026-05-21_semantic-emergence-mission-graph.json`
- Engine: `scripts/_charter_term_index_lib.py`
- Index builder: `scripts/0c_charter_term_index.py`
- Neighbors CLI: `scripts/0d_charter_neighbors.py`
- Visualization: `deploy/chat-mvp/src/components/CharterNeighborGraph.jsx`
- Skill: `.agents/skills/semantic-emergence/SKILL.md`
- Live data: `forensics/charter-term-index.json`,
  `forensics/charter-adjacency-graph.json`
- Sibling charter (substrate): `2026-05-21_canvas-as-headwater`
- Schema source-of-truth: `forensics/charters/SCHEMA.md`
