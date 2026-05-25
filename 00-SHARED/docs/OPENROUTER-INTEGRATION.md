# OpenRouter Integration — Multi-Model Cost Optimization

**Date:** 2026-04-22  
**Status:** Implementation plan + configuration  
**Scope:** Route faerie waves to free/Claude/premium models based on task type  
**Constraint:** Eval scores isolated by model tier (no cross-contamination)  

---

## Architecture: Three Model Tiers, Three Wave Buckets

```
WAVE 1 (Triage, 45s)     → FREE MODELS (OpenRouter)
  - llama-fast (bulk text work)
  - mistral-bulk (summarization, extraction)
  - qwen-coder (code review)
  Cost: $0 per task (free tier)

WAVE 2 (Features, 180s)  → CLAUDE MODELS (Native)
  - claude-haiku-4-5-20251001 (default, medium thinking effort)
  - claude-sonnet-4-6 (fallback, higher quality)
  Cost: $3/MTok (Sonnet)

WAVE 3 (Synthesis, 600s) → PREMIUM/EXTENDED (Claude API)
  - claude-opus-1 (extended thinking, $5/MTok input, $15/MTok output)
  - claude-3.5-sonnet (fallback)
  Cost: Variable (extended thinking tasks)
```

**Token Optimization:** Free tier handles 40–50% of triage volume (estimate: 30–40% cost reduction per faerie cycle).

---

## Setup: Environment Configuration

### 1. API Key Registration

```bash
# Get OpenRouter API key from https://openrouter.ai
export OPENROUTER_API_KEY="sk-or-v1-..."

# Verify connectivity
curl -s https://openrouter.ai/api/v1/models | python3 -c "import sys,json; m=json.load(sys.stdin); print(f'Available: {len(m[\"data\"])} models')"
```

### 2. Settings Configuration

Add to `~/.claude/settings.json` (or create if missing):

```json
{
  "model_routing": {
    "enabled": true,
    "default_provider": "claude",
    "wave_routing": {
      "w1": {
        "provider": "openrouter",
        "models": [
          "mistralai/mistral-7b-instruct:free",
          "meta-llama/llama-2-7b-chat:free",
          "qwen/qwen-2.5-coder-7b:free"
        ],
        "fallback": "claude-haiku"
      },
      "w2": {
        "provider": "claude",
        "models": ["claude-3.5-haiku"],
        "fallback": "claude-3.5-sonnet"
      },
      "w3": {
        "provider": "claude",
        "models": ["claude-opus-1"],
        "fallback": "claude-3.5-sonnet"
      }
    },
    "constraint_enforcement": {
      "sacred_rules": [
        "free_models CANNOT run: forensic, coc, evidence, security_analysis, hash_verification",
        "free_models CANNOT write to vault during forensic operations",
        "free_models CANNOT sign droplets or COC entries"
      ]
    },
    "cost_tracking": {
      "track_per_agent": true,
      "log_location": "~/.claude/hooks/state/model-cost-log.jsonl",
      "benchmark_against": "claude-3.5-sonnet"
    }
  }
}
```

### 3. Environment Variables (Persistent)

Add to `~/.bashrc` or shell profile:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export OPENROUTER_REFERER="https://yourcompany.ai"  # Optional, helps with rate limits
export PISTON_MODEL_ROUTING="enabled"
```

---

## Implementation: Piston Model Router

File: `~/.claude/scripts/9x_piston_model_router.py`

```python
#!/usr/bin/env python3
"""
Route agents to models based on wave + task constraints.

TIER: 9x_
REPLACES: manual model selection per spawn
METRIC: cost reduction % (target: 30–40% per faerie cycle)
LOAD: core (faerie depends on it)
"""

import json
import os
from pathlib import Path
from typing import Optional


def _load_routing_config() -> dict:
    """Load model routing config from settings.json."""
    settings_path = Path.home() / ".claude" / "settings.json"
    if not settings_path.exists():
        return {"model_routing": {"enabled": False}}
    config = json.loads(settings_path.read_text())
    return config


def select_model_for_wave(
    wave: int,
    agent_type: str,
    task_category: Optional[str] = None,
    openrouter_api_key: Optional[str] = None,
) -> dict:
    """
    Select best model for agent in given wave.
    
    Returns: {"model": "...", "provider": "claude|openrouter", "base_url": "..."}
    """
    config = _load_routing_config()
    routing = config.get("model_routing", {})
    
    if not routing.get("enabled"):
        # Fallback to default Claude
        return {"model": "claude-3.5-sonnet", "provider": "claude"}
    
    # Determine wave key
    wave_key = f"w{wave}"
    wave_config = routing.get("wave_routing", {}).get(wave_key, {})
    
    # Check sacred rules: free models can't run certain tasks
    sacred_forbidden = ["forensic", "coc", "evidence", "security_analysis", "hash_verification"]
    if task_category in sacred_forbidden and wave_config.get("provider") == "openrouter":
        # Forbidden: fall back to Claude
        return {
            "model": wave_config.get("fallback", "claude-haiku"),
            "provider": "claude"
        }
    
    # Select from available models for this wave
    models = wave_config.get("models", [])
    if not models:
        return {"model": "claude-3.5-sonnet", "provider": "claude"}
    
    # Pick first available (could add smarter selection later)
    provider = wave_config.get("provider", "claude")
    selected_model = models[0]
    
    result = {
        "model": selected_model,
        "provider": provider
    }
    
    # Add OpenRouter base URL if needed
    if provider == "openrouter":
        result["base_url"] = "https://openrouter.ai/api/v1"
        result["api_key"] = openrouter_api_key or os.environ.get("OPENROUTER_API_KEY")
    
    return result


def log_model_choice(wave: int, agent_type: str, model: str, cost_estimate: float) -> None:
    """Log model choice for cost tracking."""
    log_path = Path.home() / ".claude" / "hooks" / "state" / "model-cost-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "wave": wave,
        "agent_type": agent_type,
        "model": model,
        "estimated_cost_usd": cost_estimate,
    }
    
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 9x_piston_model_router.py <wave> <agent_type> [task_category]")
        sys.exit(1)
    
    wave = int(sys.argv[1])
    agent_type = sys.argv[2]
    task_category = sys.argv[3] if len(sys.argv) > 3 else None
    
    choice = select_model_for_wave(wave, agent_type, task_category)
    print(json.dumps(choice))
```

---

## Integration: Piston Orchestrator Updates

Update `~/.claude/scripts/piston_orchestrator.py` (or faerie BODY.md spawn logic):

```python
import subprocess
import json

# Before spawning each agent:
wave = 1  # or 2 or 3
agent_type = task["assigned_agent"]
task_category = task.get("category", "general")

# Get model choice
model_choice_json = subprocess.check_output(
    ["python3", "~/.claude/scripts/9x_piston_model_router.py", str(wave), agent_type, task_category],
    text=True
).strip()

model_choice = json.loads(model_choice_json)

# If OpenRouter, spawn via openrouter_agent.py
if model_choice["provider"] == "openrouter":
    manifest = f"~/.claude/hooks/state/wave{wave}-{agent_type}-result.json"
    subprocess.Popen([
        "python3", "~/.claude/scripts/openrouter_agent.py",
        "--tier", "free",
        "--model", model_choice["model"],
        "--task", task["goal"],
        "--task-id", task["task_id"],
        "--output-path", manifest
    ])
else:
    # Claude native spawn via Agent tool
    Agent({
        "subagent_type": agent_type,
        "team_name": f"wave{wave}-{CLAUDE_SESSION_ID[:8]}",
        "name": f"{agent_type}-{task['task_id'][:8]}",
        "model": model_choice["model"],  # ← model override
        "prompt": RENDERED_PROMPT
    })

# Log cost
cost_estimate = {
    "free": 0.0,
    "claude-haiku": 0.80,
    "claude-3.5-sonnet": 3.0,
    "claude-opus-1": 15.0,
}.get(model_choice["model"], 0.0)

subprocess.run([
    "python3", "~/.claude/scripts/9x_piston_model_router.py",
    "--log", str(wave), agent_type, model_choice["model"], str(cost_estimate)
])
```

---

## Evaluation Score Isolation (Sacred Rule)

**Problem:** Don't pollute Claude agent eval scores with free model results.

**Solution:** Separate benchmarks by tier.

### Benchmark Storage

```
~/.claude/hooks/state/benchmarks/
  claude/
    evidence-curator.json
    data-scientist.json
    ...
  free/
    mistral-bulk.json
    llama-fast.json
    ...
```

### Scoring Rules

1. **Claude agents:** Evaluated against `benchmarks/claude/{type}.json`
   - Source of truth for agent capability
   - Compared to baseline at each evalbot run
   - Determines tier promotion (sustained ≥0.90)

2. **Free agents:** Evaluated against `benchmarks/free/{slug}.json`
   - Isolated from Claude scores (no cross-contamination)
   - Tracks cost/quality tradeoff (is this free model good enough for this task?)
   - Compared to free agent baseline only

3. **Mixed runs:** When W1 uses free models and W2 uses Claude:
   - W1 results → free agent benchmarks
   - W2 results → Claude agent benchmarks
   - Cost-quality table compares them (separate rows)

### Implementation

Update `eval_harness.py`:

```python
def select_benchmark_group(agent_type: str, model: str) -> str:
    """Return benchmark group path based on model."""
    if "free" in model or "openrouter" in model:
        return "free"
    elif model.startswith("claude"):
        return "claude"
    else:
        return "custom"

benchmark_path = f"~/.claude/hooks/state/benchmarks/{select_benchmark_group(agent_type, model)}/"
```

---

## Cost Tracking Dashboard

File: `~/.claude/scripts/9x_cost_dashboard.py`

```bash
# Show cost breakdown per faerie cycle
python3 ~/.claude/scripts/9x_cost_dashboard.py --last 5

# Output example:
# FAERIE CYCLE | W1 Models | W1 Cost | W2 Models | W2 Cost | W3 Models | W3 Cost | Total
# 2026-04-22   | mistral   | $0.00   | sonnet    | $3.20   | opus-1    | $12.50  | $15.70
# 2026-04-21   | mistral   | $0.00   | sonnet    | $2.80   | sonnet    | $8.00   | $10.80
# 2026-04-20   | llama     | $0.00   | haiku     | $0.50   | sonnet    | $7.20   | $7.70
# ──────────────────────────────────────────────────────────────────────────────────
# Average: $11.40 | Savings vs all-Claude: $28/cycle (71%)
```

---

## Constraints: Sacred Rules for Free Models

**Free models CANNOT:**
- ❌ Write to forensic folders or vault forensic sections
- ❌ Sign droplets or COC entries
- ❌ Run security analysis, evidence evaluation, or hash verification
- ❌ Make final determinations on evidence or security matters
- ❌ Write to 30-Evidence/ or 01-PROTECTED/ vault zones

**Free models CAN:**
- ✅ Bulk text summarization and extraction
- ✅ Format conversion and data cleanup
- ✅ Draft-level document generation
- ✅ Code review (non-security-critical)
- ✅ Help with triage and routing

---

## Phase Rollout

### Phase 1 (This week)
- [ ] Create `9x_piston_model_router.py`
- [ ] Add settings.json model routing config
- [ ] Test W1 free models on triage tasks
- [ ] Verify eval score isolation

### Phase 2 (Week 2)
- [ ] Extend to W2 dynamic routing (use haiku if task budget permits)
- [ ] Implement cost dashboard
- [ ] Train free models (same training process as Claude, separate benchmarks)

### Phase 3 (Week 3)
- [ ] Add W3 extended-thinking routing for synthesis
- [ ] Measure 30–40% cost reduction target
- [ ] Document cost/quality tradeoff analysis

---

## References

- OpenRouter API: https://openrouter.ai/docs/api
- Free Model Tiers: https://openrouter.ai/docs/models/free
- Eval Isolation: `~/.claude/agents/free/` (separate benchmarks)
- Cost Tracking: `~/.claude/hooks/state/model-cost-log.jsonl` (append-only)

---

**Status:** Ready for Phase 1 implementation  
**Owner:** faerie orchestrator + piston model router  
**Metrics:** Cost reduction %, free model adoption rate, eval score isolation validation
