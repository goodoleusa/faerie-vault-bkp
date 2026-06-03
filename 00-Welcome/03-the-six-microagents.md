# 03 — The Six Microagents

In `_meta/microagents/` you'll find six skills:

```
charter-discipline/   evo-wave/    monkeybranching/
compass/              piston/      spawn/
```

Each is a `SKILL.md` (sometimes with a sibling script like
`measure.sh`). They are **knowledge skills** — they don't run on their
own. Your swarmy install's agent harness loads them automatically when
the conversation mentions one of their trigger words.

This page is the brief-of-briefs. Each skill has its own SKILL.md that
goes deep. Read the one(s) you need when you need them.

## charter-discipline — Maps + Journeys, Not TODO Lists

**Triggers:** `charter`, `phase_1_deliverable`, `cluster_prefix`, `scope
fence`, `mission charter`, `charter split`, `acceptance ritual`, `new
charter`, `charter authoring`, `phase_2_roadmap`.

**Why it exists:** a charter is a contract. It declares where the mission
wants to go (the **map**) and accretes evidence of how it actually
traveled (the **journey**). A map without a journey is a wish; a journey
without a map is a changelog. The skill defines four enforcement layers
(structural, cognitive, reactive, recovery) so charters don't drift.

**When you'll hit it:** writing or auditing any charter, splitting an
overgrown charter into two, deciding what goes in `cluster_prefix`.

## compass — N/S/E/W Bearing Routing

**Triggers:** `bearing`, `compass`, `north`, `south`, `east`, `west`,
`N-edge`, `S-edge`, `E-edge`, `W-edge`, plus archetype team names
(UNBLOCK / SHIP / PARALLEL / BASELINE).

**Why it exists:** agents need a tiny, shared vocabulary for "what kind
of edge is this work?" so they can route in O(1) without reading prose.
N = unblock predecessor. S = ship downstream. E = parallel sibling. W =
back to baseline / re-seat assumptions.

**When you'll hit it:** reading agent manifests (the `bearing` field on
`discovered_work[]` entries), deciding which team to spawn for a mission
frontier.

## evo-wave — Genetic / Mutation Discipline

**Triggers:** evolution, mutation, fitness, baseline, T-zero, etc.

**Why it exists:** changes to the swarm's behavior are mutations.
Mutations are classified beneficial / neutral / harmful / uncertain.
**Measure baseline BEFORE repair** — fixing harmful mutations before the
baseline is wired destroys your ability to claim improvement.

**When you'll hit it:** when you want to claim "this change made the
system better." If you can't show a baseline measurement, the claim
fails the discipline.

## monkeybranching — Parallel Spawn Scope Discipline

**Triggers:** `monkeybranching`, `parallel agents`, `parallel spawn`,
`spawn wave`, `scope discipline`, `collision safe`, `DO NOT TOUCH`, `wide
spawn`, `agent boundaries`.

**Why it exists:** spawning many agents at once is the fastest way to
make progress AND the fastest way to make a merge nightmare. The skill
codifies how to draw SCOPE / DO NOT TOUCH boundaries per agent, write
collision-safe prompts, set per-agent acceptance tests that catch
gaslighting, and pick wide-vs-deep based on the work shape.

**When you'll hit it:** any time you're dispatching ≥2 agents to
neighbouring code. Read the skill before drafting their bundles.

## piston — Context Pressure Waves

**Triggers:** piston, wave, W1, W2, W3, liftoff, cruise, insertion,
context budget, fuel.

**Why it exists:** main-context is fuel. The piston model says: low
context fill = burn hot (W1 LIFTOFF, max parallelism); medium = cruise
(W2, autonomous dispatch); high = synthesis (W3, deep work). The waves
gate exponential agent-spawning so you don't OOM the conversation.

**When you'll hit it:** at the top of any session where you have a clear
mission and a fresh context budget.

## spawn — Semantic-Intent Team Spawner

**Triggers:** `/spawn` (the slash command), spawn, team, dispatch,
bundle.

**Why it exists:** picking 4 agents at random doesn't compose. Picking 4
agents along **bearing diversity** (a NAVIGATOR for N, a MAKER for S, a
BRIDGE for E, a DEEP-DIVER for W) does. The skill codifies the
semantic-intent dispatcher logic.

**When you'll hit it:** every time you spawn agents. Eventually you'll
internalize the patterns; for now, let the skill drive.

## How loading works

Your swarmy install runs Claude / OpenHands with a skill loader that
scans the conversation for trigger words. When a trigger fires, the
`SKILL.md` content is injected into the agent's context. You don't
invoke them — you just talk about your problem and they appear.

If you want to read one cold:

```bash
cat _meta/microagents/charter-discipline/SKILL.md
```

Each is short enough to read in one sitting.

## What's NOT here

The microagents are deliberately a small set. They are the **disciplines
that benefit every project**. Your swarmy install has many more
agent-types (`python-pro`, `documentation-engineer`, `data-scientist`,
`ai-engineer`, etc.) — those are *workers*, not *disciplines*. They
live in the swarmy repo's `.agents/`, not in the vault.

If a discipline would benefit every swarmy user, it belongs in this
template's `_meta/microagents/`. If it's project-specific, it belongs in
the project, not the template.

## Next

You're done with the welcome flow. Open `_meta/cluster-prefixes.md` if
you want to deepen the discipline, or close this folder and start
working in `20-Inspirations/` (pollen) and `30-Synthesis-Log/` (nectar).
