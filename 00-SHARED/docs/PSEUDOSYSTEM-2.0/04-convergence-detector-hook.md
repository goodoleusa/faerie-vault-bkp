---
title: "Convergence Detector Hook"
tags: [pseudosystem-2.0, substrate, f0, stigmergy, equilibrium, multi-session]
related: ["02-auto-edge-inferrer", "03-compass-surface-contradictions", "08-stigmergic-clustering", "10-multi-session-heartbeat"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 04-convergence-detector-hook.md

# Convergence Detector Hook

## What it does

The Convergence Detector Hook fires when note density within a semantic cluster crosses a configurable threshold. Its purpose: identify when enough evidence has accumulated around a concept to warrant synthesis — before a session boundary erases context.

The hook:
1. Monitors edge counts per cluster after every [[02-auto-edge-inferrer|Auto-edge Inferrer]] run
2. Compares current density against the cluster's convergence threshold (default: 5 notes, 8 edges)
3. When threshold crossed: emits a convergence signal to the synthesis queue
4. Tags cluster notes with `#convergence-candidate`
5. Optionally triggers a synthesizer agent spawn via the faerie queue

This is the substrate's way of saying "enough has landed here — crystallize it now before the context window closes."

## How it composes with siblings

- Receives density input from [[02-auto-edge-inferrer|Auto-edge Inferrer]] after each add
- Reads contradiction counts from [[03-compass-surface-contradictions|Compass-surface + Contradictions]] — high contradiction density lowers the convergence threshold
- Signals [[08-stigmergic-clustering|Stigmergic Clustering]] to freeze a cluster for synthesis
- Coordinates with [[10-multi-session-heartbeat|Multi-Session Heartbeat]] — convergence signals survive session boundaries via heartbeat layer
- When fired, writes a manifest entry that [[09-prereq-preflight-self-release|Prereq Pre-flight Self-Release]] can use as an unblock condition

## Evidence / Manifests

Hook architecture documented in:
- `forensics/compact-events.jsonl` — auto-compact events are the production instance of convergence detection (compact fires at 85% context fill, analogous mechanism)
- `docs/bundle-evolution-system-design-2026-04-24.md`

## Status: live

Hook active. Threshold configurable per cluster via frontmatter `convergence_threshold: N`.

---

> doc_hash: sha256:pending
