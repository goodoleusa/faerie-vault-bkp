---
date: 2026-05-10
type: skill-expansion-draft
status: draft
tags: [openhands-sdk, faerie, ffmx, inject, langchain, openrouter, skill]
---

# 🔧 OpenHands SDK Skill — Expanded for Faerie Philosophy

## Overview

This skill unifies the **OpenHands Software Agent SDK** with the **faerie2 lifecycle system**, creating a single cohesive framework where:

1. **OpenHands SDK** provides the agent runtime (LLM, Agent, Conversation, Tools, Skills, Hooks)
2. **Faerie lifecycle** provides the orchestration philosophy (evolve → crystallize → spawn → bundle → inject)
3. **Inverted main-session flow** achieves Flow State Maximization (FFMx)

---

## 🧚 The Inverted Main-Session Flow

### Normal Agent Pattern (What Everyone Else Does)
```
Main session does all the work:
  → Reads files
  → Thinks through problems
  → Writes code
  → Reviews output
  → Next task...
  
Result: Main context fills with execution tokens.
         Single-threaded. Slow. No emergence.
```

### Faerie Inverted Pattern (What We Do)
```
Main session (🧚 Faerie):
  → Reads ONLY manifest summaries (≤80-char dashboard_line)
  → Makes bearing decisions (N/S/E/W)
  → Spawns agent teams via context-pressure sigmoid
  → Reads crystallized wisdom (HONEY.md)
  → Injects critical priorities when needed
  
Spawned agents (🔨🔬🌉🧭):
  → Do ALL meaningful work
  → Write manifests to filesystem (stigmergic coordination)
  → Self-organize via compass edges
  → Return quality + discovery signals
  
Result: Main context stays near-empty (f(0) ≈ 5%).
         Maximum parallelism. Emergence. FFMx > 30×.
```

### Why This Works

The key insight: **the main session is the most expensive compute in the system**. Every token of main context costs 5× output tokens. If main spends its context reading files and writing code, you've wasted your most valuable resource on work a $0.02/agent could do.

Faerie inverts this: main context is reserved for **judgment, bearing decisions, and consolidation**. Everything else is delegated.

---

## ⚙️ f(0) — The North Star Metric

```
f(0) = main_session_tokens / total_session_tokens

Target:    ≤ 5%  (aspirational)
Tolerance: ≤ 8%  (acceptable)
Danger:    > 10% (restructure immediately)
```

**How to maintain f(0):**
- Never read full files in main — read manifest `dashboard_line` (≤80 chars)
- Never write code in main — spawn a MAKER agent
- Never debug in main — spawn a DEEP-DIVER agent
- Never search in main — spawn a NAVIGATOR agent
- Use `/evolve` to monitor f(0) in-flight
- Use `/inject` with constraint type to enforce f(0) if drifting

---

## 🚀 FFMx — Flow State Maximization Formula

```
FFMx = Q × (1 + D) × P × N_completed

Where:
  Q  = manifest quality (0-1, avg across agents)
      measured by: output_path✓, dashboard_line✓, 
                   files_written✓, next_mission_node✓
  D  = discovery rate (discovered_work / agent_count)
      measures: T-axis improvement, emergent findings
  P  = piston efficiency (1.0 ± 0.3)
      bonus for: low latency, cache hits, good bundling
      penalty for:  high latency, cache misses, bloated bundles
  N  = agents completing valid manifests

Target: FFMx > 30 per session
Current: ~44.4 (calibration session)

FFMx > 50: 🌊 Strong emergence — system is amplifying
FFMx 30-50: ✅ Healthy — good amplification
FFMx 15-30: ⚠️ Weak — check bundle quality, increase parallelism
FFMx < 15:  ❌ Failing — agents not completing or quality too low
```

### Optimization Levers for Max FFMx

| Lever | Action | Expected Impact |
|-------|--------|-----------------|
| **Q (Quality)** | Improve bundle templates, add manifest field checkers | +20-40% |
| **D (Discovery)** | Frontier scans, cross-mission edge detection, W-west audits | +10-25% |
| **P (Piston)** | Tune spawn pressure sigmoid (c_mid, k), wave caching | +5-15% |
| **N (Count)** | Larger W1 teams (up to 6), faster W2 dispatch | +10-30% |

---

## 🧭 Compass Bearings — When to Spawn What

### N (North) — Unblock
**When:** quality < 0.70 AND belief < 0.70
**Action:** Spawn NAVIGATOR to discover why blocked
**Team:** NAVIGATOR + DEEP-DIVER + MAKER

### S (South) — Ship
**When:** quality ≥ 0.70 AND belief ≥ 0.70
**Action:** Spawn MAKER to deliver next phase
**Team:** MAKER + BRIDGE + NAVIGATOR

### E (East) — Parallel
**When:** quality ≥ 0.70 AND belief < 0.70
**Action:** Spawn BRIDGE to validate across domains
**Team:** BRIDGE + MAKER + NAVIGATOR

### W (West) — Reframe
**When:** quality < 0.70 AND belief ≥ 0.70
**Action:** Spawn DEEP-DIVER to challenge assumptions
**Team:** DEEP-DIVER + NAVIGATOR

---

## 🧬 Lifecycle Tools — How to Use Each

### 1. `/evolve` — Live Monitoring (In-Flight)
```
When: During any multi-agent session
What: Captures live metrics, detects mutations, emits steering signals

faerie evolve --phase all
faerie evolve --phase steering --mutation-family "piston-overlap"
faerie evolve --readiness-check

Outputs: fitness_snapshot, steering_signals, readiness_queue, spawn_influence
Landing: forensics/ephemeral/{date}/
```

### 2. `/crystallize` — System Consolidation (Post-Session)
```
When: After completing a sprint, or when scripts/docs accumulate dead weight
What: Evaluates mutations, promotes winners to HONEY, archives dead weight

faerie crystallize --phase all
faerie crystallize --phase evaluate
faerry crystallize --phase promote

Outputs: metric_snapshot, candidates_found, verified_candidates, promoted, superseded
Landing: HONEY.md, forensics/coc/eval/
```

### 3. `/spawn` — Agent Team Creation
```
When: 2+ independent tasks exist, OR context pressure triggers sigmoid
What: Creates agent bundles, dispatches via piston waves

faerie spawn --mission "optimize-db" --bearing S --team-size 4
faerie spawn --bearing N --wave W1

Config: bearing, team_size, mutation_influence, mission
Cost: ~60 tokens/agent
```

### 4. `/bundle` — Bundle Creation (Any Agent)
```
When: Any agent has inspiration for a reusable bundle
What: Creates bundle-*.json from templates/fragments/inheritance

faerie bundle create --archetype NAVIGATOR --mission "security-audit"
faerie bundle decompose --bundle bundle-001.json

Any agent can create bundles. Only main agent decides spawning.
```

### 5. `/inject` — Fast-Path System Priority Override ⚡
```
When: Critical wisdom/fix/priority needs to propagate NOW
      (evolution is too slow — full cycle takes 3+ sessions)
What: Injects top-level system instructions immediately

Four injection types:

  equilibrium  → Append to system-equilibrium-instructions.md (additive)
  emergence    → Append to positive-emergence-instructions.md (additive)  
  override     → REPLACE system-override-instructions.md (destructive, highest priority)
  constraint   → Append to system-constraints.md (safety)

Four priority levels with automatic deadlines:
  critical  → 1 hour
  high      → 24 hours
  normal    → 72 hours
  low       → 168 hours

Example:
  faerie inject equilibrium "f(0) must stay below 8%. Check every 2 cycles." --priority critical
  faerie inject override "All manifests must include genotype. No exceptions." --priority critical
  faerie inject constraint "Never delete code without hash-chain backup." --priority high

Why this matters: Evolution (evolve→crystallize cycle) is designed to be 
slow and evidence-based. That's correct for substrate changes. But sometimes 
you need to inject a critical philosophical principle, a safety constraint, 
or a system-level priority RIGHT NOW. Inject is the fast path.
```

### 6. `/dashboard` — Unified Metrics View
```
When: Anytime you need system health visibility
What: Collects M1-M11 membench, FFMx, piston, emergence, cost metrics

faerie dashboard --mode health
faerie dashboard --mode full
faerry dashboard --wandb-push  # sends to WANDB

Output: Terminal dashboard + WANDB-compatible JSON
Landing: forensics/coc/eval/{date}/dashboard-{ts}.json
```

---

## 🔗 OpenHands SDK Integration

### Installation
```bash
pip install openhands-sdk openhands-tools
```

### Basic Agent Setup
```python
import os
from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

llm = LLM(
    model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL", None),
)

agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ],
)

conversation = Conversation(agent=agent, workspace=os.getcwd())
```

### OpenRouter Multi-Model Routing (Faerie Wave Strategy)
```python
# W1 (Triage) → Free models via OpenRouter
w1_llm = LLM(
    model="openrouter/meta-llama/llama-4-maverick:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# W2 (Features) → Claude via native API
w2_llm = LLM(
    model="openrouter/anthropic/claude-sonnet-4-5",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# W3 (Synthesis) → Premium via OpenRouter
w3_llm = LLM(
    model="openrouter/anthropic/claude-opus-4",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# Spawn pressure sigmoid determines wave:
# c ≤ 25%: W1 (parallel, free models, up to 6 agents)
# c ≈ 50%: W2 (selective, Claude, up to 4 agents)  
# c ≥ 75%: W3 (deep, premium, 1 agent)
```

### Faerie + OpenHands SDK: Inverted Flow
```python
# Main session (Faerie) — does almost nothing directly
# Instead, spawns SDK conversations as sub-agents

from openhands.sdk import LLM, Conversation, Agent, Tool

class FaerieSession:
    """Main orchestrator. Reads bearing, spawns teams, consolidates."""
    
    def spawn_maker(self, mission: str, task: str):
        llm = self._wave_llm()  # Pick model by context pressure
        agent = Agent(llm=llm, tools=self.tools, system_prompt=self._bundle("MAKER"))
        conv = Conversation(agent=agent, workspace=self.workspace)
        conv.send_message(f"MISSION: {mission}\nTASK: {task}\nWrite manifest on completion.")
        conv.run()
        return self._read_manifest(conv)  # Read ≤80-char dashboard_line
    
    def _wave_llm(self):
        c = self.context_fill_pct()
        if c <= 25: return w1_llm  # Free, parallel
        elif c <= 65: return w2_llm  # Claude, selective
        else: return w3_llm  # Premium, deep
```

### Skills Integration
```python
from openhands.sdk import Skill

# faerie skill injection via SDK Skill system
faerie_skill = Skill(
    name="faerie",
    content="""
    You are spawned by 🧚 Faerie orchestrator.
    Mission: {{mission}}
    Bearing: {{bearing}}
    Write a manifest on completion with: dashboard_line (≤80 chars), 
    output_path, files_written, next_mission_node, discovered_work.
    """
)

# inject skill for critical priority injection
inject_skill = Skill(
    name="faerie-inject",
    content="""
    Use faerie inject for critical system priorities:
    - equilibrium: append additive guidance
    - override: replace existing instructions (highest priority)
    - constraint: add safety constraint
    - emergence: guide positive emergence
    Priority levels: critical (1h), high (24h), normal (72h), low (168h)
    """
)
```

---

## 🌊 Membench — What to Measure for Max FFMx

### M1-M11 Dimensions

| Probe | Dimension | What It Measures | Target | FFMx Relevance |
|-------|-----------|------------------|--------|----------------|
| M1 | Retention | % facts recalled correctly | ≥0.85 | Foundation: if agents can't remember, everything fails |
| M2… | … | … | … | … |
| M3 | Parallelization ROI | Work output / sequential baseline | >1.10 | Direct FFMx multiplier: parallel > sequential |
| M8 | Confabulation | % hallucinated facts | ≤0.05 | Quality gate: garbage in = garbage out |
| M11 | Honey Hit Rate | % sessions finding HONEY facts | ≥0.70 | Crystallized knowledge reaches agents |

### Dashboard Metrics (Unified)

```
📊 FAERIE DASHBOARD — 2026-05-10
═══════════════════════════════════

🔄 PISTON (Wave Orchestration)
  W1 LIFTOFF: ⚡ 3 agents in flight, spawn_latency=2.1s
  W2 CRUISE: 🔥 1 agent, cache_hit=85%
  W3 SYNTH:   💤 idle
  State: 🔄⚡ (healthy, high burn)

🧠 MEMORY (HONEY/NECTAR)
  NECTAR hit-rate: 72% ✓
  Promotions this session: 3
  State: 🧠✓ (healthy)

🗂️ FORENSICS (COC Integrity)
  Artifacts named: 100% ✓
  COC chain: valid
  State: 🗂️✓ (healthy)

🧭 COMPASS (Navigation Graph)
  Edges valid: 100% ✓
  Cold threads: 0
  State: 🧭✓ (healthy)

🚀 FFMx: 44.4×  [✅ healthy]
  Q=0.82, D=0.12, P=1.15, N_completed=8
  → Optimization: increase D (discovery) via more W-west audits

🌊 EMERGENCE TRAJECTORY: +0.04  [✅ positive]
  Pattern detected: Self-Invalidation (agent refused stale task)
  Pattern detected: Diagnostic Emergence (agent traced cross-boundary bug)

💰 COST: $1.24/session  [-12% vs last]
  W1 (free): 40% of work
  W2 (Claude): 45% of work
  W3 (premium): 15% of work

SYSTEM STATUS: ALL HEALTHY ✅
```

---

## 💉 When to Use Inject vs. Normal Evolution

| Scenario | Use | Why |
|----------|-----|-----|
| Safety constraint discovered NOW | `inject constraint` | Can't wait 3 sessions for crystallize |
| Critical bug in production | `inject override` | Must supersede immediately |
| Philosophical principle (e.g., "never delete without hash-chain") | `inject equilibrium` | Additive wisdom, persists |
| Emergence pattern to encourage | `inject emergence` | Guide positive emergence direction |
| Tuning spawn pressure sigmoid | `evolve → crystallize` | Needs evidence, measurement, 3+ cycles |
| Improving bundle quality | `evolve → crystallize` | Needs A/B comparison |
| New membench probe | code change → measure | Not a priority injection, it's infra work |

**Rule of thumb:** If it's a **principle, constraint, or priority** that must take effect immediately → **inject**. If it's a **tuning, optimization, or infrastructure** change that needs evidence → **evolve → crystallize**.

---

## 🔗 LangChain + ZimaBoard Integration

```python
# Faerie can delegate to LangChain instance on ZimaBoard
# via the OpenHands SDK's ACP agent or direct API calls

from openhands.sdk import LLM

# ZimaBoard LangChain (remote)
zima_llm = LLM(
    model="langchain/zima-custom",
    base_url="http://zima-board-ip:8000/v1",  # ZimaOS Docker LangChain app
    api_key=os.getenv("ZIMA_API_KEY"),
)

# Use for: preprocessing, embedding, entity extraction, OSINT
# Faerie orchestrates; ZimaBoard provides specialized pipeline
```

---

## 📦 File Structure

```
faerie2/
├── .openhands/skills/
│   ├── faerie/           # Lifecycle tools (evolve, crystallize, spawn, bundle, inject)
│   │   ├── __init__.py
│   │   ├── evolve.py     # Live fitness monitoring
│   │   ├── crystallize.py # System consolidation
│   │   ├── spawn.py      # Agent spawning
│   │   ├── bundle.py     # Bundle creation
│   │   ├── inject.py     # System instruction injection (FAST PATH)
│   │   └── orchestrate.py # Unified lifecycle command
│   └── openhands-sdk/    # THIS SKILL — unified SDK + faerie philosophy
│       └── SKILL.md
├── scripts/
│   └── membench/         # CANONICAL central location for ALL eval
│       ├── probes/       # M1-M11 measurement probes
│       ├── collectors/   # Metric collection scripts
│       ├── eval/         # Eval harnesses (dev_eval, release gates)
│       ├── reports/      # Dashboard, status_line, briefs
│       └── adapters/     # WANDB upload, external integrations
├── infrastructure/vps/   # VPS deployment (TO BUILD)
├── docs/
│   ├── 02-CANONICAL-GLOSSARY.md    # Emoji-anchored definitions
│   └── 03-CANONICAL-FAERIE-FORMULAS.md  # All formulas
└── HONEY.md              # Living memory (crystallized wisdom)
```

---

*Draft: 2026-05-10T11:22:00Z*
*Status: Ready for implementation → becomes SKILL.md + dashboards*
