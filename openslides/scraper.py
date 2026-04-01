"""
Brand/Website Scraper
Extracts brand context from a company URL: colors, fonts, logo, product info, team.
"""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

import httpx

from .generator import BrandContext


def scrape_brand(url: str, timeout: float = 15.0) -> BrandContext:
    """
    Scrape brand information from a company URL.

    Extracts: meta tags, OG image, colors from CSS, fonts, product description.
    Falls back gracefully on failure.
    """
    ctx = BrandContext()

    parsed = urlparse(url)
    ctx.domain = parsed.netloc or parsed.path
    if ctx.domain.startswith("www."):
        ctx.domain = ctx.domain[4:]

    try:
        resp = httpx.get(url, timeout=timeout, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (compatible; OpenSlides/2.0)"
        })
        resp.raise_for_status()
        html = resp.text
    except Exception:
        return ctx

    # Company name from <title> or og:site_name
    ctx.company_name = _extract_meta(html, "og:site_name") or _extract_title(html) or ctx.domain

    # Description
    ctx.description = (
        _extract_meta(html, "og:description")
        or _extract_meta(html, "description")
        or ""
    )

    # Tagline from h1
    ctx.tagline = _extract_first_tag(html, "h1") or ""

    # OG image
    og_img = _extract_meta(html, "og:image")
    if og_img:
        ctx.og_image = urljoin(url, og_img)

    # Favicon as logo fallback
    favicon = _extract_favicon(html, url)
    if favicon:
        ctx.logo_url = favicon

    # Colors from CSS custom properties
    ctx.colors = _extract_css_colors(html)

    # Fonts from Google Fonts links
    ctx.fonts = _extract_google_fonts(html)

    # Features from meta keywords or h2/h3 headings
    ctx.features = _extract_headings(html, "h2")[:6]

    return ctx


def scrape_team_page(base_url: str, timeout: float = 15.0) -> list[dict]:
    """Try to find and scrape a team/about page."""
    team = []
    for path in ["/team", "/about", "/about-us", "/people"]:
        try:
            resp = httpx.get(
                urljoin(base_url, path),
                timeout=timeout,
                follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (compatible; OpenSlides/2.0)"},
            )
            if resp.status_code == 200 and len(resp.text) > 500:
                # Extract names from common patterns
                names = re.findall(
                    r'<(?:h[2-4]|strong|b)[^>]*>\s*([A-Z][a-z]+ [A-Z][a-z]+)\s*</',
                    resp.text,
                )
                for name in names[:5]:
                    team.append({"name": name})
                if team:
                    return team
        except Exception:
            continue
    return team


def scrape_pricing_page(base_url: str, timeout: float = 15.0) -> list[dict]:
    """Try to find and scrape a pricing page."""
    pricing = []
    for path in ["/pricing", "/plans", "/price"]:
        try:
            resp = httpx.get(
                urljoin(base_url, path),
                timeout=timeout,
                follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (compatible; OpenSlides/2.0)"},
            )
            if resp.status_code == 200:
                # Extract price patterns
                prices = re.findall(r"\$(\d+(?:,\d+)?(?:\.\d+)?)\s*/?(?:mo|month|yr|year)?", resp.text)
                for p in prices[:4]:
                    pricing.append({"price": f"${p}"})
                if pricing:
                    return pricing
        except Exception:
            continue
    return pricing


# --- Extraction helpers ---

def _extract_meta(html: str, name: str) -> str:
    """Extract content from meta tag by name or property."""
    patterns = [
        rf'<meta\s+(?:name|property)=["\'](?:og:)?{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']',
        rf'<meta\s+content=["\']([^"\']*)["\'].*?(?:name|property)=["\'](?:og:)?{re.escape(name)}["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def _extract_title(html: str) -> str:
    match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        # Remove common suffixes like " - Home", " | Company"
        title = re.split(r"\s*[-|]\s*", title)[0].strip()
        return title
    return ""


def _extract_first_tag(html: str, tag: str) -> str:
    match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.IGNORECASE | re.DOTALL)
    if match:
        text = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        return text[:200]
    return ""


def _extract_headings(html: str, tag: str) -> list[str]:
    matches = re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.IGNORECASE | re.DOTALL)
    results = []
    for m in matches:
        text = re.sub(r"<[^>]+>", "", m).strip()
        if text and len(text) < 100:
            results.append(text)
    return results


def _extract_favicon(html: str, base_url: str) -> str:
    match = re.search(
        r'<link[^>]+rel=["\'](?:icon|shortcut icon|apple-touch-icon)["\'][^>]+href=["\']([^"\']+)["\']',
        html, re.IGNORECASE,
    )
    if match:
        return urljoin(base_url, match.group(1))
    # Default favicon path
    return urljoin(base_url, "/favicon.ico")


def _extract_css_colors(html: str) -> dict:
    """Extract CSS custom properties that look like colors."""
    colors = {}
    # Look for :root { --var: #hex; } patterns
    root_match = re.search(r":root\s*\{([^}]+)\}", html, re.IGNORECASE)
    if root_match:
        props = root_match.group(1)
        for match in re.finditer(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})", props):
            name = match.group(1).replace("-", "_")
            colors[name] = match.group(2)

    # Also try inline style vars
    for match in re.finditer(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})", html):
        name = match.group(1).replace("-", "_")
        if name not in colors:
            colors[name] = match.group(2)

    return colors


def _extract_google_fonts(html: str) -> dict:
    """Extract font families from Google Fonts links."""
    fonts = {}
    matches = re.findall(
        r"fonts\.googleapis\.com/css2?\?family=([^\"'&]+)",
        html, re.IGNORECASE,
    )
    families = []
    for m in matches:
        for part in m.split("&family="):
            family = part.split(":")[0].replace("+", " ")
            families.append(family)

    if families:
        fonts["families"] = families
        if len(families) >= 1:
            fonts["headline_family"] = families[0]
        if len(families) >= 2:
            fonts["body_family"] = families[1]

    return fonts
