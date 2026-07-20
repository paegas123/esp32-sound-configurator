"""
Lokální webserver pro GUI verzi TankSound Configurátoru.

Používá jen vestavěné knihovny Pythonu (http.server) - žádné externí
závislosti navíc, stejně jako terminálová verze. Slouží dvě věci:
1. Servíruje statické soubory frontendu (web/index.html, app.js, style.css)
2. Poskytuje JSON API pod /api/..., které volá stejné moduly jako cli.py
   (vehicle_parser, updater, param_translations, pio_runner, sound_convert)

Stav (vybrané vozidlo, jeho rozparsované parametry) se drží v paměti
procesu mezi jednotlivými HTTP requesty - je to lokální nástroj pro
jednoho uživatele najednou, takže jednoduchý globální stav stačí a je
mnohem jednodušší než řešit session cookies apod.
"""

import json
import shutil
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import pio_runner
import platformio_ini
import param_tiers
import settings
import sound_convert
import updater
import vehicle_parser as vp
from i18n import Translator, get_texts
from paths import VENDOR_SNAPSHOT_DIR, WORKING_PROJECT_DIR, ensure_directories
from param_translations import translate_category, translate_param_explanation
from param_labels import get_param_label, get_option_label

from app_paths import get_base_dir

WEB_DIR = get_base_dir() / "web"
PORT = 8743  # nahodne zvolene cislo portu, nepravdepodobne ze koliduje s necim jinym

# Registr "jednoduchých" nastavovacích souborů (ploché seznamy přepínačů/čísel),
# které se dají zobrazit stejným způsobem jako parametry vozidla - klíč je
# identifikátor karty v GUI, hodnota je cesta relativně k src/ adresáři
# pracovního projektu. Vozidlo (1_Vehicle.h) má vlastní speciální logiku
# (viz _api_select_vehicle) kvůli výběru ze seznamu, proto tady není.
SETTINGS_FILE_TABS: list[tuple[str, str, str]] = [
    # (klíč, popisek karty, relativní cesta v src/)
    ("remote", "Dálkové ovládání", "2_Remote.h"),
    ("servos", "Servo výstupy", "7_Servos.h"),
    ("shaker", "Otřesy motoru (shaker)", "5_Shaker.h"),
    ("general", "Obecná nastavení", "0_generalSettings.h"),
    ("esc", "ESC a baterie", "3_ESC.h"),
    ("transmission", "Převodovka", "4_Transmission.h"),
    ("lights", "Světla", "6_Lights.h"),
    ("sound", "Zvuk (obecné)", "8_Sound.h"),
    ("dashboard", "Palubní deska", "9_Dashboard.h"),
    ("trailer", "Přívěs", "10_Trailer.h"),
]

# --- globalni stav procesu (jednoduche, protoze jde o lokalni nastroj pro jednoho cloveka) ---
_state_lock = threading.Lock()
_current_vehicle_file: "vp.VehicleFile | None" = None

# Program běží jako neviditelný server na pozadí - i po zavření okna
# prohlížeče by jinak visel dál (viditelné jen v Aktivitě/Task Manageru).
# Prohlížeč posílá pravidelný "jsem pořád otevřený" signál (viz
# /api/heartbeat), a pokud dlouho nepřijde žádný požadavek vůbec, program
# se sám tiše ukončí.
_last_activity_time = time.time()
_HEARTBEAT_TIMEOUT_SECONDS = 45
_current_vehicle_entry: "vp.VehicleEntry | None" = None
_jobs: dict[str, dict] = {}  # job_id -> {"lines": [...], "status": "running"/"done"/"error", "process": Popen|None}
_job_counter = 0


def _new_job_id() -> str:
    global _job_counter
    _job_counter += 1
    return f"job{_job_counter}"


def _working_paths():
    src_dir = WORKING_PROJECT_DIR / "src"
    return {
        "src_dir": src_dir,
        "general_settings": src_dir / "0_generalSettings.h",
        "vehicle_h": src_dir / "1_Vehicle.h",
        "vehicles_dir": src_dir / "vehicles",
        "sounds_dir": src_dir / "vehicles" / "sounds",
        "platformio_ini": WORKING_PROJECT_DIR / "platformio.ini",
    }


def _get_translator() -> Translator:
    lang = settings.get_language() or "cs"
    return Translator(lang)


_LIGHT_PIN_MAP = [
    ("Přední světla (potkávací)", "HEADLIGHT_PIN", {"general": 22, "wemos": 3}),
    ("Světla v kabině", "CABLIGHT_PIN", {"general": None, "wemos": 22}),
    ("Zadní/brzdová světla (kombinované)", "TAILLIGHT_PIN", {"general": 15, "wemos": 15}),
    ("Levý blinkr", "INDICATOR_LEFT_PIN", {"general": 2, "wemos": 2}),
    ("Pravý blinkr", "INDICATOR_RIGHT_PIN", {"general": 4, "wemos": 4}),
    ("Mlhová světla", "FOGLIGHT_PIN", {"general": 16, "wemos": 16}),
    ("Couvací světlo", "REVERSING_LIGHT_PIN", {"general": 17, "wemos": 17}),
    ("Střešní/dálková světla (jen se SEPARATE_FULL_BEAM)", "ROOFLIGHT_PIN", {"general": 5, "wemos": 5}),
    ("Boční obrysová světla", "SIDELIGHT_PIN", {"general": 18, "wemos": 18}),
    ("Modrý maják 1", "BEACON_LIGHT1_PIN", {"general": 21, "wemos": 21}),
    ("Modrý maják 2", "BEACON_LIGHT2_PIN", {"general": 19, "wemos": 19}),
    ("Horní brzdové světlo", "BRAKELIGHT_PIN", {"general": 32, "wemos": 32}),
]


def _build_light_pin_map(board_is_wemos: bool) -> list[dict]:
    board_key = "wemos" if board_is_wemos else "general"
    entries = []
    for label, define_name, pins in _LIGHT_PIN_MAP:
        pin = pins[board_key]
        entries.append({
            "function": label,
            "pin": f"GPIO {pin}" if pin is not None else None,
            "defineName": define_name,
            "unused": pin is None,
        })
    return entries


def _serialize_params(vf: vp.VehicleFile, lang: str) -> dict:
    categories: list[dict] = []
    current_category_name = None
    current_category_raw = None
    current_category_params: list = []

    # Pokud tenhle soubor má na začátku "výběr profilu" (Remote/Servos/
    # Shaker), zjistíme, který profil je právě aktivní - vše, co patří
    # jinému profilu (viz .profile_owner nastavené parserem), se do
    # výstupu vůbec nezahrne, aby uživatel viděl jen to, co se ho týká.
    active_profile_name = None
    for param in vf.params:
        if param.kind == "flag_choice":
            active = param.active_option
            if active:
                active_profile_name = active.name
            break

    def flush():
        if current_category_name is not None and current_category_params:
            member_tiers = [p["tier"] for p in current_category_params]
            category_tier = param_tiers.get_category_tier(current_category_raw, member_tiers)
            display_name = current_category_name or get_texts(lang).get(
                "default_category_label", "Nastavení"
            )
            categories.append({
                "name": display_name,
                "categoryKey": current_category_raw,
                "params": current_category_params,
                "tier": category_tier,
                "note": param_tiers.get_note("category", current_category_raw),
                "autoExpand": not current_category_name,
            })

    for idx, param in enumerate(vf.params):
        owner = getattr(param, "profile_owner", None)
        if owner is not None and owner != active_profile_name:
            continue

        cat_name = translate_category(param.category, lang)
        if cat_name != current_category_name:
            flush()
            current_category_name = cat_name
            current_category_raw = param.category
            current_category_params = []

        if param.kind == "flag":
            current_category_params.append({
                "index": idx,
                "kind": "flag",
                "name": param.name,
                "label": get_param_label(param.name, lang, param.name),
                "explanation": translate_param_explanation(param.name, param.comment, lang),
                "active": param.active,
                "tier": param_tiers.get_param_tier(param.name, "flag"),
                "tierKey": param.name,
                "note": param_tiers.get_note("param", param.name),
            })
        elif param.kind == "number":
            value = param.value.strip()
            if value in ("true", "false"):
                render_kind = "boolean_value"
            elif "percentage" in param.name.lower():
                render_kind = "percentage_slider"
            else:
                render_kind = "number_input"
            current_category_params.append({
                "index": idx,
                "kind": render_kind,
                "name": param.name,
                "label": get_param_label(param.name, lang, param.name),
                "explanation": translate_param_explanation(param.name, param.comment, lang),
                "value": value,
                "tier": param_tiers.get_param_tier(param.name, render_kind),
                "tierKey": param.name,
                "note": param_tiers.get_note("param", param.name),
            })
        elif param.kind == "flag_choice":
            texts = get_texts(lang)
            current_category_params.append({
                "index": idx,
                "kind": "flag_choice",
                "label": texts.get("param_type_choice", "Volba"),
                "options": [
                    {"name": o.name, "description": get_option_label(o.name, lang, o.description), "active": o.active}
                    for o in param.options
                ],
                "tier": param_tiers.get_param_tier(param.category, "flag_choice"),
                "tierKey": param.category,
                "note": param_tiers.get_note("param", param.category),
            })
        elif param.kind == "sound_choice":
            texts = get_texts(lang)
            current_category_params.append({
                "index": idx,
                "kind": "sound_choice",
                "label": texts.get("param_type_sound_choice", "Zvuk"),
                "options": [
                    {"filename": o.filename, "description": o.description, "active": o.active}
                    for o in param.options
                ],
                "tier": param_tiers.get_param_tier(param.category, "sound_choice"),
                "tierKey": param.category,
                "note": param_tiers.get_note("param", param.category),
            })
        elif param.kind == "array":
            current_category_params.append({
                "index": idx,
                "kind": "array",
                "name": param.name,
                "label": get_param_label(param.name, lang, param.name),
                "explanation": translate_param_explanation(param.name, param.comment, lang),
                "value": param.items_raw,
                "tier": param_tiers.get_param_tier(param.name, "array"),
                "tierKey": param.name,
                "note": param_tiers.get_note("param", param.name),
            })
        elif param.kind == "string":
            current_category_params.append({
                "index": idx,
                "kind": "string",
                "name": param.name,
                "label": get_param_label(param.name, lang, param.name),
                "explanation": translate_param_explanation(param.name, param.comment, lang),
                "value": param.value,
                "tier": param_tiers.get_param_tier(param.name, "string"),
                "tierKey": param.name,
                "note": param_tiers.get_note("param", param.name),
            })

    flush()
    return {
        "vehicleName": vf.vehicle_name,
        "categories": categories,
        "channelMap": _build_channel_map(vf, active_profile_name, lang),
    }


# Pořadí a názvy kanálových přiřazení, která se hledají pro vizuální
# tabulku "kanál -> funkce" (viz 2_Remote.h). Vždy viditelné nezávisle
# na zvolené úrovni (začátečník/pokročilý/expert).
_CHANNEL_FUNCTION_NAMES = [
    "STEERING", "GEARBOX", "THROTTLE", "HORN", "POT2", "MODE1", "MODE2",
    "MOMENTARY1", "HAZARDS", "INDICATOR_LEFT", "INDICATOR_RIGHT",
    "FUNCTION_L", "FUNCTION_R", "CH_14", "CH_15", "CH_16",
]


def _build_channel_map(vf: vp.VehicleFile, active_profile_name, lang: str) -> list[dict]:
    entries = []
    for param in vf.params:
        if param.kind != "number" or param.name not in _CHANNEL_FUNCTION_NAMES:
            continue
        owner = getattr(param, "profile_owner", None)
        if active_profile_name is not None and owner != active_profile_name:
            continue
        value = param.value.strip()
        function_label = get_param_label(param.name, lang, param.name)
        entries.append({
            "channel": value,  # číslo kanálu z přijímače, nebo "NONE" pokud nevyužito
            "function": function_label,
            "unused": value.upper() == "NONE",
        })

    def sort_key(e):
        try:
            return (0, int(e["channel"]))
        except ValueError:
            return (1, 0)

    entries.sort(key=sort_key)
    return entries


def _ensure_working_copy_prepared():
    """Připraví working_project (kopie + připnutí verze platformy), pokud ještě neexistuje pro tento běh."""
    if WORKING_PROJECT_DIR.exists() and (WORKING_PROJECT_DIR / "platformio.ini").exists():
        return
    if WORKING_PROJECT_DIR.exists():
        shutil.rmtree(WORKING_PROJECT_DIR)
    shutil.copytree(VENDOR_SNAPSHOT_DIR, WORKING_PROJECT_DIR)
    paths = _working_paths()
    if paths["platformio_ini"].exists():
        platformio_ini.pin_compatible_platform_version(paths["platformio_ini"])


def _run_job_upload(job_id: str) -> None:
    job = _jobs[job_id]
    job["lines"].append("Spouštím nahrávání firmwaru...")
    pio_runner.ensure_known_dependencies()
    try:
        result = pio_runner.run_pio_with_auto_dependency_fix(
            ["run", "--target", "upload"], cwd=str(WORKING_PROJECT_DIR)
        )
        for line in (result.stdout or "").splitlines():
            job["lines"].append(line)
        if result.returncode == 0:
            job["status"] = "done"
            job["lines"].append("--- Nahrávání dokončeno úspěšně ---")
        else:
            job["status"] = "error"
            job["lines"].append("--- Nahrávání selhalo ---")
            for line in (result.stderr or "").splitlines():
                job["lines"].append(line)
    except Exception as e:
        job["status"] = "error"
        job["lines"].append(f"Neočekávaná chyba: {e}")


def _run_job_monitor(job_id: str) -> None:
    import subprocess

    job = _jobs[job_id]
    job["lines"].append("Připojuji se k desce...")
    try:
        process = subprocess.Popen(
            ["pio", "device", "monitor"],
            cwd=str(WORKING_PROJECT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        job["process"] = process
        for line in process.stdout:
            job["lines"].append(line.rstrip("\n"))
            if job.get("stop_requested"):
                break
        job["status"] = "done"
    except FileNotFoundError:
        job["status"] = "error"
        job["lines"].append("Nepodařilo se spustit 'pio' - je PlatformIO nainstalované?")
    except Exception as e:
        job["status"] = "error"
        job["lines"].append(f"Neočekávaná chyba: {e}")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # ztlumeni defaultniho logovani do konzole

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, data: bytes, content_type: str):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    # ---------------------------------------------------------------- GET
    def do_GET(self):
        global _last_activity_time
        _last_activity_time = time.time()
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            return self._serve_static("index.html", "text/html; charset=utf-8")
        if path == "/app.js":
            return self._serve_static("app.js", "application/javascript; charset=utf-8")
        if path == "/style.css":
            return self._serve_static("style.css", "text/css; charset=utf-8")

        if path == "/api/bootstrap":
            return self._api_bootstrap()
        if path == "/api/vehicles":
            return self._api_vehicles()
        if path == "/api/board":
            return self._api_get_board()
        if path == "/api/params":
            return self._api_get_params()
        if path == "/api/filter":
            return self._api_get_filter()
        if path == "/api/tabs":
            return self._api_get_tabs()
        if path == "/api/debug/export":
            return self._api_debug_export()
        if path == "/api/heartbeat":
            return self._send_json({"ok": True})
        if path == "/api/web-interface-choice":
            return self._api_get_web_interface_choice()
        if path.startswith("/api/sound/"):
            return self._api_sound(path[len("/api/sound/"):])
        if path.startswith("/api/job/"):
            job_id = path[len("/api/job/"):]
            since = int(query.get("since", ["0"])[0])
            return self._api_job_poll(job_id, since)

        self._send_json({"error": "not found"}, 404)

    def _serve_static(self, filename: str, content_type: str):
        file_path = WEB_DIR / filename
        if not file_path.exists():
            self._send_json({"error": f"missing static file {filename}"}, 404)
            return
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        # Bez tohohle si prohlížeč občas nechá starou verzi HTML/JS v
        # keši, i když se soubory na disku mezitím změnily (např. po
        # aktualizaci programu) - pak si nový JS a starý HTML "nerozumí".
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(data)

    # --------------------------------------------------------------- POST
    def do_POST(self):
        global _last_activity_time
        _last_activity_time = time.time()
        path = urlparse(self.path).path
        try:
            body = self._read_json_body()
        except (json.JSONDecodeError, ValueError):
            return self._send_json({"error": "invalid JSON body"}, 400)

        routes = {
            "/api/language": self._api_set_language,
            "/api/check-update": self._api_check_update,
            "/api/download-update": self._api_download_update,
            "/api/board": self._api_set_board,
            "/api/select-vehicle": self._api_select_vehicle,
            "/api/select-settings-file": self._api_select_settings_file,
            "/api/param": self._api_set_param,
            "/api/save": self._api_save,
            "/api/filter": self._api_set_filter,
            "/api/debug/set-tier": self._api_debug_set_tier,
            "/api/debug/set-category-tier": self._api_debug_set_category_tier,
            "/api/debug/set-tab-tier": self._api_debug_set_tab_tier,
            "/api/debug/set-note": self._api_debug_set_note,
            "/api/web-interface-choice": self._api_set_web_interface_choice,
            "/api/shutdown": self._api_shutdown,
            "/api/debug/clear": self._api_debug_clear,
            "/api/upload": self._api_start_upload,
            "/api/monitor/start": self._api_start_monitor,
            "/api/monitor/stop": self._api_stop_monitor,
        }
        handler = routes.get(path)
        if handler is None:
            return self._send_json({"error": "not found"}, 404)
        handler(body)

    # ------------------------------------------------------------ handlery

    def _api_bootstrap(self):
        lang = settings.get_language()
        self._send_json({
            "language": lang,
            "hasLocalCopy": updater.has_local_copy(),
        })

    def _api_set_language(self, body):
        lang = body.get("lang")
        if lang not in ("cs", "en", "de"):
            return self._send_json({"error": "unsupported language"}, 400)
        settings.set_language(lang)
        self._send_json({"ok": True})

    def _api_check_update(self, body):
        remote_info = updater.check_internet_and_get_latest_commit()
        if remote_info is None:
            if updater.has_local_copy():
                return self._send_json({"status": "no_internet_using_local"})
            return self._send_json({"status": "no_internet_no_local"})
        if not updater.has_local_copy():
            return self._send_json({"status": "first_download_needed", "remoteDate": remote_info.date})
        if updater.is_up_to_date(remote_info):
            return self._send_json({"status": "up_to_date"})
        local = updater.load_local_version() or {}
        self._send_json({
            "status": "update_available",
            "remoteDate": remote_info.date,
            "localDate": local.get("date", "?"),
        })

    def _api_download_update(self, body):
        remote_info = updater.check_internet_and_get_latest_commit()
        if remote_info is None:
            return self._send_json({"ok": False, "error": "no internet"}, 400)
        try:
            updater.download_and_replace_snapshot(remote_info)
        except Exception as e:
            return self._send_json({"ok": False, "error": str(e)}, 500)
        self._send_json({"ok": True})

    def _api_get_filter(self):
        self._send_json({"mode": settings.get_level_mode()})

    def _api_set_filter(self, body):
        mode = body.get("mode")
        if mode not in ("green", "yellow", "red"):
            return self._send_json({"error": "neplatny rezim"}, 400)
        settings.set_level_mode(mode)
        self._send_json({"ok": True})

    def _api_debug_set_tier(self, body):
        name = body.get("name")
        tier = body.get("tier")
        if name is None or tier not in ("red", "yellow", "green", "default"):
            return self._send_json({"error": "neplatny pozadavek"}, 400)
        param_tiers.set_debug_override(name, tier)
        self._send_json({"ok": True})

    def _api_debug_set_category_tier(self, body):
        key = body.get("key")
        tier = body.get("tier")
        if key is None or tier not in ("red", "yellow", "green", "default"):
            return self._send_json({"error": "neplatny pozadavek"}, 400)
        param_tiers.set_category_tier_override(key, tier)
        self._send_json({"ok": True})

    def _api_debug_set_tab_tier(self, body):
        key = body.get("key")
        tier = body.get("tier")
        if key is None or tier not in ("red", "yellow", "green", "default"):
            return self._send_json({"error": "neplatny pozadavek"}, 400)
        param_tiers.set_tab_tier_override(key, tier)
        self._send_json({"ok": True})

    def _api_debug_set_note(self, body):
        scope = body.get("scope")
        key = body.get("key")
        note = body.get("note", "")
        if key is None or scope not in ("param", "category", "tab"):
            return self._send_json({"error": "neplatny pozadavek"}, 400)
        if scope == "param":
            param_tiers.set_param_note(key, note)
        elif scope == "category":
            param_tiers.set_category_note(key, note)
        else:
            param_tiers.set_tab_note(key, note)
        self._send_json({"ok": True})

    def _api_get_web_interface_choice(self):
        self._send_json({"choice": settings.get_web_interface_choice()})

    def _api_set_web_interface_choice(self, body):
        choice = body.get("choice")
        if choice not in ("original", "new"):
            return self._send_json({"error": "neplatna volba"}, 400)
        settings.set_web_interface_choice(choice)
        self._send_json({"ok": True})

    def _api_debug_clear(self, body):
        param_tiers.clear_debug_overrides()
        self._send_json({"ok": True})

    def _api_debug_export(self):
        overrides = param_tiers.export_overrides()
        body = json.dumps(overrides, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Disposition", "attachment; filename=tier_overrides.json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _api_shutdown(self, body):
        self._send_json({"ok": True})

        def _do_shutdown():
            time.sleep(0.3)  # dej strihanci cas odeslat odpoved prohlizeci
            self.server.shutdown()

        threading.Thread(target=_do_shutdown, daemon=True).start()

    def _api_vehicles(self):
        ensure_directories()
        if not updater.has_local_copy():
            return self._send_json({"error": "no local copy yet"}, 400)
        paths = _working_paths()
        # Seznam vozidel muzeme cist rovnou z vendor_snapshot (neni potreba working_project)
        source_vehicle_h = VENDOR_SNAPSHOT_DIR / "src" / "1_Vehicle.h"
        entries = vp.parse_vehicle_list(source_vehicle_h)
        self._send_json({
            "vehicles": [
                {
                    "index": i,
                    "filename": e.filename,
                    "name": e.description or e.filename[:-2],
                    "category": e.category,
                    "active": e.active,
                }
                for i, e in enumerate(entries)
            ]
        })

    def _api_get_tabs(self):
        tabs = [{"key": "vehicle", "label": "Vozidlo"}]
        tabs += [{"key": key, "label": label} for key, label, _rel_path in SETTINGS_FILE_TABS]
        tabs.append({"key": "web", "label": "Web"})
        for tab in tabs:
            tab["tier"] = param_tiers.get_tab_tier(tab["key"])
            tab["note"] = param_tiers.get_note("tab", tab["key"])
        self._send_json({"tabs": tabs})

    def _api_select_settings_file(self, body):
        global _current_vehicle_file, _current_vehicle_entry
        key = body.get("key")
        match = next((t for t in SETTINGS_FILE_TABS if t[0] == key), None)
        if match is None:
            return self._send_json({"error": f"neznámá karta '{key}'"}, 400)

        _ensure_working_copy_prepared()
        _, _label, rel_path = match
        file_path = WORKING_PROJECT_DIR / "src" / rel_path
        if not file_path.exists():
            return self._send_json({"error": f"soubor {rel_path} nenalezen"}, 404)

        with _state_lock:
            if key == "remote":
                _current_vehicle_file = vp.parse_remote_file(file_path)
            elif key == "servos":
                _current_vehicle_file = vp.parse_servos_file(file_path)
            elif key == "shaker":
                _current_vehicle_file = vp.parse_shaker_file(file_path)
            else:
                _current_vehicle_file = vp.parse_vehicle_file(file_path)
            _current_vehicle_entry = None

        lang = settings.get_language() or "cs"
        response = _serialize_params(_current_vehicle_file, lang)
        if key == "lights":
            general_settings_path = _working_paths()["general_settings"]
            board_is_wemos = bool(vp.read_board_flag(general_settings_path))
            response["lightPinMap"] = _build_light_pin_map(board_is_wemos)
        self._send_json(response)

    def _api_get_board(self):
        _ensure_working_copy_prepared()
        paths = _working_paths()
        enabled = vp.read_board_flag(paths["general_settings"])
        self._send_json({"enabled": bool(enabled)})

    def _api_set_board(self, body):
        _ensure_working_copy_prepared()
        paths = _working_paths()
        vp.set_board_flag(paths["general_settings"], bool(body.get("enabled")))
        self._send_json({"ok": True})

    def _api_select_vehicle(self, body):
        global _current_vehicle_file, _current_vehicle_entry
        filename = body.get("filename")
        if not filename:
            return self._send_json({"error": "missing filename"}, 400)

        _ensure_working_copy_prepared()
        paths = _working_paths()
        vp.set_active_vehicle(paths["vehicle_h"], filename)

        vehicle_file_path = paths["vehicles_dir"] / filename
        if not vehicle_file_path.exists():
            return self._send_json({"error": f"soubor vozidla {filename} nenalezen"}, 404)

        with _state_lock:
            _current_vehicle_file = vp.parse_vehicle_file(vehicle_file_path)
            _current_vehicle_entry = filename

        lang = settings.get_language() or "cs"
        self._send_json(_serialize_params(_current_vehicle_file, lang))

    def _api_get_params(self):
        if _current_vehicle_file is None:
            return self._send_json({"error": "zadne vozidlo zatim neni vybrane"}, 400)
        lang = settings.get_language() or "cs"
        self._send_json(_serialize_params(_current_vehicle_file, lang))

    def _api_set_param(self, body):
        if _current_vehicle_file is None:
            return self._send_json({"error": "zadne vozidlo zatim neni vybrane"}, 400)
        idx = body.get("index")
        if idx is None or not (0 <= idx < len(_current_vehicle_file.params)):
            return self._send_json({"error": "neplatny index parametru"}, 400)

        param = _current_vehicle_file.params[idx]
        with _state_lock:
            if param.kind == "flag":
                _current_vehicle_file.set_flag_active(param, bool(body.get("active")))
            elif param.kind == "number":
                new_value = str(body.get("value"))
                _current_vehicle_file.set_number_value(param, new_value)
            elif param.kind == "sound_choice":
                _current_vehicle_file.set_sound_choice(param, body.get("filename"))
            elif param.kind == "flag_choice":
                _current_vehicle_file.set_flag_choice(param, body.get("choice"))
            elif param.kind == "array":
                _current_vehicle_file.set_array_value(param, str(body.get("value", "")))
            elif param.kind == "string":
                _current_vehicle_file.set_string_value(param, str(body.get("value", "")))
            else:
                return self._send_json({"error": "neznamy typ parametru"}, 400)

        self._send_json({"ok": True})

    def _api_save(self, body):
        if _current_vehicle_file is None:
            return self._send_json({"error": "zadne vozidlo zatim neni vybrane"}, 400)
        _current_vehicle_file.save()
        self._send_json({"ok": True})

    def _api_sound(self, rest_path: str):
        # rest_path je "<sound_filename>", napr. "IS3TankStart.h"
        filename = rest_path
        if not filename.endswith(".h"):
            return self._send_json({"error": "neplatny nazev souboru"}, 400)
        paths = _working_paths()
        sound_path = sound_convert.find_sound_header(paths["sounds_dir"], filename)
        if sound_path is None:
            # Fallback na vendor_snapshot, kdyby working_project jeste nebyl pripraveny
            sound_path = sound_convert.find_sound_header(
                VENDOR_SNAPSHOT_DIR / "src" / "vehicles" / "sounds", filename
            )
        if sound_path is None:
            return self._send_json({"error": "zvukovy soubor nenalezen"}, 404)
        try:
            wav_bytes = sound_convert.sound_header_to_wav_bytes(sound_path)
        except Exception as e:
            return self._send_json({"error": str(e)}, 500)
        self._send_bytes(wav_bytes, "audio/wav")

    def _api_start_upload(self, body):
        job_id = _new_job_id()
        _jobs[job_id] = {"lines": [], "status": "running", "process": None}
        thread = threading.Thread(target=_run_job_upload, args=(job_id,), daemon=True)
        thread.start()
        self._send_json({"jobId": job_id})

    def _api_start_monitor(self, body):
        job_id = _new_job_id()
        _jobs[job_id] = {"lines": [], "status": "running", "process": None, "stop_requested": False}
        thread = threading.Thread(target=_run_job_monitor, args=(job_id,), daemon=True)
        thread.start()
        self._send_json({"jobId": job_id})

    def _api_stop_monitor(self, body):
        job_id = body.get("jobId")
        job = _jobs.get(job_id)
        if job is None:
            return self._send_json({"error": "job nenalezen"}, 404)
        job["stop_requested"] = True
        process = job.get("process")
        if process is not None:
            try:
                process.terminate()
            except Exception:
                pass
        self._send_json({"ok": True})

    def _api_job_poll(self, job_id: str, since: int):
        job = _jobs.get(job_id)
        if job is None:
            return self._send_json({"error": "job nenalezen"}, 404)
        new_lines = job["lines"][since:]
        self._send_json({
            "status": job["status"],
            "lines": new_lines,
            "total": len(job["lines"]),
        })


def run_server():
    ensure_directories()
    url = f"http://127.0.0.1:{PORT}/"

    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError as e:
        already_running = e.errno == 48 or "in use" in str(e).lower()
        if already_running:
            # Program uz jednou bezi na pozadi (napr. z minuleho spusteni,
            # kdyz se jen zavrelo okno prohlizece) - misto padu proste
            # otevreme prohlizec na tu uz bezici instanci.
            print(f"Program už běží na pozadí - otevírám prohlížeč na {url}")
            webbrowser.open(url)
            return
        raise

    def _open_browser_delayed():
        time.sleep(0.6)
        webbrowser.open(url)

    threading.Thread(target=_open_browser_delayed, daemon=True).start()

    def _watch_for_inactivity():
        global _last_activity_time
        # Dá prohlížeči čas se poprvé načíst a začít posílat heartbeat,
        # než začneme počítat neaktivitu.
        _last_activity_time = time.time()
        while True:
            time.sleep(5)
            idle_seconds = time.time() - _last_activity_time
            if idle_seconds > _HEARTBEAT_TIMEOUT_SECONDS:
                print("Žádná aktivita v prohlížeči - program se sám ukončuje.")
                server.shutdown()
                return

    threading.Thread(target=_watch_for_inactivity, daemon=True).start()

    print(f"ESP32 Sound Configurator GUI běží na {url}")
    print("Pro ukončení stiskni Ctrl+C v tomto okně.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nUkončuji server...")
        server.shutdown()


if __name__ == "__main__":
    run_server()
