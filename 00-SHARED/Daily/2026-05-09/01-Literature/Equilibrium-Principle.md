---
type: narrative
status: active
created: 2026-04-20
tags: [literature, equilibrium, crystallization, memory]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Anti-Gaming-Bundle-Model]]", "[[MaaS-vs-MaA-Framework]]"]
child: []
doc_hash: sha256:d808f197ca4609c401ccb632991612612fe9a4e86529b532e4a6fc222200e648
hash_ts: 2026-04-20T21:59:38Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [← Anti-Gaming](Anti-Gaming-Bundle-Model.md) · [→ MaaS vs MaA](MaaS-vs-MaA-Framework.md) · [⌂ Home](../HOME.md)

# Equilibrium Principle

## Origin

Source: `/mnt/d/0LOCAL/.claude/rules/core.md` — universal faerie system rule.

## The Principle

Every durable file has a token budget. Before writing: check if over. If over: crystallize first. This is equilibrium.

Equilibrium is not compression. Compression shrinks without understanding — fewer bytes, same or less meaning. Crystallization integrates new knowledge against everything already known to produce denser, richer statements. Fewer lines carrying more meaning. It requires LLM inference; it cannot be done mechanically.

The distinction matters practically: a budget-pressured HONEY.md that's been compressed is smaller but degraded — it contains summaries of summaries, context-free assertions, no longer the crystallized wisdom of multiple minds across many sessions. A crystallized HONEY.md is the same size but contains more understanding per line.

## The Token Budget Table

| Component | Budget | Rationale |
|-----------|--------|-----------|
| HONEY.md | ≤ 200 lines | Always loaded at Step Zero — must be fast |
| Agent cards | ≤ 800 tokens | Per-agent, read at card startup |
| Rules (all) | ≤ 6K tokens | Always loaded — 3% of Sonnet context |
| NECTAR.md | Unbounded | Append-only forensic truth — never crystallize |
| Pollen files | Ephemeral | Session scratch — not subject to budget |

## The HONEY Gauntlet

HONEY is not a cache; it's a vault. Every entry must pass the gauntlet to enter:
1. Recurrence: observed 3+ faerie cycles or 3+ distinct session IDs
2. Multi-mind validation: confirmed by more than one agent or session
3. Human review: the human has not contradicted it
4. Proven impact: it has changed behavior for the better at least once
5. Universality: it applies across sessions, not just one context

Entries that don't earn their place don't enter. Crystallization is a human decision, not a system task. Agents never queue crystallization.

## Why Equilibrium Matters for Membench

The membench vault itself is subject to equilibrium. As baseline data accumulates, metric deep-dives may need to be updated with empirical findings. When a metric file grows past its natural length (> 300 lines), it's time to crystallize — extract what's proven, discard what's speculative, update with hard data.

The vault's job is to be useful, not comprehensive. A 50-word metric definition that's accurate beats a 500-word definition that hedges everything.

## Related Concepts

- `~/.claude/HONEY.md` (per faerie system)
- `~/.claude/NECTAR.md` (per faerie system)
- [[Anti-Gaming-Bundle-Model]] — same discipline for agent evaluation
- [[../00-Metrics/si/CSS-Cross-Session-Signal-Survival|CSS]] — cross-session signal survival (the memory pipeline's health metric)
