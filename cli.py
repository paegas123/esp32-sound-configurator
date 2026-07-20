"""Hlavní interaktivní běh TankSound Configurátoru (fáze 1: terminálová verze)."""

import shutil
import sys
from pathlib import Path

import pio_runner
import platformio_ini
import settings
import updater
import vehicle_parser as vp
from i18n import Translator
from paths import VENDOR_SNAPSHOT_DIR, WORKING_PROJECT_DIR, ensure_directories
from param_translations import translate_category, translate_param_explanation

LANGUAGE_MENU = [
    ("cs", "Čeština"),
    ("en", "English"),
    ("de", "Deutsch"),
]


def ask_yes_no(tr: Translator, prompt_key: str, **kwargs) -> bool:
    prompt = tr.t(prompt_key, **kwargs)
    yes_char = tr.t("yes_char")
    answer = input(prompt).strip().lower()
    return answer.startswith(yes_char)


def choose_language() -> Translator:
    lang = settings.get_language()
    if lang:
        return Translator(lang)

    print("=" * 60)
    print("Vyber jazyk programu / Choose language / Sprache wählen")
    print("=" * 60)
    for i, (_code, label) in enumerate(LANGUAGE_MENU, start=1):
        print(f"  [{i}] {label}")
    while True:
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(LANGUAGE_MENU):
            code = LANGUAGE_MENU[int(raw) - 1][0]
            settings.set_language(code)
            return Translator(code)
        print("? / ? / ?")


def run_update_check(tr: Translator) -> None:
    print(tr.t("checking_internet"))
    remote_info = updater.check_internet_and_get_latest_commit()

    if remote_info is None:
        if updater.has_local_copy():
            print(tr.t("no_internet_using_local"))
            return
        print(tr.t("no_internet_no_local"))
        sys.exit(1)

    if not updater.has_local_copy():
        print(tr.t("no_local_copy_downloading"))
        updater.download_and_replace_snapshot(remote_info)
        print(tr.t("first_download_done"))
        return

    if updater.is_up_to_date(remote_info):
        print(tr.t("up_to_date"))
        return

    local = updater.load_local_version() or {}
    print(
        tr.t(
            "update_available",
            date=remote_info.date,
            local_date=local.get("date", "?"),
        )
    )
    if ask_yes_no(tr, "update_prompt"):
        print(tr.t("update_downloading"))
        updater.download_and_replace_snapshot(remote_info)
        print(tr.t("update_done"))
    else:
        print(tr.t("update_skipped"))


def prepare_working_copy(tr: Translator) -> None:
    print(tr.t("preparing_working_copy"))
    if WORKING_PROJECT_DIR.exists():
        shutil.rmtree(WORKING_PROJECT_DIR)
    shutil.copytree(VENDOR_SNAPSHOT_DIR, WORKING_PROJECT_DIR)

    platformio_ini_path = WORKING_PROJECT_DIR / "platformio.ini"
    if platformio_ini_path.exists():
        platformio_ini.pin_compatible_platform_version(platformio_ini_path)


def select_board(tr: Translator, general_settings_path: Path) -> None:
    print(tr.t("board_selection_title"))
    enabled = ask_yes_no(tr, "board_selection_question")
    vp.set_board_flag(general_settings_path, enabled)


def select_vehicle(tr: Translator, vehicle_h_path: Path) -> vp.VehicleEntry:
    entries = vp.parse_vehicle_list(vehicle_h_path)
    print(tr.t("vehicle_selection_title"))

    current_category = None
    for idx, entry in enumerate(entries, start=1):
        if entry.category != current_category:
            current_category = entry.category
            print(f"\n-- {current_category} --")
        marker = " *" if entry.active else ""
        print(f"  [{idx}] {entry.filename[:-2]}{marker}  ({entry.description[:70]})")

    while True:
        raw = input("\n" + tr.t("vehicle_selection_prompt")).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(entries):
            chosen = entries[int(raw) - 1]
            vp.set_active_vehicle(vehicle_h_path, chosen.filename)
            return chosen
        print(tr.t("invalid_choice"))


def format_param_value(param, tr: Translator) -> str:
    if param.kind == "flag":
        return tr.t("flag_on") if param.active else tr.t("flag_off")
    if param.kind == "number":
        return param.value
    if param.kind == "sound_choice":
        active = param.active_option
        return active.filename[:-2] if active else "?"
    return "?"


def edit_vehicle_params(tr: Translator, vf: vp.VehicleFile) -> None:
    while True:
        print(f"\n### {vf.vehicle_name} ###")
        current_category = None
        for idx, param in enumerate(vf.params, start=1):
            translated_category = translate_category(param.category, tr.lang)
            if translated_category != current_category:
                current_category = translated_category
                print(tr.t("category_header", category=current_category))

            if param.kind == "sound_choice":
                label = tr.t("param_type_sound_choice")
                explanation = ", ".join(o.filename[:-2] for o in param.options)
            else:
                label = param.name
                explanation = translate_param_explanation(
                    param.name, getattr(param, "comment", ""), tr.lang
                )
            value = format_param_value(param, tr)
            print(tr.t("param_line", idx=idx, label=label, value=value, explanation=explanation))

        raw = input(tr.t("param_edit_prompt")).strip()
        if raw == "0":
            break
        if not raw.isdigit() or not (1 <= int(raw) <= len(vf.params)):
            print(tr.t("invalid_choice"))
            continue

        param = vf.params[int(raw) - 1]

        if param.kind == "number":
            new_value = input(
                tr.t("param_new_value_prompt", label=param.name, value=param.value)
            ).strip()
            if new_value:
                vf.set_number_value(param, new_value)
                print(tr.t("param_updated", label=param.name, value=new_value))

        elif param.kind == "flag":
            current_label = tr.t("flag_on") if param.active else tr.t("flag_off")
            if ask_yes_no(tr, "param_toggle_prompt", label=param.name, value=current_label):
                vf.set_flag_active(param, not param.active)
                new_label = tr.t("flag_on") if param.active else tr.t("flag_off")
                print(tr.t("param_updated", label=param.name, value=new_label))

        elif param.kind == "sound_choice":
            for i, opt in enumerate(param.options, start=1):
                marker = " *" if opt.active else ""
                print(f"  [{i}] {opt.filename[:-2]}{marker}  ({opt.description[:60]})")
            raw_opt = input(
                tr.t("sound_choice_prompt", label=tr.t("param_type_sound_choice"))
            ).strip()
            if raw_opt.isdigit() and 1 <= int(raw_opt) <= len(param.options):
                chosen_opt = param.options[int(raw_opt) - 1]
                vf.set_sound_choice(param, chosen_opt.filename)
                print(tr.t("param_updated", label="sound", value=chosen_opt.filename))

    print(tr.t("writing_changes"))
    vf.save()
    print(tr.t("changes_written"))


def maybe_upload(tr: Translator) -> None:
    if not ask_yes_no(tr, "upload_prompt"):
        print(tr.t("upload_skipped", path=str(WORKING_PROJECT_DIR)))
        return

    print(tr.t("upload_running"))
    pio_runner.ensure_known_dependencies()
    result = pio_runner.run_pio_with_auto_dependency_fix(
        ["run", "--target", "upload"], cwd=str(WORKING_PROJECT_DIR)
    )
    print(result.stdout)
    if result.returncode == 0:
        print(tr.t("upload_success"))
    else:
        print(tr.t("upload_failed"))
        print(result.stderr)


def main() -> None:
    ensure_directories()
    tr = choose_language()
    print(f"\n{tr.t('welcome')}\n")

    run_update_check(tr)
    prepare_working_copy(tr)

    src_dir = WORKING_PROJECT_DIR / "src"
    general_settings_path = src_dir / "0_generalSettings.h"
    vehicle_h_path = src_dir / "1_Vehicle.h"

    if not general_settings_path.exists():
        print(tr.t("board_master_settings_missing"))
        sys.exit(1)
    if not vehicle_h_path.exists():
        print(tr.t("vehicle_file_missing"))
        sys.exit(1)

    select_board(tr, general_settings_path)
    chosen_entry = select_vehicle(tr, vehicle_h_path)

    vehicle_file_path = src_dir / "vehicles" / chosen_entry.filename
    vf = vp.parse_vehicle_file(vehicle_file_path)
    edit_vehicle_params(tr, vf)

    maybe_upload(tr)
    print(f"\n{tr.t('goodbye')}")


if __name__ == "__main__":
    main()
