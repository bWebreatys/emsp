# CONSIGNES DE PACKAGING ET DE LIVRAISON — Projet EMSP (volet école)

Document **permanent** du projet. À respecter pour **toute nouvelle version**.
Mission Expertise France / AFD — Projet ODS 21SANOC277 — réf. 2026/EAALDDDGPLDGDLS/15420 — Webcreatys SAS.
Dépôt : github.com/webcreatys/emsp (branche main). Dernière mise à jour : 24/06/2026 (V1.70).

---

## 0. Pourquoi ce document

Incident V1.58 : l'archive de **code seul** (`emsp_interface_VXX.zip`) a été prise pour un kit
exécutable. Elle ne contenait ni lanceur, ni socle, ni classeurs. Résultat : application impossible à
démarrer, puis — une fois un socle ajouté — `FileNotFoundError` sur `donnees\data\EMSP_V1.xlsx`
(classeur absent). Ces consignes garantissent qu'aucune livraison ne reproduise ce blocage.

**Principe de base : une archive de code n'est PAS un kit. Un kit doit démarrer, hors-ligne, du premier coup.**

---

## 1. Architecture en trois couches (rappel)

- **`socle/`** — moteur technique : Python embeddable + `runtime/Lib/site-packages` (toutes les
  bibliothèques). Installé une fois, **hors-ligne**. **Jamais dans le dépôt** (binaires).
- **`programme/`** — le code (écrans, logique, modèles). **Remplacé à chaque mise à jour. Aucune
  donnée.** C'est *exactement* ce que versionne le dépôt GitHub.
- **`donnees/`** — `data/` (classeurs) + `instance/` (comptes, journal). **Jamais écrasé par une mise
  à jour.** Dossier **frère** de `programme/`.

Résolution des chemins (`config.py`) : `DONNEES_DIR = EMSP_DONNEES` sinon dossier **frère** `donnees`
de `programme/`. Le lanceur `_lancer_emsp.py` fixe `EMSP_DONNEES = <kit>\donnees` pour être
déterministe quel que soit l'emplacement du kit.

---

## 2. Deux formats de livraison — ne jamais les confondre

| Format | Contenu | Usage | Socle ? | Classeurs ? |
|---|---|---|---|---|
| `MAJ_EMSP_V1_xx.zip` | uniquement les fichiers de `programme/` modifiés | mise à jour en place | non | non |
| `EMSP_KIT_LANCEMENT_V1_xx.zip` | kit complet exécutable (socle + programme + donnees) | installation propre / poste neuf | **oui** (runtime hors-ligne) | **oui** (gabarits vides) |

Règle : ne **jamais** présenter une archive de code (`programme/` seul) comme « exécutable ».

---

## 3. Ce que tout KIT complet DOIT contenir (sinon il ne démarre pas)

- [ ] `socle/runtime/python.exe` + `Lib/site-packages` avec **toutes** les dépendances
  (Flask, openpyxl, Jinja2, Werkzeug, click, blinker, itsdangerous, markupsafe, et-xmlfile,
  colorama, pip) — **aucune étape Internet** au lancement.
- [ ] `socle/runtime/python3xx._pth` contenant `import site` **et** `.\Lib\site-packages`.
- [ ] `Demarrer_EMSP.bat` (**CRLF**) + `_lancer_emsp.py` (fixe `EMSP_DONNEES`).
- [ ] `programme/` = code de la version, **sans** `data/`, `instance/`, `__pycache__/`, `.pyc`.
- [ ] `donnees/data/EMSP_V1.xlsx` **ET** `donnees/data/EMSP_Notes.xlsx` **présents** (structure à jour,
  vides de données réelles). **← Classeur absent = 500 `FileNotFoundError`. C'est le piège n°1.**
- [ ] `donnees/instance/` présent et vide.
- [ ] `LISEZMOI.txt` + le présent `CONSIGNES_LIVRAISON.md`.

---

## 4. Test de livraison OBLIGATOIRE avant de zipper

Sur une **copie** du kit assemblé (jamais sur la production) :

1. Démarrer (ou simuler le démarrage) avec le socle.
2. Vérifier que `metier.roles()` lit `P1_Roles` **sans erreur** → preuve que le classeur est trouvé.
3. `GET /login` → 200 ; `GET /` → 302 ; au moins **une page qui lit le classeur** (tableau de bord) → **pas de 500**.
4. Vérifier l'**absence** de `__pycache__`/`.pyc` dans le zip et les `.bat` en **CRLF**.

5. **Bandeau multicritère présent** (V1.71) : `grep _lire_filtres programme/app.py` doit renvoyer une ligne, **et** au smoke-test le bandeau de filtres est visible sur une page module + le tableau de bord, et `/module/<onglet>/imprimer` répond **200** (pas 404).

**Aucune livraison ne sort sans ce test au vert.**

---

## 5. Règle d'or des données

- Une mise à jour ne touche **que** `programme/`. `donnees/` et `socle/` sont **intouchables**.
- Le KIT complet est livré avec des classeurs **gabarits** (structure à jour, **vides** de données
  réelles). En production, l'utilisateur dépose **ses** classeurs dans `donnees/data/`.
- Un kit complet s'installe dans un **dossier neuf** : ne jamais livrer un kit qui écraserait les
  données de production.

---

## 6. Pièges techniques connus (à revérifier à chaque version)

- **`.bat` en CRLF** : un LF seul casse `cmd.exe` sur les `if/else` multi-lignes.
- **Exclure `__pycache__` et `.pyc`** des zips (sinon erreur Windows 0x80010135, chemins trop longs).
- **Python embeddable** : `._pth` doit activer `import site` ; `pip` bootstrappé depuis son wheel ;
  `colorama` ajouté à la main (le marqueur Windows n'est pas évalué par `pip download`).
- **openpyxl détruit les 16 dessins** de `EMSP_V1.xlsx` à la sauvegarde → toute modification de
  **structure** du classeur maître passe par **chirurgie zip + re-scellage md5**, jamais
  `openpyxl.save`. `EMSP_Notes.xlsx` (sans dessin) : `openpyxl.save` autorisé.
- **Wheels uniquement officiels PyPI.** Aucun binaire issu d'une clé USB tierce dans le socle, le
  dépôt ou l'application (rappel sécurité : malware de cryptominage signalé sur la clé du gestionnaire).
- **Ouverture du navigateur APRÈS le serveur** : ne pas pré-ouvrir le navigateur dans le `.bat` avant
  le démarrage de Flask (le chargement de `metier.py` prend 1–2 s → `ERR_CONNECTION_REFUSED`). Le
  lanceur `_lancer_emsp.py` attend que le port 5000 réponde, puis ouvre le navigateur.
- **Renommer une liste P0 partagée** (ex. V1.70 `Bailleurs` → `Sources_financement`) : repérer **TOUS**
  les points qui pointent l'ancien libellé, sinon une liste déroulante casse silencieusement —
  (1) les appels directs `metier.options_liste("<ancien nom>")` dans `app.py` ; (2) les références de
  liste du Dictionnaire (corrigées par `DICTIONNAIRE_SURCHARGE`, jamais en remuant l'onglet de saisie).
  Vérifier après coup : `options_liste("<nouveau>")` renvoie les valeurs, `options_liste("<ancien>")`
  renvoie `None`. La résolution finale rapproche par **en-tête P0 strippé**, donc renommer la colonne
  P0 suffit à rebrancher la liste, à condition d'avoir repointé les appels et surcharges ci-dessus.
- **Ajouter un onglet saisissable** (ex. V1.70 `F3_Budget_poste` / `P2_Taux`) : l'onglet doit figurer
  dans `GUIDE_STRUCTURE` (donc `TAB_INDEX`) **sinon `/module/<onglet>` renvoie 404** ; et dans
  `ONGLETS_SAISIE_ACTIVE` pour que le formulaire de saisie apparaisse. Pour l'écriture, l'onglet doit
  être dans un groupe `MODULES_ONGLETS` **ou** `ONGLETS_DIRECTION` (sinon `peut_ecrire` le refuse, même
  à « Tous »).
- **Propager toute modification sur toutes les couches** :
  `config → data → metier → auth → app → templates → Excel (si besoin) → README → doc/doc_des_ecrans.md → ETAT.md`.

- **KIT assemblé avec un `app.py` (ou des templates) périmé** (rencontré V1.71) : un kit peut « tourner » sans aucune erreur alors que la fonctionnalité est **inerte** — bandeau de filtres invisible, routes `/…/imprimer` en **404** — parce que `programme/app.py` est une version antérieure aux templates (ou l'inverse : `app.py` à jour mais sans `_bandeau_filtres.html` / `impression_selection.html`). **Après tout assemblage du KIT**, vérifier `grep _lire_filtres programme/app.py` (doit matcher) et confirmer que `app.py` **et** les templates sont de la **même touche**.

---

## 7. Checklist de clôture (à cocher avant le ZIP numéroté)

- [ ] `VERSION` mise à jour dans `config.py`.
- [ ] `py_compile` des modules OK ; 0 erreur de formule si classeur touché ; md5 re-scellé si chirurgie.
- [ ] `README.md` + `doc/doc_des_ecrans.md` + `ETAT.md` à jour (section de version).
- [ ] `MAJ_EMSP_V1_xx.zip` (programme modifié) **et/ou** `EMSP_KIT_LANCEMENT_V1_xx.zip` (kit complet **testé** §4).
- [ ] Confirmation de la liste des champs **avant** d'implémenter un écran.
- [ ] Résumé de passation rédigé ; `ETAT.md` mis à jour.
- [ ] Push GitHub (branche main) — token via `$env:GITHUB_TOKEN`, **jamais collé** dans le chat.
