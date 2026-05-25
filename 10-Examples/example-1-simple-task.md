---
type: example
status: active
tags: [example, session, simple, W2, manifest]
parent: 10-Examples/INDEX
up: 10-Examples/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:33f31e06377ed631d7193eeef16959e78bfdb913cd8199ac0e1afbc54da02af5
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Examples](INDEX.md) · [⌂ Home](../HOME.md)

# Example 1 — Simple Task (Single W2 Agent)

A minimal session: one task, one agent, one manifest.

---

## Session Setup

Queue contains one pending task:
```json
{
  "id": "task-042",
  "title": "Document the spawn-contract mechanism",
  "category": "publishing",
  "priority": "MED",
  "wave_target": "W2",
  "context_bundle": {
    "highest_value": "developer understands spawn-contract without reading code",
    "done_looks_like": "spawn-contract.md written with examples; ≤500 words",
    "source_files": ["docs/SPAWN-BOILERPLATE.md", "hooks/8x_spawn_contract_enforcer.py"]
  }
}
```

---

## Step 1 — /faerie Runs

Main reads piston-checkpoint: `wave_state: idle, context_pct: 5`.

Wave 0 bash reads complete. W1: two trail-finder agents spawn.
They return in ~20 seconds:

```
Trail-finder-A dashboard_line: "No abandoned manifests found (scanned 47 items)"
Trail-finder-B dashboard_line: "No stale claims in queue"
```

W2: task-042 is assigned to `documentation-engineer`.
Template renders for W2:
```bash
RENDERED=$(python3 ~/.claude/scripts/7x_spawn_template.py render \
  --template w2-documentation-engineer \
  --params '{"task_id":"task-042","task_goal":"Document spawn-contract mechanism"}')
```
Spawn cost: 47 tokens (rendered prompt, not composed).

---

## Step 2 — Agent Runs

Agent spawns with 200K fresh context window. It reads:
- Source files from context_bundle
- NECTAR tail-30 (finds 2 relevant technique entries)
- Generates AGENT-RUN-ID: `ar-20260424-d4f8a1b2`

Agent writes `spawn-contract.md` to `forensics/docs/20260424T...`.

Agent writes manifest progressively:
- `status: in-progress` at start
- `status: draft` after first draft
- `status: final` after review

Final manifest:
```json
{
  "agent": "documentation-engineer",
  "task_id": "task-042",
  "agent_run_id": "ar-20260424-d4f8a1b2",
  "output_path": "forensics/docs/20260424T153000_...",
  "dashboard_line": "spawn-contract.md written; 380 words; 2 examples; template list included",
  "finding_hash": "sha256:abc123...",
  "status": "final"
}
```

---

## Step 3 — Main Reads Dashboard_Line

Main receives:
```
W2 documentation-engineer → "spawn-contract.md written; 380 words; 2 examples; template list included"
```

That is 80 chars. Main read 80 chars of output from 380 words of work.
Full output is at `output_path` if needed.

---

## Step 4 — /handoff

Main types `/handoff`. Memory-keeper spawns.
Pollen observations from the session (5 MEM blocks) are promoted.
2 HIGH-priority observations reach NECTAR.
Piston checkpoint updated.

---

## What Just Happened

| Action | Tokens spent by main |
|--------|---------------------|
| /faerie orientation | ~500 tokens |
| W1 trail-finder returns (2×) | ~160 tokens (2 dashboard_lines) |
| Template render | ~47 tokens |
| W2 agent return | ~80 tokens (1 dashboard_line) |
| /handoff | ~200 tokens |
| **Total main tokens** | **~987 tokens** |

The agent spent ~15K tokens doing the actual work.
Main spent ~1K tokens orchestrating it.
That ratio is f(0) in practice.

---

## Related

- [[example-2-multi-wave]] — a more complex session with W1+W2+W3
- [[../00-SHARED/Onboarding/04-reading-manifests]] — manifest structure explained
- [[../00-SHARED/Architecture/spawn-contract]] — spawn contract reference
