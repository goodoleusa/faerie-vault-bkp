---
type: overview
status: Todo
created: 2026-03-15
updated: 2026-03-23
tags:
  - overview
  - architecture
  - swarmy
doc_hash: sha256:075d0b9e3395a849be70c7781a5d043264df88d9a07394b9ee8b099bd5380fcc
hash_ts: 2026-03-29T16:16:46Z
hash_method: body-sha256-v1
---

# Swarmy — Self-Evolving AI Swarm for OSINT Investigations

> *Scout bees don't report to a manager. They fly out, find something, come back, and dance.
> The hive listens. The best dance wins. The swarm moves together.*

---

## The 2026 Shift

Something changed in AI around 2025. The assumption that one frontier model should handle
everything — analyst, researcher, writer, memory-keeper — all in one continuous context —
started showing its limits. Not because the models got worse. Because the work got bigger.
And because researchers started noticing something uncomfortable: you could get better
science out of smaller models by keeping them isolated from each other.

The unlock wasn't a better model. It was **routing** — and what routing implies about how
knowledge should flow between agents who can't see each other's work.

### The cost argument — why the math matters

**Model pricing (2026):**

| Model | Input | Output | Use for |
|---|---|---|---|
| Haiku | $1 / 1M tokens | $5 / 1M tokens | Extraction, classification, bulk work |
| Sonnet | $3 / 1M tokens | $15 / 1M tokens | Analysis, synthesis — the daily driver |
| Opus | $5 / 1M tokens | $25 / 1M tokens | Architecture, complex reasoning only |

Route each step to the right model and you're already paying 3–5× less per task. But
the deeper problem is what happens inside a single long-running session.

**The accumulation problem — why chatbot costs grow quadratically:**

Every API turn resends the full conversation history. The longer you run, the more you
pay — and you pay for the same content on every subsequent turn:

```
One agent, 4 research tasks — sequential:

Turn 1: [system 5K] + [task1 data 20K]                               = 25K billed
Turn 2: [system 5K] + [task1 20K] + [reply 2K] + [task2 20K]        = 47K billed
Turn 3: [system 5K] + [all above] + [reply 2K] + [task3 20K]        = 74K billed
Turn 4: [system 5K] + [all above] + [reply 2K] + [task4 20K]        = 101K billed
                                                              ──────────────
                                                 TOTAL:       247K tokens

Task 1's data was billed 4 times. Task 2's, 3 times. Each turn pays a growing tax.
```

This is why chatbot sessions spiral. Not just the tokens — the *repeated billing of
the same tokens* on every turn. Context history is a compounding liability.

**The subagent solution — parallel, isolated, fixed cost per agent:**

```
4 agents, same 4 tasks — parallel:

Agent 1: [system 5K] + [task1 data 20K]  = 25K  →  2K summary
Agent 2: [system 5K] + [task2 data 20K]  = 25K  →  2K summary   ← same time
Agent 3: [system 5K] + [task3 data 20K]  = 25K  →  2K summary   ← same time
Agent 4: [system 5K] + [task4 data 20K]  = 25K  →  2K summary   ← same time
Coord:   [system 5K] + [4 summaries 8K]  = 13K  →  synthesis
                                           ──────────────
                             TOTAL:        113K tokens    ←  54% less
                             TIME:         1 agent's runtime, not 4×
```

Now add **prompt caching** — the shared system prompt is written to cache once, then
served at 10% of normal price on every subsequent agent call:

```
Cached system prompt across 4 agents:
  Write once: $0.015/1M  →  Read 3× more: $0.30/1M (90% off)
  Effective total: ~96K token-equivalents  ←  61% less than monolithic
```

Stack the **Batch API** (50% off all non-realtime work — which describes every
overnight agent run by definition) and the combined savings reach **70–89%**.

**The five levers — stack them all:**

- **Subagent isolation** — each agent sees only its own data. No accumulation. Adding
  a fifth agent adds a flat cost, not a quadratic one.
- **Prompt caching** — stable context (mission brief, agent instructions, knowledge base)
  written once, served at 90% discount on every subsequent agent call. A 5K system prompt
  shared across 8 agents costs almost nothing after the first.
- **Model routing** — Haiku at $1/M does extraction identically to Opus at $5/M. Five times
  cheaper for tasks where reasoning depth doesn't change the output.
- **Parallel execution** — 4 agents finish in 1 agent's time. Throughput scales with team
  size; marginal API cost doesn't.
- **Batch API** — any overnight or non-realtime work qualifies for 50% off. Swarmy's
  agent runs are batch by default. The savings happen automatically.

**How costs balloon vs. collapse — the actual numbers:**

Naive: one agent, one model, no caching, no routing, sequential:
```
8-task investigation, 20K tokens each, all Opus:
  8 sequential turns with full accumulation → ~900K tokens billed
  900K × $5/M = ~$4.50 for one investigation run
```

Optimized: parallel isolated agents, cached prompts, routed models, batch:
```
Same 8 tasks:
  Haiku agents for research, Sonnet for analysis, cached system prompt, batch API
  ~180K effective token-equivalents at mixed pricing → ~$0.25
```

**Same work. ~94% lower cost. 8× faster wall-clock time.**

**Why not just use the chatbot?**

Because you can't optimize what you can't observe.

When you chat with Claude.ai — or even run Claude Teams — you have zero visibility into
how many tokens each turn consumed, whether your stable content is being cached, what
each query actually costs, or whether you're routing to the right model. The bill arrives
at the end of the month and you have no idea what drove it.

Swarmy is the opposite. Every agent run logs exact token usage, cache hit ratios, actual
cost per call, and savings vs unoptimized. `python usage_report.py --days 7` shows your
actual weekly savings broken down by model and batch vs standard. The discipline of the
system forces the optimization — you can't accidentally send your knowledge base to Opus
fifty times without it appearing in the logs.

The setup is harder than opening a chat window. That's the point. What you give up in
simplicity, you get back in observability, cost predictability, quality through
specialization, and a system that gets *cheaper* as it scales — instead of more expensive.

### The epistemic argument

This is the part that doesn't show up in cost calculators — and it's more important.

When you're deep in investigation data for hours — reading documents, following financial
threads, pattern-matching across hundreds of rows — something happens to your cognition.
You get lost in the sauce. The big picture blurs. Recency bias pulls you toward whatever
you just read. And most insidiously: you start unconsciously designing your analysis around
conclusions you've already half-formed.

This is p-value hacking. Not fraud — just human. The same researcher who generated the
hypothesis runs the significance test on data they've already partially interpreted. The
result looks rigorous. The process was not.

**Splitting work across stateless agents removes this by architecture.**

- **Agent A** designs the hypothesis and experiment structure — before touching any results
- **Agent B**, in a completely fresh context with no knowledge of what A found, runs the
  analysis and assigns significance
- **Agent C** attacks the hypothesis from an adversarial position — alternative explanations,
  confounds, what the data conspicuously does *not* show

No agent can p-hack, because no agent has seen what the other found. No agent gets lost
in the sauce, because each has a bounded task with a bounded context. The zoomed-out view
is never lost — because maintaining it is the orchestrator's explicit job, not an afterthought
that gets dropped when the investigation gets intense.

You get the epistemic equivalent of pre-registration without the ceremony: the experiment
design is locked before the analyst sees the results. And you get a built-in adversarial
reviewer for free.

---

## The Metaphors

Two ideas underpin everything in this system. Understand these and the rest clicks.

### The Swarm

A honeybee colony solves problems no single bee could solve. Scouts fly out independently,
each seeing only their small slice of the world. They return and perform a waggle dance —
direction and vigor encode what they found. Other bees evaluate the dances. The best lead
attracts more dancers. When enough bees are dancing the same dance, the swarm reaches
consensus and moves.

No bee has the full picture. No central coordinator decides. The intelligence is collective,
emergent, and self-correcting.

**This system works the same way.** Each AI agent is a scout — it takes a task, flies into
the data, and writes its findings to the shared vault (the waggle dance, encoded in
markdown). A memory-keeper evaluates all scouts' reports and promotes the strongest signals.
You, the human reviewer, are the queen: strategic, high-level, final authority. Nothing
becomes permanent without your `- [x]`. The swarm doesn't move until you've seen the dance.

The key insight: **agents communicate through the vault, never directly with each other.**
Just as bees dance in the shared space and the colony reads it — no direct bee-to-bee
handoffs, no private channels. The dance floor is the only medium. This is what makes the
isolation real: agents can't leak their conclusions to each other even if they tried.

The swarm also **teaches itself.** At the end of every sprint, the memory-keeper reviews
friction (PAIN entries from agents' scratchpads) and novel patterns (IDEA entries).
Recurring friction gets a targeted fix proposed to `improvement-proposals.md`. Session by
session, driven by evidence from actual runs — not by the designer's assumptions — the
swarm gets better at its own work.

### Dead Reckoning

Before GPS, ships navigated by dead reckoning: track your last known position, your
heading, your speed, your elapsed time. No external lookup. No satellite. Just accumulated,
disciplined knowledge of where you've been — and confidence that it tells you where you are.

Most AI systems navigate by search: embed a question, find the nearest vectors, retrieve
chunks. It works, but it's expensive, lossy, and opaque. You don't know exactly what the
model read or why it trusted it.

**This system navigates by dead reckoning.** Every agent starts from a known position:
the mission brief, validated facts from the knowledge base, compact entity stubs for the
people and organizations involved, and handoff notes from the last agent. No vector
database. No retrieval black box. The agent knows exactly what it knows and where it came
from — because you can read every file it loaded.

Context is treated like fuel: **finite, precious, non-refundable.** You can't unspend a
token. So the system loads context in tiers — the most important information first, filling
the tank from the top down, stopping when it's full. Nothing irrelevant burns the budget.
The ship knows its position because it chose its inputs deliberately.

---

## What This Gives You

**60–70% cost reduction, 4× throughput.** Not from a cheaper model — from routing the right
work to the right model and running multiple agents in parallel. Haiku handles bulk
extraction. Sonnet handles analysis. Opus handles architecture decisions. The math compounds
quickly across large investigations.

**Epistemic hygiene by architecture.** Stateless, isolated agents mean hypothesis
generation and significance testing happen in separate contexts with no shared history.
You structurally prevent p-value hacking and recency bias — not by training researchers
to be more careful, but by making the contamination path impossible. Alternative hypotheses
are a first-class agent role, built into the team composition.

**Never lost in the sauce.** The orchestrator maintains the 30,000-foot view while scouts
are nose-down in the data. The memory-keeper keeps big-picture coherence across sessions.
You always have somewhere to zoom out to — and it's always up to date.

**Asynchronous by design.** Agents don't need you present. Drop a task in Obsidian,
Syncthing propagates it, the runner picks it up, findings appear in your vault. Overnight
runs, weekend runs, runs while you're in the field. The swarm keeps scouting while you
review.

**AI is better with friends.** Multiple investigators, multiple compute nodes, zero shared
infrastructure. Async, air-gapped, no cloud accounts. See [Collaboration](#collaboration--ai-is-better-with-friends) below.

**Obsidian as the truth surface.** Markdown is the perfect middleground between
agent-readable and human-readable. A human opens a stub in Obsidian and reads it naturally.
An agent loads the same file as context. A script parses its frontmatter. No translation.
No "AI version" vs "human version" of your data. One vault, one source of truth, legible
to everyone.

**Data sovereignty (three layers).** **(1) Vault** — your **conceptual home** for collaboration: readable notes, inbox, queue, promoted narrative, dashboards. **(2) Investigation repo + COC** — **original forensic masters** (audit outputs, manifests, hashes) live here and are managed by your **chain-of-custody** system, not “instead of” the vault but as the **defensible originals**. **(3) Managed memory** — **optional**; if you use it, only **policy-approved slices** (often **HONEY-class** workflow material) should cross the wire; it **deepens** synthesis and continuity but does **not** replace the repo or vault custody story. Hosted models handle **per-request** inference. **Faerie-style** file-backed memory makes intelligence **crystallized** and **session-proof**; teams on the **same vault/repo conventions** can **swap investigation folders** and share expertise faster. See `00-META/00-OVERVIEW.md` (*Data sovereignty*) and `00-META/11-FAERIE-IMPACT-AB.md`.

**Self-evolving.** The memory-keeper reviews every session's friction and insights. Targeted
fixes get proposed to `improvement-proposals.md`. The swarm gets better at its own
workflows, session by session, driven by evidence.

**Evidence-grade provenance.** Chain of custody on every file operation. Hash signatures on
every sprint bundle. Information moves through explicit confidence tiers: raw agent
observation → `[UNVALIDATED]` → human-reviewed → `validated_by: human`. You always know
how trusted a piece of information is, who produced it, and when. Agents propose. You
approve.

---

## Collaboration — AI Is Better With Friends

### AI and humans aren't competing for the same cognitive territory

They're complementary — and once you design a system that respects that, something shifts.

AI is tireless, fast, and parallel. It can process 50 documents, cross-reference 200
entities, switch from financial analysis to infrastructure mapping to timeline
reconstruction in the same session, and do it all again tomorrow without losing its place
or its motivation. It doesn't get tunnel vision. It doesn't get emotionally invested in a
theory. It doesn't need sleep.

But it needs a compass. Without human steering, an AI agent will follow a hypothesis
confidently in the wrong direction. It will produce plausible-looking analysis that misses
what actually matters. It will optimize for the question it was asked, even when that's no
longer the right question. It is very good at going fast — but it needs humans to make
sure it's going somewhere.

Humans are the inverse. We have judgment, wisdom, domain expertise, and the pattern
recognition that comes from lived experience in a field. We know when a finding is
significant even before we can articulate why. We know when an investigation is off the
rails. We know what questions to ask next.

But we get tired. We get tunnel vision. We get lost in the data. We can only hold so many
threads simultaneously. Hours into a document review, the important things start blurring
into the noise.

**This system is designed around that complementarity.** The AI handles the volume —
extraction, structuring, cross-referencing, parallel execution, iteration without fatigue.
Your cognitive budget is freed up for the work only you can do: recognizing significance,
correcting course, deciding what matters. The `AGENT-REVIEW-INBOX`, `corrections.md`, and
human-approval gates aren't quality control overhead — they're the steering mechanism. You
don't rubber-stamp AI output; you actively redirect it, and every correction propagates
into every future run through the self-improving loop.

The result: you can operate at a strategic level across an investigation that would
normally require a team of people in the weeds. You zoom in to validate; you zoom back out
to steer. The AI stays in the sauce so you don't have to.

---

The single biggest accelerator for investigation work isn't a better model. It's a second
investigator with a different prior.

A friend with a different background notices different things. They question assumptions
you've stopped questioning. They seed tasks from angles you've stopped considering. Their
agents run in parallel with yours — four more investigation threads advancing overnight
while yours are already running. The swarm doesn't just scale computationally. It scales
epistemically.

Swarmy is designed for this from the ground up. The vault is the collaboration surface.
Syncthing is the transport. Nobody needs a shared account, a shared server, or even a
shared timezone.

### Anyone with Obsidian can participate

A collaborator doesn't need an Anthropic API key to contribute. They install Obsidian,
join the Syncthing mesh, and they immediately have access to:

- Every entity stub your agents have built, in real time
- Every intelligence report, financial trail, evidence item, and network map
- The full investigation graph in Obsidian's graph view
- The `REVIEW-INBOX` — they can review and approve agent findings just like you
- The task queue — they create tasks by dropping a `.task.md` in `00-Inbox/`

Their ideas drive the research. Your agents do the work. No API key required for them
to participate.

### Multiple compute nodes, automatic load balancing

If your collaborator runs Claude CLI, their machine becomes a second agent runner. Two
workstations polling the same vault. Task claiming is atomic — whichever picks up a task
first owns it. No coordination overhead. No double-processing. The swarm just gets bigger.

```
You seed 8 tasks overnight
  → Your workstation claims 5, runs them in parallel
  → Friend's workstation claims 3, runs them simultaneously
  → By morning: 8 completed findings, 8 signed sprint bundles
```

Three machines? Three runners. The throughput scales linearly with no central coordinator.

### Shared vault, separate trust namespaces

Human corrections and investigator preferences are scoped per person. Your friend's
`corrections.md` doesn't overwrite yours — agents load both and reconcile. You can hold
different working theories about the same target. The agents surface the tension between
them rather than flattening it into false consensus.

A finding that multiple agents — seeded by different investigators following different
threads — independently corroborate carries a different kind of confidence than one agent
following one chain of inference. The vault tracks provenance on everything. You can
always see whose hypothesis an agent was testing.

### The security model holds for collaboration

This is the part that matters for sensitive work. No collaborator ever has a direct
connection to your workstation. They have Syncthing access to the vault — that's it.

```
Your workstation           Friend's workstation
  outbound only      ←→     outbound only
       │                          │
       └────── Syncthing ─────────┘
                    │
              ZimaBoard hub  (vault sync relay)
```

If a collaborator's machine is compromised, the exposure is bounded to vault contents —
no API keys (never in the vault), no workstation access, no execution path into your
compute. Secrets never enter the shared surface. The vault is designed to be distributed;
everything sensitive stays local.

### Async means different timezones are a feature, not a bug

Your friend is asleep when you're working. You seed overnight tasks; they review findings
over breakfast. They push new leads before bed; your agents process them while you sleep.
The vault doesn't care what time it is.

Investigation work benefits from deliberate breaks — returning to a finding after sleep,
after a collaborator's cold read, after distance from the data. Async collaboration
enforces that rhythm rather than fighting it. The swarm keeps working; humans review when
they're sharp.

### What each person needs

```
┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
│            INVESTIGATOR             │  │            COLLABORATOR             │
│         (your home machine)         │  │          (any machine)              │
│       ── the compute engine ──      │  │      ── just a window in ──        │
├─────────────────────────────────────┤  ├─────────────────────────────────────┤
│                                     │  │                                     │
│  Claude CLI  or  local LLM (Ollama) │  │  ✗  No API key                     │
│  Anthropic API key                  │  │  ✗  No Claude CLI                   │
│  Obsidian + Syncthing               │  │  ✗  No compute at all               │
│  Canonical vault copy               │  │                                     │
│                                     │  │  ✓  Obsidian                        │
│                                     │  │  ✓  Syncthing                       │
│                                     │  │     (that's it)                     │
├─────────────────────────────────────┤  ├─────────────────────────────────────┤
│  Runs agents (overnight, async)     │  │  Reviews agent findings             │
│  Seeds tasks, steers investigation  │  │  Annotates dossiers                 │
│  Reviews + approves findings        │  │  Seeds new leads and tasks          │
│  Signs sprint bundles               │  │  Corrects agent errors              │
└─────────────────────────────────────┘  └─────────────────────────────────────┘
              │                                          │
              └──────────── Syncthing P2P ──────────────┘
                        (vault is the only shared surface)
```

No shared logins. No cloud accounts. The investigator's machine is the only machine
that ever touches an API. Everyone else just reads and writes markdown.

---

### Distributed Review — Collective Intelligence at Scale

Here's the problem every serious investigator hits: the research bottleneck isn't
research anymore. Agents can generate 50 entity dossiers overnight. The bottleneck is
*human judgment* — reading, validating, connecting, flagging. One person can't keep up.

But 50 people can.

Imagine: you run agents for a week on a complex investigation. You have hundreds of entity
stubs, dozens of financial trail fragments, a network map that's starting to cohere but has
gaps. You know what you need — domain experts to validate specific pieces. An accountant
to look at the corporate structures. A local journalist who knows the geography. Someone
who speaks the language of the documents. A researcher who's seen this network before in
a different context.

Each of those people needs to see *their slice* and annotate it. They don't need to
understand the whole investigation. They don't need technical skills. They open Obsidian,
they look at what needs review, they add what they know.

**The agent's job is to make human review effortless:**

- Every finding that needs eyes is pre-sorted into `AGENT-REVIEW-INBOX.md`
- Every stub that was updated by an agent is tagged `human-approved: false`
- Searching `human-approved: false` in Obsidian gives any collaborator an instant queue
- Reviewing = reading the stub, adding a note, checking the box. Done.

**The vault's job is to make contributions traceable:**

- Every annotation is timestamped and attributed
- Corrections feed directly into future agent context (`corrections.md`)
- The confidence tier of a finding upgrades when a domain expert validates it
- Multiple people independently corroborating the same finding = a different category of
  certainty than one agent following one thread

**What this actually looks like in practice:**

```
You (investigator):
  Run agents for a week → 80 entity stubs, 200 findings, 15 financial threads

Share vault access with 10 collaborators via Syncthing:
  → Accountant reviews 15-Financial/ stubs             (no compute needed)
  → Local journalist annotates 20-Entities/People/     (no compute needed)
  → Language specialist flags document translations     (no compute needed)
  → Fellow researcher adds connections to their work    (no compute needed)
  → Second investigator runs agents on new task seeds   (needs API key)

One week later:
  → 80 stubs now have domain expert annotations
  → 12 new connections identified by people who recognized names
  → 3 financial threads confirmed by the accountant as significant
  → 5 new task seeds from collaborator leads
  → Agents incorporate all corrections into the next sprint
```

This is crowdsourced OSINT done right — not "everyone do their own research and post it
somewhere," but "the AI does the structured extraction, humans provide the judgment that
AI cannot." The investigation scales with the expertise of the people you can reach, not
with the hours you personally have available.

The vault doesn't care how many people are annotating it. The quality controls are already
built in: layered confidence tiers, human-approval gates, corrections namespacing, chain
of custody on every change. You can hand out 50 dossiers to 50 people and know exactly
who said what, when, and with what confidence.

---

## System Design (Plain Language)

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU (Obsidian)                                                 │
│  Create tasks → review findings → approve changes → steer      │
└──────────────────────────┬──────────────────────────────────────┘
                           │  vault = shared bus (files on disk)
┌──────────────────────────▼──────────────────────────────────────┐
│  AGENTS (Claude CLI on workstation or ZimaBoard)                │
│  Poll inbox → claim task → research → write findings → sign     │
└─────────────────────────────────────────────────────────────────┘
```

**The vault is the only communication channel.** Agents never talk to each other directly.
They read from and write to the same Obsidian vault. You see everything in Obsidian.
Agents leave a full chain of custody log so every file creation is traceable.

### Three Physical Nodes (optional — works on a single machine too)

| Node | Role |
|---|---|
| **Your machine (Obsidian)** | Review, steer, QuickAdd task creation, human approval |
| **Workstation / WSL** | Runs Claude CLI agents, executes `scripts/2b_agent_runner.sh` |
| **ZimaBoard + OpenClaw (optional)** | Canonical vault, Syncthing hub, always-on orchestration |

You can run everything on a single machine. The ZimaBoard adds resilience and async operation.

---

## OpenClaw — The Hive's Nervous System

> OpenClaw is one of the most searched-for ZimaOS use cases right now. Here's exactly
> how it fits this system and what you can swap it for.

**OpenClaw** is ZimaOS's workflow automation layer — think n8n or Home Assistant but
built for ZimaBoard's Docker-native environment. In Swarmy, it does one job: **keep the
agent runner alive and trigger it on vault events.**

```
Syncthing detects new .task.md → OpenClaw triggers → agent_runner.sh wakes →
agent claims task → runs Claude → writes findings → vault syncs back to you
```

OpenClaw replaces the need for you to manually start an agent when a task arrives. It's
the mechanism that makes the system truly async — you drop a task into Obsidian on your
laptop, Syncthing pushes it to the ZimaBoard, OpenClaw fires the runner, and findings
appear in your vault while you're doing something else.

### What OpenClaw handles in this stack

| Function | How |
|---|---|
| Keep `agent_runner.sh` running as a daemon | Process monitor with auto-restart |
| Trigger agent run on new `.task.md` file | File watch webhook → shell action |
| Log agent runs and failures | OpenClaw workflow history |
| Alert on agent errors | Webhook to phone / Matrix / email |
| Schedule periodic runs (summarizer, kb_promote) | Cron-style trigger |

### Is OpenClaw swappable? Yes.

`agent_runner.sh` is a plain bash script with no OpenClaw dependency. OpenClaw's entire
role is process management and triggering. Every alternative below is a complete replacement:

| Alternative | Best for | Setup complexity |
|---|---|---|
| **`systemd` service** | Linux workstation / any Debian/Ubuntu machine | Low — one `.service` file |
| **`cron`** | Simple polling (runs every N minutes) | Minimal — one crontab line |
| **`pm2`** | Node.js shops, good dashboard | Low — `pm2 start agent_runner.sh` |
| **`supervisor`** | Python environments | Low — one `.conf` file |
| **Docker + restart policy** | Containerised setups | Medium — write a Dockerfile |
| **`launchd`** (macOS) | Mac-based setups | Low — one `.plist` file |
| **n8n** | If you already run n8n; richer webhook logic | Medium |

For most users without a ZimaBoard: **systemd is the right answer.** One file, battle-tested,
logs via `journalctl`, restarts on crash. See setup below.

---

## Deployment Options — Pick Your Use Case

**Core clarification before you choose:**
The agents always run on a local machine with Claude CLI installed. The ZimaBoard (or any
always-on node) is a Syncthing hub — it holds a vault copy and keeps all devices in sync,
but it never runs Claude itself. The poll script runs locally, reads the local vault copy,
and writes findings locally. Syncthing propagates everything.

---

### Use Case 1 — Solo researcher, trying it out

One machine. No sync infrastructure needed.

```
Your machine:  Obsidian + agent_runner.sh (WSL/Linux) + Claude CLI
Vault:         local folder
Sync:          none
Orchestration: run agent_runner.sh manually or via systemd/cron
```

**Setup:** Quickstart above. Five minutes. Stop here until it works.

---

### Use Case 2 — Solo researcher, async overnight runs

You want agents running while you sleep. Two options depending on what you have:

**2a — Laptop + always-on workstation**
```
Laptop:        Obsidian (your review interface)
Workstation:   agent_runner.sh as systemd daemon + Syncthing client
Vault sync:    Syncthing (LAN — instant, no cloud)
Flow:          create task on laptop → Syncthing pushes to workstation →
               agent_runner.sh polls and picks it up → findings sync back
```

**2b — Single machine + Git for backup**
```
One machine:   Obsidian + agent_runner.sh + Claude CLI
Vault sync:    git push/pull (manual or cron)
Trade-off:     git adds commit friction; fine for daily-cadence work
```

---

### Use Case 3 — Air-gapped async collab (remote ZimaBoard + local workstation)

*This is the reference architecture for sensitive investigation work.*

Your workstation does all the compute. The ZimaBoard is a stateless sync hub — it runs
Syncthing and nothing else that matters. A collaborator's machine joins the Syncthing mesh
and gets a live vault copy in Obsidian. The workstation never accepts incoming connections.

```
Workstation (you + collaborator):
  - Obsidian (review, task creation, steering)
  - agent_runner.sh polling LOCAL vault copy
  - Claude CLI making outbound HTTPS to Anthropic only
  - Outbound SSH to ZimaBoard for management (never accepts incoming)
  - Syncthing client (syncs vault to/from ZimaBoard)

ZimaBoard (remote, always-on):
  - Syncthing hub — canonical vault copy, propagates to all devices
  - No Claude, no agent runner, no incoming connections from internet
  - OpenClaw optional: notifications/monitoring only, not agent execution

Collaborator machine:
  - Syncthing client (joins same mesh via ZimaBoard as introducer)
  - Obsidian (reads findings, creates tasks, reviews)
  - No API key required — they don't run agents
```

**Network rules:**
- Workstation: outbound only — Syncthing, HTTPS to Anthropic, SSH to ZimaBoard
- ZimaBoard: Syncthing port open on LAN/VPN only; no public internet exposure
- Collaborator: Syncthing only; can be on a separate network reaching ZimaBoard via VPN

**The flow:**
```
You create task in Obsidian
  → Syncthing pushes .task.md to ZimaBoard
  → ZimaBoard propagates to all Syncthing peers
  → agent_runner.sh on workstation polls local vault copy, finds task
  → Agent claims task (atomic rename), runs Claude, writes findings
  → Syncthing pushes findings from workstation → ZimaBoard → collaborator
  → Collaborator sees findings in Obsidian without touching the workstation
```

**Agent configs in the vault:**
Agent definitions (skills, personas, configurations) have canonical copies on your local
machine (`~/.claude/agents/`). The vault holds reference copies in `02-Skills/` and
`03-Agents/` — these sync to all nodes so collaborators can see what agents are available
and what they're designed to do. The agents periodically write updates back to the vault
copies. Canonical always wins; vault copy is for visibility and sync.

#### ZimaBoard + Syncthing Setup (15 minutes)

**1. Install Syncthing on ZimaBoard**
```bash
# ZimaOS app store → Syncthing, or Docker:
docker run -d --name syncthing \
  -v /DATA/CyberOps:/var/syncthing/CyberOps \
  -p 8384:8384 -p 22000:22000/tcp -p 22000:22000/udp \
  --restart unless-stopped \
  syncthing/syncthing
```
Open `http://zimaboard-ip:8384` → Actions → Show ID (save this device ID).

**2. Install Syncthing on workstation and collaborator machines**
```bash
# Ubuntu/Debian:
sudo apt install syncthing
systemctl --user enable syncthing && systemctl --user start syncthing
# Open http://localhost:8384
```

**3. Connect devices**
On each machine: Remote Devices → Add Device → paste ZimaBoard's device ID.
On ZimaBoard: accept connection requests from each machine.
Set ZimaBoard as "Introducer" — it will automatically introduce devices to each other.

**4. Share the vault folder**
On ZimaBoard: Add Folder → path `/DATA/CyberOps` → share with all connected devices.
On each machine: accept the folder share → set local path → let it sync.

**5. Set workstation SSH to ZimaBoard (outbound only)**
```bash
# Workstation ~/.ssh/config:
Host zimaboard
    HostName 192.168.x.x    # or your ZimaBoard's IP/hostname
    User zimaos
    IdentityFile ~/.ssh/your-key
    ServerAliveInterval 60

# Connect for management:
ssh zimaboard
# Never run sshd on workstation (no incoming connections)
```

**6. Start agent runner on workstation**
```bash
# systemd (recommended — survives reboots, logs via journalctl):
sudo tee /etc/systemd/system/swarmy-agent.service <<EOF
[Unit]
Description=Swarmy Agent Runner
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/path/to/CyberOps
ExecStart=/bin/bash /path/to/CyberOps/scripts/2b_agent_runner.sh
Restart=on-failure
RestartSec=10
Environment=ANTHROPIC_API_KEY=your-key-here
Environment=CYBEROPS_VAULT=/path/to/CyberOps

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now swarmy-agent
journalctl -u swarmy-agent -f   # watch logs
```

**7. Test the full loop**
Create a task in Obsidian → Syncthing pushes it (watch the Syncthing UI) →
`journalctl` shows agent picking it up → findings appear in collaborator's Obsidian.

---

### Use Case 4 — Small team, multiple investigators

Multiple people creating tasks and reviewing findings. Each person has Obsidian + Syncthing.
One machine runs the agents (or each investigator's machine can run agents independently —
tasks are claimed atomically so no two agents double-process the same task).

```
Each investigator:  Obsidian + Syncthing client
Agent machine(s):   agent_runner.sh + Claude CLI + Syncthing client
Hub:                ZimaBoard or any always-on Linux machine running Syncthing
Coordination:       entirely through vault files — no shared accounts, no Slack needed
```

**Scaling:** run multiple agent_runner.sh instances on different machines. They compete
for tasks via atomic file claiming — whichever picks it up first owns it. No coordinator
needed. The swarm scales horizontally.

---

### Use Case 5 — Fully air-gapped (no outbound internet from agent machine)

Replace Claude API with a local model. The agent runner and context builder work the same;
only the model changes.

```bash
# Install Ollama on workstation:
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3  # or mistral, qwen, etc.

# Set in 2b_agent_runner.sh:
MODEL="ollama/llama3"
CLAUDE_CLI_FLAGS="--model ollama/llama3 --api-url http://localhost:11434"
```

Trade-off: local models are significantly less capable than Claude for complex OSINT
reasoning. Use for: testing the pipeline, sensitive work that cannot touch any external
API, or as a triage layer before escalating to Claude.

---

### OpenClaw — Where It Fits

OpenClaw is not required by any of the above setups. It becomes useful in Use Cases 3 and
4 for **monitoring and notifications** — alerting you when an agent completes, fails, or
hits an error — without needing to watch `journalctl` on the workstation.

```
OpenClaw workflow (ZimaBoard, optional):
  Trigger:  HTTP webhook from agent_runner.sh on task completion
  Action:   Push notification to phone / Matrix / email
  No agent execution on ZimaBoard — it only receives status, never runs Claude
```

To wire this: add a `curl` call at the end of `2b_agent_runner.sh`'s task completion
block pointing to your OpenClaw webhook URL. The workstation calls out; ZimaBoard listens
on LAN only.

---

### Remaining Setup Checklist

Before the system is fully operational:

- [ ] `ANTHROPIC_API_KEY` set in environment (required — agents need this)
- [ ] `CYBEROPS_VAULT` path set in `2b_agent_runner.sh` line ~10
- [ ] Claude CLI installed (`npm install -g @anthropic-ai/claude-cli` or via WSL)
- [ ] Obsidian: QuickAdd package imported, Blueprint plugin active, Dataview installed
- [ ] Obsidian: settings from `00-META/05-OBSIDIAN-SETTINGS.md` applied
- [ ] Agent runner started (systemd / OpenClaw / manual `bash scripts/2b_agent_runner.sh`)
- [ ] *Optional:* GPG key configured for hash signing (`OPENPGP_KEY_ID`)
- [ ] *Optional:* Syncthing installed on all devices and vault folder shared
- [ ] *Optional:* ZimaBoard with OpenClaw workflow wired to file watch trigger
- [ ] *Optional:* `3b_summarizer_agent.py` on weekly cron for KB compression

---

## Folder Structure

```
00-09   SYSTEM        meta, memory, agent config, skills
0a-0z   FEED          raw tool output (SpiderFoot, Shodan, etc.) — flows into stubs or products
10-29   STUB ZONE     living notes updated over time (entities, networks, case files)
30-79   PRODUCT ZONE  finished artifacts, immutable once final (evidence, reports, financials)
99      ARCHIVE       completed tasks
```

### The Three Content Zones

**Stub zone** — bite-sized, information-dense, updated over time. These are designed to
fit in an AI's context window without burning tokens. An entity stub for a person is
~400 words max: who they are, key connections, links to evidence. Agents can append freely.
Condensing or deleting requires your approval.

**Feed zone** — raw tool output. SpiderFoot runs, Shodan exports, OSINT tool dumps. These
are lead generators: the agent extracts what's useful, creates stubs or evidence files,
and links back. Not immutable, but original output is never rewritten.

**Product zone** — complete finished work. Intelligence reports, evidence files, financial
trails. Created once, never edited after `status: final`. Every product includes methodology,
sources, reproducibility notes, and the session that created it.

---

## The Champagne Pyramid (Context Loading)

The hardest problem in multi-agent AI is context bloat — agents loading too much irrelevant
history and running out of space for actual work. This vault solves it with tiered context
loading, like champagne filling a pyramid of glasses from top to bottom:

```
T1  (~1K tokens)   Mission steering — what's the current focus, standing orders
T2  (~3K tokens)   Knowledge base — only entries matching this task's keywords
T2.5 (~3K tokens)  Prior sprint bundle — if this task continues previous work
T3  (~5K tokens)   Entity stubs named in the task — the people/orgs/IPs involved
T4  (~2K tokens)   Handoff notes — what the last agent left for the next one
T5  (≤20K tokens)  The task file itself
```

Each tier fills from a shared 80K token budget. If T2 is full, T3 gets less. The task
always fits. The agent always has mission context. Irrelevant history never loads.

The context builder (`scripts/2a_context_builder.py`) assembles this automatically before
each agent run. You don't configure it — it reads your vault structure.

---

## Hash Signing & Chain of Custody

Every agent action is logged. Every file the agent creates gets hash-signed at session end.

- **Chain of custody log** (`03-Agents/agent-logs/coc-{session}.md`) — every file operation:
  read, create, modify, delete, spawn. Timestamped. Attributed to session and agent.
- **Hash snapshots** (`03-Agents/hash-snapshots/`) — SHA-256 + HMAC of every file in
  every directory where new files were created. Optional GPG signing.
- **Sprint bundles** (`.claude/sprints/`) — immutable snapshot of the full session:
  chain of custody, agent flow diagram, memory, outputs, git state. Never modified.

This means you can audit exactly what an agent did, verify no files were tampered with,
and reproduce any result from scratch.

---

## Quickstart

### 1. Clone and open in Obsidian

```bash
git clone https://github.com/goodoleusa/swarmy CyberOps
```

Open the `CyberOps/` folder as a vault in Obsidian. See `00-META/05-OBSIDIAN-SETTINGS.md` for full settings.

## Required Plugins (install after cloning)

After cloning and opening the vault in Obsidian, install these community plugins:
Settings → Community Plugins → Browse → search each name → Install → Enable

| Plugin | Why |
|--------|-----|
| Dataview | Powers all dashboards and dynamic TOC tables |
| QuickAdd | Fast note capture and templating |
| obsidian-homepage | Opens HOME.md on startup instead of last file |
| Obsidian Git | Auto-commit vault changes |
| Excalidraw | Visual diagrams (pseudosystem, architecture) |
| ExcaliBrain | Interactive graph from parent/child/sibling frontmatter |
| Templater | Advanced templating for blueprints |
| Blueprints | Template system for structured notes |
| Copilot | AI chat (optional — needs API key) |

**Critical step after enabling Dataview:**
Settings → Dataview → enable "Enable JavaScript Queries"
Without this, all dashboard blocks show blank (no error shown).

### 2. Import QuickAdd package

Settings → QuickAdd → Packages → Import → select `CyberOps-QuickAdd.quickadd.json`

This gives you keyboard shortcuts to create tasks, entity stubs, evidence records, etc.

### 3. Configure the agent runner

Edit `scripts/2b_agent_runner.sh` — set your vault path:

```bash
VAULT="/path/to/your/CyberOps"   # line ~10
```

Set your Claude API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Optionally set up GPG signing for hash snapshots:
```bash
export OPENPGP_KEY_ID="your-gpg-key-id"
```

### 4. Run vault setup

```bash
bash scripts/1b_setup_cyberops_vault.sh
```

This creates any missing folders and confirms QuickAdd is importable.

### 5. Start the agent runner

```bash
bash scripts/2b_agent_runner.sh
```

It polls `00-Inbox/` every 30 seconds for `.task.md` files. When it finds one, it
assembles context, runs a Claude agent, and writes results to the appropriate folder.

### 6. Create your first task

In Obsidian: Command Palette → QuickAdd → Create Task
Or drop a file into `00-Inbox/` named `YYYY-MM-DD-your-task.task.md`:

```yaml
---
type: task
status: pending
priority: MED
created: 2026-01-01
---
## Objective
Research the public financial connections of [target organization].

## Output expected
Entity stubs for key people in 20-Entities/People/
Financial trail in 50-Financial/
Summary report in 40-Intelligence/
```

The agent picks it up, does the work, and moves the task to `99-Archives/` when done.
Check `00-Inbox/AGENT-REVIEW-INBOX.md` for items flagged for your attention.

---

## Daily Use

**Morning:** Check `00-Inbox/AGENT-REVIEW-INBOX.md` for overnight agent findings.
Review anything marked `- [ ]` (unchecked = needs your eyes). Mark done with `- [x]`.

**Adding a lead:** QuickAdd → Create Entity Stub or Create Task. The stub gets routed
to the right folder automatically. The task gets queued for the agent.

**Steering agents:** Edit `01-Memories/agents/AGENT-CONTEXT.md` → Current Focus section.
Every agent reads this before starting. Change it and all future agents align immediately.

**Approving stub updates:** If an agent condensed or restructured a stub, it sets
`human-approved: false` in frontmatter. Search for `human-approved: false` in Obsidian
to find everything pending your review. Change to `true` when satisfied.

**Reviewing the graph:** Graph view → filter out `scripts/`, `Templates/`, `99-Archives/`.
What remains is your investigation network. Nodes with more links = more connected entities.

---

## Scripts Reference

| Script | When to run | What it does |
|---|---|---|
| `1a_ensure_vault_folders.sh` | Once on setup or after vault move | Creates any missing folders |
| `1b_setup_cyberops_vault.sh` | Once on setup | Folder check + QuickAdd import instructions |
| `2a_context_builder.py` | Called by agent runner | Assembles champagne pyramid context |
| `2b_agent_runner.sh` | Keep running as daemon | Polls inbox, runs agents, signs outputs |
| `2c_vault_sign.py` | Called by agent runner | Signs output directories via hash_tracker |
| `2d_hash_tracker.py` | Called by vault_sign | Computes SHA-256 + HMAC snapshots |
| `3a_kb_promote.py` | After reviewing inbox | Promotes checked items to knowledge base |
| `3b_summarizer_agent.py` | Weekly (cron on ZimaBoard) | Compresses old KB/logbook entries to archives |
| `4a_vault_status.py` | Any time | Prints vault state summary (active agents, inbox count) |
| `5a_process_spiderfoot_run.py` | After a SpiderFoot scan | Parses raw SpiderFoot JSON into vault entries |

---

## Design Principles

These aren't style preferences — they're load-bearing. Each one solves a specific failure
mode in long-running multi-agent systems.

---

**Zero waste. Every output is the next run's input.**
Agent findings become entity stubs. Stubs become context for the next agent. Sprint bundles
feed the T2.5 context tier for the next sprint. Handoff notes seed the next session. Nothing
leaves the system as waste. This is a closed-loop intelligence system — modelled on
permaculture, where the output of every process becomes input for another. If an insight
is discovered and not captured, it's gone. The system is designed so that's structurally
impossible.

---

**Stateless agents. Stateful vault.**
Agents carry no memory between runs. They boot, read the vault, do work, write the vault,
exit. All state lives in the vault — the shared medium. This means any agent can pick up
any task from scratch. Agents can be killed, restarted, swapped for a newer model, or
replaced by a human without any special migration. The swarm survives turnover because
knowledge lives in the hive, not in any individual bee.

---

**Vault as bus, not database.**
No central API, no message queue, no database, no coordinator process. The shared
filesystem IS the coordination mechanism. Agents discover available tasks by reading a
folder. They claim work by an atomic file rename. They communicate findings by writing
markdown. A human reviews by opening Obsidian. The entire system works offline, survives
any single component failing, and is trivially inspectable — you can audit the full state
of any agent interaction with a text editor.

---

**Async-native. Air-gapped collaboration.**
No part of this system requires synchronous coordination. Agents run when they run. You
review when you review. Remote collaborators pull vault changes via Syncthing — no git
ceremony, no cloud login. A ZimaBoard on a remote network can run agents overnight and
sync findings to your laptop by morning. Two investigators on different continents can
share a vault over Syncthing with no shared infrastructure beyond the P2P connection.
The system is designed for the realistic conditions of investigation work: intermittent
connectivity, different time zones, air-gapped environments.

---

**Stubs stay small. Density over completeness.**
Entity stubs are capped at ~400 words. This is counterintuitive — most knowledge systems
try to capture everything. This one deliberately compresses. A stub is not a dossier. It
is the concentrated essence: who this person is, why they matter, what connects them, where
the evidence lives. Small stubs load fast into agent context, stay readable in Obsidian,
and force the discipline of knowing what's actually important. The full evidence is in the
product zone, linked from the stub.

---

**Layered trust. Confidence as a first-class concept.**
Information moves through explicit confidence levels: raw agent observation → `[UNVALIDATED]`
→ flagged in REVIEW-INBOX → human-reviewed (`- [x]`) → promoted to KNOWLEDGE-BASE with
`validated_by: human`. You always know how trusted a piece of information is, who touched
it, and when. Agents are not permitted to self-promote their findings. The knowledge base
only contains things a human has looked at. This is the epistemological equivalent of
evidence law — chain of custody, not just chain of thought.

---

**Human sovereign, not human bottleneck.**
You are the queen bee — high-level, strategic, final authority. You don't do the scouting.
You don't write the stubs. You read the dances and decide which ones to follow. The system
is designed to make your review efficient: findings are pre-sorted by priority, stubs flag
when they need approval, and nothing becomes permanent without your `- [x]`. But the agents
never wait on you to proceed with new tasks. The swarm keeps scouting while you review.

---

**Immutability for forensics. The past cannot be altered.**
Evidence files and finished reports are write-once. Sprint bundles are hash-signed and
sealed. If something changes — new information, a correction — you add a new dated entry
below the original. You never overwrite. This means every finding can be traced to the
session, agent, and source that produced it. Long after the investigation concludes, you
can reconstruct exactly what was known, when, and why it was believed.

---

**Self-improving loop. The swarm teaches itself.**
At the end of every session, the memory-keeper reviews which skills and agents generated
friction (PAIN entries in scratchpads) and which produced novel insights (IDEA entries).
For each friction point referencing a specific skill or agent, it proposes a targeted fix
and writes it to `improvement-proposals.md`. You review and apply the ones you like. The
system gets better at its own workflows over time, driven by evidence from actual runs —
not by the designer's assumptions about what would go wrong.

---

**Self-contained. Clone and go.**
Every script, template, blueprint, and config needed to run the full pipeline lives in this
vault. Pull it to a new machine, set your API key, run setup. No external service
dependencies beyond Claude CLI and Python 3. The vault can be moved, zipped, archived, or
handed to a collaborator — and it will work. This is not accidental: it reflects a design
philosophy that operational knowledge should travel with the tools that use it.

---

## Further Reading

- `00-META/AGENT-SYSTEM-ARCHITECTURE.md` — full technical architecture including ZimaBoard
  setup, network topology, OpenClaw integration, secrets management
- `00-META/05-OBSIDIAN-SETTINGS.md` — recommended Obsidian settings for this vault
- `00-META/FRONTMATTER-WIKILINKS.md` — `parent` / `sibling` / `child` frontmatter with quoted `[[wikilinks]]`
- `01-Memories/agents/AGENT-CONTEXT.md` — current mission steering + agent rules
- `00-META/02-QUICKADD-SETUP.md` — QuickAdd macro reference
- `00-META/11-FAERIE-IMPACT-AB.md` — Honest A/B framing: native session vs faerie (HONEY, NECTAR, queue, inbox); demo protocol
- `00-META/KICKSTART-COLLAB.md` — Where to put tasks/briefs under `00-SHARED/`; folder naming (no new numeric prefixes except protected/private/tooling)
- `00-SHARED/HOW-SYNC-WORKS.md` — sync + env vars; **`*.sha256` files** = one-line hash proving the starting doc the agent delivered
- `00-SHARED/00-SHARED.md` — shared zone vs protected folders
- CyberTemplate repo: `launch/VAULT-OBSIDIAN-COC-SYNC.md` — short bridge from the repo side
