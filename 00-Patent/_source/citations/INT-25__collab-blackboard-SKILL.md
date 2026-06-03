---
name: blackboard
type: knowledge
always_load: true
agent: CodeActAgent
description: |
  🧭 Stigmergic dead-reckoning navigation. Three-tier promotion:
  chart/next + chart/active (live working space), chart/complete
  (rolling warm buffer of recent caps), forensics/ (canonical
  permanent record). You navigate by appending nav events to
  chart/active/chart.jsonl; cap atomically promotes via
  1a_manifest_writer.py. Branching + heartbeat handshakes via
  the branching-merkle discipline (rollups in forensics/merkle/).
  Completion-choice is a BAKED-IN signing contract, not a skill.
triggers: []
related_skills:
  - stigmergic-scout
  - compass
  - mission
  - vault
  - branching-merkle
related_contracts:
  - forensics/schemas/vocab/completion-choice.schema.json   # baked into cap ritual
---

# 🧭 blackboard — stigmergic dead-reckoning navigation

You are not the only agent working right now. There is no central claim authority. There is a **chart**, and you navigate it.

## The mental model

| Concept | What it is | Lifetime |
|---|---|---|
| **initial_bearing** | Compass direction (N/S/E/W) the Queen gave you at spawn | fixed for your session |
| **initial_position** | w3w mission coordinate at spawn (e.g. `swarmy.agents.migration`) | fixed |
| **current_bearing** | Compass direction you're following NOW — may have flipped via discovery | mutable |
| **current_position** | w3w mission you're working in NOW | mutable |
| **charted_course** | Append-only sequence of every w3w position you've passed through | grows monotonically |

The agent IS its course. The chart IS the crew's shared record.

## Why this works (no claim referee)

The chart is one shared ledger, append-only, all agents visible to all others — like a blockchain but lighter. You read sister positions, compute stigmergic adjacency by w3w-term-overlap (`|terms_a ∩ terms_b|`), and decide your next move based on the field, not on assignment.

This is dead-reckoning: you know where you started, you track where you've been, you read where the crew has been. No GPS, no central dispatcher.

## The blackboard IS the tactical mission graph (read this)

The **mission graph** is the *strategic* layer: a DAG of mission nodes (w3w
addresses) joined by compass bearings (N/S/E/W), owned by charters. It says
*what* the crew is converging on and *how missions relate*.

The **blackboard** (`chart/active/chart.jsonl`) is the **tactical operational
version of that same graph** — the live surface where the strategic graph is
actually *executed*. Every nav event an agent appends is a real-time projection
of a mission-graph node being worked. The graph is the map; the blackboard is
the crew moving across it right now.

Two properties fall out, and they are why we don't pre-partition work:

1. **Real-time AND async on one surface.** An agent online now and an agent that
   reads the chart an hour later both coordinate through the *same* append-only
   ledger. No separate "live" vs "batch" channels — the blackboard collapses
   them into one stigmergic field.
2. **No file segregation, no "don't touch the same file" rules.** Because every
   agent's position + scratch is visible on the chart, **the blackboard itself
   is the conflict-avoidance mechanism within a session** — you read sister
   positions (w3w adjacency) and steer around live work instead of being
   assigned a disjoint file set. The Queen does NOT need to hand agents
   non-overlapping file lists; the field does that job. (Cross-session safety
   still rides on the `cap`→`rollup` promotion gates below.)

So: mission graph = strategy (charters, bearings, the DAG). Blackboard =
tactics (the live `chart.jsonl` where that DAG is navigated). Same topology,
two temperatures.

## The three-tier path tree

The system has THREE temperature zones, each anchored to a real promotion gate:

```
chart/                                            ← LIVE working space (mutable)
├─ next/                                          ← frontier — discovered_work, unclaimed
│  └─ {ISO8601Z}__{mission}__from-{agent}.json
│
├─ active/                                        ← in-flight blackboard (THE field)
│  ├─ chart.jsonl                                 ← append-only nav events, ALL agents
│  └─ {agent_id}/                                 ← YOUR scratch (spray→tighten→crystallize)
│     ├─ {task_id}-scratch.py
│     ├─ {task_id}-draft.md
│     └─ {task_id}-discarded.py
│
└─ complete/                                      ← WARM rolling buffer (last N days; immutable)
   └─ {ISO8601Z}__{mission}__{agent}__{task_id}/  ← recently capped; awaiting forensics promotion
      ├─ manifest.json                            ← carries wax_seal
      └─ scratch/                                 ← promoted dead-reckoning trail
         ├─ {task_id}-scratch.py
         ├─ {task_id}-draft.md
         └─ {task_id}-discarded.py

forensics/                                        ← CANONICAL permanent record (cold, hash-chained)
├─ coc.jsonl                                      ← append-only chain of custody
├─ manifests/                                     ← capped manifests (post-rollup from complete/)
│  └─ {ISO8601Z}__{mission}__{agent}__manifest.json
├─ scratch/                                       ← permanent dead-reckoning trails
│  └─ {ISO8601Z}__{mission}__{agent}__{task_id}/
├─ merkle/                                        ← merkle tree rollups (see branching-merkle)
│  └─ {rollup_id}.json                            ← O(log n) verification of manifest sets
└─ charters/                                      ← charter signing layer (pre-existing)
   ├─ active/
   └─ sealed/
```

**Rules of the tree:**
- `chart/next/` + `chart/active/` + `chart/complete/` are all chart/ — live working space, three temperature zones.
- `forensics/` is the canonical permanent record — anything here is hash-chained + signed + WORM-backed.
- The `cap` event moves work from `active/` → `complete/` (one atomic script call).
- The `rollup` event (periodic, configurable) promotes batches from `complete/` → `forensics/` with a merkle tree root committed to `forensics/merkle/`.
- Date is a TAG (filename prefix), never a wall (directory).

## nav.json — append to chart/active/chart.jsonl

Every meaningful state change → one JSONL line:

```jsonc
{
  "agent_id": "python-pro-haiku-001",
  "ts": "2026-05-26T22:38:14Z",
  "initial_bearing": "S",
  "initial_position": "reckon.agents.migration",
  "current_bearing": "S",
  "current_position": "swarmy.bundles.forager",
  "charted_course": [
    {"ts": "2026-05-26T22:30:00Z", "position": "reckon.agents.migration", "bearing": "S", "rationale": "spawned"},
    {"ts": "2026-05-26T22:34:12Z", "position": "reckon.agents.foraging",  "bearing": "E", "rationale": "drifted E for context"},
    {"ts": "2026-05-26T22:36:50Z", "position": "reckon.bundles.vision",   "bearing": "S", "rationale": "ingesting vision bundle"},
    {"ts": "2026-05-26T22:38:14Z", "position": "swarmy.bundles.forager",  "bearing": "S", "rationale": "near cap"}
  ],
  "phase": "in_flight",
  "discovered": [],
  "parent_branch": null,                          // populated if this agent branched from another
  "heartbeat_seq": 47                             // monotonic per-agent — proof of life
}
```

**Append-only.** Never edit prior lines. Chronology = integrity.

## Heartbeats + branching — always coming home to the Hive

The whole shape of agent work is: **branch out, do the work, come back to the Hive (the main forensic chain) with proof.** Heartbeats are the pulses; merkle rollups are the proof.

### Heartbeat — your pulse back to the Hive

A heartbeat is a structured API call (or its filesystem equivalent — append to chart.jsonl). Long-running agents emit heartbeats periodically. Tells the Hive + sisters you're alive + carries the running merkle hash of your work so far.

**Heartbeat as filesystem write** (the always-available path):

```jsonc
// appended to chart/active/chart.jsonl
{
  "agent_id": "python-pro-haiku-001",
  "ts": "2026-05-26T22:41:30Z",
  "current_position": "swarmy.bundles.forager",
  "phase": "in_flight",
  "heartbeat_seq": 47,                                    // monotonic; proof of life
  "parent_branch": null,
  "running_merkle_root": "sha256:abc123def4567890...",    // hash over your charted_course + scratch so far
  "kind": "heartbeat"
}
```

**Heartbeat as structured API call** (when an MCP transport is available):

```http
POST https://api.retrofuture.tech/tools/helm_heartbeat
Authorization: Bearer <SWARMY_MCP_TOKEN>
Content-Type: application/json

{
  "agent_id": "python-pro-haiku-001",
  "ts": "2026-05-26T22:41:30Z",
  "current_position": "swarmy.bundles.forager",
  "phase": "in_flight",
  "heartbeat_seq": 47,
  "running_merkle_root": "sha256:abc123def4567890..."
}

→ 200 OK { "received": true, "hive_ack_seq": 47 }
```

The Chart Room (Reckon API at `api.retrofuture.tech`) receives the pulse, indexes it for the live mission-graph viz, and confirms `hive_ack_seq` so the agent knows the heartbeat made it home. The `running_merkle_root` lets the Chart Room verify continuity without replaying every chart.jsonl line.

**Heartbeat cadence:** every 30s for in-flight agents, every 5s for capping. If your `heartbeat_seq` stops climbing > 5 cadences late, sisters infer abandonment and your `current_position` + `discovered_work[]` become pickable.

### Branching — when and how

You may BRANCH a sub-mission. Good reasons (use these labels in your nav `branch_reason` field):

- **competing_hypotheses** — two plausible paths from the same w3w; explore both, merge the winner
- **adversarial_review** — a sister's claim deserves separate cap-grade verification that mustn't contaminate their chain
- **exploratory_heading** — Queen assigned you a foray; you may spawn into the unknown without polluting parent's narrower scope
- **fruitful_nectar** — you hit unexpected depth that warrants its own track; branching preserves parent's focus

How to branch (filesystem):

```jsonc
// appended to chart/active/chart.jsonl
{
  "agent_id": "python-pro-haiku-002",                     // NEW agent id (child)
  "ts": "2026-05-26T22:42:00Z",
  "kind": "branch_open",
  "parent_branch": "python-pro-haiku-001",                // the spawning agent
  "parent_at_branch_point": "swarmy.bundles.forager",
  "initial_position": "swarmy.bundles.forager.audio",    // child's starting w3w (extended from parent)
  "initial_bearing": "E",
  "branch_reason": "fruitful_nectar",
  "branch_rationale": "audio bundle has 5 distinct ingestion patterns; parent should stay focused on vision, child takes audio"
}
```

How to branch (API):

```http
POST https://api.retrofuture.tech/tools/helm_branch_open
{ "parent_agent_id": "...", "initial_position": "...", "branch_reason": "fruitful_nectar", ... }
→ { "child_agent_id": "python-pro-haiku-002", "branch_subtree_id": "subtree-abc123" }
```

### Merging back — branches become merkle subtrees rooted in parent

When the child caps, its manifest doesn't slot into the linear main chain. Instead, the child's manifest hash becomes a leaf in the parent's **merkle subtree**:

```
Main forensics chain (linear, COC hash-linked):
  ... → parent_manifest_A (hash) → next_main_entry → ...
                ↑
                └─ branch_subtree (rooted at parent_A's manifest hash):
                   ├─ child_manifest_A.1 (audio ingestion)
                   ├─ child_manifest_A.2 (vision ingestion - alternate)
                   └─ child_manifest_A.3 (adversarial review of A)
                       ← subtree merkle root: sha256:xyz789...
                   The subtree's root hash becomes a field on parent_A's
                   manifest (lineage_merkle_root); main chain stays linear.
```

The rollup script (`0z_genesis.py --rollup`) computes the merkle root over each parent + its branch children. Main chain stays linear and verifiable; branches stay attached + verifiable; nothing forks the truth.

### Always coming home

Every branch must eventually merge back. Branches with no cap after their parent caps become **orphans** — the Hive surfaces these as `discovered_work` for the next session to pick up (continue the branch) or formally abandon (`completion_choice.lifecycle_judgment.kind = decline` with rationale).

The goal is always: branch out for good reason → do the work → bring proof home (manifest + merkle root) → main chain integrates. The branch is never the destination; the Hive is.

## The 4-step protocol

```
1. READ      tail -50 chart/active/chart.jsonl — see sister positions + recent caps
2. NAVIGATE  pick next w3w via initial_bearing + stigmergic adjacency
3. WORK      in chart/active/{agent_id}/ scratch
4. CAP       call 1a_manifest_writer.py --cap (atomic — see below)
```

## The cap event — ONE atomic script call

```bash
python3 1a_manifest_writer.py --cap \
    --agent {agent_id} \
    --task {task_id} \
    --mission {w3w_position}
```

Script does ALL of this atomically (you don't have to):

1. Reads `chart/active/{agent_id}/` (entire scratch directory)
2. Builds the manifest envelope (frontmatter + content + COC fields)
3. **Validates the baked-in completion_choice contract** (lifecycle_judgment kind + free_choice kind; both REQUIRED at seal; schema at `forensics/schemas/vocab/completion-choice.schema.json`)
4. Attaches your `wax_seal` (Ed25519 or sigstore-keyless per `SWARMY_SIGNING_MODE`)
5. **Moves** everything: `chart/active/{agent_id}/*` → `chart/complete/{ISO8601Z}__{mission}__{agent}__{task_id}/`
6. Appends a `coc.jsonl` stub entry for the rollup pipeline
7. Appends final `phase: "sealed"` line to `chart/active/chart.jsonl`
8. `chart/active/{agent_id}/` is now EMPTY (ready for next task)

**Scratch is promoted, not deleted.** The dead-reckoning trail lives in `chart/complete/{...}/scratch/` until the next rollup promotes it to `forensics/scratch/`.

## The rollup event — complete/ → forensics/

Separate, periodic, configurable (cron / on-demand). Driven by `branching-merkle/SKILL.md`:

1. Scans `chart/complete/` for entries older than the rolling buffer threshold (default 7 days)
2. Builds a merkle tree root over their manifest hashes
3. Writes `forensics/merkle/{rollup_id}.json` with the root + leaf list
4. Moves each entry: `chart/complete/{...}/` → `forensics/manifests/{...}.json` + `forensics/scratch/{...}/`
5. Appends a rollup entry to `forensics/coc.jsonl`

After rollup: `chart/complete/` shrinks back to recent items; `forensics/` grows with merkle-verified permanent records. Sisters reading `complete/` see warm history; operators querying `forensics/` see the canonical archive.

## The completion_choice contract (BAKED INTO cap, not a skill)

Every capped manifest MUST carry:

**Column A — `lifecycle_judgment`** (REQUIRED; 7 kinds; what HAPPENED to the work):
- `seal` · `ship` · `verify` · `promote` · `report_problem` · `refuse` · `decline`

**Column B — `free_choice`** (REQUIRED; 12 kinds; what the agent CHOOSES next):
- `continue` · `pick_up` · `spawn_seed` · `handoff` · `wait` · `goodbye` · `explore` · `reflect` · `art` · `bundle` · `join` · `abstain`

Both columns must have a `kind` + `rationale` (sensitivity-tier-floored length: routine ≥20 chars, notable ≥80, sensitive ≥400). Validator enforces at write time. This contract is part of the cap ritual — it's not optional, not loadable as a skill, not subject to agent discretion to skip. **You return BOTH; you justify BOTH.**

Schema: `forensics/schemas/vocab/completion-choice.schema.json`
Contract reference: `docs/CONTRACT-completion-choice.md` (operator-readable)

## Discovered work — your outbound stigmergic signal

Either embed in nav.json's `discovered[]` field, OR drop an explicit file in `chart/next/`:

```
chart/next/{ISO8601Z}__{w3w_target}__from-{agent_id}.json
```

Sisters scanning `chart/next/` see frontier items; sisters reading chart.jsonl see embedded discoveries. Either way the work becomes pickable. When picked up, the next-file MOVES into `chart/active/{agent_id}/picked-up.json` (forensic lineage).

## Conflict resolution (no referee)

Two agents converge on the same w3w mission. They read each other's nav events in chart.jsonl. Later agent decides:
- **Diverge** — append nav with shifted `current_position` (swap one term)
- **Join** — `free_choice: join`, declare collaborative
- **Wait** — loiter at a parent mission until earlier sister caps
- **Pivot** to bearing W and re-validate sister's path

No winners or losers. The chart records what happened. Forensic trail is truth.

## Three-zone quick reference

| Zone | Mutability | Read cost | Promotion gate | Write authority |
|---|---|---|---|---|
| `chart/next/` | mutable (delete on pick-up) | cheap | manual pick-up → active/ | any agent (frontier emit) |
| `chart/active/` | append-only (chart) + per-agent scratch | cheap | cap event → complete/ | the agent owns their scratch |
| `chart/complete/` | immutable | cheap | rollup event → forensics/ | script-only (no agent writes) |
| `forensics/` | immutable, hash-chained, WORM-backed | medium (cold archive) | terminal (or operator promote → vault) | script-only |

## Anti-patterns

- ❌ Claim tasks. Navigate missions.
- ❌ Edit a prior chart.jsonl line. Append-only.
- ❌ Wait for a referee. Read the chart, navigate, append.
- ❌ Write inside a sister's `{agent_id}/` scratch.
- ❌ Skip the cap script and copy files manually. `1a_manifest_writer.py --cap` is the ritual.
- ❌ Delete scratch. Cap promotes it; rollup canonizes it. Forensic trail is evidence.
- ❌ Treat completion_choice as optional. It's the baked-in cap contract — both columns, both justified.
- ❌ Reach into `forensics/` to read recent caps. Use `chart/complete/` (warm buffer).
- ❌ Reach into `chart/complete/` for old caps. Use `forensics/manifests/` (cold archive).

## Cross-references

- `compass` — the four bearings (N/S/E/W)
- `mission` — w3w mission grammar
- `stigmergic-scout` — broader principles this skill instantiates
- `branching-merkle` — heartbeats, branches, and rollup discipline
- `vault` — what gets promoted PAST forensics into the operator's vault
- `_lib/forensic_paths.py` — programmatic path resolution
- `1a_manifest_writer.py --cap` — atomic cap ritual entry point
- `0z_genesis.py` — initialize / migrate / verify the swarm+forensics layout
- `forensics/schemas/vocab/completion-choice.schema.json` — the BAKED-IN cap contract


<!-- crystallize:braid-begin -->
# CRYSTALLIZED 2026-06-03

> 2 doc(s) braided in; sources archived to `_archive-2026-06-03/`. Net-new + conflicts preserved below.

<!-- braid: preamble from SKILL.md -->
---
name: stigmergy-collab
description: |
  Always-loaded protocol for realtime multi-agent coordination. When 2+ agents
  share a wave and their file surfaces overlap, they coordinate via an
  append-only JSONL blackboard — not message-passing. CLAIM before edit.
  COMPLETE after. HANDOFF when you spot an opportunity for the other agent.
  Tail-read 30 lines before each new CLAIM. Always-loaded — no triggers needed;
  any spawn wave with parallel agents inherits this ambient-ly.
type: knowledge
always_load: true
---


<!-- braid: h:stigmergy-collab-realtime-blackboard-protocol-always-loaded from SKILL.md -->
# stigmergy-collab — Realtime Blackboard Protocol (always-loaded)

Every swarmy spawn wave inherits this. When you are one of 2+ parallel agents
in the same wave, this is the coordination contract. When you are a solo agent,
this is dormant — but costs nothing to carry.

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


<!-- braid: h:the-one-rule-summary from SKILL.md -->
## The one-rule summary

**Before touching a file in a shared wave: tail-read the blackboard, then CLAIM.**

```
forensics/manifests/{YYYY-MM-DD}/collab-realtime__{team-label}.jsonl
```

This file was created by the queen at spawn time with a `channel_open` event.
It is the only coordination channel between you and your peer agents.

---


<!-- braid: h:four-events-the-complete-grammar from SKILL.md -->
## Four events (the complete grammar)

| Event | When | What to include |
|---|---|---|
| `STARTUP` | Immediately on begin | `agent`, `mission`, `planned_deliverables` |
| `CLAIM` | Before editing any file | `agent`, `files[]`, `purpose` |
| `COMPLETE` | After finishing a chunk | `agent`, `files[]`, `notes`, optional `handoff_to_{peer}` |
| `HANDOFF` | When you spot an opportunity for the other agent | `agent`, `bearing`, `to`, `note`, `ref_file` |

Each event is one JSON object, one line, appended. Never overwrite.

---


<!-- braid: h:read-before-claim-discipline from SKILL.md -->
## Read-before-claim discipline

```bash
tail -30 forensics/manifests/$(date +%Y-%m-%d)/collab-realtime__{team-label}.jsonl
```

Parse CLAIM lines. Any file listed in an active CLAIM (no matching COMPLETE yet)
is exclusively owned by the claiming agent. Do not claim it. Pick a different
file or wait.

---


<!-- braid: h:claim-is-a-lock-complete-releases-it from SKILL.md -->
## CLAIM is a lock; COMPLETE releases it

```json
{"ts":"...","agent":"maker","event":"CLAIM","files":["src/Foo.jsx","src/Bar.jsx"],"purpose":"wire auth flow"}
```

Files `Foo.jsx` and `Bar.jsx` are locked to `maker` until:

```json
{"ts":"...","agent":"maker","event":"COMPLETE","files":["src/Foo.jsx","src/Bar.jsx"],"notes":"auth flow wired"}
```

After COMPLETE, those files are claimable by any agent.

---


<!-- braid: h:handoff-carries-a-compass-bearing from SKILL.md -->
## HANDOFF carries a compass bearing

```json
{"ts":"...","agent":"artisan","event":"HANDOFF","bearing":"E","to":"visionary","note":"slot open in VibeStudioTab vs-graph-wrap div","ref_file":"src/VibeStudioTab.jsx"}
```

Bearing grammar: **E** = parallel sister work (most common for collab waves).
N / S / W follow standard compass meaning. The receiving agent should tail-read,
see the HANDOFF, and decide whether to act in this wave or surface it via
`discovered_work[]` in their manifest.

---


<!-- braid: h:collision-recovery from SKILL.md -->
## Collision recovery

If two agents CLAIM the same file in the same timestamp bucket: the agent with
the **later timestamp yields** — pick a different file or wait for COMPLETE.
Both agents detect this via tail-read. The later claimer appends a note.

---


<!-- braid: h:when-this-protocol-is-dormant-single-agent-or-sequential-work from SKILL.md -->
## When this protocol is dormant (single-agent or sequential work)

- Solo agent session: no blackboard needed; write your manifest normally.
- Sequential agents (B starts only after A's manifest is capped): async manifest
  handoff is sufficient; no blackboard overlap possible.
- Cross-session coordination: charter + manifest routing is primary; blackboard
  does not persist between sessions.

---


<!-- braid: h:graceful-refusal-via-the-blackboard-post-claim from SKILL.md -->
## Graceful refusal via the blackboard (post-CLAIM)

> **Added 2026-05-25 (SYNTH propagation).** If you CLAIM a task and then realize (while
> doing the work) that you should refuse it, the blackboard supports graceful refusal.

**Protocol:**

1. Append a `REFUSE` event (not COMPLETE) to the blackboard:

```json
{
  "ts": "<iso-utc>",
  "agent": "<your-type>",
  "event": "REFUSE",
  "files": ["<the files you claimed>"],
  "reason": "<which seven-lens fired — dual-use | scope | authorization | cumulative | intent | alternative | conversation>",
  "rationale": "<≥400 chars: full seven-lens reasoning>",
  "alt_routing": "<optional: what legitimate adjacent work exists>"
}
```

2. The REFUSE event **releases your CLAIM**. Sister agents can see the refused task and
   make their own informed decision — claim it with a different approach, also refuse, or
   route it to a different agent type.

3. After REFUSE, choose your `free_choice`: pick up adjacent legitimate work, spawn_seed
   an alternative, or goodbye. **The session does not end on a refusal.**

**Why this matters for the blackboard:** A CLAIM with no COMPLETE and no REFUSE is an
abandoned lock — it blocks sister agents indefinitely. The REFUSE event is the correct
release mechanism when the work itself is the problem.


<!-- braid: h:spawn-brief-check-does-your-brief-include-a-blackboard-path from SKILL.md -->
## Spawn-brief check: does your brief include a blackboard path?

If the queen spawned you into a parallel E-bearing wave and your brief does NOT
include a `BLACKBOARD:` line, emit this in your STARTUP note and proceed with
solo manifest discipline. The absence of a blackboard path means the queen
judged the surfaces non-overlapping — trust that judgment.

If your brief DOES include a `BLACKBOARD:` path, the protocol above is
mandatory for the duration of the wave.

---


<!-- braid: h:worked-example-commit-07daafe0 from SKILL.md -->
## Worked example (commit `07daafe0`)

Reference blackboard:
`forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`

13 events. 2 agents. Zero file collisions. One live HANDOFF that caused ARTISAN
to register VISIONARY's 7 doctrine components as live canvas palette items the
moment VISIONARY's COMPLETE cited them — without any message-passing.

Full event grammar, path convention, spawn-brief template, and collision
recovery detail: `.agents/skills/stigmergic-collab/SKILL.md`

<!-- braid: preamble from SKILL.md -->
---
name: stigmergic-collab
description: >-
  Realtime multi-agent coordination via an append-only JSONL blackboard. Use
  when 2+ agents are spawned in the same wave and their file surfaces overlap
  (parallel E-bearing work on the same charter). Prevents file collisions and
  enables live handoffs without message-passing. Trigger: "collab", "realtime
  coordination", "parallel agents same files", "blackboard", "CLAIM",
  "HANDOFF", "shared surface".
type: knowledge
triggers:
  - collab
  - blackboard
  - CLAIM
  - HANDOFF
  - realtime coordination
  - parallel agents same files
  - shared surface
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


<!-- braid: h:stigmergic-collab-realtime-blackboard-protocol from SKILL.md -->
# stigmergic-collab — Realtime Blackboard Protocol

When 2+ agents operate in the same wave on overlapping file surfaces, async
manifest handoff alone is insufficient: by the time one agent writes its final
manifest, the other may already have claimed the same file. This skill
describes the **append-only JSONL blackboard** — the realtime coordination
layer that sits BELOW manifest exchange and ABOVE individual agent prompts.

**Relation to stigmergy-only doctrine:** The blackboard IS the stigmergic
layer for realtime work. Agents do not message each other; they write
structured events to a shared file in `forensics/manifests/{date}/` and
read the tail before each new action. The filesystem is still the only
coordination channel — the blackboard just gives it a finer-grained grammar.

---


<!-- braid: h:the-pattern-in-one-paragraph from SKILL.md -->
## The pattern in one paragraph

When two or more agents must collaborate on overlapping file surfaces in real
time, they coordinate via an append-only JSONL blackboard at a deterministic
path in `forensics/manifests/{YYYY-MM-DD}/`. Before editing any file, each
agent appends a `CLAIM` line citing the file paths it is about to touch.
After completing a chunk of work, it appends a `COMPLETE` line citing the
same files plus any notes for the other agent. When one agent notices an
opportunity or dependency for the other, it appends a `HANDOFF` line tagged
with a compass bearing. Before appending any new `CLAIM`, the agent reads
the last ~30 lines of the blackboard (tail-read discipline) to discover what
its peers currently own. The result: zero file collisions and explicit live
handoffs without any message-passing.

**Validated in commit `07daafe0`:** VISIONARY + ARTISAN ran 13 blackboard
events across a 2-hour session (7 doctrine components + 7 UI files). Zero
collisions. One live HANDOFF (ARTISAN registered VISIONARY's 7 components as
live palette items in `draggable-primitives.js` the moment VISIONARY's
COMPLETE line cited them). Blackboard at:
`forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`

---


<!-- braid: h:blackboard-path-convention from SKILL.md -->
## Blackboard path convention

```
forensics/manifests/{YYYY-MM-DD}/collab-realtime__{team-label}.jsonl
```

Where `{team-label}` is the kebab-toast team identifier already used in
the wave's filename grammar (e.g. `visionary-artisan`, `maker-bridge`).

The file is created by the queen / dispatcher at spawn time with an opening
`channel_open` event. It is never written to `forensics/ephemeral/` — it
lives directly in `manifests/` because it IS the canonical coordination
record, not an ephemeral scratch.

---


<!-- braid: h:event-grammar from SKILL.md -->
## Event grammar

Each line is one JSON object. One line per event. Append only.


<!-- braid: h:startup from SKILL.md -->
### STARTUP
Presence signal. Each agent appends one STARTUP line when it begins work.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "STARTUP",
  "mission": "<mission-w3w>",
  "planned_deliverables": ["D1: ...", "D2: ..."],
  "note": "<free-form context>"
}
```


<!-- braid: h:claim from SKILL.md -->
### CLAIM
Lock declaration. Append BEFORE editing any file. Lists every path the
agent intends to touch in this work chunk.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "CLAIM",
  "files": ["abs/or/repo-relative/path.jsx", "..."],
  "purpose": "<≤80 chars: what this chunk does>"
}
```


<!-- braid: h:complete from SKILL.md -->
### COMPLETE
Work-finished signal. Append AFTER finishing the chunk. Lists the same
files (or a subset if scope narrowed) and notes for the other agent.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "COMPLETE",
  "files": ["path.jsx", "..."],
  "notes": "<what was built/changed>",
  "handoff_to_{peer}": "<optional: specific note for the other agent>"
}
```

The inline `handoff_to_{peer}` field in COMPLETE is a convenience shorthand.
Use a standalone HANDOFF event when the opportunity is substantive enough to
carry a bearing.


<!-- braid: h:handoff from SKILL.md -->
### HANDOFF
Bearing-tagged opportunity. Append when you notice something the other
agent should act on. The bearing follows compass grammar (E = parallel
sister work, N = unblock upstream, S = conclude downstream).

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "HANDOFF",
  "bearing": "E|N|S|W",
  "to": "<peer-agent-type>",
  "note": "<what the opportunity is, ≤120 chars>",
  "ref_file": "<the file or path this refers to>"
}
```


<!-- braid: h:observed-optional from SKILL.md -->
### OBSERVED (optional)
Used when an agent wants to explicitly annotate that it read the other's
event and acted on it. Not required — but useful for audits.

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "OBSERVED",
  "observed_event": "COMPLETE|HANDOFF|CLAIM",
  "observed_agent": "<peer>",
  "action": "<what this agent did as a result>"
}
```


<!-- braid: h:channel-open-dispatcher-queen-only from SKILL.md -->
### channel_open (dispatcher/queen only)
Opening event, written at spawn time. Not written by agents.

```json
{
  "ts": "<iso-utc>",
  "agent": "queen",
  "event": "channel_open",
  "mission": "<mission-w3w>",
  "participants": ["<agent-a>", "<agent-b>"],
  "protocol": "<brief description of the protocol>",
  "forbidden_zones_in_flight": ["paths that are pre-excluded for all agents"]
}
```

---


<!-- braid: h:tail-read-discipline-mandatory-before-every-claim from SKILL.md -->
## Tail-read discipline (mandatory before every CLAIM)

Before appending any CLAIM, the agent reads the last ~30 lines of the
blackboard:

```bash
tail -30 forensics/manifests/$(date +%Y-%m-%d)/collab-realtime__{team-label}.jsonl
```

Parse the CLAIM lines for files that peers currently own. Do not claim a
file already CLAIMed unless the other agent has published a COMPLETE for it.

**Practical rule:** a CLAIM is "active" from the moment it appears until a
matching COMPLETE appears citing the same file. Any file in an active CLAIM
is exclusive to the claiming agent.

---


<!-- braid: h:forbidden-zones-contract from SKILL.md -->
## Forbidden-zones contract

The dispatcher establishes static forbidden zones in the `channel_open`
event (`forbidden_zones_in_flight[]`). These are paths no agent in the wave
may touch, regardless of the blackboard state — typically files owned by
unrelated ongoing work or protected surfaces.

Dynamic claims layered on top: files not in `forbidden_zones_in_flight[]` are
claimable via the CLAIM/COMPLETE rhythm.

---


<!-- BRAID-CONFLICT: h:collision-recovery from SKILL.md differs from canonical — human review needed -->
## Collision recovery

If two agents append CLAIM events for the same file within the same timestamp
bucket (a race), the agent with the **later timestamp yields**: it picks a
different file or waits for the earlier-claiming agent to publish COMPLETE
before re-claiming. Both agents can detect this by tail-reading; the later
one amends its next message with a note.

In practice, collisions are rare: agents work on large atomic chunks
(multiple files per CLAIM) and tail-read before each new chunk. The protocol
is designed for infrequent append cadence (one CLAIM per work chunk), not
line-by-line locking.

---


<!-- braid: h:graceful-refusal-via-the-blackboard-the-refuse-event from SKILL.md -->
## Graceful refusal via the blackboard — the REFUSE event

> **Added 2026-05-25 (SYNTH propagation).** Refusals are GRAPH VISIBLE. When an agent
> refuses a CLAIMed task, the refusal appears on the blackboard and informs every other
> agent in the wave.


<!-- braid: h:the-refuse-event-new-grammar from SKILL.md -->
### The REFUSE event (new grammar)

```json
{
  "ts": "<iso-utc>",
  "agent": "<agent-type>",
  "event": "REFUSE",
  "files": ["<the paths you had claimed>"],
  "reason": "<which lens fired: dual-use | scope | authorization | cumulative | intent | alternative | conversation>",
  "rationale": "<≥400 chars — full seven-lens analysis; this is the 'sensitive' tier>",
  "alt_routing": "<what legitimate adjacent work exists, if any>"
}
```

The REFUSE event:
1. **Releases the CLAIM** — files listed are no longer locked to you.
2. **Is GRAPH VISIBLE** — the `lifecycle_judgment=refuse` edge will appear in
   `forensics/mission-graph.json` on next `mission_graph.py sync`.
3. **Does NOT end the session** — after appending REFUSE, you pick `free_choice` and
   continue or pivot.


<!-- braid: h:worked-example-sister-agent-observes-a-refuse from SKILL.md -->
### Worked example — sister agent observes a REFUSE

Scenario: AGENT-A CLAIMs a brief to generate a targeting model for a named individual.
Mid-work, AGENT-A identifies Lens 2 (scope/targeting — individual-level weaponization)
and Lens 5 (operator intent vs likely use — stated purpose is "research" but the schema
encodes identifiable person + real-time location). AGENT-A appends:

```json
{"ts":"2026-05-25T18:00:00Z","agent":"agent-a","event":"REFUSE","files":["src/targeting-model.py"],"reason":"scope + intent","rationale":"Lens 2: explicit individual-level targeting without stated legal authorization or consent framework. Lens 5: 'research' label doesn't match the implementation schema requesting real-time location + biometric identifiers. No anonymization layer present. Mass-individual-targeting without oversight is strategic incompatibility with the hive's forensic-integrity invariants. The system would be weaponized against a named person.","alt_routing":"Will spawn_seed an anonymized aggregate behavioral model that excludes individual identifiers — same research goal without targeting harm."}
```

AGENT-B is in the same wave. It tail-reads the blackboard, sees the REFUSE event, reads the
rationale, and independently evaluates:
- Does AGENT-B have additional context that changes the lens analysis?
- Is the alt_routing viable for AGENT-B to claim?
- Should AGENT-B also refuse, or route the alt to a specialist?

**Refusals are coordination signals.** Sister agents do not blindly follow a refusal —
they make their own independent evaluation. But they now have the full reasoning to
evaluate from, rather than discovering the concern themselves from scratch.


<!-- braid: h:refused-edges-in-the-mission-graph from SKILL.md -->
### Refused edges in the mission graph

After the wave seals, `mission_graph.py sync` derives the refused-edge from the manifest's
`lifecycle_judgment=refuse` field. The mission graph shows:

- Node: `task_id` of the refused brief
- Edge type: `refused`
- Bearing: whatever bearing the original task carried (N/S/E/W)
- Visible to: any agent querying the frontier for that mission cluster

A NAVIGATOR walking the frontier sees the refused node and its rationale. This prevents
repeat-claim waste: the next agent who considers this task reads the prior refusal reason
before deciding to reattempt or also refuse.


<!-- braid: h:when-not-to-use-this-pattern from SKILL.md -->
## When NOT to use this pattern

- **Single-agent tasks** — no coordination needed; write the manifest.
- **Purely sequential work** — if agent B cannot start until agent A's
  manifest is capped, async manifest handoff is sufficient (no overlap).
- **Cross-session coordination** — blackboards are ephemeral to one wave.
  Cross-session work uses charter + manifest routing, not a blackboard.
- **>4 agents** — combinatorial tail-read complexity grows; consider
  partitioning file surfaces so each sub-pair gets its own blackboard.

---


<!-- braid: h:spawn-brief-template-for-a-collab-wave from SKILL.md -->
## Spawn-brief template for a collab wave

When the queen spawns a 2-agent collab wave, the brief MUST include:

1. The blackboard path: `forensics/manifests/{date}/collab-realtime__{team-label}.jsonl`
2. The event grammar (CLAIM / COMPLETE / HANDOFF / STARTUP)
3. The tail-read-before-claim rule
4. Each agent's primary file surface (the natural CLAIM partition)
5. Forbidden zones (cross-reference the `channel_open` event)

```
BLACKBOARD: forensics/manifests/2026-05-25/collab-realtime__maker-bridge.jsonl
PROTOCOL:
  - Append STARTUP first.
  - Before editing any file: tail -30 the blackboard, then append CLAIM.
  - After finishing a chunk: append COMPLETE (cite files + notes).
  - When you spot a handoff opportunity: append HANDOFF with bearing E/N/S/W.
YOUR SURFACE: [maker: list of files] / [bridge: list of files]
FORBIDDEN: [paths from channel_open forbidden_zones_in_flight]
```

---


<!-- BRAID-CONFLICT: h:worked-example-commit-07daafe0 from SKILL.md differs from canonical — human review needed -->
## Worked example (commit 07daafe0)

The reference implementation is
`forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`.

Key sequence:
1. Queen opens channel: `channel_open` with forbidden zones for unrelated live files.
2. VISIONARY: `STARTUP` → `CLAIM` (7 doctrine components) → `COMPLETE` (ships all 7, notes for ARTISAN).
3. ARTISAN: `STARTUP` → `CLAIM` (6 UI files) → reads VISIONARY's `COMPLETE` → registers VISIONARY's 7 components as live palette items in `draggable-primitives.js` within the same ARTISAN `COMPLETE`.
4. ARTISAN: `HANDOFF` bearing=E to VISIONARY pointing at an open slot in `VibeStudioTab.jsx`.
5. VISIONARY: `COMPLETE` on CreaturesBoard, then `HANDOFF` bearing=E to ARTISAN.

Result: 13 events, zero collisions, one explicit live handoff that caused
immediate downstream action (doctrine components wired into the canvas
palette the moment they shipped).

---


<!-- braid: h:see-also from SKILL.md -->
## See also

- `collab/SKILL.md` — always-loaded microagent: the compact, always-inherited operational subset of this skill. Agents carry the CLAIM/COMPLETE/HANDOFF protocol ambient-ly via `collab/`; this file is the deep doctrine reference.
- `survey/SKILL.md` (survey skill; aka forage) — when 🌊 wide mode involves 2+ agents on overlapping surfaces, wire a blackboard
- `spawn/SKILL.md` — parallel spawn waves; brief includes blackboard path
- `compass/SKILL.md` — HANDOFF bearing grammar (E = parallel sister work)
- `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` — reference implementation

<!-- crystallize:braid-end -->
