"""Ukládání a načítání trvalých nastavení uživatele (jazyk programu apod.)."""

import json
from pathlib import Path
from typing import Optional

from paths import SETTINGS_FILE, ensure_directories

SUPPORTED_LANGUAGES = ("cs", "en", "de")
DEFAULT_LANGUAGE = "en"


def load_settings() -> dict:
    ensure_directories()
    if not SETTINGS_FILE.exists():
        return {}
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Poškozený soubor nastavení nesmí shodit celý program.
        return {}


def save_settings(data: dict) -> None:
    ensure_directories()
    SETTINGS_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def get_language() -> Optional[str]:
    lang = load_settings().get("language")
    return lang if lang in SUPPORTED_LANGUAGES else None


def set_language(lang: str) -> None:
    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {lang}")
    data = load_settings()
    data["language"] = lang
    save_settings(data)


DEFAULT_LEVEL_MODE = "green"  # green=začátečník, yellow=pokročilý, red=expert


def get_level_mode() -> str:
    mode = load_settings().get("levelMode")
    return mode if mode in ("green", "yellow", "red") else DEFAULT_LEVEL_MODE


def set_level_mode(mode: str) -> None:
    if mode not in ("green", "yellow", "red"):
        raise ValueError(f"Unsupported level mode: {mode}")
    data = load_settings()
    data["levelMode"] = mode
    save_settings(data)


def get_web_interface_choice() -> str:
    """'original' = puvodni web od autora projektu, 'new' = nas novy (zatim neni hotovy)."""
    choice = load_settings().get("webInterfaceChoice")
    return choice if choice in ("original", "new") else "original"


def set_web_interface_choice(choice: str) -> None:
    if choice not in ("original", "new"):
        raise ValueError(f"Unsupported web interface choice: {choice}")
    data = load_settings()
    data["webInterfaceChoice"] = choice
    save_settings(data)
