---
type: dashboard
status: active
tags: [dashboard, eval, quality, scores, dimensions]
parent: Dashboards/INDEX
up: Dashboards/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:558c82ec6dfc1292725506ec1b22fcae7365dde8c8c412af5c5154db8b16b848
hash_ts: 2026-04-25T01:10:52Z
hash_method: body-sha256-v1
---

> [↑ Dashboards](INDEX.md) · [⌂ Home](../../HOME.md)

# Eval Snapshot

Narrative interpretation of quality scores across eval dimensions.
For live data: `/dev-eval`

---

## The Four Dimensions

| Dim | Name | What it measures | Target |
|-----|------|-----------------|--------|
| T | Memory/Retention | HONEY/NECTAR retrieval accuracy; facts stay in corpus | 0.75 |
| M | Task quality | done_looks_like criteria match rate per task | 0.70 |
| R | Citation accuracy | findings-with-sources / total-findings | 0.75 |
| F | Model routing | Haiku at W1, Sonnet at W2 — cost efficiency | 0.80 |

---

## Composite Score

The composite is a weighted average. The exact weights are set in the eval harness.
Current target: **composite ≥ 0.75**.

Membench baseline (2026-04-16):
- Retention: 88/100
- Continuity: 100/100
- Work Efficiency: 15x baseline
- Overhead: 2.8% net
- Confabulation Rate: 0%

---

## Common Score Patterns

| Pattern | Diagnosis |
|---------|-----------|
| T low, M ok | NECTAR not being read at startup; agents starting cold |
| M low, T ok | done_looks_like criteria too vague OR agents not meeting them |
| R low (common) | Findings written without source citations |
| F low | W1 agents using Sonnet; W2 agents not using Sonnet for inference work |

---

## Improving Each Dimension

**T (Memory/Retention):**
- Read NECTAR tail-30 at agent startup
- Write pollen observations at task boundaries
- Run `/handoff` to promote pollen to NECTAR

**M (Task quality):**
- Ensure tasks have clear `done_looks_like` criteria in context_bundle
- Use performance-eval after each task run
- Address tasks scoring <0.70 (rework required)

**R (Citation accuracy):**
- Every finding must cite its source inline
- Format: `"Finding: [claim] [source/id]"`
- Target: 100% citation rate. Current baseline: ~11% (major gap)

**F (Model routing):**
- W1 agents must use Haiku (45s budget)
- W2 agents use Haiku (easy/bulk) or Sonnet (medium/hard)
- Explicit `model=` parameter in every Agent() call

---

## Dual-Task Hints

Actions that improve two dimensions simultaneously:

| Action | Improves |
|--------|---------|
| Write NECTAR with source citations | T + R |
| Tag spawns w1-/w2- in wave context | F + M |
| Read NECTAR at agent startup + apply techniques | T + M |

---

## Related

- [[system-health]] — full health snapshot
- [[../Skills-Reference/metrics]] — /metrics quick-ref
- [[../Skills-Reference/dev-eval]] — /dev-eval quick-ref
- [[../Glossary/terms]] — eval dimensions, composite score, beat-last defined
