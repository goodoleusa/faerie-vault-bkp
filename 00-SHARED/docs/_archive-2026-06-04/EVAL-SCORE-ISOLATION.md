# Eval Score Isolation — Sacred Separation of Claude vs Free Models

**Date:** 2026-04-22  
**Status:** Architecture rule (non-negotiable)  
**Scope:** Training, evaluation, and benchmarking workflows  
**Goal:** Prevent free model results from contaminating Claude agent baseline scores  

---

## The Problem

Without isolation, mixing Claude and free model evals creates confusion:

```
Agent: evidence-curator
Last Score: 0.87 (Claude 3.5 Sonnet, forensic analysis)
BUT: This session ran W1 evidence-curator on Mistral free tier
     and got 0.45 (because Mistral can't do forensic work correctly)
Result: Baseline corrupted. Is the agent degrading or was Mistral just wrong?
```

**Solution:** Separate eval tracks—Claude agents track vs Free agent track. No cross-contamination.

---

## Architecture: Two Parallel Benchmark Systems

### Track 1: Claude Agent Benchmarks (Source of Truth)

```
~/.claude/hooks/state/benchmarks/claude/
  evidence-curator.json
  data-scientist.json
  report-writer.json
  [all native Claude agents]
```

**Metrics:**
- Training score (constraint-based drills)
- Deployment score (real work OTJ)
- Tier level (1, 2, 3, 4)
- Baseline score (stable reference)

**Rules:**
- Updated only when Claude agents run (W2, W3)
- Compared against prior Claude scores (not free models)
- Baseline promotion requires sustained ≥0.90 on Claude runs
- Tier graduation on Claude scores only

### Track 2: Free Agent Benchmarks (Isolated)

```
~/.claude/hooks/state/benchmarks/free/
  mistral-bulk.json
  llama-fast.json
  qwen-coder.json
  [all OpenRouter free agents]
```

**Metrics:**
- Bulk throughput (tasks/minute on free tier)
- Quality on tasks they're good at (text extraction, summarization)
- Cost-quality tradeoff vs Claude baseline
- When to use (is this task worth the free tier?)

**Rules:**
- Updated only when free agents run (W1)
- Compared against prior free model scores (not Claude)
- Baseline is independent (free models have different capability curve)
- Evaluated on "is this free model good enough for this category?" not "is it as good as Claude?"

---

## Eval Workflow: Sacred Separation

### When W1 (Free) Runs

```python
# Agent spawned: mistral-bulk (free tier)
# Task: Summarize 50 documents

# Results stored SEPARATELY:
~/.claude/hooks/state/benchmarks/free/mistral-bulk.json
  {
    "agent": "mistral-bulk",
    "provider": "openrouter",
    "model": "mistralai/mistral-7b-instruct:free",
    "task_category": "bulk_summarize",
    "score": 0.82,  ← how well Mistral does bulk summarization
    "cost_usd": 0.00,
    "throughput_tasks_per_min": 8.5,
    "vs_claude_baseline": 0.92  ← context: Claude gets 0.92 on same task
  }
```

**Key:** The score is NOT compared against Claude's 0.87 baseline for evidence-curator. They're different agents in different benchmarks.

### When W2 (Claude) Runs

```python
# Agent spawned: evidence-curator (Claude)
# Task: Analyze evidence for forensic report

# Results stored SEPARATELY:
~/.claude/hooks/state/benchmarks/claude/evidence-curator.json
  {
    "agent": "evidence-curator",
    "provider": "claude",
    "model": "claude-3.5-sonnet",
    "context": "forensic_evidence_analysis",
    "score": 0.87,  ← how well Claude does forensic analysis
    "vs_prior": 0.84,  ← compared to prior Claude run (0.84)
    "delta": +0.03,
    "baseline_status": "stable"  ← baseline unchanged (needs 3x ≥0.90)
  }
```

**Key:** Only compared against Claude's prior scores, not free models.

---

## Scoring Rules (Golden Rules)

### Rule 1: Benchmark Group Isolation

```python
def get_benchmark_path(agent_type: str, model: str, provider: str) -> Path:
    """Never mix Claude and free benchmarks."""
    if provider == "openrouter":
        return Path.home() / ".claude" / "hooks" / "state" / "benchmarks" / "free"
    elif provider == "claude":
        return Path.home() / ".claude" / "hooks" / "state" / "benchmarks" / "claude"
    else:
        raise ValueError(f"Unknown provider: {provider}")
```

### Rule 2: Baseline Comparison (Self Only)

```python
# DO THIS: Compare new Claude score against prior Claude score
prior_claude_score = load_latest_score("claude", "evidence-curator")
improvement = new_score - prior_claude_score

# DON'T DO THIS: Compare new free model score against Claude baseline
NOT: improvement = free_model_score - prior_claude_score  # ❌ WRONG
```

### Rule 3: Agent Identity Tied to Provider

```python
# Same agent type, different providers = DIFFERENT agents
Agent("evidence-curator") on Claude      # ~/.claude/agents/evidence-curator.md
Agent("mistral-bulk") on OpenRouter      # ~/.claude/agents/free/mistral-bulk.md

# They have:
# - Different card files
# - Different benchmark files
# - Different eval processes
# - Different training tracks
```

### Rule 4: Eval Harness Routing

```python
# eval_harness.py logic:

if model.startswith("claude"):
    benchmark_group = "claude"
    baseline_file = f"benchmarks/claude/{agent_type}.json"
    comparison_pool = "claude_prior_scores"  # Only compare to Claude
elif "free" in model or "openrouter" in model:
    benchmark_group = "free"
    baseline_file = f"benchmarks/free/{agent_slug}.json"
    comparison_pool = "free_prior_scores"    # Only compare to free models
else:
    raise ValueError(f"Unknown model: {model}")

# Load baseline ONLY from matching group
prior_score = load_baseline(baseline_file, comparison_pool)
```

---

## Dashboard: Cost-Quality Tradeoff (Separate Tables)

When faerie reports at end of cycle:

```
AGENT PERFORMANCE (Claude Track — Source of Truth)
════════════════════════════════════════════════════════════════
Agent               | Last Score | Prior | Delta  | Tier | Status
────────────────────┼────────────┼───────┼────────┼──────┼──────────────
evidence-curator    | 0.87       | 0.84  | +0.03  | 1    | stable
data-scientist      | 0.92       | 0.91  | +0.01  | 1    | approaching 0.90 baseline
report-writer       | 0.79       | 0.80  | -0.01  | 1    | slight decline
────────────────────┴────────────┴───────┴────────┴──────┴──────────────

COST OPTIMIZATION (Free Tier Track — Cost-Quality Tradeoff)
════════════════════════════════════════════════════════════════
Agent          | Score | Tasks/Min | Cost | vs Claude | Recommendation
───────────────┼───────┼───────────┼──────┼──────────┼─────────────────
mistral-bulk   | 0.82  | 8.5       | $0   | -0.10    | Good for bulk summarize
llama-fast     | 0.75  | 12.0      | $0   | -0.17    | OK for simple triage
qwen-coder     | 0.88  | 4.2       | $0   | -0.04    | Good for code review
───────────────┴───────┴───────────┴──────┴──────────┴─────────────────

COST SAVINGS (This Cycle)
════════════════════════════════════════════════════════════════
Wave | Model Used | Tasks | Cost    | vs All-Claude
─────┼────────────┼───────┼─────────┼─────────────────
W1   | Mistral    | 15    | $0.00   | Saves $4.50
W2   | Sonnet     | 8     | $3.20   | (baseline)
W3   | Opus       | 2     | $12.50  | (deep work)
─────┴────────────┴───────┴─────────┴─────────────────
Total: $15.70 | Savings: $4.50 (28% reduction)
```

**Note:** The free tier scores (0.82, 0.75, 0.88) are NOT compared against Claude scores. They answer different questions: "Is this free model good enough for this task type?" vs "Is the agent improving?"

---

## Training & Improvement Tracking

### Claude Agents (Normal Training)

```python
# Training via /train --run evidence-curator

# Self-update on beat baseline:
if new_score > prior_claude_score:
    agent_card.last_training.score = new_score
    agent_card.last_training.delta = new_score - prior_claude_score
    agent_card.last_training.context = "training|deployment"  # which track
    # Updated in: ~/.claude/agents/evidence-curator.md
```

### Free Agents (Separate Training Track)

```python
# Training via /train --run llama-fast

# Self-update on beat baseline:
if new_score > prior_free_score:
    agent_card.last_training.score = new_score
    agent_card.last_training.context = "free_tier_benchmark"
    # Updated in: ~/.claude/agents/free/llama-fast.md
    # NOT compared to Claude baseline
```

---

## Config: Enforcement Rules

Add to `~/.claude/settings.json`:

```json
{
  "eval_score_isolation": {
    "enabled": true,
    "rules": {
      "sacred_forbidden_for_free": [
        "forensic",
        "coc",
        "evidence",
        "security_analysis",
        "hash_verification",
        "chain_of_custody"
      ],
      "baseline_comparison": {
        "claude_agents": "compare_to_claude_prior_only",
        "free_agents": "compare_to_free_prior_only",
        "mixed_runs": "separate_tracks_always"
      },
      "contamination_prevention": {
        "warn_if_free_model_on_forensic": true,
        "fail_if_free_model_on_sacred_task": true,
        "keep_benchmarks_separate": true
      }
    },
    "audit": {
      "check_monthly": "verify no cross-contamination",
      "log_location": "~/.claude/hooks/state/eval-isolation-audit.jsonl"
    }
  }
}
```

---

## Audit Trail

File: `~/.claude/hooks/state/eval-isolation-audit.jsonl` (append-only)

```json
{
  "timestamp": "2026-04-22T15:30:00Z",
  "check": "eval_score_isolation",
  "status": "pass",
  "findings": {
    "claude_benchmarks_clean": true,
    "free_benchmarks_clean": true,
    "no_cross_track_scores": true,
    "baseline_comparisons_correct": true
  }
}
```

**Monthly audit:**
```bash
python3 ~/.claude/scripts/9x_eval_isolation_audit.py --check-all
# Verifies:
# - No Claude agent baseline changed by free model score
# - No free model baseline changed by Claude score
# - All W1 evals went to free/ directory
# - All W2 evals went to claude/ directory
```

---

## Migration Path (If Existing Mixed Scores)

If you have mixed evals, clean them:

```bash
# Backup
cp -r ~/.claude/hooks/state/benchmarks ~/.claude/hooks/state/benchmarks.backup

# Create separate directories
mkdir -p ~/.claude/hooks/state/benchmarks/claude
mkdir -p ~/.claude/hooks/state/benchmarks/free

# Move Claude agent scores
mv ~/.claude/hooks/state/benchmarks/evidence-curator.json benchmarks/claude/
mv ~/.claude/hooks/state/benchmarks/data-scientist.json benchmarks/claude/
[etc.]

# Move free agent scores
mv ~/.claude/hooks/state/benchmarks/mistral-bulk.json benchmarks/free/
mv ~/.claude/hooks/state/benchmarks/llama-fast.json benchmarks/free/
[etc.]

# Verify isolation
python3 ~/.claude/scripts/9x_eval_isolation_audit.py --check-all
```

---

## References

- OpenRouter agent cards: `~/.claude/agents/free/`
- Claude agent cards: `~/.claude/agents/`
- Model routing: `9x_piston_model_router.py`
- Cost dashboard: `9x_cost_dashboard.py`
- Eval harness: `eval_harness.py` (respects isolation)

---

**Status:** Sacred rule (non-negotiable, enforced by tooling)  
**Enforcement:** Automated via eval_harness.py routing  
**Audit:** Monthly check for contamination (eval-isolation-audit.py)  
**Violations:** Treated as eval integrity failures (P0 bug)
