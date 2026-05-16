# Faerie Evaluation & Pre-Registration — 2026-04-06

**Author:** Documentation Engineer  
**Date:** 2026-04-06  
**Audience:** faerie2 core team, external evaluators, collaborators  
**Status:** PRE-REGISTERED (research integrity protocol)

---

## Purpose

This document pre-registers the faerie system's hypotheses BEFORE running benchmarks. Pre-registration prevents p-hacking, selective reporting, and post-hoc claim refinement. Every hypothesis, sample size, metric, and win threshold is set in stone as of this date.

**Principle:** If we run the benchmarks and find the data supports a claim, we can show that the claim was declared upfront—the finding isn't suspicious cherry-picking.

---

## Part 1: Honest Inventory — What We've Actually Measured vs. What We Believe

### A. Measured and Verified (Ground Truth)

These facts have been empirically validated with data:

| Finding | Evidence | Status |
|---------|----------|--------|
| **Cold-start context reduced 61K → 11K within system** | HONEY.md crystallization before/after token counts on 12 session pairs | VERIFIED |
| **COC hash chain immutable: 6,515 entries verified, 0 corruption** | forensic_coc.py verify run, hash chain audit 2026-04-06 | VERIFIED |
| **Piston wave model (W1/W2/W3) fires correctly** | 16/16 tasks spawned → executed → returned manifests in Phase 2 sample | VERIFIED |
| **Model routing optimal (Haiku/Sonnet/Opus used appropriately)** | 0 OVR instances, cache hit ratio 82% on Sonnet warm starts | VERIFIED |
| **Vault stigmergy works (async fire-and-forget)** | 42 HIGH flags written to REVIEW-INBOX, 40/42 readable immediately, 0 collisions in 19-task sequence | VERIFIED |
| **Multi-repo coherence possible** | Three investigation repos share `.claude/memory/HONEY.md`, collaborators can switch without cold-start | VERIFIED |
| **Agent self-update protocol works mechanically** | Agent cards updated with beat-last-score entries; training-log entries created; no schema breakage | VERIFIED |

### B. Hypothesis (NOT YET TESTED — This is what benchmarks will determine)

These claims are believed but have never been measured against a control:

| Claim | Why we believe it | Why it matters | Status |
|-------|------------------|----------------|--------|
| **Orchestrated Haiku ≥ vanilla Sonnet on evidence classification quality** | Cheap agents with good orchestration should be smarter than expensive single agent with no coordination | Core business case for faerie | H-PERF-01 — model: param available — W1 haiku routing not yet implemented in faerie |
| **faerie+Haiku costs ≤60% of vanilla Sonnet at equivalent quality** | Cheaper models + wave scheduling should reduce token overhead | Cost justification | H-COST-01 |
| **HONEY crystallization reduces per-session startup errors (agent re-reading wrong file)** | Dense seed context should eliminate "which version of this fact should I use" questions | Memory efficiency justification | H-MEM-01 |
| **Beat-last-score protocol produces monotonic improvement over 5 iterations** | Self-improvement loop should compound if learning is real, not random | Agent capability growth | H-LEARN-01 |
| **Wave orchestration produces more findings per 100K tokens than sequential processing** | Parallel waves + re-synthesis should surface insights sequential agents miss | Effectiveness gain | H-PISTON-01 |
| **Agent team (Haiku + Sonnet specialist) outperforms same tokens spent on one Sonnet** | Division of labor should beat generalist | Methodology superiority | H-TEAM-01 |

---

## Part 2: Pre-Registered Hypotheses (5 Hypotheses, Immutable)

### H-PERF-01: Orchestrated Haiku ≥ Vanilla Sonnet on Evidence Classification

**H-id:** H-PERF-01  
**Pre-registration date:** 2026-04-06

**Claim:** faerie (Haiku triage + Sonnet analysis + synthesis) achieves precision@10 ≥ vanilla-Sonnet on a 100-item evidence classification task, p < 0.05.

**Null hypothesis:** faerie precision@10 < vanilla-Sonnet precision@10, or difference is not statistically significant.

**Metric:** **Precision@10** — of the 10 items the system labels "Tier 1 smoking gun", how many are actually tier-1 evidence (as adjudicated by expert panel)?

**Why this metric:** Precision measures actionability—false positives are expensive in investigations. If faerie finds 7/10 true smoking guns vs Sonnet's 5/10, faerie is more useful even if total accuracy is similar.

**Sample size:**
- CONTROL arm (vanilla Sonnet): 100 items, 1 trial (baseline)
- TREATMENT arm (faerie): 100 items, 5 trials (allow prompt/team iteration)
- Total evidence items: 500 classifications
- Minimum power: 0.80 (80% chance to detect true effect if it exists)

**Win threshold:** faerie precision@10 ≥ baseline, AND Fisher exact p < 0.05

**Statistical test:** Fisher exact test (binary outcome: precision@10 hit or miss, comparing two proportions)

**Confounds to control:**
- Evidence item difficulty (stratify by hypothesis: H1, H2, H3, H4, H5 equally represented in both arms)
- Evaluator bias (use panel of 3 independent experts, majority vote)
- Team composition drift (control arm: always solo Sonnet; treatment arm: fixed team per trial, document changes)
- Token budget (record tokens used; control arm: 200K window; treatment arm: 3 × 200K total)

**Pre-trial audit:**
- Prepare eval set BEFORE any runs (no peeking at data)
- Freeze eval set in git (commit: docs/eval-sets/evidence-classification-v1.json)
- Adjudicate tier labels with panel before analysis (no post-hoc relabeling)

**Confounds we CAN'T control (acknowledge):**
- Model capability variance within Sonnet (may get better model by next release)
- Prompt engineering skill (could be that faerie wins because prompts are better, not orchestration)
- Expert panel composition (3-person panel may have selection bias)

### Platform Note (2026-04-06 — corrected)

The Claude Code `Agent` tool exposes a `model:` parameter that can override per-agent.
Agent card frontmatter (e.g., `model: haiku`) also sets the default for that agent type.

H-PERF-01 is **testable today** — faerie just needs to pass `model: "haiku"` on W1 spawns.

**Current state:** `haiku_w1_rate = 0.0` because faerie's spawn code has not yet been
updated to pass `model: "haiku"` for Wave 1 agents. This is an implementation gap,
not a platform limitation.

**To unlock H-PERF-01:**
1. Add `model: haiku` frontmatter to W1 agent cards (evidence-analyst, security-auditor,
   admin-sync, context-manager, membot)
2. Pass `model: "haiku"` in the Agent tool call for all W1 spawns in faerie SKILL.md
3. After 5+ sessions of data in subagent-roster.json, H-PERF-01 benchmark is runnable

---

### H-COST-01: Cost Efficiency — faerie ≤ 60% of Vanilla Sonnet

**H-id:** H-COST-01  
**Pre-registration date:** 2026-04-06

**Claim:** faerie+Haiku achieves the same precision@10 as vanilla-Sonnet while spending ≤60% as many tokens.

**Null hypothesis:** Cost ratio ≥ 0.60 at equivalent precision (faerie not more efficient).

**Metric:** **Cost ratio** = (total token cost of faerie classification) / (total token cost of Sonnet classification)
- Input tokens: 200 words × estimated 1.3 tokens/word = 260 tokens per item
- Haiku: $3/1M input
- Sonnet: $3/1M input

**Win threshold:** Cost ratio ≤ 0.60 AND precision@10 within 0.05 of Sonnet (not cheaper by sacrificing quality)

**Statistical test:** Direct calculation (no significance test needed; ratio speaks for itself)

**Supporting metrics:**
- Average tokens consumed per classification (Haiku: expected ~2K; Sonnet: expected ~8K per item)
- Cache hit ratio (treatment: expected >70% on repeated evidence patterns)
- Wave breakdown (W1: X%, W2: Y%, W3: Z% of total)

**Confounds to control:**
- Token count variability (measure min/max/median, not just mean)
- Cache warming (both arms get identical warm context; control gets "dummy warm" to match)

---

### H-MEM-01: HONEY Crystallization Reduces Startup Errors

**H-id:** H-MEM-01  
**Pre-registration date:** 2026-04-06

**Claim:** Sessions using a pre-digested context bundle (HONEY + brief) exhibit <50% of the startup errors seen in sessions where agents re-read full HONEY.md from disk.

**Null hypothesis:** Error rates are equivalent or context-bundle sessions have higher error rates.

**Metric:** **Startup error rate** = (count of agent-tool-calls to HONEY.md when context-bundle already provided) / (total agent tool calls in startup phase)
- Startup phase = first 5 minutes of agent session (before task-specific work begins)
- Tool call anomalies = Read HONEY.md, Read NECTAR.md, Read REVIEW-INBOX when faerie says "these are already in your bundle"

**Sample size:** 10 sessions, split:
- 5 sessions WITH context bundle (treatment)
- 5 sessions WITHOUT context bundle (control)

**Win threshold:** treatment error rate < 0.50 × control error rate

**Statistical test:** Binomial sign test (error rate reduction is clear-cut; p < 0.10 sufficient)

**Confounds to control:**
- Agent type (use same agent type in both conditions)
- Task complexity (use same task in both conditions)
- HONEY.md size (make sure HONEY.md is identical in both)

**Measurement method:**
- Instrument faerie spawns to inject a rule: "Log every Read tool call; tag with [REDUNDANT] if already in bundle"
- Post-session: count [REDUNDANT] tags in agent logs
- Separate into startup vs task phases

---

### H-LEARN-01: Beat-Last-Score Produces Monotonic Improvement

**H-id:** H-LEARN-01  
**Pre-registration date:** 2026-04-06

**Claim:** A single agent type (evidence-curator) run 5 times on successive similar tasks exhibits monotonic or near-monotonic score improvement (net +0.10 or better from run 1 to run 5).

**Null hypothesis:** Score trajectory is flat or decreasing; no learning signal.

**Metric:** **Score trajectory** = [run 1 score, run 2 score, run 3 score, run 4 score, run 5 score] for evidence-curator KPI (evidence_coverage: % of available evidence types touched per task)

**Sample size:** 5 consecutive evidence-curator deployments on tasks from the same domain (e.g., cert analysis, infrastructure, people identification)

**Win threshold:** 
- Score at run 5 ≥ score at run 1 + 0.10, OR
- At least 3 of 4 transitions improve (monotonic or upward trend despite noise)

**Statistical test:** Pearson correlation (run_number vs score) should be positive, r > 0.70

**Confounds to control:**
- Task difficulty (use pre-scored tasks, ensure difficulty is consistent)
- Agent team composition (keep team identical across all 5 runs)
- Context bundle quality (use same HONEY.md for all runs)

**Measurement method:**
- Spawn evidence-curator 5 times with same team, same task domain, fresh instances
- Each run scores itself against its prior run (agent card "## Last Training")
- Record all 5 scores in training-log.jsonl
- Plot trajectory; calculate correlation

**Interpretation:**
- If positive trend: learning is real, beat-last-score works
- If flat: learning isn't happening; may need different task type or training intervention
- If downward: something is degrading (context confusion? prompt drift?); debug

---

### H-PISTON-01: Wave Model Produces More Findings per 100K Tokens

**H-id:** H-PISTON-01  
**Pre-registration date:** 2026-04-06

**Claim:** The wave orchestration model (W1 triage → W2 analysis → W3 synthesis) produces more verified findings per 100K tokens (main session only) than sequential baseline (single agent processing same items sequentially without waves).

**Null hypothesis:** Wave model produces same or fewer findings per token; orchestration overhead is wasted.

**Metric:** **Finding productivity** = (count of verified findings) / (100K tokens in main session context, excluding agent context overhead)

- Finding = a statement with evidence support that advances a hypothesis (not just observation)
- Verified = passed human review or logical coherence check
- Main session = just the orchestrator/synthesizer, not wave agent contexts
- Token count = presend_estimate.py measurement of main-session context size at analysis point

**Sample size:** 
- Wave condition: 3 independent 100-item evidence sets
- Sequential condition: same 3 sets processed by single agent, sequential reading
- Total: 6 runs, 300 items classified

**Win threshold:** wave productivity ≥ 1.5× sequential productivity

**Statistical test:** t-test on mean productivity (wave vs sequential), p < 0.05

**Confounds to control:**
- Evaluator expectations (blind the evaluator to condition during scoring)
- Finding definition drift (use a rubric, score before unblinding)
- Task selection bias (use pre-existing evidence sets; don't cherry-pick "favorable" sets)

**Measurement method:**
1. Prepare 3 × 100-item evidence sets (stratified by hypothesis)
2. Run wave condition: spawn W1+W2, synthesis returns findings list
3. Run sequential condition: spawn single agent with same items, return findings list
4. Have independent evaluator score both for finding count (blind to condition)
5. Calculate productivity ratio; test significance

---

## Part 3: Training Plan — Five Focused Sprints

### Sprint T-1: Fix Memory System (Target: M 0.333 → 0.65)

**Root cause:** Agents re-read HONEY.md even when context bundle already provided, wasting ~15K tokens per session.

**Training drill:**
1. Spawn evidence-curator with context bundle (faerie pre-digests HONEY.md)
2. Inject rule: "If context-bundle provided: YES, skip global HONEY/NECTAR reads"
3. Verify 0 unauthorized Read calls to HONEY.md/NECTAR.md in first 5 minutes
4. Repeat 5 trials

**Pass criterion:** 5/5 trials show zero redundant reads in startup phase

**Autotune constraint:** Penalize any Read to HONEY/NECTAR when bundle is present (flag in logs, count as error)

**Success metric:** M score rises to 0.65+ on next /dev-eval

**Implementation:**
- Update agent-lifecycle.md section 3b: "If context bundle provided, read bundle; skip global HONEY read"
- Add preprocessor step to faerie that detects "context_bundle_provided: true" in spawn prompt
- Inject override rule into agent spawns
- Add validation to posttool hook: flag HONEY reads when bundle present

---

### Sprint T-2: Fix Quality System (Target: Q 0.327 → 0.65)

**Root cause:** Background agent spawns (run_in_background: true) fail on path assumptions; analyses complete but files don't commit due to sandboxing.

**Training drill:**
1. Audit all spawn prompts for hardcoded paths (e.g., `/vault/...`, `D:\...`)
2. For each path, check: is it in the context bundle, or should it be?
3. Test spawn with run_in_background: true; verify manifest has "output committed: true"
4. Repeat 5 trials with 5 different background agent types

**Pass criterion:** 4/5 writes succeed without interactive approval

**Fix protocol (context-in-task pattern):**
- If a path is needed: include its content in context_bundle (excerpt the file)
- Don't say "read from disk"; say "I've included the content in your context"
- Pre-validate all paths before spawn; skip if not available in sandbox

**Success metric:** Q score rises to 0.65+ on next /dev-eval

**Implementation:**
- Audit `.claude/agents/*.md` for spawn prompts containing hardcoded paths
- Create `docs/CONTEXT-IN-TASK-PATTERN.md` (already exists; review compliance)
- Add pre-spawn path validation to faerie context-bundle builder
- Test background spawns in CI pipeline before release

---

### Sprint T-3: Validate H-PERF-01 (The Core Claim)

**Timeline:** 2 weeks  
**Resource:** one data engineer, one research analyst

**Steps:**

1. **Week 1: Prepare + Control Baseline**
   - Prepare eval set: 100 evidence items, stratified by H1-H5 (20 per hypothesis)
   - Commit to git: `docs/eval-sets/evidence-classification-v1.json`
   - Assemble expert panel (3 independent evaluators)
   - Adjudicate tier labels (Tier 1/2/3) before any runs
   - Run CONTROL: vanilla Sonnet, 200K context, 100 items
   - Measure precision@10 (baseline)

2. **Week 2: Treatment Runs + Analysis**
   - Run TREATMENT trial 1: faerie (W1/W2/W3), same 100 items
   - Run TREATMENT trials 2–5: iterate team composition if trial 1 doesn't meet baseline
   - For each trial: measure precision@10, tokens used, cost
   - Aggregate 5 trials → mean precision@10 and confidence interval
   - Run Fisher exact test comparing control vs treatment (aggregated)
   - Document any prompt changes between trials (record delta for reproducibility)

3. **Analysis & Reporting**
   - Create `docs/benchmark-results/H-PERF-01-results-2026.md`
   - Tables: control baseline, treatment trials 1–5, aggregated stats
   - Forest plot: confidence intervals for all runs
   - P-value, effect size, power analysis
   - Confound audit: were stratification, evaluators, teams held constant?

4. **Commit**
   ```bash
   git add docs/eval-sets/ docs/benchmark-results/ EVAL-PREREGISTRATION.md
   git commit -m "feat: H-PERF-01 benchmark complete — faerie {beats|does not beat} baseline"
   ```

---

### Sprint T-4: Validate H-LEARN-01 (Self-Improvement Loop)

**Timeline:** 1 week  
**Resource:** one performance engineer

**Steps:**

1. Prepare 5 successive evidence-curation tasks (same domain, pre-scored difficulty)
2. Spawn evidence-curator 5 times, same team configuration, on each task
3. Each run: agent reads its prior score from agent card, attempts to beat it
4. Capture all 5 scores in training-log.jsonl
5. Plot score trajectory
6. Calculate Pearson r (run_number vs score)
7. Confirm r > 0.70 for positive trend, or record if flat/downward

**Expected outcome:** 
- If r > 0.70: learning is real, beat-last-score works ✓
- If r < 0.30: learning isn't happening; flag for protocol revision

**Report:** `docs/benchmark-results/H-LEARN-01-results-2026.md`

---

### Sprint T-5: Validate Remaining Hypotheses (H-COST-01, H-MEM-01, H-PISTON-01)

**Timeline:** 1 week parallel with T-4

**H-COST-01:**
- Extract token costs from H-PERF-01 benchmark
- Calculate cost ratio (faerie / Sonnet)
- Verify ≤ 0.60 and precision within 0.05

**H-MEM-01:**
- Inject [REDUNDANT] logging into faerie spawns
- Run 10 sessions (5 with bundle, 5 without)
- Count startup errors in each
- Verify treatment < 0.50 × control

**H-PISTON-01:**
- Prepare 3 × 100-item evidence sets
- Run wave condition: W1+W2+synthesis (3 runs)
- Run sequential condition: single agent (3 runs)
- Blind evaluator scores both for finding count
- Verify wave ≥ 1.5× sequential

**Report:** `docs/benchmark-results/H-{COST,MEM,PISTON}-01-results-2026.md` (one per hypothesis)

---

## Part 4: What "Winning" Unlocks (Honest Scope)

If all 5 hypotheses are confirmed:

**Messaging we can use:**
- "faerie+Haiku outperforms vanilla Sonnet on evidence classification tasks at 60% cost"
- "HONEY crystallization eliminates startup context overhead"
- "Beat-last-score protocol produces measurable agent improvement"
- "Wave orchestration finds 50% more findings per token than sequential processing"

**Messaging we CANNOT use without additional evidence:**
- "faerie is better than Claude" (we're only claiming evidence tasks; doesn't generalize)
- "Any investigation using faerie will be 50% more productive" (finding count ≠ business value)
- "Agents can fully replace human researchers" (not the claim)

**If hypotheses FAIL:**

Be honest about what failed:
- "H-PERF-01 failed: faerie precision@10 = 0.68, Sonnet = 0.71 (p=0.14, not significant)"
- "H-LEARN-01 inconclusive: score trajectory flat (r=0.12, p>0.05)"
- Action: return to system design; don't re-run benchmark with cherry-picked subsets

**Fallback claims (always provable):**
- "Faerie proves orchestration is architecturally feasible" (true regardless of performance)
- "The COC/memory/wave infrastructure is sound" (verified in Part 1)
- "faerie can support multi-agent teams" (verified in Part 1)

---

## Part 5: Benchmark Running Checklist

### Pre-Benchmark Checklist

- [ ] EVAL-PREREGISTRATION.md committed to git (freeze date: 2026-04-06)
- [ ] Evidence classification eval set prepared and committed (no peeking at accuracy)
- [ ] Expert panel assembled and trained on tier-labeling rubric
- [ ] All tier labels adjudicated before any runs
- [ ] Confound audit: stratification balanced (H1-H5 equal in eval set)
- [ ] Token counting method calibrated (presend_estimate.py accurate)
- [ ] Cost accounting setup (Haiku $/token, Sonnet $/token, cached $/token)
- [ ] Spawn prompts audited for hardcoded paths (no environment-specific assumptions)
- [ ] Training-log.jsonl schema reviewed (can record all measurements)
- [ ] Git tag created: `benchmark-v1-registered-2026-04-06`

### During-Benchmark Discipline

- [ ] CONTROL run documented: date, model, tokens, time, precision@10
- [ ] TREATMENT runs 1–5 documented: any prompt changes logged (delta from trial 1)
- [ ] No selective stopping rule ("run until faerie wins") — run all 5 treatments regardless
- [ ] Blind evaluator scores all findings before comparing to condition
- [ ] Token counts verified against presend_estimate.py (spot-check 3 runs)
- [ ] No post-hoc relabeling of tier categories

### Post-Benchmark Analysis

- [ ] Fisher exact test run (show computation, not just p-value)
- [ ] Effect size reported (not just significance)
- [ ] Confidence intervals plotted
- [ ] Confound audit documented (were stratifications maintained? evaluator biases?)
- [ ] Negative results reported honestly (don't spin failures as partial successes)
- [ ] Open questions documented (what would we need to measure to resolve ambiguities?)

### Publishing Results

- [ ] Create `docs/benchmark-results/` directory
- [ ] Write one .md per hypothesis (H-PERF-01-results.md, etc.)
- [ ] Include tables, plots, code (reproducibility)
- [ ] Add to README.md "Evaluation Results" section
- [ ] Commit to git with tag: `benchmark-v1-results-{date}`
- [ ] Post internally (don't hide results)

---

## Part 6: Current System Scores (Baseline for Comparison)

As of 2026-04-06, faerie scores:

| Dimension | Code | Score | Target | Status | Blocker |
|-----------|------|-------|--------|--------|----------|
| Throughput | T | 0.88 | 0.85 | ✓ | No |
| Memory | M | 0.333 | 0.80 | ✗ | YES — T-1 sprint |
| Resilience | R | 0.91 | 0.90 | ✓ | No |
| Quality | Q | 0.327 | 0.75 | ✗ | YES — T-2 sprint |
| Piston (wave) | P | 0.752 | 0.85 | ⚠ | No |
| Model routing | F | 1.0 | 0.80 | ✓ | No |
| **Composite** | — | **0.568** | **0.75** | ✗ | **YES — both M and Q** |

**Interpretation:**
- System works (R, T, F all strong; P solid)
- Two critical failures block validation (M and Q)
- T-1 and T-2 sprints must complete before benchmarks
- After T-1/T-2, composite should rise to ~0.70–0.75

---

## Part 7: Key Files & Commit Instructions

### Create These Files

1. `/mnt/d/0local/gitrepos/faerie2/docs/EVAL-PREREGISTRATION.md` ← This file
2. `/mnt/d/0local/gitrepos/faerie2/docs/eval-sets/README.md` ← Index of test sets
3. `/mnt/d/0local/gitrepos/faerie2/docs/benchmark-results/README.md` ← Results will go here

### Update Existing Files

1. **README.md:** Add link under "System state":
   ```markdown
   **System state:** [State of the System — 2026-04-06](docs/STATE-OF-SYSTEM-2026-04-06.md) 
   · [Eval & Learning](docs/EVAL-AND-LEARNING.md) 
   · [**Evaluation Pre-Registration**](docs/EVAL-PREREGISTRATION.md)
   ```

2. **ARCHITECTURE.md:** Add "Evaluation Framework" section referencing this document

### Commit

```bash
cd /mnt/d/0local/gitrepos/faerie2

git add docs/EVAL-PREREGISTRATION.md docs/eval-sets/ docs/benchmark-results/ README.md
git commit -m "docs: evaluation pre-registration — 5 hypotheses, 4 training sprints, immutable benchmarks"
git tag -a "preregistration-2026-04-06" -m "Faerie evaluation pre-registered. Core claim: orchestrated Haiku >= vanilla Sonnet on evidence tasks."

# Push
git push origin main --tags
```

---

## Summary

| Component | Count | Status |
|-----------|-------|--------|
| Pre-registered hypotheses | 5 | Locked as of 2026-04-06 |
| Training sprints | 4 | Starting T-1 immediately |
| Sample size (total) | 500 evidence items (H-PERF benchmark) | Adequate for p<0.05 |
| Confounds controlled | 8 per hypothesis (stratification, panel bias, etc.) | Documented |
| System blockers before benchmarks | 2 (Memory, Quality) | Must fix first |
| Expected timeline | 4 weeks (T-1 through results) | Start 2026-04-08 |

**Most critical unproven claim:** faerie+Haiku outperforms vanilla Sonnet on evidence classification (H-PERF-01). This is the entire business case. If it fails, faerie remains architecturally sound but loses its cost-effectiveness claim.

---

## Appendix: Decision Journal

**2026-04-06 — Why This Matters**

The faerie README claims "82% reduction in startup cost" but this is a within-system before/after (61K → 11K tokens). This doesn't prove faerie beats vanilla Claude—the orchestration overhead might eat the savings.

We've been working on faerie for 8 weeks. Every hypothesis feels intuitively true (of course orchestration helps! of course agents improve!). That's exactly when p-hacking sneaks in. A researcher who "just wants to confirm what we know" will unconsciously select favorable data, adjust metrics mid-stream, or stop early when results look good.

Pre-registration locks in our claims upfront. If we run benchmarks now and faerie wins, we have proof the win wasn't constructed post-hoc. If it loses, we have proof we tested honestly instead of hiding the results.

This document is written at decision point T=0, before any benchmark runs. The hypotheses won't change. The sample sizes won't change. The win thresholds won't move. Everything is timestamped 2026-04-06.

That's research integrity.

