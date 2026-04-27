---
type: architecture
blueprint: "[[Blueprints/Hive-Design.blueprint]]"
agent_type: documentation-engineer
status: final
doc_hash: sha256:48a71b81c97099fcd86a85dc36870706f12b9214a6d82e1689a3d0ddf1c4479f
created: 2026-04-06
hash_ts: 2026-04-07T00:06:57Z
hash_method: body-sha256-v1
---

# Cheap Model Routing — Faerie Hierarchical Dispatch

**Problem:** Claude Code's Agent tool is locked to Anthropic models. Many faerie tasks are trivial (classify, route, summarize, tier) and don't need Sonnet or Opus. Free/cheap models (Llama, Mistral, local Ollama) can solve these for $0–$0.01 vs $0.50+ for Sonnet.

**Solution:** Hierarchical task routing — dispatch based on task complexity tier, with fallback chain from free → cheap → local → Haiku.

---

## The Constraint

Claude Code's **Agent tool** supports only Anthropic models and routes through faerie's spawning mechanism. This is fine for deep work (research, code review, synthesis), but wasteful for:

- Text classification (is this urgent/routine?)
- Routing decisions (which queue should this go to?)
- Bulk Q&A (summarize 100 documents)
- Tier scoring (evidence ranking, priority assessment)

**Alternative:** Bash + `openrouter_agent.py` script can reach any endpoint (OpenRouter, Ollama, Anthropic directly). But Bash is synchronous and requires manual orchestration.

**Result:** Two-channel dispatch:
- **Agent tool** (async, Anthropic-locked) for deep/sensitive work
- **Bash script** (sync, flexible, cheap) for bulk/simple work

---

## Task Complexity Tiers

Every queued task gets a `complexity` field. The orchestrator uses this to pick the spawn path.

| Tier | Model | Cost | Latency | Best for | Spawn via |
|---|---|---|---|---|---|
| **free** | Llama 3.1 8B (OpenRouter) | $0.00 | ~5–10s | Classification, routing, scoring | Bash + openrouter_agent.py |
| **cheap** | Mistral 7B (OpenRouter) | ~$0.01/1M | ~3–8s | Small enrichment, Q&A | Bash + openrouter_agent.py |
| **local** | Ollama (self-hosted) | $0.00 | ~2–5s | Batch ops (requires Ollama running) | Bash + openrouter_agent.py |
| **haiku** | Claude Haiku 4.5 | ~$1/1M input | ~2–4s | Fallback, reliable baseline | Bash + openrouter_agent.py OR Agent tool |
| **sonnet** | Claude Sonnet 4.6 | ~$3/1M input | ~3–5s | Features, code, research | Agent tool only |
| **opus** | Claude Opus 4.6 | ~$15/1M input | ~8–15s | Deep architecture, complex reasoning | Agent tool only |

---

## Queue Task Fields Driving Routing

Each task in `Queue/sprint-queue.md` specifies:

```markdown
## Task: Extract invoice data
- category: data         (what class of work — data, evidence, analysis, pipeline, etc.)
- complexity: free       (cheap, local, haiku, sonnet, opus)
- model_tier: free       (alias for complexity — for clarity)
- description: Extract dates and amounts from PDFs
- next_on_success: Task B
- next_on_failure: Task A-retry
```

**Faerie's `_pick_agent()` function** will:

1. Read `complexity` field
2. Route based on:
   - `free` / `cheap` / `local` → Bash dispatch
   - `haiku` → Bash (unless Anthropic API key missing, then Agent tool)
   - `sonnet` / `opus` → Agent tool only

---

## Dispatch Flow

### Path 1: Bash + openrouter_agent.py (free/cheap/local)

```
faerie reads task from queue
  ├─ complexity: free
  ├─ task_id: T42
  └─ prompt: "classify this as urgent/routine"
       ↓
faerie spawns: bash -c 'python3 scripts/openrouter_agent.py --task-id T42 --tier free'
       ↓
openrouter_agent.py runs
  ├─ tries free tier first
  ├─ if rate-limited/fails → fallback chain (cheap, local, haiku)
  └─ writes result to ~/.claude/hooks/state/openrouter-result-{T42}.json
       ↓
bash returns JSON to faerie
       ↓
faerie reads result, chains next task

Cost: $0–$0.01 per task
Latency: 3–10 seconds
Limit: ~100 free requests/day on OpenRouter; local is unlimited if running Ollama
```

### Path 2: Agent Tool (sonnet/opus, or haiku if available)

```
faerie reads task from queue
  ├─ complexity: sonnet
  ├─ category: analysis
  └─ prompt: "correlate these evidence items"
       ↓
faerie spawns: Agent tool with research-analyst
       ↓
research-analyst runs (Sonnet context, 200K budget)
  ├─ deep synthesis
  └─ writes to vault
       ↓
memory-keeper collects result
       ↓
faerie chains next task

Cost: $0.50–$2.00 per task
Latency: 3–5 seconds (or minutes for synthesis)
Limit: No hard limit; context budget is constraint
```

### Path 3: Mixed (free initial triage + sonnet deep dive)

```
Task 1: "Triage these 50 evidence items — free tier
  ├─ Bash dispatch → openrouter_agent.py --tier free
  └─ Result: 10 high-priority, 40 low-priority

Task 2: "Synthesize the 10 high-priority items" — sonnet
  ├─ Agent tool dispatch
  └─ Result: synthesis report
```

**Two-phase pattern:** Cheap triage upstream, expensive synthesis downstream. Cost: O(log N) instead of O(N).

---

## Implementation: Extending faerie's `_pick_agent()`

**Current behavior:**
```python
def _pick_agent(task):
    return ("research-analyst", "agent_tool")  # always Sonnet via Agent tool
```

**Extended behavior:**
```python
def _pick_agent(task):
    complexity = task.get("complexity", "sonnet").lower()
    category = task.get("category", "general")
    
    # Route by complexity tier
    if complexity in ("free", "cheap", "local"):
        return ("openrouter", "bash", {"tier": complexity, "task_id": task["id"]})
    elif complexity == "haiku":
        if ANTHROPIC_API_KEY_AVAILABLE:
            return ("openrouter", "bash", {"tier": "haiku"})
        else:
            return ("research-analyst", "agent_tool")  # fallback to Agent tool
    elif complexity == "sonnet":
        # Pick best sonnet-class agent based on category
        if category == "evidence":
            return ("evidence-curator", "agent_tool")
        elif category == "analysis":
            return ("data-scientist", "agent_tool")
        else:
            return ("research-analyst", "agent_tool")
    else:  # opus
        return ("knowledge-synthesizer", "agent_tool")
```

**Bash spawn handler:**
```bash
# In faerie/workflow-orchestrator or run loop
if [ "$spawn_method" = "bash" ]; then
    python3 scripts/openrouter_agent.py \
        --task-id "$task_id" \
        --tier "$tier" \
        --task "$(cat task.json | jq -r .prompt)"
    
    result_path="~/.claude/hooks/state/openrouter-result-${task_id}.json"
    faerie reads result from $result_path
    faerie chains next_on_success or next_on_failure based on exit code
fi
```

---

## Cost Impact Table

**Example: Evidence classification task (10,000 items)**

| Route | Model | Cost | Time | Sensitivity |
|---|---|---|---|---|
| Haiku direct | Claude Haiku | ~$10 | ~30min | Medium |
| Sonnet direct | Claude Sonnet | ~$30 | ~20min | High |
| Free tier | Llama 3.1 8B | $0 | ~40min | Low (rate-limited) |
| **Free + Sonnet filter** | Llama + Sonnet | ~$2 | ~45min | High (only best get deep review) |
| Local Ollama | Llama 3.1 (self) | $0 | ~50min | Medium (depends on hardware) |

**Recommendation:** Use free tier for **triage** (scoring, classification, routing), then Sonnet for the narrowed-down set that matters.

---

## What NOT to Route to Free Models

Sacred zones (never send to cheap tier):

- **Forensic COC tasks** — chain of custody verification needs audit trail & reliability
- **Evidence analysis** — investigation-sensitive; requires Sonnet/Opus for defensibility
- **Security decisions** — access control, permission grants; can't trust cheap models
- **Findings synthesis** — complex correlations; cheap models hallucinate connections
- **Report writing** — final-form output for human review; needs polish
- **Contract/legal analysis** — regulatory risk; needs senior model

**Safe to route to free:**
- Triage / ranking (which items matter most?)
- Bulk classification (is this spam? relevant? high-priority?)
- Q&A summarization (what does this document say?)
- Routing logic (which queue should this go to?)
- Data enrichment (add metadata to structured items)
- Format conversion (JSON ↔ CSV, markdown cleanup)
- Link extraction (pull URLs from text)

**Decision rule:** If the task is **input-driven and reversible** (bad output doesn't cause harm — you can rerun with Sonnet), it's safe for cheap models.

---

## Integration with Faerie's Wave System

Faerie orchestrates work in three waves (W1, W2, W3) by model tier:

| Wave | Model | Agents | Use for |
|---|---|---|---|
| **W1** | Haiku | error-coordinator, validator, router | Triage, blocker detection, routing |
| **W2** | Sonnet | researchers, engineers, analysts | Features, research, code, synthesis |
| **W3** | Opus | knowledge-synthesizer, architect | Deep cross-correlation, architecture |

**New pattern: Micro-waves inside W1**

```
W0.5 (micro-wave)  → Free tier triage (Bash + openrouter_agent.py)
W1                 → Haiku validation (Agent tool)
W2                 → Sonnet detail work (Agent tool)
W3                 → Opus synthesis (Agent tool)
```

This lets faerie triage at massive scale (1000s of items in seconds for $0) before engaging expensive workers.

---

## Configuration

### To enable cheap model routing:

1. **Set environment variables** (see `.env.example`):
   ```bash
   OPENROUTER_API_KEY=sk-or-...
   ANTHROPIC_API_KEY=sk-ant-...
   OLLAMA_BASE_URL=http://localhost:11434  # optional
   ```

2. **Add to task queue** (example):
   ```markdown
   ## Task: Rank these 100 evidence items by relevance
   - category: evidence
   - complexity: free
   - description: Use keyword frequency to score relevance
   - next_on_success: Task B (synthesize top 10)
   ```

3. **Faerie auto-routes** based on complexity field.

### Fallback behavior:

If you don't set `OPENROUTER_API_KEY`:
- Free tier → unavailable
- Cheap tier → unavailable
- Local tier → works if Ollama is running
- Haiku → works if `ANTHROPIC_API_KEY` is set (uses Anthropic native API)

If all fail → faerie logs error and skips task (or retries with next complexity level).

---

## Monitoring & Cost Tracking

Each `openrouter_agent.py` result includes:

```json
{
  "result": "...",
  "model_used": "meta-llama/llama-3.1-8b-instruct:free",
  "tier_used": "free",
  "tokens_in": 150,
  "tokens_out": 42,
  "cost_estimate": "$0.00",
  "fallback_used": false,
  "task_id": "T42",
  "elapsed_s": 3.2
}
```

**Faerie can aggregate costs** by tier:

```bash
# Count tasks by tier and cost
ls ~/.claude/hooks/state/openrouter-result-*.json | wc -l  # total tasks via bash
jq '.tier_used' *.json | sort | uniq -c  # breakdown by tier
jq '.cost_estimate' *.json | paste -sd+ | bc  # total cost
```

---

## Why This Matters

1. **Cost reduction:** 50–100x savings on triage and bulk ops
2. **Speed:** Free tier is faster than Sonnet for trivial tasks (10s vs 3–5s)
3. **Scalability:** Can process 1000s of items in a sprint without consuming Sonnet quota
4. **Reliability:** Expensive workers (Sonnet/Opus) reserved for work that needs them
5. **Fairness:** Cheap work costs cheap; deep work costs appropriately

---

## Further Reading

- **`.env.example`** — Environment variables setup guide
- **`scripts/openrouter_agent.py`** — Full implementation of tier routing & fallback chain
- **`ARCHITECTURE.md`** — Faerie's full orchestration model
- **`Queue/sprint-queue.md` (in vault)** — Task queue with complexity field examples
- **OpenRouter docs** — https://openrouter.ai (free tier documentation)
- **Ollama docs** — https://ollama.ai (self-hosted inference)
