# PROMPT DE PASSATION — EMSP V1.99.52 → V1.99.53

> À coller en début de session. Projet EMSP (École de Médecine et de Santé Publique —
> Université des Comores), volet école uniquement (GMAO séparé). Mission Expertise
> France / AFD, Projet ODS 21SANOC277, réf. 2026/EAALDDDGPLDGDLS/15420 — Webcreatys SAS
> (Bernard Léglise). **Zéro re-diagnostic : ce document fait foi, `view` ciblés seulement.**

---

## 0. CADRAGE

- **Le TDR fait foi.** V1 = périmètre TDR strict. Hors TDR → candidat V2, pas développé.
- Stack : Python 3.12+/Flask, Excel .xlsx (openpyxl), Jinja2. 100 % hors-ligne, aucun CDN.
  Charte : zéro emoji ; Tabler Icons ; #1F4E79 ; Calibri ; dates JJ/MM/AAAA ; KMF.
  Termes « V2 » et « Partiel » interdits dans les livrables client.
- **Git : TRANCHÉ le 03/07 — dépôt NON réactivé** (coupures de courant / internet
  instable sur place). Livraisons par ZIP uniquement. Ne plus reposer la question.
- Méthode : arbitrages verrouillés AVANT le code ; propagation toutes couches
  (IHM → app.py → Excel → doc/doc_des_ecrans.md → ETAT.md) ; un fichier = un patch ;
  banc d'essai obligatoire avant livraison (0 réponse ≥ 500) ; heredocs quotés `<<'PY'`.
- Maître identifié par `dessins > 0` ; `openpyxl.save()` INTERDIT sur le maître
  (chirurgie ZIP seulement). `EMSP_Notes.xlsx` : aucun dessin, openpyxl direct autorisé.
- Fin de session : résumé de passation + mise à jour `ETAT.md` + rappeler à Bernard de
  déposer `.py` et templates à plat dans les Fichiers du projet.

---

## 1. BASE DE TRAVAIL

| Élément | Valeur |
|---|---|
| Kit de référence | `EMSP_KIT_LANCEMENT_V1_99_52_SANS_SOCLE.zip` (md5 annoncé à la livraison) |
| VERSION applicative | `1.99.52` (config.py) — prochaine : **1.99.53** |
| Maître (racine kit) | `EMSP_V1_MAITRE_V1_99_45.xlsx` — 16 dessins, 34 onglets — INCHANGÉ en V1.99.50 |
| Structure modifiée | `EMSP_Notes.xlsx` : V1.99.50 : colonne `Coef matiere (*)` dans N1 + barème AS — `migr_bareme_v1_99_50.py`. V1.99.51 : A3_Sessions chargé (646 séances) — `import_planning_A3_v1_99_51.py` (idempotents, EN PLACE) |
| Menu | 55 écrans visibles (59 entrées TAB_INDEX testées), banc d'essai = **0 plantage** |
| Packages | SANS socle. Patch = remplacer `programme/` + exécuter la migration sur les données déployées ; ne JAMAIS écraser `donnees/` |

**Acquis V1.99.50 (chantier notes/bulletin, arbitré avec Bernard le 03/07) :**
- **Coef par matière** : colonne `Coef matiere` (défaut 1) dans N1 ; moyenne d'UE =
  moyenne des matières **pondérée** (à 1 = arithmétique, modèle du relevé officiel).
  Affiché grille bulletin + relevé si ≠ 1 ; éditable écran Barème ; pré-rempli à 1.
- **Session 2 conforme au relevé officiel** (décret art. 10) : matière repassée =
  notes de session 2 SEULES (CC S1 annulé ; avant : ¼CC1+¾Ex2). Moteur revalidé au
  centième contre le relevé L2 SI : S1 = 9,89 ; sess. 2 = 11,87 ; 14 moyennes d'UE.
- **Éditions du bulletin par session** : Impressions > Relevé de notes, sélecteur
  Session (Première = sans colonnes rattrapage / Deuxième = avec) ; libellé imprimé
  par bloc semestre ; jusqu'à 4 pages (2 semestres × 2 sessions).
- **Barème Aides-soignants** créé (11 modules, coef 1, semestre 1, niveau vide).
- **Coef confirmé = Non PARTOUT** (y compris L2 SI) : constat — N1 suit la maquette
  RÉVISÉE (S3 = UE16…UE24) ; le relevé 2024-2025 suit l'ANCIENNE numérotation
  (UE10…UE16). Aucun barème n'est confirmé ligne à ligne par un document. Mention
  « Barème provisoire » réactivée ; la scolarité confirme filière par filière.
- Coefs UE SI/SO recalculés `Crédit/2` (ECTS/2, programme révisé).
- Écran bulletin (décision Bernard) : reste en CC unique dérivé (pas de saisie des
  contrôles détaillés ici — elle vit sur /notes-classe).

**Acquis V1.99.51 (P0-B, arbitré et livré le 03/07) :** planning réel S1 2025-2026
importé dans A3 — 646 séances, 2 960 h, 171 enseignants auto-joints (E1, correspondance
unique), IDs S001…S646. Mapping : L1 de l'onglet L2 TC reclassé L2 ; exclusions STAGE /
révision / Accueil / Pause (AS = 100 % STAGE, rien) ; superset 16 semaines (plusieurs
matières possibles par créneau hebdo) ; Semestre = cursus (1/3/5) ; Salle vide (à
compléter par l'EMSP à l'écran Séances — le planning des salles côté cours restera vide
d'ici là). Débloqué : présences par séance planifiée + vue par professeur, grille de
planification, sélecteurs E2. Données figées : `scripts/planning_s1_2025_2026.json`.

**Acquis V1.99.52 (P1-C, livré le 03/07) :** amorçage compta. Constat : la liste des
comptes vient de F2 (LISTES_ONGLET), pas de P0 (colonne vestige) ; F2 porte DÉJÀ les
comptes réels « Compte bancaire UDC-EMSP-ODS (BIC-Comores) » (n° 00002130706001KMF) et
« Caisse EMSP » — restent à l'EMSP : soldes initiaux + écritures. POSTE_DEPENSE_VACATIONS
= « 642 — Cours complémentaires (heures supplémentaires) » (défaut, modifiable à l'écran).
Nouveau doc de recette `doc/circuit_test_compta.md` (circuit E3→E2→E4→arrêté→compta→
contrôles F1/F2/journal, garde-fous par étape) — support de la formation finances.



---

## 2. RÈGLES ABSOLUES (inchangées)

1. Maître par `dessins > 0` ; jamais `openpyxl.save` dessus ; chirurgie ZIP + recontrôle.
2. Données de production : scripts idempotents testés sur copie jetable, puis EN PLACE.
3. Heredocs quotés. 4. `.value = None` pour vider une cellule.
5. Banc d'essai : sweep menu (Flask test client, superadmin `session["user"]`,
   `auth.doit_changer` neutralisé), 0 réponse ≥ 500 + cold checks ciblés.
6. Overlays cumulatifs ; inspecter les payloads hors-`programme/`.
7. `MANIFESTE.md5` régénéré ; `__pycache__`/`.pyc` purgés avant zip.

---

## 3. RESTE DE L'AUDIT DU 01/07 (actions suivantes, GO de Bernard par étape)

- ~~P0-B — Importer le planning A3~~ : **FAIT en V1.99.51.** Reste côté EMSP :
  affecter les salles aux séances (écran Séances) pour alimenter le planning des salles.
- ~~P1-C — Amorçage compta~~ : **FAIT en V1.99.52** (constat F2 déjà bon, poste 642,
  doc de recette). Reste côté EMSP : soldes initiaux F2 + écritures réelles + dérouler
  `doc/circuit_test_compta.md`.
- **P1-D — Seed lieux de stage** : `Liste_des_lieux_de_stages_actuels.docx` → `S2_Lieux_stage`.
- **P2-E — Registre candidats V2** : rapprochement bancaire · réservation d'équipements ·
  plaintes/évaluations stages détaillées · groupes TD/TP · montants sur relevés mensuels.

## 4. EN ATTENTE / ARBITRAGES OUVERTS

- **Écran « Saisie des notes de stage »** (maquettes appréciées, code NON écrit) — 3
  questions toujours SANS réponse : tous les élèves ou seulement les affectés ; lieu en
  liste S2 (recommandé) ; colonne Observation sur grille ou éditions seulement.
- **Stages R12** : fusion « affectation » ↔ « fiches retour » en attente specs Dr Kamal.
- **États de paiement** : proposition de retirer l'écran table `E4` du menu — attendre
  le « ok retirer » de Bernard.
- **Matrice des rôles `P1_Roles`** (fonctions nommées par rôle) à présenter pour validation.
- **Sauvegarde automatique quotidienne** (demande Bernard 03/07) : au premier lancement
  du jour, sauvegarde des classeurs (poste principal ; réseau aussi si actif). À traiter
  AVEC le volet réseau (`Demarrer_EMSP_RESEAU.bat` + doc) — le tout EN DERNIER.
- **Coefficients** : la scolarité saisit les coefs officiels filière par filière (écran
  Barème des UE) puis passe `Coef confirmé` à Oui. Coefs par matière : seulement si
  l'école applique des coefficients différenciés (ancienne maquette Imagerie en porte).

## 5. LIVRAISON (format inchangé)

1. Bump VERSION + LISEZMOI + passation. 2. Banc d'essai 0 plantage + cold checks.
3. Purge `__pycache__` → MANIFESTE.md5 → zip SANS_SOCLE → `unzip -t` → md5 annoncé.
4. Pose : copier UNIQUEMENT `programme/` + exécuter les migrations en place ;
   ne jamais écraser `donnees/`. 5. Livraison ZIP (pas de Git).
