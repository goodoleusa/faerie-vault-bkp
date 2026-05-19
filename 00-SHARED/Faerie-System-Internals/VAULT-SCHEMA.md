---
type: schema
status: active
created: 2026-03-24
updated: 2026-03-27
tags:
  - schema
  - vault-structure
  - metadata
  - coc
doc_hash: sha256:cd8810727c5f30cd8e1ae16ba03f1e177a23ce2fa41ec8ef6fbec39384482f22
hash_ts: 2026-03-29T16:10:50Z
hash_method: body-sha256-v1
---

# Vault Metadata Schema — Canonical

One schema. Every note, every agent output, every blueprint.
The fields that exist on a note ARE its workflow state.
Dataview queries in HOME.md drive the async queue from this schema.

---

## Universal Frontmatter

```yaml
# IDENTITY
type: evidence | task | dead-drop | thread | handoff | brief | entity | collab-export | observer-drop
status: pending | awaiting-human | claimed | in-progress | completed | annotated | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []

# EVIDENCE IDENTITY (evidence notes + agent deliveries)
evidence_id: ""
source_file: scripts/audit_results/FILENAME_RUNNNN.json   # canonical repo path
source_sha256: ""
local_path: /mnt/d/0local/gitrepos/.../FILENAME.json      # absolute WSL path
git_commit: ""
source_type: agent-research | tabular | mhtml | pdf | json | vision | osint

# QUALITY
confidence_level: 0.00       # 0.0–1.0
source_quality: unverified | corroborated | confirmed
hypothesis_support: []       # [H1, H2, ...]
tier:                        # 1 | 2 | 3 | 4
pipeline_run: RUNNNN

# DATES
date_collected: YYYY-MM-DD
date_analyzed: YYYY-MM-DD

# RELATIONSHIPS
parent:
  - "[[...]]"
sibling:
  -
child:
  -

# MEMORY ROUTING (drives Dataview + membot promotion)
memory_lane: inbox | queue | drops | annotation-queue | observer | collab | nectar | honey | session | archived
promotion_state: capture | promoted | crystallized
vault_path: ""               # where this note lives in vault
faerie_session: ""           # session ID that created this note
blueprint: "[[Name.blueprint]]"

# CHAIN (agent writes at creation — human does NOT edit)
chain_id: criticalexposure
chain_seq: 0
prev_hash: ""
agent_hash: ""
agent_author: ""
agent_signed: ""

# RESEARCHER SIGNATURE (optional — Ed25519/YubiKey for court-grade named signing)
sig: ""
sig_fp: ""
sig_ts: ""
sig_hw: false

# ANNOTATION COMMIT (note_sign.py fills — do not edit manually)
ann_hash: ""
ann_ts: ""
```

---

## Type-Specific Additional Fields

### task
```yaml
task_id: TASK-YYYYMMDDHHmm
queue_task_id:
task_type: work | research | triage | review
priority: HIGH | MED | LOW
assignee:
requester:
skill_required:
deadline:
completed_date:
output_files: []
output_location:
```

### dead-drop
```yaml
drop_type: DISCOVERY | ALERT | HANDOFF | REQUEST | QUESTION
from: human | agent | session-ID
to: all | human | session-ID
read: false
read_at:
```

### thread
```yaml
thread_title: ""
participants: []
needs_response_from: []    # "human" | session-ID — drives HOME.md queue
last_activity:
```

### collab-export
```yaml
export_date:
source_team:
inv_id: criticalexposure
mode: semaphore | ed25519
honey_included: true | false
pii_scanned: true | false
pii_clean: true | false
chain_verified: true | false
```

---

## How Dataview Uses This

| HOME.md panel | Field queried |
|---|---|
| Annotate These | `tier = 1 AND ann_hash = null` |
| Unread Drops | `type = "dead-drop" AND read = false` |
| Tasks awaiting review | `type = "task" AND status = "awaiting-human"` |
| Memory promotion queue | `promotion_state = "capture"` |
| Agent activity | `status = "claimed" OR status = "in-progress"` |

---

## Workflow Phase → promotion_state

```
INGEST    → promotion_state: capture   (agent wrote it, human hasn't seen it)
ANNOTATED → ann_hash filled            (human annotated + note_sign.py commit)
PROMOTED  → promotion_state: promoted  (human marked it ready for membot)
CRYSTALIZED → promotion_state: crystallized  (distilled to HONEY.md — cites "in vault")
```

Setting `promotion_state: promoted` on any note is the signal to membot.
Membot processes at session end: promoted notes → NECTAR.md entries.
faerie crystallize: NECTAR entries → HONEY.md (dense, cross-session seed).

---

## Vault Role: Annotation Interface (Not Forensic Store)

The vault is the **human annotation GUI** layered on top of an immutable forensic pipeline.
It is NOT the forensic data store. Sensitive forensic material lives locally, gitignored:

| What | Where | Why |
|------|-------|-----|
| Master COC (hash-chained) | `{repo}/.claude/forensics/` (gitignored) | Court-grade, never on remote |
| Agent tool call logs | `~/.claude/memory/forensics/` (gitignored) | System-level audit, local only |
| Raw evidence data | `{repo}/rawdata/` or `0-CriticalRAWDATA/` | Sensitive, never in vault |
| Session manifests (JSON) | `~/.claude/hooks/state/session-manifests/` | Machine-readable, local |

The vault contains:
- **Agent deliveries** (findings, briefs, summaries) — in `Agent-Outbox/`
- **Human annotations** — in `30-Evidence/` (promoted from Agent-Outbox by human)
- **Dashboards** — live Dataview views of investigation state
- **Session manifests** (Markdown) — in `Dashboards/session-manifests/`
- **Pipeline gate status** — in `Dashboards/Pipeline-Gates.md`

### Light COC in Vault Notes

Each vault note has enough COC to trace back to the forensic store:

```yaml
# In vault note frontmatter:
source_file: scripts/audit_results/FILENAME_RUNNNN.json  # what produced this
source_sha256: "abc123..."                                 # hash of source at time of sync
agent_author: "evidence-analyst"                           # which agent
agent_hash: "sha256:..."                                   # agent state hash
faerie_session: "session-abc"                              # which session

# Human annotation (added by researcher):
ann_hash: "sha256:..."        # hash of annotation content (note_sign.py)
ann_ts: "2026-03-25T..."      # when annotated
sig: "ed25519:..."            # optional YubiKey signature
```

This means: "I received THIS output from agent X with state Y, and I returned THIS annotation."
The full forensic detail lives in the local COC logs — the vault note is the receipt.

---

## New Types: session-manifest, gate-review

### session-manifest
```yaml
type: session-manifest
date: YYYY-MM-DD
ts: ISO8601
session_id: ""
plan: ""                  # plan file name that drove this session
tags: [manifest, auto-sync, session-end]
```

### brief
```yaml
brief_type: session-summary | stage-summary | finding-promotion | hypothesis-update | blocker-flag
schema_version: "1.0"
investigation_id: inv-critical-exposure
sprint_id: sprint-3
session_id: ""
run_id: RUN009
phase: SEED | DEEPEN | EXTEND | FULL | ad-hoc
pipeline_stage: ""                         # sub-stage: "data-ingest-2of3"
agent_version: "data-scientist_2026-03-22_0.95"  # {type}_{date}_{score}
coc_session_file: ""                       # path to session COC .jsonl
coc_entry_hashes: []                       # specific COC entries that drove conclusions
hypothesis_touched: []                     # [H1, H4, ...]
evidence_tier_touched: []                  # [1, 2]
confidence_delta: {}                       # {H4: +0.08, H1: +0.02}
blockers: []
review_status: unreviewed | under-review | endorsed | challenged | promoted | archived
promoted_at: ""
promotion_chain: []                        # append timestamps as status changes
```

### gate-review
```yaml
type: gate-review
gate: GATE_1_SEED_REVIEW | GATE_2_HYPOTHESIS_CHECK | GATE_3_CONVERGENCE_REVIEW | GATE_4_PRE_PUBLICATION
gate_num: 1-4
status: pending | passed | blocked
corrections_count: 0
hypothesis_sealed: false
```

---

## Agent Output → Vault Sync

`vault_narrative_sync.py` writes notes using this schema.
Fields mapped from `scripts/audit_results/*.json`:

| JSON field | Vault frontmatter |
|---|---|
| `run_id` | `pipeline_run` |
| `source_file` | `source_file` |
| `sha256` | `source_sha256` |
| `confidence` | `confidence_level` |
| `tier` | `tier` |
| `hypothesis` | `hypothesis_support` |
| `git_commit` | `git_commit` |

Script writes `agent_hash` at creation time (SHA256 of script state + content).
Human never edits chain section. `note_sign.py verify` checks the chain.
