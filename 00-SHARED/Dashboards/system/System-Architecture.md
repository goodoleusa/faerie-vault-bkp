---
type: system-design
stage: system
status: active
created: 2026-03-27
updated: 2026-03-27
tags: [system, architecture, visualization, dashboard, mermaid]
parent:
  - "[[HOME]]"
entry_point: "[[SYSTEM-DEV-HOME|← System Dev Home (start here)]]"
sibling:
  - "[[Session-Manifests]]"
  - "[[Nectar-View]]"
  - "[[SYSTEM-DEV-HOME]]"
child:
  - "[[system-state-files-guide]]"
doc_hash: sha256:ece33207edcf4fb54b0f413ada4e1bae0784c2cb0a41c455fd970fccec88d30d
hash_ts: 2026-03-29T16:10:16Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Session-Manifests|← Sessions]] · [[Nectar-View|← NECTAR]] · **System Architecture** · [[00-SHARED/Hive/_index|Hive →]]

> [!tip] Dev Entry Point
> For tools, eval scores, queue, and all design docs in one view: [[SYSTEM-DEV-HOME|System Dev Home →]]

# System Architecture

```dataviewjs
// Auto-generated TOC from headers
const content = await dv.io.load(dv.current().file.path);
const headers = content.match(/^#{2,3}\s+\d+\..+$/gm) || [];
dv.list(headers.map(h => {
  const text = h.replace(/^#+\s+/, '');
  const anchor = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
  return `[[#${text}|${text}]]`;
}));
```

> **Color language:** Gold = gateways (faerie/handoff). Teal = flowing state (work, scratch, queue). Pistachio = crystallized (HONEY, cards). Dark = immutable (forensics). Coral = human layer. **Same color = same process family.** Inputs and outputs of the same cycle share a color.

> **Design narratives**: [[design-narratives/_index|Design Docs Index]] | **Explorable graph**: [[pseudosystem/_index|Pseudosystem Map]]

---

## 0. Master Overview — The Hive


```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 60, 'rankSpacing': 60}, 'themeVariables': {
  'fontSize': '20px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#D4A843', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:4px,color:#1a1a2e,font-size:20px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef coral fill:#FF6B6B,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef dark fill:#2d2d44,stroke:#D4A843,stroke-width:3px,color:#e8e8e8,font-size:18px

    FAERIE(["/faerie<br/>orient + launch"]):::gold
    AGENTS[["Agents work<br/>learn + produce"]]:::teal
    HANDOFF(["/handoff<br/>collect + save"]):::gold
    CRYSTAL(("Crystallize<br/>denser knowledge")):::pist
    VAULT>"Vault<br/>human reviews"]:::coral
    FORENSIC[/"COC + Hashes <br/>= <br/>immutable proof"/]:::dark

    FAERIE ==>|"launches"| AGENTS
    AGENTS ==>|"produces"| HANDOFF
    HANDOFF ==>|"feeds"| CRYSTAL
    CRYSTAL ==>|"surfaces in"| VAULT
    VAULT ==>|"steers next"| FAERIE
    AGENTS -.->|"auto-logged"| FORENSIC

    linkStyle 0 stroke:#D4A843,stroke-width:4px
    linkStyle 1 stroke:#4ECDC4,stroke-width:4px
    linkStyle 2 stroke:#D4A843,stroke-width:4px
    linkStyle 3 stroke:#93C572,stroke-width:4px
    linkStyle 4 stroke:#FF6B6B,stroke-width:4px
    linkStyle 5 stroke:#2d2d44,stroke-width:2px,stroke-dasharray:8
```

> **The whole system is one circulation.** Gold gateways breathe in and out. Teal water flows. Pistachio crystals form. Coral warmth guides. Dark bedrock records. Each cycle, the crystals get denser and the outputs get better. **Shape language:** `([stadium])` = gateway, `[[subroutine]]` = process, `(())` = cycle, `>asymmetric]` = human, `[/parallelogram/]` = immutable.

---

## 1. The Cycle (Session Flow)

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px

    F(["/faerie — orient + launch"]):::gold
    W[["Agent Work"]]:::teal
    H(["/handoff — collect + save"]):::gold
    S[("handoff-snapshot.json")]:::pist

    F ==> W
    W ==> H
    H ==> S
    S ==>|"next session"| F
```

> Faerie and handoff are the **same gold** — they're the inhale and exhale of the same breath. Work flows between them like water.

---

## 2. Memory Temperature

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef hot fill:#FF6B6B,stroke:#1a1a2e,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef warm fill:#D4A843,stroke:#1a1a2e,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef cool fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef cold fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px

    HOT>"scratch-*.md — session notes"]:::hot
    WARM>"NECTAR.md — validated findings"]:::warm
    COOL>"HONEY.md — crystallized seed"]:::cold
    FROZEN>"forensics/ — immutable COC"]:::cool

    HOT ==>|"memory-keeper promotes"| WARM
    WARM ==>|"membot crystallizes"| COOL
    HOT -.->|"forensic_coc.py auto-logs"| FROZEN
```

> Heat decreases, density increases. Scratch is a rushing river. NECTAR is a lake. HONEY is a crystal. Forensics is bedrock.

---

## 3. Emergency Resilience

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#FF6B6B', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef alert fill:#FF6B6B,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px

    PANIC["Context at 1%"]:::alert
    SCRIPT(["emergency_handoff.py — 1.5 sec"]):::gold
    FILES[("snapshot + brief + atoms")]:::pist
    COMPACT["Auto-Compact"]:::alert
    NEXT(["/faerie reads snapshot"]):::gold

    PANIC ==> SCRIPT
    SCRIPT ==> FILES
    FILES ==> COMPACT
    COMPACT ==>|"next message"| NEXT
    FILES ==>|"survives compact"| NEXT
```

> The circuit breaker. Pure Python, no LLM. Writes durable files in 1.5 seconds. Everything survives the reset.

---

## 4. Two Memory Systems

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef broken fill:#FF6B6B,stroke:#FF6B6B,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px

    AUTO["Claude auto-memory<br/>51 fragments, 7+ folders"]:::broken
    BRIDGE(["emergency_handoff.py-->SHA256 + collect + dedupe"]):::gold
    OUR[("HONEY + NECTAR<br/>Canonical memory")]:::pist
    VAULT>"Vault: 00-SHARED/Hive/<br/>Human reviews collected"]:::teal

    AUTO ==> BRIDGE
    BRIDGE ==> OUR
    BRIDGE ==> VAULT
```

> Claude's auto-memory and our system are completely independent. The bridge hashes each file before touching it, deduplicates WSL/Windows variants, and promotes useful items.

---

## 5. Crystallization Cycle

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#93C572', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px

    NEW["New knowledge arrives"]:::teal
    READ["Read everything already known"]:::teal
    MERGE["Integrate: merge duplicates-->resolve contradictions-->form cross-references"]:::gold
    DENSE[("Denser, richer file-->Shorter but deeper")]:::pist

    NEW ==> READ
    READ ==> MERGE
    MERGE ==> DENSE
    DENSE ==>|"next round"| READ
```

> Not compression — crystallization. Like a saturated solution forming a crystal: more ordered, more dense, more useful. Each line carries more meaning.

---

## 6. Forensic Hash Chain

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef dark fill:#2d2d44,stroke:#D4A843,stroke-width:2px,color:#e8e8e8,font-size:16px
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px

    E1["Entry 1: sha256=abc-->prev=000000"]:::dark
    E2["Entry 2: sha256=def-->prev=hash(E1)"]:::dark
    E3["Entry 3: sha256=ghi-->prev=hash(E2)"]:::dark
    PROOF(["Court proof:<br/>File X had hash Y at time T<br/>Agent V1 produced finding F<br/>No later update biased F"]):::gold

    E1 ==> E2
    E2 ==> E3
    E3 ==> PROOF
```

> Bedrock. Each entry links to the previous. Tamper with one, the chain breaks. Write-only — agents can never read their own forensic logs.

---

## 7. Agent Learning

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef dark fill:#2d2d44,stroke:#D4A843,stroke-width:2px,color:#e8e8e8,font-size:16px

    TASK["Agent gets task"]:::gold
    WORK["Does work"]:::teal
    REFLECT["Reflects: what worked?"]:::teal
    BEAT{{"Beat score?"}}:::dark
    UPDATE["Snapshot old card-->Update Last Training"]:::pist
    QUEUE["Add to training queue<br/>with hypothesis of why"]:::dark

    TASK ==> WORK ==> REFLECT ==> BEAT
    BEAT ==>|"yes"| UPDATE
    BEAT ==>|"no"| QUEUE
    QUEUE ==>|"next /train"| TASK
    UPDATE ==>|"stronger next time"| TASK
```

> Every agent reflects after every run. ~2K tokens, invisible to you. They improve continuously, but only record process learnings — never case data.

---

## 8. Three Layers

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#D4A843', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef coral fill:#FF6B6B,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef dark fill:#2d2d44,stroke:#FF6B6B,stroke-width:2px,color:#e8e8e8,font-size:18px

    AGENT["Agent Layer<br/>Scratch, NECTAR, Agent-Outbox"]:::teal
    HUMAN["Human Layer<br/>30-Evidence, Annotations, Review"]:::coral
    FORENSIC["Forensic Layer<br/>COC, Hashes, Sprint Bundles"]:::dark

    AGENT ==>|"human promotes"| HUMAN
    AGENT -.->|"auto-logged"| FORENSIC
```

> Three rivers that never mix. Agents draft, humans validate, forensics records everything. The permission boundaries are the dams.

---

## 9. Context Budget (Equilibrium)

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#93C572', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px
    classDef over fill:#FF6B6B,stroke:#1a1a2e,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef ok fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef cycle fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px

    IN["Every session loads:<br/>Rules 274L + HONEY 138L<br/>+ Cards + CLAUDE.md<br/>~13K tokens"]:::gold
    CHECK{{"Over budget?"}}:::over
    XTAL["Crystallize first<br/>then add new content"]:::cycle
    WRITE["Write new knowledge"]:::ok
    OUT["Better outputs:<br/>more done, higher quality<br/>same context window"]:::gold

    IN ==> CHECK
    CHECK ==>|"yes"| XTAL ==> WRITE
    CHECK ==>|"no"| WRITE
    WRITE ==> OUT
    OUT ==>|"next session"| IN
```

> The budget IS the equilibrium. It forces crystallization. Crystallization makes knowledge denser. Denser knowledge means better outputs per token. Better outputs mean more gets done. More done means more knowledge. The cycle accelerates.

---

## 10. The Pipeline

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '16px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef dark fill:#2d2d44,stroke:#D4A843,stroke-width:2px,color:#e8e8e8,font-size:16px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:2px,color:#1a1a2e,font-size:16px

    P0["0a: Genesis — COC Ledger"]:::dark
    P1["1: Backup — B2 + Sync"]:::teal
    P2["2: Ingest — Raw to Manifest"]:::teal
    P3["3: Pipeline — Clean + Curate"]:::pist
    P4["4: Forensic — Sign + Verify"]:::dark
    P5["5: Publish — Site + IPFS"]:::gold
    P6["6: Archive — S3 WORM"]:::dark

    P0 ==> P1 ==> P2 ==> P3 ==> P4 ==> P5 ==> P6
```

---

## 11. Vault Flow

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#D4A843', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef coral fill:#FF6B6B,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:18px

    DRAFT["Agent writes draft-->Agent-Outbox/"]:::teal
    REVIEW["Human reviews-->Human-Inbox/"]:::coral
    ANNOTATE["Human annotates-->Your Annotations + Court Prep"]:::coral
    EVIDENCE["Human promotes-->30-Evidence/"]:::gold

    DRAFT ==> REVIEW
    REVIEW ==> ANNOTATE
    ANNOTATE ==> EVIDENCE
```

> Agents draft. Humans validate. Annotations are sacred — agents never touch them. The flow is one-directional: AI proposes, human disposes.

---

## 12. The Circulation (Everything Together)

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#D4A843', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px
    classDef coral fill:#FF6B6B,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:18px

    FAERIE(["/faerie reads crystal"]):::gold
    WORK[["Agents work, learn, flow"]]:::teal
    HANDOFF(["/handoff saves everything"]):::gold
    CRYSTAL[("Knowledge crystallizes")]:::pist
    HUMAN(["Human reviews, annotates"]):::coral

    FAERIE ==> WORK
    WORK ==> HANDOFF
    HANDOFF ==> CRYSTAL
    CRYSTAL ==> HUMAN
    HUMAN ==>|"steers next cycle"| FAERIE
```

> The whole system is a circulation. Gold gateways inhale and exhale. Teal water flows between them. Pistachio crystals form from the flow. Coral warmth guides the direction. Each cycle, the crystals get denser. Each cycle, the outputs get better. **That's the magic: we respected the physics, and the system found its own equilibrium.**

---

## 13. Data Analysis Engine (DAE → CyberTemplate)

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#D4A843', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef teal fill:#4ECDC4,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef dark fill:#2d2d44,stroke:#D4A843,stroke-width:2px,color:#e8e8e8,font-size:16px

    DAE(["data-analysis-engine<br/>Topic-agnostic template"]):::gold
    CT(["CyberTemplate<br/>Investigation-specific"]):::gold

    DAE ==>|"fork + specialize"| CT

    S0["0a: Genesis<br/>COC Ledger Init"]:::dark
    S1["1f-h: Backup<br/>B2 Sync + Verify"]:::teal
    S2["2a-f: Ingest<br/>>Raw → Hash → Manifest"]:::teal
    S3["3a-d: Pipeline<br/>Clean → Transform → Curate"]:::pist
    S4["4a-b: Forensic<br/>Sign + Run"]:::dark
    S5["5a-b: Publish<br/>Site + IPFS Pin"]:::gold
    S6["6a: Archive<br/>S3 WORM Backup"]:::dark

    CT ==> S0
    S0 ==> S1
    S1 ==> S2
    S2 ==> S3
    S3 ==> S4
    S4 ==> S5
    S5 ==> S6
```

> DAE is the reusable engine. CyberTemplate is the investigation that runs on it. Every numbered script is court-ready: hashed inputs, signed outputs, COC at every step.

---

## 14. DAE Script Pipeline (Detailed)

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '16px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#4ECDC4', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef ingest fill:#4ECDC4,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:16px
    classDef pipe fill:#93C572,stroke:#D4A843,stroke-width:3px,color:#1a1a2e,font-size:16px
    classDef forensic fill:#2d2d44,stroke:#D4A843,stroke-width:3px,color:#e8e8e8,font-size:16px
    classDef publish fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:16px

    A["2a: ingest-rawdata<br/>Scan all source files"]:::ingest
    B["2b: hash-guardian<br/>SHA256 every file"]:::forensic
    C["2c: ingest-tabular<br/>CSV/JSON/Excel → normalized"]:::ingest
    D["2e: rawdata-manifest<br/>Build evidence manifest"]:::ingest
    E["2f: build-manifest<br/>Full project manifest"]:::ingest

    A ==> B ==> C ==> D ==> E

    F["3a: pipeline-orchestrator<br/>Run full pipeline"]:::pipe
    G["3b: pipeline-clean<br/>Dedupe, validate, fix"]:::pipe
    H["3c: pipeline-transform<br/>Normalize, enrich, cross-ref"]:::pipe
    I["3d: pipeline-curate<br/>Tier, rank, evidence bundle"]:::pipe

    E ==> F ==> G ==> H ==> I

    J["4a: forensic-sign<br/>GPG sign + hash manifest"]:::forensic
    K["5a: publish-pipeline<br/>Build static site"]:::publish
    L["5b: ipfs-publish<br/>Pin to IPFS + OTS stamp"]:::publish

    I ==> J ==> K ==> L
```

> 18 scripts, each numbered. Improvements to DAE benefit every investigation that forks from it. CyberTemplate adds investigation-specific scripts in `scripts/custom/`.

---

## 15. Design Process Log

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis'}, 'themeVariables': {
  'fontSize': '18px', 'fontFamily': 'Inter, system-ui',
  'lineColor': '#93C572', 'background': '#1a1a2e'
}}}%%
graph TD
    classDef gold fill:#D4A843,stroke:#1a1a2e,stroke-width:3px,color:#1a1a2e,font-size:18px
    classDef pist fill:#93C572,stroke:#D4A843,stroke-width:2px,color:#1a1a2e,font-size:16px
    classDef dark fill:#2d2d44,stroke:#D4A843,stroke-width:2px,color:#e8e8e8,font-size:16px

    IDEA["Design idea<br/>in session"]:::gold
    DOC["Write design doc-->design-narratives/"]:::pist
    HASH["SHA256 + timestamp-->design-coc.jsonl"]:::dark
    VAULT["Vault note<br/>with frontmatter"]:::pist
    PROOF(["Timestamped proof:<br/>you had this idea<br/>at this date"]):::gold

    IDEA ==> DOC
    DOC ==> HASH
    HASH ==> VAULT
    VAULT ==> PROOF
```

> Every design doc gets hashed when created. The design COC proves: "This architecture was designed by this person at this time." If anyone challenges IP, the hash chain + git history + session transcripts prove provenance.

---

## Your Annotations

<!-- What's missing? What processes are still invisible? -->

