---
doc_hash: sha256:pending
created: 2026-04-25
type: legacy-reference
source: ObsidianVault/README.md
archived_from: ObsidianVault/ (legacy Swarmy era, pre-faerie2 rename)
breadcrumb: "vault / 00-Welcome / legacy-swarmy-architecture"
---

# Legacy Architecture Reference — Swarmy Era

> This document was the original ObsidianVault/README.md from before the project was renamed to faerie2. The system described here is the predecessor to f(0). The core architecture — stateless agents, vault as bus, stigmergy, champagne pyramid context loading — remains valid. The tooling names (agent_runner.sh, 2a_context_builder.py, etc.) refer to the old runner infrastructure, not the current 7x_spawn_template.py / faerie-queue system.
>
> Preserved as intellectual history. See [[INDEX]] for the current system.

---

The key concepts that survived the rename:

- **Stigmergy**: agents communicate through the vault, never directly (still principle 1)
- **Champagne pyramid context loading**: tiered context assembly by importance (now: bundle model)
- **Stateless agents, stateful vault**: each agent boots fresh, reads vault, writes vault, exits (unchanged)
- **Vault as bus**: filesystem IS the coordination mechanism (still core)
- **Human sovereign**: human approval gates on findings (unchanged)
- **Cost argument**: subagent isolation prevents quadratic token accumulation (still the f(0) math)

What changed:
- `agent_runner.sh` → `7x_spawn_template.py` (template-signed bundles, contract enforcement)
- `00-Inbox/*.task.md` → `sprint-queue.json` (atomic JSON queue with monkeybranch)
- `AGENT-REVIEW-INBOX.md` → forensic manifests + dashboard_lines (cascading summarization)
- GPG signing → Ed25519 + HMAC-SHA256 COC chain
- `scripts/2a_context_builder.py` → bundle model (discovery.json inlined, anti-gaming)
- "Swarmy" → "faerie2" (same hive metaphor, tighter f(0) discipline)

---

*Full original text of ObsidianVault/README.md preserved in forensics/deletions/ per COC protocol.*

[[00-Welcome/INDEX]] | [[10-Processes/INDEX]]
