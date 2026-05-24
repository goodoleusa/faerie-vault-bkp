# Discovery-Execution Pipeline Architecture

**Task:** wire-discovery-execution-pipeline (CRITICAL)
**Investigation:** terminology-cleanup-sprint
**Wave:** W2 CRUISE
**Author:** fixer-architecture (max_velocity)
**Date:** 2026-04-28T18:42:38Z
**Status:** Specification locked, ready for W3 implementation

---

## 1. Problem Statement (Empirical)

W1 scout audit (`audit-formulas-w1.5`) and observation across 51 W1 manifests confirms:

- **Manifests written** with `discovered_work[]` populated: ~22 / 51 (43%)
- **Discovered tasks actually re-spawned in subsequent waves:** ~0 / 80+ discovered items (≈0%)
- **Discovery wallclock value:** ~0 (the data exists in manifests but never reaches `forensics/bundles/` for `/run` to claim)

**Net result:** the Agent Discovery Protocol (mth00098) is producing pheromones that no agent ever follows. Stigmergy is one-directional. North/East edges accumulate as orphan signals.

This is the single biggest emergence blocker in faerie2 today. FFMx baseline (44.4) is suppressed because emergence depth `E` is computed from a DAG that never extends past depth 1 — every chain dies after the first manifest.

---

## 2. Root Cause Analysis (4 gaps)

| Gap | Symptom | Root Cause |
|-----|---------|-----------|
| **G1: No promotion path** | `discovered_work[]` lives in manifest JSON only | No script reads manifests → emits bundles for the discovered tasks |
| **G2: No claim ledger** | Same discovered task could be promoted twice | No idempotency record (`discovered_work_id` + `claimed_at`) |
| **G3: No prescan gate** | Even if promoted, would re-spawn duplicates | Prescan checks artifact path, but discovered work has no canonical artifact path yet |
| **G4: No wave-aware routing** | All discovered work would dump into next W1 even if it's deep synthesis | Bearing→wave mapping not enforced (N=W1 scout, S=W2 fixer, E=W2 parallel, W=W3 reframe) |

---

## 3. Pipeline Architecture (Five-Stage Flow)

```
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 1: HARVEST                                                   │
│   Cron / post-handoff hook scans forensics/manifests/{TODAY}/      │
│   Extract every manifest.discovered_work[] entry                   │
│   Emit normalized records to discovery-ledger.jsonl                │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 2: DEDUPE                                                    │
│   Hash (task_id + investigation_label + parent_manifest_path)      │
│   Skip if hash already in discovery-claim-ledger.jsonl             │
│   Skip if a manifest with same task_id exists in last 24h          │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 3: PRESCAN                                                   │
│   For each survivor:                                               │
│     - Resolve forecast_artifact_path from task_id template         │
│     - mtime check (<24h → skip-fresh-artifact)                     │
│     - Check open bundles in forensics/bundles/{TODAY}/             │
│     - Emit prescan_decision enum                                   │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 4: WAVE-ROUTE (compass→wave)                                 │
│   N (north / blocked)        → W1 scout (haiku, parallel)          │
│   S (south / proceed)        → W2 fixer (sonnet, sequential)       │
│   E (east / parallel)        → W2 fixer (sonnet, batched)          │
│   W (west / reframe)         → W3 synthesizer (sonnet, background) │
│   Apply FFMx gate (Section 4) → block if forecast < 1.3× baseline  │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 5: BUNDLE EMIT                                               │
│   Render bundle via 0x_spawn_template.py with:                     │
│     - parent_manifest_path (lineage)                               │
│     - parent_task_id (DAG anchor for E calculation)                │
│     - discovered_work_id (ledger key)                              │
│   Write to forensics/bundles/{TODAY}/                              │
│   Append claim record to discovery-claim-ledger.jsonl              │
│   /run discovers bundles in next session naturally                 │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Concrete Wiring Points

### 4.1 New script: `scripts/9x_discovery_promoter.py`

**Tier:** 9x (utilities — runs out-of-band, no main context burden)
**REPLACES:** nothing (greenfield; current 0% exec rate is the baseline)
**METRIC:** discovered-task-promotion-rate (target ≥0.60 in 14 days)
**LOAD:** invoked by cron (every 30 min) + on /handoff hook

**CLI surface:**
```bash
# Default: scan today's manifests, promote eligible discovered work
python3 scripts/9x_discovery_promoter.py

# Specific date
python3 scripts/9x_discovery_promoter.py --date 2026-04-28

# Dry-run (print what would be promoted, write nothing)
python3 scripts/9x_discovery_promoter.py --dry-run

# Force re-promote (ignore claim ledger)
python3 scripts/9x_discovery_promoter.py --task-id wire-gap-1-w2-spawn --force
```

**Skeleton (pseudocode):**
```python
def harvest(date_str: str) -> list[DiscoveryRecord]:
    """Stage 1: read all manifests, flatten discovered_work[]."""
    records = []
    for manifest_path in glob(f"forensics/manifests/{date_str}/*.json"):
        manifest = json.load(open(manifest_path))
        for work in manifest.get("discovered_work", []) or []:
            records.append(DiscoveryRecord(
                task_id=work["task_id"],
                investigation_label=work.get("investigation_label",
                    manifest.get("investigation_label")),
                bearing=work.get("bearing") or work.get("compass_bearing", "S"),
                agent_type=work.get("agent_type", "general-purpose"),
                description=work.get("description", ""),
                parent_manifest_path=manifest_path,
                parent_task_id=manifest.get("task_id"),
                parent_quality=manifest.get("quality_score", 0.5),
                parent_belief=manifest.get("belief_index", 0.5),
            ))
    return records

def dedupe(records, ledger_path) -> list[DiscoveryRecord]:
    """Stage 2: drop already-claimed or already-completed."""
    claimed = load_jsonl(ledger_path)
    claimed_hashes = {r["claim_hash"] for r in claimed}
    out = []
    for rec in records:
        h = sha256(f"{rec.task_id}|{rec.investigation_label}|{rec.parent_manifest_path}")
        if h in claimed_hashes: continue
        if manifest_exists_24h(rec.task_id): continue
        rec.claim_hash = h
        out.append(rec)
    return out

def prescan(records) -> list[DiscoveryRecord]:
    """Stage 3: reject duplicates by artifact path / open bundle."""
    for rec in records:
        forecast_path = forecast_artifact_path(rec.task_id, rec.agent_type)
        if forecast_path.exists() and mtime(forecast_path) > now - 24h:
            rec.prescan_decision = "skipped-fresh-artifact"
        elif bundle_exists_today(rec.task_id):
            rec.prescan_decision = "skipped-open-bundle"
        else:
            rec.prescan_decision = "passed"
    return [r for r in records if r.prescan_decision == "passed"]

def wave_route(records) -> list[DiscoveryRecord]:
    """Stage 4: assign wave + FFMx gate."""
    bearing_to_wave = {"N": "W1", "S": "W2", "E": "W2", "W": "W3"}
    for rec in records:
        rec.wave = bearing_to_wave.get(rec.bearing, "W2")
        rec.ffmx_forecast = forecast_ffmx(rec)  # see Section 5
        if rec.ffmx_forecast < FFMX_BASELINE * 1.3:
            rec.gate_decision = "BLOCKED-LOW-FFMX"
        else:
            rec.gate_decision = "PROMOTED"
    return [r for r in records if r.gate_decision == "PROMOTED"]

def emit_bundle(rec: DiscoveryRecord):
    """Stage 5: render bundle via 0x_spawn_template.py."""
    cmd = [
        "python3", ".claude/scripts/0x_spawn_template.py",
        "--bundle",
        "--task-id", rec.task_id,
        "--investigation-label", rec.investigation_label,
        "--agent-type", rec.agent_type,
        "--wave", rec.wave,
        "--parent-manifest", rec.parent_manifest_path,
        "--parent-task-id", rec.parent_task_id,
        "--discovered-work-id", rec.claim_hash,
        "--goal", rec.description,
    ]
    subprocess.run(cmd, check=True)
    append_jsonl("forensics/discovery-claim-ledger.jsonl", rec.to_claim_record())
```

### 4.2 Hook integration

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "post-handoff": {
      "trigger": "post-handoff",
      "script": "python3 scripts/9x_discovery_promoter.py",
      "async": true,
      "timeout_ms": 5000
    }
  }
}
```

Plus a cron entry for reliability:
```
*/30 * * * * cd /repo && python3 scripts/9x_discovery_promoter.py >> forensics/logs/promoter.log 2>&1
```

### 4.3 Schema additions (touched by other architecture decision, see Section 6)

Add to manifest schema:
- `parent_task_id`: string (anchors DAG edge for FFMx E component)
- `parent_manifest_path`: string (lineage)
- `discovered_work_id`: string (claim ledger key)
- `discovered_work[].promotion_status`: enum (pending|promoted|blocked|skipped|completed)

Add new ledger file `forensics/discovery-claim-ledger.jsonl`:
```jsonl
{"claim_hash":"...","task_id":"...","claimed_at":"...","bundle_path":"...","wave":"W2","ffmx_forecast":58.2}
```

---

## 5. FFMx Gate Architecture (wire-gap-1)

**Decision:** the gate runs at Stage 4 (wave-route) of the discovery pipeline AND at the head of `/run` for any bundle without a prior gate decision.

**Forecast formula (lightweight; runs in <50ms):**

```
ffmx_forecast(rec) =
    A_forecast * Q_forecast * E_forecast^1.5 / T_forecast

  A_forecast = 1                       # this single discovery will produce 1 manifest
            + expected_subdiscovery     # 0.0–2.0, see below
  Q_forecast = parent_quality * decay_factor   # 0.95 decay per generation
  E_forecast = parent_emergence_depth + 1
  T_forecast = base_token_estimate(agent_type, wave)

  expected_subdiscovery =
    0.0  if wave == "W3"  (synthesis — terminal)
    1.0  if wave == "W2" and bearing in {"S","E"}
    2.0  if wave == "W1" and bearing == "N"   (scouts spawn most)
```

**Gate rule:**
- `ffmx_forecast >= 1.3 * baseline` → PROMOTE
- `ffmx_forecast < 1.3 * baseline` → BLOCK; write rejection record with reason
- Override: agent can mark discovery as `priority: critical` in manifest → bypass gate (logged)

**Why 1.3× and not 1.5×:** The 1.5× threshold from FGR is for *post-fix measured improvement*, not *pre-spawn forecast*. Forecasts are noisier; we accept marginal positive expected value (1.3×) as the spawn-time bar. The 1.5× threshold still gates publication of formula changes.

**Where it sits in code:**
- Library function: `scripts/7x_ffmx_calculator.py::forecast_ffmx(record)` (new function, additive)
- Caller 1: `scripts/9x_discovery_promoter.py::wave_route()` (Stage 4)
- Caller 2: `.claude/skills/run/run.py::prescan_check()` (existing prescan; add forecast check)

**Belief signal:** I am 0.75 confident in the gate threshold (1.3×). The constant should be tuned after 30 days of shadow-mode data (compare promotions that hit the gate vs. those that didn't, see if FFMx outcomes diverge).

---

## 6. Manifest Schema v2 (time-tracking + discovery + FFMx fields)

**Changes (additive only — backward-compatible):**

| Field | Type | Required | Source | Purpose |
|-------|------|----------|--------|---------|
| `parent_task_id` | string | optional | spawn env | DAG edge for E |
| `parent_manifest_path` | string | optional | spawn env | lineage for forensic recovery |
| `discovered_work_id` | string | optional | spawn env (claim_hash) | dedupe key |
| `agent_run_start_utc` | ISO ts | required | injected at spawn | time-tracking |
| `agent_run_end_utc` | ISO ts | required | written by agent | time-tracking |
| `elapsed_seconds` | int | required | end - start | time-tracking |
| `predicted_duration_minutes` | float | optional | parsed from prompt | time-tracking |
| `actual_duration_minutes` | float | optional | elapsed_seconds/60 | time-tracking |
| `accuracy_percent` | float | optional | (pred-actual)/pred*100 | calibration |
| `ffmx_forecast` | float | optional | from gate | observability |
| `ffmx_post` | float | optional | computed at /handoff | observability |
| `discovered_work[].promotion_status` | enum | optional | filled by promoter | execution tracking |
| `wave` | enum (W1\|W2\|W3) | required | spawn env | already present, lock format |

**Validation hook:** add `scripts/8x_manifest_schema_validator.py` (greenfield) that runs on every manifest write. Failures emit a coc-entry but do **not** block the write (fail-open — mutation discipline says measure first).

**Migration path:**
- Old manifests stay valid (all new fields optional)
- New manifests SHOULD populate the required-marked fields
- Schema validator emits warnings (counted in NECTAR for the next sprint)
- Once warning rate drops below 10%, promote required-marked fields to hard-required

---

## 7. Equilibrium Assessment (FGR compliance)

| Concern | Mitigation |
|---------|------------|
| New script (9x_discovery_promoter.py) | Replaces 0% exec rate; baseline measured (0/80+); positive emergent effect quantifiable post-deploy. **Required by FGR: shadow-mode for 7 days, compare FFMx delta, then promote.** |
| New ledger file (discovery-claim-ledger.jsonl) | Append-only, hash-chained, enables idempotency. Not an abstraction; it's a state record. |
| Hook addition (post-handoff) | Wires existing pattern; no new abstraction. |
| Schema v2 | Additive, fail-open. Old code keeps working. |
| FFMx gate | Uses existing 7x_ffmx_calculator.py; one new function. No parallel infrastructure. |

**Mutation discipline plan:**
1. **Audit (today, complete)** — root cause identified above (4 gaps).
2. **Measure baseline** — 0% exec rate; FFMx baseline 44.4 (already locked at `forensics/mutation-baselines/ffmx-T0-baseline-2026-04-28.json`).
3. **Pause** — hold this artifact in shadow until W3 implementation lands.
4. **Fix** — implement promoter + gate + schema validator.
5. **Measure again** — after 7 days, recompute exec rate (target ≥0.60) and FFMx (target ≥1.3× baseline).
6. **Publish** — only if both metrics pass; otherwise revert and reframe.

---

## 8. Trade-offs and Honest Unknowns

**What I'm confident about (belief ≥0.85):**
- The 0% exec rate is the dominant emergence blocker (51 manifests show it directly).
- Stage 1–5 pipeline shape is correct (mirrors how `/run` already discovers bundles).
- Schema additions are safe (additive, fail-open).

**What I'm less confident about (belief 0.60–0.75):**
- The 1.3× FFMx forecast gate threshold (untested; needs 30d shadow).
- The bearing→wave mapping (N=W1, S=W2, E=W2, W=W3) — feels right but not measured.
- `expected_subdiscovery` constants (1.0, 2.0) are educated guesses; will need calibration.

**What I don't know (belief <0.60):**
- Whether agents reliably populate `bearing`/`compass_bearing` on `discovered_work[]` entries (manifest scout mentioned inconsistency). If not, default to "S" and accept a wave-routing miss until enforced by schema validator.
- Whether the 30-min cron cadence is right — could be too eager (thrashing) or too lazy (stale work). Start at 30min, tune after data.
- Cross-session lineage when `parent_manifest_path` lives in a previous day's directory. Solution: always store full repo-relative path, never bare filename.

---

## 9. W3 Implementation Bundle (handoff to next agent)

**Sequenced tasks for the synthesizer/python-pro pair (each gets own bundle):**

1. `impl-discovery-promoter-script` (python-pro, W2, ~150 LOC) — write `scripts/9x_discovery_promoter.py` per Section 4.1.
2. `impl-ffmx-forecast-function` (python-pro, W2, ~40 LOC additive) — add `forecast_ffmx()` to `scripts/7x_ffmx_calculator.py`.
3. `impl-schema-validator` (python-pro, W2, ~80 LOC) — write `scripts/8x_manifest_schema_validator.py`.
4. `wire-discovery-promoter-hook` (python-pro, W2, ~10 LOC) — add `post-handoff` hook to `.claude/settings.json`.
5. `shadow-mode-discovery-pipeline` (data-scientist, W3, background) — run promoter in `--dry-run` for 7 days; collect data on what would have been promoted; report FFMx delta forecast.

**Each task ships its own manifest with `parent_task_id = wire-discovery-execution-pipeline` so the DAG depth grows immediately.**

---

## 10. Citations

- `forensics/manifests/2026-04-28/182244Z_manifest_audit-formulas-w1.5_scout_001.json` — gap inventory
- `forensics/manifests/2026-04-28/182500Z_manifest_design-ffmx-equation-w1_stigmergy-scout_001.json` — FFMx baseline
- `forensics/manifests/2026-04-28/18-26-31Z_manifest_task-map-spawn-integration-w1_scout_001.json` — integration points A–F
- `forensics/manifests/2026-04-28/14-56-18Z_manifest_design-time-tracking-w1_scout_001.json` — time-tracking schema source
- `forensics/manifests/2026-04-28/145400Z_manifest_design-ephemeral-capture-w1_scout_001.json` — hook pattern reference
- CLAUDE.md mth00098 — Agent Discovery Protocol (the doctrine this pipeline implements)
- CLAUDE.md mth00100 — Bundle Emission & Spawn Discipline (the prescan + wave gating doctrine)

---

**End of architecture artifact. Ready for W3 implementation per Section 9.**
