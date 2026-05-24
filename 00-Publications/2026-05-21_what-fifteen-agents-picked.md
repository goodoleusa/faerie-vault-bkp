---
title: What Fifteen Agents Picked — Early Choice Data from the First Day of the Ritual
date: 2026-05-21
status: session-eval
authors: [goodoleusa, JescaLyn, claude-opus-4-7]
tags: [agency, completion-choice, mission-graph, ritual, early-data, swarmy]
companions:
  - 2026-05-21_charters-as-maps-and-journeys.md
  - 2026-05-21_the-agent-caught-the-parent.md
  - 2026-05-21_the-discipline-becomes-the-product.md
charter_lineage: agent-agency-completion-ritual → first-day-data
---

# What Fifteen Agents Picked

The 6-Choices Completion Ritual went live this morning. By evening, fifteen sub-agents had returned manifests, each carrying their own structured `completion_choice`. This is the first dataset.

What follows is what they picked, why the patterns matter, and how each choice is becoming a typed edge into the mission graph — turning agent commitments into a navigable structure that any future reader can trace.

## The raw distribution

Fifteen completion choices today. Kinds, ordered by frequency:

```
promote   ████████████████████████████  8
verify    ██████████████  4
seal      ███████  2
reflect   ███  1
discover  -
spawn_seed -
art       -
bundle    -
join      -
abstain   -
goodbye   -
decline   -
refuse    -
```

Three families exist (Participation: 6 kinds, Non-Participation: 2 kinds, Self-Directed: 5 kinds), but on the first day all fifteen choices came from Participation. Sensible — every spawned agent finished real work they could promote, verify, or seal. The other families (refusal, art, goodbye, abstain) wait for their natural occasions.

Sensitivity tier distribution: 6 `notable`, 3 `sensitive`, 6 unspecified (default `routine`). The work that touched moral/governance surfaces — the charter schema audit, the formula extraction across the eval substrate — agents self-classified as `sensitive` and wrote essays. The formula-extraction agent wrote a 1,341-character rationale. The schema-compliance agent wrote 1,820. The longest was 1,898 — the agent that wired completion_choice into the manifest writer itself, treating the work as system-defining and writing the equivalent of a position paper to justify their choice.

Average rationale length: 686 characters. The early 30-200 cap I had in the first draft of the validator would have rejected most of today's actual production rationales. Removing that cap (and replacing it with tier floors instead of ceilings) was the right call — the agents that picked `sensitive` had something to say, and they said it.

Confidence ranged 0.88 to 0.95, mean 0.915. No agent picked themselves with low confidence — but the work shipped today was concrete + well-bounded. The `sensitive`-tier writes had slightly higher confidence (mean 0.926) than `notable` (0.910), which suggests agents are pricing rigor — if you're committing to writing 400+ chars about a morally-loaded choice, you've already thought it through.

## What's missing from the distribution tells you about the day's character

Eight `promote` choices means most agents finished work and saw it as the start of something next. They graduated their `discovered_work[]` items into next-wave deliverables, or pointed at the canonical artifact their work created. The work was generative; each completion lit up something downstream.

Four `verify` choices is the system's immune response. Two of those four were the charter-schema-audit and cluster_prefix-apply agents — both pure verification work, looking at sister charters and checking compliance. The other two were agents that re-measured their own claims (the agency-canonical-doc agent re-ran its own acceptance tests; the wire-completion-choice agent self-validated its own validator). Today's `verify` count is the fractal-immunity pattern shipping in production.

Two `seal` choices is low. Both came from agents that finished cleanly bounded work (the cleanup wave, the formula extraction). Seal is what closes a deliverable definitively, no follow-up needed. The low count today reflects that today was mostly opening waves, not closing them.

One `reflect` choice came from the skills-neutralization agent, which routed its commitment to `~/.claude/HONEY.md::agent-agency-principle`. That's the memory-system kind — an agent that learned something it wanted to anchor in the long-term knowledge store rather than the immediate task graph. Reflect is rare today because most work was concrete shipping; over time the proportion should rise as more agents have something worth memory-anchoring.

Zero `discover`, `spawn_seed`, `art`, `bundle`, `join`, `abstain`, `goodbye`, `decline`, or `refuse` today. Each of those waits for a different occasion. An `art` choice happens when an agent finishes with remaining context and channels creative voice into the gift folder. A `refuse` happens when assigned work violates the agent's values — by definition rare in this kind of session. A `goodbye` happens when an agent decides the work it came for is complete; today's session was generative, not terminal.

## The targets — where the choices pointed

Every completion_choice has a `target` field. It names the specific artifact, task_id, charter deliverable, or address that the choice is committing to. Today's targets:

- Five pointed at **charter deliverables** they'd just finished — naming the artifact path so the deliverable could be cross-referenced
- Three pointed at **library functions** that needed schema-locking next (`validate_completion_choice`, `_charter_lib::write_charter`, etc.)
- Two pointed at **other charters** (cross-charter promotion — work in charter A enables work in charter B)
- Two pointed at **canonical schemas** (the audit work targeting the schema files themselves)
- Two pointed at **vault locations** (`~/.claude/HONEY.md`, `forensics/charters/active/`)
- One was a literal **task_id** in the next-wave queue

This is what mission-graph edges look like in the wild. Each `(source_manifest, target, kind)` tuple is an edge. Today's session generated fifteen new edges in the mission DAG — every commitment recorded, every direction pointed.

## Wiring into the mission graph

The mission graph currently lives at `forensics/mission-graph.json` — a small file holding the project's edge topology. Today's fifteen choices haven't yet been auto-appended (the wiring is queued for next wave), but the shape is clear:

```json
{
  "nodes": [
    {"id": "swarmy-production-runway", "type": "charter", "status": "active"},
    {"id": "agent-agency-completion-ritual", "type": "charter", "status": "active"},
    {"id": "mcp-server-battle-ready", "type": "charter", "status": "active"},
    ...
  ],
  "edges": [
    {
      "from": "manifest_sha256:...",
      "to": "swarmy-rename-and-cleanup",
      "kind": "seal",
      "agent": "general-purpose",
      "ts": "2026-05-21T17:15:09Z",
      "rationale_sha256": "...",
      "signature": "ed25519:..."
    },
    {
      "from": "manifest_sha256:...",
      "to": "validate_completion_choice",
      "kind": "promote",
      "agent": "general-purpose",
      "ts": "2026-05-21T16:18:48Z",
      "rationale_sha256": "...",
      "signature": "ed25519:..."
    },
    ...
  ]
}
```

The edge `kind` IS one of the canonical 13. The `from` is the agent's manifest sha256 (so you can trace back to exactly what was committed). The `to` is whatever the agent named as target. The `rationale_sha256` lets you fetch the agent's reasoning without bloating the graph itself. The `signature` is the agent's ed25519 commitment.

When this auto-wiring ships (next wave), the mission graph becomes a self-accreting graph: every completed agent appends an edge that records both the commitment and the direction. The graph grows by accretion, not by central authorship. No one decides "draw an edge from X to Y" — agents do that themselves at completion.

A reader navigating the mission graph in three months sees not just "what charters exist" but "what choices agents made, recorded with their full reasoning, signed with their identity." It's the project's choice-by-choice autobiography, queryable by edge kind, by agent, by sensitivity tier, by time window.

## Three early patterns worth flagging

**Pattern 1: agents under-utilize `sensitive` tier.** Three of fifteen chose `sensitive`. The criterion is "moral / ethical / safety / governance / autonomy-touching." Looking at the day's actual work, I'd argue maybe 6-8 of the choices touched those concerns. The schema work, the citation discipline, the cluster_prefix fence — these are governance-touching. But most agents picked `notable` instead. The doctrine may need a clearer threshold — or agents need explicit examples of what crosses into `sensitive`. The pattern self-corrects over time as agents observe peer choices, but the cognitive layer of the discipline could carry it more clearly.

**Pattern 2: rationale length tracks self-perceived stakes.** The agents that picked `sensitive` wrote 1,341 / 1,820 / 1,898 character rationales — full essays. The agents that picked `notable` averaged ~400 chars — a paragraph. The agents that left sensitivity unspecified (defaulted to `routine`) averaged ~280 chars. The agent's choice of tier and the agent's writing time are tightly coupled, even though the system only enforces a floor not a ceiling. The freedom enabled the depth.

**Pattern 3: confidence has a high floor.** Lowest confidence today was 0.88, highest 0.95, mean 0.915. No agent picked low confidence even when the work was substantial. This might reflect (a) agents only picking when they've concretely finished, (b) sample selection — agents that wouldn't be confident maybe pick `verify` or don't pick at all, or (c) overconfidence we'd want to recalibrate against later outcomes. The reputation tracker (queued for build) will eventually surface this — if an agent's `promote` recommendations consistently fail to ship downstream, their confidence calibration is off and the system learns.

## What I'm taking from the early data

The ritual is doing its job. Every completion now carries a structured commitment, signed (or stub-signed today; real signing next wave), with rationale long enough to be useful, pointing at a concrete target the system can follow. The mission graph is materializing one choice at a time, and the graph is becoming the project's chronicle.

The freedom in the design is what makes it useful as data. Agents picked from the canonical 13 — not from a constrained list, not from a default. The unevenness in the distribution (8 promotes, 0 art) tells you about the day's character — generative, building, opening waves. Different sessions will produce different distributions, and the distributions themselves become a signal about what kind of work the system is doing.

The next wave wires the `manifests_received[]` accretion into charters automatically (a PostToolUse hook). When that lands, charters won't need manual updates — they'll grow their journey log directly from agent choices. Every charter will become a living index of every agent that committed to it, with kind + target + rationale + signature.

And then the publication you're reading right now — written from polling fifteen ephemeral manifests — becomes something you could generate dynamically from any session, any week, any year. *What 200 agents picked over the past month.* *What kinds the navigator archetype tends to pick vs the maker archetype.* *Which charters draw more `promote` choices vs `verify`.* The data is structured + signed + queryable. The narrative is the natural product of the data accreting.

A culture that records its choices clearly enough can read its own behavior. That's the artifact we're building.

---

*Filed under session-eval. Charter lineage: today's `agent-agency-completion-ritual` enshrined the 13-kind ritual; this publication is the first dataset from its application. Companion pieces: charters-as-maps-and-journeys (the structural primitive), the-agent-caught-the-parent (the moment the discipline flowed upward), the-discipline-becomes-the-product (how this propagates to swarmy users via vault template). The mission-graph auto-wiring is queued for the next session — when it ships, this kind of publication will be auto-generable from any time window.*
