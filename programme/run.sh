#!/usr/bin/env bash
# Lancement de l'interface EMSP V1 (Linux/macOS, hors-ligne)
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv && source .venv/bin/activate
  pip install --upgrade pip >/dev/null && pip install -r requirements.txt
else
  source .venv/bin/activate
fi
echo "Interface EMSP : http://127.0.0.1:5000"
python app.py
