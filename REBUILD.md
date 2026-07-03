# REBUILD — RECONSTRUCTION DU KIT EMSP À CHAQUE ÉVOLUTION

Projet EMSP (École de Médecine et de Santé Publique — Université des Comores).
Mission Expertise France / AFD, ODS 21SANOC277, réf. 2026/EAALDDDGPLDGDLS/15420,
Webcreatys SAS (Bernard Léglise). Volet école uniquement.

Ce fichier reste DANS le kit. Il permet de reconstruire la version suivante à partir
du kit courant, sans dépendre d'un prompt externe. Le kit courant est la base : la
chaîne historique (V1.77 + package 41 + overlays 42..47) est déjà absorbée dans
`programme/`. On ne repart JAMAIS de 41 + overlays.

---

## 1. LE MODÈLE EN TROIS PARTIES (non négociable)

```
EMSP_KIT_LANCEMENT_V1_99_xx/
  Demarrer_EMSP.bat / _lancer_emsp.py   lanceurs, agnostiques de version
  EMSP_V1_MAITRE_V1_99_yy.xlsx          maître de référence À LA RACINE (16 dessins)
  LISEZMOI.txt / _PASSATION_*.md / REBUILD.md / MANIFESTE.md5
  socle/      LE MOTEUR — installé une fois, ne change pas d'une version à l'autre
  programme/  L'APPLICATION — CHANGE à chaque version, AUCUNE donnée
  donnees/    LES DONNÉES CLIENT — jamais écrasées par une mise à jour
```

Règle de patch après production : on remplace UNIQUEMENT `programme/`.
`socle/` et `donnees/` ne bougent pas.

---

## 2. CE QU'IL FAUT POUR LA VERSION SUIVANTE (n+1)

De Bernard, trois choses seulement :

1. Le nouvel overlay = les fichiers `programme/` cumulatifs modifiés (fichiers entiers,
   dernier gagne).
2. Le FLAG explicite de tout payload hors-`programme/` (voir §3) : nouveau maître,
   nouveaux wheels. C'EST LE POINT DE RISQUE No 1.
3. Si un classeur change structurellement : le maître à jour + le script de migration.

Tout le reste est repris du kit courant.

---

## 3. LES TROIS ERREURS À NE JAMAIS REFAIRE

1. Ne copier que `programme/` d'un overlay. FAUX : certains overlays portent aussi un
   maître mis à jour et/ou des wheels pour le socle. Les ignorer = perdre une évolution
   structurelle (déjà vu : colonne R8 perdue car le maître de l'overlay 45 avait été ignoré).
2. Croire qu'un overlay manquant = code perdu. FAUX : les overlays livrent des fichiers
   entiers cumulatifs. Le risque n'est pas le code, ce sont les payloads hors-`programme/`.
3. Reconstruire une structure « maison ». Toujours partir du conteneur historique
   (socle / programme / donnees), structure identique.

---

## 4. RÈGLES ABSOLUES CLASSEUR / MAÎTRE

- Maître identifié par `dessins > 0`, JAMAIS par le nom.
- `openpyxl.save()` INTERDIT sur le maître (détruit les 16 dessins). Toute modification
  structurelle = chirurgie ZIP (édition XML directe). Revérifier `dessins > 0` après
  tout rechargement.
- Runtime `donnees/data/EMSP_V1.xlsx` : appliquer les migrations livrées EN PLACE via
  les scripts de `programme/scripts/` (idempotents : 2e passage = no-op). Ne jamais
  écraser les données client.
- Colonnes de formules protégées, jamais écrasées par l'IHM. `data.py` séparé du métier.

---

## 5. SOCLE (moteur Python hors-ligne) — figé

- Réutiliser `socle/` tel quel : Python 3.12.10 embeddable + `runtime/` déplié (pip) + `wheels/`.
- Runtime contient déjà : flask, openpyxl, werkzeug, jinja2, markupsafe, click, blinker,
  itsdangerous, et_xmlfile, colorama, pip + les 4 wheels PDF (fpdf2, defusedxml, fonttools,
  pillow) installés dans `runtime/Lib/site-packages` ET copiés dans `socle/wheels/`.
- N'ajouter au socle QUE si une nouvelle version introduit une dépendance Python : déposer
  le wheel dans `socle/wheels/` ET l'installer une fois dans `runtime/Lib/site-packages`.
- `runtime/python312._pth` doit contenir : `python312.zip` / `.` / `.\Lib\site-packages`
  / `.\Scripts` / `import site`.

---

## 6. PROCÉDURE DE BUILD (ordre exact)

```bash
# 1) Conteneur = copie du kit courant (1.99.49), renommé n+1
cp -r EMSP_KIT_LANCEMENT_V1_99_49 BUILD/EMSP_KIT_LANCEMENT_V1_99_49

# 2) programme/ : conserver formation/, remplacer le reste par le cumulatif n+1
#    (kit courant + overlay n+1 ; fichiers entiers, dernier gagne)

# 3) Si payload hors-programme dans l'overlay :
#    - nouveau maître -> remplacer à la racine (tel quel, JAMAIS openpyxl.save ; dessins>0)
#    - nouveaux wheels -> socle/wheels/ + installés dans runtime/Lib/site-packages

# 4) Migrations structurelles sur le runtime, en place :
#    python programme/scripts/<migr_...>.py donnees/data/EMSP_V1.xlsx

# 5) VERSION dans programme/config.py -> n+1 ; LISEZMOI.txt et _PASSATION_*.md à jour

# 6) Régénérer MANIFESTE.md5 (voir §8)

# 7) Nettoyer puis zipper :
find . -name __pycache__ -exec rm -rf {} + ; find . -name '*.pyc' -delete
zip -r -X ../EMSP_KIT_LANCEMENT_V1_99_49.zip EMSP_KIT_LANCEMENT_V1_99_49
```

`donnees/` (data + instance seed superadmin + photos + bibliotheque) et `formation/`
sont conservés. `instance/`, `sauvegardes/`, `__pycache__` exclus.

---

## 7. COLD CHECK OBLIGATOIRE (avant livraison)

Depuis la disposition du kit (`EMSP_DONNEES=…/donnees`), Flask test client, session
superadmin (`session["user"]="superadmin"`), `auth.doit_changer` neutralisé :

- `GET /` -> 200 ET partie centrale (`acc-hero`, 6 `acc-card`, `acc-stripes`).
- `GET /stages` -> 200 (colonne R8 lue sans erreur).
- `GET /planification/volumes` -> 200 ; `GET /planification/grille` -> 200.
- `GET /planification/grille/imprimer?filiere=SI&niveau=L1&annee=2025-2026&semestre=S1`
  -> 200, `application/pdf`, commence par `%PDF`.
- Maître : `dessins = 16`, colonne « Heures d'absence » présente.
- Runtime `EMSP_V1.xlsx` : même colonne présente (migration appliquée).
- site-packages runtime : `fpdf`, `defusedxml`, `fontTools`, `PIL`, `flask`, `openpyxl`.
- Audit doc : menu = Excel « Menu » = fiches manuels (0 manquant / 0 en trop).

---

## 8. MANIFESTE md5

Régénérer `MANIFESTE.md5` à chaque build. Il couvre les fichiers qui définissent la
version et les ancres d'intégrité (racine, `programme/`, classeurs `donnees/data`,
`socle/wheels`). Le runtime Python figé n'est pas haché ligne à ligne (repris de V1.77).
Le md5 du ZIP final est reporté dans le passation, pas dans le manifeste (auto-référence).

Commande de régénération (depuis la racine du kit) :
```bash
{ for f in $(find . -path ./socle/runtime -prune -o -type f -print | sort); do
    md5sum "$f"; done; } > MANIFESTE.md5
```

---

## 9. VOLET RÉSEAU (à traiter EN DERNIER)

Le code supporte déjà le réseau de base : `_lancer_emsp.py` lit `EMSP_HOST` (0.0.0.0),
postes secondaires en lecture seule, verrou serveur unique. Il manque le lanceur de
confort `Demarrer_EMSP_RESEAU.bat` (poser `EMSP_HOST=0.0.0.0`, afficher l'IP LAN,
avertir « un seul serveur »). Volet avancé (jeton d'édition par écran) : conception
figée, non développé. Ne pas mélanger avec les droits `P1_Roles` : le jeton est de la
concurrence, indépendant des droits.

---

## 10. RÈGLES MÉTIER VERROUILLÉES (rappel)

Coefficients AS = 1 ; moyenne CC ¼ + Examen ¾ (Décret 05-106, Art. 8) ; session 2
remplace l'examen, CC S1 conservé ; budget en année civile ; clôture bornée à l'année N.
Termes « V2 » et « Partiel » interdits dans les livrables client.
