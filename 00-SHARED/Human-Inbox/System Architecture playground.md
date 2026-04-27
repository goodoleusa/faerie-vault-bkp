---
created: 2026-03-28
updated: 2026-03-28
type: system-design
status: active
tags: [hive, architecture, system-design, piston-model, memory, forensics, modularity]
aliases: [Piston Model, Hive Frame, System Map]
parent:
  - "[[_system-root]]"
  - "[[../Hive/System-Architecture|System-Architecture]]"
doc_hash: 
hash_ts: 2026-03-29T16:10:27Z
hash_method: body-sha256-v1
---

# Hive Frame — System Architecture

> **Start here:** [[SYSTEM-GUIDE]] for a full clickable learning guide.

## Related Docs

### Deep Dives (by diagram section)

| Diagram | Deep-dive doc | Pseudosystem component |
|---------|--------------|----------------------|
| Piston engine | [[PISTON-MODEL-DESIGN]] | [[session-lifecycle]] |
| Session lifecycle | [[faerie-start]] / [[handoff-end]] | [[emergency-handoff]] |
| Memory architecture | [[13-MEMORY-FLOW-ARCHITECTURE]] | [[memory-layer]] / [[honey-seed]] / [[nectar-narrative]] |
| faerie's role | [[11-FAERIE-IMPACT-AB]] | [[faerie-start]] / [[subagent-spawning]] |
| Three independent systems | [[system-state-files-guide]] | [[state-engine]] / [[context-budget]] |
| Forensics isolation | [[HOW-ANNOTATION-COC-WORKS]] | [[forensic-layer]] / [[coc-hash-chain]] |
| Data flow | [[PIPELINE-DESIGN]] | [[agent-outbox]] / [[vault-layer]] |
| Modular sauce | [[15-MODULAR-SECRET-SAUCE]] | — |

### Related Design Narratives
```dataview
LIST
FROM "00-SHARED/Hive"
WHERE (type = "system-design" OR type = "design-narrative" OR type = "narrative")
  AND file.name != this.file.name
SORT default(updated, created) DESC
```


<executed_result>
- [[00-SHARED/Hive/DAE-Scripts-Architecture.md]]
- [[00-SHARED/Hive/Trail-Protocol.md]]
- [[00-SHARED/Hive/13-MEMORY-FLOW-ARCHITECTURE.md]]
- [[00-SHARED/Hive/14-SCRATCH-DUMP-PROCESSING-STATE.md]]
- [[00-SHARED/Hive/15-MODULAR-SECRET-SAUCE.md]]
- [[00-SHARED/Hive/System-Architecture.md]]
- [[00-SHARED/Hive/DAE-Evolution-Narrative.md]]
- [[00-SHARED/Hive/PISTON-MODEL-DESIGN.md]]
- [[00-SHARED/Hive/15-SKILLS-EVOLUTION-NARRATIVE-2026-03-29.md]]
- [[00-SHARED/Hive/18-blueprint-system-design.md]]
</executed_result>




### Component Notes Referenced

<dataview_block>
<query_type>dataview</query_type>
<original_query>
TABLE WITHOUT ID
  link(file.link, file.name) AS "Component",
  component_type AS "Type"
FROM "00-SHARED/Hive/pseudosystem"
WHERE contains(["session-lifecycle", "memory-layer", "honey-seed", "nectar-narrative", "forensic-layer", "coc-hash-chain", "faerie-start", "handoff-end", "agent-layer", "subagent-spawning", "state-engine", "context-budget", "equilibrium", "crystallization", "sprint-queue", "vault-layer", "agent-outbox"], file.name)
SORT component_type ASC, file.name ASC
</original_query>
<executed_result>
| Component | Type |
| --- | --- |
| [[00-SHARED/Hive/pseudosystem/crystallization.md]] | cycle |
| [[00-SHARED/Hive/pseudosystem/agent-layer.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/equilibrium.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/forensic-layer.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/memory-layer.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/session-lifecycle.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/state-engine.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/vault-layer.md]] | layer |
| [[00-SHARED/Hive/pseudosystem/faerie-start.md]] | process |
| [[00-SHARED/Hive/pseudosystem/handoff-end.md]] | process |
| [[00-SHARED/Hive/pseudosystem/subagent-spawning.md]] | process |
| [[00-SHARED/Hive/pseudosystem/agent-outbox.md]] | state |
| [[00-SHARED/Hive/pseudosystem/coc-hash-chain.md]] | state |
| [[00-SHARED/Hive/pseudosystem/context-budget.md]] | state |
| [[00-SHARED/Hive/pseudosystem/honey-seed.md]] | state |
| [[00-SHARED/Hive/pseudosystem/nectar-narrative.md]] | state |
| [[00-SHARED/Hive/pseudosystem/sprint-queue.md]] | state |
</executed_result>
</dataview_block>

---

## The Piston: Session Engine 🔧

```mermaid
graph TD
    subgraph PISTON["PISTON ENGINE"]
        direction TB
        W1["FAST<br/>~45s<br/>Explore<br/>Security<br/>Admin"]
        W2["MEDIUM<br/>~3min<br/>Python<br/>Data Eng<br/>Evidence"]
        W3["DEEP<br/>~10min<br/>Data Sci<br/>Research<br/>Curate"]

        W1 -->|"relaunch"| W1
        W1 -->|"30s delay"| W2
        W2 -->|"90s delay"| W3
        W3 -->|"new cycle"| W1
    end

    classDef fast fill:#4a9eff,color:#fff
    classDef med fill:#f5a623,color:#fff
    classDef deep fill:#d0021b,color:#fff
    classDef piston fill:#1a1a2e,color:#fff

    class W1 fast
    class W2 med
    class W3 deep
    class PISTON piston
```

## Session Lifecycle

```mermaid
graph TD
    subgraph SESSION["Session Lifecycle"]
        F["/faerie<br/>START"] --> WORK["Work<br/>Piston"]
        WORK --> H["/handoff<br/>END"]
        WORK -.->|"mid"| C["/crystallize"]
        C -.-> WORK
    end

    subgraph COMPACT["Auto-Compact"]
        AC["Context full"] --> PRE["pre_compact<br/>checkpoint"]
        PRE --> SQUISH["Compact<br/>summarize"]
        SQUISH --> RESUME["scheduler<br/>resume"]
        RESUME --> WORK
    end

    classDef start fill:#7b68ee,color:#fff
    classDef end fill:#e74c3c,color:#fff
    classDef cryst fill:#2ecc71,color:#fff
    classDef compact fill:#95a5a6,color:#fff
    classDef resume fill:#4a9eff,color:#fff

    class F start
    class H end
    class C cryst
    class AC,PRE,SQUISH compact
    class RESUME resume
```

## Memory Architecture: Separate Systems

```mermaid
graph TB
    subgraph WORKING["Working (per-session)"]
        SCRATCH["scratch-{SID}<br/>Raw obs<br/>MEM blocks"]
    end

    subgraph DURABLE["Durable (cross-session)"]
        HONEY["HONEY.md<br/>Prefs & methods"]
        NECTAR["NECTAR.md<br/>Findings<br/>Append-only"]
        REVIEW["REVIEW-INBOX<br/>HIGH flags"]
    end

    subgraph FORENSIC["Forensic (agent-blind)"]
        COC["forensic-coc<br/>Hash-chain"]
        MANIFEST["manifests"]
        BRIEFS["briefs/"]
    end

    SCRATCH -->|"membot"| NECTAR
    SCRATCH -->|"HIGH"| REVIEW
    NECTAR -->|"cryst"| HONEY
    SCRATCH -->|"append"| COC

    classDef working fill:#2d3436,color:#fff
    classDef durable fill:#0c3c26,color:#fff
    classDef forensic fill:#4a0000,color:#fff
    classDef honey fill:#f1c40f,color:#000
    classDef nectar fill:#e67e22,color:#fff
    classDef review fill:#e74c3c,color:#fff
    classDef coc fill:#7f0000,color:#fff

    class WORKING working
    class DURABLE durable
    class FORENSIC forensic
    class HONEY honey
    class NECTAR nectar
    class REVIEW review
    class COC coc
```

## faerie's Role: Orchestrator, Not Worker

```mermaid
graph TB
    subgraph FAERIE["faerie (Orchestrator)"]
        ORIENT["1. Orient<br/>Read HONEY<br/>brief"]
        PLAN["2. Plan<br/>piston"]
        LAUNCH["3. Launch<br/>Agents xN"]
        CONDUCT["4. Conduct<br/>Process<br/>Relaunch"]
        SYNTH["5. Synthesize<br/>Connect"]
    end

    subgraph AGENTS["Subagents (200K)"]
        A1["evidence<br/>analyst"]
        A2["python-pro"]
        A3["data-sci"]
        A4["membot"]
    end

    subgraph QUEUE["Queue"]
        QF["sprint-queue<br/>.json"]
        KB["Kanban<br/>Obsidian"]
    end

    ORIENT --> PLAN --> LAUNCH
    LAUNCH --> AGENTS
    AGENTS --> CONDUCT
    CONDUCT --> SYNTH
    CONDUCT --> LAUNCH
    SYNTH --> QF
    QF <--> KB

    classDef faerie fill:#2c1654,color:#fff
    classDef agents fill:#1a3a5c,color:#fff
    classDef queue fill:#1a3c1a,color:#fff

    class FAERIE faerie
    class AGENTS agents
    class QUEUE queue
```

## Three Independent Systems

```mermaid
graph TB
    subgraph PHASES["Context Phases"]
        CP["context_phase.py"]
        CP --> LIFT["LIFTOFF<br/>0-30%"]
        CP --> ORB["ORBIT<br/>30-70%"]
        CP --> DEO["DEORBIT<br/>70-85%"]
        CP --> REE["REENTRY<br/>85%+"] 
    end

    subgraph SURFACING["Surfacing Scheduler"]
        SS["surfacing<br/>scheduler.py"]
        SS --> PLAN2["Wave plan"]
        SS --> CAL["Calibrate"]
        SS --> RESUME2["Resume"]
    end

    subgraph METRICS["Metrics"]
        SM["session<br/>metrics.py"]
        SM --> KPI["7 KPIs"]
        SM --> TREND["Trends"]
    end

    KPI --> CAL

    classDef phases fill:#34495e,color:#fff
    classDef surf fill:#2c3e50,color:#fff
    classDef metrics fill:#1a252f,color:#fff

    class PHASES phases
    class SURFACING surf
    class METRICS metrics
```

## Forensics Isolation Architecture

```mermaid
graph TB
    subgraph REPOS["Repos"]
        CT["cybertemplate<br/>forensics/"]
        DAE["DAE<br/>forensics/"]
        F2["faerie2<br/>forensics"]
    end

    subgraph GLOBAL["Global"]
        GF["~/.claude<br/>memory/forensics"]
    end

    subgraph DENY["Agent Access"]
        R["Read: DENIED"]
        W["Write: APPEND"]
    end

    REPOS --> R
    REPOS --> W
    GLOBAL --> R

    classDef repos fill:#4a0000,color:#fff
    classDef globalf fill:#4a0000,color:#fff
    classDef deny fill:#2d3436,color:#fff
    classDef read fill:#c0392b,color:#fff
    classDef write fill:#27ae60,color:#fff

    class REPOS,GLOBAL repos
    class DENY deny
    class R read
    class W write
```

## Data Flow: End to End

```mermaid
graph TD
    USER["Human"] -->|"/faerie"| SESSION["Session"]
    SESSION -->|"waves"| AGENTS["Agents"]
    AGENTS -->|"findings"| SCRATCH["Scratch"]
    SCRATCH -->|"membot"| NECTAR["NECTAR"]
    NECTAR -->|"cryst"| HONEY["HONEY"]
    AGENTS -->|"append"| FORENSICS["Forensics"]
    SESSION -->|"sync"| OBSIDIAN["Obsidian"]
    OBSIDIAN <-->|"kanban"| SESSION
    USER -->|"notes"| OBSIDIAN
    SESSION -->|"/handoff"| BRIEF["brief.json"]

    classDef user fill:#8e44ad,color:#fff
    classDef session fill:#2c1654,color:#fff
    classDef agents2 fill:#1a3a5c,color:#fff
    classDef scratch fill:#2d3436,color:#fff
    classDef nectar2 fill:#e67e22,color:#fff
    classDef honey2 fill:#f1c40f,color:#000
    classDef forensics2 fill:#4a0000,color:#fff
    classDef obsidian fill:#6c3483,color:#fff
    classDef brief fill:#2980b9,color:#fff

    class USER user
    class SESSION session
    class AGENTS agents2
    class SCRATCH scratch
    class NECTAR nectar2
    class HONEY honey2
    class FORENSICS forensics2
    class OBSIDIAN obsidian
    class BRIEF brief
```

## Modular Secret Sauce: Paid Feature Architecture

The system supports two build modes: **full** (all features) and **open** (sauce modules removed).
Proprietary modules enhance specific pain points. Remove them and the core still works — just simpler.

```mermaid
graph TB
    subgraph CORE["CORE (always)"]
        SS["scheduler.py<br/>Classify<br/>Batch<br/>Calib"]
        PCH["pre_compact<br/>Drain HIGH<br/>Snapshot"]
        QS["queue_ops<br/>Sprint queue"]
        MEM["Memory route"]
        COC2["forensic_coc"]
        AGT["Agent spawn"]
    end

    subgraph SAUCE["SAUCE (removable)"]
        PI["piston.py<br/>Waves<br/>Rhythm"]
        ON["overnight<br/>synth"]
        CP2["cryst<br/>premium"]
        TL["training<br/>loop"]
    end

    SS -->|"try piston"| PI
    SS -.->|"fallback"| SS

    classDef core fill:#1a3a5c,color:#fff
    classDef sauce fill:#4a0e0e,color:#fff
    classDef pis fill:#d4a017,color:#000

    class CORE core
    class SAUCE sauce
    class PI pis
```

### How It Works

```mermaid
sequenceDiagram
    participant C as Scheduler
    participant P as piston.py
    participant F as Fallback

    Note over C: try: import piston
    alt Full build
        C->>P: plan(tasks)
        P-->>C: waves[...]
    else Open build
        C->>F: batch(tasks)
        F-->>C: batch[...]
    end
```

### Pain Points Each Sauce Module Addresses

```mermaid
graph LR
    subgraph PAIN["Pain Points"]
        P1["Returns cluster<br/>at compact"]
        P2["Redundant re-reads<br/>post-compact"]
        P3["No cross-session<br/>learning"]
        P4["Lost deep insights<br/>at peak"]
    end

    subgraph FIX["Sauce Fixes"]
        F1["piston.py<br/>Timed waves"]
        F2["piston<br/>checkpoint"]
        F3["training_loop"]
        F4["overnight_synth"]
    end

    P1 --> F1
    P2 --> F2
    P3 --> F3
    P4 --> F4

    classDef pain fill:#5c1a1a,color:#fff
    classDef fix fill:#1a3a1a,color:#fff
    classDef gold fill:#d4a017,color:#000

    class PAIN pain
    class FIX fix
    class F1,F2,F3,F4 gold
```

### Removal Protocol

```bash
# Find all sauce modules
grep -rl '__removable__' ~/.claude/scripts/

# Remove before interview
rm ~/.claude/scripts/piston.py
rm ~/.claude/scripts/overnight_synthesis.py
rm ~/.claude/scripts/crystallize_premium.py
rm ~/.claude/scripts/training_loop.py

# Verify: everything still works
python3 ~/.claude/scripts/surfacing_scheduler.py plan   # flat_fallback model
python3 ~/.claude/scripts/surfacing_scheduler.py resume  # "no_piston_module" status
echo '{}' | python3 ~/.claude/hooks/pre_compact_hook.py  # steps 1-4 work, step 5 skipped
```

## Key Separations

| System | What it is | What it is NOT |
|---|---|---|
| **faerie** | Session orchestrator (read → launch → conduct) | Not a worker — never does task work inline |
| **HONEY** | Sacred preferences/methods earned through time | Not a scratchpad — entries are crystallized, not appended |
| **NECTAR** | Append-only validated findings | Not compressible — forensic truth record |
| **Forensics** | Agent-blind COC at repo root | Not in .claude/ — agents can't read it |
| **Vault** | Human-readable interface / message bus | Not canonical storage — repos are canonical |
| **Queue** | Sprint task list with COC on transitions | Not ephemeral — completed tasks are evidence |
| **Piston** | Three-speed agent wave rhythm (sauce) | Not a scheduler — it's a rhythm (fast/medium/deep/cycle) |
| **Crystallization** | Multi-mind knowledge forging (agents + human + time) | Not compression — integration makes text richer, not shorter |
| **Sauce modules** | `__removable__` scripts enhancing pain points | Not load-bearing — core works without them |

## Blueprint Registry

Agent output types have canonical schema definitions in `Hive/blueprints/`.
Each blueprint specifies required frontmatter, section structure, validation rules,
and links to an example output. Reference via `blueprint: blueprint_{type}` in frontmatter.

### Active Blueprints

| Blueprint | Type | Output Dir | Example |
|-----------|------|------------|---------|
| [[blueprints/blueprint_finding\|blueprint_finding]] | finding | Agent-Outbox/findings/ | (see blueprint) |
| [[blueprints/blueprint_analysis\|blueprint_analysis]] | analysis | Agent-Outbox/analysis/ | (see blueprint) |
| [[blueprints/blueprint_evidence\|blueprint_evidence]] | evidence | Agent-Outbox/evidence/ | (see blueprint) |
| [[blueprints/blueprint_report\|blueprint_report]] | report | Agent-Outbox/reports/ | (see blueprint) |
| [[blueprints/blueprint_brief\|blueprint_brief]] | brief | Session-Briefs/ | (see blueprint) |
| [[blueprints/blueprint_agent_evolution\|blueprint_agent_evolution]] | agent-evolution | Agent-Outbox/agent-evolution/ | [[Agent-Outbox/agent-evolution/example-agent-evolution\|example]] |
| [[blueprints/blueprint_droplet\|blueprint_droplet]] | droplet | Dashboards/Droplets/ | [[Agent-Outbox/droplets/example-droplet-LIVE\|example]] |
| [[blueprints/blueprint_dashboard\|blueprint_dashboard]] | dashboard | Dashboards/ | [[Agent-Outbox/dashboards/example-dashboard\|example]] |
| [[blueprints/blueprint_session_manifest\|blueprint_session_manifest]] | session-manifest | Dashboards/session-briefs/ | [[Dashboards/session-briefs/example-session-manifest\|example]] |
| [[blueprints/blueprint_design_insight\|blueprint_design_insight]] | design-narrative | Hive/ | [[18-blueprint-system-design\|18 — Blueprint System]] |

### How to Use a Blueprint

When writing an agent output file, set `blueprint: blueprint_{type}` in frontmatter.
Read the blueprint file to get required fields and sections. The blueprint is the
single source of truth for that output type — not VAULT-SCHEMA.md (which remains the
canonical universal spec but is too large to consult at write time).

For spawn prompts, include:
```
Blueprint for this output type: 00-SHARED/Hive/blueprints/blueprint_{type}.md
Read it before writing your output file.
```

See [[18-blueprint-system-design]] for the ADR explaining why this system was created.
