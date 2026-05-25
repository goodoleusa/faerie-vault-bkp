---
type: contract
status: draft-v1
created: 2026-04-23
tags: [coc, forensics, permissions, architecture, compliance, court-readiness]
parent: "[[ARCHITECTURE]]"
up: "[[ARCHITECTURE]]"
sibling:
  - "[[Hive/03-Agent-Artifacts-Court-Readiness]]"
  - "[[FOUNDER-GUIDE]]"
supersedes:
  - "ad-hoc agent direct-write pattern (deprecated 2026-04-23)"
cites:
  - "Hive/03-Agent-Artifacts-Court-Readiness.md (artifact catalog + tier ranking)"
  - "forensics/audits/coc-gap-audit-20260423 (inline findings; 9-entry fungibility zone)"
  - "CLAUDE.md rule 4 (every agent signs output — previously unenforced)"
  - "rules/core/core.md (forensic integrity section)"
  - "rules-optional/subagent-write-protocol.md (WSL sandbox boundary)"
doc_hash: sha256:pending
hash_method: body-sha256-v1
---

> [↑ Docs](./README.md) · [→ Court Readiness](../../0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Hive/03-Agent-Artifacts-Court-Readiness.md) · [⌂ Architecture](./ARCHITECTURE.md)

# COC Write Contract — Permissions + Compliance, One Fix

**Problem statement (2026-04-23 audits):** Agents write COC entries directly. This forces us to trust every agent to implement hash-chaining correctly. The 2026-04-23 COC gap audit proved trust-based chaining fails: the 2026-04-16 orphan-migration-agent produced 9 entries with identical hashes, creating a fungibility zone where any entry could be swapped undetected.

**Permission reality (from perms-audit 2026-04-23):** The Claude Code harness already blocks `Write`/`Edit` on the entire `.claude/` subtree for subagents. Bash is not sandboxed. The proposed PreToolUse hook `protect-coc-paths.py` is registered in a settings file the harness does not load — dead code. **Path-pattern blocks cannot be enforced via hooks for subagents; only via the harness.** This reshapes the architectural fix.

**Architectural fix (revised for monkeybranching):** A single writer is the only producer of chain entries, invoked via Bash. **Agents write to per-branch sub-chains in parallel, not the canonical trunk.** A merger reconciles branches into the trunk only after validation confirms reproducibility. The queue never blocks progress; parallel branches cost time only on validation failure.

---

## 1. The Three-Layer Contract

```
┌─ LAYER 3: AGENT CONTRACT (enforcement = rules-optional/coc-write-contract.md)
│  Agents MUST NOT Write/Edit on:
│    - forensics/coc.jsonl, claim-coc.jsonl, *-coc.jsonl (any path)
│    - ~/.claude/memory/forensics/*.jsonl
│    - hash_manifest*.json, genesis_manifest.json
│  Agents MUST call:
│    python3 {repo}/scripts/4x_coc_writer.py append --file <path> --entry <json>
│  Agent permission footprint: Bash only. No Write on forensic paths.
│
├─ LAYER 2: COC WRITER (single entry point = scripts/4x_coc_writer.py)
│  Contract:
│    1. Read last entry of target file → extract entry_hash → set as prev_entry_hash
│    2. Canonical-serialize new entry body (sorted keys, UTF-8, no trailing whitespace)
│    3. Compute entry_hash = HMAC-SHA256(prev_entry_hash || body, chain_key)
│    4. Sign body with agent's Ed25519 key: ~/.claude/agents/{agent_type}.key
│       (if key missing, writer FAILS with error — no silent skip)
│    5. Append atomically: fcntl.LOCK_EX on file, single-line write, LOCK_UN
│    6. Update directory-level hash via hash_tracker snapshot
│    7. Return exit code: 0 = success, non-zero = error (no silent failure)
│  Required fields (writer rejects entries missing any):
│    ts, agent_id, task_id, entry_hash, prev_entry_hash, signature, body
│
└─ LAYER 1: HARNESS ENFORCEMENT (already in place, not a hook)
   Claude Code harness blocks Write/Edit on entire .claude/ subtree for subagents.
   Verified by perms-audit 2026-04-23. No hook needed — harness does this by default.
   Bash is NOT sandboxed. Agents must use Bash to call the writer script.
   (Prior plan was a PreToolUse hook at hooks/8x_coc_write_guard.py — dead-code path,
    harness doesn't load hooks/settings.json. Abandoned in favor of harness default.)
```

This contract satisfies every finding from the 2026-04-23 audits in one architectural move.

---

## 1b. Branch-Chain Model (Monkeybranching Safety)

**Principle:** the queue never blocks progress. Multiple agents can pursue parallel hypotheses on the same logical task without serializing through a lock. Validation + reproducibility are the gate, not the queue.

**Chain topology:**

```
forensics/
├── coc.jsonl                              ← canonical trunk (merger writes only)
├── coc-branches/
│   ├── {task_id}-{branch_sig8}.jsonl      ← per-branch chain (parallel-safe)
│   ├── {task_id}-{branch_sig8}.validation.json  ← reproducibility proof
│   └── failed/                             ← branches that failed validation (immutable, retained)
│       └── {task_id}-{branch_sig8}.jsonl
└── coc-merges/
    └── {merge_ts}_{branches}_merger.jsonl ← merger's COC entry declaring merge
```

**How monkeybranching works end-to-end:**

1. Agent claims a task (via faerie queue) but does NOT lock the canonical trunk.
2. Agent appends entries to its own branch: `coc-branches/{task_id}-{branch_sig}.jsonl`.
   - `branch_sig` = first 8 chars of SHA256(agent_run_id + start_ts). Globally unique.
   - Each branch is its own hash-chain. `prev_entry_hash` references prior entry IN THE BRANCH, not the trunk.
   - Genesis anchor for a branch references the trunk entry_hash at branch creation time.
3. Other agents may claim the same logical task and start parallel branches. They do not interfere.
4. Agent completes work and emits a validation sidecar: `{task_id}-{branch_sig}.validation.json` containing:
   - Reproducibility proof (inputs, commands, outputs, hashes)
   - Pass/fail for each check
   - Reproducibility-score ∈ [0, 1]
5. Merger (triggered when branches complete or at session end) reads all branches for a task:
   - If exactly one validates: merge to trunk via `4x_coc_writer.py merge --branch {sig}`.
   - If multiple validate: they should converge; merger records both branches' trunk entries with a CONVERGENT merge type.
   - If none validate: all branches move to `coc-branches/failed/`. Merger appends a FAILED-MERGE entry to trunk pointing at the failed branches (immutable retention).
6. Merger writes a `coc-merges/{merge_ts}_{branches}_merger.jsonl` entry explaining which branches merged, which failed, and why.

**Key property:** every branch, every validation, every merge, every failure is hash-chained and forensically traceable. Failed branches are NOT deleted — they are evidence of what was tried and why it didn't work. Court can reconstruct every attempted hypothesis.

**Why this respects monkeybranching:** no branch blocks any other branch. Validation is async per-branch. Merger runs when branches complete, not on a schedule. The queue is a discovery surface ("what tasks exist, who's working on what") not a lock ("one agent at a time"). Speed × quality both win: more parallel attempts, higher likelihood one succeeds; all attempts preserved for audit.

---

## 2. How This Closes Each Audit Finding

### From `coc-gap-audit-20260423` (security-auditor):

| Finding | How the contract closes it |
|---|---|
| `coc.jsonl` L41-49 fungibility zone (identical hashes) | Writer computes fresh `entry_hash` per entry using `prev_entry_hash || body` — identical bodies across entries still get different hashes because `prev_entry_hash` differs. Batch writes cannot collide. |
| `coc.jsonl` L50 unchained | Writer refuses entries missing `entry_hash`/`prev_entry_hash` fields. Bypass is impossible. |
| `deletion-coc.jsonl` L41 undeclared genesis re-anchor | Writer introduces explicit `chain_segment_boundary` record type — migrations MUST declare re-anchor via a typed entry, not silent continuation. |
| `claim-coc.jsonl` no hash chain (57 entries) | Writer enforces chain on every `.jsonl` file it touches. `claim-coc.jsonl` gets retrofitted with genesis anchor + all future appends chained. |
| `task_id` coverage 0/50 in `coc.jsonl` | Writer rejects entries missing `task_id`. Going forward: 100% coverage. Backfill sidecar for historical entries. |
| Ed25519 signatures: 0 enforced | Writer FAILS on missing key (no silent skip). CLAUDE.md rule 4 becomes load-bearing for the first time. |

### From `03-Agent-Artifacts-Court-Readiness` (court-readiness catalog):

| Finding | How the contract closes it |
|---|---|
| Bash stdout ephemerality (biggest hole) | Writer accepts `stdout_hash` field for EXEC entries. A companion `4x_bash_stdout_capture.py` hook (PostToolUse on Bash) hashes stdout to a sidecar file + writes COC entry referencing the sidecar's hash. Output is captured, hash-chained, and reproducible. |
| `5x_forensics_b2_sync.py` unwired | Writer emits sync triggers on chain_segment_boundary entries. SessionStop hook invokes sync; writer logs the invocation as a COC entry. |
| Ed25519 signing partial | Writer fails closed. Fix: generate missing keys for context-manager + other agents via `0x_agent_keygen.py`. |
| `reasoning.jsonl` no writer | Contract explicitly names all COC files. `reasoning.jsonl` either gets a writer implementation or is declared deprecated. No orphan references. |
| `claim-coc.jsonl` no chain | Same as above — contract enforces chain on all `.jsonl` files it manages. |

### From agent-perms-audit (still in flight):

Once findings return, the contract handles them the same way: agents need only Bash access to the writer; the write-guard hook is the single place to adjust which paths are blocked from direct Write.

---

## 3. Writer Script Specification (`scripts/4x_coc_writer.py`)

**Tier header (per script-equilibrium rule):**
```python
# TIER: 4x (evidence/COC)
# REPLACES: ad-hoc direct-write pattern across all agents
# METRIC: COC chain integrity = 100% (zero silent append, zero fungibility zones)
# LOAD: core (system-critical; forensic integrity fails without it)
```

**CLI contract:**
```bash
python3 4x_coc_writer.py append \
    --file /mnt/d/0local/gitrepos/faerie2/forensics/coc.jsonl \
    --entry '{"ts":"2026-04-23T20:10:00Z","agent_id":"context-manager",
              "task_id":"wave1-triage","body":{"action":"queue-scan",...}}'

# Exit codes:
#   0   = appended, hash chain valid, signature verified
#   10  = missing required field (ts, agent_id, task_id, body)
#   11  = missing Ed25519 key for agent_id
#   12  = target file locked (retry with backoff)
#   13  = chain integrity check failed (prev_entry_hash mismatch)
#   14  = write guard bypass not authorized
```

**Required entry schema:**
```json
{
  "ts": "ISO8601",
  "agent_id": "context-manager",
  "agent_run_id": "<AGENT-RUN-ID>",
  "session_id": "<CLAUDE_SESSION_ID>",
  "task_id": "<task_id>",
  "body": {"action": "...", "...": "..."},
  "entry_hash": "<writer-computed>",
  "prev_entry_hash": "<writer-computed>",
  "signature": "<writer-computed Ed25519>"
}
```

**Atomic append pattern (pseudocode):**
```python
def append(file_path, entry):
    validate_required_fields(entry)
    key = load_ed25519_key(entry["agent_id"])  # fail if missing
    with open(file_path, "r+b") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        last = read_last_line(f)
        prev_hash = last["entry_hash"] if last else GENESIS_HASH
        body_canonical = canonical_json(entry["body"])
        entry["prev_entry_hash"] = prev_hash
        entry["entry_hash"] = hmac_sha256(prev_hash + body_canonical, CHAIN_KEY)
        entry["signature"] = ed25519_sign(body_canonical, key)
        f.seek(0, 2)  # end
        f.write(canonical_json(entry).encode() + b"\n")
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    hash_tracker.snapshot(file_path)
```

---

## 4. Write Guard Spec (`hooks/8x_coc_write_guard.py`)

**Hook type:** PreToolUse (intercepts Write + Edit before tool fires)

**Blocked path patterns** (regex):
```
.*/forensics/.*\.jsonl$
.*/forensics/.*-coc\.jsonl$
.*/memory/forensics/.*\.jsonl$
.*hash_manifest.*\.json$
.*genesis_manifest\.json$
.*evidence_manifest\.json$
```

**Allow-bypass condition:** `COC_WRITER_ACTIVE=1` env var + `COC_WRITER_PID` matches calling process.

**Error response** (when blocked):
```
COC WRITE DENIED: {path}
Direct Write to forensic files is prohibited. Use the guarded writer:
    python3 faerie2/scripts/4x_coc_writer.py append --file {path} --entry '<json>'
See: docs/COC-WRITE-CONTRACT.md
```

---

## 5. Agent Contract (rules-optional update)

Add to `rules-optional/coc-write-contract.md`:

```markdown
# COC Write Contract — Universal Rule (rules-optional)

Agents MUST NOT call Write or Edit tools on:
- Any file matching `*-coc.jsonl` or `*/forensics/*.jsonl`
- `hash_manifest*.json`, `genesis_manifest.json`, `evidence_manifest*.json`

Agents MUST append COC entries via Bash:
    python3 {repo}/scripts/4x_coc_writer.py append \
        --file {forensic_file} --entry '{<json>}'

Required entry fields: ts, agent_id, agent_run_id, session_id, task_id, body.
Writer computes: prev_entry_hash, entry_hash, signature.

Rationale: the writer is the only code path that maintains hash-chain integrity
and Ed25519 signatures. Direct writes break the chain (see 2026-04-16 orphan-
migration fungibility zone for what happens when this rule is violated).

Permission footprint: agents need Bash only. No Write on forensic paths.
```

---

## 6. Migration Plan (phased, to avoid destabilizing existing chains)

**Phase 1 (this session, design-only):** Ship this contract doc + specs. Zero code execution.

**Phase 2 (next session, implementation):**
1. Write `4x_coc_writer.py` (single producer). Test in isolation with fixture files.
2. Write `8x_coc_write_guard.py`. Enable in settings.json hook chain.
3. Write `0x_agent_keygen.py` sweep: generate missing Ed25519 keys for agents that don't have them.
4. Migrate `claim-coc.jsonl` + `training-log.jsonl` to chained format (append-only, with genesis anchor).

**Phase 3 (audit + repair, after writer stable):**
1. Re-hash `coc.jsonl` L41-49 fungibility zone: read each body, replay through writer, emit `coc_rechained_2026-04-23_{sid}.jsonl` (versioned, not overwriting original).
2. Declare `deletion-coc.jsonl` L41 genesis re-anchor via typed `chain_segment_boundary` entry appended to that file.
3. Rechain `deletion-coc.jsonl` L45-47.
4. Backfill `task_id` via sidecar `coc-task-map.jsonl` for historical entries.

**Phase 4 (hardening):**
1. Wire `5x_forensics_b2_sync.py` to SessionStop hook.
2. Wire `4x_bash_stdout_capture.py` to PostToolUse Bash.
3. CI gate: `9x_equilibrium_audit.py --check-coc` fails PR if any forensic file lacks chain integrity.

**Immutability guarantee across all phases:** original forensic files are never modified. Corrections append; re-hashed versions write to new files with `_rechained_{ts}` suffix. A COC entry declares the correction operation with pointer back to the original.

---

## 7. Permission Footprint Comparison

| Capability | Before contract | After contract |
|---|---|---|
| Agent Write on `forensics/*.jsonl` | Required (and sandboxed inconsistently) | **Denied** (write guard blocks) |
| Agent Write on `memory/forensics/*.jsonl` | Sometimes allowed | **Denied** |
| Agent Bash execution | Required | Required (unchanged) |
| Agent Write on regular files (repo, vault) | Allowed | Allowed (unchanged) |
| Failure mode if agent tries direct COC write | Silent success, may break chain | Explicit block with remediation message |

The permission matrix collapses: one blocked pattern (`*/forensics/*.jsonl`), one required tool (Bash to the writer). Every other sandbox rule stays as-is.

---

## 8. Honest Gaps

Things this contract does NOT solve on its own:

1. **Historical orphans remain.** The 9-entry fungibility zone in `coc.jsonl` is already broken — the contract prevents future instances but does not un-break the past. Phase 3 repair with append-only re-hash versions is the mitigation.
2. **Bash stdout pre-2026-04-23 is unrecoverable.** The capture hook (`4x_bash_stdout_capture.py`) only captures outputs from its activation forward. Prior executions' stdouts are lost.
3. **Writer must be correct.** Moving trust from N agents to 1 writer is progress, but concentrates risk. Writer needs: unit tests, fuzzing, and — ideally — a second independent reader that validates chain integrity (`4x_coc_verifier.py` as adversarial companion).
4. **Key revocation not designed.** If an agent's Ed25519 key is compromised, how does the system know to reject its signatures? Needs a revocation list + signature-age check. Out of scope for v1.
5. **Cross-repo coordination.** If faerie2, cybertemplate, and data-analysis-engine each run their own writer with different chain keys, cross-repo forensic queries get harder. Shared chain key or federated verifier needed eventually.

---

## 9. Next Actions

- [ ] Review this doc with user; confirm design before implementation
- [ ] Task #38: Implement `4x_coc_writer.py` (Phase 2 item 1)
- [ ] Task #39: Implement `8x_coc_write_guard.py` (Phase 2 item 2)
- [ ] Task #40: Agent keygen sweep (Phase 2 item 3)
- [ ] Task #41: `claim-coc.jsonl` + `training-log.jsonl` chain migration (Phase 2 item 4)
- [ ] Task #42: Re-hash `coc.jsonl` L41-49 fungibility zone (Phase 3)
- [ ] Task #43: Wire B2 sync + Bash stdout capture hooks (Phase 4)

Each task gets its own forensic entry when completed, written via the writer this doc specifies.
