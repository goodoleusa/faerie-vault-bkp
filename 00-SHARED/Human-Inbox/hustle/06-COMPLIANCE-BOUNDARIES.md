---
title: Compliance Boundaries — What LocalWeb Handles vs. What the Pharmacy Handles
type: guide
project: localweb
parent: [[00-SHARED/Human-Inbox/hustle/README]]
tags: #product-localweb #narrative #sales-ready #implementation
status: final
doc_hash: sha256:9326e3df7d617e47df75d250d8d9c13e103c59f4f675981049585a17d61e944f
created: 2026-04-01
hash_ts: 2026-04-01T16:08:31Z
hash_method: body-sha256-v1
---

# Compliance Boundaries

This is the document for compliance officers, pharmacy directors, and legal reviewers. It defines exactly where LocalWeb Studio's responsibility ends and the pharmacy's begins — clearly, without hedging.

---

## The Core Principle

**LocalWeb Studio never touches patient health information (PHI).**

The RxReady system is designed around a single architectural guarantee: the pharmacy's system is the source of truth. LocalWeb builds the interface. The pharmacy owns the data.

This is not a legal technicality — it is a design constraint enforced at the code level. There is no way for LocalWeb infrastructure to store, log, or process PHI because the system is built to never receive it.

---

## What LocalWeb DOES Handle

| Area | LocalWeb Responsibility |
|---|---|
| **Website security** | HTTPS enforced site-wide via Cloudflare SSL certificates |
| **DDoS protection** | Cloudflare's network-layer protection for all traffic |
| **Form encryption** | All form submissions transmitted over TLS 1.3 |
| **Static content delivery** | Global CDN caching for fast, secure asset delivery |
| **Worker security** | Cloudflare Worker code audited for injection vulnerabilities before deployment |
| **API key management** | Your pharmacy API credentials stored as encrypted Cloudflare Worker secrets — never in source code |
| **Status string mapping** | Translating your system's internal codes to approved display strings (you approve the mapping before launch) |
| **Aggregate analytics** | Heatmap stores timestamps and wait durations only — no patient identifiers |

---

## What LocalWeb Does NOT Handle

| Area | Why It's Out of Scope |
|---|---|
| **PHI encryption at rest** | PHI lives in your pharmacy management system, not on LocalWeb infrastructure |
| **Patient authentication** | The Rx lookup requires Rx number + DOB — authentication is intentionally minimal; if you need stronger auth, your system handles it |
| **API endpoint security** | Your IT team controls the API endpoint. LocalWeb connects to it but does not secure it. |
| **Prescriber authentication** | Any workflow requiring prescriber login or signature is entirely within your system |
| **Insurance data** | Never passed through LocalWeb; never displayed |
| **HIPAA Business Associate obligations** | Because LocalWeb does not store, process, or transmit PHI, a BAA is not required. LocalWeb provides a written architectural attestation confirming this. |
| **PDMP compliance** | Prescription Drug Monitoring Program obligations belong to the pharmacy and prescribers |
| **State pharmacy board compliance** | Licensing, signage, and regulatory requirements belong to the pharmacy |

---

## The Rx Lookup — A Closer Look

The prescription status lookup is the component most likely to trigger compliance questions. Here is exactly how it works:

1. **Patient submits:** Rx number (a sequence of digits, typically 7–12 characters) and date of birth (month/year only is sufficient in most implementations)
2. **Worker queries:** Your pharmacy API endpoint with those two values and your API authentication credentials
3. **Your system returns:** A status code (e.g., `READY`, `PROCESSING`, `INSURANCE_HOLD`)
4. **Worker maps:** Status code → display string using your approved mapping table
5. **Patient sees:** "Ready for pickup" — nothing else

**What the Worker never receives, stores, or transmits:**
- Patient name
- Drug name, strength, or form
- Prescriber name or DEA number
- Insurance carrier or member ID
- Fill history or refill count
- Any other prescription detail

The Rx number itself is treated as a non-PHI identifier in this context — it is functionally equivalent to an order number. Combined with date of birth, it provides enough specificity to locate a single prescription without exposing clinical data.

**If your legal team disagrees with this classification:** We can implement an alternative flow where your system generates a one-time lookup token and LocalWeb's system only ever handles the token (never the Rx number). This is a supported configuration at no extra cost.

---

## Delivery Booking Forms

The delivery booking form collects: name, address, phone, preferred delivery window.

This is operationally equivalent to a phone call — the patient is providing delivery information voluntarily. The form submission goes directly to your designated staff email via Formspree. LocalWeb retains no copy.

Formspree is GDPR-compliant and does not sell form data. If you prefer an alternative submission mechanism (e.g., webhook to your system directly), that can be configured during implementation.

---

## Compliance Checklist — Pharmacy's Responsibilities Before Launch

Before the site goes live, your compliance officer should complete the following:

- [ ] **Legal review of data sharing agreement** — LocalWeb provides a template; your attorney reviews and signs
- [ ] **Compliance officer sign-off** — On the status string list and the Rx lookup data flow documented above
- [ ] **Privacy policy review** — Most networks need a one-line addition: "We use a third-party website service that may display your prescription status. No health information is stored by this service." Specific language should be reviewed by your attorney.
- [ ] **Staff training on queue system** — Staff should understand what patients can see and how to update queue status (through your existing system — no new software required on their end)
- [ ] **Sandbox testing** — All prescription lookups should be tested in your sandbox environment before going live with real data
- [ ] **API endpoint security review** — Your IT team should confirm the endpoint is appropriately authenticated and rate-limited
- [ ] **Data retention confirmation** — Confirm you're comfortable with heatmap aggregate data (timestamps + wait durations, no patient identifiers) retained for 90 days in Cloudflare KV

---

## Documentation LocalWeb Provides at Contract Signing

1. **Architectural attestation letter** — Signed statement confirming LocalWeb infrastructure does not store, process, or transmit PHI
2. **Data flow diagram** — Visual representation of every data path in the system, with clear notation of where PHI boundaries are
3. **Status string mapping table** — For your review and approval before launch
4. **Cloudflare security settings export** — Showing SSL configuration, DDoS protection settings, and Worker permissions
5. **Worker source code** — Full source for your legal/IT team to review before deployment

---

## Frequently Asked Questions from Compliance Officers

**"Do we need a BAA with LocalWeb?"**
No. A BAA is required when a Business Associate creates, receives, maintains, or transmits PHI on behalf of a Covered Entity. Because LocalWeb's infrastructure never receives PHI — only status codes that your system returns — the HIPAA Business Associate definition is not triggered. We provide this in writing.

**"What happens if someone finds someone else's prescription status by guessing Rx numbers?"**
The lookup requires both Rx number AND date of birth. Guessing a valid combination is mathematically difficult (millions of possible DOB combinations per Rx number). Additionally, only a status string is returned — no clinical information. However, if your compliance team wants additional friction (e.g., last 4 digits of phone number as a third factor), we can add it.

**"Is Cloudflare HIPAA-compliant?"**
Cloudflare offers a HIPAA-eligible service tier with a BAA for customers who require it. Because LocalWeb is not handling PHI, our standard Cloudflare configuration does not require that tier. If your legal team requires Cloudflare to be part of a covered service arrangement, we can upgrade to Cloudflare's HIPAA-eligible tier — contact us for pricing.

**"What if we get a data breach?"**
If a breach occurs on LocalWeb infrastructure (which would not contain PHI), we notify you within 24 hours and provide a full incident report. Because no PHI is on our infrastructure, there is no HIPAA breach notification obligation triggered by a LocalWeb-side incident. A breach of your pharmacy system (where PHI lives) is handled entirely by you under your existing incident response plan — LocalWeb is not involved.

---

*Related: [[00-SHARED/Human-Inbox/hustle/03-RXREADY-DEEP-DIVE]] — full technical architecture of the RxReady data flow*
