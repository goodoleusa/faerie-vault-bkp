---
type: reference
status: active
tags: [architecture, piston, waves, context, orchestration]
parent: Architecture/INDEX
up: Architecture/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:bc4859c4148ed2c421ccc3efc9132775da56f54379261e28438f8d49bda4578c
hash_ts: 2026-04-25T01:10:51Z
hash_method: body-sha256-v1
---

> [↑ Architecture](INDEX.md) · [⌂ Home](../../HOME.md)

# Piston Waves — Technical Implementation

Technical reference for the piston wave system. For the mental model,
see [[../Hive/piston-rocket-physics]].

---

## State Files

| File | Contents | Read by |
|------|---------|---------|
| `~/.claude/hooks/state/piston-checkpoint.json` | `context_pct`, `wave_state`, `agents_in_flight`, `deferred_reason` | faerie, /faerie skill |
| `~/.claude/hooks/state/sprint-queue.json` | task list, priorities, claim state | /faerie, /run, /queue |
| `~/.claude/hooks/state/faerie-brief.json` | session brief (cold start only) | /faerie (gated) |

**Canonical truth:** `piston-checkpoint.json`. Never trust context estimates from
system reminders — use `9x_lean_query.py --get-all` for current state.

---

## Lean Queries

```bash
# All in one:
python3 ~/.claude/scripts/9x_lean_query.py --get-all

# Individual:
python3 ~/.claude/scripts/9x_lean_query.py --get-eval    # eval:0.38->
python3 ~/.claude/scripts/9x_lean_query.py --get-wave    # W2
python3 ~/.claude/scripts/9x_lean_query.py --get-queue   # pending:2 queued:33...
python3 ~/.claude/scripts/9x_lean_query.py --get-flags   # 0
python3 ~/.claude/scripts/9x_lean_query.py --get-droplets # 4
```

---

## Wave Assignments

```
piston.py plan --queue-file sprint-queue.json
→ {"waves": {"W1": [tasks], "W2": [tasks], "W3": [tasks]}, "stats": {...}}
```

**W1 (fast, 45s):** Explore, security-auditor, admin-sync, context-manager, trail-finder (2x cold-start)
**W2 (medium, 180s):** data-engineer, data-scientist, code-reviewer, knowledge-synthesizer, report-writer
**W3 (deep, 600s):** Complex synthesis, multi-source correlation, final narrative

---

## Context Thresholds

| Threshold | Action |
|-----------|--------|
| <70% | Normal operation |
| 70-85% | W3 should be firing in background |
| 85% | Compact queued; W3 synthesis window closing |
| 93.5% | Auto-compact fires |

**Measured constants (verified):**
- Spawn emit cost: ≤15 tokens per agent (queue-stores-params model)
- Bundle size: 1.6–1.9K tokens per agent (excerpt only)
- Return manifest: ≤100 tokens (dashboard_line + metadata)
- Capacity math: `(remaining - 10K safety) / 100 tok per agent`

---

## Post-Compact Restart

Auto-compact is a flywheel stutter. After compact fires:

```
1. Read piston-checkpoint.json
2. Check wave_state (last launched wave)
3. Read agents_in_flight (who is still running)
4. Launch the next wave immediately
```

Do NOT re-read summarized files. Do NOT announce "resuming after compaction."
The compact summary IS the context.

---

## Brief Gating

`8x_faerie_brief_gatekeeper.py` PreToolUse hook gates reads of `faerie-brief.json`:
- **Warm start:** skip faerie-brief.json (it was already read; reading again wastes context)
- **Cold start:** allow read (first session, no prior context)

---

## Wave Team Structure

Each wave uses TeamCreate + N named Agent() calls:

```python
TeamCreate(team_name="wave1-{SID8}", description="Wave 1 triage agents")

Agent(subagent_type="research-analyst", team_name="wave1-{SID8}",
      name="trail-finder-A", prompt=RENDERED_A)
Agent(subagent_type="research-analyst", team_name="wave1-{SID8}",
      name="trail-finder-B", prompt=RENDERED_B)
```

Teammates coordinate via manifest status reads + vault droplets (stigmergic).
No SendMessage. No polling. One team_complete event when all are final.

---

## Related

- [[../Hive/piston-rocket-physics]] — the mental model
- [[../Hive/permission-to-leap]] — why burn hot at W1
- [[spawn-contract]] — how agent spawns are rendered
- [[../Skills-Reference/faerie]] — /faerie skill reference
