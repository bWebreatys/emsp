#!/usr/bin/env bash
# Remet le jeu de FORMATION a neuf (exemples restaures, utilisateurs stagiaires effaces).
cd "$(dirname "$0")/.." || exit 1
if [ ! -f instance/formation.flag ]; then
  echo "Ce dossier n'est PAS une installation de formation (drapeau absent). Annule."
  exit 1
fi
cp -f formation/seed/EMSP_V1.xlsx data/EMSP_V1.xlsx
cp -f formation/seed/EMSP_Notes.xlsx data/EMSP_Notes.xlsx
rm -f instance/comptes.json instance/journal.csv
echo "Jeu de formation remis a neuf (mode formation conserve)."
