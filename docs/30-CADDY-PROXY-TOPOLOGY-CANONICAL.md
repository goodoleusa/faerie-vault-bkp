# 30 — Caddy + Docker Proxy Topology (CANONICAL)

> **Single source of truth** for every "where does X go?" question about the
> swarmy production stack. If a deploy 502s, an OAuth flow 404s, or you cannot
> remember whether to write `mcp-server` or `swarmy-mcp` in a Caddy directive —
> the answer is here.
>
> When this doc and a live config disagree, **the config wins and this doc is
> patched in the same commit**. Do not let the two drift.

---

## INDEX CARD — Read this first (single screen reference)

```
SWARMY PROXY ARCHITECTURE — INDEX CARD

Public entry:    0.0.0.0:443 → swarmy-caddy (TLS termination, Let's Encrypt)
Public entry:    0.0.0.0:80  → swarmy-caddy (HTTP→HTTPS 301 redirect)
QUIC/HTTP3:      0.0.0.0:443/udp → swarmy-caddy
Public domains:  retrofuture.tech (apex, basic_auth gated)
                 swarmy.* admin.* api.* faerie.* (production)
                 hustle-dev.* ct-dev.* vault-dev.* (basic_auth gated)

Backend host:    Use the docker compose SERVICE name in Caddyfile
                 (mcp-server:8080, NOT swarmy-mcp:8080)

Loopback only:   127.0.0.1:8080 → swarmy-mcp:8080 (watchdog + admin probes,
                 not exposed publicly)

To CHANGE a route:    edit deploy/caddy/Caddyfile → commit → git pull on VPS
                      → docker compose exec caddy caddy reload \
                          --config /etc/caddy/Caddyfile
To ADD a subdomain:   1. add A record (desec.io) FIRST
                      2. add site block in deploy/caddy/Caddyfile
                      3. pull + caddy reload (Let's Encrypt provisions on
                         first request)
To FIX a 502:         docker compose logs caddy --tail=20
                      (look for "dial tcp: lookup X on 127.0.0.11:53")
                      docker compose exec caddy caddy reload \
                          --config /etc/caddy/Caddyfile
To FIX OAuth 404:     FORCE_ALL=1 bash deploy/scripts/redeploy.sh
                      (forces mcp-server rebuild so /auth/callback ships)
```

---

## 1. The complete port map

### 1.1 ASCII diagram — full traffic flow

```
                    ┌────────────────────────────────────────┐
                    │   Public Internet (browser, GitHub OAuth,  │
                    │   curl, monitoring probes, bot scanners)   │
                    └────────────────┬───────────────────────┘
                                     │
                                     ▼  DNS A record:
                                     │  *.retrofuture.tech → 142.93.155.167
                                     │
                       ┌─────────────┴──────────────┐
                       │     VPS host (Droplet)     │
                       │     142.93.155.167         │
                       │                            │
                       │  iptables / ufw            │
                       │  allows :80 :443/tcp+udp   │
                       └─────────────┬──────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        ▼                        │
            │ 0.0.0.0:80     ┌──────────────────┐    0.0.0.0:443  │
            │  ─────────────►│                  │◄────────────── │
            │                │   swarmy-caddy   │   :443/udp     │
            │ (HTTP redirect)│   (caddy:2-alpine)│  (QUIC/HTTP3) │
            │                │                  │                │
            │ 127.0.0.1:8080 │  TLS termination │                │
            │  ─(loopback)─► │  Let's Encrypt   │                │
            │  swarmy-mcp:   │  ZeroSSL fallback│                │
            │   8080         │                  │                │
            │ (watchdog)     └────────┬─────────┘                │
            │                         │                          │
            │            ┌────────────┴────────────┐             │
            │            │   docker network        │             │
            │            │   swarmy-net (bridge)   │             │
            │            │   embedded DNS 127.0.0.11│            │
            │            └────────────┬────────────┘             │
            │                         │                          │
            │ ┌───────────────────────┼───────────────────────┐  │
            │ ▼              ▼        ▼         ▼        ▼    ▼  │
            │ mcp-server   chat-mvp  hustle  cybertemplate  openhands
            │ :8080         :3000    :80       :4321         :3000
            │ (swarmy-mcp) (swarmy- (swarmy- (swarmy-       (swarmy-
            │              chat-mvp) hustle) cybertemplate) openhands)
            │
            │ swarmy-vault    watchdog          vault-b2-sync
            │ :3000           (no listen,        (no listen,
            │ (swarmy-vault)  egress only)       egress only)
            └────────────────────────────────────────────────────┘

LEGEND
  service:port    → compose service NAME (what Caddy must use as upstream)
  (container)     → container_name (what docker ps shows; do NOT use in Caddy)
```

### 1.2 Port mapping table

| Layer | Direction | Source | Target | Mechanism | Why it exists |
|---|---|---|---|---|---|
| Host:Port | inbound | `0.0.0.0:443/tcp` | swarmy-caddy | `ports:` in docker-compose | TLS termination, public HTTPS |
| Host:Port | inbound | `0.0.0.0:443/udp` | swarmy-caddy | `ports:` in docker-compose | HTTP/3 (QUIC) |
| Host:Port | inbound | `0.0.0.0:80/tcp`  | swarmy-caddy | `ports:` in docker-compose | HTTP→HTTPS 301 redirect block |
| Host:Port | loopback | `127.0.0.1:8080`  | swarmy-mcp:8080 | `ports: 127.0.0.1:8080->8080/tcp` | Local watchdog/admin probes; **not public** |
| Docker net | container→container | swarmy-caddy | `mcp-server:8080` | Caddy `reverse_proxy mcp-server:8080` | `/api/*`, `/auth/*`, `/mcp/*`, `/health` on swarmy + admin + api hosts |
| Docker net | container→container | swarmy-caddy | `chat-mvp:3000`  | Caddy `reverse_proxy chat-mvp:3000` | SPA serving for swarmy + admin |
| Docker net | container→container | swarmy-caddy | `hustle:80`      | Caddy `reverse_proxy hustle:80` | Static landing on apex + hustle-dev |
| Docker net | container→container | swarmy-caddy | `openhands:3000` | Caddy `reverse_proxy /oh/* openhands:3000` | IDE access via /oh prefix |
| Docker net | container→container | swarmy-caddy | `cybertemplate:80` (note: actual expose is `:4321` in HMR mode — Caddyfile currently writes `:80`; see §8 anti-patterns) | Caddy `reverse_proxy cybertemplate:80` | Dev static site on ct-dev |
| Docker net | container→container | swarmy-caddy | `swarmy-vault:3000` | Caddy `reverse_proxy swarmy-vault:3000` | Obsidian KasmVNC UI on vault-dev |
| Docker net | sidecar | swarmy-watchdog | `mcp-server:8080/health` | curl loop in entrypoint | Self-healing health probe |
| Docker net | sidecar (egress) | vault-b2-sync | `api.backblazeb2.com:443` | rclone copy | WORM backup; no inbound listen |

**Why this is the only place ports appear in the stack:** only `mcp-server`
and `caddy` declare host-level `ports:` mappings. Every other service uses
`expose:` (container-network-only). That means **only Caddy and the watchdog
talk to backends**, and the only host-reachable backend port is the
loopback-bound `127.0.0.1:8080` for local tooling.

---

## 2. Service-name vs container_name DNS (critical, often confused)

Docker Compose uses the **service name** (top-level key in
`docker-compose.yml`) as the in-network DNS hostname. The
`container_name:` field is purely cosmetic — it controls what
`docker ps` prints, nothing else.

```yaml
services:
  mcp-server:                       # ← this name IS the in-network DNS hostname
    container_name: swarmy-mcp      # ← this is just the container's display name
                                    #    (docker ps, docker exec)
```

**Caddy upstreams MUST use the service name, not the container_name.**

```caddyfile
# CORRECT — resolves via swarmy-net embedded DNS (127.0.0.11)
reverse_proxy mcp-server:8080

# WRONG — Caddy will log: "dial tcp: lookup swarmy-mcp on 127.0.0.11:53: no such host"
reverse_proxy swarmy-mcp:8080
```

### 2.1 Service → container_name → Caddy upstream map

| Compose service name | container_name | Caddy upstream | Internal port |
|---|---|---|---|
| `mcp-server`     | `swarmy-mcp`         | `mcp-server:8080`    | 8080 |
| `chat-mvp`       | `swarmy-chat-mvp`    | `chat-mvp:3000`      | 3000 |
| `openhands`      | `swarmy-openhands`   | `openhands:3000`     | 3000 |
| `hustle`         | `swarmy-hustle`      | `hustle:80`          | 80 |
| `cybertemplate`  | `swarmy-cybertemplate` | `cybertemplate:80` (see §8) | 4321 (HMR) / 80 (static) |
| `swarmy-vault`   | `swarmy-vault`       | `swarmy-vault:3000`  | 3000 |
| `vault-b2-sync`  | `swarmy-vault-b2-sync` | — (no listener)    | — |
| `watchdog`       | `swarmy-watchdog`    | — (no listener; client only) | — |
| `caddy`          | `swarmy-caddy`       | — (it IS the proxy) | 80/443 |

**Diagnostic commands when in doubt:**

```bash
# List compose SERVICE names — these are the DNS hostnames Caddy uses
docker compose config --services

# List container_names — these are what docker ps prints
docker ps --format '{{.Names}}'

# Test in-network DNS resolution from inside caddy:
docker compose exec caddy nslookup mcp-server
# → Should resolve via 127.0.0.11 to the mcp-server container's IP

# Show Caddy's view of the upstream
docker compose exec caddy wget -qO- http://mcp-server:8080/health
```

---

## 3. Per-subdomain routing trace

Every public hostname, in the order it appears in `deploy/caddy/Caddyfile`.

### 3.1 `retrofuture.tech` / `www.retrofuture.tech` — landing (basic_auth gated)

Path: browser → DNS → VPS:443 → swarmy-caddy → site block.

```
retrofuture.tech, www.retrofuture.tech {
  import security_headers
  import deny_sensitive
  @www host www.retrofuture.tech
  redir @www https://retrofuture.tech{uri} permanent
  basic_auth {
    {$HUSTLE_BASIC_AUTH_USER} {$HUSTLE_BASIC_AUTH_HASH}
  }
  reverse_proxy hustle:80 {
    header_up Host {host}
    header_up X-Real-IP {remote_host}
  }
}
```

Flow:

1. Client GET `https://retrofuture.tech/`
2. Caddy applies `security_headers` (HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, strip `Server` header)
3. Caddy applies `deny_sensitive` (`.env*`, `.git/*`, `forensics/*`, `scripts/*`, `.openhands/*`, `node_modules/*`, `.venv/*` → 404)
4. If host is `www.*`, 301 to apex
5. `basic_auth` challenges (user/hash from `HUSTLE_BASIC_AUTH_USER` / `HUSTLE_BASIC_AUTH_HASH` in `.env`)
6. On auth success, reverse-proxy to `hustle:80` (which is a caddy:2-alpine running `caddy file-server` on a bind-mounted built `dist/`)
7. Log to `/var/log/caddy/landing.log` (rolled 10MB × 5)

**Historical fix:** Was `landing:80` before commit `c12ee172`; that name did
not exist as a compose service, so Caddy returned `dial tcp: lookup landing`.
Fixed by aligning Caddyfile to the real service name `hustle`.

### 3.2 `swarmy.retrofuture.tech` — chat-mvp + MCP back-channels

This is the **user front door**. Five handle blocks; order matters because
Caddy evaluates `handle` / `handle_path` matchers before the catch-all.

| Path prefix | Backend | Notes |
|---|---|---|
| `/auth/*`   | `mcp-server:8080` | GitHub OAuth callback (MUST exist for login flow) |
| `/api/*`    | `mcp-server:8080` | `handle_path` strips the `/api` prefix |
| `/mcp/*`    | `mcp-server:8080` | Preserves prefix (OH SDK chat panel needs `/mcp/`) |
| `/oh/*`     | `openhands:3000`  | OpenHands IDE access |
| `/health`   | `mcp-server:8080` | Public health probe |
| anything else | `chat-mvp:3000` | React SPA + assets |

Annotated flow for a typical SPA request:

```
client GET https://swarmy.retrofuture.tech/dashboard
  → DNS A record → 142.93.155.167:443
  → swarmy-caddy (TLS handshake, ACME-managed cert)
  → site block "swarmy.retrofuture.tech"
  → import security_headers (adds 5 headers, strips Server)
  → import deny_sensitive (no match)
  → handle /auth/*    — does not match
  → handle_path /api/* — does not match
  → reverse_proxy /mcp/* — does not match
  → reverse_proxy /oh/*  — does not match
  → handle /health  — does not match
  → catch-all reverse_proxy chat-mvp:3000
    → header_up Host {host}              (preserves swarmy.retrofuture.tech)
    → header_up X-Real-IP {remote_host}
    → header_up X-Forwarded-For {remote_host}
    → header_up X-Forwarded-Proto {scheme}  (always "https" — Caddy did TLS)
    → transport http read_timeout 300s
  → chat-mvp internal Caddy (deploy/chat-mvp/Caddyfile) serves /app/dist
    with try_files {path} /index.html fallback (SPA client-side routing)
  → response 200, returned through Caddy back to client (TLS re-encrypted)
```

Annotated flow for an API request:

```
client POST https://swarmy.retrofuture.tech/api/tools/swarmy_health
  → site block → handle_path /api/*
  → URI rewritten to /tools/swarmy_health (handle_path strips /api)
  → reverse_proxy mcp-server:8080
  → MCP Starlette route Route("/tools/{name}", rest_tool_endpoint, ["POST"])
  → returns JSON, back through Caddy → client
```

### 3.3 `admin.retrofuture.tech` — admin tab (same chat-mvp container)

Identical routing to `swarmy.*` but **without** the `/oh/*` handler and
**without** explicit `/health`. The Caddyfile re-declares the site block
because Caddy does not allow `handle` blocks to span sites — the duplication
is intentional and forgivable.

Key insight: `admin.*` does **not** point at a separate container. It
serves the same `chat-mvp:3000` SPA; the SPA itself reads `window.location`
and toggles the Admin Ops tab when the hostname matches `admin.*`.

### 3.4 `api.retrofuture.tech` — MCP direct (no SPA, no auth proxy)

```
api.retrofuture.tech {
  import security_headers
  import deny_sensitive
  handle /health { reverse_proxy mcp-server:8080 }
  @blocked path /docs* /openapi.json /redoc*
  respond @blocked 404
  handle { reverse_proxy mcp-server:8080 ... }
}
```

Flow:

1. Public `/docs*`, `/openapi.json`, `/redoc*` are **explicitly 404'd** (FastAPI auto-docs are not exposed in production).
2. `/health` is exempt from any auth check.
3. Everything else goes straight to `mcp-server:8080`. Authentication is enforced **inside the MCP server**, not by Caddy — clients send `Authorization: Bearer <SWARMY_MCP_TOKEN>` and the MCP middleware checks it.

### 3.5 `faerie.retrofuture.tech` — 301 alias

```
faerie.retrofuture.tech {
  redir https://swarmy.retrofuture.tech{uri} permanent
}
```

Pure permanent redirect, preserves URI. Exists because the project was
renamed `faerie → swarmy` (commit `ee546557`) and external links may still
reference the old hostname.

### 3.6 `hustle-dev.retrofuture.tech` — hustle static behind basic_auth

Same as apex but **without** the `deny_sensitive` import (intentionally —
hustle-dev exposes the raw dev build for testing). basic_auth uses the
same `HUSTLE_BASIC_AUTH_*` vars.

### 3.7 `ct-dev.retrofuture.tech` — cybertemplate dev (HMR)

```
ct-dev.retrofuture.tech {
  import security_headers
  basic_auth { {$CT_BASIC_AUTH_USER} {$CT_BASIC_AUTH_HASH} }
  reverse_proxy cybertemplate:80 { header_up Host {host} }
}
```

**Note:** the `cybertemplate` service in compose actually exposes port
`4321` (Astro dev server), not `80`. The Caddyfile shipping `:80` only
works if you flip the container to static mode (commented-out fallback
`CT_DEV_MODE=static`). For live HMR mode, the Caddyfile must point at
`:4321` — see §8 anti-patterns for the open drift.

### 3.8 `vault-dev.retrofuture.tech` — Obsidian browser UI

```
vault-dev.retrofuture.tech {
  import security_headers
  basic_auth { {$VAULT_BASIC_AUTH_USER} {$VAULT_BASIC_AUTH_HASH} }
  reverse_proxy swarmy-vault:3000 {
    header_up Host {host}
    transport http { read_timeout 600s }
  }
}
```

`swarmy-vault` runs `lscr.io/linuxserver/obsidian` — Obsidian inside
KasmVNC, served as HTML over port 3000. The 600s `read_timeout` is
critical: KasmVNC keeps long-poll connections open.

### 3.9 `:80` — global HTTP→HTTPS redirect

```
:80 {
  redir https://{host}{uri} permanent
}
```

This is the **lowest-priority** site block. Any HTTP request to any
hostname that did not match a more specific block (e.g., raw IP access,
unknown hostnames) gets 301'd to HTTPS.

### 3.10 Dynamic vault routes — `import /etc/caddy/vaults/*.caddy`

Provisioned per-customer by `07-provision-vault.sh`. Each file adds a
new site block (typically `{customer}.retrofuture.tech` → a customer's
own vault container). Not covered in detail here; see the provisioning
script for the template.

---

## 4. The OAuth flow (because it's been broken multiple times)

Full GitHub OAuth round-trip. Annotated with failure modes.

```
 ┌─────────────┐                                                   ┌──────────┐
 │   Browser   │                                                   │  GitHub  │
 │  (chat-mvp) │                                                   │  OAuth   │
 └──────┬──────┘                                                   └────┬─────┘
        │                                                               │
        │ (1) user clicks "Login with GitHub" in SPA                    │
        ├──────────────────────────────────────────────────────────────►│
        │     GET https://github.com/login/oauth/authorize              │
        │       ?client_id=<GITHUB_CLIENT_ID>                           │
        │       &redirect_uri=https://swarmy.retrofuture.tech/auth/callback
        │       &scope=read:user                                        │
        │                                                               │
        │ (2) GitHub shows consent screen, user clicks "Authorize"      │
        │◄──────────────────────────────────────────────────────────────│
        │     302 Location: https://swarmy.retrofuture.tech/auth/callback?code=XXX
        │                                                               │
        │ (3) Browser follows redirect (GET with ?code=XXX)             │
        │                                                               │
        ▼                                                               │
 ┌─────────────┐                                                        │
 │  swarmy-    │  (4) Caddy site block "swarmy.retrofuture.tech":       │
 │  caddy      │      handle /auth/* matches FIRST (before catch-all)   │
 │             │      reverse_proxy mcp-server:8080                     │
 └──────┬──────┘                                                        │
        │                                                               │
        ▼                                                               │
 ┌─────────────┐                                                        │
 │ swarmy-mcp  │  (5) Starlette Route("/auth/github", github_auth_redirect)
 │  :8080      │      — note: real callback handler is /auth/exchange   │
 │             │        OR /auth/callback depending on flow version.    │
 │             │        Both must exist on the mcp-server image.        │
 │             │  (6) Server-side exchange: POST to                     │
 │             │      https://github.com/login/oauth/access_token       │
 │             │      with client_id, client_secret, code               │
 ├─────────────┼──────────────────────────────────────────────────────►│
        │      │                                                       │
        │      │  (7) GitHub returns access_token                       │
        │      │◄──────────────────────────────────────────────────────│
        │      │  (8) MCP fetches /user, checks GITHUB_ALLOWED_USERS    │
        │      │  (9) Mints swarmy_session cookie + JWT                 │
        │      │  (10) 302 redirect to /#token=<jwt>                    │
        │◄─────┘                                                        │
        │  back through Caddy with Set-Cookie + Location header          │
        │                                                               │
 ┌──────┴──────┐                                                        │
 │   Browser   │  (11) chat-mvp SPA reads #token=…, stores in           │
 │  (chat-mvp) │       localStorage, includes Authorization: Bearer …   │
 │             │       on every subsequent /api/* call                  │
 └─────────────┘                                                        │
```

### 4.1 OAuth failure mode legend

| Symptom | Root cause | Fix |
|---|---|---|
| "The redirect_uri is not associated with this application" | `GITHUB_REDIRECT_URI` in `.env` does not exactly match what is configured in the GitHub OAuth App settings | Update one or the other so they match exactly (scheme, host, path — no trailing slash drift) |
| 404 on `/auth/callback` from Caddy | Caddyfile is missing `handle /auth/*` block, or this Caddyfile shipped but Caddy never reloaded | `docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile` |
| 404 on `/auth/callback` from MCP (with Caddy logs showing the proxy succeeded) | `mcp-server` image is **older** than the `server.py` source — the route was added to source but never rebuilt | `FORCE_ALL=1 bash deploy/scripts/redeploy.sh` (rebuilds with `--no-cache`) |
| "GitHub auth failed: bad credentials" | `GITHUB_CLIENT_SECRET` in `.env` is wrong / rotated | Regenerate in GitHub OAuth App settings, paste new value, restart mcp-server |
| Login succeeds but immediate 403 on first /api/* call | User's GitHub handle is not in `GITHUB_ALLOWED_USERS` (comma-separated allowlist) | Add the handle to `.env`, `docker compose up -d mcp-server` |
| Login loops infinitely | `swarmy_session` cookie not being set; usually `Set-Cookie` stripped by a missing `header_up` or domain mismatch | Verify `header_up Host {host}` is set on the `/auth/*` proxy block |

---

## 5. Common failure modes with diagnostic ladder

| Symptom | Most likely root cause | Diagnose with | Fix |
|---|---|---|---|
| 502 Bad Gateway from edge; containers report healthy | Caddy is holding stale config OR a `reverse_proxy` hostname is not a real compose service | `docker compose logs caddy --tail=20` (look for `dial tcp: lookup X on 127.0.0.11:53: no such host`) | Reload Caddy: `docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile`. If error persists, fix the hostname in Caddyfile to match `docker compose config --services` output |
| SSL error / "unknown subdomain" / ACME failure | DNS A record missing OR subdomain not in Caddyfile | `dig +short <sub>.retrofuture.tech` then `grep <sub> deploy/caddy/Caddyfile` | Add the A record at desec.io first; wait for propagation (≤60s); then ensure Caddyfile has a site block; then `caddy reload` |
| 401 Unauthorized on `retrofuture.tech` apex | `basic_auth` gate is intentionally active until public launch | `curl -fsS https://retrofuture.tech` returns 401 | Authenticate: `curl -u dev:changeme https://retrofuture.tech` (or whatever `HUSTLE_BASIC_AUTH_USER/HASH` were set to) |
| 404 on `/auth/callback` after deploy | mcp-server image is older than `server.py` source | `docker inspect swarmy-mcp \| grep -i created` then compare to `stat deploy/mcp-server/server.py` | `docker compose build --no-cache mcp-server && docker compose up -d --force-recreate mcp-server` — or just `FORCE_ALL=1 bash deploy/scripts/redeploy.sh` |
| Caddy refuses to start; logs show "no actor available for site" or empty basic_auth user | basic_auth env vars empty in `.env` (Caddy refuses to load an empty `basic_auth` directive) | `grep BASIC_AUTH .env` shows blank values | Run `bash deploy/scripts/fix-caddy-basic-auth.sh` OR manually generate a hash: `docker exec swarmy-caddy caddy hash-password --plaintext 'yourpass'` and paste into `.env` |
| `/@fs/.env` probes 502 in logs (or 404) | Bot scanning for Vite dev-server SSRF vulnerabilities; harmless noise | Caddy access logs show repeated `/@fs/.env*` requests from rotating IPs | `deny_sensitive` already returns 404 for `/.env*` — these are safely rejected. Optionally extend `(deny_sensitive)` with `/@fs/*` |
| Container name unresolved in Caddy | Used `container_name` in Caddyfile instead of compose service name | `docker compose config --services` shows the correct service name | Update Caddyfile to use service name (e.g., `mcp-server` not `swarmy-mcp`) + reload |
| Tool count low (<50) after deploy | mcp-server didn't rebuild — running an old image | `curl https://swarmy.retrofuture.tech/health \| jq .mcp_tools_registered` | `FORCE_ALL=1 bash deploy/scripts/redeploy.sh` |
| Let's Encrypt rate limit hit | Too many failed cert provisioning attempts in a short window (usually because A records were not in place when Caddy tried to provision) | `docker compose logs caddy \| grep -i "rate limit"` | Wait the rate-limit window (typically 1 hour for failed validations, 1 week for issuance per name) — Caddy will retry automatically with exponential backoff |
| QUIC/HTTP3 not working | UDP 443 not opened on host firewall | `sudo ufw status \| grep 443` should show `443/udp ALLOW` | `sudo ufw allow 443/udp` — TCP fallback still works without this, but newer browsers prefer HTTP/3 |
| Watchdog flapping (sentinel written every 2 min) | mcp-server is alive but `/health` is slow or intermittently failing | `tail -f forensics/system/watchdog.log` | Check mcp-server logs for slow imports or DB connection retries; bump healthcheck `timeout:` in compose if it's a known cold-start issue |

---

## 6. The 0/1/2 confusion (compose vs container vs Caddy)

The same service is represented **three different ways** depending on context.
This is the single largest source of confusion when editing the stack.

| Identity | Where it appears | Examples |
|---|---|---|
| **Compose service name** (canonical, in-network DNS) | • Top-level key in `docker-compose.yml`<br>• What `docker compose <cmd> <service>` takes<br>• What other containers use as a hostname<br>• What `Caddyfile` `reverse_proxy` MUST use | `mcp-server`, `chat-mvp`, `caddy`, `hustle`, `openhands`, `cybertemplate`, `swarmy-vault`, `vault-b2-sync`, `watchdog` |
| **container_name** (display only) | • `container_name:` in compose<br>• `docker ps` output<br>• `docker exec <container_name> …` commands<br>• `docker logs <container_name>` | `swarmy-mcp`, `swarmy-chat-mvp`, `swarmy-caddy`, `swarmy-hustle`, `swarmy-openhands`, `swarmy-cybertemplate`, `swarmy-vault`, `swarmy-vault-b2-sync`, `swarmy-watchdog` |
| **Caddyfile upstream** (always service:port) | `reverse_proxy SERVICE:PORT` directive in `deploy/caddy/Caddyfile` | `mcp-server:8080`, `chat-mvp:3000`, `hustle:80`, `openhands:3000`, `cybertemplate:80`, `swarmy-vault:3000` |

The only place these three names coincide is `swarmy-vault` (service name
happens to equal container_name). Everywhere else, the prefix `swarmy-`
appears **only** on container_names. **If you see `swarmy-foo` in a
Caddyfile, it's wrong** unless `foo` is literally the service name (only
`swarmy-vault` qualifies).

---

## 7. Bot-probe noise legend

Caddy access logs will show constant probe traffic. None of it is a real
threat to this stack, but knowing the shape helps separate noise from signal.

| Pattern | What it's looking for | Current Caddy response | Action |
|---|---|---|---|
| `/@fs/.env*`, `/@fs/etc/passwd` | Vite dev-server SSRF (CVE-2025-30208) | 404 via catch-all (no Vite in prod) or 404 via `deny_sensitive` | Ignore. Optionally add `/@fs/*` to the `(deny_sensitive)` snippet to short-circuit earlier |
| `/.env`, `/config/.env`, `/secrets.yml`, `/credentials.yml.enc`, `/appsettings.json` | Generic config-file scanning | 404 via `deny_sensitive` (matches `/.env*`) | Ignore. Extend `deny_sensitive` if new patterns recur |
| `/etc/passwd`, `/.git/config`, `/.git/HEAD` | LFI / source-leak attempts | 404 via `deny_sensitive` (`/.git/*`) | Ignore |
| `/wp-login.php`, `/admin/`, `/phpmyadmin/`, `/xmlrpc.php` | WordPress / phpMyAdmin scanning | 404 from chat-mvp SPA fallback (no such route, falls through to `index.html`) | Ignore — could optionally add `respond /wp-* 404` to short-circuit |
| `/robots.txt`, `/sitemap.xml`, `/.well-known/security.txt` | Legitimate crawlers (Google, GPTBot, OpenAI SearchBot, Bingbot) | 404 currently (no robots.txt shipped) | Optional: ship a `robots.txt` from chat-mvp's public dir to opt in / out of indexing |
| `/.well-known/acme-challenge/*` | Let's Encrypt HTTP-01 validation | Handled by Caddy's ACME machinery (not visible to site blocks) | Never block this path |
| `/api/.env`, `/api/v1/users` | API endpoint enumeration | 404 from MCP (no such tool/route) or 401 if auth-gated | Ignore |

**Rule of thumb:** if a probe pattern recurs from the same prefix more
than 100 times/day, extend `(deny_sensitive)`. Otherwise let the catch-all
404 absorb it.

---

## 8. Hard rules / anti-patterns

```
✗ NEVER reverse_proxy to a container_name. Always use the compose service name.
  WRONG:  reverse_proxy swarmy-mcp:8080
  RIGHT:  reverse_proxy mcp-server:8080

✗ NEVER put bcrypt hashes in .env without escaping $ to $$ for
  docker-compose interpolation.
  WRONG:  HUSTLE_BASIC_AUTH_HASH=$2a$14$abc...
  RIGHT:  HUSTLE_BASIC_AUTH_HASH=$$2a$$14$$abc...
  (Caddy reads via env_file: + environment: which double-interpolates.
   When in doubt: docker exec swarmy-caddy caddy hash-password ...
   then paste with $ doubled if compose interpolation chews them.)

✗ NEVER restart Caddy with `docker compose restart caddy` when a reload works.
  WRONG:  docker compose restart caddy   (loses in-flight requests, may re-ACME)
  RIGHT:  docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
  (Reload is zero-downtime, preserves cert state, validates config first.)

✗ NEVER edit Caddyfile manually on the VPS.
  WHY:    The repo is git-pulled by the deploy job; manual edits get
          clobbered on the next deploy with no warning.
  RIGHT:  Edit locally → commit → push → CI/CD pulls on VPS → caddy reload.

✗ NEVER add a new subdomain to the Caddyfile without first adding the DNS
  A record.
  WHY:    Caddy will try to provision a Let's Encrypt cert on first request.
          If the A record does not resolve to this VPS, validation fails and
          you can hit rate limits (5 failures/hour per name).
  RIGHT:  desec.io add A record → wait for propagation (`dig +short`) →
          THEN add the Caddyfile block → reload.

✗ NEVER reference an env var in the Caddyfile without setting it in .env.
  WHY:    Caddy refuses to load a basic_auth block where user OR hash is
          empty. The whole config fails to parse and Caddy exits.
  RIGHT:  Set every {$VAR} referenced in Caddyfile in .env before reload.
          If you don't want a basic_auth gate active, comment the whole
          block out — do NOT leave it with empty vars.

✗ NEVER expose mcp-server on a public host port.
  WHY:    All auth is at the application layer; binding mcp-server to
          0.0.0.0:8080 means anyone on the internet can hit it directly
          without going through Caddy's TLS termination or any IP/rate
          policy you might add to Caddy later.
  RIGHT:  Keep the compose mapping as 127.0.0.1:8080:8080 (loopback only).
          Public traffic comes through api.retrofuture.tech via Caddy.

✗ NEVER mount the docker socket into a container that runs untrusted code
  (e.g., the watchdog). The current watchdog writes a sentinel file
  intentionally instead of calling docker.sock — preserve that pattern.

✗ NEVER assume container restart order. Caddy depends_on every backend
  (see compose), but Caddy still has to retry on first boot because
  depends_on does not wait for health, only for "started". If you add a
  new backend, add it to caddy's depends_on list AND keep retries on
  reverse_proxy enabled (Caddy default is lb_try_duration which works
  out of the box).
```

### 8.1 Known drift (open items, do not silently fix without verifying)

- **cybertemplate port mismatch:** Caddyfile writes `cybertemplate:80`, but the compose service exposes `:4321` in HMR mode (current default). Either flip the Caddyfile to `:4321` (live HMR over the public subdomain — risky, exposes dev server publicly behind basic_auth) or flip the compose service back to the static caddy file-server on `:80`. Decide intentionally; do not just patch one side.
- **Watchdog cannot restart mcp-server directly** (by design, no docker socket). Self-healing relies on Docker Engine's `restart: unless-stopped` on the mcp-server container itself; the watchdog only provides visibility (sentinel file at `forensics/system/watchdog.log`). If you want active restart, add a separate host-level cron that reads the sentinel.

---

## 9. Quick verification commands

After any change to Caddyfile or compose, run this checklist:

```bash
# 1. Validate Caddyfile syntax BEFORE reloading
docker compose exec caddy caddy validate --config /etc/caddy/Caddyfile

# 2. Reload (zero-downtime)
docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile

# 3. Probe every public hostname (expect 200 or 401 for basic_auth gated)
for host in retrofuture.tech swarmy.retrofuture.tech admin.retrofuture.tech \
            api.retrofuture.tech faerie.retrofuture.tech \
            hustle-dev.retrofuture.tech ct-dev.retrofuture.tech \
            vault-dev.retrofuture.tech; do
  printf '%-40s  ' "$host"
  curl -fsSI -o /dev/null -w '%{http_code}\n' "https://$host/" || echo "FAIL"
done

# 4. Verify OAuth callback route exists on mcp-server image
curl -fsSI https://swarmy.retrofuture.tech/auth/check | head -1
# → expect HTTP/2 200 or HTTP/2 401 (NOT 404 — 404 means route missing)

# 5. Verify tool count (sanity-check mcp-server image is current)
curl -fsS https://swarmy.retrofuture.tech/health | jq .mcp_tools_registered
# → expect ≥50 as of 2026-05-20

# 6. Check Caddy access log for last 20 lines (look for stray 502s)
docker compose logs caddy --tail=20 | grep -E 'status=(5[0-9]{2}|404)' || \
  echo "no recent errors"
```

---

## 10. Where to look when this doc is wrong

If a routing question is not answered here, the canonical sources are:

| Source | What it is |
|---|---|
| `deploy/caddy/Caddyfile`              | Live multi-subdomain config (production source of truth for routing) |
| `deploy/caddy/Caddyfile.retrofuture`  | Legacy / alternate config kept for reference; **not** the active file |
| `deploy/chat-mvp/Caddyfile`           | Internal Caddy inside the chat-mvp container (serves the React SPA at `:3000`, proxies `/api/*` to mcp-server, proxies `/oh/*` to openhands) |
| `deploy/chat-mvp/Caddyfile.prod`      | Production variant (if differing from the dev one) |
| `docker-compose.yml`                  | Service names, container_names, ports, exposes, networks, volumes |
| `deploy/mcp-server/server.py` ~L1798  | The Starlette `routes = [ … ]` block — every HTTP route MCP serves |
| `.env.example` / `deploy/.env.example`| All env var names the stack reads (auth, OAuth, B2, basic_auth hashes, public URLs) |
| `deploy/scripts/redeploy.sh`          | The canonical redeploy script (`FORCE_ALL=1` forces full rebuild) |
| `deploy/scripts/fix-caddy-basic-auth.sh` | Regenerates basic_auth hashes when env is blank |

Patch this doc in the **same commit** as any change to the above. Future-you
will thank you when the next 502 lands at 2 AM.
