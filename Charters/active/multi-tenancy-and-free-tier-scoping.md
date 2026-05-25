---
type: charter
status: active
charter_id: multi-tenancy-and-free-tier-scoping
semantic_mission: tenancy.scope.isolation
cluster_prefix: ["tenancy", "scope", "isolation"]
phase: ""
author: goodoleusa
created: 2026-05-24
canonical_repo_path: "forensics/charters/active/2026-05-24Z__charter__multi-tenancy-and-free-tier-scoping__goodoleusa.json"
filename_base: "2026-05-24Z__charter__multi-tenancy-and-free-tier-scoping__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — multi-tenancy-and-free-tier-scoping

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-24Z__charter__multi-tenancy-and-free-tier-scoping__goodoleusa.json`
> Status: **active** | Phase: **** | Mission: `[[tenancy.scope.isolation]]`

---

## Thesis

Today every authenticated bearer token sees ALL charters/manifests/forensics belonging to the
operator. Verified leak: swarmy_charter verb=list returns 8 charters owned by goodoleusa to any
token. This is unacceptable for a public-MCP value proposition. Fix at three layers: (1) data layer
— every record carries an owner identity; (2) tool layer — list/read tools filter by caller
identity; (3) tier layer — capability matrix decides what each tier can read/write. Pair this with a
coherent FREE TIE

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| phase_1 | Owner-filter the leak surface (charter list + get) | 1 | in-progress |
| phase_2 | Extend owner filter to manifest, mission, coc tools | 2 | queued |
| phase_3 | Free-tier workspace provisioning | 3 | queued |
| phase_4 | Public-primitives registry | 1 | queued |
| phase_5 | Capability matrix codified in auth.py | 1 | queued |
| phase_6 | Admin-tier audit trail | 1 | queued |

## Operator Pain Points

- (none)

## Non-Goals

- Full multi-tenant database with per-row ACLs (overkill for current scale; filesystem-namespacing is sufficient)
- Per-record fine-grained permissions (use namespace-level scoping; pro tier expands to invited shared namespaces)
- Automatic publication of private HONEY to mesh (always operator-curated; the publisher chooses what's public)

## Related Charters

- (none)

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-24Z__charter__multi-tenancy-and-free-tier-scoping__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
