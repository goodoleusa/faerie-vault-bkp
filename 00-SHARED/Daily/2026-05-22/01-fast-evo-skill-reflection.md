---
date: 2026-05-22
author: openhands-agent
related_skill: fast-evo
related_mission: canon-crystallization-01
status: synthesis-log
---

# Fast-evo skill — agent self-reflection from canon-crystallization-01

Captured from the agent that ran the canon-crystallization mega-mission
(`forensics/ephemeral/2026-05-22/canon-crystallization-01/`). The agent
was asked: "how's the fast-evo skill going? any thoughts? is it
holding you back or keeping you on track?"

This is the agent's own first-person account, preserved verbatim because
it documents the skill's effect at the discipline-of-cognition layer —
not just whether the cuts shipped.

---

## The moment of arrival

When the agent first read the mega-mission, its instinct was the default
on a big consolidation: scan everything, form a mental model, start
cutting. The mission scope was wide — three directory trees, six cuts,
frontend + backend + skills + hooks all in play. Default mode would
have been "I see the shape, let me start with the obvious wins."

The fast-evo skill interrupted that instinct at the door.

## What would have happened without it

Without fast-evo, the flow would have looked like this:

1. Read a few sample files to confirm categories matched the user's framing
2. Start deleting/renaming based on what looked obviously redundant
3. Write the MCP tools next (most concrete, clear inputs/outputs)
4. Build the shell harness
5. Stub out skill .md files
6. Run a verification pass at the end
7. Discover something broke; fix forward; discover something else broke
8. Eventually arrive at a working state with a vague sense of "what changed"

Three specific things would have gone wrong:

**First.** The agent would have walked into the eval cluster and seen
`3x_eval-baseline` and `3x_eval-faerie2` as the obvious "v1 deprecated"
targets — and been right. But it also probably would have retired
`9x_membench_scorer.py` as "duplicate of probes" because at a glance
they look like overlapping membench work. The INVENTORY-first rule
forced the agent to read each file's docstring before deciding. The
scorer is a deterministic post-eval analyzer — the "analysis" half of
a clean "probes (collection) + scorer (analysis)" split. Retiring it
would have been a real loss. Caught because writing a row about it in
the inventory was a prerequisite for touching it.

**Second.** The agent would have wired `metrics_usage` and immediately
broken the frontend. The `ActionsPanel.jsx` callsite uses
`tool: 'metrics_conversation'` with `args: {}`. A bare rename would
have hit the new tool's required `scope` parameter and the dashboard
would have 500'd. The "ZERO frontend tool breakage for the 16 critical
tools" non-negotiable forced thinking about back-compat before adding
the new tool. The alias pattern (keep `metrics_conversation`, have it
call the new slicer with `scope='conversation'`) emerged from that
constraint — and is the right pattern.

**Third, the subtle one.** The agent would have written the new MCP
tools as a single big diff, then run regen + lint once at the end.
fast-evo's sandwich rule made the agent run regen after the
`eval_usage.py` edit, BEFORE writing the skills. That sequencing
matters because if the registry had been stale or lint had caught a
stranded `@authed`, the signal arrives immediately while the change
is small and reversible. Catching it after writing 6 skills means a
much bigger blast radius.

## What fast-evo specifically helped think through

### The "good pieces" doctrine vs default heuristic

Default heuristic for old code: "Is this still used? No? Delete." The
user direction explicitly contradicted that: "they all contain good
pieces, quarantine with provenance." fast-evo's pairing with
`script-quarantine` made the discipline concrete instead of
aspirational. The agent had to fill in a column called
`good_pieces_landed_in` for every retire. That column IS the
discipline. If the agent couldn't name where the good logic survived,
the retire was blocked.

`3x_vault-reconciliation` was the example. First instinct was "old
shell-style binary, probably dead, retire." But filling in
`good_pieces_landed_in` forced finding where vault reconciliation
happens now. Answer: `4a_vault_status.py` + `breadcrumbs_vault_sync.py`.
Retire safe. Without the discipline, the file might have been retired
without confirming the successors existed.

### The cluster boundary problem

The eval cluster has eight files. First read: "all eval stuff,
consolidate into one." That would have been wrong. fast-evo made the
agent cluster-then-decide, and clustering revealed three sub-categories:

- **Release readiness** (`0x_dev_eval.py`) — aggregator over all signals
- **Workload runners** (`3x_eval_baseline_runner.py`,
  `3x_eval_faerie2_runner.py`) — produces FFMx for baseline vs swarmy
- **Dimension engine** (`3x_eval_dimensions.py`) — the A–G computation core
- **A/B harness** (`9x_eval_ab.py`) — pre-registered hypothesis testing

These are not duplicates. They're four legit different jobs that share
the "eval" prefix. Consolidating would have destroyed working orthogonal
tools. fast-evo's rule "every cluster must end with exactly one
canonical KEEP" forced asking "is this really one cluster, or four?"
and the answer was four.

### The rename as a real cut

Renaming `evo-wave → fast-evo` is the kind of thing the agent would
normally do as a one-liner without thinking. fast-evo made it a cut:

- Baseline: grep for all references → 4 files reference `evo-wave`
- Apply: `git mv` + edit frontmatter + update cross-refs
- New state: grep again → 0 unresolved references (AGENTS.md leftover
  caught on second pass)

Without that discipline the `git mv` would have been "done." The
cross-refs in `monkeybranching/SKILL.md`, `piston/SKILL.md`,
`openhands-sdk/SKILL.md`, and `AGENTS.md` would have rotted silently.
A stale `.agents/skills/evo-wave/SKILL.md` link in `monkeybranching`
would have been a dead pointer until some future agent tried to follow
it and bounced.

### The 6-Choices Completion Ritual

This one merits singling out. The ritual forces picking
`discover | promote | reflect | seal | spawn_seed | verify` as the
typed graph edge from your work into the next mission. The agent's
default at the end of a big mission is to write a free-form
"what's next" paragraph. The ritual disallows that — and is correct to
disallow.

When the agent sat down to fill in `completion_choice` on the manifest,
it had to ask: what's the right KIND of edge here? Not "what comes
next in narrative" but "what graph operation am I performing on the
mission DAG." Picked `promote` with target "fast-evo wave loop +
canonical eval doctrine" because that's the truth: the work isn't
done (other agents will run the loop, future crystallizations will
use the skill), but the artifacts are ready to be lifted into the
canonical path. `seal` would have been wrong (there's downstream
work). `discover` would have been wrong (didn't surface new
task_ids). `promote` was the precise word.

That's the value of constraining choices to six. It makes the agent
say what it actually did, in vocabulary the system can act on.

## The friction that was useful

The sandwich rule is annoying when confident. There were moments when
the agent KNEW the change would work, and running the measure step
felt like overhead. But two of the regen-check runs ALMOST failed:

- After the first MCP addition, the registry was stale (caught by
  `--check`) — needed regen, not just check
- The fast-evo.sh dry-run had a Python deprecation warning on
  `datetime.utcnow()` — not blocking but a real signal that the
  harness should be updated to use timezone-aware datetimes (noted,
  not fixed in this wave)

Without the intermediate measures, those would have been caught at
the end alongside other issues, with no clean signal about which cut
introduced which problem. fast-evo's "log a baseline AND a new_state
for every cut" rule means the `_evolution_log[]` in the manifest is
actually diagnostic — pointable at cut 5 with "tools went 79 → 81,
registry clean, lint clean" without re-deriving when that happened.

## What was actually new about this mission for the skill

The mission asked for "RAP but for fast evo wave cycle" — and the
skill didn't have an automated-mode section. The skill's body was
entirely about manual sandwich-measurement. The agent had to add a
new "Two modes" preamble and a section about the automated loop.
That edit IS the skill learning from this mission — the next agent
that triggers `fast-evo` will see both modes and pick the right one.

That's a fractal lifecycle moment, in the sense CLAUDE.md talks
about. The skill went through its own liftoff/cruise/insertion arc
inside this mission. Liftoff: rename + add the automated-mode
preamble. Cruise: apply the skill's existing discipline to the cuts.
Insertion: edit the skill's body to absorb what this mission taught
it. The skill is now richer than it was when the mission started,
and that's because the mission used it.

## Net assessment

fast-evo did three things the default mode wouldn't have done:

1. **Forced looking before cutting** — the INVENTORY-first rule
   caught the membench-scorer near-miss and the eval-cluster
   sub-categories
2. **Forced sequencing measure-cut-measure** — caught the stale
   registry between cuts instead of at the end
3. **Forced closing with a typed graph edge** — `completion_choice`
   is the discipline of saying what you did in vocabulary the
   system can route on

The cost was overhead — maybe 20% of tokens went to writing INVENTORY
rows, `_evolution_log` entries, and the manifest structure. That's a
real cost. But the alternative (cut blind, debug at the end) would
have cost more in rework. And the artifacts produced
(`INVENTORY.md`, `manifest.json` with `_evolution_log`,
`QUARANTINE-LEDGER.md`) are now durable signal for the next operator.
The mission's outputs aren't just the new tools and skills — they're
the **forensic trail of how the consolidation happened**, which is
the part that compounds.

---

*Author: the agent that ran canon-crystallization-01.*
*Skill: `.agents/skills/fast-evo/`.*
*Mission trail: `forensics/ephemeral/2026-05-22/canon-crystallization-01/`.*
