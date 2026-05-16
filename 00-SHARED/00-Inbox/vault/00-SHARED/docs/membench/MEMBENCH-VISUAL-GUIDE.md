# Membench v0.2.0 — Visual Interpretation Guide

**Navigation:** [INDEX](./MEMBENCH-INDEX.md) | [Public Rubric](./MEMBENCH-PUBLIC-RUBRIC.md) | [Metrics Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md) | [Strategy](./MEMBENCH-STRATEGY.md)

**Scorecard:** [2026-04-24](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md)

**This guide translates membench scores into actionable patterns.**

---

## The Composite Score Gauge

```
0%                    50%                    75%                   100%
|-------|-------|-------|-------|-------|-------|-------|-------|
  RED              YELLOW               GREEN                 PERFECT
 FAIL             CAUTION               GOOD                 EXCELLENT

< 50    50-70     70-90      90-100
BROKEN  RISKY     HEALTHY    OPTIMAL
```

**Your score: 78.4** → GREEN zone (healthy, small optimizations needed)

---

## The Weight Distribution

```
Membench Composite Score = Weighted Sum

M1: Retention ████████████░░░░░░░░░░░░░░░░░░░░░░░░░ (25%)
   ↳ Can we find what we wrote?

M2: Relevance ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (20%)
   ↳ Are facts actionable?

M3: Efficiency ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (30%) ← HIGHEST
   ↳ How much value per token?

M4: Overhead █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (10%)
   ↳ What % is memory tax?

M5: Continuity ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ (15%)
   ↳ Survives crashes?

M6, M7, M8, M9, M10, M11: Diagnostic / Veto
```

**Key insight:** M3 (Work Efficiency) has the most weight (30%) because it measures **ROI**.

---

## Reading the Metric Scorecard

### **Healthy Scorecard (Your Current State)**

```
SESSION MEMBENCH REPORT — 2026-04-21T14:32:00Z
═══════════════════════════════════════════════

🟢 M1 Retention:       92% ✓ (facts retrievable)
🟢 M2 Relevance:       78% ⚠ (slight narrative bloat)
🟢 M3 Efficiency:     1.31× ✓ (saves work; 11:1 ROI)
🟢 M4 Overhead:       2.8% ✓ (lean; well under 3% tax)
🟢 M5 Continuity:    100% ✓ (perfect checkpoint recovery)
🟡 M6 Coordination:    34% ℹ (agents building on findings)
🟢 M7 Crystallization: 82% ✓ (HONEY density good)
🟢 M8 Confabulation:   0% ✓ (forensically clean)
🟡 M9 Ceiling-Hit:     40% ℹ (4–5 metrics mature)
🟢 M10 Coverage:      100% ✓ (all dimensions populated)
🟢 M11 Bootstrap:     100% ✓ (no startup failures)

COMPOSITE:  78.4 / 100  [HEALTHY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERDICT:  ✓ System operational. Next focus: M2 (procedural goals)
TREND:    STABLE (no degradation last 5 sessions)
ALERT:    None
```

---

## M1 Retention Patterns

### **High Retention (85%+) ✓**
```
Facts in HONEY/NECTAR: ████████████████████ 85%+
Scenario: System is stable, facts don't evaporate
Action: Maintain. Regular crystallization sufficient.
```

### **Medium Retention (60–85%) ⚠**
```
Facts in HONEY/NECTAR: ███████████░░░░░░░░░░ 70%
Scenario: Some facts are aging out or superseded
Action: Archive old NECTAR entries; consolidate duplicates
```

### **Low Retention (<60%) 🔴**
```
Facts in HONEY/NECTAR: ██░░░░░░░░░░░░░░░░░░ 20%
Scenario: Memory is lossy; critical facts evaporating
Action: Investigate git history; restore from backup
```

---

## M2 Relevance Patterns

### **Procedural-Heavy (>85%) ✓**
```
HONEY Example:
- ALWAYS write pollen before returning
- Crystallize after 3+ sessions with validation
- Model default: Haiku W1, Sonnet W2 feature work

Score: 100% relevant (every line is a decision rule)
```

### **Mixed (60–85%) ⚠**
```
HONEY Example:
- ALWAYS write pollen before returning
- The faerie system is complex and uses multiple layers
- Crystallize after 3+ sessions with validation
- Memory is important for agent coordination

Score: 67% relevant (50% procedural, 50% narrative)
Action: Remove narrative lines; keep only rules.
```

### **Narrative-Heavy (<60%) 🔴**
```
HONEY Example:
- The faerie system has many moving parts
- Memory layers help agents work together
- Evaluation is an important part of the system
- Training queues hold work for agents to claim

Score: 0% relevant (all narrative, no rules)
Action: Rewrite as procedures or archive to NECTAR.
```

---

## M3 Efficiency Patterns

### **High Efficiency (>1.3×) ✓**
```
Ratio: ████████████████████ 1.5×
Interpretation:
  - For every 100 agents spawned, memory saves 15 redundant spawns
  - ROI: ~11:1 across sessions (baseline data)
  - Memory is earning its 2.8% overhead cost ✓

Action: Maintain current memory practices; optimize M2.
```

### **Baseline Efficiency (1.0–1.3×) ⚠**
```
Ratio: ████████░░░░░░░░░░░░░░ 1.1×
Interpretation:
  - Memory saves ~10% of spawn time
  - Marginal benefit; overhead is barely justified
  
Action: Compress HONEY/NECTAR; remove low-value findings.
```

### **Negative Efficiency (<1.0×) 🔴**
```
Ratio: ░░░░░░░░░░░░░░░░░░░░░░ 0.95×
Interpretation:
  - Memory is SLOWER than no memory
  - Agents waste time reading irrelevant facts
  
Action: STOP. Disable NECTAR reads for next session. Investigate why.
```

---

## M4 Overhead Patterns

### **Lean (1–2.5%) ✓**
```
Overhead: ██░░░░░░░░░░░░░░░░░░░░ 2.0%
Interpretation:
  - HONEY (~2K) + NECTAR tail (~1.5K) = ~3.5K loaded per turn
  - With 7.5K context per agent spawn, 2% overhead is acceptable
  
Action: Keep current structure. Archive old NECTAR when >15K.
```

### **Acceptable (2.5–3.5%) ⚠**
```
Overhead: ███░░░░░░░░░░░░░░░░░░ 3.0%
Interpretation:
  - Still under 3.5% threshold
  - But creeping up; compression needed soon
  
Action: Archive NECTAR tail entries >200 lines. Run `/crystallize`.
```

### **Bloated (>4%) 🔴**
```
Overhead: ████████░░░░░░░░░░░░░░ 4.5%
Interpretation:
  - Memory is consuming 4.5% of every agent's context
  - At that cost, agents better be saving >4.5% work (they're not)
  
Action: URGENT. Archive old NECTAR. Compress HONEY to <3K lines.
```

---

## M5 Continuity Patterns

### **Perfect (100%) ✓**
```
Checkpoints: ████████████████████ 100%
Graph:
  Cycle 1 → CHECKPOINT_001 ✓
  Cycle 2 → CHECKPOINT_002 ✓
  Cycle 3 → CHECKPOINT_003 ✓
  Auto-compact → Resume → All checkpoints present ✓

Interpretation: System is bulletproof; auto-compact is safe.
```

### **Good (95–99%) ⚠**
```
Checkpoints: ███████████████████░░ 97%
Graph:
  Cycle 1 → CHECKPOINT_001 ✓
  Cycle 2 → CHECKPOINT_002 ✓
  Auto-compact → Resume → CHECKPOINT_001 ✓, CHECKPOINT_002 ✗

Interpretation: Minor data loss (<5%); acceptable if M1 is high.
Action: Run backup before next auto-compact. Git-track NECTAR.
```

### **Poor (<90%) 🔴**
```
Checkpoints: ██████░░░░░░░░░░░░░░░░ 60%
Interpretation:
  - 40% of findings lost after compact
  - NECTAR is not persisting correctly
  
Action: CRITICAL. Investigate memory write paths. Check git logs.
```

---

## M6 Coordination Patterns

### **Good Coordination (>30%) ✓**
```
Builds-on events: ████████░░░░░░░░░░░░░░ 34%
Timeline:
  Agent A: "training-queue was dark 36 days"
  Agent B: "I see that. Now let's look at the fix..."  ← builds_on
  Agent C: "Actually, queue is still slow" ← contradicts (still coordination)

Interpretation: Agents are reading NECTAR and building on findings.
```

### **Weak Coordination (10–30%) ⚠**
```
Builds-on events: ████░░░░░░░░░░░░░░░░░░ 15%
Interpretation:
  - Agents find NECTAR but don't cite it
  - OR agents don't think to search NECTAR
  
Action: Update spawn prompts: "Before solving, check NECTAR for prior work."
```

### **No Coordination (0%) 🔴**
```
Builds-on events: ░░░░░░░░░░░░░░░░░░░░░░ 0%
Interpretation:
  - Agents aren't reading NECTAR at all
  - Memory system is a silo
  
Action: URGENT. Update spawn prompts. Verify NECTAR is readable.
```

---

## M8 Confabulation Patterns

### **Clean (0–2%) ✓**
```
False facts: ░░░░░░░░░░░░░░░░░░░░░░ 0%
Interpretation:
  - HONEY/NECTAR contain no contradictions
  - Findings are forensically sound
  - Safe to train agents on these facts
```

### **Minor Issues (2–5%) ⚠**
```
False facts: ██░░░░░░░░░░░░░░░░░░░░ 3%
Interpretation:
  - 1–2 contradictory statements in corpus
  - Example: "training-queue active" + "training-queue dark" in same NECTAR tail
  
Action: Audit recent NECTAR entries. Choose authoritative version. Archive the other.
```

### **Veto (>5%) 🔴**
```
False facts: ██████░░░░░░░░░░░░░░░░ 8%
Interpretation:
  - Memory is corrupted
  - Agents trained on lies
  - All findings from this session are suspect

Action: IMMEDIATE. Quarantine session. Rollback NECTAR to last known-good. Investigate.
```

---

## Trend Analysis (5-Session Window)

### **Healthy Trend (Stable)**
```
Session 1: Composite 76
Session 2: Composite 78
Session 3: Composite 79  ← slight improvement
Session 4: Composite 78
Session 5: Composite 78  ← stable, no drift

Graph:
  79 │  •
  78 │  • • •
  77 │
  76 │•
      └─────────
      Improvement with stability = HEALTHY
```

### **Improvement Trend (Optimizing) ✓**
```
Session 1: Composite 70
Session 2: Composite 72
Session 3: Composite 75  ← improving
Session 4: Composite 77
Session 5: Composite 78

Graph:
  78 │        •
  77 │      •
  76 │
  75 │    •
  74 │
  72 │  •
  70 │•
      └─────────
      Consistent improvement = GOOD WORK
```

### **Declining Trend (Degrading) 🔴**
```
Session 1: Composite 82
Session 2: Composite 81
Session 3: Composite 77  ← declining
Session 4: Composite 74
Session 5: Composite 72

Graph:
  82 │•
  81 │  •
  80 │
  77 │      •
  74 │        •
  72 │          •
      └─────────
      Consistent decline = INVESTIGATE IMMEDIATELY
```

---

## Decision Matrix: What to Do When

| Situation | Indicator | Action |
|-----------|-----------|--------|
| **Composite is good but M2 low** | M2 < 70%, rest OK | Rewrite HONEY as procedures |
| **Composite dropping, M3 stable** | Composite ↓, M3 flat | Check M4/M5 (overhead/continuity issues) |
| **Composite dropping, M3 dropping** | Both ↓ | Memory is losing value; measure without for comparison |
| **M8 spiking** | M8 > 2% | Audit NECTAR for contradictions |
| **M8 veto** | M8 > 5% | STOP. Quarantine session. Rollback memory. Investigate. |
| **M1 dropping fast** | M1 < 70% | Check git log; restore from backup or archive |
| **M4 creeping up** | M4 > 3.5% | Archive old NECTAR. Compress HONEY. |
| **All metrics high, composite stuck** | All >85%, composite 75–80 | System is mature; diminishing returns. Accept current state. |
| **M11 < 70%** | Agent crashes > 30% | STOP. Memory corruption detected. Rollback immediately. |

---

## Real-World Example: Diagnosis

**Your membench report shows:**
```
Composite: 78.4 (HEALTHY)
M1: 92% ✓ (facts findable)
M2: 78% ⚠ (some narrative)
M3: 1.31× ✓ (good efficiency)
M4: 2.8% ✓ (lean)
M5: 100% ✓ (perfect recovery)
M8: 0% ✓ (clean)
```

**Diagnosis:**
- System is healthy and efficient
- No critical issues (M8/M11 are safe)
- M2 is the only weakness (some HONEY is narrative instead of procedural)

**Recommended action (this session):**
1. Audit HONEY for narrative sections (lines like "Memory is important")
2. Rewrite as procedural rules ("Always check NECTAR before solving")
3. Next session, expect M2 → 85%+ and composite → 80–82

**Expected outcome:** Small improvement with minimal effort.

---

## Advanced: Metric Interaction Matrix

```
           M1  M2  M3  M4  M5  M6
M1 Ret   │ 1  ↑↑  ↑   ↓   ↑   ↑
M2 Rel   │ ↑↑  1  ↑↑  ↓   ↑   ↑
M3 Eff   │ ↑  ↑↑  1  ↓↓  ↑   ↑
M4 OH    │ ↓  ↓  ↓↓  1  ↑   ↓
M5 Cont  │ ↑  ↑   ↑  ↑   1   ↑↑

Legend: ↑ = positive correlation
        ↓ = negative correlation
        ↑↑ = strong positive
        ↓↓ = strong negative
        1 = self (diagonal)
```

**Key insights:**
- **M3 ↔ M2:** High relevance (procedural) drives efficiency (agents find what they need)
- **M3 ↔ M4:** Low overhead drives high efficiency (less memory tax = more useful)
- **M5 ↔ M6:** Good continuity enables coordination (facts survive, agents cite them)

**Implication:** Optimizing M2 (relevance) and M4 (overhead) yields biggest M3 (efficiency) gains.

---

**Last updated:** 2026-04-21 | **Version:** v0.2.0
