"""
Content Validator
Validates LLM-generated slide deck content before rendering.
Catches common errors: missing fields, placeholder text, inconsistent numbers.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from .prompts import SLIDE_SCHEMAS


# ---------------------------------------------------------------------------
# Known list fields per slide type (derived from components.py signatures)
# ---------------------------------------------------------------------------

_LIST_FIELDS: dict[str, set[str]] = {
    "title": {"bottom_items"},
    "problem": {"blocker_list"},
    "validation": {"quotes"},
    "market": {"segments"},
    "team_ask": {"bio_items", "ask_uses"},
    "solution": {"features"},
    "funds": {"fund_items", "milestones"},
    "pricing": {"tiers"},
    "traction": {"milestones", "metrics"},
    "comparison": {"columns"},
    "numbered_points": {"points"},
    "demo": {"flow_items"},
}


# ---------------------------------------------------------------------------
# Placeholder patterns
# ---------------------------------------------------------------------------

_PLACEHOLDER_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"lorem\s+ipsum", re.IGNORECASE),
    re.compile(r"\bTBD\b"),
    re.compile(r"\[insert", re.IGNORECASE),
    re.compile(r"\bXXX\b"),
    re.compile(r"\bTODO\b", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Dollar amount parsing
# ---------------------------------------------------------------------------

_DOLLAR_RE = re.compile(
    r"\$\s*([\d,.]+)\s*([KMBT])?",
    re.IGNORECASE,
)

_MULTIPLIERS = {
    "k": 1_000,
    "m": 1_000_000,
    "b": 1_000_000_000,
    "t": 1_000_000_000_000,
}

# Stage ranges (min, max) in dollars
_STAGE_RANGES: dict[str, tuple[float, float]] = {
    "pre-seed": (50_000, 2_000_000),
    "pre_seed": (50_000, 2_000_000),
    "preseed": (50_000, 2_000_000),
    "seed": (1_000_000, 5_000_000),
}


def _parse_dollar(text: str) -> Optional[float]:
    """Parse a dollar string like '$1.5M', '$500K', '$2,000,000' into a float."""
    if not isinstance(text, str):
        return None
    m = _DOLLAR_RE.search(text)
    if not m:
        return None
    raw_num = m.group(1).replace(",", "")
    try:
        value = float(raw_num)
    except ValueError:
        return None
    suffix = (m.group(2) or "").lower()
    value *= _MULTIPLIERS.get(suffix, 1)
    return value


def _format_dollar(value: float) -> str:
    """Format a numeric dollar value into compact notation ($XM, $XK, $XB)."""
    abs_val = abs(value)
    if abs_val >= 1_000_000_000:
        formatted = f"${value / 1_000_000_000:.1f}B"
    elif abs_val >= 1_000_000:
        formatted = f"${value / 1_000_000:.1f}M"
    elif abs_val >= 1_000:
        formatted = f"${value / 1_000:.0f}K"
    else:
        formatted = f"${value:.0f}"
    # Strip trailing .0 (e.g. $1.0M -> $1M)
    formatted = formatted.replace(".0M", "M").replace(".0B", "B").replace(".0K", "K")
    return formatted


def _has_placeholder(text: str) -> Optional[str]:
    """Return the matched placeholder pattern if found, else None."""
    if not isinstance(text, str):
        return None
    for pat in _PLACEHOLDER_PATTERNS:
        if pat.search(text):
            return pat.pattern
    return None


def _check_string_values(data: Any, path: str = "") -> list[str]:
    """Recursively check all string values for placeholder text."""
    warnings: list[str] = []
    if isinstance(data, str):
        match = _has_placeholder(data)
        if match:
            warnings.append(f"Placeholder text at '{path}': matched pattern {match!r}")
    elif isinstance(data, dict):
        for k, v in data.items():
            warnings.extend(_check_string_values(v, f"{path}.{k}" if path else k))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            warnings.extend(_check_string_values(v, f"{path}[{i}]"))
    return warnings


def _is_long_number(text: str) -> bool:
    """Check if a dollar string uses comma-separated long form like $1,000,000."""
    return bool(re.search(r"\$[\d,]{7,}", text))


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Result of deck validation."""

    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    auto_fixes: dict[str, Any] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def __repr__(self) -> str:
        return (
            f"ValidationResult(errors={len(self.errors)}, "
            f"warnings={len(self.warnings)}, "
            f"auto_fixes={len(self.auto_fixes)})"
        )


# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------

def validate_deck(config: dict) -> ValidationResult:
    """
    Validate an entire deck config dict.

    Expected structure:
        {
            "slides": [
                {"type": "title", "company_name": "...", "headline": "...", ...},
                {"type": "market", "headline": "...", "tam": {...}, ...},
                ...
            ],
            "stage": "seed",        # optional, used for ask validation
            "theme": "dark",        # optional
        }

    Returns a ValidationResult with errors, warnings, and suggested auto-fixes.
    """
    result = ValidationResult()

    slides = config.get("slides")
    if not slides:
        result.errors.append("Deck config has no 'slides' list or it is empty")
        return result

    if not isinstance(slides, list):
        result.errors.append("'slides' must be a list")
        return result

    stage = (config.get("stage") or "").lower().strip()

    for idx, slide in enumerate(slides):
        prefix = f"slides[{idx}]"

        if not isinstance(slide, dict):
            result.errors.append(f"{prefix}: slide must be a dict, got {type(slide).__name__}")
            continue

        slide_type = slide.get("type", "")
        if not slide_type:
            result.errors.append(f"{prefix}: missing 'type' field")
            continue

        # --- Schema-based field checks ---
        schema = SLIDE_SCHEMAS.get(slide_type)
        if schema is None:
            result.warnings.append(f"{prefix}: unknown slide type '{slide_type}'")
        else:
            _validate_slide_fields(slide, schema, prefix, result)

        # --- Headline check (all slides except image and quote) ---
        if slide_type not in ("image", "quote"):
            if not slide.get("content", {}).get("headline"):
                result.errors.append(f"{prefix} ({slide_type}): missing 'headline'")

        # --- Placeholder text scan ---
        placeholder_warnings = _check_string_values(slide.get("content", {}), prefix)
        result.warnings.extend(placeholder_warnings)

        # --- Type-specific checks ---
        if slide_type == "market":
            _validate_market(slide, prefix, result)

        if slide_type == "team_ask":
            _validate_team_ask(slide, prefix, stage, result)

        if slide_type == "pricing":
            _validate_pricing(slide, prefix, result)

        if slide_type == "traction":
            _validate_traction(slide, prefix, result)

        if slide_type == "funds":
            _validate_funds(slide, prefix, result)

        # --- Number formatting auto-fixes ---
        _check_number_formatting(slide, prefix, result)

    return result


# ---------------------------------------------------------------------------
# Field-level validation
# ---------------------------------------------------------------------------

def _validate_slide_fields(
    slide: dict,
    schema: dict[str, Any],
    prefix: str,
    result: ValidationResult,
) -> None:
    """Check required fields and empty list fields per schema."""
    slide_type = slide.get("type", "unknown")
    required = schema.get("required", [])
    list_fields = _LIST_FIELDS.get(slide_type, set())

    content = slide.get("content", {})
    for field_name in required:
        val = content.get(field_name)
        if val is None and field_name not in content:
            result.errors.append(
                f"{prefix} ({slide_type}): missing required field '{field_name}'"
            )
        elif isinstance(val, list) and len(val) == 0 and field_name in list_fields:
            result.errors.append(
                f"{prefix} ({slide_type}): '{field_name}' is an empty list"
            )

    # Warn on optional list fields that are present but empty
    for field_name in schema.get("optional", []):
        val = content.get(field_name)
        if isinstance(val, list) and len(val) == 0 and field_name in list_fields:
            result.warnings.append(
                f"{prefix} ({slide_type}): '{field_name}' is an empty list"
            )


# ---------------------------------------------------------------------------
# Market slide: TAM > SAM > SOM
# ---------------------------------------------------------------------------

def _validate_market(slide: dict, prefix: str, result: ValidationResult) -> None:
    content = slide.get("content", {})
    tam_raw = content.get("tam", {})
    sam_raw = content.get("sam", {})
    som_raw = content.get("som", {})

    tam_val = _parse_dollar(tam_raw.get("value", "") if isinstance(tam_raw, dict) else "")
    sam_val = _parse_dollar(sam_raw.get("value", "") if isinstance(sam_raw, dict) else "")
    som_val = _parse_dollar(som_raw.get("value", "") if isinstance(som_raw, dict) else "")

    if tam_val is not None and sam_val is not None:
        if sam_val >= tam_val:
            result.errors.append(
                f"{prefix} (market): SAM ({_format_dollar(sam_val)}) must be less than "
                f"TAM ({_format_dollar(tam_val)})"
            )

    if sam_val is not None and som_val is not None:
        if som_val >= sam_val:
            result.errors.append(
                f"{prefix} (market): SOM ({_format_dollar(som_val)}) must be less than "
                f"SAM ({_format_dollar(sam_val)})"
            )

    if tam_val is not None and som_val is not None:
        if som_val >= tam_val:
            result.errors.append(
                f"{prefix} (market): SOM ({_format_dollar(som_val)}) must be less than "
                f"TAM ({_format_dollar(tam_val)})"
            )


# ---------------------------------------------------------------------------
# Team/ask: bio_items count, ask amount vs stage
# ---------------------------------------------------------------------------

def _validate_team_ask(
    slide: dict, prefix: str, stage: str, result: ValidationResult,
) -> None:
    content = slide.get("content", {})
    bio_items = content.get("bio_items")
    if isinstance(bio_items, list) and len(bio_items) < 1:
        pass

    ask_amount_raw = content.get("ask_amount", "")
    ask_val = _parse_dollar(ask_amount_raw) if isinstance(ask_amount_raw, str) else None

    if ask_val is not None and stage:
        range_info = _STAGE_RANGES.get(stage)
        if range_info:
            lo, hi = range_info
            if ask_val < lo or ask_val > hi:
                result.warnings.append(
                    f"{prefix} (team_ask): ask amount {_format_dollar(ask_val)} is outside "
                    f"typical range for '{stage}' stage ({_format_dollar(lo)} - {_format_dollar(hi)})"
                )


# ---------------------------------------------------------------------------
# Pricing: at least 2 tiers
# ---------------------------------------------------------------------------

def _validate_pricing(slide: dict, prefix: str, result: ValidationResult) -> None:
    tiers = slide.get("tiers", [])
    if isinstance(tiers, list) and 0 < len(tiers) < 2:
        result.warnings.append(
            f"{prefix} (pricing): only {len(tiers)} tier(s); recommend at least 2"
        )


# ---------------------------------------------------------------------------
# Traction: milestones count
# ---------------------------------------------------------------------------

def _validate_traction(slide: dict, prefix: str, result: ValidationResult) -> None:
    milestones = slide.get("milestones")
    if isinstance(milestones, list) and 0 < len(milestones) < 3:
        result.warnings.append(
            f"{prefix} (traction): only {len(milestones)} milestone(s); recommend at least 3"
        )


# ---------------------------------------------------------------------------
# Funds: milestones count
# ---------------------------------------------------------------------------

def _validate_funds(slide: dict, prefix: str, result: ValidationResult) -> None:
    milestones = slide.get("milestones")
    if isinstance(milestones, list) and 0 < len(milestones) < 3:
        result.warnings.append(
            f"{prefix} (funds): only {len(milestones)} milestone(s); recommend at least 3"
        )


# ---------------------------------------------------------------------------
# Number formatting: flag long-form numbers, suggest compact format
# ---------------------------------------------------------------------------

def _check_number_formatting(
    slide: dict, prefix: str, result: ValidationResult,
) -> None:
    """Find dollar amounts in long form and suggest compact equivalents."""
    _walk_for_long_numbers(slide, prefix, result)


def _walk_for_long_numbers(
    data: Any, path: str, result: ValidationResult,
) -> None:
    if isinstance(data, str):
        if _is_long_number(data):
            parsed = _parse_dollar(data)
            if parsed is not None:
                compact = _format_dollar(parsed)
                long_match = re.search(r"\$[\d,]+", data)
                if long_match:
                    fix_key = f"format_number:{path}"
                    result.auto_fixes[fix_key] = {
                        "path": path,
                        "original": data,
                        "suggested": data.replace(long_match.group(), compact),
                        "reason": f"Use compact notation: {compact} instead of long form",
                    }
                    result.warnings.append(
                        f"{path}: use compact dollar notation ({compact}) instead of long form"
                    )
    elif isinstance(data, dict):
        for k, v in data.items():
            _walk_for_long_numbers(v, f"{path}.{k}" if path else k, result)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            _walk_for_long_numbers(v, f"{path}[{i}]", result)


# ---------------------------------------------------------------------------
# Default label mapping (for auto-fix)
# ---------------------------------------------------------------------------

_DEFAULT_LABELS: dict[str, str] = {
    "problem": "Problem",
    "validation": "Validation",
    "market": "Market",
    "solution": "Solution",
    "funds": "Use of Funds",
    "pricing": "Pricing",
    "traction": "Traction",
    "comparison": "Comparison",
    "demo": "Demo",
}

# Default theme per slide type (from SLIDE_SCHEMAS)
_DEFAULT_THEMES: dict[str, str] = {
    stype: schema.get("theme", "light")
    for stype, schema in SLIDE_SCHEMAS.items()
}


# ---------------------------------------------------------------------------
# Apply fixes
# ---------------------------------------------------------------------------

def apply_fixes(config: dict, fixes: dict) -> dict:
    """
    Apply auto-fixes to a deck config and return a new config.

    Supported fix types (keyed by prefix):
        format_number:<path>  - replace long-form dollar amounts with compact notation

    Also runs a second pass to:
        - Add missing labels for slide types that have sensible defaults
        - Fill default theme per slide type from SLIDE_SCHEMAS

    Args:
        config: the original deck config
        fixes: the auto_fixes dict from ValidationResult

    Returns:
        A new config dict with fixes applied (original is not mutated).
    """
    config = copy.deepcopy(config)
    slides = config.get("slides", [])

    # Apply explicit fixes from the auto_fixes dict
    for fix_key, fix_info in fixes.items():
        if fix_key.startswith("format_number:"):
            _apply_number_fix(config, fix_info)

    # Second pass: add missing labels and default themes
    for slide in slides:
        if not isinstance(slide, dict):
            continue
        slide_type = slide.get("type", "")
        schema = SLIDE_SCHEMAS.get(slide_type, {})

        # Add missing label
        optional_fields = schema.get("optional", [])
        if "label" in optional_fields and not slide.get("label"):
            default_label = _DEFAULT_LABELS.get(slide_type)
            if default_label:
                slide["label"] = default_label

        # Fill default theme
        if "theme" not in slide:
            default_theme = _DEFAULT_THEMES.get(slide_type)
            if default_theme:
                slide["theme"] = default_theme

    return config


def _apply_number_fix(config: dict, fix_info: dict) -> None:
    """Navigate to the path in config and replace the value."""
    path = fix_info.get("path", "")
    original = fix_info.get("original", "")
    suggested = fix_info.get("suggested", "")
    if not path or not original or not suggested:
        return

    parts = _parse_path(path)
    obj: Any = config
    for part in parts[:-1]:
        if isinstance(part, int):
            if isinstance(obj, list) and 0 <= part < len(obj):
                obj = obj[part]
            else:
                return
        elif isinstance(obj, dict):
            obj = obj.get(part)
            if obj is None:
                return
        else:
            return

    last = parts[-1]
    if isinstance(last, int) and isinstance(obj, list) and 0 <= last < len(obj):
        if obj[last] == original:
            obj[last] = suggested
    elif isinstance(last, str) and isinstance(obj, dict):
        if obj.get(last) == original:
            obj[last] = suggested


def _parse_path(path: str) -> list[str | int]:
    """Parse 'slides[0].tam.value' into ['slides', 0, 'tam', 'value']."""
    parts: list[str | int] = []
    for segment in re.split(r"\.", path):
        if not segment:
            continue
        bracket_match = re.match(r"^(\w+)\[(\d+)\]$", segment)
        if bracket_match:
            parts.append(bracket_match.group(1))
            parts.append(int(bracket_match.group(2)))
        else:
            parts.append(segment)
    return parts
