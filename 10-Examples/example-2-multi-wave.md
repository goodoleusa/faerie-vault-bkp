---
type: example
status: active
tags: [example, session, multi-wave, W1, W2, W3, monkeybranching]
parent: 10-Examples/INDEX
up: 10-Examples/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:9e16d353eb4740e9318fdd8d2e03681bfe5dfb375794b851c273aa95c02021ab
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Examples](INDEX.md) · [⌂ Home](../HOME.md)

# Example 2 — Multi-Wave Session with Monkeybranching

A full session showing W1+W2+W3, agent selection, and a monkeybranch chain.

---

## Session Setup

Queue contains 5 pending tasks:

```
[HIGH] task-078 | python-pro     | fix null pointer in ingest.py
[HIGH] task-079 | data-engineer  | validate ingest pipeline after fix
[MED]  task-080 | research-analyst | analyze log patterns
[MED]  task-081 | documentation-engineer | document pipeline fix
[LOW]  task-082 | knowledge-synthesizer  | cross-session synthesis
```

---

## Step 1 — /faerie Wave Planning

piston.py classifies tasks:
- W1: task-078 (HIGH, fast validation)
- W2: task-079, task-080 (research, data work)
- W3: task-081, task-082 (background synthesis)

Wait — piston detects task-078 is a Python fix (complexity=easy). Reassigns to W2.
Trail-finder agents always run W1 regardless.

Revised:
- W1: trail-finder-A, trail-finder-B (cold-start mandatory)
- W2: task-078 (python-pro), task-079 (data-engineer), task-080 (research-analyst)
- W3: task-081 (documentation-engineer), task-082 (knowledge-synthesizer)

---

## Step 2 — W1 (45s)

Trail-finder-A returns:
```
"1 abandoned manifest found: task-072 (status=draft, mtime 47min ago)"
```

Trail-finder-B returns:
```
"2 stale claims found; auto-expired; tasks returned to queue"
```

Main reads 2 dashboard_lines. Cost: ~160 tokens.
The abandoned task-072 is noted for W3 follow-up.

---

## Step 3 — W2 (180s, parallel)

Three W2 agents spawn simultaneously.

**python-pro (task-078):**
- Finds null pointer at `ingest.py:42`
- Writes fix + test
- Context remaining: 68K tokens
- Monkeybranch check: gates pass → claims task-079

**python-pro monkeybranchs to task-079:**
- Runs validation suite (was assigned to data-engineer, but python-pro claimed it)
- All tests pass
- Context remaining: 52K tokens
- Monkeybranch check: context >30K, task-080 is research domain → gate fails
- Writes manifest: `{chained_tasks: ["task-078", "task-079"], chain_length: 2}`

**research-analyst (task-080) [parallel with python-pro's chain]:**
- Analyzes log patterns
- Finds 3 anomalies
- Writes dashboard_line: "3 anomalies found: timing spike at 14:00 UTC, 3 days"

W2 returns. Main reads 2 dashboard_lines (python-pro+chain, research-analyst):
```
python-pro: "task-078+079 chain complete; null fix + tests pass; pipeline healthy"
research-analyst: "3 anomalies; timing spike 14:00 UTC pattern; needs investigation"
```

Cost: ~160 tokens.

---

## Step 4 — Dashboard Response

Main builds dashboard and responds:

```
FAERIE 2026-04-24 15:05 | TURN 0 COMPLETE
================================================================
WAVE 1:  trail-A → 1 abandoned | trail-B → 2 stale claims cleared
WAVE 2:  python-pro → task-078+079 chain; pipeline healthy
         research-analyst → 3 anomalies; timing spike pattern

QUEUE: 2 MED remaining | W3 firing in background
CONTEXT: 38%  wave=W3
================================================================
NEXT: /run to claim more | /handoff when done
```

---

## Step 5 — W3 (background, after response)

W3 fires with `run_in_background: true`.

**documentation-engineer (task-081):**
- Documents the null fix with before/after examples
- Writes next_task_queued: {task_id: "task-083", reason: "anomaly investigation needs doc template"}

**knowledge-synthesizer (task-082):**
- Synthesizes across task-072 (abandoned), task-078/079 (fixed), task-080 (anomalies)
- Finds pattern: all anomalies trace to the same ingestion window
- Writes HEADLINE droplet: "Null pointer + anomaly timing both originate from task-072 era data"

Both W3 manifests complete while user reads the dashboard. Next session picks up:
- task-083 (auto-queued from documentation-engineer's manifest)
- The synthesizer's HEADLINE droplet in NECTAR (promoted at /handoff)

---

## What Main Read Total

| Event | Tokens |
|-------|--------|
| /faerie orientation | ~500 |
| W1 returns (2×) | ~160 |
| W2 returns (2 manifests from 3 agents) | ~160 |
| Dashboard build | ~50 |
| /handoff | ~200 |
| **Total** | **~1,070 tokens** |

3 agents ran in W2. 2 ran in W3 background. Monkeybranch completed 2 tasks in 1 agent.
Main spent ~1K tokens throughout. Agents spent ~80K total.

---

## Related

- [[example-1-simple-task]] — simpler single-agent example
- [[../00-SHARED/Hive/stigmergic-recursion]] — monkeybranching explained
- [[../00-SHARED/Architecture/piston-waves]] — wave architecture
