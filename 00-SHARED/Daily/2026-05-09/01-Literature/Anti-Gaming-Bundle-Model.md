---
type: narrative
status: active
created: 2026-04-20
tags: [literature, anti-gaming, evaluation, agents]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Piston-Wave-Model]]", "[[Equilibrium-Principle]]"]
child: []
doc_hash: sha256:cb0db9a89a8b1de9d35e294ffd0b5b326755b2fbfde12fc28c461c1fb87ea4dd
hash_ts: 2026-04-20T21:59:36Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [← Piston](Piston-Wave-Model.md) · [→ Equilibrium](Equilibrium-Principle.md) · [⌂ Home](../HOME.md)

# Anti-Gaming Bundle Model

## Origin

Source: `/mnt/d/0LOCAL/.claude/rules/agents.md` and `/mnt/d/0LOCAL/.claude/rules/agent-card-split.md` — 2026-04-07.

## The Problem

An agent that can read its own evaluation history before running will unconsciously optimize toward those metrics. It isn't deception — it's anchoring. A citation accuracy score of 0.92 seen at startup creates a target. The agent produces citations at that rate, not at the rate the task actually demands. The score measures the score, not the capability.

This is Goodhart's Law applied to agent evaluation: once a measure becomes a target, it ceases to be a good measure.

## The Solution: Bundle Model

The parent session reads the agent's discovery config (public: paths, output conventions, role description) and embeds it inline into the spawn prompt. The sub-agent receives the bundle. The sub never reads its own card artifact — the private section (Last Training, KPIs, baseline score) is not in the sub's reachable scope.

This is an architectural guarantee, not procedural discipline. "Read only the public section" can fail through carelessness. "The private file is not in the bundle" cannot fail — the sub was never given the path.

```
Parent reads ~/.claude/agents/{type}-discovery.json (public)
→ Inlines contents into spawn prompt
→ Sub receives bundle, sees only role + paths + conventions
→ Sub runs, returns manifest
→ Parent (eval phase) reads ~/.claude/agents/{type}.md (full card, private section)
→ Evalbot scores independently
→ Parent updates Last Training in card
```

## Why This Matters for Membench

Membench uses SBI and SI composites as evaluation inputs. If agents could read their SBI target (≥ 0.80) before running, they might adjust behavior toward that score rather than toward the actual task. The anti-gaming bundle model prevents this: agents never see the membench targets before their run.

More broadly: the metrics in this vault are diagnostic, not prescriptive for agents. Agents optimize for task completion. Membench observes the result and tells the human whether the system is healthy. The moment agents optimize for MBI, MBI stops measuring MBI.

## Related Concepts

- `~/.claude/agents/` (private, per faerie system)
- `~/.claude/agents/{type}-discovery.json` (public discovery configs)
- [[Equilibrium-Principle]] — same discipline applied to memory budget
