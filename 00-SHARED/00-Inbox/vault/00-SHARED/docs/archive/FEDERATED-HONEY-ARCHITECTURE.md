---
status: final
author: knowledge-synthesizer
ts: 2026-04-06T12:00:00Z
type: architecture-blueprint
---

# Federated Honey Architecture -- Multi-Pod Collaborative Research

## Executive Summary

The faerie system currently operates as a solo-researcher orchestration platform: one
human, multiple AI agents, a three-tier memory hierarchy (scratch -> NECTAR -> HONEY),
and a sprint queue. HONEY.md -- crystallized wisdom -- is the densest, most valuable
artifact in the system. It is loaded at every session start and shapes all agent behavior.

This document proposes extending HONEY from a local crystallized memory into a
**portable knowledge currency** that flows between autonomous research pods. Each pod
operates its own faerie instance with its own HONEY, NECTAR, agents, and queue. Pods
share knowledge through a three-layer protocol: internal crystallization (current
model), HONEY export (versioned, signed, IPFS-pinned), and cross-pod references
(hash-verified, traceable to forensic records).

The core insight: HONEY entries already have the properties needed for federation --
stable IDs, confidence scores, TTLs, and categories. What is missing is versioning,
signing, export formatting, and a cross-pod reference protocol.

---

## Part 1: Current Equilibrium Analysis

### Energy Flow (Task Generation -> Completion -> Crystallization)

The current system generates knowledge through a well-designed pipeline:

```
Task origin (human 10% / agent 70% / auto 20%)
  |
  v
Sprint queue (65 tasks, 4 active, 0 completed -- accumulating)
  |  <- /run assigns to typed agent
  v
Agent execution (writes manifests + scratch MEM blocks)
  |                    |
  v                    v
Parent reads       Memory-keeper promotes scratch -> NECTAR
manifest           (append-only, unbounded, ~6500 tokens)
  |                    |
  v                    v
Next wave          Human /crystallize -> HONEY
                   (95% full at 4740/5000 tokens)
```

**Key metrics:**
- 65 tasks in queue, 0 ever formally completed or archived
- HONEY at 95% capacity -- cannot absorb new knowledge without compression
- REVIEW-INBOX regrew from 50 to 547 lines in 9 days after last siphon
- 30 agent cards, average ~1030 tokens vs 800 token budget
- Crystallization ratio: HONEY/NECTAR = 0.73 (high density, but at ceiling)

### Bottleneck Identification

| Bottleneck | Impact | Root Cause |
|------------|--------|------------|
| No task completion state | Queue grows monotonically (72K file) | Missing lifecycle: queued -> in_progress -> completed -> archived |
| HONEY at budget ceiling | New knowledge cannot be absorbed | pref_bridge entries need compression; TTL expiry not enforced |
| REVIEW-INBOX regrowth | Human review queue overwhelms | Siphon is manual, no automation to promote/archive |
| Agent cards overbudget | T1 context cost higher than planned | Cards grew during training without compression pass |
| Crystallization is human-triggered only | Knowledge accumulates without integration | Gauntlet criteria not tracked; no dashboard showing candidates |

### Pressure Points

These must be resolved before federation adds complexity:

1. **Task lifecycle closure** -- add completed/archived states + automatic GC
2. **HONEY compression** -- free 20-30% budget headroom via pref_bridge merge
3. **REVIEW-INBOX automation** -- auto-categorize + auto-promote items meeting criteria
4. **Agent card audit** -- bring all cards under 800 token budget
5. **Gauntlet tracking** -- surface which NECTAR entries are crystallization candidates

---

## Part 2: Federated Pod Model

### Pod Structure

A research pod is an autonomous unit:

```
POD = {
  repo:           git repository (code + pipeline)
  faerie:         CLI orchestration instance
  honey:          crystallized knowledge (local authority)
  nectar:         append-only findings log
  queue:          sprint task list
  agents:         typed specialist cards (20+ types)
  vault:          Obsidian-synced human interface
  forensic_store: hash-chained COC logs
}
```

Each pod is fully self-contained. It can operate indefinitely without any other pod.
Federation is additive -- it makes pods more effective, not dependent.

### Example Research Network

```
Pod A: DOGE/Infrastructure Investigation (cybertemplate)
  HONEY: credential misuse patterns, Packetware forensics, cert rotation methods
  Strength: network forensics, infrastructure analysis, statistical validation

Pod B: Supply-Chain Risk Analysis
  HONEY: dependency graph patterns, build system vulnerabilities, SolarWinds parallels
  Strength: software supply chain, build reproducibility, code provenance

Pod C: Regulatory Capture Investigation
  HONEY: revolving door patterns, lobbying disclosure gaps, agency capture indicators
  Strength: financial analysis, regulatory filings, organizational network mapping
```

Each pod's HONEY represents crystallized domain expertise. Pod A's knowledge about
cert rotation anomalies could inform Pod B's analysis of build infrastructure. Pod C's
findings about agency personnel could contextualize Pod A's DOGE actor identification.

### HONEY as Knowledge Currency

In economics, currency has properties: fungible, portable, verifiable, scarce (in the
sense of being hard to counterfeit). HONEY entries have analogous properties:

| Currency Property | HONEY Equivalent |
|-------------------|------------------|
| **Portable** | Text format, small size (< 5K tokens per pod) |
| **Verifiable** | SHA-256 hash, source traceability to NECTAR + forensic COC |
| **Scarce** | Gauntlet (3+ sessions, multi-agent validation, human review, proven impact) |
| **Denominated** | Confidence score (0.0-1.0), TTL, category |
| **Fungible** | Standardized format: `[id | type | ttl | confidence] entry` |

HONEY is hard to produce (the gauntlet is rigorous) and easy to verify (every entry
traces to forensic records). These are exactly the properties needed for cross-pod
knowledge exchange.

---

## Part 3: Three-Layer Reference Architecture

### Layer 1: Pod-Internal (Current Model -- No Changes)

```
Task -> Agent -> scratch MEM blocks
                      |
                  memory-keeper
                      |
                  NECTAR (append-only)
                      |
                  human /crystallize
                      |
                  HONEY (crystallized, internal authority)
```

This layer is stable and well-designed. The only pre-federation improvements needed
are the bottleneck fixes from Part 1 (task lifecycle, HONEY compression, gauntlet
tracking).

### Layer 2: HONEY Export (New)

Each pod publishes its HONEY as a versioned, signed export:

```
HONEY.md (internal, mutable)
  |
  v
HONEY-EXPORT.jsonl (versioned, immutable per version, signed)
  |
  v
honey-manifest.json (hash of HONEY-EXPORT + metadata)
  |
  v
IPFS pin + OpenTimestamp (immutable, verifiable, dated)
```

#### HONEY-EXPORT.jsonl Format

```jsonl
{"honey_version": 3, "pod_id": "pod-a-doge", "ts": "2026-04-06T12:00:00Z", "prev_version_hash": "abc123..."}
{"entry_id": "pod-a:sys00001", "type": "principle", "ttl": "permanent", "confidence": 1.0, "text": "ONE PATH ONE TRUTH...", "nectar_refs": ["nectar:2026-03-15:entry-42"], "forensic_ref": "coc:session-abc:entry-17"}
{"entry_id": "pod-a:mth00024", "type": "method", "ttl": "1yr", "confidence": 0.97, "text": "Cert verification: live crt.sh SHA256...", "nectar_refs": ["nectar:2026-03-20:entry-88"], "forensic_ref": "coc:session-def:entry-5"}
```

Each entry carries:
- **entry_id**: globally unique (`pod-id:local-id`)
- **nectar_refs**: which NECTAR entries this was crystallized from
- **forensic_ref**: COC log entry establishing provenance
- **confidence**: the pod's confidence in this knowledge
- **ttl**: how long the pod believes this knowledge remains valid

#### honey-manifest.json

```json
{
  "pod_id": "pod-a-doge",
  "honey_version": 3,
  "entry_count": 42,
  "export_hash": "sha256:def456...",
  "prev_version_hash": "sha256:abc123...",
  "signed_by": "ed25519:pod-a-public-key",
  "signature": "base64:...",
  "ipfs_cid": "Qm...",
  "opentimestamp": "ots:...",
  "exported_at": "2026-04-06T12:00:00Z"
}
```

#### Export Trigger

HONEY export runs when:
1. Human invokes `/crystallize` and new entries are added to HONEY
2. Manual `/honey-export` command
3. Sprint completion (at `/handoff` when sprint boundary is crossed)

Export is NOT automatic on every HONEY write -- it is a deliberate publication act.

### Layer 3: Cross-Pod References (New)

#### Reference Syntax

```
honey:pod-a:mth00024    -- reference to Pod A's method entry
honey:pod-b:hyp00003    -- reference to Pod B's hypothesis
honey:pod-c:fnd00012    -- reference to Pod C's finding
```

#### Resolution Protocol

When an agent encounters a cross-pod reference:

```
1. Parse reference: honey:{pod_id}:{entry_id}

2. Check local cache:
   ~/.claude/memory/federated/{pod_id}/HONEY-EXPORT.jsonl
   If cached version matches known latest -> use cached entry

3. If not cached or stale:
   Fetch from IPFS: resolve pod_id -> CID via pod-registry.json
   Verify hash: sha256(fetched) == manifest.export_hash
   Verify signature: ed25519_verify(manifest, pod_public_key)
   Cache locally

4. Extract entry by entry_id from HONEY-EXPORT.jsonl

5. Inject into agent context with provenance tag:
   [FEDERATED from pod-a v3, confidence 0.97, verified 2026-04-06]
   {entry text}
```

#### Trust Model

Pods verify each other's HONEY through:

1. **Cryptographic verification**: HONEY-EXPORT is signed by the pod's ed25519 key.
   Public keys are exchanged out-of-band (pod-registry.json, manually curated).

2. **Hash chain verification**: Each HONEY-EXPORT version links to its predecessor
   via `prev_version_hash`. Tampering with history is detectable.

3. **IPFS immutability**: Once pinned, the CID is a permanent reference. The content
   at that CID can never change.

4. **OpenTimestamp**: Proves the export existed at a specific time. Prevents backdating.

5. **Forensic traceability**: Each HONEY entry has a `forensic_ref` that traces back
   to the COC log. A skeptical pod can request the NECTAR entries and forensic records
   that support a HONEY entry (trust-but-verify).

Pods do NOT need to trust each other's agents or methods. They trust the *process*:
the gauntlet, the forensic COC, the human review, the hash chain. A pod that publishes
false HONEY will have a detectable gap in its forensic trail.

---

## Part 4: Implementation Roadmap (Phased)

### Phase 1: HONEY Entry Versioning + Export Format (1-2 sessions)

**Goal:** Every HONEY entry gets a stable ID. Export format defined and tested.

Tasks:
- [ ] Add `entry_id` to every HONEY.md entry (already partially there: `sys00001`, `mth00024`, etc.)
- [ ] Standardize ID format: `{pod_id}:{category}{number}` (e.g., `pod-a:sys00001`)
- [ ] Write `honey_export.py`: reads HONEY.md, outputs HONEY-EXPORT.jsonl + honey-manifest.json
- [ ] Sign manifest with pod ed25519 key (reuse `gen-agent-key.sh` infrastructure)
- [ ] Write `honey_import.py`: reads HONEY-EXPORT.jsonl, caches in `~/.claude/memory/federated/`
- [ ] Add `nectar_refs` field: link each HONEY entry to its source NECTAR entries

**Deliverable:** A single pod can export and reimport its own HONEY. Round-trip verified.

### Phase 2: Cross-Pod Task Routing -- Manual Pilot (2-3 sessions)

**Goal:** Two pods can share HONEY and route tasks to each other.

Tasks:
- [ ] Create `pod-registry.json`: maps pod_id -> public key, IPFS gateway, contact
- [ ] Build `/honey-fetch {pod_id}`: fetches and verifies remote HONEY-EXPORT
- [ ] Add `route:{pod_id}` tag support in sprint-queue.json
- [ ] Build `cross_pod_router.py`: watches for routed tasks, writes to shared location
- [ ] Pilot: Pod A discovers gap, routes task to Pod B, Pod B executes, returns result

**Deliverable:** Two faerie instances can share tasks via vault sync or direct file exchange.

### Phase 3: Automated Cross-Pod Agent Assignment (3-5 sessions)

**Goal:** Agents in one pod can reference another pod's HONEY in their context bundles.

Tasks:
- [ ] Modify faerie context bundle builder: include relevant federated HONEY entries
- [ ] Add `federated_context` field to task JSON: lists which remote HONEY entries are relevant
- [ ] Build `relevance_scorer.py`: given a task description, score which remote HONEY entries help
- [ ] IPFS pinning automation: `honey_publish.py` pins HONEY-EXPORT to Pinata + local node
- [ ] OpenTimestamp integration: timestamp each HONEY-EXPORT version

**Deliverable:** Agents receive cross-pod knowledge automatically when relevant to their task.

### Phase 4: Federated Learning (5-10 sessions, ongoing)

**Goal:** Agent improvements in one pod benefit other pods.

Tasks:
- [ ] Agent card export: similar to HONEY export but for agent training sections
- [ ] Cross-pod technique sharing: `cat=TECHNIQUE` entries flow between pods
- [ ] Federated benchmark: pods contribute anonymized benchmark results
- [ ] Deployment score aggregation: a pod's agent scores are visible to other pods
- [ ] Technique marketplace: pods can "import" techniques that improved agent performance elsewhere

**Deliverable:** Agent training compounds across the network, not just within one pod.

---

## Part 5: Trust and Incentives

### Trust Architecture

```
VERIFICATION CHAIN:
  Remote HONEY entry
    |-> signed by pod's ed25519 key (authenticity)
    |-> hash in honey-manifest.json (integrity)
    |-> IPFS CID is content-addressed (immutability)
    |-> OpenTimestamp proves existence at time T (non-repudiation)
    |-> forensic_ref traces to COC log (provenance)
    |-> nectar_refs trace to raw findings (evidence)
    |-> gauntlet criteria documented (process)
```

A consuming pod can verify at any level of depth:
1. **Shallow trust**: verify signature + hash. "Pod A signed this; it hasn't been tampered with."
2. **Medium trust**: also verify IPFS CID + timestamp. "This existed at time T and hasn't changed."
3. **Deep trust**: request NECTAR entries + COC logs. "I can see the evidence chain that produced this."

### Attack Model

| Attack | Detection | Mitigation |
|--------|-----------|------------|
| Pod publishes false HONEY | Forensic trail is thin or missing | Deep trust verification; request NECTAR + COC |
| Pod backdates entries | OpenTimestamp detects | Timestamps are Bitcoin-anchored; unforgeable |
| Pod modifies historical HONEY | Hash chain breaks | prev_version_hash links all versions; any break is visible |
| Compromised pod key | Other pods detect when new exports fail verification | Key rotation protocol; out-of-band key verification |
| Sybil (fake pods) | Pod registry is manually curated | Human gatekeeping on pod-registry.json |

### Incentive Structure

**Why share?**
1. **Reciprocity**: Pod A shares infrastructure knowledge; Pod B shares regulatory knowledge.
   Both are more effective together than alone.
2. **Reputation**: HONEY quality is verifiable. A pod with consistently accurate, well-sourced
   HONEY becomes a trusted authority. Other pods cite it; its findings gain weight.
3. **Coverage**: No single pod can investigate everything. Federated knowledge extends each
   pod's effective reach without proportional cost.
4. **Court admissibility**: Cross-pod corroboration strengthens evidence. If Pod A and Pod C
   independently find the same pattern, the finding is stronger than either alone.

**Why not free-ride?**
1. **Gauntlet scarcity**: HONEY is hard to produce. A pod that only consumes and never
   publishes gets nothing from federation (it has no HONEY-EXPORT to share).
2. **Stale penalty**: HONEY entries have TTLs. A pod that stops publishing loses relevance
   as its entries expire from other pods' caches.
3. **Reputation cost**: A pod that publishes low-quality HONEY (entries that other pods
   find unreliable) damages its own credibility. The forensic trail makes quality auditable.

### Governance

- **Pod registry**: manually curated JSON file, distributed via signed git commits
- **Dispute resolution**: if Pod A disputes Pod B's HONEY entry, the dispute is logged in
  both pods' NECTAR with cross-references. The human researchers discuss and resolve.
- **Entry challenges**: any pod can publish a `challenge` entry targeting another pod's HONEY.
  Challenges carry evidence and are themselves hash-verified. A challenged entry gets a
  `challenged_by` field in the consuming pod's cache, reducing its effective confidence.

---

## Part 6: Protocol Specifications

### HONEY Entry ID Specification

```
entry_id    := pod_id ":" local_id
pod_id      := [a-z0-9-]+ (max 32 chars, globally unique)
local_id    := category_prefix number
category_prefix := "sys" | "pref" | "mth" | "hyp" | "fnd" | "gap" | "rule"
number      := [0-9]{5}

Examples:
  pod-a-doge:sys00001
  pod-b-supply:mth00015
  pod-c-regcap:fnd00003
```

### Cross-Pod Reference in MEM Blocks

```markdown
<!-- MEM agent=research-analyst ts=2026-04-06T12:00:00Z session=abc123 cat=CONNECTION pri=HIGH av=baseline -->
**[CONNECTION]** Pod A cert rotation pattern matches Pod B build system anomaly

Pod A's honey:pod-a-doge:mth00024 (cert verification method) reveals same rotation
cadence as Pod B's honey:pod-b-supply:fnd00008 (build system cert anomaly). Both show
24h rotation + domain registration alignment. Bayesian confidence: 0.72 (prior: 0.30,
update: 2.4x from independent convergence).

Files: none | Next: route task to Pod B for build-system cert analysis
<!-- /MEM -->
```

### Federated Cache Structure

```
~/.claude/memory/federated/
  pod-registry.json              -- known pods, keys, endpoints
  pod-a-doge/
    HONEY-EXPORT.jsonl           -- cached export
    honey-manifest.json          -- manifest with hash + signature
    fetched_at: 2026-04-06       -- (in manifest)
  pod-b-supply/
    HONEY-EXPORT.jsonl
    honey-manifest.json
```

### Export/Import Scripts

```
Scripts to build:
  ~/.claude/scripts/honey_export.py   -- HONEY.md -> HONEY-EXPORT.jsonl + manifest
  ~/.claude/scripts/honey_import.py   -- HONEY-EXPORT.jsonl -> federated cache
  ~/.claude/scripts/honey_fetch.py    -- IPFS CID -> verify -> cache
  ~/.claude/scripts/honey_publish.py  -- cache -> IPFS pin + OpenTimestamp
  ~/.claude/scripts/honey_resolve.py  -- honey:pod-id:entry-id -> cached text
```

---

## Part 7: Migration Path (Solo -> Federated)

### What Changes for Current Users

**Nothing, unless they opt in.** The federated layer is additive:

| Current Feature | With Federation | Change Required |
|-----------------|-----------------|-----------------|
| HONEY.md (local) | Still authoritative for local pod | Add entry_ids (already mostly there) |
| NECTAR.md | Unchanged | None |
| Agent cards | Can optionally share technique entries | None (sharing is opt-in) |
| Sprint queue | Can optionally accept routed tasks | None (routing is opt-in) |
| /crystallize | Also triggers HONEY-EXPORT if configured | Minor hook addition |
| Vault sync | Also syncs federated cache | Syncthing folder addition |

### Backward Compatibility

A pod that never exports HONEY is indistinguishable from a solo faerie instance.
Federation is a capability, not a requirement. The Phase 1 changes (entry IDs +
export format) improve the solo experience too: better traceability, cleaner HONEY
structure, and hash-verified knowledge provenance even without any remote pods.

### First Federation Pilot

Recommended first federation: connect the cybertemplate investigation pod with the
faerie2 development pod. faerie2 already has system-level HONEY (principles, methods,
architecture). cybertemplate has investigation-specific HONEY. Cross-pollination would
let investigation agents benefit from system improvements, and system development
would benefit from investigation workflow insights.

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Pod** | Autonomous research unit: repo + faerie + HONEY + agents + vault |
| **HONEY** | Crystallized knowledge -- dense, verified, portable |
| **NECTAR** | Raw validated findings -- append-only, unbounded, forensic trail |
| **HONEY-EXPORT** | Published, versioned, signed snapshot of a pod's HONEY |
| **Gauntlet** | Entry criteria for HONEY: recurrence, multi-agent validation, human review, proven impact |
| **Cross-pod reference** | `honey:{pod_id}:{entry_id}` -- link to another pod's crystallized knowledge |
| **Stigmergy** | Coordination through shared environment (filesystem) rather than direct messaging |
| **Forensic COC** | Hash-chained chain-of-custody log establishing provenance of every finding |

## Appendix B: Related Documents

- `FAERIE-EQUILIBRIUM-CURRENT-STATE.md` -- analysis of current system bottlenecks
- `SIGNED-DEAD-RECKONING.md` -- agent key infrastructure (reusable for pod signing)
- `ARCHITECTURE.md` -- faerie2 system architecture
- `~/.claude/rules/memory-routing.md` -- memory topology and write routing
- `~/.claude/rules/agent-lifecycle.md` -- agent startup, execution, and learning protocol
