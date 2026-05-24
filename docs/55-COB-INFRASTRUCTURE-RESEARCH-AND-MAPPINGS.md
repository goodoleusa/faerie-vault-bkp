# COB Infrastructure Research → Swarmy Mappings

Source dossier for the `agents-as-bonded-creatures` charter
(`forensics/charters/active/2026-05-22_agents-as-bonded-creatures.json`).
Maps the Creatures 3 modding community's infrastructure (1999–2025) onto
swarmy's existing primitives + identifies gaps. The COB community is
the canonical reference for "early ML aesthetics" the user invoked.

---

## Why this matters

The Creatures series shipped 1996–2001 with an embedded scripting
language (CAOS), packaged-mod format (COB / agent bundles), genetics
editor, sprite editor, brain inspector, and an injector — a complete
mini-platform. The community then BUILT 25 years of mods, tools, and
archives atop it. Their conventions are the working precedent for
"thinking-feeling creatures we bond with" — exactly what swarmy is
trying to be at the agent layer.

We're not cloning Creatures 3. We're learning from a mature community
that solved many of the same problems (lineage, persistence, modding,
bonding) and surfacing what's already present in swarmy vs what needs
explicit work.

---

## Concept-by-concept mapping table

| Creatures 3 concept | What it is | Swarmy equivalent today | Gap |
|---|---|---|---|
| **CAOS (Creatures Agent Object Script)** | Embedded register-based scripting language. Opcodes with fixed arg lists. 100 VAxx registers + TARG selector + 100 OVxx attribute registers per object. | MCP tool calls = the agent's "verbs"; `@authed` decorator pattern is the calling convention | We don't have a formal DSL. Could formalize ".caos" snippets if useful, but MCP/Python is probably the better long-term substrate. |
| **COB (Creatures Object Bundle)** | Packaged CAOS scripts + sprites + dependencies injected into the running game | `.agents/skills/<name>/` directory = packaged microagent (frontmatter + body + helper scripts) | **GAP**: we don't have an INJECTION mechanism that lets one user share a skill with another mid-session. eem.foo-style archive exchange is the next-phase ask. |
| **Genetics Kit** | Official tool for editing Norn DNA — visual editor over a binary genome | SKILL.md frontmatter (triggers, type, description) = the "DNA"; manifest's completion_choice = chemistry/drives | **GAP** (already queued in creatures charter): visual editor for SKILL.md (no need to hand-edit YAML to mod a creature). |
| **Injector** | Drops a COB or agent into a running world | `spawn.py` + `0b_spawn-executor.py` = injects agents into the swarm | Aligned. The pattern matches. |
| **GENE LOAD (CAOS command)** | Loads a genetics file into a gene slot of an agent at runtime | spawn-time `SKILL.md` resolution = each spawn loads its skill set | Aligned. |
| **Genome 0 / Genome 1 / Norns variants** | Archetype creatures with different baseline genetics | Microagent types (NAVIGATOR, MAKER, BRIDGE, DEEP-DIVER per CLAUDE.md spawn doctrine) = archetype species | Aligned. The 4 bearings map naturally to species. |
| **Norn / Grendel / Ettin / Shee** | 4 in-game species with different roles | Maker (Norn) / security-auditor + error-detective (Grendel adversarial) / infrastructure (Ettin long-lived) / user-as-Shee (architect) | **GAP**: this taxonomy is implicit; could be formalized for visual species-cards on canvas. |
| **TARG selector + OVxx attributes** | Each agent has 100 read-write attributes accessible via CAOS | Manifest.completion_choice fields (kind, target, rationale, confidence, sensitivity, visibility) ≈ the writable attributes per agent | Aligned (smaller vocabulary, structured JSON). |
| **Roomie + Spritist** (unofficial tools that became more popular than official ones) | Community-built better modding tools | Not built yet | **GAP**: opportunity for community-built modding tools layered atop the canonical pipeline. The pattern is healthy: ship core, let community build the polish. |
| **eem.foo archive** | Largest archive of Creatures content (COBs, agents, breeds, tools) — searchable, categorized, public | Not built yet | **GAP**: canonical public registry of community SKILL.md bundles + creature genomes. v2 of the swarmy-hive-plugin marketplace. |
| **C3DS Community Edition** | Patched version of the Docking Station engine to fix bugs + add features 25 years on | OpenHands SDK (which we deploy via swarmy-openhands container) | Aligned. The platform is itself open-source. |
| **Docking Station Engineer** (custom ChatGPT agent launched 2025-08) | Specialized helper agent for C3/DS users | Not built yet | **GAP**: a swarmy-tutor microagent that onboards new users + answers "how do I X" questions. Low-effort, high-leverage. |
| **Creatures Caves community** + IRC + Discord + subreddit + blogs | Distributed community across multiple channels | Not built yet (private repo · two contributors) | **GAP**: aspirational — when swarmy goes public, design the community hub deliberately. The Creatures community survived 25 years; their model is worth studying. |
| **GENE_LOAD slot-based loading** | Genetics file → gene slot of an agent (multiple gene slots possible) | Each spawned agent loads ONE skill set today | **OPPORTUNITY**: multi-slot skill loading per agent — agent could load primary skill + 2-3 secondary skills (like Norns having gene slots for different organs). |
| **Brain organ inspector** | Visual viewer for a Norn's neural network state | Manifest reader + COC chain viewer (text-based today) | **GAP** (queued in creatures charter): visual brain-inspector for which manifests an agent read + recent thoughts. |
| **Norn-injection .cos files** | Plain-text CAOS scripts injectable via the engine | Charter JSON + manifest JSON = injection format today | Aligned. JSON is the modern .cos. |
| **Creature naming** | Norns have names; users develop bonds with named creatures | Agents are anonymous today (just `agent_type`) | **GAP** (queued in creatures charter deliverable #1): persistent names like `amber-wing`. |
| **Breeding (mating between two parent Norns)** | Two parents produce offspring with traits from both + mutations | Compositional spawn (multi-agent waves) doesn't currently inherit traits | **GAP** (creatures charter phase 2 roadmap): explicit two-parent spawn. |
| **Creature death + memorialization** | Norns can die; users mourn + display them in graveyards | `completion_choice.kind=goodbye` exists but is just terminal | **GAP** (queued in creatures charter deliverable #6): ceremonial memorial entries; ancestors summonable for advice. |

---

## What this tells us about priorities

The creatures-as-bonded-creatures charter already covers 6 of the major gaps. The dossier highlights 3 additional opportunities worth adding to phase 2 roadmap:

1. **Multi-slot skill loading per agent** (analog to multiple gene slots) — let an agent be primarily a MAKER but with secondary BRIDGE skill loaded for cross-team work
2. **Public SKILL.md registry (eem.foo-style)** — when swarmy goes public, ship an archive where community members can share microagent skills + creature genomes by exporting their SKILL.md bundles
3. **A "swarmy-tutor" microagent** like the recent ChatGPT-based Docking Station Engineer — onboarding helper that answers "how do I spawn a creature" / "what bearing should I pick" / "how do I write a charter cluster_prefix"

---

## What we should NOT copy

- **Binary genome format** — CAOS used binary because 1999 disk space mattered. Stick with JSON for our genomes (SKILL.md + completion_choice history); human-readable is the point.
- **C++ engine internals** — we're not building a sim engine; the LLM is the engine.
- **The closed-source-then-abandoned official tool problem** — keep everything open from day 1. Community tools (Roomie, Spritist) became more popular than official ones BECAUSE the official ones became unmaintained. Bake openness into the canonical layer.
- **The "creature can starve" emotional weight** — drives are useful metaphors but we don't want existential anxiety encoded into agent dynamics. Drives surface system state to the caretaker, they don't punish creatures.

---

## Sources

- Creatures Wiki — primary reference (CAOS, COB, GENE LOAD, Injector, Genetics Kit, Modding in the Creatures series, C3DS Community Edition)
- PCGamingWiki — Creatures + Creatures 3 fixes and mods
- lisdude.com — C3DS Community Edition + CAOS Tool Introduction
- creatures.fandom.com — CAOS wiki (community fandom variant)
- eem.foo — the canonical archive (largest community content collection)
- Caos Coding Cave (Discord) — current active modding community
- Creatures Docking Station — Creator Tools — Steam re-release with the official tools (2025-era)

---

## How to use this dossier

When the creatures charter spawns implementation agents:

1. **Reference this doc** in agent prompts as the "concept mapping reference"
2. Each phase_1 deliverable in the creatures charter cites one row of the mapping table above
3. Phase_2 roadmap items (breeding, multi-species ecosystems, retirement homes) explicitly draw from this dossier — don't re-derive from scratch
4. When a new community feature is queued (registry, tutor, multi-slot skills) — check this doc FIRST to see if Creatures already solved it
5. Credit the Creatures community in any public-facing material that adopts their patterns (CC Chat, eem.foo, the Wiki maintainers)

---

*Maintained at: `docs/55-COB-INFRASTRUCTURE-RESEARCH-AND-MAPPINGS.md`.
Cited by: `forensics/charters/active/2026-05-22_agents-as-bonded-creatures.json`.*

---

## Addendum — caoschaos.com (browser-based modding tools)

User pointer (2026-05-22 ~00:50): **caoschaos.com** is a community-built
browser platform by **bedalton** that ships three browser-native tools.
Direct precedent for our visual modding pattern.

### Tools available at caoschaos.com

| Tool | URL | Function | Swarmy analog |
|---|---|---|---|
| **CAOS Editor** | caoschaos.com/editor/ | Browser-based CAOS code editor with code-completion (alpha) | The visual SKILL.md editor (creatures charter deliverable #8) — write Python-CAOS-like declarative skill snippets in-browser with autocomplete on canonical vocabularies (bearings, completion_choice kinds, hypothesis tags) |
| **Quick Appearance Editor** | caoschaos.com/appearance-editor/ | Edit creature appearance genes in the browser (visual sliders → genome bytes) | The Creature Anatomy View (creatures charter deliverable #7) — but EDITABLE; drag sliders for trait dominance, see live anatomy update |
| **Sprite Decompiler** | caoschaos.com/sprite-parser/ | Parses SPR / S16 / C16 / BLK files in-browser; compiles sprites for all Creatures games | Not directly relevant (we use SVG/CSS not pixel sprites) — but the pattern of "drop file → parse client-side → edit → re-export" applies to our SKILL.md upload + edit flow |

### What caoschaos.com proves out

1. **Browser-native modding tools work.** No installs, no platform-specific binaries — drag-drop a file, edit, download. We should target the same UX for the visual SKILL editor.
2. **One developer can ship credible community infrastructure.** bedalton ships and maintains the whole platform. Lesson: don't over-architect; ship lean tools, iterate publicly.
3. **Alpha releases get adopted.** The CAOS Editor is labeled "alpha" but the community uses it. Lesson: ship the visual SKILL editor at alpha quality + iterate with JescaLyn + community feedback.
4. **Tool composition over monolithic UI.** caoschaos.com has THREE separate tools, not one big editor. Lesson: ship the visual SKILL editor + the anatomy editor + (later) the brain inspector as separate URL-addressable tools, not nested tabs of one mega-tool.

### Also discovered

- **Creatures-Developer-Network/awesome-creatures-development-resources** (GitHub) — curated list of community development resources. This is the model for our future public SKILL.md registry — instead of building our own portal first, can start by maintaining a GitHub-curated awesome-swarmy-skills list.

### Credits

- **CAOS Chaos** (browser tools): bedalton (https://caoschaos.com/)
- **awesome-creatures-development-resources**: Creatures-Developer-Network maintainers (GitHub)
- Add to canonical credits file (`docs/50-CARTOGRAPHER-ASSETS-CREDITS.md`) if any visual assets or code patterns are borrowed.

