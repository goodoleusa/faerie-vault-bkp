# Token Optimization — Advanced Examples and Calibration

Detailed reference for status footer examples, context estimation accuracy, and calibration data.
Quick rule version: `~/.claude/rules/token-optimization.md`

---

## Status Footer — Example Progression

Complete session lifecycle showing how footer evolves across turns:

```
T1:  [🚀 T1 | warm cache | ctx ~25K | MISS ✗ | $0.05/turn | headroom: 160K]
     First turn: fresh session, no cache yet, all context loaded, full headroom

T2:  [🎯 T2 | 🔴 SPAWN NOW | ctx ~35K | HIT ✓ | $0.03/turn | headroom: 150K (37 max)]
     Cache HIT after ARCHITECTURE.md cached on turn 1; subagent spawn window still open

T2*: [🎯 T2 | ⚡ 3 running | ctx ~35K | HIT ✓ | $0.03/turn | headroom: 138K]
     After spawning 3 agents: context same, headroom reduced by agent return estimates

T5:  [⚡ T5 | 📦 outputs ready | ctx ~68K | HIT ✓ | $0.04/turn | headroom: 105K]
     Agents returned with content; context accumulated; consolidation phase

T8:  [⚠️ T8 | ⚠️ COMMIT+PUSH | ctx ~99K | HIT ✓ | $0.06/turn | headroom: 74K]
     Outputs written; commit window open; approaching 100K context threshold

T12: [🔴 T12 | 🔴 COMMIT+PUSH NOW | ctx ~132K | HIT ✓ | $0.08/turn | tight: 8 max]
     Context approaching limit; only 8 more subagents can be spawned; final commit needed
```

---

## Context Estimate Accuracy

### Sources and Calibration

- **Turn-by-turn accumulation** (this footer) = best available estimate for active context (what's currently in the context window for the LLM)
- **presend_estimate.py** (`~469K in`) = transcript **file** size ÷ 6, NOT active context — overcounts after compaction; ignore for context budget decisions
- **notification_handler.py** = fires only on events (permission deny, etc.) — NOT continuous monitoring
- **statusline.sh** = same transcript-file-size method — overcounts; shows WRAP at 70% of file size

### Calibration Factors

**Heavy sessions** (many agents, large outputs, images):
- ~11K tokens per turn
- Token accumulation faster; crystallize earlier

**Normal sessions** (balanced work):
- ~6K tokens per turn
- Standard progression

**Light sessions** (research, reading, simple tasks):
- ~4K tokens per turn
- More breathing room

**Baseline** (startup + rules):
- ~20-25K tokens at T0
- Varies by crystallization state

**Correction factor:** Stored in `~/.claude/hooks/state/context-calibration.json` (per project or global, tracks actual vs estimated deltas).

### Cost Math (Sonnet 4.6)

```
Input cost:          $3.00 / 1M tokens
Cached input cost:   $0.30 / 1M tokens (90% discount)
Output cost:         $15.00 / 1M tokens

Savings from cache:
  saved_dollars = cached_tokens × ($3.00 - $0.30) / 1M = cached_tokens × $2.70/1M
```

**Example:** 10K cached tokens = 10,000 × $2.70 / 1,000,000 = $0.027 per cache reuse.
With 3 agents reading the same ARCHITECTURE.md: $0.081 total cached read cost vs $0.09 uncached read cost.

---

## Advanced Strategies

### Prompt Caching Checklist

For maximum cache hit rate:
1. **Stable content first** — load ARCHITECTURE.md, KNOWLEDGE-BASE before any dynamic per-request input
2. **Freeze the order** — cache entries must appear in the same order across turns for hits
3. **Separate dynamic content** — pull diffs, timestamps, UUIDs into a separate (uncached) message block
4. **Reuse context bundles** — faerie bundles are cache-friendly by design (same format across runs)

### Batch API Trigger

When ≥5 files need the **same independent operation** (code review, classification, transform), batch cost savings typically exceed wait-time cost:

```
Batch opportunity:
  Requests:   5 × ~4K tokens = ~20K input
  Standard:   ~$0.06  →  Batch (50% off): ~$0.03
  Savings:    ~$0.03
  Est. time:  ~2-5 min (not real-time)
```

Rule of thumb: if results needed in <5 min, use standard API. Otherwise batch.

### Pre-flight Token Estimate Template

For requests likely >50K tokens, always estimate:

```
Estimate: ~50K tokens
  Stable:   20K (ARCHITECTURE.md, rules, type files)
  Dynamic:  20K (current code, task context, user input)
  Output:   10K (generated response, plan, etc)

At Sonnet 4.6:
  Standard: ~$0.18 input + $0.15 output = $0.33/turn
  Cached:   ~$0.06 input + $0.15 output = $0.21/turn (if cache hits)
  Batch:    ~$0.09 input + $0.15 output = $0.24/turn (if batched)
```

Flag to user if >50K and not batched or cached.
