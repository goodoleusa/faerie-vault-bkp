# Artifact Registry Specification — Universal Discovery & State System

**Status:** Design specification (not implemented yet)  
**Date:** 2026-04-07  
**Author:** System Architecture  
**Purpose:** Single source of truth for what Claude artifacts exist, what changed this session, and what's stale

---

## 1. Problem Statement

Claude generates and modifies artifacts across the entire system:

- **Agent cards** (`~/.claude/agents/*.md`) — subagent identity, training, KPIs
- **Skill files** (`.claude/skills/*/SKILL.md`) — skill definitions, constraints
- **Rules** (`~/.claude/rules/*.md`) — universal/project rules, equilibrium checks
- **Memory files** (`~/.claude/memory/*.md`, `{repo}/.claude/memory/*.md`) — HONEY, NECTAR, REVIEW-INBOX, pollen
- **Hook scripts** (`~/.claude/hooks/*.py`, `~/.claude/hooks/state/*.json`) — orchestration, COC, tracking
- **Pollen/scratch** (`{repo}/.claude/memory/pollen-*.md`, `scratch-*.md`) — session-scoped working notes
- **Vault docs** (mirror via `~/.claude/memory/vault-index.json`) — Obsidian annotations, dashboards
- **Output manifests** (`~/.claude/hooks/state/wave*-result.json`, session-manifests, task-states)

**Current gap:** Faerie and other orchestrators must discover these artifacts piecemeal (globbing, reading indexes, inferring state). There is no unified registry that answers:

1. What artifacts exist (topology)?
2. What changed in the last session?
3. What hasn't been read/validated in N days (stale)?
4. What can be garbage-collected safely?
5. What is the size/token cost of the artifact ecosystem?

This leads to **fragmented knowledge:** Faerie reads session manifests to find agent returns, reads HONEY.md to get context, scans agent cards for training status, manually infers what's "active" by checking timestamps. Memory promotion agents (membot) don't know if a fact already exists in NECTAR before appending (causing duplicates or stale reps). Garbage collection is never triggered (old pollen files, stale task-states, archived manifests accumulate).

**Solution:** A universal **append-only JSONL artifact registry** that becomes the single query point for: "what exists, what changed, what's stale, what can be deleted."

---

## 2. Design Rationale

### 2.1 Why JSONL (Not a Single JSON File)?

- **Append-only durability:** Each event is immutable; no risk of corruption on partial write
- **Forensic chain:** Hash-chained entries (each entry includes `prev_entry_hash`) for auditable trail
- **Concurrent safety:** Multiple hooks can append without locking (WSL/Linux safe)
- **History retention:** Every change is recorded; no overwrite means no "lost history" due to compaction
- **Analytical queryability:** Tools can aggregate/deduplicate on the fly without loading entire registry into memory
- **Incremental sync:** Faerie/agents can query "what changed since last query timestamp" — no need to rebuild full state

### 2.2 Why Append-Only?

Artifacts are mutable (agent cards get new training entries, rules get updated, pollen appends), but the **registry of those changes** must never be rewritten. This matches the forensic COC pattern already in use for training logs and session manifests. A court expert can audit the full history of what Claude created/modified without gaps.

### 2.3 Who Writes to the Registry?

**PostToolUse hook** (automatic, every tool call): Detects Write/Edit operations on artifact paths, logs the change.

**Periodic scan** (at `/faerie` startup): Glob-scan the artifact directories, compare file hashes against last known state, emit deltas.

**Manual flush** (agent-initiated, at end of session): Membot or context-manager calls `artifact_registry.py --flush-session` to batch-write working observations, staleness checks, and garbage-collection suggestions.

This **three-layer approach** ensures:
- Immediate detection of explicit file writes (hook capture)
- Discovery of stale/untracked artifacts (periodic scan)
- Deliberate memory updates and cleanup recommendations (manual flush)

---

## 3. Core Architecture

### 3.1 Registry File

**Location:** `~/.claude/hooks/state/artifact-registry.jsonl`

**Size expectation:** ~500 entries per month (at 3-4 artifact changes per session × ~30-50 sessions/month). Each entry is ~300-500 bytes (path, hash, metadata). Total: ~150-250 KB/month. Unbounded (append-only forever).

**Gitignore:** No — the registry itself is part of the forensic archive. `~/.claude/hooks/state/` is already tracked in some form for audit purposes.

### 3.2 Core JSONL Entry Schema

```json
{
  "entry_id": "art-20260407-001234",
  "ts": "2026-04-07T14:32:00.123456Z",
  "session_id": "claude-session-48116",
  "operation": "create|update|delete|read|validate|stale_flag|gc_suggest",
  "artifact_type": "agent_card|skill|rule|memory|hook|pollen|vault|output_manifest",
  "path": "/absolute/path/to/artifact.md",
  "subtype": "training_entry|rule_update|memory_promotion|manifest_return",
  "change_type": "entry_added|entry_removed|content_updated|hash_changed|metadata_changed",
  "size_bytes": 4096,
  "size_tokens": 340,
  "hash_before": "sha256:abc...",
  "hash_after": "sha256:def...",
  "prev_entry_hash": "sha256:xyz...",
  "entry_hash": "sha256:abc...",
  "metadata": {
    "agent_type": "evidence-curator",
    "rule_category": "memory",
    "memory_level": "project",
    "skill_name": "data-ingest",
    "status": "in_progress|completed|failed",
    "burst_token_cost": 45,
    "estimated_read_frequency": "every_session|weekly|monthly|rarely"
  },
  "source": "PostToolUse_hook|periodic_scan|manual_flush|agent_self_report",
  "staleness": {
    "last_read_ts": "2026-04-05T10:00:00Z",
    "last_validated_ts": "2026-03-25T00:00:00Z",
    "expected_ttl_days": 90,
    "is_stale": false
  },
  "references": [
    "/path/to/related/artifact1",
    "/path/to/related/artifact2"
  ],
  "gc_candidate": false,
  "gc_reason": null,
  "gc_severity": "safe|caution|dangerous",
  "note": "optional human-readable context"
}
```

**Field Definitions:**

| Field | Type | Purpose | Required? | Notes |
|-------|------|---------|-----------|-------|
| `entry_id` | string | Unique ID for this registry entry (not the artifact) | Yes | Format: `art-YYYYMMDD-sequential` |
| `ts` | ISO8601 | When the change occurred | Yes | UTC, 6-digit microseconds |
| `session_id` | string | Claude session ID | No | Omit if not in a session context (manual flush) |
| `operation` | enum | What happened to the artifact | Yes | One of: create, update, delete, read, validate, stale_flag, gc_suggest |
| `artifact_type` | enum | Which class of artifact | Yes | Nine types (see 3.3 below) |
| `path` | string | Absolute path to artifact | Yes | Must be absolute; no `~/` or relative paths |
| `subtype` | enum | Granular artifact variant | No | E.g. `training_entry` for agent cards |
| `change_type` | enum | What specifically changed | No | E.g. `entry_added` vs `content_updated` |
| `size_bytes` | integer | File size in bytes | No | Omit if deletion or read-only operation |
| `size_tokens` | integer | Estimated token cost | No | For budget tracking |
| `hash_before` | string | SHA256 of content before change | No | Format: `sha256:{hex}` |
| `hash_after` | string | SHA256 of content after change | No | Format: `sha256:{hex}` |
| `prev_entry_hash` | string | Hash of previous registry entry | Yes | Creates immutable chain |
| `entry_hash` | string | SHA256 of this registry entry's canonical fields | Yes | Forensic proof this entry is immutable |
| `metadata` | object | Type-specific context (agent type, rule category, etc.) | No | Flexible; see examples below |
| `source` | enum | How this entry was discovered | Yes | PostToolUse_hook, periodic_scan, manual_flush, agent_self_report |
| `staleness` | object | TTL tracking, last-read, last-validation timestamps | No | Used by stale-detection queries |
| `references` | array | Other artifact paths this one depends on or cites | No | Enables dependency tracing |
| `gc_candidate` | boolean | Should this artifact be garbage-collected? | No | Set by GC review pass |
| `gc_reason` | string | Why GC is suggested (never read in 180d, etc.) | No | Human-readable rationale |
| `gc_severity` | enum | GC risk level (safe/caution/dangerous) | No | E.g. agent cards = dangerous, old pollen = safe |
| `note` | string | Optional human context | No | Useful for manual cleanup decisions |

### 3.3 Artifact Types (Nine Categories)

```
1. agent_card
   - Path: ~/.claude/agents/{type}.md
   - Subtypes: training_entry, KPI_update, capability_bump, OTJ_learning
   - Metadata: {agent_type, last_score, tier}
   - Read frequency: on-demand (when agent spawned)
   - TTL: permanent

2. skill
   - Path: ~/.claude/skills/{skill_name}/SKILL.md
   - Subtypes: constraint_update, API_change, deprecation
   - Metadata: {skill_name, invocation_count}
   - Read frequency: on-demand (when skill invoked)
   - TTL: permanent

3. rule
   - Path: ~/.claude/rules/{category}.md or {repo}/.claude/rules/{category}.md
   - Subtypes: rule_addition, clarification, supersedure
   - Metadata: {rule_category, enforcement_level, affected_agents}
   - Read frequency: session_start (rule contextualization)
   - TTL: permanent

4. memory
   - Path: ~/.claude/memory/{HONEY|NECTAR|REVIEW-INBOX|REVIEW-HOT|.md}
   - Path: {repo}/.claude/memory/{HONEY|pollen-|scratch-|REVIEW-INBOX}.md
   - Subtypes: entry_added, crystallization, memory_promotion
   - Metadata: {memory_level, topic, confidence, NECTAR_entry_count}
   - Read frequency: HONEY=every session, NECTAR=tail-30 on investigation, REVIEW-INBOX=human read
   - TTL: unbounded for NECTAR/REVIEW-INBOX, 30d for pollen, 7d for scratch

5. hook
   - Path: ~/.claude/hooks/{name}.py or ~/.claude/hooks/state/{name}.json|.jsonl
   - Subtypes: PostToolUse, stop_hook, pre_compact, periodic_scan
   - Metadata: {hook_type, error_count, last_execution_ts}
   - Read frequency: on event (PostToolUse) or session boundary (stop/start)
   - TTL: permanent (hooks are part of orchestration)

6. pollen
   - Path: {repo}/.claude/memory/pollen-{SESSION_ID}.md
   - Subtypes: <!-- MEM --> block count, HIGH_flag_count
   - Metadata: {session_id, MEM_block_count, file_size_bytes}
   - Read frequency: session_end (promotion to NECTAR)
   - TTL: 7 days (archived to forensics after promotion, then GC candidate)

7. vault_doc
   - Path: $CT_VAULT/... (mirrored via index)
   - Subtypes: human_annotation, agent_outbox, dashboard
   - Metadata: {vault_section, write_source (human|agent), sync_status}
   - Read frequency: rarely (direct Obsidian manipulation)
   - TTL: sync'd to local vault; GC not applicable

8. output_manifest
   - Path: ~/.claude/hooks/state/session-manifests/*.json, wave*-result.json, task-states/*.json
   - Subtypes: session_manifest, wave_result, task_state, decision_log
   - Metadata: {manifest_type, agent_count, deliverables, resolved_tasks}
   - Read frequency: faerie wave assembly, agent return processing
   - TTL: 30 days (archived to forensics, GC candidate after 60d)

9. forensic_checkpoint
   - Path: ~/.claude/memory/forensics/*, {repo}/.claude/forensics/*
   - Subtypes: COC entry, hash manifest, deletion log
   - Metadata: {forensic_type, entry_count, seal_status}
   - Read frequency: on-demand (validation/audit)
   - TTL: permanent (immutable by law)
```

---

## 4. Integration Points

### 4.1 PostToolUse Hook (Automatic Capture)

**Trigger:** Every Read, Write, Edit, Bash operation.

**Logic:**
```
IF operation in (Write, Edit) AND path matches ARTIFACT_GLOB_PATTERNS:
  1. Compute hash_after
  2. If path exists in artifact-registry and hash_after != last known hash:
     - operation = "update"
     - change_type = infer from diff (entry_added|removed|content_updated)
     - size_bytes = new file size
     - size_tokens = estimate via tokenizer
  3. Else if path not in registry:
     - operation = "create"
     - hash_before = empty / hash_after = computed
  4. Append entry to artifact-registry.jsonl
  5. Set session metadata: "artifact_writes_this_session += 1"

IF operation = "Delete" AND path matches ARTIFACT_GLOB_PATTERNS:
  [This triggers deletion-safety rule — must be confirmed]
  1. operation = "delete"
  2. hash_before = last known
  3. hash_after = empty / moved to .claude/garbage/
  4. Append entry + move file to garbage folder
```

**Artifact glob patterns:**
```
~/.claude/agents/**/*.md
~/.claude/rules/**/*.md
~/.claude/skills/**/*.md
~/.claude/memory/*.md
~/.claude/memory/forensics/*
~/.claude/hooks/state/*.json
~/.claude/hooks/state/*.jsonl
{REPOS}/.claude/memory/*.md
{REPOS}/.claude/rules/**/*.md
{REPOS}/.claude/forensics/*
$CT_VAULT/**.md (vault mirror)
```

### 4.2 Periodic Scan (at /faerie Startup)

**Trigger:** `/faerie` command → context-roundup phase → artifact discovery.

**Logic:**
```
1. Read last entry in artifact-registry.jsonl → get last_scan_ts
2. For each ARTIFACT_GLOB_PATTERN:
   a. Glob all matching files (with mtime)
   b. Skip if file mtime < last_scan_ts (assume PostToolUse hook caught it)
   c. Compute hash of file
   d. Look up path in artifact-registry.jsonl:
      - If path exists AND hash == last known hash: skip
      - If path exists AND hash != last known hash: append UPDATE entry
      - If path not in registry: append CREATE entry
      - If path was in registry but file gone: append DELETE entry
3. Check for STALE artifacts:
   - If last_read_ts > 90 days ago AND artifact_type NOT in (forensic_checkpoint, rule)
     → append stale_flag entry
4. Check for GC candidates:
   - If artifact_type in (pollen, output_manifest) AND file_mtime > 60 days
     AND last_read_ts > 30 days
     → append gc_suggest entry with gc_severity = "safe"
5. Emit summary: "Scan complete: {N} CREATE, {M} UPDATE, {K} stale, {J} GC candidates"
```

### 4.3 Manual Flush (Agent-Initiated, Session End)

**Trigger:** Membot or context-manager calls `artifact_registry.py --flush-session --session-id {id}`.

**Logic:**
```
1. Read pollen-{SESSION_ID}.md → extract all <!-- MEM --> blocks
2. For each MEM block:
   a. If cat=HEADLINE or cat=CONNECTION or cat=THREAD:
      → Append entry: operation=validate, staleness.last_validated_ts=now
      → Cross-reference to NECTAR for promotion tracking
3. Check for "double promotion":
   - Read ~/.claude/memory/NECTAR.md
   - For each pollen finding, check if semantic duplicate exists in NECTAR
   - If yes: append entry: operation=read, note="semantic_duplicate_in_NECTAR"
   - Memory-keeper will skip promotion on next run
4. Compute session metrics:
   - Total MEM blocks written: {N}
   - HIGH flags: {M}
   - Cross-project connections: {K}
   - Artifacts touched this session: {J}
5. Append summary entry: operation=session_flush, metadata={metrics}
6. Rotate pollen to archive:
   - Move pollen-{SESSION_ID}.md → ~/.claude/memory/forensics/pollen-archive/{date}-{SESSION_ID}.md
   - Append entry: operation=delete, note="archival (not GC)"
```

---

## 5. Discovery API (Query Interface)

The registry is queryable via `artifact_registry.py`:

### 5.1 Core Queries

```bash
# List all artifacts of a type
artifact_registry.py --type agent_card --output json

# Get artifacts changed since timestamp
artifact_registry.py --changed-since "2026-04-07T12:00:00Z" --output json

# Find stale artifacts (not read in N days)
artifact_registry.py --stale-threshold 90 --output json

# Get garbage collection candidates
artifact_registry.py --gc-candidates --severity "safe|caution|dangerous" --output json

# Get artifact topology (what depends on what)
artifact_registry.py --topology --output graphviz

# Check hash consistency (post-compaction validation)
artifact_registry.py --validate-hashes --output json

# Get session summary (how many artifacts changed)
artifact_registry.py --session {SESSION_ID} --output json

# Export for faerie roundup
artifact_registry.py --export-roundup --output json
```

### 5.2 Faerie Integration: Context-Roundup Usage

At `/faerie` startup, context-roundup phase:

```python
# Get all artifacts changed since last faerie cycle
changed = artifact_registry.get_changed_since(faerie_state.last_cycle_ts)

# Categorize for briefing
agent_changes = {a for a in changed if a.artifact_type == "agent_card"}
rule_changes = {a for a in changed if a.artifact_type == "rule"}
memory_changes = {a for a in changed if a.artifact_type == "memory"}

# Build faerie brief snapshot
brief = {
    "session_id": ...,
    "artifacts_changed": len(changed),
    "new_agent_trainings": len(agent_changes),
    "rule_updates": len(rule_changes),
    "memory_promotions": len([m for m in memory_changes if m.operation == "validate"]),
    "gc_candidates": len(artifact_registry.get_gc_candidates(severity="safe")),
    "stale_count": len(artifact_registry.get_stale(threshold_days=90))
}

# Surface to faerie for decision
if brief["gc_candidates"] > 5:
    faerie_alerts.append(("GC", f"Safe cleanup available for {N} artifacts"))
if brief["stale_count"] > 10:
    faerie_alerts.append(("STALE", f"Consider validating {N} artifacts >90d old"))
```

### 5.3 Memory-Keeper Usage (Duplicate Prevention)

When promoting a pollen entry to NECTAR:

```python
# Check if semantic duplicate already in NECTAR
existing = artifact_registry.get_artifacts(
    artifact_type="memory",
    path="/home/user/.claude/memory/NECTAR.md"
)

# Cross-check: is this entry (content hash) already there?
for existing_entry in existing:
    if entry_hash == existing_entry.hash_after:
        # Exact duplicate — skip promotion
        artifact_registry.append(
            operation="read",
            path=pollen_path,
            note=f"semantic_duplicate_skipped: {existing_entry.ts}"
        )
        return SKIP

# Otherwise: promote normally, append entry
artifact_registry.append(
    operation="validate",
    artifact_type="memory",
    path=nectar_path,
    change_type="entry_added",
    metadata={"promoted_from": pollen_path, "entry_count": new_count}
)
```

---

## 6. Registry Entry Chaining & Forensics

### 6.1 Immutable Hash Chain

Every entry includes:
- `prev_entry_hash`: SHA256 of the PREVIOUS entry in the registry
- `entry_hash`: SHA256 of THIS entry's canonical fields (all fields except `entry_hash` itself)

**Why:** Creates an immutable proof that:
1. No entry in the registry has been tampered with (hash mismatch breaks the chain)
2. No entries have been reordered (prev_entry_hash links are sequential)
3. No entries have been deleted (gaps in the hash chain)

**Forensic value:** An expert can audit the entire registry in ~2 seconds:
```bash
artifact_registry.py --verify-chain --output json
# Returns: {"chain_valid": true, "entries": 5042, "gaps": 0, "tampering_detected": false}
```

### 6.2 Canonical Entry Hash Computation

Fields included in `entry_hash` (in order, as JSON):
```
[
  entry_id,
  ts,
  operation,
  artifact_type,
  path,
  size_bytes,
  size_tokens,
  hash_before,
  hash_after,
  prev_entry_hash,
  source,
  metadata.agent_type (if present),
  metadata.rule_category (if present),
  note
]
```

Computed as: `sha256(canonical_json_serialization)` (no whitespace, sorted keys).

---

## 7. Example Use Cases

### 7.1 Faerie Startup (Session Begin)

```
/faerie startup → context-roundup phase
  1. Query: artifact_registry.get_changed_since(last_faerie_cycle_ts)
     Result: 23 artifacts changed (8 agent card trainings, 4 rule clarifications, 11 memory promotions)
  
  2. Query: artifact_registry.get_stale(threshold_days=90)
     Result: 3 artifacts not read since March 15
     → Add to briefing: "3 artifacts >90d stale — recommend validation"
  
  3. Query: artifact_registry.get_gc_candidates(severity="safe")
     Result: 12 old pollen files + 5 archived task-states ready for deletion
     → Add to briefing: "17 safe cleanup items available"
  
  4. Build faerie-brief.json context bundle with:
     - Recent agent training learnings (agent card updates)
     - Updated rules (rule changes)
     - Memory promotions summary
     - Stale/GC alerts
  
  5. Load HONEY.md, NECTAR.md tail-30 as normal
     (but now faerie knows exactly what changed since last session)
```

**Savings:** Faerie doesn't have to glob+read 40+ agent cards to find training updates; registry tells it which ones changed. Startup time reduced ~10%.

### 7.2 Memory-Keeper Promotion (Preventing Duplicates)

```
Session end → memory-keeper processes pollen-{SID}.md
  
  For each <!-- MEM cat=HEADLINE --> block:
    1. Compute content_hash
    2. Query: artifact_registry.find_artifact_by_hash(hash, artifact_type="memory")
       Result: Found in ~/.claude/memory/NECTAR.md ts=2026-04-06, entry_hash=xyz...
    3. If found:
       → Skip promotion (already present)
       → Log: operation=read, note="duplicate_prevention"
    4. Else:
       → Promote to NECTAR normally
       → Log: operation=validate, change_type=entry_added
  
  Summary: Prevented 2 duplicate promotions, promoted 7 unique findings
```

**Savings:** Prevents stale fact repetition in NECTAR (which was growing 20% faster than needed).

### 7.3 Garbage Collection Review

```
Faerie GC phase (monthly, on demand):
  
  Query: artifact_registry.get_gc_candidates(severity="safe")
  Result:
    [
      {path: ~/.claude/memory/pollen-claude-20260101-xyz.md, reason: "not_read_180d", severity: "safe"},
      {path: ~/.claude/hooks/state/session-manifests/2026-01-15-manifest.json, reason: "not_read_180d", severity: "safe"},
      ...
    ]
  
  For each candidate:
    1. Double-check: artifact_registry.get_last_read(path) > 180 days? Yes.
    2. Double-check: artifact_type in safe_to_delete list? Yes (pollen, manifest).
    3. Append to GC log: operation=gc_suggest, gc_severity="safe"
       → This creates a human-reviewable audit trail
    4. (Optional) Execute cleanup:
       mv {path} ~/.claude/garbage/{date}-{hash8}/
       artifact_registry.append(operation=delete, ...)
  
  Summary: Cleaned up 28 safe items (3.2 MB freed), logged all in audit trail
```

**Savings:** Prevents accidental deletion of valuable artifacts; enables safe cleanup of gigabytes of old session/manifest files.

### 7.4 Staleness Detection & Validation

```
Weekly validation pass:
  
  Query: artifact_registry.get_stale(threshold_days=90)
  Result:
    [
      {path: ~/.claude/agents/admin-sync.md, last_read: 2026-01-10, status: "stale"},
      {path: ~/.claude/rules/subagent-enforce.md, last_read: 2026-02-20, status: "stale"},
    ]
  
  For each stale artifact:
    1. Read artifact
    2. Validate against its parent (e.g., admin-sync.md agent card)
       - Check: is the KPI still current? Yes → mark valid
       - Check: has the agent ever been spawned? If not → mark review_candidate
    3. Update staleness entry:
       artifact_registry.append(operation=validate, staleness.last_validated_ts=now)
  
  Result: 2 artifacts validated as current, 0 review candidates
```

**Savings:** Ensures rules and agent cards don't rot; proactive detection of obsolete configurations.

---

## 8. Schema Variants by Artifact Type

### 8.1 Agent Card Entry

```json
{
  "operation": "update",
  "artifact_type": "agent_card",
  "subtype": "training_entry",
  "change_type": "entry_added",
  "path": "~/.claude/agents/evidence-curator.md",
  "metadata": {
    "agent_type": "evidence-curator",
    "last_score": 0.94,
    "tier": 2,
    "learning_type": "on_the_job",
    "training_date": "2026-04-07",
    "prev_score": 0.91,
    "delta": 0.03
  }
}
```

### 8.2 Rule Update Entry

```json
{
  "operation": "update",
  "artifact_type": "rule",
  "subtype": "rule_addition",
  "path": "~/.claude/rules/core.md",
  "metadata": {
    "rule_category": "core",
    "enforcement_level": "strict",
    "affected_agents": ["workflow-orchestrator", "membot", "performance-eval"],
    "new_section": "Equilibrium (system-wide guardrail)",
    "reason": "prevent_over-budget_files"
  }
}
```

### 8.3 Memory Promotion Entry

```json
{
  "operation": "validate",
  "artifact_type": "memory",
  "subtype": "memory_promotion",
  "change_type": "entry_added",
  "path": "~/.claude/memory/NECTAR.md",
  "metadata": {
    "memory_level": "global",
    "promoted_from": "/mnt/d/0local/gitrepos/cybertemplate/.claude/memory/pollen-claude-20260407-xyz.md",
    "entry_count": 1243,
    "new_entries": 12,
    "investigation_id": "inv-doge-treasury"
  }
}
```

### 8.4 Pollen Archival Entry

```json
{
  "operation": "delete",
  "artifact_type": "pollen",
  "change_type": "content_deleted",
  "path": "/mnt/d/0local/gitrepos/cybertemplate/.claude/memory/pollen-claude-20260407-xyz.md",
  "metadata": {
    "session_id": "claude-20260407-48116",
    "reason": "archival_after_promotion",
    "mem_block_count": 12,
    "high_flags": 2
  },
  "note": "Moved to ~/.claude/memory/forensics/pollen-archive/2026-04-07-pollen-xyz.md"
}
```

### 8.5 GC Suggestion Entry

```json
{
  "operation": "gc_suggest",
  "artifact_type": "output_manifest",
  "path": "~/.claude/hooks/state/session-manifests/2026-01-15-manifest.json",
  "metadata": {
    "manifest_type": "session_manifest",
    "file_mtime": "2026-01-15T00:00:00Z"
  },
  "staleness": {
    "last_read_ts": "2026-01-16T02:00:00Z",
    "is_stale": true
  },
  "gc_candidate": true,
  "gc_reason": "not_read_in_180_days",
  "gc_severity": "safe"
}
```

---

## 9. Integration Checklist

### 9.1 Implementation Dependencies

- [ ] **PostToolUse hook** must be updated to log Write/Edit operations against artifact globs
- [ ] **artifact_registry.py** script (new) with:
  - [ ] Append logic with hash chaining
  - [ ] Query API (get_changed_since, get_stale, get_gc_candidates, etc.)
  - [ ] Validation (--verify-chain)
  - [ ] Export (--export-roundup for faerie)
- [ ] **context-roundup** phase updated to query registry for artifact deltas
- [ ] **memory-keeper** updated to use registry for duplicate prevention
- [ ] **Faerie briefing** extended to include artifact_changed count + stale/GC alerts
- [ ] **GC review tool** (new or integrated) to surface safe cleanup candidates

### 9.2 Faerie Workflow Integration

```
/faerie startup:
  → context-roundup
    → artifact_registry.get_changed_since() [NEW]
    → artifact_registry.get_stale() [NEW]
    → artifact_registry.get_gc_candidates() [NEW]
    → build faerie-brief.json with artifact summaries [UPDATED]

/run (agent execution):
  → PostToolUse hook logs artifact writes [UPDATED]

/handoff (session end):
  → membot uses registry for duplicate prevention [UPDATED]
  → artifact_registry.flush-session() [NEW]
  → optional: surface GC+stale alerts to user [NEW]

Optional: /garbage-collect (new command)
  → artifact_registry.get_gc_candidates(severity=user_input)
  → batch-clean with audit trail
```

---

## 10. Open Questions & Future Extensions

### 10.1 Dependency Tracking

**Question:** Should the registry track artifact dependencies? (e.g., "agent card X depends on rule Y, skill Z")

**Option A (Simple):** Store `references` array only (one-way pointers, what does this artifact cite).

**Option B (Rich):** Build a dependency graph (bidirectional: agent_card → rule, rule → agent_card). Enable impact analysis: "if rule X changes, which agents are affected?"

**Recommendation:** Start with Option A (references array). Implement graph-based queries only if faerie needs "show me all agents affected by this rule change" (for change advisory analysis).

### 10.2 Vault Mirroring

**Question:** How to index vault docs (`$CT_VAULT/...`) in the registry without replicating Obsidian's metadata?

**Current approach:** Store in `~/.claude/memory/vault-index.json` (manually curated) and mirror entries in artifact-registry as a second pass.

**Better approach:** Have vault-mutation-tracker.py (existing hook) also append to artifact-registry when vault files change. Requires vault to be mounted at a WSL path.

**Status:** Defer until vault integration is finalized. Mark vault entries as "synced_via_secondary" until then.

### 10.3 Artifact Versioning

**Question:** Should the registry track version history of artifacts (e.g., agent card version 3.2 → 3.3)?

**Recommendation:** No explicit versioning. Instead, use git history. The registry logs *that* a change happened; git logs *what changed*. This avoids duplication.

**Exception:** For forensic integrity (court cases), export the full artifact history via git archive + registry timeline for immutable proof.

### 10.4 Cross-Repo Aggregation

**Question:** For multi-repo setups (faerie, cybertemplate, flowsearch), should there be a unified registry or per-repo registries?

**Recommendation:** Single global registry at `~/.claude/hooks/state/artifact-registry.jsonl`. Each repo's artifacts (rules, pollen, memory) are tracked with their full paths. Queries can filter by repo:
```bash
artifact_registry.py --repo cybertemplate --type pollen
artifact_registry.py --repo flowsearch --type rule
```

### 10.5 Cost Tracking & Budget Enforcement

**Question:** Should the registry feed into token-optimizer for cost tracking?

**Recommendation:** Yes. The registry already computes `size_tokens` per artifact. Token-optimizer can query:
```python
total_tokens = artifact_registry.sum_tokens(
    artifact_type=["agent_card", "rule", "memory"],
    read_frequency="every_session"
)
# Result: ~18K tokens per session from startup reads
```

Use this to enforce: "all startup-read artifacts must fit in <25K tokens."

### 10.6 Automation Triggers

**Question:** Should the registry automatically trigger cleanup or validation?

**Recommendation:** No automatic action without human review. The registry provides the *decision data* (what's stale, what's a GC candidate, why); faerie/user makes the decision. This prevents accidental loss of valuable artifacts.

**Safe automated action:** Automatic archival of pollen after successful promotion (already in manual_flush protocol).

---

## 11. Security & Compliance

### 11.1 Immutability & Audit Trail

- Registry entries are append-only; no overwrites or deletions of historical records.
- Hash chain proves no tampering (forensic-grade audit trail).
- Every entry includes `source` (PostToolUse_hook, periodic_scan, manual_flush) → chain of custody clarity.

### 11.2 Privacy & Data Sensitivity

- Registry logs artifact **paths and metadata**, not content (content stays in the artifact itself).
- Paths may include investigation IDs (e.g., `inv-doge-treasury`); registry file itself is gitignored if sensitive.
- Agent names and rule categories are not sensitive; type info is non-confidential.

### 11.3 Forensic Court-Readiness

- Registry is court-admissible as a timeline of artifact lifecycle events.
- Hash chain provides cryptographic proof of integrity (expert witness can verify in seconds).
- Deletion log (in forensics/) provides immutable proof of what was removed and when.

---

## 12. Success Metrics

After implementation, validate:

1. **Discovery speed:** Faerie context-roundup takes <2 seconds to determine what changed (vs ~10 seconds globbing today).
2. **Duplicate prevention:** Memory-keeper skips 10+ duplicate promotions per month (based on semantic hash lookup).
3. **Garbage collection:** 50+ MB/month safely cleaned (pollen, old manifests) via registry suggestions.
4. **Staleness detection:** 3+ stale artifacts identified monthly, reviewed/revalidated proactively.
5. **Chain-of-custody:** Artifact lifecycle fully auditable; zero untracked changes.
6. **Context savings:** Startup reads reduced by 5-10% due to targeted briefing (instead of full HONEY.md + agent card globbing).

---

## 13. Migration & Rollout

### 13.1 Phase 1: Bootstrapping (Week 1)

- Deploy `artifact_registry.py` with `--init` flag to create baseline registry from current state.
- Scan all existing artifacts, compute hashes, initialize with `operation=baseline`.
- PostToolUse hook updated to log future writes.

### 13.2 Phase 2: Integration (Week 2-3)

- Context-roundup queries registry instead of globbing.
- Memory-keeper uses registry for duplicate check.
- Faerie briefing includes artifact-changed summary.

### 13.3 Phase 3: Monitoring (Week 3-4)

- Run validation: `artifact_registry.py --verify-chain` (check for gaps/tampering).
- Measure metrics (discovery speed, duplicate skips, GC candidates).
- Fine-tune stale thresholds based on real-world patterns.

### 13.4 Phase 4: Automation (Month 2)

- Enable optional auto-archival of pollen (safe operation).
- Add GC review command (user-triggered, audit-logged).
- Monthly validation pass (identify stale artifacts for revalidation).

---

## 14. Conclusion

The artifact registry transforms Claude's artifact ecosystem from a **fragmented piecemeal discovery problem** into a **unified, queryable, auditable system of record**. It enables:

- **Faerie** to know what changed without re-reading everything
- **Memory-keeper** to prevent duplicate promotions
- **GC review** to safely clean up with full audit trail
- **Staleness detection** to keep the system healthy
- **Forensic audit** to prove chain-of-custody for court

The design is:
- **Forensic-grade:** Append-only, hash-chained, immutable
- **Performance-conscious:** Lazy queries, no full registry loads, incremental syncs
- **Safe:** No auto-deletion, all changes auditable, rollback-capable via git
- **Extensible:** New artifact types can be added by extending the enum; new queries by adding discovery functions

Implementation can proceed in four phases (bootstrap → integrate → monitor → automate) over 4-6 weeks, with zero breaking changes to existing agents/faerie/skills.

