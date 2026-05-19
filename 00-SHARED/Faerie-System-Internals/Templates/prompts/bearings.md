---
type: faerie-internal
subtype: template
canonical_source: /mnt/d/0local/gitrepos/faerie2/prompts/partials/bearings.njk
canonical_sha256: 313b196d8595a191bcc5cf465c400ecd0bda4a688d744d498f2d07b532801351
last_synced: '2026-05-19T15:24:06+00:00'
purpose: Compass bearings partial (N/S/E/W vocabulary)
variables: []
includes: []
used_by: ['scripts/prompt_loader.py', 'deploy/mcp-server/sdk_chat.py']
N: '[Faerie System Internals Home](../../00-Home.md)'
E: []
tags: ['internal', 'template', 'njk', '#path/transparency']
---

# bearings.njk

**Path:** `prompts/partials/bearings.njk`

**Variables exposed:** _(none)_

## Plain English

Defines the four compass bearings (N/S/E/W) injected into every agent's system prompt. Common vocabulary for mission navigation.

## Raw template source

```jinja
## Compass bearings (N/S/E/W)
  N = unblock predecessors
  S = ship deliverables
  E = parallel sister work
  W = re-seat baseline assumptions
```

## Where it's used

- `scripts/prompt_loader.py` — Jinja/Nunjucks renderer
- `deploy/mcp-server/sdk_chat.py` — applied at conversation init
- MCP tool `faerie_prompt_view` exposes the rendered output

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/prompts/partials/bearings.njk`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
