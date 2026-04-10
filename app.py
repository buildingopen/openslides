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
import json
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

    # Build a single HTML preview document from all slides
    preview_parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        "<style>",
        "body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }",
        ".slide { background: #fff; padding: 40px; margin: 0 auto 24px; max-width: 960px; ",
        "  border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }",
        ".slide iframe { width: 100%; height: 600px; border: none; }",
        ".slide-divider { border: none; border-top: 1px solid #e0e0e0; margin: 0; }",
        "</style></head><body>",
    ]
    for i, slide_html in enumerate(result.html_slides):
        if i > 0:
            preview_parts.append('<hr class="slide-divider">')
        # Each slide is a full HTML doc; embed via srcdoc iframe for isolation
        escaped = slide_html.replace("&", "&amp;").replace('"', "&quot;")
        preview_parts.append(f'<div class="slide"><iframe srcdoc="{escaped}"></iframe></div>')
    preview_parts.append("</body></html>")

    output = {
        "preview": "\n".join(preview_parts),
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
def iterate(deck_id: str, prompt: str, slide_indices) -> dict:
    """Regenerate specific slides from a previous deck.

    `slide_indices` may be either a Python list of ints or a JSON-encoded
    string (e.g. from a textarea input like "[0, 2, 4]").
    """
    if isinstance(slide_indices, str):
        try:
            slide_indices = json.loads(slide_indices)
        except json.JSONDecodeError:
            return {"error": "slide_indices must be a JSON array of integers"}
    if not isinstance(slide_indices, list):
        return {"error": "slide_indices must be a list"}

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
