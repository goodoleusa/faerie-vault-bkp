---
title: Multi-Session Piston Design
status: design-review
created: 2026-03-30T01:10:00Z
branch: piston-multi-session
---

# Multi-Session Piston Orchestration

## Problem
Current piston model (fast/medium/deep waves) optimizes for **one extended session**. When two legitimate Claude users work on the same queue (sharing OUTPUTS, not API credits), they:
- Both read the queue simultaneously
- Both launch the same agent types
- No coordination — risk of thrashing, duplicate work

## Solution: Type-Based Soft Affinity Piston

Each session runs its own piston fork with **soft affinity** for agent types. Sessions coordinate via:
- Heartbeat.py (session presence signal)
- Surfacing-plan-*.json (wave timing + type allocation)
- Run-benchmarks.json (cross-session performance trend)

---

## Architecture

### Type Affinity Model (Soft)

**Session declares preferred agent types** (based on its investigation focus):

```json
{
  "session_id": "sess-AAA",
  "piston_affinity": {
    "data-engineer": 0.9,      // highly prefer
    "evidence-analyst": 0.8,   // prefer
    "research-analyst": 0.5,   // willing
    "performance-eval": 0.1,   // evergreen (low affinity, always available)
    "membot": 0.0              // shared (both sessions use)
  }
}
```

**Queue claims respect affinity but don't block:**
1. Session A reads queue: 5 data-engineer tasks queued
2. Session A claims 3 (affinity 0.9, matches its focus)
3. Session B reads same queue: 2 data-engineer tasks remain
4. Session B claims them anyway (soft affinity, don't stall)
5. If Session B finishes data-eng work and queue has analysis tasks, it pivots to those (soft affinity lets drift)

### Wave Distribution (Soft Affinity + Context Locality)

**Fast agents (evergreen):**
- data-analyst, evidence-curator, memory-keeper, membot — all sessions can claim
- Claim logic: first-come-first-served, no affinity check (too transient)

**Medium agents (specialized):**
- data-engineer, research-analyst, evidence-analyst
- Claim logic: affinity-weighted lottery WITH context clustering
  - Session A (data-engineer affinity 0.9): 90% chance to claim data-engineer tasks
  - Session B (evidence-analyst affinity 0.8): 80% chance to claim analysis tasks
  - **Context locality:** If Session A just processed targets [1.2.3.4, 5.6.7.8], and queue has follow-up DNS tasks on same IPs, keep them in Session A to leverage loaded context
  - **Multi-instance spawning:** If data-engineer queue > 10 items, spawn 2-3 parallel data-engineers instead of forcing diversity. Natural allocation > artificial constraints
  - But if Session B finishes its medium work and queue is full of data-engineer tasks, it can claim them

**Deep agents (synthesis):**
- performance-eval, knowledge-synthesizer
- Claim logic: only when context budget heavy (>70% used) or human explicitly queues
- Share fairly across sessions (alternating priority)

**Key principle:** Diversity is good, but don't force it. Let queue load + affinity + context locality drive allocation. If the best plan is "3× data-engineer + 1× evidence-analyst", spawn it.

### Piston Fork Behavior (Per-Session)

Each session's piston runs this loop:

```python
# ~/.claude/scripts/piston_orchestrator.py --session $SESSION_ID

def orchestrate():
    # Discover active sessions
    active = read_heartbeat()  # [sess-AAA, sess-BBB]
    my_plan = load_affinity()  # my type preferences

    # Claim next tasks respecting soft affinity
    for agent_type in ["data-engineer", "research-analyst", "evidence-analyst"]:
        if affinity[agent_type] > 0.5:  # only try if I care about this type
            # Claim with affinity-weighted probability
            if random.random() < affinity[agent_type]:
                tasks = queue_ops.claim(category=agent_type, max=3)
                if tasks:
                    launch_wave(tasks, agent_type)

    # Write my wave plan for other sessions to read
    write_surfacing_plan({
        "session_id": SESSION_ID,
        "wave_num": wave_count,
        "types_launching": [agent_types],
        "ts": now()
    })

    # Process returns as they arrive (non-blocking)
    for agent_return in poll_returns(timeout=1.0):
        stream_finding(agent_return)
        update_benchmarks(agent_return)

    # Check if queue is empty or my context is heavy
    if queue_empty() or context_heavy():
        return
    else:
        sleep(0.5)  # backoff to avoid busy-wait
        orchestrate()  # loop
```

### Shared Memory (Append-Only + Hash-Chained)

**NECTAR.md, streams, checkpoints:**
- All append-only (no overwrites)
- Hash-chained entries (session-A and session-B can append concurrently without collision)
- Each entry tagged with `session_id` field

**Example NECTAR entry (both sessions append to same file):**
```
<!-- MEM agent=data-engineer session=sess-AAA ts=2026-03-30T01:05:00Z cat=OSINT_FINDING av=1.0 -->
**[OSINT_FINDING]** example.com — 10 DNS records, 4 IPs
Evidence: IPs=[1.2.3.4, ...] | Source: task-20260330-003954-f760
<!-- /MEM -->

<!-- MEM agent=evidence-analyst session=sess-BBB ts=2026-03-30T01:06:00Z cat=EVIDENCE_GAP av=1.0 -->
**[EVIDENCE_GAP]** Treasury data missing from 2024-Q2 LDAP snapshot
Implication: insider access window unverified | Next: retry LDAP sync
<!-- /MEM -->
```

---

## Eval Instrumentation

### Metrics (Per-Session + Cross-Session)

**Per-session KPIs:**
| Metric | Definition | Baseline |
|--------|-----------|----------|
| `throughput_tasks/min` | Queue tasks claimed per minute | 0.8 (single-session baseline) |
| `context_used_k/min` | Context tokens consumed per minute | 42K/min (OSINT pipeline) |
| `score_avg` | Agent score average (weighted by task count) | 0.92 (prior single-session) |
| `affinity_match_pct` | % of claimed tasks matching declared affinity | N/A (new metric) |

**Cross-session KPIs:**
| Metric | Definition | Success Criteria |
|--------|-----------|-----------------|
| `combined_throughput_tasks/min` | Sum across all active sessions | ≥1.2× single-session (0.96 instead of 0.8) |
| `collision_rate` | % of duplicate task claims (failed claims) | <5% (soft affinity allows some spillover) |
| `session_independence` | Score correlation between sessions | <0.7 (different types, independent performance) |
| `shared_memory_conflicts` | Hash-chain breaks or lost writes | 0 (append-only safety) |

### Dashboard (dev eval tool)

**File:** `~/.claude/hooks/state/piston-multi-session-eval.json`

```json
{
  "eval_window": "2026-03-30T00:00:00Z / 2026-03-30T23:59:59Z",
  "sessions": {
    "sess-AAA": {
      "focus": "data-engineering",
      "throughput_tasks_per_min": 1.1,
      "context_k_per_min": 45,
      "score_avg": 0.95,
      "affinity_match_pct": 0.82,
      "tasks_claimed": 12,
      "tasks_completed": 11
    },
    "sess-BBB": {
      "focus": "analysis",
      "throughput_tasks_per_min": 0.9,
      "context_k_per_min": 38,
      "score_avg": 0.90,
      "affinity_match_pct": 0.75,
      "tasks_claimed": 8,
      "tasks_completed": 7
    }
  },
  "cross_session": {
    "combined_throughput": 2.0,
    "baseline_expected": 1.6,
    "improvement_pct": "+25%",
    "collision_rate": 0.02,
    "shared_memory_ok": true,
    "recommendation": "PASS — multi-session piston shows 25% throughput gain vs single-session baseline"
  }
}
```

### Eval Script

**File:** `~/.claude/scripts/piston_eval_multi_session.py`

```python
def eval_multi_session():
    """Compare single-session vs multi-session performance over eval window."""

    # Load run-benchmarks from window
    benchmarks = read_benchmarks(start=EVAL_START, end=EVAL_END)

    # Segment by session_id
    by_session = {s: [b for b in benchmarks if b["session_id"] == s]
                  for s in set(b["session_id"] for b in benchmarks)}

    # Compute per-session metrics
    for session_id, session_benchmarks in by_session.items():
        throughput = len(session_benchmarks) / elapsed_minutes
        score_avg = mean([b["score"] for b in session_benchmarks])
        affinity_match = sum(1 for b in session_benchmarks if b["affinity_match"])
        affinity_match_pct = affinity_match / len(session_benchmarks)
        # ... more metrics

    # Compute cross-session metrics
    combined_throughput = sum(s["throughput"] for s in by_session.values())
    collision_rate = sum(1 for b in benchmarks if b["claim_result"] == "collision") / len(benchmarks)

    # Compare vs baseline (single-session)
    baseline_throughput = 0.8  # tasks/min from OSINT-BREADCRUMB-001
    improvement_pct = (combined_throughput - baseline_throughput) / baseline_throughput

    # Write eval report
    write_report({
        "sessions": by_session,
        "cross_session": {
            "combined_throughput": combined_throughput,
            "baseline_expected": baseline_throughput,
            "improvement_pct": improvement_pct,
            "collision_rate": collision_rate,
            "recommendation": "PASS" if improvement_pct > 0.1 else "INVESTIGATE"
        }
    })

    return improvement_pct > 0.1  # pass if >10% improvement
```

---

## Git Branch Strategy

### Branch: `piston-multi-session`

**Purpose:** Isolated implementation of multi-session piston. Can be reverted if needed.

**Branching point:** From `main`, after OSINT-BREADCRUMB-001 lands.

```bash
git checkout main
git pull origin main
git checkout -b piston-multi-session
```

**Commits on branch:**
1. `piston_orchestrator.py` (main piston fork logic, feature-flagged to start)
2. `piston_eval_multi_session.py` (eval instrumentation)
3. `.claude/docs/PISTON-MULTI-SESSION-DESIGN.md` (this design doc)
4. Update `surfacing_scheduler.py` to call piston_orchestrator with multi-session params
5. Update `.claude/hooks/state/piston-config.json` with affinity definitions

**Rollback procedure:**
```bash
git log --oneline piston-multi-session | head -10
# Pick the commit before multi-session changes
git revert <commit>  # or git reset --hard <commit> if it's only on this branch
```

Or, if implementation is unwanted:
```bash
git branch -D piston-multi-session  # delete branch locally
git push origin --delete piston-multi-session  # delete on remote
# main is unaffected
```

### Success Gate Before Merge

**Merge to main only if:**
1. ✅ Eval instrumentation shows >10% combined throughput improvement
2. ✅ Collision rate <5%
3. ✅ Hash-chained NECTAR has 0 conflicts across 3+ concurrent sessions
4. ✅ Agent scores don't degrade (affinity-match doesn't hurt performance)
5. ✅ Rollback procedure tested (can cleanly revert without losing work)

---

## Implementation Phases

### Phase 1: Design Review (This Doc)
- [ ] User approves type-based soft affinity model
- [ ] User approves eval metrics
- [ ] User approves git branch strategy

### Phase 2: Piston Fork Implementation (branch: piston-multi-session)
- [ ] `piston_orchestrator.py` (orchestrate function, affinity logic, claim loop)
- [ ] Soft affinity lottery in claim logic
- [ ] Heartbeat reading (discover active sessions)
- [ ] Surfacing-plan writing (broadcast my wave plan)

### Phase 3: Eval Instrumentation
- [ ] `piston_eval_multi_session.py` (metrics computation, report writing)
- [ ] Dashboard generation (`piston-multi-session-eval.json`)
- [ ] Merge eval results into `run-benchmarks.json` with session_id tag

### Phase 4: Integration + Testing
- [ ] Integrate with `surfacing_scheduler.py` (call piston_orchestrator)
- [ ] Spawn two mock sessions, verify soft affinity claims work
- [ ] Test rollback: revert branch, verify main is clean

### Phase 5: Threshold Gate + Merge Decision
- [ ] Run eval over 8-12 hour window (multiple sessions)
- [ ] Compute improvement_pct
- [ ] If pass: merge to main with merge commit message explaining trade-offs
- [ ] If fail: document findings, optionally iterate on affinity model

---

## Success Criteria

**Minimum viable** (proceed to merge):
- Combined throughput ≥1.2× single-session baseline (1.2 × 0.8 = 0.96 tasks/min)
- Collision rate <5%
- Score avg ≥0.90 (don't hurt agent performance)

**Nice-to-have**:
- Affinity-match >70% (sessions claim their preferred types most of the time)
- Session independence score <0.7 (different sessions, different distributions)

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Concurrent writes corrupt NECTAR | Hash-chained append-only + shutil.move atomicity |
| Sessions thrash on same tasks | Soft affinity lottery + collision detection |
| Affinity model is too strict | Soft (prefer, don't block) — sessions can drift |
| Rollback is messy | Git branch isolated; can revert cleanly to main |
| Eval metrics are wrong | Eval designed upfront, testable before implementation |
| One session hogs queue | Affinity-weighted lottery, not greedy; backoff in orchestrate loop |

---

## Questions for User

1. **Type affinity thresholds:** Should session skip claiming if affinity < 0.5? Or lower threshold (0.3)?
2. **Lottery vs fair-share:** Affinity-weighted lottery (current design) or explicit fair-share (Session A gets 40%, Session B gets 40%, evergreen gets 20%)?
3. **Eval window duration:** How long should the evaluation run before deciding to merge? (Suggested: 8-12 hours, ~50-100 tasks per session)
4. **Fast-lane agents:** Should data-analyst, evidence-curator be claimed first (no affinity check), or should they also respect affinity?

---

## References

- `BREADCRUMB-SYSTEM-COMPLETE.md` — Checkpoint mechanism (reused for multi-session sync)
- `surfacing_scheduler.py` — Current piston (to be extended)
- `heartbeat.py` — Session discovery
- `run-benchmarks.json` — Shared performance baseline
- `rules/core.md` — Equilibrium + rollback guardrails
