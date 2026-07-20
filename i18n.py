"""Načítání textů programu v aktuálně zvoleném jazyce."""

import json
from pathlib import Path

from app_paths import get_base_dir

LANG_DIR = get_base_dir() / "lang"

_cache: dict[str, dict] = {}


def get_texts(lang: str) -> dict:
    if lang not in _cache:
        path = LANG_DIR / f"{lang}.json"
        _cache[lang] = json.loads(path.read_text(encoding="utf-8"))
    return _cache[lang]


class Translator:
    """Drží texty pro jeden zvolený jazyk a poskytuje pohodlné .t(key, **kwargs)."""

    def __init__(self, lang: str):
        self.lang = lang
        self.texts = get_texts(lang)

    def t(self, key: str, **kwargs) -> str:
        template = self.texts.get(key, key)
        return template.format(**kwargs) if kwargs else template
