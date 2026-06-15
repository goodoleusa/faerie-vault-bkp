---
source: /mnt/d/0local/gitrepos/reckon/forensics/ephemeral/2026-06-05/auth-simplify-01/auth-simplify-01-scratch.py
promoted: 2026-06-06T00:27:17.870837+00:00
---

# auth-simplify-01-scratch.py

```
# auth-simplify-01-scratch.py — SPRAY phase
# Task: add GET /auth/session endpoint + AuthPanel PATH E
#
# Approach for /auth/session:
#   - Read X-Forwarded-User header (set by oauth2-proxy via Caddy forward_auth)
#   - Look up existing token by github_login field in tokens.json
#   - If not found, mint a new one using secrets.token_hex(32) (same as github_auth_exchange)
#   - Return {ok, token, user: {login}, source: "forwarded_identity"}
#   - No auth on this endpoint (protected at Caddy layer)
#
# Token lookup pattern:
#   tokens = _load_tokens()
#   existing = next((t for t, r in tokens.items() if r.get("github_login") == username), None)
#   if existing: return existing token
#   else: mint new one, store with same shape as github_auth_exchange
#
# Route location: add before Mount("/") in the routes list
# Also: patch whoami_endpoint to include session_endpoint key
#
# AuthPanel PATH E:
#   - Add trySessionEndpoint() async before PATH D cookie check
#   - If returns true, skip rest of flow
#   - Non-blocking: if 401/network error, fall through silently
#   - Must be first check in useEffect (before cookie check)
#
# Pair.retrofuture.tech OAuth investigation:
#   - /auth/check already exists (token validation → X-Forwarded-User header)
#   - /auth/exchange already exists (GitHub code → session token)
#   - /auth/callback already exists (GitHub redirect → cookie + redirect /)
#   - /whoami already exists (token → user identity)
#   - pair.retrofuture.tech likely uses same OAuth dance via Caddy forward_auth
#   - Need to check if Caddyfile or docker-compose wires pair.* differently

```
