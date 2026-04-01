"""
Publisher
Upload deck to aired.sh for shareable URL.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def publish_to_aired(html_slides: list[str], title: str = "Pitch Deck") -> str | None:
    """
    Publish HTML slides to aired.sh and return the shareable URL.

    Requires aired CLI to be installed: npm install -g aired
    Falls back gracefully if not available.

    Args:
        html_slides: list of HTML strings
        title: deck title for the aired page

    Returns:
        aired.sh URL or None if publishing failed
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write a combined HTML file with all slides
        combined = _build_viewer_html(html_slides, title)
        html_path = Path(tmpdir) / "index.html"
        html_path.write_text(combined)

        try:
            result = subprocess.run(
                ["aired", "upload", str(html_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                # Extract URL from output
                for line in result.stdout.strip().splitlines():
                    line = line.strip()
                    if line.startswith("http"):
                        return line
            return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None


def _build_viewer_html(slides: list[str], title: str) -> str:
    """Build a self-contained HTML viewer with all slides embedded."""
    slide_divs = []
    for i, html in enumerate(slides):
        # Extract body content from each slide HTML
        # We embed each slide in an iframe via srcdoc
        escaped = html.replace('"', '&quot;').replace("<", "&lt;").replace(">", "&gt;")
        slide_divs.append(
            f'<div class="slide-frame">'
            f'<iframe srcdoc="{escaped}" style="width:1920px;height:1080px;border:none;'
            f'transform-origin:top left;transform:scale(var(--scale));"></iframe>'
            f'</div>'
        )

    slides_html = "\n".join(slide_divs)

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #1a1a1a; display: flex; flex-direction: column; align-items: center; padding: 40px; }}
:root {{ --scale: 0.5; }}
.slide-frame {{
    width: calc(1920px * var(--scale));
    height: calc(1080px * var(--scale));
    margin: 20px 0;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 40px rgba(0,0,0,0.3);
}}
@media (min-width: 1400px) {{ :root {{ --scale: 0.65; }} }}
@media (min-width: 1800px) {{ :root {{ --scale: 0.8; }} }}
</style></head><body>
{slides_html}
</body></html>"""
