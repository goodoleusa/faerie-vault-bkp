---
title: Monthly Retainer Scope — LocalWeb Studio
type: guide
project: localweb
parent: [[00-SHARED/Human-Inbox/hustle/README]]
tags: #product-localweb #implementation
status: final
doc_hash: sha256:dc3a1e6104f51c7a86902f564317d3cdab36f16da49694cea1af2351e6a33cef
created: 2026-04-01
hash_ts: 2026-04-01T16:13:10Z
hash_method: body-sha256-v1
---

# Monthly Retainer Scope

**For:** Active LocalWeb Studio retainer clients
**Purpose:** Defines exactly what is and is not included in your monthly retainer — no surprises

This document is shared with every client at contract signing. It is also included in the annual retainer review. Clear scope = no awkward conversations about "is this included?"

---

## What Is Always Included

Every monthly retainer includes the following, regardless of tier:

### Hosting and Infrastructure

- Cloudflare Pages hosting for all site pages
- Global CDN delivery (your site loads fast everywhere)
- DDoS protection (network-layer, no action needed from you)
- SSL certificate management (auto-renewing, always HTTPS)
- Cloudflare Workers execution for queue display and prescription lookup
- Formspree form processing for delivery booking

There is no hosting bill sent separately. Hosting is part of the retainer.

### Ongoing Bug Fixes

If any feature of your site stops working correctly — the queue display shows errors, the Rx lookup returns wrong statuses, the delivery form fails to send, the admin dashboard is broken — LocalWeb fixes it at no extra charge. Bug fixes are not counted against your monthly support hours.

**What counts as a bug:** Something that worked before and now doesn't, due to a code or configuration issue on our end.

**What doesn't count as a bug:** A change to your pharmacy management system's API that breaks the integration. If your system changes the API structure, fixing the Worker to match the new structure is a change order (see below).

### Monthly Support Hours

Your retainer includes **[1 hour / per Exhibit A]** of support time per calendar month for content updates. This covers:

- Text changes anywhere on the site (hours, addresses, staff names, service descriptions, special announcements)
- Image swaps (replacing photos with new ones)
- Hours changes (including holiday schedules)
- Minor layout adjustments (moving a section, changing a color, adjusting a heading)
- Status string updates (adding or changing a status display string)
- Admin dashboard user management (adding or removing dashboard logins)

**Unused hours do not roll over** to the following month. They reset on the 1st of each month.

### Quarterly Cloudflare Audit

Once per calendar quarter, LocalWeb reviews:

- SSL certificate status and renewal dates
- Worker error rates and performance metrics
- Formspree form submission volume and error log
- Cloudflare security settings (WAF rules, rate limiting)
- Any Cloudflare platform updates that may affect your site

A brief written summary is emailed to the client contact after each audit. No action is required from you unless an issue is found.

---

## What Is Not Included

### New Features

Anything that doesn't exist on your site today and needs to be built. Examples:

- Appointment scheduling system
- Loyalty program integration
- New page types (e.g., a blog, a team directory)
- Patient portal login
- Additional API integrations beyond those in Exhibit A
- Custom analytics dashboard
- Email marketing integration

New features are scoped as a project and billed separately. We provide an estimate before starting.

### Major Layout or Design Changes

Significant redesign work is not included in the retainer. Examples:

- Changing the overall site structure or navigation
- Redesigning the homepage from scratch
- Adding a new visual theme or rebrand
- Custom animation or interactive elements

If you're considering a redesign, we can discuss whether to treat it as a new project (one-time fee) or phase it in over several months of elevated support.

### Custom Integrations

Connecting LocalWeb's systems to any new third-party service beyond the existing implementation. Examples:

- Integrating with a new pharmacy management system (if you switch vendors)
- Adding a Google Analytics or tag manager implementation
- Connecting to a CRM or marketing automation platform
- Building a webhook receiver for a new internal tool

Custom integrations start at $500 and are scoped per engagement.

### Photography and Content Creation

Original photography, copywriting, or graphic design is not included in the retainer. If you need new photos or new written content, that is billed at our standard rate or outsourced on your behalf.

### Additional Staff Training Sessions

The initial 30-minute staff training video is included in the setup fee. If you hire new staff and want a live training session (video call walkthrough), additional sessions are $150/session.

---

## The Over-Limit Process

If a request will require more than your included monthly hours, here's what happens:

1. You submit a request (email is fine)
2. LocalWeb reviews and estimates the time required
3. If the estimate exceeds your included hours, we send a **change order** by email
4. The change order states: what work will be done, estimated hours, cost ($95/hr, 1-hour minimum)
5. You approve or decline — via email reply is sufficient
6. Work begins only after approval
7. Work is billed on the next monthly invoice, or separately for large engagements

**We never start over-limit work without approval.** If you've never received a change order from us, it's because we haven't needed to — not because we're doing it for free.

---

## Example: What Different Requests Look Like

| Request | Category | Included? |
|---|---|---|
| "Update our Sunday hours" | Text change | Yes |
| "Add two new staff photos" | Image swap | Yes |
| "The Rx lookup is showing the wrong status" | Bug fix | Yes |
| "Our API endpoint URL changed" | API update | Change order |
| "Can we add a flu shot scheduling calendar?" | New feature | Change order |
| "Redesign the homepage" | Major redesign | Change order |
| "We're switching to a new pharmacy system" | New integration | Change order |
| "Add a second language (Spanish)" | New feature | Change order |
| "Fix the broken mobile menu" | Bug fix | Yes |
| "The admin heatmap stopped updating" | Bug fix | Yes |
| "Move the phone number to a different location" | Minor layout | Yes (if under 30 min) |

---

## Escalating a Support Request

For urgent issues (e.g., the queue display is completely broken during business hours):

1. Email [your email] with subject: **URGENT — [your network name]**
2. If no response within 2 hours during business hours (M–F 9am–6pm [your time zone]): call [your phone]
3. Enterprise tier clients have a dedicated emergency contact and 4-hour SLA

For non-urgent requests: email is preferred. We respond within 1 business day.

---

## Annual Retainer Review

At the 11-month mark of each contract term, LocalWeb will send a retainer review including:

- Summary of support hours used per month (average and total)
- List of change orders completed during the year
- Site performance metrics (page load speed trend, error rate)
- Recommendations for the next term (any features worth considering?)
- Renewal pricing (locked at current rate unless infrastructure costs require adjustment)

---

*Service Agreement: [[templates/SERVICE-AGREEMENT-TEMPLATE]]*
*Implementation Checklist: [[templates/IMPLEMENTATION-CHECKLIST]]*
