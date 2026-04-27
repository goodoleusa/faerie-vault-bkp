---
title: "Forensic Chain of Custody — How Hash Chaining Builds Tamper Evidence & Stigmergy"
type: system-narrative
status: final
project: hive-infrastructure
parent: [[00-SHARED/Hive/README]]
children: []
tags: #infrastructure #forensic #hash-chaining #coc #tamper-evidence #stigmergy
created: 2026-04-01
doc_hash: sha256:0c76cd6b68b42b49ba094f26f7cb22f38fc3cf4ab56ff481032ed667d8bc2829
hash_ts: 2026-04-01T16:24:18Z
hash_method: body-sha256-v1
---

# Forensic Chain of Custody System

A narrative guide to how our hash-chaining architecture builds tamper evidence, enables agent coordination, and discovered unexpected power for multi-agent workflow.

---

## The Core Insight

**What is a chain of custody (COC)?**

In legal investigations, a chain of custody is a documented history of who handled evidence, when, and what state it was in. If the chain breaks (evidence goes missing, or someone tampers with it), the evidence becomes worthless in court.

**Our COC system applies this principle to vault files and forensic logs:**

Every time a file changes, we:
1. Record *who* changed it (agent, human user, linter)
2. Record *when* it changed (timestamp)
3. Record *what the file looked like* (cryptographic hash)
4. **Link that record to the prior record** (hash chain)

If someone tries to tamper with old records, the links break. The tampering becomes obvious.

---

## How Hash Chaining Works (Non-Technical Explanation)

### The Idea: Fingerprints That Link

Imagine each version of a file gets a unique fingerprint:
- **v1 (initial):** Fingerprint ABC-123
- **v2 (after first edit):** Fingerprint DEF-456
- **v3 (after second edit):** Fingerprint GHI-789

Now imagine each fingerprint also includes the *prior fingerprint*:
- **v1:** "I am ABC-123 (no prior version)"
- **v2:** "I am DEF-456, and I came after ABC-123"
- **v3:** "I am GHI-789, and I came after DEF-456"

If someone tries to modify v2, its fingerprint changes to XYZ-999. But now it says "I came after ABC-123" when it actually should come after... something different. **The lie is obvious.**

If someone tries to reorder the versions (move v2 to happen before v3), the chain still breaks because v3 says "I came after GHI-789 (which is v2)" but the new order doesn't match.

**Result:** Any tampering is detectable because the links no longer form a valid chain.

---

## Two-Layer Hash Chaining (The Strength)

Our system is stronger because we hash at *two levels simultaneously*:

### Layer 1: Entry-Level (Forensic Log Entries)

Each entry in the forensic log is like a signed statement:

```
Entry #47:
  "This file changed at 2026-04-01T16:45:20Z
   It was changed by agent:membot
   The new content has fingerprint GHI-789
   The previous version had fingerprint DEF-456
   I (this entry) have my own signature: ENTRY-HASH-47"
```

That signature (ENTRY-HASH-47) is computed from the entry's content. If someone edits the entry later, the signature no longer matches.

### Layer 2: File-Level (The Forensic Log File Itself)

The forensic log file (`vault-mutations.jsonl`) is itself a vault file. It gets hashed every time an entry is appended:

```
vault-mutations.jsonl:
  v1 (just created): fingerprint = SHA256(empty file)
  v2 (after entry #1): fingerprint = SHA256(entry #1)
  v3 (after entry #2): fingerprint = SHA256(entries #1-2)
  ...
  v47 (after entry #47): fingerprint = SHA256(entries #1-47)
```

And each file version links to the prior:
```
v47 says: "I contain entries #1-47, fingerprint GHI-789, came after DEF-456"
```

**Result:** Double protection.
- If someone edits entry #25, the entry's signature breaks.
- If someone deletes entry #25, the file-level chain breaks (all subsequent versions have wrong hashes).
- If someone tries to hide tampering by adjusting later versions to match, they'd need to recompute every hash and signature from #25 onward — and we have copies of those hashes elsewhere.

---

## The Weaknesses (Honest Inventory)

### 1. **Single Point of Failure: The Local Machine**

If your computer is compromised, an attacker could:
- Edit a file
- Recalculate all hashes and signatures locally
- Update the forensic log with false entries
- Everything still appears valid

**Current mitigation:** None. The hash chain proves *integrity* but not *authenticity* (who really made the change).

**Future mitigation:** Digital signatures (see "PGP for Agents, YubiKey for Humans" below).

### 2. **Replay Attacks**

An attacker could take a valid forensic log entry from 2026-03-01 and insert it into 2026-04-01's log. The entry's signature is still valid.

**Current mitigation:** Timestamps help; logical order can be validated. But a sophisticated attacker could craft a plausible entry.

**Future mitigation:** Cryptographic commitment schemes (Merkle trees, timestamp services).

### 3. **Forensic Log Is Also Mutable**

The forensic log file itself lives in the vault and can be edited. If the entire forensic log is compromised, the attacker can rewrite history.

**Current mitigation:** None. This is by design (append-only, but not cryptographically sealed).

**Future mitigation:** Off-box forensic logging (write to an immutable external service; keep a read-only copy locally).

### 4. **No Decentralized Backup**

All evidence is stored locally. If the machine is wiped, the evidence is gone.

**Current mitigation:** Manual backups to B2 / external drive.

**Future mitigation:** Sync forensic logs to a remote immutable store (e.g., OpenTimestamps, blockchain notary, secure audit service).

---

## The Unexpected Strength: Stigmergy Discovery

### What We Built For

We designed hash chains for **tamper evidence**: "Can we prove this file wasn't modified?"

### What We Discovered It Does

Hash chains enable **agent coordination through pheromone trails**.

---

## Stigmergy: The Accidental Superpower

### Definition

**Stigmergy:** Indirect coordination where agents don't communicate directly but leave signals (pheromones, in nature) that the next agent reads and responds to.

Ants don't say "build a bridge at coordinate (x, y)." Instead:
1. Ant 1 lays a pheromone trail: "food detected this way"
2. Ant 2 follows the trail, strengthens the pheromone, and adds her own: "I went this way, safe"
3. Ant 3 reads both trails and decides which path is best

### How Our Hash Chain Enables This

When an agent writes to a shared file:

```
Agent 1 writes to vault:
  - File hash changes from ABC to DEF
  - Agent 1's manifest: "I wrote to file X, hash is now DEF"
  - Forensic log: Entry #47 records "Agent 1 changed file X from ABC to DEF"

Agent 2 checks that file:
  - Reads the manifest from Agent 1
  - Sees the current hash is DEF (validates: file is in the state Agent 1 left it)
  - Reads the forensic log and sees: "Agent 1 modified this on this date, this session"
  - Reads Agent 1's work in progress (draft status) and builds on it
  - Writes her own changes, creating a new hash
  - Forensic log: Entry #48 records "Agent 2 changed file X from DEF to GHI"

Agent 3:
  - Sees hash is now GHI
  - Reads the forensic log and sees the full chain: "Agent 1 → Agent 2 → Agent 3"
  - Validates each transition is legitimate (hashes match the chain)
  - Can trust that she's building on legitimate prior work
```

**This is stigmergy:** Each agent leaves a trail (manifest + hash) that the next agent reads. The hash chain *proves* the trail is authentic (wasn't tampered with).

### Why Hash Chain Matters for Stigmergy

Without hash chain:
- Agent 2 reads Agent 1's work and wonders: "Is this the real work, or has it been modified since Agent 1 wrote it?"
- Agent 2 can't trust the prior state

With hash chain:
- Agent 2 computes the current file hash
- Compares it to the hash in Agent 1's manifest
- If they match: ✓ File is in the state Agent 1 left it
- If they don't match: ✗ File was modified; Agent 2 should investigate

### The Discovery

We didn't plan this. The hash chain was supposed to be boring infrastructure. Instead, it became the proof mechanism that makes agent handoffs trustworthy.

---

## How It Works in Practice: Agent Handoff

### Scenario: Research → Development → Publishing

**Step 1: Research Agent**
```
research-analyst writes findings to:
  $CT_VAULT/00-SHARED/Agent-Outbox/findings.md

Manifest (returned):
  "Created findings.md, hash=ABC-123, session=sess-001"

Forensic log entry #1:
  timestamp: 2026-04-01T14:00:00Z
  mutator: agent:research-analyst
  vault_path: 00-SHARED/Agent-Outbox/findings.md
  doc_hash: ABC-123
  entry_hash: ENTRY-1
```

**Step 2: Development Agent**
```
fullstack-developer reads the manifest and checks:
  - Computes current hash of findings.md
  - Compares to ABC-123 from manifest
  - Match? ✓ File is in the state research-analyst left it

Reads the forensic log:
  - Sees entry #1 from research-analyst
  - Validates entry #1's signature (ENTRY-1)
  - Trusts that research-analyst really wrote this on 2026-04-01T14:00:00Z

Adds her own work:
  findings.md now has hash DEF-456

Manifest (returned):
  "Extended findings.md, hash=DEF-456, session=sess-002, built_on=ABC-123"

Forensic log entry #2:
  timestamp: 2026-04-01T15:30:00Z
  mutator: agent:fullstack-developer
  vault_path: 00-SHARED/Agent-Outbox/findings.md
  doc_hash: DEF-456
  previous_hash: ABC-123
  chain_prev_entry_hash: ENTRY-1
  entry_hash: ENTRY-2
```

**Step 3: Publishing Agent**
```
ipfs-publisher reads both manifests and the forensic log:
  - Entry #1 (research-analyst): hash ABC-123, signature ENTRY-1 valid ✓
  - Entry #2 (fullstack-developer): hash DEF-456, signature ENTRY-2 valid ✓
  - Chain: ENTRY-2 links back to ENTRY-1 ✓
  - No gaps, no tampering detected ✓

Publishes to IPFS with COC trail:
  "This content was authored by agent:research-analyst on 2026-04-01T14:00:00Z,
   extended by agent:fullstack-developer on 2026-04-01T15:30:00Z,
   published by agent:ipfs-publisher on 2026-04-01T16:00:00Z.
   Full forensic chain available at: [coc reference]"
```

Each agent trusted the prior agent's work because the hash chain proved it was unmodified.

---

## The Future: Cryptographic Signing (PGP + YubiKey)

### Current System: Tamper Detection Only

```
Hash chain proves: "This file hasn't been modified since Agent 1 left it"
But doesn't prove: "Agent 1 really wrote this (and not an attacker pretending to be Agent 1)"
```

### Future System: Tamper Detection + Authentication

We can add digital signatures:

#### For Agents: PGP Keys

Each agent type gets a unique PGP keypair:

```
Agent: research-analyst
  Public key: -----BEGIN PUBLIC KEY-----
              MIIB...
              -----END PUBLIC KEY-----

  Private key: Stored in ~/.claude/agents/research-analyst/signing.key
               (encrypted at rest)

When research-analyst writes to vault:
  1. Creates forensic entry
  2. Signs it: PGP_SIGN(entry_content, research-analyst.private_key)
  3. Stores signature in forensic log

When publishing or handing off:
  "This entry was signed by research-analyst.
   Verify with her public key.
   If signature valid, entry really came from her."
```

**Strength:** Can't fake an entry as coming from research-analyst without her private key.

**Weakness:** Private key stored on local machine. If machine compromised, key is compromised.

#### For Humans: YubiKey Signing

YubiKey is a hardware security key (like a small USB drive). The private key **never leaves the device.**

```
Human: goodoleusa
  YubiKey serial: 12345678
  Public key: (stored on YubiKey and backed up)

When goodoleusa signs a forensic entry:
  1. Plug in YubiKey
  2. System sends: "Sign this entry" (SHA256 hash only)
  3. YubiKey signs it (private key never leaves the key)
  4. System receives signature, stores in forensic log

When auditing:
  "This entry was signed by goodoleusa using YubiKey 12345678.
   Signature is valid, timestamp is 2026-04-01T16:00:00Z.
   goodoleusa really authorized this action."
```

**Strength:** Private key never exposed, even if machine is compromised. Attacker can't sign new entries without physical access to the YubiKey.

**Future Enhancement:** YubiKey can be configured to require a PIN or biometric before signing. Attack requires physical key + PIN/fingerprint.

### Hybrid Approach

```
Agent-generated entries: Signed with agent PGP key
                         (proves entry came from that agent type)

Human-promoted entries: Signed with human YubiKey
                        (proves a human reviewed and authorized it)

Forensic log structure:
  {
    "timestamp": "2026-04-01T16:00:00Z",
    "mutator": "agent:research-analyst",
    "doc_hash": "ABC-123",
    "signatures": {
      "agent": {
        "algorithm": "PGP",
        "key_id": "research-analyst-v1",
        "signature": "-----BEGIN PGP SIGNATURE-----..."
      },
      "human_approval": {
        "algorithm": "YubiKey-ECDSA",
        "key_id": "goodoleusa-yubi-12345678",
        "signature": "30440220...",
        "timestamp": "2026-04-01T16:05:00Z"
      }
    }
  }
```

This creates a **chain of custody that's legally defensible:**
- Entry was created by research-analyst (agent signature proves it)
- Entry was reviewed and approved by goodoleusa (YubiKey signature proves human authorization)
- No modifications possible without breaking the signatures

---

## Verification Tools

### Current (Hash-Based)

```bash
# Verify vault files haven't been tampered with
python3 ~/.claude/scripts/verify-vault-hash-chains.py

# Query mutation history of a specific file
python3 ~/.claude/scripts/query-vault-mutations.py "00-SHARED/Agent-Outbox/findings.md"
```

### Future (Signature-Based)

```bash
# Verify signatures on forensic entries
python3 ~/.claude/scripts/verify-forensic-signatures.py --agent research-analyst

# Verify human approval chain
python3 ~/.claude/scripts/verify-human-approvals.py --user goodoleusa

# Audit trail report
python3 ~/.claude/scripts/audit-coc-trail.py --output pdf "00-SHARED/Agent-Outbox/findings.md"
```

---

## Why This Matters

### For Agents (Stigmergy)

Agents don't trust each other directly. They trust **the hash chain.**

When Agent 2 reads Agent 1's work and sees the hash matches the forensic log, Agent 2 knows: "This is the real work, not a fake." Agent 2 can safely build on it.

Without the hash chain, Agent 2 would have to ask Agent 1 if the work is real (direct communication). With it, Agent 2 reads the evidence and decides independently.

### For Humans (Auditability)

You can prove every change:
- Who made it (agent type or human)
- When (timestamp)
- What changed (hash diff)
- Why (context in forensic entry)
- Proof it wasn't modified after (signatures)

If an agent goes rogue or an entry is disputed, you have an unbreakable evidence trail.

### For Compliance

Some regulations require "immutable audit trails." Our hash chain creates one.

---

## Summary: The System's Real Job

We built a system to answer one question:

**"Can I trust the state of this file right now?"**

Hash chaining answers: **Yes, if the chain is unbroken.**

And as a side effect, it enables:
- Agent handoffs (stigmergy)
- Human audits (compliance)
- Dispute resolution (evidence)
- Tamper detection (security)

All from the same mechanism: unbreakable links between versions.

---

*Last updated: 2026-04-01*
*Maintained by: Hive Infrastructure Team*
*Next phase: PGP + YubiKey integration*
