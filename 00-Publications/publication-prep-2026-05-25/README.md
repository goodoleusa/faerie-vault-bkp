# Publication-Prep Bundle — 2026-05-25

**Bundle ID:** publication-prep-2026-05-25
**Assembled:** 2026-05-25
**Assembled by:** knowledge-synthesizer (agent)
**Purpose:** Every artifact needed to support submission of the forensic-stigmergy whitepaper and three adjacent papers. Read this file first. Then read `citations-manifest.json` for the machine-readable index.

---

## What Is In This Bundle

This bundle contains four primary papers, twenty supporting vault publications, a complete BibTeX citation file, twelve metric snapshot JSONs, seven architecture snippets, and a COC-signed assembly manifest. Nothing here was deleted or modified from the originals — every file is either a copy or a new artifact (README, citations-manifest.json, citations.bib) generated during assembly.

---

## The Four Primary Papers

All four papers are in `00-primary-papers/`.

**2026-05-25-forensic-stigmergy-whitepaper.md** is the main submission. It describes a coordination substrate for LLM agent swarms built on an append-only hash-chained ledger (the COC, or chain-of-custody), Ed25519 signatures, a mission-graph DAG derived from parent hashes, and stigmergic blackboards for real-time parallel-agent coordination. The empirical claims are grounded in the live faerie2 system: 231 COC entries, 265 manifests, 112 missions, 21 registered measurement shapes, and a validated multi-agent blackboard wave (commit 07daafe0, 13 events, zero file collisions).

**2026-05-25-decker-as-full-stack-atom.md** covers the Decker card ontology: a two-faced atom holding frontend-design on one face and backend-dev on the other, linked by compass-bearing hierarchy edges (NSEW) on the canvas. It is the UI substrate paper for the faerie agent canvas described in the whitepaper.

**2026-05-25-lifecycle-judgment-vs-free-choice.md** documents the two-column semantic split of the agent completion vocabulary: `lifecycle_judgment` (seven kinds — mechanical outcome assessment, pre-fillable by spawners) versus `free_choice` (twelve kinds — pure agent agency, never pre-fillable). This split is the formal basis for the agency-research design: if spawn briefs pre-fill `free_choice.kind`, the dataset of observed agent behaviors is contaminated. The paper covers the contamination problem, the doctrine fix, and the codebase migration.

**2026-05-25-refusal-as-load-bearing-doctrine.md** presents refusal as a first-class, graph-visible act — not a failure mode. The seven-lens framework (dual-use, scope and targeting, authorization and democratic supervision, cumulative effects, operator intent versus likely use, alternative formulations, refusal as conversation) gives agents a structured reasoning process. The paper documents the forgetting problem (refusal doctrine was present in only two of eight active lifecycle skills before the 2026-05-25 cross-skill propagation wave) and the fix (now present in eight skills, plus AGENTS.md root paragraph and docs/20-AGENT-AGENCY-CANONICAL.md).

---

## Supporting Vault Publications (`01-supporting-vault-pubs/`)

Twenty vault publications that the whitepaper cites or that provide context. The two most heavily cited — the Anthropic Stigmergy application document and the Forensic Hybrid Ledger Architecture paper — are copied in full. The remaining eighteen are stub copies with complete frontmatter and a summary opening, plus a pointer to the original vault path. The `COPY-MANIFEST.md` in this folder lists all twenty with their original paths, citation keys, and which primary papers cite them.

---

## arXiv Citations (`02-arxiv-citations/`)

`F0-ARXIV-SCAN-2026-05-24.md` is the scan that identified nine directly relevant arXiv preprints, ranging from Khushiyant et al. (2025) on phase transitions in LLM multi-agent systems (arXiv:2512.10166, ρ_c ≈ 0.230) to Pan et al. (2025) on LLM agent coordination.

`citations.bib` is the complete BibTeX file: 29 entries organized in two sections. Section 1 contains the nine arXiv papers. Section 2 contains twenty foundational references spanning Grasse (1959) on stigmergy, Lamport (1978) on time ordering in distributed systems, Merkle (1980) on hash trees, Nakamoto (2008) on the blockchain, and Park et al. (2023) on generative agent societies.

---

## Metric Snapshots (`03-metric-snapshots/`)

Twelve JSON files that provide the quantitative evidence for the whitepaper's empirical claims. Key files:

- `fast-evo-stigmergic-blackboard/baseline-T0.json` and `post-T1.json` — before and after evidence for the +9 propagation of the stigmergic-blackboard doctrine following the 07daafe0 wave.
- `refusal-cross-skill-propagation/baseline-T0.json` and `post-T1.json` — before and after evidence for the +6 cross-skill refusal propagation (2 to 8 lifecycle skills).
- `bulkhead-audit-2026-05-23.json` — four-bulkheads defense-in-depth status: bulkhead 1 (perimeter) active; bulkheads 2-4 not yet instrumented. Baseline for future hardening.
- `charter-schema-audit-2026-05-21.json` — charter schema enforcement constraints including the cluster_prefix exactly-3-items rule.

---

## Architecture Snippets (`04-architecture-snippets/`)

Seven files that provide the load-bearing technical excerpts:

- `shapes-registry.json` — full shapes registry with 21 entries, 9 expanded. This is the measurement substrate: each shape is a mechanically-detectable pattern of work with a target direction (increasing or decreasing), detector script, and history.
- `CANONICAL-SET-excerpt.md` — Column A and Column B tables from the completion-choice CANONICAL-SET, plus the Refusal-as-Composite section.
- `sample-signed-manifest.json` — a real Ed25519-signed agent manifest from the branch-maker wave (2026-05-25T163628Z), showing the full manifest schema including `coc_chain.parent_hashes`, `signer`, and `signed_by`.
- `coc-tail-last-20.jsonl` — the last 20 entries of `forensics/coc.jsonl` as of 2026-05-25T16:36:57Z, including two branch-merge entries with Ed25519 signatures.
- `branching-merkle-SKILL.md` — full copy of the branching-merkle skill: the FORK-WRITE-ROLLUP-MERGE-VERIFY lifecycle for parallel agent waves.
- `stigmergic-collab-SKILL.md` — full copy of the stigmergic-collab skill: the blackboard event grammar (STARTUP, CLAIM, COMPLETE, HANDOFF, REFUSE, channel_open) and the 07daafe0 worked example.
- `22-DECKER-AS-FULLSTACK-ATOM-excerpt.md` — excerpt from the canonical Decker doc covering the ontology, two-faces table, three trajectories, and compass hierarchy.

---

## COC Signing (`05-coc-of-this-bundle/`)

Contains the chain-of-custody manifest for this bundle assembly operation.

---

## Verification

To verify bundle integrity: run `sha256sum` on each file listed in `citations-manifest.json`. The `sha256` fields are marked `compute-on-verify` because hash computation was not available during assembly; the manifest structure is designed for post-assembly verification rather than pre-computed hash embedding.

No originals were modified. No files were committed to the faerie2 repo. This bundle is a read-only snapshot assembled for publication submission.
