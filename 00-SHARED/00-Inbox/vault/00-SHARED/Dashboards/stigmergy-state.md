---
type: dashboard
status: active
tags: [dashboard, stigmergy, autonomy, emergence, droplets]
parent: Dashboards/INDEX
up: Dashboards/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:d916b6addd8c3bedb98be61df5d60969c1939b2dbd967fc3186bf1e809ce7fdc
hash_ts: 2026-04-25T01:10:53Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](INDEX.md) · [⌂ Home](../../HOME.md)

# Stigmergy State

Narrative for understanding autonomy, discovery chains, droplet activity, and emergence.
For live data: `python3 ~/.claude/scripts/9x_lean_query.py --get-stigmergy`

---

## What Stigmergy State Measures

Stigmergy state captures how well the system is self-coordinating —
agents discovering each other's work without main orchestration.

Key metrics:
- **Autonomy %** — % of inter-agent handoffs happening via filesystem vs human direction
- **Discovery chains** — sequences of tasks where T+1 discovered T without faerie
- **Droplet count** — insights written during this session available for discovery
- **Emergence signals** — patterns of follow-on task generation from next_task_queued

---

## Reading Stigmergy State

```bash
python3 ~/.claude/scripts/9x_lean_query.py --get-stigmergy
# Output: autonomy:86%  chains:3  droplets:4  emerged:2
```

---

## Healthy vs Degraded Stigmergy

**Healthy (autonomy ≥ 75%):**
- Agents are discovering predecessor work via `grep -r "_{task_id}_" forensics/`
- `next_task_queued` in manifests is creating follow-on tasks automatically
- Droplets from W1 agents are being read by W2 agents at task boundaries

**Degraded (autonomy < 50%):**
- Agents are being given explicit paths to predecessor work (main relaying)
- `next_task_queued` field is absent from manifests
- Droplets are not being written or discovered

---

## Improving Stigmergy

| Problem | Fix |
|---------|-----|
| Agents not discovering predecessors | Ensure task_id appears in forensics filenames |
| next_task_queued not being set | Check manifest template includes the field |
| Droplets not being written | Check agent prompt includes droplet protocol |
| Low autonomy % | Check if main is relaying requirements (anti-pattern) |

---

## Emergence Pattern

Healthy emergence: tasks generate tasks. The backlog grows from agent discoveries,
not from human direction.

```
Task T1 completes → agent writes next_task_queued: T2
T2 claims → agent writes next_task_queued: T3
...

Result: a chain of discoveries driven by agent output, not human planning
```

This is the f(0) ideal — the work graph builds itself from agent findings.

---

## Related

- [[../Hive/stigmergic-recursion]] — the coordination model explained
- [[../Hive/staged-chain-stigmergy]] — how chains form
- [[../Architecture/forensic-integrity]] — how forensics/ enables discovery
- [[../Glossary/terms]] — stigmergy, autonomy, emergence defined
