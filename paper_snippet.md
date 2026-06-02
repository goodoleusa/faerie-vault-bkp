
The handshake pattern is the innovation that makes the architecture *stateless* in the distributed-systems sense [16]. A Merkle root is 32 bytes; computing it is O(n) over the branch's current entries. Anchoring it to main is one disk append. The cost of "the branch sends a heartbeat" is constant in branch size and trivial in absolute terms.

This dissolves the false dichotomy "branch is either fully merged or fully isolated." Via `mission_graph.py handshake <branch>` (queued for the next implementation cut), a branch publishes a progress hash to main on any cadence — every N entries, every M minutes, at meaningful checkpoints. The handshake entry on main is:

```json
{
  "entry_type": "branch-handshake",
  "branch": <name>,
  "current_merkle_root": <hex>,
  "leaf_count": <int>,
  "ts": <iso>
}
```

The branch does NOT close. The branch's next entry's `prev_entry_hash` still points to the branch's own tail; the handshake is a **side-channel anchor**, not a chain-link into main's flow. The branch continues writing; periodically it publishes new merkle roots; each one is independently anchorable to Rekor for public verifiable proof of "this branch existed at this time containing these N entries" without requiring trust in our infrastructure.

The handshake is simultaneously:

- a **heartbeat** ("I exist, here I am")
- a **commitment** ("here's my state, cryptographically")
- a **sync check** ("does main's view of my branch match my own state?")
- a natural **Rekor anchor point** ("submit this 32-byte root to the public transparency log now, without waiting for merge")

The pattern is structurally identical to Certificate Transparency's Signed Tree Head check-ins [18] and to side-chain pegging [26]. We did not invent it; we recognized the fit. The operator's framing — *graft the hash to main and keep going* — names it more precisely than the literature does.

A long-running branch accumulates a *trail* of public commitments: R₁ at handshake #1, R₂ at handshake #2, …, R_merge at final acceptance. Each independently anchorable; each a verifiable snapshot; none blocking the branch's continued evolution. No agent must hold the global state in its own context to coordinate — every agent reads the substrate at decision time. **No message routing, no leader election, no quorum protocols, no cluster discovery.** The substrate is the protocol.

---

## 7. Empirical Results

This section is the substantive empirical core of the paper. Every numerical claim cites either a verifiable repository artifact (git commit hash, file path, command that reproduces the number) or is marked as internal-eval-pending-external-validation. The two recently-completed multi-agent waves on 2026-05-25 are presented as case studies of the substrate's coordination performance under the conditions Khushiyant's phase-transition paper [4] predicts stigmergic substrates should outperform direct-messaging ones.

### 7.5 Scalability: Towards Constant-Cost Coordination

The empirical validation (commit `07daafe0`) demonstrates that Forensic Stigmergy solves the scaling bottleneck inherent in message-passing frameworks. 

| Metric | Message-Passing Architecture | Forensic Stigmergy (Our System) |
| :--- | :--- | :--- |
| **Coordination Scaling** | $O(N^2)$ (or $O(N)$ with central hub) | $O(F)$ (Number of File Ops) |
| **Merge Complexity** | High (Conflict Resolution) | $O(1)$ (Merkle Handshake Anchors) |
| **Orchestrator Cost** | High (Context Contamination) | Near-Zero ($f(0) \to 0$) |

By decoupling coordination from the orchestrator’s context window via the shared file system and Merkle-rolled anchors, we maintain constant-cost synchronization independent of the number of participating agents $N$.

### 7.1 Wave A — multi-surface doctrine + canvas, 4-agent stigmergic collaboration

**Setup.** Commit `07daafe0` (git: `git show --stat 07daafe0`). Four agents spawned in parallel from the operator's main session: VISIONARY (knowledge-synthesizer, doctrine writing), ARTISAN (frontend-design, canvas implementation), SYNTH (knowledge-synthesizer, refusal-doctrine cross-skill propagation), and POLISHER (frontend-design, readability sweep). All four shared a single coordination substrate: an append-only JSONL blackboard at `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` (cited inside the commit; reproducible by `git show 07daafe0 -- forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl`).

**Substrate-relevant claims (mechanically verifiable).**

(a) **40 files modified, +8,533 insertions, −285 deletions.** Source: `git show --stat 07daafe0` final line.

**Why this matters for the thesis — the coordination-cost scaling claim, in detail.**

The substrate's load-bearing complexity-theoretic property is that **coordination cost is O(N_files), independent of N_agents** — and this is the structural reason stigmergic substrates dominate direct-messaging substrates as agent count grows.

Let N denote the number of concurrent agents working on a shared file surface of size F (where F is the number of distinct files in scope). For each file f, exactly one agent ultimately edits it; the coordination question is "*which* agent gets to edit f, and how do the other N−1 agents learn that f is taken?" The answer determines the system's coordination-cost scaling law. We work through three architectures:

**Architecture 1 — Orchestrator-mediated (current production frameworks: AutoGen [1], MetaGPT [2], ChatDev [3]).** The orchestrator holds a registry of file-assignments and routes per-file claims through itself. To claim file f, agent A_i sends a message to the orchestrator; the orchestrator broadcasts the assignment to the remaining N−1 agents so they don't claim f. Cost per file: 1 inbound message + (N−1) outbound broadcasts = N messages. Total coordination cost: **O(N · F) messages**, plus O(F) entries in the orchestrator's working state. As N grows, the orchestrator's context fills with assignment bookkeeping; this is the precise mechanism that produces the "orchestrator context contamination" failure mode the human co-author's prior field report [31] documented qualitatively, and that Rath et al. [20] quantify as agent drift.

**Architecture 2 — Peer-to-peer direct messaging (no central orchestrator).** Each of N agents announces its claim to the remaining N−1 agents directly. Cost per file: N · (N−1) ≈ N² messages. Total coordination cost: **O(N² · F) messages**. This is the worst case and the reason peer-to-peer direct messaging is not used in practice at meaningful N.

**Architecture 3 — Stigmergic blackboard (this paper).** Each agent appends one CLAIM event to the shared blackboard JSONL file before editing f. Total CLAIM events: F (one per file, since exactly one agent ultimately wins). Each agent reads the blackboard tail before claiming — this is a passive read of a filesystem object, not a message routed to or from anyone. Total reads: bounded by some constant per claim attempt (we tail the last 30 lines; cost is O(1) in N). Total coordination cost: **O(F) write events + O(F · k) read events for some small constant k** — independent of N.

The contrast is the entire argument:

| Architecture | Messages | Orchestrator state | Scaling in N |
|---|---|---|---|
| Orchestrator-mediated | O(N · F) | O(F) | linear |
| Peer-to-peer direct | O(N² · F) | none (each agent O(N)) | quadratic |
| **Stigmergic blackboard** | **O(F)** | **none** | **constant in N** |

**Concrete numbers for Wave A — but message-count is the wrong unit.**

Counting "messages" is a proxy that *understates* the orchestrator's actual cost in LLM systems, because the load-bearing scarce resource is not message count but **tokens consumed in the orchestrator's context window**. Each "message" in a multi-agent LLM system is not 80 bytes of network protocol — it is hundreds to tens of thousands of LLM tokens that the orchestrator must compose, route, and absorb. We give the honest token-level analysis here.

In a **vanilla orchestrator-mediated scenario** (e.g., the default Claude Code Agent Teams usage pattern, or AutoGen with default settings), the orchestrator's per-agent cost has three components. **Important: the specific token counts below are industry-typical estimates used to illustrate structural scaling behavior, not values measured from a controlled experiment. Token costs vary by task complexity, doctrine verbosity, and model. The structural argument (O(N) vs. O(F) coordination cost) holds regardless of the specific values; the numbers make the argument concrete.**

1. **Spawn brief.** Main composes a structured prompt for each subagent. Industry-typical briefs in production multi-agent LLM work run 10,000–20,000 tokens (full doctrine, scope fences, examples, file paths, acceptance criteria, completion-ritual instructions). Main holds this in its own context while composing it. **Per-agent illustrative cost: ≈15,000 tokens, paid by the orchestrator. [Industry-typical estimate, not measured in a controlled experiment.]**

2. **Agent return.** When a subagent completes, the orchestrator reads the subagent's response into its own context to know what happened. In default Agent Teams usage, this is the subagent's full final assistant message — typically 5,000–20,000 tokens of structured report. The orchestrator absorbs this to know what to do next. **Per-agent illustrative cost: ≈10,000 tokens, paid by the orchestrator. [Industry-typical estimate, not measured in a controlled experiment.]**

3. **Synthesis context.** To synthesize across N agents, the orchestrator holds all N returns in context simultaneously (or pages them in and out). For N=4 agents at ≈10,000-token returns, this is **40,000 tokens of synthesis state**, paid by the orchestrator. [Industry-typical estimate, not measured in a controlled experiment.]

Total orchestrator-side illustrative cost for the vanilla N=4 wave: **(4 × 15,000) + (4 × 10,000) + 40,000 ≈ 140,000 tokens**. This is a non-trivial fraction — roughly 70% — of a 200,000-token Claude context window. The structural argument: the orchestrator's working memory is consumed by coordination bookkeeping; substantive work-in-flight is squeezed into what remains. This is the mechanism behind the human co-author's prior field report on orchestrator context contamination [31] and behind the agent-drift quantification in Rath et al. [20]: as N grows, the orchestrator's context fills with bookkeeping faster than the agents produce useful synthesizable work.

In the **stigmergic substrate (this paper)**, the equivalent costs are:

1. **Spawn brief — script-injected, NOT inline-composed.** Main does NOT compose a per-agent brief inline in its own LLM context. Main invokes a Python subprocess — `python3 scripts/spawn.py <intent> --mission <m> --wave <w> --team <team>` — that performs all heavy work outside the LLM's reasoning loop: reads `HONEY.md`, `COMB.md`, applicable skill files, and frontier-context manifests from disk; assembles a bundle.json at `forensics/bundles/{date}/{task_id}/bundle.json`; emits only a tiny JSON-line directive on stdout that main absorbs to dispatch `Agent()`. **The bundle composition happens in the subprocess; main's LLM context absorbs only the directive.** Measured per-agent cost: **~60 tokens** (cost-formula baseline T0, 2026-05-03: ~30 tokens bundle-rendering directive + ~20 tokens agent invocation overhead + ~10 tokens manifest parsing). Source: `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json`. Measured drift across 3 calibration sessions: 2.08%, 8.33% — well under the 20% acceptance threshold.

```mermaid
flowchart LR
    subgraph V["VANILLA — main pays the bundle cost in its own context"]
        direction LR
        VOp([Operator]) --> VM["Main LLM<br/>~15K tok/spawn<br/>(estimated)"]
        VM -- "composes brief inline" --> VB[Spawn brief<br/>in main's context]
        VB --> VA[Subagent]
        VA -- "full report ~10K tok" --> VM
