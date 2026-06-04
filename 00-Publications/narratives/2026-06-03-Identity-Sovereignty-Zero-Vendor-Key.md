---
title: "Identity Sovereignty: Why No Private Key Should Ever Touch a Vendor's Server"
type: publication-teaser
created: 2026-06-03
canonical_doc: reckon/docs/158-IDENTITY-SOVEREIGNTY-CANONICAL.md
patent_claim: reckon/business/patent/_source/PATENT-CLAIM-ZERO-VENDOR-KEY-CUSTODY.md
tags: [identity, cryptography, sovereignty, SLIP-0010, SLIP-0039, Ed25519, architecture]
status: teaser — full architecture in doc/158
---

# Identity Sovereignty: Why No Private Key Should Ever Touch a Vendor's Server

*A teaser for the architecture described in doc/158 — crystallized 2026-06-03.*

---

## The one-sentence version

In Reckon's multi-user architecture, every private key — for every user, for every agent — is derived client-side from a master seed that the vendor has never seen, so the vendor can never sign as you, read your data, or be compelled to hand over your keys.

## The problem with conventional identity

Every major cloud platform follows the same implicit model: the vendor generates your identity credentials, stores them, and can theoretically access or reassign them. Even "bring your own key" (BYOK) patterns rely on the vendor's key management infrastructure. You are trusting organizational policy, not math.

That model breaks down in three specific ways that matter to Reckon:

1. **Agent impersonation:** If agent keys are generated on the server, a server breach or rogue administrator can forge agent signatures — invalidating every forensic record those agents ever produced.
2. **Data exposure under legal process:** If the vendor holds enough key material to reconstruct your encryption key, a court order can unlock your data regardless of your privacy settings.
3. **Audit trail corruption:** A co-signature chain (like Reckon's charter-seal mechanism) is only as trustworthy as the source of the signing keys. Server-generated keys mean the vendor can backfill a fake history.

## The architecture

Reckon's solution is a three-tier identity hierarchy rooted in a user-held master seed:

- **Your human key** (`m/0`): signs the one act you are responsible for — accepting a charter, authorizing a mission, federating with a collaborator.
- **Agent keys** (`m/agent/N`): derived at spawn time, one per agent session, each cryptographically provable as "acting under" your human root. The derivation path IS the chain of authority — no database lookup needed.
- **Data encryption key** (`m/dek`): encrypts everything before it reaches B2 storage. The vendor sees only ciphertext.

All three tiers derive from the same master seed via SLIP-0010 hierarchical deterministic derivation — the same standard used in hardware crypto wallets, now applied to AI-agent forensic identity.

Recovery uses SLIP-0039 (Shamir's Secret Sharing) with a critical constraint: the vendor can hold at most k-1 shares, where k is the reconstruction threshold. So even with a court order, the vendor cannot reconstruct your seed. They can freeze your bucket (legitimate legal compliance) but they cannot read it (your data remains yours).

## What this enables

- **Cross-user federation:** Your human key signs a two-parent merge accepting a peer's mission branch — you become a signing node in the mission DAG, using the same co-signature protocol agents already use.
- **Governance without read access:** The operator's governance storage credential can freeze and preserve your data under legal hold — satisfying preservation obligations — without ever decrypting a byte.
- **Portable forensic trust:** Any verifier can confirm "this agent acted under this user's authority" from public information in the COC record — no trust in the vendor required.

## Current status

The signing infrastructure (Ed25519, charter seals, COC entries, Rekor anchoring) is live. The SLIP-0010 derivation layer and SLIP-0039 recovery ceremony are designed and build-ordered (doc/158 §7). A new patent claim (Claim 7e draft) extends the existing provisional to cover this architecture.

---

*Full architecture: `reckon/docs/158-IDENTITY-SOVEREIGNTY-CANONICAL.md`*  
*Patent draft: `reckon/business/patent/_source/PATENT-CLAIM-ZERO-VENDOR-KEY-CUSTODY.md`*
