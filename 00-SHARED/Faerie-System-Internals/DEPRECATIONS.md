---
type: reference
status: live
created: 2026-04-27
updated: 2026-04-27
tags: [deprecations, skills, cleanup, archival]
parent: ../README.md
doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1
---

> **Breadcrumb:** faerie-vault > 00-SHARED > DEPRECATIONS

# Deprecated Skills & Scripts (2026-04-27)

This document lists skills and scripts that are archival-only, superseded, or no longer actively used. They are kept for historical reference but should NOT be invoked for new work.

---

## Deprecated Skills (Global ~/.claude/skills/)

### Queue-Based Task Dispatch (Superseded by Compass Navigation)

| Skill | Reason | Replacement | Notes |
|-------|--------|-------------|-------|
| `/queue` | Linear FIFO queue replaced by compass bearing navigation | `/spawn` + compass edges | Manifests now route via N/S/E/W bearings, not queues |
| `/queue-and-spawn` | Atomic queue+claim+spawn; queue system removed | `/spawn` (direct) | Use /spawn to emit bundles; agents discover via investigation_label |
| `/run` | Mission-aware queue consumer; queue deprecated | `/spawn` (emit bundles) | Agents discover work via frontier scan + stigmergic clustering |
| `/sprint` | Sprint planning tied to queue | `/spawn` + /handoff | Use compass edges for phase gating, not velocity |
| `/sprint-prep` | Sprint prep on deprecated queue | N/A | Plan missions via 7x_mission_graph_ops.py add |

### Evaluation & Health Monitoring (Internal, Auto-Wired to /handoff)

| Skill | Reason | Status | Notes |
|-------|--------|--------|-------|
| `/dev-eval-loop` | Automated eval loop; now in /handoff membot | Archive | Run `/dev-eval` for single snapshot |
| `/dev-health` | System health dashboard; in eval harness | Archive | Use `/dev-eval` instead |
| `/dev-status` | Status reporting; redundant with /status | Archive | Use `/status` or `/faerie` |
| `/dev-pressure` | Context pressure monitoring; auto in piston | Archive | Pressure-responsive spawning automatic |

### Memory Management (Auto via HONEY/NECTAR + Droplets)

| Skill | Reason | Replacement | Notes |
|--------|--------|-------------|--------|
| `/memory-audit` | Manual memory audit; auto-run by /handoff | N/A | Memory wired into eval harness |
| `/memory-ingest` | Manual ingestion; automatic via handoff | N/A | pollen→NECTAR→HONEY runs at /handoff |
| `/investigate` | Old investigation workflow | Compass navigation | Use investigation_label clustering |

### Session Auditing (Archival, Auto-Generated)

| Skill | Reason | Status | Notes |
|-------|--------|--------|-------|
| `/audit-session` | Post-hoc audit; auto-generated | Archive | Sessions auto-audited via session_stop_hook.py |
| `/audit-investigation` | Investigation audit; in forensics/ | Archive | forensics/coc-entries/ + manifests/ serve as audit |
| `/audit-coc` | COC audit; redundant with hash check | Archive | Hash verification auto-runs via linter |
| `/audit-equilibrium` | Equilibrium check; in mutation discipline | Archive | Wired into /handoff eval harness |

---

## Active Skills (DO USE)

### Primary Workflow

- **`/faerie`** — Session start orchestrator
- **`/handoff`** — Session end wind-down (membot, snapshot, eval)
- **`/spawn`** — Emit task bundles for stigmergic discovery

### Secondary

- **`/dev-eval`** — System health snapshot (eval harness + vault report)
- **`/crystallize`** — Manual NECTAR→HONEY crystallization
- **`/stat`** — Statistical analysis
- **`/memory`** — Manual memory operations

### Utilities

- **`/status`** — Current system status (compass + unblocked work)
- **`/done`** — Mark task complete
- **`/suggest`** — Next work suggestions

---

## Migration

### From `/run` → `/spawn`
```bash
# OLD (deprecated)
/run --focus investigation_label

# NEW
python3 scripts/7x_mission_graph_ops.py add --goal "..." --investigation-label "..."
# Agents discover via frontier scan
```

### From `/queue` → `/spawn`
```bash
# OLD
/queue add --priority HIGH "task"
/run

# NEW
python3 scripts/7x_mission_graph_ops.py add --priority HIGH --goal "..."
# Agents discover autonomously
```

---

## Timeline

- **2026-04-27:** Deprecation published
- **2026-05-04:** Old skills marked read-only with deprecation banner
- **2026-05-11:** Skills moved to `.deprecated-skills/` for archival
- **2026-06-01:** Old skills removed from active skill list

---

**Status:** Live  
**Last Reviewed:** 2026-04-27  
**Next Review:** 2026-05-04
