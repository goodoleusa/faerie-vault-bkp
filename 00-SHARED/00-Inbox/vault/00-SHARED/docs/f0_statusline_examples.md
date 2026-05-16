# f(0) Statusline — Live Examples

Real-time f(0) metrics footer as it evolves through a session. Each line shows what the statusline displays at that point in the piston cycle.

## Example Session Progression

### T1: Cold Start (Spawn Turn)
```
[🚀 T1 | 🔴 stamping:21 | W0/7✓ | Q:0.88 | $0.00 | latency:2.1s | cache:0% ✗ | ctx:26K | headroom:200K]
```
**What it means:** 
- 🚀 Spawn turn — time to launch all Wave 1 specialists
- 🔴 stamping:21 — CRITICAL: 21 vault docs need SHA-256 stamps (fix now before agents run)
- W0/7✓ — 0 agent returns yet; target is 7 cycles per session
- Q:0.88 — quality baseline (from f(0) performance report)
- cache:0% — no cache activity yet (normal at T1)
- headroom:200K — full context available

### T2: Agents Launching (Orbit)
```
[⚡ T2 | ⚡ 3 running | W0/7✓ | Q:0.88 | $0.00 | latency:2.1s | cache:12% ✗ | ctx:35K | headroom:185K]
```
**What it means:**
- ⚡ Orbit — agents are running
- ⚡ 3 running — status changed from alert to progress indicator
- Queue stamping alert suppressed (monitoring ongoing, not actionable yet)
- cache:12% — cache starting to populate from stable context blocks

### T3–5: Agents Working (Deep Orbit)
```
[⚡ T4 | ⚡ 2 running | W0/7✓ | Q:0.88 | $0.02 | latency:2.1s | cache:45% ✓ | ctx:62K | headroom:155K]
```
**What it means:**
- 2 agents still running (1 finished)
- Cost starting to accumulate ($0.02)
- cache:45% — approaching 50% utilization (watch for underutilization)
- ctx:62K — context growing as agents work

### T6: First Agent Returns (Transition)
```
[⚡ T6 | 📦 W1/7✓ | Q:0.89 | $0.03 | latency:2.1s | cache:62% ✓ | ctx:74K | headroom:133K]
```
**What it means:**
- 📦 Consolidate phase — first agent returned
- W1/7✓ — 1 successful return (1/7 of target cycles)
- Quality improved slightly (0.88 → 0.89) from agent insights
- cache:62% — healthy cache utilization (>50%)
- Alert cleared (stamping still pending, but now monitoring background process)

### T8–10: Multiple Returns (Consolidation)
```
[📦 T9 | 📦 W4/7✓ | Q:0.88 | $0.12 | latency:2.3s | cache:71% ✓ | ctx:99K | headroom:85K]
```
**What it means:**
- W4/7✓ — 4 agent returns (halfway to 7-cycle target)
- Quality averaged across 4 returns (some high, some standard)
- Cost accumulating ($0.12 total)
- ctx:99K — approaching commit window (85% = 170K)

### T11–13: Commit Window (High Alert)
```
[⚠️ T11 | ⚠️ COMMIT+PUSH | W5/7✓ | Q:0.88 | $0.15 | latency:2.2s | cache:73% ✓ | ctx:170K | ⚠️ COMMIT NOW]
```
**What it means:**
- ⚠️ Commit window — context at 85% threshold
- ⚠️ COMMIT+PUSH — output write time, don't spawn new agents
- W5/7✓ — 5 cycles completed (approaching target)
- ctx:170K — at 85% of 200K budget
- headroom shows as "COMMIT NOW" instead of K value

### T14: Auto-Compact Signal
```
[🔴 T14 | 🔴 COMMIT NOW | W6/7✓ | Q:0.88 | $0.18 | latency:2.1s | cache:74% ✓ | ctx:190K | critical]
```
**What it means:**
- 🔴 AUTO-COMPACT IMMINENT — context <10% remaining
- 🔴 COMMIT NOW — final outputs MUST be written before auto-compact fires
- W6/7✓ — 6 cycles, very close to target
- ctx:190K — 95% of 200K used
- Continue working — auto-compact handles compaction automatically

---

## Alert Priority (What Fixes Now vs Monitor)

### 🔴 CRITICAL Alerts — Fix Immediately
- `stamping:N` — N vault documents pending SHA-256 stamps
  - **Action:** Run batch stamping script or add PostToolUse hook
- `manifest:N` — N agent manifest write failures
  - **Action:** Check sandbox permissions, diagnose Write tool issue
- `CONTEXT CRITICAL` or `COMMIT NOW` — <10% headroom
  - **Action:** Commit all outputs NOW, don't spawn new work

### ⚠️ HIGH Alerts — Address Within Current Wave
- `queue:N>48h` — N REVIEW-QUEUE items >48h old
  - **Action:** Human reviews items, marks decisions, memory-keeper applies
- `chain:M%` — COC hash-chain coverage dropped
  - **Action:** Identify which COC file broke, re-chain entries
- `wave:stall` — Agents running >5 minutes with no returns
  - **Action:** Check manifest, diagnose blocking, timeout if dead
- `COMMIT+PUSH` — Context at 85%
  - **Action:** Finish current atomic unit, commit outputs

### 🔶 MED Alerts — Monitor, Plan Fix
- `cache:N%` — Cache hit rate <50%
  - **Action:** Group related context, improve stable-content layout
- `quality:regress` — Quality score dropped >5%
  - **Action:** Review recent agent card, check for degradation

---

## f(0) Cycle Target

Session goal: **7–10 successful agent cycles per session**

- Each cycle = 1 agent return (Wave 1 triage, Wave 2 research, Wave 3 synthesis)
- Statusline shows `W{N}/7✓` where N = cycles completed
- Success threshold: N ≥ 7 by end of session
- Stretch target: N ≥ 10 (requires careful wave coordination + early commits)

---

## Reading the Statusline at a Glance

| Part | Meaning | Watch For |
|------|---------|-----------|
| `🚀/⚡/📦/⚠️` Stage | Session phase (spawn→orbit→consolidate→commit) | Alert emoji override (🔴 highest) |
| `T{N}` | Current turn number | T≥2 and no agents = 🔴 SPAWN NOW |
| Alert (right after stage) | Highest-priority action needed | None = "✓ nominal"; multiple = pick highest |
| `W{N}/7✓` | Cycles completed / target | <3 by T8 = slow progress; ≥7 by T14 = success |
| `Q:0.XX` | Quality score (0–1) | <0.70 = investigate agent card; >0.90 = excellent |
| `$X.XX` | Cost per session | Target: ≤$0.30/analysis |
| `cache:NN% ✓/✗` | Cache hit rate | ✗ = <50%, try grouping context; ✓ = >50%, stable |
| `ctx:NNK` | Current context estimate | >170K = commit window; >190K = critical |
| `headroom:NNK` | Available context before auto-compact | <50K = plan final commits |

---

## Debugging via Statusline

**Symptom: Cycles stalled (W2/7 at T10)**
- Check: Are agents in REVIEW-QUEUE or blocked on human decisions?
- Check: Did manifest writes fail? (would show 🔴 manifest:N)
- Action: Send diagnostic message to running agents; check REVIEW-QUEUE for stale items

**Symptom: Cache:0% (all misses, no reuse)**
- Check: Are stable context blocks loaded (ARCHITECTURE.md, KNOWLEDGE-BASE)?
- Action: Add `cache_control: ephemeral` to system blocks; group related context

**Symptom: stamping:N alert stuck**
- Check: Are those files actually writable? Can 5x_stamp_doc_hash.py reach them?
- Check: Do they have proper YAML frontmatter? (missing doc_hash field = not stampable)
- Action: Run script manually on subset; add debugging; might need PostToolUse hook

**Symptom: Quality dropped (Q:0.94 → Q:0.78)**
- Check: Did new agent card cause over-specialization?
- Check: Is agent targeting wrong domain?
- Action: Review agent Last Training section; check if recent eval beat baseline

---

Generated by: f0_statusline_renderer.py (7x_ orchestration layer)
Location: /mnt/d/0local/gitrepos/faerie2/scripts/7x_f0_statusline_renderer.py
