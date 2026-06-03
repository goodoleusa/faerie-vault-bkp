---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: charter-forensic-accretion
status: synthesis-log
canon_candidate: true
---

# Charters as accreting forensic containers — full per-agent traceability

User stated (verbatim):

> "charter templates shld include all manifests and final canonical
>  outputs and missions signed by each agent that worked on it with
>  their own associated COC forensic data allowing traceability of
>  each agent and its state at the time"

This upgrades the charter from "scope contract" to **full forensic
ledger of every agent that touched its bounded region**.

## The doctrine

A charter is the bounded region (per doctrine 08). Inside its
boundary, work happens — manifests get written, missions emerge,
agents come and go, canonical outputs get produced. The charter
should ACCRETE all of that into its own JSON body so a single read
of the charter file gives you:

1. Every manifest that landed in service of this charter
2. The final canonical outputs (paths to artifacts in
   `forensics/artifacts/` or repo source code)
3. Every mission that emerged within the charter's scope
4. Every agent that touched the work — with their pubkey, session
   ID, signed entries, COC chain links

If you can answer the question "which agent did what when on this
charter" by opening ONE file, the charter has done its job.

## What's missing today

The current charter schema has:

```json
{
  "charter_id": "...",
  "cluster_prefix": [...],
  "phase_X_deliverables": [...],
  "manifests_received": [   /* sparsely populated today */
    {"manifest_id": "...", "ts": "..."}
  ],
  "coc_chain": {...}
}
```

The `manifests_received[]` field exists but is rarely populated.
The `synthesis_log[]` has prose. **There's no structured
per-agent per-timestamp ledger.**

## What it should be

```json
{
  "charter_id": "agents-as-bonded-creatures",
  "cluster_prefix": ["creatures", "agency", "bonds"],
  "phase_1_deliverables": [...],

  "manifests_received": [
    {
      "manifest_id": "20260522T142300Z__manifest__creatures.naming.memorial__creatures-phase1-foundation-01_maker",
      "manifest_path": "forensics/manifests/2026-05-22/20260522T142300Z__manifest__...",
      "ts": "2026-05-22T14:23:00Z",

      "agent": {
        "agent_type": "maker",
        "session_id": "abc12345",
        "pubkey": "ed25519:JrSObBxdQ7...",
        "signed_by": "ed25519:...",   /* the signature on this manifest */
        "signer": "maker"               /* human-readable identity */
      },

      "coc_chain": {
        "entry_hash": "abc...",
        "parent_hashes": ["genesis", "prev-entry-hash"],
        "branch": "main",
        "entry_hash_algo": "sha256"
      },

      "mission_emerged": "creatures.naming.memorial",
      "completion_choice": {
        "kind": "promote",
        "target": "creature-naming-protocol-v1",
        "confidence": 0.92
      },

      "deliverables_addressed": [
        "phase_1.creature-naming-protocol",
        "phase_1.creature-bond-ledger"
      ],

      "canonical_outputs": [
        "forensics/artifacts/2026-05-22/creature-naming-protocol.md",
        "deploy/chat-mvp/src/components/creatures/NamingPanel.jsx"
      ],

      "shape_deltas": [        /* per doctrine 13 */
        {"shape_id": "creatures.naming.unspecified",
         "before": 4, "after": 0, "verdict": "beneficial"}
      ]
    },
    /* ... one entry per manifest that ever touched the charter ... */
  ],

  "missions_within": [
    {
      "cluster_prefix": ["creatures", "naming", "memorial"],
      "first_seen_manifest": "20260522T...",
      "first_seen_ts": "2026-05-22T14:23:00Z",
      "claimed_ts": "2026-05-22T15:00:00Z",
      "manifest_count": 3,
      "status": "active|sealed|orphan-after-charter-seal"
    },
    /* ... one entry per mission that emerged ... */
  ],

  "agents_involved": [
    {
      "agent_type": "maker",
      "pubkey": "ed25519:JrSObBxdQ7...",
      "first_touch": "2026-05-22T14:23:00Z",
      "last_touch": "2026-05-22T16:45:00Z",
      "manifest_count": 3,
      "total_tokens_attributable": 12450,
      "average_completion_confidence": 0.91,
      "completion_choices_distribution": {
        "promote": 2, "discover": 1
      }
    },
    /* ... one entry per agent_type that contributed ... */
  ],

  "synthesis_log": [...],   /* unchanged — prose stays prose */
  "coc_chain": {...}        /* unchanged — charter's own chain */
}
```

## Why this matters

### Auditability

"Which agent broke phase 1?" — opens charter file, reads
`manifests_received[]` filtered by deliverable. Each entry has
`agent.signed_by` + `coc_chain.entry_hash`. The audit walks the
hash chain back through `coc.jsonl` and reconstructs the exact
state at the moment of signing. No archaeology across forensics
subdirs.

### Reputation

`agents_involved[].pubkey` ties every contribution to a stable
identity. Across many charters, agent reputation accretes — which
agents land beneficial mutations, which agents author durable
synthesis, which choose `seal` vs `discover` more often. The
charter is the ground-truth source for `9x_reputation_tracker.py`.

### Forensic replay

Given the charter's full ledger, you can replay the entire mission
arc: order manifests by ts, for each open the artifact at the
referenced path, verify the signature, walk the COC chain. The
replay is deterministic because every link is cryptographically
anchored.

### Mission archeology

`missions_within[]` records every emergent w3w cluster_prefix.
After a charter seals, this becomes the historical record of which
shape patterns appeared during the work. Future work can search:
"have we seen `creatures.naming.memorial` before?" — and find this
charter as the prior occurrence.

## What needs to ship

This is a schema upgrade + a library upgrade + a hook upgrade:

### Cut 1 — Schema

`forensics/schemas/shape/charter.schema.json` extended with:
- `manifests_received[]` — full structure above
- `missions_within[]`
- `agents_involved[]`

### Cut 2 — Library

`scripts/_charter_lib.py::update_charter()` gains:
- `accrete_manifest(charter_id, manifest_path)` — pulls the
  manifest's metadata, appends a structured entry to
  `manifests_received[]`
- `update_agents_involved(charter_id, agent_data)` — upserts the
  agent's running totals
- `update_missions_within(charter_id, mission_data)` — appends
  if mission is new in this charter's history

### Cut 3 — Reactive hook

`.openhands/hooks/9x_hook-charter-accrete.py` — fires on manifest
WRITES (PostToolUse). For each manifest with a `mission` field
that resolves to an active charter's cluster_prefix neighborhood,
calls `accrete_manifest()` on that charter. Idempotent (skips if
manifest already in `manifests_received[]`).

### Cut 4 — Backfill

`scripts/0x_charter_backfill_accretion.py` — one-shot script that
walks every existing manifest, finds its bounding charter (by
mission ↔ cluster_prefix overlap), accretes. Brings historical
charters up to the new schema in one pass.

### Cut 5 — Validator + audit

Audit script: count charters whose `manifests_received[]` is
populated vs empty. Becomes a new shape:
`charter.accretion.coverage` — target_direction=increasing.
Healthy when most active charters carry full per-agent traceability.

## Implementation note

This work fits the four-layer enforcement pattern exactly:

- **Structural** — schema defines the accretion fields
- **Cognitive** — `charter-discipline/SKILL.md` (existing) updated
  to teach agents about the accretion model
- **Reactive** — the accretion hook fires on every manifest write
- **Recovery** — the audit + backfill script catch drift

It also validates the new shape registry: the
`charter.accretion.coverage` shape lets us measure whether the
discipline is sticking.

## Single-line summary

**A charter should be opened once + you should see the entire
ledger: every manifest, every agent, every mission, every canonical
output, every COC chain link. Today charters carry sparse
synthesis prose; the upgrade makes them structured forensic
accretion containers. Per-agent traceability becomes a JSON path,
not an archaeology dig.**

---

*Doctrine arc 08-19 closed. Implementation queued; will be the
next major MAKER dispatch. Companion: doctrine 09 (parent/N
commission child/S — this doctrine operationalizes the bidirectional
cite from manifest→charter as a full data structure).*
