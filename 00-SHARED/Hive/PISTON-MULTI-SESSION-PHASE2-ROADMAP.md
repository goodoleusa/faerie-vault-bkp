---
title: Phase 2 Roadmap — Piston Orchestrator Implementation
status: pre-implementation
created: 2026-03-30T01:10:00Z
branch: piston-multi-session
---

# Phase 2: Piston Fork Implementation

**Dependency:** Phase 1 (Design Review) complete + user approval + answers to 4 clarification questions

## Files Prepared on Branch

- `~/.claude/scripts/piston_orchestrator.py` — Main piston fork logic (skeleton, 380L)
- `~/.claude/scripts/piston_eval_multi_session.py` — Eval instrumentation (skeleton, 250L)
- `~/.claude/hooks/state/piston-config.json` — Session affinity configuration (template)
- `~/.claude/docs/PISTON-MULTI-SESSION-DESIGN.md` — Full design specification

## Remaining Phase 2 Work

### 1. Expand piston_orchestrator.py
- [x] Session discovery via heartbeat.py
- [x] Affinity-weighted lottery claiming
- [x] **Multi-instance spawning** (added: spawn 2nd+ agent if queue_remaining > 10)
- [x] **Context locality scaffolding** (added: comment markers for task clustering logic)
- [ ] **Integrate with Agent tool spawning** (currently stubbed as "would launch")
  - Receive parent context (queue, sprint ID)
  - For each claimed task, construct Agent tool call
  - Track agent returns non-blocking
  - **Context clustering:** Tasks with shared target context → same agent instance (reuse loaded context)
  - **Multi-copy strategy:** 3 data-engineers + 1 evidence-analyst if data-eng queue is heavy (not forced diversity)
- [ ] **Implement surfacing-plan writing** (currently stubbed)
  - Write plan.json after claiming
  - Read peer plans for coordination visibility
  - Include instance count per type (e.g., "2× data-engineer spawned this wave")
- [ ] **Add backoff/retry logic**
  - If queue claims return empty: check peer plans, adjust affinity dynamically
  - If context heavy: skip deep agents, still claim fast agents
  - If queue heavy for specific type: spawn more instances of that type
- [ ] **Graceful shutdown**
  - Write final state to disk
  - Update benchmarks with session stats
  - Delete old surfacing-plan files (cleanup)

### 2. Expand piston_eval_multi_session.py
- [x] Per-session metrics computation
- [x] Cross-session metrics aggregation
- [ ] **Dashboard generation** (currently basic JSON output)
  - CLI table format (friendly output)
  - JSON dashboard file (piston-multi-session-eval.json)
- [ ] **Correlation analysis**
  - Session independence score (measure divergence in agent focus)
  - Type distribution heatmap (which sessions claim what)
- [ ] **Beat-last verification**
  - Compare scores vs baseline (OSINT-BREADCRUMB-001 score: 0.92)
  - Flag if agent scores degrade
- [ ] **Merge gate logic**
  - Compute pass/fail based on success criteria
  - Write recommendation to eval JSON
  - Log decision to bench-decision.jsonl (forensic)

### 3. Integrate with surfacing_scheduler.py
- [ ] **Call piston_orchestrator.py** instead of (or in addition to) current piston
  - Add --multi-session flag to enable
  - Pass session_id from context
  - Pass affinity config path
- [ ] **Fallback to single-session piston** if only one session active
  - Check heartbeat: if only self, skip multi-session coordination
- [ ] **Update calibration feedback loop**
  - Read piston-multi-session-eval.json
  - Adjust affinity weights based on success metrics
  - Write to surfacing-calibration.json

### 4. Task States & Forensic Logging
- [ ] **task-states/{task_id}-piston.json** — Per-task piston state
  - session_id that claimed it
  - wave_num when claimed
  - affinity_match (was this session's preferred type?)
  - claim_result (success, collision, timeout)
- [ ] **piston-coc.jsonl** — Hash-chained orchestrator decisions
  - Every claim attempt (success/fail, session, affinity, result)
  - Wave transitions
  - Peer session presence signals
  - Forensic integrity for court audit

### 5. Testing & Validation
- [ ] **Mock multi-session test** (2 fake sessions)
  - Spawn both, verify soft affinity claims work
  - Verify no duplicate claims (collision detection)
  - Verify surfacing-plan files written correctly
- [ ] **Real eval run** (8-12 hour window as per design)
  - Run 2+ actual sessions
  - Measure metrics
  - Compare improvement_pct vs baseline
  - Check collision_rate < 5%
- [ ] **Recovery test** (crash resilience)
  - Kill one session mid-wave
  - Verify other session continues
  - Verify downed session can resume from checkpoint

## Timeline (Estimate)

- **Phase 2a (expand skeletons):** 2-3 agent turns
- **Phase 2b (surfacing_scheduler integration):** 1-2 agent turns
- **Phase 2c (forensic logging + testing):** 1-2 agent turns
- **Phase 3 (eval instrumentation refinement):** 1 agent turn
- **Phase 4 (integration testing):** 1 agent turn
- **Phase 5 (8-12h eval run + merge decision):** Scheduled eval window

**Total:** ~5-7 agent turns + overnight eval run

## Branch Operations

**Current state:** `piston-multi-session` branch from `main`

**Merge gate (Phase 5):**
```bash
# If eval passes (>10% improvement, <5% collisions, scores OK):
git checkout main
git pull origin main
git merge --no-ff piston-multi-session -m "merge: multi-session piston orchestration

- Type-based soft affinity task claiming
- Heartbeat-based session discovery
- Stigmergy coordination via surfacing-plan files
- >10% throughput improvement, <5% collisions
- Hash-chained forensic logging

Eval: {improvement_pct}% improvement, {collision_rate}% collisions, {score_avg} avg score"
git push origin main
```

**If eval fails:** Keep branch, iterate on affinity model, re-run eval. OR revert:
```bash
git reset --hard main  # lose branch changes, back to main
git branch -D piston-multi-session
git push origin --delete piston-multi-session
```

## Open Questions for User

These must be answered before Phase 2 begins:

1. **Affinity threshold:** Current design uses 0.5 (skip claiming if affinity < 0.5).
   - Keep 0.5? Or lower (0.3)? Or higher (0.7)?
   - Trade-off: lower = more eager claiming but risk wrong-type work; higher = more focused but queuing risk

2. **Claiming strategy:** Current design uses affinity-weighted lottery.
   - Keep lottery (probabilistic)? Or explicit fair-share (40% A / 40% B / 20% evergreen)?
   - Trade-off: lottery = simpler, natural variation; fair-share = predictable, harder to tune

3. **Eval window duration:** Design suggests 8-12 hours.
   - Agree? Or shorter (4-6h)? Or longer (24h)?
   - Longer = more stable statistics; shorter = faster feedback

4. **Fast-lane behavior:** Currently data-analyst, evidence-curator are always-available (no affinity check).
   - Keep? Or also respect affinity (prefer but don't skip)?
   - Trade-off: always-available = momentum, utilization; respect-affinity = type-focus

---

**Next Step:** User reviews PISTON-MULTI-SESSION-DESIGN.md, answers 4 questions. Then Phase 2 implementation begins on this branch.
