# -*- mode: python ; coding: utf-8 -*-
#
# Konfigurace pro PyInstaller - sestaví ze zdrojového kódu samostatnou
# spustitelnou aplikaci (na Macu .app, na Windows .exe), kterou už jde
# jen dvojklikem spustit, bez Terminálu a bez nutnosti mít nainstalovaný
# Python. Nespouští se ručně - stará se o to GitHub Actions (viz
# .github/workflows/build.yml), ale dá se použít i ručně na počítači,
# kde je PyInstaller nainstalovaný:
#
#   pip install pyinstaller --break-system-packages
#   pyinstaller esp32_sound_configurator.spec
#
# Výsledek najdeš ve složce dist/.
#
# Poznámka: na macOS se použije "onedir" mód (PyInstaller to sám
# doporučuje pro .app bundly - "onefile" na Macu dělá problémy s
# bezpečnostními kontrolami systému). Na Windows zůstává jeden .exe.

import os
import sys

is_mac = sys.platform == "darwin"

# Ikony jsou volitelné - pokud zrovna nejsou vygenerované (např. lokální
# test na Linuxu), sestavení proběhne dál, jen bez vlastní ikonky.
mac_icon = "icon.icns" if os.path.exists("icon.icns") else None
win_icon = "icon.ico" if os.path.exists("icon.ico") else None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('web', 'web'),
        ('lang', 'lang'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

if is_mac:
    # onedir - PyInstaller pak z toho sám poskládá .app složku (BUNDLE níže)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='ESP32 Sound Configurator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=mac_icon,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='ESP32 Sound Configurator',
    )
    app = BUNDLE(
        coll,
        name='ESP32 Sound Configurator.app',
        icon=mac_icon,
        bundle_identifier='cz.tomaspavlas.esp32soundconfigurator',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
        },
    )
else:
    # Windows (a Linux) - jeden spustitelny soubor
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='ESP32 Sound Configurator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=win_icon,
    )
