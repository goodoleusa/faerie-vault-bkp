---
title: Sales
type: hive-section
section: sales
up: "[[00-Hive-Home]]"
same: "[[01-Dev]], [[02-Eval]], [[03-UIX]], [[04-Marketing]], [[06-Agent-Chat]]"
tags:
  - hive/sales
  - path/hive
cssclasses:
  - hive-section
---

# 💰 Sales

> [!south] Ship Deliverables
> Pricing, intake pipeline, Stripe, client delivery.

## Pricing

| Tier | Price | Delivery |
|------|-------|---------|
| Starter | $799 | 5 days |
| Signature | $1,299 | 7 days |
| Powerhouse | $2,499 | 10 days |

## Pipeline

```dataviewjs
const intakes = dv.pages('"Sales/Intakes"').sort(f => f.file.mtime, 'desc').slice(0, 5)
if (intakes.length > 0) {
  dv.table(["Client", "Tier", "Status", "Date"],
    intakes.map(i => [i.file.link, i.tier ?? "—", i.status ?? "pending", i.file.mtime.toFormat("MM-dd")]))
} else {
  dv.paragraph("No intakes yet.")
}
```

## Quick Actions

```meta-bind-button
style: primary
label: "📝 New Intake"
action:
  type: link
  link: "https://cybertemplate.retrofuture.tech/intake"
```

```meta-bind-button
style: default
label: "💳 Stripe Dashboard"
action:
  type: link
  link: "https://dashboard.stripe.com"
```

## Clients

- [[Clients/]] — project folders per client
