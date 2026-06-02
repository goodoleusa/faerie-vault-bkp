# COC + Sync Script Unified Architecture

**Status:** Design Phase v1.0  
**Date:** 2026-05-06  
**Investigation:** vault-infrastructure-overhaul  
**Tier:** 0x (genesis infrastructure)  

---

## Executive Summary

This document designs a unified vault synchronization and chain-of-custody (COC) system that:

1. **Unifies COC + Sync** — Single script handles both vault change detection and forensic logging
2. **Embeds Hash Tracking** — SHA256 hashes (before/after) into COC entries + vault frontmatter
3. **Injects Manifest Metadata** — Compass bearings, mission fields, task_ids flow into vault frontmatter
4. **Captures Mission Choices** — Agent decision rationale persisted in vault docs
5. **Validates Topology** — Wikilinks verify before sync completes

**Key Design Principles:**
- **Zero duplication:** All data flows once from swarmy/forensics/ → vault frontmatter
- **Immutability guarantee:** Pre/post hashes prove no tampering between sync and COC entry
- **Stigmergy-native:** Mission field + compass bearing = vault docs act as pheromone trails
- **Incremental:** Syncs only changed files; COC entries only for mutations

---

## Architecture Overview

### Current State (Separated Systems)

```
Vault Mutation        COC Logging          Manifest Routing
────────────         ──────────           ────────────────
5x_vault_hash_sync   0x_coc_writer        0x_mission_graph_sync
  (detects changes)    (logs operations)    (reads manifests)
  
↓                    ↓                     ↓
Frontmatter          coc.jsonl             mission-graph/
  (hash stamps)        (hash chains)         (wiki-links)
  
PROBLEM: Three separate systems; manifest metadata not in vault; hash chains disconnected
```

### Desired State (Unified)

```
sync-vaults-with-coc.py (NEW unified script)
  │
  ├─ Phase 1: Scan Changes
  │   └─ Compare {swarmy/forensics, ct-vault, faerie-vault}
  │     for mtime + size delta
  │
  ├─ Phase 2: Compute Hashes + Read Manifests
  │   ├─ SHA256(file_before) + SHA256(file_after)
  │   └─ Extract manifest metadata if associated
  │
  ├─ Phase 3: Write to Vault Frontmatter
  │   ├─ Inject compass_bearing, mission, task_id
  │   ├─ Stamp hash, prev_entry_hash
  │   └─ Validate wikilinks
  │
  ├─ Phase 4: Log to COC
  │   └─ Append single entry: timestamp, file, hash_before, hash_after, agent, mission, status
  │
  └─ Phase 5: Return Status Report
      └─ N files synced, M hashes verified, K wikilinks checked, 0 errors

Output:
  ├─ vault/*.md (updated frontmatter)
  ├─ forensics/coc.jsonl (appended entries)
  └─ {date}/sync-report.json (operational metrics)
```

---

## Phase 1: Change Detection

### Input: Three Vault Sources

1. **swarmy/forensics/{YYYY-MM-DD}/manifests/** — Agent outputs (task_id, compass_edge, mission)
2. **ct-vault/** (primary) — CyberOps knowledge base
3. **faerie-vault/** (secondary) — Portable faerie knowledge graph

### Algorithm: Timestamp + Size Delta

```python
def scan_changes(faerie_repo, vault_targets, days=1):
    """
    Scan for changed files using mtime and size.
    Return list of (file_path, mtime_before, mtime_after, agent, mission)
    """
    changes = []
    cutoff_time = datetime.now() - timedelta(days=days)
    
    # Load baseline hashes from prior sync
    baseline_hashes = load_baseline_hashes(".vault_sync_state.json")
    
    for vault_path in vault_targets:
        for file_path in vault_path.rglob("*.md"):
            file_stat = file_path.stat()
            file_hash = compute_hash(file_path)
            
            # Delta detection
            if file_hash != baseline_hashes.get(str(file_path)):
                changes.append({
                    "file_path": file_path,
                    "mtime": file_stat.st_mtime,
                    "size": file_stat.st_size,
                    "hash_new": file_hash
                })
    
    return changes
```

---

## Phase 2: Hash Computation + Manifest Association

### Hash Strategy: Before-After Chain

For each changed file:

```python
def compute_file_hashes(file_path):
    """
    Return (hash_before, hash_after, file_size, mtime)
    
    hash_before: SHA256 of file from prior sync (from .vault_sync_state.json)
    hash_after: SHA256 of file now
    """
    current_hash = sha256_file(file_path)
    baseline_hash = baseline_state.get(str(file_path), "genesis")
    
    return {
        "hash_before": baseline_hash,
        "hash_after": current_hash,
        "size_bytes": file_path.stat().st_size,
        "mtime": file_path.stat().st_mtime_ns
    }
```

### Manifest Association: Discover Linked Task

For vault files updated between T-N and T, scan forensics/manifests/{YYYY-MM-DD}/ for matching agent outputs:

```python
def find_associated_manifest(file_path, faerie_repo, days=1):
    """
    Match vault file to agent manifest by:
    1. Frontmatter task_id field (explicit link)
    2. File basename similarity to task_id
    3. Timestamp proximity (file mtime ≈ manifest timestamp)
    
    Return (manifest_data, manifest_path) or (None, None)
    """
    # Extract task_id from frontmatter if present
    task_id_in_fm = extract_frontmatter_field(file_path, "task_id")
    if task_id_in_fm:
        manifest = find_manifest_by_task_id(task_id_in_fm, faerie_repo)
        if manifest:
            return manifest
    
    # Fallback: basename similarity
    file_basename = file_path.stem.lower()
    manifests = load_manifests(faerie_repo, days=days)
    for task_id, manifest in manifests.items():
        if similarity(file_basename, task_id) > 0.8:
            # Verify timestamp proximity (within 1 hour)
            manifest_ts = parse_timestamp(manifest.get("timestamp"))
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if abs((manifest_ts - file_mtime).total_seconds()) < 3600:
                return manifest
    
    return None, None
```

---

## Phase 3: Vault Frontmatter Injection

### Metadata Injection Rules

For each changed vault file with associated manifest, inject into frontmatter:

| Manifest Field | Vault Frontmatter Field | Type | Required | Notes |
|---|---|---|---|---|
| `task_id` | `task_id` | string | conditional* | Link to forensics artifact |
| `mission` | `mission` | string | conditional* | Enables mission-graph discovery |
| `compass_edge` | `compass_bearing` | string (N/S/E/W) | optional | Navigation signal |
| `agent_type` | `agent_type` | string | optional | Who performed work |
| `timestamp` | `manifest_synced_at` | ISO8601 | conditional* | Forensic timestamp |
| `dashboard_line` | `dashboard_line` | string (≤80 chars) | optional | Summary of work |
| `status` | `manifest_status` | string | optional | Task completion state |

*conditional: Only inject if manifest found AND validated

### Frontmatter Injection Pseudocode

```python
def inject_manifest_metadata(file_path, manifest, existing_frontmatter):
    """
    Merge manifest metadata into vault file frontmatter.
    Preserve existing fields; add/update manifest fields.
    """
    fm_updated = existing_frontmatter.copy()
    
    # Core compass fields
    if manifest.get("task_id"):
        fm_updated["task_id"] = manifest["task_id"]
    
    if manifest.get("mission"):
        fm_updated["mission"] = manifest["mission"]
    
    compass_edge = manifest.get("compass_edge") or manifest.get("compass_bearing")
    if compass_edge:
        fm_updated["compass_bearing"] = compass_edge
        # Add direction symbol for quick visual scan
        symbols = {"N": "⛓️", "S": "🔓", "E": "➡️", "W": "⬅️"}
        fm_updated["bearing_icon"] = symbols.get(compass_edge, "")
    
    # Agent + timestamp
    if manifest.get("agent_type"):
        fm_updated["agent_type"] = manifest["agent_type"]
    
    if manifest.get("timestamp"):
        fm_updated["manifest_synced_at"] = manifest["timestamp"]
    
    # Summary
    if manifest.get("dashboard_line"):
        fm_updated["dashboard_line"] = manifest["dashboard_line"][:80]
    
    if manifest.get("status"):
        fm_updated["manifest_status"] = manifest["status"]
    
    return fm_updated
```

### Immutability Tracking: Pre-Sync Snapshot

Before modifying frontmatter, capture baseline state:

```python
def snapshot_frontmatter_before(file_path):
    """
    Save unmodified frontmatter before injection.
    Used to detect post-sync corruption.
    """
    fm, _, _ = parse_frontmatter(file_path)
    snapshot = {
        "file_path": str(file_path),
        "timestamp": datetime.now().isoformat(),
        "frontmatter_hash": sha256(json.dumps(fm, sort_keys=True))
    }
    return snapshot
```

---

## Phase 4: COC Entry Creation

### COC Entry Schema (Unified)

```json
{
  "type": "vault_sync",
  "timestamp": "2026-05-06T14:30:45Z",
  "file_path": "/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/mission-graph/task-123.md",
  "file_type": "vault",
  "operation": "inject-metadata",
  "agent_id": "documentation-engineer",
  "mission": "vault-infrastructure-overhaul",
  "task_id": "sync-vault-coc-design",
  "hash_before": "abc123...",
  "hash_after": "def456...",
  "hash_method": "sha256",
  "frontmatter_fields_injected": [
    "task_id", "mission", "compass_bearing", "manifest_synced_at", "dashboard_line"
  ],
  "metadata_source": {
    "manifest_path": "forensics/manifests/2026-05-06/..._manifest_vault-infrastructure-overhaul_documentation-engineer.json",
    "manifest_task_id": "sync-vault-coc-design",
    "manifest_found": true,
    "association_method": "task_id_match"
  },
  "validation_results": {
    "wikilinks_checked": 3,
    "wikilinks_valid": 3,
    "wikilinks_broken": 0,
    "frontmatter_valid": true
  },
  "prev_entry_hash": "previous_entry_sha256...",
  "entry_hash": "this_entry_sha256...",
  "status": "success"
}
```

### COC Entry Writing

```python
def write_coc_entry(coc_path, entry):
    """
    Append COC entry (JSONL format, one per line).
    Compute entry_hash and chain from prior entry.
    """
    # Get previous entry hash
    prev_hash = get_last_coc_entry_hash(coc_path)
    entry["prev_entry_hash"] = prev_hash
    
    # Compute entry hash (exclude entry_hash, sig, prev_entry_hash from canonical)
    canonical = {k: v for k, v in sorted(entry.items())
                 if k not in ["entry_hash", "sig", "sig_type", "prev_entry_hash"]}
    canonical["prev_entry_hash"] = prev_hash
    entry_hash = sha256(json.dumps(canonical, sort_keys=True, separators=(',', ':')))
    entry["entry_hash"] = entry_hash
    
    # Append to COC
    with open(coc_path, 'a') as f:
        f.write(json.dumps(entry) + "\n")
    
    return entry_hash
```

---

## Phase 5: Wikilink Validation

### Validation Rules

Before committing changes, verify all wikilinks in the file are resolvable:

```python
def validate_wikilinks(file_path, vault_roots):
    """
    Extract [[wiki-links]] and verify targets exist.
    Return (valid_count, broken_count, broken_links)
    """
    content = file_path.read_text()
    
    # Pattern: [[target|label]] or [[target]]
    wikilink_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    links = re.findall(wikilink_pattern, content)
    
    broken = []
    valid = []
    
    for link_target in links:
        # Resolve link: exact match, then fuzzy match
        resolved = resolve_wikilink(link_target, vault_roots)
        if resolved:
            valid.append((link_target, resolved))
        else:
            broken.append(link_target)
    
    return len(valid), len(broken), broken
```

### Validation Report in COC

```python
# In COC entry:
"validation_results": {
    "wikilinks_checked": 3,
    "wikilinks_valid": 3,
    "wikilinks_broken": 0,
    "frontmatter_valid": true,
    "summary": "All checks passed"
}

# If broken links found:
"validation_results": {
    "wikilinks_checked": 5,
    "wikilinks_valid": 4,
    "wikilinks_broken": 1,
    "broken_links": ["task-123"],
    "frontmatter_valid": true,
    "status": "warning"
}
```

---

## Phase 6: Operational Report

### Report Format (JSON + Summary)

```json
{
  "sync_session": "20260506T143045Z",
  "duration_seconds": 12.34,
  "vaults_scanned": [
    "/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED",
    "/mnt/d/0local/gitrepos/faerie-vault"
  ],
  "files_processed": {
    "total": 47,
    "changed": 8,
    "skipped_no_manifest": 3,
    "synced": 8
  },
  "hashes": {
    "computed": 8,
    "verified_no_corruption": 8,
    "hash_mismatches": 0
  },
  "metadata_injection": {
    "manifests_found": 8,
    "fields_injected_avg": 5.2,
    "mission_field_populated": 8,
    "compass_bearing_populated": 7
  },
  "wikilink_validation": {
    "links_checked": 23,
    "links_valid": 23,
    "links_broken": 0,
    "validation_pass_rate": 1.0
  },
  "coc_entries": {
    "appended": 8,
    "hash_chain_verified": true,
    "last_entry_hash": "xyz789..."
  },
  "errors": [],
  "warnings": [
    "task-consolidation-1: compass_bearing field not in manifest (defaulted to 'S')"
  ],
  "status": "success"
}
```

---

## Mission Choice Metrics Capture

### What We Capture

From manifest, extract agent's decision-making:

```python
def extract_mission_choice_metrics(manifest):
    """
    Extract mission choice data from manifest.
    Used for future analysis: "What decisions do agents make? Why?"
    """
    choice_data = {
        "task_id": manifest.get("task_id"),
        "agent_type": manifest.get("agent_type"),
        "timestamp": manifest.get("timestamp"),
        "choice": manifest.get("mission_choice", {}).get("choice"),
        "rationale": manifest.get("mission_choice", {}).get("rationale"),
        "alternatives_considered": manifest.get("mission_choice", {}).get("alternatives_considered"),
        "confidence": manifest.get("mission_choice", {}).get("confidence"),
        "discovered_work": manifest.get("discovered_work", [])
    }
    return choice_data
```

### Inject into Vault Frontmatter

```python
def inject_mission_choice_metrics(frontmatter, choice_metrics):
    """
    Add decision data to frontmatter under mission_choice section.
    """
    if choice_metrics.get("choice"):
        frontmatter["mission_choice"] = {
            "made_by": choice_metrics.get("agent_type"),
            "choice": choice_metrics["choice"],
            "rationale": choice_metrics.get("rationale", ""),
            "alternatives": choice_metrics.get("alternatives_considered", []),
            "confidence": choice_metrics.get("confidence", 0.5)
        }
    
    if choice_metrics.get("discovered_work"):
        frontmatter["discovered_work_summary"] = {
            "count": len(choice_metrics["discovered_work"]),
            "entries": choice_metrics["discovered_work"][:3]  # Top 3
        }
    
    return frontmatter
```

---

## Integration Points

### Hook: PostToolUse[Write]

When manifest written to forensics/{date}/manifests/:

1. Agent writes manifest (status: "draft" or "final")
2. PostToolUse hook triggers `sync-vaults-with-coc.py --manifest-changed {path}`
3. Script loads new manifest → detects associated vault file → injects metadata → COC entry
4. Returns: sync report appended to ephemeral/{task_id}/sync-report.json

### Hook: SessionStart

Before session begins:

1. Read config: `vault_sync_config.json` (defines vault paths, update frequency, metrics targets)
2. Run `sync-vaults-with-coc.py --full-scan` (catch up on prior 24h changes)
3. Pre-populate `.vault_sync_state.json` with baseline hashes
4. Return: sync report from prior session

### Mission Graph Routing

After COC entry written, mission field becomes discoverable:

```python
# In manifest → vault frontmatter:
{
  "mission": "vault-infrastructure-overhaul",
  "compass_bearing": "S",
  "task_id": "sync-vault-coc-design"
}

# Agents scanning `forensics/manifests/` can now group by mission:
manifests = load_manifests_by_mission("vault-infrastructure-overhaul")
# Returns all vault files + manifests sharing this mission
```

---

## Success Metrics

### Phase 1: Change Detection
- Scan duration < 2 seconds (for 1000+ vault files)
- False positive rate < 2% (files incorrectly marked changed)

### Phase 2: Hash Computation
- Hash computation < 10ms per file
- Hash collision rate = 0 (cryptographic guarantee)

### Phase 3: Metadata Injection
- All injected fields valid JSON
- Frontmatter passes schema validation (8x_vault_frontmatter_validator)
- Field coverage: ≥80% of manifests get mission + compass_bearing

### Phase 4: COC Logging
- All entries appended atomically
- Hash chain unbroken (prev_entry_hash links verified)
- COC immutability verified (post-sync hashes match COC records)

### Phase 5: Wikilink Validation
- Broken link detection rate = 100%
- False positive rate < 1%
- Validation time < 100ms per file

### Phase 6: Reporting
- Report generation < 500ms
- Report completeness: all metrics populated
- Error detection: catches missing manifests, broken links

---

## Error Handling

### Recoverable Errors

| Error | Detection | Recovery |
|-------|-----------|----------|
| Manifest not found | No task_id in metadata discovery | Proceed; skip injection; log warning |
| Broken wikilink | Link validation fails | Continue sync; record in report; no blocking |
| Hash mismatch | hash_after ≠ expected | Log warning; allow manual review |
| Frontmatter invalid | Schema validation fails | Reject injection; preserve original; log error |
| COC entry write fails | Append operation fails | Rollback partial entry; raise error (blocking) |

### Non-Recoverable Errors (Blocking)

- COC file corrupted or unreachable
- Vault file system read error
- Manifest JSON unparseable
- Faerie repo path misconfigured

### Rollback Strategy

```python
def sync_with_rollback(changes, coc_path, vault_files):
    """
    Sync with transaction semantics.
    If any critical operation fails, rollback all changes.
    """
    # Create snapshots before any writes
    snapshots = {
        "vault": snapshot_vault_files(vault_files),
        "coc": snapshot_coc(coc_path)
    }
    
    try:
        # Process all changes
        for change in changes:
            inject_metadata(change)
            write_coc_entry(change)
        
        return "success"
    except Exception as e:
        # Rollback
        restore_vault_files(snapshots["vault"])
        restore_coc(snapshots["coc"])
        raise e
```

---

## Implementation Phases

### Phase A: Core Script (sync-vaults-with-coc.py)
- Change detection
- Hash computation
- Manifest association
- Vault frontmatter injection
- COC entry writing
- Validation + reporting

### Phase B: Hook Integration
- PostToolUse[Write] hook for manifests
- SessionStart hook for full sync
- Mission graph router integration

### Phase C: Metrics + Analysis
- Mission choice analytics
- Sync performance dashboard
- COC health monitoring

### Phase D: Documentation
- User guide for vault sync
- COC entry schema reference
- Troubleshooting guide

---

## Files to Create

1. **sync-vaults-with-coc.py** — Main unified script
2. **FRONTMATTER-METADATA-INJECTION-RULES.json** — Canonical mapping schema
3. **COC-ENTRY-SCHEMA.json** — COC entry format specification
4. **vault-sync-config.json** — Configuration (vault paths, update frequency)
5. **vault-sync-user-guide.md** — User documentation

---

## References

- **Chain of Custody Standard:** forensics/master-coc.jsonl (format + hash chain)
- **Manifest Format:** forensics/manifests/{YYYY-MM-DD}/*_manifest_*.json
- **Vault Frontmatter Schema:** hooks/8x_vault_frontmatter_validator.py
- **Mission Graph Sync:** scripts/0x_mission_graph_sync.py (existing; will integrate with)

---

## Appendix: Design Decisions

### Q: Why Unified Script vs. Three Separate Tools?
**A:** Single entry point reduces coordination overhead, guarantees atomic operations (all-or-nothing), and enables cross-phase data passing (hash → metadata → COC in one transaction).

### Q: How to Handle Vault Path Canonicity?
**A:** sync-vaults-with-coc.py reads VAULT_TARGETS from config (environment var or settings.json). Agents target single canonical path; script respects config to handle existing path variants gracefully.

### Q: What if Manifest Not Found?
**A:** Script proceeds without metadata injection (graceful degradation). File gets synced with basic frontmatter (hash, timestamp). Warning logged in report. Enables catch-up when manifests are delayed.

### Q: Why Hash Both Before and After?
**A:** Before-hash proves file was in expected state at sync start (detects mid-operation corruption). After-hash proves sync didn't corrupt. Together: "state A → [sync operation] → state B" is cryptographically verified.

### Q: Should Wikilink Validation Block Sync?
**A:** No. Broken links are warnings, not errors. Some agents may reference future work (forward links). Validation is informational; preserves authorial intent.

---

**END OF DESIGN DOCUMENT**
