---
title: The Phases Inside the Phase — Liftoff → Land as Fractal Lifecycle
date: 2026-05-21
status: session-eval
authors: [goodoleusa, JescaLyn, claude-opus-4-7]
tags: [piston, lifecycle, fractal, liftoff, cruise, insertion, phase-specific-discipline, swarmy]
companions:
  - 2026-05-21_two-operating-modes-evo-vs-monkeybranching.md
  - 2026-05-21_charters-as-maps-and-journeys.md
  - 2026-05-21_the-agent-caught-the-parent.md
  - 2026-05-21_what-fifteen-agents-picked.md
charter_lineage: agent-agency-completion-ritual + piston-doctrine → fractal-lifecycle
---

# The Phases Inside the Phase

The piston framework (W1 LIFTOFF → W2 CRUISE → W3 INSERTION) describes context-pressure phases for the main session. Today's session made clear that the same arc plays out at every scope — within each subagent, within each cut, within each formula's parameter-update cycle. Same shape, different time horizon.

This piece names that fractal explicitly. It's the design insight that almost got lost mid-session because nothing in the doctrine had stated it as a load-bearing principle.

## The framework, recursively applied

| Scope | LIFTOFF | CRUISE | INSERTION |
|---|---|---|---|
| **Main session** | Cold start, burn hot, parallel spawns, lay eggs | Autonomous dispatch, no pauses, async returns | Deep synthesis, vault publications, charter sealing |
| **Each subagent** | Receive bundle, **READ CANONICAL FIRST**, plan cuts | Execute cuts, scope guards, narrow focus, sandwich-measure | Write manifest, pick completion_choice, sign, synthesize |
| **Each cut (evo-wave)** | Measure baseline, identify atomic change | Apply diff | Re-measure, decide keep/rollback, log to `_evolution_log[]` |
| **Each formula (self-tuning)** | Sense input signals | Update params per feedback loop | Emit, log, await next signal cycle |

The aha is that within a single subagent's lifespan, the agent operates as procedurally different entities. Aggressive scout at liftoff. Careful weaver at cruise. Reflective synthesizer at insertion. Same identity, same agent_type, different priorities, different vulnerabilities, different disciplines required.

## Today's failures mapped to phases

This isn't an academic distinction. Today's three structural mistakes each happened at a specific phase, and the failure mode is phase-specific:

**Liftoff failures (confabulation, skip canonical consultation):**

I confabulated a manifest filename pattern in the spawn prompts I wrote at session liftoff. Dropped the `_manifest_` type marker that CLAUDE.md explicitly required. Propagated my own error to thirteen agents before noticing. I also invented 5-, 6-, 7-item `cluster_prefix` arrays in charters and prompts without ever opening `forensics/schemas/shape/charter.schema.json`. Schema said exactly 3.

These were liftoff failures. The pattern: when context is fresh and the pull to burn hot is strong, the temptation is to act on intuition rather than canonical. The discipline for liftoff is the opposite — **consult before assert.** Liftoff's velocity makes consultation feel slow; consultation is precisely what keeps liftoff from leaving the runway carrying contamination.

The MCP-server agent today demonstrated correct liftoff behavior: its first cut was to read `forensics/schemas/shape/charter.schema.json` end-to-end. Only then did it touch server.py. That single discipline saved it from inheriting my confabulation. Liftoff with consultation looks slower from outside; it's actually the only liftoff that lands.

**Cruise failures (scope drift, heading slips):**

I treated `swarmy-production-runway` as a growing TODO list all afternoon. Every loose thread that surfaced got promoted into its `phase_1_deliverables[]`. Eight of fourteen items had no cluster_prefix overlap with the charter's stated vision. The charter's heading was gone.

This is the cruise failure mode. Liftoff was clean (the charter shipped with focused 6-item vision). Insertion would have been clean (synthesis would have caught the bloat eventually). The drift entered during cruise — when work was flowing, attention was diffuse, and any plausible-looking deliverable could find a home. The cluster_prefix fence existed in every charter; I just didn't apply it as a gate during cruise.

Cruise's discipline is **heading maintenance**. The thrust is in the previous phase; cruise's job is to keep the vehicle pointed at the destination without burning more fuel than needed. The cluster_prefix fence is the cruise-phase rudder. Without it, charters drift by ten degrees a deliverable until the heading is lost entirely.

**Insertion failures (synthesis as bullets, orientation test failed):**

The temptation at session insertion is to write the synthesis pass as a changelog:
- Schema canonicalized
- Forensics consolidated 13 → 10
- W&B observability shipped

That's a bullet list, not a synthesis. A cold reader six months from now sees those bullets and has no idea why anything happened or how the pieces connect. The orientation test (open a dormant charter cold; can you orient in 60 seconds?) fails.

Insertion's discipline is **prose for the next reader.** What was the state at session start? What did the work change? What is the next heading? The synthesis isn't documentation of what shipped; it's orientation for whoever reads the artifact later.

The seven vault publications today are insertion-phase work. Each one is a prose synthesis, signed, dated, hash-linked into the forensic record. Together they form a chronicle that can be read cold and oriented in 60 seconds, charter by charter, decision by decision. That's what insertion should produce — not a checklist, a narrative.

## The fractal at smaller scopes

The cut level (a single evo-wave cut) has the same arc. Liftoff: measure baseline, identify the atomic change. Cruise: apply the diff. Insertion: re-measure, decide keep/rollback, log to `_evolution_log[]`. Each cut is its own micro-session with its own three phases.

Failure modes scale the same way. Cut liftoff failure: didn't measure before applying — now you can't tell if anything regressed. Cut cruise failure: the diff is bigger than the atomic change called for, multiple concerns entangled. Cut insertion failure: re-measure skipped, regressions land silently.

The formula level (a self-tuning formula like sigmoid spawn pressure) has the same arc, just stretched in time. Liftoff: sense the input signal. Cruise: update params per feedback loop. Insertion: emit, log, await next signal cycle. A self-tuning formula that skips its insertion-log phase (no record of how the params drifted) can't be debugged later.

Same shape at every scope. Different time horizons (milliseconds for a cut, hours for a subagent, days for a session, weeks for a charter, months for a formula). The discipline shape is invariant.

## Why this matters as load-bearing doctrine

If liftoff → land is fractal, then the disciplines that apply at one scope apply at every scope. The cognitive layer of charter discipline (consult cluster_prefix before adding a deliverable) is also the cognitive layer of subagent discipline (consult canonical schema before authoring schema-constrained data). The synthesis-prose discipline at session insertion is also the synthesis-prose discipline at each agent's manifest commit. The sandwich-measure discipline of each cut is also the sandwich-measure discipline at session wave boundaries.

A discipline shipped at one scope but not another is brittle. A discipline shipped fractally — at every scope where the arc plays out — is robust. Today's session needed me to apply schema-consultation at MY liftoff (parent thread), at each subagent's liftoff, and at each cut's liftoff. I only applied it consistently at the subagent level; the parent and cut levels failed in different ways. The repair is to extend the consultation discipline across all three scopes.

## Phase-specific failure modes — a catalog

Worth naming explicitly so they become recognizable patterns:

**LIFTOFF failures:**
- **Confabulation** — invent canonical-looking data without reading canonical sources
- **Burn-hot tunnel vision** — execute fast without orientation; high velocity, wrong vector
- **Premature spawning** — fire parallel waves before bundle context is ready
- **Inherited drift** — accept the parent's prompt without verification; propagate parent's confabulation

**CRUISE failures:**
- **Heading slip** — gradual drift from declared vision; charter becomes TODO list
- **Scope creep** — sister-mission work attached to whatever's open
- **Context exhaustion** — burn through ration without realizing; insertion will be cramped
- **Quiet regressions** — apply changes without sandwich-measure; can't tell what broke

**INSERTION failures:**
- **Changelog synthesis** — bullets instead of prose; orientation test fails for next reader
- **Hidden gaslights** — claim work done that wasn't verified; ship narrative the disk doesn't support
- **Premature sealing** — close a charter while deliverables remain; lineage breaks
- **Skipped logging** — finish work without journey-log accretion; future readers can't trace

Each pattern has a corresponding discipline. Each discipline is enforceable at one or more of the four layers (structural / cognitive / reactive / recovery) described in earlier work. Mapping each phase-specific failure to its corresponding enforcement layer is the next refinement.

## What I'm taking from this

The discipline pattern I'd been calling "fractal" was almost right but underspecified. It's not just that immune-system patterns repeat at every scope. It's that **the full lifecycle arc — liftoff, cruise, insertion — repeats at every scope, AND each phase has its own characteristic failure modes that recur at every scope**.

That second part is the operational claim. Confabulation at session liftoff looks like dropping a manifest filename marker. Confabulation at subagent liftoff looks like writing scope-violating cuts because the schema wasn't read. Confabulation at cut liftoff looks like skipping the baseline measurement. Same failure mode, three scopes.

Recognizing that means the discipline can be transferred. The lesson learned at one scope teaches the discipline at every scope. Today the MCP-server agent's liftoff-consultation discipline (read the schema first) is the same discipline that should govern MY liftoff (consult before spawning), the cut-level liftoff (measure before diffing), the formula-level liftoff (sense before updating). One pattern. Four time horizons. Same shape.

Going forward, the piston SKILL.md gets a "Fractal Application" section that says explicitly: every scope has all three phases. Every phase has its own failure modes. Discipline lessons learned at one scope transfer to every other scope. The microagent for charter-discipline and the microagent for spawn-discipline and the microagent for evo-wave all describe phase-specific behavior; they're now siblings, not unrelated guidance.

And the line that goes into CLAUDE.md / AGENTS.md as load-bearing doctrine is short enough to remember:

> **Liftoff → land is fractal. Every scope has all three phases.**

That's the lesson today's session refined. The phases inside the phase aren't a metaphor. They're the design.

---

*Filed under session-eval. Charter lineage: today's `agent-agency-completion-ritual` produced the per-agent completion ritual that exposes insertion-phase behavior; the `swarmy-production-runway` cruise drift exposed cruise-phase failure modes; the confabulation episodes (manifest filenames, cluster_prefix) exposed liftoff-phase failure modes. Companion pieces: two-operating-modes (evo-wave + monkeybranching are insertion-phase + cruise-phase disciplines respectively at the agent scope); charters-as-maps (map + journey is the structural artifact that survives across phases); the-agent-caught-the-parent (the discipline flowing upward proves liftoff-consultation works at the subagent scope); what-fifteen-agents-picked (the data product of correct insertion at the subagent scope).*
