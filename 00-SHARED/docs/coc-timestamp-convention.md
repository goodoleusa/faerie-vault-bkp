# Universal COC Timestamp-First Convention

**Adopted:** 2026-04-22  
**Scope:** All forensic artifacts (droplets, manifests, COC logs, agent runs, vault artifacts)  
**Purpose:** Make filesystem chronologically sortable, match hash-chain order, enable timeline reconstruction

---

## The Pattern

```
{YYYY-MM-DDThh:mm:ssZ}_{product-type}_{disambiguators}_{session_id8}.{ext}
```

**Components:**
- `{YYYY-MM-DDThh:mm:ssZ}` — ISO 8601 UTC timestamp (always leading, always this format)
- `_{product-type}` — What is this artifact? (droplet, manifest, agent-run, coc, finding, narrative)
- `_{disambiguators}` — Context (task_id, agent_type, wave, etc.)
- `_{session_id8}` — First 8 chars of session ID (scope isolation)
- `.{ext}` — File extension (md, json, jsonl)

---

## Examples Across Products

### Droplets (Task-Centric, Agent-Signed)

```
forensics/droplets/2026-04-22/
  2026-04-22T04:15:00Z_droplet_40_data-scientist-ghi012_3b62c9df.md
  2026-04-22T04:22:00Z_droplet_41_code-reviewer-jkl345_3b62c9df.md
  2026-04-22T04:45:00Z_droplet_42_evidence-curator-mno678_3b62c9df.md

forensics/droplets/2026-04-21/
  2026-04-21T16:30:00Z_droplet_39_data-scientist-def789_3b62c9df.md
```

**Organized by:** Date folder (YYYY-MM-DD) for timeline organization  
**Sorted by:** ISO timestamp (filesystem natural sort = chronological order)  
**Naming:** `{timestamp}_droplet_{task_id}_{agent_type}-{agent_id}_{session_id8}`

---

### COC Audit Logs (Immutable, Hash-Chained)

```
forensics/
  2026-04-22T04:15:00Z_coc_droplet_task-40.jsonl
  2026-04-22T04:22:00Z_coc_droplet_task-41.jsonl

forensics/agent-runs/2026-04-22/
  2026-04-22T04:15:00Z_agent-run_data-scientist-40_3b62c9df.jsonl
  2026-04-22T04:22:00Z_agent-run_code-reviewer-41_3b62c9df.jsonl
```

**Append-only:** Each timestamp is a new entry (or new file for high-volume products)  
**Hash-chained:** `prev_entry_hash` → `entry_hash` → `next_entry_hash`  
**Sortable:** `ls forensics/ | sort` = event timeline

---

### Agent Runs (Session-Scoped Execution Logs)

```
forensics/agent-runs/2026-04-22/
  2026-04-22T04:15:00Z_agent-run_data-scientist-40_3b62c9df.jsonl
  2026-04-22T04:22:00Z_agent-run_code-reviewer-41_3b62c9df.jsonl
  2026-04-22T04:45:00Z_agent-run_evidence-curator-42_3b62c9df.jsonl
```

**Content:** Full agent execution log (startup, work, return, manifest)  
**Organized by:** Date folder (timeline)  
**Why:** Reconstruct agent sequence from a date ("what did agents do on 2026-04-22?")

---

### Manifests (Wave Output Artifacts)

```
~/.claude/hooks/state/2026-04-22/
  2026-04-22T04:15:00Z_manifest_wave2-data-scientist_3b62c9df.json
  2026-04-22T04:22:00Z_manifest_wave2-code-reviewer_3b62c9df.json
  2026-04-22T04:45:00Z_manifest_wave3-evidence-curator_3b62c9df.json
```

**Fields:** `output_path`, `dashboard_line`, `files_written`, `next`  
**Timestamp:** When agent returned (not when spawned)  
**Lookup:** `find . -name "*_manifest_*" -type f | sort` = execution timeline

---

### Vault Artifacts (Daily Output Findings)

```
00-SHARED/ONBOARDING/2026-04-22-phase-3-eval/
  2026-04-22T04:15:00Z_findings_evidence-gap_3b62c9df.md
  2026-04-22T04:22:00Z_narrative_summary_3b62c9df.md
  2026-04-22T04:45:00Z_analysis_tier1-smoking-guns_3b62c9df.md
```

**Frontmatter required:**
```yaml
type: finding | narrative | analysis
status: draft | complete
created: 2026-04-22T04:15:00Z
doc_hash: sha256:...
hash_ts: pending
```

**Sorting:** `ls 2026-04-22-phase-3-eval/ | sort` = creation timeline

---

## Why This Pattern?

### 1. Filesystem = Hash Chain

```
ls -la forensics/droplets/2026-04-22/
2026-04-22T04:15:00Z_droplet_40_...
2026-04-22T04:22:00Z_droplet_41_...
2026-04-22T04:45:00Z_droplet_42_...
```

File order = event order. No database needed, no manual sorting.

### 2. Temporal Sorting (Natural)

```bash
# All forensic events from today, in order
find forensics/ -name "2026-04-22T*" | sort
# Output: 04:15, 04:22, 04:45 (chronological)

# All events from a task (across any date)
find forensics/ -name "*droplet_40*" | sort
# Output: all task-40 events across dates (sortable by timestamp)
```

### 3. Date Folders Enable Timeline Queries

```bash
# "What happened on 2026-04-21?"
ls forensics/droplets/2026-04-21/
# Shows all droplets created that day, sortable by time

# Archive by date (compress old droplets)
tar czf archive-2026-04-01-to-2026-04-10.tar.gz forensics/droplets/2026-04-*/
```

### 4. COC Hash Chain + Filesystem Order

**Immutable log (forensics/droplet-coc-task-40.jsonl):**
```json
{"type": "droplet_created", "timestamp": "2026-04-22T04:15:00Z", "signature": "a1b2...", "payload_hash": "sha256:...", "prev_entry_hash": "..."}
{"type": "droplet_read", "timestamp": "2026-04-22T04:22:00Z", "signature": "x9y8...", "prev_entry_hash": "a1b2..."}
```

**Filename (forensics/droplets/2026-04-22/):**
```
2026-04-22T04:15:00Z_droplet_40_...    ← matches COC first timestamp
2026-04-22T04:22:00Z_coc_droplet_task-40.jsonl  ← matches COC second timestamp
```

Filesystem order = COC order (proof of non-repudiation).

---

## Implementation Checklist

- [x] Droplets: `{timestamp}_droplet_{task_id}_{agent_type}-{agent_id}_{session_id8}.md`
- [x] Droplets organized by date folder: `forensics/droplets/{YYYY-MM-DD}/`
- [x] Discovery searches date folders in reverse chronological order (recent first)
- [x] COC logs use timestamp prefix (append-only per task)
- [x] Agent runs logged: `{timestamp}_agent-run_{agent_type}-{task_id}_{session_id8}.jsonl`
- [ ] Manifests logged: `{timestamp}_manifest_wave{N}-{agent_type}_{session_id8}.json`
- [ ] Vault artifacts stamped: `{timestamp}_finding|narrative_..._{session_id8}.md`

---

## Migration Path (For Existing Droplets)

If you have pre-timestamp-first droplets (e.g., `droplet-40_data-scientist-a1818e09_2026-04-22_3b62c9df.md`):

```bash
# Rename to timestamp-first + organize by date
for file in forensics/droplets/droplet-*.md; do
  # Extract timestamp from COC or use file mtime
  timestamp=$(python3 -c "
    import json
    from pathlib import Path
    task_id = Path('$file').stem.split('_')[1]
    coc = Path('forensics/droplet-coc-task-$task_id.jsonl')
    if coc.exists():
      with open(coc) as f:
        first_event = json.loads(f.readline())
        print(first_event['timestamp'])
  ")
  # Rename with timestamp prefix + organize by date
  mkdir -p "forensics/droplets/${timestamp:0:10}"
  mv "$file" "forensics/droplets/${timestamp:0:10}/${timestamp}_droplet_..."
done
```

---

## Queries You Can Now Ask

```bash
# "Show me all droplets from 2026-04-22"
ls forensics/droplets/2026-04-22/ | sort

# "Find all droplets from Task #40 (any date)"
find forensics/droplets/ -name "*_droplet_40_*"

# "Show droplet discovery timeline for Task #40"
grep -l "discovering_task_id.*40" forensics/droplet-coc-*.jsonl | xargs cat | jq '.timestamp'

# "Verify hash chain integrity"
python3 << 'EOF'
import json
prev_hash = None
for line in open("forensics/droplet-coc-task-40.jsonl"):
    entry = json.loads(line)
    if entry.get("prev_entry_hash") != prev_hash:
        print(f"BROKEN CHAIN at {entry['timestamp']}")
    prev_hash = entry.get("payload_hash")
print("✓ Chain verified")
EOF

# "Archive droplets older than 7 days"
find forensics/droplets/ -maxdepth 1 -type d -name "2026-04-*" \
  -not -newer <(date -d "7 days ago" +%Y-%m-%d) \
  -exec tar czf archive-{}.tar.gz {} \;
```

---

## Related

- **Droplet architecture:** `docs/task-droplet-architecture.md`
- **SDK guide:** `00-SHARED/ONBOARDING/droplet-sdk-guide.md`
- **Implementation:** `scripts/9x_task_droplet_writer.py`, `scripts/9x_task_droplet_discovery_bootstrap.py`
- **Forensics overview:** `forensics/droplets/README.md`

---

**Status:** Convention established, droplet implementation complete, ready for adoption across all COC'd products.
