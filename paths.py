"""
Centrální definice všech cest používaných programem.

Struktura na disku uživatele:

~/TankSound_Configurator/
├── vendor_snapshot/      <- čistá, nedotčená kopie originálu z GitHubu
│   └── version.json      <- uložený commit hash + datum stažení
├── working_project/      <- pracovní kopie, do které se zapisují uživatelovy volby
└── config_profiles/
    └── settings.json     <- trvalá nastavení uživatele (jazyk atd.)
"""

from pathlib import Path

APP_DIR = Path.home() / "ESP32_Sound_Configurator"

VENDOR_SNAPSHOT_DIR = APP_DIR / "vendor_snapshot"
VENDOR_VERSION_FILE = VENDOR_SNAPSHOT_DIR / "version.json"

WORKING_PROJECT_DIR = APP_DIR / "working_project"

CONFIG_PROFILES_DIR = APP_DIR / "config_profiles"
SETTINGS_FILE = CONFIG_PROFILES_DIR / "settings.json"

# GitHub repozitář originálního projektu
GITHUB_OWNER = "TheDIYGuy999"
GITHUB_REPO = "Rc_Engine_Sound_ESP32"
GITHUB_BRANCH = "master"

GITHUB_API_LATEST_COMMIT = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/commits/{GITHUB_BRANCH}"
)
GITHUB_ZIP_URL = (
    f"https://codeload.github.com/{GITHUB_OWNER}/{GITHUB_REPO}/zip/refs/heads/{GITHUB_BRANCH}"
)


def ensure_directories() -> None:
    """Vytvoří všechny potřebné adresáře, pokud ještě neexistují."""
    APP_DIR.mkdir(parents=True, exist_ok=True)
    VENDOR_SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    WORKING_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PROFILES_DIR.mkdir(parents=True, exist_ok=True)
