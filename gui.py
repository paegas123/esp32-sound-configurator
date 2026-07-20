"""
Spouštěč grafické (webové) verze ESP32 Sound Configurátoru.

Spustí lokální webserver a automaticky otevře výchozí prohlížeč na
správné adrese - stejný postup funguje na Windows i na Macu.

Použití:
    python3 gui.py

Pokud je tenhle soubor zabalený přes PyInstaller do samostatné appky
(.app / .exe) BEZ viditelného okna Terminálu, běžná chyba by jinak byla
neviditelná - appka by se jen tiše "nespustila" a nikdo by nevěděl proč.
Proto se každá neočekávaná chyba při startu zapíše do souboru
(~/ESP32_Sound_Configurator/crash_log.txt) a na Macu se navíc rovnou
zobrazí i chybové okno.
"""

import sys
import traceback


def _write_crash_log(exc: BaseException):
    from paths import APP_DIR

    APP_DIR.mkdir(parents=True, exist_ok=True)
    log_path = APP_DIR / "crash_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=f)
    return log_path


def _show_mac_error_dialog(message: str) -> None:
    if sys.platform != "darwin":
        return
    try:
        import subprocess

        safe_message = message.replace('"', "'")
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display dialog "{safe_message}" with title "ESP32 Sound Configurator" '
                f'buttons {{"OK"}} default button "OK" with icon caution',
            ],
            timeout=10,
        )
    except Exception:
        pass  # Chybové okno je jen "bonus" - hlavní je zapsaný log soubor.


if __name__ == "__main__":
    try:
        from web_server import run_server

        run_server()
    except Exception as exc:
        try:
            log_path = _write_crash_log(exc)
            _show_mac_error_dialog(
                f"Nastala chyba při spouštění.\n\nPodrobnosti jsou uložené v souboru:\n{log_path}\n\n"
                f"Pošli tenhle soubor Claudovi, ať to spraví."
            )
        except Exception:
            pass
        raise
