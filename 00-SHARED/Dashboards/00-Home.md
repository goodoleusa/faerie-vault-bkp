---
type: dashboard
tier: home
title: "Faerie Home — f(0) Overview"
status: live
cssclasses: [wide-page, dashboard-home]
refresh_cadence: per-session
S: ['[01-Today](01-Today.md)', '[02-Missions-Emergent](02-Missions-Emergent.md)', '[03-Anchors](03-Anchors.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)', '[05-Stigmergy](05-Stigmergy.md)']
E: ['[VAULT-STRUCTURE](../VAULT-STRUCTURE.md)', '[Compass-Graph](Compass-Graph.md)']
tags: [dashboard, home, faerie]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md)

# Faerie Home — f(0) Overview

Sentence-trail summary of today's hive state. Mission clusters, recent anchors,
eval dimension scores. FFFF structure: Findings · Flags · Friction · Flow.

---

## 🌱 Learning paths

```dataviewjs
const paths = dv.pages('#path/onboarding').sort(p => p['path-step'])
dv.table(['Step', 'Note', 'Summary'],
  paths.map(p => [p['path-step'] ?? '?', dv.fileLink(p.file.path), p.summary ?? '']))
```

---

## 🐝 Hive actions (Meta Bind)

```meta-bind-button
label: 🐝 Spawn manifest
id: faerie-spawn
style: primary
actions:
  - type: inlineJS
    code: |
      const tokenPath = '.faerie-token';
      let tok = '';
      try { tok = (await app.vault.adapter.read(tokenPath)).trim(); } catch(e) { new Notice('Set ' + tokenPath + ' first'); return; }
      const charter = await app.vault.adapter.read('forensics/charters/active.txt').catch(() => 'default');
      const r = await fetch('https://api.retrofuture.tech/tools/faerie_spawn', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json' },
        body: JSON.stringify({ charter_ref: charter.trim() })
      });
      new Notice(r.ok ? '🐝 manifest spawned' : '⚠ ' + r.status);
```

```meta-bind-button
label: 📊 Refresh metrics
id: faerie-metrics
style: default
actions:
  - type: inlineJS
    code: |
      const tokenPath = '.faerie-token';
      let tok = '';
      try { tok = (await app.vault.adapter.read(tokenPath)).trim(); } catch(e) { new Notice('Set ' + tokenPath + ' first'); return; }
      const r = await fetch('https://api.retrofuture.tech/tools/faerie_metrics', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      if (!r.ok) { new Notice('⚠ ' + r.status); return; }
      const data = await r.json();
      const out = '00-SHARED/Dashboards/_metrics-latest.md';
      await app.vault.adapter.write(out, '```json\n' + JSON.stringify(data, null, 2) + '\n```\n');
      new Notice('📊 metrics → ' + out);
```

```meta-bind-button
label: 🌼 Mirror today
id: faerie-mirror
style: default
actions:
  - type: inlineJS
    code: |
      const tokenPath = '.faerie-token';
      let tok = '';
      try { tok = (await app.vault.adapter.read(tokenPath)).trim(); } catch(e) { new Notice('Set ' + tokenPath + ' first'); return; }
      const today = new Date().toISOString().slice(0,10);
      const r = await fetch('https://api.retrofuture.tech/tools/faerie_vault_mirror_daily', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: today })
      });
      new Notice(r.ok ? '🌼 mirrored ' + today : '⚠ ' + r.status);
```

---

## 💎 Lifecycle ladder

> Read the crystals, not the volume. See [[../HELP/crystallization-workflow|crystallization workflow]] and [[../Faerie-System-Internals/Sync-Scripts/PROMOTION-PIPELINE|promotion pipeline]].

**Time tiers (volume → crystal):**

- 📌 **Today** — atomic notes: [[../Daily/_index|Daily/]]
- 🗓️ **This week** — [[../Weekly/_index|Weekly digests]]
- 📆 **This month** — [[../Monthly/_index|Monthly digests]]
- ⚓ **Anchor set** — [[../Anchors/_index|Anchors/]] (permanent principles)
- 🍯 **Honey droplets** — [[../Honey/_index|Honey/]] (crystallized memory)
- 📜 **Charters** — [[../Charters/_index|Charters/]] (declared intent)

**Promotion pipeline (ephemeral → canonical, mirrors `faerie2/forensics/`):**

- 🌼 **Ephemeral** — [[../Ephemeral/_index|Ephemeral/]] (agent scratch, only writable path)
- 📌 **Manifests** — [[../Manifests/_index|Manifests/]] (work cells, symlink overlay)
- ⬡ **Artifacts** — [[../Artifacts/_index|Artifacts/]] (work products, symlink overlay)
- 📦 **Bundles** — [[../Bundles/_index|Bundles/]] (spawn context, symlink overlay)
- 🔗 **COC entries** — [[../COC-Entries/_index|COC-Entries/]] (hash-chained audit)
- 🧑 **Human** — [[../Human/_index|Human/]] (your annotations, parallel COC chain)

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const week = (() => {
  const d = new Date(); d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
  const wk = Math.ceil((((d - yearStart) / 86400000) + 1)/7);
  return `${d.getUTCFullYear()}-W${String(wk).padStart(2,'0')}`;
})();
const month = today.slice(0,7);
dv.table(['Tier','Pointer'], [
  ['📌 Daily', `[[../Daily/${today}/_index|${today}]]`],
  ['🗓️ Weekly', `[[../Weekly/${week}/_index|${week}]]`],
  ['📆 Monthly', `[[../Monthly/${month}/_index|${month}]]`],
  ['⚓ Anchors', '[[../Anchors/_index|view set]]'],
  ['🍯 Honey', '[[../Honey/_index|view droplets]]'],
]);
```

---

## FFFF (today)

- **Findings:** see [[01-Today]]
- **Flags:** see [[03-Anchors]] (status=proposed)
- **Friction:** see [[04-Eval-Dimensions]] (low-trend dimensions)
- **Flow:** see [[05-Stigmergy]] (discovered_work density)
