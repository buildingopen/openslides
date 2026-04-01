"""
Image Handler
Product screenshots, team photos, OG images.
"""
from __future__ import annotations

import asyncio
import base64
import tempfile
from pathlib import Path
from io import BytesIO

import httpx
from PIL import Image


def screenshot_url(url: str, width: int = 1280, height: int = 800) -> str | None:
    """
    Take a screenshot of a URL and return base64 PNG data URI.

    Returns None on failure.
    """
    try:
        b64 = asyncio.run(_async_screenshot(url, width, height))
        return f"data:image/png;base64,{b64}"
    except Exception:
        return None


async def _async_screenshot(url: str, width: int, height: int) -> str:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.goto(url, wait_until="networkidle", timeout=15000)
        png_bytes = await page.screenshot(type="png")
        await browser.close()
        return base64.b64encode(png_bytes).decode()


def fetch_image(url: str, max_width: int = 1920) -> str | None:
    """
    Fetch an image URL and return as optimized base64 PNG data URI.

    Resizes if wider than max_width. Returns None on failure.
    """
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))

        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

        # Convert to PNG bytes
        buf = BytesIO()
        img.save(buf, format="PNG", optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}"
    except Exception:
        return None


def extract_dominant_colors(image_url: str, count: int = 5) -> list[str]:
    """
    Extract dominant colors from an image URL.

    Returns list of hex color strings.
    """
    try:
        resp = httpx.get(image_url, timeout=10, follow_redirects=True)
        resp.raise_for_status()

        from colorthief import ColorThief
        ct = ColorThief(BytesIO(resp.content))
        palette = ct.get_palette(color_count=count, quality=10)
        return [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in palette]
    except Exception:
        return []
