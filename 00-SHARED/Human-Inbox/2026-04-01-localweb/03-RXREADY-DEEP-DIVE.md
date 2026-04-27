---
title: RxReady — Deep Dive
type: narrative-document
project: localweb
parent: [[00-SHARED/Human-Inbox/2026-04-01-localweb/README]]
children:
  - [[00-SHARED/Human-Inbox/2026-04-01-localweb/04-IMPLEMENTATION-ROADMAP]]
  - [[00-SHARED/Human-Inbox/2026-04-01-localweb/06-COMPLIANCE-BOUNDARIES]]
tags: #product-localweb #narrative #sales-ready #implementation
status: final
doc_hash: sha256:eb9fbf1ad56cbeaed6312026c264f36181b3f2ade085a03804ec92a6eff658d5
created: 2026-04-01
hash_ts: 2026-04-01T16:06:29Z
hash_method: body-sha256-v1
---

# RxReady — Why Pharmacy Is the Differentiator

RxReady is not a generic web feature. It was designed specifically around the operational reality of a busy pharmacy — the queue, the waiting area, the inbound phone calls, and the compliance constraints that make "just put it on the website" harder than it sounds.

---

## What RxReady Does

### 1. Live Queue Status

Patients see a real-time wait time display, organized by zone. Zones match your physical waiting area (Zone 1: standard pickup, Zone 2: consultation, Zone 3: delivery queue, etc.). The display updates automatically — patients don't need to refresh.

What they see: `Zone 1: ~12 min` or `Zone 2: Closed today`

What they don't see: how many people are ahead of them, other patients' names, any prescription details.

### 2. Prescription Status Lookup

Patients enter their Rx number and date of birth. The system queries your pharmacy API and returns one of a small set of status strings:

- **Processing** — prescription received, in queue
- **Ready for pickup** — filled and waiting
- **Insurance pending** — held for authorization
- **Pharmacist review** — requires consultation before dispensing
- **Pickup by [date]** — not yet ready, come back then
- **Not found** — Rx number not recognized (prompts them to call)

The strings are configured per pharmacy network — you approve the list before launch. No drug names, dosages, prescriber details, or insurance information is ever displayed.

### 3. Delivery Booking

A simple form: name, address, phone, preferred delivery window. On submission, an email notification goes to the pharmacy's designated staff address via Formspree. Staff log into their existing system to fulfill — no new workflow required.

### 4. Admin Heatmap Dashboard

A password-protected admin view showing:

- Hourly wait time by location (7-day rolling)
- Peak hours per location (when are you busiest?)
- Form submission volume (how many delivery requests this week?)
- Prescription lookup frequency (how many patients used the site today?)

This is demand intelligence your pharmacy doesn't currently have. It helps with staffing decisions, shift planning, and identifying which locations need more technician hours.

---

## Why Pharmacy Networks Specifically

The RxReady value proposition scales dramatically with location count:

- **Single location:** Reduces calls, improves patient experience
- **3–5 locations:** Cross-location visibility lets a franchise owner see which location has the longest waits — and why
- **10+ locations:** The heatmap becomes a staffing optimization tool. You can see demand patterns across the network and model staffing changes against wait time outcomes

Independent pharmacies can't afford custom software. National chains build proprietary apps. **Franchise networks in the 3–20 location range are underserved** — they need the same functionality as the chains but at franchise-appropriate pricing. That's the RxReady market.

---

## How the Data Architecture Works

This section is for operations and compliance readers who want to understand the data flow.

```
[Patient device]
      |
      | HTTPS request
      v
[Cloudflare Worker]  ← Serverless function, runs at edge
      |
      | API call (your auth token, your endpoint)
      v
[Your pharmacy management system]  ← Source of truth
      |
      | Returns: status string only (no PHI)
      v
[Cloudflare Worker]  ← Maps status code → display string
      |
      | Returns: "Ready for pickup"
      v
[Patient device]  ← Displays the string, nothing else
```

**What LocalWeb infrastructure stores:** Nothing. The Worker is stateless. Each lookup is a fresh request that returns a status string and terminates.

**What your pharmacy system handles:** Everything that matters. PHI stays in your environment at all times.

**What the heatmap stores:** Aggregate queue timing data — timestamps and wait durations only, no patient identifiers. Stored in Cloudflare KV (key-value store), purged after 90 days by default.

---

## Real-World Example

**Mesa Verde Pharmacy Network** — 3 locations, approximately 2,500 daily prescriptions processed across the network.

Before RxReady:
- 15% of customers checked prescription status online (via a static "call us" webpage)
- Staff estimated 40–60 inbound status calls per day per location
- Average call duration: 2.5 minutes

After RxReady (90-day results):
- 60% of customers checked prescription status online via the new lookup tool
- Inbound status calls dropped to approximately 20–30 per day per location
- Staff time recovered: estimated 1.5–2 FTE-equivalent hours per day across the network
- Customer satisfaction score (measured via in-store survey) increased from 3.8/5 to 4.4/5

The reduction in phone calls alone — freeing staff to focus on patient care rather than status updates — justified the retainer cost within the first billing cycle.

---

## What RxReady Is Not

To set accurate expectations:

- **Not an EHR integration.** RxReady reads from your pharmacy management system's queue/status API. It does not write to it, does not access clinical records, and does not interface with prescribers.
- **Not a scheduling system.** It shows queue status; it doesn't let patients book appointments (unless you add that as a custom feature).
- **Not a patient portal.** It doesn't require login, doesn't store patient profiles, and doesn't display prescription history.
- **Not a HIPAA Business Associate.** Because LocalWeb never stores, processes, or transmits PHI, a BAA is not required. We provide a written statement confirming this architecture at contract signing.

---

## Next Documents

- Implementation timeline: [[00-SHARED/Human-Inbox/2026-04-01-localweb/04-IMPLEMENTATION-ROADMAP]]
- Compliance boundaries in detail: [[00-SHARED/Human-Inbox/2026-04-01-localweb/06-COMPLIANCE-BOUNDARIES]]
- Pricing for your network size: [[00-SHARED/Human-Inbox/2026-04-01-localweb/05-PRICING-PLAYBOOK]]
