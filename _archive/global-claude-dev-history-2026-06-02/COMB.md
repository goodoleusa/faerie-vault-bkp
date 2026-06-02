# HONEY-DISCIPLINE.md — Immutable F(0) Orchestration Doctrine

> Discipline is infrastructure, not willpower.
> This section is read by main every turn and never changes.

**This is the part that main reads to know their role in f(0). It is immutable across sessions.**

---

## THE CORE DECISION (Read This Every Turn)

```
Identify: How many distinct >100-token tasks exist?

COUNT TASKS
  ├─ <2 tasks? → INLINE (spawn not cost-effective)
  └─ ≥2 tasks? → proceed

MISSION AVAILABLE?
  ├─ No mission → auto-generate: "spawn-YYYY-MM-DD-HH-hash"
  └─ Mission known? → proceed

BUNDLE CONTEXT READY?
  ├─ No HONEY/manifests → gather (~2K tokens), then spawn
  └─ Bundle ready? → SPAWN VIA spawn.py NOW

SEMANTIC TRUTH: If tasks ≥2, mission exists, bundle ready → SPAWN is the default.
Math: ~50 tokens spawn + ~80 char return < 100+ tokens inline work.
```

---

## F(0) Math (Why SPAWN Wins)

| Scenario | Main Cost | Benefit | Verdict |
|----------|-----------|---------|---------|
| 2+ tasks, >100 tokens each | ~130 (spawn + return) | agents work in parallel + deep synthesis | SPAWN wins |
| 1 task, <100 tokens | >100 (inline) | local work | INLINE OK |
| 2+ tasks, mission unknown | gather mission (10 tok) + spawn | agents + quality | SPAWN after gather |
| 2+ tasks, agents running | wait for manifest return | agents don't block each other | WAIT (don't search) |

**Decision rule:** Context > 200K? Compress before spawn. Context 50-200K? Spawn W1/W2. Context <50K? W3 background only.

---

## Anti-Patterns (NEVER)

- ❌ "Let me read the file first" → SPAWN WHILE READING (agents work in parallel)
- ❌ "I'll bash-check if agents finished" → WAIT FOR MANIFEST (async protocol)
- ❌ "Maybe this is too small" → If >100 tokens, spawn is justified (math)
- ❌ "I'll search forensics/ for manifests" → Manifest paths are deterministic (no discovery)

---

## Enforcement

**Presend Hook (presend_estimate.py):**
- Scans prompt for anti-f(0) patterns (grep, cat, bash, inline reads)
- Detects SPAWN DECISION violations: "≥2 tasks + mission known + bundle ready BUT prompt contains inline ops"
- Outputs: 🔴 SPAWN DECISION VIOLATION (non-ignorable red flag)

**Manifest Validator (8x_manifest_mission_validator.py):**
- Rejects manifests without `mission` field (REQUIRED)
- Rejects manifests without `dashboard_line` (≤80 chars)
- Rejects manifests without `next_mission_node` bearing (N/S/E/W)

**Statusline Signal:**
- 🟢 LIFTOFF READY when spawn conditions met
- ⚪ WAITING when bundle not ready

---

## Session Phases

**Turn 1 (Cold Start):**
- Read CLAUDE.md (global) + CLAUDE.md (project) + HONEY-DISCIPLINE (this file)
- Identify missions from briefing or prompt
- Count independent tasks
- Spawn W1 (6 agents max) if tasks ≥2 and mission known

**Turns 2-N (Autonomous Dispatch):**
- Spawn W1/W2/W3 autonomously based on context fill (piston thresholds)
- No user prompt needed for spawning; it's the default
- Wait for manifest returns; do not poll agents

**Context Burn:**
- W1 GREEN (≤25%): 6 agents, hit 5-min cache TTL
- W2 ORANGE (25-65%): 4 agents, autonomous dispatch
- W3 RED (65-95%): 1 background agent, deep synthesis
- >95%: Compact before next spawn

---

**Last Updated:** 2026-04-30  
**Status:** Immutable — do not change without user approval  
**Enforcement:** Presend hooks + manifest validators + statusline signals
