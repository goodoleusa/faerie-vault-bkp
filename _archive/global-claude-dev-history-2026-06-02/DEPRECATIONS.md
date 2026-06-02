---
type: reference
status: live
created: 2026-04-27
updated: 2026-04-27
tags: [deprecations, skills, cleanup, archival]
---

# Deprecated Skills & Scripts (2026-04-27)

This document lists skills and scripts that are archival-only, superseded, or no longer actively used. They are kept in the repo for historical reference but should NOT be invoked for new work.

---

## Deprecated Skills (Global ~/.claude/skills/)

### Queue-Based Task Dispatch (Superseded by Compass Navigation)

| Skill | Reason | Replacement | Notes |
|-------|--------|-------------|-------|
| `/queue` | Linear FIFO queue replaced by compass bearing navigation | `/spawn` + compass edges | Manifests now route via N/S/E/W bearings, not queues |
| `/queue-and-spawn` | Atomic queue+claim+spawn; queue system removed | `/spawn` (direct) | Use /spawn to emit bundles; /run discovers them via investigation_label |
| `/run` | Mission-aware queue consumer; queue deprecated | `/spawn` (emit bundles) + stigmergic discovery | Agents discover work via frontier scan, not /run dispatch loop |
| `/sprint` | Sprint planning tied to queue | `/spawn` + /handoff | Use compass edges for phase gating, not sprint velocity |
| `/sprint-prep` | Sprint prep on deprecated queue | N/A (manual planning) | Plan missions via 7x_mission_graph_ops.py add |

### Evaluation & Health Monitoring (Internal Infrastructure, Not User-Facing)

| Skill | Reason | Status | Notes |
|-------|--------|--------|-------|
| `/dev-eval-loop` | Automated eval loop; now wired into /handoff | Archive | Evals run at session end via /handoff membot |
| `/dev-health` | System health dashboard; now in /dev-eval | Archive | Use `/dev-eval` for single health snapshot |
| `/dev-status` | Status reporting; redundant with /status | Archive | Use `/status` (alias for /faerie compass view) |
| `/dev-pressure` | Context pressure monitoring; auto-wire in piston model | Archive | Pressure-responsive spawning happens automatically |

### Memory Management (Superseded by HONEY/NECTAR/Pollen + Droplets)

| Skill | Reason | Replacement | Notes |
|--------|--------|-------------|--------|
| `/memory-audit` | Manual memory audit; now auto-run by /handoff | N/A | Memory health wired into eval harness |
| `/memory-ingest` | Manual memory ingestion; automatic via handoff | N/A | pollen→NECTAR→HONEY flow runs at /handoff |
| `/investigate` | Old investigation workflow | Compass navigation | Use investigation_label clustering instead |

### Session Auditing (Archival Records, Not Active Workflows)

| Skill | Reason | Status | Notes |
|-------|--------|--------|-------|
| `/audit-session` | Post-hoc session audit log | Archive | Session audits auto-generated via session_stop_hook.py |
| `/audit-investigation` | Investigation audit; now in forensics/ | Archive | forensics/coc-entries/ and manifests/ serve as audit trail |
| `/audit-coc` | COC audit; redundant with hash verification | Archive | Hash verification runs automatically via linter hooks |
| `/audit-equilibrium` | Equilibrium check for system improvements | Archive | Mutation discipline wired into /handoff eval harness |

### Miscellaneous Archival

| Skill | Reason | Status | Notes |
|-------|--------|--------|-------|
| `/reconstruct-db` | Database reconstruction (legacy project) | Archive | Not applicable to faerie2 |
| `/compress-context` | Manual context compression | Archive | Auto-compression managed by session compact hook |
| `/context-roundup` | Manual context roundup | Archive | /handoff writes context snapshot automatically |

---

## Deprecated Scripts (faerie2/.claude/scripts/ & ~/.claude/scripts/)

### Queue Management (Removed)

```
DEPRECATED: 7x_sprint_queue_ops.py
DEPRECATED: 7x_queue_query.py
DEPRECATED: 8x_queue_monitor.py
REASON: Linear queue replaced by compass bearing navigation
REPLACEMENT: 7x_mission_graph_ops.py (mission-aware routing)
```

### Memory Management (Automated via Hooks)

```
DEPRECATED: 5x_memory_consolidator.py (manual consolidation)
DEPRECATED: 5x_nectar_ripener.py (manual crystallization)
REASON: Now wired into /handoff membot + pollen system
REPLACEMENT: automatic via handoff → membot → /crystallize
```

---

## Active Skills (DO USE THESE)

### Primary Workflow Entry Points

- **`/faerie`** — Session start orchestrator (read brief, launch team, execute)
- **`/handoff`** — Session end wind-down (membot, snapshot, eval)
- **`/spawn`** — Emit task bundles for stigmergic discovery

### Secondary Workflow

- **`/dev-eval`** — System health snapshot (runs eval harness, writes vault report)
- **`/crystallize`** — Manual NECTAR→HONEY crystallization (when needed)
- **`/stat`** — Statistical analysis for hypothesis testing
- **`/memory`** — Manual memory operations (read NECTAR, update HONEY)
- **`/data-ingest`** — Batch data ingestion for investigations

### Utilities

- **`/status`** — Current system status (compass edges, unblocked work)
- **`/done`** — Mark task complete
- **`/suggest`** — Get suggestions for next work

---

## Migration Guide

### If You Were Using `/run`:
Instead of:
```bash
/run --focus investigation_label
```
Do this:
```bash
# Option 1: Spawn agents directly
/spawn --goal "investigation objective" --investigation-label "label"

# Option 2: Let agents discover work
# Agents scan forensics/{YYYY-MM-DD}/ frontier, find matching investigation_label, claim work
```

### If You Were Using `/queue`:
Instead of:
```bash
/queue add --priority HIGH "task description"
/run
```
Do this:
```bash
# Chart mission via script
python3 scripts/7x_mission_graph_ops.py add \
  --goal "atomic objective" \
  --investigation-label "mission-cluster" \
  --priority HIGH

# Agents discover and claim via /spawn or natural investigation_label clustering
```

### If You Were Using `/sprint`:
Instead of:
```bash
/sprint-prep --velocity 40 --duration 2w
```
Do this:
```bash
# Plan missions via compass graph
python3 scripts/0x_compass_query.py --topology
# Chart new bundles
python3 scripts/7x_mission_graph_ops.py add ...
# Let agents execute with W1/W2/W3 wave dispatch
```

---

## Why Deprecate?

1. **Reduce cognitive load:** Fewer skills = clearer mental model
2. **Enable emergence:** Compass navigation + stigmergy doesn't need central dispatcher (/run)
3. **Automate infrastructure:** Evaluation, memory management, auditing now run at session boundaries
4. **Align with f(0) principle:** Zero orchestration burden on main; agents self-coordinate

---

## Timeline

- **2026-04-27:** Deprecation list published
- **2026-05-04:** Old skills marked read-only (BODY.md shows deprecation banner)
- **2026-05-11:** Old skills moved to `.claude/deprecated-skills/` (for archival reference)
- **2026-06-01:** Old skills removed from active skill list

---

## Questions?

If a deprecated skill was critical to your workflow, please open an issue or ask for clarification. Some skills may be kept alive if evidence shows they're still needed.

---

**Status:** Live (2026-04-27)  
**Last Reviewed:** 2026-04-27  
**Next Review:** 2026-05-04
