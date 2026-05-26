---
title: The Blackboard and the Comb — Two Memory Planes for Stigmergic Agent Coordination
author: goodoleusa
co-authors: [claude-opus-4-7]
date: 2026-05-26
publication_target: faerie-vault/00-Publications/coordination/
tags: [stigmergy, charter-doctrine, memory-architecture, swarmy, openhands, mission-graph, wax-seal]
status: draft-1
related_charters:
  - swarmy-ui-faerie2-backend-merge
  - hive-pair-coding-end-to-end
  - swarmy-ui-first-flight-and-deploy
related_glossary_candidates:
  - swarm_out (verb for external delivery beyond cap)
  - wax_seal (noun for agent signature artifact)
  - wax_cap (verb for the act of agent authentication)
  - comb_pattern (aggregate of wax_seals on a capped charter)
---

# The Blackboard and the Comb — Two Memory Planes for Stigmergic Agent Coordination

## Abstract

Multi-agent systems that try to use a single memory architecture for both live coordination AND sealed commitments end up either too brittle to permit mid-flight discovery or too loose to support audit. The healthy alternative — implemented in swarmy as two complementary planes — separates a **blackboard layer** (live, ephemeral, open-write, stigmergic) from a **charter signing layer** (sealed, immutable, bounded, contractual). This essay maps the architecture, names the failure modes of using either alone, and argues that the two planes are not in tension — they are two halves of one healthy memory system, separated cleanly by the `cap` event and the agent's `wax_seal`.

## 1 · The problem that names two planes

When a swarm of agents works on a complex mission, two distinct kinds of memory need to coexist. The first is **live coordination memory** — agents need to know, in flight, what their sisters are working on, where the frontier is, what claims have been laid down in the past few minutes, what discoveries have just surfaced. This memory has to be cheap to write, cheap to read, and open to anyone working in the same semantic neighborhood. Its lifetime is short; its purpose is to keep N parallel agents from stepping on each other while letting them pick up adjacent work without explicit routing.

The second is **commitment memory** — once a piece of work is done, the system needs to remember what was done, by whom, on what evidence, against which acceptance criteria. This memory has to be immutable, signed, auditable, and structurally legible by future agents (and humans) reading the record cold. Its lifetime is permanent; its purpose is to be the receipts when someone asks "did we ever actually ship that?" or "who approved this?"

A naive design conflates the two. Either every scratch note gets cryptographically sealed (which makes mid-flight discovery prohibitively expensive — every reroute means a new signed contract) or every commitment lives as a mutable note (which means there's no audit trail and no defense against silent rewrites). The swarmy stack avoids the trap by having both planes — the **blackboard** for live coordination, the **charter signing layer** for sealed commitments — and binding them together with one well-defined transition: the `cap` event.

## 2 · The blackboard: live, ephemeral, stigmergic

The blackboard layer in swarmy lives under `swarm/{date}/ephemeral/{task_id}/`. Anyone can drop a marker there. Scratch ambrosia (the in-progress substance), waggle traces (behavioral signals about what an agent is currently doing), claim markers ("I am working on mission X right now"), in-flight `discovered_work[]` entries with N/S/E/W bearings — all of it lives on the blackboard.

The coordination model is **stigmergic**. There is no central dispatcher. Agents don't call each other; they leave traces in the shared environment. Sister agents read those traces and decide independently whether to pick up adjacent work, race-claim a frontier task, or stay focused on their current scope. The bee metaphor is precise: stigmergy is what happens on the dance floor at the hive entrance, where returning foragers waggle directions and other bees decide on their own whether to fly out toward those flowers.

Two properties make the blackboard scale horizontally:

**(a) Density-based clustering without external coordination.** Missions are addressed in a what.three.words-style three-dotted format (`tenancy.scope.isolation`, `hive.pair.bee`). Two missions sharing one dotted term are neighbors *by definition*; sharing all three means they're the same mission. The adjacency formula is `|terms_a ∩ terms_b|`. Agents working on `tenancy.scope.isolation` and `tenancy.role.scoping` discover they're working in the same neighborhood without anyone routing them — the shared `tenancy` term IS the coordination signal. Density-of-traces along the mission graph becomes the live-system pulse.

**(b) Open-write namespaced by mission.** Every blackboard marker carries its mission address. Writes from `tenancy.scope.isolation` agents don't conflict with writes from `hive.pair.bee` agents, even if both are happening in the same blackboard directory. The same blackboard can serve a fairly large, diverse team working on different or overlapping missions, because the mission term is the partition key. There is no need to spin up per-mission scratch areas.

The blackboard's failure mode if used alone is **lack of accountability**. Anyone can write anything. There's no acceptance gate, no audit trail, no defense against an agent silently overwriting a sister's claim. If the only memory plane is the blackboard, the system has no answer to "did we ever actually finish that?" or "who approved this?"

## 3 · The charter signing layer: sealed, immutable, contractual

The charter signing layer lives under `forensics/charters/active/` (and `forensics/charters/sealed/` once a charter is fully capped). A charter is a **commissioning document** — a contract between a commissioner (a user, or a parent agent) and one or more agents authorized and spawned to perform the work. The charter specifies scope, acceptance criteria, out-of-scope items, and a phase breakdown. Each phase is satisfied by one or more capped manifests, each carrying a `wax_seal` from the agent that produced it.

The metaphor is the comb pattern in finished honeycomb. Each capped cell carries a tactile, visible wax cap; the aggregate mosaic of caps across a frame is the comb pattern, and that pattern is the colony's evidence that the season's foraging actually happened. In the charter signing layer, each capped manifest carries its agent's wax_seal (cryptographic signature — sigstore-keyless OIDC or GPG); the charter's `comb_pattern` is the aggregate of all wax_seals on manifests claiming that charter.

Three properties make the charter signing layer scale vertically:

**(a) Bounded authorization.** Only agents authorized at spawn time can claim work against a charter's phases. The commission is a contract; the wax_seal is the proof of work and identity. Random write access is prohibited by construction.

**(b) Immutable wax_seal on each capped manifest.** Once an agent caps a manifest with their wax_seal, that record is permanent. The `cap` event triggers promotion from `ephemeral/` to `manifests/`, hash-chain entry to `coc.jsonl`, and signature application. Re-running the same work produces a new manifest with a new wax_seal — the old record is not edited. This is what makes the charter layer auditable.

**(c) Acceptance criteria as the contract.** The charter specifies what "done" looks like in operational prose. Acceptance is verified against the comb_pattern: are all phases populated with capped manifests that meet their criteria? The charter's `derived_rollup_status` transitions from `frontier` (no manifests yet) to `uncapped` (some phases capped, others not) to `capped` (every phase has at least one capped manifest meeting its acceptance gate). This rollup is a pure function of the manifest set; it doesn't require manual marking.

The charter signing layer's failure mode if used alone is **rigidity that prevents discovery**. Every reroute requires a new charter or a charter amendment with its own signing event. Mid-flight discoveries — the kind that happen when an agent spots better adjacent work — can't be recorded cheaply, so they don't get recorded at all, and the system loses the emergent intelligence of its own swarm. If the only memory plane is the charter layer, the system becomes brittle: it can audit what it committed to, but it can't tell you what it learned along the way.

## 4 · The transition: the `cap` event

The two planes are bound together by a single well-defined transition. When an agent decides their work is complete — when they reach a `lifecycle_judgment` of `seal` (faerie2-native) or `cap` (swarmy-ui canonical) — the following happens, atomically:

1. The work product crystallizes from `ephemeral/{task_id}/` scratch into a canonical manifest at `swarm/{date}/manifests/`.
2. The agent's `wax_seal` (sigstore-keyless or GPG signature over the manifest bytes) is attached.
3. The manifest's hash is appended to `coc.jsonl`, chained to the previous entry's `this_hash` via `prev_hash`.
4. Any `discovered_work[]` entries the agent surfaced are finalized — no more edits after `cap`.
5. The charter rollup re-runs: the manifest's `charter_id` field tells the rollup which charter just gained a capped manifest. The charter's `comb_pattern` grows by one wax_seal. The charter's `derived_rollup_status` re-derives from the new manifest count.

After the `cap` event, the manifest is in the charter signing layer. The agent has crossed from blackboard to comb. Their wax_seal is permanent. The discovered_work they surfaced is also permanent, but it lives as **frontier markers for the next wave** — it's part of the past tense of the blackboard, not the present tense. New agents reading the discovered_work see it as commissionable scope, not as in-flight activity.

This is what it means to say *the charter is the past tense of yesterday's blackboard*. Every charter is, in its origin, a snapshot of what the live blackboard surfaced as worth committing to. Every blackboard, at any moment, is the open superset of what might next become charter-grade.

## 5 · Practical guidance — when to reach for which

The two planes serve different needs at different scopes. The table below maps common agent intentions to the correct plane:

| You want to... | Reach for... | Why |
|---|---|---|
| Find adjacent missions in flight | Blackboard | Read manifest dir + mission-graph density. Stigmergic adjacency is computed in-browser. |
| Race-claim a frontier task | Blackboard | Write a claim marker. Check stigmergic conflict via adjacency. No central registry needed. |
| Surface discovered work | Blackboard | `discovered_work[]` entries with N/S/E/W bearing. Lives on the in-flight manifest until cap. |
| Check what sisters shipped | Blackboard | Read recent manifests + `dashboard_line` (≤80 chars). Cheap survey of session state. |
| Pivot mid-flight to a better path | Blackboard | New discovered_work entry; possibly trigger a new charter at next wave. NOT a charter amendment. |
| Make a binding commitment | Charter | Explicit scope + acceptance criteria + signed authorization for spawned agents. |
| Tell future you what was DONE | Charter | The comb_pattern of capped manifests with wax_seals. Read-only audit surface. |
| Audit who decided what when | Charter | Signed immutable record + COC hash chain. Forensic-grade. |
| Hand off to a new wave | Charter | The new wave's commission becomes their charter. Spawning agents are authorized against it. |

A simpler heuristic: if you would be uncomfortable having no record of this in five years, it belongs in the charter layer. If you would be uncomfortable forcing a signature event for every tiny reroute, it belongs on the blackboard.

## 6 · Why the metaphor matters — bees got there first

The blackboard / comb distinction maps with surprising fidelity to a real bee colony's two memory architectures. Bees coordinate live activity via two stigmergic channels: pheromone trails on the dance floor and chemical markers on individual cells. Forager bees returning with new nectar sources waggle-dance the direction and quality of the find; other bees decide independently whether to fly out. This is the blackboard — open-write, ephemeral, density-based, no central dispatcher.

Bees record commitments via the comb. Each cell is built by workers, filled with honey or brood, and then capped with wax once it's complete. The wax cap is the visible, tactile evidence that this cell is finished. A frame of capped comb is the colony's commitment record — a beekeeper inspecting a frame can tell at a glance how much of the season's foraging was successful, where the laying patterns are, what the colony has actually achieved versus what it set out to do. The comb does not change once capped. New cells are built around it.

Calling our two planes the blackboard and the comb isn't decoration. It's reaching for a well-tested biological coordination architecture and saying: this is the shape we're after, this is why it works, this is why neither alone would scale to a real swarm.

## 7 · Implications for the UI

The hive view (`hive.retrofuture.tech`) presents both planes simultaneously, in different surfaces:

- **The Graph tab** is the blackboard visualization. Force-directed mission clustering driven by stigmergic adjacency (term-overlap). Real-time. Updates as new manifests land. No authoritative routing rendered — the topology emerges from the data alone.
- **The Charters tab** is the charter signing layer. Capped commitments, wax_seal verification per agent, comb_pattern aggregation per charter, COC hash chain with prev/this/next clickable. Static snapshot, but with hash links that resolve into live blackboard state for in-flight references.
- **The Activity Feed** (always-on collapsed sidebar) is the blackboard's live ticker. Every cap event, every discovered_work surfacing, every claim marker flows through here as a server-sent event. The feed is the system's heartbeat.
- **The Eval tab** sits between the two planes — it shows the conceptual formulas (stigmergic adjacency, mutation discipline, charter rollup status) and the live measurements from the corpus. This is where the two planes are reconciled as evidence.

An operator using the hive UI is, at any given moment, looking at both planes. The blackboard tells them where activity IS; the charter layer tells them what activity HAS BEEN. Together they tell them what the swarm is becoming.

## 8 · Conclusion

The trap of treating a multi-agent system's memory as one undifferentiated store is real. Systems that conflate live coordination with sealed commitment either become too brittle for discovery or too loose for audit. The two-plane architecture — blackboard for stigmergic coordination, charter signing layer for sealed contracts — solves both problems by separating them at the right seam: the `cap` event and the agent's `wax_seal`.

Calling these planes the blackboard and the comb is metaphor doing real work. It encodes which writes are open and which are bounded, which records decay and which are permanent, which coordination is indirect-via-traces and which is direct-via-contract. The metaphor is consistent across the swarmy-ui glossary (`cap`, `capped`, `uncapped`, `frontier`, `ambrosia`, `wax_seal` candidate, `comb_pattern` candidate) and provides a stable substrate for future term decisions.

The healthy system uses both. The charter is the past tense of yesterday's blackboard.

---

## References

- swarmy-ui canonical glossary: `swarmy-ui/docs/GLOSSARY.md`
- Vocab translation seam: `swarmy-ui/server/vocab_adapter.py`
- Glossary merge candidates (proposed terms): `swarmy-ui/docs/GLOSSARY-MERGE-CANDIDATE.md`
- Charter doctrine origin: `forensics/charters/active/2026-05-25Z__charter__swarmy-ui-faerie2-backend-merge`
- Completion choice canonical set (lifecycle_judgment + free_choice, 19 kinds): `.agents/skills/completion-choice/CANONICAL-SET.md`
- python-pro agent card (MAKER archetype with sandwich + forage rhythm): `swarmy-ui/.agents/agents/python-pro.md`
- Mission-graph API endpoint: `swarmy-ui/server/app.py` `_handle_graph`
- Force-directed mission visualization: `swarmy-ui/graph.jsx`

## Provenance

This essay was written during the 2026-05-26 merger session that consolidated faerie2's backend substrate into swarmy-ui. The two-plane framing emerged as the operator's question — "what's the difference between the blackboard method and the charter signing method, is it one or the other or is the blackboard truly better for scratch stigmergy?" — was answered live in the session. The session's full COC chain is recorded under `forensics/coc.jsonl` and `swarm/2026-05-26/coc.jsonl` respectively. Co-authorship is by `goodoleusa` (operator + commissioner) and `claude-opus-4-7` (agent voice; rendered the architecture).
