---
type: technical-narrative
status: candidate-application-supporting-material
author: jessica-terry
title: "Stigmergy as a Coordination Substrate for AI Agent Teams"
subtitle: "A practitioner's case for filesystem-mediated swarm coordination over message-passing — drawn from direct experience with Claude Code's Agent Teams and a parallel implementation called faerie"
date: 2026-05-19
bundle_note: "COPIED (not moved) from 00-Publications/ for publication-prep-2026-05-25 bundle. Original: 00-Publications/00-Anthropic Application STIGMERGY-FOR-AGENT-TEAMS.md"
---

# Stigmergy as a Coordination Substrate for AI Agent Teams

## Context

Anthropic's Claude Code includes an Agent Teams feature: a parent Claude session can spawn parallel subagents, each with its own context, and orchestrate them toward a shared goal. The feature is powerful but, as anyone who has used it in production knows, **buggy in characteristic ways**: subagents collide on file writes; the parent loses track of which subagent did what; coordination overhead grows quadratically with the team size; spawning more than three or four agents produces output that's hard to attribute, dedupe, or audit; recovery from a partial failure requires reading every subagent's transcript individually.

These are not "Claude is dumb" bugs. They are **coordination-architecture bugs** — the same class of failure mode that distributed systems researchers have spent fifty years cataloging and fixing in non-AI contexts. The good news is that the fix is well-understood and has been used at scale by biological systems for hundreds of millions of years. It's called **stigmergy**, and I want to make the case here that adopting it as the coordination substrate for Agent Teams would resolve a meaningful fraction of the bugs that currently make the feature painful in real workflows.

This piece is informed by:
- Direct, daily use of Agent Teams across multiple projects.
- Building a parallel implementation called *faerie* — a stigmergic coordination framework that has run on top of Claude Code and OpenHands for the past several months across investigations, code repositories, and an Obsidian-based collab vault.
- A field session on 2026-05-19 in which I deliberately ran an ad-hoc Potemkin version of faerie inside Claude Code itself (no install, just filesystem conventions and discipline) and watched 8 subagents coordinate to produce real work product. The session's failure modes are documented in `POTEMKIN-FAERIE-FIELD-REPORT.md` in this repository and are referenced throughout this piece.

## What stigmergy is, in one paragraph

Stigmergy is coordination via *environmental marker* rather than via *direct messaging*. The canonical biological example: when an ant finds food, it doesn't tell the colony directly. It deposits a pheromone trail on the ground as it returns to the nest. Other ants that encounter the trail follow it, deposit more pheromone, and reinforce the path. No ant communicates with any other ant; they all communicate *with the substrate*, asynchronously and durably. The result is robust, scalable, self-healing collective behavior with **zero central coordinator** and **no message-passing protocol**.

The principle generalizes far beyond ants. Termites build complex mounds via stigmergy. Slime molds solve optimization problems via stigmergy. Wikipedia's edit model is effectively stigmergic. Build systems like Bazel and Nix are stigmergic. Git itself, when used well across a team, is stigmergic — the repository state is the coordination substrate; the team coordinates by mutating it asynchronously.

For an AI agent team, the substrate is the **filesystem**, optionally augmented with a hash-chained ledger (chain of custody) for auditability. The "pheromone" is whatever an agent writes, where it writes it, and what filename it chooses.

## The specific bugs in Claude Code's Agent Teams that stigmergy addresses

Each of these bugs has been observed in production use and is reproducible:

### 1. Silent collision on shared file writes

**The bug:** Two subagents both decide they should write to `docs/X-INDEX.md`. They both proceed. The second write clobbers the first. No error is raised. The parent only notices when the artifact is missing structure from the first write.

**Why stigmergy fixes it:** A claim protocol — write `docs/_claims/X-INDEX.claim` *before* writing the artifact, using an atomic-create operation (`O_EXCL` or `mkdir`). If the claim file already exists, your subagent yields and picks a different artifact. The filesystem's atomicity guarantee becomes the lock. No coordinator needed.

**Field evidence from the 2026-05-19 session:** five subagents claimed five distinct themes via `docs/_claims/*.claim` without a single literal-collision. The one near-miss (worker-1 and worker-2 both targeting MEMORY-AND-CRYSTALLIZATION) was a *semantic* race that string-named claims couldn't catch — and the fix is well-known: use deterministic content-hash IDs rather than string names. This is the version of the bug Anthropic could fix at the framework level.

### 2. Parent loses track of subagent progress

**The bug:** Once a subagent is spawned in Agent Teams, the parent has no incremental visibility. It can't tail the subagent's tool calls; it can't query its current state; it can only wait for the terminal `task-notification`. If the subagent is doing something destructive or wrong, the parent finds out too late.

**Why stigmergy fixes it:** The subagent doesn't *tell* the parent what it's doing; it *writes* what it's doing into the shared substrate. The parent (and any other observer) reads the substrate. A subagent that writes `manifest_in_progress` files, updates them progressively, and only finalizes on success gives the parent — and a debugger, and a dashboard, and a future agent — observable state for free. **The substrate is the protocol.**

### 3. Recovery from partial failure requires reading every transcript

**The bug:** When an Agent Teams run partially fails, recovering requires the parent to read each subagent's tool-use transcript individually. Reading them all consumes the parent's context, often past the point where the parent can actually act on what it learns.

**Why stigmergy fixes it:** Recovery state lives in the substrate, not in the transcripts. After a partial failure: list `_claims/` (who started what), list `_claims/*.done` (who finished), list the artifacts on disk (what was actually produced). Reconciliation is a directory scan, not a transcript dump.

### 4. Coordination overhead scales quadratically

**The bug:** As Agent Teams grows from 2 to 5 to 10 subagents, the parent's coordination load scales worse than linearly. Each subagent needs scoping, briefing, monitoring, result-integration. The parent runs out of context not from the work but from the meta-work of coordination.

**Why stigmergy fixes it:** Per-agent coordination cost in a stigmergic system is *constant*, not linear in the number of agents. The parent writes a charter once. Every subagent reads it. The substrate handles the rest. The parent's role shifts from "broker" to "observer."

### 5. No audit trail for which subagent made which decision

**The bug:** Agent Teams produces artifacts but doesn't natively record provenance. If you want to know "which subagent wrote this file?" you have to go back to the transcripts. This is fatal for any domain where decisions need to be auditable.

**Why stigmergy fixes it:** A hash-chained chain-of-custody appended to a shared `coc.jsonl` file, with each entry signed by the agent's Ed25519 key, gives you forensic auditability for free. Every artifact carries a back-reference to its signed manifest entry.

### 6. Adding a new agent type requires updating the orchestrator

**Why stigmergy fixes it:** Agents self-route by reading the substrate. A new agent reads the same charter, the same mission queue, the same claim files. It joins the swarm by *showing up*; it doesn't need to be registered with anyone.

## Why this is timely

The bottleneck is no longer model capability; it is coordination architecture. For AI agent teams, the coordination architecture that wins will be the one that:

1. Doesn't require a central orchestrator (no SPOF, no bottleneck).
2. Survives partial failure gracefully (subagents can die without poisoning the team).
3. Produces auditable provenance for every artifact.
4. Scales by adding workers, not by upgrading the manager (linear, not quadratic).
5. Has well-understood debugging and recovery semantics.

**Stigmergy satisfies all five.** Message-passing orchestration satisfies, at best, one.

## Specific implementation proposals for Agent Teams

### Tier 1 — Conventions, not infrastructure

- **Claim protocol primitive:** atomic-create claim files. This is 30 lines of code.
- **Mission queue convention:** designate a path agents scan at idle for pickup-able work units.
- **Termination markers:** per-agent terminal-state files parents read instead of transcripts.
- **Output registry:** append-only artifact index every subagent appends to.

### Tier 2 — Substrate-level features

- **Filesystem-event streaming:** parent subscribes to substrate events via Server-Sent Events.
- **Per-subagent signing keys:** auto-generate Ed25519 keypairs per spawned subagent.
- **Hash-chained ledger:** one append-only `coc.jsonl` as canonical chain.

### Tier 3 — First-class coordination model

Shift the framework's mental model from "orchestrator dispatches to workers" to "workers self-route via substrate."

## What faerie demonstrates

For the past several months the author has been building *faerie* — a stigmergic coordination framework for Claude Code and OpenHands. The whole system is `bash -c` plus Python plus filesystem conventions. No new infrastructure, no message broker, no orchestrator service. The faerie repo demonstrates that the pattern is implementable on the existing primitives Claude Code and OpenHands already expose.

## The closing observation

The bug pattern in Agent Teams is the same bug pattern Wikipedia would have if it used a central editor instead of pages-as-substrate. The same bug pattern Git would have if it used a central message bus instead of commits-as-substrate. The fix is *biological*. It works because the substrate is durable, observable, asynchronous, and self-healing. Agent Teams already has the substrate — the filesystem is right there. The question is whether the framework treats the filesystem as a *shared mind* or as an *output target*.

If it's a shared mind: stigmergy, robustness, scale, auditability.

If it's an output target: orchestrator bottleneck, race conditions, silent failures, transcript-archaeology debugging.

---

*Supporting documents: POTEMKIN-FAERIE-FIELD-REPORT.md, FOR-SKEPTICS-zero-confabulation.md. All real artifacts from a real working system.*
