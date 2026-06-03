# Deep Dive 1: Biosemiotics — The Signal Loop

## Diagram: Signal → Interpretation → Action Loop

This diagram shows how faerie2 mirrors biosemiotic signaling in living systems:

```mermaid
graph LR
    A["Agent 1<br/>(Completes Task)"] -->|Writes manifest<br/>with discovered_work[]| B["Manifest File<br/>(Pheromone Trail)<br/>mission=foo<br/>bearing=N"]
    B -->|Mission field = 'foo'<br/>Bearing = 'N'| C["Agent 2<br/>(Reads frontier)"]
    C -->|Interprets:<br/>'Here is unblocked work'| D["Agent 2<br/>(Claims work)"]
    D -->|Appends to<br/>discovered_work[]| E["Updated Manifest<br/>(Next agent reads)"]
    E -->|Cycle repeats| F["Emergent mission<br/>DAG completion"]
    
    style B fill:#e1f5ff
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style F fill:#e8f5e9
```

## Key Points

**Signal carriers (Manifests):**
- Carry `mission` field (clustering signal)
- Carry `bearing` field (N/S/E/W interpretation)
- Carry `quality_score` (signal vigor)
- Are passive — no sender intent required

**Interpretation (Agent frontier scanning):**
- Agent reads manifest
- Filters by `mission` field (receiver selectivity)
- Ranks by `bearing` and `quality_score`
- Decides autonomously whether to claim work

**Action (Work claim):**
- Agent appends to `discovered_work[]`
- Next agent reads the update
- Cycle continues without central planner

**Emergence property:** System coherence (mission DAG completion) emerges from local signal-response interactions, not from top-down planning.

## Analogy to Biology

In a cell:
1. Ligand (signal molecule) approaches receptor
2. Receptor interprets meaning ("grow", "divide", "die")
3. Cell acts on interpretation
4. New state triggers new signals

In faerie2:
1. Manifest (signal document) is discovered by agent
2. Agent interprets bearing and mission field ("work here", "unblock this", "backtrack")
3. Agent acts (claims work, appends discovery)
4. Updated manifest triggers next agent response

Both are **meaning-making systems**: signals become meaningful through receiver interpretation, not sender intent.

---

**Reference:** CROSS-DOMAIN-DEEP-DIVES.md, Deep Dive 1
