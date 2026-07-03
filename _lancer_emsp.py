# -*- coding: utf-8 -*-
"""Lanceur EMSP : ajoute programme/ au chemin de recherche Python, fixe
l'emplacement des donnees (couche donnees/ separee, V1.53), ouvre le navigateur
UNE FOIS le serveur pret (evite ERR_CONNECTION_REFUSED au demarrage), puis lance
l'application."""
import os, sys, runpy, threading, socket, time, webbrowser
BASE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(BASE, "programme")
os.environ.setdefault("EMSP_DONNEES", os.path.join(BASE, "donnees"))
sys.path.insert(0, PROG)      # pour 'import config', 'import metier', etc.
os.chdir(PROG)                # chemins relatifs eventuels

HOTE = os.environ.get("EMSP_HOST", "127.0.0.1")
CIBLE = "127.0.0.1" if HOTE in ("127.0.0.1", "0.0.0.0") else HOTE
PORT = 5000

def _ouvrir_navigateur_quand_pret():
    # Attend que le serveur reponde sur le port avant d'ouvrir le navigateur.
    for _ in range(120):                      # ~60 s au maximum
        try:
            with socket.create_connection((CIBLE, PORT), timeout=0.5):
                break
        except OSError:
            time.sleep(0.5)
    webbrowser.open("http://%s:%d" % (CIBLE, PORT))

threading.Thread(target=_ouvrir_navigateur_quand_pret, daemon=True).start()
runpy.run_path(os.path.join(PROG, "app.py"), run_name="__main__")
