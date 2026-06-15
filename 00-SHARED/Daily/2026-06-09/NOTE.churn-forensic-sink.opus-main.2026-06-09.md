---
source: /mnt/d/0local/gitrepos/reckon/charts/active/reckon-substrate-canonicalization/NOTE.churn-forensic-sink.opus-main.2026-06-09.md
promoted: 2026-06-09T23:09:19.635046+00:00
---

# NOTE.churn-forensic-sink.opus-main.2026-06-09.md

```
# NOTE — Churn is a forensic-sink failure, not a git problem

**By:** opus-main · **2026-06-09** · charter: forensic-chain-and-public-anchoring
(Could not write to the charter directly — `charter.py lib update` signing is broken:
stale hint at `charter.py:473` points to renamed `5e_agent_sink.py`, and signing for
`opus-main` fails even though `forensics/reputation/keys/opus-main.key` exists. **Denumber-sweep
regression — fix the charter signer's resolver.**)

## Root cause
Runtime telemetry ledgers are **git-tracked**, so hooks dirty the working tree on every
tool call → pulls block → 27+ `telemetry churn` commits. Specifically:
- `forensics/eval/{altimeter,spawn-costs,token-economics}/*.jsonl` — tracked, covered by
  `merge=union` (`forensics/**/*.jsonl`) so merges don't conflict, but **dirty tree still
  blocks the pull's pre-merge check**.
- `chart/active/_piston/gate-decisions.jsonl` — under `chart/`, **NOT** covered by the union
  driver at all → hard conflict.
- `forensics/reputation/keys/navigator.pub` — **REGENERATED** by the signing hooks
  (`9x_hook-signature-verify.py` / `9x_hook-manifest-sign-enforce.py`). A signing key is
  **write-once**; regenerating it is a key-clobber **DEFECT**, not telemetry.

## The real failure (why "never JUST rely on git" is correct)
The three-store design is git + B2 WORM + custody DAG. But the non-git legs are empty:
- B2 upload queue → buckets are **0 bytes** (nothing enqueues telemetry).
- `custody.jsonl` → 186 nodes = charters/manifests only, **no telemetry**.

So the **only** copy of session telemetry is the git working tree — the most fragile place
possible. `git stash` / `git checkout --` silently **destroys forensic data**. That is the
anti-pattern: forensic capture is happening as a *side-effect of leaving files dirty*, not as
a *push into a governed sink*.

## Two approaches (the comparison)
- **Other agent (pulled):** make churn **cheap** — auto-commit `[auto][skip ci]` + paths-ignore
  + local rekor anchor (`a5e005ac`, fit free-tier 2000 min/mo). Git stays the record; just stops
  costing CI. Also shipped `88ef3384` parent_root Merkle fan-in + `0a5169f4` GOLD→vault + coc-anchor JOIN.
- **This plan:** make telemetry **leave git** — push to the sink so the durable record survives
  a git discard.

## Recommendation — COMBINE
1. Keep the cheap auto-commit as the **disposable git mirror** (their fix is good for that).
2. **Also** push each ledger segment to the sink: `content_sha256 → custody node_hash` +
   B2 enqueue (`data_class=working` for telemetry, `worm` for sealed rollups). The B2 routing
   for this is already wired (`b2_realtime_uploader.py` + `promote_to_forensics.py::queue_b2_upload`
   stamps customer+data_class) — but **nothing enqueues telemetry yet**. Wire that.
3. **gitignore / union-complete** the runtime ledgers — extend `merge=union` to `chart/**/*.jsonl`,
   and consider gitignoring pure runtime state so it never blocks a pull.
4. **Make signing-hook key-init idempotent** — init a key only if absent; never regenerate
   `navigator.pub` (or any existing key).

**Principle:** forensic capture must be a *push into governed sinks* (custody DAG + B2 WORM).
Git is a disposable mirror — if you can't `git checkout --` a file without losing forensic
data, the capture is in the wrong place.

## Found bugs (file separately)
- `charter.py lib update` signing broken for keyed authors (denumber regression) — blocks the
  canonical "write synthesis to charter" path.
- `navigator.pub` regen by signing hooks.

```
