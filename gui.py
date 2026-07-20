"""
Spouštěč grafické (webové) verze TankSound Configurátoru.

Spustí lokální webserver a automaticky otevře výchozí prohlížeč na
správné adrese - stejný postup funguje na Windows i na Macu.

Použití:
    python3 gui.py
"""

from web_server import run_server

if __name__ == "__main__":
    run_server()
