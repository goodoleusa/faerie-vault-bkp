# /spawn System Update — 2026-04-28

**Status:** Ready & Shippable | faerie2 pushed | synced to both vaults

## Summary

Fixed broken /spawn skill:
- **Problem:** run.py + executor.py split → 0 agents spawned
- **Solution:** Consolidated to single run.py → outputs Agent() directives
- **Result:** 4 agents spawn W1 LIFTOFF inline (verified smoke test)

## Key Changes

1. **W1 LIFTOFF Default** — `/spawn` always defaults to max velocity (unless --wave 2 or 3)
2. **Removed executor.py** — redundant, caused confusion
3. **Bundle Context** — HONEY (200t) + NECTAR (1.2K) + template injected
4. **Formulas Updated** — quality gates recalibrated on N=52 measurement
5. **COC + B2 Wiring** — programmatic, immutable, real-time backup

## Files

- run.py: `/mnt/d/0LOCAL/.claude/skills/spawn/`
- Formulas: `/mnt/d/0LOCAL/.claude/faerie2-formulas.json`
- Hooks: `/mnt/d/0LOCAL/.claude/hooks/presend-forensic-coc-b2-stream.sh`
- Pushed to faerie2 main branch

## Measurement

| Before | After |
|--------|-------|
| 0 agents/spawn | 4 agents/spawn |
| 2 confusing scripts | 1 clear script |
| context-gated (conservative) | user-controlled (W1 default) |

---

Synced to:
- CT_VAULT: `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Hive/0dotclaude/2026-04-28/`
- FAERIE_VAULT: `/mnt/d/0local/gitrepos/faerie-vault/0dotclaude/2026-04-28/`
