---
title: "Court-Admissible Evidence Chain — Making the Swarmy Substrate Expert-Witness Ready"
date: 2026-05-25
status: vision-doc
authors: [Amanda Morton, Claude Opus 4.7, the Swarmy collective]
charter_pre_reg: forensics/charters/proposals/2026-05-25Z__charter__court-admissible-evidence-chain__goodoleusa.json
related:
  - 2026-05-25-forensic-stigmergy-whitepaper.md
  - 2026-05-25-arxiv-draft-forensic-stigmergy.md
  - 2026-05-21_forensic-hybrid-ledger-architecture.md
  - patent/2026-05-25-PROVISIONAL-PATENT-APPLICATION-v2-SIMPLIFIED.md
  - patent/2026-05-25-PATENT-EVIDENCE-PROVENANCE.md
tags: [forensics, court-admissibility, expert-witness, evidence-chain, rekor, ed25519, worm-backup, discovery, patent-evidence, high-stakes-domains, medicine, law, journalism]
---

# Court-Admissible Evidence Chain

## The vision in one paragraph

A customer running the swarmy substrate in a high-stakes domain — a hospital's diagnostic-assist pipeline, a law firm's discovery workflow, a journalism outfit's source-protection chain, a precision-manufacturing audit trail — must be able to walk into a courtroom and have their expert witness produce **every agent tool call, every chain-of-thought chunk, every meaningful action that impacted the final output**, all cryptographically tamper-evident, all externally time-stamped via a public transparency log, all verifiable by hostile opposing counsel *without our infrastructure or trust*. This document defines what that looks like end-to-end and what's left to ship.

---

## 1. The four-tier trust model

Court admissibility is not a single property; it's a layered evidence stack. The swarmy substrate already captures the bottom layers; the top layers are the work-in-progress that the corresponding charter pre-reg covers.

```
TIER 4 — PUBLIC TIME-STAMP (this evidence existed at this point in time, verifiable globally)
  └─ Sigstore Rekor inclusion proof for the COC merkle root at submission time
  └─ Verifiable by: anyone in the world, without our infrastructure or trust

TIER 3 — CHAIN-OF-CUSTODY (this evidence has been preserved tamper-evidently)
  └─ COC entry hash-chained to all prior entries in forensics/coc.jsonl
  └─ Verifiable by: walk the chain from genesis; any modification breaks all forward links

TIER 2 — STRUCTURED ATTESTATION (an authorized agent committed to this work as meaningful)
  └─ Signed manifest citing task_id, lifecycle_judgment, charter_id, parent_hashes[]
  └─ Verifiable by: Ed25519 signature against the agent_type's stable pubkey

TIER 1 — RAW EVIDENCE (the model actually did this)
  └─ Claude Code session transcript line — verbatim message + tool call + result + ts
  └─ Verifiable by: SHA-256 of archived .jsonl file in forensics/_claude-session-archive/
```

The expert witness's job is to walk the court through each tier for each contested assertion. Tier 1 alone is "we say it happened." Tier 1 + 2 is "an authorized agent committed to this work." Tier 1 + 2 + 3 is "tamper-evident across time." **All four tiers together is the gold standard: verifiable by hostile counsel without our cooperation.**

---

## 2. What already exists (the foundation)

The substrate captures three layers of evidence simultaneously on every agent execution:

**Layer A — Raw session transcripts** at `~/.claude/projects/<encoded-repo>/<session-uuid>.jsonl`. Claude Code writes one `.jsonl` file per session. Each line is one event: a user message, an assistant message, a tool call, a tool result, or a metadata event. Every record carries an ISO-8601 millisecond-precision timestamp. Assistant messages carry per-message token usage. Tool call records carry the exact file path written, the content, and the result. Chain-of-thought reasoning when the model produces `<thinking>` blocks lands in the transcript verbatim. **Nothing is summarized.** As of 2026-05-25 the archive contains 45+ sessions, ~11.3 billion tokens, ~$15K of measured LLM API spend.

**Layer B — Manifests + COC chain** at `forensics/manifests/` and `forensics/coc.jsonl`. Every meaningful work product writes a signed manifest with `task_id`, `mission`, `bearing` (compass routing), `lifecycle_judgment`, `free_choice`, `discovered_work[]`, and `parent_hashes[]` (cryptographic pointers into the COC ledger). The COC ledger hash-chains entries via SHA-256: each entry's `prev_entry_hash` is the previous entry's `entry_hash`. Editing any entry breaks all forward links detectably.

**Layer C — Mission graph derived view** at `forensics/mission-graph.json`. Self-healing read view derived from the manifest corpus on every `sync`. `parent_hashes[]` from manifests ARE the graph edges. Tampering the graph requires tampering the chain; chain verification catches it.

Together: Layer A captures WHAT happened, Layer B captures WHY it mattered, Layer C captures HOW it connected. Every node on the mission graph is reachable by cryptographic pointer back to a specific COC entry, which is reachable back to a specific manifest, which is reachable back to a specific transcript line in a session jsonl.

---

## 3. What just unblocked (2026-05-25)

Two structural unlocks shipped today that move the substrate substantively closer to court-readiness:

**Ed25519 signing is now actually operational.** Before today, the substrate's `1a_manifest_writer.py` auto-signing routine fell through to `signed_by: ed25519:UNSIGNED_<agent>_NO_KEY` placeholder strings because `pynacl` was not installed in either Python venv. **Today the operator ran `uv pip install pynacl` in both `.venv/` and `deploy/mcp-server/.venv/`** and Ed25519 sign-verify roundtrips PASS in both. The canonical `5f_init_reputation.py` script now successfully provisions agent keypairs (e.g., `forensics/reputation/keys/court-admissibility-test.{key,pub}` verified working). Every future manifest seal produces a REAL Ed25519 signature, not a placeholder.

**Patent-evidence chain-of-custody preserved.** The FORENSIC-ARCHIVIST agent (commit anticipated) built `scripts/9x_claude_session_forensic_archive.py` which archives every Claude Code session transcript to `forensics/_claude-session-archive/{YYYY-MM-DD}/session-{uuid}.jsonl` via hard-link (preserving SHA-256 by inode equality) or copy-with-verification fallback. Each session writes a manifest line to `_manifest.jsonl` and a COC entry. The full session corpus (29 top-level sessions + ~270 subagent sessions, ~500MB-1GB total) has its provenance chain anchored.

These together mean: as of 2026-05-25, for **Claude Code sessions run on the operator's workstation**, every new agent execution that goes through the canonical writer produces signed manifest output, every signed manifest is hash-chained into the COC ledger, and every session transcript that produced the manifest is preserved tamper-evidently in the archive. Tiers 1, 2, and 3 of the four-tier trust model are operational for the local workstation.

**Critical scope qualifier:** the local workstation is the operator's development environment, not the customer's production deployment. Customer-facing production runs on **OpenHands**, not Claude Code. The OH runtime has its own conversation event stream (`.openhands/conversations/<id>/events/event-*.json`) which is *separate from* the Claude Code session jsonl files we just archived. **For court-admissibility in customer production, the OH conversation event stream must have the equivalent Tier 1-3 chain operational** — and as of 2026-05-25 it does NOT yet have continuous archival + signing + COC anchoring wired. This is the largest single gap between "operator-readiness" and "customer-production-readiness."

What's needed for the OH-native prod path:

- **OH conversation event archival** — equivalent to `9x_claude_session_forensic_archive.py` but for OH's `.openhands/conversations/<id>/events/*.json` directory-based event streams (rather than Claude Code's single-jsonl-per-session format). The CONTINUOUS-EVIDENCE-PRESERVER agent (Phase 2 of this charter) handles both lanes; needs proper-perms re-dispatch.
- **MCP-server-side signing for OH agent returns** — the LiteLLM token logger we shipped today writes per-call records; the equivalent signing wrapper should ensure every OH agent's terminal output that lands in a manifest is signed by the agent_type's stable key (not just hash-recorded). The `pynacl` install in `deploy/mcp-server/.venv/` (today) is the precondition.
- **Per-session reproducibility manifest** captured at OH session start, recording git_sha + venv lockfile hash + OH SDK version + tool inventory hash. Currently captured for Claude Code in transcripts; not yet captured for OH sessions.
- **Continuous capture cron** running inside the OH deployment (not on the operator's workstation), so customer-production sessions are archived within ≤15 min of any session activity without operator action.

Tiers 1, 2, and 3 will be operational for **both lanes** when the above ships. Tier 4 (Rekor public anchoring) is then the remaining structural gap **uniformly across both lanes**.

---

## 4. The expert-witness pipeline

For each contested assertion in a customer engagement, the expert witness walks through this sequence:

1. **Identify the assertion's task_id and the manifest that sealed it.** Search `forensics/manifests/` by `mission` + `charter_id` + date range using `mission_graph.py find`.

2. **Walk the manifest's `parent_hashes[]` back through the COC** to confirm the assertion is anchored in a tamper-evident chain. `scripts/1g_coc_core.py verify_chain` does this mechanically.

3. **Verify the manifest's Ed25519 signature** against the agent_type's pubkey in `forensics/reputation/keys/`. The signature proves authorship without contesting it. The agent_type-to-pubkey mapping is in `_registry.jsonl` (key registry).

4. **Pull the underlying Claude Code session transcript** from `forensics/_claude-session-archive/` and locate the specific tool calls + reasoning chunks that produced the assertion. The manifest references the session_uuid; the archive's `_manifest.jsonl` cross-references it to `archive_path` + `sha256`.

5. **Verify SHA-256 of the archived transcript** matches the `_manifest.jsonl` record. Proves the transcript hasn't been edited since archival.

6. **Verify Rekor inclusion proof** for the COC merkle root covering this assertion's date range. Proves external time-stamping that doesn't require our infrastructure or our trust. (Pending Phase 4 of the corresponding charter.)

7. **Present the verification chain** in court as a step-by-step exhibit (PDF). Opposing counsel can independently re-verify each step using only the public Rekor log, the public swarmy verification toolchain, and the operator's public keys (which are on the manifest signatures and need no separate disclosure).

The whole chain is built so that **the expert witness is not the trust anchor.** The cryptography is the trust anchor; the expert witness is the guide who walks the court through it.

---

## 5. Honest disclosures (what an expert MUST admit under oath)

This is what every expert witness using this substrate must honestly disclose. These disclosures don't weaken the testimony; they strengthen it by demonstrating the witness understands the system's epistemic boundaries.

- **LLM non-determinism.** Large language models at temperature > 0 are non-deterministic. The substrate captures what happened, not what would deterministically happen on re-run. Reproducibility claims must be probabilistic, not deterministic. The system prompts + spawn briefs ARE captured (so the influence on the model is auditable), but distinguishing 'legitimate doctrine' from 'leading-the-witness prompts' is a matter for jury interpretation, not cryptographic proof.

- **Authorship attribution granularity.** Authorship is attributed to the agent_type that signed the manifest, not to the underlying model instance. The same agent_type may have been served by different model versions across the session window. The model + version IS captured per-message in transcripts, so the underlying execution is auditable — but the cryptographic identity is the agent_type's stable role, not the specific model.

- **Chain-of-custody window.** Chain of custody is operator-maintained between session-write and archive-promote. The window is short (≤15 minutes with the continuous-capture cron in Phase 2 of the corresponding charter) but it exists. The Rekor inclusion proof anchors the archive root at promotion time; modifications BEFORE Rekor submission are operator-trusted. This is a real epistemic limit; it doesn't make the system inadmissible, but it constrains the strongest possible claim.

- **What we can prove vs cannot prove.** We can prove what was committed to the substrate (every manifest hash-chained, every transcript archived, every signature verifiable). We cannot prove the operator did not influence the model via the prompts. The prompts ARE captured, so the influence is fully auditable — but the question of "was this influence appropriate" is for the jury, not the cryptography.

- **Statistical-mechanics boundary.** Phase-transition behavior in the substrate's stigmergic coordination (per Khushiyant 2025, ρ_c ≈ 0.230) is empirically observed but the boundary itself is statistical, not crisp. Claims about emergent behavior should be presented as probability-weighted observations, not deterministic outputs.

Courts trust witnesses who admit limits. The substrate's design philosophy is: **everything that can be proven cryptographically is proven cryptographically; everything that cannot be is honestly disclosed as a limit.** No magic, no overstating.

---

## 6. What's left to ship (the corresponding charter)

The eight phases of `forensics/charters/proposals/2026-05-25Z__charter__court-admissible-evidence-chain__goodoleusa.json` (the charter the COURT-ADMISSIBILITY-CHARTER agent is writing in parallel):

| Phase | Status | Why it matters for court |
|---|---|---|
| 1. Signing substrate operational | ✅ SHIPPED 2026-05-25 | Without working Ed25519, authorship cannot be cryptographically attributed |
| 2. Continuous evidence preservation cron | Open (re-dispatch pending) | Without continuous capture, gaps in the archive become disputable territory |
| 3. Per-session reproducibility manifest | Open | Expert testimony requires "this output came from this substrate at this code-state with these tools" |
| 4. Rekor public anchoring | Open | Without external transparency log, every timestamp is operator-trusted; Rekor closes the trust gap |
| 5. COC schema unification | ✅ SHIPPED 2026-05-25 (ahead of schedule) | A single canonical verification path; no schema branching to explain in court. Genesis-seal executed: 3600 v1 entries frozen, v2 chain starts clean from `prev_entry_hash: "v2_genesis"`. |
| 6. B2 WORM backup with object-lock | Open | Single-host = single point of failure; redundancy is admissibility |
| 7. Discovery export tool | Open | Opposing counsel will request "everything related to assertion X" — needs to be a one-command production |
| 8. Notarized operator attestation | Open | Operator's legal identity bound to GitHub OIDC + ed25519 master key; filed once with patent/legal team |

Phases 2 + 4 are the highest-priority unblocks (continuous capture + external time-stamping). Phase 7 is the highest customer-facing value (the discovery-export tool is what makes a customer's expert-witness work easy). Phase 8 is the legal precondition for any production filing.

---

## 7. The customer-facing value proposition

For a customer in a high-stakes domain considering whether to adopt the substrate, the court-admissibility property reframes the value calculation. Without it: the substrate accelerates work cheaply. With it: the substrate accelerates work cheaply AND produces a verifiable evidence chain that survives adversarial scrutiny. The first is a productivity story; the second is a risk-management story. The second commands materially higher pricing because it removes the catastrophic-litigation tail risk that bounds adoption in regulated domains.

Concretely: a medical-records AI assistant that produces a diagnosis suggestion is useless to a hospital if the hospital cannot defend the suggestion in a malpractice trial. The hospital's defense requires showing the diagnostic reasoning, the inputs available to the system at the moment of suggestion, the chain-of-custody for both inputs and outputs, and proof that nothing was edited after the fact. The substrate's evidence chain is engineered specifically to produce this defense by construction. The hospital doesn't have to do anything special; using the substrate IS the defense.

The same argument applies in legal e-discovery, journalism source-protection, precision-manufacturing audit trails, financial-services compliance — every domain where AI output may be challenged in adversarial proceedings.

---

## 8. Synthesis

The substrate's other capabilities (mission-graph coordination, stigmergic blackboards, branching/Merkle/handshake, observation-driven design) are the *productivity* side of the value proposition. The court-admissible evidence chain is the *risk-management* side. Both are needed for high-stakes adoption. As of 2026-05-25, the productivity side is mature and validated empirically (commits `07daafe0` + `731749ad`; 11.3B-token measured workload). The evidence-chain side has its bottom three tiers operational (Tiers 1-3 of the four-tier model) and a clear 8-phase charter to close the top tier (Rekor) plus the supporting infrastructure (continuous capture, reproducibility manifest, WORM backup, discovery export, notarized attestation).

The expert witness of the future, walking into court with a customer engagement built on the substrate, can produce every tool call, every reasoning chunk, every meaningful action — and the court can independently verify each one without trusting the customer, the operator, or the substrate's infrastructure. That's the goal. Today we're on Tier 3; the work to reach Tier 4 is concrete, sequenced, and named.

---

*Drafted 2026-05-25 by Amanda Morton + Claude Opus 4.7. Companion to the formal charter pre-registration at `forensics/charters/proposals/2026-05-25Z__charter__court-admissible-evidence-chain__goodoleusa.json`. Cross-references the forensic-stigmergy whitepaper for substrate architecture, the patent provisional v2 for legal-claim structure, the patent-evidence-provenance document for the chain-of-custody mechanics, and the prior forensic-hybrid-ledger paper for the blockchain-to-AI-memory translation that established the trust model.*
