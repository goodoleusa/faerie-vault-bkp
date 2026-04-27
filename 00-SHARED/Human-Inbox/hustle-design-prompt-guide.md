# Design Prompt Guide — Luma AI to Web Templates

A practical reference for generating design inputs that translate cleanly into code.

---

## 1. What to Generate in Luma AI

You are generating **reference artifacts**, not deliverables. The AI image becomes a specification that Claude reads and translates into tokens, components, and CSS. Use the right vocabulary so you get the right output.

| What to Ask For | What It Is | What It Produces |
|---|---|---|
| **Style tile** | Single image: colors + type + buttons + cards in one layout | `palettes.ts` + font pairing |
| **Component mockup** | One isolated UI section (hero, nav, card grid) | Astro component |
| **Color palette board** | Swatches with visible hex values | `client-theme.css` custom properties |
| **Typography specimen** | Heading + body font pairing at multiple sizes | Font hierarchy decisions |

**What a style tile is NOT:** a wireframe (no lorem ipsum gray boxes), a logo (no brand identity work), a screenshot (not a real site).

A style tile is a mood board with rules. It shows what every repeated element looks like before any page is built.

---

## 2. Prompt Templates for Luma AI

Copy, fill in the brackets, generate.

---

### Style Tile

```
In a [AESTHETIC] style, create a web design style tile showing:
- Color palette with 6 swatches (primary dark, accent bright, surface white, text, muted, border)
- Typography: display heading font + body text sample paragraph
- Button styles: primary filled, secondary outlined, ghost
- Card with shadow, border radius, and content
- Navigation bar sample
- Badge/pill styles
Background: white. Clean, organized layout. Professional reference sheet.
```

**Fill [AESTHETIC] with:** brutalist / minimalist / art deco / retro-futurist / Swiss grid / vaporwave

---

### Hero Section

```
Website hero section mockup in a [AESTHETIC] style:
- Large bold headline: "[YOUR TAGLINE HERE]"
- Subheading paragraph below
- Two CTA buttons side by side
- Trust badges below (checkmarks with short text)
- Background: [COLOR or gradient description]
- Clean, modern, production-ready web design
```

---

### Brutalist Variant

```
Raw brutalist web design style tile. Rules: monospace typography throughout,
thick 3px black borders on all elements, zero rounded corners, high contrast
black and [ACCENT COLOR] on white. Show: navigation bar, hero section with
massive 96px headline, three feature cards with heavy borders, stark footer.
Anti-aesthetic. Bold. Uncompromising. No drop shadows. No gradients.
```

---

### Color Palette Board

```
Flat design color palette board for a [AESTHETIC] web brand.
Show 8 color swatches arranged horizontally. Each swatch labeled with:
its hex code, its role (Primary / Accent / Surface / Text / Muted / Border / Success / Error).
Background: white. Clean grid layout. No decorative elements.
```

---

### Typography Specimen

```
Web typography specimen sheet for a [AESTHETIC] brand.
Show two font pairings side by side:
Left: display/heading font — show at 72px, 48px, 32px, 24px with sample text
Right: body font — show paragraph text, 16px regular, 14px muted, 12px caption
Include: letter-spacing demo, font-weight ladder (300 400 600 700 900 if available)
Background: white. Grid lines optional. Professional reference format.
```

---

## 3. The Translation Pipeline

How each Luma output maps to actual code:

```
Style tile
  └── Color palette block     →  palettes.ts (color token object)
  └── Button styles           →  button variants in component CSS
  └── Card style              →  .card base styles, border-radius, shadow tokens
  └── Nav bar                 →  Nav.astro layout + active state

Hero mockup
  └── Headline + subhead      →  h2 + p in Hero.astro
  └── CTA buttons             →  <a class="btn-primary"> + <a class="btn-secondary">
  └── Background color/image  →  CSS background property or gradient token
  └── Trust badges            →  <ul class="trust-badges"> with SVG icons

Color palette board
  └── Primary dark            →  --color-primary in client-theme.css
  └── Accent bright           →  --color-accent
  └── Surface white           →  --color-surface
  └── Text                    →  --color-text
  └── Muted                   →  --color-muted
  └── Border                  →  --color-border

Typography specimen
  └── Display font            →  --font-display (h1, h2)
  └── Body font               →  --font-body (p, li, label)
  └── Size ladder             →  --text-xs through --text-6xl tokens
  └── Weight choices          →  font-weight values per element type
```

---

## 4. Font Hierarchy Cheat Sheet

Each heading level serves a specific communication job. Match the font choice to the job.

| Level | Role | Personality | Notes |
|---|---|---|---|
| **h1** | Logo / brand name | Distinctive, memorable | Often styled as text, not an image. Use `letter-spacing`, `text-transform`, `font-weight` for character. |
| **h2** | Hero headline / section titles | The FIRST thing visitors read. Story font. | Needs to work at 48px+. Brutalist: massive and blunt. Elegant: refined and airy. |
| **h3** | Card titles, feature names | Clear, scannable | Slightly smaller than h2. Same family or complementary. |
| **h4** = | Section labels, sidebar headers | Quiet authority | Often uppercase + letter-spaced for label feel. |
| **p / body** | Running text | Always readable | Inter, Lato, Source Sans Pro. Never decorative. |
| **small / .muted** | Captions, timestamps, metadata | Invisible but present | Lighter weight, muted color. |

**The rule:** You can use one font family for everything (vary weight/size) OR pair a display font (h1–h2) with a workhorse body font (p). Do not use three fonts. Do not use a display font at 14px.

**Brutalist font stack:** `font-family: 'Courier New', Courier, monospace` for everything. No exceptions. That IS the aesthetic.

---

## 5. What Makes a Good Input for Claude

When you hand off a Luma image, the more of this you can name, the better the output:

**Critical (always include):**
- Color palette — hex values if visible, or at minimum: "navy + gold + cream", "black + lime on white"
- Overall mood in 2–3 words — "stark industrial minimalist", "warm editorial luxury", "playful tech startup"

**High value (include when visible):**
- Font mood — not the exact font name, but: "bold condensed industrial", "elegant editorial serif", "clean geometric sans", "raw monospace"
- Corner radius feel — sharp (0px) / subtle (4–6px) / rounded (12–16px) / pill (9999px)
- Shadow intensity — flat (none) / subtle (soft small) / dramatic (hard offset)

**Bonus (name if obvious):**
- Border weight — hairline (1px) / medium (2px) / heavy (3–4px) / ultra-heavy (6px+)
- Spacing feel — tight and dense / balanced / airy and generous
- Any specific component you saw that you want replicated

**What Claude does NOT need:** the exact Luma prompt you used, pixel dimensions, or apologies for imperfect images.

---

## 6. Quick Reference: Aesthetic Vocabulary

### Design Movements

| Term | What It Means | Visual Signature |
|---|---|---|
| **Brutalist** | Deliberately raw, anti-decorative | Heavy borders, monospace, no rounded corners, stark contrast |
| **Minimalist** | Maximum reduction | White space, one accent color, thin strokes, subtle type |
| **Swiss / International** | Grid-based, functionalist | Strong grid, Helvetica/Neue, red accents, rigid alignment |
| **Art Deco** | Geometric luxury | Gold + black, geometric ornaments, serif display fonts |
| **Vaporwave** | 80s-90s digital nostalgia | Magenta + cyan + purple, gradients, retro fonts, grid floors |
| **Chillwave** | Soft nostalgic warmth | Muted pastels, grainy textures, rounded forms |
| **Retro-futurism** | Space-age optimism | Green-on-black terminals OR chrome + orange + white |
| **Neobrutalism** | Brutalism with color pop | Primary colors, thick borders, offset shadows, bold type |

---

### Font Category Glossary

| Term | Means | Example Use |
|---|---|---|
| **Serif** | Has small feet/strokes at letter ends | Editorial, luxury, traditional |
| **Sans-serif** | No feet, clean strokes | Tech, modern, readable |
| **Slab-serif** | Block-style feet, heavy | Industrial, Western, confident |
| **Monospace** | Every character same width | Brutalist, code, terminal |
| **Display** | Decorative, only for headlines | Logos, hero text, never body |

---

### Design Approach Glossary

| Term | Means |
|---|---|
| **Flat design** | No shadows, no gradients, pure color and shape |
| **Skeuomorphic** | Looks like a physical object (buttons that look pressed, leather textures) |
| **Neomorphic / Neumorphism** | Soft extruded plastic look, light/shadow from same surface color |

---

### UI Component Glossary

| Term | Means |
|---|---|
| **Above the fold** | What you see without scrolling |
| **CTA** | Call to action — a button or link that asks for a click ("Get Started", "Buy Now") |
| **Hero** | The first full-width section of a page |
| **Nav / Navbar** | Navigation bar (top or side) |
| **Footer** | Bottom section of a page |
| **Card** | A contained unit of content with border or background |
| **Badge / Pill** | Small inline label (tag, status indicator) |
| **Toast** | Temporary notification that appears and disappears |
| **Modal** | Overlay dialog that blocks the page |

---

### Spacing and Shape Glossary

| Term | Means |
|---|---|
| **Padding** | Space INSIDE an element (between content and its border) |
| **Margin** | Space OUTSIDE an element (between it and neighbors) |
| **Border-radius** | Corner roundness. `0` = sharp square. `9999px` = full pill. |
| **Box-shadow** | Drop shadow. Format: `X-offset Y-offset blur spread color` |
| **Gap** | Space between items in a flex or grid container |
| **Stroke / Border** | The line around an element. Weight measured in `px`. |

---

*Last updated: 2026-04-02*
