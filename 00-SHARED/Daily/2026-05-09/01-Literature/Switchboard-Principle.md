---
type: narrative
status: active
created: 2026-04-20
tags: [literature, switchboard, faerie, delegation]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Stigmergy-in-Software-Systems]]", "[[Piston-Wave-Model]]"]
child: []
doc_hash: sha256:cc404c9c07dc0e5cd7c1ef28c8eea3e36c9a8014b0fd91a630b97ba11ed0f8b0
hash_ts: 2026-04-20T22:04:26Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [← Stigmergy](Stigmergy-in-Software-Systems.md) · [→ Piston](Piston-Wave-Model.md) · [⌂ Home](../HOME.md)

# The Switchboard Principle

## Origin

Source: `/mnt/d/0LOCAL/.claude/CLAUDE.md` — core faerie operating principle.

The main session is a switchboard. A switchboard does not do the calls — it routes them. The person at the switchboard does not solve the caller's problem; they connect the caller to the person who can. The moment the switchboard operator starts solving problems, the board jams.

Applied to faerie: the main session reads user intent, identifies the right agent(s), assembles the spawn prompt, launches, and waits. It does not reason through the problem, draft the analysis, or synthesize what the agent should synthesize. Those are agent tasks.

## The Economic Argument

Every token the main session spends on reasoning is a token not spent routing. At 8K tokens of main-session reasoning per agent return, a 10-agent session burns 80K tokens of coordination overhead. At 500 tokens per return (target RAL), the same session burns 5K tokens of overhead — a 16× cost reduction, and a qualitative improvement in scalability.

More importantly: the main session has a finite context window. An aggressive routing discipline (spawn fast, stay lean) preserves that window for routing many more waves. A reasoning-heavy main session hits the context ceiling after 3–4 waves. A lean switchboard can sustain 20+ waves without compaction.

## What It Requires

The principle is simple; the discipline is not. Faerie must resist three temptations:

1. **The planning temptation:** "Let me think through this before I delegate." The thinking belongs in the agent.
2. **The synthesis temptation:** "Let me summarize what the agent found before I decide next steps." The summary belongs in the next agent.
3. **The validation temptation:** "Let me verify the agent's output before trusting it." Trust is the default; flag for investigation only when something specifically looks wrong.

SBI measures adherence to this discipline. IRR catches temptation 1. SPX catches temptation 2. RAL catches temptation 3.

## Related Metrics

- [[../00-Metrics/SBI-Switchboard-Index|SBI]] — composite switchboard health
- [[../00-Metrics/sbi/IRR-Inline-Reasoning-Ratio|IRR]] — deliberation before spawning
- [[../00-Metrics/sbi/SPX-Switchboard-Purity-Index|SPX]] — fraction of session that is spawn events
- [[../00-Metrics/sbi/RAL-Return-to-Action-Latency|RAL]] — speed of action on agent returns
