# Membench v0.2.0 — Quick Reference Card

**Navigation:** [INDEX](./MEMBENCH-INDEX.md) | [Public Rubric](./MEMBENCH-PUBLIC-RUBRIC.md) | [Metrics Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md) | [Strategy](./MEMBENCH-STRATEGY.md)

**Scorecard:** [2026-04-24](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md)

**TL;DR:** 11 metrics measuring memory-system health. Target: composite >75. Run automatically every session.

---

## The 11 Metrics at a Glance

| # | Metric | Measures | Weight | Target | Status Light |
|---|--------|----------|--------|--------|---------------|
| **M1** | **Retention** | Can we find facts we wrote? | 25% | >85% | % corpus searchable |
| **M2** | **Relevance** | Are facts actionable? | 20% | >80% | % facts procedural |
| **M3** | **Work Efficiency** | How much value per token? | 30% | >1.3× | tasks/token ratio |
| **M4** | **Overhead** | What % tokens for memory? | 10% | <3% | inverted score |
| **M5** | **Continuity** | Survives crashes/compact? | 15% | 100% | checkpoint recovery |
| **M6** | **Coordination** | Agents building on each other? | 0% (observe) | >30% | "builds_on" events |
| **M7** | **Crystallization** | HONEY density/efficiency? | 0% (observe) | >75% | lines per fact |
| **M8** | **Confabulation** | False facts in memory? | **VETO** | <2% | RED if >5% |
| **M9** | **Ceiling-Hit** | How many are perfect? | 0% (diagnostic) | — | metric maturity |
| **M10** | **Instruction Coverage** | All dimensions populated? | ×1.0 multiplier | 100% | dimension count |
| **M11** | **Bootstrap Exit** | Agents crash at startup? | **VETO** | >70% | agent init failure |

---

## Composite Score Calculation

```
composite = (M1×0.25 + M2×0.20 + M3×0.30 + (100-M4)×0.10 + M5×0.15) × M10

Veto gates:
  M8 > 5.0%  → INVALID (confabulation)
  M11 < 70%  → INVALID (corruption)

Result interpretation:
  90–100     Excellent memory system
  70–90      Good system; optimization opportunities
  50–70      Functional; significant debt
  <50        System failing; investigate
```

---

## How to Read Your Score

**Composite = 78.4 | M1=92 M2=78 M3=1.31 M4=2.8 M5=100 M6=34 M7=82 M8=0.0 M9=40 M10=100 M11=100**

✅ **What's working:**
- M1 (92%) — facts are findable
- M3 (1.31×) — memory saves agent work (11:1 ROI across sessions)
- M5 (100%) — perfect crash recovery
- M8 (0%) — forensically clean (no false facts)

⚠️ **Room to improve:**
- M2 (78%) — some findings are narrative instead of procedural
- M7 (82%) — HONEY has some verbose sections (compress them)
- M6 (34%) — agents could coordinate more on findings

🎯 **Action:** Next session, focus on M2 (make HONEY more procedural).

---

## One-Minute Diagnostics

### **Composite is dropping**
→ Check M3 first (work efficiency). If M3 is stable, check M4 (overhead growing?).

### **M1 dropped, M2 stayed flat**
→ NECTAR is shrinking (findings archived?). Check if M3 is still good (if yes, compression working).

### **M3 < 1.0**
→ Memory is slowing agents. Measure without memory for 1 session to confirm. If confirmed, disable HONEY/NECTAR temporarily.

### **M8 > 2%**
→ NECTAR has contradictions. Find them (git diff + manual audit). Minor issue unless >5% (VETO).

### **M8 > 5%**
→ **VETO triggered.** Do not spawn agents. Quarantine session. Fix contradictions in NECTAR immediately.

### **M11 < 70%**
→ **VETO triggered.** Agents crashing at startup = memory corruption. Rollback HONEY/NECTAR from last known-good commit.

### **All metrics near 100%, composite stuck at 80**
→ M10 issue (incomplete dimensions populated) or systematic ceiling-hit (system is mature, diminishing returns).

---

## Optimization Priority (Month 1)

| Week | Focus | Action | Expected | Effort |
|------|-------|--------|----------|--------|
| **W1** | M3 | Measure; baseline work efficiency | Confirm 1.3× ratio | 15 min |
| **W2** | M2 | Audit HONEY for narrative bloat | Remove 20% verbose text | 30 min |
| **W3** | M1 | Baseline probe set | Establish M1 score | 45 min |
| **W4** | M4 | Archive old NECTAR | Reduce overhead to <2.5% | 20 min |

**Expected result after Month 1:** Composite 78 → 82 (+5%).

---

## Setting Alerts (Production)**

```bash
# Monitor these thresholds
if composite < 50:  # System failing
  alert("CRITICAL: Membench composite below 50")
  action: investigate immediately

if M8 > 5.0:        # Confabulation veto
  alert("CRITICAL: Confabulation detected (>5%)")
  action: block spawning, audit NECTAR, rollback

if M11 < 0.70:      # Bootstrap failure veto
  alert("CRITICAL: Agent startup failure (M11 <70%)")
  action: quarantine session, rollback memory

if composite < 65:  # Trending down
  alert("WARNING: Composite below 65")
  action: schedule crystallization

if M4 > 4.0:        # Overhead creeping up
  alert("WARNING: Memory overhead >4%")
  action: archive old NECTAR, compress HONEY
```

---

## Updating Probe Set (Quarterly)

Current probe set measures **known facts** (e.g., "training-queue was dark 36 days").

**Every 90 days:**
1. Retire probes that score 100% (too easy; system knows them)
2. Add new probes testing newer learning (e.g., "when should we use Sonnet vs Haiku?")
3. Increase keyword diversity (don't just search for exact phrases)

**Example update (Q2 2026):**
- Retire: "faerie2 exists" (100% retrieval; too easy)
- Retire: "HONEY is used for prefs" (always true)
- Add: "monkeybranching reduces faerie replanning by X%"
- Add: "model routing saves Y% cost vs baseline"

---

## Membench vs Other Metrics

| Metric Type | Measures | When to Use |
|-------------|----------|------------|
| **Membench (M1–M11)** | Memory system health | Every session; diagnose memory issues |
| **Eval Harness (6D)** | Agent output quality | Every agent run; score individual agents |
| **Model Routing (Dim F)** | Cost/speed optimization | Track per-session; optimize model selection |
| **Roster** | Model distribution | Trend over time; enforce Haiku-default |
| **COC** | Forensic integrity | Court-admissibility; detect tampering |

**All are complementary.** Membench is **not** agent quality. It's **substrate quality** (does memory help agents be good?).

---

## Common Mistakes to Avoid

❌ **Optimizing composite score instead of M3**
→ Composite is health check. M3 is business value.

❌ **Ignoring M6 (Coordination = 0%)**
→ Means agents aren't reading NECTAR. Fix spawn prompts to explicitly ask: "Check NECTAR for..."

❌ **Allowing M8 to creep above 2%**
→ Even 3% is a red flag. Each false fact poisons downstream agents.

❌ **Over-crystallizing HONEY**
→ Dense is good, but not at the cost of removing nuance. Target 1.2 lines/fact, not 0.5.

❌ **Running membench once, then ignoring it**
→ Trend matters more than absolute score. Monthly analysis reveals whether system is improving.

---

## Session Checklist

Before declaring session complete:

- [ ] Composite score captured in eval-history.jsonl
- [ ] M8 (confabulation) ≤5% (if >5%, quarantine)
- [ ] M11 (bootstrap) ≥70% (if <70%, quarantine)
- [ ] At least one metric is being optimized (not all stable)
- [ ] Probe set is up-to-date (retried easy probes recently?)
- [ ] NECTAR has no contradictions (spot-check last 10 entries)
- [ ] HONEY is procedural-first (spot-check: >75% are actionable rules?)

---

## Quick Command Reference

```bash
# One-time setup
cat > ~/.claude/hooks/state/membench-probes.json << 'EOF'
{probe set here}
EOF

# Run membench (automatic in eval harness)
python3 scripts/eval/eval_harness.py --membench --session $SESSION_ID

# View recent scores
jq '.[] | {ts, composite: .membench.composite}' \
  ~/.claude/hooks/state/eval-history.jsonl | tail -5

# Audit confabulation
jq '.membench.M8_confabulation_pct' \
  ~/.claude/hooks/state/eval-history.jsonl | tail -1

# Alert if composite < 50
jq -r '.membench.composite' \
  ~/.claude/hooks/state/eval-history.jsonl | tail -1 | \
  awk '{if ($1 < 50) print "CRITICAL: " $0}'
```

---

**Last updated:** 2026-04-21 | **Version:** v0.2.0
