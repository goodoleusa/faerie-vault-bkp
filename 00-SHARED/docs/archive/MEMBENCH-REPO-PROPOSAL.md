---
type: proposal
status: draft
created: 2026-04-17T05:00:00Z
tags: [membench, benchmark, governance, open-standard]
parent: "[[../README.md]]"
up: "[[../README.md]]"
child: []
same: []
doc_hash: sha256:pending
hash_ts: 2026-04-17T05:00:00Z
hash_method: body-sha256-v1
---

> [↑ Root](../README.md) · [⌂ Docs Index](./README.md)

# Proposal: MEMBENCH as Its Own Repository

## TL;DR

Extract MEMBENCH (the metric spec + reference implementation) from its current in-tree home (`~/.claude/scripts/eval_membench.py`) into a dedicated `membench/` repository. The benchmark governs no single implementation; the implementation vendors the reference code. This separation is what lets MEMBENCH credibly score any multi-agent orchestration system, not just this one.

## Why separate

Benchmarks live apart from the tools they measure. MMLU is not in the GPT repo. HumanEval is not in OpenAI's codebase. GAIA stands apart from its submitter systems. The structural reason: a benchmark authored inside the tool it scores reads as marketing. Separation is what transforms "our tool measures well" into "our tool's measurements can be independently verified."

## What makes MEMBENCH different from existing agent benchmarks

The current field (AgentBench, GAIA, SWE-bench, τ-bench, SALAD, etc.) shares one blind spot: **sparse instrumentation is silently rewarded**. A system that populates 3 of 14 metrics scores on the 3, as if the other 11 didn't exist. The tool appears strong because the weak parts are invisible.

MEMBENCH v0.2 introduces **M10 (instrumentation coverage) as a multiplier**, not an addend. This is a small change with large implications:

- A system with 60% coverage scoring 0.90 on populated metrics produces composite = 0.54, not 0.90
- The penalty is proportional and honest
- It cannot be gamed without actually instrumenting
- The metric is self-documenting — low M10 means "build more thermometers"

Pair this with **M9 (ceiling-hit)** and **M11 (bootstrap-exit veto)** and the benchmark has structural defenses against three common score-inflation failure modes: saturation not detected, sparse coverage hidden, premature promotion.

## Proposed repo structure

```
membench/
├── README.md                    — what MEMBENCH is, why it exists
├── SPEC.md                      — metric definitions, composite formula, versioning
├── CHANGELOG.md                 — v0.1 → v0.2 transitions, rationale per change
├── CONTRIBUTING.md              — how to propose new metrics, dispute scores
├── LICENSE                      — likely Apache-2.0 (permissive for benchmarks)
├── reference/
│   ├── eval_membench.py         — canonical metric computation
│   ├── eval_harness.py          — runner (system-agnostic)
│   └── schemas/
│       ├── submission.json      — score submission JSON schema
│       └── metric-contract.json — per-metric input contract
├── examples/
│   ├── README.md                — "how to score your system"
│   ├── faerie-submission-2026-04-17.json
│   └── minimal-system-stub.py   — smallest legal submission
├── leaderboard/
│   ├── README.md                — how entries get added/verified
│   └── 2026-04/
│       └── submissions.jsonl    — append-only verified entries
└── tests/
    └── test_selftest.py          — runs the internal selftest fixtures
```

## Submission schema (sketch)

```json
{
  "$schema": "https://membench.org/schemas/submission-v0.2.json",
  "system": "faerie|autogen|crewai|custom",
  "system_version": "1.0",
  "membench_version": "0.2",
  "run_date": "2026-04-17T05:00:00Z",
  "run_environment": "WSL2/Ubuntu 22.04/Python 3.13",
  "composite": {
    "additive": 0.78,
    "adjusted": 0.65,
    "formula_version": "v0.2",
    "veto_fired": false
  },
  "dimensions": {
    "T": 1.00, "M": 0.88, "R": 1.00, "Q": 0.70,
    "P": 0.80, "F": 0.65, "M3_is_estimate": 0.60,
    "M9_ceiling_hit": 0.786,
    "M10_instr_coverage": 0.85,
    "M11_bootstrap_exit": 0.95
  },
  "evidence": {
    "raw_logs_cid": "bafy...ipfs-cid",
    "hash_chain_root": "sha256:...",
    "artifacts_manifest": "https://...",
    "independently_verifiable": true
  },
  "notes": "optional human-readable context"
}
```

**The `evidence` block is mandatory.** A submission without verifiable raw logs is a claim. With them, it is a measurement. This is the rule that distinguishes MEMBENCH from self-reported benchmarks.

## Migration plan

1. **Phase 0 (now):** Vendored copy in `faerie2/scripts/eval/` — reference state for comparison (done 2026-04-17).
2. **Phase 1 (next):** Create `membench/` repo at `github.com/goodoleusa/membench` (or a neutral org name). Copy canonical files. Publish SPEC.md v0.2 as first tagged release.
3. **Phase 2:** faerie2 vendors `membench` as a git submodule in `vendor/membench/`. CI runs selftest from the submodule.
4. **Phase 3:** Publish first submission (this system's score, with evidence). Document verification process.
5. **Phase 4:** Open for external submissions. Add submission-verifier CI (rehashes evidence, validates schema, rejects unverifiable).

## Open questions for human decision

- **Repo name:** `membench` or longer (`multi-agent-membench`, `orchestration-bench`)?
- **Hosting:** personal org, neutral org (e.g., new `membench-org` GitHub), or donate to an existing foundation?
- **Governance:** BDFL, steering committee, or fully community-driven from day one?
- **Veto threshold calibration:** M11 at 0.70 is the current cut — should first external submissions help calibrate?
- **Metric additions:** should v0.3 add M12 challenge-engagement rate (proposed earlier in notes)?

## Why now

The MEMBENCH v0.2 spec is the moment the benchmark transitioned from a diagnostic-only tool (look at our numbers) to a governance-capable framework (honest multiplier + veto). If it stays in-tree past this point, the separation cost grows — every new metric requires synchronized releases, and the "tool-judges-itself" optics compound.

The right time to extract is **before the first external submission**, not after.

---

*Status: draft proposal, 2026-04-17. Decision pending human review.*
