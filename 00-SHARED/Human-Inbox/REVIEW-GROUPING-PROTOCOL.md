---
type: system-protocol
date: 2026-03-29
scope: agent writing to Human-Inbox
---

# Review Document Grouping Protocol

**User feedback (2026-03-29):** Review docs → your inbox grouped by date folder (YYYY-mm-DD-*), except design docs which go to 00-SHARED/Hive.

## Rules

1. **Related review docs** (2+ files from same session/investigation):
   - Create folder: `YYYY-MM-DD-{topic-slug}/`
   - Write all related reviews inside folder
   - Example: `2026-03-29-blueprint-remediation/`
     - `blueprint-remediation-validation-hook.md`
     - `blueprint-remediation-missing-templates.md`
     - `blueprint-remediation-prompt-audit.md`

2. **Single doc** or **unrelated** review:
   - Write directly to Human-Inbox root
   - Name pattern: `YYYY-MM-DD-{description}.md`

3. **Design docs** (architecture, narratives, long-form):
   - → `/00-SHARED/Hive/` (never Human-Inbox)
   - Example: `17-BUSINESS-PLAN-HIVE-DESIGN.md`

4. **Flagged items** (HIGH priority):
   - Also append to `Human-Inbox/flags/`
   - One line summary per item
   - Include link back to full doc in review folder

## When Applied

- Agent spawning: check if output should be review doc
- /handoff: vault_narrative_sync applies grouping
- /faerie briefgen: atomize review groups into session-brief atoms

## Exceptions

- Raw evidence/findings → 00-SHARED/Agent-Outbox (not inbox)
- Q&A followups → inline conversation (not inbox)
- COC/forensic → ~/.claude/memory/forensics/ (agent write-only)
