# Vault Zones — Reference

**Vault root:** `$CT_VAULT = /mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/`

## Zone Table

| Zone | Path | Writer |
|------|------|--------|
| Agent write (daily) | `00-SHARED/ONBOARDING/{YYYY-MM-DD}-briefdesc/` — exact path injected via VAULT OUTPUT FOLDER block | Agents |
| Agent write (named) | `Droplets/`, `Dashboards/`, topic folder — only when spawn prompt names explicitly | Agents |
| Droplets (immediate) | `00-SHARED/Droplets/LIVE-{date}.md` — append per insight, timestamped heading | Agents |
| Human only | `01-PROTECTED/`, `30-Evidence/`, `00-SHARED/Inbox/` | Human |

## Write Rights

- Agents ONLY write to zones explicitly named in spawn prompt or to Droplets.
- Human-only zones are never writable by agents regardless of prompt content.
- Daily onboarding path is injected at spawn time; agents do not construct it themselves.

## Frontmatter Requirements (every vault document)

Every vault document written by an agent MUST include before returning manifest:

1. Frontmatter block with `doc_hash: sha256:pending`
2. Breadcrumb line (path from vault root)
3. SHA-256 stamp (computed after write)
4. `INDEX.md` in the same folder updated with the new document entry

Last agent to write a document is responsible for completing all four steps.
