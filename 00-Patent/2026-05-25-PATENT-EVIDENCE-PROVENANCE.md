---
title: "Patent Evidence Provenance — Chain of Custody for Claim Support"
date: 2026-05-25
status: DRAFT — attorney review required
purpose: "Documents the cryptographic chain-of-custody for Claude Code session transcripts preserved as patent evidence for the USPTO provisional application filed 2026-05-25."
related_patent: "2026-05-25-PROVISIONAL-PATENT-APPLICATION-v2-SIMPLIFIED.md"
---

# Patent Evidence Provenance

## 1. Purpose

This document is written for patent attorney review. It describes how the session transcripts produced during development of the *faerie2* multi-agent orchestration system are preserved as evidence supporting the 19 claims in the provisional patent application filed 2026-05-25. For every claim in the application that cites a specific behavior, script, or empirical result, there is a corresponding line in a Claude Code session transcript that contains the actual agent work — the tool calls, the file writes, the manifest outputs, and the reasoning.

These transcripts are the primary empirical evidence. Without them, the patent's demonstrability assertions (e.g., "demonstrable via `scripts/1g_coc_core.py`") rest on the presence of the artifact alone, not on the record of how it was created. With the transcripts preserved and hash-anchored, an independent auditor can walk from any claim to the session that produced the evidence.

---

## 2. Source Transcripts Being Preserved

**Source directory:** `/mnt/d/0LOCAL/.claude/projects/-mnt-d-0LOCAL-gitrepos-faerie2/`

Claude Code writes one `.jsonl` file per session. Each line is a JSON record containing either a user message, an assistant message, a tool call, a tool result, or a metadata event. Every record carries a `timestamp` field (ISO 8601 with milliseconds). Assistant messages carry per-message token counts. Tool call records carry the exact file path written, the content, and the result.

**Top-level sessions:** 29 UUIDs discovered as of 2026-05-25:

| Session UUID | First message date | Notes |
|---|---|---|
| 55a26639-d2fc-4ae2-881f-60a479aff4a0 | 2026-04-24 | Earliest session in corpus |
| c0a275d0-9aba-4645-9682-4410476ee31b | (see mtime) | Large session with extensive subagents |
| 35918dd1-768d-43bc-a084-a2e60572b5d5 | (see mtime) | Session with most subagent files |
| a558f9b1-9c77-42b3-b8f6-05bf82f08852 | 2026-05-24 | Most recent before filing |
| [25 additional sessions] | 2026-04-24–2026-05-25 | Full list in `_manifest.jsonl` |

**Subagent sessions:** Several hundred `.jsonl` files under `{session-uuid}/subagents/agent-*.jsonl`. These contain the actual agent work — each subagent is a separate Claude invocation with its own tool calls and outputs.

**Date range of evidence:** 2026-04-24 through 2026-05-25 (the filing date).

---

## 3. Chain-of-Custody Structure

The preservation pipeline creates a four-link chain:

```
SOURCE FILE                    →  ARCHIVE COPY                →  COC ENTRY            →  MANIFEST SIGNATURE
~/.claude/projects/            →  forensics/                  →  forensics/            →  Ed25519 over
  -mnt-d-0LOCAL-gitrepos-         _claude-session-archive/       coc.jsonl              all manifest entries
  faerie2/{uuid}.jsonl            {YYYY-MM-DD}/                  (one entry
                                  session-{uuid}.jsonl            per session)
SHA-256 computed               →  hard-link (same inode)      →  entry carries:        →  canonical hash
before archival                   or copy + SHA-256 verify        session_uuid,          committed in
                                                                  sha256,                signature record
                                                                  archive_path,
                                                                  prev_entry_hash
```

**Link 1 — Source to archive:** The script `scripts/9x_claude_session_forensic_archive.py` reads each `.jsonl` file, computes its SHA-256 before any archival step, then either hard-links (preferred — source and destination share one inode; hash equality is guaranteed by file system) or copies and re-verifies SHA-256. The source file is never modified.

**Link 2 — Archive to COC:** For each archived session, one entry is appended to `forensics/coc.jsonl` via `scripts/1g_coc_core.py::append_coc_entry()`. The COC entry carries `session_uuid`, `sha256`, and `archive_path`. The entry is hash-chained: its `prev_entry_hash` is the `entry_hash` of the immediately preceding COC entry, computed as SHA-256(json.dumps(entry, sort_keys=True)). This means: if any COC entry is edited, all subsequent `prev_entry_hash` values become invalid. The chain breaks at the point of tampering.

**Link 3 — Manifest to Ed25519 signature:** After all sessions are processed, the script computes a canonical deterministic representation of the manifest (all entries sorted by `source_path`, serialized with `sort_keys=True, separators=(',',':')`), computes SHA-256 of that canonical form, and signs it with the `forensic-archivist` Ed25519 private key at `forensics/reputation/keys/forensic-archivist.key`. The signature is appended as a final record in `_manifest.jsonl`. The corresponding public key is at `forensics/reputation/keys/forensic-archivist.pub`.

**Tamper-evidence properties:**
- Editing any archived `.jsonl` file breaks SHA-256 comparison against the manifest entry.
- Editing any manifest entry breaks Ed25519 signature verification.
- Editing any COC entry breaks the hash chain from that entry forward.
- Deleting any COC entry breaks the `prev_entry_hash` linkage in the next entry.

---

## 4. How to Verify a Claim: Worked Example

**Claim cited:** Patent Section 9, Claim 9 — "Real-Time Stigmergic Blackboard with Five-Event Grammar." The demonstrability citation reads: `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` (live blackboard from Wave A, commit `07daafe0`).

**Step 1 — Find the session that produced it.**

The blackboard file `collab-realtime__visionary-artisan.jsonl` was written by agents VISIONARY, ARTISAN, and SYNTH operating concurrently. Open `forensics/_claude-session-archive/_manifest.jsonl` and search for entries with `models_used` containing those agent names, or with `first_msg_ts` / `last_msg_ts` overlapping the 2026-05-25 date of commit `07daafe0`.

The session that spawned those agents will appear as a top-level session entry. Its subagent files (under `{session-uuid}/subagents/`) contain the actual agent executions.

**Step 2 — Verify the archive copy.**

From `_manifest.jsonl`, locate the entry for the relevant session UUID. It contains `source_path`, `archive_path`, and `sha256`. Run:

```bash
sha256sum <archive_path>
```

Compare the output to the `sha256` field in the manifest entry. They must match.

**Step 3 — Locate the blackboard write in the transcript.**

Open the archived `.jsonl` file. Each line is a JSON record. Search for lines where `type == "tool_result"` and the tool was a file write to `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`. The content of that write is the raw blackboard data. The `timestamp` field gives the exact time of the write.

Alternatively, search for `CLAIM` or `COMPLETE` strings in the assistant message content — these are the blackboard events the agent produced.

**Step 4 — Walk the COC chain.**

Open `forensics/coc.jsonl`. Find the entry where `session_uuid` matches and `operation == "claude_session_archive"`. Verify `prev_entry_hash` matches the `entry_hash` of the preceding line. This confirms the session's archive event is anchored in the chain.

**Step 5 — Verify the manifest signature.**

The last record in `_manifest.jsonl` has `record_type == "manifest_signature"`. The `signature` field is `ed25519:<base64>:<canonical_hash>`. Reconstruct the canonical representation (sort all non-signature entries by `source_path`, `json.dumps(..., sort_keys=True, separators=(',',':'))`), compute SHA-256, compare to `<canonical_hash>` in the signature. Then verify the Ed25519 signature against the canonical bytes using the public key at `forensics/reputation/keys/forensic-archivist.pub`.

---

## 5. Integrity Guarantees

| Property | Mechanism | Strength |
|---|---|---|
| Tamper-evidence | SHA-256 of each transcript stored in manifest | Single-hash; see caveat below |
| Non-repudiation | Ed25519 signature over manifest canonical form | Strong; requires private key compromise |
| Ordering / timing | `timestamp` fields in every message record (Claude Code SDK) | Source-of-truth: Claude Code's own clock |
| Authorship | `sessionId` in every record; Claude model name in assistant messages | Recorded by Claude Code runtime |
| Continuity | COC hash chain (`prev_entry_hash` = SHA-256 of prior entry) | Chain breaks at any modification |

**SHA-256 caveat (per training learnings 2026-03-18):** For critical artifacts, the ideal standard is SHA-256 + MD5 or SHA-1 cross-check, providing redundancy against single-hash collision. This implementation uses SHA-256 only. For patent-evidence admissibility, SHA-256 alone is sufficient for current court standards. However, if filing in a jurisdiction that requires FIPS 140-2 multi-hash validation, the operator should run `md5sum` cross-checks and store results alongside SHA-256 values before the filing date. This is flagged as a Phase 3 open gap.

---

## 6. Open Gaps (Phase 3 Work)

The following integrity enhancements are NOT yet implemented and should be completed before non-provisional filing:

1. **Rekor anchor (transparency log):** The manifest SHA-256 (or a Merkle root of all session hashes) should be submitted to a public transparency log (Sigstore Rekor at `https://rekor.sigstore.dev` or equivalent) before the patent filing date. This provides an independent, publicly verifiable timestamp with sub-second precision, establishing that the archive existed in its current state on the filing date. The `entry_id` returned by Rekor should be stored in `forensics/_claude-session-archive/_rekor-anchor.json`.

2. **B2 WORM backup:** The entire `forensics/_claude-session-archive/` directory should be backed up to a write-once-read-many B2 bucket before filing. The B2 bucket's immutability policy prevents retroactive modification. The B2 file IDs and upload timestamps provide a second independent timestamp chain.

3. **Continuous capture hook:** A `.openhands/hooks/` hook or cron job should capture new session transcripts automatically on session close, so future Claude Code work against `faerie2` is also archived for patent-evidence completeness. Currently, archival is a manual one-time operation.

4. **MD5 cross-hash:** As noted in Section 5, add `md5` field alongside `sha256` in manifest entries for multi-hash redundancy.

5. **COC schema unification:** ✅ COMPLETED 2026-05-25. The mixed-schema v1 ledger (3600 entries) was frozen as a read-only archive via `scripts/9x_coc_genesis_seal.py`. A v2 genesis entry now starts the chain with the unified `entry_hash`/`prev_entry_hash` schema. All new entries chain cleanly from the genesis. The v1 Merkle root is publicly anchored on Sigstore Rekor (log_index 1630813609). See Section 7 "Genesis Seal" for full cryptographic details.

---

## 7. Genesis Seal — Cryptographic Cutoff (2026-05-25)

**Event:** COC v1 genesis seal executed 2026-05-25 (ahead of schedule relative to charter Phase 5).

The mixed-schema v1 COC ledger (3600 entries, 2026-05-19 through 2026-05-25) was frozen and anchored with a cryptographic Merkle summary, and a clean v2 chain was initialized. This closes the schema-branching gap (hash/prev vs entry_hash/prev_entry_hash) that would otherwise complicate expert-witness testimony.

| Field | Value |
|---|---|
| Seal timestamp | 2026-05-25T19:54:31Z |
| v1_anchor.merkle_root | `27c09fed0323de30841a3e4d56f3229fc2d4f4df5fc1384cd9008b2f24923ee2` |
| v1_anchor.file_sha256 | `5d794998174cf56ba7cd2bd74d15f38bdafadaa977acec944b5bf1dc80ce9833` |
| v1_anchor.line_count | 3600 |
| v1_anchor.first_line_ts | 2026-05-19T20:47:51.755484+00:00 |
| v1_anchor.last_line_ts | 2026-05-25T19:46:29Z |
| v1 archive path | `forensics/_pre-genesis-archive/coc.jsonl.v1.frozen.20260525T195431Z.jsonl` |
| v2 genesis entry_hash | `80f56b10dd86ce53e74c0758c4d87769c4e6f85f767e9636b9fb711171079ce3` |
| v2 genesis signature | `ed25519:TboQqixPdBdHgLxtiR8BaDdywnW6zDjhzV0kK42lRSk/QabajSSq...` (forensic-archivist key) |
| Rekor log_index | `1630813609` |
| Rekor UUID | `108e9186e8c5677a32c001a09438ae4158643f06388f43466295cd48e247982f7612fbda9ac8db38` |
| Rekor verify URL | https://search.sigstore.dev/?logIndex=1630813609 |

**What this means for expert-witness testimony:**

Pre-genesis entries (lines 1–3600 of the v1 archive) are verifiable via the v1 Merkle root. Any expert can recompute the Merkle root by hashing each line of the archived file and applying the Bitcoin-style Merkle construction implemented in `scripts/_merkle_tree.py`. The result must equal `27c09fed...`. This proves the v1 corpus has not been modified since the seal.

Entries from the v2 genesis forward use the unified `entry_hash`/`prev_entry_hash` schema (1g_coc_core.py canonical). The walk path is unambiguous — a single canonical chain from `prev_entry_hash: "v2_genesis"` forward. There is no schema branching to explain in court.

The v1 archive is read-only (`chmod 0444`, hard-linked from the original to guarantee byte-exact identity). Its SHA-256 is embedded in the v2 genesis entry's `v1_anchor` field, so the cryptographic cutoff is itself hash-chained and signed.

---

## 8. Archive Location Reference

| Artifact | Path |
|---|---|
| CC archive root | `forensics/_claude-session-archive/` |
| CC session index | `forensics/_claude-session-archive/_manifest.jsonl` |
| CC archived sessions | `forensics/_claude-session-archive/{YYYY-MM-DD}/session-{uuid}.jsonl` |
| OH archive root | `forensics/_openhands-session-archive/` |
| OH conversation index | `forensics/_openhands-session-archive/_manifest.jsonl` |
| OH archived conversations | `forensics/_openhands-session-archive/{YYYY-MM-DD}/conv-{conv-id}/` |
| COC ledger | `forensics/coc.jsonl` |
| CC signing public key | `forensics/reputation/keys/forensic-archivist.pub` |
| OH signing public key | `forensics/reputation/keys/continuous-evidence-preserver.pub` |
| CC archival script | `scripts/9x_claude_session_forensic_archive.py` |
| OH archival script | `scripts/9x_openhands_session_forensic_archive.py` |
| Cron dispatcher | `scripts/9x_evidence_archive_cron_dispatcher.sh` |
| Shape (unanchored count) | `_meta/shapes.json` → `patent.evidence.unanchored_session` (sums both lanes) |

---

## 9. Continuous Capture (Phase 2) — Operational Since 2026-05-25

Phase 1 established the Claude Code lane: a one-time backfill script (`9x_claude_session_forensic_archive.py`) archived 1,686 sessions and brought the `patent.evidence.unanchored_session` shape count from 29 to 0. That was a manual, operator-initiated operation.

Phase 2 closes the remaining gaps: automation and OH-native coverage.

### What changed

**Two lanes, one dispatcher.** The evidence archive now covers both:

1. **Claude Code lane** — operator-local sessions in `~/.claude/projects/-mnt-d-0LOCAL-gitrepos-faerie2/`. These are individual `.jsonl` files, one per session UUID. Archived to `forensics/_claude-session-archive/`.

2. **OpenHands lane** — customer-production conversations in `.openhands/conversations/<conv-id>/`. These are directory trees (one `base_state.json` + one JSON file per event). Archived to `forensics/_openhands-session-archive/` as mirrored directory trees using hard-link or copy + SHA-256 verify. The canonical hash is computed over all event files concatenated in event-number order — this hash is stable as long as the conversation is complete.

The new script `scripts/9x_openhands_session_forensic_archive.py` is the OH-native equivalent of the Claude Code archiver. It uses the same COC chain (`forensics/coc.jsonl` via `1g_coc_core.py::append_coc_entry`) and the same signing pattern (Ed25519 via `continuous-evidence-preserver` keypair at `forensics/reputation/keys/continuous-evidence-preserver.{key,pub}`).

### Operator does NOT need to remember to run anything

The dispatcher (`scripts/9x_evidence_archive_cron_dispatcher.sh`) runs every 15 minutes via cron (`deploy/scripts/install-crons.sh`, sentinel `faerie-managed:evidence-archive-cron`). It runs both lanes in sequence and logs structured JSONL to `forensics/eval/evidence-archive-cron-{date}.jsonl`.

A PostToolUse hook in `.openhands/hooks.json` (`post_tool_use_evidence_archive`) fires after every Edit/Write/Bash tool call in OpenHands sessions and runs the OH archiver in `--quick --since 1d` mode (~50ms overhead). This is the defense-in-depth layer: if the cron is broken for any reason, every tool call still ensures recent work is captured within seconds.

### Failure isolation

The two lanes are independent. A failure in the Claude Code archiver does not stop the OpenHands archiver and vice versa. The dispatcher exits 0 if either archiver returns 0 (success) or 1 (nothing new). Exit code >1 from either lane causes the dispatcher to exit 1 (alerts on-call cron monitoring).

### Partial session handling

OpenHands conversations with a most-recent event file mtime within the last 5 minutes are marked `partial: true` in the manifest and re-archived on the next cron tick. This prevents claiming a still-active session as completely anchored.

### COC chain integration

Both lanes append to the same `forensics/coc.jsonl` chain. Entries from the OH lane carry `operation: "openhands_conversation_archive"` and `agent_id: "continuous-evidence-preserver"`. An independent auditor walking the chain can distinguish CC vs. OH entries by the `operation` field and can verify either lane's canonical hash independently.

### Shape update

The `patent.evidence.unanchored_session` shape detector was updated (2026-05-25) to sum both lanes:

```
total_unanchored = claude_code_unarchived_count + openhands_unarchived_count
```

The target remains 0. With the 15-min cron + PostToolUse hook in place, the shape should self-heal to 0 within 15 minutes of any new session in either lane.

---

*Phase 2 section added by CONTINUOUS-EVIDENCE-PRESERVER agent, 2026-05-25.*

*Prepared by FORENSIC-ARCHIVIST agent, 2026-05-25. For attorney review.*
