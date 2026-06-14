> ⚠️ SUPERSEDED 2026-06-14 — This document describes the Syncthing Docker sidecar
> (heavy; NOT-YET-DEPLOYED; now abandoned). The canonical sync model is:
> **git-signed commits by the operator** (see `HOW-SYNC-WORKS.md § Operator Sync`).
> The VPS holds only the git-tracked markdown files; no Obsidian process on VPS.
> Thin debounced watcher (reckon chart/active/vault-authority-plane P3) replaces
> the Syncthing container entirely. This file is retained as historical reference only.

# Vault Sidecar Sync — Quick Reference

> **NOT-YET-DEPLOYED / HUMAN-GATED**. This file documents the opt-in Syncthing
> sidecar that lives in `reckon/deploy/vault-sidecar/`. It does NOT auto-start
> with the main reckon stack.

## What this is

A Syncthing sidecar container that bi-directionally syncs the vault between:

- **Side A (VPS)**: `/opt/reckon-vault` (or `RECKON_VAULT_PATH` on VPS)
  — same bind-mount the `openhands` container sees at `/workspace/faerie-vault`
- **Side B (operator)**: your laptop's local vault path (configured once via GUI)

Both sides see the same files. Edits in a live OH/Claude session appear in
Obsidian within seconds. Obsidian edits on your laptop appear in OH sessions
within seconds.

## Canonical docs

Full architecture, setup steps, and conflict model: `reckon/docs/165-VAULT-SIDECAR.md`

## Start / stop

```bash
# From reckon repo root on VPS:
docker compose \
  -f docker-compose.yml \
  -f deploy/vault-sidecar/docker-compose.yml \
  --profile vault-sync up -d vault-sidecar-syncthing

# Stop (does NOT affect main stack):
docker compose \
  -f docker-compose.yml \
  -f deploy/vault-sidecar/docker-compose.yml \
  --profile vault-sync down vault-sidecar-syncthing
```

## First-run pairing

1. SSH tunnel: `ssh -L 18384:127.0.0.1:18384 <your-vps>`
2. Open `http://localhost:18384`
3. Add your laptop as a remote device
4. Share the `faerie-vault` folder; accept on laptop
5. Watch both sides reach "Up to Date"

## Conflict model

Last-writer-wins per block. True conflicts produce a `.sync-conflict-YYYYMMDD-*.md`
sibling file. Review + delete the loser. The canonical forensic COC in
`reckon/forensics/` is NOT affected — vault edits are derivative artifacts.

## Files

- `reckon/deploy/vault-sidecar/docker-compose.yml` — the sidecar service
- `reckon/deploy/vault-sidecar/syncthing-config-stub.xml` — first-run config
- `reckon/deploy/vault-sidecar/.stignore` — ignore patterns (copy to vault root)
- `reckon/docs/165-VAULT-SIDECAR.md` — full architecture doc
