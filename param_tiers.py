"""
Klasifikace parametrů vozidel do tří úrovní důležitosti, podle logiky
domluvené s uživatelem:

- "green"  (nutno nastavit)   - věci vázané na fyzický hardware/ovládání
             modelu. Když je to špatně, model se nebude chovat správně
             nebo vůbec (typ desky, PWM/PPM kalibrace ESC, typ vozidla
             jako tank/rypadlo/jeřáb, zapojení světel).
- "yellow" (doporučeno nastavit) - zapnutí/vypnutí funkce (turbo ano/ne)
             nebo výběr KONKRÉTNÍHO zvukového souboru (jaký klakson).
             Výchozí hodnota funguje, ale stojí za to si to doladit podle
             vlastního vkusu.
- "red"    (nešahat) - jemné číselné doladění už zapnuté/vybrané zvukové
             funkce (hlasitosti, prahy, intervaly), které autor projektu
             už vyladil tak, aby to dohromady znělo dobře. Změna
             jednotlivých čísel může tuhle rovnováhu rozbít.

Výchozí pravidlo podle typu parametru (pokud není v seznamu níže
explicitně přepsáno):
- flag / boolean_value  -> yellow (zapnutí/vypnutí funkce)
- number / percentage   -> red    (jemné číselné doladění)
- sound_choice          -> yellow (výběr konkrétního zvukového souboru)
"""

import json
from typing import Optional

from paths import CONFIG_PROFILES_DIR, ensure_directories

# Parametry vázané na fyzický hardware/ovládání - špatná hodnota reálně
# rozbije funkčnost, ne jen zvuk.
GREEN_PARAMS: set[str] = {
    # Základní typ/režim vozidla - určuje, jak se čte řízení z vysílačky
    "TRACKED_MODE",
    "AIRPLANE_MODE",
    "EXCAVATOR_MODE",
    "LOADER_MODE",
    "CRANE_MODE",
    "STEAM_LOCOMOTIVE_MODE",
    "DUMP_BED",
    "HYDROSTATIC_TRACK_MOTORS",

    # Zapojení světel/blinkrů - musí sedět s tím, jak je model fyzicky zapojený
    "SEPARATE_FULL_BEAM",
    "INDICATOR_SIDE_MARKERS",
    "INDICATOR_DIR",

    # PWM/PPM a ESC kalibrace - musí sedět s konkrétním ESC/přijímačem
    "pwmStrokeChainDriveTopSpeed",
    "pwmStrokeChainDriveStartRotation",
    "pwmSoundTrigger",
    "engineManualOnOff",
    "escRampTimeFirstGear",
    "escRampTimeSecondGear",
    "escRampTimeThirdGear",
    "escBrakeSteps",
    "escAccelerationSteps",
    "MAX_RPM_PERCENTAGE",
    "acc",
    "dec",

    # --- 2_Remote.h ---
    "sbusBaud",
    "sbusFailsafeTimeout",
    "channelAutoZero",
    "channelReversed",

    # --- 7_Servos.h --- (servo/ESC kalibrace - musí sedět s fyzickým servem)
    "CH1L", "CH1C", "CH1R", "CH1_RAMP_TIME",
    "CH2L", "CH2C", "CH2R", "CH2_RAMP_TIME",
    "CH3L", "CH3C", "CH3R", "CH3_RAMP_TIME", "CH3_BEACON",
    "CH4L", "CH4C", "CH4R", "CH4_RAMP_TIME",
    "ESC_L", "ESC_C", "ESC_R", "ESC_MIN", "ESC_MAX",
    "MODE2_HYDRAULIC", "MODE2_TRAILER_UNLOCKING", "MODE2_WINCH",
    "NO_WINCH_DELAY", "PINGON_MODE", "SERVO_FREQUENCY",
    "STEERING_RAMP_TIME", "boomDownwardsHydraulic",

    # --- 5_Shaker.h --- (musí sedět s fyzickým shakerem)
    "shakerStart", "shakerIdle", "shakerFullThrottle", "shakerStop",

    # --- 0_generalSettings.h ---
    "WEMOS_D1_MINI_ESP32",
    "ENABLE_WIRELESS",

    # --- 3_ESC.h --- (běžná ESC/motor kalibrace - přesně to, co má uživatel doladit)
    "QUICRUN_FUSION",
    "QUICRUN_16BL30",
    "ESC_DIR",
    "HYDROSTATIC_MODE",
    "directionChangeLimit",
    "RZ7886_DRIVER_MODE",
    "RZ7886_FREQUENCY",
    "RZ7886_DRAGBRAKE_DUTY",
    "escPulseSpan",
    "escTakeoffPunch",
    "escReversePlus",
    "crawlerEscRampTime",
    "BATTERY_PROTECTION",

    # --- 4_Transmission.h --- (musí sedět s reálnou převodovkou)
    "VIRTUAL_3_SPEED",
    "automaticReverseAccelerationPercentage",
    "lowRangePercentage",
    "SEMI_AUTOMATIC",
    "MODE1_SHIFTING",
    "maxClutchSlippingRpm",
    "DOUBLE_CLUTCH",

    # --- 6_Lights.h --- (musí sedět s fyzickým zapojením/počtem světel)
    "NEOPIXEL_ENABLED",
    "NEOPIXEL_ON_CH4",
    "NEOPIXEL_COUNT",
    "MAX_POWER_MILLIAMPS",
    "THIRD_BRAKELIGHT",
    "ROTATINGBEACON_ON_B1",
    "noCabLights",
    "noFogLights",
    "swap_L_R_indicators",
    "indicatorsAsSidemarkers",
    "separateFullBeam",

    # --- 9_Dashboard.h ---
    "SPI_DASHBOARD",
    "FREVIC_DASHBOARD",
    "dashRotation",
    "MAX_REAL_SPEED",
    "manualGearRatios",

    # --- 10_Trailer.h ---
    "TRAILER_LIGHTS_TRAILER_PRESENCE_SWITCH_DEPENDENT",
    "defaultUseTrailer1",
    "defaultUseTrailer2",
    "defaultUseTrailer3",
}

# Výchozí barva CELÝCH karet nahoře stránky (Vozidlo, ESC a baterie...) -
# vozidlo a dálkové ovládání jsou zelené (vždy vidět, bez nich se model
# nerozjede správně), zbytek má rozumné výchozí hodnoty a dá se použít
# beze změny (viz eepromInit() v originále - zapíše se jen jednou při
# prvním startu), takže je defaultně žlutá.
TAB_TIERS: dict[str, str] = {
    "vehicle": "green",
    "remote": "green",
    "servos": "yellow",
    "shaker": "yellow",
    "general": "yellow",
    "esc": "yellow",
    "transmission": "yellow",
    "lights": "yellow",
    "sound": "yellow",
    "dashboard": "yellow",
    "trailer": "yellow",
    "web": "yellow",
}

# Parametry, u kterých autor projektu výslovně varuje před úpravou
# ("experimental", "never more than", "may damage", "always X") nebo jde
# o čistě ladicí/vývojářské přepínače - defaultně nešahat, i když to
# formálně vypadá jako obyčejné číslo/přepínač.
RED_PARAM_OVERRIDES: set[str] = {
    # --- 2_Remote.h ---
    "PROTOTYPE_36",  # "do not uncomment it or it will cause boot issues!"
    "EMBEDDED_SBUS",  # "recommended, don't change it"

    # --- 0_generalSettings.h ---
    "DEBUG", "CHANNEL_DEBUG", "ESC_DEBUG", "AUTO_TRANS_DEBUG",
    "MANUAL_TRANS_DEBUG", "TRACKED_DEBUG", "SERVO_DEBUG", "ESPNOW_DEBUG",
    "CORE_DEBUG", "ERASE_EEPROM_ON_BOOT", "eeprom_id",

    # --- 3_ESC.h ---
    "brakeMargin", "globalAccelerationPercentage",
    "CUTOFF_VOLTAGE", "FULLY_CHARGED_VOLTAGE", "RECOVERY_HYSTERESIS",
    "RESISTOR_TO_BATTTERY_PLUS", "RESISTOR_TO_GND", "DIODE_DROP",

    # --- 4_Transmission.h ---
    "VIRTUAL_16_SPEED_SEQUENTIAL",

    # --- 8_Sound.h ---
    "numberOfVolumeSteps",  # vázané na pole, které zatím needitujeme

    # --- 9_Dashboard.h ---
    "RPM_MAX",  # komentář autora: "always 500"
}

# Parametry typu "number", které navzdory obecnému pravidlu (red) patří
# spíš mezi doporučené stylové volby, ne jemné vyladění zvuku.
YELLOW_NUMBER_OVERRIDES: set[str] = {
    "NumberOfAutomaticGears",
    "NEOPIXEL_BRIGHTNESS",
    "neopixelMode",
    "cabLightsBrightness",
    "sideLightsBrightness",
    "rearlightDimmedBrightness",
    "rearlightParkingBrightness",
    "headlightParkingBrightness",
    "reversingLightBrightness",
    "fogLightBrightness",
    "masterVolumeCrawlerThreshold",
    "outOfFuelVolumePercentage",
}

TIER_RED = "red"
TIER_YELLOW = "yellow"
TIER_GREEN = "green"

_RENDER_KIND_TO_DEFAULT_TIER = {
    "flag": TIER_YELLOW,
    "boolean_value": TIER_YELLOW,
    "percentage_slider": TIER_RED,
    "number_input": TIER_RED,
    "sound_choice": TIER_YELLOW,
    "flag_choice": TIER_GREEN,
    "array": TIER_RED,
    "string": TIER_YELLOW,
}

# ---------------------------------------------------------------------------
# Ladicí režim - dočasné ruční přepsání barvy (a volitelná poznámka proč)
# přes GUI. Ukládá se do souboru, aby přežilo i restart programu, dokud
# si to Tomáš neexportuje a nepošle zpět ke trvalému zapracování do kódu
# výše - export pak obsahuje i poznámky, aby Claude věděl PROČ danou
# barvu chce, a mohl to dávkově zapracovat i s odůvodněním.
#
# Tři oddělené scope, každý má stejný tvar {klíč: {"tier": ..., "note": ...}}:
# - "params"     - barva/poznámka jednotlivé položky (jen informativní,
#                  na filtr nemá vliv)
# - "categories" - barva/poznámka celé složky - TA rozhoduje o viditelnosti
#                  podle filtru, bez ohledu na barvy položek uvnitř
# - "tabs"       - barva/poznámka celé karty nahoře stránky - stejný princip
# ---------------------------------------------------------------------------

_OVERRIDES_FILE = CONFIG_PROFILES_DIR / "tier_overrides_draft.json"
_SCOPES = ("params", "categories", "tabs")


def _load_overrides_file() -> dict:
    if not _OVERRIDES_FILE.exists():
        return {s: {} for s in _SCOPES}
    try:
        data = json.loads(_OVERRIDES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {s: {} for s in _SCOPES}
    for s in _SCOPES:
        data.setdefault(s, {})
    return data


def _save_overrides_file(data: dict) -> None:
    ensure_directories()
    _OVERRIDES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _set_override(scope: str, key: str, tier: Optional[str] = None, note: Optional[str] = None) -> None:
    data = _load_overrides_file()
    entry = dict(data[scope].get(key, {}))
    if tier is not None:
        if tier == "default":
            entry.pop("tier", None)
        else:
            entry["tier"] = tier
    if note is not None:
        if note == "":
            entry.pop("note", None)
        else:
            entry["note"] = note
    if entry:
        data[scope][key] = entry
    else:
        data[scope].pop(key, None)
    _save_overrides_file(data)


def _get_override_tier(scope: str, key: str) -> Optional[str]:
    entry = _load_overrides_file()[scope].get(key)
    return entry.get("tier") if entry else None


def load_debug_overrides() -> dict[str, str]:
    """Zpětná kompatibilita - jen tier parametrových přebití (bez poznámek)."""
    return {k: v["tier"] for k, v in _load_overrides_file()["params"].items() if "tier" in v}


def set_debug_override(name: str, tier: str) -> None:
    _set_override("params", name, tier=tier)


def set_param_note(name: str, note: str) -> None:
    _set_override("params", name, note=note)


def load_category_overrides() -> dict[str, str]:
    return {k: v["tier"] for k, v in _load_overrides_file()["categories"].items() if "tier" in v}


def set_category_tier_override(category_key: str, tier: str) -> None:
    _set_override("categories", category_key, tier=tier)


def set_category_note(category_key: str, note: str) -> None:
    _set_override("categories", category_key, note=note)


def set_tab_tier_override(key: str, tier: str) -> None:
    _set_override("tabs", key, tier=tier)


def set_tab_note(key: str, note: str) -> None:
    _set_override("tabs", key, note=note)


_SCOPE_FILE_KEY = {"param": "params", "category": "categories", "tab": "tabs"}


def get_note(scope: str, key: str) -> str:
    file_key = _SCOPE_FILE_KEY.get(scope, scope)
    entry = _load_overrides_file()[file_key].get(key)
    return entry.get("note", "") if entry else ""


def get_tab_tier(key: str) -> str:
    tier = _get_override_tier("tabs", key)
    return tier if tier is not None else TAB_TIERS.get(key, TIER_YELLOW)


def clear_debug_overrides() -> None:
    _save_overrides_file({s: {} for s in _SCOPES})


def export_overrides() -> dict:
    return _load_overrides_file()


_SEVERITY_ORDER = [TIER_GREEN, TIER_YELLOW, TIER_RED]  # zelena ma prednost jako vychozi odhad


def get_category_tier(category_key: str, member_tiers: list[str]) -> str:
    """
    Vrátí barvu CELÉ složky (kategorie) - rozhoduje o viditelnosti podle
    filtru, bez ohledu na to, jaké barvy mají jednotlivé položky uvnitř.

    Pokud si to Tomáš přes ladicí režim nastavil ručně, použije se to.
    Jinak se spočítá rozumný výchozí odhad: pokud je uvnitř aspoň jedna
    zelená položka, celá složka je defaultně zelená (ať ji beginner
    nepřehlédne), jinak žlutá, jinak červená.
    """
    override_tier = _get_override_tier("categories", category_key)
    if override_tier is not None:
        return override_tier
    present = set(member_tiers)
    for tier in _SEVERITY_ORDER:
        if tier in present:
            return tier
    return TIER_YELLOW


def _base_name(name: str) -> str:
    """Pro položky pole typu 'channelAutoZero[CH1]' vrátí jen 'channelAutoZero'."""
    idx = name.find("[")
    return name[:idx] if idx != -1 else name


def get_param_tier(name: str, render_kind: str) -> str:
    overrides = load_debug_overrides()
    if name in overrides:
        return overrides[name]
    base = _base_name(name)
    if base in overrides:
        return overrides[base]
    if base in GREEN_PARAMS:
        return TIER_GREEN
    if base in RED_PARAM_OVERRIDES:
        return TIER_RED
    if base in YELLOW_NUMBER_OVERRIDES:
        return TIER_YELLOW
    return _RENDER_KIND_TO_DEFAULT_TIER.get(render_kind, TIER_YELLOW)
