"""
Floom app entrypoint for OpenSlides.

Exposes three actions to the Floom runtime:
  - generate: build a branded pitch deck from a prompt (+ optional company URL).
  - iterate:  regenerate specific slides of a previously produced deck.
  - resolve_logo: look up the best logo for a company/domain.

The heavy lifting lives in the `openslides` package. This wrapper is
intentionally thin: it adapts the public functions to the Floom action
signature and base64-encodes the rendered PDF so it travels back through
the runtime JSON protocol.
"""

import base64
from pathlib import Path

from floom import app, context

# The stock Floom runtime image does not ship headless Chromium, so
# openslides.export.export_pdf_sync (which uses playwright) would crash the
# `generate` action. We replace it with a no-op before the openslides.main
# module is imported so the HTML slides still come back cleanly. When
# playwright IS available (custom image) the original function is preserved.
try:
    import openslides.export as _export_mod  # noqa: F401

    _original_export_pdf_sync = getattr(_export_mod, "export_pdf_sync", None)

    def _noop_export_pdf_sync(*args, **kwargs):  # noqa: ARG001
        return None

    try:
        import playwright  # noqa: F401
    except ImportError:
        _export_mod.export_pdf_sync = _noop_export_pdf_sync  # type: ignore[assignment]
except Exception:  # noqa: BLE001
    # If the export module itself blows up on import, we let generate_deck
    # surface the error on the first real call.
    pass

from openslides.main import generate_deck  # noqa: E402
from openslides.logos import resolve_logo as _resolve_logo  # noqa: E402


@app.action
def generate(
    prompt: str,
    company_url: str = "",
    audience: str = "vc",
    deck_type: str = "pitch",
) -> dict:
    """Generate a branded pitch deck from a prompt and optional company URL."""
    result = generate_deck(
        prompt=prompt,
        company_url=company_url or None,
        deck_type=deck_type,
        audience=audience,
        api_key=context.get_secret("GEMINI_API_KEY"),
    )

    output = {
        "deck_id": result.deck_id,
        "slide_count": len(result.html_slides),
        "slides": result.html_slides,
    }

    if result.pdf_path:
        pdf_file = Path(result.pdf_path)
        if pdf_file.exists():
            pdf_bytes = pdf_file.read_bytes()
            output["pdf_base64"] = base64.b64encode(pdf_bytes).decode("ascii")
            output["pdf_size_bytes"] = len(pdf_bytes)

    return output


@app.action
def iterate(deck_id: str, prompt: str, slide_indices: list) -> dict:
    """Regenerate specific slides from a previous deck."""
    result = generate_deck(
        prompt=prompt,
        previous_deck_id=deck_id,
        slides_to_regenerate=slide_indices,
        api_key=context.get_secret("GEMINI_API_KEY"),
    )

    output = {
        "deck_id": result.deck_id,
        "slide_count": len(result.html_slides),
    }

    if result.pdf_path:
        pdf_file = Path(result.pdf_path)
        if pdf_file.exists():
            pdf_bytes = pdf_file.read_bytes()
            output["pdf_base64"] = base64.b64encode(pdf_bytes).decode("ascii")
            output["pdf_size_bytes"] = len(pdf_bytes)

    return output


@app.action
def resolve_logo(name: str) -> dict:
    """Find the best logo for a company name or domain."""
    logo = _resolve_logo(name)
    if logo:
        return {"url": logo.url, "format": logo.format, "provider": logo.provider}
    return {"url": "", "format": "", "provider": "none"}
