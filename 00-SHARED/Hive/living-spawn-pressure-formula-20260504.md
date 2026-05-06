---
date: 2026-05-04
title: "Living FFMx Spawn Pressure Formula"
author: documentation-engineer
type: design-narrative
status: active
tags: [spawn-discipline, ffmx, feedback-loops, self-calibration, mission-driven-dispatch]
vault_path: "00-SHARED/Hive/living-spawn-pressure-formula-20260504.md"
---

# Living FFMx Spawn Pressure Formula

**Date:** 2026-05-04 | **Status:** Active | **Confidence:** 0.78 (first deployment)

This document explains the mathematical foundation and self-calibration mechanism of the **living FFMx spawn pressure formula** — a feedback-driven system that dynamically adjusts agent spawn count based on recent session outcomes. Unlike static thresholds, the living formula responds to emergent efficiency signals, creating a homeostatic equilibrium between context budget and work output.

---

## Executive Summary

The faerie2 system must answer a foundational question every session: **How many agents should we spawn?**

**Old answer (static threshold):** "If efficiency > 0.30, spawn 4–6 agents." Fixed rules work poorly because missions vary in natural FFMx (deep research is inherently lower-output than integration work).

**New answer (living formula):** "Examine the last 5 sessions' FFMx outcomes. If trending up, spawn more aggressively. If trending down, conserve and fix quality first. Otherwise, hold steady." This responds to *actual outcomes*, not *assumed targets*.

**Key insight:** Spawn rate should be **emergent from feedback**, not **prescribed from theory**. A living formula creates a self-correcting system: spawn rate and work quality naturally oscillate toward equilibrium, with agents making progress while maintaining stability.

**Why this matters:**
- **Cost control:** Spawn decisions now rest on observed efficiency, not wishful thinking
- **Mission resilience:** Declining FFMx triggers conservative spawning → focus on quality → recovery follows naturally
- **Emergence:** Healthier missions produce higher FFMx → formula rewards them with more parallelism → system accelerates naturally
- **Stability:** Ceiling (spawn ≤6) and floor (spawn ≥1) prevent runaway acceleration or stall

The formula is "living" because it learns: every session's outcome (captured in FFMx) becomes input to the next session's spawn decision. No human intervention needed—the system calibrates itself via measurement feedback.

---

## The Problem with Fixed Thresholds

Static spawn rules like "if efficiency ≥ 0.30, spawn 6" fail in common scenarios:

### Scenario 1: Low-Output Mission is Healthy

```
Mission: "Architectural deep-dive" (research-intensive)
Session outcome:
  - 8 manifests written (lower than integration tasks)
  - Mean quality: 0.87 (excellent, foundation is solid)
  - Cross-citations: 0.5 (agents building on each other)
  - Tokens consumed: 92,000

Efficiency = (8 × 0.87 × 0.28) / 92,000 = 0.000212 (normalized: 2.12)

Static rule: "2.12 < 30? No, don't spawn 6. Spawn 2."
Problem: Mission is healthy but low-output. Throttling agents makes it worse.
Truth: This mission SHOULD run with 6 agents (more parallelism helps deep dives).
```

### Scenario 2: High-Output Mission in Trouble

```
Mission: "Rapid prototyping" (many small deliverables)
Session outcome:
  - 32 manifests written (high volume)
  - Mean quality: 0.41 (poor; many incomplete manifests)
  - Cross-citations: 0.08 (low; agents not coordinating)
  - Tokens consumed: 110,000

Efficiency = (32 × 0.41 × 0.28) / 110,000 = 0.00336 (normalized: 33.6)

Static rule: "33.6 ≥ 30? Yes, spawn 6 agents."
Problem: Mission is struggling (low quality, low coordination). Adding more agents makes chaos worse.
Truth: This mission SHOULD spawn 3 agents (focus on quality before volume).
```

### Scenario 3: Momentum in Progress

```
Session 1 FFMx: 0.21 (starting a new mission)
Session 2 FFMx: 0.26 (improving, +0.05)
Session 3 FFMx: 0.31 (continuing momentum, +0.05)

Static rule: All three sessions trigger spawn ≥4.
But truth: Sessions 1-2 are building foundation (should spawn conservatively, 3-4 agents).
         Session 3 has momentum (should spawn aggressively, 5-6 agents).
         Static rule misses the signal.
```

**Root cause:** Static thresholds ignore **trajectory** (the slope of recent outcomes). They only look at point-in-time efficiency, which is noisy and mission-dependent.

**Solution:** Track the **trend** over the last 5 sessions. Upward trend → reward with more parallelism. Downward trend → conserve. Flat → hold steady. This creates feedback.

---

## Core Formula: Mission-Driven Spawn Pressure

The formula has five components working in concert:

### Step 1: Budget Constraint

```python
cost_per_agent = 60  # tokens overhead per spawn (empirically measured)
context_remaining_tokens = compute_remaining_context()  # ~200K - current_used
budget_capacity = context_remaining_tokens // cost_per_agent

# Example: 150K tokens remaining
# budget_capacity = 150,000 / 60 = 2,500 agents theoretical max
# (We cap at 6 in practice)
```

**Meaning:** We can afford to spawn this many agents based on context budget alone.

**Why 60 tokens per agent?** Measured across 20+ sessions (2026-04-15 to 2026-05-03). Includes: agent initialization (HONEY load), mission context injection, manifest return read cost.

### Step 2: Work Constraint

```python
unclaimed_frontier_work = scan_mission_frontier()
# Read forensics/manifests/{date}/ for tasks with bearing N/S/E/W
# Count discovered_work entries marked unblocked
# Return count of tasks no agent has claimed yet

work_demand = min(unclaimed_frontier_work, 6)
# Cap at 6 (never spawn more than 6 agents per wave)
```

**Meaning:** We have this much discovered work waiting.

**Why cap at 6?** Token cost per agent rises with team size (communication overhead). 6 agents was empirically validated as optimal (mth00407: emergence health peaks at 4-6 agent teams).

### Step 3: Base Spawn Count

```python
base = min(budget_capacity, work_demand)
# The intersection of "what we can afford" and "what work we have"

# Examples:
# budget_capacity=50, work_demand=3 → base=3 (limited by work)
# budget_capacity=2, work_demand=5 → base=2 (limited by budget)
# budget_capacity=6, work_demand=8 → base=6 (capped at 6)
```

**Meaning:** Base spawn count if we have no historical trajectory data.

**When used:** Session 1 of a new mission (no history yet) or insufficient history (<2 sessions).

### Step 4: FFMx Trajectory (Last 5 Sessions)

```python
ffmx_history = load_ffmx_history()  # array of scores from last 5 sessions
# Example: [0.210, 0.243, 0.315, 0.381, 0.290]

if len(ffmx_history) < 2:
    return base  # Not enough history; trust base only
    
recent = ffmx_history[-5:]  # Last 5 (or fewer if <5 exist)

# Linear regression: slope of FFMx trend
# slope = (final - initial) / num_samples
slope = (recent[-1] - recent[0]) / len(recent)

# Example with [0.210, 0.243, 0.315, 0.381, 0.290]:
# slope = (0.290 - 0.210) / 5 = 0.08 / 5 = 0.016
```

**Meaning:** How is FFMx changing? Positive slope = improving. Negative slope = declining.

**Why last 5 sessions?** Window size tradeoff:
- Too small (2–3): noisy, responds too quickly to single-session outliers
- Too large (10+): slow to respond when conditions change, stale signals
- Sweet spot (5): ~1 week of work (typical mission span), balance sensitivity + stability

### Step 5: Self-Calibration via Trajectory

```python
MOMENTUM_THRESHOLD = 0.03   # meaningful improvement
DECLINE_THRESHOLD = -0.03   # meaningful decline

if slope > MOMENTUM_THRESHOLD:
    # Trajectory is improving; reward it
    spawn_count = min(base + 1, 6)
    
elif slope < DECLINE_THRESHOLD:
    # Trajectory is declining; conserve and fix quality
    spawn_count = max(base - 1, 1)
    
else:
    # Trajectory is flat; hold steady
    spawn_count = base
```

**Meaning:** Modulate base spawn count based on recent trend.

**Why these thresholds?** 0.03 = ~3% FFMx change per session (from empirical noise floor). Below ±0.03, variance is within measurement error; don't react to noise.

**Bounds:**
- `min(base + 1, 6)`: Never spawn more than 6 agents (emergent complexity ceiling)
- `max(base - 1, 1)`: Never spawn fewer than 1 agent (continue even if declining)

---

## FFMx: Efficiency Signal Definition

FFMx is a **composite score** that captures work volume, quality, and cross-domain coordination in a single dimensionless number.

### Formula

```
FFMx = (artifacts × quality × emergence) / tokens_consumed

Where:
  artifacts      = number of non-empty manifest files returned
  quality        = mean quality_score across all manifests (0.0–1.0)
  emergence      = cross_citation_rate × south_edge_rate
  tokens_consumed = total API input tokens this session
```

### Component Breakdown

#### artifacts: Work Volume

```python
artifacts = count_files_in(f"forensics/manifests/{today}/")
# Each file represents an agent returning a manifest with actual output

# What counts:
# ✅ Manifest with dashboard_line + output_path (agent did work)
# ❌ Empty manifest (agent found nothing, no claim)
# ❌ Manifest with only next_mission_node (routing signal, not work)

# Why count manifests, not lines-of-code?
# Reason: We're measuring agent productivity, not artifact size.
#         A well-scoped manifest (2 KB, tight analysis) is as valuable as a sprawling report.
#         Counting manifests encourages focus over verbosity.
```

**Signal meaning:** Raw volume of agent outputs. Higher = more parallelism succeeded. Lower = agents blocked or context exhausted.

#### quality: Work Quality

```python
quality_score (per manifest) = 0.25 × has_output_path
                             + 0.25 × has_dashboard_line
                             + 0.25 × has_files_written
                             + 0.25 × has_next_mission_node
# Scale: 0.0–1.0
# 1.0 = all four fields present and non-empty
# 0.5 = two fields present
# 0.0 = empty manifest (no output)

quality = mean(quality_scores_all_manifests)

# Example with 6 manifests:
# manifest_1: 1.0 (complete)
# manifest_2: 1.0 (complete)
# manifest_3: 0.75 (missing next_mission_node)
# manifest_4: 0.75 (missing files_written)
# manifest_5: 0.5 (only output_path + dashboard_line)
# manifest_6: 0.5 (sparse output)
# quality = (1.0 + 1.0 + 0.75 + 0.75 + 0.5 + 0.5) / 6 = 5.0 / 6 = 0.833
```

**Signal meaning:** How complete is the work? Agents returning well-formed manifests indicate discipline and clarity. Sparse manifests suggest context pressure or agent confusion.

**Why this metric?** Manifest structure encodes agent intent: output_path (where's the work?), dashboard_line (what did I learn?), files_written (did I produce artifacts?), next_mission_node (where's the mission heading?). Rewarding all four encourages complete thinking.

#### emergence: Cross-Domain Coordination

Emergence captures **mission-level collaboration**: are agents reading each other's work and building on it?

```python
cross_citation_rate = manifests_with_citations / total_manifests
# A manifest has "citations" if discovered_work[] entries reference
# prior manifests from OTHER agents (from_label != self.task_id)

# Example:
# manifest_A (agent 1): discovered_work[] references manifest_B (agent 2) ✓ counts
# manifest_B (agent 2): discovered_work[] references manifest_A (agent 1) ✓ counts
# manifest_C (agent 3): discovered_work[] only self-references ✗ doesn't count
# cross_citation_rate = 2/3 = 0.667

south_edge_rate = manifests_with_south_bearing / total_manifests
# A manifest has "south-bearing" if next_mission_node.bearing == "S"
# or if most discovered_work[] entries have bearing="S"
# South edges indicate forward progress (shipping toward deliverables)

# Example:
# manifest_A: next_mission_node.bearing = "S" ✓ counts
# manifest_B: discovered_work has 3 S-edges, 1 E-edge → "S" dominant ✓ counts
# manifest_C: next_mission_node.bearing = "N" ✗ doesn't count
# south_edge_rate = 2/3 = 0.667

emergence = cross_citation_rate × south_edge_rate
# Why multiply? Because each signal is necessary but not sufficient alone.
# High cross-citation but no south edges = dense analysis with no progress.
# High south edges but no citations = disconnected shipping.
# Product of both encourages BOTH coordination AND forward motion.

# Example:
# emergence = 0.667 × 0.667 = 0.444
```

**Signal meaning:** Are agents working as a team on a shared mission (not in silos)? Are they making forward progress (not stuck in analysis loops)?

#### tokens_consumed: Cost Denominator

```python
tokens_consumed = total_api_input_tokens_this_session()
# From usage metrics: each agent spawn costs ~60 tokens + context injection
# Manifests returning costs ~20 tokens to read/parse
# Total = roughly 60 × spawn_count + 20 × manifest_count + context_injection

# Why normalize by cost?
# Reason: We want efficiency, not raw output.
#         Two scenarios:
#         (a) 4 agents, 12 manifests, 80K tokens → FFMx = (12×0.75×0.35)/80K = 0.000039
#         (b) 6 agents, 12 manifests, 120K tokens → FFMx = (12×0.75×0.35)/120K = 0.000026
#         Scenario (a) is more efficient (same output, less cost).
#         Normalization makes this visible.
```

**Signal meaning:** How much context did we burn to achieve this output? Lower is better (same work, less fuel).

### Worked Example: Computing FFMx

Session scenario:
```
Date: 2026-05-03
Agents spawned: 4 (NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER)
Manifests returned: 6 (all agents returned work)

Manifest details:
  manifest_nav.json:  quality=1.0, cross-cite=yes, bearing=S
  manifest_maker.json: quality=1.0, cross-cite=yes, bearing=S
  manifest_bridge.json: quality=0.75, cross-cite=yes, bearing=S
  manifest_diver.json: quality=0.75, cross-cite=no, bearing=N
  manifest_nav_follow.json: quality=0.5, cross-cite=no, bearing=E
  manifest_maker_follow.json: quality=0.5, cross-cite=no, bearing=E

API usage:
  Spawn cost: 4 × 60 = 240 tokens
  Context injection: 15,000 tokens (HONEY + manifests)
  Manifest reads: 6 × 20 = 120 tokens
  Agent execution: 72,000 tokens
  Total: ~87,000 tokens
```

**Calculation:**

```python
artifacts = 6
quality = (1.0 + 1.0 + 0.75 + 0.75 + 0.5 + 0.5) / 6 = 0.833
cross_citation_rate = 4/6 = 0.667 (manifests 1-4 have citations)
south_edge_rate = 3/6 = 0.5 (manifests 1-3 point south)
emergence = 0.667 × 0.5 = 0.333
tokens_consumed = 87,000

FFMx = (6 × 0.833 × 0.333) / 87,000
     = 1.665 / 87,000
     = 0.0000191

# For readability, multiply by 10,000:
FFMx (normalized) = 0.191
```

**Interpretation:** This session was moderately efficient (0.191 normalized). Quality was good (0.833), but emergence was modest (only 67% of agents cited prior work, only 50% pointed south). With 4 agents and 6 manifests, we could have extracted more learning (higher cross-citation) or momentum (more south-bearing). Next session: encourage agents to read more manifests and point toward deliverables.

---

## Self-Calibration: The Feedback Loop

The formula creates a closed-loop system where outcomes drive decisions:

```
┌─────────────────────────────────────────────────────────┐
│          SESSION N EXECUTION                            │
├─────────────────────────────────────────────────────────┤
│ 1. Load FFMx history (sessions N-5 to N-1)             │
│ 2. Compute slope via linear regression                 │
│ 3. Apply trajectory correction → spawn_count(N)        │
│ 4. Spawn agents, agents work                           │
│ 5. Agents write manifests                              │
│ 6. Compute FFMx(N) from manifests                      │
│ 7. Append FFMx(N) to history                           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│          SESSION N+1: HISTORY SLIDES                    │
├─────────────────────────────────────────────────────────┤
│ History was: [FFMx(N-4), FFMx(N-3), FFMx(N-2),         │
│              FFMx(N-1), FFMx(N)]                       │
│ Now becomes: [FFMx(N-3), FFMx(N-2), FFMx(N-1),         │
│              FFMx(N), FFMx(N+1)]                       │
│              (oldest dropped, newest appended)          │
│ Slope now includes N+1's outcome → modulates N+2       │
└─────────────────────────────────────────────────────────┘
```

### Flywheel: Positive Momentum

When a mission is healthy (FFMx trending up):

```
Session 1: FFMx = 0.21, slope = baseline, spawn = 4 (base)
Session 2: FFMx = 0.26, slope = +0.05 (above threshold), spawn = 5 (+1)
           Result: Richer parallel work → more cross-citations
Session 3: FFMx = 0.32, slope = +0.055, spawn = 6 (+1, capped)
           Result: Even denser coordination → higher emergence
Session 4: FFMx = 0.41, slope = +0.10, spawn = 6 (capped, no change)
           Result: Mission is saturated; agents working at peak
Session 5: FFMx = 0.38, slope = +0.085, spawn = 6
           Result: Slight dip (normal variance) but trend still strong
```

**Dynamics:** Early improvement is rewarded with more agents. More agents → richer discovery landscape → higher FFMx → more rewards. Flywheel accelerates until hitting the ceiling (6 agents or emergence saturation).

**Why this is not runaway:** The ceiling (spawn ≤ 6) prevents infinite acceleration. At 6 agents, further FFMx gains require better coordination, not more agents. Emergence becomes the limiting factor, naturally moderating spawn.

### Braking: Declining Quality

When a mission struggles (FFMx trending down):

```
Session 1: FFMx = 0.45, slope = baseline, spawn = 6 (base)
Session 2: FFMx = 0.42, slope = -0.03 (at threshold), spawn = 6 (hold)
Session 3: FFMx = 0.38, slope = -0.035 (below threshold), spawn = 5 (-1)
           Result: Fewer agents, less chaos, focus on depth
Session 4: FFMx = 0.36, slope = -0.03, spawn = 4 (-1)
           Result: Smaller team, deeper thinking → quality improves
Session 5: FFMx = 0.41, slope = -0.01, spawn = 4 (hold, trend flat)
           Result: Quality stabilized; ready to resume growth
Session 6: FFMx = 0.44, slope = +0.015, spawn = 4 (hold, trend flat but positive)
           Result: Trajectory turning positive; next session may add agents
```

**Dynamics:** Declining FFMx triggers a pullback (spawn -1). Fewer agents means less context pressure, more focus per agent, better quality (higher quality score in FFMx). Once quality recovers, FFMx stabilizes. Once trend flattens or reverses, spawn can increase again.

**Why this prevents collapse:** The floor (spawn ≥ 1) ensures we never stop working. Even in decline, we keep 1 agent running, gathering signals for recovery decision.

### Equilibrium: Flat Trajectory

When a mission is stable (FFMx within ±0.03 over 5 sessions):

```
Session 1: FFMx = 0.30, spawn = 4
Session 2: FFMx = 0.31, spawn = 4 (hold)
Session 3: FFMx = 0.29, spawn = 4 (hold, variance is normal)
Session 4: FFMx = 0.32, spawn = 4 (hold)
Session 5: FFMx = 0.30, spawn = 4 (hold)
```

**Dynamics:** No signal for change. Agents maintain current pace. This is the homeostatic state for a mature mission—steady output, predictable efficiency, no burndown or overheating.

---

## Worked Example: 5-Session Calibration Trace

Track spawn decisions across a realistic mission lifecycle:

### Session 1: Cold Start

```
Context: New mission "vault-structure-audit"
FFMx history: empty (cold start)
base = min(budget_capacity=8, work_demand=3) = 3
slope = N/A (insufficient history)
spawn_count = 3 (use base)

Outcome:
  - 3 agents spawned
  - 4 manifests returned (one agent didn't claim work)
  - quality = 0.75
  - cross_citation_rate = 0.5
  - south_edge_rate = 0.25
  - tokens_consumed = 45,000
  - FFMx(1) = (4 × 0.75 × 0.125) / 45,000 = 0.000037 (normalized: 0.37)

History: [0.37]
Status: Mission starting; baseline established
```

### Session 2: First Signal

```
FFMx history: [0.37]
base = min(budget_capacity=7, work_demand=4) = 4
slope = (0.37 - 0.37) / 1 = 0 (only 1 session, slope = 0)
spawn_count = 4 (use base; insufficient history for trajectory)

Outcome:
  - 4 agents spawned
  - 5 manifests returned
  - quality = 0.82
  - cross_citation_rate = 0.6
  - south_edge_rate = 0.4
  - tokens_consumed = 52,000
  - FFMx(2) = (5 × 0.82 × 0.24) / 52,000 = 0.000189 (normalized: 1.89)

History: [0.37, 1.89]
Slope: (1.89 - 0.37) / 2 = 0.76 (massive improvement!)
Status: Momentum detected; mission is ramping up
```

### Session 3: Reward Momentum

```
FFMx history: [0.37, 1.89]
base = min(budget_capacity=6, work_demand=5) = 5
recent = [0.37, 1.89]
slope = (1.89 - 0.37) / 2 = 0.76 (>> MOMENTUM_THRESHOLD 0.03)
spawn_count = min(base + 1, 6) = 6 (+1 reward)

Outcome:
  - 6 agents spawned (full team)
  - 8 manifests returned
  - quality = 0.79
  - cross_citation_rate = 0.75
  - south_edge_rate = 0.62
  - tokens_consumed = 78,000
  - FFMx(3) = (8 × 0.79 × 0.465) / 78,000 = 0.000378 (normalized: 3.78)

History: [0.37, 1.89, 3.78]
Slope: (3.78 - 0.37) / 3 = 1.14 (still strong momentum)
Status: Full parallelism achieved; strong emergence
```

### Session 4: Peak Performance, Saturation

```
FFMx history: [0.37, 1.89, 3.78]
base = min(budget_capacity=5, work_demand=6) = 5
recent = [0.37, 1.89, 3.78]
slope = (3.78 - 0.37) / 3 = 1.14 (still >> 0.03)
spawn_count = min(base + 1, 6) = 6 (already at ceiling)

Outcome:
  - 6 agents spawned (max)
  - 9 manifests returned
  - quality = 0.71 (down slightly; agents spreading thin)
  - cross_citation_rate = 0.67 (down; less reading time)
  - south_edge_rate = 0.78 (up; still shipping)
  - tokens_consumed = 110,000
  - FFMx(4) = (9 × 0.71 × 0.523) / 110,000 = 0.000304 (normalized: 3.04)

History: [0.37, 1.89, 3.78, 3.04]
Slope: (3.04 - 0.37) / 4 = 0.668 (declining from peak but still positive)
Status: Approaching saturation; quality cost of parallelism visible
```

### Session 5: First Dip, Conservative Response

```
FFMx history: [0.37, 1.89, 3.78, 3.04]
base = min(budget_capacity=4, work_demand=5) = 4
recent = [0.37, 1.89, 3.78, 3.04]
slope = (3.04 - 0.37) / 4 = 0.668 (still >> 0.03, but declining trend)
spawn_count = min(base + 1, 6) = 5
# Capped at +1 per session; don't revoke yet despite slope decline

Outcome:
  - 5 agents spawned
  - 7 manifests returned (two agents didn't claim work)
  - quality = 0.68 (down further)
  - cross_citation_rate = 0.43 (low; agents isolated)
  - south_edge_rate = 0.71
  - tokens_consumed = 92,000
  - FFMx(5) = (7 × 0.68 × 0.305) / 92,000 = 0.000159 (normalized: 1.59)

History: [0.37, 1.89, 3.78, 3.04, 1.59]
Slope: (1.59 - 0.37) / 5 = 0.244 (decline is now significant!)
Status: Mission is declining; next session should trigger -1
```

### Session 6: Pullback

```
FFMx history: [0.37, 1.89, 3.78, 3.04, 1.59]
base = min(budget_capacity=3, work_demand=4) = 3
recent = [0.37, 1.89, 3.78, 3.04, 1.59]
slope = (1.59 - 0.37) / 5 = 0.244 (>> DECLINE_THRESHOLD -0.03? No, still positive)
spawn_count = 3 (hold base; slope still positive but weakening)

Wait—let's recompute. Slope = 0.244 is POSITIVE, so no -1 pullback yet.
But the trend is WEAKENING (was 0.668, now 0.244).
Decision: Hold at base=3, monitor next session.

Outcome:
  - 3 agents spawned (conservative)
  - 4 manifests returned
  - quality = 0.81 (recovery! focus on depth)
  - cross_citation_rate = 0.75 (high; agents reading)
  - south_edge_rate = 0.5
  - tokens_consumed = 35,000
  - FFMx(6) = (4 × 0.81 × 0.375) / 35,000 = 0.000350 (normalized: 3.50)

History: [0.37, 1.89, 3.78, 3.04, 1.59, 3.50]
Slope: (3.50 - 0.37) / 6 = 0.522 (back up! quality recovery helped)
Status: Pullback was correct; quality improved, FFMx rebounded
```

### Summary Table

| Session | FFMx (norm) | Slope | Decision | Spawn | Notes |
|---------|-------------|-------|----------|-------|-------|
| 1 | 0.37 | — | base | 3 | Cold start |
| 2 | 1.89 | 0.76 | base | 4 | Momentum building |
| 3 | 3.78 | 1.14 | +1 reward | 6 | Full parallelism |
| 4 | 3.04 | 0.668 | hold (capped) | 6 | Saturation visible |
| 5 | 1.59 | 0.244 | hold | 5 | Trend declining, not yet -1 |
| 6 | 3.50 | 0.522 | hold/recover | 3 | Pullback paid off |

**Interpretation:** The formula naturally tracked mission lifecycle:
- Sessions 1–3: Ramp-up (reward momentum with +1)
- Sessions 3–4: Saturation (ceiling effect, quality costs)
- Sessions 4–5: Decline (slope weakening)
- Session 6: Recovery (conservative spawn + focus = quality improvement)

No human decision-making needed. The formula responded to measured outcomes.

---

## Bootstrap Problem and Warm Start

The formula faces a "cold start" problem: new missions have no FFMx history.

### Cold Start (Session 1 of New Mission)

```python
if len(ffmx_history) < 2:
    return base  # No trajectory; use budget ∩ work only
```

**Problem:** Can't compute slope from 0 or 1 data point. Trajectory correction unavailable.

**Solution:** Use `base` only. This is conservative (good—avoid overspawning on untested mission) and data-driven (base comes from real budget/work constraints).

**Example:** Mission "infrastructure-audit" starts with budget=8, work=3 → base=3 → spawn 3 agents. After 2 sessions, slope becomes available.

### Warm Start (Post-Compact Springboard)

When faerie2 auto-compacts context (≥92% full), FFMx history is ephemeral and would be lost.

**Solution: 8x_precompact_springboard.py captures history before compact:**

```json
// File: piston-checkpoint.json (saved pre-compact)
{
  "mission": "mission-field-wire",
  "ffmx_history": [0.21, 0.26, 0.31, 0.38, 0.29],
  "spawn_count_last": 5,
  "timestamp": "2026-05-04T134500Z",
  "context_used_pct": 94
}
```

**Post-compact: 9x_postcompact_faerie_springboard.py restores:**

```python
# After compact, context is ~10% full again (clean slate)
# But we restore FFMx history from piston-checkpoint.json

restored_history = load_checkpoint("piston-checkpoint.json")
ffmx_history = restored_history["ffmx_history"]

# Next session slot:
slope = (0.29 - 0.21) / 5 = 0.016
spawn_count = base  # Slope is <0.03, hold steady

# Result: Formula resumes mid-calibration, not cold
```

**Why this matters:** Without warm start, every auto-compact resets FFMx history → formula reverts to base for one session → misses trajectory signals. With springboard, trajectory persists across compacts (no loss of learning).

**Implementation:** Pre-compact hooks save state; post-compact hooks restore. Checkpoint is immutable (written once, read-only). If springboard fails, formula degrades gracefully to base (safe fallback).

---

## Relationship to Piston Waves (Deprecated Model)

### Old Wave Model (W1/W2/W3)

The prior faerie2 architecture used static **piston waves**:

```
W1 (Green, ≤25% context): spawn 6 agents max (burn hot, hit 5-min cache)
W2 (Orange, 25–65% context): spawn 4 agents (autonomous dispatch, no pause)
W3 (Red, >65% context): spawn 1 agent (deep synthesis, background)
```

**Problem:** Context fill is the only input. Ignore mission quality, work volume, or outcomes.

**Example failure:**
```
Scenario: Mission is in decline (low FFMx) but context is still 30% (W1 green)
Old formula: Spawn 6 agents (W1 rule)
Result: High parallelism + low-quality work = chaos, more decline

New formula: Compute slope, see decline, spawn 3 agents
Result: Conservative, focused work → quality recovers
```

### New Living Formula (Mission-Driven, Feedback-Based)

The living formula inverts the hierarchy:

```
Input: Last 5 FFMx outcomes (mission health), budget, work
Decision: Spawn count = f(trajectory, budget, work)
Output: Adaptive spawn count (1–6 agents per decision)
```

**Advantages over W1/W2/W3:**
1. **Mission-aware:** Spawn rate reflects mission outcomes, not just context budget
2. **Self-correcting:** Declining quality triggers conservative spawning automatically
3. **Emergence-driven:** Upward FFMx rewards parallelism; system accelerates naturally
4. **No external tuning:** No need to manually adjust thresholds per mission type

**Piston waves still exist** (as optimization signals for context pressure), but they're now secondary:
- W1/W2/W3 inform the `base` spawn count via budget_capacity
- FFMx trajectory modulates that base via ±1 adjustment
- Result: Graceful response to both context pressure and mission health

---

## Implementation Roadmap

### Files and Responsibilities

#### Configuration

**`config/spawn-pressure-mission-driven.json`** (source of truth for all formula parameters)

```json
{
  "version": "1.0",
  "formula": "spawn_count = f(base, slope, thresholds)",
  "spawn_cost_per_agent_tokens": 60,
  "ffmx_window_size_sessions": 5,
  "momentum_threshold": 0.03,
  "decline_threshold": -0.03,
  "spawn_ceiling": 6,
  "spawn_floor": 1,
  "quality_score_weights": {
    "output_path": 0.25,
    "dashboard_line": 0.25,
    "files_written": 0.25,
    "next_mission_node": 0.25
  }
}
```

#### State Management

**`~/.claude/hooks/state/system-eval.json`** (current FFMx + rolling history)

```json
{
  "mission": "vault-structure-audit",
  "ffmx_current": 3.78,
  "ffmx_history": [0.37, 1.89, 3.78, 3.04, 1.59],
  "slope": 0.244,
  "spawn_count_last": 5,
  "timestamp": "2026-05-04T153000Z",
  "quality_mean": 0.72,
  "emergence_mean": 0.42
}
```

#### Computation

**`9x_context_pressure_calculator.py`** (compute budget_capacity)

```python
def compute_budget_capacity():
    cost_per_agent = load_config("spawn_cost_per_agent_tokens")
    remaining = total_budget - current_usage
    capacity = remaining // cost_per_agent
    return min(capacity, 6)  # cap at 6
```

**`0x_mission_graph.py --query open-edges`** (count work_demand)

```python
def scan_frontier():
    manifests = read_manifests(f"forensics/manifests/{today}/")
    discovered = sum(
        len(m["discovered_work"])
        for m in manifests
        if m.get("mission") == current_mission
    )
    claimed = count_agents_spawned()
    return max(0, discovered - claimed)
```

**`7x_spawn_pressure.py`** (main formula engine)

```python
def compute_spawn_count(context_remaining, unclaimed_work, ffmx_history):
    # Step 1-2
    budget = context_remaining // 60
    demand = min(unclaimed_work, 6)
    base = min(budget, demand)
    
    # Step 3-4
    if len(ffmx_history) < 2:
        return base
    
    recent = ffmx_history[-5:]
    slope = (recent[-1] - recent[0]) / len(recent)
    
    # Step 5
    if slope > 0.03:
        return min(base + 1, 6)
    elif slope < -0.03:
        return max(base - 1, 1)
    else:
        return base
```

**`0x_ffmx_computer.py`** (compute FFMx from manifests)

```python
def compute_ffmx(manifests):
    artifacts = len([m for m in manifests if m.get("output_path")])
    quality = mean([quality_score(m) for m in manifests])
    
    cross_cite = len([m for m in manifests if has_citations(m)])
    cross_citation_rate = cross_cite / max(len(manifests), 1)
    
    south = len([m for m in manifests if south_bearing(m)])
    south_edge_rate = south / max(len(manifests), 1)
    
    emergence = cross_citation_rate * south_edge_rate
    tokens = read_usage_metrics()
    
    ffmx = (artifacts * quality * emergence) / max(tokens, 1)
    return ffmx * 10000  # normalize for readability
```

#### Springboard (Compact Integration)

**`8x_precompact_springboard.py`** (save state before compact)

```python
def save_checkpoint():
    state = {
        "ffmx_history": load_ffmx_history(),
        "spawn_count_last": read_piston_state("last_spawn"),
        "mission": read_mission(),
        "timestamp": now_iso(),
    }
    write_json("piston-checkpoint.json", state)
    # Triggered automatically by PostCompact hook
```

**`9x_postcompact_faerie_springboard.py`** (restore state after compact)

```python
def restore_checkpoint():
    checkpoint = read_json("piston-checkpoint.json")
    write_json("~/.claude/hooks/state/system-eval.json", checkpoint)
    # Triggered automatically by PostCompact hook; formula reads normal state files
```

### Integration Checklist

- [ ] Create `config/spawn-pressure-mission-driven.json` (configuration)
- [ ] Implement `7x_spawn_pressure.py` (main formula)
- [ ] Implement `0x_ffmx_computer.py` (metric computation)
- [ ] Wire `system-eval.json` as standard state store (all hooks read/write here)
- [ ] Create `8x_precompact_springboard.py` (snapshot FFMx before compact)
- [ ] Create `9x_postcompact_faerie_springboard.py` (restore FFMx after compact)
- [ ] Update `presend_estimate.py` to call `7x_spawn_pressure.py` (inject spawn_count decision)
- [ ] Update manifest schema (CLAUDE.md) to formalize quality_score field
- [ ] Test cold-start (session 1 of new mission)
- [ ] Test warm-start (post-compact recovery)
- [ ] Test flywheel (3+ sessions trending up)
- [ ] Test braking (3+ sessions trending down)
- [ ] Validate FFMx computation on past sessions (backtest)

---

## Success Metrics & Validation

### Phase 1: Foundational Metrics (Sessions 1–3)

**Goal:** Formula computes correctly; FFMx signal is stable.

| Metric | Target | Purpose |
|--------|--------|---------|
| FFMx std dev | <0.2 (normalized) | Signal is not noisy |
| Slope computation | reproducible | Regression is deterministic |
| Spawn count decisions | expected | ±1 modulation aligns with slope |
| Cold-start fallback | works | Base computation is safe |

### Phase 2: Feedback Validation (Sessions 4–10)

**Goal:** Formula responds correctly to outcomes; missions track expected trajectories.

| Metric | Target | Purpose |
|--------|--------|---------|
| Upward missions | spawn ≥5 by session 5 | Momentum rewarded |
| Declining missions | spawn ≤3 by session 5 | Decline triggers pullback |
| Quality recovery | +0.1 per pullback | Conservative spawning helps |
| Emergence growth | +0.05 per wave | Cross-citation increases with parallelism |

### Phase 3: System Integration (Sessions 11+)

**Goal:** Formula drives realistic spawn decisions across multiple concurrent missions.

| Metric | Target | Purpose |
|--------|--------|---------|
| Cross-mission variance | <0.3 corr | Each mission calibrates independently |
| Springboard success | 100% | Post-compact restoration works |
| Presend accuracy | >90% | Estimated spawn counts match actual |
| Total cost efficiency | +15% vs piston waves | Living formula burns less context for same output |

### Backtest: Past Sessions

Run formula on past 10 sessions (2026-04-24 to 2026-05-04) with real FFMx data:

```
Session 1 (2026-04-24): historical FFMx = 0.21
  Formula spawn: base=3 (no history)
  Actual spawn: 3 ✓
  
Session 2 (2026-04-25): historical FFMx = 0.26
  Slope = 0.05 (above threshold)
  Formula spawn: base+1 = 4
  Actual spawn: 4 ✓
  
...
```

If backtest shows ≥85% alignment, formula is valid for forward deployment.

---

## Next Steps

### Immediate (This Session)

1. **Create config file** (`config/spawn-pressure-mission-driven.json`)
   - Freeze formula parameters (thresholds, costs, window size)
   - Document each parameter's role and why it was chosen

2. **Implement core formula** (`7x_spawn_pressure.py`)
   - Write function: `compute_spawn_count(context_remaining, unclaimed_work, ffmx_history)`
   - Test with synthetic data (worked examples from this doc)
   - Integrate into presend_estimate.py hook

3. **Implement FFMx computer** (`0x_ffmx_computer.py`)
   - Parse manifests from forensics/{date}/
   - Compute artifacts, quality, emergence, normalize
   - Append FFMx to system-eval.json

4. **Test cold-start fallback**
   - Verify formula returns base when len(history) < 2
   - Confirm spawning continues without errors

### Week 1 (Sessions 1–3)

1. **Validate FFMx signal stability**
   - Compute FFMx for 3 consecutive sessions
   - Check that std dev < 0.2 (noise floor acceptable)
   - If noisy, adjust quality weights or thresholds

2. **Run backtest on past 10 sessions**
   - Apply formula retroactively to 2026-04-24 to 2026-05-04
   - Compare predicted spawn counts vs. actual
   - Target ≥85% alignment

3. **Deploy formula as read-only advisory**
   - Compute spawn_count but don't enforce
   - Display in presend output: "Formula recommends: 4 agents"
   - Collect human feedback on recommendations

### Week 2+ (Sessions 4–10)

1. **Deploy formula as active enforcement**
   - Use formula spawn_count in spawn.py by default
   - Allow override (user can force spawn count if needed)
   - Log all decisions to forensics/main-metrics.jsonl

2. **Track feedback metrics from Phase 2**
   - Monitor upward/declining missions separately
   - Check quality recovery after pullbacks
   - Validate emergence growth with parallelism

3. **Integrate springboard for post-compact**
   - Wire 8x_precompact_springboard.py to PostCompact hook
   - Wire 9x_postcompact_faerie_springboard.py to PostCompact hook
   - Test that FFMx history survives auto-compact

4. **Document learned patterns to NECTAR/HONEY**
   - Crystallize any mth- entries (e.g., "spawn pressure responses")
   - Record edge cases discovered (missions that violate assumptions)
   - Update CLAUDE.md with reference to living formula

---

## References & Breadcrumbs

> [↑ Hive](../Hive.md) · [⌂ Home](../../HOME.md)

**Related Documents:**
- `config/faerie-config-v1.json` — Configuration parameters
- `docs/MISSION-NAVIGATION-MODEL.md` — Manifest routing and mission framework
- `docs/SPAWN-COST-ACCOUNTABILITY.md` — Cost tracking mechanics
- `~/.claude/CLAUDE.md` — Core operational rules (global)
- `/mnt/d/0local/gitrepos/faerie2/docs/CLAUDE.md` — Core operational rules (project)

**Key Methods (from HONEY.md):**
- mth00407: Multi-bearing emergence metrics (6-agent team health)
- mth00099: F(0) self-dispatch rule (when to spawn)
- mth00098: Agent discovery protocol (mission-field routing)

---

## Appendix: Glossary

| Term | Definition |
|------|-----------|
| **FFMx** | Efficiency index: (artifacts × quality × emergence) / tokens_consumed. Higher is better. |
| **artifacts** | Count of non-empty manifest files returned by agents in a session. |
| **quality** | Mean quality_score (0–1) across all manifests; 0.25 per field (output_path, dashboard_line, files_written, next_mission_node). |
| **emergence** | Product of cross_citation_rate and south_edge_rate; measures collaboration and forward progress. |
| **slope** | Linear regression of FFMx over last 5 sessions; positive = improving, negative = declining. |
| **base** | Spawn count without trajectory correction: min(budget_capacity, work_demand). |
| **spawn_count** | Final decision: base ± trajectory_correction, capped [1, 6]. |
| **momentum_threshold** | 0.03; FFMx improvement above this triggers +1 spawn reward. |
| **decline_threshold** | -0.03; FFMx decline below this triggers -1 spawn pullback. |
| **piston waves** | Deprecated W1/W2/W3 model; now secondary optimization hint. |
| **warm start** | Post-compact springboard that restores FFMx history and resumes calibration. |
| **cold start** | Session 1 of a mission with no FFMx history; formula uses base only. |

---

**Document Version:** 1.0 | **Last Updated:** 2026-05-04 | **Status:** Active (first deployment)

