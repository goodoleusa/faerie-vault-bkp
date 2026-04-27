---
type: entity
entity_type: domain
status: stub
created: {{ file.ctime | moment("YYYY-MM-DD") }}
updated: {{ file.mtime | moment("YYYY-MM-DD") }}
tags: [osint, entity, domain]
entity_name: "{{ file.basename }}"
domain: "{{ file.basename }}"
registrar:
registration_date:
expiry_date:
nameservers: []
resolved_ips: []
hosting_provider:
ssl_issuer:
ssl_fingerprint:
parent:
  -
sibling:
  -
child:
  -
confidence_level: unassessed
source_quality: unverified
priority: medium
blueprint: "[[Domain.blueprint]]"
doc_hash: sha256:6ea3c5b281ccf0a91a371178bed9b02c13ea1ce62e80034a43008560ed18e61f
hash_ts: 2026-03-29T16:16:46Z
hash_method: body-sha256-v1
---

# {{ file.basename }}

{% section "Overview" %}
<!-- What is this domain? Why is it relevant? -->
{% endsection %}

{% section "Registration Info" %}
| Field | Value |
|-------|-------|
| **Domain** | {{ file.basename }} |
| **Registrar** | |
| **Registration Date** | |
| **Expiry Date** | |
| **Registrant** | |
| **Nameservers** | |
{% endsection %}

{% section "DNS Records" %}
| Type | Value | TTL |
|------|-------|-----|
| A | | |
| MX | | |
| TXT | | |
| NS | | |
{% endsection %}

{% section "SSL/TLS Certificate" %}
| Field | Value |
|-------|-------|
| **Issuer** | |
| **Subject** | |
| **SANs** | |
| **Valid From** | |
| **Valid To** | |
| **Fingerprint** | |
{% endsection %}

{% section "Historical DNS" %}
<!-- PassiveDNS, SecurityTrails, etc. -->
{% endsection %}

{% section "OSINT Sources" %}
| Source | URL | Date | Reliability |
|--------|-----|------|-------------|
| | | | |
{% endsection %}

{% section "Related IPs" %}
```dataview
LIST file.link
FROM "20-Entities/IPs"
WHERE contains(sibling, this.file.link)
SORT file.mtime DESC
```
{% endsection %}

{% section "Notes" %}
{% endsection %}
