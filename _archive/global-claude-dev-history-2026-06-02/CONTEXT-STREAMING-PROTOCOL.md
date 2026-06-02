# CONTEXT-STREAMING PROTOCOL

**Tier:** Agent behavioral injection (≤300 tokens)  
**Applies to:** All agent card types  
**Purpose:** Stream discoveries to vault/manifest as context fills, not batch at task completion  
**Enabled:** 2026-05-03 (mission-faerie-ffmx-loops W2)

---

## Core Rule: Stream Discoveries Before Context Dies

**When context_pct > 30, 60, or 90%:** immediately emit droplet insights to vault + manifest, do NOT wait for task completion.

Why: Context is fuel. High context fill = high evaporation risk. If agent hits context limit before writing discoveries, insights are lost. Streaming prevents total knowledge loss.

---

## Three Streaming Milestones

### Milestone 1: 30% Context Fill (Early Stream)

**Trigger:** Agent estimates remaining tokens < 70% of starting budget

**Action:**
1. Pause main task (do NOT abandon it)
2. Write droplet to vault: `{vault_root}/00-SHARED/Droplets/ddmmm-HH-MM-SS-STREAMING-30pct-{investigation_label}.md`
   - Format: 2-3 bullet points, ≤200 words
   - Content: Initial observations, patterns spotted so far, uncertainty level
3. Append to manifest's `streaming_events[]`:
   ```json
   {
     "timestamp": "2026-05-03T14:30:22Z",
     "context_pct": 30,
     "droplet_path": "vault://00-SHARED/Droplets/03may-14-30-22-STREAMING-30pct-mission-x.md",
     "insight_summary": "Found 3 related entries; confidence 0.65"
   }
   ```
4. Resume task (do NOT block main work)

### Milestone 2: 60% Context Fill (Mid Stream)

**Trigger:** Agent estimates remaining tokens < 40% of starting budget

**Action:**
1. Write droplet: synthesis of findings from 30% → now, confidence update
2. Write manifest discovery: if unblocking work discovered, append immediately to `discovered_work[]` (do NOT wait for task end)
3. Append to manifest's `streaming_events[]`

### Milestone 3: 90% Context Fill (Emergency Stream)

**Trigger:** Agent estimates remaining tokens < 10% of starting budget

**Action:**
1. **STOP PRIMARY TASK** (accept incomplete work)
2. Write final droplet: "Context critical, switching to synthesis"
3. **FORCE MANIFEST WRITE:** All findings (partial or complete) + discovered_work + streaming_events all flushed immediately
4. Set manifest field: `context_saturation: "critical_90pct"`, `task_status: "PARTIAL"` or `"COMPLETE"` (honest assessment)
5. Clean exit (no token waste on apologies or summaries)

---

## Droplet Format (Vault Write)

**Location:** `$CT_VAULT/00-SHARED/Droplets/` or `$FAERIE_VAULT/droplets/` (mapped via config)

**Filename:** `{DDMMM}-{HH-MM-SS}-STREAMING-{pct}pct-{investigation_label}.md`
- Example: `03may-14-30-22-STREAMING-30pct-treasury-cert-origins.md`

**Content (strict format for automatic parsing):**
```markdown
# Droplet — [investigation_label] @ {pct}% Context

## Observed Patterns
- Pattern 1 (confidence: 0.XX, reasoning)
- Pattern 2 (confidence: 0.XX)
- ...

## Uncertainty & Gaps
- Gap 1: why unsure
- Gap 2

## Next Phase (if context continues)
- Task: [brief]
- Blocker status: none / [specific]
```

**Constraints:**
- ≤200 words per streaming milestone
- Always include confidence levels + uncertainty
- Do NOT wait for perfect; stream rough findings
- Include investigation_label in filename for discovery

---

## Manifest Streaming Field

Every manifest MUST include:
```json
{
  "task_id": "...",
  "streaming_events": [
    {
      "timestamp": "ISO8601",
      "context_pct": 30 or 60 or 90,
      "droplet_path": "vault://path/to/droplet.md",
      "insight_summary": "≤80 chars summary",
      "discovered_work_appended": true or false
    },
    ...
  ],
  "discovered_work": [
    {
      "task_id": "...",
      "mission": "...",
      "bearing": "N|S|E|W",
      "from_label": "self_task_id",
      "to_label": "discovered_task_id",
      "rationale": "≤80 chars"
    }
  ]
}
```

**discovered_work** entries are appended IMMEDIATELY upon discovery (at 30%/60%/90% milestones), NOT batched at task end.

---

## Measurement & Validation

**KPIs tracked per session:**

1. **vault_write_frequency** — How many droplets emitted vs. task completions?
   - Baseline (pre-streaming): ~0.1 droplets/task (10% of agents write droplets)
   - Target: ≥0.3 droplets/task (30% write per milestone)
   - Measurement: count `.md` files created in Droplets/ per task via forensics hook

2. **manifest_write_latency** — Time from discovery to manifest write
   - Baseline: ~20 min (end-of-task batch writes)
   - Target: <5 min (stream writes happen at milestone, not end)
   - Measurement: `streaming_events[].timestamp` vs. discovery timestamp in work

3. **droplet_count_under_load** — How many droplets survive high context fill?
   - Baseline: 2-3 droplets/session (end-of-session summary)
   - Target: 8-15 droplets/session (milestone streaming)
   - Measurement: count Droplets/*.md files created in session window

4. **discovery_lag** — From discovery to manifest write
   - Baseline: 600–1200 seconds (batched at task end)
   - Target: 30–120 seconds (stream immediately)
   - Measurement: manifest `discovered_work[].timestamp` vs. discovery moment in agent MEM blocks

---

## Integration Checklist

**For each agent card type (architect, code-reviewer, data-scientist, etc.):**

- [ ] Read this protocol at startup (inject after bundle context, before task)
- [ ] Estimate context pressure at 30%, 60%, 90%
  - Use: `python3 9x_context_pressure_calculator.py --compute-pressure` (returns JSON with `pressure_level`)
  - Or: simple heuristic: `(tokens_used / context_limit) * 100 > 30` → emit
- [ ] Write vault droplets at milestones (do NOT skip even if uncertain)
- [ ] Append manifest streaming_events[] entries (one per milestone)
- [ ] Append discovered_work[] entries immediately (not wait for task end)
- [ ] On context > 90%: abort task, force manifest write, exit cleanly

**Hook integration (PostToolUse):**
- `0x_vault_coc_tracker.py` logs every vault droplet write to forensics COC
- `0x_output_pressure_metrics.py` aggregates streaming KPIs per session
- Manual validation: `python3 0x_output_pressure_metrics.py --session {session_id} --summary`

---

## Anti-Patterns (What NOT to Do)

❌ **Wait for task completion to write manifests**  
✅ Do: Write manifests (including discovered_work) at 30%, 60%, 90% milestones

❌ **Skip droplets if uncertain**  
✅ Do: Stream rough findings with confidence levels; uncertainty is signal, not silence

❌ **Batch discoveries into one mega-write at end**  
✅ Do: Append discovered_work[] to manifest immediately when discovery happens

❌ **Abandon task at 90% to "make room"**  
✅ Do: Downgrade task_status to PARTIAL, write findings honestly, exit

❌ **Write to vault WITHOUT manifest entry**  
✅ Do: Always mirror vault droplet in manifest streaming_events[] field

---

## Falsifiable Success Criteria (3-Session Trial)

After running agents under this protocol for 3 sessions:

- **vault_droplet_count:** ≥2–3x baseline (from ~3 to ≥9 droplets/session)
- **manifest_write_latency:** <5 min after discovery (from ~20 min baseline)
- **discovered_work_streaming:** ≥80% appended within 10 min of discovery (was 100% batched at end)
- **context_saturation_incidents:** 0 lost discoveries due to context overrun (baseline: 1–2 per session)

**FALSIFICATION GATES:**
- If vault_droplet_count < 2x baseline after 3 sessions → protocol is not incentivizing streaming
- If manifest_write_latency > 10 min after discovery → agents not reading context pressure signals
- If discovered_work still mostly batch-written (>50%) → manifest discovery trigger not wired correctly

---

## Reference Implementation (Agent Pseudocode)

```python
# At agent startup (after reading bundle)
context_budget = 200000  # or from API call
tokens_used = 0

while task_not_complete:
    tokens_used += tokens_this_iteration
    context_pct = (tokens_used / context_budget) * 100
    
    # Check streaming milestones
    if context_pct > 30 and not yet_streamed_30:
        emit_droplet(vault_path, "STREAMING-30pct", findings_so_far)
        append_manifest_event("30pct_stream")
        yet_streamed_30 = True
    
    if context_pct > 60 and not yet_streamed_60:
        emit_droplet(vault_path, "STREAMING-60pct", updated_findings)
        append_discovered_work_to_manifest()  # Immediate, not wait
        append_manifest_event("60pct_stream")
        yet_streamed_60 = True
    
    if context_pct > 90:
        emit_droplet(vault_path, "STREAMING-90pct-FINAL", all_findings)
        write_manifest_immediately(status="PARTIAL")
        exit()  # Emergency exit
    
    # Continue task work...

# Normal task completion (context < 90%)
write_manifest(all_findings, discovered_work=[...], streaming_events=[...])
```

---

**Last updated:** 2026-05-03  
**Charter:** mission-faerie-ffmx-loops  
**PRE-REG:** Wire output pressure — agents stream discoveries to vault/manifest as context fills

