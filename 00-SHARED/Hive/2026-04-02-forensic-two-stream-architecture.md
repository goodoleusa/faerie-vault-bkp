---
title: "Two-Stream Forensic Architecture — Design Narrative"
date: 2026-04-02
type: design-narrative
blueprint: "[[Blueprints/TechDoc.blueprint]]"
agent_type: fullstack
session_id: w6-vault-docs
doc_hash: sha256:pending
status: draft
tags:
  - forensics
  - architecture
  - coc
  - two-stream
  - court-admissibility
---

# Two-Stream Forensic Architecture — Design Narrative

## Context: Why This Was Built

The investigation stack was producing work that might one day end up in court. Not "court-ready" as a marketing phrase — actual chain-of-custody requirements where a defense attorney looks for any seam to discredit findings. The early system had a fundamental gap: agents were writing to local files, those files were ephemeral by nature, and there was no verifiable record of who made a finding, when, and why.

The other pressure was scale. Twenty-plus agents can run in a single session. They coordinate not by talking to each other but through shared filesystem state — stigmergy, the same coordination mechanism ants use via pheromone trails. This works beautifully when every agent write leaves a trace that persists. It breaks completely when agents write to volatile /tmp paths, crash without saving, or overwrite each other silently.

Both problems — court admissibility and agent coordination — turned out to have the same solution.

---

## The Two-Stream Principle

Every agent action naturally produces two parallel outputs from a single write operation.

```
AGENT OPERATION
      |
      +---> [Stream A: FORENSIC] --------------------------------->
      |          local coc.jsonl (hash-chained)
      |          PGP-signed per entry
      |          uploaded to B2 WORM bucket (Object Lock)
      |          reasoning_snapshot captured
      |
      +---> [Stream B: STIGMERGIC] ------------------------------>
                 Agent-Outbox (vault write zone)
                 status: in-progress -> draft -> final
                 next agent reads this path
                 emergent coordination via filesystem
```

The forensic stream is immutable and verifiable. The stigmergic stream is living and collaborative. They serve different masters — court and coordination — but they emerge from the same act of doing work.

The key insight: these are NOT two separate systems that need synchronizing. They are two interpretations of the same write event. The forensic layer captures the metadata envelope around every write. The stigmergic layer is the write itself in a shared namespace.

---

## Three-Bucket B2 Architecture

Backblaze B2 provides the durability backbone. Three buckets, each with a distinct role:

```
LOCAL CANONICAL                    B2 BUCKETS
--------------                     ----------
forensic/coc.jsonl  -----sync----> [1] hustle-forensic-worm
(hash-chained,                         Object Lock: Compliance mode
git-tracked)                           Retention: 7 years
                                        No delete API -- ever

Agent-Outbox/       -----sync----> [2] hustle-working
(living docs,                          Standard bucket
vault writes)                          Versioned, deletable
                                        Human + agent collaboration

code/data/          -----backup--> [3] hustle-canonical
(source of truth,                      Cold storage, periodic snapshot
git history)                           Emergency recovery baseline
```

Provisioned by forensic/forensic_bucket_provision.py. The WORM bucket uses Backblaze Object Lock in Compliance mode -- the setting where even the account owner cannot delete objects before the retention period expires. This is the property that makes it court-useful: the records cannot have been altered retroactively.

The working bucket is not forensic -- it is convenience storage for the stigmergic stream. Agents write drafts there, humans annotate, content evolves. The canonical bucket is for disaster recovery: periodic snapshots of the git repo and evidence corpus.

---

## PGP Per-Agent Signing with Ed25519 Keys

Every agent type has its own GPG keypair. Not a shared "system" key -- individual agent identity that can be verified independently.

Why this matters for court: if the forensic log shows "finding made by fullstack-agent at 14:32" and the signature can be verified against a public key that has been in the key registry since before the investigation started, that is a testable, verifiable claim. A defense attorney who wants to challenge it must show either (a) the key was compromised or (b) the hash chain was broken. Both are forensically auditable.

Ed25519 was chosen over RSA for three reasons:
1. Smaller signatures (64 bytes vs ~256 bytes) -- the COC log stays compact
2. Faster operations -- signing adds <5ms per entry at logging time
3. Deterministic -- same private key always produces the same signature for the same message (no k-value randomness as in ECDSA), which aids reproducibility

The human researcher signs via YubiKey (hardware-backed PIV). This creates an intentional asymmetry: software-generated agent keys can be audited and their provenance traced. The hardware key adds a "physical custody" layer for the human's annotations that software keys cannot provide.

forensic/agent_keyring.py manages the registry: generates keypairs on first use for each agent type, exports public keys for verification, and stores key metadata in forensic/key-registry.json.

---

## Hash Chain Format

Each COC entry has this structure (canonical JSON, deterministic field ordering):

```json
{
  "entry_id": "uuid4",
  "ts": "ISO8601-UTC",
  "agent_type": "fullstack",
  "session_id": "w6-xxx",
  "operation": "write",
  "target_path": "relative/path/to/file",
  "input_hash": "sha256:abc...",
  "output_hash": "sha256:def...",
  "reasoning_snapshot": "Brief field notes: why this decision was made",
  "prev_entry_hash": "sha256:previous-entry...",
  "entry_hash": "sha256:this-entry...",
  "sig": "-----BEGIN PGP SIGNATURE-----\n...",
  "sig_type": "pgp-ed25519"
}
```

The hash chain rule: entry_hash = SHA256(canonical_JSON_excluding_entry_hash_and_sig). The prev_entry_hash field links to the previous entry's entry_hash, creating the chain. Genesis entry uses prev_entry_hash: "".

Important: entry_hash, sig, and sig_type are EXCLUDED from the canonical form used to compute the hash. This is a one-way commitment: you cannot change the entry without invalidating all subsequent hashes. The chain can be verified by any party with access to the public keys and the coc.jsonl file.

The verification command:
```bash
python3 forensic/forensic_stream.py --verify-chain
```

This checks every entry in sequence: recomputes each hash, verifies the chain linkage, and verifies each PGP signature against the registered public key for that agent type. Output is a verification report that can itself be included as a court exhibit.

---

## Reasoning Snapshots: The Field Notes Argument

The reasoning_snapshot field captures a brief text note from the agent at the time of each operation. This is not a transcript of the full reasoning -- it is a field note in the tradition of forensic investigators who annotate evidence in real time.

The court argument for this: in physical forensic work, the difference between "chain of custody" and "chain of understanding" matters. You can prove who touched the evidence (CoC) but not necessarily what they understood about it at the time (reasoning). When AI agents produce findings, the defense will ask: did the agent understand what it was doing, or was it pattern-matching blindly?

The reasoning snapshot answers this. It records, at the moment of the operation, what the agent believed it was doing and why. This is not post-hoc reconstruction -- it is contemporaneous documentation, time-stamped, hash-chained, and signed.

Example snapshots from production:
- "Normalizing date formats before join -- source has mixed ISO8601 and Unix epoch"
- "Writing final manifest -- all 847 items verified against input hash, 3 nulls dropped"
- "PGP signing entry -- agent=evidence-analyst, chain length=142"

---

## Terminology Decision: Stroke / Cycle / Shift / Sprint

"Session" was retired because it meant different things to different people -- a user session, a CLI invocation, an API call, a work period. The ambiguity caused real bugs in piston-checkpoint.json and agent_state.json where "session" was being used for both the CLI lifetime and the context window.

The replacement hierarchy:

| Term   | Boundary        | Boundary event                     |
|--------|-----------------|------------------------------------|
| STROKE | Context window  | Auto-compact fires (intake -> power -> exhaust) |
| CYCLE  | CLI invocation  | User types claude / exit           |
| SHIFT  | Work session    | /faerie -> /handoff                |
| SPRINT | Feature phase   | All work to enter next project phase |

The piston metaphor: a stroke is one compression cycle of the engine. Exhaust (compaction) clears the cylinder. Intake (new context) fills it again. Power (the work) happens in between. The engine (Claude CLI process) runs many strokes per cycle. The worker (human) runs many cycles per shift.

This naming eliminated the ambiguity. piston-checkpoint.json now stores stroke_count (increments per compact), cycle_id (the CLI run UUID), shift_start (the /faerie timestamp), and sprint_id (the current sprint from ARCHITECTURE.md).

The forensic log uses cycle_id as the primary identifier for grouping entries from the same CLI invocation, with stroke_count as a sub-index.

---

## Agent Trace Preservation

Before this system, when an agent crashed or was killed mid-task, its reasoning was gone. The /tmp paths it used for scratch were cleaned by the OS. The only surviving artifact was whatever it managed to write to a shared path before dying.

forensic/trace_collector.py solves this by:
1. Monitoring known agent scratch patterns under /tmp/claude-* and /tmp/agent-*
2. When an agent completes (or is killed), sweeping those paths to forensic/agent-traces/{agent_type}/{cycle_id}/
3. Hashing each collected file and adding a COC entry with operation: trace-collected
4. Uploading to the WORM bucket with the forensic batch

Traces are not evidence in themselves -- they are context for understanding evidence. A trace file that shows an agent considered but rejected an alternative hypothesis is valuable if that decision is ever questioned. The collector ensures it survives.

---

## Flight Deck: Real-Time Agent Tracking

The flight deck addresses a specific problem: during heavy sessions with 20+ agents, faerie loses track of what is in flight vs returned vs stalled. The piston model assumes agents return to manifest files -- but if an agent stalls, there is no notification, no timeout, no visibility.

scripts/flight_deck.py (designed this session):
- Reads ~/.claude/hooks/state/agent_state.json (written by spawn hooks)
- Tracks agent status: spawned, in-progress, returned, timed-out, errored
- Refreshes from manifest file mod-times to detect stalls (no write in N minutes = stall alert)
- Survives auto-compact: state is in a JSON file, not in context
- Dashboard output: one line per agent, status, last-write time, manifest path

The key property: the flight deck is a read-only view of filesystem state. It cannot break anything. It does not need to communicate with agents. It observes the stigmergic stream passively.

---

## Eval Harness: 0.306 to 0.568 (+86%)

The evaluation harness started as a simple benchmark runner. The jump from 0.306 to 0.568 came from three improvements:

Baseline bootstrapping. The first run is never scored as an improvement -- it IS the baseline. Previous versions would score the first run against a zero baseline (100% improvement that meant nothing). Bootstrapping records the first-run score as the reference point and tracks delta from there.

Auto-queue for failed cases. When an agent scores below threshold on a test case, the harness automatically adds a task to the training queue with the case context, failure mode, and hypothesis for improvement. This closes the loop between evaluation and improvement without human intervention.

Forensic history. Each eval run appends to forensic/eval-history.jsonl with the same hash-chain format as the main COC log. This means eval results are chain-of-custody tracked. If an agent's score improves, the improvement is verifiable against the immutable history. If a model update regresses a score, the regression is documented with a precise timestamp and input hash.

The 0.568 score is not a ceiling -- HONEY mth00037 specifies that a first-run score above 0.95 means the criteria are too easy. The target ceiling is 0.85-0.90. 0.568 means meaningful room for improvement remains, which is the correct calibration state.

---

## Template System: CourtReady-LightGreen

The template system emerged from a specific client need: a legal team needed a website that looked trustworthy and professional without looking corporate or aggressive. Green-on-white, clean typography, clear information hierarchy.

CourtReady-LightGreen became the hero template because it solved multiple problems at once:
- Accessibility-first color palette (WCAG AA throughout)
- Print-ready layouts (court filings often get printed)
- Structured data markup for legal entities, documents, and timelines
- Zero JavaScript fallback for environments where JS is blocked

The ThemeCustomizer (packages/foundationcraft/src/components/ThemeCustomizer.astro, 1386 lines) is the scaffolding system that makes CourtReady one of five style presets rather than a one-off. The five presets: CourtReady-LightGreen, CourtReady-Navy, TrustBuilt-Warm, DataFirst-Dark, CommunityVoice-Accessible.

Each preset is a complete design token set -- colors, typography scale, spacing, component variants -- that can be switched without touching component code. The ThemeCustomizer generates a CSS custom-properties file from the selected preset plus any overrides.

TemplateGallery.astro provides the showcase view: a grid of previews with live switching. Built for the foundationcraft sales flow where clients choose a starting point before onboarding.

---

## Cross-Repo Enforcement

The forensic architecture needed to be enforced, not just documented. Three enforcement layers:

Global rules (~/.claude/rules/): The rules files are loaded at every session start. core.md contains the hash-before-and-after requirement. agents.md contains the streaming and stigmergy requirements. These are not optional -- they are the instructions every agent receives before it starts working.

Cybertemplate forensic gate: The cybertemplate repository has a pre-commit hook that checks whether any file in forensic/ was modified without a corresponding COC entry. If an agent writes to forensic/coc.jsonl without a chain-valid entry, the hook rejects the commit. Forensic artifacts can only enter the repo through the verified pipeline.

DAE as standalone pipeline: The data-analysis-engine is designed for eventual open-source release. Its forensic implementation is self-contained: no dependency on the cybertemplate infrastructure. DAE's COC implementation works identically but writes to dae/forensic/ with its own hash chain. When DAE is released, it comes with forensic rigor as a built-in feature, not an afterthought.

---

## ASCII Data Flow Diagrams

### End-to-End COC Flow

```
AGENT WORK
    |
    v
[forensic_stream.py --log]
    |
    +--[1]--> forensic/coc.jsonl          (local, hash-chained, git-tracked)
    |              |
    |              v
    |         [--sync-b2]
    |              |
    |              v
    |         B2 WORM Bucket             (Object Lock Compliance, 7yr)
    |         hustle-forensic-worm
    |
    +--[2]--> 00-SHARED/Agent-Outbox/     (vault, stigmergic stream)
                   |
                   v
              Next agent reads           (filesystem = nervous system)
                   |
                   v
              Human promotes             (30-Evidence/ after review)
```

### Hash Chain Link Structure

```
ENTRY N-1                    ENTRY N                       ENTRY N+1
---------                    -------                       ---------
entry_hash: "sha256:aaa"  <- prev_entry_hash: "sha256:aaa" <- prev_entry_hash: "sha256:bbb"
                              entry_hash: "sha256:bbb"
                              |
                              v
                          canonical JSON hash
                          PGP sig (Ed25519)
```

### Stroke/Cycle/Shift/Sprint Nesting

```
SPRINT (weeks -- feature phase)
  |
  +-- SHIFT 1 (/faerie -> /handoff)
  |     |
  |     +-- CYCLE 1a (claude ... exit)
  |     |     |
  |     |     +-- STROKE 1 (context window)
  |     |     |       [work ... compact fires ... exhaust]
  |     |     +-- STROKE 2
  |     |     |       [intake ... work ... compact fires]
  |     |     +-- STROKE N
  |     |
  |     +-- CYCLE 1b
  |           |
  |           +-- STROKE 1
  |
  +-- SHIFT 2
        ...
```

---

## Unplanned Benefits (Proof the Architecture Hit a Structural Truth)

Per sys00019 in HONEY -- unplanned benefits signal a real structural truth was hit.

Planned: immutable audit trail, agent coordination, reduced orchestration overhead.

Unplanned:
- Debugging becomes trivial. When an agent produces a wrong finding, the reasoning_snapshot and input_hash let you replay exactly what it saw and decided. No more guessing what the agent was thinking.
- Parallelism safety. Multiple agents writing to the same WORM bucket never conflict -- each entry is UUID-keyed and hash-chained independently. The chain merges at verification time.
- Training data. The COC log with reasoning snapshots is a labeled dataset of agent decisions with outcomes. The eval harness can query it. Future training runs can use it.
- The forensic log IS the provenance chain. Originally designed as a supplement to git history. Turned out to replace several scripts that were trying to reconstruct provenance manually.

The feature closed: court admissibility, agent coordination, debugging, parallelism safety, training data generation, and provenance reconstruction. That is six problems from one architectural decision. By sys00019, this indicates a real structural truth: the audit trail and the communication channel were always the same thing.

---

*Written: 2026-04-02. Agent: fullstack. Session: w6-vault-docs.*
*Next: promote to NECTAR after human review. Annotate via .ann.md sibling.*
