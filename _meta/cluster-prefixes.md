# cluster_prefix — the scope fence

Every charter declares a `cluster_prefix`. It is the load-bearing field that
tells the swarm **what this charter is allowed to touch**.

## The rule (canonical, schema-locked)

```
cluster_prefix MUST be a JSON array of EXACTLY 3 strings.
```

Source of truth: `_meta/schemas/charter.schema.json` — `minItems: 3,
maxItems: 3`.

This is not a guideline. It is a schema constraint, and your swarmy install
will reject any charter that does not satisfy it.

## Why exactly 3?

Two items is too narrow (you can't express both a subject and a context).
Four or more items lets a charter slowly accrete unrelated work until the
scope fence is meaningless. Three is the smallest number that lets a
charter say "**this** kind of work, in **this** layer, for **this**
mission" — and nothing else.

Three items also forces the author to **choose**. Most early charter
drafts feel like they need 5–6 prefix tokens. The discipline of cutting it
to 3 is itself the work; if you can't reduce to 3, the charter is probably
two charters.

## What goes in each slot?

There is no strict positional schema (the items are an unordered set in
terms of validation), but the convention that has emerged across the
swarmy investigations is roughly:

| Slot | Meaning | Example |
|------|---------|---------|
| **1: domain** | What part of the system this touches | `vault`, `mcp-server`, `dashboard`, `forensics`, `ci-cd` |
| **2: layer** | What kind of work it is | `template`, `infra`, `ui`, `schema`, `ops` |
| **3: anchor** | The proper-noun anchor (mission, tool, surface) | `seed`, `swarmy`, `the-hive`, `caddy`, `evo-wave` |

A working example from this template's own charter:

```json
"cluster_prefix": ["vault", "template", "seed"]
```

A charter that wired W&B observability into swarmy might be:

```json
"cluster_prefix": ["observability", "infra", "wandb"]
```

A charter consolidating forensics subdirectories:

```json
"cluster_prefix": ["forensics", "ops", "consolidation"]
```

## Anti-patterns

- **More than 3:** the schema will reject the charter at write time. If
  you find yourself wanting 5 tokens, you have a charter-split problem,
  not a prefix problem. Read the `charter-discipline` microagent — it has
  a section on splitting charters.
- **Too generic:** `["work", "stuff", "swarmy"]` passes the schema but
  doesn't fence anything. The agents reading the frontier can't tell what
  this charter is for. Be specific.
- **Repetition:** `["vault", "vault", "vault"]` technically passes the
  schema but is structurally meaningless. Pick 3 *distinct* tokens.

## How agents use it

When an agent reads the frontier (`forensics/charters/active/`), they
filter by `cluster_prefix` membership. If an agent's mission is
`vault-template-seed`, they look for charters whose prefix contains
`vault` AND `template` AND `seed` — and they ignore everything else.

The 3-item rule is therefore a **performance contract** with the swarm:
your charter declares its scope upfront, agents route on it in O(1),
nobody wastes context reading misclassified work.

## Further reading

- `_meta/microagents/charter-discipline/SKILL.md` — full discipline doc
- `_meta/schemas/charter.schema.json` — the JSON Schema (authoritative)
- `00-Welcome/02-your-first-charter.md` — walkthrough using this rule
