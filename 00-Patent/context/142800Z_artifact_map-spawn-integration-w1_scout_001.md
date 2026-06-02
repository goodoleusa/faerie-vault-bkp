# /spawn Integration Map — W1 Scout Report

## Mission Summary
Mapped 6 integration points across `/spawn` skill pipeline where ephemeral capture, FFMx measurement, and terminology enforcement hooks need injection. All critical files identified. W2 implementation ready.

---

## Integration Points (A–F)

### Point A: Bundle Creation (run.py:77-115)
**Location:** `read_context_bundle()` function

**Current State:**
- Reads global HONEY + project HONEY + NECTAR tail-50
- Assembles bundle text for agent prompt injection
- Does NOT measure input token count

**Required Hooks:**
- BEFORE bundle assembly: capture `start_context_tokens` (count tokens in HONEY + NECTAR)
- Inject `quality_gate_target` into bundle metadata (e.g., `quality_score >= 0.70` for S bearing)
- Enforce terminology: `investigation_label` (not mission/cluster_id)

**Lines to Modify:** 5–10 lines

---

### Point B: Agent Spawn Invocation (run.py:174-226 + executor.py:44-64)
**Location:** `spawn_agents()` + `emit_agent_invocation()` functions

**Current State:**
- `spawn_agents()` builds prompt with bundle + task description
- `emit_agent_invocation()` generates Python code snippet for Agent() call
- Does NOT capture baseline context before spawn

**Required Hooks:**
- BEFORE Agent() call: capture `baseline_context_tokens = len(spawn_output['prompt'].split())`
- AFTER Agent() spawns: log `spawn_event` with (investigation_label, agent_type, wave, timestamp_start)
- Validate: wave format is W1|W2|W3, agent_type in AGENT_TYPES

**Lines to Modify:** 8–12 lines

---

### Point C: Manifest Return & FFMx Scoring (executor.py:113-124)
**Location:** Main loop after agents return

**Current State:**
- executor.py prints wave summary and agent types
- Does NOT read agent's returned manifest
- Does NOT call FFMx calculator
- Does NOT validate manifest schema

**Required Hooks:**
- AFTER agent returns: read manifest from `forensics/manifests/{date}/{timestamp}*.json`
- Extract: task_id, quality_score, belief_index, compass_edge, dashboard_line
- CALL: `python3 7x_ffmx_calculator.py --manifests-dir ... --investigation-label ... --baseline ...`
- Validate manifest fields: task_id, investigation_label, quality_score, belief_index, compass_edge (N|S|E|W), prescan_decision, discovered_work

**Lines to Modify:** 15–20 lines

---

### Point D: Artifact Naming Convention (run.py:197-209)
**Location:** Agent prompt injection (task assignment section)

**Current State:**
- BODY.md documents naming pattern: `{HH-MM-SS}Z_{type}_{task_id}_{agent}_{counter}.{ext}`
- BODY.md example: `forensics/artifacts/{YYYY-MM-DD}/{TIMESTAMP}_{task}_{agent-type}_{counter}.{ext}`
- **NOT enforced** in prompt; agents write with arbitrary names

**Required Hooks:**
- In agent prompt: explicitly instruct filename pattern with WAVE ID included
- New pattern: `{HH-MM-SS}Z_{type}_{task_id}_{agent}_{wave}_{counter}.{ext}`
- Example: `142800Z_artifact_task-123_data-analyst_W1_001.md`
- Validate: counter = zero-padded 3-digit, wave in (W1|W2|W3)

**Lines to Modify:** 6–8 lines

---

### Point E: Prescan Decision Logging (run.py:117-144 + 146-172)
**Location:** `prescan_check()` + `output_manifest()` functions

**Current State:**
- `prescan_check()` returns boolean only
- `output_manifest()` hardcodes `prescan_decision: "passed"` (ignores actual decision)
- Decision reason not captured

**Required Hooks:**
- Modify `prescan_check()` return type: `(bool, decision_reason: str)`
- Update `output_manifest()` to accept and use decision_reason param
- Standardize enum: `passed` | `skipped-fresh-artifact` | `skipped-prescan-gate`
- Log prescan result: artifact_path + mtime + decision → forensics/coc.jsonl

**Lines to Modify:** 8–12 lines

---

### Point F: Wave-Aware Context Compression (executor.py:113-124)
**Location:** Post-wave summary block

**Current State:**
- executor.py prints wave name + agent list
- Does NOT measure context burn
- Does NOT aggregate FFMx across wave
- Does NOT emit dashboard_line

**Required Hooks:**
- AFTER all agents in wave return: measure `aftermath_context_tokens` (remaining context)
- Compute: `context_burn_pct = 100 * (baseline - aftermath) / baseline`
- Aggregate FFMx from all agent manifests: `FFMx = avg([manifest['ffmx_score'] for m in manifests])`
- Emit dashboard_line to STDOUT: `"W{wave} {N_agents} agents, FFMx={score:.2f}, burn={burn_pct}%"`
- Write summary to: `forensics/mutation-metrics/{date}/wave-{wave}-summary.json`

**Lines to Modify:** 10–15 lines

---

## Critical Hooks Summary

| Hook | File | Action |
|------|------|--------|
| **pre-bundle-assembly** | run.py:76 | Capture global_context_token_count BEFORE reading HONEY.md |
| **post-agent-spawn** | executor.py:98–105 | Log spawn_event; call 7x_ffmx_calculator.py with manifest |
| **post-wave-complete** | executor.py:113–124 | Measure context_burn, aggregate FFMx, emit dashboard_line |
| **prescan-decision-log** | run.py:146–172 | Update prescan_decision from hardcoded to enum (passed/skipped-*) |

---

## Scripts to Call

### 7x_ffmx_calculator.py
**When:** After each agent manifest returns  
**Args:**
```
--manifests-dir forensics/manifests/{YYYY-MM-DD}
--investigation-label {investigation_label}
--baseline {baseline_path}
```
**Output:** JSON with FFMx score + components (A, Q, E^k, T)

### 8x_time_estimate_analyzer.py
**When:** After W1/W2/W3 wave completes  
**Args:**
```
--generate-curves --days 1
```
**Output:** Time estimate baselines for next wave

---

## Terminology Standards to Enforce

| Term | Canonical Form | Anti-patterns |
|------|---|---|
| Mission identifier | `investigation_label` | `mission`, `cluster_id`, `label` |
| Output quality | `quality_score` | `quality`, `output_quality`, `score` |
| Self-awareness | `belief_index` | `honesty`, `self_awareness_score`, `confidence` |
| Bearing | `compass_edge` | `bearing`, `direction`, `edge_type` |
| Wave identifier | W1, W2, W3 | `wave_1`, `WAVE1`, `1`, `liftoff` |
| Prescan result | `passed`, `skipped-fresh-artifact`, `skipped-prescan-gate` | `skipped`, `ok`, `fail` |
| Frontier results | `discovered_work` (list of task_ids) | `discoveries`, `found_work`, `queue` |

---

## Estimated Effort

| Point | Lines | Complexity |
|-------|-------|------------|
| A | 7 | Low (add token capture + metadata field) |
| B | 10 | Medium (pre/post measurement + logging) |
| C | 18 | High (script integration + validation) |
| D | 7 | Low (prompt injection + enforcement) |
| E | 10 | Medium (return type change + enum) |
| F | 12 | Medium-High (aggregation + JSON output) |
| **Total** | **64** | **Medium** |

---

## Files to Modify

1. `/mnt/d/0LOCAL/.claude/skills/spawn/run.py` (5 hooks: A, B, D, E)
2. `/mnt/d/0LOCAL/.claude/skills/spawn/executor.py` (2 hooks: B, C, F)

---

## Manifest Schema Enforcement

**Required Fields:**
- `task_id` (string)
- `investigation_label` (string, matches pheromone trail)
- `agent_type` (string, in AGENT_TYPES list)
- `wave` (string, W1|W2|W3)
- `timestamp` (ISO 8601)
- `compass_edge` (string, N|S|E|W)
- `prescan_decision` (string, passed|skipped-fresh-artifact|skipped-prescan-gate)

**Optional Fields:**
- `quality_score` (float, [0.0, 1.0])
- `belief_index` (float, [0.0, 1.0])
- `discovered_work` (list of task_ids)
- `next_task_queued` (string, bearing for next phase)
- `dashboard_line` (string, ≤80 chars)

**Validation Rules:**
```python
assert manifest['wave'] in ('W1', 'W2', 'W3')
assert manifest['compass_edge'] in ('N', 'S', 'E', 'W')
assert manifest['prescan_decision'] in ('passed', 'skipped-fresh-artifact', 'skipped-prescan-gate')
assert 0.0 <= manifest.get('quality_score', 0.5) <= 1.0
assert 0.0 <= manifest.get('belief_index', 0.5) <= 1.0
assert len(manifest.get('dashboard_line', '')) <= 80
```

---

## Next Phase (W2 Implementation)

Ready to implement all 6 points:
- Point A: ~2 hours (token capture + metadata)
- Point B: ~3 hours (pre/post measurement + logging)
- Point C: ~4 hours (FFMx integration + validation)
- Point D: ~1 hour (prompt injection)
- Point E: ~2 hours (return type refactor)
- Point F: ~2 hours (context burn + aggregation)

**Total estimated W2 effort:** 14–16 hours
