---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: distress-signal-protocol
status: synthesis-log
canon_candidate: true
---

# Stigmergic distress signals — when agents hit dead ends, they call for scouts

User stated (verbatim):

> "sometimes agents might finish, sometimes they might run into a
>  dead end or some error and throw up a stigmergic distress signal..
>  the idea is if agent is hitting a snag they shld create an emergency
>  bundle to pass off to whichever scout picks up the signal and rather
>  than just ignoring failures we go explore them and see what the
>  commotion was about"

This completes the agent lifecycle. Today we handle two endings:

1. **Success** — manifest with `completion_choice.kind in {promote,
   seal, verify, ...}`. Becomes part of the charter's accretion.

2. **Failure** — error / dead end. Agent throws, gets logged
   somewhere unstructured, swarm ignores it. **The failure is lost.**

This doctrine adds a third ending:

3. **Distress** — agent hits a snag, writes a structured **emergency
   bundle**, drops it stigmergically. Future scouts that pick up the
   signal investigate. Failures become exploration substrate, not
   garbage.

## Why this matters

A failure is a measurement just like a success — it tells you the
shape of the territory. Today's swarm ignores failures, so:

- The same dead end gets re-discovered repeatedly by new agents
  (no memory of "we tried this; here's what blocked")
- Patterns of failure don't compound into systemic insight
- The hardest problems (the ones that block agents) are exactly the
  ones we DON'T learn from
- Operators only see failures when they grep logs by hand

Stigmergy is supposed to mean "agents leave markers; other agents
read them and coordinate without messages." Right now the markers
for SUCCESS are clean (manifests, COC, charters); the markers for
DISTRESS are missing.

## The distress bundle — what it carries

An emergency bundle is an artifact written by an agent that knows
it's blocked, sized roughly like a manifest but with different
semantics (it's a question, not a deliverable).

Canonical filename:
```
forensics/ephemeral/{YYYY-MM-DD}/{YYYYMMDD}T{HHMMSS}Z__distress__{mission.w3w}__{slug}_{agent}.json
```

Note the type marker `__distress__` (vs `__manifest__` for normal
work, `__charter__` for charters). Greppable across the forensics
tree — `ls forensics/ephemeral/{date}/*__distress__*` surfaces every
open distress signal of the day.

### Body shape

```json
{
  "kind": "distress",
  "ts": "2026-05-22T17:42:00Z",
  "agent": {
    "agent_type": "maker",
    "session_id": "abc12345",
    "pubkey": "ed25519:...",
    "signer": "maker"
  },
  "mission": "doctrine.coverage.audit",
  "initial_bearing": "N",
  "bearing_at_distress": "W",
  "bearing_trajectory": [...],

  "block": {
    "kind": "error | dead-end | scope-explosion | conflict | unknown",
    "title": "manifest writer can't extract created_ts from sealed charters",
    "exception_class": "KeyError",
    "exception_detail": "'first_signed' missing from coc_chain in 8 of 24 charters",
    "blocking_artifact": "scripts/_charter_lib.py:line-167",
    "tried": [
      "fallback to file mtime",
      "extract from coc.jsonl trailing entry",
      "extract from first manifests_received[]"
    ],
    "tried_but_failed_why": [
      "mtime drifts after git checkout",
      "coc.jsonl entries don't all reference charters",
      "manifests_received[] is sparsely populated today"
    ]
  },

  "context_dump": {
    "recent_reads": ["scripts/_charter_lib.py", "forensics/charters/active/*.json"],
    "recent_writes": ["20260522T163000Z__manifest__...__layer-retrofit-01_maker.json"],
    "open_files_or_dirs_consulted": [...],
    "frontier_snapshot": "13 active charters, 5 of which have null created_ts"
  },

  "hypothesis": [
    {
      "guess": "created_ts was never populated on charters created pre-2026-04",
      "evidence_path": "git log --oneline forensics/charters/ | grep 2026-04",
      "confidence": 0.6
    },
    {
      "guess": "manual charter writes (not via _charter_lib) skipped the field",
      "evidence_path": "any charter without coc_chain.entry_hash",
      "confidence": 0.3
    }
  ],

  "ask_of_scout": "Determine ground-truth source for created_ts on legacy charters. Options: (a) accept null + fallback to file mtime, (b) backfill via git log of first commit, (c) add migration step on next charter sweep.",

  "next_bearing_suggestions": ["W", "N"],
  "blocking_priority": "medium | high | critical",
  "would_unblock": ["four-layer-retrofit", "charter-accretion-rollout"],

  "coc_chain": { ... canonical chain block ... }
}
```

### Why structured

The bundle's structure makes it RESCUABLE. A scout reading the
file knows immediately:
- What was tried (no duplicate-effort waste)
- What the agent hypothesizes (no re-deriving)
- What kind of help is needed (`ask_of_scout`)
- Where to look (`context_dump.recent_reads`)
- What unblocks next (`would_unblock`)

A scout with this much context can usually resolve in minutes,
whereas a scout starting from "the previous agent errored" would
take an hour to reconstruct the same state.

## The scout pattern

A scout is an agent (or behavior) that walks the day's distress
folder and picks up signals:

```python
distress_signals = glob("forensics/ephemeral/{today}/*__distress__*.json")
distress_signals.sort(key=oldest_first)  # FIFO; rescue older first

for d in distress_signals:
    bundle = json.load(open(d))

    if already_being_investigated(bundle):
        continue  # another scout has it

    claim(bundle)  # write a sibling file marking 'claimed by <my-pubkey>'
    investigate(bundle)
    # → either resolves (writes a normal manifest cross-citing the bundle)
    # → or escalates (writes a new distress bundle marked 'escalated-from')
```

Scout discipline:

1. **Read the full bundle before acting.** The previous agent
   already tried things; don't redo them. Address what they
   asked of the scout (the `ask_of_scout` field).

2. **Cite the distress bundle in your manifest.** When you resolve
   it, your manifest gets a `resolved_distress[]` field pointing at
   the bundle file. The bundle's `claimed_ts` + `resolved_ts` make
   the rescue trajectory replayable.

3. **Mark explicitly** if you fail too. If you can't resolve, write
   YOUR own distress bundle citing the prior one (`escalated_from`).
   Don't let signals die silently.

4. **Don't engage on critical signals if you lack capacity.** A
   distress bundle marked `blocking_priority: critical` may need a
   different archetype (DEEP_DIVER for analysis, NAVIGATOR for path
   rerouting). Match capacity to need.

## The four-layer enforcement

### Structural

`forensics/schemas/shape/distress-bundle.schema.json` defines the
required fields. The writer rejects malformed bundles.

### Cognitive

NEW `.agents/skills/distress-signaling/SKILL.md` teaches BOTH sides:

> Triggers (write side): "stuck", "dead end", "blocked", "can't
> figure out", "error keeps recurring", "tried everything".
>
> Triggers (scout side): "frontier scan", "look for distress",
> "rescue", "what's blocking", "investigate failure".
>
> When the agent recognizes a write-side trigger in its own
> reasoning: STOP. Don't grind. Write the distress bundle. Drop
> it. End the session with completion_choice=`distress` (NEW
> kind — extends the 6-choices ritual to 7).

### Reactive

`.openhands/hooks/9x_hook-distress-bundle.py` — fires on every
manifest write with `completion_choice.kind == "distress"`. Validates
the bundle has the required fields (`block`, `tried`, `ask_of_scout`,
`would_unblock`). If a manifest closes with kind=distress but
omits the bundle structure, hook rejects (forces honest distress
authoring, not vague "I gave up" closures).

### Recovery

`scripts/audit-distress-signals.py` — nightly cron walks the last
7 days of distress bundles, computes:

- **Open distress count** — bundles without a `resolved_ts`
- **Mean resolution time** — how fast scouts are reaching them
- **Recurring distress patterns** — bundles with similar `block.title`
  values across the window (suggests a systemic issue worth
  surfacing as a charter)

Becomes a new shape: `distress.open.count` (target=decreasing,
fast resolution wins) + `distress.recurring.patterns` (target=
decreasing, recurring failures = systemic debt).

## Operational shifts

### completion_choice kinds — extend from 6 to 7

The Six-Choices Ritual becomes the Seven-Choices Ritual:

| Kind | When |
|---|---|
| `discover` | Surfaced new task_ids the swarm should claim |
| `verify` | Independent re-check of a previous claim |
| `promote` | Lift ephemeral → canonical |
| `spawn_seed` | Plant seed mission for another agent |
| `seal` | Mission complete; no downstream work |
| `reflect` | Synthesis-only; no production artifact |
| **`distress`** *(NEW)* | **Blocked; emergency bundle written; awaiting scout** |

### Manifests citing distress

When a scout resolves a distress bundle, their manifest carries:

```json
{
  "completion_choice": {"kind": "verify"},
  "resolved_distress": [
    {
      "bundle_id": "20260522T174200Z__distress__doctrine.coverage.audit___charter_lib-created-ts_maker",
      "claimed_ts": "2026-05-22T18:15:00Z",
      "resolution_summary": "backfilled created_ts from git log; updated _charter_lib to read it from git log when JSON body lacks it",
      "outcome": "resolved | escalated | reopened"
    }
  ]
}
```

The distress bundle's lifecycle becomes traceable: written →
claimed → either resolved or escalated. Each transition produces
a COC entry.

## Why "stigmergic" is the right word

The signal is left in the environment (filesystem). No message
gets passed. No queue gets enqueued. Any scout walking the
ephemeral folder sees the signal in their normal frontier scan.
The signal's strength is encoded in its filename + body
(`blocking_priority`, `would_unblock`).

This is exactly stigmergy: agents leave markers; other agents
read them and coordinate without direct communication.

## Single-line summary

**When agents hit dead ends, they write structured EMERGENCY
BUNDLES (`__distress__` type marker) with everything a rescuing
scout needs: what was tried, what failed, the hypothesis, the
ask. Scouts walk the day's distress folder, pick up signals,
investigate. Failures become exploration substrate. The 6-choices
ritual gains a 7th: `distress` — honest signal that the agent is
blocked and needs help, not silent abandonment.**

---

*Closes a 14-doctrine arc for 2026-05-22 (08-21). Implementation:
new schema + completion_choice kind + writer field + hook + scout
skill + audit shape. Should follow the bearing-trajectory MAKER
since both touch the manifest body.*
