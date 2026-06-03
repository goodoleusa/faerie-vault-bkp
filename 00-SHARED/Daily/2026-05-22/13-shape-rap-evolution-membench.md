---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: shape-as-measurement-substrate
status: synthesis-log
canon_candidate: true
---

# How "shape" fits into RAP, evolution, mutation assessment, and membench

User asked (verbatim):

> "how does this shape thing fit into RAP and evolution and assessing
>  mutations and membench"

The answer is structural: **shape is the measurement substrate**.
RAP, evolution, mutation assessment, and membench all become
concrete + comparable when you ground them in shape detection.
Without shapes, all three measure vague abstractions. With shapes,
every cycle is "did the count of shape X change."

## The substrate question

The mission emergence doctrine (`11-missions-as-emergent-cross-repo-shape.md`)
established that a **shape** is a recognizable pattern of work:
"stranded `@authed`", "missing frontmatter", "DelegateTool rename",
"cluster_prefix length != 3", etc.

A shape has two properties that make it ideal for measurement:

1. **Countable.** You can scan a repo (or the whole family) and
   count instances. The count is a real number.
2. **Detectable mechanically.** A shape can be expressed as an AST
   pattern, a regex, a query against forensics — no human-judgment
   bottleneck.

These two properties make shape THE measurement substrate for
everything that measures "is the system getting better."

## How shape fits RAP

**RAP (Rapid Agent Pipeline)** is the discipline of:
measure → cut → measure → log. The fast-evo five-beat heartbeat IS
RAP condensed.

**Without shape:** measure-before is vague ("the code is messy"),
measure-after is vague ("the code feels better"). The cycle is
qualitative and not comparable across runs.

**With shape:** measure-before is the count of the targeted shape;
measure-after is the count after the cut. The delta is a real number.

| RAP phase | Without shape | With shape |
|---|---|---|
| MEASURE BEFORE | "we have too many tools" | shape `mcp.tools.granular` → 85 instances |
| CUT | "consolidate some" | apply consolidation protocol; trace which 10 absorbed into dispatchers |
| MEASURE AFTER | "feels better" | shape `mcp.tools.granular` → 75 instances; delta = −10 (12% reduction) |
| LOG | "shipped wave 1" | `_evolution_log[]` entry: shape, baseline=85, new_state=75, delta=−10, verdict=beneficial |

The whole session's discipline becomes auditable because every cut
has a numeric baseline + numeric new state + numeric delta against
a NAMED SHAPE.

## How shape fits evolution

**Evolution** in swarmy is the long-running pressure to improve the
system via mutation × selection. The genetic-drift charter
(`forensics/charters/active/70-genetic-drift...` lineage) gives the
framework.

**Without shape:** a "mutation" is anything that changes the system.
You can't tell if it's an improvement or a side step.

**With shape:** every shape has a TARGET DIRECTION (count should
trend down, OR count should stay bounded, OR count should grow if
the shape is "tests added"). A mutation is **classified** by what
it does to its targeted shape's count:

- `beneficial` — shape count moved in target direction
- `neutral` — no measurable change
- `harmful` — shape count moved against target direction
- `uncertain` — shape detection couldn't measure (skip; mark for follow-up)

Over time, a SHAPE accumulates a **mutation history**:

```
shape: mcp.tools.granular  (target: decreasing)
  2026-05-22T11:00  count=85  (baseline)
  2026-05-22T12:30  count=75  (mutation: wave-1; verdict=beneficial)
  2026-05-22T15:00  count=?   (mutation: wave-2 in flight; pending verdict)
```

This is real evolution — measured pressure, tracked mutations,
classified outcomes. Without shapes, it's vibes.

## How shape fits mutation assessment

Mutation assessment is the question: **was this change good?**

Today's `_evolution_log[]` entries already classify
beneficial/neutral/harmful/uncertain — but the classification is
loose without a shape to compare against.

**Shape-based assessment:**

For each cut:
1. Identify the SHAPE the cut intends to affect
2. Capture baseline shape count
3. Apply the cut
4. Capture new shape count
5. Verdict:
   - target_direction_aligned + significant delta → beneficial
   - delta within noise threshold → neutral
   - target_direction_violated + significant delta → harmful
   - shape detection failed → uncertain

The `_evolution_log[]` entry becomes:

```json
{
  "cut": 3,
  "shape": "mcp.tools.granular",
  "shape_detector": "scripts/audit-mcp-tool-count.py",
  "baseline": {"count": 85, "ts": "..."},
  "new_state": {"count": 75, "ts": "..."},
  "delta": -10,
  "target_direction": "decreasing",
  "verdict": "beneficial",
  "verdict_confidence": 0.95,
  "lineage": "ed25519:..."
}
```

The forensic trail becomes a real ledger of measured progress, not a
diary.

## How shape fits membench

**Membench** (the membench harness — `scripts/3x_membench_probes.py`)
runs periodic probes that score the system's memory + reasoning
quality. Each probe returns a number.

The connection: **a membench probe IS a shape detector at the
quality layer.**

| Membench probe | Underlying shape |
|---|---|
| Can-I-find-prior-decisions | "decisions discoverable in COC" |
| Onboarding-time-to-first-action | "newcomer can act within N minutes" |
| Frontier-scan-latency | "agent can grok recent work in <30s" |
| Charter-orientation-cold | "60-second test passes for any charter" |
| Manifest-signature-coverage | "% manifests signed (rolling)" |

Each probe = a shape. Each shape has a target count. Each membench
run measures the count. Probes that trend in the right direction =
system is healthy. Probes that regress = a harmful mutation slipped
through.

The new `lint-manifest-signing.sh` IS a membench probe under the
hood — it returns rc=1 when the "% recent manifests with
signed_by + signer" shape's count is below threshold.

## The integration matrix

| Surface | Shape's role | Concrete artifact |
|---|---|---|
| **RAP / fast-evo** | Beat 1 + Beat 3 measure against a named shape | `_evolution_log[]` entries cite shape + baseline + new_state |
| **Evolution / mutation pressure** | Target-direction + verdict classification | `_evolution_log[].verdict ∈ {beneficial, neutral, harmful, uncertain}` |
| **Mutation assessment** | The verdict logic IS shape-direction comparison | `9x_membench_scorer.py` produces verdicts |
| **Membench** | Each probe = a shape detector at quality layer | `forensics/eval/membench/{date}/probe-{name}.json` |
| **Cross-repo mission** | The shape is what propagates; not the specific code | Cluster_prefix-as-address + shape's detector = cross-repo applicable |
| **Charter claim** | A claim is valid when charter goal aligns with shape's target-direction | `claimed_missions[].claim_rationale` cites the shape alignment |

## The missing piece: shape registry

Today shapes are implicit. A `_meta/shapes.json` (or
`_meta/shape-registry/{slug}.json` per shape) would make them
first-class:

```json
{
  "shape_id": "mcp.tools.granular",
  "cluster_prefix": ["mcp", "tools", "granular"],
  "description": "MCP tools that should be verb-dispatcher-merged",
  "target_direction": "decreasing",
  "detector_script": "scripts/audit-mcp-tool-count.py",
  "membench_probe": true,
  "applicable_repos": ["faerie2", "swarmy-hive-plugin"],
  "current_count": 75,
  "history": [
    {"ts": "2026-05-22T11:00:00Z", "count": 85, "mutation": null},
    {"ts": "2026-05-22T12:30:00Z", "count": 75, "mutation": "wave-1"}
  ]
}
```

With a shape registry, every cut KNOWS its target shape. The
membench harness reads the registry to compute health. The
cross-repo propagation reads `applicable_repos[]`. The mutation
log writes verdicts grounded in shape-target alignment.

**Today this doesn't exist.** Open enhancement. Highest leverage:
shape-registry + retroactive backfill for the ~10 shapes already
implicit in the codebase. Once the registry exists, RAP / evolution
/ mutation / membench all align.

## Single-line summary

**Shape is the measurement substrate. Without shapes, RAP /
evolution / mutation / membench measure vibes. With shapes, every
cycle becomes "did the count of shape X move in its target direction"
— a real number, comparable across runs, valid for cross-repo
propagation, and the basis for honest mutation classification.**

---

*Completes the 6-doctrine arc (08-13) that fully articulates the
mission + charter + shape + measurement system. Open enhancement:
shape registry at `_meta/shapes.json` to make implicit shapes
first-class. Should fold into Part 5 of
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` (or its own
canonical doc once the registry exists).*
