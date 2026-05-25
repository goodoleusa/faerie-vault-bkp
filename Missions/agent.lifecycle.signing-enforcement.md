---
type: mission
status: open
mission_id: agent.lifecycle.signing-enforcement
task_count: 1
last_ts: "2026-05-22T16:12:06"
bearing_summary: {"S": 1}
charter_ids: []
canonical_repo_path: "forensics/mission-graph.json"
tags: [mission, pseudosystem]
blueprint: "[[Mission.blueprint]]"
---

# Mission — agent.lifecycle.signing-enforcement

> **Vault pseudosystem dossier** — canonical source: `forensics/mission-graph.json`
> Task count: **1** | Bearings: **S:1** | Last activity: **2026-05-22**

---

## Related Charters

- (no active charters in graph yet)

## Open Work

| Bearing | Task ID | Rationale |
|---------|---------|-----------|
| S | signing-backfill-legacy-decision | operator review AUDIT.md per-file: leave / stamp UNSIGNED_LEGACY / rewrite-and-s |
| E | provision-missing-agent-keypairs | 3 manifests carry UNSIGNED_*_NO_KEY; init missing keypairs |
| N | wire-ci-lint-manifest-signing | lint-manifest-signing.sh must be wired into pre-commit + CI |

## Recent Manifests

- `signing-enforcement` — signing-enforcement: writer raises on missing key; hook blocks unsigned; lint+au

## Narrative

signing-enforcement: writer raises on missing key; hook blocks unsigned; lint+au

---

*Mission dossier derived from `forensics/mission-graph.json`. Schema version: ?. Corpus: 265 manifests.*
