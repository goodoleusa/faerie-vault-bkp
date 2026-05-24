# Benchmark Results

Results from pre-registered faerie evaluation hypotheses (started 2026-04-06).

## Hypothesis Status

| Hypothesis | Target | Status | Result File |
|-----------|--------|--------|------------|
| H-PERF-01: Orchestrated Haiku ≥ Sonnet on classification | precision@10 ≥ baseline, p<0.05 | PENDING | (run during T-3 sprint) |
| H-COST-01: faerie ≤ 60% cost of Sonnet | cost_ratio ≤ 0.60 | PENDING | (derived from H-PERF results) |
| H-MEM-01: HONEY reduces startup errors | error_rate < 0.50 × baseline | PENDING | (run during T-1 sprint) |
| H-LEARN-01: Beat-last improves monotonically | score_trajectory r > 0.70 | PENDING | (run during T-4 sprint) |
| H-PISTON-01: Waves > sequential | productivity ≥ 1.5× | PENDING | (run during T-5 sprint) |

## Files

- **H-PERF-01-results.md** — Primary benchmark: evidence classification (control vs treatment)
- **H-COST-01-results.md** — Cost efficiency analysis (derived from H-PERF data)
- **H-MEM-01-results.md** — Memory system evaluation (startup error rates)
- **H-LEARN-01-results.md** — Self-improvement trajectory (beat-last-score)
- **H-PISTON-01-results.md** — Wave vs sequential comparison (finding productivity)

## Pre-Registration Lock

All hypotheses, sample sizes, and win thresholds pre-registered 2026-04-06. See [EVAL-PREREGISTRATION.md](../EVAL-PREREGISTRATION.md) for immutable protocol.

Results will be updated as sprints T-1 through T-5 complete (estimated completion: 2026-05-06).

## Negative Results Welcome

If any hypothesis fails, the failure will be reported honestly:
- Full p-value, confidence intervals, effect size
- Confound audit (were controls maintained?)
- Open questions (what would we need to measure to resolve?)
- Faerie remains valuable even if cost-efficiency claim fails (proof of concept, architectural soundness)
