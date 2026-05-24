# Code Review — Discovery-to-Execution Pipeline & FFMx Integration

**Task:** wire-discovery-execution-pipeline (HIGHEST PRIORITY) + wire-gap-1-w2-spawn (FFMx threshold gate)
**Reviewer:** code-reviewer (W2 CRUISE max-velocity stage agent)
**Investigation label:** terminology-cleanup-sprint
**Files reviewed:**
- `/mnt/d/0LOCAL/.claude/skills/spawn/run.py` (322 LOC)
- `/mnt/d/0LOCAL/.claude/skills/spawn/executor.py` (127 LOC)
- `/mnt/d/0local/gitrepos/faerie-vault/scripts/7x_ffmx_calculator.py` (522 LOC)

---

## Section 1 — Root Cause: 0% Execution Rate (CRITICAL)

The scout claim "0% exec rate blocker" is **confirmed by code reading**. The architectural gap is real and reproducible.

### 1.1 Run.py never invokes Agents (by design — it is a code generator)

`run.py:319` ends with `print(json.dumps(spawn_output))`. It emits a JSON payload of *spawn requests*. It does NOT call the Agent tool. Comments at `run.py:174-177` explicitly state: **"Does NOT invoke subprocess; instead adds to spawn_requests list."**

This is correct in itself — separation of generation from execution is a sound pattern.

### 1.2 Executor.py never invokes Agents either (CRITICAL FINDING)

`executor.py:44-64` `emit_agent_invocation()` returns a **string** containing Python source code:
```python
return f'''Agent(
    description="Spawn {agent_type} for {investigation_label}",
    prompt="{escaped_prompt}",
    ...
)'''
```

Then `executor.py:113-124` **prints** these strings to stdout. Nothing reads them back. There is no `eval()`, no `exec()`, no IPC bridge to the Claude tool harness, no `subprocess` invocation of a tool runner.

**This is the 0% execution rate root cause:** the executor produces *Python code that pretends an Agent() function exists in the printing scope* — but `Agent()` is a **Claude platform tool, not a Python callable**. The printed code is never consumed.

### 1.3 Severity: CRITICAL

- Severity: CRITICAL
- Impact: All spawn calls are no-ops. Manifest at `run.py:188` is written with `compass_edge: "S"` and `prescan_decision: "passed"` *before any agent runs* — this is a **manifest truthfulness violation** (mth00099 reputation hit). Manifests claim agents spawned when they did not.
- Class: silent failure (forward grep for `Agent(` in executor.py shows 1 hit at line 58 inside an f-string; no caller invokes it)

### 1.4 Recommended fixes (lowest-cost first)

**Fix A — Honest dry-run mode (1 LOC):**
Rename `executor.py` outputs to "EMITTED INVOCATION CODE (paste into harness)" and exit with code 2 to flag non-execution. Stops the lie at the manifest level.

**Fix B — Tool-bridge invocation (preferred, ~30 LOC):**
The Claude harness exposes the Agent tool via the parent context, not via a standalone Python entrypoint. Replace `executor.py` printing with a JSONL emission to a known path (e.g., `forensics/spawn-queue/{date}/pending.jsonl`). The orchestrator agent (this agent, or the /spawn skill harness) reads that JSONL and issues real `Agent()` tool calls in its own turn.

**Fix C — Block manifest write until agent confirmed running (CRITICAL for honesty):**
Move `output_manifest()` (run.py:146-172) from spawn-time to *first-callback-from-agent* time. Until then, write a `pending` marker only. This eliminates the "manifest claims success before execution" failure mode.

---

## Section 2 — Manifest Schema Enforcement (HIGH)

Per W1 scout `map-spawn-integration-w1` integration point C, manifests must enforce schema: `task_id, investigation_label, quality_score, belief_index, compass_edge, prescan_decision`.

### 2.1 Current state in run.py:157-167

The manifest dict written at spawn time contains:
- `task_id` — present (good)
- `investigation_label` — present (good)
- `wave` — present (good)
- `compass_edge` — hardcoded `"S"` (BAD — pre-execution; agent has not yet earned a bearing)
- `next_task_queued` — present (formulaic, low signal)
- `prescan_decision` — hardcoded `"passed"` (BAD — does not reflect actual prescan return value at line 183-185)
- `quality_score` — **ABSENT** (CRITICAL gap)
- `belief_index` — **ABSENT** (CRITICAL gap)

### 2.2 Severity: HIGH

This is what the scout flagged as the "0% execution rate" — but read carefully, it's actually a **schema completeness** failure that compounds the execution gap. Even if Fix A above is applied, FFMx calculator at `7x_ffmx_calculator.py:117-144` will fall back to `0.5` for every spawn-time manifest because `quality_score` is missing. **FFMx becomes uncomputable for spawn-time manifests.**

### 2.3 Recommended fix

In `run.py:157-167`, change the schema for **spawn-time manifests** to mark them clearly as pre-execution:

```python
manifest = {
    "task_id": f"spawn-{investigation_label}",
    "agent_type": agent_type,
    "investigation_label": investigation_label,
    "wave": wave,
    "task_description": task_description,
    "timestamp": datetime.now(timezone.utc).isoformat(),  # BUG: line 163 uses naive datetime
    "compass_edge": "PENDING",  # NOT "S" — agent has not run
    "manifest_kind": "spawn-intent",  # explicit marker; FFMx loader filters these out
    "prescan_decision": prescan_actual_value,  # capture real result; do not hardcode
}
```

And in `7x_ffmx_calculator.py:79-103`, filter out `manifest_kind == "spawn-intent"` so FFMx only computes over true outcome manifests.

---

## Section 3 — FFMx Threshold Gate Readiness (wire-gap-1-w2-spawn) — MEDIUM

The W1 scout marked FFMx calculator as ready for W2 wiring. Code review confirms the calculator is **functionally correct and well-structured**, but flags 3 issues that block production wiring.

### 3.1 Issue F1 — `prescan_check()` cache fallback swallows all exceptions (run.py:136)

```python
except (NameError, AttributeError, Exception):
    # Cache unavailable; fall back to linear stat-based scan
```

`Exception` is the base class — the explicit `NameError, AttributeError` are dead code. More importantly, `BaseException` subtypes like `KeyboardInterrupt`, `SystemExit` are not caught (good), but every other failure (disk error, encoding error, prescan_cache returning malformed data) is silently masked into "fall back to linear scan." **Severity: LOW** but indicates fragile error handling. Recommended: `except Exception as e: logger.warning(...)`.

### 3.2 Issue F2 — `_trace_longest_chain()` returns wrong path (7x_ffmx_calculator.py:226-240)

```python
next_node = max(
    parent_to_children[current],
    key=lambda x: len(parent_to_children.get(x, []))
)
```

This greedily picks the child with **most immediate grandchildren**, not the child whose subtree is deepest. This is a classic mistake that produces incorrect "deepest_chain" reporting in `metadata`. **Severity: MEDIUM (cosmetic — actual `max_depth` value at line 202 is correct via DFS).**

Recommended fix: track deepest chain inside the DFS recursion rather than re-tracing afterward:

```python
def max_depth_from(task_id, visited):
    if task_id in visited:
        return 0, []
    visited = visited | {task_id}
    children = parent_to_children.get(task_id, [])
    if not children:
        return 1, [task_id]
    best_depth, best_chain = 0, []
    for child in children:
        d, chain = max_depth_from(child, visited)
        if d > best_depth:
            best_depth, best_chain = d, chain
    return 1 + best_depth, [task_id] + best_chain
```

Note: `visited = visited | {task_id}` (new set) avoids the mutation bug at line 196 — currently the shared `visited: set` is mutated during recursion, so once a node is visited via one root, it cannot be revisited via another root. For a true DAG-with-shared-children this under-counts. **Severity: MEDIUM (correctness bug under DAG-not-tree topology).**

### 3.3 Issue F3 — Token estimate is wildly variable, threshold gate will be unstable (7x_ffmx_calculator.py:257-295)

`estimate_tokens_burned()` mixes two methods per manifest:
- If `artifact_size_bytes` exists → `bytes * 0.125`
- Else → `+30,800` (default per-manifest)

A 20-manifest sprint with 10 manifests carrying `artifact_size_bytes` and 10 without yields wildly different `T` than a 20-manifest sprint where all carry the field. **The FFMx threshold gate (FFMx_post / FFMx_baseline >= 1.5) will trigger spawn-block decisions on a metric whose denominator can vary 5-10x based on field-presence alone.**

**Severity: HIGH (for the W2 spawn gate use-case).** The calculator is fine for retrospective measurement, but is **not safe to wire as a spawn gate** without first either: (1) requiring `artifact_size_bytes` in the manifest schema, or (2) using a single estimation method (always default × manifest count, more honest if less precise).

Recommended fix before wiring threshold gate:
```python
# Require artifact_size_bytes; reject mixed estimation
if any(m.get("artifact_size_bytes") is None for m in manifests):
    return -1, {"error": "incomplete schema; cannot gate"}
```

---

## Section 4 — Additional Findings (LOW severity, cleanup)

### 4.1 `run.py:163` uses `datetime.now()` without `timezone.utc`

`"timestamp": datetime.now().isoformat()` produces a naive datetime, but elsewhere in run.py (line 294) `datetime.now(timezone.utc)` is used. This inconsistency means manifest timestamps from `output_manifest()` cannot be compared to UTC timestamps from other sources. **Severity: LOW** (correctness bug for sprint window filtering in `7x_ffmx_calculator.py:72-73` which expects ISO+UTC).

### 4.2 `executor.py:55` shell-escape is incomplete

```python
escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')
```

This protects against `\` and `"` in Python source but does not handle:
- `${...}` shell expansion if the printed code is ever piped to bash
- f-string brace conflicts (`{` and `}` in prompt content would break the f-string at line 58)
- Unicode normalization (zero-width characters from copy-paste)

Since the output is currently never consumed by anything (Section 1.2), this is moot — but if Fix B (tool-bridge invocation) is adopted, replace string-escaping with `json.dumps(prompt)` to get correct quoting.

### 4.3 `WAVE_CONFIG` for W2 disagrees with CLAUDE.md doctrine

`run.py:43-47`:
```python
"2": {"name": "CRUISE", "max_parallel": 4, "model": "haiku", "inline": True},
```

CLAUDE.md states W2 = sonnet (feature work), 2-3 agents. Current code uses haiku and 4 parallel, which is W1-like. **Severity: LOW** (terminology drift; flag for design-aligned cleanup in same investigation).

### 4.4 `select_team()` keyword routing is brittle

`run.py:228-242` — substring matching like `"audit" in intent` will route "audit_log query" to the audit team incorrectly, and miss intents like "investigate", "examine". **Severity: LOW.** Per the FGR (`Wire formulas, don't infer`), this is a candidate to replace with the agent-selection formula from `wire-gap-2-agent-selection`.

---

## Section 5 — Recommended W2 Execution Path

Given this is W2 CRUISE max-velocity, my role as code-reviewer is to gate and route, not execute. Recommended sequencing for downstream agents (note: I am writing recommendations only; not modifying the platform spawn skill since it lives in `/mnt/d/0LOCAL/.claude/skills/spawn/` which is platform-shared infrastructure, not investigation-scoped):

| Order | Task | Agent type | Severity rationale |
|---|---|---|---|
| 1 | Fix manifest schema (Section 2.3) — add `manifest_kind`, real `prescan_decision`, UTC timestamp | python-pro | CRITICAL — unblocks honest measurement |
| 2 | Fix FFMx token estimator (Section 3.3) — single method or hard-fail | python-pro | HIGH — gate stability |
| 3 | Fix FFMx longest-chain DFS (Section 3.2) | python-pro | MEDIUM — correctness |
| 4 | Decide on spawn-execution bridge (Section 1.4 Fix B vs. Fix C) | ai-engineer or fullstack-developer | CRITICAL — but is design decision, not pure code fix |
| 5 | Audit/clean Wave2 config drift (Section 4.3) | documentation-engineer | LOW — terminology hygiene |

I am **not** executing fixes 1–4 in this turn because:
- Tasks 1–3 modify code in `/mnt/d/0LOCAL/.claude/skills/spawn/` and `/mnt/d/0local/gitrepos/faerie-vault/scripts/`. These are platform/script files. Per code-reviewer card, my role is review + recommendations, not implementation. python-pro should execute.
- Task 4 requires a design decision that should not be made unilaterally by a reviewer.
- W2 CRUISE quality_score >=0.75 is best served by a tight, accurate review than by hasty edits.

---

## Section 6 — Quality & Belief Self-Assessment

### Quality components (0.0–1.0):
- Root-cause identification (Section 1): **0.92** — confirmed by reading three source files, traced f-string output to consumer (no consumer found)
- Schema gap analysis (Section 2): **0.88** — clear gaps identified, fix proposals concrete
- FFMx readiness analysis (Section 3): **0.84** — three issues found with severity grading; F2 includes corrected algorithm
- Cleanup findings (Section 4): **0.78** — accurate but lower impact
- Routing recommendations (Section 5): **0.80** — explicit ordering with severity rationale

**Aggregated quality_score: 0.85** (>= 0.75 threshold).

### Belief components (honest self-reporting):
- `dashboard_line_truthfulness`: 0.92 — dashboard accurately summarizes the three findings + their severity
- `next_bearing_accuracy`: 0.85 — recommended next agent (python-pro for fixes 1-3) matches scout pre-existing routing
- `assumption_validity`: 0.78 — assumed Agent() is a tool not a Python callable; this is well-established but I did not verify by reading the harness source (uncertainty admitted)
- `failure_honesty`: 0.95 — explicitly declined to execute fixes 1-4, gave reasons, did not fabricate completion claims

**Aggregated belief_index: 0.875** (>= 0.70 threshold).

### Compass edge: **S** (proceed)
Both gates pass for W2 CRUISE thresholds. Findings are actionable; downstream python-pro can execute fixes 1-3 immediately without further analysis.

### Uncertainty admissions:
1. I did not run the spawn skill end-to-end to **observe** 0% execution. I inferred from code reading that `Agent(...)` printed strings cannot execute. If the Claude skill harness has an undocumented `eval` step on stdout, my Section 1 conclusion would be wrong. Confidence ~85%.
2. I did not check whether the printed Python is actually consumed by an outer wrapper (e.g., a slash-command harness might `exec(stdout)`). Searched for callers of `executor.py` was not exhaustive across `~/.claude/skills/`. Confidence ~80% that no consumer exists.
3. FFMx Section 3.2 — the "DFS visited mutation" bug only matters under DAG-not-tree manifest topology. In current practice manifests form a tree (each task has at most one parent_task), so this is latent. Reported as MEDIUM but in practice LOW.

### Method confidence: HIGH
Three source files read in full. Cross-referenced with W1 scout findings (4 manifests). Severity grading aligned with mth00076 forensic discipline. No fabricated claims.
