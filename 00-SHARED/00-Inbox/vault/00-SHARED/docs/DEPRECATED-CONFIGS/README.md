# Deprecated Configurations (Archive Reference)

These JSON files are historical artifacts. They have been superseded by newer systems and should not be used.

## Files

### bundle-composition.json
- **Deprecated:** 2026-04-22
- **Reason:** Redundant with spawn-templates/ registry. Templates now declare body_partials explicitly.
- **Replaced by:** `~/.claude/spawn-templates/agents/*.json` (body_partials field)
- **Archive reason:** Single source of truth moved to template definitions

### consolidation-phase1-plan.json
- **Deprecated:** 2026-04-22
- **Reason:** One-time task (completed 2026-04-21)
- **Purpose (historical):** Tracked consolidation work during Phase 1
- **Archive reason:** Completed, no ongoing reference needed

### model-routing-policy.json
- **Deprecated:** 2026-04-22
- **Reason:** Duplicates AGENT-TYPE-ROUTING.json
- **Replaced by:** `AGENT-TYPE-ROUTING.json` (single source of truth)
- **Archive reason:** Prevents drift, maintains single authoritative source

---

**Keep:** AGENT-TYPE-ROUTING.json, waves-config.json (both critical, non-redundant)
