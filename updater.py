"""
Správa 'vendor_snapshot' - nedotčené kopie originálního projektu TheDIYGuy999/Rc_Engine_Sound_ESP32.

Logika:
1. Zkusí se zjistit nejnovější commit na GitHubu (lehký API dotaz).
2. Pokud internet není dostupný:
   - a lokální kopie existuje -> pokračuje se s ní (tichý fallback).
   - a lokální kopie neexistuje -> jasná chyba, program nemůže pokračovat.
3. Pokud internet je dostupný:
   - a lokální kopie neexistuje -> stáhne se rovnou, bez ptaní (první spuštění).
   - a lokální kopie existuje a je stejná verze -> nic se neděje.
   - a lokální kopie existuje, ale je starší -> uživatel se zeptá, jestli chce update.
"""

import json
import shutil
import ssl
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

# Zabalené (PyInstaller) aplikace si někdy "nenajdou" systémové bezpečnostní
# certifikáty, i když internet reálně funguje - projeví se to jako "není
# dostupný internet", i když je. Pokud je k dispozici balíček certifi
# (přibalený do .app/.exe), použijeme jeho certifikáty explicitně, ať se
# tomu předejde. Pokud certifi není nainstalované (běžné spuštění přes
# `python3 gui.py`), použije se prostě výchozí chování jako dřív.
try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = None

from paths import (
    GITHUB_API_LATEST_COMMIT,
    GITHUB_ZIP_URL,
    VENDOR_SNAPSHOT_DIR,
    VENDOR_VERSION_FILE,
)

REQUEST_TIMEOUT_SECONDS = 6
USER_AGENT = "TankSound-Configurator/0.1 (+https://github.com/TheDIYGuy999/Rc_Engine_Sound_ESP32)"


@dataclass
class RemoteVersionInfo:
    sha: str
    date: str  # ISO 8601 datum commitu


def check_internet_and_get_latest_commit() -> Optional[RemoteVersionInfo]:
    """
    Vrátí info o nejnovějším commitu na GitHubu, nebo None, pokud není
    dostupné internetové připojení / GitHub nedostupný.
    Nikdy nevyhazuje výjimku ven - to je záměr, aby volající mohl
    jednoduše přejít na offline fallback.
    """
    try:
        request = Request(
            GITHUB_API_LATEST_COMMIT,
            headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"},
        )
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS, context=_SSL_CONTEXT) as response:
            data = json.loads(response.read().decode("utf-8"))
        sha = data["sha"]
        date = data["commit"]["committer"]["date"]
        return RemoteVersionInfo(sha=sha, date=date)
    except (URLError, TimeoutError, KeyError, ValueError, OSError):
        return None


def load_local_version() -> Optional[dict]:
    """Vrátí obsah version.json lokální kopie, nebo None, pokud kopie neexistuje."""
    if not VENDOR_VERSION_FILE.exists():
        return None
    try:
        return json.loads(VENDOR_VERSION_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def has_local_copy() -> bool:
    """Kopie se považuje za platnou, pokud existuje version.json A obsah snapshotu."""
    if load_local_version() is None:
        return False
    # Snapshot musí obsahovat aspoň nějaké soubory kromě version.json
    contents = [p for p in VENDOR_SNAPSHOT_DIR.iterdir() if p.name != "version.json"]
    return len(contents) > 0


def download_and_replace_snapshot(remote_info: RemoteVersionInfo, progress_callback=None) -> None:
    """
    Stáhne ZIP z GitHubu, rozbalí ho a atomicky nahradí obsah VENDOR_SNAPSHOT_DIR.
    Používá dočasný adresář, aby při selhání uprostřed stahování nezůstal
    vendor_snapshot v poškozeném/napůl rozbaleném stavu.
    """
    if progress_callback:
        progress_callback()

    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        zip_path = tmp_dir / "repo.zip"

        request = Request(GITHUB_ZIP_URL, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=60, context=_SSL_CONTEXT) as response:
            zip_path.write_bytes(response.read())

        extract_dir = tmp_dir / "extracted"
        extract_dir.mkdir()
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        # GitHub ZIP obsahuje jeden kořenový adresář typu "Rc_Engine_Sound_ESP32-master"
        extracted_roots = list(extract_dir.iterdir())
        if len(extracted_roots) != 1 or not extracted_roots[0].is_dir():
            raise RuntimeError(
                "Neočekávaná struktura staženého ZIPu z GitHubu (očekáván jeden kořenový adresář)."
            )
        repo_root = extracted_roots[0]

        # Zapíšeme verzi do staženého obsahu ještě před přesunem
        version_data = {"sha": remote_info.sha, "date": remote_info.date}
        (repo_root / "version.json").write_text(
            json.dumps(version_data, indent=2), encoding="utf-8"
        )

        # Atomická náhrada: nejdřív smažeme starý snapshot, pak přesuneme nový obsah.
        if VENDOR_SNAPSHOT_DIR.exists():
            shutil.rmtree(VENDOR_SNAPSHOT_DIR)
        shutil.move(str(repo_root), str(VENDOR_SNAPSHOT_DIR))


def is_up_to_date(remote_info: RemoteVersionInfo) -> bool:
    local = load_local_version()
    if local is None:
        return False
    return local.get("sha") == remote_info.sha
