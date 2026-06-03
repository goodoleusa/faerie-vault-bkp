---
title: "Reckon Systems — retrofuture.tech Index Redesign"
date: 2026-05-28
author: goodoleusa
status: review-required
source_repo: hustle
source_path: templates/packages/main-hub/src/pages/index.astro
companion_docker_renames:
  - hustle/docker-compose.yml
  - cybertemplate/docker-compose.yml
  - faerie2/docker-compose.yml
  - faerie2/deploy/scripts/redeploy.sh
---

# Reckon Systems — retrofuture.tech Index Redesign

## What this is

A full rewrite of the storefront page at `retrofuture.tech` (root). Aesthetic
direction: scholarly cartography — Nature journal meets Golden Age sea charts.
Warm cream `#FAF7F0` background, amber/gold `#D4920A` accents, deep ink
`#0A0A0A` text, electric teal `#00E5B4` used sparingly (1-2 hits per section)
as the single funky pop color.

No "queen/bee/honey/hive/loom/weaver" terminology anywhere on the page.

## Section structure (in order)

1. **Nav** — `RECKON · f(0) systems` wordmark + sectional anchors
2. **Hero** — "Set bearing. Spawn the crew. Reckon the distance."
3. **Metrics strip** — 4 provenance-linked numbers, each carries `data-claim-id`,
   `data-source-file`, `data-source-hash`, `data-confidence` for the
   hover-over forensic preview feature
4. **D3 Eval Chart** — composite trajectory across runs 1-6 from
   `eval-history.jsonl`, neon-teal annotation arrow at run 6 marking
   "piston mutation applied"
5. **The Problem** — preserved, cleaned of legacy terminology
6. **Dead Reckoning** — new section on stigmergy + pull quote from
   ORCHESTRATOR-OBSERVATIONS: "Stigmergic coordination is genuinely cheaper
   than RPC at small N."
7. **The Formulas** — amber/gold palette (replaced violet); f(0) formula
   prominent
8. **The Crew** — four compass archetypes (NAVIGATOR/MAKER/BRIDGE/DEEP-DIVER)
   with compass rose
9. **Field Reports** — 3 cards linking to real vault publications, each
   showing the date and source_file path for forensic transparency
10. **Proof Chain** — pull quote: "The chain isn't proving the claims are
    true — it's making the producing-and-reviewing pipeline care, by making
    'being added' expensive enough to be earned."
11. **Footer** — `RECKON · f(0) systems · retrofuture.tech` (no personal name)

## Provenance hooks for the forensic hover feature

Each `.metric-cell.metric-provenance` element carries:

```html
<div class="metric-cell metric-provenance"
     data-claim-id="C-001"
     data-source-file="~/.claude/hooks/state/eval-history.jsonl"
     data-source-hash="f7b418b42f754f56a4ff4c26dd487159a52bf57b52932257e285c38e89b8f120"
     data-prev-hash="5458a09c331c02021fa2dc06f9d1806c74f333230509e65fa7712de20f0c27ba"
     data-confidence="HIGH">
```

The main-thread hover handler can `querySelectorAll('.metric-provenance')`
and attach a source-document preview popover keyed by `data-claim-id`.

## Live numbers (from forensic-provenance.json)

| Metric | Value | Claim | Confidence |
|---|---|---|---|
| Composite eval score, run 6 (piston active) | **0.797** | C-001 | HIGH |
| Piston dimension improvement | **2×** (0.5 → 1.0) | C-002 | HIGH |
| M3 work efficiency, tasks/token | **1.31** | C-007 | MEDIUM |
| f(0) target — orchestration burden | **≤ 5%** | C-009 | HIGH |

## Companion rename — swarmy → reckon

Same review window also did a clean cut of "swarmy" → "reckon" across
docker-compose + redeploy:

- **Network:** `swarmy-net` → `reckon-net`
- **Containers:** `swarmy-*` → `reckon-*` (mcp / openhands / caddy /
  chat-mvp / hustle / cybertemplate / vault / librechat / defenseclaw /
  forensic-sentinel / frontier-walker / ui)
- **Volumes:** `swarmy-*` → `reckon-*` (live data will not migrate
  automatically; fresh start required, see Quickstart)
- **Project name:** `swarmy` → `reckon`
- **In-container paths:** `/workspace/swarmy` → `/workspace/reckon`
- **Env vars:** `SWARMY_REPO_ROOT` → `RECKON_REPO_ROOT`, `SWARMY_VAULT_*` →
  `RECKON_VAULT_*`, etc.

DNS host `swarmy.retrofuture.tech` is intentionally left as-is in
`redeploy.sh` invariant checks — a DNS rename is a separate operational
change (would require desec API updates + new Caddy cert request).

## Quickstart (fresh deploy)

```bash
# 1. On VPS, create the new network (one time):
docker network create reckon-net

# 2. Bring the main stack up:
cd /opt/reckon && bash deploy/scripts/redeploy.sh

# 3. Bring the dev sidecars up (optional):
cd /opt/hustle         && docker compose up -d
cd /opt/cybertemplate  && docker compose up -d
```

`redeploy.sh` already does aggressive disk-pruning by default (`AGGRESSIVE_PRUNE=1`)
and a full invariant verification at the end. Operator triad:

- `bash deploy/scripts/redeploy.sh`     — full one-command redeploy + verify
- `bash deploy/scripts/04-smoke-test.sh` — invariant verification only
- `bash deploy/scripts/disk-recovery.sh` — disk health + aggressive prune

## What still needs review

- [ ] Live preview at `https://retrofuture.tech/` (after rebuild + push)
- [ ] D3 chart rendering on mobile (responsive at ≤480px)
- [ ] Forensic-hover handler wiring on `data-claim-id` attrs (main thread)
- [ ] DNS rename `swarmy.retrofuture.tech` → `reckon.retrofuture.tech` (deferred)
- [ ] Volume migration plan if any old `swarmy-*` volumes hold data worth preserving

## Source files touched

- `hustle/templates/packages/main-hub/src/pages/index.astro` — full rewrite
- `hustle/docker-compose.yml` — clean rename
- `cybertemplate/docker-compose.yml` — clean rename
- `faerie2/docker-compose.yml` — clean rename + project name
- `faerie2/deploy/scripts/redeploy.sh` — container + path + env var rename
