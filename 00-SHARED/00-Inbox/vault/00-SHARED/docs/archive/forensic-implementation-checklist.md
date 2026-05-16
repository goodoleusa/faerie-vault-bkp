# Forensic System Implementation Checklist

**Target:** Phase 1 completion by 2026-04-21

---

## Pre-Implementation Review

- [ ] Read full design doc: `/mnt/d/0LOCAL/.claude/hooks/state/forensic-system-design.md`
- [ ] Review existing COC rules: `~/.claude/rules/evidence-coc.md`
- [ ] Review memory routing: `~/.claude/rules/memory-routing.md`
- [ ] Confirm archive root location: `~/.claude/forensic-archive/`

---

## Phase 1: Core Infrastructure (2026-04-07 to 2026-04-21)

### Step 1: Create Directory Structure

```bash
mkdir -p ~/.claude/forensic-archive/{artifacts,agent-state,working-memory,transcripts,verification}
mkdir -p ~/.claude/forensic-archive/agent-state/{task-states,checkpoints,rosters}
mkdir -p ~/.claude/forensic-archive/working-memory/{scratch,pollen,reasoning-trails,mem-blocks}
mkdir -p ~/.claude/forensic-archive/transcripts/{conversations,tool-calls,execution-traces}
mkdir -p ~/.claude/forensic-archive/verification/{hash-proofs,pgp-signatures,audit-queries,court-exports}
```

Checkpoint: [ ] All directories created

### Step 2: Initialize Core Python Module

**File:** `~/.claude/scripts/forensic_archive.py`

- [ ] Create `ForensicArchive` class (copy from design doc)
- [ ] Implement `_load_manifest()` (read all entries, build indices)
- [ ] Implement all discovery queries (get_artifacts, get_changed_since, etc.)
- [ ] Implement verification queries (verify_coc_chain)
- [ ] Add CLI entry point: `python ~/.claude/scripts/forensic_archive.py --help`
- [ ] Test on empty manifest (graceful handling)

Checkpoint: [ ] Module loads, basic queries work

### Step 3: Create manifest.jsonl Foundation

**File:** `~/.claude/forensic-archive/manifest.jsonl`

- [ ] Initialize empty file (will be append-only forever)
- [ ] Add genesis event:
  ```json
  {
    "event_id": "evt-genesis-20260407",
    "ts": "2026-04-07T00:00:00Z",
    "layer": "system",
    "operation": "archive_initialized",
    "metadata": {
      "version": "1.0-alpha",
      "root": "~/.claude/forensic-archive/",
      "description": "Unified forensic knowledge graph of Claude ecosystem"
    },
    "prev_event_id": null,
    "event_hash": "sha256:genesis_000000000000000000000000000000000000000000000000000000000000",
    "signature": ""
  }
  ```

Checkpoint: [ ] manifest.jsonl created with genesis entry

### Step 4: Implement Session Hooks

**Hook 1: Session Open** (`~/.claude/hooks/pre_run.py`)

When faerie or `/faerie` starts, log session_open event:

```python
def log_session_open(session_id: str):
    archive = ForensicArchive(Path("~/.claude/forensic-archive"))
    event = {
        "event_id": f"evt-{session_id}-transcripts-open",
        "ts": datetime.utcnow().isoformat(),
        "layer": "transcripts",
        "operation": "session_open",
        "session_id": session_id,
        "prev_event_id": archive.entries[-1]["event_id"],
        "event_hash": ""  # Will compute after
    }
    archive.append_event(event)
```

- [ ] Add to session startup hook
- [ ] Test: verify entry appears in manifest.jsonl

**Hook 2: Session Close** (session_stop_hook)

When session ends, log session_close event:

```python
def log_session_close(session_id: str, summary: Dict):
    archive = ForensicArchive(...)
    event = {
        "event_id": f"evt-{session_id}-transcripts-close",
        "ts": datetime.utcnow().isoformat(),
        "layer": "transcripts",
        "operation": "session_close",
        "transcript": {
            "session_id": session_id,
            "session_summary": summary
        },
        "prev_event_id": archive.entries[-1]["event_id"]
    }
    archive.append_event(event)
```

- [ ] Add to session_stop_hook
- [ ] Test: verify entry created at session end

Checkpoint: [ ] Sessions begin and end with manifest entries

### Step 5: Agent Learning Event Hook

**Integration:** When agent beats baseline (in agent.md update flow)

```python
def record_otj_learning(agent_type: str, kpi_before: float, kpi_after: float, 
                        session_id: str, task_id: str):
    archive = ForensicArchive(...)
    
    # Agent state event (learning)
    learning_event = {
        "event_id": generate_event_id(f"agent-{agent_type}-learning"),
        "ts": datetime.utcnow().isoformat(),
        "layer": "agent_state",
        "operation": "learning_event",
        "agent_state": {
            "agent_type": agent_type,
            "learning_event": {
                "type": "otj_improvement",
                "kpi": "primary_kpi",
                "score_before": kpi_before,
                "score_after": kpi_after,
                "delta": kpi_after - kpi_before,
                "context_task": task_id
            }
        },
        "session_id": session_id,
        "prev_event_id": archive.entries[-1]["event_id"]
    }
    
    archive.append_event(learning_event)
    
    # Artifact event (agent card update)
    agent_card_path = Path(f"~/.claude/agents/{agent_type}.md")
    artifact_event = {
        "event_id": generate_event_id(f"artifact-{agent_type}-update"),
        "ts": datetime.utcnow().isoformat(),
        "layer": "artifacts",
        "operation": "update",
        "artifact": {
            "name": agent_card_path.name,
            "category": "agents",
            "content_hash_after": hash_file(agent_card_path),
            "path": str(agent_card_path),
            "version": f"{datetime.utcnow().date()}_{kpi_after}"
        },
        "source": f"agent_{agent_type}",
        "source_event_id": learning_event["event_id"],
        "session_id": session_id,
        "prev_event_id": learning_event["event_id"]
    }
    
    archive.append_event(artifact_event)
```

- [ ] Add to agent.md update flow (currently inline in workflow)
- [ ] Test: beat baseline, verify two entries (learning + artifact) created

Checkpoint: [ ] Learning events logged with causal links

### Step 6: Memory Promotion Hook

**Integration:** memory-keeper promotes pollen → NECTAR

```python
def log_memory_promotion(mem_block_id: str, content: str, category: str, 
                        confidence: float, session_id: str):
    archive = ForensicArchive(...)
    
    event = {
        "event_id": generate_event_id(f"memory-{mem_block_id}-promoted"),
        "ts": datetime.utcnow().isoformat(),
        "layer": "working_memory",
        "operation": "promoted",
        "memory": {
            "block_id": mem_block_id,
            "category": category,
            "confidence": confidence,
            "promoted_to": "~/.claude/memory/NECTAR.md",
            "promoted_ts": datetime.utcnow().isoformat()
        },
        "source": "memory_keeper",
        "session_id": session_id,
        "prev_event_id": archive.entries[-1]["event_id"]
    }
    
    archive.append_event(event)
```

- [ ] Add to memory-keeper phase (Phase 9 of faerie)
- [ ] Test: promotion, verify entry created

Checkpoint: [ ] Memory promotions tracked

### Step 7: Manual Testing Session

Run a single complete session (faerie → work → handoff) and verify:

- [ ] Session open event created
- [ ] At least 20 working events logged (tasks, states, memory operations)
- [ ] Session close event created with summary
- [ ] manifest.jsonl is valid JSONL (one entry per line)
- [ ] No entries are duplicated
- [ ] All entries have required fields (event_id, ts, layer, operation, prev_event_id)

Checkpoint: [ ] One full session logged successfully

### Step 8: Documentation + README

**File:** `~/.claude/forensic-archive/README.md`

- [ ] Overview: what this archive contains
- [ ] File structure: each directory's purpose
- [ ] How to query: basic `ForensicArchive` usage
- [ ] How to verify: `verify_coc_chain()` example
- [ ] Retention policy: how long entries are kept
- [ ] Emergency access: how to handle archive corruption

Checkpoint: [ ] README complete

---

## Phase 1 Completion Criteria

- [ ] Directory structure created
- [ ] ForensicArchive Python module functional
- [ ] manifest.jsonl created and actively logging
- [ ] Session hooks integrated (open/close)
- [ ] Agent learning events logged
- [ ] Memory promotions logged
- [ ] One complete manual test session
- [ ] README documentation
- [ ] **Minimum 50+ entries in manifest.jsonl from real usage**

---

## Phase 2: Signing + Verification (Post-Phase 1)

Items to tackle 2026-04-21+:

- [ ] Add PGP signing to critical events (learning_event, promoted, findings)
- [ ] Implement `verify_coc_chain()` hash verification
- [ ] Create `export_for_court()` bundler
- [ ] Test: court-ready export for one session
- [ ] Write expert witness affidavit template

---

## Common Gotchas

### manifest.jsonl Must Be Append-Only

- [ ] Use `with open(path, "a")` NEVER `"w"`
- [ ] Each entry is one complete JSON line
- [ ] No trailing commas
- [ ] One entry per line (JSONL format)

### Event IDs Must Be Unique

- [ ] Use: `f"evt-{datetime.now().isoformat()}-{uuid.uuid4().hex[:8]}"`
- [ ] Or: `f"evt-{session_id}-{layer}-{counter}"`
- [ ] Check: no duplicates in manifest

### Hash Chain Requires Strict Ordering

- [ ] Each entry's `prev_event_id` points to previous entry's `event_id`
- [ ] No out-of-order appends
- [ ] Verify: last 10 entries have correct chain

### Session IDs Must Be Consistent

- [ ] Session ID created at `/faerie` start
- [ ] Same ID used for all events in that session
- [ ] Check: all events with same session_id have timestamps in order

---

## Quick Start for Phase 1

```bash
# Create archive structure
mkdir -p ~/.claude/forensic-archive/{artifacts,agent-state,working-memory,transcripts,verification}

# Initialize manifest with genesis event
python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime

manifest = Path.home() / ".claude" / "forensic-archive" / "manifest.jsonl"
genesis = {
    "event_id": "evt-genesis-20260407",
    "ts": datetime.utcnow().isoformat() + "Z",
    "layer": "system",
    "operation": "archive_initialized",
    "metadata": {"version": "1.0-alpha"},
    "prev_event_id": None,
    "event_hash": "sha256:genesis"
}
manifest.write_text(json.dumps(genesis) + "\n")
print("✓ Genesis event created")
EOF

# Verify
python3 ~/.claude/scripts/forensic_archive.py --list --limit 1
```

---

## Sign-Off

When Phase 1 is complete, verify:

- Human reviews manifest.jsonl structure (sample entries)
- Human reviews ForensicArchive API (makes sense? sufficient?)
- Human tests: can restore session from manifest + transcripts
- Human approves integration hooks (no breaking changes?)

Then proceed to Phase 2.

---

**Document created:** 2026-04-07  
**Phase 1 target:** 2026-04-21  
**Next review:** After first 50+ entries logged
