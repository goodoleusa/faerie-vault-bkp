---
type: narrative
status: active
created: 2026-04-20
tags: [literature, piston, waves, faerie, orchestration]
parent: "[[../_INDEX.md]]"
up: "[[_INDEX.md]]"
sibling: ["[[Switchboard-Principle]]", "[[Anti-Gaming-Bundle-Model]]"]
child: []
doc_hash: sha256:f97875b2a123258117c708f495727e96ac22fed1e6cbc0939be3c4c582bf3e88
hash_ts: 2026-04-20T21:59:40Z
hash_method: body-sha256-v1
---

> [↑ Literature Index](_INDEX.md) · [← Switchboard](Switchboard-Principle.md) · [→ Anti-Gaming](Anti-Gaming-Bundle-Model.md) · [⌂ Home](../HOME.md)

# The Piston Wave Model

## Origin

Source: `/mnt/d/0LOCAL/.claude/rules/agents.md` — faerie dispatch architecture.

Faerie organizes agent work into sequential waves, each with a defined scope, timeout, and model tier. The piston analogy: each wave is a compression stroke — work is pushed down into parallel agents, the main session waits, results return, the piston resets for the next stroke.

## Wave Structure

| Wave | Model | Timeout | Purpose |
|------|-------|---------|---------|
| W1 | Haiku | 45s | Triage, blockers, gap checks — fast and cheap |
| W2 | Sonnet | 3–5 min | Feature work, analysis, research |
| W3 | Sonnet (Opus for >200K) | Up to 30 min | Deep synthesis, court-admissible analysis |

W1 is inline-awaited — faerie waits before proceeding. W2 can be parallel. W3 runs in background (`run_in_background: true`).

## Why Waves?

Waves prevent two failure modes:

**Underparallelism:** Without wave discipline, faerie might spawn agents one at a time, waiting for each before launching the next. Waves enforce parallel launch: all W2 agents for a task set launch simultaneously.

**Overmixing:** Without wave tiers, a 45-second triage agent and a 30-minute synthesis agent compete for the same attention. Waves ensure the triage layer completes before deep work begins — blockers are resolved before resources are committed.

## Coordination Between Waves

The SI metrics measure wave-to-wave coordination quality. A healthy wave cycle looks like:

```
W1 returns manifests → faerie reads dashboard_lines (RAL < 500 tokens)
→ launches W2 parallel based on W1 findings (MPL < 1 turn)
→ W2 agents self-discover W1 manifests (SDR high)
→ W2 manifests trigger W3 chains (CD ≥ 2)
→ W3 returns → NECTAR promotion → session complete
```

When this chain holds, throughput is high and the human receives compounding value. When any link breaks, the degradation cascades.

## Teams vs Plain Agents

W2 and W3 work that has multiple parallel lanes uses teams (`TeamCreate`). W1 work and single-lane W2 work uses plain agents (`Agent(...)`). Teams carry coordination overhead — they're worth it when agents genuinely need to coordinate (share findings mid-run, avoid overlap). They're waste when work is independent.

## Related Metrics

- [[../00-Metrics/sbi/ARD-Agent-Return-Density|ARD]] — throughput across waves
- [[../00-Metrics/sbi/WCR-Wave-Completion-Rate|WCR]] — wave completion health
- [[../00-Metrics/si/CD-Cascade-Depth|CD]] — autonomous inter-wave chains
- [[../00-Metrics/si/MPL-Manifest-Pickup-Latency|MPL]] — latency between waves
