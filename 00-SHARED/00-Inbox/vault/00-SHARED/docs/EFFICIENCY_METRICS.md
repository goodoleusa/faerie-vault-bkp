# Faerie2 Efficiency Metrics — Scientific Measurement of Optimization Impact

## Overview

Faerie2's competitive advantage is **continuous training + stigmergic optimization**. These five orthogonal efficiency dimensions prove the system earns its operational overhead.

Every agent spawn produces measurable evidence that the system is getting smarter, cheaper, and more efficient.

---

## The Five Dimensions

### 1. Token Burn Rate (Efficiency Ratio)

**What:** Useful outputs per 1,000 tokens consumed.

**Formula:**
```
efficiency = (tasks_completed + findings_produced) / (tokens_consumed / 1000)
```

**Why it matters:**
- Baseline (vanilla Claude): 0.5–1.0 outputs/1K tokens
- Faerie2 target: 2.0–3.5 outputs/1K tokens
- With memory system: 3.5–5.0 outputs/1K tokens (11:1 payback drives the multiplier)

**Measurement:** `9x_session_metrics.py` collects `context_efficiency` at session end.

**What drives improvement:**
- Better prompts (from HONEY learnings)
- Focused problem decomposition (agents don't re-solve solved problems)
- NECTAR cross-references prevent redundant research

---

### 2. Stigmergy Multiplier

**What:** Queue auto-completion savings vs. flat agent launch cost.

**Formula:**
```
multiplier = (manifests_returned / agents_spawned) × 11
```

The `11` comes from memory payback: each agent that succeeds without re-exploration saves ~11 agents downstream the same exploration cost.

**Why it matters:**
- Flat launch cost: ~15K tokens per agent (full context reload)
- Stigmergic flow: shared queue → no re-spawning same task → 11:1 memory multiplication
- Session-level measurement: completion_rate (returned/spawned) tells you how well coordination is working

**Example:**
- 10 agents spawned, 8 returned manifests: completion_rate = 0.8
- multiplier = 0.8 × 11 = 8.8× payback
- Estimated tokens saved: (10 - 8) × 15K = 30K tokens

**Measurement:** `9x_statusline_enhanced.py` reads `stigmergy.multiplier` from efficiency log.

---

### 3. Wave Coordination ROI

**What:** Piston overhead vs. baseline sequential agent spawning.

**Formula:**
```
flat_cost = N_agents × 15K tokens (sequential, full context per agent)
piston_cost = 3K fixed overhead + N_agents × 8K tokens (reduced context via piston)
roi = flat_cost / piston_cost
```

**Why it matters:**
- Proves piston wave coordination pays for itself
- ROI > 1.0 means piston saves tokens
- ROI > 2.0 means waves are compounding efficiency (W1 results feed W2 with reduced overhead)

**Example:**
- 6 agents total across 3 waves
- Flat: 6 × 15K = 90K tokens
- Piston: 3K + (6 × 8K) = 51K tokens
- ROI = 90/51 = 1.76×

**Bonus:** Surfacing quality metric tracks % of returns arriving in productive windows (not near auto-compact). High surfacing quality (>80%) means piston timing is optimal.

**Measurement:** `9x_efficiency_metrics.py` computes wave ROI; `9x_statusline_enhanced.py` displays it.

---

### 4. Memory Substrate Contribution

**What:** Progress toward 11:1 NECTAR payback ratio.

**Formula:**
```
nectar_growth_ratio = nectar_entries / agents_spawned
target = 0.1 (1 entry per 10 agents)
health = "healthy" if ratio >= 0.1 else "building"
```

**Why it matters:**
- Every NECTAR entry is a learnable fact that future agents can use
- Target ratio (0.1) means you're creating ~1 reusable finding per 10 agent runs
- Ratio < 0.1 = system is still building knowledge (expected early)
- Ratio > 0.15 = knowledge generation exceeds agent consumption (scaling mode)

**Quality signal:**
- Low ratio + high efficiency = agents solving novel problems (good, but no learning accumulation)
- High ratio + high efficiency = agents generating reusable insights (optimal)

**Measurement:** `9x_efficiency_metrics.py` samples NECTAR.md and measures growth.

---

### 5. Training Velocity

**What:** On-the-job eligible agents marked/redeemed per cycle.

**Formula:**
```
velocity = redeemed_on_the_job / on_the_job_eligible
redemption_rate = (redeemed / eligible) × 100%
```

**Why it matters:**
- Faerie2's continuous training loop: agents beat baseline → marked eligible → redeemed in next spawn
- Velocity > 0 = system is learning in real-time
- High velocity (>50%) = training queue flowing well, agents improving faster than baseline drift

**Example:**
- 8 agents marked on_the_job_eligible (beat baseline recently)
- 4 agents redeemed this session (spawned + beat baseline again)
- velocity = 4/8 = 0.5 (50% redemption rate)

**Business implication:**
- 0% velocity = no continuous improvement (system stalled)
- 30–50% velocity = healthy learning (baseline being beaten regularly)
- >50% velocity = rapid improvement (unusual, requires very clean problem signals)

**Measurement:** `9x_training_queue_manager.py` reads training-queue.json; `9x_efficiency_metrics.py` computes velocity.

---

## Statusline Integration

### Original Statusline
```
[########] 65% done | ctx:42%^ ORB r:3 d:2 | Opus $1.23 | 2hi 5q (main)
```

### Enhanced with Efficiency Metrics
```
[########] 65% done | ctx:42%^ ORB r:3 d:2 | Opus $1.23 | 2hi 5q (main)
[piston | w2 | eff 0.85× | stig +23% | roi 1.2× | train ↑12%]
```

**Breaking down the second line:**
- `piston` — wave coordination active
- `w2` — currently in Wave 2 execution
- `eff 0.85×` — token efficiency at 0.85 outputs/1K tokens
- `stig +23%` — stigmergy multiplier at 1.23× (23% above baseline)
- `roi 1.2×` — wave piston paying back 1.2× vs sequential
- `train ↑12%` — training velocity at 12% per cycle (12% of eligible agents redeemed)

**Interpretation for operator:**
- Low eff (< 0.5) + high stig (> 1.5) = memory system working, but inference expensive (need better prompts)
- High eff (> 1.5) + low stig (< 1.1) = good local performance, but not accumulating knowledge
- High eff + high stig = optimal: learning + efficiency compounding

---

## Collection & Reporting

### Automatic Collection
```bash
# Called at each turn (hookable)
python3 9x_efficiency_metrics.py --collect
→ writes to ~/.claude/hooks/state/efficiency-metrics.jsonl
→ one-liner JSON per snapshot
```

### Statusline Display
```bash
# Integrated into statusline (reads latest snapshot)
python3 9x_statusline_enhanced.py
→ line 1: original statusline
→ line 2: efficiency metrics headline
```

### Deep-Dive Dashboard
```bash
# For analysis & optimization
python3 9x_efficiency_metrics.py --dashboard
→ renders all five dimensions with detailed breakdown
→ useful for debugging why efficiency dropped
```

### Historical Report
```bash
# Track trends over time
python3 9x_efficiency_metrics.py --report --days 7
→ aggregates snapshots, shows averages
→ detects drift in token efficiency, stigmergy multiplier, etc.
```

---

## Files & Integration Points

| File | Role | Hook | Trigger |
|------|------|------|---------|
| `9x_efficiency_metrics.py` | Core measurement engine | – | Called at turn start or end |
| `9x_statusline_enhanced.py` | Display + integration | StatusLine | Every turn (reads efficiency log) |
| `efficiency-metrics.jsonl` | Append-only log | – | Written by `--collect` command |
| `session-metrics.jsonl` | Session context (cost, tokens) | Stop hook | Session end |
| `training-queue.json` | Training state | – | Read for velocity calculation |
| `subagent-roster.json` | Agent completion tracking | – | Read for stigmergy calculation |

### Hookup in settings.json

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 /path/to/9x_statusline_enhanced.py"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/9x_efficiency_metrics.py --collect"
          }
        ]
      }
    ]
  }
}
```

---

## Business Implications

Every agent spawn produces one efficiency snapshot. Over a sprint:

**Week 1 (building):**
- eff: 0.6–0.8× (agents learning from HONEY + NECTAR)
- stig: 1.1–1.3× (completion rate 10–30%)
- roi: 1.2–1.5× (piston covers its overhead)
- train: 5–10% (early agents beat baseline)
- nectar_ratio: 0.05–0.08 (building knowledge base)

**Week 4 (scaling):**
- eff: 1.5–2.0× (HONEY dense, NECTAR deep)
- stig: 2.0–2.5× (completion rate 60–70%, queue flows)
- roi: 2.0–3.0× (waves compounding)
- train: 20–30% (steady improvement cycle)
- nectar_ratio: 0.12–0.18 (knowledge exceeds consumption)

**Proof point for founder:** Month 4, show investor:
```
Session Metrics (30-day aggregate):
  - Token efficiency improved 250% (0.6× → 1.8×)
  - Stigmergy multiplier grew from 1.2× to 2.3×
  - Wave ROI at 2.1× (saves 30K tokens per wave)
  - Training velocity steady 25% (agents beating baseline regularly)
  - Memory contribution at 0.15 (knowledge growing faster than agent consumption)

Translation: Every $1 spent on agents now generates $2.10 in coordinated output.
Memory overhead (11:1 ratio) proving out in practice.
```

---

## Implementation Checklist

- [ ] `9x_efficiency_metrics.py` deployed and collecting
- [ ] `9x_statusline_enhanced.py` hooked into statusline
- [ ] `efficiency-metrics.jsonl` being appended (check first entry after deploy)
- [ ] Dashboard tested (`--dashboard` flag shows all five dimensions)
- [ ] Historical tracking working (`--report` shows trends)
- [ ] Founder briefed on meaning + how to read metrics
- [ ] Monthly snapshot scheduled (track metrics growth over time)

---

## FAQ

**Q: Why measure efficiency at all?**
A: Proof. Every agent spawn is evidence. Vanilla Claude can't show this. Competitors' evals are sideline. Faerie2's continuous measurement is the product.

**Q: What's the target range?**
A: Month 1–2: eff 0.5–1.0, stig 1.1–1.3, roi 1.2–1.5. Month 3–4: eff 1.5–2.5, stig 2.0–3.0, roi 2.0–3.5. Scaling: eff > 2.0, stig > 2.5, roi > 2.5.

**Q: What if efficiency drops?**
A: Dashboard + historical report will tell you why. Usually: (1) NECTAR not growing (agents not learning), (2) completion rate dropped (stigmergy broken), (3) context% rising (rounds expended). Use metrics to diagnose.

**Q: Can these be gamed?**
A: Harder than single metrics. All five must improve together. Can't boost eff without stig. Can't grow stig without training velocity. Orthogonal dimensions prevent Goodhart's law.

---

**Document Version:** 2026-04-21  
**Status:** Ready for deployment  
**Integration Point:** Settings.json + Turn 0 dashboard
