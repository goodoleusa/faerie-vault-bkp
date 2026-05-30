---
type: technical-narrative
status: candidate-application-supporting-material
author: jessica-terry
title: "Stigmergy as a Coordination Substrate for AI Agent Teams"
subtitle: "A practitioner's case for filesystem-mediated swarm coordination over message-passing — drawn from direct experience with Claude Code's Agent Teams and a parallel implementation called faerie"
date: 2026-05-19
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

**Field evidence:** during the swarm phase of the 2026-05-19 session, I could `ls -la docs/_claims/` at any moment and see which workers had started which themes. Stale `.claim` files would indicate dead workers; absent ones would indicate yielding. Progress was visible without RPC.

### 3. Recovery from partial failure requires reading every transcript

**The bug:** When an Agent Teams run partially fails, recovering — knowing what got done, what didn't, what state is consistent — requires the parent to read each subagent's tool-use transcript individually. Each transcript is large (sometimes 50K+ tokens). Reading them all consumes the parent's context, often past the point where the parent can actually act on what it learns.

**Why stigmergy fixes it:** Recovery state lives in the substrate, not in the transcripts. After a partial failure: list `_claims/` (who started what), list `_claims/*.done` (who finished), list the artifacts on disk (what was actually produced). Reconciliation is a directory scan, not a transcript dump. The parent doesn't need to read megabytes of tool-use history to know the system's state because the system's state IS the directory listing.

**Field evidence:** when I needed to know what the swarm had produced, I ran `ls docs/*-INDEX.md` and got the answer in 50ms. I never read a subagent transcript.

### 4. Coordination overhead scales quadratically

**The bug:** As Agent Teams grows from 2 to 5 to 10 subagents, the parent's coordination load scales worse than linearly. Each subagent needs scoping, briefing, monitoring, result-integration. The parent runs out of context not from the work but from the meta-work of coordination.

**Why stigmergy fixes it:** Per-agent coordination cost in a stigmergic system is *constant*, not linear in the number of agents. The parent writes a charter once. Every subagent reads it. The substrate handles the rest. The parent's role shifts from "broker" to "observer" — checking state, intervening when needed, but not actively orchestrating each step.

**Field evidence:** 5 parallel workers, 1 charter (the swarm-coordination prompt), zero brokering. The parent (me) didn't intervene in worker-to-worker coordination at all during the synthesis phase. The workers self-routed.

### 5. No audit trail for which subagent made which decision

**The bug:** Agent Teams produces artifacts but doesn't natively record provenance. If you want to know "which subagent wrote this file? at what step? with what reasoning?" you have to go back to the transcripts. This is fatal for any domain where decisions need to be auditable (security, compliance, research forensics, legal).

**Why stigmergy fixes it:** A hash-chained chain-of-custody appended to a shared `coc.jsonl` file, with each entry signed by the agent's Ed25519 key, gives you forensic auditability for free. Every artifact carries a back-reference to its signed manifest entry. This is essentially the same architecture as Git's commit graph plus Sigstore — well-understood, well-tooled.

**Field evidence:** the same 2026-05-19 session demonstrated that hash-chained doc-crystallization events (`9x_coc_append_doc_crystallization.py`) make the doc-reorganization auditable end-to-end. Without it, the 100+ doc moves would have been a black box.

### 6. Adding a new agent type requires updating the orchestrator

**The bug:** Adding a new specialized agent to an Agent Teams system today requires teaching the orchestrator how to dispatch to it. The orchestrator is a bottleneck for the team's capability surface.

**Why stigmergy fixes it:** Agents self-route by reading the substrate. A new agent reads the same charter, the same mission queue, the same claim files. It joins the swarm by *showing up*; it doesn't need to be registered with anyone. Drop the agent's spawn-binary on the worker pool and it integrates automatically. This is how new ants join a colony — they don't get registered, they just start following pheromone.

## Why this is timely

I am writing this on the same day that Anthropic released Claude Opus 4.7. The model is dramatically more capable than the one I started using six months ago. Agent Teams is increasingly viable as a primary workflow. **The bottleneck is no longer model capability; it is coordination architecture.**

This is the same pattern as databases in the 1990s: the bottleneck moved from query speed (a per-node concern) to consistency model (a coordination concern). The teams that solved coordination — Spanner, CockroachDB, Aurora — built the multi-decade winners. The teams that didn't ended up with single-node systems pretending to be distributed and losing data in characteristic ways.

For AI agent teams, the coordination architecture that wins will be the one that:

1. Doesn't require a central orchestrator (no SPOF, no bottleneck).
2. Survives partial failure gracefully (subagents can die without poisoning the team).
3. Produces auditable provenance for every artifact (decisions are recoverable post-hoc).
4. Scales by adding workers, not by upgrading the manager (linear, not quadratic).
5. Has well-understood debugging and recovery semantics (any operator can read the substrate).

**Stigmergy satisfies all five.** Message-passing orchestration satisfies, at best, one (auditability, if you log every message — at the cost of #4).

## Specific implementation proposals for Agent Teams

Concrete things Anthropic could add to Agent Teams to move it toward stigmergic coordination, in increasing order of architectural commitment:

### Tier 1 — Conventions, not infrastructure

The following are zero-infrastructure additions. They could ship in a Claude Code release this quarter:

- **Claim protocol primitive:** add a built-in atomic claim-file pattern that subagents can use to lock work units. `claim_path = ".claude/claims/{id}.claim"`. Atomic-create with O_EXCL. If create fails, yield. This is 30 lines of code.
- **Mission queue convention:** designate a path (`docs/_next-missions/` or similar) that subagents scan at idle for pickup-able work units. This is the "join the colony by showing up" pattern.
- **Termination markers:** standardize a per-agent terminal-state file (`agent-{id}.done` with summary JSON). Parents read these instead of transcripts.
- **Output registry:** an append-only `_indexed-artifacts.jsonl` that every subagent appends to when it writes a durable artifact. Replaces "ask the parent what got produced" with `cat _indexed-artifacts.jsonl`.

These four conventions alone would address bugs 1, 2, 3, and 6 from the list above without any framework changes.

### Tier 2 — Substrate-level features

Modest framework additions:

- **Filesystem-event streaming:** the orchestrator can subscribe to events on the shared substrate via Server-Sent Events. When a subagent writes a claim, manifest, or done marker, the parent gets a push within seconds. This eliminates the "blind during spawn" problem. Cost: ~200 LOC plus a simple SSE endpoint.
- **Per-subagent signing keys:** auto-generate an Ed25519 keypair per spawned subagent. Every artifact write is signed. Tampering detection comes free. Cost: pynacl + key management; ~100 LOC.
- **Hash-chained ledger:** designate one file (`coc.jsonl`) as the canonical append-only chain. Every subagent action appends a signed entry with prev-sha. Provides forensic auditability matching what regulated industries already require. Cost: ~150 LOC of append+verify logic.

### Tier 3 — First-class coordination model

The most substantial change: shift the framework's mental model from "orchestrator dispatches to workers" to "workers self-route via substrate." This means:

- The parent's role becomes "charter author + observer," not "dispatcher."
- Workers run with full read-write access to a shared scratch space; coordination IS that space.
- New agent types integrate by reading the same charter, not by being registered.
- Failure recovery is "scan the substrate, resume from observable state."

This is the deepest commitment but it's also where the asymptotic wins live. Once the framework is stigmergic at its core, every additional agent makes the system stronger rather than the orchestrator weaker.

## What I built that informs this argument

For the past several months I've been building *faerie* — a stigmergic coordination framework for Claude Code and OpenHands. Faerie ships:

- A canonical chain-of-custody (`forensics/coc.jsonl`) with hash-linked, Ed25519-signed entries.
- A reputation ledger that tracks per-agent truthfulness via post-tool-use verification of file-write claims, producing measurable confabulation rates (zero, currently, on the verifiable surface).
- An archive-as-genesis primitive (`0a_genesis_recurse.py`) where forensic-tree reorganizations are themselves cryptographically committed events — you can audit the entire history including reorganizations.
- A mission-graph DAG navigated by agents via compass bearings (N=unblock, S=ship, E=parallel, W=re-baseline) plus dead-reckoning navigation. Agents read the frontier; they don't ask the queen.
- A skill registry where data-ingest skills (reconstruct-db, vision-ingest, audio-ingest, etc.) emit per-pipeline-phase COC entries that chain end-to-end, so a skeptic can verify the linkage from raw input to final artifact.
- An Obsidian plugin that closes the loop: humans annotate AI work in the vault; annotations sync to MCP; the next AI session reads the annotations as first-class steering input.

The whole system is `bash -c` plus Python plus filesystem conventions. No new infrastructure, no message broker, no orchestrator service. The faerie repo is public-research-grade and demonstrates that the pattern is implementable on the existing primitives Claude Code and OpenHands already expose.

The 2026-05-19 session in this repository is the most recent evidence that **even when faerie is not actually installed — when I improvised the pattern with plain filesystem conventions and prompt discipline** — the throughput, coverage, and auditability gains are measurable. Five parallel synthesis agents produced ~25 themed index documents in 6 minutes of wall clock. The failure modes that emerged (silent write failures, semantic collision on similarly-named themes, attribution drift) all have well-understood fixes that the full faerie install would provide.

## Why I want to work on this at Anthropic

Two reasons.

**First, the empirical case is strong but the work is unfinished.** Faerie demonstrates that stigmergic coordination produces value on top of Claude Code today, with no framework changes. The next step is making the pattern first-class — moving the conventions into the framework so every user benefits, not just users who self-build a coordination layer. That work belongs at Anthropic, not in user space. I want to do it where it ships to everyone.

**Second, I've been on the user side of Agent Teams' bugs for six months.** I have detailed reproduction cases, observed failure-mode taxonomies, and concrete proposals (above) that aren't speculative — they're drawn from running the workarounds in production. The shortest path to a great Agent Teams feature is to have the people who built the workarounds inform what gets built. I would like to be one of those people.

## The closing observation

The bug pattern in Agent Teams is the same bug pattern Wikipedia would have if it used a central editor instead of pages-as-substrate. The same bug pattern Git would have if it used a central message bus instead of commits-as-substrate. The same bug pattern ant colonies would have if they used radio signals instead of pheromone.

The fix is not exotic. The fix is *biological*. It works because the substrate is durable, observable, asynchronous, and self-healing. Agent Teams already has the substrate — the filesystem is right there. The question is whether the framework treats the filesystem as a *shared mind* or as an *output target*.

If it's a shared mind: stigmergy, robustness, scale, auditability.

If it's an output target: orchestrator bottleneck, race conditions, silent failures, transcript-archaeology debugging.

I think the choice is clear, and I think the timing is now.

---

*Supporting documents in this repository:*

- `docs/POTEMKIN-FAERIE-FIELD-REPORT.md` — forensic write-up of the 2026-05-19 ad-hoc session, with measured throughput, observed failure modes, and faerie-component-by-failure-mode mapping.
- `docs/ORCHESTRATOR-OBSERVATIONS.md` — first-person orchestrator notes from the same session, with specific tweaks.
- `docs/FOR-SKEPTICS-zero-confabulation.md` — the citability + promotion-gate model that makes the reputation/confabulation metrics auditable.
- `docs/22-AGENT-CARD-REPUTATION-SCHEMA.md` — the per-agent reputation ledger format.
- `forensics/ORGANIZATION.md` — the canonical forensic-tree layout.
- `scripts/9x_reputation_tracker.py` — the hook that verifies subagent file-write claims and writes the chain.

All of the above are real artifacts from a real working system. I'd be glad to walk through any of them in detail.
