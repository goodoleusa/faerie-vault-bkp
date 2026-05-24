# Cartographer-View Assets + Credits

Curated for the planned `🗺 Cartographer` view of charters + future canvas
aesthetic work. **All assets MUST have their license + author credited in
this file before being committed to the repo.** When adding new assets,
update this doc — it is the canonical credits ledger.

---

## Fonts — legible-but-characterful cartography flavor

### Primary recommendation — Alagard (Hewett Tsoi)

- **License:** Free for commercial use (the author hosts the file freely; pixel/bitmap design intended for games)
- **Style:** Bitmap gothic; designed for legibility in game projects but reads as antique signage; pairs well with parchment palette
- **Sizes:** 16pt is the canonical "map inscription" size (per Medieval Fantasy City Generator community thread on itch.io)
- **Use in cartographer view:** charter titles, prominent labels, the compass-rose "N/S/E/W" letters
- **Source / download:** `fontmeme.com/fonts/alagard-font/` · also archived on `fontget.com`
- **Notes:** Pixel-perfect at integer multiples; do NOT scale fractionally
- **Credit line for footer/about:** "Alagard font by Hewett Tsoi"

### Companion serifs to load alongside

For body text + cluster_prefix annotations (Alagard is title-only):

- **IM Fell DW Pica** — Google Fonts; OFL license; antique press-era serif (Fell Types digitized by Igino Marini)
  Credit: "IM Fell DW Pica by Igino Marini (OFL)"
- **Cormorant SC** — Google Fonts; OFL; small caps for elegant charter-name headers
  Credit: "Cormorant SC by Catharsis Fonts / Christian Thalmann (OFL)"
- **Cinzel Decorative** — Google Fonts; OFL; engraved-stone look for "★" / sealed-charter labels
  Credit: "Cinzel Decorative by Natanael Gama (OFL)"
- **Old Standard TT** — Google Fonts; OFL; clean 1900s-academic serif as a fallback body font
  Credit: "Old Standard TT by Alexey Kryukov (OFL)"

All four are already on Google Fonts CDN — add to the existing fonts.googleapis
.com link in `deploy/chat-mvp/index.html` rather than vendoring.

### Decorative-only (use sparingly, ≤2 words):

- **Pirata One** — Google Fonts; OFL; blackletter; for "Here be dragons" annotations and isolated-charter labels only
  Credit: "Pirata One by Rodrigo Fuenzalida (OFL)"

---

## Tilesets + decorative SVG assets — itch.io and CC0 sources

### Map decoration packs (paid/free mix)

- **Penzilla — RPG Adventure Map Assets (Tileset)** — itch.io, hand-drawn, royalty-free use after purchase
  URL: penzilla.itch.io/hand-drawn-map-assets
  Use: trees, mountains, ruins, structures for canvas card decorations
  Credit: "Map decorations by Penzilla (penzilla.itch.io)"

- **cartography_BIGpack — under_score_lab** — itch.io, pixel-art over 200 tiles, 64 locations
  URL: under-score-lab.itch.io/cartography-bigpack
  Use: pixel-art mode in BrainstormCanvas (companion to retro themes V1/V2/V3)
  Credit: "Cartography BIGpack by under_score_lab (under-score-lab.itch.io)"

- **CC0 Hand-drawn Fantasy Icon Pack** — itch.io, 269 PNG + SVG icons, **CC0 (no attribution required, but credit anyway)**
  URL: search itch.io "CC0 hand-drawn fantasy icon pack"
  Use: charter type icons, smoking-gun emblems, wax-seal substitutes
  Credit: "Fantasy icons (CC0) via itch.io"

### Compass rose + sea-monster SVGs

- **Wikimedia Commons compass roses** — Public Domain
  Use: compass rose decoration in corner of cartographer view (use bearing colors: N=magenta, S=teal, E=cyan, W=gold)
  Credit: "Compass rose (Public Domain, Wikimedia Commons)"

- **OpenMoji** — CC-BY-SA 4.0; emoji set with hand-drawn alternates
  URL: openmoji.org
  Use: dragons, ships, sea-monster "here be dragons" annotations
  Credit: "Emoji from OpenMoji (CC-BY-SA 4.0)"

### Parchment + texture backgrounds

- **Subtle Patterns by Toptal** — CC-BY-SA 3.0; aged-paper / linen / parchment textures
  URL: subtlepatterns.com
  Pattern names to use: "old-mathematics" or "parchment" or "old-paper-2"
  Credit: "Background textures from Subtle Patterns (CC-BY-SA 3.0)"

- **Lost & Taken** — public-domain paper textures
  URL: lostandtaken.com
  Use: tileable parchment background for cartographer view
  Credit: "Parchment textures from Lost & Taken (Public Domain)"

---

## How credits get rendered

Three places attribution MUST appear:

1. **`docs/50-CARTOGRAPHER-ASSETS-CREDITS.md`** (this file) — full canonical ledger
2. **`deploy/chat-mvp/src/components/CartographerView.jsx`** footer (when shipped) — abbreviated credits with link to this doc
3. **`THIRD_PARTY_NOTICES.md`** at repo root if/when one exists (currently only swarmy-hive-plugin has one) — copy the credit lines verbatim

Format for in-app footer:
```
🗺 Cartographer view · fonts: Alagard (Hewett Tsoi) · IM Fell DW Pica · Cormorant SC · Cinzel Decorative · Pirata One · icons (CC0 itch.io) · textures (Subtle Patterns + Lost & Taken)
```

---

## Acquisition workflow (before committing any asset)

1. Read the license on the asset's listing page
2. Note the EXACT credit line the author wants (some say "by NAME" — use their exact form)
3. Add a row to this credits file with: asset name · author · license · URL · use case
4. If CC0: still credit (good practice, not required)
5. If GPL / non-commercial: do NOT use (we ship under a permissive license)
6. Test in a `forensics/ephemeral/{date}/cartographer-asset-pilot-NN/` sandbox before committing to canonical `src/`

---

## Open shopping list (for the cartographer agent + next session)

- [ ] Vendor Alagard.ttf or Alagard.woff2 to `deploy/chat-mvp/public/fonts/alagard/` (and add credit to license file)
- [ ] Add Google Fonts loader for IM Fell DW Pica + Cormorant SC + Cinzel Decorative + Pirata One to index.html
- [ ] Download CC0 fantasy icon pack — pick 6-8 icons (chest, scroll, compass, banner, ruin, mountain, ship, wax-seal)
- [ ] Source 2-3 parchment textures from Subtle Patterns or Lost & Taken (pick the most legible — avoid noisy ones that fight text)
- [ ] Vector compass rose SVG (bearing-colored arms; bake the N=magenta, S=teal, E=cyan, W=gold mapping)
- [ ] Wax-seal SVG component (red circle, embossed initial, ribbon below) for sealed charters
- [ ] "Here be dragons" annotation glyph (small dragon SVG + scrolly underline)
- [ ] Aged-card vignette CSS class (parchment fill, deckled edges via SVG mask, slight rotation animation when card is "active")

---

*Maintained at: `docs/50-CARTOGRAPHER-ASSETS-CREDITS.md`. Update before
shipping any asset that touches the cartographer view, BrainstormCanvas,
or CharterNeighborGraph styling.*
