---
title: "Loop-Gap Dual-State Fix"
tags: [pseudosystem-2.0, substrate, f0, stigmergy, anti-fabrication, equilibrium]
related: ["12-anti-fab-validators", "09-prereq-preflight-self-release", "10-multi-session-heartbeat", "11-confab-class-taxonomy"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 13-loop-gap-dual-state-fix.md

# Loop-Gap Dual-State Fix

## What it does

The Loop-Gap Dual-State Fix addresses a specific failure mode: a task that is simultaneously marked `in-progress` in the faerie queue AND has a `status: final` manifest on disk. This phantom dual-state occurs when:

1. An agent writes its final manifest
2. The queue update (marking task complete) fails or is skipped
3. A new session starts, sees the task as `in-progress`, and claims it again
4. Two agents now believe they own the same task

The fix:
1. On session startup, scan all `status: final` manifests in `.claude/manifests/`
2. Cross-reference against the faerie queue for the same task_ids
3. If a manifest is final but the queue shows in-progress: auto-complete the queue entry
4. Emit a COC entry recording the reconciliation event
5. Log to `forensics/` so the gap is forensically visible

This is not a retry mechanism — it is a state reconciliation that runs once at startup. The fix does not re-execute the task; it trusts the manifest and closes the gap.

## How it composes with siblings

- Uses [[12-anti-fab-validators|Anti-Fab Validators]] manifest_metric to verify that the `status: final` manifest is legitimate before auto-completing
- Works alongside [[10-multi-session-heartbeat|Multi-Session Heartbeat]]: heartbeat records make it possible to detect when a session died mid-completion
- Prevents the stuck states that [[09-prereq-preflight-self-release|Prereq Pre-flight Self-Release]] would wait on forever
- Often triggered by [[11-confab-class-taxonomy|label-conflation confabs]] that wrote status inconsistently

## Evidence / Manifests

Dual-state problem documented in:
- `forensics/diagnosis-queue-bottleneck.md` — queue bottleneck diagnosis that identified dual-state as primary cause
- `scripts/7x_queue_ops.py` — queue ops include reconciliation logic
- `forensics/audit-statusline-consolidation.md` — statusline audit that found in-progress phantom tasks

## Status: live

Reconciliation logic active in `7x_queue_ops.py`. Runs at session startup when faerie claims its first task. COC entries written to `forensics/coc.jsonl` for each reconciliation event.

---

> doc_hash: sha256:pending
