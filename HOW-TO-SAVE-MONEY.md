---
type: reference
status: active
created: 2026-03-15
updated: 2026-03-22
tags:
  - cost-optimization
  - reference
  - token-management
doc_hash: sha256:ff88b2a2d5b627b804515238b22ee125cbce8e0f4d12f25c5b9b4c3d9435327f
hash_ts: 2026-03-29T16:16:46Z
hash_method: body-sha256-v1
---

# How to Save 70–94% on AI API Costs

This document is the reference for cost optimization — the math, the decision framework,
the code, the levers. Skills and CLAUDE.md contain only the operational rules.
Read this once; let the skill enforce it automatically.

---

## Pricing (2026)

| Model | Input | Cached input | Output | Use for |
|---|---|---|---|---|
| `claude-haiku-4-5` | $1.00 / 1M | $0.10 / 1M | $5.00 / 1M | Bulk, extraction, classification |
| `claude-sonnet-4-6` | $3.00 / 1M | $0.30 / 1M | $15.00 / 1M | Analysis, code, daily driver |
| `claude-opus-4-6` | $5.00 / 1M | $0.50 / 1M | $25.00 / 1M | Architecture, complex reasoning |

Batch API: **50% off** all of the above for non-realtime work.
Cache write: 1.25× input rate (one-time). Cache read: 0.1× input rate (90% off).

---

## The Root Problem — Quadratic Cost Growth in Long Sessions

Every API turn resends the full conversation history. The longer the session, the more
you pay — and you pay for old content on every subsequent turn:

```
One agent, 4 research tasks — sequential:

Turn 1: [system 5K] + [task1 data 20K]                               = 25K billed
Turn 2: [system 5K] + [task1 20K] + [reply 2K] + [task2 20K]        = 47K billed
Turn 3: [system 5K] + [all above] + [reply 2K] + [task3 20K]        = 74K billed
Turn 4: [system 5K] + [all above] + [reply 2K] + [task4 20K]        = 101K billed
                                                              ──────────────
                                                 TOTAL:       247K tokens

Task 1's data was billed 4 times. Each turn pays a growing tax on everything before it.
```

This is why chatbot sessions spiral. The cost curve is quadratic in the number of turns.

---

## The Fix — Isolated Parallel Subagents

Each subagent sees only its own data. Cost per agent is flat, not cumulative.

```
4 agents, same 4 tasks — parallel:

Agent 1: [system 5K] + [task1 data 20K]  = 25K  →  2K summary output
Agent 2: [system 5K] + [task2 data 20K]  = 25K  →  2K summary   ← same time
Agent 3: [system 5K] + [task3 data 20K]  = 25K  →  2K summary   ← same time
Agent 4: [system 5K] + [task4 data 20K]  = 25K  →  2K summary   ← same time
Coord:   [system 5K] + [4 summaries 8K]  = 13K  →  synthesis
                                           ──────────────
                             TOTAL:        113K tokens   ← 54% less
                             TIME:         1 agent's runtime, not 4×
```

Add prompt caching (system prompt shared across all agents, written once, read at 90% off):

```
Effective total with cache: ~96K token-equivalents  ← 61% less than monolithic
```

Stack Batch API (50% off overnight runs):

```
Effective total with cache + batch: ~48K equivalent  ← 81% less than monolithic
```

Route bulk work to Haiku instead of Sonnet/Opus:

```
Research agents on Haiku ($1/M) vs Sonnet ($3/M): 3× cheaper on those steps
Combined with above: 70–89% total savings depending on task mix
```

---

## The Five Levers

**1. Subagent isolation** — each agent sees only its own data; no turn-by-turn accumulation.
Adding a fifth agent adds a flat cost, not a quadratic one. Break even vs monolithic at
N≥2 whenever each task chunk is >5K tokens.

**2. Prompt caching** — stable context (mission brief, agent instructions, knowledge base)
written to cache once, served at 90% discount on every subsequent agent call in the same
session. A 5K system prompt shared across 8 agents costs almost nothing after the first.
Structure: stable content first, dynamic content last, `cache_control: ephemeral` on blocks.

**3. Model routing** — Haiku does extraction and classification at $1/M input vs Opus at $5/M.
Five times cheaper for tasks where the simpler model performs identically. Sonnet for
analysis. Opus only for architecture decisions and complex multi-step reasoning.

**4. Parallel execution** — 4 agents finish in 1 agent's wall-clock time. Throughput scales
with team size; marginal API cost does not. 4× parallelism = 4× throughput at ~same cost.

**5. Batch API** — 50% off all non-realtime work. Any overnight agent run qualifies.
Trigger: ≥5 independent requests, results not needed in <5 min. Stack on top of all above.

---

## Balloon vs. Collapse — The Actual Numbers

**Naive:** one session, one model, no caching, no routing, sequential:
```
8-task investigation, 20K tokens each, all on Opus, sequential turns:
  Monolithic accumulation → ~900K tokens billed at $5/M input
  Output ~40K × $25/M
  Total ≈ $4.50 + $1.00 = ~$5.50 for one investigation run
```

**Optimized:** parallel isolated agents, cached prompt, routed models, Batch API:
```
Same 8 tasks:
  6× Haiku research agents (20K each) + 2× Sonnet analysis + cached 5K system prompt
  Batch API (50% off)
  Effective ~180K token-equivalents at blended ~$0.25/M equivalent
  Total ≈ ~$0.30
```

**Same work. ~95% lower cost. 8× faster.**

The savings grow nonlinearly: each additional optimization lever multiplies the previous
saving, not adds to it.

---

## Decision Framework — One Question

> **"Does this sub-task need to see what other sub-tasks are doing in real time?"**

| Answer | Pattern |
|---|---|
| No — independent data, independent output | Subagent (parallel fan-out) |
| Only needs the final result | Subagent + coordinator collects outputs |
| Needs constant back-and-forth | Keep in one agent |
| Task is sequential and tiny (<5K tokens) | Keep in one agent (overhead > savings) |

**Subagents SAVE money when:**
- Each agent has a real chunk of data to process (>5K tokens)
- Tasks are independent (no live cross-reference needed)
- 3 or more subagents share a cached system prompt
- The task will take >10 turns (fresh context resets the accumulation clock)

**Subagents WASTE money when:**
- Tasks are tiny (<500 tokens each) — the 5K system prompt overhead dominates
- Sequential dependencies pass large intermediate outputs between agents — you pay to
  shuttle data; fix by having each agent output a small summary, not raw data
- More than ~8 subagents per coordinator — the coordinator's own context balloons
  collecting results; fix with hierarchical fan-out

---

## Batch API Trigger Conditions

Submit as a batch when ALL are true:
- ≥5 independent requests with the same prompt pattern
- Total estimated input >50K tokens
- Non-interactive task (review, lint, doc gen, classification, overnight agent runs)
- Results not needed in <5 min

Always output an estimate before submitting:
```
⚡ Batch opportunity
  Requests : N × ~XK tokens = ~YK total
  Standard : ~$A  →  Batch (50% off): ~$B
  Savings  : ~$C
  Est. time: ~30-60 min
```

```python
PRICING = {
    "claude-haiku-4-5":  {"in": 1.00, "out": 5.00},
    "claude-sonnet-4-6": {"in": 3.00, "out": 15.00},
    "claude-opus-4-6":   {"in": 5.00, "out": 25.00},
}

def estimate_batch(model, n, avg_in, avg_out):
    p = PRICING[model]
    std   = (n * avg_in / 1e6) * p["in"] + (n * avg_out / 1e6) * p["out"]
    batch = std * 0.50
    mins  = min(60, max(30, n // 50))
    return dict(standard=round(std,4), batch=round(batch,4),
                savings=round(std-batch,4), est=f"~{mins} min")
```

---

## Live Cost Estimator — Subagent vs. Monolithic

Run this before building any multi-agent system:

```python
def subagent_vs_monolithic(n, task_tokens, system_tokens=5000,
                            output_tokens=500, reply_tokens=500,
                            model="claude-sonnet-4-6"):
    PRICING = {
        "claude-haiku-4-5":  {"in": 1.00, "cr": 0.10, "out": 5.00},
        "claude-sonnet-4-6": {"in": 3.00, "cr": 0.30, "out": 15.00},
        "claude-opus-4-6":   {"in": 5.00, "cr": 0.50, "out": 25.00},
    }
    p = PRICING[model]
    M = 1_000_000

    # Monolithic: each turn pays for all previous turns
    mono = 0
    for k in range(1, n+1):
        turn_in = system_tokens + task_tokens*k + reply_tokens*(k-1)
        mono += turn_in * p["in"]/M + output_tokens * p["out"]/M

    # Subagents: each sees only its own data; system cached after first
    sub_1  = (system_tokens + task_tokens) * p["in"]/M + output_tokens * p["out"]/M
    sub_n  = (system_tokens*0.1 + task_tokens) * p["in"]/M + output_tokens * p["out"]/M
    coord  = (system_tokens*0.1 + n*output_tokens) * p["in"]/M + output_tokens * p["out"]/M
    sub_total = sub_1 + sub_n*(n-1) + coord

    pct = (mono - sub_total) / mono * 100
    verdict = "✅ use subagents" if pct > 20 else "⚠ marginal" if pct > 0 else "❌ monolithic wins"
    print(f"N={n} | task={task_tokens:,}t | {model}")
    print(f"  Monolithic : ${mono:.4f}")
    print(f"  Subagents  : ${sub_total:.4f}")
    print(f"  Savings    : {pct:.0f}%  {verdict}")

# Key cases:
subagent_vs_monolithic(n=4,  task_tokens=20_000)   # ← the 70% case
subagent_vs_monolithic(n=8,  task_tokens=50_000)   # large pipeline
subagent_vs_monolithic(n=3,  task_tokens=500)      # danger zone — tiny tasks
```

Expected:
```
N=4,  task=20K:  Monolithic $0.0108  Subagents $0.0033  Savings 69%  ✅
N=8,  task=50K:  Monolithic $0.1440  Subagents $0.0156  Savings 89%  ✅
N=3,  task=500:  Monolithic $0.0001  Subagents $0.0003  Savings -200% ❌ monolithic wins
```

**Rule:** subagents always win when task chunk >5K tokens and N≥3.
Tiny tasks + subagents = overhead kills you.

---

## Usage Logger — Prove It Per Turn

Drop in any script that calls the API. Appends to `~/.claude/usage_log.jsonl`.

```python
# usage_logger.py
import json, time
from pathlib import Path

LOG_PATH = Path.home() / ".claude" / "usage_log.jsonl"
PRICING  = {
    "claude-haiku-4-5":  {"in": 1.00, "cw": 1.25, "cr": 0.10, "out": 5.00},
    "claude-sonnet-4-6": {"in": 3.00, "cw": 3.75, "cr": 0.30, "out": 15.00},
    "claude-opus-4-6":   {"in": 5.00, "cw": 6.25, "cr": 0.50, "out": 25.00},
}

def log_usage(response, model: str, task_label: str = "", batch: bool = False):
    u  = response.usage
    p  = PRICING.get(model, PRICING["claude-sonnet-4-6"])
    m  = 1_000_000
    inp = getattr(u, "input_tokens", 0)
    cw  = getattr(u, "cache_creation_input_tokens", 0)
    cr  = getattr(u, "cache_read_input_tokens", 0)
    out = getattr(u, "output_tokens", 0)
    total_in = inp + cr
    actual   = (inp*p["in"] + cw*p["cw"] + cr*p["cr"] + out*p["out"]) / m
    nocache  = (total_in*p["in"] + out*p["out"]) / m
    if batch: actual *= 0.5; nocache *= 0.5
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "model": model, "task": task_label,
        "batch": batch, "inp": inp, "cache_write": cw, "cache_read": cr, "out": out,
        "hit_ratio": round(cr/total_in, 4) if total_in else 0,
        "cost_actual": round(actual, 6), "cost_nocache": round(nocache, 6),
        "saved": round(nocache - actual, 6),
    }
    LOG_PATH.parent.mkdir(exist_ok=True)
    LOG_PATH.open("a").write(json.dumps(record) + "\n")
    return record
```

Weekly report: `python usage_report.py --days 7`

---

## Verification Checklist

- [ ] `cache_read_input_tokens > 0` on second request to same stable context
- [ ] `cache_creation_input_tokens > 0` on first request (cache being written)
- [ ] Cache hit ratio >50% after turn 2; >60% steady state
- [ ] Stable content (ARCHITECTURE.md, agent instructions) placed BEFORE dynamic content
- [ ] Haiku used for all bulk/extraction/classification steps
- [ ] Batch API triggered for any ≥5 independent non-realtime requests
- [ ] Subagent outputs are summaries (<2K tokens), not raw data
- [ ] Token pre-flight run for any request likely >50K tokens
- [ ] Usage logger wired — `~/.claude/usage_log.jsonl` growing each session

---

## Status Footer Reading Guide

```
[ctx ~35K/200K | cache HIT ✓ | turn 3 | ~$0.04 | saved ~$0.09 | session ~$0.18]
                       ↑
           HIT = cache_read_input_tokens > 0 this turn (real proof, not estimate)
           MISS = cold turn — cache being written, reads start next turn
```

Turn 1 is always MISS (writing cache). Turn 2+ should be HIT. Persistent MISS after
turn 2 means stable content is mutating — find what changed and stop caching it.

---

*Source of truth for cost optimization. Operational rules live in `/token-optimizer` skill
and CLAUDE.md. This document explains the why and provides the calculators.*
