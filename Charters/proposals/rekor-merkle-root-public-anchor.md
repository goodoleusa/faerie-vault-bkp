---
type: charter
status: proposed
charter_id: rekor-merkle-root-public-anchor
mission_id: rekor.anchor.public
created: 2026-05-25
canonical_repo_path: "forensics/charters/proposals/2026-05-25Z__charter__rekor-merkle-root-public-anchor__goodoleusa.json"
filename_base: "2026-05-25Z__charter__rekor-merkle-root-public-anchor__goodoleusa"
tags: [charter, proposal, pseudosystem]
blueprint: "[[Charter.blueprint]]"
---

# Charter Proposal — rekor-merkle-root-public-anchor

> **Vault pseudosystem mirror** — canonical source: `forensics/charters/proposals/2026-05-25Z__charter__rekor-merkle-root-public-anchor__goodoleusa.json`
> Status: **proposed** | Mission: `[[rekor.anchor.public]]`

---

## Scope

Anchor each merge's Merkle root to Sigstore Rekor immediately post-merge. Persist inclusion proof in
forensics/anchors/. Wire into mission_graph.py merge verb as automatic post-merge step.

## Non-Goals

- Replacing Ed25519 local signing — Rekor is the public log; signing remains the local trust root
- Anchoring every individual COC entry (only merge points; branch detail is in the Merkle tree)
- Replacing Sigstore Rekor with a custom transparency log
- L1/L2 blockchain anchoring (explicitly skipped in parent charter forensic-coc-v2-rekor)

---

*Proposal charter — not yet activated. To activate, operator moves JSON to `forensics/charters/active/` and updates status field.*
