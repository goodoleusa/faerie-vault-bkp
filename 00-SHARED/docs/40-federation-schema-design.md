# Tier 40 — Cross-Team Mission Federation Schema (Design)

**Status:** DESIGN ONLY — no implementation in this artifact.
**Tier:** 40 (COC contracts, per HONEY mth00080).
**Task:** task-20260425-153515-6237.
**Author:** stigmergy-scout (behavioral protocol; mth00091).
**Date:** 2026-04-25.

## 1. Problem

Multi-Agent branching (current) assumes a single team owns a mission. Cross-team
federation requires N independently-keyed teams to coordinate on a shared
mission via stigmergy alone — no SendMessage, no central authority, no shared
process tree. Branch ownership, liveness, and trust must be expressible in
on-disk artifacts and verifiable by any reader.

Three additions are needed:

1. Branch claims must identify *which team* claimed, signed by that team's key.
2. Mission liveness must be observable across team boundaries (heartbeat).
3. Trust must be bounded — only allowlisted teams may claim mission branches.

## 2. Schema Gain — `branch_claim`

Existing `branch_claim` payloads (from Multi-Agent branching) gain three fields:

| Field        | Type          | Required | Notes                                          |
|--------------|---------------|----------|------------------------------------------------|
| `team_id`    | str (slug)    | yes      | Stable team identifier; see registry (§5).     |
| `team_pubkey`| str (hex-64)  | yes      | Ed25519 public key, hex-encoded, 64 chars.     |
| `signature`  | str (hex-128) | yes      | Ed25519 signature over canonical claim payload.|

Canonical signing payload (deterministic JSON, sorted keys, no whitespace):

```json
{"branch_id":"...","mission_id":"...","claimed_at":"...","claimer_session_id":"...","team_id":"..."}
```

Signature is over `sha256(canonical_payload)` so verification is constant-cost
regardless of payload size. `team_pubkey` is included alongside the signature
to make claim files self-verifying without registry lookup; the registry
(§5) is the authority for *which* pubkey is valid for `team_id` at claim time.

**Verification rule:** A claim is valid iff
(a) `signature` verifies against `team_pubkey` over canonical payload, AND
(b) `(team_id, team_pubkey)` is the active pair in `forensics/federation/teams.json`
at `claimed_at`, AND (c) `team_id` is in the mission's `allowed_teams` allowlist (§4).

## 3. Schema — `mission_heartbeat`

Heartbeat is per-team-per-mission. Each team writes its own heartbeats; readers
union across all teams to compute mission liveness.

| Field                   | Type      | Required | Notes                                    |
|-------------------------|-----------|----------|------------------------------------------|
| `ts`                    | ISO-8601  | yes      | UTC, microsecond precision.              |
| `mission_id`            | str       | yes      | Mission identifier.                      |
| `team_id`               | str       | yes      | Emitting team.                           |
| `branches_claimed`      | list[str] | yes      | Branch IDs currently held by this team.  |
| `last_member_session_id`| str       | yes      | Most recent live agent session for team. |
| `dead_session_after_sec`| int       | no       | Default 1800. Per-mission overridable.   |
| `signature`             | hex-128   | yes      | Ed25519 over canonical heartbeat payload.|
| `prev_hash`             | hex-64    | yes      | SHA256 of previous heartbeat line (chain).|

**Liveness rule:** A team holds a branch iff it has emitted a heartbeat
listing that branch within `dead_session_after_sec` of now AND
`last_member_session_id` is still active in that team's session ledger.
Otherwise the branch is reapable by another allowlisted team.

**Heartbeat cadence:** Recommended 300s (5min) — well under default
1800s `dead_session_after_sec` so transient agent stalls do not orphan branches.

## 4. Trust Model — Per-Mission Allowlist

Trust is *per mission*, not global. At mission creation, the mission manifest
declares an allowlist of `team_pubkey` values:

```json
{
  "mission_id": "msn-...",
  "created_at": "...",
  "allowed_teams": [
    {"team_id": "alpha", "team_pubkey": "ab12...", "added_at": "..."},
    {"team_id": "bravo", "team_pubkey": "cd34...", "added_at": "..."}
  ],
  "allowlist_signature": "..."
}
```

`allowlist_signature` is signed by the mission creator's key (also a registered
team in the global registry §5). Allowlist is *append-only after creation* —
removing a team requires a new mission. Adding a team requires a signed
amendment record (out of scope for this design; tracked as future work).

**Spawn-time enforcement:** Branch claim spawns MUST fail closed if claimer's
`team_id` is not in the active mission's `allowed_teams`. Enforcement lives in
the same hook that validates `branch_claim` signatures (8x_*).

## 5. Storage Layout

All federation state lives under `forensics/federation/`:

```
forensics/federation/
├── teams.json                    # global team registry, append-only
├── missions/
│   └── {mission_id}.json         # mission manifest with allowlist
└── mission-heartbeats.jsonl      # hash-chained heartbeats, all teams, all missions
```

### 5.1 `teams.json` (registry, append-only)

```json
{
  "version": 1,
  "teams": [
    {
      "team_id": "alpha",
      "team_pubkey": "ab12...",
      "registered_at": "2026-04-25T...",
      "registrar_signature": "...",
      "status": "active"
    }
  ]
}
```

Append-only: rotating a team's key requires a *new* entry with same `team_id`;
the prior entry's `status` becomes `rotated` and a `superseded_by` field is
added. Resolution at verification time picks the entry whose
`[registered_at, superseded_at)` interval contains the claim's `claimed_at`.

Registrar is bootstrapped at federation init (single root key, key path
documented in deployment, NOT in this design). Subsequent registrations may
be co-signed by M-of-N existing teams (future work).

### 5.2 `mission-heartbeats.jsonl` (hash-chained)

One JSON object per line. Each line includes `prev_hash` referencing the
SHA256 of the previous line's canonical bytes. First line uses
`prev_hash = "0" * 64`. Chain breaks are detectable by readers and trigger a
COC violation entry.

Heartbeats are interleaved across teams and missions; readers filter by
`(mission_id, team_id)`. Append-only file; rotation is by date suffix
(`mission-heartbeats-YYYYMMDD.jsonl`) when size exceeds 64 MiB, with a
chain-bridge record carrying `prev_hash` from the rotated tail.

## 6. Forensic Tie-In

- Every claim, heartbeat, and registry append produces a COC entry via
  `4x_coc_writer.py` (direct write to `forensics/*.jsonl` is blocked by hook).
- COC chain references file path + sha256 of the appended line, so the
  forensics log is the index of truth; the JSONLs are the data.
- Three-store architecture (mth00076) applies unchanged: forensics canonical,
  vault derivative, S3/B2 WORM backup.

## 7. Failure Modes & Reaper Behavior

| Condition                                  | Behavior                                      |
|--------------------------------------------|-----------------------------------------------|
| Heartbeat missing > `dead_session_after_sec`| Branch becomes reapable; reaper logs to COC. |
| Signature invalid on claim                  | Spawn fails closed; COC violation entry.     |
| `team_id` not in mission allowlist          | Spawn fails closed; COC violation entry.     |
| Hash chain break in heartbeats              | All affected mission liveness queries return `unknown`; ops alert via COC. |
| Registry pubkey rotation mid-claim          | Verification uses interval lookup (§5.1).    |

Reaping is *cooperative* — the reaper is itself an allowlisted-team agent and
its reap action is a signed branch_claim with a `reap_of` field referencing
the dead claim. No central reaper.

## 8. Out of Scope (Future Work)

- M-of-N team registration co-signing.
- Allowlist amendment protocol (mid-mission team add).
- Heartbeat compression for long-running missions.
- Cross-federation peering (federation-of-federations).

## 9. Acceptance Criteria for Implementation Phase

1. `branch_claim` JSON schema updated; existing claims migrated with
   one-time signing pass (or marked `legacy_unsigned` and gated behind a flag).
2. `mission_heartbeat` JSONL writer uses `4x_coc_writer.py`; direct writes blocked.
3. `8x_*` enforcer rejects claims failing §2 verification rule.
4. `teams.json` registry created with at least one bootstrap team.
5. Reaper utility (`9x_*`) reads heartbeats and emits reap claims.
6. Tests: signature round-trip, allowlist denial, dead-session reap,
   chain-break detection, key rotation interval lookup.

## 10. References

- mth00076 — three-store forensic architecture.
- mth00080 — tier 40 = COC contracts.
- mth00088 — main-context discipline (federation reads are scalar-only).
- mth00091 — scout convention (this doc authored under that protocol).
- `docs/MULTI-AGENT-BRANCHING.md` (extended by this design).
- `docs/FORENSIC-INTEGRITY.md` (hash-chain conventions reused).
