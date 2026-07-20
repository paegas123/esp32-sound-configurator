"""
Zjištění základního adresáře programu - funguje jak při běžném spuštění
(`python3 gui.py`), tak po zabalení do samostatné aplikace (PyInstaller
`.app`/`.exe`), kde jsou přiložené soubory (web/, lang/) rozbalené do
dočasného adresáře `sys._MEIPASS`, ne vedle skutečného .py souboru.
"""

import sys
from pathlib import Path


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).parent
