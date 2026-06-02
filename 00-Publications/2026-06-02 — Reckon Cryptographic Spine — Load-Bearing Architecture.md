---
title: "Reckon's Cryptographic Spine — A Load-Bearing Architecture Report"
type: architecture-narrative
created: 2026-06-02
canonical_tier: { agents: true, humans: true }
tags: [architecture, forensics, cryptography, sigstore, branching, charter-seal, coc, f0]
related:
  - "docs/145-THE-CHARTER-SEAL-CANONICAL.md"
  - "docs/90-THE-IMMUTABLE-LEDGER-CANONICAL.md"
  - "docs/95-SALTED-IDENTITY-CHAIN-CANONICAL.md"
  - "scripts/5e_agent_sign.py"
  - "scripts/0b_path_utils.py"
---

# Reckon's Cryptographic Spine — A Load-Bearing Architecture Report

*How a swarm of agents produces work that is tamper-evident from the first keystroke
to a publicly-anchored, immutable contract — while the orchestrator ("main") does
exactly one thing.*

---

## 0. The thesis (and the north star)

Reckon is an autonomous multi-agent system whose **product is forensic truth**: not
just code or analysis, but *provable* records of who did what, in what order, and
that a human authority accepted it. The whole architecture is bent toward one
constraint — **f(0)**: the orchestrator's burden trends to zero. Agents flow
autonomously; the human/main touches the system as little as physically possible.

The tension this report resolves: **maximum autonomy** (agents act without
supervision) versus **maximum accountability** (every action is attributable and
tamper-evident). Cryptography is how those two are reconciled. The crypto is not a
feature bolted on — it *is* the load-bearing spine. Remove it and the system is a
pile of unverifiable JSON.

---

## 1. The load-bearing parts (what breaks the system if it breaks)

Ranked by blast radius — these are the components where a silent failure corrupts
*everything downstream*:

| Rank | Component | If it fails… |
|---|---|---|
| 1 | **Agent key store** (`forensics/reputation/keys/{agent}.{key,pub}`) | identity collapses — nothing can be attributed; every signature below is meaningless |
| 2 | **The COC hash chain** (`forensics/coc.jsonl`) | the append-only audit trail can be silently rewritten; lineage is lost |
| 3 | **The charter seal** (co-sign rollup → main counter-seal) | "completion" becomes unfalsifiable; partial/fake work can claim canon |
| 4 | **Sigstore Rekor anchor** | records lose their *public* immutable timestamp — tamper-evidence drops from "global" to "local" |
| 5 | **The path authority** (`scripts/0b_path_utils.py`) | hot vs at-rest regimes blur; promotion mis-routes; the date-less/date-keyed contract breaks |
| 6 | **B2 WORM backup** | last line of defense against disk-level tampering is gone |

Notice the shape: **1–4 are cryptographic.** The integrity of the entire system
rests on a small, auditable set of crypto operations. The rest of this report is
those operations and how they interlock.

---

## 2. The cryptographic operations, bottom to top

Each layer consumes the guarantee of the one below it. This is **defense in depth**:
to forge an accepted deliverable, an attacker must break *every* layer simultaneously.

### 2.1 Identity — Ed25519 agent keys
- **Where:** `forensics/reputation/keys/{agent_type}.key` (private, gitignored, `chmod 600`) + `.pub` (committed).
- **What:** every agent role (`diver`, `maker`, `navigator`, … and `opus-main`) has an Ed25519 keypair, provisioned idempotently at session start (`5f_init_reputation.py`).
- **The linking primitive — `agent_version_id`:** `fingerprint()` = `{agent_type}-{sha256(pubkey)[:8]}`. This binds *every* artifact a key produces to that exact key version. Rotate the key → new fingerprint → new identity → visible in filenames. This is how you grep the entire forensic tree by "which key made this."
- **Why load-bearing:** identity is the root of trust. A signature only means something because the public key it verifies against is itself committed and fingerprinted.

### 2.2 Attestation — manifest signing (agent self-report)
- Each agent, on finishing its task atom, writes a **manifest** (`status`, `dashboard_line`, `navigation`, `next_mission_node`, `discovered_work[]`) and **signs it** (`5e_agent_sign.py sign {agent} <manifest>` → `ed25519:<b64>`).
- **Canonicalization matters:** signing is over `json.dumps(body, sort_keys=True, separators=(",",":"))` with the `signed_by` field excluded. Deterministic bytes → reproducible signatures → verifiable by anyone with the `.pub`.
- The manifest's `navigation` record is itself a piece of provenance: `bearing_assigned` (the direction given at spawn) paired with `course_charted[]` (the actual w3w mission-address vector the agent traversed). *"A bearing is a direction; a course is the exact vector."* The signature covers this realized trajectory.

### 2.3 The append-only ledger — the COC hash chain
- **Where:** `forensics/coc.jsonl` — the chain of custody. Append-only, hash-linked: each entry references the prior entry's hash. Git-tracked + mirrored to B2 WORM.
- This is the **timeline**: every promotion, every signature, every state transition lands here. Because entries are hash-linked, you cannot edit history without breaking the chain from that point forward.

### 2.4 The keystone — the charter seal (multi-party hash rollup)
This is the operation built in the 2026-06-02 evolution, and it is the most
intricate. It turns a flat list of "agents who helped" into a **cryptographic proof
of the ordered sequence of work**, sealed by a single authority signature.

```
body_hash      = sha256(charter MINUS .seal)                  ← stable charter identity
co_sig[0].prev = body_hash
co_sig[i].prev = co_sig[i-1].rollup_hash                      ← each links to its predecessor
co_sig[i].sig  = Ed25519_sign(agent_i, body_hash || prev)     ← agent binds itself to its SLOT
co_sig[i].rollup_hash = sha256(prev || canonical(entry_i))    ← the running rollup
merkle_root    = last co_sig.rollup_hash
counter_seal.sig = Ed25519_sign(opus-main, merkle_root || body_hash)   ← MAIN, once
```

**Why this is strong:** because each agent signs over the *previous* rollup hash,
the co-signatures form a chain. Re-ordering them, inserting a fake one, dropping
one, or editing the charter body all change a `prev_hash` somewhere — and
`verify_seal()` fails at that link. So **main's single signature over `merkle_root`
certifies the entire ordered work history at once.** One act; total coverage.

This was validated empirically: a full `cosign(diver) → cosign(maker) →
counterseal(opus-main) → verify` cycle returns `True`; mutating the body or
reordering the co-signatures returns `False`.

**The ritual mapping (the human meaning of the crypto):**
- *L3a co-sign* = each contributing agent's **completion act** ("I did my part; I attest").
- *L3b counter-seal* = **main accepts**. This is **the one thing main is truly responsible for.** Signing over the agents' rollup means "I accept work *these specific agents in this order* attested to." It is simultaneously the acceptance, the seal, and the contract.

### 2.5 Public anchoring — Sigstore Rekor
The seal above is verifiable by anyone holding the public keys — but *when* did it
exist? A local clock can lie. **Sigstore** answers "this existed by time T" with a
**public, append-only transparency log** that no single party controls. See §3.

### 2.6 Immutable backup — B2 WORM
Finally, the canonical tree (`forensics/`) is mirrored to a Backblaze B2 bucket in
**WORM** (write-once-read-many) mode via `rclone copy --immutable` (never `sync` —
local deletes never propagate). This defends against disk-level tampering: even if
someone rewrites local history, the WORM copy stands.

### The relationship, in one line
> **key** signs a **manifest**, whose promotion lands in the **COC chain**; the
> charter gathers agent **co-signatures** into a **merkle rollup**, which **main**
> counter-seals; that seal's root is **Rekor-anchored** for public time, and the
> whole tree is **B2-WORM** backed. Each layer's guarantee is the next layer's input.

---

## 3. Sigstore, explained

Sigstore is the public-transparency backbone. Two halves matter here.

### 3.1 Keyless signing (Fulcio)
Traditional signing needs a long-lived private key on disk — a theft target.
Sigstore's **keyless** flow instead: you authenticate via **OIDC** (e.g. GitHub
Actions' workload identity), and **Fulcio** issues a *short-lived* (≈10-minute)
X.509 signing certificate bound to that identity. You sign, then the cert expires.
There is no durable key to steal. The repo uses this for **container image
signing**: every `v*` release is `cosign`-signed during `mcp-image-publish.yml`, so
anyone can prove a given image was built by *this repo's CI from that exact commit*:

```bash
cosign verify ghcr.io/Persistech/swarmy-mcp-server:vX.Y.Z \
  --certificate-identity-regexp 'https://github.com/Persistech/swarmy' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com'
```

### 3.2 The transparency log (Rekor)
**Rekor** is a public, cryptographically-verifiable, append-only log (a Merkle
tree). When you record a signature there, you get back an **inclusion proof** and a
**log index / UUID** — proof that the entry existed at a globally-witnessed time and
cannot be retroactively removed or altered without detection. Reckon anchors two
things to Rekor (`.github/workflows/sigstore-rekor.yml`):
1. The **COC chain** + manifests (ongoing forensic state).
2. The **charter seal's `merkle_root`** (the new piece). The resulting public link is
   stored *inline* on the charter (`seal.anchor.url`, e.g.
   `https://search.sigstore.dev/?uuid=…`), so the sealed charter is self-describing:
   it carries its own public, immutable timestamp.

**Why both signing *and* Rekor:** the agent/main signatures prove **who**; Rekor
proves **when**, publicly and irrevocably. Together: *this authority accepted this
exact ordered work, no later than this globally-witnessed moment.* That is the
strongest claim a forensic system can make without a trusted third party — because
Rekor *is* the untrusted-but-verifiable third party.

`storage_tier` on each charter enumerates where its proof lives:
`disk_repo`, `obsidian_vault`, `b2_worm`, `sigstore_rekor`, `ipfs`, `arweave`.

---

## 4. Branching, explained

Branches are how the swarm parallelizes *risky or divergent* work without polluting
the shared trunk — and they are deliberately designed to **add zero burden to main**.

### 4.1 What a branch is
An agent (or sub-swarm) can take a **git worktree** isolated from `main` and work
there. The mission graph tracks the topology explicitly:
`branch_fork_edges` (where it diverged), `branch_internal_edges` (work within it),
and `branch_merge_edges` (where it returned).

### 4.2 The heartbeat — a liveness handshake, not a timer
A diverged branch can run for a while. To prove it's alive *and* to forensically
anchor its progress, on **every merkle rollup / Rekor timestamp** it emits a
**heartbeat** back to main:

```json
{ "branch": "...", "merkle_root": "sha256:...", "rekor_anchor": "<uuid>", "ts": "<utc>" }
```

→ appended to `forensics/heartbeats/{branch}.jsonl`, which **main tails passively**
(zero burden). Semantics: *"I'm alive; here is my tamper-evident state at time T."*
It is event-driven (per anchor), never a clock. The branch eventually returns for
its (automated) acceptance.

### 4.3 Why branches need NO special merge protocol (the f(0) payoff)
This is the subtle, important part — and a documented **anti-pattern** to avoid
(`.agents/skills/spawn/SKILL.md`):

A branch merging back to main is **just delivery of already-signed work**:
- the manifests are **agent-signed** (§2.2),
- the outputs are **hashed and referenced**,
- and if the branch completed a charter, the contributing agents have **co-signed**
  it (§2.4),
- while the divergence itself is **heartbeat-anchored** (merkle + Rekor, §4.2).

So nothing crossing the boundary is un-vouched-for. There is **no need for main to
sign the merge** — and adding such a step would be f(0) drift. The COC chain and the
`branch_merge_edges` absorb the merge mechanically. **Main's authority enters
exactly once: the charter counter-seal**, which *is* the acceptance of whatever the
branch returned. The ledger therefore reads:

| Branch merges back with… | Main acts |
|---|---|
| intermediate work (no charter completed) | **0** — self-signed artifacts + heartbeat flow in automatically |
| work that completes a charter | **1** — the counter-seal (which it would do anyway) |

Branching, in other words, is *free* from main's perspective. That is the whole point.

---

## 5. The two regimes the crypto lives in

Crypto operations attach to artifacts, and artifacts live in one of two
deliberately-different regimes (`scripts/0b_path_utils.py` is the single path
authority):

- **HOT — `forensics/ephemeral/{active,next,complete}/`** — *date-less*, partitioned
  by lifecycle state. A 24h boundary is artificial; it fragments a charter's
  stigmergic trail across days. Agents on a hot charter traverse one continuous
  space. Co-signing happens here.
- **AT REST — `forensics/{type}/{YYYY-MM-DD}/`** — grouped by **type and date**:
  greppable, time-ordered, immutable. The **promotion gate** is the boundary
  crossing: a sealed charter (main-counter-signed, Rekor-anchored) is verified, then
  promoted from hot to at-rest canon (symlink + COC entry + vault mirror + B2 WORM).

The gate is where the crypto is *enforced*: nothing promotes to canon unless
`verify_seal()` passes and the counter-seal is `accepted`.

---

## 6. How it all relates — one diagram

```
  Ed25519 agent key ──signs──▶ manifest (navigation: bearing + course)
        │                              │ promoted →
        │                              ▼
        │                        COC hash chain (append-only)
        ▼
  charter co-signatures (each signs body_hash‖prev) ──rollup──▶ merkle_root
        │                                                           │
        │                                          opus-main counter-signs ◀── MAIN's 1 act
        ▼                                                           ▼
   sealed charter ──── Rekor anchor (public, immutable time) ──── promote → {type}/{date}/
        │                                                           │
        └──────────────────── B2 WORM (immutable backup) ──────────┘

  branches: fork → heartbeat(merkle+Rekor) → merge (= delivery of signed work, 0 main acts)
```

Every arrow is a cryptographic dependency. The system is autonomous because agents
self-attest; it is accountable because those attestations chain into a single
authority signature that is publicly anchored. **Main does one thing. The math does
the rest.**

---

*Companion canonical docs: `docs/145-THE-CHARTER-SEAL-CANONICAL.md` (the ritual
ladder + schema), `docs/90-THE-IMMUTABLE-LEDGER-CANONICAL.md` (the COC chain),
`docs/95-SALTED-IDENTITY-CHAIN-CANONICAL.md` (key identity). Implementation:
`scripts/5e_agent_sign.py` (signing + seal), `scripts/0b_path_utils.py` (path
authority), `scripts/1c_promote_to_forensics.py` (the gate).*
