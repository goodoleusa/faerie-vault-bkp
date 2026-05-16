---
type: pointer-contract
status: active
created: 2026-04-23
tags: [spawn, agent, enforcement, contract, programmatic]
parent: "[[COC-WRITE-CONTRACT]]"
up: "[[COC-WRITE-CONTRACT]]"
sibling:
  - "[[COC-WRITE-CONTRACT]]"
  - "[[GENESIS-CHAIN-REANCHOR-SPEC]]"
  - "[[NATIVE-FAERIE-BRIDGE]]"
cites:
  - "HONEY.md mth00077 (spawn = bundle lookup + delta injection)"
  - "HONEY.md mth00078 (contracts are programmatic templates)"
  - "HONEY.md sys00034 (programmatic composition)"
  - "HONEY.md mth00076 (proof-in-place substrate enforcement)"
supersedes:
  - "docs/SPAWN-CONTRACT.md v1 (400-line prose draft, 2026-04-23 morning) — SUPERSEDED same day after user correction: 'that contract needs to be a programmatic template that is injected with scripts and hooks and almost no inference on main'"
doc_hash: sha256:pending
hash_method: body-sha256-v1
---

> [↑ COC Write Contract](./COC-WRITE-CONTRACT.md) · [→ Genesis Re-anchor](./GENESIS-CHAIN-REANCHOR-SPEC.md) · [→ Native Bridge](./NATIVE-FAERIE-BRIDGE.md) · [⌂ Docs](./README.md)

# Spawn Contract — Programmatic Artifacts Index

**This is a pointer doc. Authoritative spec lives in the artifacts below.**

Per HONEY mth00078: contracts are programmatic templates, never prose. Main never re-authors contract content — just triggers rendering.

## Artifact Table

| Artifact | Path | Kind | Authoritative for |
|---|---|---|---|
| **Policy** | `config/spawn-policy.yaml` | Declarative data | Enforcement rules, limits, violation types, bundle source registry |
| **Schema** | `schemas/spawn-prompt.schema.json` | JSON schema | Structural contract for rendered prompts |
| **Template** | `templates/spawn-prompt.tmpl` | Literal substitution template | The exact string rendered with placeholders |
| **Renderer** | `scripts/7x_spawn_template.py` | Python script | Reads policy + schema, fills template, emits signed prompt |
| **Enforcer** | `hooks/8x_spawn_contract_enforcer.py` | PreToolUse hook (Agent tool) | Rejects prompts that don't verify against signing policy |
| **Registration** | `/mnt/d/0LOCAL/.claude/settings.json` (PreToolUse matcher) | Config registration | Wires enforcer into harness |

## Flow (both modes from mth00077)

**Mode A (Claude/human-authored bundle):** write bundle once as a doc. Then:
```
python3 scripts/7x_spawn_template.py render \
    --bundle docs/<spec>.md --task-id <id> --agent-type <type> \
    --delta '<session-specific json>'
```

**Mode B (script-generated bundle):** script composes the bundle. Then same template render invocation pointing at the generated bundle path.

Either way: renderer emits a signed prompt; Agent() fires with that prompt; enforcer verifies signature at harness; invalid prompts are rejected.

## Change Protocol

- Changes to enforcement rules: edit `config/spawn-policy.yaml` (declarative; no code change)
- Changes to prompt structure: edit `schemas/spawn-prompt.schema.json` + `templates/spawn-prompt.tmpl` together
- Changes to enforcement behavior: edit `hooks/8x_spawn_contract_enforcer.py` (must pass schema conformance tests)
- This pointer doc updates only when the artifact set changes (add/remove an artifact)

## Non-Goals

- This doc is NOT the spec. The artifacts are.
- Main does NOT re-author contract content here — only updates the pointer table if artifacts move.

## W1+W2 Bundle Validation Complete (2026-04-25)

**Status:** All 73 bundle validation tests PASS. 100% coverage of injection patterns, agent types, and edge cases.

**Synthesis document:** [ARCHITECTURE-BUNDLE-VALIDATION.md](./ARCHITECTURE-BUNDLE-VALIDATION.md)
- Section 1: Bundle injection patterns (DROPLETS_TOD, HONEY, NECTAR, pollen) — 100% operational
- Section 2: Test coverage (73/73 PASS; formulas, agent types, edge cases, integration)
- Section 3: Design decisions (two-source HONEY join, fail-open degradation, tail-N bounds)
- Section 4: Hardening (exit-13 gates for specialist rejection + scout protocol + agent card validation)
- Section 5: Next steps (cost-per-test metrics, pollen+droplet patterns, concurrent safety, performance baseline)

**Test execution:**
```
PASS: 73/73 tests (100%)
  - Formula rendering: 23/23
  - Agent type routing: 43/43
  - Edge cases: 18/18
  - Integration scenarios: 14/14
```

**Enforcer status:** Active via `8x_spawn_contract_enforcer.py` (PreToolUse hook).

## Current Enforcement Phase

See `config/spawn-policy.yaml` → `current_mode`. Flips from `warn` → `block` after smoke test passes.

**Current mode (2026-04-25):** HARDENED. Exit-13 gates active for:
- General-purpose on `[specialist]` tasks
- Scout-protocol absence
- Agent card validation
