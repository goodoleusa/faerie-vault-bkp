---
title: "Multi-Session Heartbeat Layer"
tags: [pseudosystem-2.0, substrate, multi-session, f0, stigmergy, equilibrium]
related: ["08-stigmergic-clustering", "09-prereq-preflight-self-release", "04-convergence-detector-hook", "06-mission-auto-promotion"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 10-multi-session-heartbeat.md

# Multi-Session Heartbeat Layer

## What it does

The Multi-Session Heartbeat Layer maintains liveness state across session boundaries. Claude sessions are ephemeral — context is destroyed at /compact or session end. The heartbeat layer ensures that:

1. Cluster states, prereq statuses, and convergence signals survive session termination
2. A new session starting mid-sprint can reconstruct current system state from the heartbeat log without re-reading all history
3. Dead sessions are detected (no heartbeat in N minutes) and their in-progress tasks are released back to the queue

The heartbeat writes a lightweight pulse to `forensics/` every N operations (not time-based — triggered by agent activity). Each pulse records: active clusters, blocked tasks, pending convergence signals, session_id.

This is the substrate's answer to the question "what happens to coordination when a session dies?" Answer: the filesystem holds state, the heartbeat makes it readable, the pre-flight hook acts on it.

## How it composes with siblings

- Provides state persistence for [[08-stigmergic-clustering|Stigmergic Clustering]] cluster boundaries
- Enables [[09-prereq-preflight-self-release|Prereq Pre-flight Self-Release]] to function across session boundaries
- Records [[04-convergence-detector-hook|Convergence Detector Hook]] signals that may outlive the session that detected them
- Feeds [[06-mission-auto-promotion|Mission Auto-Promotion (Step 2)]] with cross-session reference counts

## Evidence / Manifests

Production heartbeat is currently manual — the `forensics/compact-events.jsonl` file records context compression events that serve as session boundary markers. Real evidence:
- `forensics/compact-events.jsonl` — compact events are the heartbeat signal in production
- `forensics/coc.jsonl` — COC chain is the audit log the heartbeat reads for reconstruction

## Status: live

Manual heartbeat via compact events is active. Automated pulse writes not yet implemented — that is a future optimization. The critical behavior (state survives sessions via forensics/) is live.

---

> doc_hash: sha256:pending
