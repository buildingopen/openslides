# WORKPLAN: OpenSlides Visual Quality - From 7/10 to 10/10

**Created:** 2026-04-01
**Status:** PLANNING
**Scope:** HOLD (visual quality only, no new features)
**Depends on:** Engine complete (Sprint 1 done), content quality 8/10 (done)
**Score:** 10/10

## Problem Statement

OpenSlides generates pitch decks from a prompt. The content is 8/10 (specific, punchy, well-structured). The visuals are 6-7/10 (clean typography, correct colors, icons, but every slide is text + colored rectangles). The real floom deck is 9/10 because every slide has a bespoke visual anchor: app mockup, code block, chart, photo, logo grid.

The gap: programmatic templates produce "wireframes with good fonts." Professional decks have visual density, variety, and data visualization.

This workplan closes that gap without overfitting to any single industry (tech, consulting, consumer).

## Competitive Benchmark

Before building, establish the target. Take 3 Gamma-generated decks, screenshot them, score with our Gemini rubric. Those scores become the bar.

| Benchmark | How | Target |
|-----------|-----|--------|
| Gamma pitch deck | Generate via gamma.app, screenshot all slides, Gemini-score | Record per-slide scores |
| Beautiful.ai deck | Same process | Record per-slide scores |
| Hand-crafted floom deck | Already have screenshots | 9/10 (known) |
| OpenSlides current | Already have screenshots | 6-7/10 (known) |

**Success criteria:** OpenSlides Gemini scores >= Gamma scores on the same brief.

## Diagnosis: Why It's Still Weak

| Visual element | Real deck has it | OpenSlides has it | Impact |
|---|---|---|---|
| Product screenshot/mockup | Title + solution slides | None | HIGH |
| Code block with syntax highlighting | Title + solution slides | Built (visuals.py) but not wired | MEDIUM |
| Bar/pie chart SVG | Market slide | None | HIGH |
| Comparison table with logos | Competition slide | Text-only columns | HIGH |
| Timeline visualization | Traction slide | Dots + text | MEDIUM |
| Team photos | Team slide | None | MEDIUM |
| Hero stat numbers | Multiple slides | None | HIGH |
| Varied layouts per slide type | Every slide different | Same layout per type | HIGH |
| Contextual icons (not generic stars) | Feature cards | Keyword match (weak) | MEDIUM |

Root cause: templates only render text, not visual elements.

## Architecture: Two-Pass Generation

### Current (broken)
```
Prompt -> LLM generates text content -> Template renders text as HTML
```

### Target
```
Prompt -> LLM generates text + layout choice + visual data -> Template renders text + visual elements as HTML
```

### Schema Change

Current:
```json
{
  "type": "market",
  "content": {
    "headline": "A $24B Market.",
    "tam": {"value": "$24B", "description": "..."},
    "sam": {"value": "$4.8B", "description": "..."},
    "som": {"value": "$120M", "description": "..."}
  }
}
```

New (adds layout + visual):
```json
{
  "type": "market",
  "layout": "chart",
  "content": {
    "headline": "A $24B Market.",
    "tam": {"value": "$24B", "description": "..."},
    "sam": {"value": "$4.8B", "description": "..."},
    "som": {"value": "$120M", "description": "..."}
  },
  "visual": {
    "type": "bar_chart",
    "data": [
      {"label": "TAM", "value": 24, "unit": "B"},
      {"label": "SAM", "value": 4.8, "unit": "B"},
      {"label": "SOM", "value": 0.12, "unit": "B"}
    ]
  }
}
```

Both `layout` and `visual` are optional. If absent, current behavior is the fallback. Backwards compatible.

### Variant Selection: How the LLM Picks

The prompt includes a decision tree per slide type:

```
Solution slide layouts:
- "features": Use when the solution has 3-6 distinct capabilities. Grid of icon+title+desc cards.
- "before_after": Use when the value prop is a transformation (pain -> relief). Two columns.
- "steps": Use when the solution is a process (step 1 -> 2 -> 3). Numbered flow.
Pick based on the brief. Default: "features".
```

This is explicit guidance, not a random choice. The LLM sees descriptions of when each variant fits.

### Icon Assignment: LLM-Driven, Not Keyword

Current (broken): `auto_icon("Predictive Spoilage Engine")` -> star (no keyword match).

Fix: the LLM assigns icons in the content:
```json
{
  "features": [
    {"title": "Predictive Spoilage Engine", "description": "...", "icon": "trending-up"},
    {"title": "Automated Markdowns", "description": "...", "icon": "dollar-sign"}
  ]
}
```

The prompt includes the full icon list. The LLM picks the best match. The template uses `get_icon_svg(f.get("icon", "star"))` instead of `auto_icon()`.

Fallback: if no `icon` field, use keyword matching (current behavior). If keyword matching fails, use a deterministic rotation (not all stars).

### Content-to-Visual Mapping (Decision Tree)

| Slide type | Visual type | When to use |
|---|---|---|
| market | `bar_chart` | Always (TAM/SAM/SOM are numbers, charts are always better than text) |
| market | `funnel` | When the narrative is about narrowing focus (TAM -> wedge) |
| traction | `metric_row` | When there are 2-4 key metrics (ARR, users, NRR) |
| traction | `timeline` | When milestones are the focus (prototype -> beta -> launch) |
| funds | `pie_chart` | When allocation breakdown is the focus |
| funds | `bar_chart` | When comparing amounts across categories |
| comparison | `table` | When there are 4+ comparison dimensions |
| comparison | `quadrant` | When positioning on 2 axes (ease vs power) |
| solution | `features` | When 3-6 distinct capabilities |
| solution | `before_after` | When clear pain -> solution transformation |
| solution | `steps` | When the product is a process/workflow |
| problem | `stat_hero` | When there's a shocking stat ($450B wasted) |
| problem | `story` | When the narrative is personal/emotional |
| title | `split` | When company_url is provided (show product) |
| title | `text_only` | When no URL or the product is abstract |

This decision tree goes into the prompt. The LLM follows it.

## Phase 1: Multi-Variant Templates

### Slide Variants (2-3 per type)

**Title:**
- `text_only` - headline left, subtle gradient right (current)
- `split` - headline left (55%), product screenshot right (45%)
- `hero_stat` - headline + one massive stat number centered

**Problem:**
- `story` - narrative text + blocker cards with icons (current)
- `stat_hero` - large stat number (font-size 120px+) as hero, supporting text below
- `quote_lead` - customer quote as visual hero, pain points as cards below

**Solution:**
- `features` - icon+title+desc card grid (current, improved with icon boxes)
- `before_after` - two columns with contrasting styles (muted left, accent right)
- `steps` - numbered vertical flow with connector lines

**Market:**
- `boxes` - TAM/SAM/SOM boxes (current)
- `chart` - horizontal bar chart SVG + segment pills
- `funnel` - SVG funnel narrowing from TAM to SOM

**Competition:**
- `columns` - highlighted column cards (current)
- `table` - structured grid with check/x per cell, company logos in headers
- `quadrant` - 2x2 SVG scatter with labeled axes

**Traction:**
- `timeline` - status box + milestone dots (current)
- `metrics` - 3-4 hero numbers (64px+) in a row, with labels and change indicators
- `logo_bar` - customer/partner logos + key metric below each

**Funds:**
- `bars` - allocation bars + milestones (current)
- `pie` - SVG donut chart left, milestone list right
- `hero_ask` - massive ask number centered, breakdown cards below

**Team/Ask:**
- `split` - founder left, ask box right (current)
- `solo_hero` - founder name large, credentials as badges, ask below
- `grid` - 2-3 team members in cards (for multi-founder teams)

### Implementation Steps
1. Add `layout` field to SLIDE_SCHEMAS (optional, string enum per type)
2. Update prompts.py with variant descriptions and decision tree
3. Create variant functions in templates_modern.py
4. Update renderer dispatch in generator.py to route by layout
5. Test with 3 different industries

### Effort: 2 sessions

## Phase 2: SVG Visual Components

### Components

**`svg_bar_chart(data, accent_color, width, height)`**
- Horizontal bars with rounded ends
- Accent color for primary, muted for secondary
- Value labels right-aligned
- Max 6 bars
- Used in: market, traction, funds

**`svg_donut_chart(data, accent_color, width, height)`**
- Donut (not pie) with gap between segments
- Max 5 segments
- Center text for total/label
- Used in: funds allocation

**`svg_funnel(stages, accent_color, width, height)`**
- 3-4 trapezoid stages
- Narrowing from top to bottom
- Labels and values per stage
- Used in: market (TAM -> SAM -> SOM)

**`svg_timeline(milestones, accent_color, width)`**
- Horizontal line with dots
- Done (filled accent) / current (filled + ring) / upcoming (outline)
- Date labels above, title below
- Used in: traction, funds

**`svg_metric_row(metrics, accent_color)`**
- 2-4 large numbers (48-72px) in a horizontal row
- Label below each
- Optional change indicator (+15% YoY)
- Used in: traction, title hero stat

**`svg_quadrant(items, x_label, y_label, accent_color, width, height)`**
- 2x2 grid with axis labels
- Dots positioned by x,y coordinates
- "Us" dot is larger and accent-colored
- Used in: competition positioning

**`svg_comparison_grid(rows, columns, accent_column)`**
- Structured table: rows are features, columns are competitors
- Check icon (accent) / X icon (muted) / text per cell
- Highlighted column has accent background
- Company logos in header (from logo resolver)
- Used in: competition

### Implementation Steps
1. Create `openslides/svg.py` with all generators
2. Each function returns an inline SVG string (no external files)
3. All SVGs use theme colors (accent, text_primary, text_muted, surface)
4. Wire into template variants that declare visual type
5. Test with real data from generated decks

### Effort: 2-3 sessions

## Phase 3: Auto-Screenshot Integration

### What It Does
- Screenshots company_url at 1280x800
- Embeds as base64 PNG in the title_split variant
- Also used in solution slide as "what users see"

### Implementation
1. `images.screenshot_url(url)` already exists (needs Playwright)
2. Add to generator pipeline: if company_url provided, screenshot it
3. Pass screenshot data URI to title_split and solution_before_after templates
4. Fallback: if screenshot fails (timeout, error), use text_only variant

### Constraints
- Playwright on AX41 only
- 5-10s latency per screenshot
- Cookie banners, loading states degrade quality
- Add `--disable-notifications --disable-popup-blocking` flags

### Effort: 1 session

## Phase 4: Logo Grid for Competition

### What It Does
- LLM names competitors in comparison slide
- `resolve_logos()` fetches SVG/PNG for each
- Template embeds logos in column/table headers

### Implementation
1. After LLM generation, extract competitor names from comparison slide
2. Batch resolve via `resolve_logos(names)`
3. Pass resolved logo URLs to comparison template
4. Template uses `<img>` for PNG or inline SVG for SVG logos
5. Fallback: first letter in a circle (like avatar fallbacks)

### Effort: 0.5 session

## Phase 5: Gemini Auto-Fix Loop

### What It Does
1. Render deck to PNGs
2. Send to Gemini with rubric
3. Get per-slide scores + fixes
4. Map fixes to parameter changes
5. Re-render
6. Max 2 iterations

### Fix Mapping (the hard part)

| Gemini feedback | Mapped action |
|---|---|
| "Too much dead space" | Switch to a variant with more visual elements |
| "Headline too small" | Increase font-size in template |
| "No visual anchor" | Add chart/mockup if data available |
| "Colors clash" | Reduce accent usage, more neutral |
| "Text hard to read" | Increase contrast, reduce text density |
| "Slide looks empty" | Add more content or switch to metric_row variant |

### Implementation
1. Run auditor on generated deck
2. Parse per-slide fixes into actionable categories
3. Map categories to template parameter overrides
4. Re-render with overrides
5. Score again. If improved, keep. If not, revert.

### Effort: 2 sessions

## Performance Budget

| Phase | Added latency | Total |
|-------|--------------|-------|
| Baseline (LLM + render) | 15-30s | 15-30s |
| + SVG generation | <1s | 16-31s |
| + Logo resolution | 2-5s (cached after first) | 18-36s |
| + Auto-screenshot | 5-10s | 23-46s |
| + Gemini auto-fix (1 iteration) | 20-40s | 43-86s |

**Target:** Under 60s without auto-fix. Under 120s with auto-fix. Auto-fix is optional.

**Parallelization opportunities:**
- Logo resolution runs in parallel with LLM generation
- Screenshot runs in parallel with LLM generation
- SVG generation runs during template rendering (near-zero cost)
- Gemini audit is the only sequential bottleneck

## Font Fallback Strategy

Google Fonts requires network access. For reliable PDF rendering:

1. **Primary:** Google Fonts `<link>` tag (works when online)
2. **Fallback:** Base64-embedded font subsets for headline + body (2 fonts, ~200KB each)
3. **Last resort:** System font stack (`-apple-system, 'Segoe UI', sans-serif`)

Implementation: `theme.py` gets a `font_embed_mode` field: `"link"` (default), `"base64"`, `"system"`. PDF export uses `"base64"` to ensure fonts render correctly in Chrome headless.

Known Chrome headless issue: fonts sometimes don't load even with base64. Mitigation: `document.fonts.ready` wait + retry loop (already in export.py).

## Fallback Quality Guarantee

Every template variant must have a text-only fallback that scores at least 6/10 on its own. Fallbacks are not "broken" states, they're "clean minimal" states.

Rules:
- If screenshot fails -> text_only variant (not a broken image placeholder)
- If logo doesn't resolve -> first-letter circle avatar (not empty space)
- If SVG data is malformed -> skip the visual, show text-only layout (not a broken SVG)
- If icon field is missing -> rotate through 6 default icons (not all stars)
- Every fallback must be tested. Write a test that renders each slide type with minimal content (only required fields) and verifies it produces valid HTML with no empty containers.

## Brand Consistency Rules

When generating with a custom theme (from_brand or from_url):

1. **Accent color usage:** Max 3 elements per slide use the accent color. Rest are neutral. Accent overuse makes slides look like a color swatch.
2. **Dark slides:** Title and team_ask use dark bg. Accent color appears as text or small elements, not large fills. Exception: one accent-colored card per slide is OK.
3. **Light slides:** Background is always the warm/neutral bg from theme. Cards use surface color. Accent is for icons, highlights, chart bars.
4. **Font balance:** Headlines use headline font. Everything else uses body font. Never mix more than 2 font families on one slide.
5. **Logo dot:** Top-left uses accent color. Same size and position on every slide. Consistent brand anchor.

## Testing Strategy

### Automated (run on every change)
- `test_core.py`: 21 existing tests (schema, imports, basic rendering)
- New: `test_variants.py`: render each variant with minimal content, verify valid HTML, no empty containers
- New: `test_svg.py`: render each SVG component with sample data, verify valid SVG XML
- New: `test_fallbacks.py`: render each slide type with missing optional fields, verify graceful degradation

### Visual (run per session)
- Generate 3 decks (tech, consulting, consumer) with current code
- Screenshot all slides
- Gemini-score each deck
- Compare against baseline scores (track in `scores.json`)
- Regression = any slide scores lower than previous session

### Benchmark (run once at start, once at end)
- Generate equivalent deck on Gamma
- Screenshot and Gemini-score
- OpenSlides target: match or exceed Gamma per-slide scores

## Build Order

| # | Phase | Effort | Impact | Prerequisite |
|---|-------|--------|--------|---|
| 0 | Competitive benchmark (score Gamma) | 0.5 session | Baseline | None |
| 1a | Prompt update (layout choices, icon assignment, decision tree) | 0.5 session | HIGH | None |
| 1b | Template variants (2-3 per type) | 1.5 sessions | HIGH | 1a |
| 2a | SVG bar chart + metric row | 1 session | HIGH | None |
| 2b | SVG funnel + donut + timeline | 1 session | MEDIUM | 2a |
| 2c | SVG comparison grid + quadrant | 1 session | MEDIUM | 2b |
| 4 | Logo grid in competition | 0.5 session | MEDIUM | 2c |
| 3 | Auto-screenshot | 1 session | MEDIUM | 1b |
| 5 | Gemini auto-fix loop | 2 sessions | MEDIUM | All above |
| - | Final benchmark + polish | 0.5 session | Validation | All above |

Total: ~9-10 sessions.

Phases 1a, 2a can run in parallel (prompt changes don't depend on SVG code). Phase 0 should be first (establish the target).

## What's Already Done (Don't Redo)

- Engine: 14 modules, all working, 21/21 tests
- Content: few-shot prompting, 8/10 from single prompt
- Theme: from_url, from_brand, from_css, font propagation through dark/light slides
- Logos: SimpleIcons -> Clearbit -> Google chain, file cache
- Icons: 40+ Lucide icons in icons.py
- Visuals: code_block, browser_mockup, stat_badge, output_badges (built in visuals.py)
- Export: PDF (Playwright page.pdf + PyPDF2 merge) + PPTX (python-pptx), tested on AX41
- floom protocol: floom.yaml + floom_app.py + requirements.txt
- Modern templates: 12 slide types in templates_modern.py
- Normalizer: handles Gemini output format variations
- Validator: catches TAM>SAM>SOM, placeholders, missing fields

## Non-Goals

- Interactive editing (not an editor, it's a generator)
- Real-time collaboration
- Animation or transitions
- Video/audio embedding
- Custom user-created templates (future, not now)
- Supporting non-pitch deck types like resumes, reports, one-pagers (future)
- Image generation via AI (Gemini image gen is too slow and inconsistent for slide visuals)
