#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import V1.99.51 — planning reel S1 2025-2026 dans `A3_Sessions` (EMSP_V1.xlsx).

IDEMPOTENT : relançable sans doublon (cle = annee + filiere + niveau + section +
jour + heure debut + heure fin + matiere). Agit EN PLACE via la couche d'acces
(`data.py`) — AUCUN openpyxl.save sur le maitre (le script ecrit dans le classeur
RUNTIME, sans dessin).

Source : `planning_s1_2025_2026.json` (fige depuis
`plnfiction_du_semestre_1_20252026__OK.xlsx` — 16 semaines, onglets L1/L2/L3 TC).
Arbitrages Bernard (03/07/2026) :
  - etiquettes « L1 » de l'onglet L2 TC reclassees L2 (matieres du programme L2) ;
  - exclusions : STAGE, Semaine de revision, Accueil, Pause (l'onglet AS, 100 %
    STAGE, n'apporte aucune seance de cours) ;
  - modele SUPERSET : le planning tourne sur 16 semaines, un meme creneau hebdo
    peut donc porter plusieurs matieres ; chaque (classe, jour, creneau, matiere)
    distinct = 1 seance recurrente ; `Vol. horaire prog.` = occurrences x 2 h ;
  - Semestre = semestre CURSUS (L1->1, L2->3, L3->5) ;
  - Enseignant : jointure E1 quand la matiere correspond a UN SEUL enseignant,
    sinon vide (completable a l'ecran A3) ; Salle vide (absente de la source).

Usage :
    python scripts/import_planning_A3_v1_99_51.py [chemin_EMSP_V1.xlsx]
Sans argument : config.WORKBOOK (donnees deployees).
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
sys.path.insert(0, RACINE)

import config            # noqa: E402
import data              # noqa: E402

JSON_PLANNING = os.path.join(ICI, "planning_s1_2025_2026.json")


def _norm(x):
    return str(x or "").strip().lower()


def main():
    chemin = sys.argv[1] if len(sys.argv) > 1 else config.WORKBOOK
    print("Classeur :", chemin)
    src = json.load(open(JSON_PLANNING, encoding="utf-8"))
    annee = src["annee"]
    sem_cursus = src["semestre_cursus"]
    db = data.AccesDonnees(chemin)

    ent = db.entetes("A3_Sessions")

    def brut(lib):
        for b in ent:
            propre = str(b)
            for m in (" (*)", " (**)"):
                if propre.endswith(m):
                    propre = propre[: -len(m)]
            if propre.strip() == lib:
                return b
        return lib

    # --- existant : cle d'idempotence + plus grand ID ------------------------
    existants = set()
    mx = 0
    idx = {}
    for i, b in enumerate(ent):
        propre = str(b)
        for m in (" (*)", " (**)"):
            if propre.endswith(m):
                propre = propre[: -len(m)]
        idx[propre.strip()] = i
    for r in db.lignes("A3_Sessions"):
        def v(lib):
            i = idx.get(lib, -1)
            return str(r[i]).strip() if i >= 0 and r[i] is not None else ""
        existants.add((_norm(v("Annee acad.")), _norm(v("Filiere")), _norm(v("Niveau")),
                       _norm(v("Section")), _norm(v("Jour")), _norm(v("Heure debut")),
                       _norm(v("Heure fin")), _norm(v("Matiere"))))
        sid = v("ID session")
        if sid[:1] in ("S", "s") and sid[1:].isdigit():
            mx = max(mx, int(sid[1:]))
        elif sid.isdigit():
            mx = max(mx, int(sid))

    # --- jointure enseignant (E1) : matiere -> nom si correspondance UNIQUE --
    e1 = {}
    ent1 = db.entetes("E1_Enseignants")
    idx1 = {}
    for i, b in enumerate(ent1):
        propre = str(b)
        for m in (" (*)", " (**)"):
            if propre.endswith(m):
                propre = propre[: -len(m)]
        idx1[propre.strip()] = i
    col_mat = next((c for c in idx1 if "Mati" in c), None)
    col_nom = next((c for c in idx1 if c.startswith("Nom")), None)
    col_pre = next((c for c in idx1 if c.startswith("Prenom")), None)
    if col_mat and col_nom:
        for r in db.lignes("E1_Enseignants"):
            mats = str(r[idx1[col_mat]] or "")
            nom = str(r[idx1[col_nom]] or "").strip()
            pre = str(r[idx1[col_pre]] or "").strip() if col_pre else ""
            libelle = (nom + " " + pre).strip()
            for mm in mats.replace(";", ",").split(","):
                mm = _norm(mm)
                if mm:
                    e1.setdefault(mm, set()).add(libelle)
    ens_unique = {m: sorted(s)[0] for m, s in e1.items() if len(s) == 1}

    # --- import -------------------------------------------------------------
    lignes, sautees, joints = [], 0, 0
    for s in src["seances"]:
        cle = (_norm(annee), _norm(s["filiere"]), _norm(s["niveau"]), _norm(s["section"]),
               _norm(s["jour"]), _norm(s["debut"]), _norm(s["fin"]), _norm(s["matiere"]))
        if cle in existants:
            sautees += 1
            continue
        existants.add(cle)
        mx += 1
        ens = ens_unique.get(_norm(s["matiere"]), "")
        if ens:
            joints += 1
        lignes.append({
            brut("ID session"): "S%03d" % mx,
            brut("Annee acad."): annee,
            brut("Semestre"): sem_cursus.get(s["niveau"], ""),
            brut("Filiere"): s["filiere"],
            brut("Niveau"): s["niveau"],
            brut("Section"): s["section"],
            brut("Matiere"): s["matiere"],
            brut("Enseignant"): ens,
            brut("Salle"): "",
            brut("Jour"): s["jour"],
            brut("Heure debut"): s["debut"],
            brut("Heure fin"): s["fin"],
            brut("Vol. horaire prog."): s["volume_h"],
        })
    if lignes:
        db.ajouter_lignes("A3_Sessions", lignes)
    print("Seances ajoutees :", len(lignes), "| deja presentes (sautees) :", sautees)
    print("Enseignant joint automatiquement (correspondance E1 unique) :", joints)
    print("OK — import planning A3 V1.99.51 termine.")


if __name__ == "__main__":
    main()
