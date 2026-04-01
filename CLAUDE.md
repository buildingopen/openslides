# OpenSlides v2 - AI Context

## What This Is

Python library + CLI + floom app for generating branded pitch decks from a prompt + company URL.

**Core flow:** `prompt + company_url -> scrape brand -> generate content (Claude) -> render HTML -> export PDF/PPTX -> audit (Gemini) -> publish (aired.sh)`

## Architecture

```
openslides/
  main.py             # Entry point, generate_deck() function, CLI
  theme.py            # Design system tokens, Theme dataclass, from_url/from_brand/from_css
  components.py       # 16 HTML slide type renderers (9,400 lines, from v1)
  generator.py        # LLM orchestration, BrandContext, partial regen
  content_validator.py # Validates LLM output (TAM>SAM>SOM, no placeholders, etc.)
  prompts.py          # System prompts for Claude, audience-aware
  logos.py            # Logo resolution: SimpleIcons -> Clearbit -> Google favicon
  images.py           # Product screenshots, team photos, color extraction
  export.py           # PDF (Playwright), PPTX (python-pptx), PNG
  scraper.py          # Brand extraction from company URL
  auditor.py          # Gemini visual scoring per slide
  publish.py          # aired.sh upload
  versions.py         # Deck versioning for iteration
```

## Key Design Decisions

- **Theme tokens**: components.py uses Theme dataclass values. `{theme.accent}`, `{theme.background}` etc.
- **Logo chain**: SimpleIcons (SVG) > Clearbit (PNG) > Google favicon. Cache in ~/.openslides/logo_cache/
- **PDF export**: Playwright page.pdf() (preserves text) + PyPDF2 merge + link annotations
- **PPTX**: Render to PNG, embed in PowerPoint slides (visual fidelity over editability)
- **Validation**: content_validator.py checks LLM output before rendering. Fields are in slide["content"], not slide root.
- **Versioning**: Each deck gets a UUID, stored in ~/.openslides/decks/

## floom Interface

```python
def generate_deck(
    prompt: str,
    company_url: str = None,
    design_system_url: str = None,
    recipient: str = None,
    deck_type: str = "pitch",      # pitch | sales | update | general
    audience: str = "vc",          # vc | angel | ff | customer
    slides_to_regenerate: list[int] = None,
    previous_deck_id: str = None,
    format: str = "all",           # html | pdf | pptx | all
    audit: bool = False,
    publish: bool = False,
) -> DeckResult
```

## Dependencies

anthropic, playwright, httpx, Pillow, PyPDF2, python-pptx, colorthief
Optional: google-genai (for audit)

## Common Tasks

- Add slide type: add renderer to components.py, add schema to SLIDE_SCHEMAS in prompts.py
- Add logo provider: add _try_X function to logos.py, add to resolve_logo chain
- Change theme defaults: edit LightTheme/DarkTheme in theme.py
