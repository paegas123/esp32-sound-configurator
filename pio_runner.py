"""
Automatická správa Python závislostí, které potřebuje PlatformIO pro
kompilaci nejnovějších verzí ESP32 platformy (littlefs-python, fatfs-ng,
pyyaml a případně další, které se objeví v budoucnu).

Cíl: uživatel nikdy nemusí sám spouštět žádný 'pip install' příkaz -
program si všechno potřebné zjistí a doinstaluje sám, tiše, na pozadí.
"""

import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Známé případy, kdy se jméno Python modulu (to, co se objeví v chybové
# hlášce "No module named 'xxx'") liší od jména balíčku pro pip install.
MODULE_TO_PIP_PACKAGE = {
    "littlefs": "littlefs-python",
    "fatfs": "fatfs-ng",
    "yaml": "pyyaml",
}

_module_not_found_re = re.compile(r"No module named '([\w.]+)'")


def get_platformio_python() -> Optional[str]:
    """
    Zjistí cestu k Python interpretu, pod kterým reálně běží příkaz 'pio'.
    To je důležité proto, že na macOS/Windows může být PlatformIO nainstalované
    pod úplně jiným Pythonem, než je ten, co spouští náš vlastní program
    (např. přímo pod python.org instalací, ne pod tou z Homebrew).
    Zjišťujeme to přečtením 'shebang' řádku souboru 'pio' (u konzolových
    Python skriptů první řádek vždy ukazuje na interpret, pod kterým byly
    nainstalovány).
    """
    pio_path = shutil.which("pio")
    if not pio_path:
        return None
    try:
        with open(pio_path, "r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline().strip()
    except (OSError, UnicodeDecodeError):
        return None
    if first_line.startswith("#!"):
        candidate = first_line[2:].strip()
        if Path(candidate).exists():
            return candidate
    return None


def pip_install(python_exe: str, pip_package: str) -> bool:
    """Nainstaluje balíček do daného Python interpretu. Vrátí True při úspěchu."""
    result = subprocess.run(
        [python_exe, "-m", "pip", "install", "--quiet", pip_package],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def ensure_known_dependencies() -> None:
    """
    Preventivně doinstaluje balíčky, o kterých už víme, že je nejnovější
    verze espressif32 platformy potřebuje. Bezpečné volat opakovaně -
    pokud už balíček nainstalovaný je, pip to jen rychle přeskočí.
    """
    python_exe = get_platformio_python()
    if not python_exe:
        return
    for pip_package in set(MODULE_TO_PIP_PACKAGE.values()):
        pip_install(python_exe, pip_package)


def run_pio_with_auto_dependency_fix(
    args: list[str], cwd: str, max_attempts: int = 5
) -> subprocess.CompletedProcess:
    """
    Spustí 'pio' s danými argumenty. Pokud selže na 'ModuleNotFoundError',
    automaticky doinstaluje chybějící balíček do správného Python interpretu
    a zkusí to znovu - bez nutnosti čehokoliv ze strany uživatele.
    """
    python_exe = get_platformio_python()
    already_tried: set[str] = set()

    result = None
    for _attempt in range(max_attempts):
        result = subprocess.run(
            ["pio", *args], cwd=cwd, capture_output=True, text=True
        )
        if result.returncode == 0:
            return result

        combined_output = (result.stdout or "") + (result.stderr or "")
        match = _module_not_found_re.search(combined_output)
        if not match or not python_exe:
            return result

        module_name = match.group(1).split(".")[0]
        if module_name in already_tried:
            # Už jsme to zkusili a nepomohlo to - dál by to jen zacyklilo.
            return result
        already_tried.add(module_name)

        pip_package = MODULE_TO_PIP_PACKAGE.get(module_name, module_name)
        pip_install(python_exe, pip_package)
        # ... a smyčka zkusí 'pio' spustit znovu.

    return result
