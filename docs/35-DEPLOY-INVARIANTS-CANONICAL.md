# 35 — DEPLOY INVARIANTS (CANONICAL)

**Status:** canonical
**Last updated:** 2026-05-21
**Owners:** infrastructure / deploy
**See also:** [30-CADDY-PROXY-TOPOLOGY-CANONICAL.md](./30-CADDY-PROXY-TOPOLOGY-CANONICAL.md)
· `.openhands/skills/vps-deploy` (operator runbook)

---

## 1. The Deploy Contract

After every successful `redeploy.sh` run (or every successful CI deploy via
`.github/workflows/deploy.yml`), **the following statements MUST be true**.
If any are false, the deploy did not succeed regardless of what the logs say.

The contract is declared in machine-readable form at
`deploy/scripts/baseline_expected.json`. The script enforces it; this
document is the prose explanation. **The JSON is the single source of
truth; this doc reflects it.**

The contract is split into four bands, from cheapest to most expensive:

1. **Pre-flight invariants** — static, readable from disk + DNS only.
2. **Post-build invariants** — image freshness + container health, local to the VPS.
3. **Public endpoint invariants** — HTTP status codes + JSON shape from the public internet.
4. **Container health invariants** — Docker reports each named container as `healthy`.

Bands 1 + 2 catch the most expensive failure modes (silent cache builds,
clobbered `.env`) before they reach production. Bands 3 + 4 catch
regressions in routing, OAuth wiring, and runtime crashes.

---

## 2. Pre-flight invariants

Run by `deploy/scripts/preflight.sh`. Exits **4** on any failure
(distinct from redeploy's 1/2/3 so the cause is obvious in CI logs).

| Invariant | Failure mode it blocks |
| --- | --- |
| `.env` exists on disk and is ≥100 bytes | "`.env` clobbered by `git pull`" (ec0f6008 was the last instance) |
| Required env vars populated (`OPENROUTER_API_KEY`, `GITHUB_CLIENT_ID/SECRET/REDIRECT_URI`, `SWARMY_MCP_TOKEN`, `HUSTLE_BASIC_AUTH_HASH`) | Caddy boot-loops on empty `basic_auth`, MCP boots without OAuth |
| `docker compose config --quiet` passes | Compose syntax breakage caught before `down`/`up` |
| `caddy validate` passes on the on-disk Caddyfile | "Caddy crash-looped on empty basic_auth" class of bug |
| DNS resolves the three public hosts to the expected VPS IP | Deploy to wrong host / DNS propagation gaps |
| Disk ≥5 GB free | Build failures mid-`--no-cache` rebuild |
| `GITHUB_REDIRECT_URI` ends in `/auth/callback` | OAuth callback 404 |

`preflight.sh` is read-only (no docker actions, no git mutations). Safe to
run as often as you like.

---

## 3. Post-build invariants

Verified by `redeploy.sh` between the `build` and `restart` phases.

### Image-freshness check (Phase 4.5)

For each rebuilt service, the script compares the resulting image's
`CreatedAt` timestamp to the build start timestamp. If the image is
older than build start, the build silently re-used cache layers despite
`--no-cache --pull`. Script exits **2** with the diagnostic:

```bash
docker rmi -f $(docker images -q --filter reference='*<service>*')
bash deploy/scripts/redeploy.sh   # retry
```

This is the codified fix for "rebuilt mcp-server but tool count still 55."

### Container health

`docker inspect --format='{{.State.Health.Status}}' swarmy-mcp` must
report `healthy` within 90 s (18 × 5 s poll). Failure prints the last
30 lines of `mcp-server` logs and exits 3.

---

## 4. Public endpoint invariants

Every endpoint in `baseline_expected.json#/endpoints` must return its
declared status code. Endpoints can additionally assert a JSON field
value (`expect_json_field` + `expect_json_value`).

| URL | Expect | Why this is the SUCCESS signal |
| --- | --- | --- |
| `https://swarmy.retrofuture.tech/health` | 200 + JSON `{status:"healthy"}` | MCP responding and reports itself healthy |
| `https://api.retrofuture.tech/health` | 200 | chat-mvp proxy path is alive |
| `https://retrofuture.tech/` | **401** | basic_auth gate active — 401 means the gate is wired, NOT that the site is broken |
| `https://swarmy.retrofuture.tech/auth/callback?code=TEST` | **302** | OAuth callback alive; 404 here is a regression (see fix 98535c3e) |

The `mcp_tools_registered_min` invariant (currently 59) is asserted against
the JSON returned from `/health`. Bump it in `baseline_expected.json`
when adding new tools so a future cache-build can't silently regress
tool-count without failing the deploy.

---

## 5. How to add a new invariant

1. Edit `deploy/scripts/baseline_expected.json`:
   - For an endpoint, append to `endpoints[]`.
   - For a container, append to `containers_healthy[]`.
   - For pre-flight env vars or DNS hosts, edit the `preflight` block.
2. Run locally:
   ```bash
   bash deploy/scripts/preflight.sh                   # if pre-flight
   bash deploy/scripts/redeploy.sh --report-only      # if post-deploy
   ```
3. Commit with a 1-line rationale that names the failure mode the
   invariant prevents from recurring.

The verification loop in `redeploy.sh::invariant_check()` walks the JSON
generically, so no script changes are needed unless you're inventing a
new invariant *kind*.

---

## 6. Common false alarms and how the script handles them

| Symptom | Reason it's not a failure | Where it's encoded |
| --- | --- | --- |
| `retrofuture.tech/` returns 401 | `basic_auth` gate is intentionally guarding the dev/admin apex | `endpoints[2].expect_code = 401` |
| `/auth/callback` returns 302 instead of 200 | OAuth flow correctly redirects after consuming `?code=…` | `endpoints[3].expect_code = 302` |
| `mcp_tools_registered=59` (not 55) | Tool count grows over time; floor is `_min`, not equality | `mcp_tools_registered_min` |
| Container missing `Health.Status` | Some services intentionally run without a healthcheck — `running == true` is treated as a soft pass | invariant_check fallback |

If you see any of these reported as a hard failure, the invariant file
disagrees with reality — fix the JSON, not the script.

---

## 7. Recovery playbook (per failure mode)

| Failure | Recovery |
| --- | --- |
| **preflight exit 4 — `.env` missing or small** | Restore from `.env.example` + secret manager; never `git reset --hard` until preflight green |
| **preflight exit 4 — Caddyfile invalid** | `docker run --rm -v "$PWD/deploy/caddy/Caddyfile:/etc/caddy/Caddyfile:ro" caddy:2-alpine caddy validate --config /etc/caddy/Caddyfile` then fix |
| **redeploy exit 2 — image-freshness fail** | `docker rmi -f $(docker images -q --filter reference='*<service>*')` then rerun redeploy |
| **redeploy exit 3 — `/auth/callback` not 302** | Confirm `GITHUB_REDIRECT_URI` env var + check `oauth_router` registered in `server.py`; refer to fix 98535c3e |
| **redeploy exit 3 — `mcp_tools_registered < min`** | Check `mcp-server` logs for tool-registration ImportError; `--pull` flag should be present in build command |
| **redeploy exit 3 — apex returns 200 instead of 401** | basic_auth gate dropped from Caddyfile (regression); diff `deploy/caddy/Caddyfile` against last green deploy |
| **redeploy exit 3 — apex returns 502** | Caddy started before chat-mvp was healthy — verify `depends_on: chat-mvp.condition: service_healthy` still in docker-compose.yml |

---

## 8. Operator quick reference

```bash
# Local pre-deploy sanity (read-only):
bash deploy/scripts/preflight.sh

# Full deploy with all hardening:
bash deploy/scripts/redeploy.sh

# Just verify the contract (no build, no restart) — safe for cron:
bash deploy/scripts/redeploy.sh --report-only

# Bypass the preflight check (NOT recommended):
bash deploy/scripts/redeploy.sh --skip-preflight
```

GitHub Actions runs the contract automatically on every push to `main`
that touches a deploy-relevant path (see `.github/workflows/deploy.yml`).
Failed invariants fail the workflow.

---

## 9. Cross-references

- [`30-CADDY-PROXY-TOPOLOGY-CANONICAL.md`](./30-CADDY-PROXY-TOPOLOGY-CANONICAL.md) — Caddy route table; explains why the apex 401 is correct
- `deploy/scripts/baseline_expected.json` — machine-readable contract
- `deploy/scripts/preflight.sh` — pre-flight runner
- `deploy/scripts/redeploy.sh` — full pipeline + `--report-only` mode
- `.github/workflows/deploy.yml` — CI deploy + invariant verification
- `.openhands/skills/vps-deploy/SKILL.md` — operator runbook for SSH-driven manual deploys
