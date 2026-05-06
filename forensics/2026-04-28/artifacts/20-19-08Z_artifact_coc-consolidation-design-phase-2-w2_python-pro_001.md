# COC Consolidation — Unified Architecture Design (Phase 2)

**Task:** coc-consolidation-design-phase-2-w2
**Agent:** python-pro
**Date:** 2026-04-28
**Investigation:** coc-consolidation-design-phase-2-w2

---

## 1. System Diagram — Data Flow

```
Caller (any script)
       │
       ├─ routine write ──────────────────────────────────►  0x_coc_writer.py
       │                                                        (faerie2 canonical)
       │                                                        fcntl locking + HMAC chain
       │                                                        output: forensics/coc.jsonl
       │
       ├─ sensitive write (manifest, bucket, credential) ──►  9x_coc_writer_signed.py
       │                                                        wraps 0x_coc_writer
       │                                                        adds Ed25519 signature field
       │                                                        output: same chain
       │
       └─ file hash stamp only ──────────────────────────►   4x_coc_bridge.py (stamp/verify)
                                                               KEEP as hash utility only
                                                               does NOT write chain entries

Chain (append-only JSONL)
       forensics/coc.jsonl
       forensics/vault-mutations.jsonl  (domain-specific; same pattern)
       forensics/coc-branches/{task_id}-{sig}.jsonl  (parallel branches)
              │
              ▼
       9x_coc_verifier.py  (reads ALL COC files; validates chain + signatures)
              │
              ▼
       9x_forensic_query.py  (lookup by AGENT-RUN-ID, task_id, session_id)
              │
              ▼
       9x_forensic_signer.py  (hook: sign manifest writes to hooks/state/)
              │
              ▼
       2_weekly_2a_b2_verify_coc_chain_admin.py  (B2 WORM audit)
```

---

## 2. Canonical Function Specifications

### 2a. `0x_coc_writer.py` — Unsigned Routine Writer (CANONICAL)

**Location:** `faerie2/.claude/scripts/0x_coc_writer.py`
**Status:** EXISTS; mostly correct; requires targeted enhancements (see Section 4)

**Current public API (keep as-is):**

```python
def log_tool_call(tool_name: str, action: str, path: str | None = None,
                  status: str = "success") -> None: ...

def log_manifest_write(task_id: str, manifest_path: str | Path,
                       dashboard_line: str | None = None) -> None: ...

def log_operation(operation: str, detail: str | None = None,
                  status: str = "success") -> None: ...

def log_b2_upload(local_path, remote_path, local_hash, git_commit=None,
                  b2_file_id=None, status="uploaded", dry_run=False,
                  repo_root=None) -> None: ...

def append_entry(file_path: str | Path, entry_dict: dict) -> None: ...
```

**Missing: add these two functions**

```python
def log_vault_mutation(
    file_path: str | Path,
    mutation_type: str,           # "hash-stamp" | "frontmatter-update" | "content-change"
    file_hash: str,               # "sha256:{hex}"
    doc_hash_before: str | None = None,
    doc_hash_after: str | None = None,
    coc_ref: str | None = None,
) -> None:
    """
    Replaces the direct-write in 5x_vault_mutation_tracker.py.
    Writes to forensics/vault-mutations.jsonl (domain-specific chain,
    separate from coc.jsonl to keep mutation log bounded).
    Idempotent: if entry for same (file_path, file_hash) exists within
    last 60 seconds, skip write and return.
    """

def log_annotation(
    ann_path: str | Path,
    sha256_hash: str,
    worm_dest: str | None = None,
    status: str = "submitted",
) -> None:
    """
    Replaces the direct-write in 5d_ann_coc_watcher.py.
    Writes to forensics/ann-coc.jsonl.
    Called after successful rclone upload or on dry-run.
    """
```

**Error handling contract (applies to ALL functions in this file):**

```
Write failure:
  1. Retry up to 3 times with exponential backoff: 0.1s, 0.2s, 0.4s
  2. On 3rd failure: write failure record to stderr (never raise — callers
     are hooks and must not crash Claude)
  3. If coc.jsonl is unavailable, fall back to {CLAUDE_HOME}/memory/forensics/fallback-coc.jsonl
  4. Log fallback path used in the entry itself: {"fallback": true, "intended_path": "..."}

Timeout:
  5 second hard timeout per write attempt (configurable via COC_WRITE_TIMEOUT_S env var).
  On timeout: treat as write failure, trigger retry logic.

Rate limit guard:
  If the same (event_type, path, task_id) triple appears more than 10 times within
  the last 10 seconds, suppress writes and emit a single "rate_limited" entry.
  Guard state held in memory (not persisted) — reset on process restart.

Circuit breaker:
  After 5 consecutive write failures (no recovery between), flip to OPEN state.
  While OPEN: all writes log to stderr only (no filesystem operations).
  Reset OPEN state after 60 seconds (half-open probe write).
  Current state accessible via: get_circuit_state() -> "CLOSED" | "OPEN" | "HALF_OPEN"
```

**CLI interface (add new subcommand):**
```
python3 0x_coc_writer.py log-vault-mutation --file PATH --type TYPE --hash SHA256
python3 0x_coc_writer.py log-annotation --file PATH --hash SHA256 --status STATUS
```

---

### 2b. `9x_coc_writer_signed.py` — Signed Sensitive Writer (CANONICAL)

**Location:** `faerie2/.claude/scripts/9x_coc_writer_signed.py`
**Status:** EXISTS; keep as-is
**Use for:** manifest outputs, bucket provisioning events, credential issuance

**Current key API (correct; no changes needed):**
```python
def write_signed_entry(
    agent_run_id: str,
    agent_type: str,
    project_key: str,
    repo_root: Path,
    entry: dict,
    coc_file: Path,
) -> str:  # returns entry_hash
```

**Rule:** This script MUST always call out to `0x_coc_writer` logic for the
chain management. It is a signing wrapper only; it does not maintain its own
chain hash computation logic.

---

### 2c. `4x_coc_writer.py` — SHIM (backward compat only)

**Location:** `faerie2/.claude/scripts/4x_coc_writer.py`
**Status:** EXISTS; far more capable than 0x; see note below.

**Discovery during audit:** `4x_coc_writer.py` is actually MORE capable than
`0x_coc_writer.py` — it has fcntl locking, HMAC chains, Ed25519 signing, branch
support, and merge operations. The Phase 1 canonical designation is architecturally
correct (0x tier = genesis/always-present; 4x tier = evidence-layer) but the
implementation order got inverted.

**Resolution strategy:**
- Port the superior features from 4x into 0x (lock, HMAC chain, branch support)
- Then make 4x a shim that imports 0x and delegates
- Do NOT delete 4x until migration verified across all callers

**Shim implementation (after feature port):**
```python
#!/usr/bin/env python3
"""4x_coc_writer.py — SHIM. Delegates to 0x_coc_writer. See that file."""
from pathlib import Path as _P
import sys as _s
_s.path.insert(0, str(_P(__file__).parent))
from coc_writer_0x_compat import cmd_append, cmd_verify, cmd_merge, cmd_append_branch
import sys
if __name__ == "__main__":
    # Re-export main from 0x implementation
    from importlib import import_module
    m = import_module("0x_coc_writer")
    sys.exit(m.main())
```

---

### 2d. `9x_coc_verifier.py` — Canonical Verifier + Indexer (CANONICAL)

**Location:** `faerie2/.claude/scripts/9x_coc_verifier.py`
**Status:** EXISTS; keep as-is; extend with droplet index mode

**Add one new mode to existing CLI:**
```
python3 9x_coc_verifier.py --droplet-index
```
Reads `forensics/droplet-coc.jsonl` + droplet files in vault, builds cadence
index. Replaces the indexing function of `9x_droplet_cadence.py` (keep cadence
script for its strategic read logic, remove its index-build path).

---

### 2e. `4x_coc_bridge.py` — Hash Utility (KEEP, narrowed scope)

**Current role:** stamp_file, stamp_frontmatter, verify_manifest — pure hash operations,
no COC chain writes.

**Decision:** KEEP as hash utility library. It serves a distinct purpose (SHA-256
stamping + frontmatter manipulation) from COC chain writing. Rename conceptually to
"hash bridge" but keep filename for backward compat. Document its scope:
- stamp_file: OK
- stamp_frontmatter: OK
- verify_manifest: OK
- Chain entry writing: NOT in scope (use 0x_coc_writer instead)

**Remove from the delete list.** Phase 1 classified this as redundant; after direct
inspection it is a pure hash utility with no COC chain overlap. The confusion arose
from the name. Add a prominent comment to the file header:
```python
# SCOPE: SHA-256 hash utilities only. Does NOT write COC chain entries.
# For COC chain writes: use 0x_coc_writer.py
```

---

## 3. Script-by-Script Migration Map (61 scripts)

### Group A: Writers — Action Required

| Script | Location | Action | Destination | Priority |
|--------|----------|--------|-------------|----------|
| `0x_coc_writer.py` | faerie2 | ENHANCE | Canonical (add log_vault_mutation, log_annotation, error handling) | W1 |
| `4x_coc_writer.py` | faerie2 | SHIM | After feature port to 0x; delegates to 0x | W2 |
| `4x_coc_writer.py` | global (~/.claude) | SHIM | Same shim pointing to faerie2/0x | W2 |
| `9x_coc_writer_signed.py` | faerie2 | KEEP | Canonical signed writer | — |
| `9x_coc_writer_signed.py` | global | SHIM | Delegates to faerie2/9x | W3 |
| `4x_coc_bridge.py` | faerie2 | KEEP+ANNOTATE | Hash utility only; add scope comment | W1 |
| `4x_coc_bridge.py` | global | SHIM | Delegates to faerie2/4x | W2 |
| `5x_vault_mutation_tracker.py` | faerie2 | MIGRATE | Replace line 170 direct write → `log_vault_mutation()` | W2 |
| `5x_post_vault_write_stamp.py` | faerie2 | MIGRATE | Replace line 78 direct write → `log_annotation()` style | W2 |
| `5d_ann_coc_watcher.py` | faerie2 | MIGRATE+FIX | Replace direct write → `log_annotation()`; add retry logic | W2 |
| `8x_droplet_coc_tracker.py` | faerie2 | MIGRATE | Replace line 123 direct write → `log_annotation()` or new log_droplet() | W2 |

### Group B: Indexers — Action Required

| Script | Action | Notes |
|--------|--------|-------|
| `9x_coc_verifier.py` | KEEP+EXTEND | Add --droplet-index mode; canonical verifier |
| `4x_forensic_coc_check.py` | DEPRECATE | Replace with `9x_coc_verifier.py --quick`; archive after 90 days |
| `4x_synthesize_master_coc.py` | ARCHIVE | One-time migrator; run final time, move to forensics/deprecated/ |
| `4x_subagent_coc_collector.py` | KEEP | Distinct function (collecting subagent traces); not a duplicate |
| `9x_droplet_cadence.py` | KEEP (narrow) | Remove index-build logic; keep strategic read/scan logic |

### Group C: Auditors — Action Required

| Script | Action | Notes |
|--------|--------|-------|
| `8x_protect_coc_paths.py` | DEDUPLICATE | Identical to 4x_protect_coc_paths.py body; delete 8x, keep 4x |
| `4x_protect_coc_paths.py` | KEEP | Single surviving protection hook |
| `8x_pre_write_forensics_guard.py` | KEEP | Different hook (Write tool guard, not Bash guard) |
| `9x_coc_verifier.py` | KEEP | Chain validator |
| `2_weekly_2a_b2_verify_coc_chain_admin.py` | KEEP | Weekly B2 audit; distinct |
| `9x_forensic_signer.py` | KEEP+MIGRATE | Move watched path from hooks/state/ to forensics/ paths; update patterns |

### Group D: Recovery — Action Required

| Script | Action | Notes |
|--------|--------|-------|
| `9x_forensic_query.py` | KEEP | Canonical lookup by AGENT-RUN-ID |
| `9x_forensic_signer.py` | KEEP | Signing hook; keep in recovery tier |
| `5x_backup_forensics.py` | KEEP | Local backup; distinct |
| `0x_state_to_forensics_migrator.py` | ARCHIVE | Run final time with date stamp; move to forensics/deprecated/ |
| `4x_forensic_coc_check.py` | DEPRECATE→ARCHIVE | Superseded by 9x_coc_verifier |

### Group E: Eval Harnesses — Low Priority

| Script | Action | Notes |
|--------|--------|-------|
| `3x_eval_harness.py` | ANNOTATE | eval-history.jsonl has own hash chain (acceptable; separate domain) |
| `3x_eval_membench.py` | NO CHANGE | Reads manifests; doesn't write COC chain |
| `3x_eval_mutation.py` | NO CHANGE | Reads manifests; direct writes are baselines not COC entries |

### True Duplicates (DELETE immediately after shim verification)

| Script | Duplicate Of | Delete Path |
|--------|-------------|-------------|
| `8x_protect_coc_paths.py` | `4x_protect_coc_paths.py` (identical body) | DELETE 8x after confirming hook refs updated |
| `4x_coc_bridge.py` (global) | `4x_coc_bridge.py` (faerie2) | Convert global to shim |
| `8x_build_spawn_bundle.py` | `0x_spawn_template.py` (functionally) | Archive 8x; confirm 0x covers all use cases |

---

## 4. Error Handling Protocol

### Write Failure Handling (add to 0x_coc_writer.py)

```python
import time
import threading

_circuit_state = "CLOSED"
_circuit_failure_count = 0
_circuit_reset_at: float | None = None
_CIRCUIT_THRESHOLD = 5
_CIRCUIT_RESET_S = 60
_rate_limit_window: dict = {}  # key -> list of timestamps

def _check_rate_limit(event_type: str, path: str | None, task_id: str | None) -> bool:
    """Return True if write should be suppressed (rate limited)."""
    key = f"{event_type}:{path}:{task_id}"
    now = time.monotonic()
    window = _rate_limit_window.get(key, [])
    window = [t for t in window if now - t < 10.0]
    if len(window) >= 10:
        return True
    window.append(now)
    _rate_limit_window[key] = window
    return False

def _with_retry(write_fn, max_retries=3) -> bool:
    """Execute write_fn with exponential backoff. Returns True on success."""
    global _circuit_state, _circuit_failure_count, _circuit_reset_at

    if _circuit_state == "OPEN":
        if _circuit_reset_at and time.monotonic() > _circuit_reset_at:
            _circuit_state = "HALF_OPEN"
        else:
            return False  # circuit open, skip write

    delays = [0.1, 0.2, 0.4]
    for attempt in range(max_retries):
        try:
            write_fn()
            _circuit_failure_count = 0
            if _circuit_state == "HALF_OPEN":
                _circuit_state = "CLOSED"
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delays[attempt])
            else:
                _circuit_failure_count += 1
                if _circuit_failure_count >= _CIRCUIT_THRESHOLD:
                    _circuit_state = "OPEN"
                    _circuit_reset_at = time.monotonic() + _CIRCUIT_RESET_S
                print(f"COC write failed after {max_retries} retries: {e}", file=sys.stderr)
                return False
    return False

def get_circuit_state() -> str:
    return _circuit_state
```

### Timeout Enforcement

```python
import signal

def _timeout_handler(signum, frame):
    raise TimeoutError("COC write timeout")

def _write_with_timeout(write_fn, timeout_s=5):
    old = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_s)
    try:
        return write_fn()
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
```

Note: SIGALRM is Unix-only. On Windows, use `concurrent.futures.ThreadPoolExecutor`
with `future.result(timeout=timeout_s)` instead.

### Fallback Path

```python
def _fallback_coc_path() -> Path:
    claude_home = Path(os.environ.get("CLAUDE_HOME", Path.home() / ".claude"))
    return claude_home / "memory" / "forensics" / "fallback-coc.jsonl"
```

---

## 5. Migration Guide — Per-Script Instructions

### Week 1 (W1): Enhance canonical writers, annotate, delete pure duplicates

1. **0x_coc_writer.py — add missing functions:**
   - Add `log_vault_mutation()` and `log_annotation()`
   - Add error handling wrapper (`_with_retry`, circuit breaker, rate limit)
   - Add fallback path logic
   - Add `log-vault-mutation` and `log-annotation` CLI subcommands
   - Test: run `0x_coc_writer.py self-test` (add self-test cases for new functions)

2. **4x_coc_bridge.py — annotate scope:**
   - Add `# SCOPE: SHA-256 hash utilities only...` comment to header
   - No functional changes

3. **8x_protect_coc_paths.py vs 4x_protect_coc_paths.py:**
   - `diff 8x_protect_coc_paths.py 4x_protect_coc_paths.py` — confirm identical body
   - Update any hook references from 8x to 4x
   - Delete 8x file

4. **Port 4x_coc_writer.py features into 0x_coc_writer.py:**
   - fcntl locking (copy from 4x)
   - HMAC chain computation with CHAIN_KEY (copy from 4x)
   - Branch support: `cmd_append_branch`, `cmd_merge` (copy from 4x)
   - Verify mode (copy from 4x's `cmd_verify`)
   - Fail-fast exit codes (10-15) (copy from 4x)
   - Ed25519 signing (copy from 4x, make optional with graceful degradation)

### Week 2 (W2): Migrate direct writers to canonical API

5. **5x_vault_mutation_tracker.py — line 170:**
   ```python
   # BEFORE:
   with open(FORENSIC_LOG, "a") as f:
       f.write(json.dumps(entry) + '\n')
   
   # AFTER:
   import sys; sys.path.insert(0, str(Path(__file__).parent))
   from coc_writer_import import log_vault_mutation  # or run via subprocess
   log_vault_mutation(
       file_path=str(file_path),
       mutation_type=entry.get("event_type", "content-change"),
       file_hash=entry.get("file_hash", ""),
       doc_hash_before=entry.get("prev_hash"),
       doc_hash_after=entry.get("file_hash"),
       coc_ref=entry.get("coc_ref"),
   )
   ```

6. **5x_post_vault_write_stamp.py — line 78:**
   ```python
   # BEFORE:
   with open(coc_file, "a") as f:
       f.write(json.dumps(coc_entry) + "\n")
   
   # AFTER:
   import subprocess, json as _json
   subprocess.run([
       sys.executable, str(Path(__file__).parent / "0x_coc_writer.py"),
       "--log-operation", "--operation", "vault-stamp",
       "--detail", _json.dumps({"file": str(path), "hash": hash_str}),
   ], check=False)  # non-fatal: stamp must not block vault writes
   ```

7. **5d_ann_coc_watcher.py — line 123 + add retries:**
   ```python
   # BEFORE: direct open().write()
   # AFTER: call log_annotation() + add retry loop around rclone
   
   # Add retry loop around rclone (currently missing):
   MAX_RETRIES = 3
   for attempt in range(MAX_RETRIES):
       success, msg = _rclone_copy_to_worm(rclone, src, ...)
       if success:
           break
       if attempt < MAX_RETRIES - 1:
           time.sleep(2 ** attempt)
   else:
       _err(f"Upload failed after {MAX_RETRIES} attempts: {src.name}")
       continue  # skip COC entry if upload failed
   ```

8. **8x_droplet_coc_tracker.py — line 123:**
   ```python
   # BEFORE: direct open().write() to droplet-coc.jsonl
   # AFTER: call log_annotation() with mutation_type="droplet-register"
   # OR: add log_droplet() function to 0x_coc_writer.py
   ```

9. **Make 4x_coc_writer.py (faerie2) a shim:**
   - Verify all callers work with 0x API (run smoke tests)
   - Replace 4x body with shim (import 0x, re-export)

### Week 3 (W3): Archive, deprecate, global shims

10. **0x_state_to_forensics_migrator.py:**
    - Run once more with `--dry-run` to confirm all state files migrated
    - Run `--execute`, record output
    - Move to `forensics/deprecated/0x_state_to_forensics_migrator_final_YYYYMMDD.py`

11. **4x_synthesize_master_coc.py:**
    - Run one final synthesis pass
    - Move to `forensics/deprecated/4x_synthesize_master_coc_final_YYYYMMDD.py`

12. **4x_forensic_coc_check.py:**
    - Replace all usages with `9x_coc_verifier.py --coc-file <path>`
    - Move to `forensics/deprecated/`

13. **Global (~/.claude/scripts) shims:**
    - `4x_coc_writer.py` (global): shim to faerie2/0x_coc_writer
    - `9x_coc_writer_signed.py` (global): shim to faerie2/9x

### Week 4 (W4): Smoke tests, chain verification, close

14. Run `9x_coc_verifier.py --all` — confirm chain intact across all COC files
15. Run `3x_eval_mutation.py --baseline` — capture post-migration baseline
16. Verify `manifest_truthfulness_score` unchanged or improved (measure before W1 starts)
17. Update `docs/COC-WRITE-CONTRACT.md` with new canonical API
18. Update hook configs: remove 8x_protect_coc_paths references, point to 4x

---

## 6. Testing Roadmap

### Smoke Test Suite (add to 0x_coc_writer.py self-test)

```python
# ST-01: log_vault_mutation() writes to vault-mutations.jsonl
# ST-02: log_annotation() writes to ann-coc.jsonl
# ST-03: Rate limiter suppresses >10 identical events in 10s window
# ST-04: Circuit breaker opens after 5 consecutive failures
# ST-05: Circuit breaker resets after 60s
# ST-06: Fallback path used when primary coc.jsonl unavailable
# ST-07: 4x_coc_writer.py shim delegates correctly to 0x (append + verify)
# ST-08: 8x_protect_coc_paths.py blocked after deletion (no hook references)
# ST-09: 5x_vault_mutation_tracker.py migration: trace written to chain
# ST-10: 5d_ann_coc_watcher.py retry loop fires on rclone failure
```

### Phase-In Verification Gates

| Phase | Gate | Pass Criteria |
|-------|------|---------------|
| W1 complete | 0x self-test | All ST-01 through ST-06 pass |
| W2 complete | Migration check | grep for direct-write pattern in migrated scripts returns 0 hits |
| W3 complete | Chain verify | `9x_coc_verifier.py --all` returns 0 chain breaks |
| W4 complete | Eval baseline | `3x_eval_mutation.py` manifest_truthfulness delta >= 0 vs pre-migration baseline |

---

## 7. COC Integration Spec — Every Operation Logged

Every operation category must route through canonical writer:

| Operation | Function | Chain File |
|-----------|----------|-----------|
| Tool call (Read/Write/Bash) | `log_tool_call()` | coc.jsonl |
| Manifest write | `log_manifest_write()` | coc.jsonl |
| Agent spawn/operation | `log_operation()` | coc.jsonl |
| B2 upload | `log_b2_upload()` | coc.jsonl |
| Vault file mutation | `log_vault_mutation()` [NEW] | vault-mutations.jsonl |
| Annotation submit | `log_annotation()` [NEW] | ann-coc.jsonl |
| Droplet register | `log_annotation()` [NEW] | droplet-coc.jsonl |
| Branch append | `cmd_append_branch()` | coc-branches/{task}-{sig}.jsonl |
| Branch merge | `cmd_merge()` | coc.jsonl (merge record) |
| Signed manifest | `write_signed_entry()` via 9x | coc.jsonl (signed) |

---

## 8. Backward Compatibility Matrix

| Old Call Pattern | New Pattern | Breaking? | Shim Available? |
|-----------------|-------------|-----------|-----------------|
| `4x_coc_writer.py append` | `0x_coc_writer.py append` | No (shim redirects) | Yes |
| `import 4x_coc_writer; cmd_append(...)` | `import 0x_coc_writer; cmd_append(...)` | No after shim | Yes |
| Direct `open(coc_file, "a").write(...)` | `log_*()` function call | Yes (requires code change) | No — must migrate |
| `8x_protect_coc_paths.py` hook | `4x_protect_coc_paths.py` hook | Config change needed | N/A (update settings.json) |
| `4x_coc_bridge.py stamp` | `4x_coc_bridge.py stamp` | No change | N/A (keeping) |
| `4x_forensic_coc_check.py` | `9x_coc_verifier.py --coc-file` | CLI args differ | No — update call sites |

---

## 9. Emergence Metrics

**Pre-migration baseline (measure before W1):**
```bash
python3 9x_coc_verifier.py --all 2>&1 | grep "Chain breaks"
python3 3x_eval_mutation.py --report 2>&1 | grep manifest_truthfulness
grep -c "open.*'a'" $(find . -name "*.py" | head -100) 2>/dev/null
```

**Post-migration measurement (W4):**
- Chain breaks: should decrease (all domain logs now routed through verifiable chain)
- manifest_truthfulness: should be neutral or improve (more entries = more verification surface)
- Direct-write count: should reach 0 in COC-relevant scripts

**Positive emergence expected:**
- Every COC entry traceable to originating script via `agent_id` + `task_id` fields
- New `log_vault_mutation()` enables vault mutation rate analytics (currently invisible)
- Circuit breaker gives first-ever visibility into COC write failure rate

**Neutral emergence (watch, don't fix):**
- vault-mutations.jsonl will grow faster with explicit logging — expected
- droplet-coc.jsonl volume increase — expected

**Uncertain (measure before claiming):**
- Will consolidated writer reduce manifest_truthfulness gaps? Need pre/post comparison.
  Do not claim improvement until W4 measurement confirms.
