# Evaluation & Learning — Self-Improving Agent System

This document describes how faerie agents improve continuously through real work, structured training, and lightweight reflection. It covers three improvement paths (on-the-job learning, autotune, mini-learning), the performance dimensions that matter, and the commands used to measure and drive improvement.

## The Self-Improving Loop

Every agent session produces two artifacts:
1. **Output** — the work the agent did (manifest, findings, etc.)
2. **Performance data** — how well the agent did it (KPI scores, calibration metrics)

The loop:

```
AGENT COMPLETES WORK (task output + manifest)
  ↓
PERFORMANCE EVALUATION (6 dimensions scored)
  ├→ Beat last score? → Update agent card + log improvement
  └→ Didn't beat? → Queue for training, set on_the_job_eligible
       ↓
       Later beats target during live work?
       ├→ Yes → REDEMPTION (more valuable than scheduled training)
       └→ No → Explicit training session via /train --run
            ↓
            Self-update agent card + log learning
```

**Key insight:** On-the-job (OTJ) learning during real deployment beats autotune (structured drills) because it proves the improvement works in production conditions.

## Performance Dimensions (6D Model)

Every agent is scored across six independent dimensions. Each has a target (baseline or KPI). Score range: 0.0–1.0 per dimension. Composite target: ≥0.75.

| Dimension | Code | What it measures | Target | Failure looks like |
|---|---|---|---|---|
| **Throughput** | T | Tasks completed per 200K context budget | 0.85 | Agent uses 150K+ context for simple task; spawning delayed |
| **Memory** | M | HONEY.md budget health, scratch promotion rate | 0.80 | Over-budget HONEY.md blocks crystallization; findings lost from NECTAR |
| **Resilience** | R | Recovery from agent failures, retry success rate | 0.90 | Task fails; retry fails again; no handoff to next agent |
| **Quality** | Q | Output quality vs KPI targets per agent type | Agent-specific | Research has 15+ sources but only 3 novel; findings not actionable |
| **Piston** | P | Wave structure health — W1/W2/W3 fire in sequence | 0.85 | Agents stall between waves; spawn-first rule not followed |
| **Model routing** | F | Haiku/Sonnet/Opus used appropriately (cost efficiency) | 0.80 | Haiku routed to complex research; Opus used for triage; cost 4× over budget |

**Composite score** = floor(mean of T, M, R, Q, P, F). Below 0.7 triggers review.

## Agent Self-Update Protocol (Beat-Last-Score)

When an agent completes work and **beats its last score** on the primary KPI:

### Steps

1. **Read your agent card** (`~/.claude/agents/{your-type}.md`)
2. **Find the "## Last Training" section** (create if missing)
3. **Append what you learned** (max 5 bullets):
   - Specific technique that improved output
   - Constraint that worked (e.g., "cite max 3 sources → higher precision")
   - Failure mode you avoided that hurt last time
4. **Update the date** to today's date
5. **Keep it durable** — only add learning that transfers to future tasks, not task-specific luck

### Card Format

```markdown
## Last Training — 2026-04-06

Score: 0.91 (prev: 0.86, delta: +0.05)
Context: deployment (real work)
KPI: source_diversity (5 sources avg → 8 sources avg)

Learnings:
- Separate OSINT search by category (infrastructure, certs, people) before synthesis
- Three-pass discovery: first pass finds obvious; second finds connections; third finds gaps
- Budget 40% of time to gap analysis before finalizing findings
```

### When NOT to Update

- If you didn't beat your last score → don't update. Add to training-queue.json instead (see OTJ Failure Path below).
- If the improvement is task-specific luck → don't update. Learning must generalize.
- If it's already in your agent card → don't duplicate. Crystallization removes noise.

## Three Paths to Improvement

### Path 1: On-The-Job Learning (OTJ) — Always On

**When:** Every time an agent completes real work.

**How it works:**
1. Agent finishes task and scores itself against its last deployment score
2. If beat: self-updates agent card → logged to training-log.jsonl
3. If didn't beat: added to training-queue.json with `on_the_job_eligible: true`

**Why OTJ is best:**
- Happens in real conditions, not artificial drills
- Agents see consequences of their choices immediately
- If later redemption occurs (queued agent beats target on different task), it counts as proof the improvement works
- Lower friction than scheduled training

**Training Queue Schema** (`~/.claude/hooks/state/training-queue.json`):
```json
{
  "agent": "research-analyst",
  "status": "queued",
  "source": "deployment",
  "kpi_missed": "source_diversity",
  "score": 0.72,
  "target": 0.80,
  "gap": 0.08,
  "hypothesis": "Over-relying on single source type; need cross-category search",
  "suggested_training": [
    "Category-separated OSINT: one sub-task per infrastructure domain",
    "Three-pass discovery drill: obvious → connections → gaps"
  ],
  "on_the_job_eligible": true,
  "created": "2026-04-05T14:22:00Z"
}
```

**OTJ Failure Path:**
- Agent deployed, scored < last score, added to queue with `on_the_job_eligible: true`
- Later deployed on different task, beats the previous target
- **REDEMPTION:** Self-updates card, marks training entry `redeemed_on_the_job`, logged as redemption
- Redemption is more valuable than explicit training because it proves improvement in wild conditions

---

### Path 2: Structured Autotune — Explicit Training Sessions

**When:** Use `/train --run AGENT` when:
- Agent is queued and not making progress in OTJ (3+ tasks failed)
- Sprint preparation requires specific capability lift
- Baseline needs to be established for a new agent type

**How it works:**
1. `/train --run research-analyst` → runs constrained training loop
2. Training system selects constraint from queue entry or infers from agent type
3. Loop (max 5 iterations):
   - Spawn agent with constraint (e.g., time-box, evidence-budget, adversarial challenge)
   - Score output
   - Feedback
   - Retry
4. Stop when: target met, budget exhausted, or 3 consecutive plateau
5. Results logged to training-log.jsonl

**Constraints** (selected based on agent type and failure pattern):

| Constraint | How it works | Best for |
|---|---|---|
| `time-box` | Hard wall: 5 min per iteration | Throughput (T) issues |
| `evidence-budget` | Max N citations allowed per finding | Quality (Q) issues — too verbose |
| `adversarial` | Second agent challenges each output | Resilience (R) — tests edge cases |
| `blind-handoff` | Write brief, next agent continues from brief only | Memory (M) — context leakage detection |
| `negative-space` | Must list missing evidence per finding | Quality (Q) — incompleteness detection |

**Training differs from deployment:**
- Training score ≠ deployment score (measured separately)
- Agent can score 1.0 in training (artificial drill) but 0.7 in deployment (real conditions)
- Faerie uses deployment scores for sprint readiness; training as fallback only

---

### Path 3: Mini-Learning — Lightweight Reflection

**When:** Enabled via `MINI_LEARNING=true` in spawn prompt (opt-in per session).

**How it works:**
1. Agent reserves last ~4K tokens (roughly the last minute of work) for reflection
2. Reflects: What worked? What was harder? What next time?
3. Writes 1-2 MEM blocks to scratch
4. Conditionally updates agent card (only if learning is general, durable, not already there)
5. Returns main output normally — reflection is invisible to user

**Output format:**
```
MINI_LEARNING complete.
Observations written: 2 MEM blocks
Agent.md: {updated | unchanged}
```

**Rules for mini-learning card updates:**
- ALL three conditions must be true:
  1. Discovered a technique that measurably improved output (vs start-of-session baseline)
  2. Technique is general (not task-specific)
  3. Not already in agent.md
- Max 3 bullets per agent card
- If no conditions met: skip — do not add noise

**Why mini-learning exists:**
- Real deployment reveals insights that artificial training misses
- No overhead: 4K tokens = ~30 seconds
- Flows through standard memory pipeline: scratch → memory-keeper → REVIEW-INBOX → faerie

## Commands Reference (Eval & Training)

### `/dev-eval` — System Performance Snapshot

**When:** After sessions to check system health.

**What it does:**
```bash
python3 ~/.claude/scripts/eval_harness.py --quick
```

**Output:**
- Scores all 6 dimensions (T/M/R/Q/P/F)
- Compares against baseline
- Flags any dimension below 0.7
- Flags if eval_run_number < 3 (baseline not established)
- Shows model routing efficiency (cost per token)

**Example output:**
```
SYSTEM EVAL — 2026-04-06
═══════════════════════════════════════════
Throughput (T):     0.88  ✓ (23 tasks/200K budget)
Memory (M):         0.79  ✓ (HONEY.md 4.1K, -12% since last)
Resilience (R):     0.91  ✓ (18/20 retries successful)
Quality (Q):        0.82  ✓ (avg agent KPI: 0.82)
Piston (P):         0.84  ✓ (W3 avg completion 185s)
Model routing (F):  0.76  ⚠ (Sonnet OVR 12%, review usage)
═══════════════════════════════════════════
Composite: 0.83 ✓ (above 0.75 target)
Last 3 evals: 0.81, 0.79, 0.83 (trend: +0.04)
```

**Flags to watch:**
- Any dimension < 0.7 → investigate + fix
- F (model routing) < 0.8 → audit Haiku/Sonnet/Opus usage
- Composite trend downward → check HONEY.md budget, memory promotion rate

---

### `/debloat` — System Health Scan with Failure Analysis

**When:** Before commits, when system feels slow, or monthly.

**What it does:**
1. Mechanical scan: checks all durable file budgets
2. For each over-budget item, explains:
   - **WHY** it grew (duplication? drift? crystallization missed?)
   - **CASCADE** — what this breaks (over-budget HONEY → blocks crystallization → insights lost)
   - **FIX** — specific action (crystallize, siphon, archive)
   - **LEARNING** — what this teaches about system evolution

**Budget table** (hard limits):

| File | Budget | Trigger |
|---|---|---|
| `~/.claude/memory/HONEY.md` | 200 lines / ~4K tokens | > 150 lines |
| `{repo}/.claude/memory/HONEY.md` | 150 lines / ~3K tokens | > 100 lines |
| Any agent card | ~1K tokens | > 800 tokens |
| Any skill file | ~2K tokens | > 1.5K tokens |

**Cascade example:**
```
COMPONENT: HONEY.md (5.2K / 4K budget)
WHY: Three new methods from last sprint not yet crystallized. NECTAR has 12 new observations.
CASCADE: Over-budget HONEY blocks faerie from crystallizing NECTAR → insights stay
         in validation state → agents on next sprint don't see recent learnings
FIX: Run /faerie crystallize to integrate NECTAR entries into HONEY
LEARNING: Crystallize needs to happen at sprint boundary, not ad-hoc
```

**Conflict detection:**
- Same concept in rules/ AND commands/ AND skills/ → flag overlap
- Budget in debloat.py differs from rules/ → flag mismatch
- Command descriptions stale vs frontmatter → flag
- DEPRECATED skills still in registry → flag for removal

**Run it:**
```bash
/debloat --scan              # Just show budget table
/debloat --explain COMPONENT # Deep-dive on one over-budget file
/debloat --fix               # (spawns membot to crystallize)
/debloat --dry-run           # Show what --fix would do
```

---

### `/train` — Agent Training Hub

**Single entry point** for all training, OTJ visibility, and sprint prep.

**Subcommands:**

| Command | What |
|---|---|
| `/train` (no args) | Training dashboard: queue + recent OTJ + scores + redemptions |
| `/train --queue` | Full queue with priorities, gaps, OTJ-eligible count |
| `/train --run AGENT` | Autotune one agent (iterative, constrained) |
| `/train --prep CATEGORY` | Prep roster for sprint — readiness check + run needed training |
| `/train --roster CATEGORY` | Batch train related agents (evidence, pipeline, analysis, etc.) |
| `/train --dashboard` | JSON output for statusline + dashboards |
| `/train --all` | Full cycle: prioritize → pick highest → autotune → update queue |

**Example: Prep sprint**
```bash
/train --prep evidence
```

Output:
```
SPRINT PREP — evidence category
────────────────────────────────────────
evidence-curator     0.91  ✓ ready (trained 2d ago)
data-scientist       0.82  ⚠ below target 0.85 — will autotune
report-writer        0.65  ✗ needs training — plateau, try adversarial
coc-manager          0.84  ✓ ready
security-auditor     0.77  ⚠ below target 0.80 — will autotune
────────────────────────────────────────
Ready: 2/5 | Needs training: 3/5
Est. training time: ~15 min (3 agents × 5 min)
```

If confirmed, runs autotune on agents below target, updates sprint-progress.json.

---

### `/eval` — Evaluation Suite (COC-Tracked)

**When:** Score individual task outputs, audit trails, baselines, dashboards.

| Command | What |
|---|---|
| `/eval baseline AGENT` | Establish first reference score |
| `/eval score TASK_ID` | Score completed task output |
| `/eval audit DATE` | Forensic inspection + hash chain validation |
| `/eval report AGENT` | Performance trend (last 10 runs, baseline comparison) |
| `/eval dashboard` | All agents at a glance, color-coded by score range |
| `/eval auto-learn on/off` | Toggle auto-queueing of failing agents |
| `/eval collect` | Scan manifests, score any missing evals |

**Scoring model:**

Agents have two independent score tracks:
- **Training track** — from `/train --run` (constrained drills)
- **Deployment track** — from OTJ (real work)

Comparison is within-track only. First score in any track = BASELINE (not improvement).

**Example dashboard:**
```
AGENT EVALUATION DASHBOARD
═══════════════════════════════════════════════════════════════
Excellent (8.0–10.0):
  fullstack-developer     9.1/10  ↑+1.0 (3 evals)
  data-scientist          8.7/10  ↑+0.2 (5 evals)

Good (6.0–7.9):
  research-analyst        7.5/10  →     (8 evals)

⚠ FLAGGED FOR TRAINING (< 4.0):
  evidence-analyst        3.2/10  ↓-2.1 (1 eval, baseline pending)
═══════════════════════════════════════════════════════════════
```

Scores written to JSONL with hash chains for forensic COC.

## Key Files

| File | Purpose |
|---|---|
| `~/.claude/hooks/state/training-queue.json` | Agents queued for improvement, OTJ-eligible status |
| `~/.claude/hooks/state/training-log.jsonl` | Append-only history of all training events + redemptions |
| `~/.claude/hooks/state/subagent-roster.json` | Every agent run ever spawned (when, why, outcome) |
| `~/.claude/hooks/state/crystallization-metrics.json` | HONEY/NECTAR budget state, pressure points |
| `~/.claude/hooks/state/evals/*.jsonl` | Eval records with hash chains (forensic COC) |
| `~/.claude/agents/{type}.md` | Agent identity card; includes "## Last Training" section |

---

## Integration with Faerie's Session Flow

### Session Start (`/faerie`)

Faerie reads:
1. Agent cards (all, quick scan) → KPIs, last training scores, deployment status
2. Training queue (full) → identifies agents needing prep
3. Training log tail → recent improvements + redemptions for dashboard

### Session Work

As agents complete tasks:
- OTJ reflection happens automatically (mini-learning or full reflection)
- If beat score → agent self-updates card
- If didn't beat → added to queue

### Session End (`/handoff`)

1. Scratch MEM blocks promoted to NECTAR.md
2. Training queue reviewed → HIGH priority agents flagged for next sprint
3. Training log updated with any redemptions
4. Faerie prepares brief for next session

### Next Session

Faerie sees:
- Updated agent cards (beat-last improvements)
- New training queue entries (failure → on_the_job_eligible)
- Redemption entries (failure → success trajectory)
- Uses deployment scores for sprint readiness (training scores as fallback)

---

## Baseline vs Improvement

**First measurement** in any track (training or deployment) = BASELINE.
- Don't treat 0→0.95 as "improvement" → it's initial measurement
- Record as `Context: baseline`

**Improvement** = beating a prior score in the SAME track.
- Training: 0.82 → 0.91 = +0.09 improvement (both training scores)
- Deployment: 0.84 → 0.89 = +0.05 improvement (both deployment scores)

**Untested agent** = has training score but no deployment score (may score high in drills but struggle in production).

## When to Use Each Path

| Situation | Path | Command |
|---|---|---|
| **Agent completes real work and beats score** | OTJ | (automatic — agent self-updates) |
| **Agent fails real work, queued, later beats target** | OTJ Redemption | (automatic — agent self-updates + marks redeemed) |
| **Agent queued for training, not improving via OTJ** | Autotune | `/train --run AGENT` |
| **Sprint prep — need specific capability lift** | Autotune | `/train --prep CATEGORY` |
| **Agent starts new task, want lightweight reflection** | Mini-learning | (enable via spawn: `MINI_LEARNING=true`) |
| **Batch train related agents before sprint** | Autotune + Roster | `/train --roster CATEGORY` |
| **Establish first score for new agent** | `/eval baseline` | `/eval baseline AGENT` |
| **Score output of completed task** | `/eval` | `/eval score TASK_ID` |

---

## Troubleshooting

### Agent scoring < baseline, not improving via OTJ

1. Check training queue: `is on_the_job_eligible: true`?
2. Run `/train --run AGENT` with explicit constraint (time-box, adversarial, etc.)
3. If training also plateaus: agent may need redesign or different task assignment

### Training score high, deployment score low

Agent excels in artificial drills but struggles in real conditions. This is normal.
- Recommend rotating agent to different task category (maybe better-matched capability)
- Or: deploy on simpler tasks, let OTJ build confidence
- Deployment score is ground truth for sprint readiness

### Over-budget HONEY.md blocking crystallization

1. Run `/debloat --explain HONEY.md` to see what grew
2. Run `/faerie crystallize` to integrate NECTAR entries
3. Check: is crystallization happening at sprint boundaries? (should be automatic)

### Model routing (F dimension) below 0.8

1. Run `/dev-eval` to see current usage (Haiku %, Sonnet %, Opus %)
2. Audit recent sessions: were simple tasks routed to Opus? Complex to Haiku?
3. Add model routing rules to agent cards (e.g., "use Haiku for classification; Sonnet for synthesis")

## Examples

### Example 1: Beat-Last-Score Update

Agent `research-analyst` completes task and beats last deployment score (0.73 → 0.80).

Agent reads its card, finds:
```markdown
## Last Training — 2026-03-28
Score: 0.73 (prev: 0.70, delta: +0.03)
Context: deployment
```

Agent appends:
```markdown
## Last Training — 2026-04-06
Score: 0.80 (prev: 0.73, delta: +0.07)
Context: deployment
KPI: source_diversity (improved from 5 sources avg to 8)

Learnings:
- Category-separated OSINT: one sub-task per infrastructure domain (before synthesis)
- Three-pass discovery: obvious → connections → gaps (prevents premature conclusion)
- Allocate 40% discovery time to gap analysis (finds unknowns before finalizing)
```

Logged to training-log.jsonl:
```json
{
  "type": "improvement",
  "agent": "research-analyst",
  "from": 0.73,
  "to": 0.80,
  "context": "deployment",
  "task": "task-67890",
  "kpi": "source_diversity",
  "ts": "2026-04-06T14:22:00Z"
}
```

Next session, faerie sees this improvement and considers agent ready for similar tasks.

---

### Example 2: OTJ Failure → Queue → Redemption

Agent `data-scientist` completes first task in new role, scores 0.68 (below target 0.80).

Training queue entry created:
```json
{
  "agent": "data-scientist",
  "status": "queued",
  "source": "deployment",
  "score": 0.68,
  "target": 0.80,
  "gap": 0.12,
  "hypothesis": "Over-smoothing data; missing significance tests",
  "on_the_job_eligible": true
}
```

One week later, agent deployed on different task (different domain, similar KPI). Analyzes carefully, includes three statistical tests, finds significant pattern. Scores 0.84 (beats target 0.80).

Redemption logged:
```json
{
  "type": "redemption",
  "agent": "data-scientist",
  "original_failure": "0.68 on task-A",
  "redemption_score": 0.84,
  "context": "deployment",
  "task": "task-B",
  "ts": "2026-04-06T09:15:00Z"
}
```

Agent self-updates card:
```markdown
## Last Training — 2026-04-06
Score: 0.84 (prev: 0.68, delta: +0.16)
Context: deployment (redeemed on-the-job)

Learnings:
- Statistical tests first (before smoothing) — preserves signal
- Report confidence intervals, not just point estimates
- Separate exploratory from confirmatory analysis
```

Faerie surfaces this redemption in next session's training dashboard. The arc from failure to success is proof the improvement works in production.

---

### Example 3: Sprint Prep with Autotune

User runs `/train --prep evidence` before evidence-heavy sprint.

System checks roster:
- `evidence-curator`: 0.91 (trained recently, ready)
- `data-scientist`: 0.82 (below 0.85 target)
- `report-writer`: 0.65 (below 0.75 target, plateau)
- `coc-manager`: 0.84 (ready)
- `security-auditor`: 0.77 (below 0.80 target)

User confirms prep. System:
1. Runs `/train --run data-scientist` → targets throughput (T), max 5 iterations, time-box constraint
2. Runs `/train --run security-auditor` → targets quality (Q), max 5 iterations, evidence-budget constraint
3. Skips `report-writer` (significant plateau) — flags for human review

Results:
- `data-scientist`: 0.82 → 0.87 (beats target) → updates card + training log
- `security-auditor`: 0.77 → 0.81 (beats target) → updates card + training log
- `report-writer`: flagged, recommend different constraint or task reassignment

Sprint readiness: 4/5 ready (evidence-curator, data-scientist, coc-manager, security-auditor). report-writer needs attention.

---

## Summary Table

| What | When | How | Output |
|---|---|---|---|
| **Automatic improvement** | Every task | Agent beats last score | Self-update card + training-log entry |
| **Failure → queue** | When agent doesn't beat | OTJ failure path | training-queue entry with on_the_job_eligible |
| **Redemption** | When queued agent later beats target | OTJ redemption path | Self-update + training-log redemption entry |
| **Explicit training** | Planned sprint prep | `/train --run AGENT` | Autotune loop + card update |
| **Sprint readiness** | Before major sprint | `/train --prep CATEGORY` | Readiness report + run needed training |
| **Batch training** | Multi-agent improvement | `/train --roster CATEGORY` | Cross-pollinated training + results table |
| **Lightweight reflection** | During real work | Enable `MINI_LEARNING=true` | MEM blocks + conditional card update |
| **System health check** | After sessions | `/dev-eval` | 6D scores + flags below 0.7 |
| **Budget scan** | Before commits | `/debloat` | Over-budget files + WHY + cascade + fix |
| **Individual scoring** | Task completion | `/eval score TASK_ID` | Score + trend + baseline comparison |
| **Audit trail** | Monthly review | `/eval audit DATE` | Hash chain validation + anomaly detection |

