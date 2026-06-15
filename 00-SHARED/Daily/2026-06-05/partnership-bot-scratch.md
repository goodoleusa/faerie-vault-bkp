---
source: /mnt/d/0local/gitrepos/reckon/forensics/ephemeral/2026-06-05/partnership-bot-01/partnership-bot-scratch.py
promoted: 2026-06-06T00:13:03.542065+00:00
---

# partnership-bot-scratch.py

```
# SCRATCH — partnership-bot-01
# Approaches considered:
# 1. Single Python script, argparse CLI, anthropic + httpx
# 2. Read patent/GOLD context at runtime vs hardcode
#    -> Runtime read is cleaner; hardcode claims titles as fallback
# 3. Config JSON + env var override pattern
# 4. HTML email: two sections, one send to treasonhunter@proton.me
# 5. Dashboard integration: new panel + new API route in api_server.py
#
# Decision: runtime read first 50 lines patent, 30 lines GOLD.
# Fall back to hardcoded if files not found (portable).
# Model: claude-haiku-4-5-20251001
# Resend via httpx (no requests)
# Dashboard: add Panel 5 — Partnership Bot to index.html + /partnership-draft route to api_server.py

```
