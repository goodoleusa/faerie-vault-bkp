---
type: narrative
status: active
created: 2026-04-20
tags: [literature, stigmergy, software, multi-agent]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Stigmergy-Origins-Grasse]]", "[[Switchboard-Principle]]"]
child: []
doc_hash: sha256:e7ef0634e2b9b51341116b440248401847eef3f2465e0526f9bc6ec9a1ea9c42
hash_ts: 2026-04-20T21:59:40Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [← Origins](Stigmergy-Origins-Grasse.md) · [→ Switchboard](Switchboard-Principle.md) · [⌂ Home](../HOME.md)

# Stigmergy in Software Systems

## From Termites to Multi-Agent Software

Theraulaz and Bonabeau (1999) extended Grassé's biological stigmergy to computational multi-agent systems. Their key insight: stigmergy is not unique to biology. Any system where agents modify shared state that other agents later read implements stigmergy. The substrate doesn't matter — pheromone or filesystem entry, the coordination mechanism is the same.

Applied to software: agents read and write shared state (files, queues, databases). When an agent's write changes what another agent will do, stigmergy is operating. When agents coordinate only through direct messages, they are doing something else — and losing the persistence and asynchrony advantages that stigmergy provides.

## Why Stigmergy Beats Direct Messaging for LLM Agents

Direct messaging between LLM agents has a fundamental problem: the message exists only in context. When the receiving agent's context is reset (compaction, new session, timeout), the message is gone. The coordination was ephemeral.

Filesystem-based stigmergy persists. A manifest written during session N is still there at session N+7. The CSS metric (Cross-Session Signal Survival) exists specifically because faerie uses the filesystem as persistent coordination state — and measures whether that persistence is actually working.

Additionally, stigmergy is decoupled. A sending agent doesn't need to know which agent will read its output, or when. It writes to the expected path and exits. This is the property that enables parallel agent waves (W2/W3) to work without the main session brokering message delivery.

## The Stigmergy Spectrum in Faerie

Faerie's coordination mechanisms range from pure stigmergy to direct messaging:

| Mechanism | Type | Persistence | Faerie element |
|-----------|------|-------------|----------------|
| Manifest file at predictable path | Stigmergy | Permanent | `wave*-result.json` |
| REVIEW-QUEUE entry | Stigmergy | Cross-session | `REVIEW-QUEUE.json` |
| Broadcast droplet | Stigmergy | Session+ | `broadcast.jsonl` |
| Pollen MEM block | Stigmergy | Session | `pollen-{SID}.md` |
| SendMessage call | Direct | Context-only | `SendMessage(...)` |
| Inline spawn instruction | Direct | Spawn-only | Prompt text |

SI measures where on this spectrum a session's coordination actually falls. The goal is maximum weight at the top (permanent, session-scoped stigmergy) and minimal reliance on the bottom (ephemeral direct messaging).

## Related Metrics

- [[../00-Metrics/si/CMR-Coordination-Message-Ratio|CMR]] — direct messaging vs manifest-triggered
- [[../00-Metrics/si/CSS-Cross-Session-Signal-Survival|CSS]] — cross-session persistence
- [[../00-Metrics/si/BPR-Broadcast-Propagation-Rate|BPR]] — broadcast (mid-spectrum) propagation

**Sources:** Theraulaz, G. & Bonabeau, E. (1999). A brief history of stigmergy. *Artificial Life*, 5(2), 97–116. | Dorigo, M. et al. (2006). Ant Colony Optimization. *IEEE Computational Intelligence Magazine*.
