---
type: entity
entity_type: ip-address
status: stub
created: {{ file.ctime | moment("YYYY-MM-DD") }}
updated: {{ file.mtime | moment("YYYY-MM-DD") }}
tags: [osint, entity, ip-address]
entity_name: "{{ file.basename }}"
ip_address: "{{ file.basename }}"
asn:
asn_org:
country:
city:
hosting_provider:
first_seen:
last_seen:
ports_open: []
services: []
certificates: []
parent:
  -
sibling:
  -
child:
  -
confidence_level: unassessed
source_quality: unverified
shodan_url:
censys_url:
priority: medium
blueprint: "[[IP-Address.blueprint]]"
doc_hash: sha256:91f18b1a5ece5479fcf09948c736e78b1d28a106df361b8f6ee7ab9bdbd403b8
hash_ts: 2026-03-29T16:16:46Z
hash_method: body-sha256-v1
---

# {{ file.basename }}

{% section "Overview" %}
<!-- What is this IP? Why is it significant to the investigation? -->
{% endsection %}

{% section "Network Info" %}
| Field | Value |
|-------|-------|
| **IP Address** | {{ file.basename }} |
| **ASN** | |
| **ASN Organization** | |
| **Country** | |
| **City** | |
| **Hosting Provider** | |
| **Reverse DNS** | |
{% endsection %}

{% section "Open Ports & Services" %}
| Port | Protocol | Service | Version | Notes |
|------|----------|---------|---------|-------|
| | | | | |
{% endsection %}

{% section "Certificates" %}
| Subject | Issuer | Valid From | Valid To | Fingerprint |
|---------|--------|-----------|---------|-------------|
| | | | | |
{% endsection %}

{% section "Historical Data" %}
<!-- Shodan history, Censys snapshots, passive DNS records -->
{% endsection %}

{% section "OSINT Sources" %}
| Source | URL | Date | Reliability |
|--------|-----|------|-------------|
| Shodan | | | |
| Censys | | | |
| VirusTotal | | | |
{% endsection %}

{% section "Related Domains" %}
```dataview
LIST file.link
FROM "20-Entities/Domains"
WHERE contains(sibling, this.file.link)
SORT file.mtime DESC
```
{% endsection %}

{% section "Notes" %}
{% endsection %}
