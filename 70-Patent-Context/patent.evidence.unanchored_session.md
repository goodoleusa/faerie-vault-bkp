---
type: shape
shape_id: patent.evidence.unanchored_session
target_direction: decreasing
current_count: 29
baseline_ts: "2026-05-25T20:00:00Z"
membench_probe: false
cluster_prefix: ["patent", "evidence", "unanchored"]
applicable_repos: ["faerie2"]
canonical_repo_path: "_meta/shapes.json"
tags: [shape, measurement, pseudosystem]
blueprint: "[[Shape.blueprint]]"
---

# Shape — patent.evidence.unanchored_session

> **Vault pseudosystem mirror** — canonical source: `_meta/shapes.json` (shape_id: `patent.evidence.unanchored_session`)
> Target direction: **decreasing** | Current count: **29** | Membench probe: **False**

---

## Description

Count of sessions/conversations that do NOT have a corresponding entry in their respective archive manifest. Sums BOTH lanes: (1) Claude Code sessions in ~/.claude/projects/-mnt-d-0LOCAL-gitrepos-faerie2/ not in forensics/_claude-session-archive/_manifest.jsonl, plus (2) OpenHands conversations in .openhands/conversations/ not in forensics/_openhands-session-archive/_manifest.jsonl. Target: decreasing to zero. Non-zero means patent-evidence completeness is at risk — new sessions are not yet anchored in the COC-preserved archive.

## Measurement

| Field | Value |
|-------|-------|
| Target direction | decreasing |
| Current count | 29 |
| Baseline timestamp | 2026-05-25T20:00:00Z |
| Noise threshold | 0 |
| Detector script | `python3 -c "import json, os, pathlib; cc_dir = pathlib.Path('/mnt/d/0LOCAL/.claude/projects/-mnt-d-0LOCAL-gitrepos-faerie2'); cc_mf = pathlib.Path('forensics/_claude-session-archive/_manifest.jsonl'); oh_dir = pathlib.Path('.openhands/conversations'); oh_mf = pathlib.Path('forensics/_openhands-session-archive/_manifest.jsonl'); def archived_keys(mf, key):   s = set();   [s.add(json.loads(l).get(key,'')) for l in open(mf) if l.strip() and json.loads(l).get('record_type') != 'manifest_signature'] if mf.exists() else None;   return s; cc_archived = archived_keys(cc_mf, 'source_path'); oh_archived = archived_keys(oh_mf, 'conv_id'); cc_unarch = sum(1 for p in (cc_dir.glob('*.jsonl') if cc_dir.exists() else []) if str(p) not in cc_archived); oh_unarch = sum(1 for p in (oh_dir.iterdir() if oh_dir.exists() else []) if p.is_dir() and p.name not in oh_archived); print(cc_unarch + oh_unarch)"` |
| Membench probe | False |
| Applicable repos | faerie2 |

## History

| Timestamp | Count | Mutation | Verdict |
|-----------|-------|----------|---------|
| 2026-05-25T20:00:00 | 29 | shape-declared: forensic-archivist F5 (pre-backfill baseline) | None |
| 2026-05-25T20:45:00 | 0 | F3-backfill: 9x_claude_session_forensic_archive.py --rebuild-all | beneficial |
| 2026-05-25T00:00:00 | 0 | Phase 2 (continuous-evidence-preserver): detector extended to sum both lanes (Claude Code + OpenHands). 15-min cron + PostToolUse hook installed. OH archive initialized with forensics/_openhands-session-archive/. | beneficial |

## Interpretation

<!-- What a count of 29 means in context, and what moves this toward/away from target. -->

---

*Canonical source: `_meta/shapes.json` in repo. Do not edit count here — it reflects the repo registry.*
