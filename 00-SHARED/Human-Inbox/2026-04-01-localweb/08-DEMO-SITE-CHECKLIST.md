---
title: Demo Site Checklist — RxReady Live Demo Setup
type: checklist
project: localweb
parent: [[00-SHARED/Human-Inbox/2026-04-01-localweb/README]]
tags: #product-localweb #narrative #implementation
status: final
doc_hash: sha256:e8e76dce8d519aa05a34b52a03ed2df244463b273d333750d9d72fb84fe19af1
created: 2026-04-01
hash_ts: 2026-04-01T16:10:21Z
hash_method: body-sha256-v1
---

# Demo Site Checklist — How to Set Up the RxReady Demo

This is your pre-pitch preparation checklist. Before any sales call where you plan to show a live demo, these items should be complete. A broken demo loses the sale faster than a missing feature.

---

## Step 1 — Create the Demo Pharmacy Network

Use a fictional 3-location pharmacy network with plausible names. Do NOT use a real pharmacy's name without permission.

**Suggested demo network:** "Clearwater Rx" — 3 locations in a mid-sized metro

| Location | Name | URL Path |
|---|---|---|
| Location 1 | Clearwater Rx — Westside | `/westside` |
| Location 2 | Clearwater Rx — Downtown | `/downtown` |
| Location 3 | Clearwater Rx — Campus | `/campus` |

Brand colors for the demo: a clean professional blue (#1e3a5f) + white + a warm accent (#f4a430). These look trustworthy without looking like any specific real pharmacy chain.

---

## Step 2 — Set Up Demo Queue Data

You have two options:

**Option A: Hardcoded demo data (fastest)**

In the Cloudflare Worker, hardcode a static response object:

```js
const DEMO_QUEUE = {
  westside: { zone1: 12, zone2: 8, zone3: "Delivery booking only" },
  downtown: { zone1: 24, zone2: 15, zone3: 6 },
  campus: { zone1: 7, zone2: "Closed today", zone3: 19 }
};
```

This requires no API endpoint — the Worker just returns these values. Perfect for demos where you want full control of what the prospect sees.

**Option B: Live test data from Cloudflare KV**

Set up a Cloudflare KV namespace (`DEMO_QUEUE_DATA`) and write test values via the Cloudflare dashboard. The Worker reads from KV on each request. This lets you update queue times in real time during a demo (impressive, if you need it).

**Recommendation:** Start with Option A. Use Option B for enterprise prospects who want to see "real" data flow.

---

## Step 3 — Set Up Demo Prescription Lookup

Create a small lookup table of fictional Rx numbers that return different statuses. Store in Cloudflare KV or hardcode in the Worker:

| Rx Number | DOB (any) | Status Returned |
|---|---|---|
| 8801234 | any valid DOB | Ready for pickup |
| 8805678 | any valid DOB | Processing |
| 8809012 | any valid DOB | Insurance pending |
| 8803456 | any valid DOB | Pharmacist review required |
| 8807890 | any valid DOB | Pickup by Friday |
| 9990001 | any valid DOB | Not found — please call |

During the demo, you enter Rx `8801234` to show "Ready for pickup," then `8805678` to show "Processing." The prospect sees the variety of status options in under 60 seconds.

---

## Step 4 — Set Up Delivery Booking Form

Configure Formspree with a demo email address (your own email) so you can show a submission being received in real time.

- Go to formspree.io → create a free account → create a new form
- Set the submission destination to your email address
- Copy the form endpoint into the demo site's HTML
- Test: submit the form from the demo site → confirm the email arrives in under 30 seconds

During the demo: have your email inbox visible in a second tab. Submit the form, then immediately switch tabs to show the email arriving. This is the most viscerally convincing moment in the pitch.

---

## Step 5 — Build the Admin Heatmap

The admin dashboard is password-protected (`/admin`). Use Cloudflare Access (free tier) or a simple hardcoded password check in the Worker.

**Demo heatmap data to show:**

Create a 7-day heatmap with realistic patterns:
- Monday and Friday: busiest (show longer bars in those columns)
- Tuesday–Thursday: moderate
- Saturday: moderate morning, quiet afternoon
- Sunday: closed

The heatmap's purpose in the demo is to make the phrase "demand data you've never had before" concrete and visual. Make sure it looks compelling — use clear color gradients (light = short wait, dark = long wait).

**Suggested colors:** White (#ffffff) → light teal (#a8d8d8) → dark teal (#1a6b6b) for the heatmap scale. Professional and readable.

---

## Step 6 — Deploy to Cloudflare Pages

```bash
# From your project directory
npm run build   # Astro build

# Then deploy via Cloudflare dashboard or wrangler
npx wrangler pages deploy dist/ --project-name rxready-demo
```

Your demo site will be live at: `rxready-demo.pages.dev`

For a more professional demo URL: add a custom subdomain via Cloudflare DNS. For example, `demo.localwebstudio.com/clearwater` — takes about 10 minutes to configure.

---

## Step 7 — Pre-Call Testing Checklist

Run through this within 2 hours of the call:

- [ ] Demo site loads in under 2 seconds on mobile (test on your phone)
- [ ] Queue displays show current times for all 3 locations
- [ ] Prescription lookup returns correct status for Rx 8801234 and 8805678
- [ ] Delivery booking form submits and email arrives
- [ ] Admin dashboard loads and heatmap is visible
- [ ] All 3 location URL paths work (`/westside`, `/downtown`, `/campus`)
- [ ] HTTPS is active (padlock shows in browser)
- [ ] You have the admin password memorized or written somewhere you can see it

---

## Demo Scripts — What to Say While Showing Each Feature

### Patient-facing view

"Here's what a patient sees when they open the pharmacy's website. They don't need to download an app or create an account.

They see the queue for their location — Zone 1 is about 12 minutes right now. They can decide if they want to come in or come back later.

If they want to check their prescription: they enter their Rx number and date of birth. *(Type in 8801234)* They see 'Ready for pickup.' That took 5 seconds instead of a phone call.

If they want delivery: one form, 3 fields. They submit it — and watch..."

*(Switch to email inbox tab — show the notification arriving.)*

"Your staff just got that. No new workflow. No new system. Just an email they can act on."

---

### Admin dashboard view

"Now here's what you see.

This is the heatmap for all three locations over the past 7 days. You can see immediately: Friday afternoons are your peak across the network. Downtown is consistently busier than Westside on Mondays. Campus is surprisingly light on Tuesdays.

You've always known some of this intuitively. Now you have the data to act on it — staffing, shift scheduling, knowing when to bring in a float tech."

---

### Technical walkthrough (for IT-curious prospects)

"And here's the architecture, for your IT team's comfort.

This is the Cloudflare Worker. It sits between the patient's browser and your API endpoint. When a patient does a lookup, the Worker calls your system, gets a status code back, maps it to a display string, and returns that string. The Rx number and date of birth never touch our infrastructure again — they're gone the moment the Worker finishes.

Your API endpoint is stored here as an encrypted secret — I can't read it, and it never appears in the site's source code."

---

## If the Demo Breaks During the Call

Stay calm. Have a fallback:

1. **If queue display fails:** "Let me show you a screenshot — I'm seeing an intermittent issue with the demo network." Switch to a saved screenshot.
2. **If prescription lookup fails:** Explain the flow verbally. "In practice, you'd see 'Ready for pickup' appear here within 2 seconds. The backend is connecting to your system in real time."
3. **If admin dashboard fails:** Same approach — screenshot as backup, explain the heatmap concept.

**Key rule:** Never apologize profusely or get flustered. A brief technical hiccup in a demo is normal. How you handle it is actually a proof point about how you handle production issues.

---

*Sales script: [[00-SHARED/Human-Inbox/2026-04-01-localweb/07-SALES-PITCH-SCRIPT]]*
*Client intake: [[templates/CLIENT-INTAKE-FORM]]*
