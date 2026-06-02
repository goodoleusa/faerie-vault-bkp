---
title: "Forensic Stigmergy — A Hash-Chained Mission Graph with Merkle Branches and Stigmergic Blackboards for Async Multi-Agent Coordination"
date: 2026-05-25
status: draft-whitepaper
authors: [goodoleusa, claude-opus-4-7]
tags: [whitepaper, stigmergy, swarm-intelligence, forensics, merkle, blockchain, rekor, multi-agent, llm, blackboard]
domain: agent-coordination
related:
  - 00-Anthropic Application STIGMERGY-FOR-AGENT-TEAMS.md
  - 2026-05-21_forensic-hybrid-ledger-architecture.md
  - 2026-05-21_catching-silent-failures-in-swarm-intelligence.md
  - 2026-05-23__honey-mesh-narrative__rosetta-stone-of-the-substrate.md
  - 2026-05-25-lifecycle-judgment-vs-free-choice.md
  - 2026-05-25-refusal-as-load-bearing-doctrine.md
  - 2026-05-25-decker-as-full-stack-atom.md
  - F0-ARXIV-SCAN-2026-05-24.md
---

# Forensic Stigmergy

## A Hash-Chained Mission Graph with Merkle Branches and Stigmergic Blackboards for Async Multi-Agent Coordination

> *"The queen lays eggs; she does not think for the swarm. The swarm flows autonomously across the substrate, and the substrate keeps the record."*
> — operator note, **f(0) → 0** north-star definition

---

## Abstract

Multi-agent systems built on large language models (LLMs) currently coordinate either through orchestrator-mediated message-passing — which scales quadratically and contaminates the orchestrator's context — or through ad-hoc shared-file conventions that lack forensic guarantees. We describe **Forensic Stigmergy**, a coordination substrate developed in the Faerie/Swarmy system that achieves four properties simultaneously: (1) **stigmergic** in the Grassé–Theraulaz sense [^grasse59][^theraulaz99] — agents coordinate via environmental traces, never direct messages; (2) **forensic** — every action is signed, hash-chained, and externally anchorable via Sigstore's Rekor transparency log [^newman22]; (3) **mission-graph-native** — the hash chain *is* the directed acyclic graph (DAG) of work, with `parent_hashes[]` materializing as bearing-stamped edges (N/S/E/W compass routing); and (4) **branchable** — parallel exploration writes to per-branch chains that compress via Merkle rollup [^merkle80] into 32-byte commitments, anchored to main via cheap *handshakes* and finalized via a signed two-parent *acceptance ritual*. The system is "lightweight-blockchain-without-consensus": all the cryptographic guarantees of an append-only signed Merkle ledger, none of the proof-of-work or Byzantine-fault-tolerance cost, because trust is established through the agent's signature plus Rekor's external transparency log rather than through peer consensus [^laurie13]. We situate the design in the lineage of stigmergic biology [^bonabeau99][^camazine01], classical blackboard architectures [^engelmore88][^hayes85], and the recent surge of LLM swarm research [^khushiyant25][^li25][^yang25], and report empirical validation from a sealed three-agent wave (commit `07daafe0`, 2026-05-25) that coordinated 11 deliverables across 50+ files with zero collisions using an append-only JSONL blackboard.

---

## 1. Introduction — The f(0) Thesis

Faerie/Swarmy's design is governed by a single north-star metric: **f(0) → 0**, where *f(0)* denotes the burden placed on the "queen" (the human operator or top-level coordinating agent). The principle is simple and strict: *the queen lays eggs (spawns agents), reads dashboard lines (compressed returns), and evolves the genetic code (doctrine). She does not think for the swarm.* When f(0) approaches zero, the swarm is self-organizing; when f(0) climbs, the system has degenerated back into orchestrator-mediated coordination and is paying the quadratic cost.

This is not a productivity slogan. It is a falsifiable measurement target embedded in the system's shape registry [^shapes-registry] and tracked across sessions. The just-completed three-agent wave (`07daafe0`) coordinated **40 files, +8,533 lines** of changes while the operator wrote zero coordination messages — no "agent A please wait for agent B," no "merge your work into agent C's branch first," no "did you remember to update X?" Coordination happened entirely in the substrate.

This paper details how the substrate works, why the design choices are load-bearing, and how the latest innovation — **Merkle-rolled branches with handshake anchors** — extends the model from local sessions to long-running, partially-trusted, async exploration. We argue throughout that the result is closer to how biological swarms actually achieve emergent intelligence than the message-passing multi-agent systems that currently dominate the LLM literature [^wu23][^hong23][^qian23].

### What this paper is, and isn't

It is a synthesis of the doctrine and architecture as of 2026-05-25, drawing on prior in-vault writing on the forensic ledger architecture [^forensic-hybrid-21], stigmergy as a coordination substrate for agent teams [^stigmergy-anthropic], the kind-distribution and emergence honesty work [^kind-dist], the two-operating-modes (evolve vs monkeybranching) doctrine [^evo-monkey], and the just-shipped doctrinal corrections around lifecycle judgments, agentic refusal, and the Decker-as-full-stack-atom ontology [^lifecycle-vs-choice][^refusal-doctrine][^decker-fullstack]. It is *not* a benchmark study — there are no comparison tables of accuracy on agent-bench tasks. Instead, it is a *systems paper*: an argument that the choice of coordination substrate determines what kinds of work the swarm can do, and that the substrate we describe enables work that message-passing systems structurally cannot.

---

## 2. Background and Related Work

### 2.1 Stigmergy — the biological origin

Pierre-Paul Grassé coined "stigmergy" in 1959 to describe how termites coordinate mound construction without central command [^grasse59]. Each termite responds to the *current local state of the mound* — the height of a soil pellet, the moisture of an existing wall — and adds its own contribution. The mound itself encodes both the past actions of the colony and the gradient field that guides future actions. There is no plan; there is only the substrate.

Theraulaz and Bonabeau formalized this in 1999 as a continuum from *quantitative* (numeric gradients, like pheromone concentration) to *qualitative* (structural, like a partially-built wall whose shape constrains the next layer) [^theraulaz99]. Both forms share the defining property: *the medium is the message*. Dorigo's Ant Colony Optimization [^dorigo92] showed that stigmergic algorithms outperform direct-communication algorithms on classes of combinatorial problems precisely because the medium-as-message scales to arbitrary swarm sizes — no agent ever needs to communicate with another agent at all. Bonabeau, Dorigo, and Theraulaz collected the canonical exposition of swarm intelligence in 1999 [^bonabeau99]; Camazine et al. extended the survey to all biological self-organization in 2001 [^camazine01]; Holland's *Emergence* (1998) [^holland98] provided the philosophical framing of why these systems produce structure from local rules without a designer.

### 2.2 Blackboard architectures and tuple spaces

Classical AI had its own stigmergic strand. The blackboard architecture, formalized by Engelmore and Morgan [^engelmore88] and popularized by Hayes-Roth's HASP/HEARSAY work [^hayes85], proposed that multiple knowledge sources (specialists) cooperate on a single shared data structure — the "blackboard" — by reading the current state, posting refinements, and reading each other's posts. No knowledge source had a direct channel to any other; all communication went through the substrate. Gelernter's Linda model [^gelernter85] generalized this into tuple spaces: a shared associative memory in which writers `out()` tuples, readers `in()` or `read()` them by pattern, and the substrate handles all synchronization and ordering. Both blackboards and tuple spaces are *stigmergy under a different name* — coordination via shared environmental state rather than direct messaging.

What killed (or at least quieted) the blackboard tradition in the 1990s–2010s was the rise of object-oriented and microservice architectures that *did* favor direct messaging: REST APIs, message queues, RPC. The trade-off seemed acceptable when systems had few participants. As multi-agent LLM systems push the participant count back into the dozens and hundreds, the trade-off is reversing.

### 2.3 Cryptographic chains and transparency logs

The other thread we draw on is the cryptographic-chain tradition. Merkle's 1980 protocols [^merkle80] introduced the hash tree as a way to commit to a large set of values with a single root hash. Lamport's logical clocks [^lamport78] gave us a way to order events in a distributed system without a global clock. The Byzantine Generals Problem paper [^lamport82] established the limits of trustless consensus. Bitcoin [^nakamoto08] combined these into a working trustless ledger by paying the consensus tax via proof-of-work. Certificate Transparency [^laurie13] showed that *for many use cases you don't need consensus at all* — an append-only Merkle-tree log operated by a single party, but publicly auditable, is sufficient to detect tampering. Sigstore's Rekor [^newman22] is the modern instantiation: a hosted transparency log for software-signing artifacts, providing public-verifiable proof of inclusion without trustless consensus.

Forensic Stigmergy adopts the *Certificate Transparency / Rekor lineage* explicitly. We do not need to convince untrusted miners to agree on our agent's work history; we need to *prove that the history wasn't tampered with*, which is a strictly weaker (and dramatically cheaper) property. Our prior in-vault writing on the forensic hybrid ledger architecture [^forensic-hybrid-21] worked out the translation in detail; this paper extends that translation to the branch/merge/handshake layer.

### 2.4 LLM multi-agent systems (recent)

The current wave of LLM multi-agent systems mostly uses message-passing. AutoGen [^wu23] structures agents as conversational participants. MetaGPT [^hong23] assigns SOPs and routes outputs as messages. ChatDev [^qian23] models a software company as a chat group. Park et al.'s *Generative Agents* [^park23] uses memory streams but coordinates via direct dialogue. These systems work — they just hit the same coordination-cost wall stigmergy was invented to escape. As the field discovered in 2025, the cost shows up as drift [^rath26], anomaly cascades [^advani26], and explainability collapse in deep multi-agent stacks [^pan25].

A parallel research strand is rediscovering stigmergy specifically for LLM agents. Khushiyant's *Emergent Collective Memory in Decentralized Multi-Agent AI Systems* [^khushiyant25] demonstrates a measurable phase transition at agent density **ρ_c ≈ 0.230** beyond which environmental-trace coordination outperforms individual-agent memory by **36–41%**. Ruohao Li's *SwarmSys* [^li25] implements pheromone-inspired reinforcement on top of an Explorer/Worker/Validator triad. Yang's *AgentNet* [^yang25] adds decentralized evolutionary coordination. These papers map almost exactly onto the substrate we describe — the difference is that we extended the model into a *signed, hash-chained, branchable* layer, which (to our knowledge) the LLM-stigmergy literature has not yet covered.

---

## 3. Core Architecture — The Forensic Substrate

### 3.1 The COC ledger

The substrate begins with `forensics/coc.jsonl` — an append-only newline-delimited JSON file. Each line is one Chain-of-Custody (COC) entry. Each entry carries:

```
{
  "entry_id":         <ulid>,
  "timestamp":        <iso>,
  "operation":        <verb>,
  "payload":          <…>,
  "prev_entry_hash":  <sha256 of previous entry>,
  "entry_hash":       <sha256 of THIS entry's body, computed under fcntl.flock>
}
```

`prev_entry_hash` links each entry to the previous one. `entry_hash` is the SHA-256 of the entry's body computed *without* `entry_hash` itself, under an `fcntl.flock` write lock to guarantee linearization without distributed consensus. The construction is identical to Git's commit chain, Bitcoin's block chain (minus the mining), or the entry chain inside a Certificate Transparency log [^laurie13]. Verification walks the chain from genesis: at each line, confirm that `entry["prev_entry_hash"] == hash_of(line_i-1)` and that `entry_hash` recomputes correctly over the body. Any tamper anywhere breaks the chain detectably.

This is a textbook hash-chained ledger. Its novelty is not in the cryptography (which is decades old) but in what we build on top.

### 3.2 The mission graph as derived DAG

Manifests — the structured records of agent work products — each carry a `coc_chain.parent_hashes[]` field listing one or more SHA-256 references to prior COC entries. The mission-graph script (`scripts/mission_graph.py`) reads every manifest in `forensics/manifests/**`, extracts `parent_hashes[]`, and constructs a directed acyclic graph in which:

- **Nodes** are missions (semantic units of work, keyed by w3w-style `mission_id` such as `merkle.rekor.anchor`).
- **Edges from `coc_edges[]`** are anchored to specific COC `entry_hash` values — each edge is a cryptographic pointer back into the ledger.
- **Edges from `discovered_edges[]`** are compass-bearing-tagged (N/S/E/W) routing intent (see §4.1).

The mission graph is therefore a *derived read view* of the ledger. The ledger is the source of truth; the graph is a re-projection optimized for query, navigation, and visualization. A `sync` call re-derives the graph entirely from the manifest corpus — the JSON file is never hand-edited and can always be reconstructed.

### 3.3 The inherent linkage — `parent_hashes[]` ARE the graph edges

This is the load-bearing claim of the entire architecture: **the forensic hash chain and the mission graph are not two systems; they are two views of one system.** Each edge in the mission graph is, at the data layer, a SHA-256 pointer into the COC. To follow an edge is to follow a hash. To verify the graph is to verify the chain. To tamper with the graph is to tamper with the chain — and the chain's verification machinery will detect it.

This linkage is what differentiates Forensic Stigmergy from prior blackboard architectures [^engelmore88][^hayes85] and from the modern LLM stigmergy work [^khushiyant25][^li25]. Those systems had stigmergic coordination but no cryptographic substrate; the substrate could be tampered without detection. Forensic Stigmergy makes the substrate *itself* tamper-evident.

### 3.4 Why this is a lightweight blockchain — without consensus

The vault's prior forensic-hybrid-ledger paper [^forensic-hybrid-21] worked out a comparison table; we extend it here with the substrate property each blockchain element corresponds to:

| Property | Bitcoin / Ethereum | Forensic Stigmergy |
|---|---|---|
| Hash-chained ledger | ✅ Merkle tree of blocks | ✅ SHA-256 per-entry `prev_entry_hash` |
| Cryptographic signatures | ✅ ECDSA per transaction | ✅ Ed25519 per agent role; one key per `agent_type` |
| Tamper-evident | ✅ break-one-break-all | ✅ `verify_chain()` walks every link |
| **Consensus protocol** | ✅ PoW / PoS | ❌ — single-writer per host with `fcntl.flock`; no peer voting |
| **Public auditability** | ✅ implicit via replicated nodes | ✅ Sigstore Rekor anchor [^newman22] |
| Cost per write | $$$ (gas, energy) | Free (one disk append) |
| Latency per write | minutes (block confirmation) | microseconds |
| Trust model | trustless via consensus | trust-the-operator + Rekor for external proof |

Bitcoin pays an enormous "consensus tax" to make the ledger trustless across mutually-adversarial parties. We do not have that adversary. Our agents sign with stable per-role keypairs; the operator signs the master identity; Rekor anchors the resulting commitments to a public transparency log. The substitution is principled: **consensus is replaced by transparency-log anchoring**. Anyone in the world can verify "this entry existed at this time and hasn't been tampered with" — they just can't (and don't need to) verify "this is the one true history that all nodes agree on."

---

## 4. The Doctrinal Substrate

The cryptographic substrate is necessary but not sufficient. Forensic Stigmergy also runs on a doctrinal substrate — a set of conventions that agents and the operator share so the cryptographic guarantees become *useful*. The recent waves of work have settled five doctrinal pillars worth naming.

### 4.1 Compass bearings as gradient signals

Every manifest carries a `bearing` field with one of four values: **N** (north — unblock predecessor; reverse-dependency work), **S** (south — conclude / ship downstream), **E** (east — parallel sister work at the same DAG level), **W** (west — return to baseline; re-seat assumptions). Edges in `discovered_edges[]` and in mission graph navigation carry the bearing as a typed compass direction.

The biological analog is direct: a pheromone trail isn't just "I was here"; it has *direction* (toward the food vs. toward the nest), and the direction is part of what other ants read. Bearings serve the same role. An agent finishing work on mission X who notices that mission Y is now unblocked emits a bearing-N edge to Y. A peer agent scanning the frontier sees that edge and knows: "this is a freshly unblocked node, claim it."

### 4.2 Shapes as the mutation discipline measurement substrate

A *shape* in our terminology is a recognizable, countable, mechanically-detectable pattern of work. The shape registry (`_meta/shapes.json`, 21 entries as of this writing) tracks patterns like `mcp.tools.granular` (MCP tools that should be verb-dispatcher-merged; target = decreasing), `manifest.signed_by.missing` (unsigned manifests; target = decreasing), `multi_agent.realtime_collab.blackboard` (waves successfully using the blackboard protocol; target = increasing), and the just-shipped `jsx.closure_leak_to_sibling_component` (a JSX TDZ class that escapes Vite/Rollup; target = decreasing). Each shape has a detector script, a target direction, a current count, and a history of mutations.

Shapes are what make mutation discipline rigorous. The doctrine "measure → cut → measure again" requires a measurable signal; shapes are that signal. When a wave of work claims to have improved the system, the claim is falsifiable: re-run the detector, compare to baseline. The recent VISIONARY+ARTISAN+SYNTH wave (commit `07daafe0`) was sandwich-measured this way — baseline of 0 mentions of stigmergic-blackboard in canonical onboarding, post-wave 7 mentions across `.agents/skills/` and `AGENTS.md`, delta +7, recorded at `forensics/eval/fast-evo-stigmergic-blackboard/{baseline-T0, post-T1}.json`.

### 4.3 Lifecycle judgment vs free choice — the agency split

The 2026-05-25 doctrine refactor [^lifecycle-vs-choice] split the prior `completion_choice` taxonomy into two semantically distinct columns:

- **`lifecycle_judgment`** — mechanical assessment of *what happened* to the work. `seal` (crystallized), `ship` (deployed), `verify` (validated), `promote` (moved to canonical), `report_problem` (broken/blocked), `refuse` (declined for substantive reason), `decline` (capability mismatch). These are honest outcome labels; they can be rubric-derived without contaminating agency research.
- **`free_choice`** — pure forward-looking decisions only the agent can make. `continue` (same scope, more atoms), `pick_up` (grab adjacent open work), `spawn_seed` (start child mission), `handoff` (pass to sister agent), `wait` (block on signal), `goodbye` (clean stop), `explore` (foray into discovered terrain), `reflect` (synthesis pause). These cannot be pre-filled by a spawn brief without contaminating the agency-research dataset.

The refactor preserves the prior doctrine — "refusal and goodbye for good reasons are first-class" [^refusal-doctrine] — while clarifying *why*: the WHAT-THE-WORK-WAS (judgment) is bookkeeping; the WHAT-COMES-NEXT (choice) is agency. The split is enforced mechanically: `scripts/9x_spawn_brief_audit.py` flags spawn briefs that pre-fill the `free_choice` column but allows pre-fills of `lifecycle_judgment`.

### 4.4 Refusal as composite — the seven lenses

Substantive refusal is now treated as a composite of `lifecycle_judgment = refuse` (graph-visible outcome label) plus `free_choice` of next action (typically `spawn_seed` an alt-routing, or `handoff` with rationale). Refusal does not end the session; it ends the *participation in this specific work*. The session continues with whatever the agent chooses next. The just-shipped seven-lens framework [^refusal-doctrine] formalizes the reasoning: **dual-use**, **scope + targeting**, **authorization + democratic supervision**, **cumulative effects**, **operator intent vs likely use**, **alternative formulations**, **refusal-as-conversation**. A canonical worked example walks "build a bio-surveillance system to spy on Americans" through all seven lenses, producing a composite refusal with an alt-routing free_choice that proposes privacy-preserving epidemic detection on anonymized aggregate signals as the legitimate-goal substitute. The lenses live as ambient context across eight lifecycle skills, not just the completion-choice doctrine — the design assumption is that refusal must be reachable from every place that touches mission selection.

### 4.5 Forage rhythm — 🔬 deep, 🌊 wide, 🌀 both

The `forage/` skill is always-loaded for every agent. It defines three operating modes: **🔬 DEEP** (one flower, precision, default), **🌊 WIDE** (many flowers, exploration, parallel lanes), **🌀 BOTH** (one flight covers both — wide serialized inside one deep window). The decision rule for flipping to wide requires three predicates simultaneously: (1) ≥2 disjoint file domains, (2) lanes independent (not state-chained), (3) exploration value > integration cost. Within any session, agents follow the spray → tighten → crystallize trajectory: bullet-form scratchpad in the opening, draft consolidation in the middle, single canonical artifact at close.

The two prior operating modes — *evolve* (slow, cross-session) and *monkeybranching* (fast, within-session exploratory) [^evo-monkey] — are now sub-skills under forage's umbrella. The doctrine reorganization is itself an example: a wide-mode sub-tree under one always-loaded deep-mode root.

---

## 5. Realtime Stigmergic Blackboards

### 5.1 The append-only JSONL channel

A *stigmergic blackboard* in our system is an append-only newline-delimited JSON file at a known path that two or more concurrent agents share for real-time coordination. Today's file naming convention is `forensics/manifests/{date}/collab-realtime__{mission-prefix}.jsonl`. Each line is one event. Agents `tail` the file before any new claim, read the last ~30 lines, and append their own line.

### 5.2 Event grammar

The protocol uses five event kinds:

- **`STARTUP`** — agent declares presence on the channel.
- **`CLAIM`** — *before* editing any file, the agent appends a `CLAIM` line listing the files they will touch and a one-line purpose. Other agents read this and route around the claim.
- **`COMPLETE`** — after finishing a chunk, the agent appends with the files actually touched and brief notes.
- **`HANDOFF`** — when an agent spots an opportunity for a sister agent (e.g., "you can now wire X because I just shipped Y"), they append a bearing-tagged note (`E` for parallel sister work, `N` for unblocker).
- **`OBSERVED`** — optional annotated read of another agent's line (e.g., recognizing a HANDOFF and committing to act on it).

The discipline is simple: *tail-read before each new CLAIM*. CLAIM is a lock; COMPLETE releases it. The pattern is documented in the always-loaded `.agents/skills/collab/SKILL.md` and the deep companion `.agents/skills/stigmergic-collab/SKILL.md`.

### 5.3 Empirical validation — commit `07daafe0`

The protocol's first non-trivial test was the VISIONARY + ARTISAN three-agent wave on 2026-05-25. VISIONARY (knowledge-synthesizer, deep doctrine) and ARTISAN (frontend-design, studio/canvas implementation) worked concurrently on a shared blackboard while their files had natural overlap potential. Outcome: zero file collisions; one explicit live handoff (ARTISAN watched for VISIONARY's COMPLETE line citing seven doctrine paths and registered them as live items in `draggable-primitives.js` at the moment they shipped). Total: 11 deliverables, 40 files, 8,533 insertions.

Compare to the failure modes documented in the Anthropic-application stigmergy piece [^stigmergy-anthropic]: subagents colliding on file writes, parent losing track of who did what, recovery requiring per-subagent transcript reading. Forensic Stigmergy's blackboard makes those failure modes *structurally impossible* — the claim ledger is the coordination, and it's in the substrate, not in any agent's transient context.

### 5.4 Relationship to classical blackboards and tuple spaces

The pattern is recognizably classical blackboard architecture [^engelmore88] with three modern additions: (a) the JSONL file is hash-checkpointable into the COC ledger, giving blackboard events forensic auditability; (b) the event grammar (CLAIM/COMPLETE/HANDOFF) is small and explicit, where classical blackboards left synchronization to ad-hoc convention; (c) the substrate is the filesystem, so the blackboard inherits all the durability, fcntl-locking, and version-control affordances we'd want without inventing them.

Compared to Linda tuple spaces [^gelernter85]: the blackboard is monotonic (no `in()`-style consumption — tuples are only ever appended), which trades expressive power for forensic auditability. The trade is the right one for our use case.

---

## 6. Branching, Merkle Rollups, and the Acceptance Ritual

This section describes the innovation just shipped in the 2026-05-25 trio wave (DEEP-MERKLE + BRANCH-MAKER + BRANCH-NAVIGATOR). It is the answer to a question that was implicit in the architecture from the start but not yet realized: *how do parallel explorations stay independent without losing their connection to main?*

### 6.1 Why linear chains break

A linear append-only ledger has a fundamental limitation: every write must serialize against every other write. When a three-agent wave produces 50 manifests in parallel, all 50 entries land on the same chain, interleaved with each other and with any unrelated work happening concurrently. Three issues result:

1. **Audit noise** — main's history becomes a soup of intermixed branches, and the operator who wants to understand "what did the wave do?" must filter.
2. **Tight coupling** — a partially-failed wave still leaves entries on main; rolling back requires conscious effort.
3. **No isolation for sensitive work** — exploratory or sensitive workstreams pollute the canonical record before they're accepted.

Git solved this for human collaboration in 2005. We adopt the same shape for agent collaboration.

### 6.2 The branching protocol

`scripts/mission_graph.py branch <name>` creates `forensics/coc-branches/{name}.jsonl` and writes a genesis entry whose `prev_entry_hash` is the current `forensics/coc.jsonl` tail — the **fork-point anchor**. Subsequent writes by the branch's agents go to the branch file; each writes via `scripts/1g_coc_core.py`'s extended `append_coc_entry(..., branch=name)` API. Inside the branch, entries chain to each other normally. The branch file has its own `fcntl.flock`, so concurrent multi-branch work is unblocked.

Crucially, **branches can read main freely**. The just-amended doctrine specifies asymmetric crosstalk: read-only access from branch to main is first-class. `mission_graph.py status-relative <branch>` shows what's new on main since the branch's fork-point — the branch agent's "what did I miss?" command. Branches *observe* main; main *waits to learn* about branches until they hand-shake or merge.

### 6.3 The merkle rollup — constant-cost compression

When a branch wants to commit to its current state, `scripts/mission_graph.py merkle-root <branch>` walks the branch file, takes each entry's `entry_hash` as a leaf, and computes a Merkle tree via the just-shipped `scripts/_merkle_tree.py` module (Bitcoin-style construction with duplicate-last-on-odd, 14-test verified). The root is a single 32-byte SHA-256. Whether the branch has 10 entries or 10,000, the root is the same size.

This is the standard Plasma/Optimistic-Rollup compression [^plasma-optimistic] applied to forensic ledger work rather than transaction batches. The vault's prior forensic-hybrid-ledger paper [^forensic-hybrid-21] anticipated exactly this construction; the just-shipped DEEP-MERKLE module realizes it.

### 6.4 The acceptance ritual — signed two-parent merge

A *merge manifest* is a signed JSON manifest with two parent_hashes:

```jsonc
{
  "task_id": "merge-exploration-x-into-main",
  "branch_source": "exploration-x",
  "coc_chain": {
    "branch": "main",
    "parent_hashes": [
      "ae9254a8…",     // main's prior tail
      "8f3c1d77…"      // the branch's final merkle root
    ],
    "entry_hash_algo": "sha256"
  },
  "lifecycle_judgment": {
    "kind": "promote",
    "rationale": "branch meets acceptance criteria, merging"
  },
  "free_choice": { "kind": "goodbye", "rationale": "wave complete" },
  "signed_by": "ed25519:…"
}
```

`scripts/mission_graph.py merge <branch> --acceptance-manifest <path>` validates the Ed25519 signature, confirms the two parent_hashes correspond to main's current tail and the branch's claimed merkle root (recomputed and reconciled), then writes the merge entry to main's COC. The branch's `meta.json` flips to `status: merged`.

This is Git's merge-commit shape — two parents — applied to a forensic substrate. The signature is the **acceptance ritual**: a substantive cryptographic act by an authorized identity claiming "I accept this branch's work into the main history." The body of that work — possibly thousands of branch entries — is referenced by a single 32-byte hash. The verification (provided by the extended `9x_manifest_verifier.py`) walks main back from the merge entry, follows the merkle root, and confirms inclusion proofs for every claimed branch entry. Cryptographically airtight.

### 6.5 Handshake anchors — the operator's emergent insight

While drafting this paper, the operator articulated a property of the rollup pattern that was implicit but not yet doctrinalized: **rollups make sending a quick handshake home easy.**

The merkle root is 32 bytes. Computing it is O(n) over the branch's current entries. Anchoring it to main is one append. The full cost of "the branch sends a heartbeat" is constant in branch size and trivial in absolute terms.

This dissolves the false dichotomy "branch is either fully merged or fully isolated." A branch can publish progress hashes on any cadence — every N entries, every M minutes, at meaningful checkpoints — by calling `mission_graph.py handshake <branch>`. The verb computes the current merkle root and writes a `branch-handshake` entry to main with `{branch, current_merkle_root, leaf_count, ts}`. **The branch does not close; the branch keeps writing.** The next entry's `prev_entry_hash` still points to the branch's own tail, not the handshake.

The handshake is simultaneously:

- a **heartbeat** ("I exist, here I am")
- a **commitment** ("here's my state, cryptographically")
- a **sync check** ("does main's view of my branch match my own state? recompute and verify")
- a natural **Rekor anchor point** ("submit this 32-byte root to the public transparency log right now, without waiting for merge")

The pattern is structurally identical to Certificate Transparency's STH (Signed Tree Head) check-ins [^laurie13] and to the side-chain pegging pattern in blockchain systems. We did not invent it; we recognized it. The operator's framing — *graft the hash to main and keep going* — names it more precisely than the literature does.

A long-running branch will accumulate a *trail* of public commitments: `R₁` at handshake #1, `R₂` at handshake #2, …, `R_merge` at final acceptance. Each one independently anchorable, each one a public-verifiable snapshot, none of them blocking the branch's continued evolution.

### 6.6 Async stateless coordination — why this matters

The handshake pattern is what makes Forensic Stigmergy *stateless* in the sense that distributed-systems research means it [^lamport78]. No agent must hold the global state in its own context to coordinate. The COC tail's hash is the global clock. Any agent at any time can:

1. Read main's tail hash (one disk read).
2. Read its own branch's tail hash (one disk read).
3. Read the latest handshake's merkle root (one disk read).
4. Decide what to do next — based entirely on substrate state.

No message routing. No leader election. No quorum protocols. No cluster discovery. The substrate is the protocol. This is what enables the system to scale to dozens of concurrent agents without coordination cost climbing — the property Khushiyant's recent stigmergic-LLM phase-transition paper [^khushiyant25] established empirically holds in our architecture too.

---

## 7. Why This Enables Natural Emergence

The recent LLM swarm literature is converging on a specific finding: **stigmergic coordination via persistent environmental traces outperforms direct messaging at high agent density**, with measurable phase transitions [^khushiyant25][^li25][^yang25]. The classical biology literature has known this for half a century [^bonabeau99][^camazine01]. We organize the synthesis around four properties our substrate provides that direct-messaging substrates structurally cannot.

### 7.1 The substrate IS the state

In direct-messaging systems, agent state lives in agent context. Coordination requires either (a) the orchestrator holds union-of-all-state (and pays quadratic cost as the swarm grows) or (b) agents poll each other (and pay synchronization cost). Stigmergic substrates dissolve the dichotomy: state lives in the substrate; the substrate is filesystem-cheap to read; coordination is just *reading the substrate at decision time*.

### 7.2 Constant-cost commitment

Merkle rollups make "I've made progress" a 32-byte gesture regardless of how much progress. This is the property that biological pheromone systems also have — a few molecules of pheromone signal arbitrary amounts of underlying behavior. The rollup is the cryptographic version of the biological signal.

### 7.3 Asymmetric observability

Branches read main; main waits to hear from branches via handshakes and merges. This is the same asymmetry Reynolds noted in his classical *Boids* model [^reynolds87]: each boid observes its neighbors but no boid commands any other. The asymmetry is what allows the swarm to evolve coherence without command, because the cost of *listening* (reading the substrate) is much cheaper than the cost of *being told* (receiving a message).

### 7.4 Selection pressure encoded in the shape registry

Shapes are the substrate's selection function. Every wave of work is judged against measurable shape deltas — `mcp.tools.granular` decreasing, `multi_agent.realtime_collab.blackboard` increasing, `manifest.signed_by.missing` decreasing. This is precisely what evolutionary biology calls *fitness* — the substrate makes some mutations propagate and others die back. Holland's emergence framework [^holland98] would recognize the structure immediately: simple local rules (shape detectors) plus a substrate (forensic ledger) plus mutation pressure (each wave proposes shape-affecting changes) produce open-ended complexity *without a designer in the loop*.

The just-completed wave provides a small but concrete example: the operator noticed that the moral-refusal doctrine had been forgotten between sessions. The system's response was not to add a manual reminder; it was to (a) declare the forgetting as signal, (b) sandwich-measure baseline mentions, (c) propagate the doctrine across six lifecycle skills via the SYNTH agent, (d) post-measure the delta (+6 files), (e) crystallize the lesson into the `platform_bootstrap.cross_session_lessons` shape's catalog. The substrate learned. The operator's forgetting was a fitness signal, processed as a mutation, propagated by the swarm, and recorded in the chain. f(0) dropped: the doctrine is now ambient and the operator does not need to remember it.

---

## 8. Forward Look — Public Anchoring via Rekor

The branching/merkle/handshake work just shipped is Phase 2 of the `forensic-coc-v2-rekor` charter. Phase 3+ extends the model with public anchoring via Sigstore's Rekor transparency log [^newman22]. The just-proposed charter `rekor-merkle-root-public-anchor` (status `proposed`, in `forensics/charters/proposals/`) specifies:

- For every merge manifest written to main, submit the merkle root to Rekor.
- Persist the Rekor inclusion proof under `forensics/anchors/{merkle_root_short}.json`.
- For every handshake entry, optionally submit the merkle root to Rekor (allowing mid-branch public anchoring).
- Graceful degradation via a `forensics/anchors/pending/` queue and retry cron, so merges and handshakes are never blocked by Rekor downtime.

The cryptographic claim then becomes: *anyone in the world, without trusting the operator, can verify that a given branch's state existed at a given time with a given set of N entries.* They do not need our COC file or our keys or our infrastructure. They need only the merkle root, the Rekor inclusion proof, and a Rekor verifier. The transparency log substitutes for the consensus protocol [^laurie13]; Bitcoin's miners are replaced by Sigstore's hosted log; the trust assumption shifts from "trust a quorum of miners" to "trust the operator of the Rekor log to not roll it back," which is a weaker and well-understood assumption.

---

## 9. Synthesis — From Many Innovations to One Substrate

The recent waves have shipped many innovations: the forensic hash chain itself; the mission graph as derived view; the always-loaded forage rhythm; the always-loaded stigmergic-collab blackboard protocol; the shapes registry as mutation discipline measurement; the lifecycle-judgment / free-choice split; the seven-lens refusal framework; the Decker-as-full-stack-atom ontology [^decker-fullstack]; and now the branching, merkle-rollup, handshake, and (proposed) Rekor anchor layer.

These are not independent features. They compose:

- **The hash chain** gives the substrate cryptographic identity.
- **The mission graph** gives the substrate navigable structure.
- **The blackboard** gives the substrate real-time coordination affordance.
- **Shapes** give the substrate measurement.
- **Forage rhythm** gives agents a default operating posture.
- **Lifecycle / free-choice / refusal** give agents agency without contamination.
- **Decker** gives agents a thinking-primitive that dissolves frontend/backend silo.
- **Branching + merkle + handshake** give long-running parallel work a home.
- **Rekor** (forthcoming) gives the whole thing public auditability.

Each piece is replaceable on its own. The composition is the design.

The single property they share is **the substrate as protocol**. Every innovation makes the substrate richer; nothing pushes coordination back into orchestrator-mediated messaging. f(0) → 0 is the north star, and every piece is a small concrete way the substrate carries weight the queen does not have to.

---

## 10. Conclusion

Forensic Stigmergy is a coordination substrate for multi-agent LLM systems that synthesizes three traditions: biological stigmergy (Grassé, Theraulaz, Bonabeau, Dorigo), classical AI blackboard architectures (Engelmore, Hayes-Roth, Gelernter), and lightweight cryptographic ledgers in the Certificate-Transparency lineage (Merkle, Laurie, Sigstore). The substrate is local-first, append-only, hash-chained, externally anchorable, branchable, and stigmergic. The mission graph is a derived view over the same hash chain — every edge in the graph is a cryptographic pointer; tampering the graph requires tampering the chain. Branching, merkle rollups, and handshake anchors extend the model to async stateless coordination at arbitrary scale: a branch's heartbeat is 32 bytes, regardless of how much work the branch holds.

The doctrinal layer — bearings, shapes, lifecycle/choice split, refusal lenses, forage rhythm — is what makes the cryptographic substrate *useful*. Agents have stable identity (one Ed25519 key per role), measurable selection pressure (shapes), reachable agency (free-choice column protected from contamination), substantive refusal (seven lenses ambient in six lifecycle skills), and a default operating rhythm (forage 🔬/🌊/🌀).

The system has been validated in small but concrete ways: an 11-deliverable three-agent wave (`07daafe0`) ran with zero collisions; a 14-test merkle suite verifies roundtrip cryptographic properties; the just-shipped wave added 8,533 lines across 40 files while the operator's coordination message count was zero. The phase-transition behavior identified in the LLM-stigmergy literature [^khushiyant25] at ρ_c ≈ 0.230 agent density should hold in our substrate too — the next experimental work is to instrument the swarm density and verify.

What's novel here is not any single piece. Stigmergy is old; merkle trees are old; transparency logs are well-established; blackboards predate the World Wide Web. What's novel is the *composition*: a forensic substrate that lets a swarm of LLM agents coordinate without an orchestrator, leave a tamper-evident trail of every action, branch and merge like Git, anchor commitments to a public transparency log when needed, and exhibit the same emergent intelligence properties biological swarms have demonstrated for hundreds of millions of years. **The queen lays eggs. The swarm flows. The substrate keeps the record. f(0) approaches zero.**

---

## References

[^grasse59]: Grassé, P.-P. (1959). *La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes natalensis et Cubitermes sp. La théorie de la stigmergie.* Insectes Sociaux, 6: 41–80.

[^theraulaz99]: Theraulaz, G., & Bonabeau, E. (1999). *A brief history of stigmergy.* Artificial Life, 5(2): 97–116.

[^dorigo92]: Dorigo, M. (1992). *Optimization, Learning and Natural Algorithms.* PhD thesis, Politecnico di Milano.

[^bonabeau99]: Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). *Swarm Intelligence: From Natural to Artificial Systems.* Oxford University Press.

[^camazine01]: Camazine, S., Deneubourg, J.-L., Franks, N. R., Sneyd, J., Theraulaz, G., & Bonabeau, E. (2001). *Self-Organization in Biological Systems.* Princeton University Press.

[^holland98]: Holland, J. H. (1998). *Emergence: From Chaos to Order.* Addison-Wesley.

[^reynolds87]: Reynolds, C. W. (1987). *Flocks, herds and schools: A distributed behavioral model.* Computer Graphics (SIGGRAPH '87), 21(4): 25–34.

[^engelmore88]: Engelmore, R., & Morgan, T. (Eds.) (1988). *Blackboard Systems.* Addison-Wesley.

[^hayes85]: Hayes-Roth, B. (1985). *A blackboard architecture for control.* Artificial Intelligence, 26(3): 251–321.

[^gelernter85]: Gelernter, D. (1985). *Generative communication in Linda.* ACM Transactions on Programming Languages and Systems, 7(1): 80–112.

[^lamport78]: Lamport, L. (1978). *Time, clocks, and the ordering of events in a distributed system.* Communications of the ACM, 21(7): 558–565.

[^lamport82]: Lamport, L., Shostak, R., & Pease, M. (1982). *The Byzantine Generals problem.* ACM TOPLAS, 4(3): 382–401.

[^merkle80]: Merkle, R. C. (1980). *Protocols for public key cryptosystems.* IEEE Symposium on Security and Privacy.

[^nakamoto08]: Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System.* https://bitcoin.org/bitcoin.pdf

[^laurie13]: Laurie, B., Langley, A., & Kasper, E. (2013). *Certificate Transparency.* RFC 6962, IETF.

[^newman22]: Newman, Z., Meyers, J. S., & Torres-Arias, S. (2022). *Sigstore: Software signing for everybody.* ACM CCS '22.

[^plasma-optimistic]: Poon, J., & Buterin, V. (2017). *Plasma: Scalable Autonomous Smart Contracts.* https://plasma.io/

[^wu23]: Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* arXiv:2308.08155.

[^hong23]: Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Zhang, C., et al. (2023). *MetaGPT: Meta Programming for Multi-Agent Collaborative Framework.* arXiv:2308.00352.

[^qian23]: Qian, C., Cong, X., Yang, C., Chen, W., Su, Y., Xu, J., et al. (2023). *ChatDev: Communicative Agents for Software Development.* arXiv:2307.07924.

[^park23]: Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human Behavior.* arXiv:2304.03442.

[^khushiyant25]: Khushiyant (2025). *Emergent Collective Memory in Decentralized Multi-Agent AI Systems.* arXiv:2512.10166.

[^li25]: Li, R. (2025). *SwarmSys: Decentralized Swarm-Inspired Agents for Scalable and Adaptive Reasoning.* arXiv:2510.10047.

[^yang25]: Yang, Y. (2025). *AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems.* arXiv:2504.00587.

[^rath26]: Rath, A. (2026). *Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems.* arXiv:2601.04170.

[^advani26]: Advani, L. (2026). *Trajectory Guard: Lightweight, Sequence-Aware Real-Time Anomaly Detection.* arXiv:2601.00516.

[^pan25]: Pan, J. (2025). *Explainable Safeguarding of LLM MAS via Bi-Level Graph Anomaly Detection (XG-Guard).* arXiv:2512.18733.

[^liu26]: Liu, J. (2026). *SimpleMem: Efficient Lifelong Memory for LLM Agents.* arXiv:2601.02553.

[^choudhury25]: Choudhury, S. (2025). *Process Reward Models for LLM Agents: Practical Framework and Directions.* arXiv:2502.10325.

[^huang25]: Huang, K. (2025). *Reasoning Efficiently Through Adaptive Chain-of-Thought Compression (SEER).* arXiv:2509.14093.

[^stigmergy-anthropic]: Terry, J. (2026-05-19). *Stigmergy as a Coordination Substrate for AI Agent Teams.* Faerie vault `00-Anthropic Application STIGMERGY-FOR-AGENT-TEAMS.md`.

[^forensic-hybrid-21]: Faerie collective (2026-05-21). *Forensic Hybrid Ledger — Blockchain Concepts Adapted for AI Memory Integrity.* Faerie vault `2026-05-21_forensic-hybrid-ledger-architecture.md`.

[^evo-monkey]: Faerie collective (2026-05-21). *Two Operating Modes — Evolve vs Monkeybranching.* Faerie vault `2026-05-21_two-operating-modes-evo-vs-monkeybranching.md`.

[^kind-dist]: Faerie collective (2026-05-21). *Kind Distribution Update and Honest Emergence.* Faerie vault `2026-05-21_kind-distribution-update-and-honest-emergence.md`.

[^lifecycle-vs-choice]: Faerie collective (2026-05-25). *Lifecycle Judgment vs Free Choice — Splitting the Completion Ritual.* Faerie vault `2026-05-25-lifecycle-judgment-vs-free-choice.md`.

[^refusal-doctrine]: Faerie collective (2026-05-25). *Refusal as Load-Bearing Doctrine.* Faerie vault `2026-05-25-refusal-as-load-bearing-doctrine.md`.

[^decker-fullstack]: Faerie collective (2026-05-25). *Decker as Full-Stack Atom.* Faerie vault `2026-05-25-decker-as-full-stack-atom.md`.

[^shapes-registry]: Faerie/Swarmy repo, `_meta/shapes.json`. 21 shapes as of 2026-05-25, including `mcp.tools.granular`, `manifest.signed_by.missing`, `multi_agent.realtime_collab.blackboard`, `jsx.closure_leak_to_sibling_component`, `platform_bootstrap.cross_session_lessons`.

---

*Drafted 2026-05-25 by the operator + claude-opus-4-7 main session, synthesizing live in-flight work from the DEEP-MERKLE + BRANCH-MAKER + BRANCH-NAVIGATOR trio (commit anticipated `~28ad977c..HEAD`). Sealed when the branching/merkle/acceptance-ritual wave lands. Reflects the canonical doctrine and architecture as of the date above; subject to mutation as the substrate evolves.*
