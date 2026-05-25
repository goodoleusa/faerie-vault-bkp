---
type: reference
status: active
tags: [skill, run, queue, tasks, execution]
parent: Skills-Reference/INDEX
up: Skills-Reference/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:78d7effa11837833afe8aa774c95a170a65c86237d30ee6fcfed70f5aac79a09
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Skills-Reference](INDEX.md) · [⌂ Home](../../HOME.md)

# /run — Queue Consumer

Picks up the next unclaimed task from the sprint queue, spawns the appropriate
agent, monitors performance, and loops.

---

## Invocation

| Command | Behavior |
|---------|----------|
| `/run` | Claim next HIGH task and execute |
| `/run blockers` | Run only blocker tasks, then stop |
| `/run critical` | Run critical-path tasks (W1→W2→W3) |
| `/run --once` | Run exactly one task then stop |
| `/run --dry-run` | Show what would be claimed, no execution |
| `/run {filter}` | Run tasks matching project or investigation label |

---

## Execution Flow

```
Step 0: Batch-claim HIGH priority tasks (up to 4)
Step 0b: Select agent via 7x_select_agent.py (performance-ranked)
Step 1: W1 wave spawn (inline, Haiku — faerie waits)
Step 2: W2 wave spawn (inline, Sonnet — faerie waits)
Step 3: End-of-run — spawn membot + performance-eval in parallel
Step 4: W3 wave spawn (background, after response)
Step 5: Loop (unless --once flag)
```

---

## Model Routing

| Wave | Complexity | Model |
|------|-----------|-------|
| W1 | any | Haiku (45s budget) |
| W2 | easy/bulk | Haiku |
| W2 | medium, HIGH priority | Sonnet |
| W2 | hard, inference domain | Opus |
| W3 | inference domain | Opus |
| W3 | other | Sonnet |

Inference domains: `research-analyst`, `knowledge-synthesizer`, `api-designer`, `evidence-curator`

---

## Monkeybranching

When an agent completes a task with >30K context remaining:

```
IF context_remaining > 30K
AND next task is in-domain
AND next task is unblocked:
  → chain-claim next task (no return to faerie)
  → execute inline
  → continue until gate fails
```

Final manifest includes `chained_tasks: [T1, T2, T3]` and `chain_length: 3`.

---

## Agent Selection

```bash
python3 ~/.claude/scripts/7x_select_agent.py --task "ETL pipeline CSV" --json
# → [{"agent": "data-engineer", "score": 0.87, ...}]
```

Falls back to `general-purpose` on any error.

---

## What /run Produces

For each task completed:
- Agent output in `forensics/{type}/{date}/`
- Manifest at `forensics/manifests/{TS}_{type}_{task-id}_{agent-id}_{sid8}.json`
- COC entry in `forensics/coc.jsonl`
- Performance score from auto-eval
- Task marked complete in sprint-queue.json

---

## Related

- [[faerie]] — /faerie skill reference
- [[queue]] — /queue skill reference
- [[../Onboarding/03-spawn-your-first-agent]] — hands-on spawn guide
- [[../Architecture/spawn-contract]] — spawn template contract
