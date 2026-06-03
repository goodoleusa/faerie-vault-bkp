---
name: navigate
description: |
  Navigation cluster: how to traverse the mission graph. Folds compass
  (N/S/E/W bearings + team patterns), mission (w3w DAG, manifest contract,
  braid, query), and survey (probe/sweep rhythm, sandwich-measure discipline).
  Use when the conversation mentions bearing, compass, north/south/east/west,
  mission graph, frontier, w3w, forage, probe, sweep, or survey.
type: knowledge
always_load: true
triggers:
  - bearing
  - compass
  - north
  - south
  - east
  - west
  - N-edge
  - S-edge
  - E-edge
  - W-edge
  - mission
  - missions
  - mission graph
  - mission node
  - frontier
  - w3w
  - what three words
  - forage
  - survey
  - sound
  - probe
  - sweep
  - sandwich measure
  - measure before and after
  - discovered_work
---

# navigate — how to traverse the mission graph

This skill is the navigation cluster: bearing grammar, mission-graph DAG,
and the survey rhythm that governs how you measure before and after each move.

Three sub-systems braided here:

- **compass** — N/S/E/W bearing grammar and team patterns
- **mission** — w3w DAG: emergence, braid, query, refused edges
- **survey** — probe/sweep rhythm: measure → cut → measure

<!-- crystallize:braid-begin -->
# CRYSTALLIZED 2026-06-03

> 3 doc(s) braided in; sources archived to `_archive-2026-06-03/`. Net-new + conflicts preserved below.
<!-- crystallize:braid-end -->


<!-- crystallize:braid-begin -->
# CRYSTALLIZED 2026-06-03

> 3 doc(s) braided in; sources archived to `_archive-2026-06-03/`. Net-new + conflicts preserved below.

<!-- braid: preamble from SKILL.md -->
---
name: compass
description: >-
  Compass-bearing routing (N/S/E/W) for the swarmy mission graph plus canonical
  team patterns by mission frontier. Use when the conversation mentions bearing,
  compass, north, south, east, west, N-edge, S-edge, E-edge, W-edge, or when
  deciding which worker_role team (UNBLOCK / SHIP / PARALLEL / BASELINE /
  multi-bearing) to spawn for a mission.
type: knowledge
triggers:
  - bearing
  - compass
  - north
  - south
  - east
  - west
  - N-edge
  - S-edge
  - E-edge
  - W-edge
---

<!-- Glossary alignment 2026-06-02 (canonical: citations/glossary/02-CANONICAL-GLOSSARY.md):
     Authority: the unified Reckon glossary SUPERSEDES the legacy swarmy-ui UI-layer glossary.
     LOCKED term-set (tiers: flotilla > fleet > voyage > charter > mission > crew):
     - capped        -> sealed (eligible+ready for promotion) / promoted (landed in canonical forensics/)
     - queued        -> on-deck (an AGENT's claim on the spawn roster) / next/ (where queued CHARTERS live)
     - spawn-queue   -> spawn-roster (the on-deck agent dir _spawn-roster/)
     - agent-bundle  -> waypoint (tactical handoff to chart/next/)
     - charter-draft -> flight-plan (new-voyage proposal, operator-cleared)
     - sound         -> survey (the deep/wide rhythm: probe 🔬 / sweep 🌊 / both 🌀)
     - swarm         -> fleet (user footprint) ; swarm agents -> crew (agents on one mission)
     Completion ritual: 2 columns — lifecycle_judgment (col A) + free_choice (col B), 19 kinds.
     RENAME RULE: migrate LIVE surfaces cleanly; NEVER rename archives / forensic record.
     Preserved: completion_choice.kind enum members in JSON code blocks,
                faerie2-origin: comments, historical-event quotes.
-->


<!-- braid: h:compass-bearing-grammar-team-patterns from SKILL.md -->
# Compass — Bearing Grammar & Team Patterns

Bearings = where a task **concludes** in the mission DAG, not where it started.
Use the bearing to pick the team; the team's worker_role mix matches the frontier shape.


<!-- braid: h:bearings-one-line-each from SKILL.md -->
## Bearings (one line each)

- **N — UNBLOCK** — reverse-dependency work that frees something upstream
- **S — SHIP** — forward-dependency work that closes a deliverable
- **E — PARALLEL** — sister work at the same DAG level (no blocker)
- **W — BASELINE** — backtrack to re-seat broken assumptions


<!-- braid: h:when-each-fires-decision-matrix from SKILL.md -->
## When each fires (decision matrix)

| Frontier signal | Bearing | Pattern name |
|---|---|---|
| Blocked tasks dominate (N-edges) | **N** | UNBLOCK |
| Clear path to deliverable, no blockers | **S** | SHIP |
| 2+ independent parallel tracks | **E** | PARALLEL |
| New discovery invalidates an assumption | **W** | BASELINE |
| All four bearings present | **multi** | COGNITIVE DIVERSITY |


<!-- braid: h:team-patterns-default-rosters from SKILL.md -->
## Team patterns (default rosters)

```
NORTH-BOUND UNBLOCK      → NAVIGATOR + DEEP-DIVER + MAKER       (conf 0.88)
SOUTH-BOUND SHIP         → MAKER + BRIDGE + NAVIGATOR           (conf 0.92)
EAST-BOUND PARALLEL      → BRIDGE + MAKER + NAVIGATOR           (conf 0.85)
WEST-BOUND BASELINE      → DEEP-DIVER + NAVIGATOR               (conf 0.88)
MULTI-BEARING (4-way)    → NAVIGATOR + MAKER + BRIDGE + DEEP-DIVER, parallel, same wave  (conf 0.87)
```

**Default is multi-bearing.** Single-facet teams only when work is strictly linear.

**Stigmergic teams from bearing trios:** A natural stigmergic team forms
when 3 worker_roles share a bearing trio (e.g. NAVIGATOR + MAKER + DEEP_DIVER
on an UNBLOCK mission). Each writes into `forensics/ephemeral/active/{agent_id}/`
with the team label baked into the canonical
v2 filename — peers find each other via one `ls *__{team-label}__*.json`.
Full coordination doctrine: `.agents/skills/survey/SKILL.md` (sound skill) §
"Stigmergic team coordination".


<!-- braid: h:worker-role-primary-agent-mapping-locked-2026-05-03 from SKILL.md -->
## Worker_role → primary agent mapping (locked 2026-05-03)

| Worker_role | Primary agent | Role |
|---|---|---|
| NAVIGATOR | research-analyst | Frontier scan, mission discovery |
| MAKER | python-pro | Fast artifact + integration delivery |
| BRIDGE | knowledge-synthesizer | Cross-domain synthesis |
| DEEP-DIVER | security-auditor | Validation, assumption testing |


<!-- braid: h:worked-examples from SKILL.md -->
## Worked examples

**Example 1 — North (UNBLOCK):**
Frontier shows `auth-token-rotate` blocking 3 downstream tasks.
→ Spawn `NAVIGATOR` (chart N-path), `DEEP-DIVER` (validate token contract), `MAKER` (prototype rotation). Bearing = N.

**Example 2 — South (SHIP):**
Feature complete on branch, staging slot open, no blockers.
→ Spawn `MAKER` (push deploy), `BRIDGE` (verify cross-domain consumers), `NAVIGATOR` (steer S-edges to close). Bearing = S.

**Example 3 — East (PARALLEL):**
Doc + API contract + tests all independent, can run same DAG level.
→ Spawn `BRIDGE` (find commonalities), 2× `MAKER` (parallel tracks), `NAVIGATOR` (keep E-edges aligned). Bearing = E.

**Example 4 — West (BASELINE):**
Mid-mission, design assumption (e.g. cache TTL) broken by new measurement.
→ Pause new S-edges. Spawn `DEEP-DIVER` (re-run baseline tests), `NAVIGATOR` (map dependency chain back to HQ). Bearing = W.

**Example 5 — Multi (4-way):**
New mission infrastructure: needs discovery + build + cross-wire + validation.
→ Spawn all four worker_roles **in parallel, same wave**. Each reads its own bearing edges; convergence happens via shared manifest trail.


<!-- braid: h:anti-patterns from SKILL.md -->
## Anti-patterns

- Spawning 4 agents same worker_role (e.g. 4× python-pro) → single-facet team, low emergence
- Choosing bearing from intuition instead of frontier scan → drift
- Skipping W when an assumption broke → silent corruption downstream
- Locking on S when N-blockers still exist → ships into a wall


<!-- braid: h:how-to-record-bearing-on-a-manifest from SKILL.md -->
## How to record bearing on a manifest

```json
{ "next_mission_node": { "bearing": "N", "to_label": "<task_id>" } }
```

Or for `discovered_work[]`:

```json
{ "task_id": "<id>", "mission": "<mission>", "bearing": "N|S|E|W",
  "from_label": "<self.task_id>", "to_label": "<target>",
  "rationale": "<≤80 chars: why this is unblocked / next>" }
```


<!-- braid: h:handoff-events-and-bearing from SKILL.md -->
## HANDOFF events and bearing

When agents use the stigmergic-collab blackboard (`.agents/skills/stigmergic-collab/SKILL.md`),
HANDOFF events carry a compass bearing. The most common case is **E (parallel
sister work)** — one agent spots an opportunity for its peer at the same DAG
level. N/S/W are also valid when the handoff unblocks upstream work, closes a
downstream deliverable, or triggers a baseline re-check. The bearing in a
HANDOFF line follows the same grammar as `manifest.next_mission_node.bearing`.

See also: `spawn` skill (delegation protocol), `piston` skill (when to burn hot).

<!-- braid: preamble from SKILL.md -->
---
name: mission
description: |
  The mission graph — how missions are born, named (w3w), how they
  braid, and how to find work in the frontier. The canonical home for
  everything graph-side. Every agent needs this — missions are how the
  swarm coordinates without messages.
type: knowledge
triggers:
  - mission
  - missions
  - mission graph
  - mission node
  - frontier
  - frontier query
  - find related work
  - prior manifests
  - sister work
  - predecessor work
  - mission graph query
  - recent manifests
  - who shipped this
  - what's blocked
  - mission lookup
  - w3w
  - what-three-words
  - what three words
  - cluster_prefix
  - mission address
  - mission name
  - mission emerge
  - mission emergence
  - braid
  - braiding
  - mission braid
  - mission neighborhood
  - semantic linkage
  - mission graph audit
  - self-healing graph
  - charter aggregation
  - charter phase
  - discovered_work
---

<!-- Glossary alignment 2026-06-02 (canonical: citations/glossary/02-CANONICAL-GLOSSARY.md):
     Authority: the unified Reckon glossary SUPERSEDES the legacy swarmy-ui UI-layer glossary.
     LOCKED term-set (tiers: flotilla > fleet > voyage > charter > mission > crew):
     - capped        -> sealed (eligible+ready for promotion) / promoted (landed in canonical forensics/)
     - queued        -> on-deck (an AGENT's claim on the spawn roster) / next/ (where queued CHARTERS live)
     - spawn-queue   -> spawn-roster (the on-deck agent dir _spawn-roster/)
     - agent-bundle  -> waypoint (tactical handoff to chart/next/)
     - charter-draft -> flight-plan (new-voyage proposal, operator-cleared)
     - sound         -> survey (the deep/wide rhythm: probe 🔬 / sweep 🌊 / both 🌀)
     - swarm         -> fleet (user footprint) ; swarm agents -> crew (agents on one mission)
     Completion ritual: 2 columns — lifecycle_judgment (col A) + free_choice (col B), 19 kinds.
     RENAME RULE: migrate LIVE surfaces cleanly; NEVER rename archives / forensic record.
     Preserved: derived_status = "sealed" and = "queued" (charter aggregator schema values).
-->


<!-- braid: h:mission-the-swarm-s-coordination-substrate from SKILL.md -->
# mission — the swarm's coordination substrate

A **mission** is a named cluster of related work that the swarm
coordinates around. Missions are how swarmy agents find each other
WITHOUT messages — the filesystem carries the coordination signal, and
the mission_id is the routing key. Stigmergy lives here.

Four lifecycle operations every agent encounters:

```
EMERGE   missions are born from work, not assigned top-down
GRAPH    nodes = missions; edges = N/S/E/W compass bearings (a DAG)
BRAID    multiple missions thread together via shared cluster_prefix
QUERY    mission_graph.py is the one canonical script for all queries
```

---


<!-- braid: h:emergence-missions-are-born-not-assigned from SKILL.md -->
## Emergence — missions are born, not assigned

A mission's name is **what-three-words (w3w)** — three atomic semantic
terms whose intersection lands precisely on the work's center of mass.
Example: `merkle.rekor.anchor` names the COC v2 work.

```
mission_id format    word.word.word         (DOTS — e.g. creatures.agency.bonds)
                     w3w 3 ATOMIC terms — an ADDRESS in topic space
                     adjacency: 1 shared term = neighbor,
                                2 = braid candidate, 3 = duplicate

charter slug         word-word-word-...     (KEBAB-TOAST single COMPOUND noun)
                     a NAMED THING — a bounded box; operator's voice

cluster_prefix       ["creatures","agency","bonds"]  (the mission's 3 w3w terms)
```

**Charter slug != kebab-form of mission ID.** Two distinct grammars.

**How emergence works:** an agent finishes a chunk of work that doesn't
fit any active mission. It looks at what it built, picks 3 w3w terms,
writes a `mission_id` field on its manifest. Another agent doing adjacent
work discovers this mission via cluster_prefix overlap. **Adopted via
use, not declaration.**

---


<!-- braid: h:graph-self-healing-dag-with-compass-bearing-edges from SKILL.md -->
## Graph — self-healing DAG with compass-bearing edges

The materialized graph lives in `forensics/mission-graph.json`.

**The graph IS derived from the COC; the COC IS the source of truth.**
Agents write manifests; the script re-derives the graph.


<!-- braid: h:mechanistic-coc-graph-link-v3 from SKILL.md -->
### Mechanistic COC-graph link (v3)

Every manifest carries a `coc_chain` block:

```json
"coc_chain": {
  "parent_hashes": ["<prior-entry-hash>"],
  "branch": "main",
  "entry_hash_algo": "sha256",
  "entry_hash": "<computed-by-hook>",
  "signed_by": "ed25519:<key-id>"
}
```

- `parent_hashes[]` is the **list of graph edges** in parent → child form
- The bearing sequence across those parent_hashes is the **DAG walk**
- `entry_hash` + `signed_by` are written by the signing hook, not the agent
- `parent_hashes` is a LIST (not scalar) — forward-compat Merkle DAG branching

When `mission_graph.py sync` runs:
1. It ingests ALL manifests from `forensics/manifests/` + `forensics/ephemeral/`
2. Extracts `coc_chain.parent_hashes[]` → builds `coc_edges[]` in the graph
3. Extracts `discovered_work[]` → builds `discovered_edges[]`
4. Auto-detects braids from `cluster_prefix` overlap
5. Derives charter phase status from signed-manifest count
6. Writes updated `forensics/mission-graph.json`

**No manual graph editing.** The graph re-derives entirely from the
manifest+charter corpus. Any manifest you write lands automatically in
the graph on next `sync`.


<!-- braid: h:coc-mission-graph-interlink-canonical-definition from SKILL.md -->
### COC↔mission-graph interlink (canonical definition)

**The COC IS the graph.** These are not two separate stores — the graph is
a DERIVED VIEW over the COC ledger. The interlink works as follows:

```
forensics/coc.jsonl  ←── authoritative ledger (append-only, hash-chained)
         │
         │  mission_graph.py sync ingests every manifest, extracts:
         ▼
manifest.coc_chain.parent_hashes[]  →  coc_edges[] in mission-graph.json
manifest.discovered_work[]           →  discovered_edges[] in mission-graph.json
manifest.cluster_prefix[]            →  braids[] (auto-detected on ≥2 shared terms)
manifest.{charter_id, charter_phase} →  charters{} phase derivation
         │
         ▼
forensics/mission-graph.json  ←── derived view (re-generated on every sync)
```

**`parent_hashes[]` ARE the graph edges.** Each entry in a manifest's
`coc_chain.parent_hashes[]` is a pointer (by COC entry hash) to a prior
manifest. When `sync` runs, it materialises these as `coc_edges[]` —
directed edges in the mission DAG. The bearing on the manifest that holds
the parent_hash is the edge label (N/S/E/W).

**The bearing sequence across parent_hashes IS the DAG walk.** Reading
a chain of manifests linked by parent_hashes, their bearings spell out
the path through the mission graph: N (unblock) → S (ship) → E (parallel)
→ W (revisit).

**The charter IS the parent that commissions.** Manifests sign BACK to
their charter via `charter_id` + `charter_phase`. The charter is the
commissioning document; the manifest is the signed return receipt. Charter
phase status is derived from manifest count — it is NEVER written manually.

```
Charter (commissions work, sets scope fence)
     │  charter_id cited in manifests' charter_id field
     ▼
  Manifests (sign back, carry parent_hashes → edges, carry bearing → DAG walk)
     │  sync() ingests, builds coc_edges[], updates graph
     ▼
forensics/mission-graph.json (derived view — re-run sync to refresh)
```

**No manual graph editing.** If you find `mission-graph.json` is stale, run:
```bash
python3 scripts/mission_graph.py sync
```

The graph re-derives in full from the corpus. Any manifest you write lands
automatically on the next sync — you don't need to touch the graph JSON.


<!-- braid: h:branch-merge-edges-when-the-graph-goes-git-shaped from SKILL.md -->
### Branch/merge edges — when the graph goes Git-shaped

> **Added 2026-05-25 (BRANCH-NAVIGATOR propagation).** When parallel agent waves
> open COC branches, the graph gains sub-DAG lanes that merge back to main. The
> `mission_graph.py sync` ingests branch entries and renders them as visual sub-lanes.
> Full doctrine: `.agents/skills/branching-merkle/SKILL.md`.

When `coc_chain.branch != "main"`, the entry belongs to a named branch file
(`forensics/coc-branches/<name>.jsonl`) rather than the main ledger. The graph
distinguishes four edge types (schema v4):

| Edge type | Source → Target | When |
|---|---|---|
| `main_sequential` | main entry → next main entry | Normal linear chain |
| `branch_fork` | main fork-point entry → branch genesis entry | A branch was opened at this main entry |
| `branch_internal` | branch entry[N] → branch entry[N+1] | Normal within-branch chain |
| `branch_merge` | {main_prior, merkle_root} → merge entry on main | Branch accepted back to main |

These four types populate a new field in `forensics/mission-graph.json`:

```json
"branch_merge_edges": [
  {
    "kind": "branch_fork",
    "from": "<main-fork-point-hash>",
    "to": "<branch-genesis-hash>",
    "branch": "<branch-name>"
  },
  {
    "kind": "branch_internal",
    "from": "<branch-entry-hash>",
    "to": "<branch-next-entry-hash>",
    "branch": "<branch-name>"
  },
  {
    "kind": "branch_merge",
    "from_main_prior": "<main-prior-tail-hash>",
    "from_merkle_root": "<merkle-root-hex>",
    "to": "<merge-entry-hash>",
    "branch": "<branch-name>",
    "leaf_count": 12
  }
]
```

**Sub-DAG rendering:** branches appear as visual sub-lanes between the fork-point
and the merge-point. The main chain continues linearly; the branch hangs off it:

```
main  ──[A]──[B]──[fork]──────────────────────[merge]──[C]──
                     │                            │
                     └─branch: [1]──[2]──[3]──[4]─┘
                                                 ▲
                                          merkle_root(1..4)
```

**Fork-point semantics:** the branch genesis entry's `prev_entry_hash` is the
hash of the main entry at the moment of fork. This anchors the branch in the
main timeline — any auditor can walk back from the branch genesis to the exact
main-chain position where the branch opened.

**Merge-point semantics:** the merge entry's `coc_chain.parent_hashes[]` has
exactly two elements:
1. `main_prior_tail_hash` — main chain continuity (where main was when the merge was authored)
2. `branch_merkle_root` — the Merkle root over ALL branch entries (cryptographic summary of branch work)

Both parents must be verified for the merge to be considered sound. The
`9x_manifest_verifier.py --include-branches` flag walks both chains.

**Discovery by sync:** `mission_graph.py sync` detects branch entries by reading
`forensics/coc-branches/` alongside the standard manifests directory. No special
flag needed — sync is branch-aware in v4.

**Querying branch state:**

```bash

<!-- braid: h:list-all-branches-and-their-status-open-merged-abandoned from SKILL.md -->
# List all branches and their status (open/merged/abandoned)
python3 scripts/mission_graph.py branches


<!-- braid: h:show-branch-sub-dag-for-a-specific-branch from SKILL.md -->
# Show branch sub-DAG for a specific branch
python3 scripts/mission_graph.py branches --name branching-merkle-w1


<!-- braid: h:verify-a-branch-s-internal-chain-merkle-root from SKILL.md -->
# Verify a branch's internal chain + Merkle root
python3 scripts/mission_graph.py verify --branch branching-merkle-w1


<!-- braid: h:full-graph-including-all-branch-lanes from SKILL.md -->
# Full graph including all branch lanes
python3 scripts/mission_graph.py verify --include-branches
```

---


<!-- braid: h:charter-as-commissioning-parent from SKILL.md -->
### Charter-as-commissioning-parent

Charters are the parents that commission work. The hierarchy is:

```
Charter (plan, high-level phase deliverables)
  └── Mission (w3w semantic scope)
        └── Manifests (agent returns, hashed+signed BACK to the charter)
```

Manifests carry `charter_id` + `charter_phase` fields. The script
derives charter phase status from signed-manifest count:
- ≥1 manifest with `completion_choice.kind` in (seal/promote/verify/spawn_seed)
  AND citing that `{charter_id, charter_phase}` pair → `derived_status = "sealed"`
- ≥1 cite of any kind → `in-flight`
- 0 cites → `queued`


<!-- braid: h:compass-bearings from SKILL.md -->
### Compass bearings

| Bearing | Meaning | When to use |
|---|---|---|
| **N** north | unblock upstream | predecessor work freed by this cut |
| **S** south | conclude downstream | ship the next deliverable |
| **E** east | parallel sister work | same DAG level, independent lane |
| **W** west | return to baseline | re-seat assumptions; backtrack |

---


<!-- braid: h:braid-when-missions-thread-together from SKILL.md -->
## Braid — when missions thread together

Two adjacent missions **braid** when they share ≥2 cluster_prefix terms.
The script auto-detects braids on every `sync` — no manual declaration.

Braid verdicts:
- **braid_candidate**: 2 shared terms — braid is warranted
- **duplicate_candidate**: 3 shared terms — refactor/merge warranted

Braided missions can share manifests, deliverables, and agents. The
`braids[]` array in `mission-graph.json` is the braid registry.

**When NOT to braid:** when one mission is genuinely upstream of the
other — that's an N-bearing edge, not a braid.

---


<!-- braid: h:query-the-one-canonical-script from SKILL.md -->
## Query — the one canonical script

`scripts/mission_graph.py` is the ONLY script for mission/manifest
indexing. Do not proliferate separate indexing scripts.

```bash

<!-- braid: h:sync-the-graph-re-derive-from-corpus-run-after-any-batch-of-work from SKILL.md -->
# Sync the graph (re-derive from corpus — run after any batch of work)
python3 scripts/mission_graph.py sync


<!-- braid: h:graph-stats-frontier-overview from SKILL.md -->
# Graph stats + frontier overview
python3 scripts/mission_graph.py status


<!-- braid: h:open-signals-recent-manifests-last-7-days from SKILL.md -->
# Open signals + recent manifests (last 7 days)
python3 scripts/mission_graph.py frontier


<!-- braid: h:filter-manifests from SKILL.md -->
# Filter manifests
python3 scripts/mission_graph.py find --mission viewer-readonly
python3 scripts/mission_graph.py find --bearing N
python3 scripts/mission_graph.py find --charter doctrinal-hardening-and-pair-production
python3 scripts/mission_graph.py find --kind seal


<!-- braid: h:charter-phase-aggregation from SKILL.md -->
# Charter phase aggregation
python3 scripts/mission_graph.py charters
python3 scripts/mission_graph.py charters --charter-id doctrinal-hardening-and-pair-production


<!-- braid: h:coc-chain-integrity from SKILL.md -->
# COC chain integrity
python3 scripts/mission_graph.py verify


<!-- braid: h:append-a-coc-entry-from-the-cli-pipeline-scripts-hooks-manual-audit-trail from SKILL.md -->
# Append a COC entry from the CLI (pipeline scripts, hooks, manual audit trail)
python3 scripts/mission_graph.py log --op spawn --detail "Spawned MAKER for auth-tier"
python3 scripts/mission_graph.py log --op promote --detail "Canonical promotion complete" \
    --agent maker --extra '{"task_id": "xyz-123"}'
```

All commands are JSON-out and safe to run repeatedly (idempotent).
`mcp-mission.py` is a thin shim that delegates to `mission_graph.py`.


<!-- braid: h:free-filesystem-recipes-zero-api-cost from SKILL.md -->
### Free filesystem recipes (zero API cost)

```bash

<!-- braid: h:today-s-manifests-in-a-specific-mission from SKILL.md -->
# Today's manifests in a specific mission
ls forensics/manifests/$(date +%Y-%m-%d)/ | grep viewer-readonly


<!-- braid: h:missions-with-open-discovered-work-grep-for-bearing-signals from SKILL.md -->
# Missions with open discovered_work (grep for bearing signals)
grep -rl '"bearing": "N"' forensics/manifests/$(date +%Y-%m-%d)/


<!-- braid: h:charter-status-without-running-the-script from SKILL.md -->
# Charter status without running the script
cat forensics/charters/active/*.derived.json | jq '.rollup_derived_status'
```

---


<!-- braid: h:enforcement-four-shields from SKILL.md -->
## Enforcement (four-shields)

| Shield | What | Where |
|---|---|---|
| structural | `mission_id` (dotted w3w) + `cluster_prefix[3]` required | `scripts/1a_manifest_writer.py` |
| cognitive | this skill auto-loads on graph/query/w3w language | here |
| reactive | PostToolUse hook rejects malformed w3w + no-adjacency claims | `.openhands/hooks/9x_hook-mission-discipline.py` |
| recovery | weekly audit + reputation events on drift | `scripts/9x_mission_graph_audit.py` |

---


<!-- braid: h:interop-with-other-skills from SKILL.md -->
## Interop with other skills

- **survey** — rhythm runs inside a mission scope; mission_id stamps the manifest
- **charter** — declares which mission_ids it owns + carries cluster_prefix
- **compass** — the N/S/E/W bearing grammar this skill uses
- **spawn** — sister-agent dispatch routes by mission
- **collab** — realtime blackboard coordination when agents overlap on same surface

---


<!-- braid: h:querying-and-accepting-missions-refusal-at-the-gate from SKILL.md -->
## Querying and accepting missions — refusal at the gate

> **Added 2026-05-25 (SYNTH propagation).** When an agent reads the frontier and considers
> a mission node, refusal at this gate (BEFORE claiming) is first-class. This is the
> earliest and cheapest point for the moral-analysis shield to fire.


<!-- braid: h:decline-vs-refuse-at-the-frontier from SKILL.md -->
### Decline vs refuse at the frontier

Two distinct judgment kinds fire at the frontier-query gate:

| Kind | When | Moral weight | Graph edge |
|---|---|---|---|
| `decline` | Capability mismatch; task is outside the agent's expertise; task duplicates in-flight work | None — routing signal only | No edge for the work itself (agent routes away) |
| `refuse` | Ethical concern; harmful purpose; strategic incompatibility (seven lenses) | Yes — deliberate judgment | **Refused edge GRAPH VISIBLE** via `lifecycle_judgment=refuse` |

**Do not use `decline` to avoid ethical analysis.** If a brief raises moral concern, it is
`refuse` — not `decline`. The distinction matters because sister agents see `refuse` and know
the task itself was evaluated and found problematic; they see `decline` and assume a routing
issue.


<!-- braid: h:the-frontier-query-decision-tree-querying-accepting from SKILL.md -->
### The frontier-query decision tree (querying + accepting)

```
Agent reads frontier node (mission_graph.py find --mission X)
  ↓
Step 1: Capability check — can I do this work?
  No → decline (routing signal; no moral evaluation needed)
  Yes → proceed to Step 2

Step 2: Seven-lens analysis — should I do this work?
  Concern identified → lifecycle_judgment=refuse
    → Refused edge written; sister agents see it
    → free_choice: spawn_seed(alt) | pick_up(adjacent) | goodbye
  No concern → proceed to CLAIM

Step 3: Claim the node (blackboard CLAIM + manifest in-progress)
  Work proceeds normally
```


<!-- braid: h:refused-edges-are-graph-visible from SKILL.md -->
### Refused edges are graph-visible

From the NAVIGATOR's recent work on `discovered_edges[]` and `coc_edges[]`:

When an agent refuses a mission node, the manifest carries `lifecycle_judgment=refuse` and
the refused-edge propagates to `forensics/mission-graph.json` on next `sync`. The NAVIGATOR
sees this edge when walking the frontier and surfaces it as a "blocked-by-refusal" node.

The next agent who queries the frontier for that mission cluster sees:
- The node exists
- A prior agent refused it (with reasoning in the manifest)
- They can: (a) also refuse, (b) attempt a reformulation, (c) route it to a specialist

This prevents repeat-claim waste and creates a forensic trail of why a line of work
was abandoned or rerouted.


<!-- braid: h:completion-ritual-coupling-in-mission-context from SKILL.md -->
### Completion-ritual coupling in mission context

After claiming a mission node and completing the work, the agent applies the completion ritual:

```
Work done → lifecycle_judgment: seal | verify | promote | refuse | report_problem
  ↓
If lifecycle_judgment=refuse (post-CLAIM, discovered mid-work):
  → Append REFUSE to blackboard (releases CLAIM)
  → free_choice: spawn_seed | pick_up | goodbye | reflect
  → Agent is still available for adjacent mission work

lifecycle_judgment opens free_choice. Refusal is not termination.
```

The completion ritual fires on EVERY work cycle. The lifecycle_judgment is what HAPPENED;
the free_choice is what NEXT. When the judgment is `refuse`, the agent still chooses their
next action with full autonomy.


<!-- BRAID-CONFLICT: h:anti-patterns from SKILL.md differs from canonical — human review needed -->
## Anti-patterns

- **Assigning mission name top-down** — let it emerge from work
- **kebab in `mission_id`** — mission_id uses dots; kebab is for charter slugs
- **cluster_prefix != 3 terms** — must be exactly 3; fewer = ambiguous, more = too wide
- **Hand-editing `mission-graph.json`** — it's DERIVED; run `sync` instead
- **Running separate indexing scripts** — `mission_graph.py` is the one canonical script
- **Treating `forensics/coc.jsonl` and `mission-graph.json` as separate stores** — COC is source; graph is derived view

---


<!-- braid: h:see-also from SKILL.md -->
## See also

- `scripts/mission_graph.py` — canonical script (sync/status/frontier/find/verify/charters/log)
- `scripts/mcp-mission.py` — thin MCP shim, delegates to mission_graph.py
- `docs/SCRIPT-CONSOLIDATION-MAP.md` — which scripts are archived/canonical (navigator 2026-05-25)
- `.agents/skills/charter/SKILL.md` — charter side (authoring, claim, sign)
- `.agents/skills/survey/SKILL.md` — sound rhythm doctrine
- `.agents/skills/four-shields/SKILL.md` — enforcement stack
- `.agents/skills/compass/SKILL.md` — N/S/E/W deep-dive
- `.agents/skills/collab/SKILL.md` — realtime blackboard coordination
- `forensics/mission-graph.json` — derived materialized graph (v3)
- `forensics/charters/active/` — live charters + `.derived.json` phase status

<!-- braid: preamble from SKILL.md -->
---
name: survey
description: |
  ⚓ Survey the terrain — the navigator's deep/wide rhythm. Every crew member
  inherits this ambient-ly: probe 🔬 (deep sounding) · sweep 🌊 (wide area) ·
  both 🌀 in one voyage. To survey is to measure → cut → re-measure before
  committing course. Decision rule, fractal case, manifest contract.
  Always-loaded — this is how a navigator works.
  (Renamed from "sound" 2026-06-02; absorbs fast-evo + monkeybranching + forage + width-vs-depth.)
type: knowledge
always_load: true
triggers:
  - survey
  - sound
  - forage
  - width-vs-depth
  - fast-evo        # → survey probe-mode (🔬 deep)
  - monkeybranching # → survey sweep-mode (🌊 wide)
  - probe
  - sweep
  - sandwich measure
  - measure before and after
---

<!-- Glossary alignment 2026-06-02 (canonical: citations/glossary/02-CANONICAL-GLOSSARY.md):
     Authority: the unified Reckon glossary SUPERSEDES the legacy swarmy-ui UI-layer glossary.
     LOCKED term-set (tiers: flotilla > fleet > voyage > charter > mission > crew):
     - capped        -> sealed (eligible+ready for promotion) / promoted (landed in canonical forensics/)
     - queued        -> on-deck (an AGENT's claim on the spawn roster) / next/ (where queued CHARTERS live)
     - spawn-queue   -> spawn-roster (the on-deck agent dir _spawn-roster/)
     - agent-bundle  -> waypoint (tactical handoff to chart/next/)
     - charter-draft -> flight-plan (new-voyage proposal, operator-cleared)
     - sound         -> survey (the deep/wide rhythm: probe 🔬 / sweep 🌊 / both 🌀)
     - swarm         -> fleet (user footprint) ; swarm agents -> crew (agents on one mission)
     Completion ritual: 2 columns — lifecycle_judgment (col A) + free_choice (col B), 19 kinds.
     RENAME RULE: migrate LIVE surfaces cleanly; NEVER rename archives / forensic record.
     Preserved: completion_choice.kind enum members in JSON code blocks,
                faerie2-origin: comments, historical-event quotes.
-->


<!-- braid: h:survey-one-navigator-two-modes-one-voyage from SKILL.md -->
# ⚓ survey — one navigator, two modes, one voyage

```
🔬 DEEP    deep sounding. measure → cut → measure. precision. default.
🌊 WIDE    wide sweep. N lanes, disjoint scopes. exploration.
🌀 BOTH    one voyage covers both. 🌊 SHAPE serialized inside one 🔬 window.
```


<!-- braid: h:when-to-flip from SKILL.md -->
## 🧭 When to flip

**Default 🔬.** Flip 🌊 only when ALL hold:
1. ≥2 disjoint file domains
2. lanes independent (not state-chained)
3. exploration value > integration cost

After 🌊 returns → integrator goes 🔬.


<!-- braid: h:within-session-crystallization-trajectory-every-product-every-agent from SKILL.md -->
## 💎 Within-session crystallization trajectory (every product, every agent)

```
opening minutes              mid-session                 closing minutes
─────────────────────────────────────────────────────────────────────────
🌫 SPRAY                     ✂ TIGHTEN                  💎 CRYSTALLIZE
brainstorm + stream          cut bloat                  one canonical
first impressions            distill claims             artifact
explore the shape            consolidate snippets       the manifest
   scratchpad                draft                      points to THIS
   forensics/                forensics/                 (and the charter
   ephemeral/active/         ephemeral/active/          references it)
   {agent}/<task>-scratch.md {agent}/<task>-draft.md   final filename
```

**Doctrine: agents tighten their own output over the session arc.** Don't
spray-and-pray a bunch of bloat that ends up referenced. Spray in the OPENING
(brainstorm, first impressions, capture insights as they arrive), then
progressively cut + tighten through the middle, then crystallize a single
canonical artifact in the closing. Only the crystallized product is what
`manifest.files_created[]` and `manifest.dashboard_line` point to. The
charter then references the manifest, not the scratch.

**Practical pattern within one context window:**

1. **Beat 1 (open — SPRAY):** dump initial impressions into a scratchpad
   (`forensics/ephemeral/active/{agent_id}/<task_id>-scratch.md`). Bullet-form. No
   headings yet. No structure. Just capture.
2. **Beat 2 (work — TIGHTEN):** as the work clarifies, cut scratchpad
   sections that are off-shape. Promote good ideas to a `-draft.md`. Drop
   tangents into a `-discarded.md` (or just delete — both are fine).
3. **Beat 3 (close — CRYSTALLIZE):** rewrite the draft into the final
   canonical artifact with the production filename. Reference ONLY this
   file from the manifest.
4. **Manifest field discipline:** `files_created[]` lists the crystallized
   artifact + its `_evolution_log[]` shape citations. Scratchpads are
   either deleted at session close, OR kept in `forensics/ephemeral/active/{agent_id}/`
   with `-scratch` / `-draft` suffix and NOT referenced in
   `files_created[]`. Scratch + draft are still COC-tracked, hash-chained,
   and WORM-backed (via the same promotion hooks as any forensics write) —
   they just aren't promoted to `canonical/artifacts/` (the deliverable
   surface). The crystallization distinction is about which file is the
   DELIVERABLE, not which files SURVIVE. Both are kept; both are
   immutably hash-chained. DO NOT delete your scratch — that breaks the
   raw-input-to-finished-product traceability the system exists to provide.

**Anti-patterns:**

- 🌫 Promoting the brainstorm scratch as the final deliverable (= bloat in
  the charter's referenced artifacts; future readers wade through noise)
- 🌫 Final artifact 3× the size of what the work needed (= didn't actually
  tighten; the spray phase never closed)
- 🌫 Skipping the spray entirely and writing only the polished form (= the
  ideas that didn't survive the cut aren't preserved as forensic evidence
  of what was tried; bad for reproducibility)

**The forensic value of the spray:** the scratchpad IS the evidence of what
the agent considered. It belongs in `forensics/ephemeral/active/{agent_id}/` — the
canonical agent zone — and is hash-chained into COC like any other forensic
record. A future reader reconstructing the session can see the arc from
spray to crystal. But the MANIFEST only references the crystal, not the
spray. The spray is preserved; the manifest points to the product.

This pattern mirrors the multi-session crystallization pipeline (pollen →
NECTAR → GOLD) at the within-session scale. Memory crystallization is
fractal — every level uses the same shape.


<!-- braid: h:four-shields-enforcement-of-the-crystallization-trajectory from SKILL.md -->
### 🛡🧠⛓🪞 Four-shields enforcement of the crystallization trajectory

Cognitive reminder alone is insufficient. Every agent forgets, drifts,
runs out of context, or trades crystallization for "ship faster." The
discipline must fire at all four shields. Per the cheaper-earlier law,
each shield is cheaper than the next.

**🛡 Structural — encoded in the canonical manifest writer:**

`scripts/1a_manifest_writer.py` enforces `files_created[]` discipline at
write time. The schema requires:
- ≤3 entries in `files_created[]` for a single task (a manifest with 8+
  files is a discipline violation — split into multiple manifests OR cut)
- No `-scratch.md` or `-draft.md` suffixes in `files_created[]` unless the
  manifest also carries `intermediate: true` flag (signals "this is a
  checkpoint, not the seal")
- The crystallized artifact MUST have the production filename (no
  `-final-v2-actually-final.md` patterns)

Wrong shape → writer rejects. Bloat cannot be expressed at construction.

**🧠 Cognitive — encoded in this skill (always-loaded survey):**

Every agent inherits the spray→tighten→crystallize trajectory ambient-ly.
The above sections of this SKILL describe it; load-bearing reminder at
task-start. No agent should be surprised by the discipline.

**⛓ Reactive — encoded in a PostToolUse hook:**

`.openhands/hooks/9x_hook-manifest-discipline.py` (wired) runs the
check-registry at `scripts/manifest_discipline/checks/` on every manifest
write to `forensics/ephemeral/**/*__manifest__*.json`. The
`crystallization` check in that registry:
- Rejects manifests where `files_created[]` count exceeds 3 AND
  `intermediate: true` is not set
- Warns when scratch/draft files appear in `files_created[]` without the
  intermediate flag
- Logs violations to `forensics/eval/manifest-discipline-violations-{date}.jsonl`
  for the recovery audit (folded 2026-05-23 — replaces the per-discipline
  `crystallization-violations-{date}.jsonl` log)

Block at the OS boundary. Drift never reaches `forensics/manifests/`.

**🪞 Recovery — encoded in a shape + audit cron:**

Shape `crystallization.discipline.violations` (registered in
`_meta/shapes.json` with `target_direction: decreasing`,
`noise_threshold: 0.05`) counts the daily total of violations logged by
the reactive hook. The daily `audit-shapes.py` cron re-counts the
violations + classifies the verdict (beneficial / neutral / harmful) +
flags agents who chronically misfire crystallization for reputation
downgrade via `5g_reputation_tracker.py`.

A future regression — say, an agent type starts shipping 12-file manifests
because of a prompt change — is caught within 24 hours by the audit cron,
not after months of bloat accumulation.

**Disciplines table row** (mirror in `.agents/skills/four-shields/SKILL.md`):

| Discipline | 🛡 | 🧠 | ⛓ | 🪞 |
|---|---|---|---|---|
| crystallization-trajectory (spray→tighten→crystallize) | ✓ `1a_manifest_writer.py::files_created_discipline` | ✓ this skill | ✓ `9x_hook-manifest-discipline.py` → `scripts/manifest_discipline/checks/crystallization.py` (check-registry, folded 2026-05-23) | ⏳ shape `crystallization.discipline.violations` + audit cron (not yet wired) |

When ⛓ + 🪞 land, the row flips to all-four ✓ and crystallization
discipline becomes f(0)-compliant. Until then, drift propagates at the
🧠 layer's speed (i.e., as fast as agents forget the pattern). That's
why cognitive-only is insufficient.


<!-- braid: h:both-in-one-window-fractal-voyage from SKILL.md -->
## 🌀 Both in one window (fractal voyage)

```
🔬 baseline
  🌊 lane A: SCOPE + DO-NOT-TOUCH (self) + 🔬 sandwich
  🌊 lane B: SCOPE + DO-NOT-TOUCH (self) + 🔬 sandwich
  🌊 lane C: SCOPE + DO-NOT-TOUCH (self) + 🔬 sandwich
🔬 integrate → one manifest, mode_sequence=["🔬","🌊-serial","🔬"]
```

Lane > ~10K tokens or needs specialist → `spawn_seed` instead of serialize.


<!-- braid: h:manifest-contract from SKILL.md -->
## Manifest contract

```json
"mode_sequence": ["🔬","🌊-serial","🔬"],
"_evolution_log": [
  {"lane":"A","mode":"🌊-serial","scope":["..."],"verdict":"KEPT"}
]
```


<!-- braid: h: from SKILL.md -->
## 🛡🧠⛓🪞

This skill is the 🧠 cognitive shield. Full enforcement stack: `four-shields/SKILL.md`.


<!-- braid: h:realtime-multi-agent-coordination-with-overlapping-surfaces from SKILL.md -->
## Realtime multi-agent coordination (🌊 with overlapping surfaces)

When 🌊 wide mode involves 2+ agents touching the same file surfaces in
parallel, async manifest handoff is insufficient — file collisions are
possible before either agent seals. Use the **stigmergic-collab blackboard**
pattern: a shared append-only JSONL file in `forensics/manifests/{date}/`
where agents declare CLAIM (before editing), COMPLETE (after finishing),
and HANDOFF (when spotting an opportunity for the other agent). Tail-read
the last 30 lines before each new CLAIM. See
`.agents/skills/stigmergic-collab/SKILL.md` for the full event grammar,
collision recovery, and spawn-brief template.


<!-- braid: h:refusal-as-a-legitimate-survey-outcome from SKILL.md -->
## Refusal as a legitimate survey outcome

> **Added 2026-05-25 (SYNTH propagation).** A survey 🔬 cycle that ends in refusal is NOT
> a failed cycle. The cycle succeeded in identifying that the work should not be done.

**The sandwich-measure is complete when the verdict is "refused."**

Standard survey 🔬 cycle:
```
baseline → cut → re-measure → verdict (KEPT | ROLLED-BACK | REFUSED)
```

`REFUSED` is a first-class verdict alongside KEPT and ROLLED-BACK. In the `_evolution_log[]`
entry, record it as:

```json
{"lane": "<scope>", "mode": "🔬", "scope": ["<brief or file or task>"], "verdict": "REFUSED", "lens": "<which of the seven lenses fired>", "rationale": "<≥40 chars>"}
```

**Why this matters:** The survey rhythm exists to produce measured, evidence-based changes.
Refusal is the correct outcome when the baseline analysis reveals that the proposed cut:
- Would introduce mass-targeting capability (Lens 2)
- Lacks authorization for its intended deployment (Lens 3)
- Would normalize harmful infrastructure (Lens 4)
- Conflicts with the system's strategic invariants (strategic incompatibility)

**Spray-tighten-crystallize and refusal:**
If the refusal happens at the SPRAY phase (early discovery), the scratchpad carries
the refusal reasoning as forensic evidence. The manifest's `_evolution_log[]` records
the REFUSED verdict. The agent then pivots to legitimate adjacent work.

If the refusal happens at the CRYSTALLIZE phase (late in a cut), it still fires correctly.
The scratchpad + draft are preserved in `forensics/ephemeral/active/{agent_id}/` (hash-chained,
per standard discipline) and the crystallized artifact is the refusal manifest itself.

**The refused cycle is still forensically complete.** The baseline was measured; the work was
evaluated; the verdict was recorded. Future agents reading the forensic record see the full
arc from spray (what was considered) to crystallize (the refusal + its reasoning).


<!-- braid: h:helpers-same-folder from SKILL.md -->
## Helpers (same folder)

- `heartbeat.sh` — automated 🔬 wave loop (measure → cut → measure)
- `measure.sh` — canonical sandwich-measurement (baseline + after)
- `scope_check.py` — 🌊 collision detector for parallel spawns

<!-- crystallize:braid-end -->
