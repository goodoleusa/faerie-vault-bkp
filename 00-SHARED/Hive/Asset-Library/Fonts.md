---
title: Fonts
type: asset-library
up: "[[03-UIX]]"
tags:
  - assets/fonts
  - hive/uix
---

# Fonts — Asset Library

All OFL-licensed, Google Fonts CDN.

## Active (already in use)

| Font | Use | CDN |
|------|-----|-----|
| Inter | UI labels, body | `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap` |
| Space Grotesk | Headers, RetroFuture brand | `https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap` |

## Recommended additions

| Font | Best for | CDN |
|------|---------|-----|
| DM Sans | UI labels, small body text — low contrast geometric | `https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap` |
| Outfit | Diagram headers, badges — friendly geometric | `https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap` |
| Plus Jakarta Sans | Technical prose + UI hybrid | `https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap` |
| Figtree | Dashboard labels, relaxed professional | `https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;600;700&display=swap` |
| Sora | Retro-futuristic headers, hive branding | `https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap` |

## Obsidian Font Settings

Set in `.obsidian/appearance.json`:
- `interfaceFontFamily`: `"DM Sans"` — clean UI chrome
- `textFontFamily`: `"Plus Jakarta Sans"` — note body text
- `monospaceFontFamily`: `"JetBrains Mono"` — code blocks

## Excalidraw

Default font is now set to **Helvetica** (clean, professional). CJK fonts (Chinese + Japanese) enabled.
To use a custom font in diagrams, place a `.woff2` file in `Excalidraw/CJK Fonts/`.
