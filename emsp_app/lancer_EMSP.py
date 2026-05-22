"""
Lanceur de l'application EMSP – Gestion Formation
Double-cliquez sur ce fichier, ou exécutez : python lancer_application.py
"""
import subprocess, sys, os, webbrowser, time

PORT = 5000
script = os.path.join(os.path.dirname(__file__), "app.py")

print("=" * 60)
print("  EMSP – Gestion Formation  |  Démarrage du serveur local")
print("=" * 60)
print(f"\n  ➡  Ouverture dans le navigateur : http://127.0.0.1:{PORT}")
print("  ⛔  Pour arrêter : fermez cette fenêtre (Ctrl+C)\n")

proc = subprocess.Popen([sys.executable, script])
time.sleep(1.5)
webbrowser.open(f"http://127.0.0.1:{PORT}")
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    print("\nServeur arrêté.")
