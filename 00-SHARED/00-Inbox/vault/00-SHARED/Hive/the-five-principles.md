---
type: narrative
status: active
tags: [principles, f0, stigmergy, design]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:4e934e39c4183acb89cb1de2eeafe94f3d33670498e5105cf8502fbfc6b3958b
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# The Five Principles

These five principles are each necessary and together sufficient to produce f(0) —
the state where orchestration burden on main context approaches zero.

---

## 1. Stigmergy-Only

**No `SendMessage`. The filesystem IS the coordination layer.**

Agents coordinate through environmental marks:
- **Manifest paths** — each agent writes to a known path; others discover it
- **faerie-queue `blockedBy`** — express dependencies; blocked tasks auto-unblock
- **Vault droplets** — cross-domain insights written live, discovered by any agent

Why: `SendMessage` routes through main context. Every relay burns 15-25K tokens.
Stigmergy costs zero main-context tokens. Agents discover work passively.

See: [[stigmergic-recursion]] for the full coordination model.

---

## 2. Artifacts-in-Forensics

**Every produced artifact lives in `{repo}/forensics/`, never in `.claude/`.**

Properties:
- **Hash-chained** — each entry records `prev_entry_hash` → `entry_hash`
- **Platform-agnostic** — git-tracked, works across Windows/WSL/Linux
- **Append-only** — never deleted; archive to `forensics/deletions/` with COC entry

Why: `.claude/` is operational-ephemeral (state files, wave coordination).
`forensics/` is the permanent record. Mixing them means audit trails vanish
when state is cleaned.

See: [[../Architecture/forensic-integrity]] for the full COC model.

---

## 3. Task_id-in-Filename

**Universal filename pattern: `{ts}_{type}_{task_id}_{agent}_{session_id8}.{ext}`**

Every artifact embeds its `task_id` in the filename. New agents can discover
all predecessor work for a task with a single grep:

```bash
grep -r "_{task_id}_" forensics/
```

Zero context cost. No orchestrator needed. The filesystem is the index.

---

## 4. Cascading Summarization

**Main reads only `dashboard_line` (≤80 chars). Deeper synthesis spawns a synthesizer.**

Return protocol:
- Agent writes full output to `forensics/`
- Agent returns manifest path + `dashboard_line`
- Main reads only `dashboard_line` (≤80 chars)
- Deep synthesis needed? Spawn a synthesizer agent; it returns its own `dashboard_line`

Why: Reading N full manifests costs O(N) main context. Reading N dashboard_lines
costs ≤80N chars, effectively O(1). Main stays lean regardless of agent count.

The **Main-Inference Heuristic (mth00086)**:
> If main's thought connects ≥2 subagent returns OR makes a routing decision
> OR catches a contradiction, it's earning its inference cost.
> If it's reformulating something a subagent already said, it's burning context.

---

## 5. Pressure-Responsive Streaming

**Capture rate scales exponentially with context fill. Waves gated by altimeter, not clock.**

As context fills:
- Observations stream more frequently (not less)
- Waves are gated by context pressure reading from `piston-checkpoint.json`
- Auto-compact triggers at 85% context fill, then again at 93.5% max

Why: The richest context moment (just before auto-compact) is when the most
has been learned. Streaming highest at that moment prevents evaporation of
insights that would be lost when context is cleared.

See: [[piston-rocket-physics]] for the altimeter and wave gate model.

---

## How They Compose

Each principle handles a different failure mode:

| Principle | Failure mode it prevents |
|---|---|
| Stigmergy-only | Relay overhead burning main context |
| Artifacts-in-forensics | Audit trail loss from state cleanup |
| Task_id-in-filename | Orphaned work from predecessor discovery failure |
| Cascading summarization | Main context O(N) growth with agent count |
| Pressure-responsive streaming | Insight evaporation at auto-compact |

Together they make the system self-scaling: more agents does not mean more
orchestration overhead. It means more parallel throughput at constant main cost.

---

## Related

- [[what-is-faerie]] — introduction and overview
- [[piston-rocket-physics]] — the wave model
- [[stigmergic-recursion]] — how coordination actually works
- [[../Architecture/forensic-integrity]] — the COC implementation
- [[../Glossary/terms]] — f(0), stigmergy, pollen, NECTAR defined
