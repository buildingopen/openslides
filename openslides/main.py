"""
OpenSlides Main Entry Point
The floom script interface: prompt + URL -> branded pitch deck.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AuditResult:
    """Per-slide audit scores from Gemini."""
    scores: list[dict] = field(default_factory=list)  # [{slide: int, score: float, fixes: [str]}]
    overall: float = 0.0
    recommendation: str = ""


@dataclass
class DeckResult:
    """Result of deck generation."""
    deck_id: str = ""
    html_slides: list[str] = field(default_factory=list)
    html_paths: list[str] = field(default_factory=list)
    pdf_path: str = ""
    pptx_path: str = ""
    aired_url: str = ""
    audit: AuditResult | None = None
    config: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def generate_deck(
    prompt: str,
    company_url: str | None = None,
    design_system_url: str | None = None,
    recipient: str | None = None,
    deck_type: str = "pitch",
    audience: str = "vc",
    slides_to_regenerate: list[int] | None = None,
    previous_deck_id: str | None = None,
    format: str = "all",
    audit: bool = False,
    publish: bool = False,
    output_dir: str | None = None,
    api_key: str | None = None,
) -> DeckResult:
    """
    Generate a branded pitch deck from a prompt and optional company URL.

    This is the main floom interface. When deployed on floom, it becomes:
    - Web UI: form with prompt + URL fields
    - REST API: POST /generate
    - MCP tool: generate_deck(prompt=..., company_url=...)

    Args:
        prompt: what the deck is about ("Raising $200K pre-seed for AI deploy platform")
        company_url: company website to scrape brand from
        design_system_url: explicit design system JSON URL
        recipient: name for title slide personalization
        deck_type: "pitch" | "sales" | "update" | "general"
        audience: "vc" | "angel" | "ff" | "customer"
        slides_to_regenerate: list of 0-based slide indices to redo (for iteration)
        previous_deck_id: deck ID to iterate on
        format: "html" | "pdf" | "pptx" | "all"
        audit: run Gemini visual audit
        publish: upload to aired.sh
        output_dir: where to save files (defaults to ~/.openslides/output/)
        api_key: Gemini API key (defaults to GEMINI_API_KEY env var)

    Returns:
        DeckResult with paths to generated files
    """
    from .generator import DeckGenerator, BrandContext
    from .theme import Theme, LightTheme
    from .scraper import scrape_brand
    from .versions import save_deck, load_deck

    result = DeckResult()
    output_dir = Path(output_dir or Path.home() / ".openslides" / "output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Step 1: Brand context ---
    brand = BrandContext()
    if company_url:
        print(f"Scraping brand from {company_url}...", file=sys.stderr)
        brand = scrape_brand(company_url)

    # --- Step 2: Theme ---
    theme = LightTheme()
    if design_system_url:
        print(f"Loading design system from {design_system_url}...", file=sys.stderr)
        theme = Theme.from_url(design_system_url)
    elif brand.colors or brand.fonts:
        theme = Theme.from_brand(brand)

    # --- Step 3: Generate content ---
    gen = DeckGenerator(api_key=api_key)

    if slides_to_regenerate and previous_deck_id:
        print(f"Iterating on deck {previous_deck_id}, regenerating slides {slides_to_regenerate}...", file=sys.stderr)
        prev_config = load_deck(previous_deck_id)
        config = gen.generate_partial(
            prompt=prompt,
            previous_config=prev_config,
            slide_indices=slides_to_regenerate,
            brand=brand,
            audience=audience,
        )
    else:
        print(f"Generating {deck_type} deck for audience: {audience}...", file=sys.stderr)
        config = gen.generate(
            prompt=prompt,
            brand=brand,
            audience=audience,
            deck_type=deck_type,
        )

    result.config = config

    # --- Step 4: Personalize ---
    if recipient:
        for slide in config.get("slides", []):
            content = slide.get("content", {})
            if slide.get("type") == "title":
                if "bottom_items" in content:
                    content["bottom_items"].append(f"For {recipient}")

    # --- Step 5: Render HTML ---
    print("Rendering slides...", file=sys.stderr)
    html_slides = gen.render(config, theme=theme)
    result.html_slides = html_slides

    # Save HTML files
    html_paths = []
    for i, html in enumerate(html_slides, 1):
        path = output_dir / f"slide-{i:02d}.html"
        path.write_text(html)
        html_paths.append(str(path))
    result.html_paths = html_paths

    # --- Step 6: Version ---
    from dataclasses import asdict
    deck_id = save_deck(config)
    result.deck_id = deck_id
    print(f"Saved as deck {deck_id}", file=sys.stderr)

    # --- Step 7: Export ---
    if format in ("pdf", "all"):
        print("Exporting PDF...", file=sys.stderr)
        from .export import export_pdf_sync
        pdf_path = output_dir / "deck.pdf"
        export_pdf_sync(html_slides, pdf_path)
        result.pdf_path = str(pdf_path)

    if format in ("pptx", "all"):
        print("Exporting PPTX...", file=sys.stderr)
        from .export import export_pptx
        pptx_path = output_dir / "deck.pptx"
        export_pptx(html_slides, pptx_path)
        result.pptx_path = str(pptx_path)

    # --- Step 8: Audit ---
    if audit:
        print("Running visual audit...", file=sys.stderr)
        try:
            from .auditor import audit_slides
            result.audit = audit_slides(html_slides)
        except ImportError:
            result.warnings.append("Gemini audit skipped: google-genai not installed")

    # --- Step 9: Publish ---
    if publish:
        print("Publishing to aired.sh...", file=sys.stderr)
        from .publish import publish_to_aired
        company = brand.company_name or "Pitch Deck"
        url = publish_to_aired(html_slides, title=f"{company} - Pitch Deck")
        if url:
            result.aired_url = url
            print(f"Published: {url}", file=sys.stderr)
        else:
            result.warnings.append("Publishing failed (is aired CLI installed?)")

    # --- Done ---
    print(f"\nDeck generated: {len(html_slides)} slides", file=sys.stderr)
    if result.pdf_path:
        print(f"  PDF: {result.pdf_path}", file=sys.stderr)
    if result.pptx_path:
        print(f"  PPTX: {result.pptx_path}", file=sys.stderr)
    if result.aired_url:
        print(f"  URL: {result.aired_url}", file=sys.stderr)
    if result.warnings:
        for w in result.warnings:
            print(f"  Warning: {w}", file=sys.stderr)

    return result


def cli():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="OpenSlides - Prompt + URL -> branded pitch deck",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", help="What the deck is about")
    parser.add_argument("--url", help="Company URL to scrape brand from")
    parser.add_argument("--design-system", help="Design system JSON URL")
    parser.add_argument("--recipient", help="Recipient name for personalization")
    parser.add_argument("--type", default="pitch", choices=["pitch", "sales", "update", "general"])
    parser.add_argument("--audience", default="vc", choices=["vc", "angel", "ff", "customer"])
    parser.add_argument("--format", default="all", choices=["html", "pdf", "pptx", "all"])
    parser.add_argument("--audit", action="store_true", help="Run Gemini visual audit")
    parser.add_argument("--publish", action="store_true", help="Publish to aired.sh")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--iterate", help="Previous deck ID to iterate on")
    parser.add_argument("--regen", help="Comma-separated slide indices to regenerate (0-based)")

    args = parser.parse_args()

    slides_to_regen = None
    if args.regen:
        slides_to_regen = [int(x.strip()) for x in args.regen.split(",")]

    result = generate_deck(
        prompt=args.prompt,
        company_url=args.url,
        design_system_url=args.design_system,
        recipient=args.recipient,
        deck_type=args.type,
        audience=args.audience,
        slides_to_regenerate=slides_to_regen,
        previous_deck_id=args.iterate,
        format=args.format,
        audit=args.audit,
        publish=args.publish,
        output_dir=args.output,
    )

    return result


if __name__ == "__main__":
    cli()
