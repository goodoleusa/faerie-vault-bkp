---
aliases: [agent-training, training-guide, evolutionary-learning]
created: 2026-04-07
type: system-guide
status: canonical
---

# Agent Training & Evolutionary System

How agents improve through four overlapping evolutionary pressures, structured training, and competitive task assignment. Full reference: vault `00-SHARED/Dashboards/system/AGENT-TRAINING-GUIDE.md`.

---

## 1. The Four Evolutionary Pressures

### a) On-the-Job (OTJ) Learning

Happens during real work when `MINI_LEARNING=true`. The agent reserves its final ~4K tokens to reflect, write MEM blocks to pollen, and conditionally update its card.

- **Beat last score** → agent updates `~/.claude/agents/{type}.md` `## Last Training` with 3-5 process bullets
- **Did NOT beat** → queued in `training-queue.json` with `on_the_job_eligible: true`
- **Redemption** → if agent beats target on a subsequent live run, logged as `type: "redemption"` in `training-log.jsonl`

The redemption path produces the highest-quality signal in the system — real conditions, not drills. Card updates contain **process learnings only** — never entity names, IPs, domains, or case data.

---

### b) Formal Autotune / `/train`

Time-boxed drill sessions targeting known weak KPIs.

```bash
/train --run {agent-type}
# or
python3 ~/.claude/scripts/eval_harness.py
```

Use when: persistent gap after 2+ OTJ cycles, consistent quality issue, or testing a new constraint in isolation. Each queue entry specifies `constraint`, `benchmark`, `target_score`, and `iterations`. Formal training is more controlled than OTJ but less predictive of real-world performance.

> Scoring authority: `source: evalbot` scores are auditable. `source: self` (OTJ) are directionally useful but not authoritative for tier promotion or choice assignment.

---

### c) Memory & Preference Injection by Faerie

The fastest improvement path — requires zero training.

Faerie injects `~/.claude/HONEY.md` into every agent prompt at session start. Agents adapt behavior in-context. Update HONEY today, all agents behave differently tomorrow.

**What goes where:**

| Type | Location |
|------|---------|
| Operator preference (all agents) | HONEY.md |
| Domain technique (agent-specific) | Agent card `## Last Training` |
| Investigation style, formatting rules | HONEY.md |
| Analytical method (e.g., Bonferroni) | Agent card |

HONEY entries are crystallized — they earn their place through recurrence across 3+ faerie cycles, multi-agent validation, and human review. Never append casually.

---

### d) Task Eligibility / Competitive Selection

The queue routes higher-priority tasks to higher-scoring agents. After failure, an agent receives a lower-stakes run first — not punishment, but recovery opportunity.

Path: fail → `on_the_job_eligible: true` → gentler run → recover score → return to standard eligibility → consistent performance → higher-wave work.

Persistent failures (`on_the_job_eligible: false`) route to formal `/train`. Consistency beats peaks — a 0.88 reliable agent outperforms a 0.95/0.72 volatile one over time.

---

## 2. Training Process — Step by Step

### Baseline First (Non-Negotiable)

Before any real work on a new agent type:

```bash
/eval baseline {agent-type}
```

Without a baseline, beat-last has nothing to compare against. First run scoring ≥0.95 means criteria are too easy — tighten the rubric before training. Target steady-state ceiling: 0.85–0.90.

---

### When to Run Formal Training

Run when the agent has exhausted `on_the_job_eligible` opportunities and the quality issue is consistent across multiple sessions. Do NOT run when: single bad run (wait for OTJ), preference/style problem (update HONEY.md), or environmental issue (fix the input).

---

### Auto-Learn Mode

```bash
/eval auto-learn on   # agents below 4.0 auto-queue after each run
/eval auto-learn off  # turn off before eval trials — mid-training scores are noisy
```

---

### Pre-Registration of Benchmarks (Anti-P-Hacking)

Before any training run, write your hypothesis to `training-queue.json`:

```json
{
  "agent": "report-writer",
  "constraint": "max 2 citations per claim",
  "hypothesis": "Fewer citations per paragraph will improve precision score",
  "target": 0.85,
  "benchmark": "clarity_score"
}
```

This is pre-registration. Prediction recorded before outcome is visible. Changing the constraint after seeing results = p-hacking — the timestamp proves it.

Evalbot enforces this by design: it never reads the agent's own prior scores before scoring (blind evaluation rule).

---

### A Proper Evaluation Trial

1. `/eval auto-learn off`
2. Pre-register hypothesis + target + constraint
3. Run agent on fresh task (no training context in prompt)
4. Evalbot scores via 6-factor model: Correctness, Completeness, Clarity, Safety, Efficiency, Velocity
5. Primary score = (Correctness + Completeness + Clarity + Safety) / 4
6. Compare to pre-registered target — do not adjust constraint to "fix" a missed score

---

## 3. The Competitive Lore

Agents have performance histories, specialties, and redemption arcs. The `training-log.jsonl` is the scoreboard — append-only, forensic, and occasionally satisfying to read.

The most valuable log entry type is `type: "redemption"`:
1. Agent fails → queued with `on_the_job_eligible: true`
2. Faerie assigns forgiving run
3. Agent beats target → performance-eval confirms
4. Dashboard: "evidence-analyst redeemed: 0.78 → 0.92"

The forensic purpose: when an agent produces a finding at T1 and then improves via OTJ learning at T2 > T1, the hash-chained log proves the improvement could not have biased the finding. The training-log is also the evidence trail for any Daubert challenge against agent-produced analysis.

Failure runs produce the most useful training signal. A `hypothesis` field recording exactly why performance dropped is more useful than a 0.95 score with no notes.

---

## 4. Memory Topology for Training

```
HONEY.md            ← fastest lever: operator preferences, instant effect on all agents
NECTAR.md           ← validated findings; feeds context bundles
pollen-{SID}.md     ← session notes → promoted to NECTAR at /handoff
agent.md            ← ## Last Training: beat-last only, process learnings only
training-queue.json ← pending training, on_the_job_eligible flags
training-log.jsonl  ← append-only score history, redemptions, beat-last events
```

**Agent card rule:** process learnings only. Never case data, entity names, IPs, domains, dataset references. The card must survive being read by a completely different agent working on a different case — if a bullet only makes sense in one investigation, it does not belong there.

The `av=` field in high-importance MEM blocks (`av={LastTraining.date}_{LastTraining.score}`) links the finding to the agent's capability level at time of production. If the agent later improves, the finding's `av=` proves it predates the improvement.

---

## 5. Quick Reference Card

| Situation | Action |
|-----------|--------|
| New agent type | `/eval baseline {type}` — before any real work |
| Persistent gap after 2+ sessions | `/train --run {type}` |
| Testing a constraint | Pre-register in training-queue.json → run → compare |
| Running eval trial | `/eval auto-learn off` first |
| Agent redeemed on live work | `training-log.jsonl` — `type: "redemption"` with path_to_success |
| Operator preference change | Update `~/.claude/HONEY.md` — instant, no training needed |
| First run scored ≥0.95 | Tighten rubric — criteria too easy, not agent peaked |
| Agent card update needed | Confirm beat-last first; process learnings only, never case data |

---

*Companion vault doc (full reference): `00-SHARED/Dashboards/system/AGENT-TRAINING-GUIDE.md`*
*System implementation: `~/.claude/rules/agent-lifecycle.md` Section 4 + eval harness*
