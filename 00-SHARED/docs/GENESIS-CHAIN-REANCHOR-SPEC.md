---
type: spec
status: draft-v1
created: 2026-04-23
tags: [coc, worm, genesis-chain, hash-chain, reanchor, forensics]
parent: "[[COC-WRITE-CONTRACT]]"
up: "[[COC-WRITE-CONTRACT]]"
sibling: 
cites: 
supersedes: 
doc_hash: sha256:fb2738603f97762f2dbbeae558ffde83f25b21be04bae31f50dd6904c22f6d6c
hash_ts: 2026-04-23T20:56:27.498687+00:00
hash_method: body-sha256-v1
---

> [↑ COC Write Contract](./COC-WRITE-CONTRACT.md) · [→ Native Bridge](./NATIVE-FAERIE-BRIDGE.md) · [⌂ Docs](./README.md)

# Genesis Chain Re-Anchor Spec

**User directive (2026-04-23):** "ensure if script runs again it creates a genesis 2 for helping get coc back on track ... genesis script when normalization or realigning of the hash chain must happen."

**Principle:** Genesis proofs are not one-time events. They form their own **meta-chain** above the COC chain. Each provisioner run creates the next genesis-N, and the new genesis IS the mechanism by which damaged or drifted COC segments get realigned — forward-only, evidence-preserving.

---

## 1. Why Genesis-N (Not One-Shot)

**Historical damage requires forward recovery, not retroactive rewrite.** The 2026-04-23 COC audit found a 10-entry fungibility zone at `coc.jsonl` L41-49 (orphan-migration-agent batch wrote identical hashes), plus L50 unchained, plus several unchained tails in `deletion-coc.jsonl`. The naive fix (re-hash in place) would modify evidence — forensically illegal. The correct fix is to **declare the damaged segment closed, anchor a new segment from genesis-N, and chain forward from there.**

**Drift between bucket state and audit claims needs re-attestation.** Even if the COC chain is intact, bucket settings may have been modified (bucket info updated, retention changed, new files uploaded outside policy). A fresh genesis proof re-attests the current state against the current policy — if they diverge, the genesis run fails loudly.

**Admin compromise requires re-anchoring.** If someone ever gains admin access and modifies retention policies or bucket settings, a later genesis run detects the divergence and writes a compliance-locked record of what was altered and when.

**Operational heartbeat.** Running the genesis script periodically (monthly, quarterly, or on trigger events) produces a compliance-locked timeline showing the bucket was verified at each point. Auditors can walk genesis-1 → genesis-2 → genesis-N and verify no gaps.

---

## 2. Genesis Chain Topology

```
faerie-worm/
├── worm-genesis/
│   ├── genesis-1-20260423T204109Z.json         ← initial (already exists)
│   ├── genesis-2-20260423T{ts}.json            ← second run (this spec)
│   ├── genesis-3-20260???T{ts}.json            ← third run (future)
│   └── genesis-N-{ts}.json                     ← each prior-linked
└── worm-genesis-meta/
    └── genesis-chain-index.json                 ← list of genesis files + prior_hash links
```

**Each genesis-N file includes:**

```json
{
  "schema_version": "1.1",
  "proof_type": "worm-genesis",
  "genesis_sequence_number": N,
  "created_at": "<iso8601>",
  "bucket_name": "faerie-worm",
  "bucket_id": "00224c6103a1b1c890dd0812",

  "prior_genesis": {
    "sequence_number": N - 1,
    "filename": "worm-genesis/genesis-(N-1)-<ts>.json",
    "file_id": "<b2 fileId of genesis-(N-1)>",
    "sha256": "<sha256 of genesis-(N-1) body>",
    "created_at": "<iso8601 of N-1>"
  },

  "bucket_settings_observed": {
    "file_lock_enabled": true,
    "default_retention_mode": "governance",
    "default_retention_period_days": 90,
    "default_sse_mode": "SSE-B2",
    "default_sse_algorithm": "AES256",
    "bucket_type": "allPrivate",
    "bucket_info_digest": "sha256:<canonical-json-of-bucket-info>"
  },

  "settings_drift_from_prior": {
    "any_drift": false,
    "changed_keys": [],
    "prior_value": {},
    "current_value": {}
  },

  "enforcement_tests": [ /* 6 tests, same as genesis-1 */ ],

  "coc_chain_state_snapshot": {
    "coc_jsonl_line_count": 50,
    "coc_jsonl_last_entry_hash": "sha256:...",
    "coc_jsonl_integrity": "COMPROMISED|CLEAN|RE-ANCHORED",
    "known_damage_segments": [
      {"file": "coc.jsonl", "lines": "41-49", "type": "fungibility-zone", "declared_by": "genesis-1"},
      {"file": "coc.jsonl", "line": 50, "type": "unchained-tail", "declared_by": "genesis-1"}
    ],
    "segment_closed_by_this_genesis": "coc.jsonl[1..50]",
    "new_segment_anchor_hash": "sha256:<genesis-N's own sha256>",
    "new_segment_first_entry_hint": "next append to coc.jsonl should set prev_entry_hash = sha256 of this genesis"
  },

  "legal_hold": true,
  "file_retention_mode": "compliance",
  "retain_until_timestamp_ms": <1 year from now>,

  "auditor_instructions": "To verify this genesis: (1) fetch genesis-N's file from faerie-worm; (2) verify its sha256 matches coc_chain_state_snapshot.new_segment_anchor_hash; (3) walk prior_genesis links back to genesis-1 — each must chain cleanly; (4) attempt delete of any genesis file — all should reject with HTTP 401 (compliance + legal hold).",

  "coc_anchor": {
    "coc_writer_used": "4x_coc_writer.py",
    "task_id": "task-42d-genesis-N-reanchor",
    "entry_in_coc_jsonl": "<entry_hash of COC entry declaring this genesis>"
  }
}
```

---

## 3. Provisioner Behavior Changes

When `0x_b2_faerie_worm_provision.py` runs:

### 3.1 If bucket doesn't exist
- Create bucket (existing logic)
- Run validation suite
- Upload `genesis-1-{ts}.json` with legal-hold=on + compliance retention
- Initialize `worm-genesis-meta/genesis-chain-index.json` with entry for N=1

### 3.2 If bucket exists (EVERY SUBSEQUENT RUN)
- Skip bucket creation (idempotent)
- Read `worm-genesis-meta/genesis-chain-index.json` to find latest N
- Fetch prior genesis (N) via b2 download; verify its hash
- Re-run validation suite against current bucket state
- **Detect settings drift:** compare current bucket_settings vs prior genesis's snapshot
- **Snapshot COC chain state:** read `forensics/coc.jsonl` last entry; record damaged segments known from prior genesis
- Build genesis-(N+1) with:
  - Sequence number incremented
  - `prior_genesis.sha256` linking back to N
  - Drift report (if any)
  - New segment anchor hash = genesis-(N+1)'s own sha256
  - enforcement_tests results (fresh run)
- Upload `genesis-(N+1)-{ts}.json` with legal-hold=on + compliance-retention
- Update `worm-genesis-meta/genesis-chain-index.json` with new entry
- **Append COC entry to `forensics/coc.jsonl` via `4x_coc_writer.py`** declaring:
  - Genesis-(N+1) created
  - Prior segment closed at line K
  - New segment anchors to genesis-(N+1)'s hash
  - Entry itself uses prev_entry_hash = old tail; entry's body includes the new segment boundary declaration

### 3.3 Exit conditions
- Exit 0: genesis-(N+1) uploaded + verified + COC entry appended + legal hold confirmed
- Exit non-zero + rollback: if any step fails (upload, verification, legal-hold confirmation)

---

## 4. Chain Normalization Semantics

**"Normalization" = forward-only, evidence-preserving realignment.**

Prior COC entries are NEVER modified. Instead:

- **Damaged segments are named, not rewritten.** Genesis-(N+1)'s `coc_chain_state_snapshot.known_damage_segments` explicitly cites lines and damage type.
- **Segment boundary is declared.** `segment_closed_by_this_genesis: "coc.jsonl[1..50]"` tells any future reader where the prior (damaged) segment ends.
- **New segment anchors to the genesis.** `new_segment_anchor_hash` is the genesis's own sha256. Any future COC entry in `coc.jsonl` that wants to chain correctly sets its `prev_entry_hash` to this value, starting a fresh integrity zone.
- **COC entry in `coc.jsonl` declares the re-anchor.** Written via `4x_coc_writer.py`, chain-linked, signed. The declaration IS the re-anchor — readers who reach that entry know "from here, the chain starts fresh against genesis-(N+1)."

### 4.1 For the current 2026-04-23 damage (known state)

- `coc.jsonl` L1-40: intact chain (legacy `sha256:` prefix entries, pre-writer)
- `coc.jsonl` L41-49: fungibility zone (orphan-migration-agent bug, identical hashes)
- `coc.jsonl` L50: unchained tail (2026-04-21 restore entry, no hash fields)
- `deletion-coc.jsonl` L45-47: unchained tail

**Genesis-2 declares:**
- `known_damage_segments`: all 4 listed above
- `segment_closed_by_this_genesis`: "coc.jsonl[1..50] and deletion-coc.jsonl[1..47]"
- `new_segment_anchor_hash`: genesis-2's sha256
- Writes COC entry to `coc.jsonl` as line 51 (or to a new file `coc_segment-2.jsonl` if user prefers clean split) via `4x_coc_writer.py`, with `prev_entry_hash = sha256(genesis-2.json body)`, chain-correctly linked forward.
- Writes matching entry to `deletion-coc.jsonl` as re-anchor boundary

After genesis-2 uploads:
- Legacy damage is preserved as evidence (never touched)
- Forward chain is provably correct from genesis-2 onward
- Auditor can verify: "from line 51 forward, hash chain is valid against genesis-2"
- Genesis-2 itself is compliance-locked + legal-held, so the re-anchor point is unforgeable

---

## 5. Implementation Steps

This spec is authoritative for the **next** provisioner update. Implementation sequencing:

1. **Legal-hold agent finishes first** (in-flight, agent `acf61cde`). It will:
   - Add policy module `4x_b2_legal_hold_policy.py`
   - Wire legal-hold into provisioner + sync
   - Retroactively legal-hold the existing genesis-1 proof
   - This leaves the provisioner at a clean state (legal-hold wired, genesis-1 locked)

2. **Genesis-N agent runs next** (spawned after legal-hold completes):
   - Implements `worm-genesis-meta/genesis-chain-index.json` write logic
   - Adds prior-genesis detection + drift check
   - Adds `coc_chain_state_snapshot` collection from `forensics/coc.jsonl`
   - Adds segment-close declaration logic
   - Adds COC entry via `4x_coc_writer.py` with the re-anchor metadata
   - Tests: run provisioner again → produce genesis-2 → verify chain linkage
   - Upload genesis-2 to live bucket as proof-of-concept

3. **Task #40 deprecated/superseded.** The earlier plan to re-hash `coc.jsonl` L41-49 is replaced by this forward-only re-anchor approach. Task description should change to "run genesis-2 to declare the L41-49 fungibility zone as a closed segment and anchor forward chain." Evidence is preserved; damage is declared; recovery is auditable.

---

## 6. Non-Goals

- **Not modifying prior COC entries.** They stay exactly as-is. Damage is evidence, not a bug to hide.
- **Not automating re-genesis on a timer.** Each run is deliberate (operator invokes or CI runs on specific triggers). Avoids generating spurious chain segments.
- **Not replacing per-entry hash chains.** The entry-level `4x_coc_writer.py` chain still applies within each segment. Genesis-N is the meta-level anchor between segments.
- **Not encrypting the genesis proof body.** Genesis proofs are designed to be PUBLICLY auditable. Encrypt only the bucket contents (which already is, via SSE-B2).

---

## 7. Testing

The provisioner's "run it again" flow must be tested by:

1. Run provisioner → confirm it detects existing bucket + existing genesis-1
2. Confirm it generates genesis-2 (not genesis-1 again)
3. Confirm genesis-2 links to genesis-1 via `prior_genesis.sha256`
4. Confirm `coc_chain_state_snapshot` correctly identifies the known damage
5. Confirm new COC entry appended to `coc.jsonl` via `4x_coc_writer.py` with correct segment-boundary body
6. Download genesis-2; try to delete → confirm rejection (compliance + legal hold)
7. Run provisioner a third time → produce genesis-3, linking back to genesis-2
8. Walk the genesis chain via `worm-genesis-meta/genesis-chain-index.json` — verify 3 entries, each prior-linked

---

## 8. Summary for HONEY

This concept belongs in HONEY as an extension of mth00076 (proof-in-place). Proposed follow-up entry (to add once genesis-2 successfully lands):

> **mth000XX | method | permanent | 1.0] GENESIS CHAIN IS ITS OWN META-PROOF.** When the primary COC chain is damaged (fungibility zone, unchained tail, admin drift), recovery is forward-only: create genesis-N with compliance-lock + legal-hold, declare prior segment closed, anchor new segment to genesis-N's own hash. Evidence preserved; damage named, not hidden; recovery auditable; walk genesis-1 → genesis-N to verify no gaps. Each re-anchor event writes a COC entry via the writer, linking damage declaration to the genesis proof that superseded it.

---

## 9. Report-as-Super-Genesis

**User directive (2026-04-23):** "like when the report is published, the new hash chain is every artifact cited."

**Principle:** A published investigation report IS a super-genesis at the publication scale. It operates at a higher abstraction layer than the bucket-level genesis chain — it commits to the Merkle tree of every artifact it cites.

### 9.1 Why Reports Are Super-Genesis Proofs

- **Reports synthesize evidence.** A published report names, cites, and depends on every artifact that informed its conclusions. If any cited artifact is later tampered, the report's claims become unsupported.
- **Publishing freezes the tree.** Uploading a super-genesis proof with compliance + legal-hold (5 years) creates an unforgeable record of which artifacts existed, with which hashes, at the moment of publication.
- **The Merkle root is the integrity seal.** `merkle_root = sha256(concat(sorted(sha256(artifact_i) for all cited) + [report_sha256]))`. Any future tampering with any cited artifact breaks the Merkle root — verifiable by any auditor with access to the original files.
- **Supersedes "report is just a doc."** Prior practice treated reports as vault documents with a doc_hash stamp. That stamps the report itself but does not commit to its evidence tree. Super-genesis does both.

### 9.2 Report Super-Genesis Topology

```
faerie-worm/
├── report-supergenesis/
│   ├── {slug}-{ts}.json      ← published report's super-genesis (5-year compliance lock)
│   └── ...
forensics/
└── report-supergenesis/
    └── {slug}-{ts}.json      ← local copy (git-tracked)
```

### 9.3 Super-Genesis Schema (v1.0)

```json
{
  "schema_version": "1.0",
  "proof_type": "report-supergenesis",
  "report_slug": "01-F0-Architecture-Emergence",
  "report_path": "/mnt/d/.../Hive/01-F0-Architecture-Emergence.md",
  "report_sha256": "sha256 of report body (frontmatter stripped for .md)",
  "created_at": "ISO8601",
  "cited_artifacts": [
    {
      "path": "...",
      "sha256": "sha256 of artifact file bytes",
      "coc_anchor": "entry_hash:hmac:... | genesis:worm-genesis/genesis-N.json | null",
      "resolved": true
    }
  ],
  "merkle_root": "sha256 of concat(sorted cited_artifact sha256s + report_sha256)",
  "prior_report_supergenesis": {...} | null,
  "legal_hold": true,
  "file_retention_mode": "compliance",
  "retain_until_timestamp_ms": "<5 years from publish>",
  "b2_file_id": "<B2 fileId>",
  "coc_entry_hash": "<entry_hash of COC entry for this publication>"
}
```

**Why 5 years (not 1 year like bucket genesis)?** Reports are publication-grade artifacts. Statutes of limitations for the domains served by faerie2 extend to 5+ years. The retention period must outlast any anticipated challenge period.

### 9.4 Merkle Discipline

- **Sort cited_artifacts by path before hashing** — deterministic order, reproducible by any verifier.
- **Include report sha256 in the Merkle inputs** — the report itself is a member of its own tree.
- **Unresolved citations** (paths that don't exist as files) are recorded but excluded from Merkle computation. Their presence is documented; their absence in the hash tree is declared explicitly.
- **Prior reports as citations** — if a report cites an earlier published report, that report's super-genesis sha256 is its anchor. Reports form a recursive meta-chain.

### 9.5 Relationship to Bucket Genesis Chain

| Scale | Object | Retention | Chain |
|-------|--------|-----------|-------|
| Bucket | genesis-N.json | 1 year, compliance | prior_genesis.sha256 → chain |
| Report | {slug}-supergenesis.json | 5 years, compliance | merkle_root → artifact tree |
| Session | coc.jsonl entries | governance | prev_entry_hash → HMAC chain |

These are three independent (but cross-referencing) proof layers. The bucket genesis anchors the COC chain. The report super-genesis anchors the evidence tree. COC entries reference both.

### 9.6 Implementation

Script: `scripts/6x_report_supergenesis.py` (TIER 6x, LOAD sauce)

```bash
# Publish a report
python3 scripts/6x_report_supergenesis.py publish \
    --report /path/to/report.md \
    --citations citations.json \
    --bucket faerie-worm

# Auto-extract citations from frontmatter cites: field
python3 scripts/6x_report_supergenesis.py publish \
    --report /path/to/report.md

# Verify a supergenesis proof (re-hash all cited artifacts)
python3 scripts/6x_report_supergenesis.py verify \
    --file forensics/report-supergenesis/{slug}-{ts}.json
```

**citations.json format:**
```json
[{"path": "/absolute/path/to/artifact.md"}, ...]
```

If `--citations` is omitted, the script auto-extracts from frontmatter `cites:` list (yaml list of paths or doc references).

### 9.7 Relation to HONEY mth00076 (proof-in-place)

mth00076 states: "proof lives in the artifact's storage location, not in an audit log." Super-genesis extends this to the publication scale: the report's proof lives where the report is published (B2 WORM), not in a separate audit system. The entire evidence tree is frozen at the point of publication. Any later challenge faces a compliance-locked, legal-held, Merkle-verified record of exactly what existed when the report was written.

**Follow-up crystallization for HONEY (to add after genesis-2 + report super-genesis land):**

> **mth000XY | method | permanent | 1.0] GENESIS CHAIN IS RECURSIVE: bucket → report → session.** Three proof scales compose: (1) bucket genesis-N anchors the COC chain segment (1-year compliance lock); (2) report super-genesis commits to the Merkle tree of cited artifacts at publication (5-year compliance lock); (3) session COC entries chain-link individual operations (HMAC). Each scale references the one below it. Any challenge walks the chain: report super-genesis → cited artifact sha256s → COC entry anchors → bucket genesis. The chain is forward-only and unforgeable at every level.
