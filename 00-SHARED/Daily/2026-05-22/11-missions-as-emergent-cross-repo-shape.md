---
date: 2026-05-22
author: goodoleusa + openhands-agent
related_mission: missions-as-emergent
status: synthesis-log
canon_candidate: true
---

# Missions are emergent shape-patterns, not forced assignments

User stated (verbatim, the corrective):

> "but we shouldnt be forcing missions to hapepen, missions can
>  naturally evolve from what the agents experience, ideally missions
>  are semantically and logically linked tasks in certain bearing
>  direction that all fit the same shape and serve the same goal. that
>  way instead of just fixing one thing on one repo, a mission moves
>  progress in a safe yet swift manner across ALL repos who have that
>  same sort of shape or issue"

This is THE corrective on missions. Earlier doctrine (08 + 09) framed
charters as the bounding boxes around mission flow — true. But the
mission *itself* needs proper framing: it is **emergent shape**, not
an assignment.

## The corrected definition

**A mission is:** a set of semantically + logically linked tasks
that:
- share a **bearing direction** (N unblock / S ship / E parallel / W baseline)
- share a **shape** (same kind of work — same fix pattern, same
  refactor pattern, same audit pattern)
- serve a **shared goal**
- can be applied to any artifact that matches the shape

The cluster_prefix=3 (the w3w address) is the mission's NAME but not
its essence. The essence is the SHAPE.

## What "shape" means concretely

A shape is recognizable across files, modules, projects, repos:

| Shape | Example | Where it shows up |
|---|---|---|
| "stranded `@authed` without `@mcp.tool()`" | The mcp-overhaul bug | Every repo's MCP layer |
| "missing frontmatter on synthesis log" | Vault hygiene | faerie-vault + swarmy-vault-template + any sister vault |
| "deprecated DelegateTool → TaskToolSet rename" | OH-SDK 1.23 migration | Every repo using openhands-sdk |
| "missing `signed_by` on manifest write" | Signing-enforcement | Every forensics tree across all repos |
| "active charter open >7 days with no new deliverables" | Stale-charter detection | faerie2 + any repo with charters |
| "card template uses hardcoded bearing colors" | Visual-language consolidation | chat-mvp + swarmy-hive-plugin + any future surface |
| "cluster_prefix length != 3" | Mission addressing violation | Every charter set |

Each shape is a mission CANDIDATE. The mission doesn't exist until
an agent (or a human) recognizes the pattern. Once recognized, it
becomes an emergent mission with its own cluster_prefix.

## Why this matters: cross-repo propagation

If we fix "stranded @authed" only in faerie2, we miss the same shape
in:
- `cybertemplate` (if it ever grows MCP tools)
- `hustle` (if it has its own server)
- any future repo

But if we frame it as a MISSION — `mcp.authed.stranded` — the work
naturally propagates: any time a swarm agent scans a repo with the
same shape, the mission's accepted protocol applies.

**The killer property:** mission propagates SAFELY (the protocol
defines acceptance) but SWIFTLY (you don't redo the analysis per
repo).

## What's different from "forced" missions

Forced (anti-pattern):
- Human assigns a mission to an agent
- The agent works the mission in one repo
- "Mission complete" when that one repo is done
- The shape elsewhere is invisible until someone else notices

Emergent (canonical):
- Agent encounters a SHAPE while doing other work
- Agent appends `discovered_work[]` to its manifest with bearing +
  rationale
- Subsequent agents read the frontier, see the recurring shape,
  cluster their cluster_prefix to it
- A charter eventually forms around the cluster (bounding box on
  the convergent work)
- Charter + mission propagate ACROSS REPOS that match the shape

The shape comes FIRST. The mission emerges from shape recognition.
The charter forms to bound the propagation. Order matters.

## Cross-repo mechanism (what we have + what's missing)

### What we have today

1. **Vault as cross-repo state** — every swarmy-family repo shares
   the faerie-vault. A narrative about a recognized shape in
   faerie-vault is visible to agents in any repo.
2. **Manifest frontier scan** — `forensics/manifests/{date}/` per
   repo. An agent in cybertemplate can read faerie2's manifests if
   given access.
3. **Mission graph addressing** — cluster_prefix=3 is
   repo-agnostic. `mcp.authed.stranded` reads the same regardless of
   which repo's MCP layer.
4. **Skills (`.agents/skills/`)** — semantic patterns + recipes.
   If a skill defines "how to detect stranded @authed," every repo
   that loads the skill carries the detection logic.
5. **poll-deploy daemon** — 5 repos polled every 5 min. Each repo's
   own deploy script reads its own forensics; the cross-repo
   convergence is at the vault + skill layers, not the deploy layer.

### What's missing for full cross-repo mission propagation

1. **Shape-scanner skill** — `.agents/skills/shape-scanner/SKILL.md`
   doesn't exist yet. Should codify: "given a shape (regex or AST
   query), find every match across all configured swarmy-family
   repos." Triggers: 'find this shape', 'where else does X appear',
   'cross-repo audit'.

2. **Shared mission registry** — a vault-level
   `_meta/missions.json` (or `_meta/mission-shapes/{slug}.json`) that
   defines: shape detector, acceptance protocol, applicable repos.
   Agents in any repo read this registry.

3. **Manifest schema field** — `applicable_repos[]` on missions. If
   a mission emerges as cross-repo, this field lists which repos
   carry the shape today. Agents in those repos consume the mission
   without re-deriving.

4. **Cross-repo COC** — today each repo has its own
   `forensics/coc.jsonl`. A mission that propagates across 3 repos
   produces 3 separate chains. The vault could carry a
   `cross-repo-mission-log.jsonl` that stitches them.

## Concrete example: how the mcp-tool-consolidation mission emerged

User said today (verbatim): "i thought we wanted less tools, not
more...?" THIS is shape recognition.

The shape: "MCP server has too many granular tools that should be
verb-dispatcher-merged." This shape:
- has bearing direction = S (ship — concrete consolidation work)
- has a clear acceptance protocol (tool count below threshold + 18
  critical tools still pass)
- serves a goal (smaller cognitive surface, easier discovery)
- can be applied to ANY repo that exposes an MCP-style tool set

The mission emerged from the user's complaint. It got a w3w
address: `mcp.tools.consolidate`. A charter formed (the 62→~30
standing mission). Wave 1 shipped (85→75). Wave 2 in flight (target
<40).

This mission CAN propagate cross-repo when:
- cybertemplate grows an MCP layer → mission applies
- swarmy-hive-plugin exposes tools → mission applies (with adjusted
  protocol since TS not Python)
- any future product surface that has "too many granular tools" →
  the same protocol fires

## What changes operationally

For agents:
- When you encounter a shape mid-task, **always** append to
  `discovered_work[]` with bearing + rationale. Don't try to fix
  the shape in scope — that's how charters get crept.
- When you DECIDE to commission a charter for an emerging shape,
  use the cluster_prefix=3 to give it its address. The CHARTER is
  the bounded box; the SHAPE is the underlying mission essence.

For humans:
- Don't write missions in advance. Author SHAPES (in skills or
  inspirations) and let missions emerge when agents repeatedly hit
  the same shape.
- A "mission" with one charter in one repo is fine but ungeneralized.
  A mission with multiple charters across multiple repos sharing the
  same shape is fully emergent and worth crystallizing in
  `_meta/mission-shapes/`.

For the genesis script (`0x_charter_genesis.py`):
- The MISSION-CLUSTERS.md output already surfaces uncharted
  clusters — that's shape detection at the cluster_prefix level.
- Next enhancement: also surface cross-repo clusters. Read other
  repos' `forensics/manifests/{date}/` if cross-mounted, group by
  cluster_prefix, surface multi-repo missions explicitly.

## Single-line summary

**Missions emerge from shape recognition — they aren't assigned.
The cluster_prefix=3 is the mission's address; the shape is its
essence. Charters bound the propagation; the SAME mission can spawn
many charters across many repos as the shape appears. Don't force;
let shapes surface, then commission charters around them.**

---

*Capturing today (2026-05-22) at user's articulation. Companion to
`08-living-graph-vs-bounded-charters.md` (charters as boxes on the
flow) and `09-type-ontology-parent-child.md` (the commission rule).
Together: 08 = dynamics, 09 = types + lineage, 11 = emergence.
Should fold into Part 4 of
`docs/45-SEMANTIC-MISSION-EMERGENCE-CANONICAL.md` as the third
sub-section (after addressing layer + types).*
