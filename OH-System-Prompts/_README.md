# OH-System-Prompts

This folder is the **Obsidian editing surface** for OpenHands (OH) system prompts.

## How it works

1. **Source of truth**: `prompts/system/*.njk` in the swarmy repo.
2. **Sync**: `scripts/9x_sync_oh_system_prompts_to_vault.py` copies .njk content
   into this folder as `.md` files (idempotent, cron-safe).
3. **Edit**: open any `.md` here in Obsidian. The `njk` fenced block IS the prompt.
   The hive plugin renders Nunjucks preview inline via the blueprint engine.
4. **Push**: run `Swarmy: push system prompt to OH session` (command palette).
   - Calls `swarmy_prompt verb=update` via MCP.
   - Server writes back to `prompts/system/<name>.njk`.
   - Broadcasts a `.reload-signal` so active OH sessions pick up the new prompt
     on the next agent turn (no restart required).
   - **Pro subscription required** for push. View/list is demo-accessible.

## Tier gating

| Action | Min tier |
|--------|----------|
| View / list prompts | demo (no signup) |
| Push changes to OH session | pro |

Demo callers see a `{error_type: tier_gate}` response; the hive plugin shows
an upgrade prompt instead of a raw error.

## Files in this folder

Each `.md` file corresponds to one `.njk` source file.  The `prompt_file`
frontmatter field is the relative path used by the MCP verb dispatcher.

_Managed by `scripts/9x_sync_oh_system_prompts_to_vault.py`. Do not rename._
