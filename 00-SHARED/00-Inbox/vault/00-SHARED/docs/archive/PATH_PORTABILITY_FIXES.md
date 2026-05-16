# Path Portability Fix Plan

## Status: IN PROGRESS
Date: 2026-04-21
Task: task-w4-path-portability

## Hardcoded Paths Found: 144 instances across 38 scripts

### Breakdown
- `/mnt/c/Users/amand/.claude` hardcodes: 8 scripts (lines 49-50, 21, 16, etc.)
- `/mnt/d/0LOCAL/.claude` hardcodes: 12 scripts
- `/mnt/d/0LOCAL/gitrepos/*` hardcodes: 8 scripts
- `~/.claude` in docstrings/comments: ~80 instances (not actual code)
- `/mnt/d/0LOCAL/0-ObsidianTransferring` hardcodes: 4 scripts

## Canonical Resolution Pattern
```python
def _resolve_claude_home() -> Path:
    if "CLAUDE_HOME" in os.environ:
        return Path(os.environ["CLAUDE_HOME"])
    homedrive = os.environ.get("HOMEDRIVE", "")
    homepath = os.environ.get("HOMEPATH", "")
    if homedrive and homepath:
        candidate = Path(homedrive + homepath) / ".claude"
        if candidate.parent.exists():
            return candidate
    return Path.home() / ".claude"
```

## Fixed Scripts (Executed)
- [ ] 8x_agent_spawn_autoinject.py
- [ ] 8x_context_shed_monitor.py
- [ ] 8x_hook_runner.py
- [ ] 8x_intent_classifier.py
- [ ] 8x_manifest_auto_continue.py
- [ ] 8x_notification_handler.py
- [ ] 8x_pre_action_memory_scan.py
- [ ] 8x_pre_compact_shed.py
- [ ] 8x_pre_write_forensics_guard.py
- [ ] 8x_pre_write_memory_guard.py
- [ ] 8x_inject_vault_output.py
- [ ] 9x_context_weight.py
- [ ] 9x_debloat.py
- [ ] 9x_droplet_cadence.py
- [ ] 9x_enforce_budget.py
- [ ] 9x_equilibrium_audit.py
- [ ] 9x_faerie_ab_test_runner.py
- [ ] 9x_generate_review_hot.py
- [ ] 9x_stigmergy_tracker.py
- [ ] 9x_sync_obsidian_vault.py
- [ ] 9x_validate_state_files.py
- [ ] 9x_statusline.py
- [ ] 9x_shared_file_cache.py
- [ ] 9x_state_serializer.py
- [ ] 9x_citation_verifier.py

## Environment Variables
- `CLAUDE_HOME` — points to ~/.claude (normalized)
- `CT_VAULT` — points to Obsidian vault root
- `GITREPOS` — points to /mnt/d/0LOCAL/gitrepos (or equivalent)
- `HOMEDRIVE` + `HOMEPATH` — Windows context (Git Bash, native Python)

## Next Steps
1. Replace all `/mnt/c/Users/amand/.claude` with Path.home() / ".claude" or env-var lookups
2. Replace `/mnt/d/0LOCAL/gitrepos` with GITREPOS env var + fallback
3. Replace `/mnt/d/0LOCAL/0-ObsidianTransferring` with CT_VAULT env var
4. Verify path_utils.py remains as canonical safety validator (not path resolver)
5. Test 5-10 key scripts for path correctness
