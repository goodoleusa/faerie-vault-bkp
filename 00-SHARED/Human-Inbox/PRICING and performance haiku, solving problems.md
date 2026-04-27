  ## Turning Failure into Gold
  
  ### Phase 1: The original problem
  
  The system had no memory continuity between sessions. Every cold start, faerie had no idea what happened last time.
  Scratch files, NECTAR, REVIEW-INBOX, per-project MEMORY.md files — all scattered. Faerie's solution was to read everything, everywhere, every session start. It had to. There was no alternative.

  That was correct behavior for the problem at the time.

  ### Phase 2: The solution that caused the new problem
  
  The reading worked. Context continuity improved. But faerie got better at its job by reading more — so it read more.
  NECTAR grew (append-only, unbounded). REVIEW-INBOX grew. Per-project memories multiplied. The more the system
  produced, the more faerie consumed at startup just to orient itself. By the time faerie was "fully oriented," it had
  burned 30% of the context window and hadn't launched a single agent yet.

  The solution worked so well it created the next problem: faerie became the bottleneck it was designed to prevent. The
   cost of knowing everything was that there was less room to do anything.

  ### Phase 3: The structural cause
  
  The root wasn't faerie reading too much — it was that the outputs of prior sessions weren't pre-digested for
  consumption. Raw NECTAR (24K tokens) contains the same information as a 1,334-token faerie-brief, but nobody was
  assembling the brief before faerie needed it. Faerie had to do the assembly inline, at startup, every time, in the
  most expensive context in the system.

  Agents were producing → but nothing was packaging the product for the next consumer.

  ### Phase 4: Stigmergy closes the loop
  
  The Stop hook now runs membot, session_metrics, surfacing calibration, eval_harness, and vault_narrative_sync. By the
   time the session ends, the next session's cold-start fuel is already packaged: faerie-brief.json is written, eval
  score is cached, manifests are sealed. Faerie wakes up and reads receipts instead of raw material.

  The handoff-snapshot.json bomb (185K tokens) is the last vestige of Phase 2 thinking — it's emergency_handoff.py
  collecting everything raw, as a fallback. Now that the normal path works, that fallback is rarely hit. But it's still
   a live grenade if the brief is stale.

  The pattern that keeps repeating:
  ## Every phase, the solution to fragmentation creates consolidation — which then becomes its own kind of bloat at the next level. 
  
  ## The answer is always the same: push the synthesis earlier, closer to where the information was created,
  so the consumer gets a receipt instead of raw material.

  Agents write manifests (not return blobs). 
  Stop hook packages the session (not faerie at startup). membot promotes scratch (not faerie reading scratch). 
  
  Each time, the work moves upstream and faerie gets lighter.

  The pilot/mission-control model is the asymptote: faerie reads only summaries, launches agents, reads their receipts.
   The actual work — and the actual understanding — lives in the agents and the trail they leave.
  
  ## On codifying wave model routing + system design tools in eval

  The eval should measure model routing efficiency as its own dimension — are cheap models being used where they should
   be, and is the output quality justified by the model tier used? Spawning an agent to add this to eval_harness.py and
   the Eval-Framework.md, alongside the other two flags from the siphon:

● python-pro(Add model routing efficiency to eval + fix H1 confidence conflict)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● Also still waiting on HONEY crystallization agent. Current board:

  ┌───────────────────┬───────────┬───────────────────────────────────────────────┐
  │       Agent       │  Status   │                     Task                      │
  ├───────────────────┼───────────┼───────────────────────────────────────────────┤
  │ eval + H1 fix     │ submerged │ model routing dimension + conflict resolution │
  ├───────────────────┼───────────┼───────────────────────────────────────────────┤
  │ crystallize HONEY │ submerged │ merge sys00019+sys00019b, free budget         │
  └───────────────────┴───────────┴───────────────────────────────────────────────┘

  [ORBIT | 2 agents submerged | ctx ~89K]

  Flag 3 for you when you have a moment: T1 publication blocker — 18 Tier 1 evidence items have no sha256 verification.
   Run python3 scripts/2b-hash-guardian.py before any disclosure. That's not automated — needs you.

✻ Worked for 1m 7s · 2 background tasks still running (↓ to manage)

❯ can we start to set up tests to compare my systems haiku outputs to baseline higher models

● python-pro(Build model comparison test harness)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● 3 agents submerged. The comparison harness will run 4 arms × 3 tasks:

  - system-haiku — your system + cheapest model
  - system-sonnet — your system + current default
  - vanilla-sonnet — cold Sonnet, no context
  - vanilla-haiku — cold Haiku, no context

  Scoring is deterministic keyword matching — not LLM-judged, so there's no circular bias from using Claude to score
  Claude. The results are hash-chained so the improvement trajectory is forensically verifiable. You can show run #1 →
  run #20 and prove the gap widened as the system matured.

  Target threshold: system-haiku ≥ vanilla-sonnet score. When that's consistently true, you have the benchmark that
  proves the business model.