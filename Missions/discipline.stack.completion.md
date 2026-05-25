---
type: mission
status: open
mission_id: discipline.stack.completion
task_count: 2
last_ts: "2026-05-24T00:09:27"
bearing_summary: {"S": 2}
charter_ids: []
canonical_repo_path: "forensics/mission-graph.json"
tags: [mission, pseudosystem]
blueprint: "[[Mission.blueprint]]"
---

# Mission — discipline.stack.completion

> **Vault pseudosystem dossier** — canonical source: `forensics/mission-graph.json`
> Task count: **2** | Bearings: **S:2** | Last activity: **2026-05-24**

---

## Related Charters

- (no active charters in graph yet)

## Open Work

| Bearing | Task ID | Rationale |
|---------|---------|-----------|
| S | eval-writer-keypair-provisioning-sweep | provision agent keypairs for bulkhead-1-perimeter, bulkhead-2-purification, bulk |
| E | eval-writes-unsigned-shape-register | register eval.writes.unsigned in _meta/shapes.json + wire shape detector via scr |
| S | eval-writer-verify-helper | add eval_writer.verify(path) helper that walks a jsonl/snapshot file and checks  |
| S | vault-writer-as-human | Future _vault_writer.py extension: emit authorship frontmatter signatures using  |
| E | os-keychain-integration | Placeholder hook in get_current_human_key_path step 3 — wire macOS Keychain / GN |

## Recent Manifests

- `eval-writer-discipline-stack-completion` — eval_writer.py shipped; 6 hooks + 2 lib sites retrofitted to signed JSONL/snapsh
- `human-lib` — MAKER HUMAN: _human_lib + 5f --actor-tier human + 1a/_charter_lib --as-human wir

## Narrative

eval_writer.py shipped; 6 hooks + 2 lib sites retrofitted to signed JSONL/snapsh MAKER HUMAN: _human_lib + 5f --actor-tier human + 1a/_charter_lib --as-human wir

---

*Mission dossier derived from `forensics/mission-graph.json`. Schema version: ?. Corpus: 265 manifests.*
