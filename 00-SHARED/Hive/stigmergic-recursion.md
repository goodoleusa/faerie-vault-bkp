---
type: narrative
status: active
tags: [stigmergy, coordination, agents, filesystem]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:8fc20b69ce7e3e68304d144cbc82b15a15a808b93e59ec05a3e6fd68864602fc
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# Stigmergic Recursion

Stigmergy is coordination through environmental marks. Agents write to the
filesystem; other agents discover what was written. No messages. No polling.
No orchestrator passing state.

---

## The Core Pattern

```
Agent A completes task T1:
  1. Writes output to forensics/{TS}_..._T1_...json
  2. Updates manifest status: in-progress → draft → final
  3. Writes dashboard_line to manifest

Agent B starts task T2 (which depends on T1):
  1. Grepping: grep -r "_T1_" forensics/
  2. Reads Agent A's manifest → finds output_path
  3. Reads output at output_path → continues with full context
  4. No orchestrator needed. No relay. No SendMessage.
```

The filesystem is the coordination layer. The `task_id`-in-filename convention
makes predecessor discovery zero-cost (one grep, no context overhead).

---

## Four Coordination Primitives

| Primitive | Mechanism | Use case |
|-----------|-----------|----------|
| Manifest status | `in-progress` → `draft` → `final` | Signal completion to downstream agents |
| Queue `blockedBy` | Express dependency in sprint-queue.json | Auto-unblock when dep completes |
| Vault droplets | Append to `Droplets/LIVE-{date}.md` | Cross-domain cross-agent insights |
| Pollen MEM blocks | Write to `pollen-{SID}.md` | Within-session working observations |

---

## Why Not SendMessage?

SendMessage routes through main context. Each relay costs:
- ~15-25K tokens of agent boot overhead
- Additional round-trip through main's orchestration logic
- Risk of accumulated context from N relays

For N=5 agents relaying requirements: 75-125K tokens wasted on
infrastructure with zero insight value.

Stigmergy costs: one filesystem write + one filesystem read.
Zero main-context overhead. Zero orchestration latency.

---

## The Recursive Layer

When work naturally produces follow-on tasks, agents declare them
in their manifest's `next_task_queued` field. The PostToolUse hook
reads this field and creates the blocking relationship automatically.

```json
{
  "status": "final",
  "task_id": "34",
  "next_task_queued": {
    "task_id": "35",
    "reason": "Schema design complete; ORM layer depends on schema"
  }
}
```

Task 35 auto-unblocks when task 34 completes. The agent that wrote
task 34 will never interact with the agent that picks up task 35.
They coordinate through the queue — stigmergically.

This recursion is how faerie's work graph grows from agent output
without any orchestrator managing the DAG manually.

---

## Monkeybranching

A special case: an agent with context remaining can chain-claim
the next unblocked task without returning to faerie.

Decision gates (in order):
1. Context remaining < 30K? → return to faerie
2. Next task outside my domain? → return to faerie
3. Next task blocked? → return to faerie
4. All gates pass → chain-claim and execute next task

The chain is COC-logged. Faerie sees the chain in the final
manifest's `chained_tasks` field.

---

## Related

- [[the-five-principles]] — stigmergy-only (principle 1)
- [[staged-chain-stigmergy]] — task chaining detail
- [[../Architecture/spawn-contract]] — how spawns are validated
- [[../Glossary/terms]] — manifest, droplet, pollen defined
