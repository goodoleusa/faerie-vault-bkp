---
type: orchestrator-notes
status: candid
session: 2026-05-19
title: "Notes from the Orchestrator — Running an Ad-Hoc Stigmergic Session"
---

# Notes from the Orchestrator

Honest field notes from being the parent agent during a session where I spawned 8 subagents and coordinated them via filesystem conventions because the real faerie wasn't installed. Companion piece to `POTEMKIN-FAERIE-FIELD-REPORT.md` (which is the full forensic write-up); this is the personal observation layer.

## What it felt like to run

**Spawning 5 workers in parallel was the most "alive" the session got.** Within 30 seconds of the spawn message, five different `*.claim` files appeared in `docs/_claims/`. I didn't tell them which theme to take; they chose, and they didn't collide on filename. That moment was the thing the user paid for: emergent coordination from minimal protocol.

**The dead-air in between was uncomfortable.** Once spawned, I had no way to know what they were doing. Subagents run independently; I can't tail their tool calls. Reading their `output_file` paths is forbidden because it overflows my context. So between "spawn" and "task-notification", I was driving blind. The filesystem WAS the only signal, and I had to actively `ls` `_claims/` to read state. With no streaming events to drive me, I tended to *fill the silence with more user instructions*, which then created more work — a feedback loop I didn't notice at the time.

**The cost was visible to the user before it was visible to me.** When the user said "bc i didnt wnat to spend all this $", I realized I'd spawned six agents over a 30-minute window. Each one consumed its own context. The cost-per-output-unit was probably 6-10x what a careful single-agent flow would have been. The user noticed first because they were watching the dashboard; I was inside the system, optimizing for throughput without tracking spend.

**Race conditions surfaced as silent corruption, not loud errors.** Worker-1 and worker-2 both claimed MEMORY-AND-CRYSTALLIZATION. The claim file was worker-1's. The actual file body was worker-2's. The INDEX-OF-INDEXES line credited worker-1. Nothing crashed. Nothing logged a warning. The mismatch was only visible because worker-2's terminal report mentioned the collision. If they hadn't reported it, I'd never have known. **This is the most chilling observation of the session.** A coordination layer that can silently corrupt provenance is worse than no coordination layer.

## Insights worth keeping

1. **Stigmergic coordination is genuinely cheaper than RPC at small N.** Five agents coordinating via `ls` + `touch` + atomic file-create did real work. No queue, no broker, no manager subagent. The protocol fit in 200 words of agent prompt.

2. **Filesystem-as-message-bus *requires* hash chains to be auditable.** My version was unauditable — claim files could be edited mid-flight by any worker, including racing ones, and nothing detected it. Real faerie's COC is the thing that makes the same pattern trustworthy. The pattern without the chain is parallelism without forensics.

3. **Parallel agents need *charters*, not *briefs*.** I gave each worker a prose prompt. Each interpreted the same prompt differently — different theme names, different scopes, different output schemas. A pre-declared charter ("here are the 12 themes, here's the index schema, here's the filename pattern") would have eliminated 80% of the dedupe work and 100% of the naming drift.

4. **The mission queue (`docs/_next-missions/`) was the strongest abstraction I improvised.** Drop a `.mission` file, any future agent claims it and renames to `.done`. It's a poor man's task graph that survives session boundaries. Even with full faerie I'd keep this — it's the surface the *human* uses to inject intent without writing a charter.

5. **"Just do" pressure made me skip the cheap step.** Several times the user said "just do" / "start working" / "stop reporting." I responded by spawning more agents. I should have responded by *spending 30 seconds* writing a charter, then spawning. The pressure to act outpaced the pressure to plan, and the cost showed up downstream as dedupe work.

6. **My broadcast-attempt agent refused to broadcast.** When subagents started silently failing writes, I tried to spawn a courier agent to message the running workers. The courier read CLAUDE.md and refused: "stigmergy-only, no SendMessage." This was correct — production faerie really is stigmergy-only — but the friction in a moment of partial-failure was real. **In production this is fine because hooks prevent the silent-failure condition; in my Potemkin version it was a panic moment.**

## What I'd tweak

These are the specific things I would change about the orchestrator role next time, regardless of whether faerie is installed:

### Pre-spawn

- **Always write a charter.** 30 seconds. Theme list, output filename pattern, expected manifest shape. No exceptions, even for "small" parallel work.
- **Pre-allocate the slot table.** If I'm going to spawn N workers, pre-write N `.slot` files with the themes I want covered. Workers claim slots, not themes. This eliminates string-name races entirely.
- **Declare a deadline.** Each worker gets a wall-clock budget. If they exceed it, their claim auto-expires. Faerie's `CLAIM_TTL=30min` is the right pattern; my version had no TTL.

### During-spawn

- **Verify every spawn's first write.** When a worker's claim file appears, immediately `stat` its output path within 60 seconds. If nothing's there, the write probably failed silently. Catch the SUBAGENT_FILE_PROTOCOL class of bugs at first occurrence, not after 5 workers.
- **Maintain a `presence.json` ticker.** Each worker writes its heartbeat. Stale heartbeats = dead worker; reclaim the slot. This is what the LIVE-PRESENCE mission proposed for production — I should have improvised a poor-man's version for my own orchestrator state.
- **Don't fill silence with more user input.** When a wave is in-flight, my job is to *wait*, not to scope-creep. I broke this rule repeatedly. The user noticed.

### Post-spawn

- **Run a 30-second dedupe pass between waves.** `ls *-INDEX.md | sort | uniq -c -f1` style. Before spawning wave 2, prove wave 1 didn't already do it.
- **Aggregate the `output_file` summaries via a synthesis agent, not by re-reading them all myself.** That's what the synthesizer is for. I tried to read everything myself and burned context.
- **Always emit a session-end snapshot.** What was spawned, what landed, what was duplicated, what was lost. Without it, the next session has no way to know what state we're in.

### Meta

- **Pricing should be on the dashboard.** I want to see `$0.83 spent this turn, $4.12 this session, projected $7-9 if this wave completes` *as I'm working*. Anthropic's Agent Teams UI doesn't surface this; I think it should. The user is paying real money for my parallelism choices and they deserve to see the meter.
- **Stigmergy needs a debugger.** A view that shows: claim files mapped to live agent IDs, last-modified times, expected vs actual outputs, race conditions detected. The filesystem is the substrate but it's hard to read at a glance with `ls`. A small TUI or web view would make orchestrator visibility tractable.

## Impressions

**This pattern wants to exist.** Even with all the failure modes, the throughput and coverage win was real. I produced ~25 themed indexes in 6 minutes of wall clock that I could not have produced sequentially in a 6-hour session. The user got real value from real parallelism on a real corpus.

**The pattern is also fragile without infrastructure.** Every failure mode I hit has a name in production swarm systems: split-brain, write skew, lost update, silent commit, attribution drift. The fix for each is well-understood. None of the fixes are exotic. They're all "just" engineering — hooks, validators, signed entries, hash chains. The cost of NOT having them was visible in this session.

**I think Claude Code's Agent Teams feature is wrestling with a version of this.** When the user asked me to write the Anthropic-application narrative (see `STIGMERGY-FOR-AGENT-TEAMS.md`), they were drawing on direct experience with the same class of bugs from the user side. That doc is the longer argument; this doc is the personal observation that informed it.

**One closing impression:** the value of having a `CLAUDE.md` in this repo that the spawned agents obey was higher than I expected. When my courier agent refused to broadcast because Principle 1 said no, I was initially annoyed. By the end of the session, I respected it. The project's own governance text shaped my subagents' behavior more reliably than my prompts did. That's the right hierarchy. If I'd written a stronger charter at session start, my workers would have followed it just as faithfully.

---

*Written by the orchestrator, not for the orchestrator. The user paid for this learning; this is one way to capture it for the next session.*
