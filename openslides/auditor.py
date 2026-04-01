"""
Visual Auditor
Screenshots slides and sends to Gemini for independent scoring.
"""
from __future__ import annotations

import asyncio
import base64
import tempfile
from pathlib import Path

from .main import AuditResult


AUDIT_PROMPT = """You are a professional pitch deck design auditor. Score each slide independently.

For each slide screenshot, evaluate on these dimensions (1-10 each):
1. Visual Hierarchy: Is there one clear hero element? Can you identify the key message in 2 seconds?
2. Typography: Font sizing appropriate? Clear headline/body/label hierarchy?
3. Color Usage: Accent color used purposefully? Not too many colors?
4. Whitespace: Proper breathing room? No cramped elements? No dead space?
5. Professionalism: Would this look designed, not AI-generated? Would an investor take this seriously?
6. Readability: Can all text be read at presentation distance? Sufficient contrast?
7. Brand Consistency: Does it feel like part of a cohesive deck?

For each slide, return:
- Overall score (weighted average, 1-10)
- Top 3 specific, actionable fixes

Then provide:
- Overall deck score (1-10)
- "Ship" or "Iterate" recommendation
- Top 3 deck-level fixes

Return as JSON:
{
  "slides": [
    {"slide": 1, "score": 8.5, "fixes": ["Increase headline size to 56px", "Add more padding left", "Reduce body text"]},
    ...
  ],
  "overall": 8.2,
  "recommendation": "Ship",
  "deck_fixes": ["Inconsistent heading sizes across slides", ...]
}"""


def audit_slides(html_slides: list[str]) -> AuditResult:
    """
    Audit slides using Gemini vision.

    Renders each slide to PNG, sends to Gemini for scoring.
    Requires google-genai package.
    """
    import os

    try:
        from google import genai
    except ImportError:
        raise ImportError("Install google-genai for auditing: pip install 'openslides[audit]'")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable required for auditing")

    # Render slides to PNGs
    pngs = asyncio.run(_render_pngs(html_slides))

    # Build Gemini request with images
    client = genai.Client(api_key=api_key)

    parts = [AUDIT_PROMPT]
    for i, png_path in enumerate(pngs):
        png_bytes = Path(png_path).read_bytes()
        b64 = base64.b64encode(png_bytes).decode()
        parts.append(f"\n\nSlide {i + 1}:")
        parts.append({"inline_data": {"mime_type": "image/png", "data": b64}})

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=parts,
    )

    # Parse response
    import json
    import re

    text = response.text
    json_match = re.search(r"\{[\s\S]*\}", text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            result = AuditResult(
                scores=data.get("slides", []),
                overall=data.get("overall", 0),
                recommendation=data.get("recommendation", ""),
            )
            return result
        except json.JSONDecodeError:
            pass

    return AuditResult(recommendation="Could not parse audit response")


async def _render_pngs(html_slides: list[str]) -> list[str]:
    """Render slides to temporary PNGs for auditing."""
    from .export import ExportEngine

    tmpdir = tempfile.mkdtemp(prefix="openslides-audit-")
    async with ExportEngine() as engine:
        paths = await engine.export_png(html_slides, tmpdir)
    return [str(p) for p in paths]
