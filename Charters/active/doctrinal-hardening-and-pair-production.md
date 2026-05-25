---
type: charter
status: active
charter_id: doctrinal-hardening-and-pair-production
semantic_mission: swarmy-doctrinal-hardening
cluster_prefix: []
phase: "1-of-4"
author: goodoleusa
created: 2026-05-25
canonical_repo_path: "forensics/charters/active/2026-05-25Z__charter__doctrinal-hardening-and-pair-production__goodoleusa.json"
filename_base: "2026-05-25Z__charter__doctrinal-hardening-and-pair-production__goodoleusa"
tags: [charter, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter — doctrinal-hardening-and-pair-production

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/active/2026-05-25Z__charter__doctrinal-hardening-and-pair-production__goodoleusa.json`
> Status: **active** | Phase: **1-of-4** | Mission: `[[swarmy-doctrinal-hardening]]`

---

## Thesis

The 2026-05-25 wave shipped Path 3 pair coding + DRY cleanup + doctrinal corrections (Voice vs
Bookkeeping + all-14-equal-peers + spawn-brief-discipline). But the corrections are doctrinal-only —
no automatic enforcement, no aggregator that DERIVES charter status from signed manifests instead of
relying on operator JSON edits. This charter ships the enforcement layer + closes remaining DRY debt
+ hardens pair coding for actual two-user testing. Discipline becomes mechanical: violations
detected

## Phases

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| phase_1 | Charter aggregator + spawn-brief detector (doctrinal enforce | 5 | queued |
| phase_2 | Close DRY debt + altimeter wire-up + SessionStateMCPMixin | 4 | queued |
| phase_3 | Pair coding production-ready (real-world hardening) | 5 | queued |
| phase_4 | Sigstore signing per manifest (forensic-coc-v2-rekor adjacen | 6 | queued_stretch |

## Operator Pain Points

- Charter phase status set by manual JSON edit (operator/main) instead of derived from signed manifests — out of band of t
- Spawn briefs can still pre-fill completion_choice — doctrine shipped but no automatic detector blocks it
- DRIVE OP-gate + completion-trajectory-gate silently degrade to allow because altimeter+session-start writers aren't wire
- swarmy_canvas + swarmy_pair_state share is_member→JSON→ticker pattern — boilerplate ready to extract
- Hardcoded z-index values still exist; tokens shipped but migration deferred

## Non-Goals

- Cut E Codespaces integration (still deferred to whenever the operator wants actual shared dev env beyond shared chat+can
- mission-graph viz polish (already shipped; further polish is its own scope)
- New formulas (the 17 + P(t) composite are sufficient; new formulas need their own pre-registration)
- Anything that requires touching the canonical 14 choice enumeration (locked by CANONICAL-SET.md until charter pre-regist

## Related Charters

- 2026-05-25Z__charter__pair-coding-completion-and-dry-cleanup (just sealed; this 
- 2026-05-24Z__charter__forensic-coc-v2-rekor (sigstore signing — adjacent surface
- 2026-05-24Z__charter__multi-tenancy-and-free-tier-scoping (auth scaffolding this

---

*To jump to canonical JSON: open `forensics/charters/active/2026-05-25Z__charter__doctrinal-hardening-and-pair-production__goodoleusa.json` in repo. Vault note is navigation-only — do not edit to change charter state.*
