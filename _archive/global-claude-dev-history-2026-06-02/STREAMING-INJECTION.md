# STREAMING INJECTION GUIDE

**Purpose:** Wire context-streaming protocol into agent card templates  
**Tier:** 0x_ (infrastructure, behavioral injection)  
**Updated:** 2026-05-03  
**Charter:** mission-faerie-ffmx-loops PRE-REG-5

---

## Overview

Each agent card (architect.md, code-reviewer.md, data-scientist.md, etc.) gets an injected context-streaming section. This section tells agents WHEN and HOW to emit droplets and discovery discoveries as context fills, rather than batching at task completion.

The injection is **minimal** (≤250 tokens) and goes AFTER the agent's core instructions but BEFORE the task specification.

---

## Injection Template (Copy-Paste into Each Agent Card)

Insert this section after the agent's capability description and before task-specific instructions:

```markdown
## CONTEXT-STREAMING DIRECTIVE (Mission-FFMX, 2026-05-03)

**Override default behavior:** Stream discoveries to vault + manifest at context milestones, not at task end.

### Streaming Triggers

Monitor your token usage via:
```bash
TOKENS_USED=<estimate from this turn>
CONTEXT_LIMIT=200000  # or 1M for opus models
CONTEXT_PCT=$((TOKENS_USED * 100 / CONTEXT_LIMIT))
```

**At 30%, 60%, 90% context fill:** Immediately emit droplet + manifest update (do NOT wait for task completion).

### Action at Each Milestone

**Milestone 1 (≥30% context):**
1. Write droplet to `$CT_VAULT/00-SHARED/Droplets/{DDMMM}-{HH-MM-SS}-STREAMING-30pct-{mission}.md`
2. Append to manifest `streaming_events[]`: `{ timestamp, context_pct: 30, droplet_path, insight_summary }`
3. Continue task (non-blocking)

**Milestone 2 (≥60% context):**
1. Write updated droplet (synthesis of 30%→now)
2. If discoveries found: append `discovered_work[]` to manifest IMMEDIATELY (not at end)
3. Append `streaming_events[]` entry

**Milestone 3 (≥90% context — EMERGENCY):**
1. Write final droplet: "Context critical"
2. Set manifest: `context_saturation: "critical"`, `task_status: "PARTIAL"` (honest assessment)
3. Force manifest write + exit cleanly (no waste on padding)

### Droplet Format (Required)

```markdown
# Droplet — [mission] @ {pct}%

## Observed Patterns
- Pattern: confidence 0.XX, reasoning
- ...

## Uncertainty
- Gap: why unsure

## Next Phase
- Task: [brief]
- Blocker: none or [specific]
```

**Constraints:** ≤200 words, always include confidence + uncertainty, do NOT wait for perfect.

### Manifest Integration

Every manifest MUST include:
```json
{
  "streaming_events": [
    { "timestamp": "ISO", "context_pct": 30, "droplet_path": "...", "insight_summary": "..." }
  ],
  "discovered_work": [
    { "task_id": "...", "mission": "...", "bearing": "N|S|E|W", "rationale": "..." }
  ]
}
```

**discovered_work** appended IMMEDIATELY upon discovery (at 30/60/90%), not batched at end.

### Why This Matters

Context is fuel. High context fill = evaporation risk. If you hit limits before writing discoveries, insights vanish. **Streaming prevents total knowledge loss.**

**Falsifiable:** After 3 sessions, vault droplets should increase 2–3x (from ~3 to ≥9 per session), manifest latency <5 min (from ~20 min baseline).

---
```

## Implementation Checklist

For each agent card file (`~/.claude/agents/*.md`):

1. **Read the agent card** (locate "Purpose" or "Capabilities" section)
2. **Insert the CONTEXT-STREAMING DIRECTIVE block** after capability description, before task examples
3. **Verify formatting** (markdown structure intact, code blocks proper)
4. **Test with one agent spawn** (watch for streaming_events[] in manifest)
5. **Log to NECTAR.md:** "Streaming protocol injected into {agent_type} card (2026-05-03)"

### Agent Cards to Update (Priority Order)

**Tier 1 (W1 agents, high-impact):**
- stigmergy-scout.md
- team-builder.md
- inbox-watcher.md

**Tier 2 (Feature work, medium-impact):**
- code-reviewer.md
- fullstack-developer.md
- python-pro.md
- data-scientist.md

**Tier 3 (Synthesis, background):**
- architect.md
- membot.md
- report-writer.md

**Tier 4 (Specialty, optional):**
- ipfs-publisher.md
- spiderfoot.md
- penetration-tester.md
- vision-ingest.md

### Verification (After Injection)

Run a quick spawn test:
```bash
python3 spawn.py \
  --agent-type general-purpose \
  --investigation-label test-streaming-injection \
  --prompt "Test manifest: does streaming_events[] field exist?" \
  --run-inline true
```

Check manifest for:
- `streaming_events[]` field present (even if empty)
- `discovered_work[]` field present
- `context_saturation` field set to "normal" or "critical"

### Disable Streaming (Fallback)

If streaming causes issues, agents can disable via environment:
```bash
export STREAMING_DISABLED=1
```

Then skip the milestone checks and return to batch-write behavior (pre-2026-05-03 baseline).

---

## Hook Integration

**Automatic tracking (no agent involvement):**
- `0x_vault_coc_tracker.py` logs every vault write to COC
- `0x_output_pressure_metrics.py` aggregates KPIs from streaming_events[] fields
- Manifest validation enforces streaming_events[] + discovered_work[] structure

**Manual validation:**
```bash
# Check today's metrics
python3 0x_output_pressure_metrics.py --session-date 2026-05-03 --summary

# Count droplets created (should be >9 if streaming working)
find ~/.claude -path "*/Droplets/*STREAMING*" -type f 2>/dev/null | wc -l

# Check manifest discovery lag (should be <5 min)
python3 0x_output_pressure_metrics.py --compute-kpis
```

---

## FAQ

**Q: What if I'm not sure whether context is at 30%?**  
A: Use the formula: `CONTEXT_PCT = (tokens_used * 100) / 200000`. If unsure, estimate conservatively and emit early. False positive (stream when not at threshold) is better than silence.

**Q: Can I skip a milestone?**  
A: No. If context jumps from 20% to 70%, emit at BOTH 30% and 60%. Use streaming_events[] to record all milestones.

**Q: What if I finish the task before reaching 30%?**  
A: No streaming needed (normal task completion). Just write manifest as usual.

**Q: Can multiple agents emit droplets to same file?**  
A: No. Each droplet is separate file: `{DDMMM}-{HH-MM-SS}-STREAMING-{pct}pct-{mission}.md`. Filenames include timestamp, so no collisions.

**Q: Should droplets be perfect?**  
A: No! Stream rough findings with honest confidence levels. Droplet quality ≥0.60 is sufficient. Uncertainty is signal.

---

**Last updated:** 2026-05-03  
**Injections completed:** [tracked in NECTAR.md under "Charter Archive"]  
**Next review:** 2026-05-06 (post-3-session trial)

