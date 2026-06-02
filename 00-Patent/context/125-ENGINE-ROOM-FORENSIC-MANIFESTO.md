# Manifesto: The Forensic Engine Room & Sovereign Data

## The Core Concept
The Reckon Engine Room is not an operational dashboard; it is a **forensic control plane**. In traditional systems, infrastructure deployments are "states" that exist independently of their audit logs. In Reckon, the deployment is a **derivative of its audit log**.

## I. Infrastructure-as-Forensics
Every infrastructure state—whether a Helm chart deployment or a container scaling event—must be cryptographically anchored to a Chain of Custody entry *before* the action is authorized by the infrastructure pipeline.

*   **Intent**: Agent signs off on a deployment hash.
*   **Proof**: The signature is committed to the COC.
*   **Execution**: The pipeline verifies the signature against the COC and only then applies the infrastructure change.

## II. Zero-Knowledge Data Sovereignty
Data privacy is not a feature; it is an architectural constraint. Reckon implements a **Split-Key Sovereignty Model**:

1.  **Encryption Plane**: Customer holds the encryption keys to their B2 storage. Vendor servers never see the raw plaintext.
2.  **Signing Plane (The Novelty)**: Even forensic audit entries (the COC) are signed with customer-held keys. We have moved the forensic integrity plane outside of the vendor's total control.
3.  **No-Vendor-Crypto Surface**: Because the signing of audit logs happens on the customer's machine (via the signing daemon), the vendor cannot forge history or impersonate the customer. The machine acts on behalf of the customer, but the customer retains the "Hand."

## III. Forensic Integrity Claims
Every byte produced by the system is verifiable:
*   **Verification**: `COC entry + Signature == Truth`.
*   **Audit**: Any auditor—third-party or customer—can mechanically trace every production artifact back to a cryptographically authenticated Agent Roster and a signed Spawn Directive.

---
*Drafted by the Engine Room. Operator: Review, polish, and promote to `faerie-vault/00-Publications/` for external transparency.*
