# Cheap Model Routing

## Problem

Claude Code's `Agent` tool is locked to Anthropic models (haiku/sonnet/opus). Many
faerie tasks -- classification, routing decisions, bulk Q&A, summarization -- do not
need Sonnet-grade intelligence. Running them on free or cheap models saves cost without
sacrificing quality.

## Architecture

Two execution paths coexist:

```
faerie _pick_agent()
  |
  +-- complexity=hard/deep --> Agent tool (sonnet/opus)
  |                            Native Claude Code subagent
  |
  +-- complexity=easy/medium --> Bash tool
       python3 scripts/openrouter_agent.py --tier free --task "..."
       Returns JSON to stdout; faerie reads it
```

**Path A (Agent tool):** Standard faerie subagent spawning. Full Claude Code sandbox,
tool access, MEM blocks, streaming. Used for anything requiring reasoning, code writing,
multi-step work, or forensic-sensitive tasks.

**Path B (Bash-spawned cheap model):** A Python script calls an OpenAI-compatible API
(OpenRouter, Ollama, or Anthropic Haiku as fallback). Returns structured JSON. No tool
access, no file writes beyond the result JSON. Used for simple, stateless tasks.

## Model Tier Table

| Tier | Model | Endpoint | Cost/1M in | Cost/1M out | Latency | Quality |
|------|-------|----------|-----------|------------|---------|---------|
| `free` | meta-llama/llama-3.1-8b-instruct:free | OpenRouter | $0 | $0 | 1-5s | Low-medium |
| `cheap` | mistralai/mistral-7b-instruct:free | OpenRouter | $0 | $0 | 1-3s | Low-medium |
| `local` | llama3.1 | Ollama (localhost:11434) | $0 | $0 | 0.5-2s | Medium |
| `haiku` | claude-haiku-4-5 | Anthropic | $0.80 | $4.00 | 0.5-1s | High |
| `sonnet` | claude-sonnet-4-6 | Agent tool | $3.00 | $15.00 | 1-3s | Very high |
| `opus` | claude-opus-4-6 | Agent tool | $15.00 | $75.00 | 2-5s | Highest |

**Cost comparison for 10K classification tasks (~200 tokens each):**
- Free tier: $0.00
- Haiku: ~$1.60
- Sonnet: ~$6.00
- Opus: ~$30.00

## Fallback Chain

If the requested tier fails (missing API key, rate limit, network error), the script
tries the next tier automatically:

```
free  --> cheap --> local --> haiku
cheap --> free  --> local --> haiku
local --> free  --> cheap --> haiku
haiku --> (no fallback -- last resort)
```

The result JSON includes `fallback_used: true` and `original_tier` when a fallback fires.

## Usage

### Direct CLI

```bash
# Simple task
python3 scripts/openrouter_agent.py --task "Classify: is this a phishing email?" --tier free

# From prompt file
python3 scripts/openrouter_agent.py --prompt-file task.json --tier cheap --task-id T42

# Piped JSON
echo '{"task":"summarize this","content":"..."}' | python3 scripts/openrouter_agent.py --tier local

# List available tiers
python3 scripts/openrouter_agent.py --list-tiers
```

### From faerie (Bash tool spawn)

```python
# In faerie's task execution, when complexity=easy:
result = Bash("python3 scripts/openrouter_agent.py --task 'classify: ...' --tier free --task-id T42")
parsed = json.loads(result.stdout)
```

### Prompt file format

```json
{
  "task": "Classify the following text as SPAM or HAM",
  "content": "You have won a free iPhone...",
  "system": "You are a text classifier. Respond with exactly one word: SPAM or HAM."
}
```

### Result format

```json
{
  "content": "SPAM",
  "model_used": "meta-llama/llama-3.1-8b-instruct:free",
  "tier_used": "free",
  "tokens_in": 45,
  "tokens_out": 1,
  "cost_estimate": "$0.0000",
  "fallback_used": false,
  "elapsed_s": 1.23,
  "task_id": "T42",
  "result_path": "/home/user/.claude/hooks/state/openrouter-result-T42.json"
}
```

## Faerie Routing Integration

### Task complexity field

Queue tasks gain a `model_tier` or `complexity` field:

```json
{
  "task_id": "T42",
  "type": "classify",
  "complexity": "easy",
  "model_tier": "free",
  "prompt": "Classify this text..."
}
```

### _pick_agent() extension

The existing `_pick_agent()` (or equivalent routing logic) checks model_tier before
spawning via Agent tool:

```python
def _pick_agent(task):
    tier = task.get("model_tier") or infer_tier(task.get("complexity", "medium"))

    if tier in ("free", "cheap", "local"):
        # Bash-spawn cheap model -- no Agent tool needed
        result = run_bash(
            f'python3 scripts/openrouter_agent.py '
            f'--task {shlex.quote(task["prompt"])} '
            f'--tier {tier} --task-id {task["task_id"]}'
        )
        return json.loads(result)

    # Standard Agent tool path
    agent_type = routing_advisor.recommend(task["category"])
    model = "haiku" if tier == "medium" else "sonnet" if tier == "hard" else "opus"
    return spawn_agent(agent_type, model=model, task=task)


def infer_tier(complexity: str) -> str:
    return {
        "easy": "free",
        "medium": "haiku",
        "hard": "sonnet",
        "deep": "opus",
    }.get(complexity, "haiku")
```

### Complexity inference from task type

| Task type | Default complexity | Tier |
|-----------|-------------------|------|
| classify, route, tag, label | easy | free |
| summarize (short text) | easy | free |
| bulk_qa (simple factual) | easy | free |
| summarize (long document) | medium | haiku |
| code_review, analysis | hard | sonnet |
| architecture, security_audit | deep | opus |
| forensic, coc_sensitive | hard+ | sonnet/opus (NEVER free) |

## Setup: OPENROUTER_API_KEY

### Option 1: Claude Code settings.json

Add to `~/.claude/settings.json` (or project `.claude/settings.json`):

```json
{
  "env": {
    "OPENROUTER_API_KEY": "sk-or-v1-..."
  }
}
```

### Option 2: Shell environment

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### Option 3: .env file (not committed)

Create `~/.claude/.env`:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

### Getting the key

1. Go to https://openrouter.ai/keys
2. Create an API key (free tier requires no payment method)
3. Free models are rate-limited (~10 req/min) but cost $0

### Ollama setup (local tier)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.1

# Ollama serves on http://localhost:11434 by default
# Override with OLLAMA_BASE_URL env var if needed
```

## Safety Boundaries

### Tasks that MUST NOT use free/cheap models

| Category | Reason | Minimum tier |
|----------|--------|--------------|
| Forensic analysis | Court-admissibility requires auditable AI | sonnet |
| Chain of custody | Hash verification, evidence handling | sonnet |
| Security audit | False negatives have real consequences | sonnet |
| Complex reasoning | Multi-step logic, architecture design | sonnet/opus |
| Code generation | Correctness matters more than cost | haiku+ |
| Any COC-sensitive task | Forensic integrity is non-negotiable | sonnet |

### Tasks well-suited for free/cheap models

| Category | Examples |
|----------|----------|
| Classification | spam/ham, sentiment, topic routing |
| Routing decisions | "which agent should handle this?" |
| Simple Q&A | factual lookups, definitions |
| Bulk summarization | one-paragraph summaries of short texts |
| Text formatting | reformatting, template filling |
| Data extraction | pulling structured fields from text |

## Monitoring and Cost Tracking

Each call writes a result JSON to `~/.claude/hooks/state/openrouter-result-{task_id}.json`.
These accumulate and can be aggregated:

```bash
# Count calls by tier
python3 -c "
import json, glob
from collections import Counter
files = glob.glob(os.path.expanduser('~/.claude/hooks/state/openrouter-result-*.json'))
tiers = Counter()
for f in files:
    d = json.load(open(f))
    tiers[d.get('tier_used', 'unknown')] += 1
print(json.dumps(dict(tiers), indent=2))
"
```

Faerie's token-optimizer agent can read these results to track actual savings vs
the Agent-tool path.

## Design Decisions

**Why not use the `anthropic` SDK with base_url override?**
The anthropic SDK is not installed in the faerie2 repo's Python environment. Using
`httpx` (which is available) to call the OpenAI-compatible chat completions endpoint
works with both OpenRouter and Ollama without additional dependencies.

**Why JSON to stdout instead of file-only output?**
Faerie reads Bash tool output from stdout. Writing to a file AND stdout gives both
the immediate Bash-readable result and a persistent record for auditing.

**Why not a long-running server?**
A per-call script avoids PID management complexity, port conflicts, and zombie
processes. Each call is stateless. The HTTP overhead (~100ms) is negligible vs
model inference time (~1-5s).

**Why fallback to Haiku, not Sonnet?**
Haiku is 3.75x cheaper than Sonnet and handles all "easy" tasks well. If a task
needs Sonnet-grade reasoning, it should have been routed to the Agent tool path
in the first place, not the cheap-model runner.
