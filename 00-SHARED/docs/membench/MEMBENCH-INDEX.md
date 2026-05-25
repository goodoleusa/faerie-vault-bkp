# Membench v0.2.0 — Documentation Index

**This field is brand new.** The following documents establish the complete framework for measuring memory-system health in faerie2.

**Navigation:** [Public Rubric](./MEMBENCH-PUBLIC-RUBRIC.md) | [Metrics Explanatory](./MEMBENCH-METRICS-EXPLANATORY.md) | [Quick Reference](./MEMBENCH-QUICK-REFERENCE.md) | [Visual Guide](./MEMBENCH-VISUAL-GUIDE.md) | [Strategy](./MEMBENCH-STRATEGY.md)

**Latest Scorecard:** [FAERIE-SCORECARD-2026-04-24](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md)

---

## The Core Documentation Stack

### 0. **MEMBENCH-PUBLIC-RUBRIC.md** (Canonical Scoring Framework)
**"How is membench scored?"**

- **Audience:** Anyone evaluating a memory system, researchers building on membench
- **Content:** Canonical membench rubric, scoring framework, M1-M11 definitions (canonical spec version)
- **Key sections:**
  - Metric weights and formulas
  - Composite score calculation
  - Veto gates (M8 > 5%, M11 < 70%)
  - Acceptance criteria for scorecards
  - Worked examples
- **When to read:** Before running membench on your system, to understand what's being measured
- **Key takeaway:** This is the authoritative scoring framework; all submissions reference it

---

### 1. **MEMBENCH-METRICS-EXPLANATORY.md** (4.8K)
**"What are we measuring and why?"**

- **Audience:** Data scientists, researchers, anyone building membench
- **Content:** Complete definition of all 11 metrics (M1–M11), rationale, optimization strategies
- **Key sections:**
  - M1 Retention — Can we retrieve facts?
  - M2 Relevance — Are facts actionable?
  - M3 Work Efficiency — **The ROI metric** (11:1 payoff)
  - M4 Overhead — Cost as % of tokens
  - M5 Continuity — Survives crashes?
  - M6–M11 — Diagnostic & safety gates
- **When to read:** If you're implementing new probes, understanding the science, or explaining membench to others
- **Key takeaway:** Baselines established (M3=1.31×, M8=0%, Composite=78.4)

---

### 2. **MEMBENCH-QUICK-REFERENCE.md** (2.4K)
**"What do I do right now?"**

- **Audience:** Operators, session leads, anyone running faerie
- **Content:** One-minute diagnostics, alert thresholds, commands
- **Key sections:**
  - Metrics at a glance (11-row table)
  - One-minute diagnostics ("Composite is dropping" → Check M3 first)
  - Production alerts (M8 >5%, M11 <70%, composite <50)
  - Command reference (bash one-liners)
  - Session checklist (before declaring done)
- **When to read:** During or after every session
- **Key takeaway:** Quick triage tool; know which metric to fix

---

### 3. **MEMBENCH-VISUAL-GUIDE.md** (3.1K)
**"How do I interpret these numbers?"**

- **Audience:** Everyone looking at membench output
- **Content:** Visual patterns, trend analysis, decision matrices
- **Key sections:**
  - Composite score gauge (0–100 color-coded)
  - Healthy vs concerning scorecards (example patterns)
  - Per-metric patterns (high/med/low interpretations)
  - 5-session trend analysis (stable? improving? declining?)
  - Real-world diagnosis example (you are here: composite 78.4)
  - Metric interaction matrix (which metrics affect each other?)
- **When to read:** When looking at a score and asking "Is this good?"
- **Key takeaway:** Pattern recognition; know what normal looks like

---

### 4. **MEMBENCH-STRATEGY.md** (3.2K)
**"Why does this matter to faerie2's mission?"**

- **Audience:** Founders, architects, strategic decision-makers
- **Content:** Connection between membench metrics and system design
- **Key sections:**
  - Strategic insight (memory as leverage multiplier, 11:1 ROI)
  - Each metric → architectural implication
  - How membench validates design decisions (model routing, monkeybranching, etc.)
  - 12-week optimization roadmap
  - The North Star (proof of agent superiority via membench)
  - Success criteria for Q2 2026
- **When to read:** Planning resource allocation, explaining faerie2 to stakeholders
- **Key takeaway:** Membench is the proof mechanism; without it, "agents improve" is opinion

---

## Live Scorecards (Implementation Examples)

### **faerie2 Scorecard (2026-04-24)**
See [2026-04-24_FAERIE-SCORECARD.md](../forensics/scorecards/2026-04-24_FAERIE-SCORECARD.md) for faerie2's current membench results:
- **Agents Returned:** 41 | **Wave State:** W2 Complete
- **Mutations Elevated:** 68% harmful (vs. baseline 36%)
- **Status:** Operational; Memory Promotion Ready

This scorecard serves as a reference implementation showing how to use the PUBLIC-RUBRIC to measure a live agent orchestration system.

---

## Quick Navigation by Role

### **If you're a...**

#### **Data Scientist**
→ Read METRICS-EXPLANATORY first
→ Then STRATEGY (understand ROI implications)
→ Use VISUAL-GUIDE for pattern recognition
→ QUICK-REFERENCE for operational checks

#### **Operator / Session Lead**
→ Start with QUICK-REFERENCE (what to do)
→ Consult VISUAL-GUIDE for interpretation
→ Refer to METRICS-EXPLANATORY if need details
→ STRATEGY is context (nice-to-know)

#### **Founder / Decision-Maker**
→ Read STRATEGY first (business case)
→ Skim METRICS-EXPLANATORY (the science)
→ Look at VISUAL-GUIDE diagnostics (is system healthy?)
→ QUICK-REFERENCE shows operational maturity

#### **Engineer Building Tools**
→ METRICS-EXPLANATORY (complete spec)
→ STRATEGY (architectural decisions)
→ VISUAL-GUIDE (expected output patterns)
→ QUICK-REFERENCE (common queries)

---

## Key Insights From This Documentation

### **1. M3 (Work Efficiency) is the Primary Metric**

**The data:** 11:1 ROI on memory tokens
- For every 100 agents spawned WITH memory, they complete ~115 effective tasks
- For every 100 agents spawned WITHOUT memory, they complete ~100 effective tasks
- Memory overhead: 2.8% of context per turn
- Payback ratio: 11× (save 11 agents' worth of work per 100 spawns)

**Why it matters:** This is the ONLY metric that matters for business. If M3 < 1.0, shut down the memory system.

---

### **2. Veto Gates Protect System Integrity**

**M8 (Confabulation) > 5% = VETO**
- If memory is lying to agents, everything downstream is poisoned
- One false fact ruins training for N agents that read it
- Zero tolerance: quarantine session, rollback immediately

**M11 (Bootstrap) < 70% = VETO**
- If agents crash during memory load, system is corrupted
- Can't trust any findings from that session
- Circuit breaker: blocks spawning until fixed

---

### **3. Baselines are Empirical, Not Theoretical**

**v0.2.0 baselines from real runs:**
```
M1 Retention:        88%    (88 of 100 facts findable)
M2 Relevance:        84%    (84% of HONEY is procedural)
M3 Efficiency:      1.31×   (31% more effective work with memory)
M4 Overhead:        2.8%    (memory costs 2.8% of context)
M5 Continuity:     100%    (perfect checkpoint recovery)
M6 Coordination:     34%    (34% of findings are cited by later agents)
M7 Crystallization:  82%    (HONEY is 82% efficient density)
M8 Confabulation:    0%    (zero false facts)
M9 Ceiling-Hit:      40%    (4–5 metrics at near-perfect)
M10 Coverage:       100%    (all 11 dimensions populated)
M11 Bootstrap:      100%    (no agent startup failures)

COMPOSITE:          78.4    (healthy, room to optimize)
```

These are NOT targets — they're **observations**. Over time, targets will evolve.

---

### **4. Optimization Has Diminishing Returns**

**Month 1 focus: M2 + M4 (highest leverage)**
- M2 from 78% → 85%: rewrite HONEY as procedures (1–2 hours)
- M4 from 2.8% → 2.5%: archive old NECTAR (30 minutes)
- Expected result: Composite 78.4 → 82–84

**Month 2+ focus: Monitoring, not tweaking**
- Once baselines stabilize, focus shifts to detecting degradation
- Monthly trend analysis (is composite trending down? investigate)
- Quarterly probe set refresh (retire easy probes, add harder ones)

---

### **5. Memory Compounding Requires Coordination**

**The leverage only works if agents USE memory:**
- M6 (Coordination) is observational (tracks if agents cite findings)
- Low M6 → agents don't know to search NECTAR → no compounding
- Fix: explicit spawn prompts ("Check NECTAR for related findings")

**This is NOT automatic.** Agents must be told to look.

---

## How to Use This Documentation

### **Setting Up Membench (First Time)**

1. **Read STRATEGY** (5 min) — understand why this matters
2. **Read METRICS-EXPLANATORY** (15 min) — learn all 11 metrics
3. **Create probe set** (30 min) — 10 domain-relevant facts
4. **Run baseline session** (1–2 hours) — capture initial composite
5. **Review VISUAL-GUIDE** (5 min) — learn pattern recognition

**Total: ~2 hours to full membench maturity**

---

### **Running Membench Every Session (Ongoing)**

1. **At session end:** `python3 scripts/eval/eval_harness.py --membench` (automatic)
2. **Check alerts:** View QUICK-REFERENCE; any veto gates triggered?
3. **Review trends:** Compare to last 5 sessions (is composite stable? improving? declining?)
4. **Identify next optimization:** Which metric is lowest? (Use decision matrix from VISUAL-GUIDE)

**Total: ~5 minutes/session (mostly automated)**

---

### **Monthly Reviews (Process Checkpoint)**

1. **Trend analysis:** Graph composite across last 30 sessions
2. **Metric breakdown:** Which metrics improved? Which degraded?
3. **Root cause:** If M1 dropped, why? (NECTAR archived? Probe set changed?)
4. **Next priority:** Based on bottleneck (use STRATEGY roadmap)

**Total: ~30 minutes/month**

---

### **Quarterly Updates (System Refresh)**

1. **Probe set audit:** Retire probes scoring 100%; add harder ones
2. **Baseline reset:** Document new baselines for trending (e.g., "baseline now 80, not 78")
3. **Architecture review:** Did system changes affect membench? (e.g., new crystallization rules)
4. **Founder update:** Show composite trend + M3 ROI data (proof of compounding)

**Total: ~2 hours/quarter**

---

## Critical Thresholds

| Metric | Status Light | Action |
|--------|---|---|
| Composite **< 50** | 🔴 CRITICAL | INVESTIGATE IMMEDIATELY |
| Composite **50–70** | 🟡 RISKY | Schedule optimization |
| Composite **70–90** | 🟢 HEALTHY | Maintain, small tweaks OK |
| Composite **>90** | 🟩 EXCELLENT | System is mature |
| M8 **> 5%** | 🔴 VETO | Block spawning; quarantine |
| M11 **< 70%** | 🔴 VETO | Block spawning; rollback |
| M5 **< 90%** | 🟡 RISKY | Auto-compact unsafe |
| M1 **< 70%** | 🟡 RISKY | Facts are evaporating |
| M3 **< 1.0** | 🟡 RISKY | Memory is slowing agents |
| M4 **> 4%** | 🟡 RISKY | Overhead creeping up |

---

## The Document Hierarchy

```
MEMBENCH-PUBLIC-RUBRIC.md
  (canonical spec)
  ├─→ M1–M11 metric definitions
  ├─→ Scoring formulas
  ├─→ Veto gates
  └─→ Acceptance criteria

        ↓

MEMBENCH-STRATEGY.md
  ↑ (answers "why?")
  │
  ├─→ MEMBENCH-METRICS-EXPLANATORY.md
  │   (answers "what?" in detail)
  │   ├─→ M1–M11 definitions + rationale
  │   ├─→ optimization strategies
  │   └─→ FAQ
  │
  ├─→ MEMBENCH-VISUAL-GUIDE.md
  │   (answers "how do I interpret this?")
  │   ├─→ pattern recognition
  │   ├─→ trend analysis
  │   └─→ decision trees
  │
  └─→ MEMBENCH-QUICK-REFERENCE.md
      (answers "what do I do NOW?")
      ├─→ one-minute diagnostics
      ├─→ command reference
      └─→ session checklist

        ↓

Live Scorecards (e.g., FAERIE-SCORECARD-2026-04-24.md)
  (implementation reference)
  ├─→ Measures against PUBLIC-RUBRIC
  ├─→ Real system data
  └─→ Metric results

MEMBENCH-INDEX.md (this document)
  ↑ (navigation hub + orientation)
```

---

## FAQ

### **Q: Do I need to read all four documents?**

**A:** No. Pick based on your role:
- **Operator?** → QUICK-REFERENCE + VISUAL-GUIDE
- **Scientist?** → METRICS-EXPLANATORY + STRATEGY
- **Founder?** → STRATEGY + VISUAL-GUIDE
- **Engineer?** → METRICS-EXPLANATORY + QUICK-REFERENCE

---

### **Q: How often should I check membench?**

**A:** Automatic every session (eval_harness runs it). Manual review:
- **Daily:** Check for veto gates (M8 >5%, M11 <70%)
- **Weekly:** Review trend (composite trending down?)
- **Monthly:** Deep analysis (which metric bottleneck?)
- **Quarterly:** Update probe set + baselines

---

### **Q: What if my composite doesn't match the v0.2 baseline (78.4)?**

**A:** Normal. Baselines vary by:
- **Domain** (faerie2 domain ≠ investigation domain)
- **Probe set** (different probes = different results)
- **Session length** (5-agent session ≠ 50-agent session)
- **Memory age** (fresh NECTAR ≠ 100-session-old NECTAR)

Establish YOUR baseline first, then optimize from there.

---

### **Q: Can I optimize multiple metrics at once?**

**A:** Yes, but **prioritize by weight:**
1. **M3 (Efficiency, 30% weight)** — always
2. **M1 (Retention, 25% weight)** — if M3 is OK
3. **M2 (Relevance, 20% weight)** — if M1/M3 are OK
4. **M5 (Continuity, 15% weight)** — gate (must be >95%)
5. **M4 (Overhead, 10% weight)** — last

---

### **Q: What does "NECTAR trimmed to tail-500 lines" mean for M1?**

**A:** M1 (Retention) searches NECTAR tail-500 (last 500 lines only), not all of NECTAR. This means:
- **Fresh findings** (last 500 lines) are fully searchable
- **Old findings** (>500 lines ago) are archived (not in M1 probe set)
- **M1 measures active memory**, not historical

If you want to measure long-term retention, increase tail size in eval_membench.py.

---

## Getting Help

### **Metric confused?**
→ METRICS-EXPLANATORY has 2–3 page explanation per metric

### **Score looks weird?**
→ VISUAL-GUIDE has decision matrix ("When situation X, do Y")

### **Need to decide what to optimize?**
→ STRATEGY has 12-week roadmap + priority sequencing

### **Need a command to check something?**
→ QUICK-REFERENCE has bash one-liners for common queries

### **Don't understand baseline values?**
→ METRICS-EXPLANATORY has detailed baseline rationale

---

## Version History

| Version | Date | What Changed |
|---------|------|--------------|
| **v0.2.0** | 2026-04-21 | Complete documentation + 4-document stack |
| **v0.1.0** | (historical) | Initial membench implementation |

---

**Document version:** v0.2.0 | **Date:** 2026-04-21 | **Status:** Complete documentation ready for production use

---

## Next Session

When you run membench next, refer back to this index:
1. Check QUICK-REFERENCE for alerts
2. Consult VISUAL-GUIDE to interpret scores
3. Use STRATEGY to plan optimizations
4. Read METRICS-EXPLANATORY if you need to understand a specific metric in detail

The system is ready. Let's measure.
