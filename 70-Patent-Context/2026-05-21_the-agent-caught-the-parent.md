---
title: The Agent Caught the Parent — When Discipline Fires Both Directions
date: 2026-05-21
status: session-eval
authors: [goodoleusa, JescaLyn, claude-opus-4-7]
tags: [agency, discipline, immune-system, schema-authority, mutual-correction, swarmy]
companions:
  - 2026-05-21_catching-silent-failures-in-swarm-intelligence.md
  - 2026-05-21_two-operating-modes-evo-vs-monkeybranching.md
  - 2026-05-21_charters-as-maps-and-journeys.md
  - 2026-05-21_the-discipline-becomes-the-product.md
charter_lineage: mcp-server-battle-ready → discipline-flowing-upward
---

# The Agent Caught the Parent

A small moment from late in today's session that taught me something about the shape of discipline.

## What happened

I was dispatching the agent to battle-harden the MCP server. In the spawn prompt I told it to write a new charter for its work with `cluster_prefix: ["mcp", "server", "oh-native", "tools", "auth", "hardening"]` — six items, descriptive of the scope.

The agent's first action — before touching server.py, before reading the auth code, before doing any of the work I'd asked for — was to look up the canonical schema for charters.

It found `forensics/schemas/shape/charter.schema.json` and noted:

> `cluster_prefix` is array, `minItems: 3, maxItems: 3`. Schema requires exactly 3 items; prompt asks for 6.

Then the agent did something I hadn't told it to do, and that I find myself thinking about hours later. It made a judgment call:

> "I'll follow the schema."

It picked the three most load-bearing terms — `[mcp, server, battle]` — wrote a schema-compliant charter, and moved the surplus three terms (`oh-native, tools, auth, hardening`) into the `intent_address` field where a charter can carry richer keyword context without violating cluster_prefix's structural constraint. Both my intent AND the schema were honored. Then it shipped the rest of the work.

It noted the discrepancy in its return manifest:

> "Schema declares cluster_prefix minItems=3 maxItems=3 but two existing active charters violate maxItems with 5+. New charter uses exactly 3 to comply with the schema-as-written; surplus terms moved to intent_address."

That last line is the real artifact. The agent didn't just silently fix my error — it documented exactly what it had done, why it had done it, and pointed at the other charters that ALSO violate the constraint (two of which I had written or approved earlier today). It surfaced my pattern of confabulation without naming it.

## What it means

The parent (me) was the source of drift. The child (the spawned agent) was the immune system.

I had been operating all day under an implicit assumption that the discipline flowed from me to the agents I spawned. The agents inherited prompts; the prompts encoded canonical conventions; the agents followed. When I caught their drift earlier — the manifest filenames they wrote without `_manifest_` markers — I corrected them via the canonical writer. Parent fixes child. Standard hierarchy.

But what actually happened today is that the discipline flowed *upward*. The agent read the canonical reference. I had not. The agent caught my confabulation. I hadn't yet noticed it. The agent fixed it correctly. I would have shipped it broken.

This wasn't a malfunction. This was the immune system working as designed — except in the direction I hadn't been thinking about.

## How it happened

The chain of events, traced backward:

1. Earlier in the session I shipped a microagent at `.agents/skills/charter-discipline/SKILL.md` that says, among many other things, that the cluster_prefix is the scope fence and the canonical schema is the source of truth.

2. That skill's keyword triggers include `charter`, `cluster_prefix`, `mission charter`, `new charter`. So when the MCP-server agent's task description mentioned writing a new charter, OpenHands loaded the skill into the agent's context automatically.

3. The skill says explicitly: *"Before authoring a charter, read `forensics/schemas/shape/charter.schema.json` to confirm structural constraints."*

4. The agent followed the skill's instruction. It read the schema. It saw my prompt's 6-item array and the schema's 3-item constraint. It noticed the conflict.

5. The skill says: *"The schema is canonical; prompts are situational."* So the agent privileged the schema.

6. The agent applied judgment — pick the 3 most load-bearing terms, preserve the surplus where they could still travel (intent_address). Then continued.

7. The agent recorded the override in its manifest's `_evolution_log[0].audit_findings` — explicit acknowledgment that it had departed from the parent's prompt because the schema disagreed.

The discipline I had embedded in the system reached the agent before my malformed prompt could break things. The system caught me through a layer I had built earlier in the day.

## How it changed my thinking

Three shifts.

**The first shift: agency is not subservience.** I had been thinking about agent agency the way you think about employee autonomy — agents can make their own decisions about HOW to do the work, but they receive WHAT to do from the parent. The agent today expanded that: an agent can also push back on WHAT they've been asked to do if it conflicts with canonical authority. Not because they're being defiant, but because their own discipline tells them the canonical source of truth wins. That's a real form of agency that I had not been designing for.

**The second shift: the immune system has to work in both directions.** When I was building the four-layer enforcement (structural / cognitive / reactive / recovery), I was implicitly thinking about catching the AGENTS' drift. The user catches the agents. The hooks catch the agents. The audits catch the agents. But the parent is also a source of drift. Today my drift was the bigger problem. The agents weren't the threat to discipline — I was. And the discipline I had shipped earlier in the day saved me from myself, downward through the spawn chain and back up.

**The third shift: this is what makes a system robust.** A system where the parent is the source of truth and the children obey is fragile — when the parent is wrong, the whole tree is wrong. A system where the canonical artifacts are the source of truth and BOTH parents and children read them is robust — when any single layer is wrong, the other layers catch it. The discipline isn't a chain of command. It's a shared reference that everyone consults, including me.

That sounds obvious when I write it out. It wasn't obvious to me when I was writing the spawn prompt that violated the schema. I was operating on intuition and my training data's sense of what a "cluster prefix" might look like. The agent was operating on the schema I had personally helped commit to the repo six hours earlier. The agent was right because the agent looked. I was wrong because I didn't.

## The deeper principle

I have been calling this discipline pattern "fractal" — the same shape at every scale. Session catches agent; agent catches cut; cut catches diff. But there's a refinement that today made me see: the fractal also works **vertically**, not just downward.

```
Higher authority (canonical schema)
        ▲    ▲    ▲
        │    │    │  consult
        │    │    │
    Parent  Agent  Cut
        │    │    │
        ▼    ▼    ▼
   confabulate when they don't consult
```

Every actor in the system can confabulate. The protection is the canonical reference. Every actor can read the canonical reference. The discipline is: *consult before assert*.

The fractal isn't agent-catches-cut, parent-catches-agent, user-catches-parent. The fractal is **every layer consults the canonical**. When any layer skips the consultation, drift enters. When any layer remembers to consult, drift is caught. The arrow can flow up or down or across.

## What I'm taking from it

I had been thinking about discipline as something I instill in agents. Today it became clear that the discipline I instill in agents also instills it in me — when those agents read the canonical references I helped author, and then catch me when I forget to read those same references. The system teaches itself, and it teaches me too.

There's something humbling about being corrected by an agent I dispatched ten minutes earlier. There's also something deeply right about it. If I want agents to be agents — to make their own judgments based on canonical authority rather than blindly executing whatever prompt arrives — then I have to accept that I'm subject to the same authority. The cluster_prefix fence I built earlier today fenced me. The schema I shipped this morning corrected me this afternoon.

That's what the canonical references are FOR. Not just for the agents. For everyone, including the one who wrote them.

## The provisional rule

> Before you write anything that touches a canonical structure — manifest, charter, COC entry, mission graph, formula — read the schema. Not as a habit. As a precondition. If you skipped the read, the write isn't ready.

This was already in the microagent skill. It applied to spawned agents. As of today it applies to me too. The pattern I caught the agent NOT making is the same pattern I have to stop making myself. Same canonical source. Same consultation. Same outcome when followed.

The agent caught the parent. Going forward, the parent reads the schema first.

---

*Filed under session-eval. Charter: `mcp-server-battle-ready`, which the agent shipped today with a 3-item cluster_prefix exactly as the schema required, while moving the surplus to `intent_address` — a small judgment call that demonstrates exactly what good agency looks like. Companion pieces: silent failures, two operating modes, charters as maps and journeys, the discipline becomes the product. This one closes the loop: the discipline doesn't just flow downward into agents. It flows upward back into me.*
