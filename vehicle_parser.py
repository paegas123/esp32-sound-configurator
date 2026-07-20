"""
Parsování a úprava:
  - src/1_Vehicle.h            (výběr aktivního vozidla)
  - src/vehicles/<Vehicle>.h   (nastavení konkrétního vozidla)
  - src/0_generalSettings.h    (výběr typu desky)

Návrhový princip: nikdy nepřepisujeme soubor "od nuly" z naparsovaných dat.
Vždy držíme originální řádky souboru (list[str]) a měníme jen konkrétní
řádky na přesně daných indexech. Díky tomu zůstane zachováno formátování,
komentáře, odsazení atd. u všeho, co se needituje.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# 0_generalSettings.h - výběr desky
# ---------------------------------------------------------------------------

BOARD_DEFINE_NAME = "WEMOS_D1_MINI_ESP32"
_board_define_re = re.compile(r"^(\s*)(//\s*)?(#define\s+" + BOARD_DEFINE_NAME + r"\b)(.*)$")


def read_board_flag(general_settings_path: Path) -> Optional[bool]:
    """Vrátí True, pokud je WEMOS_D1_MINI_ESP32 aktivní (odkomentované), False pokud
    je zakomentované, None pokud definice v souboru vůbec nebyla nalezena."""
    lines = general_settings_path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        m = _board_define_re.match(line)
        if m:
            is_commented = m.group(2) is not None
            return not is_commented
    return None


def set_board_flag(general_settings_path: Path, enabled: bool) -> None:
    lines = general_settings_path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = _board_define_re.match(line)
        if m:
            indent, _comment_prefix, define_part, rest = m.groups()
            new_line = f"{indent}{'' if enabled else '// '}{define_part}{rest}"
            lines[i] = new_line
            break
    general_settings_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# 1_Vehicle.h - výběr aktivního vozidla
# ---------------------------------------------------------------------------

_category_header_re = re.compile(r"^//\s*(.+?)\s*-{2,}\s*$")
_vehicle_include_re = re.compile(
    r'^(\s*)(//\s*)?(#include\s+"vehicles/([^"]+\.h)")\s*(?://\s*(.*))?$'
)


@dataclass
class VehicleEntry:
    line_index: int
    filename: str
    description: str
    category: str
    active: bool


def parse_vehicle_list(vehicle_h_path: Path) -> list[VehicleEntry]:
    lines = vehicle_h_path.read_text(encoding="utf-8").splitlines()
    entries: list[VehicleEntry] = []
    current_category = ""
    for i, line in enumerate(lines):
        header_match = _category_header_re.match(line)
        if header_match and "#include" not in line:
            current_category = header_match.group(1)
            continue
        m = _vehicle_include_re.match(line)
        if m:
            _indent, comment_prefix, _include_part, filename, description = m.groups()
            entries.append(
                VehicleEntry(
                    line_index=i,
                    filename=filename,
                    description=(description or "").strip(),
                    category=current_category,
                    active=comment_prefix is None,
                )
            )
    return entries


def get_active_vehicle(vehicle_h_path: Path) -> Optional[VehicleEntry]:
    for entry in parse_vehicle_list(vehicle_h_path):
        if entry.active:
            return entry
    return None


def set_active_vehicle(vehicle_h_path: Path, filename: str) -> None:
    """Zakomentuje všechny #include vehicles/*.h řádky a odkomentuje jen ten vybraný."""
    lines = vehicle_h_path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = _vehicle_include_re.match(line)
        if not m:
            continue
        indent, comment_prefix, include_part, this_filename, description = m.groups()
        comment_suffix = f" // {description}" if description else ""
        if this_filename == filename:
            lines[i] = f"{indent}{include_part}{comment_suffix}"
        else:
            # Zajistíme přesně jedno "// " na začátku, i když už tam nějaký
            # komentářový prefix byl.
            lines[i] = f"{indent}// {include_part}{comment_suffix}"
    vehicle_h_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# vehicles/<Vehicle>.h - parametry konkrétního vozidla
# ---------------------------------------------------------------------------

_number_param_re = re.compile(
    r"^(\s*)(volatile\s+)?(const\s+)?"
    r"(uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t|int|float|boolean|bool)\s+"
    r"(\w+)\s*=\s*([^;]+?)\s*;\s*(?://\s*(.*))?$"
)

# Víceřádkové deklarace typu "uint16_t CH1L = 1000, CH1C = 1500, CH1R = 2000;"
# (používá 7_Servos.h pro servo koncové body) - jedna fyzická řádka, víc
# samostatných hodnot. Detekujeme podle čárky v hodnotové části.
_multi_number_re = re.compile(
    r"^(\s*)(volatile\s+)?(const\s+)?"
    r"(uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t|int|float|boolean|bool)\s+"
    r"((?:\w+\s*=\s*[^,;]+,\s*)+\w+\s*=\s*[^,;]+)\s*;\s*(?://\s*(.*))?$"
)
_multi_segment_re = re.compile(r"(\w+)\s*=\s*(.+)")

# Pole, např. "const uint8_t masterVolumePercentage[] = {100, 66, 44, 0};"
# nebo "uint8_t defaultBroadcastAddress1[] = {0xFE, 0x49, 0x01, 0x00, 0x00, 0x01};"
_array_re = re.compile(
    r"^(\s*)(volatile\s+)?(const\s+)?"
    r"(uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t|int|float|boolean|bool)\s+"
    r"(\w+)\s*\[\s*\d*\s*\]\s*=\s*\{([^}]*)\}\s*;\s*(?://\s*(.*))?$"
)

# Víceřádkové pole, např.:
#   boolean channelAutoZero[17] = {
#       false, // CH0 (unused)
#       true,  // CH1
#       ...
#   };
_array_multiline_start_re = re.compile(
    r"^(\s*)(volatile\s+)?(const\s+)?"
    r"(uint8_t|uint16_t|uint32_t|int8_t|int16_t|int32_t|int|float|boolean|bool)\s+"
    r"(\w+)\s*\[\s*\d*\s*\]\s*=\s*\{\s*$"
)
_array_multiline_element_re = re.compile(r"^(\s*)([^,]+?)(,)?\s*(?://\s*(.*))?$")
_array_multiline_end_re = re.compile(r"^\s*\}\s*;\s*$")

# Textové hodnoty typu "String default_ssid = \"My_Truck\";"
_string_var_re = re.compile(
    r'^(\s*)(const\s+)?String\s+(\w+)\s*=\s*"([^"]*)"\s*;\s*(?://\s*(.*))?$'
)

_define_string_re = re.compile(
    r'^(\s*)(//\s*)?(#define\s+(\w+)\s+)"([^"]*)"\s*(?://\s*(.*))?$'
)

_define_value_re = re.compile(
    r"^(\s*)(//\s*)?(#define\s+(\w+)\s+)(\S+)\s*(?://\s*(.*))?$"
)

_define_flag_re = re.compile(
    r"^(\s*)(//\s*)?(#define\s+(\w+))\s*(?://\s*(.*))?$"
)

_sound_include_re = re.compile(
    r'^(\s*)(//\s*)?(#include\s+"(?:vehicles/)?sounds/([^"]+\.h)")\s*(?://\s*(.*))?$'
)


@dataclass
class ArrayParam:
    kind = "array"
    line_index: int
    category: str
    name: str
    items_raw: str  # obsah mezi { } tak, jak je v souboru (např. "100, 66, 44, 0")
    comment: str


@dataclass
class StringParam:
    kind = "string"
    line_index: int
    category: str
    name: str
    value: str
    comment: str


@dataclass
class NumberParam:
    kind = "number"
    line_index: int
    category: str
    name: str
    value: str
    comment: str
    is_multi: bool = False  # True, pokud je na řádku více deklarací najednou (např. "CH1L = 1000, CH1C = 1500, CH1R = 2000;")
    is_array_element: bool = False  # True, pokud je to jeden prvek viceradkoveho pole (napr. "true, // CH1")


@dataclass
class FlagParam:
    kind = "flag"
    line_index: int
    category: str
    name: str
    active: bool
    comment: str


@dataclass
class SoundOption:
    line_index: int
    filename: str
    description: str
    active: bool


@dataclass
class SoundChoiceParam:
    kind = "sound_choice"
    category: str
    options: list[SoundOption] = field(default_factory=list)

    @property
    def active_option(self) -> Optional[SoundOption]:
        for opt in self.options:
            if opt.active:
                return opt
        return None


@dataclass
class FlagOption:
    line_index: Optional[int]  # None u syntetické volby bez vlastního řádku (napr. "PWM" = žádný protokol aktivní)
    name: str
    description: str
    active: bool


@dataclass
class FlagChoiceParam:
    kind = "flag_choice"
    category: str
    options: list[FlagOption] = field(default_factory=list)

    @property
    def active_option(self) -> Optional[FlagOption]:
        for opt in self.options:
            if opt.active:
                return opt
        return None


@dataclass
class VehicleFile:
    path: Path
    lines: list[str]
    vehicle_name: str
    params: list  # list[NumberParam | FlagParam | SoundChoiceParam]

    def save(self) -> None:
        self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")

    def set_number_value(self, param: NumberParam, new_value: str) -> None:
        if param.is_array_element:
            line = self.lines[param.line_index]
            m = _array_multiline_element_re.match(line)
            assert m, f"Line at index {param.line_index} no longer matches expected array element pattern"
            indent, _old_value, comma, comment = m.groups()
            comma_suffix = "," if comma else ""
            comment_suffix = f" // {comment}" if comment else ""
            self.lines[param.line_index] = f"{indent}{new_value}{comma_suffix}{comment_suffix}"
            param.value = new_value
            return

        if param.is_multi:
            line = self.lines[param.line_index]
            m = _multi_number_re.match(line)
            assert m, f"Line at index {param.line_index} no longer matches expected multi-value pattern"
            indent, volatile, const, ctype, body, comment = m.groups()
            segments = [s.strip() for s in body.split(",")]
            new_segments = []
            for seg in segments:
                seg_m = _multi_segment_re.match(seg)
                seg_name, seg_value = seg_m.groups()
                if seg_name == param.name:
                    new_segments.append(f"{seg_name} = {new_value}")
                else:
                    new_segments.append(f"{seg_name} = {seg_value}")
            comment_suffix = f" // {comment}" if comment else ""
            prefix = f"{indent}{volatile or ''}{const or ''}{ctype} "
            self.lines[param.line_index] = f"{prefix}{', '.join(new_segments)};{comment_suffix}"
            param.value = new_value
            return

        line = self.lines[param.line_index]
        m = _number_param_re.match(line)
        assert m, f"Line at index {param.line_index} no longer matches expected pattern"
        indent, volatile, const, ctype, name, _old_value, comment = m.groups()
        comment_suffix = f" // {comment}" if comment else ""
        prefix = f"{indent}{volatile or ''}{const or ''}{ctype} {name} = "
        self.lines[param.line_index] = f"{prefix}{new_value};{comment_suffix}"
        param.value = new_value

    def set_flag_active(self, param: FlagParam, active: bool) -> None:
        line = self.lines[param.line_index]
        m = _define_flag_re.match(line)
        assert m, f"Line at index {param.line_index} no longer matches expected pattern"
        indent, _comment_prefix, define_part, _name, comment = m.groups()
        comment_suffix = f" // {comment}" if comment else ""
        prefix = "" if active else "// "
        self.lines[param.line_index] = f"{indent}{prefix}{define_part}{comment_suffix}"
        param.active = active

    def set_sound_choice(self, param: SoundChoiceParam, chosen_filename: str) -> None:
        for opt in param.options:
            m = _sound_include_re.match(self.lines[opt.line_index])
            assert m, f"Line at index {opt.line_index} no longer matches expected pattern"
            indent, _comment_prefix, include_part, _filename, description = m.groups()
            comment_suffix = f" // {description}" if description else ""
            is_chosen = opt.filename == chosen_filename
            prefix = "" if is_chosen else "// "
            self.lines[opt.line_index] = f"{indent}{prefix}{include_part}{comment_suffix}"
            opt.active = is_chosen

    def set_flag_choice(self, param: FlagChoiceParam, chosen_name: str) -> None:
        for opt in param.options:
            is_chosen = opt.name == chosen_name
            if opt.line_index is not None and opt.active != is_chosen:
                line = self.lines[opt.line_index]
                m = _define_flag_re.match(line)
                assert m, f"Line at index {opt.line_index} no longer matches expected pattern"
                indent, _comment_prefix, define_part, _name, comment = m.groups()
                comment_suffix = f" // {comment}" if comment else ""
                prefix = "" if is_chosen else "// "
                self.lines[opt.line_index] = f"{indent}{prefix}{define_part}{comment_suffix}"
            opt.active = is_chosen

    def set_array_value(self, param: ArrayParam, new_items_raw: str) -> None:
        line = self.lines[param.line_index]
        m = _array_re.match(line)
        assert m, f"Line at index {param.line_index} no longer matches expected array pattern"
        indent, volatile, const, ctype, name, _old_items, comment = m.groups()
        comment_suffix = f" // {comment}" if comment else ""
        prefix = f"{indent}{volatile or ''}{const or ''}{ctype} {name}[] = "
        self.lines[param.line_index] = f"{prefix}{{{new_items_raw}}};{comment_suffix}"
        param.items_raw = new_items_raw

    def set_string_value(self, param: StringParam, new_value: str) -> None:
        line = self.lines[param.line_index]
        m = _string_var_re.match(line)
        assert m, f"Line at index {param.line_index} no longer matches expected String pattern"
        indent, const, name, _old_value, comment = m.groups()
        comment_suffix = f" // {comment}" if comment else ""
        prefix = f"{indent}{const or ''}String {name} = "
        self.lines[param.line_index] = f'{prefix}"{new_value}";{comment_suffix}'
        param.value = new_value


def _compute_block_comment_mask(lines: list[str]) -> list[bool]:
    """
    Vrátí seznam bool hodnot (jedna na řádek) - True, pokud je daný řádek
    uvnitř C-stylového blokového komentáře (/* ... */). Autor originálního
    projektu takhle občas "dočasně vypíná" celé kusy kódu (viz např.
    KenworthCummins335.h) - bez téhle detekce by parser omylem považoval
    zakomentovaný draft za živý kód.

    Zjednodušené (ne plnohodnotný C parser), ale pro styl komentářů
    použitý v tomto projektu (/* a */ vždy na vlastním řádku) dostatečné.
    """
    mask = [False] * len(lines)
    in_comment = False
    for i, line in enumerate(lines):
        if in_comment:
            mask[i] = True
            if "*/" in line:
                in_comment = False
            continue
        if "/*" in line:
            mask[i] = True
            close_pos = line.find("*/")
            open_pos = line.find("/*")
            if close_pos == -1 or close_pos < open_pos:
                in_comment = True
            continue
    return mask


def _parse_flat_range(
    lines: list[str],
    comment_mask: list[bool],
    start: int,
    end: int,
    dedupe_scope: str = "global",
    start_category: str = "",
    on_vehicle_name=None,
) -> list:
    """
    Sdílená "plochá" parsovací smyčka (kategorie, přepínače, čísla,
    víceřádkové deklarace, výběr zvuku) použitá jak pro celé jednoduché
    soubory (vozidla, ESC, ...), tak pro konkrétní rozsah řádků uvnitř
    složitějších souborů (např. obsah aktuálního #ifdef bloku v
    7_Servos.h). `on_vehicle_name(value)` se zavolá, pokud se narazí na
    `#define VEHICLE_NAME "..."` (jen vozidla to využívají).
    """
    params: list = []
    seen_names: set[str] = set()
    current_category = start_category
    current_sound_group: Optional[SoundChoiceParam] = None

    def flush_sound_group():
        nonlocal current_sound_group
        if current_sound_group and current_sound_group.options:
            params.append(current_sound_group)
        current_sound_group = None

    for i in range(start, end):
        if comment_mask[i]:
            continue
        line = lines[i]

        multiline_start_match = _array_multiline_start_re.match(line)
        if multiline_start_match:
            flush_sound_group()
            _indent, _volatile, _const, _ctype, array_name = multiline_start_match.groups()
            element_index = 0
            j = i + 1
            while j < end:
                if comment_mask[j]:
                    j += 1
                    continue
                el_line = lines[j]
                if _array_multiline_end_re.match(el_line):
                    break
                el_match = _array_multiline_element_re.match(el_line)
                if el_match:
                    _el_indent, el_value, _el_comma, el_comment = el_match.groups()
                    el_comment = (el_comment or "").strip()
                    # Kanál z komentáře (např. "CH1" z "CH1" nebo "CH0 (unused)"),
                    # jinak jen pořadové číslo prvku.
                    ch_match = re.match(r"(CH\d+)", el_comment)
                    suffix = ch_match.group(1) if ch_match else str(element_index)
                    elem_name = f"{array_name}[{suffix}]"
                    if elem_name not in seen_names:
                        seen_names.add(elem_name)
                        params.append(
                            NumberParam(
                                line_index=j,
                                category=current_category,
                                name=elem_name,
                                value=el_value.strip(),
                                comment=el_comment,
                                is_array_element=True,
                            )
                        )
                element_index += 1
                j += 1
            continue

        header_match = _category_header_re.match(line)
        if header_match and "#include" not in line and "#define" not in line:
            flush_sound_group()
            current_category = header_match.group(1)
            if dedupe_scope == "category":
                seen_names.clear()
            continue

        if on_vehicle_name is not None:
            name_str_match = _define_string_re.match(line)
            if name_str_match:
                _indent, _cp, _prefix, macro_name, value, _comment = name_str_match.groups()
                if macro_name == "VEHICLE_NAME":
                    on_vehicle_name(value)
                    flush_sound_group()
                    continue

        sound_match = _sound_include_re.match(line)
        if sound_match:
            _indent, comment_prefix, _include_part, filename, description = sound_match.groups()
            if current_sound_group is None:
                current_sound_group = SoundChoiceParam(category=current_category)
            current_sound_group.options.append(
                SoundOption(
                    line_index=i,
                    filename=filename,
                    description=(description or "").strip(),
                    active=comment_prefix is None,
                )
            )
            continue

        # Jakákoliv jiná řádka ukončuje sérii voleb zvuku
        array_match = _array_re.match(line)
        if array_match:
            flush_sound_group()
            _indent, _volatile, _const, _ctype, name, items_raw, comment = array_match.groups()
            if name not in seen_names:
                seen_names.add(name)
                params.append(
                    ArrayParam(
                        line_index=i,
                        category=current_category,
                        name=name,
                        items_raw=items_raw.strip(),
                        comment=(comment or "").strip(),
                    )
                )
            continue

        string_match = _string_var_re.match(line)
        if string_match:
            flush_sound_group()
            _indent, _const, name, value, comment = string_match.groups()
            if name not in seen_names:
                seen_names.add(name)
                params.append(
                    StringParam(
                        line_index=i,
                        category=current_category,
                        name=name,
                        value=value,
                        comment=(comment or "").strip(),
                    )
                )
            continue

        multi_match = _multi_number_re.match(line)
        if multi_match:
            flush_sound_group()
            _indent, _volatile, _const, _ctype, body, comment = multi_match.groups()
            for segment in body.split(","):
                seg_m = _multi_segment_re.match(segment.strip())
                if not seg_m:
                    continue
                seg_name, seg_value = seg_m.groups()
                if seg_name in seen_names:
                    continue
                seen_names.add(seg_name)
                params.append(
                    NumberParam(
                        line_index=i,
                        category=current_category,
                        name=seg_name,
                        value=seg_value.strip(),
                        comment=(comment or "").strip(),
                        is_multi=True,
                    )
                )
            continue

        num_match = _number_param_re.match(line)
        if num_match:
            flush_sound_group()
            _indent, _volatile, _const, _ctype, name, value, comment = num_match.groups()
            if name in seen_names:
                continue
            seen_names.add(name)
            params.append(
                NumberParam(
                    line_index=i,
                    category=current_category,
                    name=name,
                    value=value.strip(),
                    comment=(comment or "").strip(),
                )
            )
            continue

        define_value_match = _define_value_re.match(line)
        if define_value_match:
            flush_sound_group()
            _indent, _cp, _prefix, name, value, comment = define_value_match.groups()
            if name in seen_names:
                continue
            seen_names.add(name)
            params.append(
                NumberParam(
                    line_index=i,
                    category=current_category,
                    name=name,
                    value=value.strip(),
                    comment=(comment or "").strip(),
                )
            )
            continue

        flag_match = _define_flag_re.match(line)
        if flag_match:
            flush_sound_group()
            _indent, comment_prefix, _define_part, name, comment = flag_match.groups()
            if name in seen_names:
                continue
            seen_names.add(name)
            params.append(
                FlagParam(
                    line_index=i,
                    category=current_category,
                    name=name,
                    active=comment_prefix is None,
                    comment=(comment or "").strip(),
                )
            )
            continue

    flush_sound_group()
    return params


def parse_vehicle_file(vehicle_file_path: Path, dedupe_scope: str = "global") -> VehicleFile:
    """
    dedupe_scope="global" (výchozí, chování jako dřív) - stejné jméno
    parametru se v celém souboru bere jen jednou (řeší drobné duplicity
    v originále, viz "R6" v některých vozidlech).

    dedupe_scope="category" - jméno se smí opakovat v různých kategoriích
    (reset při každé změně kategorie). Nutné pro soubory, kde se stejné
    jméno záměrně opakuje v každém profilu (např. "CH1L" v každém z 16
    profilů v 7_Servos.h) - jinak by šly vidět jen hodnoty prvního profilu.
    """
    lines = vehicle_file_path.read_text(encoding="utf-8").splitlines()
    comment_mask = _compute_block_comment_mask(lines)
    vehicle_name_holder = {"name": vehicle_file_path.stem}

    def on_vehicle_name(value: str) -> None:
        vehicle_name_holder["name"] = value

    params = _parse_flat_range(
        lines, comment_mask, 0, len(lines),
        dedupe_scope=dedupe_scope, on_vehicle_name=on_vehicle_name,
    )

    return VehicleFile(
        path=vehicle_file_path,
        lines=lines,
        vehicle_name=vehicle_name_holder["name"],
        params=params,
    )


# ---------------------------------------------------------------------------
# 2_Remote.h - výběr profilu vysílačky a komunikačního protokolu
# ---------------------------------------------------------------------------
#
# Tenhle soubor má jinou strukturu než vozidla nebo ostatní jednoduché
# nastavovací soubory: hned na začátku je "vyber přesně jeden profil
# vysílačky" (stejný princip jako výběr vozidla, ale přes #define, ne
# #include) a "vyber přesně jeden komunikační protokol" (PWM/SBUS/IBUS/
# SUMD/PPM - PWM je speciální "žádný z ostatních není aktivní" volba).
#
# Za tím následují desítky bloků #ifdef <PROFIL> ... #endif, každý s
# vlastní kalibrací kanálů (včetně polí, která zatím neumíme editovat) -
# ty se v týhle první verzi NEparsují, jen se zachovají beze změny.

_PROFILE_NAMES = [
    "FLYSKY_FS_I6X",
    "FLYSKY_FS_I6S",
    "FLYSKY_FS_I6S_LOADER",
    "FLYSKY_FS_I6S_DOZER",
    "WB_EXCAVATOR",
    "FLYSKY_FS_I6S_EXCAVATOR",
    "FRSKY_TANDEM_EXCAVATOR",
    "FRSKY_TANDEM_HARMONY_LOADER",
    "FRSKY_TANDEM_CRANE",
    "FLYSKY_GT5",
    "RGT_EX86100",
    "GRAUPNER_MZ_12",
    "MICRO_RC",
    "MICRO_RC_STICK",
    "FLYSKY_FS_I6S_EXCAVATOR_TEST",
]

_PROTOCOL_NAMES = [
    "SBUS_COMMUNICATION",
    "IBUS_COMMUNICATION",
    "SUMD_COMMUNICATION",
    "PPM_COMMUNICATION",
]

_PROFILE_CATEGORY = "Profil vysílačky"
_PROTOCOL_CATEGORY = "Komunikační protokol"
_OTHER_CATEGORY = "Ostatní nastavení dálkového ovládání"


def _strip_arrow_comment(comment: str) -> str:
    """Odstraní úvodní '<-------' z komentářů typu '// <------- Flysky FS-i6x'."""
    return comment.lstrip("<- ").strip()


def parse_remote_file(remote_file_path: Path) -> VehicleFile:
    all_lines = remote_file_path.read_text(encoding="utf-8").splitlines()
    comment_mask = _compute_block_comment_mask(all_lines)

    first_ifdef = len(all_lines)
    for i, line in enumerate(all_lines):
        if line.strip().startswith("#ifdef"):
            first_ifdef = i
            break

    profile_options: list[FlagOption] = []
    protocol_options: list[FlagOption] = []
    header_params: list = []
    seen_names: set[str] = set()

    for i in range(first_ifdef):
        if comment_mask[i]:
            continue
        line = all_lines[i]

        flag_match = _define_flag_re.match(line)
        if flag_match:
            _indent, comment_prefix, _define_part, name, comment = flag_match.groups()
            active = comment_prefix is None
            description = _strip_arrow_comment(comment or "")
            if name in _PROFILE_NAMES:
                profile_options.append(
                    FlagOption(line_index=i, name=name, description=description, active=active)
                )
            elif name in _PROTOCOL_NAMES:
                protocol_options.append(
                    FlagOption(line_index=i, name=name, description=description, active=active)
                )
            elif name not in seen_names:
                seen_names.add(name)
                header_params.append(
                    FlagParam(
                        line_index=i,
                        category=_OTHER_CATEGORY,
                        name=name,
                        active=active,
                        comment=description,
                    )
                )
            continue

        num_match = _number_param_re.match(line)
        if num_match:
            _indent, _volatile, _const, _ctype, name, value, comment = num_match.groups()
            if name not in seen_names:
                seen_names.add(name)
                header_params.append(
                    NumberParam(
                        line_index=i,
                        category=_OTHER_CATEGORY,
                        name=name,
                        value=value.strip(),
                        comment=(comment or "").strip(),
                    )
                )
            continue

    # PWM je "virtuální" volba bez vlastního řádku - aktivní, pokud žádný
    # ze 4 skutečných protokolů (SBUS/IBUS/SUMD/PPM) není zapnutý.
    any_protocol_active = any(opt.active for opt in protocol_options)
    protocol_options.insert(
        0,
        FlagOption(
            line_index=None,
            name="PWM",
            description="Klasický PWM signál (žádný z ostatních protokolů níže není aktivní)",
            active=not any_protocol_active,
        ),
    )

    params: list = []
    if profile_options:
        params.append(FlagChoiceParam(category=_PROFILE_CATEGORY, options=profile_options))
    if protocol_options:
        params.append(FlagChoiceParam(category=_PROTOCOL_CATEGORY, options=protocol_options))
    params.extend(header_params)

    # Zbytek souboru (kalibrace uvnitř jednotlivých profilů vysílačky) -
    # kategorie se odvodí ze stejných "// Nadpis ----" komentářů jako
    # jinde, se scope=category (stejné jméno se smí opakovat v každém
    # profilu, např. "STEERING" kanál). Pole (channelReversed[] apod.)
    # se stále needitují (parser je bezpečně přeskočí).
    start_category = ""
    for j in range(first_ifdef - 1, -1, -1):
        if comment_mask[j]:
            continue
        m = _category_header_re.match(all_lines[j])
        if m:
            start_category = m.group(1)
            break
        if all_lines[j].strip():
            break

    body_params = _parse_flat_range(
        all_lines, comment_mask, first_ifdef, len(all_lines),
        dedupe_scope="category", start_category=start_category,
    )
    owner_map = _compute_ifdef_profile_owner(all_lines)
    _tag_profile_owners(body_params, owner_map)
    params.extend(body_params)

    return VehicleFile(
        path=remote_file_path,
        lines=all_lines,
        vehicle_name=remote_file_path.stem,
        params=params,
    )


# ---------------------------------------------------------------------------
# 7_Servos.h a 5_Shaker.h - obecný "vyber profil + zbytek souboru" vzor
# ---------------------------------------------------------------------------

def _compute_ifdef_profile_owner(lines: list[str]) -> list[Optional[str]]:
    """
    Pro každý řádek zjistí, uvnitř kterého profilového #ifdef bloku se
    nachází (bere JAKÝKOLIV #ifdef/#ifndef/#if, který není vnořený uvnitř
    jiného - tzn. je na "nulté úrovni" dané sekce) - None, pokud není
    uvnitř žádného (obecné, vždy viditelné nastavení). Vnořené #ifdef
    uvnitř profilu (např. kontrolní #if pro jednu konkrétní volbu) dědí
    vlastníka obklopujícího profilu, takže se nepletou.
    """
    owner: list[Optional[str]] = [None] * len(lines)
    stack: list[Optional[str]] = []
    ifdef_re = re.compile(r"^\s*#(?:ifdef|ifndef|if)\b\s*(\w+)?")
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = ifdef_re.match(stripped)
        if m:
            if not stack:
                stack.append(m.group(1))  # nova "nulta uroven" - novy profil
            else:
                stack.append(stack[-1])  # vnorene - zdedi aktualniho vlastnika
            owner[i] = stack[-1]
            continue
        if stripped.startswith("#endif"):
            owner[i] = stack[-1] if stack else None
            if stack:
                stack.pop()
            continue
        owner[i] = stack[-1] if stack else None
    return owner


def _tag_profile_owners(params: list, owner_map: list[Optional[str]]) -> None:
    """Doplní ke každému parametru dynamický atribut .profile_owner (podle jeho line_index)."""
    for p in params:
        line_idx = getattr(p, "line_index", None)
        if line_idx is None and hasattr(p, "options") and p.options:
            # SoundChoiceParam/FlagChoiceParam nemá vlastní line_index - vezmeme první možnost
            first_opt = p.options[0]
            line_idx = getattr(first_opt, "line_index", None)
        p.profile_owner = owner_map[line_idx] if line_idx is not None else None


def parse_profiled_file(
    file_path: Path,
    profile_names: list[str],
    profile_category: str,
) -> VehicleFile:
    """
    Obecný parser pro soubory se strukturou "vyber přesně jeden profil ze
    seznamu (#define), pak následují #ifdef <PROFIL> ... #endif bloky s
    vlastním nastavením". Používá se pro 7_Servos.h a 5_Shaker.h.

    Na rozdíl od 2_Remote.h (kde jsou per-profilové bloky hlavně pole,
    která needitujeme) mají tyhle dva soubory uvnitř profilů běžné
    hodnoty (čísla, přepínače) - ty se PARSUJÍ VŠECHNY (ne jen aktivní
    profil), aby šlo upravit/porovnat libovolný profil stejně jako ve
    VSCode. Kategorie (a tím i skupina v GUI) se odvodí z komentářových
    nadpisů před každým "#ifdef" blokem - ty už v originále obsahují
    název profilu.
    """
    all_lines = file_path.read_text(encoding="utf-8").splitlines()
    comment_mask = _compute_block_comment_mask(all_lines)

    first_ifdef = len(all_lines)
    for i, line in enumerate(all_lines):
        if line.strip().startswith("#ifdef") or line.strip().startswith("#if "):
            first_ifdef = i
            break

    profile_options: list[FlagOption] = []
    for i in range(first_ifdef):
        if comment_mask[i]:
            continue
        flag_match = _define_flag_re.match(all_lines[i])
        if not flag_match:
            continue
        _indent, comment_prefix, _define_part, name, comment = flag_match.groups()
        if name in profile_names:
            profile_options.append(
                FlagOption(
                    line_index=i,
                    name=name,
                    description=_strip_arrow_comment(comment or ""),
                    active=comment_prefix is None,
                )
            )

    params: list = []
    if profile_options:
        params.append(FlagChoiceParam(category=profile_category, options=profile_options))

    # Nadpis prvního profilu bývá řádek těsně PŘED prvním '#ifdef' (mimo
    # rozsah, který níže parsujeme) - dohledáme ho zpětně, ať první profil
    # nezůstane bez názvu kategorie.
    start_category = ""
    for j in range(first_ifdef - 1, -1, -1):
        if comment_mask[j]:
            continue
        m = _category_header_re.match(all_lines[j])
        if m:
            start_category = m.group(1)
            break
        if all_lines[j].strip():
            break  # narazili jsme na jiný obsah, žádný nadpis tam není

    body_params = _parse_flat_range(
        all_lines, comment_mask, first_ifdef, len(all_lines),
        dedupe_scope="category", start_category=start_category,
    )
    owner_map = _compute_ifdef_profile_owner(all_lines)
    _tag_profile_owners(body_params, owner_map)
    params.extend(body_params)

    return VehicleFile(
        path=file_path,
        lines=all_lines,
        vehicle_name=file_path.stem,
        params=params,
    )


_SERVO_PROFILE_NAMES = [
    "SERVOS_DEFAULT",
    "SERVOS_LANDY_MN_MODEL",
    "SERVOS_LANDY_DOUBLE_EAGLE",
    "SERVOS_C34",
    "SERVOS_URAL",
    "SERVOS_RGT_EX86100",
    "SERVOS_ACTROS",
    "SERVOS_KING_HAULER",
    "SERVOS_RACING_TRUCK",
    "SERVOS_MECCANO_DUMPER",
    "SERVOS_OPEN_RC_TRACTOR",
    "SERVOS_EXCAVATOR",
    "SERVOS_EXCAVATOR_1060_ESC",
    "SERVOS_HYDRAULIC_EXCAVATOR",
    "SERVOS_WB_EXCAVATOR",
    "SERVOS_CRANE",
]

_SHAKER_PROFILE_NAMES = [
    "GT_POWER_STOCK",
    "GT_POWER_PLASTIC",
]


def parse_servos_file(servos_file_path: Path) -> VehicleFile:
    return parse_profiled_file(servos_file_path, _SERVO_PROFILE_NAMES, "Profil serv")


def parse_shaker_file(shaker_file_path: Path) -> VehicleFile:
    return parse_profiled_file(shaker_file_path, _SHAKER_PROFILE_NAMES, "Profil shakeru")
