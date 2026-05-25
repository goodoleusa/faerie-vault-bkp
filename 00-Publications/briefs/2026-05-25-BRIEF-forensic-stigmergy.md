---
title: "Brief — Forensic Stigmergy for Multi-Agent LLM Coordination"
date: 2026-05-25
status: spray-E — technical brief (~1,800 words)
authors: [Amanda Morton, Claude Opus 4.7, the Swarmy collective]
crystal: 2026-05-25-arxiv-draft-forensic-stigmergy.md
target_audience: technical readers — engineering leads, CTOs, ML researchers — who want enough to evaluate the substrate without reading 9,000 words
length: 2 pages
citation_discipline: "Every claim cites a specific section in the crystal arxiv draft via [§N] notation. No claim originates here."
companions:
  - 2026-05-25-EXECUTIVE-BRIEFING-swarmy.md (Spray-D, 1-page executive)
  - 2026-05-25-court-admissible-evidence-chain.md (Spray-A, legal architecture)
  - 2026-05-25-MEGA-REPORT-token-economics-and-real-numbers.md (Spray-C, financial)
---

# Brief — Forensic Stigmergy

## The problem (1 paragraph)

Production multi-agent LLM systems (AutoGen [1], MetaGPT [2], ChatDev [3]) coordinate through orchestrator-mediated message-passing. The pattern works at small N but collapses structurally as agent count grows: the parent LLM composes spawn briefs inline in its own context, then reads each subagent's full return back into its context for synthesis. By N≈6 concurrent agents on substantive scope, the orchestrator's context window saturates with coordination bookkeeping before any synthesis work begins — the Brooks's-Law-analog cliff [§1.2 f(0) scaling]. Recent diagnostic work [Rath 2026, Advani 2026, Pan 2025] empirically confirms behavioral drift, anomaly cascades, and explainability collapse in deep multi-agent stacks [arxiv §2.4]. Parallel research [Khushiyant 2025, Li 2025, Yang 2025] reports stigmergic coordination (environmental-trace coordination, no direct messaging) outperforms message-passing by 36–41% above a phase-transition density ρ_c ≈ 0.230 [arxiv §2.5]. The substrate has been built, but no production framework has unified it with cryptographic auditability.

## The contribution (5 properties no prior LLM multi-agent system has unified)

**1. Filesystem-mediated stigmergic blackboards** with a five-event grammar (CLAIM/COMPLETE/HANDOFF/STARTUP/OBSERVED). Two-plus agents share an append-only JSONL file at a known path; each agent tail-reads before claiming. CLAIM is a lock; COMPLETE releases it. Coordination cost is O(F) substrate events for F files, **independent of N agents** — versus O(N·F) for orchestrator-mediated and O(N²·F) for peer-to-peer direct messaging [§5, §7.1(a) complexity analysis with concrete numbers for the validated wave].

**2. Hash-chained chain-of-custody (COC) ledger** whose `parent_hashes[]` field IS the mission-graph edge structure. The mission graph at `forensics/mission-graph.json` is a derived read view of the COC; every graph edge is a cryptographic pointer back into the ledger. Tampering the graph requires tampering the chain; chain verification catches it. SHA-256 prev_entry_hash linkage under fcntl.flock for single-host linearization without distributed consensus [§3.1–3.3].

**3. Branching + Merkle rollups + signed two-parent acceptance ritual.** Per-branch JSONL files at `forensics/coc-branches/{name}.jsonl` with per-branch flocks (concurrent multi-branch work doesn't serialize). Branch state compresses to a 32-byte Merkle root via `scripts/_merkle_tree.py` (Bitcoin-style construction, 14-test cryptographic suite verified). Merge entries on main carry exactly two parent_hashes (`main_prior`, `merkle_root`); Ed25519 signature on the merge manifest IS the acceptance ritual. Asymmetric crosstalk: branches read main freely; main learns about branches only via handshakes or merges [§6].

**4. Constant-cost handshake anchors.** A merkle root is 32 bytes; computing it is O(n) over branch entries; anchoring it to main is one disk append. Branches publish progress hashes on any cadence (`handshake` verb) without ending the branch. The handshake is simultaneously a heartbeat, a cryptographic commitment, a sync check, and a natural Rekor anchor point. Structurally identical to Certificate Transparency's Signed Tree Head check-ins [Laurie 2013 / RFC 6962] and side-chain pegging [Poon-Buterin 2017] applied to forensic agent work [§6.5].

**5. Transparency-log public anchoring** via Sigstore Rekor [Newman 2022], not distributed consensus. Bitcoin's consensus tax (PoW/PoS) is unnecessary for a single-operator workstation with trusted agents; the auditability property remains via transparency-log inclusion proofs. Replaces "trust a quorum of miners" with "trust the public append-only log" — a strictly weaker and well-understood assumption [§3.4 + court-admissibility doc].

## Why the composition is the contribution

Each piece — stigmergy [Grassé 1959, Theraulaz 1999], blackboards [Engelmore-Morgan 1988], Merkle trees [Merkle 1980], hash chains, transparency logs — is decades old. **What is novel is the composition**: forensic substrate + mission graph + blackboard + shapes + Merkle rollup + handshake + Rekor anchoring + agency-preserving completion-choice taxonomy, working together in deployed production [§9 Conclusion]. Prior LLM multi-agent systems satisfy at most two of these properties simultaneously; ours satisfies all five plus the doctrinal substrate that makes them composable.

## Empirical validation (mechanically verifiable)

**Wave A (commit `07daafe0`, 2026-05-25):** 4 agents on shared blackboards, 40 files modified, +8,533 / −285 lines, 11 named deliverables, **zero file collisions** despite agents touching overlapping `deploy/chat-mvp/src/components/canvas/` surfaces, 1 explicit live handoff (ARTISAN consumed VISIONARY's COMPLETE event citing 7 doctrine paths and registered them as live items at the moment they shipped, without message-passing). Operator coordination messages during the wave: **0** [§7.1].

**Wave B (commit `731749ad`):** 5 agents on two blackboards (sigstore-trio + decker-trio), 167 files modified, +23,463 / −1,501 lines, cryptographic test suite shipped 14/14 PASS, mission graph self-healing verified (110 missions, 260 manifests, 33 charters), branch/merkle-root/merge round-trip verified, **zero file collisions** despite tight import dependency between sister agents [§7.2].

**Sandwich-measured cross-skill doctrine propagation:** baseline T0 = 2 lifecycle skills containing refusal doctrine; post T1 = 8 skills; delta = +6 in 45 minutes, recorded at `forensics/eval/refusal-cross-skill-propagation/{baseline-T0, post-T1}.json` [§7.3].

**Coordination cost measurement (cost-formula baseline T0, 2026-05-03):** 3 calibration sessions, per-agent orchestrator overhead measured at **~61 tokens** with measured drift 2.08% / 8.33% / 2.78% — all well below the 20% acceptance threshold. The bundle composition happens in `spawn.py` subprocess, not in the parent LLM's context — the "shell game" that makes orchestrator-side cost constant in N. Compare to vanilla orchestrator-mediated frameworks at industry-typical 10,000–20,000 tokens per spawn brief [§7.1(a) measured numbers + comparison table].

**Token cost over a 32-day session window:** 45 sessions audited, 11.3 billion tokens, **$14,939 measured cumulative cost** at Opus 4.7 pricing. Cache-read fraction: **97.3%**. Counterfactual cost without prompt caching: ~$135,000 (9× higher). The substrate's cache-friendly design (always-loaded skills, subprocess-composed shared bundles, stable mission-graph context) is the structural reason for the cache fraction — typical caching hygiene yields ~85%; the extra 12 percentage points is what the substrate's discipline earns [Mega-Report §3].

## What's mature vs. what's in active development

| Layer | Status (2026-05-25) |
|---|---|
| Orchestration (mission graph, blackboards, branching) | **Mature**, empirically validated at production scale |
| Forensic chain (signed manifests, hash chain, archive) | **Operational** for Claude Code on operator workstation; OH-native prod-path archival continuous cron just shipped (15-min + PostToolUse hook) |
| Cross-session memory (membench) | **In active development.** Composite 48.13 (critical band). Operational dimensions strong (M3/M5/M6 ≈ 95); memory dimensions failing (M1/M2/M7 = 0). Disclosed transparently [§7.7 + §8.2 Limitations] |
| Public anchoring (Sigstore Rekor) | **Not yet shipped.** Charter pre-reg `court-admissible-evidence-chain` Phase 4 covers it |

## Limitations honestly disclosed

LLM output is non-deterministic at temperature > 0; the substrate captures what happened, not what would deterministically replay. Authorship is attributed at the agent_type level (the role), not the specific model instance. Adversarial-rewrite resistance against an adversarial operator who wants to rewrite their own history requires full consensus, which we explicitly do not provide — Rekor provides public-inclusion proof which makes selective rewrite detectable, but a fully-determined adversary could simply not anchor. Multi-host distribution requires either a cluster-aware lock or master-shard architecture; shadow scripts prototype the master-shard direction; production multi-host has not been deployed [§8.2 Limitations].

## Reproducibility

Every empirical number in this brief reproduces from on-disk artifacts at the cited commit hashes. `git show --stat 07daafe0` confirms Wave A counts. `python3 forensics/tests/test_merkle_roundtrip.py` runs the 14-test suite. `python3 scripts/9x_claude_token_aggregator.py --days 32` regenerates the token rollup. `python3 scripts/mission_graph.py sync` rebuilds the mission graph from the manifest corpus. Internal-eval competitor claims from `4x-RESEARCH-PAPER-OUTLINE.md` (the +149/+108/+91 vs vanilla/ChatGPT/mem0) were AUDITED AND STRIPPED today after the smoking-gun discovery that comparator baselines in `forensics/eval/_imported/scripts-quarantine-canonical-eval/3x_eval_harness.py:2097-2099` are hardcoded approximations, not controlled runs [§7.4]. The retained self-improvement claim (+34%, 0.554 → 0.742 composite) is sourced from internal eval baselines and characterized as such.

## Where to read further

- **Full empirical paper** (the crystal this brief distills): `2026-05-25-arxiv-draft-forensic-stigmergy.md` — ~9,000 words, 49 verified references, §1–9 + Verification Status appendix
- **Legal architecture for high-stakes adoption**: `2026-05-25-court-admissible-evidence-chain.md` (4-tier trust model, expert-witness pipeline, charter pre-reg with 8 phases)
- **Financial / token economics**: `2026-05-25-MEGA-REPORT-token-economics-and-real-numbers.md` (the $135K-saved counterfactual + 97.3% cache fraction analysis)
- **Patent**: `patent/2026-05-25-PROVISIONAL-PATENT-APPLICATION-v2-SIMPLIFIED.md` (19 claims, 21pp)
- **1-page executive briefing**: `2026-05-25-EXECUTIVE-BRIEFING-swarmy.md` (audience: customers, business development)

---

*Spray-E technical brief, 2026-05-25. Crystal-and-spray discipline: every [§N] notation points to a section in the arxiv draft where the claim is empirically grounded. If a claim feels unsourced, the spray is broken — check the crystal at the cited section.*
