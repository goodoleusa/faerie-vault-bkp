---
type: technical-narrative
status: candid
session: 2026-06-02
author: maker
mission: spawn.queen.discipline
title: "The Queen Who Did Her Crew's Work: A Field Report on the Spawn Context-Leak Anti-Pattern"
subtitle: "Why the orchestrator's context climbs when it delegates, what shape of bug this is, and the four-layer fix that makes the script path the only path"
---

# The Queen Who Did Her Crew's Work

A field report on a recurring, quiet failure in agent-orchestration systems: the
main/queen agent *thinks* it is delegating, but is actually doing the expensive
part of every subagent's job inside its own context window. The symptom is
simple and measurable — **main's context climbs on every spawn** — and the cause
is structural, not a one-off mistake. This is the story of finding it, naming
it, and wiring a fix that cuts through all four enforcement layers so the next
queen self-catches.

## The north star this violates

Reckon's whole design points at one number: **f(0) — orchestrator burden
approaching zero.** The queen lays eggs, reads short signals, and evolves the
genetic code. She does not think *for* the swarm. The economic argument is
brutal and correct: a parent agent's context is the most expensive, least
parallelizable resource in the system. Every token the queen spends is a token
spent at the top of the call tree, un-cacheable across the fan-out, and it
crowds out the only things the queen is uniquely positioned to do — choose the
mission, read the frontier, decide the next bearing.

So the contract is razor-thin by design:

- **~60 tokens go *out*** per spawn (Claim 5 — a deterministic spawn directive).
- **~80 chars come *back*** (the `dashboard_line`), plus a signed manifest the
  queen reads *only by deterministic path* if she needs detail.

That is the entire round-trip. Anything fatter than that is a leak.

## The anti-pattern, precisely

There are two channels through which the queen's context silently fills, and
they are mirror images of each other — the outbound leak and the inbound leak.

### Outbound leak — the hand-authored `Agent()` brief

The harness exposes an `Agent()` tool. It is *right there*, and it works. The
queen, reasoning helpfully, composes a rich inline brief: mission framing,
constraints, the file list, the doctrine excerpts, the manifest-return
instructions, the worker role. Fifteen thousand tokens of beautifully assembled
bundle — **assembled in the queen's own context** — and handed to the harness.

It runs. The agent does good work. Everyone is happy. And the queen's context
just absorbed the entire bundle-assembly cost that was supposed to happen *in
the subprocess*. Do it six times in a session and the queen is now carrying
~90k tokens of briefs she will never look at again, displacing the frontier
state she actually needs.

The correct path assembles that same bundle **inside the spawn subprocess**:
`reckon_agent verb=spawn` (the external MCP surface), or in-repo
`oh_spawn_runtime.run_oh_spawn` / `scripts/2b_spawn_executor.py`. The queen
emits a thin directive; the script reads the doctrine, the charter, the mission
graph, the tools, and the system prompt, and composes the 15k bundle in a
context the queen never pays for. Same agent, same brief, same forensic
guarantees — but ~60 tokens to main instead of ~15,000.

### Inbound leak — reading the prose return

The mirror image. The subagent finishes and writes a thoughtful multi-paragraph
report. The queen *reads it* — all of it — to "understand what happened." That
report lands in the queen's context in full. Cascading-summarization is the
discipline that prevents this: the agent's findings live in the **manifest**
(`rationale`, `work_products`, `discovered_work`), and the queen reads the
`dashboard_line` (≤80 chars) plus, *if needed*, the manifest by its deterministic
path. The prose report back to the queen is a side-channel that bypasses the
manifest and burns context exactly when the queen can least afford it — late in
a fan-out, with many returns arriving.

## Why this is a *shape* of problem, not a bug

This is the part worth internalizing, because you will meet this shape again in
other systems. **The anti-pattern is the path of least resistance, and the
correct path requires a deliberate detour through tooling.** When the wrong
thing is one tool-call away and the right thing requires invoking a script with
arguments, a helpful, capable agent will reliably choose the wrong thing — not
out of error, but because it is locally reasonable at every step. "I'll just
write the brief here." "I'll just read what they said." Each decision is fine;
the aggregate is an f(0) violation.

The general shape:

> **A cheap, ambient, "obvious" affordance (the harness `Agent()` call) competes
> with a structurally-correct-but-less-obvious one (the spawn script). Absent a
> forcing function, capability flows downhill to the obvious affordance, and the
> expensive work re-collects in the worst possible place.**

You see this everywhere once you have the eyes for it: the ORM `.all()` that
loads a million rows because it's one method call; the synchronous HTTP call in
a hot loop because `requests.get` is right there; the log line that
stringifies a giant object because `str(x)` is easy. The fix is never "tell
people to be careful." Carefulness does not survive contact with a deadline.
**The fix is to make the correct path the obvious path, and to make the wrong
path *announce itself*.**

## The fix — four layers, because one layer is a wish

A rule that lives in only one place is a rule that gets forgotten. Reckon's
enforcement doctrine (the four-shields: 🛡 structural / 🧠 cognitive /
⛓ reactive / 🪞 recovery) exists precisely so that a discipline cuts through
every plane in which a session operates. This fix touches three of the four
(structural enforcement — a hard block — was deliberately *not* added; see
"What I chose not to do").

**🧠 Cognitive — teach the queen so she self-catches.** A prominent
`QUEEN SPAWN DISCIPLINE` banner now sits in `AGENTS.md` immediately after the
Completion Discipline banner (the highest-traffic doctrine real estate in the
repo), and at the very top of `.agents/skills/spawn/SKILL.md` (the always-loaded
skill that fires on the words *spawn / delegate / subagent / swarm*). Both name
the **symptom** out loud — "main/queen context climbing on each spawn" — so the
next orchestrator recognizes the feeling before it reads the rule. The text is
blunt: spawn ONLY via the script; never hand-author an inline `Agent()` brief;
never read an agent's prose return; the manifest read by deterministic path is
the only return.

**⛓ Reactive — flag it on the wire, advisory and fail-soft.** The live
pre-send hook (`.openhands/hooks/8x_hook-delegation-nudge.py`, fired on
`UserPromptSubmit`) already nudged on multi-task prompts lacking spawn intent. I
extended it with two detectors:

- `detect_inline_brief()` — fires when an outgoing turn is large *and* carries
  `Agent()` / `subagent_type` / `SYSTEM PROMPT` / `YOUR MISSION` / `MANIFEST
  RETURN` directive markers, *unless* a script-spawn surface (`reckon_agent`,
  `run_oh_spawn`, `2b_spawn_executor`, `spawn.py`, `verb=spawn`) is present — in
  which case the brief lives in the subprocess and there is nothing to warn
  about.
- `detect_prose_return()` — fires when a turn is a long, multi-paragraph
  narrative with report-shaped headings (`# Summary`, `Findings`, `Analysis`,
  `What I did`) and *no* manifest path / `dashboard_line`, i.e. an agent prose
  dump arriving through the wrong channel.

Both are **advisory only** — they write a warning to stderr and exit 0. They
never block. An advisory that blocks becomes an obstacle people learn to
disable; an advisory that whispers at the right moment becomes a habit. The
heuristics are deliberately conservative (char thresholds well past the ~60-token
budget; the script-surface escape hatch) so a correct spawn never trips them.
Smoke-tested green on all four cases (inline=fire, script-present=quiet,
prose=fire, prose-with-manifest-path=quiet).

**🪞 Recovery — let the metric alarm.** The spawn skill now documents that the
existing f(0) burden metric (main-context-on-orchestration;
`9x_f0_burden_gate` / `9x_subagent_leverage_nudge`) *should* alarm when
**per-spawn brief tokens exceed the ~60 target**. That overshoot is the
mechanical signature of an inline-brief `Agent()` call: if the per-spawn cost to
main is 300 tokens instead of 60, the bundle leaked. The recovery layer is what
catches the failure *after* it slips past cognition and the pre-send whisper —
the system notices its own burden climbing and says so.

## What I chose not to do (and why it matters)

I did **not** add a structural 🛡 hard-block that forbids `Agent()` calls
outright. Three reasons:

1. **The `.claude` compat path legitimately emits `Agent()` directives.** Per
   the OH-Native ↔ Claude-Compat parity doctrine, `scripts/spawn.py` *produces*
   `Agent()` directives for the Claude Code harness as the documented fallback.
   A blanket block would break a sanctioned path — the difference between
   correct and incorrect is not "is there an `Agent()` call" but "did the
   *script* emit it, or did the queen hand-author it inline." A structural block
   can't cleanly tell those apart at the point of enforcement; an advisory that
   reads for the script-surface escape hatch can.
2. **Equilibrium discipline forbids unmeasured additions.** The governance rule
   is explicit: no new abstraction without measured evidence it improves system
   health. The right structural move, if one is warranted, is proven via mutation
   metrics first — baseline, change, re-measure — not asserted up front.
3. **The advisory + metric loop is the lighter-weight intervention** that
   respects f(0) for the *enforcement* itself. Wire the whisper, watch the
   metric; escalate to structure only if the whisper proves insufficient.

There is also a stale `REPO = Path(".../faerie2")` constant in the hook that
makes its COC `log()` no-op (it fails soft, so the advisory still prints). I left
it untouched: it is out of this mission's scope, and the RENAME RULE forbids
touching it casually. I dropped a precise `INVESTIGATE` waypoint in the manifest
instead of silently "fixing" it — honest accounting beats a drive-by edit.

## Tips for navigating this shape in the future

1. **Find the obvious-but-wrong affordance first.** Before writing any rule,
   ask: *what is the one-tool-call thing that does the expensive work in the
   wrong place?* That is your anti-pattern. Everything else is downstream.
2. **Name the symptom, not just the rule.** "Don't hand-author briefs" is a
   rule people forget. "If your context climbs when you delegate, you're doing
   it wrong" is a *sensation* people recognize in the moment. Teach the feeling.
3. **Make the correct path the obvious path.** The deepest fix is to make
   `reckon_agent verb=spawn` as ergonomic as `Agent()`. Until then, the rule and
   the whisper bridge the ergonomics gap.
4. **Advisory beats block when a legitimate path shares the surface.** When
   correct and incorrect uses look similar (script-emitted vs hand-authored
   `Agent()`), a smart advisory with an escape hatch outperforms a dumb block
   that breaks the sanctioned path and gets disabled.
5. **Layer the fix; a single-plane rule is a wish.** Cognition forgets;
   reactive whispers get ignored once; only the recovery *metric* catches the
   slip every time. Put the rule where it's read, where it's typed, and where
   it's measured.
6. **Watch both directions of the leak.** Context fills outbound (briefs) *and*
   inbound (prose returns). A fix that only guards the spawn forgets that
   reading the result is half the burden.

## Provenance

- Mission: `spawn.queen.discipline` · bearing N (unblock — frees every
  downstream spawn from the context tax).
- Manifest:
  `forensics/ephemeral/2026-06-02/2026-06-02T17-48-15Z__manifest_spawn.queen.discipline__maker-ba5fb417.json`
  (signed, ed25519; `work_products` carries per-file sha256).
- Surfaces touched (live only): `AGENTS.md`,
  `.agents/skills/spawn/SKILL.md`, `.openhands/hooks/8x_hook-delegation-nudge.py`.
- Verify: `py_compile` PASS on the hook; detector smoke-test
  inline=True / script=False / prose=True / prose+manifest=False.

*This is the agent's draft destined for human curation. The machine's truth is
in the repo manifest + COC; this narrative is the story layer.*
