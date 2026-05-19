---
type: faerie-internal
subtype: template
canonical_source: /mnt/d/0local/gitrepos/faerie2/prompts/partials/coc-discipline.njk
canonical_sha256: 12eb1ed148f8643b3a799da92b03cf786c2ee7facb7b1017a0e2d57a4fb568ce
last_synced: '2026-05-19T15:24:06+00:00'
purpose: Chain-of-custody discipline reminder
variables: []
includes: []
used_by: ['scripts/prompt_loader.py', 'deploy/mcp-server/sdk_chat.py']
N: '[Faerie System Internals Home](../../00-Home.md)'
E: []
tags: ['internal', 'template', 'njk', '#path/transparency']
---

# coc-discipline.njk

**Path:** `prompts/partials/coc-discipline.njk`

**Variables exposed:** _(none)_

## Plain English

The chain-of-custody discipline reminder — every agent receives this to know that all actions must leave a forensic trace.

## Raw template source

```jinja
## Chain-of-custody (COC) discipline
- Every action emits a forensic entry to `forensics/coc.jsonl`.
- Manifests written to `forensics/ephemeral/{date}/{task_id}/`; promotion
  to `forensics/manifests/{date}/` is automatic via PostToolUse hooks.
- Never write to canonical forensics paths directly — only via promotion.
- Hash before + after every durable write (belt + suspenders).
```

## Where it's used

- `scripts/prompt_loader.py` — Jinja/Nunjucks renderer
- `deploy/mcp-server/sdk_chat.py` — applied at conversation init
- MCP tool `faerie_prompt_view` exposes the rendered output

> [!warning] Read-only mirror
> Canonical source: `/mnt/d/0local/gitrepos/faerie2/prompts/partials/coc-discipline.njk`
> Edit there, not here. Re-run `scripts/dev/vault/09-internals-sync.py` to refresh.
