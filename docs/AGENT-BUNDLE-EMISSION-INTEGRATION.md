# Agent-Side Bundle Emission — Integration Specification

**TIER:** 0x (governance)  
**COMPLETES:** mth00100 (Bundle Emission & Spawn Discipline)  
**RESPECTS:** f(0) equilibrium (agents render bundles instead of main)  
**FORENSICS:** All bundles written to `forensics/bundles/{YYYY-MM-DD}/`, COC-signed, immutable  
**METRIC:** emergence_index (bundles emitted per session × cross-citations in downstream manifests)

---

## Summary

Agent-side bundle emission reuses existing `0x_spawn_template.py` infrastructure. No new abstractions. Agents with >30% remaining context after primary task can render bundles for future agents on the same `investigation_label`.

**Key principle:** Agents do synthesis work (rendering bundles); main never touches it. Cost to main = 0. Cost to agent = 5-10% of remaining context. Payoff = future agents start 1-2 phases ahead.

---

## Inventory: Existing Infrastructure

### Core Scripts Available

| Script | Purpose | Status | Agent-Usable |
|--------|---------|--------|-------------|
| `0x_spawn_template.py` | Bundle rendering (Mustache templates + presets) | READY | YES |
| `0x_mission_graph.py` | Mission charting + compass query | READY (basic) | YES |
| `0x_prescan_cache.py` | Staleness checking (LRU, 5min TTL) | READY | YES |
| `0x_coc_writer.py` | Chain-of-custody logging | EXISTS (inferred) | YES |
| `0x_path_utils.py` | Forensic path resolution | EXISTS (inferred) | YES |

### Forensic Structure (Operational)

All artifacts typed by folder:

```
forensics/
  bundles/
    2026-04-28/
      {HH-MM-SS}Z_bundle_{investigation_label}_{agent_id}_{counter}.json
  manifests/
    2026-04-28/
      {HH-MM-SS}Z_manifest_{task_id}_{agent_id}_{counter}.json
  artifacts/
    2026-04-28/
      {HH-MM-SS}Z_artifact_{type}_{task_id}_{agent_id}_{counter}.{ext}
  coc-entries/
    2026-04-28/
      {HH-MM-SS}Z_coc-entry_{task_id}_{agent_id}_{counter}.jsonl
```

### Bundle Naming Convention (ACTIVE)

Existing bundles in `forensics/bundles/2026-04-28/`:

- `183001Z_bundle_manifest-schema-wiring-critical_python-pro_001.json`
- `183002Z_bundle_wormbucket-ci-discovery_general-purpose_001.json`

Pattern: `{timestamp}Z_bundle_{investigation_label}_{agent_id}_{counter}.json`

**No changes needed.** Agents emit with same pattern.

---

## Design: Agent-Side Bundle Emission Workflow

### 1. Primary Task Completion → Manifest Return (Non-negotiable)

```python
# Agent pseudocode (execution sequence)

# PHASE 1: Execute primary task
findings = investigate_task()

# PHASE 2: Write manifest FIRST (priority #1, cannot fail)
manifest = {
    "task_id": task_id,
    "dashboard_line": "X findings; quality=0.82; belief=0.88",
    "investigation_label": investigation_label,
    "compass_edge": "S",  # or N/E/W based on quality + belief
    "discovered_work": [],  # empty, filled in discovery phase if found
    "next_task_queued": None,  # will be set if discovery succeeds
    # ... (all standard fields)
}
write_manifest(manifest)  # Must succeed before proceeding

# PHASE 3: Check context remaining
context_remaining = estimate_context_used()  # e.g., 40%
if context_remaining < 0.30:
    return  # Not enough for bundle emission

# PHASE 4: Optional discovery (if context + prescan allows)
if context_remaining > 0.40:
    work = scan_frontier_for_unblocking_tasks()
    if work and prescan_passes(work):
        manifest["discovered_work"] = work  # Append to existing manifest
        manifest["next_task_queued"] = work[0]["task_id"]
        update_manifest(manifest)  # In-place update
        context_remaining -= 0.20  # Spent 20% on discovery

# PHASE 5: Bundle emission (if context >20% remains + agent has insights)
if context_remaining > 0.20:
    bundle_to_emit = decide_bundle_for_next_phase()
    if bundle_to_emit:
        emit_bundle(investigation_label, bundle_to_emit)
        manifest["emitted_bundle"] = {
            "timestamp": utcnow(),
            "preset": bundle_to_emit.preset,
            "path": bundle_path
        }
        update_manifest(manifest)  # Second in-place update
```

### 2. Discovery Protocol (Within Remaining Context)

After manifest is written, agent scans frontier for unblocking work:

```bash
# Agent's discovery query (after manifest return)
grep -r "investigation_label.*${INVESTIGATION_LABEL}" \
  forensics/manifests/{YYYY-MM-DD}/ | \
  grep "compass_edge.*N" | \
  head -10

# Filter by: (1) same investigation_label, (2) North bearing (unblocked prerequisites), 
#            (3) matching agent capability
# Prescan: Is work <24h old? Use 0x_prescan_cache.py

if prescan_passes:
    discovered = [task1, task2, task3]
    # Append to manifest discovered_work
    # Update next_task_queued to task1
```

**Prescan protocol (agent-side):**

```bash
python3 0x_prescan_cache.py check \
  --artifact-path "forensics/artifacts/2026-04-28/..." \
  --investigation-label "${INVESTIGATION}" \
  --agent-type "code-reviewer" \
  --max-age-seconds 86400

# Returns: (is_stale: bool, reason: str)
# Example: (False, "fresh") or (True, "stale")

if [ "$is_stale" = "False" ]; then
    # Work is recent: safe to discover + queue
else
    # Work is stale: don't spawn (would block on old task)
fi
```

### 3. Bundle Emission (Remaining Context >20%)

Agent calls existing `0x_spawn_template.py` in **emit mode**:

```bash
# Agent calls (within their agent session)
python3 0x_spawn_template.py emit-bundle \
  --investigation-label "treasury-cert-ip-origins" \
  --preset "standard" \
  --goal "Deep validation of treasury-cert-to-IP mappings" \
  --context-hints "[
    {\"from_manifest\": \"task-123\", \"insight\": \"Certs drift from configs\"},
    {\"from_droplet\": \"legacy-cert-persistence\", \"relevance\": \"HIGH\"}
  ]" \
  --creator-agent-id "scout-001" \
  --output-path "forensics/bundles"
```

**Returns:** Bundle written to `forensics/bundles/2026-04-28/{ts}_bundle_...json` (agent writes JSON directly, no main involvement).

### 4. Manifest Annotation (Bundle Emission Recorded)

After bundle emitted, agent updates manifest in-place:

```json
{
  "task_id": "treasury-cert-analysis-task-123",
  "dashboard_line": "82 certs analyzed; 5 contradictions found; validation chain complete",
  "investigation_label": "treasury-cert-ip-origins",
  "compass_edge": "S",
  "discovered_work": [
    {"task_id": "treasury-cert-risk-calc", "reason": "Ready for next phase (north-edge resolved)"}
  ],
  "next_task_queued": "treasury-cert-risk-calc",
  "emitted_bundle": {
    "timestamp": "2026-04-28T14:30:50Z",
    "preset": "standard",
    "path": "forensics/bundles/2026-04-28/143050Z_bundle_treasury-cert-ip-origins_scout-001_001.json",
    "goal": "Deep validation of treasury-cert-to-IP mappings for risk scoring phase",
    "context_consumed_percent": 8
  }
}
```

---

## Changes Needed: 0x_spawn_template.py New Subcommand

### Current State
- `render` — Render template to prompt (for main)
- `list`, `show`, `validate` — Template introspection

### New Subcommand: `emit-bundle`

```python
# Pseudocode addition to 0x_spawn_template.py

def emit_bundle(
    investigation_label: str,
    preset: str,  # "light" | "standard" | "rich"
    goal: str,
    creator_agent_id: str,
    context_hints: List[Dict] = None,
    output_path: Path = None,
) -> Path:
    """
    Render + write a bundle for future agents.
    
    Args:
        investigation_label: Mission cluster label (e.g., "treasury-cert-ip-origins")
        preset: Bundle size/scope: "light" (~2K), "standard" (~4K), "rich" (~7K)
        goal: One-sentence goal for next phase
        creator_agent_id: Agent emitting bundle (for forensic chain)
        context_hints: Optional cross-citations to manifests/droplets
        output_path: forensics/bundles/{YYYY-MM-DD}/ (auto-resolved if None)
    
    Returns:
        Path to written bundle
    
    Writes:
        forensics/bundles/2026-04-28/{HH-MM-SS}Z_bundle_{investigation_label}_{creator_agent_id}_{counter}.json
    
    COC:
        Logs bundle creation via 0x_coc_writer.py (immutable)
    """
    
    # 1. Assemble bundle content (reuse existing 0x_spawn_template render logic)
    bundle_json = {
        "task_id": f"emit-{investigation_label}-{timestamp_hash()}",
        "investigation_label": investigation_label,
        "preset": preset,
        "goal": goal,
        "created_by_agent": creator_agent_id,
        "created_utc": utcnow(),
        "context_hints": context_hints or [],
        
        # Reuse existing template rendering (CRITICAL: don't duplicate logic)
        "prompt_body": render_template(
            template_id=f"bundle-{preset}",
            params={"goal": goal, "investigation_label": investigation_label}
        ),
        
        "success_criteria": [...],
        "compass_edge": "TBD",  # Downstream agent sets bearing
    }
    
    # 2. Determine output path
    date_dir = output_path / datetime.utcnow().strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%H-%M-%SZ")
    counter = increment_collision_counter(date_dir, investigation_label, creator_agent_id)
    
    bundle_filename = f"{timestamp}_bundle_{investigation_label}_{creator_agent_id}_{counter:03d}.json"
    bundle_path = date_dir / bundle_filename
    
    # 3. Write bundle
    bundle_path.write_text(json.dumps(bundle_json, indent=2))
    
    # 4. Log to COC (immutable chain)
    coc_entry = {
        "timestamp": utcnow(),
        "operation": "bundle_emission",
        "creator_agent_id": creator_agent_id,
        "bundle_path": str(bundle_path),
        "investigation_label": investigation_label,
        "file_hash": sha256_file(bundle_path),
    }
    call_0x_coc_writer_append(coc_entry)
    
    return bundle_path
```

**CLI hook:**

```bash
# In main() of 0x_spawn_template.py:

if args.command == "emit-bundle":
    bundle_path = emit_bundle(
        investigation_label=args.investigation_label,
        preset=args.preset,
        goal=args.goal,
        creator_agent_id=args.creator_agent_id,
        context_hints=json.loads(args.context_hints) if args.context_hints else None,
        output_path=Path(args.output_path or "forensics/bundles"),
    )
    print(json.dumps({
        "bundle_written": str(bundle_path),
        "timestamp": datetime.utcnow().isoformat(),
        "investigation_label": args.investigation_label,
    }))
```

---

## Changes Needed: Manifest Schema Extension

### Current Manifest Fields (OPERATIONAL)

```json
{
  "task_id": "string",
  "dashboard_line": "≤80 chars",
  "investigation_label": "string",
  "compass_edge": "N|S|E|W",
  "quality_score": 0.0–1.0,
  "belief_index": 0.0–1.0,
  "discovered_work": [],
  "next_task_queued": "string or null",
  "artifacts": [...]
}
```

### NEW Field: `emitted_bundle` (Optional)

```json
{
  "emitted_bundle": {
    "timestamp": "2026-04-28T14:30:50Z",
    "preset": "light|standard|rich",
    "path": "forensics/bundles/2026-04-28/...",
    "goal": "One-sentence purpose",
    "context_consumed_percent": 8
  }
}
```

**Semantics:**
- Present if agent emitted bundle after completing task
- Absent if no bundle emitted (agent lacked context or saw no value in emitting)
- Used by main to track: "How many bundles → how much emergence gained?"

---

## Changes Needed: Droplet Emission (Companion Protocol)

**SEPARATE from bundle emission.** Agents write droplets to vault instead of forensics:

```bash
# Agent writes droplet WITHIN execution (not at end)
# When: AHA moment discovered during investigation

cat > ~/ct_vault/00-SHARED/Droplets/2026-04-28-{slug}.md << 'EOF'
---
investigation_label: treasury-cert-ip-origins
parent_task: task-123
aha_type: cross_validation | pattern | contradiction | methodology
priority: HIGH | MED | LOW
source_agent: scout-001
source_session: 2026-04-28
created_utc: 2026-04-28T14:30:50Z
---

# Key Insight: [Title]

[One sentence insight + why it matters]

## Evidence
- Finding 1
- Finding 2

## Related Work
- Manifest: task-123 (parent)
- Droplet: 2026-04-27-legacy-cert-persistence.md (cited)

EOF

# Then reference in manifest:
{
  "emitted_droplet": {
    "timestamp": "2026-04-28T14:30:50Z",
    "path": "~/ct_vault/00-SHARED/Droplets/2026-04-28-legacy-cert-drift.md",
    "aha_type": "cross_validation",
    "investigation_label": "treasury-cert-ip-origins"
  }
}
```

**Integration:** Droplet emission is INDEPENDENT of bundle emission. Agent can do both (within remaining context). Vault handles droplet discovery; forensics handles bundle discovery.

---

## Discovery: How Future Agents Find Emitted Bundles

### Main (Orchestrator) Discovers Bundles

```bash
# After W1 wave completes, main queries compass for next phase

# 1. List all bundles created today
ls forensics/bundles/2026-04-28/ | grep -E "^[0-9].*_bundle_"

# 2. Group by investigation_label
grep -h "investigation_label" forensics/bundles/2026-04-28/*.json | sort | uniq -c

# 3. For next LIFTOFF, read bundles matching investigation_label
python3 0x_mission_graph.py query --bundles-for-label "treasury-cert-ip-origins"

# 4. Render new spawn context with emitted bundles injected
python3 0x_spawn_template.py render-wave-2 \
  --investigation-label "treasury-cert-ip-origins" \
  --include-emitted-bundles forensics/bundles/2026-04-28/*.json
```

### Downstream Agents Discover Bundles

Bundle discovery is IMPLICIT (no explicit agent command):

1. Agent reads context bundle (main-rendered, includes recent manifests)
2. Agent sees `investigation_label="treasury-cert-ip-origins"` in manifest
3. Agent queries: "Any unfinished work or bundles from peers?"
4. Agent scans: `ls forensics/bundles/2026-04-28/*treasury-cert*`
5. Agent reads emitted bundles (optional; enhances context if available)

**No explicit discovery call needed.** Bundles are part of the compass graph topology.

---

## Prescan Gate (Prevent Stale Bundle Emission)

### Agent Checks Before Emitting Bundle

```bash
# Before agent emits bundle, check: "Are there recent tasks in this mission?"
python3 0x_prescan_cache.py check-mission \
  --investigation-label "treasury-cert-ip-origins" \
  --max-age-hours 24

# Returns: { "is_mission_active": bool, "last_activity": ISO8601, "reason": str }

if is_mission_active:
    # Emit bundle: downstream work exists and is recent
    emit_bundle(...)
else:
    # Skip bundle: mission dormant or completed 24h ago
    # Log decision to manifest prescan_decision
fi
```

**Rationale:** Don't emit bundles for dead missions. Prevents forensics bloat and context waste.

---

## Equilibrium Check: Bundle Emission Cost vs. Payoff

### Agent Cost Model

| Phase | Context | Outcome |
|-------|---------|---------|
| Primary task | 60% | manifest + findings |
| Discovery (optional) | 20% | discovered_work appended |
| Bundle emission | 8% | bundle written to forensics |
| **Total** | **88%** | manifest + discoveries + bundle |
| Remaining | **12%** | (preserved for droplets or idle) |

**Cost to main:** 0 (agent does synthesis; main never reads bundle unless scheduling next wave).

**Cost to agent:** 8% context (5% discovery + 3% bundle render).

**Payoff (future agent):** 25% context saved (downstream agent starts 1-2 phases ahead).

**Net ROI:** 25% / 8% = 3.1x return on investment.

### Equilibrium Rule: When NOT to Emit

1. **Mission is blocked (North edge):** Don't emit bundles for incomplete missions. Emit only when compass_edge=S.
2. **Agent has <20% context remaining:** Don't emit. Preserve context for droplets + hydration.
3. **No downstream work queued:** Don't emit. Bundle would sit unused.
4. **Investigation is 24h+ dormant:** Don't emit. Mission likely abandoned.

---

## Mutation Discipline: Measuring Success

### Baseline Metrics (T+0, 2026-04-28)

```json
{
  "bundles_emitted_per_session": 0,
  "discovery_incidents_per_session": 0,
  "downstream_citations_per_bundle": 0,
  "ff_mx_improvement_percent": 0
}
```

### After Integration (T+7)

Track:
- **Bundles emitted per W1 wave:** (target: ≥3 bundles/10 agents)
- **Downstream agent adoption rate:** % of future agents citing emitted bundles
- **Emergence index:** Cross-citations in downstream manifests referencing upstream bundles
- **FF-Mx trend:** Artifacts × quality × emergence / tokens (should increase >1.2x baseline)

### Kill Switch

If any metric regresses:
- Bundles not being used (0 downstream citations after 7 days) → disable emission
- Emergence index flat or negative → reframe bundle strategy (too rich? too vague?)
- FF-Mx drops → investigate whether bundle overhead is uncompensated

---

## Specification Summary: Files to Modify

| File | Change | Impact |
|------|--------|--------|
| `0x_spawn_template.py` | Add `emit-bundle` subcommand + logic | Agents can render bundles |
| Manifest schema (docs/) | Add optional `emitted_bundle` field | Track bundle emission in forensics |
| Droplet writer (agent-side) | Already supported; ensure vault path is documented | Agents emit insights independently |
| `0x_prescan_cache.py` | Add `check-mission` mode (optional) | Agents avoid emitting for dead missions |
| `0x_mission_graph.py` | Add `--bundles-for-label` query mode | Main discovers emitted bundles |

**No new scripts.** Reuse existing infrastructure.

---

## Next Steps (Execution Phases)

### Phase 1: Implementation (WA2)
1. Add `emit-bundle` method to `0x_spawn_template.py`
2. Update manifest schema docs to include `emitted_bundle` field
3. Wire `0x_coc_writer.py` call into emit-bundle (immutable logging)
4. Test: Manual bundle emission from agent context

### Phase 2: Integration (W2)
1. Inject `emit-bundle` example into agent spawn prompts (behavioral guidance)
2. Add prescan gate: agents check before emitting
3. Test: Agents emit bundles during discovery phase

### Phase 3: Discovery (W3)
1. Add `--bundles-for-label` to mission graph query
2. Main reads emitted bundles at wave boundary
3. Test: Downstream agents discover + cite bundles

### Phase 4: Measurement (Async)
1. Track bundle emission metrics → forensics/session-metrics/
2. Compare FF-Mx before/after
3. Publish mutation audit (beneficial, neutral, harmful, or retract)

---

## See Also

- `SPAWNING-DISCIPLINE.md` — Agent autonomy + stigmergy principles
- `docs/SPAWN-CONTRACT.md` — Template enforcement (main-side)
- `mth00100` — Bundle emission theoretical foundations
- `0x_spawn_template.py` — Implementation reference
- `forensics/2026-04-28/bundles/` — Operational bundle examples
