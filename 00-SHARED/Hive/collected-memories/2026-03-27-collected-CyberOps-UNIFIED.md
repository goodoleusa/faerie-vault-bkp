---
type: collected-memory
status: unreviewed
created: 2026-03-27
updated: 2026-03-27
tags: [memory, collected, agent-memory, CyberOps-UNIFIED]
source_project: "/mnt/d/0LOCAL/0/ObsidianTransferring/CyberOps/UNIFIED"
source_file: "MEMORY.md"
source_path_wsl: "/mnt/c/Users/amand/.claude/projects/-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED/memory/MEMORY.md"
source_path_windows: "C:\Users\amand\.claude\projects\-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED\memory\MEMORY.md"
source_sha256: "1b8779bdd65b739101c2cd9c3e28f46e42e48616032afc432590588d81530cd3"
source_size_bytes: 2945
collected_at: "2026-03-27T19:27:15Z"
collector: emergency_handoff.py
parent:
  - "[[agent-history]]"
sibling: []
child: []
memory_lane: inbox
promotion_state: capture
review_status: unreviewed
ann_hash: ""
ann_ts: ""
doc_hash: sha256:e9869b3c0e6c07c561aae84aa6a888fcb5e37fadce24d760e5fab3fb7032661a
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:30Z
hash_method: body-sha256-v1
---

# Collected Memory: CyberOps-UNIFIED

| Field | Value |
|-------|-------|
| Source Project | `/mnt/d/0LOCAL/0/ObsidianTransferring/CyberOps/UNIFIED` |
| Source File | `MEMORY.md` |
| Local Path (WSL) | `/mnt/c/Users/amand/.claude/projects/-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED/memory/MEMORY.md` |
| Local Path (Windows) | `C:\Users\amand\.claude\projects\-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED\memory\MEMORY.md` |
| SHA256 (at collection) | `1b8779bdd65b739101c2cd9c3e28f46e42e48616032afc432590588d81530cd3` |
| Lines | 56 |
| Collected | 2026-03-27T19:27:15Z |

## Content

```markdown
# CyberOps-UNIFIED Vault Memory

## Session 2026-03-27 (continued): Emergency Handoff + Memory Fusion

### New Architecture: Emergency Handoff
- `~/.claude/scripts/emergency_handoff.py` — fire-and-forget at 1% context
- Collects ALL splintered `.claude/projects/*/memory/MEMORY.md` (51 files, 1776 lines)
- Nests project memories into their repos (`collected/` subdirs)
- Writes atomized brief checkpoint to `brief-atoms/` (accumulates, never overwritten)
- Writes `handoff-snapshot.json` (700KB roundup) + updates `faerie-brief.json`
- `/handoff` Step Zero fires this script BEFORE any LLM work
- `/faerie` reads snapshot first (1 file replaces 15 scattered reads)

### Atomized Brief Architecture
- Briefs are NOT a single overwritten file — they're chunked checkpoints
- `brief-atoms/` accumulates: handoff atoms, pipeline phase atoms (from briefgen.py)
- `faerie-brief.json` = lightweight pointer, NOT source of truth
- On data-ingest days: 4+ atoms per day (SEED, DEEPEN, EXTEND, handoff)
- Obsidian Dataview queries atoms; Blueprints templates assemble human reports

### Memory Fusion (project memories + investigation memory)
- Claude's auto-memories (`.claude/projects/*/memory/`) are splintered across 7+ folders
- Emergency handoff collects and nests them into repo `collected/` dirs
- Immediately useful items flagged for membot crystallization → NECTAR/HONEY
- `faerie-brief.json` lists `fragmented_memory_files` so faerie knows what to process

### Three-Layer Separation (preserved)
- COC: `forensics/` — immutable, hash-chained, agents WRITE-ONLY (749 entries, 3492 sessions)
- Human: vault `30-Evidence/`, `## Your Annotations` — agents never touch
- Narrative: NECTAR/HONEY/atoms — agents write JSON, Blueprints render human-readable

### Commands → Skills Compatibility
- CLI v2.1.72 relabels commands as "skills" internally (`--disable-slash-commands` = "Disable all skills")
- Both mechanisms still work. Commands = user types `/name`. Skills = LLM calls Skill tool.
- If deprecated: move 9 command files to skills/ format (same content, different wrapper)

### Forensic Corpus (criticalexposure investigation)
- `master-coc.jsonl`: 749 entries
- Session manifests: 3,492 files
- Audit log: 347 lines
- Context bundles archived: 8 files
- Needs dedicated /data-ingest sprint, not ad-hoc processing

### Prior Session Completed (2026-03-27 early)
- VAULT-SCHEMA.md, briefgen.py, Brief-Assembly.blueprint, System-Design.blueprint
- agent_card_snapshot.py, vault_agent_evolution_sync.py
- COC reconciled (DAE→CT), pipeline renumbered (0a→6a)
- Agent-Performance.md (FFFF dashboard), System-Architecture.md (MermaidJS)

### Open Items
1. Consolidate briefgen.py (lib/ vs scripts/)
2. QuickAdd macro for MermaidJS from headers
3. 03-Agents/cards/ read-only mirror
4. Git commit vault cleanup
5. 8 agents missing evolution narratives
6. criticalexposure forensic corpus processing (queue as /data-ingest sprint)
```

## Your Annotations

<!-- What's useful here? Should any items be promoted to NECTAR/HONEY? -->
<!-- Are there tasks or threads to queue? -->

