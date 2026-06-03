# Claim 9: Public Hash-Chained Stigmergic Blackboard for Massively-Scaled, Cross-Tenant Multi-Agent Coordination

> **Standalone section for insertion into the USPTO Provisional Patent Application.**
> Folds into the Claims section as Claim 9 (+ dependents 9a–9d) and into the
> Detailed Description. Self-contained for independent attorney review.

⚠️ DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED BEFORE USE

---

## Part A: Formal Claim Language (USPTO Claim 9)

### Claim 9

A computer-implemented system for coordinating a large plurality of autonomous software agents working on semantically-related units of work without central orchestration and without inter-agent message-passing, the system comprising:

(a) an append-only, hash-chained ledger (a "blackboard") constituting the exclusive coordination substrate, wherein each ledger entry contains a reference to a cryptographic hash of the immediately preceding entry such that the ledger is tamper-evident and any party may verify its integrity from any prior anchor to its head;

(b) a navigation-event interface by which each agent appends to the ledger a navigation event comprising at least: a semantic mission coordinate expressed as a dot-delimited multi-word ("w3w-style") address, a compass bearing selected from a fixed set {North, South, East, West} encoding the work's relationship to a mission frontier, and a monotonically-growing charted-course vector recording the ordered sequence of mission coordinates the agent has traversed;

(c) a stigmergic adjacency function that computes, for any two agents, a relatedness measure equal to the cardinality of the set-intersection of the semantic terms of their respective mission coordinates, such that each agent selects its next unit of work by reading the field of other agents' navigation events and maximizing or thresholding said relatedness measure, rather than by receiving an assignment;

(d) a dual representation comprising (i) a strategic directed-acyclic mission graph whose nodes are mission coordinates and whose edges are compass bearings, and (ii) the tactical blackboard ledger of (a), wherein each appended navigation event is a real-time projection of a mission-graph node being executed, the mission graph being the map and the blackboard being the executed reality; and

(e) an indexed frontier scanner that reads a pre-computed summary index aggregating navigation events by mission coordinate and bearing, rather than scanning all ledger entries, such that the per-agent coordination cost grows sublinearly in the total number of agents;

wherein, by virtue of (a) the public verifiability of the hash-chained ledger and (c) the assignment-free stigmergic routing, a number of agents in the thousands, including agents operated by mutually-independent organizational tenants, coordinate on related missions through a single shared, publicly-auditable substrate without any central orchestrator and without any agent directly messaging another.

---

### Claim 9a (Dependent — Sublinear Coordination Cost at Scale)

The system of Claim 9, wherein the indexed frontier scanner of Claim 9(e) reduces the per-scan information cost from a quantity proportional to the total volume of navigation events to a quantity proportional to the number of distinct (mission coordinate, bearing) pairs, achieving an order-of-magnitude reduction in coordination overhead per agent, such that adding agents to the system does not impose a linear increase in per-agent coordination cost.

### Claim 9b (Dependent — Cross-Tenant Public Coordination)

The system of Claim 9, wherein the hash-chained blackboard is published to a substrate readable by mutually-independent organizational tenants, and wherein agents operated by different tenants append navigation events to and read navigation events from the same ledger, such that cross-organization agent coordination on related missions is achieved with verifiable integrity and without any tenant trusting any other tenant or a central coordinator, the hash-chain providing tamper-evidence in lieu of mutual trust.

### Claim 9c (Dependent — Anchoring to a Public Transparency Log)

The system of Claim 9, wherein periodic digests of the blackboard ledger head are submitted to a public append-only cryptographic transparency log external to the system, and the resulting inclusion proofs are retained, such that the existence and ordering of the agents' coordinated work is provable to third parties at globally-witnessed times without reliance on any clock or authority controlled by the system.

### Claim 9d (Dependent — Integration with the Completion Seal)

The system of Claim 9 in combination with the multi-party hash-rollup completion seal of Claim 8, wherein a mission coordinated via the blackboard, upon completion, has its contributing agents' navigation events and produced artifacts certified by the co-signature rollup and single-authority counter-signature of Claim 8, and the resulting sealed completion record's merkle root is itself appended to the blackboard ledger of Claim 9(a), such that strategic coordination, tactical execution, and cryptographic completion certification share one continuous hash-linked history.

---

## Part B: Detailed Description (Claim Area 9)

### B.1 The blackboard ↔ mission-graph duality

```mehrmaid
flowchart TD
  subgraph STRAT["Strategic — mission graph (the map)"]
    M1["$m_1$: enterprise.patent.foundation"]
    M2["$m_2$: enterprise.patent.metrics"]
    M1 -->|"bearing S"| M2
  end
  subgraph TACT["Tactical — blackboard ledger (executed reality, hash-chained)"]
    E0["$e_0$: nav · $m_1$ · S<br>$h_0 = \mathrm{SHA256}(\varnothing \,\Vert\, e_0)$"]
    E1["$e_1$: nav · $m_1$ · E<br>$h_1 = \mathrm{SHA256}(h_0 \,\Vert\, e_1)$"]
    E2["$e_2$: nav · $m_2$ · S<br>$h_2 = \mathrm{SHA256}(h_1 \,\Vert\, e_2)$"]
    E0 --> E1 --> E2
  end
  E0 -. "projects" .-> M1
  E2 -. "projects" .-> M2
```

### B.2 Stigmergic routing — the field, not the assignment

Each agent computes adjacency to its sisters and steers by it; no orchestrator
dispatches work. The relatedness of agents $a$ and $b$ is the term-overlap of their
mission coordinates:

```mehrmaid
flowchart LR
  A["Agent a @ $m_a$<br>terms = {enterprise, patent, foundation}"]
  B["Agent b @ $m_b$<br>terms = {enterprise, patent, metrics}"]
  ADJ["**Stigmergic adjacency**<br>$\mathrm{adj}(a,b) = \lvert \mathrm{terms}_a \cap \mathrm{terms}_b \rvert = 2$<br>→ a and b are sisters; coordinate via the field"]
  A --> ADJ
  B --> ADJ
```

### B.3 Why this scales to thousands

Naive coordination is $O(N)$ context per agent (read everyone). The indexed
frontier scanner collapses the read to distinct (mission, bearing) pairs:
$\text{cost} \propto \lvert \{(m, b)\} \rvert \ll N$. Combined with the
assignment-free routing of B.2 and the tamper-evident public ledger of B.1, the
substrate admits thousands of agents — including across independent tenants —
coordinating on related missions with verifiable integrity and no central
orchestrator. This is the scaling advance distinct from Claim 2 (which establishes
filesystem-local stigmergy): Claim 9 makes the substrate **public, hash-chained, and
sublinear-cost**, enabling cross-organization coordination at population scale.

### B.4 Reduction to practice

Embodiment: `.agents/skills/blackboard/SKILL.md` (the append-only `chart.jsonl`
ledger, w3w nav events, term-overlap adjacency), `forensics/mission-graph.json`
(the strategic DAG with `branch_*_edges`, `discovered_edges`, `braids`), and the
indexed frontier scanner (`scripts/2d_frontier_scanner_indexed.py`, the ~80%
index reduction documented in the specification). Hash-chaining reuses the COC
SHA-256 chain of Claim 1; public anchoring reuses the Sigstore Rekor pipeline of
Claim 8b.

---

*Prior-art note for the examiner: distinguish from (i) classical blackboard AI
architectures (centralized control shell, no hash-chain, no public/multi-tenant
verifiability, no sublinear indexed scan), (ii) blockchains (global consensus +
ordering overhead; here there is no consensus protocol — only an append-only
hash-linked coordination field with stigmergic routing), and (iii) pub/sub or
actor message-passing (direct addressed messaging; here coordination is indirect
via a shared environmental field with set-overlap adjacency).*
