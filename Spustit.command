#!/bin/bash
# Dvojklikem na tenhle soubor se spustí TankSound Configurator - žádné
# ruční psaní příkazů do Terminálu není potřeba. Terminálové okno se na
# chvíli otevře samo (ukazuje, co se právě děje), a jakmile se spustí
# server, otevře se ti sám prohlížeč.

cd "$(dirname "$0")"
python3 gui.py
