---
status: READY-TO-START — awaiting operator greenlight
title: Forensic COC v2 — Phase 1 Implementation Kickoff (Shadow Writer)
parent_doc: 00-Publications/FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md
created: 2026-05-24
last_updated: 2026-05-24
scope: Concrete implementation plan for week 1 of v2 rollout (zero-risk shadow writing)
tags: [forensics, implementation, phase-1, shadow-writer, merkle, sigstore]
---

# Forensic COC v2 — Phase 1 Implementation Kickoff

> **Companion to** `FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md` (the architecture).
> This doc is the **buildable plan** for Phase 1 — the shadow-writer week.
> Phase 1 has zero production risk: legacy `coc.jsonl` remains authoritative
> through this phase. The new code observes, writes a parallel chain, and
> we compare daily.

---

## 0. Phase 1 success criteria

Phase 1 is done when ALL of the following hold for 7 consecutive days:

1. ✅ Every event that lands in legacy `coc.jsonl` ALSO lands in a v2 shard
2. ✅ Daily diff job reports zero divergence between legacy and v2 encodings
   of the same events
3. ✅ Master index reflects every shard head accurately
4. ✅ `swarmy_coc_v2_block_get` MCP tool returns valid data for any v2 block
5. ✅ No performance regression — hot-path latency stays within 10% of
   pre-Phase-1 baseline
6. ✅ Total disk overhead < 2× legacy chain size (shadow writing doubles
   but doesn't catastrophically inflate)
7. ✅ No crashes or data corruption in either chain

If any criterion fails persistently, roll back Phase 1: stop writing v2,
keep legacy chain only. The new code is feature-flagged and reversible.

---

## 1. The deliverables

Four scripts + two MCP tools + one cron + one feature flag.

### 1.1 `scripts/2x_coc_v2_writer.py` — The shadow writer

The brain. Reads the same events the legacy writer sees; emits to v2 shards.

**Interface (called from `_append_coc_entry()`):**

```python
def shadow_write_v2(
    operation: str,
    detail: str,
    agent_id: str,
    extra: dict | None,
    *,
    shard: str | None = None,
) -> dict:
    """
    Shadow-write an event to the v2 architecture.
    
    Returns:
      {"shard": "<resolved shard>", "block_index": <int>, "leaf_index": <int>,
       "leaf_hash": "<sha256>", "ok": True}
    
    On failure: returns {"ok": False, "error": "..."} — NEVER raises.
    Phase 1 is observe-only; the legacy chain is still authoritative.
    """
```

**Behavior:**
1. Resolve shard (default: derive from `extra.mission` field or "main")
2. Append leaf event to the current open session buffer for that shard
3. If buffer hits N=100 leaves OR T=300s since last seal → seal a block
4. Write block to `forensics/v2/shards/<shard>/blocks.jsonl`
5. Update `forensics/v2/master.jsonl` with new shard head anchor
6. Return success descriptor

**Failure semantics:**
- ANY exception in v2 path → log + return `{"ok": False, ...}`
- Legacy chain write must NEVER be blocked by v2 failure
- Phase 1 must be invisible to existing code paths

### 1.2 `scripts/2x_coc_v2_shard.py` — Per-shard chain manager

Owns one shard's blocks file. Pure data layer — no business logic.

**Interface:**
```python
class ShardChain:
    def __init__(self, shard_name: str, root_dir: Path): ...
    
    def append_leaf(self, leaf: dict) -> int: ...      # returns leaf index in current buffer
    def buffer_size(self) -> int: ...
    def buffer_age_seconds(self) -> float: ...
    def seal_block(self, agent_id: str, signer: Signer) -> dict: ...
    def latest_block(self) -> dict | None: ...
    def get_block(self, index: int) -> dict | None: ...
    def merkle_proof(self, block_index: int, leaf_index: int) -> list[str]: ...
```

**Files written:**
```
forensics/v2/shards/<shard>/
    buffer.jsonl              ← current open session (replaces on seal)
    blocks.jsonl              ← sealed blocks (append-only)
    payloads/<date>/<block_index>.jsonl  ← raw event leaves
```

### 1.3 `scripts/2x_coc_v2_master.py` — Master index manager

Owns `forensics/v2/master.jsonl`. Single-writer, append-only.

**Interface:**
```python
class MasterIndex:
    def __init__(self, path: Path): ...
    
    def upsert_shard_anchor(
        self, shard: str, head_block_hash: str, block_index: int
    ) -> dict: ...                       # writes a new anchor entry
    
    def latest_anchor(self, shard: str) -> dict | None: ...
    def all_anchors(self) -> Iterator[dict]: ...
    def shard_list(self) -> list[str]: ...
```

**File format:**
```jsonl
{"ts": "...", "shard": "main", "head_block_hash": "...", "block_index": 0}
{"ts": "...", "shard": "mission-A", "head_block_hash": "...", "block_index": 0}
{"ts": "...", "shard": "main", "head_block_hash": "...", "block_index": 1}
...
```

Each anchor entry is itself signed by the master writer's key (for now,
the same key the legacy chain uses).

### 1.4 `scripts/2x_coc_v2_diff_check.py` — Daily divergence detector

Runs on cron at 03:30 UTC. Walks today's legacy entries + today's v2 leaves;
reports any event that exists in one chain but not the other.

```bash
python3 scripts/2x_coc_v2_diff_check.py --date 2026-05-25
# → divergence_count: 0  (good)
# → divergence_count: 3  (bad — write to forensics/system/v2-divergence.log)
```

Phase 1 success criterion #2 is this script reporting zero divergence
across 7 consecutive days.

### 1.5 MCP tools (read-only verification surface)

In `deploy/mcp-server/tools/coc_v2.py` (NEW):

```python
@authed("reader")
def swarmy_coc_v2_block_get(shard: str, block_index: int) -> dict:
    """Read a specific v2 shard block. Returns block JSON + payload ref."""

@authed("reader")
def swarmy_coc_v2_proof_get(shard: str, block_index: int, leaf_index: int) -> dict:
    """Return the Merkle inclusion proof for a leaf in a block.
    Caller verifies offline by reconstructing the merkle root."""
```

Wire into `server.py` Routes list. Read-only — safe to ship in Phase 1.

### 1.6 Cron entry

```
# Daily 03:30 UTC — v2 shadow chain divergence check
30 3 * * * cd /opt/swarmy && python3 scripts/2x_coc_v2_diff_check.py >> /var/log/coc-v2-diff.log 2>&1   # swarmy-managed:coc-v2-diff
```

Added to `deploy/scripts/install-crons.sh`.

### 1.7 Feature flag

```bash
# In .env:
COC_V2_SHADOW_WRITE=1   # default: 0 — opt-in for Phase 1
```

Honored by `_append_coc_entry()` — when 0, the legacy-only path runs
(current behavior). When 1, also calls `shadow_write_v2()`.

This is the kill switch. If anything goes wrong, `COC_V2_SHADOW_WRITE=0`
+ restart MCP server reverts to pure legacy behavior with zero data loss.

---

## 2. Implementation order (4 PR-sized commits)

Each commit is independently committable, reversible, and low-risk. None
change the legacy code path.

### Commit 1: `2x_coc_v2_shard.py` + tests
- `ShardChain` class implementation
- Merkle tree (hand-rolled, ~50 LOC)
- Block sealing + signature
- Unit tests for: append, seal, merkle_proof, get_block

**Verification:** `pytest scripts/test_coc_v2_shard.py` passes; can manually
create a shard, append 5 leaves, seal a block, fetch the proof for leaf #3.

### Commit 2: `2x_coc_v2_master.py` + tests
- `MasterIndex` class implementation
- `upsert_shard_anchor` writes signed master entries
- Idempotent — same anchor written twice doesn't break

**Verification:** Drive a few shards through, check `master.jsonl` reflects
all heads accurately.

### Commit 3: `2x_coc_v2_writer.py` + integration
- `shadow_write_v2()` function
- Calls into `ShardChain` + `MasterIndex`
- Feature flag wiring (`COC_V2_SHADOW_WRITE`)
- Hook into `_append_coc_entry()` (additive — never blocks legacy path)
- MCP tools `swarmy_coc_v2_block_get` + `swarmy_coc_v2_proof_get`

**Verification:** Set flag, run a few MCP tool calls that trigger
`_append_coc_entry()`, verify both `coc.jsonl` AND `forensics/v2/shards/*`
get updated.

### Commit 4: `2x_coc_v2_diff_check.py` + cron + docs
- Diff-check script
- Cron entry in `install-crons.sh`
- Update `deploy/ENV-REFERENCE.md` with `COC_V2_SHADOW_WRITE` flag
- Update operator-facing aliases (e.g., `swarmy-coc-v2-status` to inspect
  shadow chain state)

**Verification:** Run diff-check manually; cron entry installs; status alias
shows shard list + last anchor times.

---

## 3. Test plan

### 3.1 Unit tests
- Merkle tree correctness (proof reconstruction works for all leaves)
- Block signature verification
- Shard chain integrity (each block's prev_hash matches previous block)
- Master index ordering preserved

### 3.2 Integration tests
- End-to-end: append 1000 events across 3 shards, seal blocks, check
  master index has correct anchors
- Failure injection: kill writer mid-block-seal; restart; chain
  recovers without corruption
- Concurrent writes to same shard from multiple processes — must
  serialize correctly

### 3.3 Shadow comparison
- Run `_append_coc_entry` 10K times in a loop
- Verify every legacy entry has a v2 leaf equivalent
- Verify divergence count = 0

### 3.4 Performance
- Measure `_append_coc_entry` latency with flag off vs on
- Acceptable: <10% slowdown (because v2 writes are async after legacy)
- Unacceptable: >25% slowdown — would block on hot loops

---

## 4. Rollback plan

If Phase 1 reveals problems:

| Problem | Action |
|---|---|
| Divergence detected | Set `COC_V2_SHADOW_WRITE=0`, restart MCP. Legacy keeps running. Investigate offline. |
| Performance regression > 25% | Same — kill flag, investigate. |
| Disk usage > 2× legacy | Same — investigate retention / compaction. |
| Crashes in v2 path | Defensive try/except around `shadow_write_v2()` already; flag-off cleans up state. |
| Hash mismatch in master index | Most serious — diff-check should catch this on day 1. Investigate root cause before any further v2 development. |

In all cases: legacy chain has been untouched. Rollback is `flag=0 +
restart` — no data migration, no orphan state.

---

## 5. Phase 1 → Phase 2 handoff criteria

Greenlight Phase 2 (Merkle batching becomes authoritative) requires:

1. All 7 Phase 1 success criteria met
2. Operator has reviewed the v2 chain manually
3. Diff-check report archived in vault
4. No open bugs in v2 code path
5. Performance metrics documented (latency before/after)

Phase 2 then flips: new events go ONLY to v2; legacy `coc.jsonl` becomes
read-only on a specific timestamp. The v2 genesis block (Phase 3) anchors
the final legacy hash so the history remains verifiable.

---

## 6. Estimated effort

| Item | Estimate |
|---|---|
| Commit 1 (shard) | 4-6 hours |
| Commit 2 (master) | 2-3 hours |
| Commit 3 (writer + MCP) | 3-5 hours |
| Commit 4 (diff-check + cron + docs) | 2 hours |
| Manual verification + bug fixes | 4-6 hours |
| **Total** | **15-22 hours** |

That's ~2-3 focused work days for a human or a focused MAKER spawn.

---

## 7. Open Phase 1 questions

1. **Shard naming convention.** Default to `extra.mission` field? Or
   `extra.task_id` (more granular)? Or operator-configured map? Start with
   `mission` field, fall back to "main" if absent.

2. **Buffer seal triggers.** Default `N=100 events OR T=300 seconds` —
   should these be per-shard tunable? Probably yes; add to ENV-REFERENCE.

3. **Block signing key in Phase 1.** Reuse the legacy chain's existing key
   for shadow writing? Or generate a separate v2 key? Lean: REUSE existing
   key in Phase 1 to keep complexity low. Phase 3 introduces a v2-specific
   notary key when Rekor lands.

4. **Master index single-writer enforcement.** Use `flock` on
   `master.jsonl` to prevent concurrent writes from racing? Yes — even
   though we only have one MCP server today, future scaling will need this.

5. **Payload storage.** Keep payloads inline in blocks (small N), or
   external `payloads/<date>/<block_index>.jsonl`? Lean: external from
   day 1 — keeps blocks small + lets us cold-archive payloads later
   without touching the chain.

---

## 8. The "GO" trigger

**Operator types:** "greenlight Phase 1" (or equivalent).

**System spawns** a MAKER (or operator works directly) to execute the
4-commit sequence above. Manifest written to `forensics/ephemeral/2026-05-24/`.

Phase 1 begins when commit 3 lands + the flag is set on the VPS:
```bash
ssh vps 'cd /opt/swarmy && git pull && echo COC_V2_SHADOW_WRITE=1 >> .env && bash deploy/scripts/redeploy.sh'
```

Phase 1 ends when 7 consecutive days of zero divergence are recorded.

---

## Appendix A: File layout summary

After Phase 1 completes, the forensic tree looks like:

```
forensics/
    coc.jsonl                           ← legacy chain (still authoritative)
    coc-signing-keys/                   ← agent keys
    schemas/                            ← schema definitions
    sessions/                           ← agent session manifests (existing)
    ephemeral/                          ← agent ephemeral writes (existing)
    
    v2/                                 ← NEW in Phase 1
        master.jsonl                    ← master index (append-only)
        shards/
            main/
                buffer.jsonl            ← current open session
                blocks.jsonl            ← sealed blocks
                payloads/
                    2026-05-24/
                        0.jsonl         ← block 0's leaves
                        1.jsonl         ← block 1's leaves
                        ...
            mission-A/
                buffer.jsonl
                blocks.jsonl
                payloads/...
            ...
```

After Phase 3 (Rekor anchoring lands):
```
forensics/v2/
    master.jsonl                        ← now includes rekor_anchor entries
    rekor-proofs/
        <log_index>.json                ← cached inclusion proofs (offline-verifiable)
    genesis.json                        ← v2 genesis block + legacy chain reference
    shards/...                          ← (unchanged from Phase 1)
```

Compact, traceable, audit-friendly.

---

*End of Phase 1 kickoff doc. Companion to architecture paper.*
