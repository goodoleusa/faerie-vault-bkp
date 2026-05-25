---
type: mission
status: open
mission_id: agent.agency.citation-and-coc-chain-discipline.schema-lock
task_count: 1
last_ts: "2026-05-21T16:18:48"
bearing_summary: {"S": 1}
charter_ids: []
canonical_repo_path: "forensics/mission-graph.json"
tags: [mission, pseudosystem]
blueprint: "[[Mission.blueprint]]"
---

# Mission — agent.agency.citation-and-coc-chain-discipline.schema-lock

> **Vault pseudosystem dossier** — canonical source: `forensics/mission-graph.json`
> Task count: **1** | Bearings: **S:1** | Last activity: **2026-05-21**

---

## Related Charters

- (no active charters in graph yet)

## Open Work

| Bearing | Task ID | Rationale |
|---------|---------|-----------|
| N | register-posttooluse-coc-sign-hook-oh-sdk-native | wire OH-native PostToolUse[Write] hook on forensics/ephemeral/** to call coc_sig |
| E | sync-orchestrate-and-system-agent-to-new-schema | .openhands/skills/{faerie,swarmy}/orchestrate.py + system agent prompts must sur |
| E | sync-20-agent-agency-doc-with-citation-and-chain | docs/20-AGENT-AGENCY-CANONICAL.md still describes the original schema; needs cla |
| S | phase-2-harden-coc-chain-missing-to-error | soft-enforce ships today; phase 2 stops stubbing genesis-parent + raises ValueEr |
| W | design-branching-merkle-divergence-convergence | schema is forward-compat (parent_hashes:list) but 0a_coc-core still linear; desi |

## Recent Manifests

- `wire-completion-choice-into-manifest-writer-01` — claims[]+coc_chain schema locked; coc_sign_manifest hook stub wired

## Narrative

claims[]+coc_chain schema locked; coc_sign_manifest hook stub wired

---

*Mission dossier derived from `forensics/mission-graph.json`. Schema version: ?. Corpus: 265 manifests.*
