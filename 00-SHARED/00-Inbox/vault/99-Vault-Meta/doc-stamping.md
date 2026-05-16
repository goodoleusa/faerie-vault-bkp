---
type: reference
status: active
tags: [meta, doc_hash, stamping, integrity]
parent: 99-Vault-Meta/INDEX
up: 99-Vault-Meta/INDEX
created: 2026-04-24
updated: 2026-04-24
doc_hash: sha256:598e8cfd9ef63dd7666b0d95d4806876bffe5283e768c7397343b21046b1734a
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [↑ Vault-Meta](INDEX.md) · [⌂ Home](../../HOME.md)

# Doc Stamping

How `doc_hash` works in vault frontmatter.

---

## Purpose

Every vault document gets a SHA256 hash of its body content stored in
frontmatter as `doc_hash`. This enables:
- Detecting when a document has been edited
- COC entries linking vault content to forensics/
- Integrity verification of the vault derivative artifacts

---

## Stamp Command

```bash
python3 ~/.claude/scripts/stamp_doc_hash.py --file path/to/doc.md
```

This computes the SHA256 of the document body (excluding the frontmatter hash field
itself) and writes it to `doc_hash` in the frontmatter.

---

## Initial State

New documents start with:
```yaml
doc_hash: sha256:pending
```

This is intentional — indicates the document has not been stamped yet.
Hooks at session stop will catch unstamped documents and flag them.

---

## When to Stamp

- After completing a new document (before committing)
- After editing an existing document
- The 8 priority documents in this vault are stamped as part of creation

If `stamp_doc_hash.py` is missing: leave `sha256:pending` and note in
manifest for follow-up. The COC will show it as unstamped.

---

## hash_method

The stamp script records which hashing method was used:
```yaml
doc_hash: sha256:abc123...
hash_ts: 2026-04-24T15:30:00Z
hash_method: body-sha256-v1
```

`body-sha256-v1` = SHA256 of body content after stripping frontmatter block.

---

## Related

- [[../00-SHARED/Architecture/forensic-integrity]] — the broader integrity system
- [[breadcrumb-conventions]] — other vault conventions
- [[../00-SHARED/Hive/proof-in-place]] — why integrity matters
