---
title: Service Agreement Template — LocalWeb Studio
type: guide
project: localweb
parent: [[00-SHARED/Human-Inbox/hustle/README]]
tags: #product-localweb #implementation
status: final
doc_hash: sha256:e394549ea197178f2f84fd8d89c21041c2e6117633aef55c28e8c1e8b1d00a33
created: 2026-04-01
hash_ts: 2026-04-01T16:11:48Z
hash_method: body-sha256-v1
---

# Service Agreement — LocalWeb Studio

**IMPORTANT NOTICE:** This is a template for your review. It is not legal advice. Have your attorney review before using this as a binding contract with any client.

---

**SERVICE AGREEMENT**

This Service Agreement ("Agreement") is entered into as of [DATE] between:

**LocalWeb Studio** ("Service Provider")
[Your name and address]
[Your email and phone]

and

**[CLIENT NETWORK NAME]** ("Client")
[Client's legal business name and address]
[Client's primary contact name, email, phone]

---

## 1. Scope of Services

Service Provider agrees to design, build, configure, and maintain a website and associated services for Client's pharmacy network ("the Site") in accordance with the specifications outlined in Exhibit A (Project Scope) attached hereto.

**Core services included:**

a) **Website design and build** — A custom-configured RxReady pharmacy website based on Service Provider's template system, branded to Client's visual identity, deployed to Cloudflare Pages

b) **RxReady queue and status system** — A Cloudflare Worker-based prescription status lookup and live queue display system, integrated with Client's pharmacy management system API endpoint as specified in Exhibit A

c) **Delivery booking functionality** — A form-based delivery request system that delivers notifications to Client's designated staff email address(es)

d) **Admin heatmap dashboard** — A password-protected administrative view showing aggregate wait time and usage data across Client's locations

e) **Monthly support** — Up to [1 hour / as specified in Exhibit A] of content updates per month, bug fixes, and Cloudflare infrastructure monitoring

f) **Quarterly security audit** — Review of Cloudflare configuration, SSL certificates, and Worker permissions once per calendar quarter

---

## 2. Project Timeline

Service Provider will complete the initial build and deliver a staging environment to Client within [28 / 35] days of receiving all required intake materials from Client (see Exhibit B — Client Responsibilities). Timeline extensions caused by delays in Client-provided materials do not constitute a breach by Service Provider.

---

## 3. Client Responsibilities

Client agrees to:

a) Provide all intake materials requested in Exhibit B within 7 days of contract signing, or notify Service Provider of any delays

b) Designate a technical point of contact (IT administrator) with access to the pharmacy management system API

c) Designate a compliance officer to review the data flow documentation provided by Service Provider and complete the compliance sign-off checklist before the site goes live

d) Conduct User Acceptance Testing (UAT) during Week 3 as outlined in the Implementation Roadmap and provide written approval before public launch

e) Ensure that Client's pharmacy management system API endpoint is functional, authenticated, and rate-limited appropriately; Client bears sole responsibility for API endpoint security

f) Complete staff training within 14 days of site launch

---

## 4. Fees and Payment

**Setup Fee:** $[AMOUNT]
- 50% due upon execution of this Agreement
- 50% due upon delivery of staging environment (end of Week 2)

**Monthly Retainer:** $[AMOUNT] per month
- First month due upon public launch
- Subsequent months due by the 5th of each calendar month
- Late payment (after the 10th): 1.5% monthly late fee applied

**Additional Services:**
- Work exceeding monthly included hours: $95/hr, billed on written change order approved by Client before work begins
- Out-of-scope feature development: Scoped and billed separately per written statement of work
- Emergency support (outside business hours, enterprise tier only): $150/hr

**Payment methods:** ACH bank transfer, check, or credit card (credit card subject to 2.9% processing fee)

---

## 5. Term and Renewal

This Agreement commences on the date of execution and continues for an initial term of [12 / 24] months ("Initial Term"). Following the Initial Term, this Agreement automatically renews on a month-to-month basis unless either party provides 60 days written notice of non-renewal.

---

## 6. Termination

**Termination by Client:**
Client may terminate this Agreement with 90 days written notice to Service Provider, or by paying a termination fee equal to one (1) month's retainer in lieu of the notice period.

**Termination by Service Provider:**
Service Provider may terminate this Agreement with 60 days written notice for any reason, or immediately upon Client's material breach that remains uncured 14 days after written notice.

**Upon termination:**
- Service Provider will provide Client with all source files, Cloudflare configuration exports, and a handoff documentation package within 5 business days
- Cloudflare account transfer will be completed within 5 business days of request
- The Site will remain live until the Cloudflare account transfer is complete or 30 days after termination, whichever comes first
- Service Provider retains the right to use non-identifiable portions of the work as portfolio examples

---

## 7. Intellectual Property

**Client IP:** All content provided by Client (brand assets, photography, copy, data) remains Client's property.

**Service Provider IP:** The underlying template architecture, Worker code framework, and admin dashboard system remain the property of Service Provider. Client receives a perpetual, non-exclusive license to use the configured version of these systems for the life of the contract and, upon termination, via the handoff package.

**Work product:** The finished, configured Site (the assembled combination of Client IP + Service Provider templates, as customized for Client) is owned by Client upon full payment of all invoiced amounts.

---

## 8. Data and Privacy

Service Provider represents and warrants that:

a) Service Provider's infrastructure does not store, process, or transmit patient health information (PHI) as defined under HIPAA

b) Prescription status lookup responses are processed transiently in Service Provider's Cloudflare Worker and are not logged, stored, or retained

c) The only patient-identifiable data that passes through Service Provider's Worker is the Rx number and date of birth submitted by the patient for the purpose of a single lookup query; this data is not retained after the query completes

d) Aggregate analytics data (timestamps, wait durations) stored in Cloudflare KV contains no patient identifiers and is purged after [90] days

e) Service Provider will notify Client within 24 hours of becoming aware of any security incident affecting Service Provider's infrastructure

**Client acknowledges** that Client's pharmacy management system API and all PHI contained therein are solely Client's responsibility, and that Client bears sole HIPAA compliance obligations for any PHI in Client's system.

Service Provider is not a HIPAA Business Associate as defined under 45 C.F.R. §164.502(e). A Business Associate Agreement (BAA) is not required. Service Provider will provide a written architectural attestation confirming this determination upon Client's request.

---

## 9. Warranties and Disclaimers

Service Provider warrants that:
- The Site will function materially as described in Exhibit A for the duration of the Agreement
- All work will be performed in a professional and workmanlike manner

Service Provider does not warrant:
- Specific search engine rankings or traffic outcomes
- Uptime of Cloudflare infrastructure (subject to Cloudflare's own SLA — historical uptime 99.99%)
- Compatibility with future updates to Client's pharmacy management system API

---

## 10. Limitation of Liability

Service Provider's total liability under this Agreement for any cause of action, regardless of form, shall not exceed the total fees paid by Client in the 3 months preceding the claim. In no event shall Service Provider be liable for indirect, incidental, consequential, or punitive damages.

---

## 11. Governing Law

This Agreement shall be governed by the laws of the State of [STATE], without regard to its conflict of laws provisions. Any disputes shall be resolved by binding arbitration in [CITY, STATE] under the rules of the American Arbitration Association.

---

## 12. Entire Agreement

This Agreement, together with Exhibits A and B, constitutes the entire agreement between the parties and supersedes all prior negotiations, representations, and agreements relating to the subject matter hereof. Amendments must be in writing and signed by both parties.

---

**SIGNATURES**

Service Provider:
Name: _____________________________
Title: ______________________________
Date: ______________________________
Signature: __________________________

Client:
Name: _____________________________
Title: ______________________________
Date: ______________________________
Signature: __________________________

---

## Exhibit A — Project Scope

*(Complete this per engagement)*

- Number of locations: _____
- Location names and URL slugs: _____
- Included features: [ ] Queue display [ ] Rx lookup [ ] Delivery booking [ ] Admin dashboard
- Monthly support hours included: _____
- Setup fee: $_____
- Monthly retainer: $_____
- Contract term: [ ] 12 months [ ] 24 months
- Special requirements or custom integrations: _____

---

## Exhibit B — Client Responsibilities Checklist

*(Sign off as items are delivered)*

- [ ] Intake form completed (Section 1–10 of CLIENT-INTAKE-FORM)
- [ ] Brand assets delivered
- [ ] Photography delivered (or stock approved)
- [ ] API endpoint details provided (sandbox + production)
- [ ] IT administrator introduced
- [ ] Compliance officer introduced
- [ ] Status strings approved
- [ ] UAT completed and signed off
- [ ] Staff training completed
- [ ] Launch approved
