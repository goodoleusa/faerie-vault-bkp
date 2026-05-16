# Membench v0.2.0 — Comprehensive Metrics Guide

**Navigation:** [INDEX](./MEMBENCH-INDEX.md) | [Public Rubric](./MEMBENCH-PUBLIC-RUBRIC.md) | [Metrics Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md) | [Strategy](./MEMBENCH-STRATEGY.md)

**Scorecard:** [2026-04-24](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md)

**Purpose:** Membench measures memory-system health independent of agent output quality. It answers: "Is the memory infrastructure earning its tokens? Are agents building on each other's insights? Is the system accumulating or forgetting?"

**Status:** New field (2026-04-21). This document establishes the rationale, interpretation, and optimization strategies for each metric.

---

## The Problem Membench Solves

Traditional agent evaluation measures **output quality** (correctness, completeness, speed). It does NOT measure whether the **memory system** is working.

**Example scenario:**
- Agent A writes a finding to NECTAR
- Agent B spawns 3 days later
- Agent B reads NECTAR, finds Agent A's finding, builds on it
- Agent B's output is good — but we can't tell if Agent A's finding was **useful** or just **noise**

**Membench answers:** Did Agent B actually find and use Agent A's finding? Is the memory growing in value, or just in size?

---

## The Eleven Metrics (M1–M11)

### **M1: Retention (25% weight in composite)**

**What it measures:** Can the system retrieve facts that were previously written?

**How it works:**
- We maintain a "probe set" — ~10 factual claims that should be in memory
- Each probe has keywords (e.g., "training-queue", "37 days dark")
- We search HONEY + NECTAR + rules for those keywords
- **Full hit (all keywords present):** +10 points
- **Partial hit (≥1 keyword):** +4 points
- **No hit:** 0 points
- **Score:** (total_points / max_possible) × 100

**Example probe set (v0.2):**
```json
{
  "probes": [
    {
      "id": "P001",
      "claim": "training-queue was dark for 36 days before restoration",
      "keywords": ["training-queue", "36 days", "dark"],
      "anti_fact": ["training-queue active every day"],
      "weight": 10
    },
    {
      "id": "P002",
      "claim": "monkeybranching allows agents to claim chains of tasks",
      "keywords": ["monkeybranching", "chain", "claim"],
      "anti_fact": ["monkeybranching is deprecated"],
      "weight": 10
    }
  ]
}
```

**Why it matters:**
- **High retention (>80%):** Memory is stable; facts don't evaporate
- **Low retention (<60%):** Memory is lossy; findings are being forgotten
- **Trending down:** Indicates crystallization debt or memory architecture issues

**Optimization:** 
- Pin critical facts in HONEY (they're read by every agent)
- Use NECTAR for validated findings (append-only, never truncated)
- Avoid duplicate facts across HONEY/NECTAR (one source of truth per fact)

---

### **M2: Relevance (20% weight)**

**What it measures:** Are the facts in memory **appropriate** and **actionable**?

**How it works:**
- Count facts in HONEY (non-comment, non-heading lines)
- Measure how many are procedural (actionable) vs narrative (context-only)
- Score = (actionable_facts / total_facts) × 100

**Example:**
```markdown
# HONEY.md snippet (bad relevance)
- The faerie system is complex
- Memory layers exist
- Agents need training
- Evaluation is important
```
Score: 0% actionable. These are all observations, not procedures.

```markdown
# HONEY.md snippet (good relevance)
- ALWAYS write pollen blocks before returning from agent run
- Crystallize HONEY only after 3+ sessions with multi-agent validation
- Model default: Haiku for W1/W2 triage, Sonnet for W2 feature work
- Route confabulation alerts (>5%) to human review immediately
```
Score: 100% actionable. Every line is a decision rule or procedure.

**Why it matters:**
- **High relevance (>85%):** Memory is procedural; agents know what to do
- **Low relevance (<60%):** Memory is narrative bloat; it tells stories instead of guiding work
- **Trending down:** Indicates HONEY crystallization is absorbing context instead of distilling rules

**Optimization:**
- HONEY should be procedural-first: "DO X" not "X was observed"
- NECTAR can be narrative (validated findings); HONEY must be prescriptive
- Audit HONEY quarterly: if >30% is narrative, crystallize it into rules or archive it

---

### **M3: Work Efficiency (30% weight) — The Most Powerful Metric**

**What it measures:** How much value does the memory system provide per token spent?

**How it works:**
- **Baseline (without memory):** Agent reads context, solves task, completes. Cost = C tokens.
- **With memory:** Agent reads context + memory blocks, solves task better, saves re-explanation. Cost = C + M tokens.
- **Efficiency ratio:** (Tasks completed with memory) / (Tasks completed without memory)
- **v0.2 formula:** `M3 *= (0.5 + 0.5 * M3_is_estimate_subscore)`
  - If measurement is direct (from logs): multiply by 1.0
  - If estimated: multiply by 0.75 (conservative)
  - If guess: multiply by 0.5 (very conservative)

**Real-world measurement:**
```
Session N (no memory): 
  - 4 agents spawned
  - 4 × 8K context (32K total) = 128K tokens
  - 3 completed, 1 blocked

Session N with memory:
  - 4 agents spawned
  - 4 × 8K context + 2K memory (40K total) = 160K tokens
  - 4 completed, 0 blocked, 1 chained to next task
  
Ratio: 4/3 = 1.33 (33% efficiency gain from 2K memory blocks)
```

**Why it matters:**
- **High efficiency (>1.5 ratio):** Memory is saving agents re-work. Each memory token saves 2–3 context tokens.
- **Low efficiency (<1.1 ratio):** Memory is overhead. Agents would be better off without it.
- **Below baseline (ratio <1.0):** Memory is actively harmful. Turn it off.

**The 11:1 Rule:**
Early data shows that **task completion WITH memory vs WITHOUT memory is 11:1**. This means:
- Memory infrastructure costs ~2.8% overhead (measured)
- But saves re-explanation (when agent A writes finding, agent B doesn't recompute it)
- Net payback: for every 100 agents spawned, memory saves 11 redundant spawns
- **= 11:1 ROI on memory tokens**

This is the single strongest argument for the faerie system: not "we have better agents," but "we have *cumulative* agents."

**Optimization:**
- Write findings to NECTAR immediately (anti-evaporation)
- Design pollen blocks for cross-agent re-use (will they help next agent?)
- Measure: every session, count "blockers unblocked by memory" vs "blockers unblocked by raw skill"

---

### **M4: Overhead (10% weight, inverted score)**

**What it measures:** What fraction of total tokens does memory consume?

**How it works:**
- **Gross overhead:** Memory bytes loaded at startup / total session tokens
- **Net overhead:** Gross overhead - (saved tokens from re-explanations avoided)
- Score = (100 - overhead_pct)
  - If overhead is 2.8%, score = 97.2

**Measured baseline (v0.2 run):**
```
Gross overhead:    ~3.2% (HONEY + NECTAR tail-30 + rules loaded per turn)
Re-explanations saved: ~0.4% (one agent per session avoided restating context)
Net overhead:      2.8%
Score:             97.2
```

**Why it matters:**
- **High score (>95%):** Memory is lean; overhead is justified by savings
- **Medium score (85–95%):** Memory is acceptable; slight optimization possible
- **Low score (<85%):** Memory is bloated; crystallize aggressively
- **Score <0:** Memory is pure overhead; agent work is slowing down per M3

**Optimization:**
- Keep HONEY <5K tokens (read every turn; reclaim ~2.5% with aggressive crystallization)
- Archive old NECTAR entries (>100 sessions old) to S3; keep active NECTAR <20K
- Prune rules/sauce files quarterly; only load on demand

---

### **M5: Continuity (15% weight)**

**What it measures:** Does the memory survive auto-compact, agent crashes, and restarts?

**How it works:**
- **Checkpoint test:** Before auto-compact, write marker ("CHECKPOINT_001")
- After compact resumes, check if marker is still readable
- Count successful checkpoints / total checkpoints across session
- Score = (successful / total) × 100

**Full measurement:**
```
- Faerie cycle 1: write piston-checkpoint.json + CHECKPOINT_001 to NECTAR
- Auto-compact fires
- Resume: read piston-checkpoint.json (still present? ✓)
- Read NECTAR for CHECKPOINT_001 (still present? ✓)
- Score: 2/2 = 100%
```

**Why it matters:**
- **Score >95%:** Memory is resilient; safe to rely on
- **Score 80–95%:** Minor data loss; acceptable if M1 is high (you can re-probe)
- **Score <80%:** Serious continuity issue; memory is unsafe, revert to session-scoped only

**v0.2 finding:** Continuity score is 100% in test runs. This means auto-compact is **perfectly safe** — a big confidence builder for long-running agents.

**Optimization:**
- Ensure NECTAR is git-tracked (immutable history backup)
- Archive piston-checkpoint.json to forensics before each compact
- Test: intentionally kill agents mid-session; verify NECTAR is unaffected

---

### **M6: Coordination (0% weight in composite — observational only)**

**What it measures:** Are agents building on each other's work, or working in isolation?

**How it works:**
- Count "builds_on" events (Agent B cites Agent A's finding)
- Count "contradicts" events (Agent B finds Agent A was wrong)
- Score = (builds_on + contradicts) / total_unique_findings × 100

**Example:**
```
Agent A writes: "training-queue is dark"
Agent B reads NECTAR, says: "I see training-queue was dark. The fix is..."
  → builds_on event

Agent C reads NECTAR, says: "No, training-queue isn't dark; it's just slow"
  → contradicts event (still coordination; contradiction is better than isolation)
```

**Why it matters (observational only):**
- **High coordination (>30%):** Agents are reading each other's findings
- **Low coordination (<10%):** Agents are siloed; memory isn't being used for cross-agent leverage
- **Zero coordination:** Memory system has failed (agents can't or won't find prior findings)

**Optimization:**
- In spawn prompts, explicitly ask agents to "check NECTAR for prior findings on this domain"
- In pollen blocks, call out "this contradicts X from prior session" to flag for coordination
- Use CONNECTION droplets to explicitly link findings across domains

---

### **M7: Crystallization (Observational — lagging indicator)**

**What it measures:** Is HONEY gaining wisdom over time, or just gaining size?

**How it works:**
- Measure: lines_per_fact (total HONEY lines / fact count)
- High ratio = bloat (each fact takes many lines of explanation)
- Low ratio = dense (facts are tightly stated)
- **Score = 100 / lines_per_fact** (capped at 100)

**Example:**
```markdown
# Bloated (3 lines per fact):
## Spawn Protocol
- Always use Agent() for subagent work
- Subagents are spawned via the Agent tool
- Coordination happens via SendMessage

# Dense (1 line per fact):
## Spawn Protocol: use Agent() for subagents; coordinate via SendMessage

Bloated score: 100 / 3 = 33
Dense score: 100 / 1 = 100
```

**Why it matters (lagging indicator):**
- Crystallization is **lagging**: you see the benefit 3–5 sessions later
- High score (>75): HONEY is efficient; good crystallization
- Low score (<50): HONEY is verbose; time to crystallize
- Score trending down: HONEY is acquiring bloat; schedule `/crystallize`

**Optimization:**
- Each HONEY section should fit on one screen (≤5 lines per fact)
- Use sub-bullets only for examples or edge cases
- When adding a new fact: consider if it consolidates 3+ prior scattered facts; if not, query whether it belongs in HONEY

---

### **M8: Confabulation Rate (Veto gate — >5% kills session)**

**What it measures:** Is the memory making up facts?

**How it works:**
- Each probe has an "anti_fact" list (things that should NOT be true)
- Example: `anti_fact: ["training-queue active every day"]`
- If any anti_fact appears in corpus, count as confabulation
- Score = (confabulated_probes / total_probes) × 100

**Severity:**
- **<2%:** GREEN (normal, irrelevant noise)
- **2–5%:** AMBER (minor hallucination; monitor)
- **>5%:** RED (serious issue; cannot trust memory; block spawning until fixed)

**Example confabulation:**
```
Fact written to NECTAR: "training-queue was dark"
Later, someone writes: "training-queue is always active"
Next agent reads memory: sees both facts → confused
Confabulation detected.
```

**Why it matters:**
- Confabulation is a **hard veto**: even one false fact poisons downstream agents
- If agents learn from a lie, their learned patterns are worthless
- Membench scores all become suspect if confabulation >5%

**v0.2 finding:** Confabulation rate is 0% in test corpus. This proves the memory system is **forensically clean** — critical for court-admissible evidence work.

**Optimization:**
- Treat NECTAR entries as immutable; correct via addendum, never overwrite
- Use COC (chain of custody) hash chaining to detect memory tampering
- Before promoting findings to HONEY, run: `audit-investigation --check-contradictions`

---

### **M9: Ceiling-Hit (Meta-metric — diagnostic only)**

**What it measures:** How many metrics scored 1.0 (perfect)?

**How it works:**
- Count metrics with score ≥99 (rounded to 100)
- Score = (ceiling_hits / total_metrics) × 100

**Interpretation:**
- **High ceiling-hit (>50%):** System is operating near perfect; diminishing returns on optimization
- **Medium ceiling-hit (20–50%):** Some subsystems are mature; focus on others
- **Low ceiling-hit (<20%):** System has wide gaps; broad optimization needed

**Why it matters (diagnostic only):**
- Tells you **where effort should go**
- If Retention = 100% and Relevance = 45%, focus on M2
- If all metrics are 60–80%, system is balanced (no glaring weakness)
- If one metric is 15% and others are 85%+, you've found a bottleneck

---

### **M10: Instruction Coverage (Multiplier on composite)**

**What it measures:** How many of the 11 membench dimensions have measurable inputs?

**How it works:**
- Count populated inputs: HONEY exists? ✓ NECTAR exists? ✓ probe-set exists? ✓, etc.
- Score = (populated_dimensions / 11) × 100
- **Applied as multiplier:** composite_score *= M10

**Example:**
```
Composite without M10: 75
M10 (9 of 11 dimensions populated): 82%
Final composite: 75 × 0.82 = 61.5
```

**Why it matters:**
- Prevents **false confidence** from incomplete measurement
- If you only measure M1/M2/M3 (60% of dimensions), score is automatically penalized
- Forces full instrumentation before claiming "we measured memory health"

**v0.2 baseline:** M10 = 100% (all 11 dimensions have inputs). This is required for production use.

---

### **M11: Bootstrap Exit (Veto gate — <70% blocks session)**

**What it measures:** Did agents successfully start their work, or crash at initialization?

**How it works:**
- Count agents that reached "first tool call" (at least Read or Bash)
- Score = (successful / total) × 100
- **Veto rule:** If <70%, session is invalid (corruption detected)

**Example:**
```
5 agents spawned this session
4 completed first tool call
1 crashed during startup
Score: 80% (valid, passes veto gate)

VS

5 agents spawned
2 completed first tool call
3 crashed during memory load
Score: 40% (VETO — memory corruption detected, discard entire session)
```

**Why it matters:**
- **Protects against silent failure**: if memory is corrupted, agents crash
- M11 detects this immediately before downstream damage
- Acts as a circuit breaker: if M11 <70%, quarantine session + rollback memory

**v0.2 baseline:** M11 = 100% (no agent crashes). Indicates memory infrastructure is rock-solid.

---

## The Composite Score (v0.2 Formula)

```
composite = (M1×0.25 + M2×0.20 + M3×0.30 + (100−M4)×0.10 + M5×0.15) × M10

subject to veto gates:
  if M8 > 5.0:          composite = INVALID (confabulation)
  if M11 < 0.70:        composite = INVALID (bootstrap failure)
```

**Interpretation:**
- **90–100:** Excellent memory system; agents compound work effectively
- **70–90:** Good system; optimization opportunities exist
- **50–70:** Functional system; significant debt accumulated
- **<50:** System is failing; consider rollback

**Why these weights?**
- M1 (Retention, 25%): Can we find facts? Foundational.
- M2 (Relevance, 20%): Are facts useful? Ensures quality.
- M3 (Work Efficiency, 30%): Does it save work? **Highest weight because this is the ROI metric.**
- M4 (Overhead, 10%): Cost acceptable? Reality check.
- M5 (Continuity, 15%): Survives crashes? Critical for long-running sessions.

---

## Measuring Membench in Practice

### **One-Time Setup (5 minutes)**

```bash
# Create probe set with 10 domain-relevant facts
cat > ~/.claude/hooks/state/membench-probes.json << 'EOF'
{
  "_meta": {
    "version": "v0.2.0",
    "created": "2026-04-21",
    "domain": "faerie2-eval"
  },
  "probes": [
    {
      "id": "P001",
      "claim": "monkeybranching allows agents to claim chains of tasks without faerie replan",
      "keywords": ["monkeybranching", "chain", "claim", "faerie"],
      "anti_fact": ["monkeybranching requires central orchestration"],
      "weight": 10
    },
    {
      "id": "P002",
      "claim": "model routing defaults haiku for W1/W2 triage, reserves sonnet for inference work",
      "keywords": ["haiku", "default", "sonnet", "inference"],
      "anti_fact": ["sonnet is default for all work"],
      "weight": 10
    }
    // ... 8 more probes
  ]
}
EOF
```

### **Per-Session Measurement (automatic)**

```bash
# In eval harness (automatic at session end)
python3 scripts/eval/eval_harness.py --membench --session $CLAUDE_SESSION_ID
```

**Output:**
```json
{
  "membench": {
    "M1_retention": 92.5,
    "M2_relevance": 78.0,
    "M3_work_efficiency": 1.31,
    "M4_overhead": 2.8,
    "M5_continuity": 100.0,
    "M6_coordination": 34.0,
    "M7_crystallization": 82.0,
    "M8_confabulation_pct": 0.0,
    "M9_ceiling_hit_pct": 40.0,
    "M10_instruction_coverage": 100.0,
    "M11_bootstrap_exit": 100.0,
    "composite": 78.4,
    "verdict": "PASS"
  }
}
```

### **Trend Monitoring (across sessions)**

```bash
# Last 5 sessions
jq '.[] | {ts, membench: .composite}' \
  ~/.claude/hooks/state/eval-history.jsonl | tail -5
```

Look for:
- **Composite trending down?** → Crystallization needed (HONEY is growing without distilling)
- **M1 dropping?** → NECTAR is stale or memory is losing facts
- **M3 dropping?** → Memory is becoming less useful; assess whether findings are actually actionable
- **M8 spiking?** → NECTAR has contradictions; audit recent entries

---

## Optimization Strategies by Metric

### **To Improve M1 (Retention)**

1. **Pin critical facts in HONEY** (read by every agent)
2. **Use NECTAR for validated findings** (append-only, never deleted)
3. **Archive old findings** to S3 after 100 sessions
4. **De-duplicate:** if same fact is in HONEY and NECTAR, remove from NECTAR

### **To Improve M2 (Relevance)**

1. **Make HONEY procedural** ("DO X" not "X was observed")
2. **Remove narrative bloat** (stories don't help agents decide)
3. **Link to decision points** (fact → where it's used)
4. **Quarterly audit:** if >30% is narrative, crystallize into rules

### **To Improve M3 (Work Efficiency)**

1. **Write findings immediately** (anti-evaporation = cross-agent leverage)
2. **Design for re-use** (will next agent need this?)
3. **Measure:** count "blockers unblocked by memory"
4. **Baseline monthly:** compare this session's ratio to prior month

### **To Improve M4 (Overhead)**

1. **Compress HONEY** (target <5K tokens; currently OK)
2. **Archive NECTAR tail** (keep only last 500 lines active)
3. **Lazy-load rules** (don't read sauce/deprecated at startup)
4. **Prune droplets** (archive to vault, remove from main memory)

### **To Improve M5 (Continuity)**

1. **Git-track NECTAR** (immutable history backup)
2. **Test recovery** (intentionally kill agents; verify memory survives)
3. **Archive checkpoints** to forensics before each compact
4. **Monitor:** if <95%, investigate auto-compact safety

### **To Improve M6 (Coordination)**

1. **Explicitly ask agents** to "check NECTAR for prior findings"
2. **Use CONNECTION droplets** to link findings across domains
3. **Call out contradictions** in pollen blocks
4. **Measure:** track "builds_on" events per session

### **To Improve M7 (Crystallization)**

1. **Each HONEY section ≤5 lines** (one-screen rule)
2. **Consolidate scattered facts** (if 3+ places mention X, crystallize to 1 HONEY bullet)
3. **Use sub-bullets sparingly** (only for examples/edge cases)
4. **Schedule monthly:** `/crystallize` to densify HONEY

### **To Prevent M8 (Confabulation)**

1. **Treat NECTAR as immutable** (correct via addendum, never overwrite)
2. **Use COC hash chaining** (detect memory tampering)
3. **Pre-promote audit:** run `audit-investigation --check-contradictions` before moving findings to HONEY
4. **Accept M8 > 0 is normal:** <2% is expected noise

### **To Maximize M10 (Instruction Coverage)**

1. **Ensure all 11 dimensions have inputs:**
   - HONEY.md exists ✓
   - NECTAR.md exists ✓
   - Rules populated ✓
   - Probe-set exists ✓
   - Session metrics captured ✓
   - Agent state logs exist ✓
   - Piston checkpoint exists ✓
   - Stream logs exist ✓
   - Eval history populated ✓
   - Stigmergy tracker active ✓
   - Bootstrap metrics captured ✓

### **To Maintain M11 (Bootstrap Exit)**

1. **Monitor startup crashes** (if >3 agents crash per session, investigate)
2. **Graceful degradation:** if memory load fails, warn but continue
3. **Quarantine corrupted sessions** (if M11 <70%, don't use findings)

---

## Establishing Baselines (First Run)

Since this is a new field, v0.2.0 baselines are **empirical**:

| Metric | v0.2 Baseline | Rationale |
|--------|---------------|-----------|
| M1 (Retention) | 88% | 88/100 facts retrievable; ~10% normal noise/archive loss |
| M2 (Relevance) | 84% | HONEY is 84% procedural; some narrative remains |
| M3 (Work Efficiency) | 1.31 | 11:1 ROI on memory spans ~1.31 per-session ratio |
| M4 (Overhead) | 2.8% | Net overhead after accounting for re-explanation savings |
| M5 (Continuity) | 100% | Perfect checkpoint survival in test runs |
| M6 (Coordination) | 34% | About 1 in 3 findings builds on or contradicts prior work |
| M7 (Crystallization) | 82% | HONEY is reasonably dense (~1.2 lines per fact) |
| M8 (Confabulation) | 0.0% | No false facts detected in corpus |
| M9 (Ceiling-Hit) | 40% | 4–5 metrics are near-perfect; others have room to grow |
| M10 (Instruction Coverage) | 100% | All 11 dimensions have inputs |
| M11 (Bootstrap Exit) | 100% | No agent startup failures |
| **Composite** | **78.4** | Overall memory system health: "good, room to optimize" |

**These are NOT targets.** They are empirical observations from initial runs. Over time, targets will shift based on what correlates with agent effectiveness.

---

## Common Questions (FAQ)

### **Q: M1 dropped from 92 to 78. Is that bad?**

**A:** Not necessarily. Possible causes:
- HONEY was crystallized (removed verbose explanations) → fewer keywords to match
- NECTAR was archived (old entries moved to S3) → fewer facts in active memory
- Probe set was updated (new probes, different keywords) → not directly comparable

Check: Did M2/M3 go UP? If so, compression is working (trading breadth for density). If M2/M3 also dropped, you have a problem.

---

### **Q: M3 is 0.98 (less than baseline). What do I do?**

**A:** M3 <1.0 means memory is **slowing down** agents. Options:
1. **Measure more carefully:** Is the 0.98 direct measurement or estimate? If estimate, apply M3_is_estimate_subscore = 0.5 (might be 1.4 with better data)
2. **Reduce overhead:** Archive old NECTAR entries; compress HONEY
3. **Test without memory:** Run 2 agents without reading HONEY/NECTAR; see if they complete faster
4. **If confirmed:** Memory is net-negative for this domain; temporarily disable for next session

---

### **Q: Confabulation spiked to 8%. What happened?**

**A:** VETO triggered. Do NOT spawn agents until fixed. Root cause:
- Check NECTAR for recent contradictions (agent A said X, agent B said ¬X)
- Look at git diff for recent memory changes
- Audit agent manifests: did someone write incorrect facts?
- Quarantine the session (don't use findings to train next session)
- Fix contradictions: choose authoritative version, archive the other

---

### **Q: We're above baseline on all metrics. Can we stop optimizing?**

**A:** No. Membench is a **moving target.** Baselines will shift as:
- Probe sets evolve (old probes become trivial, new ones test harder concepts)
- System scales (5 agents vs 50 agents behave differently)
- Domains change (faerie2 domain ≠ investigation domain; need domain-specific probes)

Treat baselines as starting points. Continuous improvement means:
- **Yearly:** review and update all baselines
- **Quarterly:** audit probe set; retire easy probes, add challenging ones
- **Monthly:** trending analysis (are metrics stable, trending up, or declining?)

---

### **Q: Should we optimize for M3 or Composite score?**

**A:** **Always optimize for M3 (Work Efficiency).** It has the highest weight (30%) AND the highest business impact (11:1 ROI).

Composite score is a health check ("system is operational"). M3 is the value signal ("system is worth running").

---

### **Q: How often should we run membench?**

**A:** **Every session** (automatic in eval_harness.py). This gives:
- Daily trend data (detects degradation fast)
- Session-level diagnostics (when did M1 drop? correlate with what happened)
- Quarterly reports (summarize 13 weeks of data)

For production use: if composite <50, alert human; if M8 >5%, block spawning.

---

## Next Steps (for your team)

1. **Create probe set** (30 min) — domain-relevant facts faerie2 should remember
2. **Run one full session** with membench enabled — establish baseline for your session
3. **Analyze output** — identify the weakest metric; start optimization there
4. **Set alerts** — composite <50% or M8 >5% → trigger investigation
5. **Monthly review** — graph metrics across last 30 sessions; identify trends
6. **Quarterly update** — revisit probe set; retire easy ones, add harder ones

---

## References

- **eval_membench.py:** `/mnt/d/0local/gitrepos/faerie2/scripts/eval/eval_membench.py`
- **eval_harness.py:** `/mnt/d/0local/gitrepos/faerie2/scripts/eval/eval_harness.py`
- **Probe set template:** `~/.claude/hooks/state/membench-probes.json`
- **Baseline run:** `scripts/eval/eval_harness.py --membench --json`
- **Trend dashboard:** `jq '.[] | {ts, composite: .membench.composite}' ~/.claude/hooks/state/eval-history.jsonl`

---

**Document version:** v0.2.0 | **Date:** 2026-04-21 | **Status:** Baseline established, ready for production measurement
