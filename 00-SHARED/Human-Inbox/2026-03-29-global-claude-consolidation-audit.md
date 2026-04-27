---
type: audit-report
agent_type: fullstack-developer
session_id: consolidation-20260329
doc_hash: sha256:pending
status: final
date: 2026-03-29
---

# Global .claude Consolidation Audit — 2026-03-29

## Summary

Full audit of ~/.claude/ complete. All primary infrastructure present and wired.
Three gaps resolved inline. One budget issue (AGENTS.md) remains queued.

## Subsystem Status

### Scripts (verified functional)
- queue_analyzer.py: PRESENT in scripts/, all 4 intent modes tested (unblock/momentum/deep/balanced)
- memory_gate.py: PRESENT in scripts/, status command functional, BUDGETS config updated
- staging_promoter.py: PRESENT in scripts/ (160 lines)
- blueprint-validator.py: IN hooks/ -- correct; blueprint_vault_write_hook.py delegates to it

### Skills (all 4 core skills verified)
- faerie/SKILL.md: PRESENT (420 lines), includes Step 6 queue_analyzer.py intent-driven piston
- run/SKILL.md: PRESENT (147 lines)
- handoff/SKILL.md: PRESENT (132 lines)
- crystallize/SKILL.md: PRESENT (83 lines)

### Hooks wired in settings.json
PreToolUse: budget_check, blueprint_vault_write_hook, prevent-staging
PostToolUse: forensic_coc, validate_state_files, vault_hash_stamp, memory_collector
Stop: forensic_coc, session_stop_hook, session_metrics, surfacing_scheduler, eval_harness, write_eval_mirror, write_memory_status, routing_feedback, vault_narrative_sync
PreCompact: pre_compact_hook, scratch_collector
UserPromptSubmit: health_check (faerie2/brain), pre-session, dashboard_launcher, vault_narrative_sync, memory_bridge, queue_vault_sync

### Rules
All 5 present. Total: 5755 tok vs 6000 tok budget -- OK.

### Memory Files
- HONEY.md: 4334 tok / 5K budget -- OK
- NECTAR.md: unbounded
- REVIEW-INBOX.md: unbounded
- AGENTS.md: 2076 tok / 2000 tok budget -- OVER (76 tok). Crystallize task queued.

### Queue (sprint-queue.json)
50 tasks total, 42 queued. All required schema fields present.
queue_analyzer.py --intent unblock --print-dashboard: WORKING.

## Fixes Applied

1. health_check.py wrapper created at ~/.claude/scripts/health_check.py
   Delegates to faerie2/brain/health_check.py (resolves path mismatch in faerie SKILL.md Step 0).

2. memory_gate.py BUDGETS updated
   Stale commands/faerie.md + commands/launch.md -> skills/faerie/SKILL.md (max=500) + skills/run/SKILL.md (max=200).
   0 MISSING entries now.

3. Manifest written to ~/.claude/consolidation-audit-20260329.json

## Remaining (queued)
- AGENTS.md crystallize: sprint-20260328-020725-7db3
- rules/ line-count shows OVER in memory_gate but token budget is fine (6K)
