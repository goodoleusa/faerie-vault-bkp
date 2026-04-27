---
type: design-narrative
created: 2026-03-28
updated: 2026-03-28
tags:
  - design
  - architecture
  - modularity
  - career
  - piston-model
parent:
  - "[[System-Architecture]]"
sibling:
  - "[[PISTON-MODEL-DESIGN]]"
  - "[[DAE-Evolution-Narrative]]"
memory_lane: honey
promotion_state: crystallized
doc_hash: sha256:f8cd1b460f40abc3263a907eb1464e552db1affc18b1962464ec7795be725389
hash_ts: 2026-03-29T16:16:16Z
hash_method: body-sha256-v1
---

# Modular Secret Sauce Architecture

> **Context:** [[SYSTEM-GUIDE]] for full system map. [[System-Architecture#Modular Secret Sauce Paid Feature Architecture]] for visual diagrams.

## Related Docs

| Topic | Doc | Why it matters here |
|-------|-----|---------------------|
| Piston model (the first sauce module) | [[PISTON-MODEL-DESIGN]] | Deep dive on wave timing — the primary removable module |
| System architecture visuals | [[System-Architecture]] | Mermaid diagrams showing core vs sauce separation |
| DAE evolution | [[DAE-Evolution-Narrative]] | Release path for DAE standalone |
| Pipeline design | [[PIPELINE-DESIGN]] | Which pipeline steps are sauce-enhanced |
| Agent orchestration | [[AGENT-SYSTEM-ARCHITECTURE-ZIMA]] | What employers see (full agent system) |
| Marketing positioning | [[MARKETING-IDEAS]] | How to pitch the open version |
| Equilibrium principle | [[equilibrium]] | Budget system that sauce modules respect |
| Session lifecycle | [[session-lifecycle]] | Where piston hooks into the session |
| Crystallization | [[crystallization]] | Premium crystallization is a future sauce module |

### Sauce-Adjacent System Components

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) AS "Component",
  component_type AS "Type"
FROM "00-SHARED/Hive/pseudosystem"
WHERE contains(["session-lifecycle", "faerie-start", "context-budget", "crystallization", "state-engine", "subagent-spawning", "agent-work", "equilibrium"], file.name)
SORT component_type ASC, file.name ASC
```

---

## Why This Matters

Three things need to happen simultaneously:
1. **Job applications** — show the repo to potential employers. They see a capable system, not your competitive advantage.
2. **Cybertemplate report** — finish and release the investigation product. Needs the full engine.
3. **DAE release** — data-analysis-engine as a standalone tool. Useful without the sauce.

The problem: the best parts of the system (piston engine, surfacing scheduler, crystallization, agent training loop) ARE the competitive advantage. Showing them to employers means giving away the sauce. Not showing anything means no job.

**Solution: modular architecture where proprietary features are separate importable modules that the core gracefully degrades without.**

## The Pattern

```python
# In any consumer (surfacing_scheduler.py, pre_compact_hook.py, etc.)
try:
    from piston import plan, resume, checkpoint, SPEED_TIERS
    _HAS_PISTON = True
except ImportError:
    _HAS_PISTON = False
    # Flat fallback: still works, just not as smart
```

Every proprietary module follows the same contract:
- **`__removable__ = True`** — flag in the module itself, marks it as sauce
- **`try: import` at every consumer** — never crashes if absent
- **Flat fallback in the consumer** — core function still works, just simpler
- **One `rm` to remove** — `rm piston.py` and everything still runs

## What's Proprietary vs Open

| Module | Type | What employer sees | What you keep |
|--------|------|--------------------|---------------|
| `piston.py` | Proprietary | Flat batch launches (all agents at once) | Phased waves with rhythm, checkpoint/resume |
| `surfacing_scheduler.py` | Open (with import) | Basic job classification + flat plan | Piston integration, wave timing |
| `pre_compact_hook.py` | Open (with import) | Steps 1-4 (drain, snapshot, droplets, brief) | Step 5 (piston checkpoint) |
| `crystallize.py` | Open | Basic memory promotion | Advanced integration intelligence |
| `session_metrics.py` | Open | Hash-chained KPIs | Self-calibration closed loop |
| Agent cards | Open (generic) | Standard agent definitions | Training scores, deployment tuning |
| Forensic COC | Open | Full chain of custody | Your investigation-specific data |

## How Removal Works

**Before interview:**
```bash
# From ~/.claude/scripts/
rm piston.py surfacing_scheduler_premium.py overnight_synthesis.py
# That's it. Everything else auto-degrades.
```

**What the employer experiences:**
- Agents launch in flat batches (still works, just all at once instead of waves)
- No checkpoint/resume across auto-compact (session restarts clean)
- No self-calibrating surfacing timing (uses defaults)
- Queue system, memory routing, forensic COC, agent spawning — all fully functional
- They see a sophisticated multi-agent orchestration system. They just don't see the piston rhythm that makes it flow.

**What you keep:**
- The piston model (phased waves creating flow)
- Surfacing forecast (predicting when agent returns cluster)
- Self-calibration loop (system improves itself from session metrics)
- Overnight synthesis (batch Opus for deep cross-cutting analysis)
- Crystallization intelligence (not just compression — integration)

## Implementation Status

| Component | Modularized | Import guard | Fallback tested |
|-----------|-------------|--------------|-----------------|
| `piston.py` | Yes | `surfacing_scheduler.py`, `pre_compact_hook.py` | Yes |
| `overnight_synthesis.py` | Not yet | — | — |
| `crystallize_premium.py` | Not yet | — | — |
| Agent training loop | Inline | Needs extraction | — |

## Design Rules

1. **Never break the consumer.** If `import` fails, the system must still function. No degraded error states — just simpler behavior.
2. **Flag what's removable.** Every sauce module has `__removable__ = True` at the top. A script can find and remove all of them: `grep -rl '__removable__' ~/.claude/scripts/`.
3. **Keep the interface stable.** `plan()`, `resume()`, `checkpoint()`, `classify()` — these function signatures don't change. The consumer doesn't care whether it's calling piston.py or a flat fallback.
4. **Don't over-modularize.** If something isn't competitive advantage, don't extract it. The point is surgical removal of sauce, not a plugin architecture. Three similar lines are better than a premature abstraction.
5. **The employer gets something USEFUL.** Not a broken shell. Not a demo mode. A real multi-agent orchestration system that does real work — just without the secret rhythm.

## Path Forward

- **Week of 2026-03-28:** piston.py complete, wired into surfacing_scheduler + pre_compact_hook
- **Next:** Extract overnight_synthesis, crystallize_premium, agent training scorer
- **Before applying:** Run `grep -rl '__removable__' ~/.claude/scripts/ | xargs rm`, verify all tests pass, push clean branch
- **For the interview:** "Here's my multi-agent orchestration system. It manages 20+ specialized agents, has hash-chained forensic provenance, self-calibrating launch timing, and a memory architecture that survives context compaction." That's already impressive. The piston rhythm is what makes it *magic* — and that stays with you.
