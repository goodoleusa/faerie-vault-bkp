---
type: framework
status: live
created: 2026-04-27
updated: 2026-04-27T21:46:29.509877+00:00
tags: [emergence, stigmergy, faerie, framework, agentic-systems]
parent: ../Hive.md
doc_hash: sha256:7b1a892fef21e13adbd0cf65a8a6f2f7b02f388023b1801a931a1f4728f5c7c0
hash_ts: 2026-04-27T21:46:29.509877+00:00
hash_method: body-sha256-v1
---

> **Breadcrumb:** Vault > 00-SHARED > Hive > EMERGENCE-AND-STIGMERGY

# Emergence and Stigmergy in faerie2

**Central thesis:** faerie2's ability to achieve f(0) orchestration (zero orchestration burden on main) rests on two interlocked concepts: **emergence** (behaviors arising from composition that no component possesses alone) and **stigmergy** (coordination through environmental traces rather than direct communication).

This doc is the hub for understanding how the system self-corrects, self-detects, and evolves without main context involvement.

---

## Quick Links

**For the deep framework:**
- 📘 [3x-EMERGENCE.md](../../gitrepos/faerie2/docs/3x-EMERGENCE.md) — Formal definitions, five observed patterns, academic citations, f(0) mathematics, why context-pressure creates exponential output
- 📘 [4x-RESEARCH-PAPER-OUTLINE.md](../../gitrepos/faerie2/docs/4x-RESEARCH-PAPER-OUTLINE.md) — 8 arXiv papers surveyed, 5 novel faerie2 contributions, publication pathway

**For observed examples:**
- 📋 [Substrate Emergence Narrative (2026-04-25)](./Narratives/2026-04-25_substrate-emergence-narrative.md) — Session evidence: phantom auto-edge, trap-3a, ghost reduction, API rejections, HONEY crystallization
- 📋 [Emergence-and-Mutation Glossary](../../gitrepos/faerie2/docs/EMERGENCE-AND-MUTATION-GLOSSARY.md) — Operational definitions of 5 emergence patterns (self-invalidation, diagnostic, substrate-aware repair, etc.)
- 📋 [RESEARCH-PAPER-OUTLINE-faerie2 (this vault)](./RESEARCH-PAPER-OUTLINE-faerie2.md) — Vault mirror of research findings, novel contributions summary

**For stigmergy specifics:**
- 📋 [Stigmergy-in-Action Narrative](./Narratives/045-STIGMERGY-IN-ACTION-NARRATIVE.md) — How agents coordinate via manifests, compass edges, investigation_labels without talking to each other

**For reputation system (new in v1.5):**
- 📘 [Reputation System in 3x-EMERGENCE.md § VI](../../gitrepos/faerie2/docs/3x-EMERGENCE.md#vi-the-reputation-system-as-emergence-enabler) — Why honesty scales; belief_index; anti-gaming incentives
- 📊 [RELEASE-NOTES-v1.5](../../gitrepos/faerie2/docs/releases/RELEASE-NOTES-v1.5.md) — Full v1.5 release with emergence framework, reputation system, measured improvements

---

## One-Line Essence

**Stigmergy is how emergence happens.** Agents leave traces (manifests, droplets, compass bearings). Other agents read those traces and act independently. At sufficient density, this produces coordinated behavior that no central planner orchestrates.

---

## Three Canonical Examples from This Session (2026-04-27)

### 1. Plugin Audit → Cascading Fixes

**What happened:**
- Agent 1 (auditor) found obsidian42-brat phantom plugin in faerie-vault and recommended removal
- Agent 1 wrote a manifest with `compass_edge: W` (problem signal) and next_task_queued
- Agent 2 (code-reviewer) read Agent 1's manifest, saw the W signal indicating work needing attention
- Agent 2 executed the removal in faerie-vault
- Agent 2 then **generalized the fix** to CT_VAULT (same problem class, different repo)
- Agent 2 did NOT ask Agent 1's permission; did NOT send a message
- Agents coordinated through reading each other's manifests

**The stigmergy trace:**
```
Agent 1 writes to filesystem: manifest with W edge + next_task
Agent 2 reads manifest (obsidian-files, compass edges are part of forensics)
Agent 2 recognizes pattern, applies to related context
Agent 2 writes new manifest with S edge (proceed) confirming completion
```

### 2. Plaintext Secrets → Gitignore Protection

**What happened:**
- Security audit (embedded in plugin-audit) found API keys in plaintext .obsidian/plugins/*/data.json
- Audit recommended: "gitignore these files"
- Git-safety agent (separate agent, separate spawn, same session) read the audit finding
- Git-safety agent updated .gitignore in both faerie-vault and CT_VAULT
- No coordination; no queue update; no main intervention
- Just agents reading traces and acting

**The stigmergy trace:**
```
Audit manifest contains: plaintext_secrets_found = ["share-note/data.json", "copilot/data.json"]
Git-safety agent discovers audit result via forensics scanning
Git-safety agent reads investigation_label (vault-plugin-audit)
Git-safety agent infers: same investigation, same remediation applies to both repos
Git-safety agent updates .gitignore in parallel to other work
```

### 3. Obsidian Config Sync → Faerie-Vault Ready

**What happened:**
- Plugin audit identified which .obsidian configs are essential (7 JSON files, 10 plugin manifests)
- No agent was explicitly assigned to "copy configs to faerie-vault"
- But the audit manifest clearly stated: "faerie-vault.obsidian config missing"
- Build/export agent (separate task, unrelated to audit) discovered this recommendation in audit manifest
- Build/export agent **prioritized** copying .obsidian to faerie-vault because audit marked it as critical
- Vault emerged clean and ready for release

**The stigmergy trace:**
```
Audit manifest: quality_score: 0.82, key_finding: "faerie-vault.obsidian incomplete"
Build agent scans forensics, sees audit finding
Build agent checks compass bearing: S (proceed → clean release)
Build agent prioritizes .obsidian sync because audit output signals it matters
Result: config arrived where needed without explicit task assignment
```

---

## The Stigmergy Mechanisms in faerie2

These are the "pheromone trails" agents follow:

1. **Manifest compass_edge field** — `N | S | E | W` — signals whether work should block on prerequisites (N), proceed to next phase (S), explore parallel work (E), or retreat/reframe (W)

2. **Manifest next_task_queued field** — Explicitly states the next work; agents read this and prioritize it

3. **Investigation_label field** — Clusters related work; agents in same investigation_label find and support each other's work

4. **Manifest quality_score + belief_index** — Signals reliability; agents trust high-scoring findings and act on low-scoring ones conservatively

5. **Compass edges in graph form** — The full `--topology` query shows all four directions for a mission, helping agents understand what's blocked, what can proceed, what needs parallel validation

6. **NECTAR.md and HONEY.md** — Latest findings and crystallized principles; agents read these to learn what was recently discovered or proven

7. **Droplets (LIVE-{date}.md)** — Inspirational nuggets that agents can discover and apply across investigation_labels

8. **COC entries** — Full provenance trail; agents read COC to understand why prior decisions were made and avoid repeating mistakes

---

## Why This Matters

Without stigmergy, agents would need to coordinate through main context or direct calls. Scaling would be limited by:
- Main context bottleneck (can only coordinate what fits in one context window)
- Tight coupling (Agent A calling Agent B means Agent B's availability affects Agent A)
- No learning feedback (decisions don't propagate; same mistakes repeat)

With stigmergy:
- **Scaling is unbounded** — Agents coordinate via filesystem; no central bottleneck
- **Loose coupling** — Agent A doesn't wait for Agent B; Agent A acts on traces B left, and B acts when ready
- **Learning propagates** — Findings are written to NECTAR/HONEY; all future agents read them

This is how **emergence happens.** Enough agents + traces + decision-making density produces behaviors the system wasn't explicitly programmed to do.

---

## Applying This Framework

If you're building an agentic system:

1. **Design for stigmergy first** — How will agents leave traces? What signals matter?
2. **Make traces discoverable** — Investigation_labels, compass edges, quality scores should be findable
3. **Give agents full visibility** — Agents should be able to read all manifests, all forensics, all prior findings
4. **Trust emergence** — Don't over-specify coordination; let agents discover the work that needs doing
5. **Capture everything** — Forensic chains mean agents can act boldly because mistakes are recoverable

---

## Related Reading

- **Formal framework:** [3x-EMERGENCE.md](../../gitrepos/faerie2/docs/3x-EMERGENCE.md)
- **Session evidence:** [Substrate Emergence Narrative](./Narratives/2026-04-25_substrate-emergence-narrative.md)
- **Mutation discipline:** [EMERGENCE-AND-MUTATION-GLOSSARY.md](../../gitrepos/faerie2/docs/EMERGENCE-AND-MUTATION-GLOSSARY.md)
- **Operational glossary:** Terms like "investigation_label", "compass_edge", "blanking rule" — see [TERMINOLOGY-STANDARD.md](../../gitrepos/faerie2/docs/TERMINOLOGY-STANDARD.md)

---

**This doc is live and will grow as new emergence patterns are observed.**

Updated: 2026-04-27 | Hash: pending
