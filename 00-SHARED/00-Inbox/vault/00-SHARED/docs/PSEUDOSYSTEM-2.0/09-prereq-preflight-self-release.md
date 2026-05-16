---
title: "Prereq Pre-flight Self-Release"
tags: [pseudosystem-2.0, substrate, f0, stigmergy, multi-session, equilibrium]
related: ["08-stigmergic-clustering", "10-multi-session-heartbeat", "04-convergence-detector-hook", "13-loop-gap-dual-state-fix"]
created: 2026-04-25
doc_hash: sha256:pending
status: pending
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 09-prereq-preflight-self-release.md

# Prereq Pre-flight Self-Release

## What it does

Prereq Pre-flight Self-Release is a pending primitive that enables agents to self-unblock when their declared prerequisites land, without requiring a coordinator agent to check and release them.

The mechanism:
1. When an agent queues a blocked task, it writes its prereqs as a structured list in the task manifest
2. A lightweight pre-flight hook monitors the filesystem for prereq completion signals (manifest status=final with matching task_id)
3. When all prereqs land, the hook updates the task's `blockedBy` field to `[]` in the faerie queue
4. The task becomes claimable on the next queue scan — no human, no coordinator

This is the self-organizing layer that keeps the faerie queue moving without orchestrator intervention. It is the task-lifecycle expression of stigmergy: the completing agent's manifest is the pheromone that unblocks the next agent.

## How it composes with siblings

- Monitors [[08-stigmergic-clustering|Stigmergic Clustering]] cluster index notes as one class of prereq signal
- Coordinates with [[10-multi-session-heartbeat|Multi-Session Heartbeat]] so prereq state survives session boundaries
- Uses [[04-convergence-detector-hook|Convergence Detector Hook]] convergence events as unblock triggers for synthesis tasks
- Eliminates a class of stuck states that [[13-loop-gap-dual-state-fix|Loop-Gap Dual-State Fix]] currently handles manually

## Evidence / Manifests

`blockedBy` field in faerie queue is the existing manual version of this primitive. Self-release automates what humans currently do. Design referenced in:
- `scripts/7x_queue_ops.py` — queue ops that manage blockedBy relationships
- `docs/SPAWN-BOILERPLATE.md` — `blockedBy` + `next_task_queued` protocol section

## Status: pending

The `blockedBy` infrastructure exists. Self-release hook not yet written. Estimated impact: eliminates 80% of manual queue intervention during multi-agent sprints.

---

> doc_hash: sha256:pending
