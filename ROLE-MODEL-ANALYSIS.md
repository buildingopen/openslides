# Role Model Analysis: 5 Deck Archetypes

The component system must work across ALL these styles, not just one. Every component must accept theme tokens and look native in each archetype.

---

## Archetype 1: Warm Tech (floom)

**Reference:** floom pitch deck v4
**Colors:** Warm white #FAFAF7 bg, emerald #059669 accent, dark green #064E3B for cards
**Fonts:** DM Serif Display (headlines), Plus Jakarta Sans (body), JetBrains Mono (code)
**Feel:** Human, warm, approachable. "Not developer-SaaS, think Notion/Loom"

### Distinctive Patterns
- Split layouts (55/45, 40/60) on every slide
- Code blocks with syntax highlighting as visual anchors
- Browser mockups showing the deployed product
- Dark green accent cards for emphasis
- Green-tinted (#ECFDF5) cards for callouts
- Badge rows with Heroicons (Live URL, Web UI, REST API, MCP)
- Stats inline within cards ("2 hrs" / "3 days" / "$0")
- Comparison table with real SVG company logos
- Subtle emerald radial gradient in top-right corner

### Components Used
- split layout, dark_card, surface_card, tinted_card, blocker_card (with stat), feature_card, stat_hero, code_block, browser_mockup, badge_row, comparison_table, fund_bars, milestone_timeline, metadata_bar, section_label

---

## Archetype 2: Consulting (McKinsey/BCG)

**Reference:** McKinsey-style strategy decks
**Colors:** Navy #1a2744 + white, occasional gold #c4981a accent
**Fonts:** Georgia/Playfair Display (headlines), Inter/Helvetica (body)
**Feel:** Authoritative, data-dense, structured. "We did the analysis."

### Distinctive Patterns
- **Takeaway bar** at top of every slide: one sentence in bold that summarizes the slide's message. The most distinctive McKinsey element.
- **Exhibit labels**: "Exhibit 3: Market Sizing Analysis" - numbered, formal
- **Framework diagrams**: 2x2 matrices, process arrows, waterfall charts
- **Data tables**: structured grids with alternating row colors
- **Source citations** at bottom: "Source: McKinsey Global Institute, 2025"
- Heavy use of bar charts (horizontal, stacked, grouped)
- Minimal decorative elements. Information density is the aesthetic.
- Left-aligned text blocks with bullet hierarchies (indented bullets)
- Navy accent bar at top or left edge of slide
- Page numbers and confidentiality notices

### Components Needed
- takeaway_bar (bold summary sentence at top)
- exhibit_label ("Exhibit 3: Title")
- framework_2x2 (quadrant with labels)
- process_arrows (horizontal flow with steps)
- data_table (structured grid, alternating rows)
- stacked_bar_chart
- waterfall_chart
- source_citation
- bullet_hierarchy (indented nested bullets)
- navy_accent_bar (top or left edge)

### How Current Components Adapt
- `split layout` -> works, but consulting decks use more full-width layouts
- `stat_hero` -> works, but numbers are smaller and accompanied by more context
- `comparison_table` -> works perfectly for this style
- `dark_card` -> swap green for navy
- NEW: takeaway_bar is unique to consulting, needs its own component

---

## Archetype 3: Startup Classic (Airbnb 2009)

**Reference:** Airbnb's original pitch deck, Buffer's open deck
**Colors:** White bg, one blue accent #3b82f6, minimal palette
**Fonts:** Simple sans-serif (Helvetica, Arial), nothing fancy
**Feel:** Founder-direct, scrappy, authentic. "Let me tell you a story."

### Distinctive Patterns
- **Extreme simplicity**: one idea per slide, sometimes just a headline + one image
- **Large photos**: full-bleed or near-full-bleed product/experience photos
- **Big numbers, no charts**: "$1.2B" in 96px font, nothing else on the slide
- **No cards, no grids**: just text + image, or text + number
- **Problem/solution as before/after**: "Traveling..." (sad) vs "With Airbnb..." (happy)
- Little to no decoration: no gradients, no shadows, no borders
- Personality through content, not design
- Bottom-aligned metadata (confidential, page number)

### Components Needed
- hero_image (full or half-width photo/screenshot)
- big_number (single stat, massive font, centered)
- simple_text (headline + one paragraph, generous whitespace)
- before_after (two states side by side, minimal)
- photo_strip (row of 3-4 photos)

### How Current Components Adapt
- Most current components are TOO complex for this style
- Need simpler variants that show LESS, not more
- `stat_hero` at 120px+ with nothing else on the slide
- `split layout` with image on one side, text on other

---

## Archetype 4: Modern Minimal (Linear/Notion/Vercel)

**Reference:** Linear.app, Vercel, Raycast pitch decks
**Colors:** Near-white #fafafa or pure dark #0a0a0a, single accent (purple, blue, or red)
**Fonts:** Inter, SF Pro, or custom brand font. One weight.
**Feel:** Precise, engineered, tasteful. "Every pixel is intentional."

### Distinctive Patterns
- **Product screenshots are the hero**: large, high-quality screenshots dominate
- **Minimal text**: headlines are 6-8 words max. Body text is rare.
- **No borders on cards**: cards defined by subtle shadow or background offset
- **Monochrome + one accent**: everything is gray scale except one color
- **Dark mode as default** for title/closing, light for content
- **Generous whitespace**: slides feel spacious, never crowded
- **Metric dashboards**: rows of 3-4 KPIs with labels
- **Timeline as horizontal dots**: not vertical, minimal
- **Logo walls**: customer or partner logos in a clean grid

### Components Needed
- screenshot_hero (large product screenshot, dominant)
- minimal_metric_row (3-4 numbers, tiny labels, lots of space)
- logo_wall (grid of customer logos, grayscale)
- shadow_card (no border, subtle shadow only)
- horizontal_timeline (dots on a line)
- dark_hero (full dark bg with centered headline)

### How Current Components Adapt
- Current cards have borders. Need borderless shadow variants.
- `stat_hero` works but needs more whitespace around it
- `comparison_table` needs a cleaner, more minimal variant
- Product screenshots are the main gap (need auto-screenshot or placeholder)

---

## Archetype 5: Consumer Editorial (Glossier/Allbirds/Warby Parker)

**Reference:** DTC brand pitch decks, lifestyle brands
**Colors:** Warm cream #FFF8F0, blush #fda4af or sage #86efac accent, earth tones
**Fonts:** Serif headlines (Freight, Canela, Playfair), clean sans body
**Feel:** Magazine editorial, aspirational, emotional. "Feel, then think."

### Distinctive Patterns
- **Large lifestyle photography**: people using the product, not product shots
- **Pull quotes as visual elements**: large italic quotes with author photos
- **Editorial typography**: drop caps, varied font sizes, mixed serif/sans
- **Pastel color blocking**: large colored sections (blush, sage, cream)
- **Testimonial-heavy**: customer stories are the evidence, not metrics
- **Minimal data viz**: numbers exist but aren't charted. Just stated elegantly.
- **Full-bleed images** with text overlaid
- **Magazine-style grids**: asymmetric photo + text layouts

### Components Needed
- pull_quote (large italic quote with attribution)
- lifestyle_image (full-bleed or large-format photo)
- editorial_headline (mixed sizes, drop cap option)
- color_block (full-width tinted section)
- testimonial_card (photo + quote + name)
- asymmetric_grid (mixed-size blocks, editorial feel)

### How Current Components Adapt
- `dark_card` -> swap green for blush/sage
- `stat_hero` -> works but with serif font and softer styling
- `badge_row` -> works, swap pill style for rounded softer pills
- Current templates are too structured/corporate for this style
- Need a way to break the grid (asymmetric layouts)

---

## Component Matrix: What Each Archetype Needs

| Component | Warm Tech | Consulting | Startup Classic | Modern Minimal | Consumer Editorial |
|-----------|-----------|-----------|----------------|---------------|-------------------|
| split layout | PRIMARY | sometimes | PRIMARY | sometimes | sometimes |
| full_width | sometimes | PRIMARY | sometimes | PRIMARY | sometimes |
| stat_hero | inline in cards | standalone | PRIMARY (huge) | standalone | standalone (serif) |
| dark_card | green bg | navy bg | rare | dark bg | blush/sage bg |
| surface_card | white+border | white+border | rare | shadow only | cream+soft |
| tinted_card | green tint | blue tint | rare | accent tint | pastel tint |
| code_block | PRIMARY | rare | rare | sometimes | never |
| browser_mockup | PRIMARY | never | rare | PRIMARY | rare |
| comparison_table | yes | PRIMARY | rare | yes (minimal) | rare |
| bar_chart | yes | PRIMARY | rare | yes | rare |
| milestone_timeline | vertical | horizontal arrows | rare | horizontal dots | rare |
| badge_row | yes | rare | rare | yes | yes (softer) |
| takeaway_bar | never | PRIMARY | never | never | never |
| photo/screenshot | product mockup | frameworks | lifestyle photos | product screenshots | lifestyle photos |
| pull_quote | rare | never | sometimes | rare | PRIMARY |
| fund_bars | yes | yes | simple | yes | rare |
| logo_wall | in comparison | rare | rare | yes (customers) | rare |
| blocker_card | with stat | bullet list | simple text | minimal | emotional text |

### Universal Components (work in all 5)
1. `split(left, right, ratio)` - every style uses two-column
2. `stat_hero(value, label)` - every style has big numbers
3. `section_label(text)` - every style labels sections
4. `headline(text, accent_phrase)` - every style has headlines with emphasis
5. `subtitle(text)` - every style has supporting text
6. `card(content, variant)` - every style has cards (variant: dark, surface, tinted, shadow, pastel)
7. `badge_row(items)` - most styles have pill labels
8. `metadata_bar(items)` - every slide has header/footer

### Style-Specific Components
- Consulting: `takeaway_bar`, `exhibit_label`, `framework_2x2`, `source_citation`
- Startup Classic: `big_number_solo`, `hero_image`, `simple_text`
- Modern Minimal: `screenshot_hero`, `logo_wall`, `shadow_card`, `horizontal_timeline`
- Consumer Editorial: `pull_quote`, `lifestyle_image`, `color_block`, `testimonial_card`
- Warm Tech: `code_block`, `browser_mockup`, `deploy_command`

---

## Architecture Decision

Build the 8 universal components first. They cover 80% of all slides across all styles. Then add style-specific components as the LLM declares them.

The LLM doesn't need to know about "archetypes." It picks components based on the content:
- Financial data -> `bar_chart` or `stat_hero`
- Customer evidence -> `pull_quote` or `testimonial_card`
- Product demo -> `code_block` + `browser_mockup` or `screenshot_hero`
- Competitive landscape -> `comparison_table`
- Timeline -> `milestone_timeline`

The theme controls the LOOK (colors, fonts, card styles). The components control the STRUCTURE (what visual elements exist). The LLM controls the ASSEMBLY (which components on which slide).
