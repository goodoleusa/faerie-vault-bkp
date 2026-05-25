---
type: charter
status: active
charter_id: mission-docker-deploy-stability
semantic_mission: mission-docker-deploy-stability
cluster_prefix: ["deploy", "invariants", "redeploy"]
phase: "phase 2 active"
author: goodoleusa
created: 2026-05-21
canonical_repo_path: "forensics/charters/active/2026-05-21Z__charter__mission-docker-deploy-stability__goodoleusa.json"
filename_base: "2026-05-21Z__charter__mission-docker-deploy-stability__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — mission-docker-deploy-stability

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-21Z__charter__mission-docker-deploy-stability__goodoleusa.json`
> Status: **active** | Phase: **phase 2 active** | Mission: `[[mission-docker-deploy-stability]]`

---

## Thesis

Bake invariants into the deploy pipeline so the five recurring footguns from 2026-05-21 (stale image
after rebuild, 401 misread as failure, OAuth 404 after edit, Caddy crash-loop on empty basic_auth,
.env clobbered by pull) cannot recur silently. Single source of truth =
deploy/scripts/baseline_expected.json. Script + CI both verify the same contract on every redeploy.

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| (see repo JSON for phase details) | | | |

## Operator Pain Points

- (none)

## Non-Goals

- Refactoring deploy/mcp-server/server.py (recently shipped + sister-agent dependency)
- Touching deploy/chat-mvp/src/* (frontend churn out of scope)
- Re-architecting Caddy routes (current state is correct)
- Cross-repo changes (cybertemplate/ is a different repo)
- Per-image digest pinning (would break security patch flow at patch-version)

## Related Charters

- (none)

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-21Z__charter__mission-docker-deploy-stability__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
