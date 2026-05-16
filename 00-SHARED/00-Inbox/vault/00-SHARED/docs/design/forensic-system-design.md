---
type: design
status: active
created: 2026-04-21
tags: [forensics, design, coc]
up: README.md
next: FORENSIC-SYSTEM-INDEX.md
---

> [↑ Readme](README.md) · [→ Forensic System Index](FORENSIC-SYSTEM-INDEX.md) · [⌂ Home](../../README.md)

# Unified Forensic System — Complete Knowledge Graph

**Version:** 1.0-alpha  
**Status:** Architecture + Schema (Phase 1-2 planning)  
**Date:** 2026-04-07  
**Scope:** Complete forensic capture of all four layers of Claude ecosystem  

---

## Executive Summary

The current system has scattered forensic controls:
- Evidence COC (append-only, versioned hash manifests)
- Memory routing (four separate stores: HONEY, NECTAR, REVIEW-INBOX, scratch)
- Agent state (task-states JSON files, scattered across hooks/state/)
- Transcripts (nowhere — lost after auto-compact)

This design unifies all four into a single forensic knowledge graph with hash-chained COC entries, progressive disclosure capability, and court-admissible audit trails.

**Core principle:** Every significant event in the system gets one immutable hash-chained entry. Chain integrity is verifiable. History is queryable. The system can prove what happened, when, and by whom.

---

## Why Unified Forensic System

### Problem Statement

1. **Fragmented accountability:** Agent improvements are recorded in agent.md, but the session context that enabled the improvement is in scratch-*.md, which is gitignored. The causal link is invisible.

2. **Memory promotion unaudited:** When memory-keeper promotes pollen → NECTAR, what exactly was promoted? What was filtered out? No record.

3. **Transcript loss:** After auto-compact, the full conversation is summarized and discarded. Critical reasoning chains vanish. Investigators can't verify "how did we reach this conclusion?"

4. **State transitions hidden:** Task states exist in isolation. We don't see: "state V1 formed with assumptions {A,B,C} → new evidence → state V2 updated assumptions to {A',B',C'} → 3 hours later agent beat its baseline." These forensic proof points are scattered.

5. **COC doesn't speak:** Evidence manifests exist (hash_manifest_RUN004.json) but contain no narrative. Court needs to understand: "Why were these 5,000 files ingested? What changed in RUN005? Where are the justifications?"

6. **Cross-layer traceability missing:** I cannot easily ask: "Show me every change to agent card X, the sessions that triggered updates, the evidence that drove the updates, and the resulting impact." The system has the data but no query interface.

### Solution Architecture

Single append-only JSONL master log (manifest.jsonl) records:
- Every artifact create/update (rules, skills, agent cards, memories)
- Every agent state transition (task checkpoint, capability improvement, OTJ learning event)
- Every memory operation (scratch created, promoted, validated, archived)
- Every transcript boundary (session open, close, compaction)

Each entry:
- Contains hash of affected content (BEFORE and AFTER)
- Links to previous entry via prev_event_id (hash chain)
- Records metadata (who triggered it, which agents affected, impact on other entries)
- Includes hash of the entry itself (verifiable chain)
- Optionally PGP-signed for court admissibility

Together, these entries form a **complete temporal graph** of the Claude system's evolution. You can:
- Trace artifact lineage (when did this rule change, by whom, why)
- Prove agent learning causation (observation at T1 → capability improvement at T2 > T1 → finding at T3 > T2)
- Verify memory integrity (which memory blocks were promoted, when, with what confidence)
- Reconstruct any session (read transcript + session manifest + agent state deltas)

---

## Four-Layer Architecture

```
UNIFIED FORENSIC ARCHIVE
├── manifest.jsonl                  (1,000s of entries, hash-chained)
├── coc.jsonl                       (optional: digest/summary for quick scanning)
├── artifacts/                      (immutable storage — hash-keyed)
│   ├── agent-cards/
│   ├── skills/
│   ├── rules/
│   ├── memories/
│   └── system-config/
├── agent-state/                    (versioned, session-scoped)
│   ├── task-states/
│   ├── checkpoints/
│   ├── rosters/
│   └── learning-events/
├── working-memory/                 (ephemeral, progressive lifecycle)
│   ├── scratch/                    (sessions)
│   ├── pollen/                     (agents → promoted)
│   ├── reasoning-trails/
│   └── mem-blocks/                 (categorized, timestamped)
├── transcripts/                    (immutable record)
│   ├── conversations/              (session-keyed)
│   ├── tool-calls/
│   └── execution-traces/
└── verification/
    ├── hash-proofs/
    ├── pgp-signatures/
    ├── audit-queries/
    └── court-exports/
```

---

## Layer 1: Artifacts (Durable, Permanent)

**What:** Agent cards, skills, rules, memories, system config.  
**Lifecycle:** Created once, updated rarely, queryable forever.  
**Storage:** Deduplicated by content hash (same artifact in multiple locations = single canonical copy).  

### Artifact Entry Schema

```json
{
  "event_id": "evt-20260407-a3d8f2c1-artifacts-001",
  "ts": "2026-04-07T14:22:15Z",
  "layer": "artifacts",
  "operation": "create|update|deprecate",
  "artifact_type": "agent_card|skill|rule|memory|hook_script|config",
  
  "artifact": {
    "name": "research-analyst.md",
    "category": "agents",
    "content_hash_before": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
    "content_hash_after": "sha256:f3c2a9e8d1b7c4a6f0e9d2c5b8a1f4e7c3d6a9f2e5b8c1d4a7f0e3c6b9a2",
    "size_bytes_before": 0,
    "size_bytes_after": 1247,
    "lines_before": 0,
    "lines_after": 47,
    "path": "~/.claude/agents/research-analyst.md",
    "version": "2026-04-07_0.91"
  },
  
  "source": "agent_research-analyst",
  "session_id": "session-20260407-main-001",
  "source_event_id": "evt-20260407-a3d8f2c1-agent-state-024",
  
  "metadata": {
    "section_changed": "## Last Training",
    "entry_ids_modified": ["technique_001", "failure_mode_012"],
    "kpi_improved_from": 0.88,
    "kpi_improved_to": 0.91,
    "trigger": "otj_learning_event",
    "agents_affected": ["research-analyst"],
    "related_artifacts": ["scripts/research-analyst-workflow.py"],
    "human_readable_change": "OTJ learning: cross-project detection technique (+0.03 score improvement)"
  },
  
  "validation": {
    "yaml_valid": true,
    "md_format_valid": true,
    "size_within_budget": true,
    "no_entity_names": true,
    "no_case_data": true
  },
  
  "prev_event_id": "evt-20260407-a3d8f2c1-memory-012",
  "event_hash": "sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1",
  "sig_type": "none|hmac|pgp",
  "signature": ""
}
```

### Entry Fields Explained

| Field | Type | Purpose |
|-------|------|---------|
| `event_id` | uuid | Globally unique, immutable, sortable by timestamp prefix |
| `ts` | ISO8601 | Precise ordering for causality analysis |
| `layer` | enum | Filters to artifact layer only |
| `operation` | enum | create / update / deprecate (never delete from immutable log) |
| `artifact.content_hash_before` | sha256 | Before state (all zeros for create) |
| `artifact.content_hash_after` | sha256 | After state (proves immutability via chain) |
| `source` | string | Who triggered the change (agent type, script name, hook name, "human") |
| `source_event_id` | uuid | Causal link to the event that triggered this write (e.g., OTJ learning event → artifact write) |
| `metadata.trigger` | string | Why the artifact changed (otj_learning_event, periodic_crystallize, manual_edit, auto_bump) |
| `metadata.entry_ids_modified` | array | Which specific entries in HONEY/NECTAR/agent card were touched (granular accountability) |
| `prev_event_id` | uuid | Pointer to previous manifest entry (forms hash chain) |
| `event_hash` | sha256 | Hash of this entry's canonical form (proves tampering attempts) |
| `signature` | string | Optional PGP signature for court admissibility |

---

## Layer 2: Agent State (Intermediate, Session-Scoped)

**What:** Task states, checkpoints, manifests, roster entries, capability improvements.  
**Lifecycle:** Created per-run, updated as agent progresses, may be superseded by next run.  
**Forensic value:** Proves OTJ learning didn't retroactively bias earlier findings.  

### Agent State Entry Schema

```json
{
  "event_id": "evt-20260407-a3d8f2c1-agent-state-024",
  "ts": "2026-04-07T13:45:30Z",
  "layer": "agent_state",
  "operation": "state_transition|checkpoint|learning_event|capability_bump",
  
  "agent_state": {
    "agent_type": "evidence-curator",
    "agent_version": "2026-03-19_0.88",
    "task_id": "task-20260407-evidence-bundle-001",
    
    "state_transition": {
      "from_version": 1,
      "to_version": 2,
      "ts_from": "2026-04-07T13:15:00Z",
      "ts_to": "2026-04-07T13:45:30Z",
      "duration_seconds": 1830,
      
      "state_v1": {
        "data_seen": "partial (summary only)",
        "assumptions": {
          "H1_confidence": 0.70,
          "H2_confidence": 0.30
        },
        "findings": ["finding_A", "finding_B"],
        "open_questions": ["Q1: connection to H2?", "Q2: strength of evidence?"]
      },
      
      "state_v2": {
        "data_seen": "full dataset (364 items)",
        "assumptions": {
          "H1_confidence": 0.95,
          "H2_confidence": 0.78
        },
        "findings": ["finding_A (confirmed)", "finding_B (refined)", "finding_C (new)"],
        "open_questions": ["Q1 resolved: clear H1 pattern", "Q2: data quality of source D"]
      },
      
      "delta_explanation": {
        "trigger": "full dataset became available",
        "assumptions_changed": [
          {
            "assumption": "H1_confidence",
            "old_value": 0.70,
            "new_value": 0.95,
            "evidence_that_changed_it": ["cert_fingerprint_collision", "github_ID_verification", "NLRB_corroboration"],
            "confidence": 0.95
          }
        ],
        "findings_added": ["finding_C: cross-project connection detected (Bayesian confidence 0.85)"],
        "findings_removed": [],
        "reasoning_changed": "Initial assessment underweighted evidence strength; full corpus clarifies pattern"
      }
    },
    
    "checkpoint": {
      "manifest_path": "scripts/audit_results/evidence_RUN009_curated.json",
      "manifest_hash": "sha256:e1d2c3b4a5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1",
      "items_curated": 364,
      "tiers_assigned": [
        {"tier": 1, "count": 247},
        {"tier": 2, "count": 89},
        {"tier": 3, "count": 28}
      ],
      "high_confidence_findings": 3
    },
    
    "learning_event": {
      "type": "otj_improvement",
      "kpi": "tier1_accuracy",
      "score_before": 0.88,
      "score_after": 0.91,
      "delta": 0.03,
      "technique_discovered": "Cross-project detection — recognizing when two separate data streams converge on same entity",
      "context_task": "Curation of H1 evidence (DOGE credential misuse)",
      "generalizability": "High — applicable to any multi-stream investigation",
      "added_to_agent_card": true
    }
  },
  
  "source": "agent_evidence-curator",
  "session_id": "session-20260407-main-001",
  "manifest_event_id": "evt-20260407-a3d8f2c1-artifacts-001",
  
  "metadata": {
    "agents_involved": ["evidence-curator"],
    "downstream_events": [
      "evt-20260407-a3d8f2c1-artifacts-001 (agent card update)",
      "evt-20260407-a3d8f2c1-working-memory-015 (MEM block promotion)"
    ],
    "impact_classification": "kpi_improvement (score +0.03)",
    "forensic_significance": "Proves learning occurred AFTER state V1, BEFORE state V2. State V1 findings cannot be biased by post-hoc learning."
  },
  
  "prev_event_id": "evt-20260407-a3d8f2c1-agent-state-023",
  "event_hash": "sha256:b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
  "signature": ""
}
```

### Key Forensic Features

**Progressive Disclosure (state versioning):**
- Agent forms V1 assumptions with partial data
- New data arrives → agent updates to V2
- Learning event occurs at T2 > V1 timestamp
- Therefore: V1 findings cannot be biased by learning at T2

**Causality Proof:**
- `state_v1.ts` = 13:15:00 (when agent had partial data)
- `learning_event.ts` = 13:45:30 (when improvement happened)
- `source_event_id` in artifact layer links learning → artifact update
- Court can verify: "Finding was made at 13:15, improvement happened at 13:45, no retroactive bias possible"

---

## Layer 3: Working Memory (Ephemeral, Progressive Lifecycle)

**What:** Scratch blocks, pollen notes, reasoning trails, MEM entries.  
**Lifecycle:** Draft → Validated → Promoted to durable → Archived.  
**Forensic value:** Captures the messy thinking process; shows what agents considered and rejected.  

### Memory Entry Schema

```json
{
  "event_id": "evt-20260407-a3d8f2c1-working-memory-015",
  "ts": "2026-04-07T13:42:15Z",
  "layer": "working_memory",
  "operation": "created|updated|promoted|archived",
  
  "memory": {
    "session_id": "session-20260407-main-001",
    "source_agent": "evidence-curator",
    "block_id": "mem-20260407-01547",
    "category": "CONNECTION",
    "priority": "HIGH",
    "version": "1",
    
    "content": "Cross-project detection: BGP AS400495 observed in CyberTemplate investigation (Treasury/DOGE) AND independently reported in FaerieInvestigation (NATO cybersecurity). Two separate data collection streams, same infrastructure node. Bayesian confidence: 0.85 (need: collateral network pattern, third independent source).",
    "tags": ["cross_project", "infrastructure_node", "AS400495", "bgp_pattern"],
    "confidence_statement": "Bayesian prior P(random collision | same AS) = 0.02. Observed collocation = 3 independent streams. Posterior: 0.85",
    
    "lifecycle": {
      "created_ts": "2026-04-07T13:42:15Z",
      "created_by": "evidence-curator",
      "validation_status": "unvalidated",
      "promoted_ts": null,
      "promoted_by": null,
      "archive_ts": null,
      "archive_reason": null
    },
    
    "evidence_cited": [
      {
        "source": "scripts/audit_results/unified_evidence_H2.json",
        "hash": "sha256:c1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6c7d8e9f0",
        "extract": "AS400495 observed in 18 .gov domain MX records, Montreal node TX anomaly (Z=9.89, p=2.3e-23)"
      },
      {
        "source": "faerie2:.claude/memory/NECTAR.md",
        "hash": "sha256:d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6c7d8e9f0g1",
        "extract": "NATO investigation (2026-03-15): AS400495 re-routed Russian-origin BGP prefixes to Frankfurt. Same infrastructure pattern."
      }
    ],
    
    "minimum_additional_evidence_needed": [
      "Collateral network (ASNs adjacent to AS400495 connecting to federal systems)",
      "Third independent observation (outside these two investigations)",
      "Temporal correlation (same time window in both investigations)"
    ]
  },
  
  "source": "agent_evidence-curator",
  "session_id": "session-20260407-main-001",
  "parent_event": "evt-20260407-a3d8f2c1-agent-state-024",
  
  "metadata": {
    "memory_size_bytes": 2847,
    "can_promote": false,
    "promotion_blockers": ["minimum_evidence_threshold_not_met (need 2, have 2 from same session)"],
    "human_action_required": true,
    "high_flags_count": 1,
    "cross_project_connections": 1,
    "downstream_inbox_entry": "20260407_as400495_cross-project.md"
  },
  
  "prev_event_id": "evt-20260407-a3d8f2c1-working-memory-014",
  "event_hash": "sha256:c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
  "signature": ""
}
```

### Memory Lifecycle States

```
CREATED (draft)
  ↓ [content written, category assigned, evidence cited]
UNVALIDATED
  ↓ [agent considers the claim vs. evidence: is confidence justified?]
VALIDATED (ready to promote, but may need human approval)
  ↓ [memory-keeper or human reviews for promotion eligibility]
PROMOTED (moved to NECTAR.md)
  ↓ [at next faerie crystallize, may distill to HONEY.md]
ARCHIVED (moved to forensic storage, still queryable forever)
```

**Forensic Importance:** Shows what agents considered, with full confidence justifications. Court can see: "Agent found this CONNECTION with Bayesian 0.85, but flagged that it needs additional evidence. The agent was appropriately cautious, not cherry-picking."

---

## Layer 4: Transcripts (Immutable Audit Trail)

**What:** Conversation history, tool call logs, execution traces.  
**Lifecycle:** Never modified, complete record of what happened.  
**Forensic value:** Proof of reasoning chain, prevents post-hoc narrative.  

### Transcript Entry Schema

```json
{
  "event_id": "evt-20260407-a3d8f2c1-transcripts-042",
  "ts": "2026-04-07T14:30:15Z",
  "layer": "transcripts",
  "operation": "session_open|tool_call|response|session_close",
  
  "transcript": {
    "session_id": "session-20260407-main-001",
    "session_open_ts": "2026-04-07T13:00:00Z",
    "conversation_turn": 23,
    "turn_role": "assistant",
    
    "tool_call": {
      "tool": "Read",
      "path": "scripts/audit_results/unified_evidence_H1.json",
      "result_hash": "sha256:e1d2c3b4a5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1",
      "result_size_bytes": 45821,
      "elapsed_ms": 187
    },
    
    "response_summary": {
      "type": "finding_stated_with_confidence",
      "finding": "H1 confidence increases from 0.70 to 0.95 based on full dataset review",
      "confidence_expressed": 0.95,
      "evidence_cited": 3,
      "sources": ["cert_timestamp_collision", "github_verification", "nlrb_corroboration"],
      "caveats_stated": 1,
      "caveat": "Temporal test vs Treasury breach not significant (p=0.294), disclosed in report"
    },
    
    "context_used": {
      "loaded_files": [
        "~/.claude/memory/HONEY.md (3.2K tokens)",
        "~/.claude/memory/NECTAR.md tail-30 (12.1K tokens)"
      ],
      "context_total_tokens": 67000,
      "cache_hit": true,
      "cache_saved_tokens": 45000
    }
  },
  
  "source": "claude_main",
  "session_id": "session-20260407-main-001",
  "agent_manifest_event": "evt-20260407-a3d8f2c1-agent-state-024",
  
  "metadata": {
    "finding_stated": true,
    "confidence_level": 0.95,
    "evidence_count": 3,
    "minimum_required": 2,
    "requirement_met": true,
    "transcript_size_bytes": 8472,
    "reasoning_chain_preserved": true,
    "reproducible": true
  },
  
  "prev_event_id": "evt-20260407-a3d8f2c1-transcripts-041",
  "event_hash": "sha256:d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3",
  "signature": ""
}
```

**Session Close (end-of-session summary):**

```json
{
  "event_id": "evt-20260407-a3d8f2c1-transcripts-098",
  "ts": "2026-04-07T14:45:00Z",
  "layer": "transcripts",
  "operation": "session_close",
  
  "transcript": {
    "session_id": "session-20260407-main-001",
    "session_open_ts": "2026-04-07T13:00:00Z",
    "session_close_ts": "2026-04-07T14:45:00Z",
    "duration_seconds": 6300,
    "total_turns": 47,
    "total_tool_calls": 34,
    
    "session_summary": {
      "work_done": [
        "Evidence curation: 364 items tiered",
        "OTJ learning: cross-project detection technique (+0.03 KPI)",
        "Memory promoted: 8 MEM blocks to NECTAR",
        "Agent card updated: research-analyst (Last Training bumped)"
      ],
      "findings_stated": 3,
      "findings_confidence_levels": [0.95, 0.78, 0.78],
      "caveats_stated": 2,
      "evidence_citations": 23,
      "high_flags_raised": 1
    },
    
    "integrity_hash": "sha256:e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4",
    "transcript_full_path": "/mnt/d/0LOCAL/.claude/hooks/state/transcripts/session-20260407-main-001.md",
    "transcript_hash": "sha256:f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5"
  },
  
  "metadata": {
    "agents_spawned": ["evidence-curator"],
    "memory_promoted": 8,
    "artifacts_updated": 1,
    "state_transitions": 4,
    "learning_events": 1
  },
  
  "prev_event_id": "evt-20260407-a3d8f2c1-transcripts-097",
  "event_hash": "sha256:f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3g4h5",
  "signature": ""
}
```

---

## Unified Manifest Structure (manifest.jsonl)

**One append-only JSONL file:** `~/.claude/forensic-archive/manifest.jsonl`

Each line is a complete, valid JSON object representing one forensic event.

### File Format Rules

```
1. APPEND ONLY — never overwrite, never modify past entries
2. One JSON object per line — no multiline objects, no trailing commas
3. Sorted by timestamp within events (preserved insertion order)
4. Entry count: expect 1,000s per year (avg ~2-3 per session, 50+ sessions/month)
5. File size: ~500MB-1GB per year (manageable for git, but consider separate archive)
```

### Sample Session Events (chronological order)

```jsonl
{"event_id": "evt-20260407-session-001-open", "ts": "2026-04-07T13:00:00Z", "layer": "transcripts", "operation": "session_open", "session_id": "session-20260407-main-001", "prev_event_id": "evt-20260406-session-099-close", ...}
{"event_id": "evt-20260407-task-001-start", "ts": "2026-04-07T13:15:00Z", "layer": "agent_state", "operation": "checkpoint", "agent_type": "evidence-curator", "task_id": "task-001-curation", ...}
{"event_id": "evt-20260407-memory-001-created", "ts": "2026-04-07T13:42:15Z", "layer": "working_memory", "operation": "created", "category": "CONNECTION", ...}
{"event_id": "evt-20260407-state-001-transition", "ts": "2026-04-07T13:45:30Z", "layer": "agent_state", "operation": "state_transition", "from_v": 1, "to_v": 2, ...}
{"event_id": "evt-20260407-artifact-001-update", "ts": "2026-04-07T14:22:15Z", "layer": "artifacts", "operation": "update", "artifact_type": "agent_card", ...}
{"event_id": "evt-20260407-transcript-001-turn23", "ts": "2026-04-07T14:30:15Z", "layer": "transcripts", "operation": "tool_call", "turn": 23, ...}
{"event_id": "evt-20260407-memory-001-promoted", "ts": "2026-04-07T14:40:00Z", "layer": "working_memory", "operation": "promoted", ...}
{"event_id": "evt-20260407-session-001-close", "ts": "2026-04-07T14:45:00Z", "layer": "transcripts", "operation": "session_close", ...}
```

---

## COC Hash Chain

**Core principle:** Every entry contains the hash of the previous entry. If anyone modifies an entry, the chain breaks.

```
Entry N-1:
  event_hash = SHA256(prev_event_id + operation + content_key_fields)

Entry N:
  prev_event_id = Event(N-1).event_id
  event_hash = SHA256(prev_event_id + operation + content_key_fields)
  → linking N-1.event_hash is not directly used, but prev_event_id creates causal link

VERIFICATION:
  1. Compute SHA256(Entry N's canonical fields)
  2. Compare to Entry N.event_hash
  3. If match: Entry N is authentic
  4. Compute Entry(N+1).event_hash using Entry(N).event_id in the causal chain
  5. If all entries verify: entire chain is intact
```

**Canonical field order (for hash computation):**

```python
canonical_fields = {
  "event_id": entry.event_id,
  "ts": entry.ts,
  "layer": entry.layer,
  "operation": entry.operation,
  "prev_event_id": entry.prev_event_id,
  
  # Layer-specific content hash (MOST IMPORTANT)
  "content_hash_after": entry[layer].content_hash_after,
  
  # Impact metadata
  "metadata.trigger": entry.metadata.trigger,
  "metadata.agents_affected": sorted(entry.metadata.agents_affected)
}

event_hash = SHA256(json.dumps(canonical_fields, sort_keys=True))
```

---

## Verification API (Python)

```python
#!/usr/bin/env python3
"""Forensic archive verification and query interface."""

from pathlib import Path
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class ForensicArchive:
    """Complete knowledge graph of Claude ecosystem."""
    
    def __init__(self, archive_root: Path):
        self.root = archive_root
        self.manifest_path = archive_root / "manifest.jsonl"
        self._load_manifest()
    
    def _load_manifest(self):
        """Load all entries, build index."""
        self.entries = []
        self.index_by_id = {}
        self.index_by_session = {}
        self.index_by_artifact = {}
        
        with open(self.manifest_path) as f:
            for line in f:
                entry = json.loads(line.strip())
                self.entries.append(entry)
                self.index_by_id[entry["event_id"]] = entry
                
                # Session index
                sid = entry.get("session_id")
                if sid:
                    if sid not in self.index_by_session:
                        self.index_by_session[sid] = []
                    self.index_by_session[sid].append(entry)
                
                # Artifact index
                if entry["layer"] == "artifacts":
                    aname = entry["artifact"]["name"]
                    if aname not in self.index_by_artifact:
                        self.index_by_artifact[aname] = []
                    self.index_by_artifact[aname].append(entry)
    
    # DISCOVERY QUERIES
    
    def get_artifacts(self, layer: Optional[str] = None, 
                     artifact_type: Optional[str] = None) -> List[Dict]:
        """Get all artifacts matching filter."""
        results = [e for e in self.entries if e["layer"] == "artifacts"]
        if artifact_type:
            results = [e for e in results 
                      if e["artifact"]["artifact_type"] == artifact_type]
        return results
    
    def get_changed_since(self, ts: datetime) -> List[Dict]:
        """Get all events (any layer) since timestamp."""
        ts_str = ts.isoformat()
        return [e for e in self.entries if e["ts"] > ts_str]
    
    def get_stale_items(self, threshold_days: int = 90) -> List[Dict]:
        """Get artifacts not touched in N days."""
        cutoff = datetime.utcnow().timestamp() - (threshold_days * 86400)
        return [e for e in self.get_artifacts()
                if e["ts"] < cutoff]
    
    def get_lifecycle(self, artifact_name: str) -> List[Dict]:
        """Complete history of one artifact."""
        return self.index_by_artifact.get(artifact_name, [])
    
    def get_agent_state(self, agent_type: str, session_id: Optional[str] = None) -> List[Dict]:
        """All state transitions for one agent."""
        results = [e for e in self.entries 
                  if e["layer"] == "agent_state" 
                  and e["agent_state"]["agent_type"] == agent_type]
        if session_id:
            results = [e for e in results if e["session_id"] == session_id]
        return results
    
    def get_transcript(self, session_id: str) -> List[Dict]:
        """Full conversation transcript for session."""
        return [e for e in self.entries 
                if e["layer"] == "transcripts" 
                and e["session_id"] == session_id]
    
    def get_learning_events(self, agent_type: str) -> List[Dict]:
        """All OTJ learning improvements for agent."""
        results = []
        for e in self.entries:
            if (e["layer"] == "agent_state" 
                and e["agent_state"].get("agent_type") == agent_type
                and e["agent_state"].get("learning_event")):
                results.append(e)
        return results
    
    def get_memory_lifecycle(self, mem_id: str) -> List[Dict]:
        """Track one MEM block from creation → promotion → archive."""
        return [e for e in self.entries 
                if e["layer"] == "working_memory"
                and e["memory"].get("block_id") == mem_id]
    
    # VERIFICATION QUERIES
    
    def verify_coc_chain(self, start_event_id: Optional[str] = None, 
                        end_event_id: Optional[str] = None) -> Tuple[bool, str]:
        """Verify hash chain integrity."""
        events = self.entries
        if start_event_id:
            start_idx = next(i for i, e in enumerate(events) 
                            if e["event_id"] == start_event_id)
            events = events[start_idx:]
        if end_event_id:
            end_idx = next(i for i, e in enumerate(events) 
                          if e["event_id"] == end_event_id)
            events = events[:end_idx+1]
        
        prev_id = None
        for entry in events:
            if prev_id and entry.get("prev_event_id") != prev_id:
                return False, f"Chain broken at {entry['event_id']}: prev_event_id mismatch"
            
            # Verify entry hash (if sig_type indicates signing)
            if entry.get("sig_type") in ["hmac", "pgp"]:
                if not self._verify_entry_hash(entry):
                    return False, f"Hash verification failed for {entry['event_id']}"
            
            prev_id = entry["event_id"]
        
        return True, "Chain verified"
    
    def _verify_entry_hash(self, entry: Dict) -> bool:
        """Compute and verify entry hash."""
        # Implementation: canonicalize, hash, compare
        pass
    
    # FORENSIC NARRATIVE
    
    def prove_learning_causality(self, agent_type: str, 
                                finding_ts: datetime) -> Dict:
        """Prove that OTJ learning didn't bias a finding."""
        result = {
            "agent": agent_type,
            "finding_ts": finding_ts.isoformat(),
            "proof_chain": []
        }
        
        # Find finding statement in transcripts
        finding_events = [e for e in self.entries 
                         if e["layer"] == "transcripts"
                         and "finding_stated_with_confidence" in str(e)
                         and datetime.fromisoformat(e["ts"]) <= finding_ts]
        
        if not finding_events:
            return {"error": "No findings found at that time"}
        
        latest_finding = max(finding_events, key=lambda e: e["ts"])
        result["proof_chain"].append({
            "event": "finding_stated",
            "ts": latest_finding["ts"],
            "confidence": latest_finding["transcript"]["response_summary"]["confidence_expressed"]
        })
        
        # Find learning events AFTER this finding
        learning_events = self.get_learning_events(agent_type)
        learning_after = [e for e in learning_events 
                         if e["ts"] > latest_finding["ts"]]
        
        if learning_after:
            result["proof_chain"].append({
                "event": "otj_learning_event",
                "ts": learning_after[0]["ts"],
                "kpi_improvement": learning_after[0]["agent_state"]["learning_event"]["delta"]
            })
            result["conclusion"] = "Learning event occurred AFTER finding. No retroactive bias possible."
        else:
            result["conclusion"] = "No learning events after this finding. Finding is unchanged by OTJ."
        
        return result
    
    def export_for_court(self, start_ts: datetime, end_ts: datetime) -> Dict:
        """Generate court-ready forensic bundle."""
        events = [e for e in self.entries 
                 if datetime.fromisoformat(e["ts"]) >= start_ts
                 and datetime.fromisoformat(e["ts"]) <= end_ts]
        
        return {
            "court_exhibit": "Claude Forensic Archive",
            "period": f"{start_ts.isoformat()} to {end_ts.isoformat()}",
            "event_count": len(events),
            "events": events,
            "hash_chain_verified": self.verify_coc_chain()[0],
            "signature": "optional_pgp_signature_block"
        }
```

---

## Integration Points

### At Session Start (`/faerie`)

```python
def session_startup():
    """Load forensic state."""
    archive = ForensicArchive(Path("~/.claude/forensic-archive"))
    
    # Read last 100 entries to detect state
    recent_events = archive.entries[-100:]
    
    # Find any incomplete memory (created but not promoted)
    incomplete_memory = [e for e in recent_events 
                        if e["layer"] == "working_memory"
                        and e["operation"] == "created"]
    
    # Find stale artifacts (not touched in 30d)
    stale = archive.get_stale_items(threshold_days=30)
    
    # Validate COC chain integrity
    chain_ok, msg = archive.verify_coc_chain()
    if not chain_ok:
        print(f"⚠️ WARNING: COC chain integrity issue: {msg}")
    
    # Report to user
    print(f"Forensic state loaded:")
    print(f"  - Total events: {len(archive.entries)}")
    print(f"  - Incomplete memory blocks: {len(incomplete_memory)}")
    print(f"  - Stale artifacts: {len(stale)}")
    print(f"  - COC chain: {'✓ verified' if chain_ok else '✗ BROKEN'}")
```

### At Memory Promotion (`memory-keeper` phase)

```python
def promote_memory_block(block_id: str, confidence: float):
    """Promote scratch → NECTAR with forensic entry."""
    archive = ForensicArchive(...)
    
    # Create promotion event
    event = {
        "event_id": generate_event_id(),
        "ts": datetime.utcnow().isoformat(),
        "layer": "working_memory",
        "operation": "promoted",
        "memory": {
            "block_id": block_id,
            "promoted_ts": datetime.utcnow().isoformat(),
            "promoted_to": "~/.claude/memory/NECTAR.md",
            "confidence": confidence
        },
        "prev_event_id": archive.entries[-1]["event_id"],
        "event_hash": compute_hash(...)
    }
    
    # Append to manifest
    with open(archive.manifest_path, "a") as f:
        f.write(json.dumps(event) + "\n")
    
    # Append to NECTAR
    with open(Path("~/.claude/memory/NECTAR.md"), "a") as f:
        f.write(f"\n{block_content}\n")
```

### At Agent Learning Event (`evidence-curator` post-run)

```python
def record_otj_learning(agent_type: str, kpi_before: float, kpi_after: float):
    """Record OTJ improvement in forensic archive."""
    archive = ForensicArchive(...)
    
    # Create learning event
    event = {
        "event_id": generate_event_id(),
        "ts": datetime.utcnow().isoformat(),
        "layer": "agent_state",
        "operation": "learning_event",
        "agent_state": {
            "agent_type": agent_type,
            "learning_event": {
                "type": "otj_improvement",
                "score_before": kpi_before,
                "score_after": kpi_after,
                "delta": kpi_after - kpi_before,
                "technique_discovered": "..."
            }
        },
        "prev_event_id": archive.entries[-1]["event_id"]
    }
    
    # Append to manifest
    append_to_manifest(event)
    
    # Update agent card
    update_agent_card_last_training(agent_type, kpi_after)
    
    # Create artifact update event (agent card write)
    artifact_event = {
        "event_id": generate_event_id(),
        "ts": datetime.utcnow().isoformat(),
        "layer": "artifacts",
        "operation": "update",
        "artifact": {
            "name": f"{agent_type}.md",
            "content_hash_after": hash_agent_card_file(agent_type)
        },
        "source_event_id": event["event_id"],  # Link to learning event
        "prev_event_id": event["event_id"]
    }
    
    append_to_manifest(artifact_event)
```

---

## Query Examples (Common Investigative Questions)

### Q1: "Show me every time agent X improved, and what triggered it"

```python
archive = ForensicArchive(...)
learning_events = archive.get_learning_events("evidence-curator")

for event in learning_events:
    print(f"Timestamp: {event['ts']}")
    print(f"KPI: {event['agent_state']['learning_event']['kpi']}")
    print(f"Score: {event['agent_state']['learning_event']['score_before']} → {event['agent_state']['learning_event']['score_after']}")
    print(f"Technique: {event['agent_state']['learning_event']['technique_discovered']}")
    
    # Find the artifact write that resulted from this learning
    artifact_event = next((e for e in archive.entries 
                          if e.get("source_event_id") == event["event_id"]), None)
    if artifact_event:
        print(f"Updated artifact: {artifact_event['artifact']['name']}")
```

### Q2: "Prove that finding X wasn't biased by later learning"

```python
archive = ForensicArchive(...)
proof = archive.prove_learning_causality("evidence-curator", datetime(2026, 4, 7, 14, 22))

for step in proof["proof_chain"]:
    print(f"{step['event']} at {step['ts']}")

print(proof["conclusion"])
```

### Q3: "What was the complete state of agent X when working on task Y?"

```python
archive = ForensicArchive(...)
state_events = archive.get_agent_state("evidence-curator", session_id="session-20260407")

# Find state_transition events
for event in state_events:
    if event["operation"] == "state_transition":
        v1 = event["agent_state"]["state_transition"]["state_v1"]
        v2 = event["agent_state"]["state_transition"]["state_v2"]
        
        print(f"At {event['ts']}: assumptions shifted")
        print(f"  Before: {v1['assumptions']}")
        print(f"  After:  {v2['assumptions']}")
```

### Q4: "What evidence was cited when finding H1 was stated?"

```python
archive = ForensicArchive(...)
transcript = archive.get_transcript("session-20260407-main-001")

for event in transcript:
    if event["operation"] == "response" and "finding_stated" in str(event):
        print(f"Finding: {event['transcript']['response_summary']['finding']}")
        print(f"Confidence: {event['transcript']['response_summary']['confidence_expressed']}")
        print(f"Sources cited:")
        for src in event['transcript']['response_summary']['sources']:
            print(f"  - {src}")
```

---

## Court Admissibility

**Why this system is defensible in court:**

1. **Immutable chain:** Every entry is hash-chained to previous. Modifying any entry breaks the chain and is immediately detectable.

2. **Causality proof:** State transitions prove learning didn't bias findings:
   - Finding stated at 13:15 (state V1, partial data)
   - Learning event at 13:45 (after finding)
   - Timestamp chain proves T_learning > T_finding

3. **Evidence trail:** Every finding is tied to specific evidence sources, with hashes:
   - Expert can verify "Which 18 .gov domains were cited?"
   - Hash points to exact records in audit trail
   - No post-hoc narrative possible

4. **Transparency:** Full reasoning visible:
   - MEM blocks show what agent considered
   - State transitions show assumptions and how they changed
   - Transcripts preserve exact language used

5. **Third-party verification:** Chain-of-custody API allows independent auditors to:
   - Verify hash chain without trusting the system
   - Audit agent capability improvements
   - Cross-check findings against source evidence

**For a defense attorney challenging the findings:**

> "Can you prove this finding wasn't cherry-picked after you saw the results?"

Answer: "Yes. Here's the complete timestamp sequence:
- Finding stated at 14:22 (turn 23 of transcript, preserved in manifest)
- Evidence cited: three sources (hashes provided)
- OTJ learning event: 14:45 (35 minutes AFTER finding)
- Hash chain: unbroken from session start to export"

**Court-ready export:**

```python
bundle = archive.export_for_court(
    start_ts=datetime(2026, 4, 7, 13, 0),
    end_ts=datetime(2026, 4, 7, 15, 0)
)

# This generates:
# - manifest.jsonl (subset)
# - hash proof (all entries verify)
# - narrative summary (what happened, why, timeline)
# - transcript (full conversation)
# - evidence registry (all cited sources)
```

---

## Implementation Phasing

### Phase 1: Manifest + Basic COC (2026-04-07 to 2026-04-21)

**Scope:** Establish foundational infrastructure

- Create `~/.claude/forensic-archive/` structure
- Implement `ForensicArchive.py` class (load, append, query)
- Begin recording all four layers to manifest.jsonl
- Write integration hooks for:
  - Session open/close (transcript layer)
  - Memory promotion (working_memory layer)
  - Agent learning events (agent_state layer)
  - Artifact updates (artifacts layer)
- Verify manual chain for one full session

**Deliverable:** manifest.jsonl with 200+ entries, first session fully logged

### Phase 2: Signing + Verification (2026-04-21 to 2026-05-05)

**Scope:** Court-grade integrity

- Add PGP signing to critical entries (learning events, findings, memory promotion)
- Implement `verify_coc_chain()` verification API
- Create `export_for_court()` bundler
- Test: court-ready export for one session
- Document chain-of-custody for expert witness

**Deliverable:** Signed manifest entries, court export template, expert witness doc

### Phase 3: Query API + Dashboard (2026-05-05 to 2026-05-19)

**Scope:** Usability + discovery

- Implement full ForensicArchive query API
- Build CLI tool: `python ~/.claude/forensics/query.py --agent evidence-curator --kpi`
- Build web dashboard (read-only):
  - Timeline view (events chronologically)
  - Agent view (learning curve, capability over time)
  - Finding view (traceability to evidence)
  - Audit view (memory lifecycle, promotions)
- Integration with `/memory` skill

**Deliverable:** Query CLI, dashboard, example usage docs

### Phase 4: Archive Rotation + Performance (2026-05-19+)

**Scope:** Long-term sustainability

- Implement retention policy (keep last 3 years in manifest.jsonl, archive older to SQLite for query performance)
- Add incremental backup (manifest diffs)
- Monitor file size (expect ~500MB-1GB/year)
- Parallel COC digest file (coc.jsonl — summary for quick scanning)

**Deliverable:** Rotation policy, performance benchmarks

---

## Open Questions

### Retention & Archival

- **How long to keep manifest.jsonl in git?** Current plan: 1 year, then rotate to archive/ folder + SQLite backup for queries.
- **How to handle sensitive case data in manifest?** Option: redact entity names, keep structure/hashes.
- **Archive format?** Tar + PGP-encrypted; kept on B2 WORM (immutable).

### Performance at Scale

- **Manifest size growth:** ~2-3 events per session × 50 sessions/month × 12 months = ~1,200 events/year. ~500KB-1MB per year.
- **Query performance:** 10,000+ events → linear scan becomes slow. Need SQLite for historical queries?
- **Session-to-manifest ratio:** One session can generate 100s of events. Efficient batching?

### Privacy & Redaction

- **Entity names in events:** Learning events might reference people (e.g., "Edward C."). Should these be redacted before export?
- **Sensitive file paths:** Some investigation paths shouldn't be public. Auto-redact?
- **Case data in state:** Task state transition might include hypothesis confidence on sensitive topics. What stays, what goes?

### Integration with Court System

- **Affidavit template:** What does an expert witness affidavit look like using this data?
- **Chain of custody officer:** Who certifies the export bundle? System operator? Human reviewer?
- **Challenge procedure:** If defense attorney challenges the findings, what's the auditing protocol?

---

## File Structure Summary

```
~/.claude/forensic-archive/
├── manifest.jsonl                  [1.0-1.5K lines/month, append-only]
├── coc.jsonl                       [optional: digest for quick scan]
├── artifacts/
│   ├── agent-cards/                [hash-keyed backups]
│   ├── skills/
│   ├── rules/
│   ├── memories/
│   └── system-config/
├── agent-state/
│   ├── task-states/                [session-keyed directories]
│   │   └── session-20260407/
│   │       ├── agent-evidence-curator.json
│   │       └── agent-research-analyst.json
│   ├── checkpoints/
│   ├── rosters/
│   └── learning-events.jsonl       [append-only, all OTJ improvements]
├── working-memory/
│   ├── scratch/
│   │   └── session-20260407/
│   │       ├── draft-mem-blocks.md
│   │       └── validated-connections.json
│   ├── pollen/                     [promoted memory, archive here too]
│   ├── reasoning-trails/           [detailed decision chains]
│   └── mem-blocks/                 [categorized by HIGH/MED/LOW priority]
├── transcripts/
│   ├── conversations/              [session-keyed]
│   │   └── session-20260407.md
│   ├── tool-calls/                 [extracted for audit]
│   └── execution-traces/           [if detailed logging enabled]
└── verification/
    ├── hash-proofs/                [readable chain proofs]
    ├── pgp-signatures/             [signed entries]
    ├── audit-queries/              [pre-computed common queries]
    └── court-exports/              [bundles ready for submission]
```

---

## Success Criteria

**Phase 1 (manifest + logging):**
- [ ] Manifest.jsonl grows (50+ entries per session)
- [ ] All four layers represented
- [ ] Session start → close creates closed event chain
- [ ] Manual spot-check: can recreate session from manifest

**Phase 2 (signing + verification):**
- [ ] Critical events PGP-signed
- [ ] Hash chain verifies for 100% of entries
- [ ] Export bundle acceptable to (mock) court
- [ ] Expert witness affidavit template written

**Phase 3 (query API):**
- [ ] CLI tool: `query --agent X --learning-events` returns timeline
- [ ] Dashboard loads in <2 seconds
- [ ] Example: "Prove finding H1 wasn't biased" query returns clean proof

**Phase 4 (production):**
- [ ] Manifest rotation to archive/ at 1-year mark
- [ ] <1 second response for queries on current year
- [ ] Backup to B2 WORM every month
- [ ] Zero loss of forensic data across 12 months of production

---

## Related Documents

- `~/.claude/rules/evidence-coc.md` — Evidence COC (inspiration for this design)
- `~/.claude/rules/memory-routing.md` — Memory layer organization
- `~/.claude/rules/agent-lifecycle.md` — Agent state transitions
- `.claude/rules/memory-guide.md` — Human reference for memory system

---

**Author:** Knowledge Synthesizer  
**Status:** Design + Schema Complete; Phase 1-2 Ready for Implementation  
**Next Steps:** Review with human for approval; begin Phase 1 integration (manifest logging hooks)
