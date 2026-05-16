---
type: narrative
status: active
tags: [forensics, proof, compliance, mth00076, integrity]
parent: Hive/INDEX
up: Hive/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:6ae3ae40c6ea07c42c3719c8300eb48b7472df711ad28e5bed693110990149f9
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Hive](INDEX.md) · [⌂ Home](../../HOME.md)

# Proof-in-Place

**mth00076: The artifact attesting to a system's compliance must be administratively
stronger than the system it attests to.**

---

## The Principle

When you audit a mechanism, ask:

> "Can the thing being audited tamper with its own audit trail?"

If yes — the audit trail is on the wrong substrate. Move it to a stronger one.

---

## The Classic Failure Mode

**Scenario:** A system writes its compliance proof to a log file that the system
administrator can also delete.

The proof says: "This system is compliant."
The administrator can delete that proof.
The proof is weaker than the system it attests to.

This is not compliance. It is theatre.

---

## Correct Substrate Hierarchy

From weakest to strongest:

```
1. Same-process memory (trivially tamperable)
2. Same-machine file (admin can delete)
3. Git-tracked file (requires force-push to tamper)
4. WORM bucket with compliance-mode lock (admin cannot bypass)
5. Blockchain timestamp (computationally infeasible to tamper)
```

The compliance proof must live at a **higher level** than the system it proves.

---

## faerie Applications

| Artifact | Substrate | Why |
|----------|-----------|-----|
| WORM genesis proof | B2 bucket with compliance-mode lock | Admin cannot bypass bucket-level lock |
| Vault `doc_hash` frontmatter | Git-tracked forensics/ | Force-push required to alter; separate from vault |
| Chain re-anchor declarations | Cross-repo hash commit | Cannot alter without visible git history change |
| Agent audit trail | `forensics/coc.jsonl` (append-only, hash-chained) | Each entry includes hash of previous entry |

---

## The Hash Chain

faerie's forensic COC log is hash-chained:

```json
{
  "ts": "2026-04-24T...",
  "agent_type": "documentation-engineer",
  "prev_entry_hash": "sha256:abc123...",
  "entry_hash": "sha256:def456..."
}
```

Each entry includes the hash of the previous entry. Altering any entry
invalidates all subsequent entries. The chain is self-proving.

This chain lives in `{repo}/forensics/coc.jsonl` — git-tracked.
Any alteration to the chain requires a visible git commit, creating
its own audit trail.

---

## What This Means for Agents

Agents WRITE to forensics/, they do not READ from it.

Reading forensic artifacts during analysis would allow agents to reason
backward from prior conclusions, potentially reinforcing confirmation bias.
The forensic layer is write-only from the agent's perspective.

Hooks handle forensic capture silently. PostToolUse hooks write COC entries,
compute hashes, and append to chains — without agent involvement.

---

## Related

- [[../Architecture/forensic-integrity]] — the full COC implementation
- [[the-five-principles]] — artifacts-in-forensics (principle 2)
- [[../Glossary/terms]] — COC, hash chain, forensics defined
