---
title: "Stigmergic Clustering"
tags: [pseudosystem-2.0, substrate, stigmergy, f0, multi-session, equilibrium]
related: ["01-idea-compass", "04-convergence-detector-hook", "05-mission-as-tag", "09-prereq-preflight-self-release", "10-multi-session-heartbeat"]
created: 2026-04-25
doc_hash: sha256:pending
status: live
---

> Breadcrumb: faerie2 / docs / PSEUDOSYSTEM-2.0 / 08-stigmergic-clustering.md

# Stigmergic Clustering

## What it does

Stigmergic Clustering is the mechanism by which agents writing to the filesystem produce emergent topic clusters without explicit coordination. It is the graph-layer expression of the f(0) stigmergy principle.

How it works:
1. Agents write artifacts to `forensics/` with task_id-in-filename convention
2. Each artifact carries tags and compass edges
3. Over time, artifacts with shared tags and overlapping edge targets accumulate
4. The clustering engine periodically scans for co-citation density — notes cited together frequently become a cluster
5. Cluster boundaries are written as `cluster-{name}.md` index notes, themselves linked via compass edges

This is stigmergy applied to graph topology: no agent designs the cluster; the cluster emerges from individual agent writes. The pheromone is the manifest. The trail is the wikilink.

## How it composes with siblings

- Reads [[01-idea-compass|Idea Compass]] South edges to identify what a note contributes to
- Triggers [[04-convergence-detector-hook|Convergence Detector Hook]] when cluster density crosses threshold
- Is the primary substrate for [[05-mission-as-tag|Mission-as-Tag]]: `#f0` cluster is the mission cluster
- Produces cluster index notes that [[09-prereq-preflight-self-release|Prereq Pre-flight Self-Release]] monitors for unblock conditions
- Cluster state persists across sessions via [[10-multi-session-heartbeat|Multi-Session Heartbeat]]

## Evidence / Manifests

Clustering is the operational mode of faerie2's forensics folder. Real evidence:
- `forensics/manifests/` — every manifest is a stigmergic artifact; file density by date shows cluster formation
- `forensics/bundles/` — bundle files are cluster artifacts
- `forensics/vault-2026-04-24-bundle-evolution-synthesis/` — synthesis cluster that emerged from a single sprint

## Status: live

Stigmergic clustering active. Cluster index notes not yet auto-generated (manual for now). Auto-generation is a Step 3 feature.

---

> doc_hash: sha256:pending
