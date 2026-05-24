# Free Model Test Procedure

Step-by-step verification that the free model stable is operational.

## Prerequisites

- OPENROUTER_API_KEY set in environment (check: `echo $OPENROUTER_API_KEY | head -c 20`)
- Python 3.13+ with httpx installed (or urllib fallback will be used)
- faerie2 repo at `/mnt/d/0local/gitrepos/faerie2/`

---

## Step 1: Confirm API Key

```bash
echo $OPENROUTER_API_KEY | head -c 20
```

Expected: prints first 20 chars of key (e.g. `sk-or-v1-...`).
If blank: check `~/.claude/hooks/state/settings.json` or set in shell.

---

## Step 2: List Free Models

```bash
python3 ~/.claude/scripts/free_model_picker.py --list
# or via skill:
# /model-roster list
```

Expected output:
- Table with 30-80+ models ending in `:free`
- Columns: `#`, `Model ID`, `Context`, `Provider`
- Models already in stable marked with `*`

---

## Step 3: Test Existing Stable

```bash
python3 ~/.claude/scripts/free_model_picker.py --test-stable
# or:
# /model-roster test
```

Expected:
- 4 agents tested: llama-fast, mistral-bulk, qwen-coder, ollama-local
- Each should show `OK` with latency < 10000ms (10s)
- ollama-local will show `FAIL` if Ollama is not running locally (expected in cloud/WSL)
- Score: at least 3/4 agents healthy

If an agent shows `FAIL`:
```bash
# Get full diagnostics on specific model:
python3 ~/.claude/scripts/free_model_picker.py --benchmark MODEL_ID
```

---

## Step 4: Add a New Agent

```bash
python3 ~/.claude/scripts/free_model_picker.py --interactive
# or:
# /model-roster add
```

Walk through:
1. Table of models not yet in stable displays
2. Enter number to select a model
3. Benchmark runs automatically (3 prompts, ~30s)
4. Select role: 1=fast 2=bulk 3=coder 4=analyst
5. Card created at `~/.claude/agents/free/{slug}.md`
6. `subagent-options.json` updated with new entry

Verify card created:
```bash
ls ~/.claude/agents/free/
cat ~/.claude/agents/free/{new-slug}.md
```

---

## Step 5: Assign a Queue Task to Free Routing

Edit `~/.claude/hooks/state/sprint-queue.json` and find a queued task with:
- `category` in: classification, routing, bulk_summarize, format_conversion, tag_extraction
- `priority` NOT HIGH

Add these fields:
```json
"complexity": "easy",
"model_tier": "free"
```

Then on next `/faerie`, faerie_turn1.py should pick the free model route.

---

## Step 6: Verify Routing in faerie-brief.json

After running `/faerie`, check:
```bash
cat ~/.claude/hooks/state/faerie-brief.json | python3 -m json.tool | grep -A3 "free"
```

Look for entries showing `"spawn_method": "(free)"` or model from free tier.

---

## Expected Pass/Fail Criteria

| Check | Expected | Action if Fail |
|-------|----------|----------------|
| API key present | First 20 chars printed | Set OPENROUTER_API_KEY in env |
| Model list returns | 30+ models shown | Check network / API key validity |
| test-stable: 3/4 pass | 3+ OK | Benchmark failing model, check card |
| ollama-local | May fail (OK) | Expected if Ollama not running |
| New agent add | Card created in agents/free/ | Check write permissions |
| Routing in brief | (free) tag visible | Check faerie_turn1.py routing logic |

---

## Benchmark Pass Criteria

Each model runs 3 prompts:
1. **Math/Reasoning**: "What is 15% of 240?" -- PASS if response contains "36"
2. **Code**: "Python one-liner to flatten nested list" -- PASS if response has `[` or `sum`/`chain`
3. **Summarize**: 50-word text, one-sentence summary -- PASS if 20 < response length < 500

Score >= 2/3 = model suitable for stable. Score < 2/3 = degraded, investigate.

---

## Troubleshooting

**"Already running (PID N)"**: stale PID file. Remove: `rm ~/.claude/scripts/.free_model_picker.pid`

**httpx not available**: script falls back to urllib. If SSL errors: `pip install httpx`

**Rate limit 429 from OpenRouter**: free tier has rate limits. Wait 60s and retry.

**ollama-local always fails**: Normal if Ollama not running. Set `OLLAMA_BASE_URL` env var
to your Ollama instance if available.
