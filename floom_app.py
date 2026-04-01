"""floom app wrapper for OpenSlides."""
from floom import app, context
from openslides.main import generate_deck
from openslides.logos import resolve_logo as _resolve_logo
from openslides.versions import load_deck
from openslides.generator import DeckGenerator


@app.action
def generate(
    prompt: str,
    company_url: str = None,
    design_system_url: str = None,
    recipient: str = None,
    deck_type: str = "pitch",
    audience: str = "vc",
    format: str = "all",
) -> dict:
    """Generate a branded pitch deck from a prompt and optional company URL."""
    result = generate_deck(
        prompt=prompt,
        company_url=company_url,
        design_system_url=design_system_url,
        recipient=recipient,
        deck_type=deck_type,
        audience=audience,
        format=format,
        api_key=context.get_secret("GEMINI_API_KEY"),
    )
    return {
        "deck_id": result.deck_id,
        "slide_count": len(result.html_slides),
        "pdf_url": result.pdf_path,
        "slides": result.html_slides,
    }


@app.action
def iterate(deck_id: str, prompt: str, slide_indices: list[int]) -> dict:
    """Regenerate specific slides from a previous deck."""
    result = generate_deck(
        prompt=prompt,
        previous_deck_id=deck_id,
        slides_to_regenerate=slide_indices,
        api_key=context.get_secret("GEMINI_API_KEY"),
    )
    return {"deck_id": result.deck_id, "slide_count": len(result.html_slides)}


@app.action
def resolve_logo(name: str) -> dict:
    """Find the best logo for a company name or domain."""
    logo = _resolve_logo(name)
    if logo:
        return {"url": logo.url, "format": logo.format, "provider": logo.provider}
    return {"url": "", "format": "", "provider": "none"}
