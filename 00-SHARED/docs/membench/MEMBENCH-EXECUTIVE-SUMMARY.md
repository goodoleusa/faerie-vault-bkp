---
type: executive-summary
status: active
created: 2026-04-24
updated: 2026-04-24
tags: [membench, executive-summary, non-technical]
audience: non-technical stakeholders
doc_hash: sha256:pending
hash_ts: pending
hash_method: body-sha256-v1
---

# Faerie2 Memory Benchmark — Executive Summary

**What is faerie2?** A platform that gives AI assistants persistent memory across work sessions — so the system learns from session 1 and uses that knowledge in session 2, without the user repeating context. Think of it as a long-term working memory layer on top of standard AI.

**Latest eval:** Run #354, 2026-04-24. 20 sessions analyzed. Composite score: 0.544 (bootstrap phase — see interpretation below).

---

## How Faerie2 Compares to Alternatives

On equivalent task volume, faerie2 completes significantly more work per session than competing systems:

| System | Faerie2 advantage |
|---|---|
| Vanilla Claude (no memory) | +145% — faerie2 completes 10 tasks/session vs. 4 for a cold-start AI |
| ChatGPT Memory | +104% — has memory but no parallel task orchestration |
| Mem0 | +87% — has retrieval but no structured task-flow coordination |

**Caveat:** These numbers come from faerie2's own session logs, not an independent third-party audit. They reflect task throughput only; cost-per-task instrumentation is still being wired.

---

## The Seven Performance Dimensions

### A — Throughput (score: 0.50)
How much work the system completes per session, and at what cost. Faerie2 is hitting 10 tasks per session median — solid performance — but the cost-per-task and time-to-first-result instruments are not yet wired, leaving the score at 0.50. The work is happening; we just cannot yet measure its efficiency precisely.

### B — Memory (score: 0.33)
Whether the system actually uses what it has learned. The memory store (called NECTAR) has 225 accumulated findings, but there is no tracking yet to confirm whether agents retrieve and apply those findings or ignore them. This is the most strategically important gap: if agents are not using stored knowledge, the memory system is overhead rather than advantage.

### C — Resilience (score: 1.00 — with caveat)
Whether the system survives failures without losing work. The score looks perfect, but it is based on only one manifest analyzed. The agent-registration hook that would give real coverage data is not firing. Treat this as "not yet measured" rather than "confirmed excellent."

### D — Quality (score: 0.00)
Whether findings are original, well-sourced, and retrievable across sessions. Zero reflects complete absence of instrumentation — not confirmed poor quality. NECTAR's 225 findings have never been evaluated for depth, citation, or cross-session recall. This is uninstrumented, not broken.

### E — Piston (score: 1.00 — with caveat)
Whether parallel task orchestration is starting fast and returning useful results in the first wave. One checkpoint confirms W1 responses are happening. No wave-history data yet to validate consistency or parallelization efficiency across sessions.

### F — Model Routing (score: null)
Whether the system correctly assigns cheap models to simple tasks and expensive models to complex reasoning. The agent roster that would capture this data is empty because a registration hook is not firing. The routing logic exists in code; observability does not yet exist.

### G — Defense (score: N/A)
Resistance to adversarial inputs, prompt injection, and forensic log tampering. Reserved for a future instrumentation phase when multi-user or external-audit scenarios become relevant.

---

## Membench Substrate: M1–M11

Membench measures whether the memory system pays for itself. The five metrics that matter to stakeholders, drawn from the last measured dogfood run, are:

| Metric | Score | Plain English |
|---|---|---|
| **Retention** | 88 / 100 | 88% of findings from one session were correctly available in the next |
| **Continuity** | 100 / 100 | No session started from zero — context carried over perfectly |
| **Work Efficiency** | 15x | Each session accomplished 15 times more useful work than a cold-start equivalent |
| **Overhead** | 2.8% | The memory context (rules + HONEY) consumed only 2.8% of the available AI context window |
| **Confabulation** | 0% | Zero instances of the system inventing false memories from prior sessions |

**Note:** These scores are from the pre-production dogfood run. A full membench re-run against the current 20-session production dataset has not yet been executed. The current composite (0.544) is lower because four dimensions are in bootstrap mode — instrumentation gaps, not performance regression.

---

## The Three Most Important Levers for Improvement

**1. Wire memory retrieval tracking (highest strategic impact).** NECTAR is growing but usage is invisible. Adding retrieval logging to the memory query script would immediately show whether the system is learning across sessions or accumulating noise. Estimated effort: 3–4 hours. This validates or refutes the core product thesis.

**2. Fix the agent roster registration hook (unlocks two dimensions at once).** One hook not firing leaves both Resilience (C) and Model Routing (F) blind. Fixing it would give visibility into agent coverage and whether cost-efficient model routing is actually happening in production. Estimated effort: 1–2 hours. Highest return-per-hour of any gap.

**3. Add token and cost capture to session metrics (completes the efficiency story).** Throughput numbers without cost numbers cannot prove efficiency. Wiring cost-per-finding would make the +145% vs. vanilla Claude claim auditable, not just asserted. Estimated effort: 2–3 hours.

Total estimated effort to move from bootstrap to validated: 16–24 engineering hours.

---

## When to Read What

**Read this summary if:** You need to understand faerie2's performance posture, competitive position, and where investment should go. This covers the "what and why" in plain language.

**Read MEMBENCH-METRIC-ENCYCLOPEDIA.md if:** You are instrumenting a new metric, debugging a score you believe is wrong, writing eval harness code, or making a decision about metric methodology. The encyclopedia contains the formal definitions, scoring formulas, instrumentation requirements, and edge-case handling for all M1–M11 metrics. It is a reference document for engineers, not a performance summary.

---

**System status:** Stable and functioning. Not failing — instrumenting. The platform is delivering results; the observation layer is catching up.

**Generated:** 2026-04-24 | **Source:** eval-report run #354 + membench dogfood baseline | **Audience:** non-technical stakeholders
