"""
Design System / Theme Tokens for OpenSlides.

Supports loading from URL (JSON spec), CSS custom properties, or brand colors.
Includes preset themes for dark/light and style variants.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, fields
from typing import Any, Dict, Optional
from urllib.parse import quote


@dataclass
class Theme:
    """All design tokens for slide rendering."""

    # Identity
    name: str = "light"

    # Colors
    background: str = "#FAFAF7"
    surface: str = "#F5F4F0"
    text_primary: str = "#161512"
    text_secondary: str = "#5A5850"
    text_muted: str = "#A09D94"
    accent: str = "#2563eb"
    accent_secondary: str = "#60a5fa"
    border: str = "#ECEAE4"
    border_light: str = "#F0EDE7"

    # Gradients
    gradient_primary: str = "linear-gradient(135deg, #2563eb, #60a5fa)"
    gradient_text: str = "linear-gradient(135deg, #2563eb, #60a5fa)"

    # Typography - families
    headline_font_family: str = "'DM Serif Display', serif"
    body_font_family: str = "'Plus Jakarta Sans', sans-serif"
    mono_font_family: str = "'JetBrains Mono', monospace"

    # Typography - sizes
    font_size_hero: str = "96px"
    font_size_display: str = "82px"
    font_size_headline: str = "64px"
    font_size_subheadline: str = "28px"
    font_size_large: str = "22px"
    font_size_label: str = "14px"

    # Typography - weights
    font_weight_medium: int = 500
    font_weight_semibold: int = 600
    font_weight_bold: int = 700
    font_weight_extrabold: int = 800

    # Typography - line heights & spacing
    line_height_tight: float = 1.1
    line_height_normal: float = 1.5
    letter_spacing_tight: str = "-0.03em"
    letter_spacing_wide: str = "0.08em"

    # Spacing
    slide_padding: str = "64px 80px"

    # Borders
    radius_medium: str = "14px"
    radius_large: str = "20px"

    # Assets
    logo_url: Optional[str] = None
    background_image_url: Optional[str] = None

    @property
    def font_family(self) -> str:
        """Backward-compatible: returns body font family."""
        return self.body_font_family

    @property
    def google_fonts_url(self) -> str:
        """Generate a Google Fonts import URL from font families."""
        families = set()
        for fam in (self.headline_font_family, self.body_font_family, self.mono_font_family):
            # Extract the first font name from a CSS font-family string
            raw = fam.split(",")[0].strip().strip("'\"")
            if raw:
                families.add(raw)

        params = []
        for fam in sorted(families):
            encoded = quote(fam)
            params.append(f"family={encoded}:wght@300;400;500;600;700;800;900")

        return "https://fonts.googleapis.com/css2?" + "&".join(params) + "&display=swap"

    def get_css_variables(self) -> str:
        """Output a CSS :root block with all color/spacing/typography tokens."""
        lines = [":root {"]
        mappings = {
            "--bg": self.background,
            "--surface": self.surface,
            "--text-primary": self.text_primary,
            "--text-secondary": self.text_secondary,
            "--text-muted": self.text_muted,
            "--accent": self.accent,
            "--accent-secondary": self.accent_secondary,
            "--border": self.border,
            "--border-light": self.border_light,
            "--gradient-primary": self.gradient_primary,
            "--gradient-text": self.gradient_text,
            "--headline-font": self.headline_font_family,
            "--body-font": self.body_font_family,
            "--mono-font": self.mono_font_family,
            "--font-size-hero": self.font_size_hero,
            "--font-size-display": self.font_size_display,
            "--font-size-headline": self.font_size_headline,
            "--font-size-subheadline": self.font_size_subheadline,
            "--font-size-large": self.font_size_large,
            "--font-size-label": self.font_size_label,
            "--slide-padding": self.slide_padding,
            "--radius-medium": self.radius_medium,
            "--radius-large": self.radius_large,
        }
        for var, val in mappings.items():
            lines.append(f"  {var}: {val};")
        lines.append("}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def from_url(cls, url: str) -> Theme:
        """Fetch a JSON design system spec from a URL and build a Theme."""
        import httpx

        resp = httpx.get(url, timeout=15, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()
        return cls._from_spec(data)

    @classmethod
    def from_css(cls, css_text: str) -> Theme:
        """Parse CSS custom properties (--var: value) into a Theme."""
        # Match lines like:  --bg: #FAFAF7;
        pattern = re.compile(r"--([\w-]+)\s*:\s*(.+?)\s*;")
        props: Dict[str, str] = {}
        for match in pattern.finditer(css_text):
            props[match.group(1)] = match.group(2)

        css_to_field = {
            "bg": "background",
            "surface": "surface",
            "text-primary": "text_primary",
            "text-secondary": "text_secondary",
            "text-muted": "text_muted",
            "accent": "accent",
            "accent-secondary": "accent_secondary",
            "border": "border",
            "border-light": "border_light",
            "gradient-primary": "gradient_primary",
            "gradient-text": "gradient_text",
            "headline-font": "headline_font_family",
            "body-font": "body_font_family",
            "mono-font": "mono_font_family",
            "font-size-hero": "font_size_hero",
            "font-size-display": "font_size_display",
            "font-size-headline": "font_size_headline",
            "font-size-subheadline": "font_size_subheadline",
            "font-size-large": "font_size_large",
            "font-size-label": "font_size_label",
            "slide-padding": "slide_padding",
            "radius-medium": "radius_medium",
            "radius-large": "radius_large",
        }

        kwargs: Dict[str, Any] = {}
        for css_name, field_name in css_to_field.items():
            if css_name in props:
                kwargs[field_name] = props[css_name]

        return cls(**kwargs)

    @classmethod
    def from_brand(cls, brand_context) -> Theme:
        """
        Derive a full theme from a BrandContext dataclass or dict.

        Accepts BrandContext (with .colors, .fonts) or dict with keys:
            primary, accent, mode, headline_font, body_font
        """
        if hasattr(brand_context, "colors"):
            colors = brand_context.colors or {}
            fonts = brand_context.fonts or {}
            primary = colors.get("accent") or colors.get("primary") or "#2563eb"
            accent_val = colors.get("accent_secondary")
            mode = "light"
            headline_font = fonts.get("headline_family")
            body_font = fonts.get("body_family")
        else:
            primary = brand_context.get("primary", "#2563eb")
            accent_val = brand_context.get("accent")
            mode = brand_context.get("mode", "light")
            headline_font = brand_context.get("headline_font")
            body_font = brand_context.get("body_font")

        r, g, b = _hex_to_rgb(primary)
        accent_hex = accent_val or _lighten(r, g, b, 0.35)

        if mode == "dark":
            base = DarkTheme()
        else:
            base = LightTheme()

        kwargs: Dict[str, Any] = {
            "name": f"brand-{mode}",
            "accent": primary,
            "accent_secondary": accent_hex,
            "gradient_primary": f"linear-gradient(135deg, {primary}, {accent_hex})",
            "gradient_text": f"linear-gradient(135deg, {primary}, {accent_hex})",
        }

        if headline_font:
            kwargs["headline_font_family"] = headline_font
        if body_font:
            kwargs["body_font_family"] = body_font

        # Merge onto base
        base_dict = {f.name: getattr(base, f.name) for f in fields(base)}
        base_dict.update(kwargs)
        return cls(**base_dict)

    @classmethod
    def _from_spec(cls, data: Dict[str, Any]) -> Theme:
        """Build a Theme from a design system JSON spec."""
        kwargs: Dict[str, Any] = {}

        if "name" in data:
            kwargs["name"] = data["name"]

        colors = data.get("colors", {})
        color_map = {
            "background": "background",
            "surface": "surface",
            "text_primary": "text_primary",
            "text_secondary": "text_secondary",
            "text_muted": "text_muted",
            "accent": "accent",
            "accent_secondary": "accent_secondary",
            "border": "border",
            "border_light": "border_light",
            "dark_bg": None,  # not a direct field
        }
        for spec_key, field_name in color_map.items():
            if spec_key in colors and field_name:
                kwargs[field_name] = colors[spec_key]

        # Derive gradients from accent colors
        accent = colors.get("accent", "#2563eb")
        accent_sec = colors.get("accent_secondary", "#60a5fa")
        kwargs.setdefault("gradient_primary", f"linear-gradient(135deg, {accent}, {accent_sec})")
        kwargs.setdefault("gradient_text", f"linear-gradient(135deg, {accent}, {accent_sec})")

        typo = data.get("typography", {})
        if "headline_family" in typo:
            kwargs["headline_font_family"] = f"'{typo['headline_family']}', serif"
        if "body_family" in typo:
            kwargs["body_font_family"] = f"'{typo['body_family']}', sans-serif"
        if "mono_family" in typo:
            kwargs["mono_font_family"] = f"'{typo['mono_family']}', monospace"

        spacing = data.get("spacing", {})
        if "slide_padding" in spacing:
            kwargs["slide_padding"] = spacing["slide_padding"]

        borders = data.get("borders", {})
        if "radius_medium" in borders:
            kwargs["radius_medium"] = borders["radius_medium"]
        if "radius_large" in borders:
            kwargs["radius_large"] = borders["radius_large"]

        return cls(**kwargs)


# ------------------------------------------------------------------
# Color helpers
# ------------------------------------------------------------------

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def _lighten(r: int, g: int, b: int, amount: float) -> str:
    nr = min(255, int(r + (255 - r) * amount))
    ng = min(255, int(g + (255 - g) * amount))
    nb = min(255, int(b + (255 - b) * amount))
    return _rgb_to_hex(nr, ng, nb)


def _darken(r: int, g: int, b: int, amount: float) -> str:
    nr = max(0, int(r * (1 - amount)))
    ng = max(0, int(g * (1 - amount)))
    nb = max(0, int(b * (1 - amount)))
    return _rgb_to_hex(nr, ng, nb)


# ------------------------------------------------------------------
# Preset Themes
# ------------------------------------------------------------------

# Base dark/light

class DarkTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="dark",
            background="#0F0F0F",
            surface="#1A1A1A",
            text_primary="#FFFFFF",
            text_secondary="#A0A0A0",
            text_muted="#666666",
            accent="#2563eb",
            accent_secondary="#60a5fa",
            border="#2A2A2A",
            border_light="#222222",
            gradient_primary="linear-gradient(135deg, #2563eb, #60a5fa)",
            gradient_text="linear-gradient(135deg, #2563eb, #60a5fa)",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


class LightTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="light",
            background="#FAFAF7",
            surface="#F5F4F0",
            text_primary="#161512",
            text_secondary="#5A5850",
            text_muted="#A09D94",
            accent="#2563eb",
            accent_secondary="#60a5fa",
            border="#ECEAE4",
            border_light="#F0EDE7",
            gradient_primary="linear-gradient(135deg, #2563eb, #60a5fa)",
            gradient_text="linear-gradient(135deg, #2563eb, #60a5fa)",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


# Pitch (alias for base)

class PitchDarkTheme(DarkTheme):
    def __init__(self, **overrides: Any):
        overrides.setdefault("name", "pitch-dark")
        super().__init__(**overrides)


class PitchLightTheme(LightTheme):
    def __init__(self, **overrides: Any):
        overrides.setdefault("name", "pitch-light")
        super().__init__(**overrides)


# Consulting - formal, serif headlines, muted palette

class ConsultingDarkTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="consulting-dark",
            background="#0C1220",
            surface="#141C2E",
            text_primary="#F0F0F0",
            text_secondary="#94A3B8",
            text_muted="#64748B",
            accent="#2563EB",
            accent_secondary="#60A5FA",
            border="#1E293B",
            border_light="#1A2332",
            gradient_primary="linear-gradient(135deg, #2563EB, #60A5FA)",
            gradient_text="linear-gradient(135deg, #2563EB, #60A5FA)",
            headline_font_family="'Playfair Display', serif",
            body_font_family="'Inter', sans-serif",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


class ConsultingLightTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="consulting-light",
            background="#FFFFFF",
            surface="#F8FAFC",
            text_primary="#0F172A",
            text_secondary="#475569",
            text_muted="#94A3B8",
            accent="#2563EB",
            accent_secondary="#60A5FA",
            border="#E2E8F0",
            border_light="#F1F5F9",
            gradient_primary="linear-gradient(135deg, #2563EB, #60A5FA)",
            gradient_text="linear-gradient(135deg, #2563EB, #60A5FA)",
            headline_font_family="'Playfair Display', serif",
            body_font_family="'Inter', sans-serif",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


# Consumer - playful, vibrant gradients

class ConsumerDarkTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="consumer-dark",
            background="#0A0A0A",
            surface="#161616",
            text_primary="#FFFFFF",
            text_secondary="#B0B0B0",
            text_muted="#707070",
            accent="#8B5CF6",
            accent_secondary="#C084FC",
            border="#262626",
            border_light="#1E1E1E",
            gradient_primary="linear-gradient(135deg, #8B5CF6, #EC4899)",
            gradient_text="linear-gradient(135deg, #8B5CF6, #EC4899)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
            font_weight_extrabold=900,
        )
        defaults.update(overrides)
        super().__init__(**defaults)


class ConsumerLightTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="consumer-light",
            background="#FAFAFA",
            surface="#F3F0FF",
            text_primary="#1A1A2E",
            text_secondary="#4A4A6A",
            text_muted="#9090B0",
            accent="#8B5CF6",
            accent_secondary="#C084FC",
            border="#E8E0FF",
            border_light="#F0ECFF",
            gradient_primary="linear-gradient(135deg, #8B5CF6, #EC4899)",
            gradient_text="linear-gradient(135deg, #8B5CF6, #EC4899)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
            font_weight_extrabold=900,
        )
        defaults.update(overrides)
        super().__init__(**defaults)


# Creative - bold, high contrast, asymmetric feel

class CreativeDarkTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="creative-dark",
            background="#111111",
            surface="#1C1C1C",
            text_primary="#FFFFFF",
            text_secondary="#CCCCCC",
            text_muted="#777777",
            accent="#FF3366",
            accent_secondary="#FF6B6B",
            border="#333333",
            border_light="#282828",
            gradient_primary="linear-gradient(135deg, #FF3366, #FF6B6B)",
            gradient_text="linear-gradient(135deg, #FF3366, #FF6B6B)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
            font_weight_extrabold=900,
            letter_spacing_tight="-0.04em",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


class CreativeLightTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="creative-light",
            background="#FFFDF7",
            surface="#FFF5EB",
            text_primary="#1A1A1A",
            text_secondary="#555555",
            text_muted="#999999",
            accent="#FF3366",
            accent_secondary="#FF6B6B",
            border="#FFE0CC",
            border_light="#FFF0E6",
            gradient_primary="linear-gradient(135deg, #FF3366, #FF6B6B)",
            gradient_text="linear-gradient(135deg, #FF3366, #FF6B6B)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
            font_weight_extrabold=900,
            letter_spacing_tight="-0.04em",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


# Minimal - restrained, lots of whitespace

class MinimalDarkTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="minimal-dark",
            background="#111111",
            surface="#181818",
            text_primary="#E8E8E8",
            text_secondary="#999999",
            text_muted="#555555",
            accent="#E8E8E8",
            accent_secondary="#CCCCCC",
            border="#282828",
            border_light="#1E1E1E",
            gradient_primary="linear-gradient(135deg, #E8E8E8, #CCCCCC)",
            gradient_text="linear-gradient(135deg, #E8E8E8, #CCCCCC)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


class MinimalLightTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="minimal-light",
            background="#FFFFFF",
            surface="#F9F9F9",
            text_primary="#1A1A1A",
            text_secondary="#666666",
            text_muted="#AAAAAA",
            accent="#1A1A1A",
            accent_secondary="#444444",
            border="#EEEEEE",
            border_light="#F5F5F5",
            gradient_primary="linear-gradient(135deg, #1A1A1A, #444444)",
            gradient_text="linear-gradient(135deg, #1A1A1A, #444444)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
        )
        defaults.update(overrides)
        super().__init__(**defaults)


# Sales - energetic, orange/warm tones

class SalesDarkTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="sales-dark",
            background="#0F0F0F",
            surface="#1A1410",
            text_primary="#FFFFFF",
            text_secondary="#C0A080",
            text_muted="#806040",
            accent="#F97316",
            accent_secondary="#FBBF24",
            border="#2A2015",
            border_light="#221A10",
            gradient_primary="linear-gradient(135deg, #F97316, #FBBF24)",
            gradient_text="linear-gradient(135deg, #F97316, #FBBF24)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
            font_weight_extrabold=900,
        )
        defaults.update(overrides)
        super().__init__(**defaults)


class SalesLightTheme(Theme):
    def __init__(self, **overrides: Any):
        defaults = dict(
            name="sales-light",
            background="#FFFCF5",
            surface="#FFF7ED",
            text_primary="#1C1208",
            text_secondary="#7C5A2C",
            text_muted="#B89060",
            accent="#F97316",
            accent_secondary="#FBBF24",
            border="#FFE4C4",
            border_light="#FFF0DC",
            gradient_primary="linear-gradient(135deg, #F97316, #FBBF24)",
            gradient_text="linear-gradient(135deg, #F97316, #FBBF24)",
            headline_font_family="'Inter', sans-serif",
            body_font_family="'Inter', sans-serif",
            font_weight_extrabold=900,
        )
        defaults.update(overrides)
        super().__init__(**defaults)


# ------------------------------------------------------------------
# Theme registry for lookup by name
# ------------------------------------------------------------------

THEME_REGISTRY: Dict[str, type[Theme]] = {
    "dark": DarkTheme,
    "light": LightTheme,
    "pitch-dark": PitchDarkTheme,
    "pitch-light": PitchLightTheme,
    "consulting-dark": ConsultingDarkTheme,
    "consulting-light": ConsultingLightTheme,
    "consumer-dark": ConsumerDarkTheme,
    "consumer-light": ConsumerLightTheme,
    "creative-dark": CreativeDarkTheme,
    "creative-light": CreativeLightTheme,
    "minimal-dark": MinimalDarkTheme,
    "minimal-light": MinimalLightTheme,
    "sales-dark": SalesDarkTheme,
    "sales-light": SalesLightTheme,
}


def get_theme(name: str) -> Theme:
    """Look up a preset theme by name. Raises KeyError if not found."""
    cls = THEME_REGISTRY[name]
    return cls()
