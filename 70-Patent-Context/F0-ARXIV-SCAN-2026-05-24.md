# F(0) Gap — arXiv Research Scan, 2026-05-24

**Executive summary.** Nine arXiv papers from 2025-2026 map directly onto swarmy's remaining f(0) gaps: stigmergic environment-trace coordination (gaps 1, 6), label-free process reward modeling (gap 2), adaptive chain-of-thought compression (gap 3), lifelong semantic memory consolidation (gap 4), trajectory anomaly detection without operator triage (gap 5), and behavioral-drift quantification with routing-aware mitigation (gap 5). Together they outline a tractable 18-month implementation agenda; none require model fine-tuning — all can be layered as hooks, scripts, or MCP middleware over the existing infrastructure.

---

## Papers

| # | Title | Author | arXiv ID | Date |
|---|-------|---------|----------|------|
| P1 | Emergent Collective Memory in Decentralized Multi-Agent AI Systems | Khushiyant | [2512.10166](https://arxiv.org/abs/2512.10166) | 2025-12-10 |
| P2 | SwarmSys: Decentralized Swarm-Inspired Agents for Scalable and Adaptive Reasoning | Ruohao Li | [2510.10047](https://arxiv.org/abs/2510.10047) | 2025-10-11 |
| P3 | AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems | Yingxuan Yang | [2504.00587](https://arxiv.org/abs/2504.00587) | 2025-04-01 |
| P4 | Process Reward Models for LLM Agents: Practical Framework and Directions | Sanjiban Choudhury | [2502.10325](https://arxiv.org/abs/2502.10325) | 2025-02-14 |
| P5 | Reasoning Efficiently Through Adaptive Chain-of-Thought Compression (SEER) | Kerui Huang | [2509.14093](https://arxiv.org/abs/2509.14093) | 2025-09-17 |
| P6 | SimpleMem: Efficient Lifelong Memory for LLM Agents | Jiaqi Liu | [2601.02553](https://arxiv.org/abs/2601.02553) | 2026-01-29 |
| P7 | Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems | Abhishek Rath | [2601.04170](https://arxiv.org/abs/2601.04170) | 2026-01-07 |
| P8 | Trajectory Guard: Lightweight, Sequence-Aware Real-Time Anomaly Detection | Laksh Advani | [2601.00516](https://arxiv.org/abs/2601.00516) | 2026-01-02 |
| P9 | Explainable Safeguarding of LLM MAS via Bi-Level Graph Anomaly Detection (XG-Guard) | Junjun Pan | [2512.18733](https://arxiv.org/abs/2512.18733) | 2025-12-21 |

---

## Findings

### P1 — Emergent Collective Memory in Decentralized Multi-Agent AI Systems

*Contribution:* Proves stigmergic coordination via persistent environmental traces dominates individual-agent memory in large swarms, with a measurable phase-transition at critical agent density (ρ_c ≈ 0.230) beyond which trace-based coordination outperforms individual memory by 36-41%.

*F(0) gaps:* Gap 1 (autonomous mission discovery), Gap 6 (stigmergic coordination).

*Swarmy action:* The paper's multi-category environmental trace schema maps onto swarmy's manifest structure. `scripts/2e_discovery_frontier_cache.py` currently caches manifest paths but doesn't score trace density. Add a density probe: once in-flight agents exceed ρ_c, the cache should trigger a trace-consolidation pass rather than spawning more agents. The manifest `bearing` field is the existing trace encoding — add a `trace_strength` float (decays over time, reinforced on successful completion) to `scripts/1b_manifest_loader.py`. Gives the swarm the feedback loop that enables convergence behavior.

### P2 — SwarmSys: Decentralized Swarm-Inspired Agents

*Contribution:* Three-role closed-loop cycle (Explorer, Worker, Validator) with pheromone-inspired reinforcement — validated traces strengthen future probabilistic task matching; ineffective traces decay — achieving dynamic task allocation without global supervision.

*F(0) gaps:* Gap 1, Gap 6.

*Swarmy action:* Swarmy's NAVIGATOR / MAKER / BRIDGE / DEEP-DIVER taxonomy maps cleanly onto Explorer / Worker / Validator. Wire `scripts/3a_emergence_metrics.py` to emit per-manifest `reinforcement_signal` (1.0 on successful 6-choices completion, 0.0 on task abandonment, decaying by 0.9/day). `scripts/6g_frontier_index.py` reads this to weight task-matching probability during the frontier scan. No new abstraction — only new fields on existing data structures.

### P3 — AgentNet: Decentralized Evolutionary Coordination

*Contribution:* DAG-structured agent network with retrieval-based memory enabling continuous skill refinement and fault-tolerant task routing with no central orchestrator.

*F(0) gaps:* Gap 1.

*Swarmy action:* AgentNet's DAG topology is structurally identical to swarmy's mission graph compass edges. The novel piece is retrieval-based skill refinement per node — each agent maintains a compact skill-profile updated after every task. Wire `scripts/3g_kb_promote.py` to append a skill-delta record (task type, outcome, bearing chain used) per session. `scripts/4e_charter_term_index.py` can index these for retrieval during spawn, pre-seeding each spawned agent with skill context that primes it to the correct compass bearing without operator instruction.

### P4 — Process Reward Models for LLM Agents

*Contribution:* AgentPRM uses lightweight Monte Carlo rollouts for process-level reward targets at each reasoning step; InversePRM extracts reward signals from demonstration trajectories without explicit outcome labels — both eliminate human-in-the-loop annotation.

*F(0) gaps:* Gap 2 (self-evaluating quality / mutation discipline).

*Swarmy action:* `scripts/5a_mutation_baseline_capture.py` and `5b_mutation_measure_post.py` currently require a human to declare mutations beneficial or harmful. Implement InversePRM-style reward inference: treat all `forensics/` manifests with `status=completed` as demonstration trajectories. `scripts/3b_eval_baseline_runner.py` can replay each manifest's `discovered_work[]` chain and score intermediate steps against final outcome. Regression = negative process reward = automatic rollback flag before human verdict.

### P5 — SEER: Adaptive Chain-of-Thought Compression

*Contribution:* Best-of-N sampling with task-aware adaptive filtering; pre-inference output analysis dynamically sets compression thresholds, achieving 42.1% CoT length reduction while improving accuracy on SWE tasks.

*F(0) gaps:* Gap 3 (crystallization trajectory — spray → tighten).

*Swarmy action:* SEER's pre-inference threshold gate maps to W1/W2/W3 piston-wave transitions. In `deploy/mcp-server/swarmy_condenser.py`, add a compression step that fires when context fill crosses W2 threshold (65%). Measure current manifest verbosity (token count of `rationale` + `dashboard_line`), apply SEER threshold filtering to truncate to 80-char dashboard_lines. Automates the "tighten" phase of spray-tighten-crystallize without operator pruning.

### P6 — SimpleMem: Efficient Lifelong Memory

*Contribution:* Three-stage pipeline — semantic structured compression converts interactions to indexed memory units; online semantic synthesis consolidates within-session context; intent-aware retrieval plans reads. 30× token reduction and +26.4% F1 on recall.

*F(0) gaps:* Gap 4 (pollen → NECTAR → HONEY promotion without operator selection).

*Swarmy action:* SimpleMem's online semantic synthesis is exactly the pollen→NECTAR promotion step swarmy is missing. Wire `scripts/3h_summarizer_agent.py` to run SimpleMem's consolidation heuristic at session end: cluster all `forensics/ephemeral/{date}/` pollen entries by mission field, apply semantic deduplication, and emit candidate NECTAR entries to `REVIEW-INBOX` (preserving HONEY write-protection). Operator burden shifts from choosing what to promote to approving pre-consolidated candidates — much lower friction.

### P7 — Agent Drift: Quantifying Behavioral Degradation

*Contribution:* Agent Stability Index (ASI) — composite metric across 12 dimensions — paired with three mitigation strategies: episodic memory consolidation, drift-aware routing, adaptive behavioral anchoring.

*F(0) gaps:* Gap 5 (autonomous defense-in-depth).

*Swarmy action:* Implement a lightweight ASI probe in `scripts/3a_emergence_metrics.py` tracking three dimensions already measurable from existing data: tool usage patterns (`tools_used[]`), reasoning pathway stability (bearing chain consistency), inter-agent agreement rate (`dashboard_line` consensus across parallel agents). Emit ASI per session; threshold breach triggers drift-aware routing in `scripts/6c_inbox_router.py` — reroute to DEEP-DIVER for W-edge re-seating, no operator triage.

### P8 — Trajectory Guard: Real-Time Anomaly Detection

*Contribution:* Siamese Recurrent Autoencoder with hybrid contrastive + reconstruction loss detects wrong-plan-for-task AND malformed-plan-structure anomalies at 32ms inference; no human in the loop.

*F(0) gaps:* Gap 5.

*Swarmy action:* Deploy as PostToolUse hook in `.openhands/hooks/` or as middleware in `deploy/mcp-server/mcp_security_middleware.py`. Each agent's action sequence is the "trajectory." Contrastive check: embed task description and action sequence, flag cosine distance > threshold. Reconstruction check: validate the bearing chain (N/S/E/W) is structurally coherent for the mission type. At 32ms this is inline-safe. Flagged trajectories quarantine to `forensics/quarantine/incoming/{date}/` pending review.

### P9 — XG-Guard: Bi-Level Graph Anomaly Detection

*Contribution:* Bi-level encoder models sentence- and token-level agent representations jointly; theme-based anomaly detector tracks evolving discussion focus to detect agent behavior drift; bi-level score fusion provides interpretable anomaly explanations.

*F(0) gaps:* Gap 5 (autonomous quarantine without operator triage).

*Swarmy action:* XG-Guard's theme-based focus tracking can monitor mission-field drift in the swarm: if an agent's `mission` field begins diverging from its spawn bundle's declared mission, that's theme drift. Add a check in `scripts/9a_manifest_index_enforcer.py` validating mission-field consistency across in-flight manifests for a session. Divergence above 2σ from the session baseline triggers quarantine before promotion.

---

## Priority Ladder — Act on These Three First

1. **P1 + P2 (stigmergic trace density + pheromone reinforcement).** Closes the largest gap (autonomous mission discovery / zero-operator routing) and requires only new float fields on existing manifest schemas — lowest implementation cost, highest structural leverage. Wire `trace_strength` into `scripts/2e_discovery_frontier_cache.py` and `scripts/6g_frontier_index.py` in one sprint.

2. **P6 (SimpleMem consolidation → automated pollen promotion).** Memory promotion is the biggest human-burden point after routing. SimpleMem's within-session synthesis is implementable as a `scripts/3h_summarizer_agent.py` extension in under 200 lines and drops REVIEW-INBOX load significantly without touching HONEY write-protection.

3. **P8 (Trajectory Guard inline anomaly detection).** At 32ms inference it's the only defense-in-depth mechanism cheap enough to run on every agent action as a PostToolUse hook. Closes gap 5 without a dedicated triage agent — the purest expression of f(0) in the security domain.

---

**Scan provenance.** All 9 arXiv IDs verified against their abstract pages during the 2026-05-24 session (research-analyst subagent + cross-check). Reviewer should re-verify before citing in publications.
