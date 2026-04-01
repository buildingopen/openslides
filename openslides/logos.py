"""
Logo Resolution
Resolve company names/domains to logo images via multiple providers.
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

CACHE_DIR = Path("~/.openslides/logo_cache").expanduser()

# Timeout for each HTTP request (seconds)
REQUEST_TIMEOUT = 5.0


@dataclass
class LogoResult:
    """Result of a logo resolution."""
    url: str
    format: str  # "svg" or "png"
    provider: str
    cached_path: Path | None = None


def _normalize_name(name_or_domain: str) -> str:
    """
    Normalize a company name to a simple lowercase slug for SimpleIcons.

    "Google for Startups" -> "google"
    "Docker Inc." -> "docker"
    "VS Code" -> "vscode"
    """
    # Strip common suffixes
    cleaned = re.sub(
        r"\b(inc\.?|corp\.?|ltd\.?|llc|gmbh|for\s+\w+)\b",
        "",
        name_or_domain,
        flags=re.IGNORECASE,
    )
    # Keep only alphanumeric, collapse whitespace, lowercase
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "", cleaned).lower()
    return cleaned


def _extract_domain(value: str) -> str | None:
    """
    Extract a bare domain from a URL or domain string.

    "https://stripe.com/pricing" -> "stripe.com"
    "stripe.com" -> "stripe.com"
    "Google" -> None
    """
    # If it looks like a URL, parse it
    if "://" in value:
        parsed = urlparse(value)
        if parsed.hostname:
            return parsed.hostname.removeprefix("www.")
        return None

    # If it has a dot and no spaces, treat as domain
    if "." in value and " " not in value:
        return value.removeprefix("www.")

    return None


def _cache_key(provider: str, identifier: str, color: str | None) -> str:
    """Generate a stable filename for caching."""
    raw = f"{provider}:{identifier}:{color or 'default'}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    safe_id = re.sub(r"[^a-zA-Z0-9_.-]", "_", identifier)[:50]
    return f"{provider}_{safe_id}_{h}"


def _ensure_cache_dir() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def _get_cached(cache_key: str) -> Path | None:
    """Check if a cached file exists, return its path."""
    cache_dir = _ensure_cache_dir()
    # Check for both svg and png
    for ext in ("svg", "png"):
        path = cache_dir / f"{cache_key}.{ext}"
        if path.exists() and path.stat().st_size > 0:
            return path
    return None


def _save_to_cache(cache_key: str, data: bytes, fmt: str) -> Path:
    """Save logo data to cache, return the file path."""
    cache_dir = _ensure_cache_dir()
    path = cache_dir / f"{cache_key}.{fmt}"
    path.write_bytes(data)
    return path


def _try_simpleicons(
    client: httpx.Client,
    name: str,
    color: str | None,
) -> LogoResult | None:
    """
    Try SimpleIcons CDN. Best for tech brands, returns SVG.

    URL format: https://cdn.simpleicons.org/{name}/{color}
    """
    slug = _normalize_name(name)
    if not slug:
        return None

    key = _cache_key("simpleicons", slug, color)
    cached = _get_cached(key)
    if cached:
        url = f"https://cdn.simpleicons.org/{slug}"
        if color:
            url += f"/{color}"
        return LogoResult(
            url=url,
            format="svg",
            provider="simpleicons",
            cached_path=cached,
        )

    url = f"https://cdn.simpleicons.org/{slug}"
    if color:
        url += f"/{color}"

    try:
        resp = client.get(url, follow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 50:
            path = _save_to_cache(key, resp.content, "svg")
            return LogoResult(
                url=url,
                format="svg",
                provider="simpleicons",
                cached_path=path,
            )
    except httpx.HTTPError:
        logger.debug("SimpleIcons failed for %s", slug)

    return None


def _try_clearbit(
    client: httpx.Client,
    domain: str,
) -> LogoResult | None:
    """
    Try Clearbit Logo API. Good quality PNG, free.

    URL format: https://logo.clearbit.com/{domain}
    """
    if not domain:
        return None

    key = _cache_key("clearbit", domain, None)
    cached = _get_cached(key)
    if cached:
        return LogoResult(
            url=f"https://logo.clearbit.com/{domain}",
            format="png",
            provider="clearbit",
            cached_path=cached,
        )

    url = f"https://logo.clearbit.com/{domain}"
    try:
        resp = client.get(url, follow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 100:
            content_type = resp.headers.get("content-type", "")
            if "image" in content_type or len(resp.content) > 500:
                path = _save_to_cache(key, resp.content, "png")
                return LogoResult(
                    url=url,
                    format="png",
                    provider="clearbit",
                    cached_path=path,
                )
    except httpx.HTTPError:
        logger.debug("Clearbit failed for %s", domain)

    return None


def _try_google_favicon(
    client: httpx.Client,
    domain: str,
) -> LogoResult | None:
    """
    Try Google Favicon service. Always works, lower quality.

    URL format: https://www.google.com/s2/favicons?domain={domain}&sz=128
    """
    if not domain:
        return None

    key = _cache_key("google_favicon", domain, None)
    cached = _get_cached(key)
    if cached:
        return LogoResult(
            url=f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
            format="png",
            provider="google_favicon",
            cached_path=cached,
        )

    url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
    try:
        resp = client.get(url, follow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 0:
            path = _save_to_cache(key, resp.content, "png")
            return LogoResult(
                url=url,
                format="png",
                provider="google_favicon",
                cached_path=path,
            )
    except httpx.HTTPError:
        logger.debug("Google favicon failed for %s", domain)

    return None


def _guess_domain(name: str) -> str | None:
    """
    Guess a domain from a company name.

    "Google" -> "google.com"
    "Stripe" -> "stripe.com"
    """
    slug = _normalize_name(name)
    if slug:
        return f"{slug}.com"
    return None


def resolve_logo(
    name_or_domain: str,
    color: str | None = None,
) -> LogoResult | None:
    """
    Resolve a company name or domain to a logo image.

    Tries providers in order:
    1. SimpleIcons (SVG, best for tech brands)
    2. Clearbit (PNG, good quality)
    3. Google Favicon (PNG, always works)

    Args:
        name_or_domain: Company name ("Google"), domain ("google.com"),
                        or URL ("https://google.com/about")
        color: Optional hex color for SimpleIcons (without #), e.g. "4285F4"

    Returns:
        LogoResult on success, None if all providers fail.
    """
    if not name_or_domain or not name_or_domain.strip():
        return None

    name_or_domain = name_or_domain.strip()

    with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
        # 1. Try SimpleIcons (works with names)
        result = _try_simpleicons(client, name_or_domain, color)
        if result:
            return result

        # Figure out domain for Clearbit and Google
        domain = _extract_domain(name_or_domain)
        if not domain:
            domain = _guess_domain(name_or_domain)

        # 2. Try Clearbit (needs domain)
        result = _try_clearbit(client, domain)
        if result:
            return result

        # 3. Try Google Favicon (needs domain, almost always works)
        result = _try_google_favicon(client, domain)
        if result:
            return result

    return None


def resolve_logos(items: list[str], color: str | None = None) -> list[LogoResult | None]:
    """
    Batch resolve logos for multiple names/domains.

    Args:
        items: List of company names or domains.
        color: Optional hex color for SimpleIcons.

    Returns:
        List of LogoResult (or None for failures), same length as input.
    """
    return [resolve_logo(item, color=color) for item in items]


def clear_cache() -> int:
    """
    Remove all cached logos.

    Returns:
        Number of files deleted.
    """
    if not CACHE_DIR.exists():
        return 0

    count = 0
    for f in CACHE_DIR.iterdir():
        if f.is_file():
            f.unlink()
            count += 1
    return count
