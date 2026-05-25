---
type: guide
status: active
tags: [onboarding, first-session, getting-started]
parent: Onboarding/INDEX
up: Onboarding/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:4112009697f5281c2229a1433397e9c20383bb90c4216ade7cbf495e0a7b56e1
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Onboarding](INDEX.md) · [⌂ Home](../../HOME.md)

# 01 — Your First Session

Concrete steps for the first time you open faerie2.

**Time:** ~15 minutes
**Prerequisite:** faerie2 repo cloned, Claude Code installed

---

## Step 1 — Open Terminal in the faerie2 Repo

```bash
cd /mnt/d/0local/gitrepos/faerie2
claude
```

This opens a Claude Code session with faerie2 as the working directory.

---

## Step 2 — Run /faerie

Type `/faerie` in the Claude Code prompt and press Enter.

What happens:
1. faerie reads the piston checkpoint (wave state, context %)
2. faerie reads the sprint queue (pending tasks)
3. W1 agents spawn and run (you will see them working)
4. W2 agents spawn and run after W1 completes
5. faerie responds once with a dashboard

If this is a fresh repo with no tasks queued, faerie will note the empty queue
and orient you to next steps.

---

## Step 3 — Read the Dashboard

The dashboard looks like this:

```
FAERIE 2026-04-24 15:05 | TURN 0 COMPLETE
================================================================
EVAL: 0.64→  T:0.75  M:0.67  R:0.67
QUEUE: 3 HIGH | 2 MED | 0 LOW
MEMORY: brief fresh | HONEY 2.1K
================================================================
NEXT: /run to claim tasks | /handoff to close session
```

Key fields:
- `EVAL` — system quality score (higher is better; 0.75 is the target)
- `QUEUE` — tasks waiting to be claimed, by priority
- `MEMORY` — memory system status
- `NEXT` — what to do next

---

## Step 4 — Try /run

Type `/run` to claim and execute the next pending task.

faerie will:
1. Claim the highest-priority unclaimed task
2. Spawn the appropriate agent
3. Agent runs, writes output to forensics/, returns manifest
4. faerie reads the dashboard_line from the manifest
5. You see a one-line summary of what the agent did

---

## Step 5 — Try /metrics

Type `/metrics` (or `/dev-eval`) to see system health.

This shows:
- Quality dimensions and scores
- Gap analysis — what needs attention
- Eval trends across recent sessions

---

## Step 6 — Close with /handoff

When you are done, type `/handoff`.

What happens:
1. Session memory (pollen) is promoted to NECTAR
2. Vault is synced with agent outputs
3. Piston checkpoint is updated for next session

---

## What You Just Did

```
/faerie   → oriented to session state, ran W1+W2 waves
/run      → claimed and executed one task
/metrics  → checked system health
/handoff  → cleanly closed the session
```

This is the full faerie loop. Every session follows this pattern.

---

## Common First-Session Issues

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `/faerie` stalls for >5 min | W1 agent timeout | It will recover — watch for PARTIAL in dashboard |
| Dashboard shows empty queue | No tasks queued | Add tasks via `/queue add` |
| Error reading piston-checkpoint | Fresh install | Normal — faerie creates it on first run |

---

## Next Steps

- [[02-skills-tour]] — understand all the skills
- [[03-spawn-your-first-agent]] — deeper dive into agent spawning
- [[../Hive/what-is-faerie]] — understand the design behind what you just ran

---

## Related

- [[../Skills-Reference/faerie]] — full /faerie skill reference
- [[../Skills-Reference/run]] — full /run skill reference
- [[../Skills-Reference/handoff]] — full /handoff skill reference
