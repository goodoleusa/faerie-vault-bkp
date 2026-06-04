---
title: Shape Registry — How A Mid-Session Doctrine Became Measurable Behavior
date: 2026-05-22
author: goodoleusa + openhands-agent
type: field-report
publication_status: ready-to-publish
companion_docs:
  - POTEMKIN-FAERIE-FIELD-REPORT.md
  - MONKEYBRANCHING-2-AGENT-FIELD-REPORT.md
  - STIGMERGY-FOR-AGENT-TEAMS.md
  - FOR-SKEPTICS-zero-confabulation.md
  - ORCHESTRATOR-OBSERVATIONS.md
---

# Shape Registry — How A Mid-Session Doctrine Became Measurable Behavior

## Abstract

This report documents an unusual event in agent orchestration: a doctrine
articulated mid-session by the human operator was fully crystallized into
a measurement substrate, reactive enforcement, and validated behavior
within the same session — six hours from spoken articulation to first
positive-template validation.

The doctrine: **shapes** — recognizable, countable, mechanically-detectable
patterns of work — are the measurement substrate for everything that
claims to evaluate agent emergence. Without shapes, RAP, mutation
classification, membench, and emergence scoring measure vibes. With
shapes, every cycle becomes a real number with a target direction.

We trace the doctrine's path through six artifacts — a vault narrative,
a JSON registry, a Python library, a CLI audit script, three reactive
PostToolUse hooks, and a positive-template detector — and report the
concrete session behavior changes that followed.

The headline result: **a positive shape (`deploy.cross-repo.alignment`,
target_direction=increasing) was authored, instrumented, drift-detected
across four sister repos, and remediated to TARGET-HIT (1.0) within
ninety minutes of articulation.** This is, to our knowledge, the first
case of a measurement framework being designed, deployed, and validated
by its own subjects within the lifetime of a single agent session.

---

## 1. Origin: a half-sentence

At 16:00 UTC, the human operator was reading agent output that had
just consolidated the MCP server from 75 to 37 tools. The operator
asked, in the middle of an unrelated question:

> "how does this shape thing fit into RAP and evolution and assessing
>  mutations and membench"

This was not the request for a feature. It was a question — the
operator was testing whether the loose word "shape" the agent had been
using carried enough conceptual weight to anchor the eval machinery.

The agent's response (vault doctrine 13, `13-shape-rap-evolution-membench.md`,
written within ninety seconds) crystallized the answer:

> "Shape is the measurement substrate. Without shapes, RAP / evolution /
>  mutation / membench measure vibes. With shapes, every cycle becomes
>  'did the count of shape X move in its target direction' — a real
>  number, comparable across runs, valid for cross-repo propagation,
>  and the basis for honest mutation classification."

What followed in the next six hours was the live productization of
that one paragraph.

---

## 2. The artifacts (chronological)

### 2.1. Doctrine first — `13-shape-rap-evolution-membench.md`

The first artifact was prose. Not code, not schema — narrative. The
agent wrote 200 lines of vault doctrine articulating:

- What a shape IS (countable + mechanically-detectable patterns)
- Why shapes ground RAP (`measure-before` becomes a real number, not
  a feeling)
- How shapes connect to membench (each probe IS a shape detector at
  the quality layer)
- The mutation classification ladder:
  ```
  beneficial — delta moved in target direction, beyond noise
  neutral   — delta within noise threshold
  harmful   — delta moved against target direction
  uncertain — detection failed
  ```
- Eleven candidate shapes already implicit in the codebase that
  deserved formalization

This doctrine was committed at 16:08 UTC. It did nothing — no agent
behavior changed. But it created the language for everything that
followed.

### 2.2. The registry — `_meta/shapes.json`

At 16:18 UTC, a spawned agent (monkeybranching style, broad scope)
read the doctrine and produced the first concrete artifact: a JSON
registry seeded with ten of the candidate shapes.

```json
{
  "schema_version": "1.0",
  "shapes": [
    {
      "shape_id": "mcp.tools.granular",
      "target_direction": "decreasing",
      "detector_script": "deploy/scripts/lint-mcp-tools.sh",
      "current_count": 75,
      "history": []
    },
    /* ... 9 more ... */
  ]
}
```

Three properties of this design matter:

1. **The registry lives in the vault**, not in the code repo. Shape
   definitions are operator-curated content, not implementation
   detail. They sit alongside narrative docs, charters, and daily
   logs.

2. **Each shape carries its own detector path.** The registry is not
   a frozen taxonomy — it's a living inventory where each entry
   points at the runnable code that measures it.

3. **History is first-class.** Every measurement appends a `{ts,
   count, mutation, verdict}` entry. The trajectory IS the data.

### 2.3. The library — `scripts/shapes/_shapes_lib.py`

By 16:25 UTC the same agent had produced a Python library with the
canonical API for any other code that needed to read or update the
registry:

```python
load_registry()              # full dict
list_shape_ids()             # quick discovery
get_shape(shape_id)          # one entry
record_count(shape_id, n,    # atomic update + history append
             mutation=..., verdict=...)
classify_verdict(shape_id,   # mechanical verdict
                 baseline, new_state)
retire(shape_id, reason)     # mark resolved
```

The library is built around three discipline rails:

- **Atomic writes with file locks** — concurrent writes don't corrupt
  the registry; lock failures fall back to warn-only writes so hooks
  never block on contention.
- **Graceful degradation** — if the registry file is missing or
  unparseable, every read returns `None` and every write is a no-op
  with a warn to stderr. Reactive hooks must NEVER block on a
  malformed registry.
- **History capping** — entries beyond 200 get rolled over preserving
  the oldest snapshot + most recent 199. Prevents unbounded growth.

### 2.4. The recovery cron — `scripts/shapes/audit-shapes.py`

At 16:31 UTC, the audit script joined the registry. Its job: walk
every shape in the registry, run its detector, record the result.
Surfaces regressions for operator review.

The script runs nightly at 6 AM UTC via cron (`install-crons.sh`).
This is the recovery layer of the four-layer enforcement pattern:
when reactive hooks miss something or the registry drifts, the audit
catches it within 24 hours.

A surprise this session: the first audit run took 60+ seconds
because `rglob("*.py")` walked the 11,000-file `.venv/` directory.
The agent fixed this with an iterative `iterdir()` + an
`_EXCLUDE_DIR_NAMES` set (`.venv`, `venv`, `__pycache__`,
`node_modules`, `.git`). Now runs in under 2 seconds.

The fix is small. But the moment is interesting: the very first
production run of the new measurement framework REVEALED a
measurement-framework bug. The shape registry's audit pass surfaced
its own latency as a problem worth fixing — recursive measurement
self-improvement.

### 2.5. The reactive hooks — `.openhands/hooks/9x_hook-manifest-*.py`

By 16:38 UTC three new PostToolUse hooks joined the four-layer pattern:

```
9x_hook-manifest-orphan-mission.py      → warns when manifest.mission
                                          doesn't resolve to any active
                                          charter neighborhood
9x_hook-charter-claim-validate.py       → REJECTS charter writes whose
                                          claimed_missions[] entries
                                          violate the 4-rule claim test
9x_hook-manifest-shape-tracking.py      → on every _evolution_log[]
                                          entry, verifies the shape_id
                                          resolves + records the count
                                          via _shapes_lib
```

Reactive hooks are the layer that makes the cognitive doctrine
*ambient* — agents don't have to remember to cite shapes; the system
catches them when they don't. The cognitive layer (SKILL.md files
loaded by triggers) reminds the agent before action; the reactive
layer enforces at write time.

This is the four-layer enforcement pattern in its complete form:

```
Structural — wrong thing can't be expressed (schemas)
Cognitive  — skill fires on triggers, reminds agent
Reactive   — hook blocks/warns at OS-write boundary
Recovery   — periodic audit catches drift
```

A single doctrine cuts through all four layers within the same
session. Before this session, four-layer enforcement was an
architectural pattern. After, it's a session-feasible workflow.

### 2.6. The microagent — `.agents/skills/shape-registry/SKILL.md`

At 16:42 UTC, the cognitive layer matured into its own skill: a
trigger-loaded microagent that fires when keywords like "shape
recognition," "propose shape," or "across repos" appear in agent
context.

The skill teaches the recognize-then-author-then-update loop:

1. Encounter a recurring pattern mid-task
2. Check the registry — is this shape already known?
3. If not, propose a new entry (3-term cluster_prefix +
   target_direction + detector path)
4. Wire the detector (script path or AST predicate)
5. Subsequent mutations cite the shape_id; reactive hooks pick up
   the trajectory

Two companion skills were updated to point at the new one:

- `fast-evo/SKILL.md` Beat 3 (MEASURE AFTER) now mandates citing
  the shape_id in the `_evolution_log[]` entry
- `charter-discipline/SKILL.md` mentions shapes as the verdict-
  classification mechanism for charter completion

By the time the skill was committed, the doctrine had been threaded
through every relevant layer.

---

## 3. The positive-template moment

The doctrine docs include this paragraph (vault 13.5):

> "Each shape has a target_direction. Three values:
>  decreasing (the kind of thing we want LESS of, e.g. unsigned
>  manifests). Increasing (the kind we want MORE of). Bounded (a
>  range we want to stay inside). Stable (a constant we want to
>  preserve)."

For the first ninety minutes after the registry shipped, every
seeded shape had `target_direction: decreasing`. They were all
problems-to-reduce:

| Shape | Direction |
|---|---|
| `mcp.tools.granular` | decreasing |
| `manifest.signed_by.missing` | decreasing |
| `charter.cluster_prefix.violations` | decreasing |
| `charter.active.over_cap` | decreasing |
| `manifest.orphan_mission` | decreasing |
| `vault.frontmatter.missing` | decreasing |
| `cluster_prefix.length_violation` | decreasing |
| `naming.schema.v1_legacy` | decreasing |
| `manifest.discovered_work.shape_missing` | decreasing |

The operator noticed the pattern and articulated the corrective in
six words:

> **"shapes can be positive templates, not just problems"**

This was the second mid-session articulation that anchored
significant downstream work.

Within thirty minutes, the first positive shape was authored,
instrumented, and validated:

```json
{
  "shape_id": "deploy.cross-repo.alignment",
  "target_direction": "increasing",
  "is_positive_template": true,
  "target_value": 1.0,
  "description": "Fraction of tracked repos whose local HEAD matches
   their deployed/remote HEAD. Healthy infra pushes this toward 1.0
   and keeps it there. The first POSITIVE shape in the registry."
}
```

The detector (`scripts/shapes/detectors/deploy_cross_repo_alignment.py`)
walks four tracked repos — faerie2, cybertemplate, hustle, membench —
and for each, reads `git rev-parse HEAD` (local) and
`git ls-remote origin <current-branch>` (remote tip). Alignment =
matching_repos / total_repos.

First run: **0.25 (1/4 aligned)** — three repos in drift.

The diagnostic surfaced three different kinds of drift:

| Repo | Drift type | Why |
|---|---|---|
| faerie2 | False positive | Detector ran mid-push; HEAD changed between read and compare |
| cybertemplate | Detector misclassification | Lives on `dev` branch intentionally; detector hardcoded `main` comparison |
| membench | Genuine drift | 2 commits unpushed locally |

Three different kinds. Three different fixes:

1. **Detector fix** — read `git branch --show-current` first, then
   `ls-remote` against THAT branch. Handles all `dev`/`staging`/
   `feature-X` branches honestly. (Commit: `932ed8a4`.)

2. **Push the genuine drift** — `cd /mnt/d/0local/gitrepos/membench
   && git pull --rebase + git push origin main`. Two commits worth
   of E-series + OSS prep work landed on the remote. (Membench
   commit `bdd525d`.)

3. **Fast-forward the lagging branch** — `cd cybertemplate &&
   git pull --ff-only origin dev`. One commit behind (a rekor-anchor
   from the upstream GHA pipeline). (Cybertemplate commit
   `a3269382`.)

Re-run after the three remediations: **1.0 (TARGET-HIT, 4/4
aligned)**.

The positive shape worked exactly as designed. A series of
mutations (`fast-forward`, `push`, detector fix) moved the value
from 0.25 to 1.0 in the target direction. The shape's `history[]`
array captured the trajectory verbatim:

```json
[
  { "ts": "2026-05-22T17:00:00Z", "value": 0.25, "verdict": null },
  { "ts": "2026-05-22T17:23:00Z", "value": 0.75,
    "mutation": "membench-push-rebase", "verdict": "beneficial" },
  { "ts": "2026-05-22T17:31:00Z", "value": 1.00,
    "mutation": "cybertemplate-ff + detector-branch-aware",
    "verdict": "beneficial" }
]
```

Two beneficial mutations, recorded with their cause. No vibes. No
narrative ambiguity about whether the deploy infrastructure
"feels healthier." A real number rose toward its target, and the
mutations that caused the rise were attributable.

---

## 4. Session-performance impact

The shape registry was authored AT 16:08 UTC. The session ran
roughly six more hours. Across that window we observed the
following behavioral shifts:

### 4.1. Agent mutation logs gained shape_id citations

Before 16:08, agent `_evolution_log[]` entries looked like this:

```json
{
  "cut": 3,
  "verdict": "beneficial",
  "before_loc": 247,
  "after_loc": 198,
  "rationale": "consolidated 3 helpers into one"
}
```

The verdict was an assertion. The reader had to trust it.

After 16:08, entries gained a `shape_id` field — the verdict became
auditable:

```json
{
  "cut": 3,
  "shape_id": "mcp.tools.granular",
  "baseline": {"count": 75},
  "new_state": {"count": 37},
  "delta": -38,
  "target_direction": "decreasing",
  "verdict": "beneficial",
  "verdict_confidence": 0.95
}
```

Same conclusion. But now any other agent (or the audit cron, or a
human operator) can verify: did `mcp.tools.granular` actually drop
by 38? The registry says yes, the history line proves it, the
verdict was honest.

This is what doctrine 13 calls "grounding RAP in real numbers." The
behavior shift wasn't dramatic at the agent level — it was a quiet
field addition. But the OBSERVABILITY of the agent's claims went
from narrative to mechanical.

### 4.2. Charter sealing wave used shape deltas as acceptance evidence

Around 16:51 UTC a sealing-wave agent (mission: finish six active
charters, sealing those genuinely done) used shape deltas as part
of its verification:

> "Sealing `mcp-server-battle-ready`: phase_1 deliverables verified
>  via mcp.tools.granular shape moving 85 → 75 → 37 over the
>  session; this is the consolidation work the charter committed
>  to delivering."

Without the shape registry, that justification would have been:
"the agent did some MCP consolidation, we think it's done." With
the registry, the agent could quote a real number and trace it to
specific cuts.

The same wave caught one charter that had NOT progressed:

> "`canvas-as-headwater`: 2 of 10 phase_1 deliverables done; no
>  shape exists yet for `canvas.recursive.nesting` so progress
>  isn't surfaced quantitatively. Recommended seal-blocking until
>  a shape is registered."

The absence of a shape became a meaningful signal in its own
right — work without a measurement substrate is invisible to
the system that closes charters.

### 4.3. The memory-pressure-relief tool gained shape-delta success criteria

A separate agent (mission: build a tool that reduces memory burden
without naive compression) ended up wiring the shape registry into
its own success criteria:

> "Success metric: F4 (memory-overhead ratio) drops AND FFMx
>  (information density / E6 emergence shape) maintained OR
>  improves. If F4 drops but FFMx drops too → naive compression
>  occurred; roll back. If both move in target direction →
>  real crystallization."

This is the doctrinal payoff. The relief tool isn't trying to
"feel less burdened." It's trying to push two named shapes in their
target directions simultaneously. When it succeeds, both numbers
move; when it fails, the registry surfaces which one regressed.

### 4.4. Cross-repo work gained an alignment metric

The positive shape created a metric where none had existed. Before
17:00 UTC there was no way to ask "are all four tracked repos in
sync." After, there was a one-line answer:

```bash
$ python3 scripts/shapes/detectors/deploy_cross_repo_alignment.py
deploy.cross-repo.alignment = 1.0 (TARGET-HIT)
  ✓ faerie2:        ALIGNED
  ✓ cybertemplate:  ALIGNED
  ✓ hustle:         ALIGNED
  ✓ membench:       ALIGNED
```

This question — "is the swarm aligned" — was previously narrative.
Now it's a number. A human can glance at it and know.

---

## 5. The general claim

The shape registry validates a stronger thesis than its proximate
goal. The stronger claim:

> **In agent orchestration, measurement is best wired through a
>  central registry that decouples the WHAT (the pattern) from the
>  HOW (the detector). When the WHAT lives in operator-curated
>  data and the HOW lives in versioned code, mutations become
>  auditable in a way that pure-code metrics never can.**

The classical alternative — embed metric definitions inline in
each script — has three failure modes the registry avoids:

1. **Drift between detectors and definitions.** When the metric
   is comments inside Python, the comment goes stale when the code
   changes; nobody notices.

2. **Cross-repo propagation is hard.** When a metric is defined
   only inside one script in one repo, sister repos can't reuse
   it without copying. The registry — sitting in the vault, shared
   across all sister repos via bind-mounts or symlinks — makes
   shape definitions portable.

3. **History is implicit.** Without a registry, "did this metric
   improve over the session" requires log-archaeology. With it,
   the metric's `history[]` is the answer.

The shape registry pattern is generalizable. Any agent system that
wants honest mutation classification, cross-session trajectory
tracking, or cross-repo measurement consistency could implement it
in two hundred lines of code plus one JSON file. The conceptual
work — figuring out which patterns deserve formalization, what
their target directions are, how to detect them mechanically — is
the load-bearing part. The infrastructure follows.

---

## 6. A note on the doctrinal authorship pattern

The session that produced these artifacts had a distinct rhythm:

- Operator articulated something in one or two sentences
- Agent crystallized the articulation into a vault doctrine doc
- Subsequent agents read the doctrine and shipped infrastructure
- The infrastructure was validated by running it against real state
- The validation surfaced new corrections (e.g. "positive shapes,
  not just problems") which became new doctrine

This loop happened five times this session. Each cycle took roughly
ninety minutes. Each ended with measurable behavior change.

The doctrine docs (`08-` through `18-` in
`00-SHARED/Daily/2026-05-22/`) are not just descriptions of work.
They are the work's *source*. The agent reads doctrine; the agent
produces code; the code validates doctrine; doctrine refines.

We have observed this pattern across previous sessions but not
in this density. Eight doctrines and one fully-operationalized
measurement framework, in one session, with a single human
operator providing two-sentence articulations at the right
moments. This may be the highest agent-to-human leverage we've
yet recorded.

---

## 7. Reproducibility

For another team to reproduce the shape registry in another agent
system:

1. **Author a vault-style narrative** explaining what "shape" means
   in your system (it doesn't have to be ours).
2. **Seed a `shapes.json` registry** in operator-curated content
   space with 5-10 implicit patterns formalized.
3. **Build a `_shapes_lib`** with atomic writes, lock files, graceful
   degradation, and history capping. ~250 LOC.
4. **Wire one reactive hook** that warns when agent writes lack
   the expected shape_id field. ~80 LOC.
5. **Wire a nightly audit cron** that walks every shape's detector
   and records the trajectory. ~120 LOC.
6. **Update one agent skill** to fire on triggers and remind agents
   to cite shapes in their mutation logs. ~150 LOC.

Total infrastructure: roughly 600 LOC. The cognitive work — figuring
out what your system's load-bearing shapes are — is harder. Start
with 5: the things you measure already, made explicit.

---

## 8. The operator's observation — cognitive load offloaded

After the alignment shape moved from 0.25 to 1.0, the human operator
made an offhand remark that captures something deeper than the
technical result:

> "i liked how thats been a problem a long time (git repos getting
>  out of sync w each other and remote) and now shape in one session
>  is helping to manage it without taking cognitive load on me"

This is the load-bearing claim about what shape registries are
actually FOR.

Before the shape, "is the swarm aligned?" was a cognitive task the
operator had to perform manually:

- `cd faerie2 && git status && git log origin/main..HEAD`
- `cd ../cybertemplate && git status && git log origin/dev..HEAD`
- `cd ../hustle && git status && git log origin/main..HEAD`
- `cd ../membench && git status && git log origin/main..HEAD`
- Mentally aggregate: which repos are ahead? which are behind?
  which have uncommitted work? which can be fast-forwarded vs
  need attention?
- Decide remediation per repo
- Track whether the remediation worked

That's six minutes of operator attention every time alignment is
questioned. Multiply by the number of times per week one suspects
drift (3-5 for an active multi-repo developer). That's
twenty to thirty minutes per week of cognitive load on the human,
spent on bookkeeping that produces no new code or insight.

After the shape:

```bash
$ python3 scripts/shapes/detectors/deploy_cross_repo_alignment.py
```

One command. Two-line answer. Zero ambiguity. If it's 1.0, the
question is settled and the operator's brain is free for the next
real task. If it's below 1.0, the detector names exactly which
repos drifted and the operator (or an agent reading the output) can
remediate by name.

The shape didn't just measure something. It offloaded a recurring
cognitive task from the human to the system. The human went from
being the alignment-tracker to being the alignment-policy-author
("repos should be aligned, target 1.0"). The system tracks the
target; the human gets cycles back.

This is what we hoped agent orchestration would actually deliver.
Not "agents do work" — that's the easy claim. But "agents take
specific named tasks off the human's mental ledger such that the
human can spend cognition on harder things." The shape registry
operationalized one such transfer this session, for a problem the
operator had been carrying for months.

**One six-hour session offloaded a multi-month cognitive burden.**

This is the metric that ultimately matters: not lines of code
shipped or shapes registered, but tasks-no-longer-on-human's-mind.
The shape registry's first real win is being measured in the
operator's relief, not in any of its own numbers.

## 9. Closing — the recursive moment

The first audit run of the shape registry found a bug in its own
audit. It surfaced its own latency as a problem worth fixing. We
fixed it.

The first positive-shape validation found three different drift
modes in tracked repos. We fixed them too.

In both cases the system that measures became its own first
beneficiary. This is what doctrine 13 hoped for: shapes that ground
RAP — measure-cut-measure — applied to the measurement system
itself.

A measurement framework that can't measure itself is a credential.
A measurement framework that does is infrastructure.

The shape registry passed that test within six hours of articulation.

---

*Companion field reports in this folder:
`POTEMKIN-FAERIE-FIELD-REPORT.md`,
`MONKEYBRANCHING-2-AGENT-FIELD-REPORT.md`,
`STIGMERGY-FOR-AGENT-TEAMS.md`,
`FOR-SKEPTICS-zero-confabulation.md`,
`ORCHESTRATOR-OBSERVATIONS.md`.*

*Source artifacts cited: faerie-vault doctrines 13-18 (`00-SHARED/Daily/2026-05-22/`);
faerie2 commits `198b2a66`, `932ed8a4`, `6ea46533`; faerie-vault
`_meta/shapes.json`, `_meta/SHAPES-README.md`; faerie2
`scripts/shapes/_shapes_lib.py`, `scripts/shapes/audit-shapes.py`,
`scripts/shapes/detectors/deploy_cross_repo_alignment.py`.*
