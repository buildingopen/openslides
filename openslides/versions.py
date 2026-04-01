"""
Deck Versioning
Saves and loads deck configs for iterative refinement.
"""
from __future__ import annotations

import json
import uuid
import shutil
from datetime import datetime, timedelta
from pathlib import Path

STORE_DIR = Path.home() / ".openslides" / "decks"


def save_deck(config: dict, theme_dict: dict | None = None) -> str:
    """
    Save a deck config and return a deck_id.

    Stores config.json and optionally theme.json in ~/.openslides/decks/{deck_id}/
    """
    deck_id = datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8]
    deck_dir = STORE_DIR / deck_id
    deck_dir.mkdir(parents=True, exist_ok=True)

    (deck_dir / "config.json").write_text(json.dumps(config, indent=2))
    if theme_dict:
        (deck_dir / "theme.json").write_text(json.dumps(theme_dict, indent=2))

    # Write metadata
    meta = {
        "deck_id": deck_id,
        "created": datetime.now().isoformat(),
        "slide_count": len(config.get("slides", [])),
    }
    (deck_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    return deck_id


def load_deck(deck_id: str) -> dict:
    """Load a saved deck config by ID."""
    deck_dir = STORE_DIR / deck_id
    config_path = deck_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Deck not found: {deck_id}")
    return json.loads(config_path.read_text())


def load_theme(deck_id: str) -> dict | None:
    """Load saved theme for a deck."""
    theme_path = STORE_DIR / deck_id / "theme.json"
    if theme_path.exists():
        return json.loads(theme_path.read_text())
    return None


def list_decks() -> list[dict]:
    """List all saved decks, newest first."""
    if not STORE_DIR.exists():
        return []
    decks = []
    for d in sorted(STORE_DIR.iterdir(), reverse=True):
        meta_path = d / "meta.json"
        if meta_path.exists():
            decks.append(json.loads(meta_path.read_text()))
    return decks


def cleanup(max_age_days: int = 30):
    """Delete decks older than max_age_days."""
    if not STORE_DIR.exists():
        return
    cutoff = datetime.now() - timedelta(days=max_age_days)
    for d in STORE_DIR.iterdir():
        meta_path = d / "meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            created = datetime.fromisoformat(meta["created"])
            if created < cutoff:
                shutil.rmtree(d)
