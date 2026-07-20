"""
Automatická úprava platformio.ini v pracovním projektu.

Originální projekt má v platformio.ini řádek 'platform = espressif32'
bez čísla verze, což PlatformIO interpretuje jako "vždy nejnovější dostupná
verze". Nejnovější verze (ESP32 Arduino jádro 3.x) ale odstranila některé
starší funkce (ledcSetup, ledcAttachPin), na kterých staví knihovna
'statusLED' použitá tímto projektem - kompilace by na nich vždy selhala.

Autor projektu si je toho vědom (viz jeho vlastní zakomentovaná poznámka
v souboru), a doporučuje konkrétně ověřenou verzi 6.0.1. Tuhle verzi tady
připínáme automaticky, aby uživatel nemusel nic řešit ručně.
"""

import re
from pathlib import Path

KNOWN_COMPATIBLE_VERSION = "6.0.1"

_platform_line_re = re.compile(r"^(\s*)platform\s*=\s*espressif32\s*(;.*)?$")


def pin_compatible_platform_version(
    platformio_ini_path: Path, version: str = KNOWN_COMPATIBLE_VERSION
) -> bool:
    """
    Najde řádek 'platform = espressif32' (bez čísla verze) a připne ho na
    ověřenou funkční verzi. Vrátí True, pokud úpravu provedl, False pokud
    už byla verze připnutá nebo řádek nenašel (aby se to nezkusilo udělat
    dvakrát zbytečně).
    """
    lines = platformio_ini_path.read_text(encoding="utf-8").splitlines()
    changed = False
    for i, line in enumerate(lines):
        m = _platform_line_re.match(line)
        if m:
            indent = m.group(1)
            lines[i] = (
                f"{indent}platform = espressif32 @ {version} "
                f"; verze automaticky připnuta TankSound Configurátorem "
                f"kvůli kompatibilitě se staršími knihovnami projektu"
            )
            changed = True
            break
    if changed:
        platformio_ini_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed
