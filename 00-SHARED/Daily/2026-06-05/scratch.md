---
source: /mnt/d/0local/gitrepos/reckon/forensics/ephemeral/2026-06-05/chat-debug-robust-01/scratch.py
promoted: 2026-06-06T00:37:52.662421+00:00
---

# scratch.py

```
# SPRAY scratch — chat-debug-robust-01
# Approaches:
# 1. /chat/diagnose: ordered checks, real httpx call to OR, no auth
# 2. /chat/ping: trivial liveness (no auth)
# 3. verbose logging in chat_endpoint: sha256 hash of token, conv_id, frame count, elapsed
# 4. ChatDebugPanel: collapsible, auto-refresh, run-full-diag, copy report, clear error
# 5. chatStore fixes: no-token visible system msg, lastRequestStats, empty stream detection
# 6. Chat.jsx: import + render ChatDebugPanel above MessageInput in footer
#
# Key decisions:
# - diagnose endpoint: no auth so it works even when token is broken
# - test_llm_call: direct httpx to OR, bypass SDK complexity
# - frontend auto-refresh: 5s interval via useEffect
# - interactive: per-check expand, spinners, copy, manual re-run

```
