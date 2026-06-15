# Script Consolidation Log — 2026-04-05

## Problem Statement

Scripts lived in 3-4 locations with duplicates and no clear canonical home:
- `brain/` (8 scripts) — repo-level modules
- `nervous-system/hooks/` (7 scripts) — portable hook layer
- `nervous-system/vault-sync/` (4 scripts) — vault sync portable layer
- `.claude/scripts/` (58 scripts) — Claude CLI runtime scripts
- `.claude/hooks/` — hook scripts referenced by settings.json

## Canonical Locations After Consolidation

| What | Canonical | Notes |
|------|-----------|-------|
| Runtime scripts (non-hook) | `.claude/scripts/` | Skills, memory, vault ops |
| Hook scripts | `.claude/hooks/` | settings.json references these |
| Queue/state ops | `.claude/hooks/state/` | queue_ops.py canonical here |

## brain/ Decisions

| File | Decision | Rationale |
|------|----------|-----------|
| `health_check.py` | Replaced .claude/scripts/ thin wrapper with full brain/ impl | .claude/scripts/ was a 36-line delegating wrapper; brain/ had the real 590-line implementation |
| `emergency_handoff.py` | brain/ version now canonical in .claude/scripts/ | brain/ was newer (22:15 vs 22:03 Apr5) |
| `surfacing_scheduler.py` | .claude/scripts/ kept (newer) | Mar29 vs Mar28 |
| `session_metrics.py` | .claude/scripts/ kept (newer) | Mar29 vs Mar28 |
| `context_phase.py` | .claude/scripts/ kept (newer) | Mar29 vs Mar28 |
| `queue_ops.py` | Identical to .claude/hooks/state/queue_ops.py — stub only | No content migration needed |
| `coc_bridge.py` | Moved to .claude/scripts/coc_bridge.py | Unique to brain/, REPO_ROOT path depth fixed (parent.parent.parent) |
| `metrics_renderer.py` | Moved to .claude/scripts/metrics_renderer.py | Unique to brain/ |

## nervous-system/hooks/ Decisions

| File | Decision | Rationale |
|------|----------|-----------|
| `forensic_coc.py` | .claude/hooks/ kept | Same commit timestamp (22:13), canonical location |
| `session_stop_hook.py` | .claude/hooks/ kept (newer) | 22:15 vs 22:03 Apr5 |
| `agent_tracker.py` | ns/ version copied to .claude/hooks/ | Mar28 vs Mar18 |
| `notification_handler.py` | .claude/hooks/ kept (identical) | Same MD5 |
| `statusline.py` | ns/ version copied to .claude/hooks/ | ns/ richer (317 vs 222 lines) AND newer (Mar28 vs Mar25) |
| `memory_collector.py` | Copied to .claude/hooks/ | Unique to ns/ (Apr5) |
| `memory_router.py` | Copied to .claude/hooks/ | Unique to ns/ (Apr5) |

## nervous-system/vault-sync/ Decisions

| File | Decision | Rationale |
|------|----------|-----------|
| `note_sign.py` | .claude/scripts/ kept (newer) | 22:15 vs 22:03 Apr5 |
| `vault_annotation_sync.py` | .claude/scripts/ kept (newer) | 22:03 Apr5 vs Mar28 |
| `vault_narrative_sync.py` | .claude/scripts/ kept (richer) | 984 lines vs 351 lines |
| `vault_nectar_atomize.py` | Copied to .claude/scripts/ | Unique to ns/ (Apr5) |

## Reference Updates

| File | Change |
|------|--------|
| .claude/skills/health/SKILL.md | brain/health_check.py -> .claude/scripts/health_check.py |
| .claude/skills/metrics/SKILL.md | brain/metrics_renderer.py -> .claude/scripts/metrics_renderer.py |
| .claude/hooks/settings.json | brain/health_check.py --brief -> .claude/scripts/health_check.py --brief |
| .claude/scripts/blueprint_inject.py | docstring brain/coc_bridge.py -> .claude/scripts/coc_bridge.py |
| .claude/scripts/coc_bridge.py | docstring self-references + REPO_ROOT depth (2->3 levels up) |

## Backward Compatibility

All 8 brain/*.py files now contain thin stubs redirecting to canonical locations:

    # brain/health_check.py - MOVED to .claude/scripts/health_check.py
    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / ".claude" / "scripts"))
    from health_check import *
    if __name__ == "__main__": import runpy; runpy.run_path(...)

queue_ops.py stub redirects to .claude/hooks/state/queue_ops.py.

No stubs created for nervous-system/ because no Python code imports from nervous_system.*.

## Garbage Locations

.claude/garbage/brain/ — All 8 original brain/ scripts before consolidation
.claude/garbage/nervous-system-hooks/ — All 7 ns/hooks/ scripts (superseded or identical)
.claude/garbage/nervous-system-vault-sync/ — All 4 ns/vault-sync/ scripts (superseded or identical)

## Docs Still To Update (not blocking)

docs/CLI-GIT-TRANSITION.md — historical mapping table, intentionally kept as-is
LAYOUT.md — repo layout description, update if repo layout changes

## Verification

    # Confirm no live brain/ references in code (excluding docs and garbage)
    grep -rn "brain/" --include="*.py" --include="*.json" . \
      | grep -v __pycache__ | grep -v .git/ | grep -v .claude/garbage | grep -v "brain/.*\.py:.*brain/"
    # Expected: no output
