---
status: ACTIVE — adopted, in implementation
title: Forensic COC v2 — Merkle Rollups + Sigstore Rekor Anchoring
authors: [swarmy, goodoleusa]
created: 2026-05-23
last_updated: 2026-05-24
scope: swarmy's forensics/coc.jsonl — speed, accuracy, third-party time attestation
operator_decisions:
  forensic_auditability: HARD REQUIREMENT (no equivocation)
  public_anchor: Sigstore Rekor (NOT L2 / blockchain)
  rollout: backward-compat from genesis — old chain remains valid throughout
status_per_phase:
  phase_1_shadow_writing: PROPOSED — awaiting greenlight
  phase_2_merkle_batching: not started
  phase_3_rekor_pinning: not started
  phase_4_old_chain_archival: not started
tags: [forensics, whitepaper, architecture, sigstore, rekor, merkle, transparency-log]
companion_docs:
  - 00-Publications/FORENSIC-COC-V2-PHASE-1-KICKOFF.md (implementation plan for shadow-writer week 1)
---

# Forensic COC v2 — Merkle Rollups + Sigstore Rekor Anchoring

> **Operator-adopted (2026-05-24).** Forensic auditability is a hard
> requirement, not a nice-to-have. Public anchor target is **Sigstore
> Rekor** (transparency log, not blockchain). All migration phases preserve
> the existing `coc.jsonl` chain as authoritative until superseded —
> backward compatibility is the genesis property.

---

## 0. Operator decisions (locked-in 2026-05-24)

| Decision | Locked answer | Rationale |
|---|---|---|
| Adopt the v2 architecture? | **Yes** | Forensic auditability is hard-requirement |
| Public anchor target? | **Sigstore Rekor** | Free, public, Merkle-backed transparency log; no blockchain consensus tax; mature tooling (cosign / sigstore-python / rekor-cli); designed for exactly this use case |
| L2 / blockchain? | **No** | Avoided. Rekor gives us third-party timestamping without wallet custody, gas costs, or chain selection |
| Rollout model? | **Genesis backward-compat** | Old `coc.jsonl` stays valid throughout migration. New chain shadow-writes from day 1. No flag-day cutover. |
| Notary key custody? | Phase 1: Sigstore OIDC keyless signing (operator's GitHub identity, ephemeral cert). Phase 4+: long-lived swarmy notary key | OIDC keyless flow eliminates Phase 1 custody complexity entirely |
| Old chain archival? | **Keep forever, append-only**. New chain anchors back to last `coc.jsonl` entry's hash at v2 genesis block | Historical chain is itself part of the v2 chain via the v2 genesis block |

---

## TL;DR

Three-tier evolution from one fully-signed JSONL to:

1. **Local Merkle batching** — agents accumulate events into per-session
   micro-trees, sign only the root. ~250× signature reduction per event.
2. **Sidecar shards per investigation** — isolated chains checkpointing
   into a master index. Auditors fetch only the shard they need.
3. **Sigstore Rekor anchoring** — hourly/daily, master head hash is
   submitted to `rekor.sigstore.dev` (free public Merkle-backed transparency
   log maintained by Linux Foundation Sigstore). Returns a signed inclusion
   proof. No blockchain. No wallet. No gas.

Light-client verification in O(log N). Public third-party timestamping at
$0/month. Backward compat from genesis.

---

## 1. Why Sigstore Rekor (and not L2 / blockchain)

Originally drafted with Ethereum L2 anchoring; operator chose Rekor.
Direct comparison:

| Property | L2 (Arbitrum/Base/Optimism) | Sigstore Rekor |
|---|---|---|
| Provides third-party timestamp? | ✅ yes | ✅ yes |
| Merkle-backed inclusion proofs? | ✅ yes | ✅ yes (Trillian backend) |
| Cost per anchor | ~$0.05-$0.50 | **$0** |
| Wallet / private key custody | Required | Not required (OIDC ephemeral keys) |
| Setup complexity | Smart contract deploy + ethers + wallet | One CLI call: `rekor-cli upload` |
| Designed for this use case? | Bolted on | **Yes — this is exactly what it's for** |
| Transparency log paradigm | Indirect (via tx history) | Native |
| Latency (anchor → confirmation) | ~30s-2min | ~2s |
| Community / ecosystem | Crypto-financial | Software supply chain (cosign, gitsign, in-toto, SLSA) |
| Long-term durability | Chain-dependent | Linux Foundation + Google + Red Hat |

Rekor is the transparency log that npm, PyPI, Kubernetes, and Linux
distros use to attest to their software supply chain. Adopting it puts our
forensic chain on the same trust substrate as the broader open-source
software-supply-chain world.

### What Rekor gives us

1. **Append-only Merkle-backed log** (Trillian — same engine as Certificate
   Transparency for the public web). Anyone can verify our anchor was
   admitted at time T.
2. **Signed Entry Timestamps (SETs)** — Rekor signs every entry with its
   own key. Verifying = `cosign verify-blob` against a published Sigstore
   trust root. No trust in our host required.
3. **Inclusion proofs verifiable offline.** Once we have the proof bundle,
   we can verify it 10 years from now without contacting Rekor.
4. **OIDC keyless signing** — Phase 1 anchors signed using the operator's
   GitHub identity via Sigstore's ephemeral-cert flow. No long-lived
   signing key to protect. Graduate to a long-lived key only in Phase 4+
   if desired.
5. **Mature CLI ecosystem** — `cosign`, `rekor-cli`, `sigstore-python`,
   `gitsign`, `policy-controller`. Not the first ones using this for
   high-stakes attestation.

---

## 2. Current architecture (what we have)

`forensics/coc.jsonl` is an append-only JSONL file. Each entry:

```json
{
  "ts": "2026-05-23T14:30:00Z",
  "operation": "manifest_promote",
  "detail": "promoted manifest <id> to canonical",
  "agent_id": "maker-h",
  "extra": {"task_id": "...", "files_touched": [...]},
  "prev_hash": "sha256(previous entry)",
  "entry_hash": "sha256(this entry minus entry_hash)",
  "sig": "ed25519(entry_hash) by agent_id's key"
}
```

Implementation:
- `scripts/1g_coc_core.py` — writer + signer
- `deploy/mcp-server/server.py:_append_coc_entry()` — MCP helper
- `.openhands/hooks/` — promotion hooks feed events

### What it gets right

- Tamper detection — modifications break `entry_hash` chain
- Agent attribution — ed25519 sig binds entry to a specific key
- Append-only via filesystem write-protect rules

### Where it strains at scale

| Failure mode | Root cause |
|---|---|
| Per-event sig overhead in burst writes | ~10ms × 1000 events = 10s CPU |
| Audit cost grows linearly | Verifying entry #50K = walk 50K entries |
| No third-party time anchor | Host operator could rewrite chain; nothing external attests state at time T |

Not biting at ~5K entries. Will bite at 100K. Painful at 1M.

---

## 3. The v2 architecture — three tiers

### 3.1 Tier A: Local Merkle batching

Agents write events to a session buffer. Every N events OR T seconds, the
buffer seals into a Merkle tree and commits as a single chain block.

```
┌────────────────────────────────────────────────────────────────┐
│  Agent session: maker-h on task hive-foundation-w1            │
│  buffer = [event_1...event_4]                                  │
│        ┌──────── merkle tree ─────────┐                       │
│             H(H1,H2)    H(H3,H4)                              │
│                  │           │                                 │
│                  └─── ROOT ──┘                                 │
│                       │                                        │
│  Chain block:  prev_hash + merkle_root + agent_sig + ts       │
└────────────────────────────────────────────────────────────────┘
```

Block schema:

```json
{
  "block_index": 4217,
  "ts": "2026-05-23T14:30:00Z",
  "prev_hash": "sha256(block_4216)",
  "merkle_root": "sha256(top of session merkle tree)",
  "leaf_count": 247,
  "agent_id": "maker-h",
  "agent_sig": "ed25519(prev_hash || merkle_root || leaf_count || ts)",
  "payload_ref": "forensics/sessions/2026-05-23/maker-h-task42.jsonl",
  "shard": "hive-foundation-w1"
}
```

Per-event sig cost drops "1 per event" → "1 per session block." At 247
events per block, ~250× reduction in signature work.

### 3.2 Tier B: Sidecar shards per investigation

One shard per mission + a master index that anchors all shards.

```
                    ┌──────────────────────────┐
                    │   MASTER INDEX CHAIN     │
                    │ forensics/coc-master.jsonl│
                    │                          │
                    │ shard_anchor:            │
                    │   shard="mission-A"      │
                    │   head_block_hash        │
                    │   block_index: 1042      │
                    │   notary_sig             │
                    └──────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
        ┌────────────┐ ┌────────────┐ ┌────────────┐
        │ mission-A  │ │ mission-B  │ │ defense    │
        │ shard      │ │ shard      │ │ shard      │
        └────────────┘ └────────────┘ └────────────┘
```

Each shard publishes head hash to master every N blocks OR T seconds.
Audit win: walk only shard in scope, not all entries. Concurrency win:
parallel writers don't fight for chain head.

### 3.3 Tier C: Sigstore Rekor anchoring

Master head hash submitted to `rekor.sigstore.dev` on schedule:
- **Hourly** (default) — third-party timestamp every hour
- **Daily** (minimum)

Submission is a Sigstore `intoto` attestation:

```bash
MASTER_HEAD=$(jq -r '.entry_hash' forensics/coc-master.jsonl | tail -1)

# Sign — Phase 1 uses OIDC keyless (no key custody)
cosign sign-blob \
    --output-signature anchor.sig \
    --output-certificate anchor.cert \
    --bundle anchor.bundle \
    forensics/coc-master.jsonl

# Upload to Rekor public log
rekor-cli upload \
    --rekor_server https://rekor.sigstore.dev \
    --type intoto \
    --signature anchor.sig \
    --public-key anchor.cert \
    --artifact forensics/coc-master.jsonl

# Returns: Rekor log index, Signed Entry Timestamp (SET), inclusion proof
```

The Rekor entry includes our hash + our sig + Rekor's own sig (SET) +
Trillian inclusion proof. All recorded back in `coc-master.jsonl`:

```json
{
  "ts": "2026-05-23T15:00:00Z",
  "operation": "rekor_anchor",
  "master_head_hash": "sha256:abc...",
  "rekor_log_index": 142849721,
  "rekor_set": "<base64 signed entry timestamp>",
  "rekor_inclusion_proof": "<base64 proof>",
  "rekor_uuid": "24296fb24b8ad77a..."
}
```

Third-party verification (offline, 10 years from now):

```bash
rekor-cli verify \
    --uuid <rekor_uuid> \
    --signature anchor.sig \
    --public-key anchor.cert \
    --artifact master_head_hash
# → VALID + timestamp Rekor recorded the entry
```

---

## 4. Genesis backward-compat (the migration contract)

**Backward compatibility from genesis. No flag-day cutover. Old chain
remains valid throughout.**

The mechanism: a **v2 genesis block** written as the FIRST block of the new
master chain at migration:

```json
{
  "block_index": 0,
  "ts": "<migration timestamp>",
  "kind": "genesis",
  "prev_hash": null,
  "legacy_chain_anchor": {
    "path": "forensics/coc.jsonl",
    "final_entry_index": 4892,
    "final_entry_hash": "sha256(last legacy entry)",
    "entries_count": 4893,
    "merkle_root_of_legacy": "sha256(merkle tree built from ALL legacy entries)"
  },
  "v2_design_doc": "00-Publications/FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md",
  "v2_design_doc_hash": "sha256(this document at time of genesis)",
  "operator_sig": "<sig over all above by goodoleusa's key>"
}
```

**What this gives us:**

1. Legacy `coc.jsonl` is **encapsulated** by v2. v2 verification automatically
   validates legacy too (compare `merkle_root_of_legacy` against legacy file).
2. Walking the new chain backward eventually hits genesis; legacy chain
   pulled to extend audit back to origin.
3. Legacy `coc.jsonl` is never rewritten — read-only from v2 genesis on.
4. Tools that only understand the old format keep working — read `coc.jsonl`
   as before. Tools that understand v2 see genesis, pull legacy reference,
   present unified history.
5. The genesis block itself is anchored to Rekor as the FIRST anchor —
   the very act of switching to v2 is timestamped by a third party.

### Concrete migration ordering

```
   Day -∞ to Day 0:    coc.jsonl is THE chain
       Day 0:          v2 genesis block written + Rekor-anchored
                       coc.jsonl is sealed (read-only from here)
       Day 0+:         v2 shard chains start receiving new events
                       Master index aggregates shards
                       Hourly Rekor anchors begin
                       Legacy coc.jsonl reference remains in every audit
```

**No event is ever in both chains.** First v2 block's
`prev_hash = legacy_final_hash` ensures single continuous lineage.

---

## 5. Verification flows

### 5.1 Light-client (the common case)

```
1. Fetch master anchor for shard:
   GET /master/anchors/mission-A → {head_block: 1042, head_hash: 0xabc}

2. Fetch block containing event #5000:
   GET /shard/mission-A/block/847 → {merkle_root, agent_sig, payload_ref}

3. Fetch Merkle proof for event #5000 in block 847:
   GET /shard/mission-A/block/847/proof?leaf=5000 → [sibling_hashes...]

4. Locally verify:
   a. Reconstruct merkle_root from event #5000 hash + proof siblings
   b. Compare to block.merkle_root → MATCH
   c. Verify agent_sig over block content → VALID
   d. Verify block links forward to master anchor → CHAINED
   e. Verify master anchor's Rekor entry → REKOR-CONFIRMED at time T

Total data: ~20 hashes + 2 small JSON docs ≈ 5KB at N=1M.
```

### 5.2 Full audit

1. Pull master index (small — one entry per shard checkpoint)
2. Pull each shard's full block chain (medium)
3. Pull payloads ONLY for events in audit scope
4. Verify each block's merkle_root locally
5. Verify master chain links to latest Rekor anchor
6. Pull genesis block + verify legacy chain anchor → full history confirmed

### 5.3 Recovery from host loss

```
1. From any preserved copy, find latest Rekor log index for our anchor type.
2. Query rekor.sigstore.dev for that entry — get master head hash with
   Rekor's signed timestamp.
3. Restore master + shards + legacy from any backup; verify against
   Rekor-attested values.
4. Anything written between last anchor and host loss is GONE — everything
   up to the anchor is provably intact.
5. Resume v2 writes from last anchor.
```

Dramatically better than today (corrupted `coc.jsonl` = unrecoverable).

---

## 6. Threat model

| Threat | Today | After v2 + Rekor |
|---|---|---|
| Agent key compromise | Future entries faked | Same — past blocks sealed by original sig |
| Host wipe / data loss | Unrecoverable | Recoverable to last Rekor anchor |
| Single-event tampering | Detectable on full chain walk | Detectable via O(log N) Merkle proof |
| Mass rewrite of chain | Detectable iff someone retains prior copy | **Detectable via Rekor — public log doesn't lie** |
| Notary key compromise | N/A | Future anchors faked; past anchors immutable (Rekor doesn't accept rewrites) |
| Censorship of shard | N/A | Master index makes omission detectable |
| Operator collusion + Rekor compromise | N/A | Linux Foundation + Sigstore community + Trillian would need to cooperate — practically impossible |

Biggest gain: **mass rewrite no longer has plausible deniability.** Today a
determined operator could backdate the chain. After Rekor anchoring, the
public transparency log attests "swarmy's chain at time T had master head
X" — rewriting requires also rewriting Rekor's Merkle tree, which is
publicly verifiable and would be detected the instant anyone re-fetched
the same log index.

---

## 7. Phase plan (now adopted)

### Phase 1 (week 1): Shadow writing + genesis prep
- Shadow writer emits to BOTH legacy `coc.jsonl` AND new shard files
- Build master index lazily from shard heads
- No Rekor yet
- Legacy chain stays authoritative; new chain is read-only sanity check
- Draft v2 genesis block (operator reviews)
- **Zero risk to current operations**

**Exit criterion:** 1 week of shadow writing with zero hash mismatches
between the two chains' encoding of the same events.

### Phase 2 (week 2-3): Merkle batching writes
- Switch new events to session-buffer batching
- ed25519 sig per-block (not per-event)
- Legacy chain continues receiving events too (double-writing through
  Phase 2; cutover at end of Phase 2)

**Exit criterion:** All MCP tools verified writing correctly; no perf
regression on hot loops.

### Phase 3 (week 4): Rekor pinning + genesis
- v2 genesis block written (with operator sig) — seals legacy chain
- Legacy `coc.jsonl` becomes read-only
- Hourly cron submits master head to Rekor via `rekor-cli`
- Anchor entries recorded back in master with UUID + SET + inclusion proof
- First public anchor lands

**Exit criterion:** 7 consecutive successful Rekor anchors; verification
tooling tested against new architecture.

### Phase 4 (month 2): Legacy archival
- All new audits use v2 chain
- Legacy chain remains queryable but read-only

### Phase 5 (month 3+): Hardening
- Notary key rotation policy (graduate from OIDC ephemeral)
- Cold storage for long-lived notary key
- Multi-notary signing for Rekor anchor (overkill until Phase 5)
- Compaction policy for old payloads

---

## 8. What we explicitly skip

| Technique | Skip because |
|---|---|
| Full blockchain (L1/L2) | Rekor gives timestamping without consensus tax or wallet custody |
| DIDs / Verifiable Credentials | We trust the swarmy key registry; adds moving pieces without identity gain |
| BFT consensus for anchoring | One Rekor entry suffices; future multi-notary via threshold ed25519, not Tendermint |
| Zero-knowledge group sigs (Semaphore) | Don't need agent anonymity. Attribution IS the property we want |
| Homomorphic encryption / MPC | Forensic data is meant to be inspectable. Hiding from auditors defeats the purpose |
| Verkle trees | Plain Merkle plenty for our N << 10M per shard |
| RSA accumulators | Same — Merkle sufficient |
| Custom transparency log | Rekor exists, free, mature. Don't reinvent it |

---

## 9. Implementation pointers

### Code locations

```
TODAY:
  scripts/1g_coc_core.py                   ← legacy writer (kept untouched in Phase 1)
  deploy/mcp-server/server.py              ← _append_coc_entry() helper
  .openhands/hooks/                        ← promotion hooks

PHASE 1 (shadow writing):
  scripts/2x_coc_v2_writer.py              ← shadow writer
  scripts/2x_coc_v2_master.py              ← master index manager
  scripts/2x_coc_v2_shard.py               ← per-shard chain manager

PHASE 3 (genesis + Rekor):
  scripts/3x_coc_v2_rekor_anchor.py        ← hourly cron — Rekor submission
  scripts/3x_coc_v2_genesis_writer.py      ← one-shot — v2 genesis block
  deploy/scripts/cron-rekor-anchor.sh      ← cron wrapper

NEW MCP tools (read-only verification):
  swarmy_coc_v2_block_get      verb-style read of a specific shard block
  swarmy_coc_v2_proof_get      Merkle proof for a leaf in a block
  swarmy_coc_v2_rekor_verify   verify a Rekor anchor offline + show timestamp
  swarmy_coc_v2_legacy_link    show genesis block + walk back into legacy
```

### Tech stack

- **Language:** Python (canonical). Hot loops to Rust if perf demands.
- **Hashing:** SHA-256 (already used)
- **Signatures:** ed25519 via `cryptography` (already used)
- **Merkle library:** `pymerkle` OR hand-rolled (~50 LOC). Prefer hand-rolled
  for explicit control.
- **Rekor client:** `sigstore-python` (OIDC + signing + Rekor in one) OR
  shell out to `cosign` + `rekor-cli` for Phase 1 simplicity
- **Storage:** keep JSONL (familiar). Payloads in JSONL too.
- **No IPFS dependency in Phase 1.** Rekor is sufficient.

### Cron schedule (Phase 3+)

```
# Hourly Rekor anchor — master head to rekor.sigstore.dev
0 * * * * /opt/swarmy/deploy/scripts/cron-rekor-anchor.sh >> /var/log/rekor-anchor.log 2>&1

# Daily Rekor inclusion-proof refresh — caches latest proof for offline use
0 4 * * * /opt/swarmy/deploy/scripts/cron-rekor-refresh-proofs.sh >> /var/log/rekor-refresh.log 2>&1
```

---

## 10. The next concrete step

**Phase 1 kickoff** — see companion doc:
[`FORENSIC-COC-V2-PHASE-1-KICKOFF.md`](./FORENSIC-COC-V2-PHASE-1-KICKOFF.md)

Summary: 2-3 days of focused work to build shadow-writer + shard manager.
Hot path doesn't change yet — legacy stays authoritative through Phase 2.

---

## 11. Open questions (decide as we go)

These don't block Phase 1 but will need answers by Phase 3:

1. **Rekor identity for OIDC keyless signing.** Operator's GitHub identity?
   Dedicated org-owned identity? Sigstore supports both.
2. **Long-lived notary key adoption timing.** OIDC ephemeral works
   indefinitely; graduating removes OIDC dependency but adds custody
   complexity. Phase 4 or later.
3. **Compaction policy.** When (if ever) do we delete raw event payloads
   not audit-flagged? Chain skeleton stays forever.
4. **Multi-shard sharding strategy.** One per mission is start. Could
   also shard by date / agent / sensitivity class. Pick once we have
   access-pattern data.
5. **Forensic disclosure protocol.** External auditors need a tar of
   master + shards + Rekor proofs + verifier CLI. Bundle script TBD.

---

## 12. Why this isn't crypto-bro nonsense (and isn't blockchain bullshit either)

A skeptical reader might say: "We don't need any of this. Just back up
`coc.jsonl` nightly."

Honest counter:
- Backups protect against accidental loss but **not against the operator
  being adversarial**. Forensic systems are built to constrain the host
  operator's ability to rewrite history. Backups don't do this.
- A Rekor anchor costs $0 and gives a property no backup can: **a third
  party attests state existed at time T**. The transparency log is
  publicly inspectable; rewriting is detectable.
- Merkle + sidecar restructure isn't blockchain-cult — it's the right
  data structure for "audit a needle in a 1M-event haystack." Same
  tooling Git, Certificate Transparency, the entire software supply chain
  ecosystem uses.

We also explicitly chose **NOT** to use blockchain:
- No L1 / L2 anchor
- No wallets, gas, mining, validators
- No tokens, no DAO, no governance
- No "decentralized" theater

Just a Merkle log + a free, mature, publicly-hosted transparency service
that exists to solve exactly this problem.

---

## Appendix A: Living document policy

This vault copy is the **source of truth.** The repo copy at
`docs/whitepapers/forensic-coc-merkle-rollup-sidecars.md` is a snapshot;
this vault copy is the working copy. Updates land here as decisions firm
up. Major versions get a changelog entry below.

This is a publishable forensic document — assume external auditors may
read it. Be honest about gaps, deferred decisions, and open questions.

### Changelog

- **2026-05-23** — Initial draft. Three-tier proposal (Merkle batch +
  sidecar shards + L2 anchor). Operator decision matrix at end.
- **2026-05-24** — Operator decisions locked:
  - Forensic auditability = hard requirement
  - Public anchor = **Sigstore Rekor** (not L2)
  - Rollout = backward-compat from genesis
  - Rewrote Tier C to use Rekor. Added Section 4 (genesis backward-compat).
  - Added Section 1 (Why Rekor over L2). Renumbered sections.
  - Status: "Draft — proposal" → "ACTIVE — adopted, in implementation".
  - Relocated to vault `00-Publications/` as living source of truth.
  - Added companion Phase 1 kickoff doc.


<!-- crystallize:braid-begin -->
# CRYSTALLIZED 2026-06-04

> 1 doc(s) braided in; sources archived to `_archive-2026-06-04/`. Net-new + conflicts preserved below.

<!-- braid: preamble from FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md -->
---
status: ACTIVE — adopted, in implementation
title: Forensic COC v2 — Merkle Rollups + Sigstore Rekor Anchoring
authors: [swarmy, goodoleusa]
created: 2026-05-23
last_updated: 2026-05-24
scope: swarmy's forensics/coc.jsonl — speed, accuracy, third-party time attestation
operator_decisions:
  forensic_auditability: HARD REQUIREMENT (no equivocation)
  public_anchor: Sigstore Rekor (NOT L2 / blockchain)
  rollout: backward-compat from genesis — old chain remains valid throughout
status_per_phase:
  phase_1_shadow_writing: PROPOSED — awaiting greenlight
  phase_2_merkle_batching: not started
  phase_3_rekor_pinning: not started
  phase_4_old_chain_archival: not started
tags: [forensics, whitepaper, architecture, sigstore, rekor, merkle, transparency-log]
companion_docs:
  - 80-Publications/FORENSIC-COC-V2-PHASE-1-KICKOFF.md (implementation plan for shadow-writer week 1)
---


<!-- BRAID-CONFLICT: h:4-genesis-backward-compat-the-migration-contract from FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md differs from canonical — human review needed -->
## 4. Genesis backward-compat (the migration contract)

**Backward compatibility from genesis. No flag-day cutover. Old chain
remains valid throughout.**

The mechanism: a **v2 genesis block** written as the FIRST block of the new
master chain at migration:

```json
{
  "block_index": 0,
  "ts": "<migration timestamp>",
  "kind": "genesis",
  "prev_hash": null,
  "legacy_chain_anchor": {
    "path": "forensics/coc.jsonl",
    "final_entry_index": 4892,
    "final_entry_hash": "sha256(last legacy entry)",
    "entries_count": 4893,
    "merkle_root_of_legacy": "sha256(merkle tree built from ALL legacy entries)"
  },
  "v2_design_doc": "80-Publications/FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md",
  "v2_design_doc_hash": "sha256(this document at time of genesis)",
  "operator_sig": "<sig over all above by goodoleusa's key>"
}
```

**What this gives us:**

1. Legacy `coc.jsonl` is **encapsulated** by v2. v2 verification automatically
   validates legacy too (compare `merkle_root_of_legacy` against legacy file).
2. Walking the new chain backward eventually hits genesis; legacy chain
   pulled to extend audit back to origin.
3. Legacy `coc.jsonl` is never rewritten — read-only from v2 genesis on.
4. Tools that only understand the old format keep working — read `coc.jsonl`
   as before. Tools that understand v2 see genesis, pull legacy reference,
   present unified history.
5. The genesis block itself is anchored to Rekor as the FIRST anchor —
   the very act of switching to v2 is timestamped by a third party.


<!-- BRAID-CONFLICT: h:cron-schedule-phase-3 from FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md differs from canonical — human review needed -->
### Cron schedule (Phase 3+)

```
# Hourly Rekor anchor — master head to rekor.sigstore.dev
0 * * * * /opt/faerie/deploy/scripts/cron-rekor-anchor.sh >> /var/log/rekor-anchor.log 2>&1

# Daily Rekor inclusion-proof refresh — caches latest proof for offline use
0 4 * * * /opt/faerie/deploy/scripts/cron-rekor-refresh-proofs.sh >> /var/log/rekor-refresh.log 2>&1
```

---


<!-- BRAID-CONFLICT: h:changelog from FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR.md differs from canonical — human review needed -->
### Changelog

- **2026-05-23** — Initial draft. Three-tier proposal (Merkle batch +
  sidecar shards + L2 anchor). Operator decision matrix at end.
- **2026-05-24** — Operator decisions locked:
  - Forensic auditability = hard requirement
  - Public anchor = **Sigstore Rekor** (not L2)
  - Rollout = backward-compat from genesis
  - Rewrote Tier C to use Rekor. Added Section 4 (genesis backward-compat).
  - Added Section 1 (Why Rekor over L2). Renumbered sections.
  - Status: "Draft — proposal" → "ACTIVE — adopted, in implementation".
  - Relocated to vault `80-Publications/` as living source of truth.
  - Added companion Phase 1 kickoff doc.

<!-- crystallize:braid-end -->
