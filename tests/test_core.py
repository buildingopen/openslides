"""Core tests for OpenSlides v2."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from openslides.theme import Theme, DarkTheme, LightTheme
from openslides.logos import resolve_logo, resolve_logos, LogoResult
from openslides.prompts import get_deck_prompt, SLIDE_SCHEMAS
from openslides.content_validator import validate_deck, apply_fixes, ValidationResult
from openslides.generator import DeckGenerator, BrandContext
from openslides.scraper import scrape_brand
from openslides.versions import save_deck, load_deck, list_decks


def test_theme_basics():
    t = LightTheme()
    assert t.background == "#FAFAF7"
    assert t.accent == "#059669"
    assert t.headline_font_family

    dt = DarkTheme()
    assert dt.background  # has a background
    assert dt.text_primary  # has text color


def test_theme_from_url():
    assert hasattr(Theme, "from_url")


def test_theme_from_brand():
    brand = BrandContext(colors={"accent": "#ff6600"})
    theme = Theme.from_brand(brand)
    assert theme.accent == "#ff6600"


def test_theme_from_brand_empty():
    brand = BrandContext()
    theme = Theme.from_brand(brand)
    assert theme.accent  # should have a default


def test_logo_resolve():
    logo = resolve_logo("docker")
    assert logo is not None
    assert logo.provider == "simpleicons"
    assert "docker" in logo.url


def test_logo_resolve_domain():
    logo = resolve_logo("stripe.com")
    assert logo is not None


def test_logo_batch():
    results = resolve_logos(["docker", "google", "nonexistent-xyz-123"])
    assert len(results) == 3
    assert results[0] is not None
    assert results[1] is not None


def test_schemas():
    assert "title" in SLIDE_SCHEMAS
    assert "problem" in SLIDE_SCHEMAS
    assert "solution" in SLIDE_SCHEMAS
    assert "market" in SLIDE_SCHEMAS
    assert "team_ask" in SLIDE_SCHEMAS
    for schema in SLIDE_SCHEMAS.values():
        assert "required" in schema


def test_prompt_generation():
    prompt = get_deck_prompt("Test brief", audience="vc")
    assert len(prompt) > 100
    assert "JSON" in prompt


def test_prompt_with_brand():
    prompt = get_deck_prompt(
        "Test brief",
        brand_context={"company_name": "TestCo", "description": "A test company"},
        audience="angel",
    )
    assert "TestCo" in prompt
    assert "angel" in prompt.lower() or "story" in prompt.lower()


def test_validator_valid():
    config = {
        "slides": [
            {"type": "title", "content": {
                "company_name": "Test", "headline": "H", "subheadline": "S",
            }},
        ]
    }
    result = validate_deck(config)
    assert len(result.errors) == 0


def test_validator_missing_field():
    config = {
        "slides": [
            {"type": "title", "content": {"company_name": "Test"}},
        ]
    }
    result = validate_deck(config)
    assert len(result.errors) > 0


def test_validator_placeholder():
    config = {
        "slides": [
            {"type": "title", "content": {
                "company_name": "Test", "headline": "TBD headline",
                "subheadline": "Lorem ipsum dolor sit amet",
            }},
        ]
    }
    result = validate_deck(config)
    assert len(result.warnings) > 0


def test_render():
    gen = DeckGenerator()
    config = {
        "slides": [
            {"type": "title", "theme": "dark", "content": {
                "company_name": "Test", "headline": "Hello World",
                "subheadline": "Testing", "bottom_items": ["2026"],
            }},
        ]
    }
    slides = gen.render(config, theme=LightTheme())
    assert len(slides) == 1
    assert "<body" in slides[0].lower()
    assert "Hello World" in slides[0]


def test_scraper():
    brand = scrape_brand("https://floom.dev")
    assert brand.domain == "floom.dev"
    assert brand.company_name
    assert brand.description


def test_versioning():
    config = {"slides": [{"type": "title", "content": {"headline": "V"}}]}
    deck_id = save_deck(config)
    assert deck_id
    loaded = load_deck(deck_id)
    assert loaded["slides"][0]["content"]["headline"] == "V"
    decks = list_decks()
    assert any(d["deck_id"] == deck_id for d in decks)


def test_font_theming():
    """Custom fonts appear in rendered HTML."""
    gen = DeckGenerator()
    custom = Theme.from_brand({"primary": "#ff6600", "headline_font": "Playfair Display", "body_font": "Roboto"})
    config = {
        "slides": [
            {"type": "title", "theme": "dark", "content": {
                "company_name": "Test", "headline": "H", "subheadline": "S",
            }},
        ]
    }
    slides = gen.render(config, theme=custom)
    assert "Roboto" in slides[0], "Custom body font not in output"
    assert "Playfair" in slides[0], "Custom headline font not in output"


def test_all_slide_types_render():
    """Every slide type renders without error."""
    from openslides.components import SlideBuilder
    gen = DeckGenerator()
    config = {
        "slides": [
            {"type": "title", "theme": "dark", "content": {
                "company_name": "T", "headline": "H", "subheadline": "S",
            }},
            {"type": "problem", "content": {
                "headline": "H", "story_html": "<p>S</p>",
            }},
            {"type": "solution", "content": {
                "headline": "H", "subheadline": "S",
                "features": [{"title": "F1", "description": "D1"}],
            }},
            {"type": "market", "content": {
                "headline": "H",
                "tam": {"value": "$24B", "description": "D"},
                "sam": {"value": "$4B", "description": "D"},
                "som": {"value": "$100M", "description": "D"},
            }},
            {"type": "comparison", "content": {
                "headline": "H",
                "columns": [
                    {"name": "Us", "items": [{"text": "Good", "good": True}]},
                    {"name": "Them", "items": [{"text": "Bad", "good": False}]},
                ],
            }},
            {"type": "traction", "content": {
                "headline": "H",
                "label": "Traction",
            }},
            {"type": "team_ask", "theme": "dark", "content": {
                "founder_name": "F", "founder_title": "CEO",
                "bio_items": [{"company": "C", "detail": "D"}],
                "ask_amount": "$200K", "ask_uses": ["MVP"],
            }},
        ]
    }
    slides = gen.render(config, theme=LightTheme())
    assert len(slides) == 7, f"Expected 7 slides, got {len(slides)}"
    for i, s in enumerate(slides):
        assert "<body" in s.lower(), f"Slide {i} missing body tag"


def test_theme_from_css():
    """Theme.from_css parses CSS custom properties."""
    css = ":root { --accent: #ff0000; --background: #ffffff; --text-primary: #000000; }"
    theme = Theme.from_css(css)
    assert theme.accent == "#ff0000"


def test_validator_tam_sam_som():
    """Validator catches TAM < SAM."""
    config = {
        "slides": [
            {"type": "market", "content": {
                "headline": "H",
                "tam": {"value": "$1B", "description": "D"},
                "sam": {"value": "$10B", "description": "D"},
                "som": {"value": "$100M", "description": "D"},
            }},
        ]
    }
    result = validate_deck(config)
    has_tam_warning = any("TAM" in w or "tam" in w.lower() for w in result.warnings + result.errors)
    # TAM ($1B) < SAM ($10B) should trigger a warning
    assert has_tam_warning, f"Should warn about TAM < SAM, got: {result.warnings + result.errors}"


def test_brand_context_scrape_and_theme():
    """Full pipeline: scrape -> theme -> render."""
    brand = scrape_brand("https://floom.dev")
    theme = Theme.from_brand(brand)
    gen = DeckGenerator()
    config = {
        "slides": [
            {"type": "title", "theme": "dark", "content": {
                "company_name": brand.company_name or "floom",
                "headline": "Test", "subheadline": "Test",
            }},
        ]
    }
    slides = gen.render(config, theme=theme)
    assert len(slides) == 1
    assert "fonts.googleapis.com" in slides[0]


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
