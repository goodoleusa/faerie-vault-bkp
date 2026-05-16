# Evaluation Test Sets

Pre-registered evaluation sets for faerie benchmarking. These are immutable gold standards—no post-hoc modification allowed.

## Files

- **evidence-classification-v1.json** — 100 evidence items for H-PERF-01 benchmark (prepared 2026-04-06, locked before any runs)
  - Schema: array of `{ id, content, H1_relevance, H2_relevance, ..., H5_relevance, expected_tier: 1|2|3 }`
  - Stratification: 20 items per hypothesis (H1–H5) to prevent H-bias
  - Adjudicated tier labels: expert panel consensus (3 independent evaluators)

## Benchmark Integrity

- All test sets committed to git BEFORE benchmark runs
- No peeking at accuracy during runs (use git to verify timestamp)
- Expert panel adjudication completed before runs
- Eval sets frozen (no post-hoc relabeling after seeing results)

See [EVAL-PREREGISTRATION.md](../EVAL-PREREGISTRATION.md) for full protocol.
