---
type: guide
status: active
tags: [onboarding, manifests, output, forensics]
parent: Onboarding/INDEX
up: Onboarding/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:5970ac7bd453d361c22d3f694ccb7992e0ef90678d8b950d0d936b6096d5db78
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Onboarding](INDEX.md) · [⌂ Home](../../HOME.md)

# 04 — Reading Manifests

Manifests are what agents return. Understanding them is the key to working
with faerie2 effectively.

---

## What a Manifest Is

A manifest is a JSON file that every agent writes when it completes work.
It is the contract between agent and orchestrator.

**Location:** `{repo}/forensics/manifests/{TS}_{agent-type}_{task-id}_{agent-id}_{sid8}.json`

**Main reads:** only `dashboard_line` (≤80 chars)
**Deep reads:** only when `dashboard_line` signals something needing investigation

---

## Required Fields

```json
{
  "agent": "documentation-engineer",
  "ts": "2026-04-24T15:30:00Z",
  "wave": 2,
  "task_id": "task-042",
  "agent_run_id": "ar-20260424-abc123",
  "output_path": "/mnt/d/0local/gitrepos/faerie2/forensics/docs/...",
  "dashboard_line": "spawn contract documented; 3 templates; ready-for-review",
  "files_written": ["/path/to/output.md"],
  "finding_hash": "sha256:abc123...",
  "manifest_hash": "sha256:def456...",
  "status": "final"
}
```

---

## Status Progression

| Status | Meaning |
|--------|---------|
| `in-progress` | Agent is still running |
| `draft` | Agent has completed a draft milestone |
| `final` | Agent is done; safe to consume |

Manifests are written progressively. An agent running for 3 minutes
should write `in-progress` at start, `draft` at midpoint, `final` at end.

---

## The dashboard_line

The dashboard_line is the primary signal main reads. It must be ≤80 chars.
Good format (value · diagnosis · signal):

```
"12 endpoints documented; 2 auth gaps flagged; ready-for-security-review"
 ↑ value              ↑ diagnosis           ↑ signal/next
```

If the dashboard_line says something alarming (gap, failure, blocker),
then read the full output at `output_path`.

---

## Finding the Output

```bash
# From the manifest:
cat <output_path>

# Search by task_id:
grep -r "_task-042_" /mnt/d/0local/gitrepos/faerie2/forensics/

# List all manifests for a session:
ls /mnt/d/0local/gitrepos/faerie2/forensics/manifests/ | grep <session-id>
```

---

## Hash Chain Fields

```json
{
  "finding_hash": "sha256:...",   ← hash of output_path file content
  "manifest_hash": "sha256:...",  ← hash of this manifest (excluding itself)
  "prev_entry_hash": "sha256:...",← hash of previous COC entry (from coc.jsonl)
  "entry_hash": "sha256:..."      ← this entry's hash (chains to next)
}
```

These form the forensic chain of custody. You do not need to compute them —
hooks handle it. But you can verify integrity:

```bash
python3 /mnt/d/0local/gitrepos/faerie2/scripts/verify_chain.py \
  --coc forensics/coc.jsonl
```

---

## next_task_queued

When an agent identifies follow-on work:

```json
{
  "next_task_queued": {
    "task_id": "task-043",
    "title": "Security review of documented endpoints",
    "reason": "Auth gaps found; needs security-auditor",
    "preferred_agent": "security-auditor",
    "priority": "HIGH"
  }
}
```

The PostToolUse hook reads this and creates the task automatically.
The follow-on task starts as `blocked_by: [task-042]` and unblocks
when task-042 status reaches `final`.

---

## Related

- [[03-spawn-your-first-agent]] — spawning agents that produce manifests
- [[../Architecture/forensic-integrity]] — COC and hash chain architecture
- [[05-using-the-queue]] — what happens to next_task_queued
- [[../Glossary/terms]] — manifest, dashboard_line, COC defined
