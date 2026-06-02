---
type: test-result
test_run_id: sdk-qa-2026-04-28T14-54-32Z
date: 2026-04-28
verdict: NOT_SHIP_READY
blocker_count: 3
---

# Test Result — 2026-04-28

**Run ID:** sdk-qa-2026-04-28T14-54-32Z  
**Verdict:** `NOT_SHIP_READY`  
**Blockers:** 3

## API Contract Validation

| Check | Result | Note |
|-------|--------|------|
| bundle_structure_complete | PASS | All 8 required keys present |
| bundle_json_serializable | PASS | json.dumps() clean |
| bundle_assembly_tokens | PASS |  |
| manifest_task_id_present | PASS | 25/25 |
| manifest_dashboard_line_present | FAIL | 11 spawn-intent records lack dashboard_line |
| manifest_compass_edge_present | PASS | 23/25 |
| manifest_dashboard_line_under_80_chars | FAIL | 14/25 |
| manifest_json_serializable | PASS | 25/25 |
| coc_entries_immutable | FAIL | coc-entries/ absent, path hardcoded to faerie2 repo |
| coc_writer_algorithm | PASS | fcntl+HMAC+Ed25519+atomic-rename — correct implementation |
| error_messages_actionable | PASS | ValueError messages include fix instructions + docs links |

## Security Audit

| Check | Result | Severity |
|-------|--------|----------|
| task_id_prompt_injection | FAIL | HIGH |
| delta_field_injection | PASS | - |
| honey_nectar_sensitive_data_leak | CONDITIONAL_FAIL | MEDIUM |
| manifest_write_atomicity | PASS | - |
| coc_audit_trail_complete | FAIL | HIGH |
| queue_autonomy_deprecated_path | FAIL | HIGH |
| spawn_chain_key_default_public | FAIL | MEDIUM |
