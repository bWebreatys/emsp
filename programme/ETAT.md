# ETAT — Projet EMSP (volet École)

Dernière mise à jour : 03/07/2026 — **Interface V1.99.52**
Dépôt Git **abandonné** (retranché le 03/07 : coupures de courant / internet instable) — livraisons par archives ZIP (MAJ + kit).

## Ce qui change en V1.99.52 (P1-C : amorçage comptabilité)

> **AUCUNE modification des classeurs ni migration** : lot documentaire + un défaut de configuration.

- **Constat d'analyse** : la liste des comptes sélectionnables est alimentée par **F2_Comptes** (`config.LISTES_ONGLET`), pas par la colonne P0 `Comptes_caisses` (vestige jamais lu, laissé en l'état). F2 porte **déjà les comptes réels** de l'EMSP : « Compte bancaire UDC-EMSP-ODS (BIC-Comores) » (n° 00002130706001KMF — journaux banque/caisse et rapprochements d'avril 2024 à janvier 2026) et « Caisse EMSP ». Le manque réel n'est donc pas le référentiel mais les **soldes initiaux et les écritures**, qui reviennent à l'EMSP.
- **`POSTE_DEPENSE_VACATIONS` renseigné** : `642 — Cours complémentaires (heures supplémentaires)` (défaut du passage en compta des états de paiement, modifiable à l'écran au moment du passage).
- **Nouveau document de recette** : `doc/circuit_test_compta.md` — circuit de bout en bout à dérouler par l'EMSP (présences → heures constatées E3 → report E2 à motif → état de paiement E4 `PAIE-<année>-<semestre>` → arrêté → passage en compta → contrôles F1 (1 dépense/enseignant réf commune) / F2 (solde courant) / `journal.csv` / éditions AFD), garde-fous listés étape par étape (anti-double-passage, état non arrêté refusé, motif de régularisation obligatoire, enseignant à 0 h absent).
- **Lot** : `config.py` (VERSION 1.99.52, poste 642), `doc/circuit_test_compta.md` (nouveau), `LISEZMOI.txt`, `ETAT.md`.
- **Banc d'essai** : comptes réels présents dans `comptes_treso()` (source F2) ; garde-fou « passage sans arrêté » refusé ; sweep 59 écrans = 0 plantage ; cold checks trésorerie / F2 / E4 à 200.

## Ce qui change en V1.99.51 (P0-B : import du planning réel dans A3_Sessions)

> **AUCUNE modification de structure des classeurs, maître INCHANGÉ.** Données ajoutées au
> runtime `EMSP_V1.xlsx` (onglet `A3_Sessions`, sans dessin) via la couche d'accès.
> Import idempotent : `scripts/import_planning_A3_v1_99_51.py` + données figées
> `scripts/planning_s1_2025_2026.json` (précédent V1.57 `bareme_data.json`).

- **Source** : `plnfiction_du_semestre_1_20252026__OK.xlsx` (document EMSP) — 16 semaines (S1…S16), onglets L1/L2/L3 TC + AS, grilles jours × 4 créneaux de 2 h × sections, cellules fusionnées gérées.
- **Mapping arbitré avec Bernard (03/07)** : étiquettes « L1 » de l'onglet L2 TC **reclassées L2** (matières du programme L2) ; **exclusions** STAGE / Semaine de révision / Accueil / Pause (l'onglet AS = 100 % STAGE → aucune séance de cours) ; **modèle superset** (le planning tourne sur 16 semaines → un créneau hebdo peut porter plusieurs matières ; chaque (classe, jour, créneau, matière) distinct = 1 séance récurrente, `Vol. horaire prog.` = occurrences × 2 h) ; **Semestre = cursus** (L1→1, L2→3, L3→5) ; **Enseignant** joint depuis E1 quand la matière ne correspond qu'à un seul enseignant, sinon vide ; **Salle vide** (absente de la source, à compléter à l'écran Séances).
- **Résultat** : **646 séances**, **2 960 h programmées**, 164 matières, **171 séances avec enseignant auto-joint**, IDs `S001…S646` (convention de l'écran A3).
- **Débloqué en cascade (audit du 01/07, point 2)** : feuille de présence par séance planifiée ; vue Présences **par professeur** (20 enseignants au planning) ; **grille de planification hebdomadaire** remplie ; sélecteurs de séances du report d'heures E2. Le planning des **salles** côté cours restera vide tant que l'EMSP n'a pas affecté les salles aux séances.
- **Lot** : `EMSP_V1.xlsx` (A3 : +646 lignes), `config.py` (VERSION 1.99.51), `scripts/import_planning_A3_v1_99_51.py` (nouveau), `scripts/planning_s1_2025_2026.json` (nouveau), `LISEZMOI.txt`, `ETAT.md`. Aucun changement de code applicatif.
- **Banc d'essai** : import idempotent (double passage : 0 ajout, 646 sautées) ; `metier.seances()` = 646 ; cold checks présences classe+date (cours du lundi affichés), vue par professeur (avec et sans professeur choisi), grille remplie (matières aux bons créneaux), module A3 ; **sweep 59 écrans = 0 plantage**.

## Ce qui change en V1.99.50 (barème : coef par matière · session 2 conforme au relevé · éditions du bulletin par session · barème Aides-soignants)

> **Modification de structure : une colonne** — `Coef matiere (*)` insérée dans `N1_Bareme_UE`
> (`EMSP_Notes.xlsx`, classeur sans dessin → openpyxl direct, le maître reste INCHANGÉ).
> Migration idempotente : `scripts/migr_bareme_v1_99_50.py` (à exécuter EN PLACE sur les données déployées).

- **Coefficient par matière** (arbitré avec Bernard) : nouvelle colonne `Coef matiere` (défaut 1). La **moyenne d'UE** est désormais la **moyenne des matières pondérée** par ce coef ; à 1 partout elle reste arithmétique — c'est le modèle du **relevé officiel** (recontrôlé au centième : UE11 = 11,78 ; S3 = 9,89). Affiché sur la grille bulletin et le relevé quand ≠ 1, éditable à l'écran Barème des UE, pré-rempli à 1 à la saisie.
- **Session 2 — alignement sur le relevé officiel** (et décret 05-106 art. 10 « la note de la 1ère session est annulée ») : la moyenne d'une matière repassée = **notes de la session 2 seules** (CC de rattrapage s'il existe, sinon examen seul). L'ancien comportement (CC de S1 conservé, ¼CC1+¾Ex2) donnait p. ex. 8,50 là où le relevé officiel affiche 10,00. Vérifié au centième : moyennes session 2 UE13 = 11,88, UE14 = 10,13, UE15 = 10,50, **semestre = 11,87**.
- **Éditions du bulletin par session** (demande Bernard, modèle = les 2 pages du relevé fourni) : sélecteur **Session** sur Impressions > Relevé de notes — *Première session* (page sans colonnes rattrapage, notes S1 seules) / *Deuxième session* (colonnes Exam. sess. 2 / Moy. sess. 2). Libellé de session imprimé en tête de chaque bloc semestre. Jusqu'à 4 pages (2 semestres × 2 sessions).
- **Barème Aides-soignants créé** : 11 modules du programme révisé (1 ligne par module, semestre 1, niveau vide comme dans A1, coef 1, `Coef confirmé = Non`).
- **Coefs UE SI/SO** recalculés selon le programme révisé (`Coef = Crédit/2`, dérivé des ECTS). **`Coef confirmé = Non` PARTOUT** (y compris L2 SI) : constat d'audit — le barème N1 suit la **maquette révisée** (UE16…UE24 en S3) alors que le relevé officiel 2024-2025 suit l'ancienne numérotation (UE10…UE16) ; aucun barème n'est donc confirmé ligne à ligne par un document. La mention « Barème provisoire » est réactivée partout ; la scolarité confirmera filière par filière.
- **Lot** : `EMSP_Notes.xlsx` (+ colonne, migration), `config.py` (VERSION 1.99.50, dictionnaire + largeur + pré-remplissage `Coef matiere`), `metier.py` (`_bareme_ues`, `releve_semestre`, `releve_annuel`, `_notes_effectives`, `_cc_session`, `_notes_brutes`, `bulletin_saisie`, `bulletin_officiel` — paramètre session), `app.py` (`/impressions/bulletin?session=`), `templates/bulletin_saisie.html` (coef affiché + moyenne UE pondérée côté client), `templates/releve.html`, `templates/bulletin_officiel.html` (libellé session), `templates/impressions.html` (sélecteur), `scripts/migr_bareme_v1_99_50.py` (nouveau), `doc/doc_des_ecrans.md`, `ETAT.md`.
- **Banc d'essai** : moteur reproduit le relevé officiel L2 SI au centième — 7 moyennes d'UE session 1 + semestre **9,89**, 7 moyennes session 2 + semestre **11,87**, matière témoin 4,00 → 10,00 ; pondération coef matière vérifiée (UE10 coefs 3/1 → 16,00) ; éditions session 1/2 du bulletin vérifiées (colonnes conditionnelles + libellés) ; migration idempotente (double passage sans effet) ; **sweep 59 écrans TAB_INDEX = 0 plantage** ; cold checks écrans notes/bulletin/impressions OK.
- **Règle métier documentée** : le relevé officiel scanné (RELEVE_NOTES) fait foi pour les calculs ; les maquettes révisées font foi pour la structure des barèmes. Les deux référentiels ne coïncidant pas (numérotations différentes), tout barème reste provisoire jusqu'à confirmation par la scolarité.

## Ce qui change en V1.77 (matière non dispensée)

> **Modification de structure des classeurs : un seul ajout** — nouvel onglet `N5_Matieres_ND` dans `EMSP_Notes.xlsx` (classeur sans dessin → ajout openpyxl direct, aucune chirurgie ZIP ; le maître `EMSP_V1_MAITRE_V1_70.xlsx` reste INCHANGÉ).

- **Interrupteur « Matière non dispensée ce semestre »** dans la grille de saisie des notes (avec motif facultatif). Statut au **niveau classe** (pas par étudiant), tracé dans `N5_Matieres_ND` (Filière, Niveau, Section, Année, Session, Semestre, N° UE, Matière, Motif, Saisi par). Réversible : décocher retire la trace.
- **Affichage (b)** sur relevé / bulletin : la matière ND **n'apparaît pas** ; **mention de traçabilité** ajoutée en pied ; **moyenne recalculée** automatiquement sur les seules matières faites et notées. Remplace l'exclusion implicite (matière vide) par un statut **explicite et tracé**.
- **ECTS — option (i)** (validée avec la direction) : l'UE **garde tous ses ECTS** tant qu'au moins une matière est faite ; seule une **UE entièrement non dispensée** est retirée du relevé et de l'`ects_total` (prorata = retrait). Une matière dispensée mais **pas encore notée** ≠ ND : le relevé est marqué **incomplet/provisoire**, sans exclusion.
- **Lot** : `EMSP_Notes.xlsx` (+ onglet N5), `config.py` (VERSION 1.77, `ONGLETS_NOTES` + schéma Dictionnaire N5), `metier.py` (helpers `_matieres_nd` / `_nd_etat_exact` / `enregistrer_matiere_nd`, `releve_semestre` / `releve_annuel` / `bulletin_officiel` / `notes_grille` / `enregistrer_notes_grille`), `app.py` (route d'enregistrement : `non_dispensee` + `motif`), `templates/saisie_notes_classe.html`, `templates/releve_print.html`, `templates/bulletin_officiel.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## Ce qui change en V1.76 (grille de saisie des notes par classe)

> **AUCUNE modification de structure des classeurs.** Écriture dans `N4_Controles` (contrôles) et `N2_Notes` (examen) via la couche d'accès ; CC dérivé de N4.

- Nouvel écran **Saisie des notes par classe** (`NOT_Grille` → `/notes-classe`) : liste d'élèves façon feuille de présence, pour une classe × matière (sélection filière/niveau/section/année/semestre/session/matière).
- **Plusieurs contrôles** paramétrables (3 par défaut, coef 1 par colonne modifiable) → **CC = moyenne pondérée** des contrôles ; **Moyenne = ¼ CC + ¾ examen** (décret 05-106, art. 8, confirmé sur le relevé officiel).
- Écriture : `metier.enregistrer_notes_grille` (upsert N4 par étudiant × contrôle + N2 examen) ; réduction du nombre de contrôles → nettoyage des contrôles supprimés (pas d'orphelin) ; colonne entièrement vide non ressurgie au rechargement.
- **Édition** imprimable `/impressions/feuille-notes` (paysage, C1…Cn + CC + Examen + Moyenne, signatures).
- **Lot** : `config.py` (VERSION 1.76, entrée hub + `SPECIAL_ROUTES["NOT_Grille"]`), `metier.py` (grille + édition, bloc V1.76 en fin de fichier), `app.py` (routes `/notes-classe`, `/notes-classe/enregistrer`, `/impressions/feuille-notes`), `templates/saisie_notes_classe.html` (nouveau), `doc/doc_des_ecrans.md`, `ETAT.md`.
- **Tests** (boot superadmin, classe réelle Soins infirmiers L1 2025-2026 / UE1 Communication) : 9 routes à 200 (sélection, grille, édition, non-régression bulletin/relevé/impressions/présences/droits) ; calcul vérifié (3 contrôles coef 1/1/2 → CC 12,5 ; moyenne ¼-¾ exacte) ; réduction de contrôles propre ; **0 emoji**.

## Ce qui change en V1.75 (éditions logistiques & financières)

> **AUCUNE modification du classeur** (md5 maître inchangé `c44c7864…`). Lecture seule sur M1 / L3 / F1, rendu générique `kind="table"`.

- **Inventaire des équipements** `/impressions/inventaire?axe=salle|bailleur|etat` (M1) : regroupement au choix par salle, bailleur ou état, **sous-totaux** quantité + montant + total général (paysage). Couvre #12/#13 du reste-à-faire.
- **Expression de besoin** `/impressions/bon-besoin?statut=&priorite=&salle=` (L3) : état filtrable des besoins, total des coûts estimés (paysage). Couvre #14.
- **Recettes / dépenses par source de financement** `/impressions/etat-bailleur?annee=` (F1) — **garde financier** : regroupement par bailleur (AFD/OMS/EMSP…), total recettes/dépenses/solde, filtre année civile facultatif. Couvre #26 (**reporting bailleur AFD**).
- Cartes inventaire/besoin en section **Logistique** du hub (la matrice des droits en hérite via le groupe Logistique) ; carte bailleur en section financière (`peut_financier`).
- **Lot** : `config.py` (VERSION 1.75), `metier.py` (3 éditions + 6 helpers de filtres, bloc V1.75 en fin de fichier), `app.py` (3 routes `/impressions/inventaire|bon-besoin|etat-bailleur` + contexte du hub), `templates/impressions.html` (3 cartes), `doc/doc_des_ecrans.md`, `ETAT.md`.
- **Tests** (boot superadmin, copie seedée M1 280 lignes / L3 / F1) : les 12 routes à 200 (3 éditions × axes/filtres + non-régression hub, balance, accueil, fiche enseignant, autorisations), inventaire bailleur TOTAL 2 415 000 KMF, état bailleur AFD solde 3 800 000 KMF, bon de besoin total 500 000 KMF, hub mis à jour, **0 emoji**.

## Ce qui change en V1.74 (droits par utilisateur)
- Les droits etaient deja **par login** dans `P1_Roles` (role = etiquette) : deux comptes d'un meme role peuvent differer.
- Ecran « Comptes & acces » : **roles-modeles** (pre-remplissage) + **cases par groupe** Lecture/Ecriture + bascules **Acces financier** / **Admin droits**, ajustables **par utilisateur**. Ecriture via `enregistrer_utilisateur` (anti-blocage dernier admin).
- Modeles dans `config.ROLES_MODELES` (editables, sans toucher au classeur) ; reglage fin compte par compte a l'usage (prevu pour la formation).
- **Tests** : ecran rendu (modele + cases + bascules) ; creation `gestionnaire` (ecrit Finances) vs `assistant_compta` (lecture seule Finances) -> meme role, droits differents ; modele « Tous » -> ecrit P0 ; matrice 2 lignes distinctes ; non-regression / et /autorisations 200.

## Ce qui change en V1.73 (interface : accueil + fiche enseignant)
- **Accueil** : bandeau KPI retiré (point de départ pur) ; tuiles agrandies.
- **Fiche enseignant `/enseignant`** symétrique de la fiche étudiant : recherche, photo (hors classeur), identité E1 en lecture seule + bouton « Modifier dans le module » (`?modifier=`), heures E2 (totaux), séances A3 (lien Nom+Prénom, matricule à terme), exceptions E3, fiche imprimable (navigateur, paysage).
- **Fiche étudiant imprimable** ajoutée (même moteur).
- **Classeur non touché** (md5 maître inchangé). Pseudo-page `ENS_Fiche`.
- **Lot** : config.py (VERSION 1.73), metier.py (helpers enseignant), app.py (routes /enseignant*, impressions fiches), templates (accueil, enseignant, *_print, etudiant, module), README, doc/doc_des_ecrans.md, ETAT.md.
- **Correctif recherche (fiches)** : la selection dans la liste deroulante envoyait le **libelle complet** (`matricule — Nom (...)`) au lieu du seul matricule (le `form.submit()` natif ne declenchait pas le nettoyage). Corrige cote **JS** (nettoyage avant envoi + `requestSubmit`) et cote **serveur** (`_matricule_saisi` extrait le matricule meme si le libelle complet arrive ; tolere les espaces). Vaut pour `/etudiant` et `/enseignant`.
- **Tests** : boot superadmin — `/enseignant` 200 (recherche + fiche peuplée : identité, heures+totaux, séances A3, exception E3), introuvable, `/enseignant/<m>/imprimer` 200 (paysage), `/etudiant/<m>/imprimer` 200, deep-link `?modifier=` OK, non-régression tableau de bord / E1 / A3 / impressions 200, zéro emoji.

## Ce qui change en V1.72 (refonte UX : menu regroupé, masquage par droits, accueil en tuiles)

> **AUCUNE modification du classeur.** Refonte purement IHM à partir des routes existantes (TDR), validée écran par écran avec B. Léglise.

- **Menu de gauche en 6 groupes** (Pilotage / Scolarité / Enseignants / Ressources / Finances / Administration) par réécriture de `GUIDE_STRUCTURE` (`config.py`). **Aucune route perdue** (self-test : ensemble des clés de module identique). Modules hors-TDR (Examens, Diplômes, Qualifications, Indemnités, Non-conformités, Audits, Conflits) **sortis du menu**, routes conservées.
- **Masquage par droit de lecture** : `MODULES_CACHES` calculé au `context_processor` (`est_admin` → rien de masqué ; sinon onglets gouvernés non lisibles via `peut_lire`). `base.html` masque les modules cachés et les groupes/sections devenus vides. Pseudo-pages toujours visibles.
- **Accueil en tuiles** : `accueil.html` remplace le répertoire central par 6 grandes tuiles gardées par les droits, bandeau KPI conservé.
- **Méthode** : 4 touches validées une par une — A (`config` GUIDE), B (`app` + `base.html`), C (`accueil.html`), D (docs + VERSION 1.72).
- **Lot** : `config.py` (VERSION 1.72, GUIDE 6 groupes), `app.py`, `templates/base.html`, `templates/accueil.html`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.
- **Tests** : `py_compile` OK ; self-tests A/B/C/D au vert ; smoke-test Flask (login superadmin) — accueil 200 avec tuiles, menu rendu, module 200. Classeur **non touché**.

## Ce qui change en V1.71 (bandeau de filtres multicritère + impression de la sélection)

> **AUCUNE modification du classeur** (maître `EMSP_V1_MAITRE_V1_70.xlsx` inchangé, md5 `c44c7864d256a436315a0d1538add70e`, 16 dessins / 30 onglets). Chantier b : un bandeau de filtres commun + l'impression de la sélection courante, **par le navigateur** (pas de WeasyPrint).

- **Bandeau de filtres commun** (`_bandeau_filtres.html`) en tête des pages module et du tableau de bord : **Filière / Niveau / Année académique / Période (Du–Au, JJ/MM/AAAA)**. Chaque contrôle est masqué quand l'onglet ne le supporte pas (`bandeau.supporte`) ; bandeau entièrement masqué sur `P0_Parametres` et les onglets de référence.
- **Option B** : année et période filtrent finances et heures ; **seuls filière et niveau** grisent les cartes financières du tableau de bord (non ventilables par filière/niveau). Sans filtre, comportement **identique** aux versions antérieures (rétro-compatible).
- **Impression de la sélection** par le **navigateur** (`window.print()` → Enregistrer en PDF) : bouton « Imprimer cette sélection » (`formaction` + `formtarget=_blank` emporte les filtres) → page **autonome paysage** (`@page A4 landscape`, `.doc-page.paysage`), en-tête Université des Comores / EMSP + date + rappel de la sélection ; modes **module** (table) et **dashboard** (table KPI, KMF sans décimale). `templates/impression_selection.html`.
- **Décision verrouillée** : impression = **navigateur**, pas WeasyPrint (zéro dépendance native à vendoriser).
- **Méthode** : chantier livré en **3 touches** validées une par une — Touche 1 `app.py` (1613 lignes, md5 `2d11bb3da6c24d46303250cc52fd8b03`, 15/15), Touche 2 templates (20/20), Touche 3 docs + bump VERSION (la présente).
- **Lot code** : `config.py` (VERSION 1.71), `app.py` (`_lire_filtres`, `_bandeau_dashboard`, routes `/module/<onglet>/imprimer` + `/tableau-de-bord/imprimer`, `/api/dashboard` filtré), `templates/_bandeau_filtres.html` + `templates/impression_selection.html` (nouveaux), `templates/module.html` + `templates/tableau_bord.html` (include + option B), `README.md`, `doc/doc_des_ecrans.md`, `CONSIGNES_LIVRAISON.md`, `ETAT.md`.
- **Tests** : `py_compile` 5 modules OK ; T1 15/15 et T2 20/20 (rendus Flask réels, sessions précédentes) ; patch docs idempotent (md5 stables au 2ᵉ passage). Classeur **non touché** (md5 inchangé).

## Ce qui change en V1.70 (budget compta : prévu / réalisé / écart + taux de change)

> **Comparatif budgétaire sans double stockage.** Le « prévu » vit dans le nouvel onglet `F3_Budget_poste` ; le « réalisé » est agrégé depuis `F1_Mouvements` par poste (calcul Python, **année civile**). Les taux de change de référence vivent dans `P2_Taux`. Ces deux onglets, attendus depuis V1.58 mais **absents du maître à 28 onglets** (régression d'une reconstruction ancienne), sont (re)créés et câblés ici.

- **Chirurgie ZIP du maître** (16 dessins préservés) : ajout de `F3_Budget_poste` (sheet29) et `P2_Taux` (sheet30). 28 → **30 onglets**. **Nouveau md5 canonique : `c44c7864d256a436315a0d1538add70e`** (depuis `ff60d30ed29e75c6281bc6d32a9bced8`, V1.69). Script `scripts/chirurgie_V1_70.py` (idempotent, autres membres recopiés, sharedStrings : 4 chaînes neuves, jamais de mutation). `P2_Taux` **semé EUR = 491,967** (parité fixe) au 01/01/2026.
- **Copie déployée** mise à niveau (F3 + P2, EUR semé) par `scripts/migration_copie_V1_70.py` (idempotent, openpyxl ; la copie déployée n'a pas de dessin).
- **Liste partagée renommée** : `Bailleurs (*)` → **`Sources_financement (*)`** en `P0_Parametres` (col O), valeurs **AFD / Etat comorien / Ressources propres EMSP / Autres donateurs**. Liste **unique** partagée `F1` / `M1` / `F3` (surcharge Dictionnaire, classeur non remué côté libellés des onglets de saisie).
- **`F3_Budget_poste` (budget par poste, prévu)** : Exercice · Poste budgétaire (liste `Postes_budgetaires`) · Filière (**optionnelle**) · Sens (Recette/Dépense) · Source de financement (liste `Sources_financement`) · Montant budgété (KMF) · Observations · Saisi par (auto). Saisissable (menu **Finances & pilotage**), réservé au **droit financier**. Budget rattaché au **poste** ; la filière reste facultative.
- **`P2_Taux` (taux de change, références)** : Devise · Code · Taux en KMF · Date d'effet · Observations. EUR = 491,967 KMF (parité fixe) pré-semé ; USD et autres **laissés à l'EMSP**. Saisissable (menu **Paramétrage**, Direction). `metier.taux_change('EUR')` = 491.967.
- **Édition « Budget : prévu / réalisé / écart »** (`/impressions`, carte dédiée + sélecteur d'exercice) : comparatif par poste **Prévu** (F3) / **Réalisé** (F1, année civile) / **Écart** / **Taux de réalisation**, en paysage (`/impressions/etat-poste?exercice=AAAA`). Le réalisé est raisonné en **année civile** (cohérent avec la clôture compta). Couverture sanitaire (658b) **hors réconciliation**.
- **Action sur installation déployée** : lancer une fois `python scripts/migration_copie_V1_70.py` (idempotent ; `donnees` non écrasé) ; sur le **maître** du projet, `python scripts/chirurgie_V1_70.py` (chirurgie ZIP, dessins préservés, md5 re-scellé). Le kit V1.70 livre la copie déjà migrée.
- **Lot code** : `config.py` (VERSION 1.70 ; F3 au menu Finances & pilotage + `ONGLETS_FINANCIERS` ; P2 au menu Paramétrage + `ONGLETS_DIRECTION` ; les deux dans `ONGLETS_SAISIE_ACTIVE` ; Dictionnaire F3/P2 ; surcharge F1/M1 « Source de financement / Bailleur » → `Sources_financement` ; `CHAMPS_AUTO_LOGIN` F3), `metier.py` (`taux_change`, `budget_par_poste`, `_realise_par_poste`, `_sens_par_poste`, `etat_poste_budget`), `app.py` (route `/impressions/etat-poste` avec paramètre `exercice` → comparatif budget ; filtre bailleur des vues rebranché ; `annee_civile` au hub impressions), `templates/impressions.html` (carte budget), `scripts/chirurgie_V1_70.py`, `scripts/migration_copie_V1_70.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.
- **Tests** : `py_compile` 5 modules ; boot Flask (client superadmin) — `/module/F3_Budget_poste` et `/module/P2_Taux` 200, `/impressions` carte budget présente, `/impressions/etat-poste?exercice=2026` Prévu/Réalisé/Taux, `/requetes/vue/equip_loc` + `equip_bailleur` 200 (filtre rebranché), **non-régression M1 et F1** 200, F3/P2 au menu d'accueil ; `taux_change('EUR')`=491,967 ; `options_liste('Sources_financement')`=4 libellés ; `options_liste('Bailleurs')`=None. Maître : 30 onglets / **16 dessins** (md5 `c44c7864…`). Le maître du projet **reste V1.69** tant que V1.70 n'est pas validé à l'usage.

## Ce qui change en V1.69 (suivi des droits d'inscription par étudiant)

> **Vue dérivée de `F1_Mouvements`, sans double stockage.** Le « Payé » est agrégé depuis F1 (calcul en Python). Les tarifs sont lus dans P0 (colonnes appariées, éditables), jamais en dur.

- **Chirurgie ZIP du maître** (16 dessins préservés, md5 `ff60d30ed29e75c6281bc6d32a9bced8`) : `F1_Mouvements` + colonnes `Matricule` (18) et `Annee academique (*)` (19) ; `P0_Parametres` + colonnes `Tarif_inscription_niveau` (26) et `Tarif_inscription_KMF` (27). Script `scripts/chirurgie_V1_69.py` (idempotent, autres membres octet pour octet). Base = maître 16 dessins du projet (`EMSP_V1_MAITRE_16DESSINS.xlsx`).
- **Copie déployée** mise à niveau (4 colonnes) + **tarifs semés** L1 = 70 000 / L2 = 70 000 / L3 = 80 000 KMF via `scripts/import_tarifs_inscription.py` (idempotent, openpyxl). Tarifs **entièrement éditables** par l'EMSP dans Paramètres.
- **Bloc « Droits d'inscription »** sur la fiche `/etudiant` (lecture seule pour scolarité/direction) : **Dû** (tarif du niveau), **Payé** (somme F1 Recette filtrée par matricule + poste 706 du niveau courant + année académique), **Reste dû**, détail daté des versements. Niveau hors grille (Master, formation continue, AS) → **« Tarif non défini »** avec pointeur vers P0.
- **Mini-écran `/etudiant/<matricule>/encaisser`** (écriture réservée au **droit financier**, bloqué sur poste secondaire, journalisé) : pré-remplit Date = aujourd'hui, Sens = Recette, Poste = 706 du niveau, Montant = reste dû (éditable), Matricule, Tiers, Année académique (reprise de la fiche, éditable via liste `Annees_acad`). **Compte / caisse** et **Mode de paiement** obligatoires (rattachement caisse + solde) ; **Catégorie laissée vide** → complétée par la comptabilité dans `/tresorerie`.
- **Lien personne = matricule ; lien niveau/année = poste 706 + année académique** : un redoublant voit ses versements isolés par niveau (L1 sur 706b ≠ L2 sur 706c). Pré-inscription (706a) et formation continue (706e) **hors** de ce suivi (frais distincts) ; couverture sanitaire (658b) hors rapprochement.
- **Action sur installation déployée** : lancer une fois `python scripts/import_tarifs_inscription.py` (idempotent ; `donnees` non écrasé). Le kit V1.69 livre colonnes + tarifs déjà chargés.
- **Lot code** : `config.py` (VERSION 1.69, `POSTE_INSCRIPTION_PAR_NIVEAU`, Dictionnaire F1 Matricule/Année), `metier.py` (`tarifs_inscription`, `droits_inscription`, `enregistrer_encaissement`), `app.py` (route `/etudiant` enrichie + `etudiant_encaisser` GET/POST), `templates/etudiant.html` (panneau Droits), `templates/encaisser.html` (nouveau), `scripts/chirurgie_V1_69.py`, `scripts/import_tarifs_inscription.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## Ce qui change en V1.68 (Brique 0 — listes compta opérationnelles)

> **Données, pas structure** : écriture openpyxl sur la **copie déployée** (donnees/data), aucune chirurgie. La colonne « Solde courant » de F2 (formule SUMIF protégée) n'est jamais touchée.

- **Listes compta de `P0_Parametres` alimentées** (elles étaient vides → écran trésorerie / saisie F1 inopérants) : `Cat_Recettes` (3 chapitres : 70, 74, 13), `Cat_Depenses` (10 chapitres : 60, 61, 62, 64, 65, 66, 67, 16, 20, 21), `Postes_budgetaires` (60 articles + sous-articles, recettes & dépenses confondues, format « code — intitulé », codes OCR `617 (sorties)` / `625 (récep.)` / `626 (tel.)` et suffixes conservés tels quels). Source figée : `scripts/listes_compta_data.json` (depuis `Nomenclature_budgetaire_EMSP.xlsx`).
- **Comptes réels pré-renseignés** dans `F2_Comptes` : « Compte bancaire UDC-EMSP-ODS (BIC-Comores) » (Banque) et « Caisse EMSP » (Caisse) ; **soldes initiaux laissés vides** (à saisir par la compta) ; solde courant = formule protégée intacte.
- **Vérifié** : `metier.options_liste` résout la catégorie F1 (13 options = 3 recettes + 10 dépenses), les postes (60) et la liste compte/caisse (2). L'écran `/tresorerie` et la saisie `F1_Mouvements` sont désormais opérationnels.
- **Script idempotent** : `scripts/import_listes_compta.py` (+ `listes_compta_data.json`), rejouable sans doublon (upsert F2 par nom).
- **Action sur installation déployée** : exécuter une fois `python scripts/import_listes_compta.py` (le classeur `donnees/data/EMSP_V1.xlsx` n'est pas écrasé par une mise à jour). Le kit V1.68 livre déjà les listes alimentées.
- **Maître de référence retrouvé et remis à niveau** : l'utilitaire `scripts/trouver_maitre.py` (repère le maître = 28 onglets + dessins parmi tous les `.xlsx`) a identifié le maître à 16 dessins en **ex-V55**. Remis à niveau V1.67 par chirurgie de la colonne Quantité M1 (16 dessins préservés, md5 `7e81532e33eadb3ae022f4c83cca5c59`). C'est le maître de référence pour la suite.
- **Dépôt Git abandonné** : livraisons désormais par archives ZIP. À consigner dans `CONSIGNES_LIVRAISON.md`.

> **À venir — V1.69 (suivi paiement par étudiant, dégroupé pour tenir un cycle propre)** : chirurgie colonne `Matricule` sur `F1_Mouvements` + deux colonnes appariées de tarifs (`Tarif_inscription_niveau` / `Tarif_inscription_KMF` : L1 70 000 / L2 70 000 / L3 80 000) sur `P0_Parametres` ; vue dérivée Dû / Payé / Reste dû sur `/etudiant` (mouvements recette F1 postes 706b/c/d filtrés par matricule) ; mini-écran d'encaissement pré-remplissant le mouvement F1. **Couverture sanitaire (2 500 KMF) hors rapprochement** (pas de poste recette dédié ; `658b` est une dépense).



> Le classeur maître EMSP_V1.xlsx porte 16 dessins : l'ajout de colonne se fait par **chirurgie ZIP** (jamais openpyxl.save sur le maître). Le seed de données se fait par openpyxl sur la **copie déployée** (donnees/data), comme l'import des élèves.

- **Colonne `Quantité`** ajoutée à `M1_Equipements` : sur le maître via `scripts/ajout_quantite_M1.py` (chirurgie ZIP, dessins préservés, md5 re-scellé, idempotent) ; sur la copie déployée, ajoutée automatiquement par l'import openpyxl.
- **Import de l'inventaire** : `scripts/import_equipements.py` + `scripts/equipements_data.json` (figé depuis les inventaires EMSP : répartition par bureau et par salle). **280 articles**, somme des quantités ≈ 1412, sur 24 emplacements. Une ligne par article, avec sa quantité ; n° d'inventaire = matriculation `UDC/EMSP/…` ; état repris de l'observation ; date d'acquisition reportée telle quelle (souvent une année). Idempotent.
- **Laissés vides, à affecter depuis la compta** : `Montant`, `Source de financement / Bailleur`, `Référence / N° pièce`, `Catégorie`. C'est le point d'accroche **Patrimoine ↔ Compta** : un équipement = une dépense affectée à un poste budgétaire (605 / 605A / 21…) et à un financement (AFD/dons/État), reliée à `F1_Mouvements` par la `Référence / N° pièce` ; les entrées AFD/dons = recettes affectées (74). Les dérives = écart budget prévu vs réalisé.
- **Action sur installation déployée** : exécuter une fois `python scripts/import_equipements.py` (le classeur `donnees/data/EMSP_V1.xlsx` n'est pas écrasé par une mise à jour) ; et `python scripts/ajout_quantite_M1.py <…\EMSP_V1.xlsx>` sur le **maître** du dépôt. Le kit V1.67 livre déjà l'inventaire chargé.

### À retenir (acquis non encore intégrés au code)
- **Coefficients** : les relevés réels 2024-2025 (`Sess1_*`) montrent des Coef UE différents des maquettes (réf. `Recoupement_coefficients_barème_EMSP`). Référence à privilégier = relevés réels ; arbitrage scolarité.
- **Modèle de relevé officiel** : colonnes `Matières | CC | Examen | Moyenne | Coef | ECTS` ; moyenne UE = moyenne arithmétique ; décision annuelle = moyenne des deux semestres, « Admis en 1ère session » au seuil de 10.
- **Aides-soignants** : aucun barème fourni → bulletins AS non réalisables ; barème (UE/matières, coef, ECTS, règles) à réclamer à la scolarité.
- **Nomenclature recette/dépense** disponible (`Nomenclature_budgetaire_EMSP`) ; note de procédure révisée (`Procedure_developpement_EMSP_revisee`).

## Ce qui change en V1.66 (validation des coefficients du barème)

> **Décision (23/06/2026) : on valide les coefficients indiqués au barème ; les erreurs éventuelles seront corrigées ensuite par la scolarité.** `Coef confirmé` passe de « Non » à **« Oui »** sur les **642 matières** de `N1_Bareme_UE`. Effet : le bandeau **« Barème provisoire »** disparaît du bulletin et du relevé. Données dans `EMSP_Notes.xlsx` (aucun dessin → `openpyxl.save`, pas de chirurgie). Lot code : `config.py` (VERSION 1.66), `scripts/confirmer_coefficients.py` (nouveau, idempotent), `scripts/import_bareme.py` (semis désormais en « Oui »), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **À faire sur une installation déjà déployée** : exécuter une fois `python scripts/confirmer_coefficients.py` (le classeur de données `donnees/data/EMSP_Notes.xlsx` n'est jamais écrasé par une mise à jour). Le kit V1.66 livre déjà le barème confirmé.
- **Recoupement avec les 3 documents officiels** (`Licence imagerie médicale crédits coefficients`, `Licence Technicien maintenance biomédical`, `Maquettes Formation S.I et S.O`) : **non réalisé** — ces fichiers ne sont pas accessibles (ni disque, ni index projet). À refaire si Bernard les réattache en lisible.
- **Anomalies laissées à la scolarité** (non corrigées) : 1 UE sans ECTS ; une UE à coef 0 (ne pèse pas dans la moyenne semestre) ; des UE à coef 11 et 12 (inhabituel). Filière Aides-soignants absente du barème (hors LMD).

## Ce qui change en V1.65 (saisie façon bulletin)

> **AUCUNE modification de structure du classeur.** Écriture de données uniquement : upsert `N2_Notes`. Lot code : `config.py` (VERSION 1.65, menu `BUL_Saisie`, `SPECIAL_ROUTES`), `metier.py` (`semestres_classe`, `_n2_par_session`, `bulletin_saisie`, `_note_valide`, `enregistrer_bulletin`), `app.py` (`/bulletin`, `/bulletin/enregistrer`), `templates/bulletin_saisie.html` (nouveau), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Principe** : un étudiant → sa grille de bulletin (UE → matières du barème `filière+niveau+semestre`). Examen saisi, **CC affiché** : dérivé des contrôles `N4` (lecture seule, N4 prime) sinon saisissable. Moyennes **en direct** côté client : matière = ¼ CC + ¾ examen ; UE = moyenne arithmétique des matières ; semestre = UE pondérées par `Coef UE` ; mention et proposition Admis/Ajourné (indicative, délibération manuelle) ; ECTS acquis.
- **Sélection** : recherche par **matricule** (autocomplétion hors-ligne), Année (défaut `2025-2026`), Semestre (semestres du barème pour la classe), Session 1 / 2. En session 2, la grille pré-remplit les notes de session 2 déjà saisies et affiche la **session 1 en référence**.
- **Écriture** : upsert `N2_Notes` (clé `Matricule + Année + Session + Semestre + N° UE + Matière`) **uniquement pour les matières renseignées** (CC manuel ou Examen saisi) ; le CC dérivé de `N4` n'est pas réécrit dans `N2`. Notes validées dans `[0..20]`.
- **Droits** : réservé au droit d'écriture `N2_Notes` (403 sinon), bloqué sur poste secondaire, journalisé.
- **Placement** : cartes `.panel` centrées, grille `table.data` ; aucun chevauchement avec le menu.

## Ce qui change en V1.64 (présences en liste — séance ad hoc, option B)

> **AUCUNE modification de structure du classeur.** Écriture de données uniquement : lignes `A2_Presences` (upsert) et, en option, une ligne `A3_Sessions` créée à la volée. Lot code : `config.py` (VERSION 1.64, entrée de menu `PRESL_Libre`, `SPECIAL_ROUTES`), `metier.py` (`classes_en_service`, `roster_classe`, `cle_session_libre`, `_prochain_id_session`, `creer_session_recurrente`, `_jour_de_date`, `_annee_acad_defaut`, `presences_existantes_libre`, `enregistrer_presences_libre`), `app.py` (`/presences/libre`, `/presences/libre/enregistrer`), `templates/presences_libre.html` (nouveau), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Principe (option B)** : aucun emploi du temps requis. On choisit la **classe** (Filière + Niveau, Section si renseignée), la **date**, l'**heure début/fin**, la **matière** (barème/maquette) et l'**enseignant** (liste `E1`) ; le **roster** vient de `A1` ; on coche les présents (non coché = absent) ; re-saisie = correction (upsert par personne autorisée).
- **Créneau** = plage `HH:MM-HH:MM` stockée dans `A2_Presences` (et non plus un créneau prédéfini).
- **Clé `A2` « Session / Matière »** : clé composée lisible `Filière Niveau - Matière - Enseignant`. Si « **enregistrer comme récurrente** » est coché, une ligne `A3_Sessions` est d'abord créée (ID `Sxxx`, jour déduit de la date) et son **ID** devient la clé `A2`.
- **Salle** : champ libre optionnel (lien `L2_Reservations` = candidat V2, non développé).
- **Droits** : écran réservé au droit d'écriture `A2_Presences` ; la création `A3` exige en plus le droit `A3_Sessions` (sinon case désactivée). Bloqué sur poste secondaire (lecture seule), journalisé.
- **Placement** : cartes `.panel` dans la colonne centrale, formulaire compact, sélecteurs Filière→Niveau→Section en cascade (hors-ligne) ; aucun chevauchement avec le menu de gauche.
- **Coexistence** : l'écran « séance libre » complète l'écran séance-first (`/presences`), qui reste la cible quand `A3_Sessions` sera peuplé (option A).

## Ce qui change en V1.63 (dépôt de photo sur la fiche étudiant)

> **AUCUNE modification du classeur.** La photo est un **fichier image** (`donnees/photos/<matricule>.jpg`), hors classeur et hors dépôt. Lot code : `config.py` (VERSION 1.63, `PHOTO_MAX_OCTETS = 1 Mo`), `metier.py` (`chemin_photo`, `photo_servie`, `enregistrer_photo`, `supprimer_photo`, `_type_image`, `_photo_existe` réécrit), `app.py` (`/etudiant/photo/<matricule>/televerser`, `/etudiant/photo/<matricule>/retirer`, route d'affichage qui détecte le type aux octets, passage de `peut_modifier` au template), `templates/etudiant.html` (bloc d'upload), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Emplacement** : sous la photo, dans la carte d'identité `.panel` (colonne centrale, `margin:0 auto`). Flux normal, aucun `position:absolute/fixed` : pas de chevauchement possible avec le menu de gauche (sidebar = colonne flex distincte de 286 px).
- **Bouton « Choisir une photo… » / « Changer la photo »** : ouvre le sélecteur de fichier ; au choix du fichier, le formulaire se soumet automatiquement (un seul clic).
- **Bouton « Retirer la photo »** (rouge) : présent uniquement si une photo existe ; confirmation avant suppression.
- **Formats** : JPEG et PNG, détectés par **signature binaire** d'en-tête (pas de ré-encodage, aucune dépendance binaire ajoutée — wheelhouse PyPI officiel inchangé). Enregistrement sous le nom canonique `<matricule>.jpg` ; à l'affichage, un PNG est servi en `image/png`, le reste en `image/jpeg`. Tout autre format est refusé avec un message clair.
- **Taille** : 1 Mo maximum, vérifiée dans la route (lecture bornée à 1 Mo + 1 octet, pas de `MAX_CONTENT_LENGTH` global).
- **Garde** : action réservée au droit d'**écriture sur `A1_Etudiants`** (sinon 403 ; bouton masqué) ; **bloquée sur poste secondaire** (lecture seule) ; **journalisée** (`Photo etudiant` / Televersement / Retrait). Écriture fichier uniquement, jamais le classeur.
- Vérifié (copie jetable) : upload JPEG → `image/jpeg`, remplacement par PNG → `image/png`, refus format et refus >1 Mo, retrait → placeholder portrait, journal alimenté.

## Ce qui change en V1.62 (correctif affichage fiche étudiant)

> `templates/etudiant.html` : la classe `.bloc` utilisée existe en double dans `style.css` — l'une est la carte standard, l'autre (chargée) est le **bloc de planning** (`position:absolute; fond bleu; texte blanc`). Résultat : fiche en bleu plein, illisible, débordant sous le menu. **Corrigé** : cartes `.panel`/`.ph`/`.pb` (fond blanc, contenu dans la colonne centrale), table `.data` pour les stages. `config.py` VERSION 1.62. Vérifié : 3 panels, 0 `.bloc`, rendu lisible.

## Ce qui change en V1.61 (fiche étudiant + recherche par matricule)

> **AUCUNE modification du classeur.** Lot code : `config.py` (VERSION 1.61, `PHOTOS_DIR`, `PAGES_REF`/`SPECIAL_ROUTES`/menu `ETU_Fiche`), `metier.py` (`recherche_etudiants`, `fiche_etudiant`, `stages_etudiant`, `_photo_existe`), `app.py` (`/etudiant`, `/etudiant/photo/<matricule>`), `templates/etudiant.html` (nouveau), `README.md`, `ETAT.md`.

- **Écran** (menu Étudiants, en tête) : recherche par **matricule** ou **nom** via une saisie + datalist hors-ligne (« matricule — Nom Prénom (filière niveau) »), pas de longue liste ; bouton « Afficher la fiche » ; sélection dans la liste = soumission directe (JS extrait le matricule du libellé).
- **Fiche** : identité A1 (Matricule, Genre, Nom, Prénom, naissance, origine, filière, niveau, section, année, statut, date inscription) + **photo** ; liens vers relevé (pré-rempli), présences, stages ; **stages de l'étudiant** listés depuis S1.
- **Photos** : `donnees/photos/<matricule>.jpg` ; placeholder portrait SVG `#1F4E79` si absente. Dossier `donnees/photos/` prêt dans le kit (avec LISEZMOI).
- **Composant recherche** réutilisable (même `recherche_etudiants()`) → à brancher sur la **sélection élève des stages** (prochaine étape).
- **Tests (client authentifié, copie peuplée)** : `/etudiant` 200 (562 options) ; fiche 74180 = ABASSE / Soins infirmiers + liens + stages ; doublon `73395b` (Imagerie) OK ; photo placeholder SVG ; introuvable → message ; `py_compile` OK.
- **Reste à faire (validé)** : recherche élève dans stages ; **présences par séance en liste** (séances par défaut heure par heure regroupables, cocher la présence ; matière + enseignant rattachés → double usage feuille de présence enseignant pour la paie) ; **roster CC** et **roster examens** (saisie en liste façon bulletin, upsert/correction) ; saisie des notes façon bulletin ; coefficients officiels ; doublon 73395 ; `FORMATION_MAX`.



## Ce qui change en V1.60 (écrans de saisie compacts)

> **AUCUNE modification du classeur.** Lot code : `config.py` (VERSION 1.60, `LARGEURS_CHAMPS`, défauts A1), `metier.py` (`_prochain_ordre`, largeur par champ dans `champs_saisie`), `templates/module.html`, `static/css/style.css`, `README.md`, `ETAT.md`.

- **Constat** : formulaire générique en grille `minmax(220px,1fr)`, label au-dessus → champs trop larges (Genre 1 car., Matricule, N° d'ordre), identité sur plusieurs lignes, saisie lente.
- **Refonte** : `.saisie-grid` passe en **flex-wrap**, chaque champ dimensionné à son **nombre de caractères** via `style="--w:<n>ch"` (largeur = `LARGEURS_CHAMPS[libelle]`, sinon auto par type/options ; input `width:calc(var(--w)+26px)`). Identité A1 sur une ligne.
- **Saisie par matricule** : `N ordre` pré-suggéré (`@next_ordre` = max+1) et modifiable ; report `@last` du contexte A1 (filière/niveau/section/année/statut). `metier._prochain_ordre`.
- **Portée** : un seul formulaire générique → corrige A1, N1, N2, N3, N4 et les autres onglets simultanément. Largeurs définies pour les champs de ces écrans.
- **Fiche de présence** : opérationnelle dès A1 peuplé (effectif tiré par Filière+Niveau ; Section ignorée car vide) ; nécessite des séances dans A3.
- **Tests** : `champs_saisie("A1")` renvoie les largeurs attendues (Genre 4, Matricule 10, dates 12, N ordre 6, auto = 101) ; `py_compile` config/metier/app OK.
- **Reste à faire (confirmé séparément)** : écran de saisie des notes **façon bulletin** (Nota important) ; affinage écran par écran sur la base des états de sortie ; coefficients officiels du barème ; doublon 73395 ; `FORMATION_MAX`.



## Ce qui change en V1.59 (chargement des élèves et des filières — données réelles)

> **Données chargées dans la copie de PRODUCTION** (`donnees/data/EMSP_V1.xlsx`, via openpyxl = voie d'écriture de l'IHM ; **master template figé non touché**, ses 16 dessins restent dans le template). Nouveaux fichiers : `scripts/import_eleves.py` + `scripts/eleves_data.json`. Lot code : `config.py` (VERSION 1.59), `templates/base.html`, `README.md`, `ETAT.md`.

- **562 élèves** dans `A1_Etudiants` + **5 filières** dans `P0_Parametres`. Répartition : Soins infirmiers L1/L2/L3 = 100/85/60 ; Soins obstétricaux L1/L2/L3 = 83/64/63 ; Imagerie médicale L1 = 57 ; Maintenance biomédicale L1 = 20 ; Aides-soignants = 30 (hors LMD, sans niveau). Source = listes définitives transmises (panneau projet).
- **Mapping** : Matricule, Nom, Prénom, Date naissance, Lieu naissance depuis les listes ; Filière + Niveau déduits du fichier ; Année `2025-2026` ; Statut `Inscrit` ; Genre/Section/Origine/Date inscription **vides** (à compléter via la fiche étudiant) ; Saisi par = `import`.
- **Doublon arbitré** : `73395` (HASSANI BAHADJATI) en Aides-soignants **et** Imagerie L1 → **deux lignes conservées** (`73395` / `73395b`), Statut `Doublon a arbitrer` sur les deux. À trancher : transfert, double inscription ou erreur.
- **Filière officielle** « Soins obstétricaux » (alias maquette « sages-femmes » → zone complémentaire à ajouter ultérieurement).
- **Formation (nouveau paradigme)** : mêmes données réelles qu'en production (fin du jeu fictif). Côté code je n'ai touché qu'au **liseré rouge** (texte adapté : plus de « données fictives »). Le liseré reste rouge (`#C0241F`, `.formation-banner`). Installation des dossiers formation/production = côté Bernard. **À noter** : `FORMATION_MAX = 50` déclenche une alerte non bloquante au-delà de 50 lignes — obsolète avec les données réelles ; à relever/retirer (non fait, hors périmètre demandé).
- **Tests (copie de prod)** : 562 lignes, comptages par filière/niveau exacts, idempotent ; doublon = `73395`/`73395b` marqués ; P0 Filieres = 5 libellés ; la couche data lit 562 élèves ; `etudiant_a1` résout filière/niveau (74180 → Soins infirmiers L1). `py_compile` OK.
- **Action côté prod** : `python scripts/import_eleves.py` sur le `EMSP_V1.xlsx` de production, ou déposer le classeur peuplé fourni dans `donnees/data/`.
- **Suite** : fiabilisation des coefficients du barème (fichiers officiels Licence imagerie / Licence maintenance / maquettes SI-SO → Coef confirmé Non→Oui) ; refonte des écrans de saisie en s'appuyant sur les états de sortie.



## Périmètre
Volet EMSP uniquement (GMAO écarté). V1 sur le seul périmètre TDR. CR du 11/06 et retours
terrain → candidats V2 (à spécifier après validation à l'usage).

## Ce qui change en V1.58 (restauration de la couche de lancement — kit exécutable)

> **AUCUNE modification du classeur.** Lot : `Demarrer_EMSP.bat`, `Demarrer_EMSP_RESEAU.bat`, `construire_socle.bat`, `LISEZMOI_INSTALLATION.txt`, `socle/wheelhouse/` (11 wheels) ; `config.py` (VERSION 1.58), `README.md`, `ETAT.md`. Couche `programme/` (code) inchangée hors numéro de version.

- **Constat (blocage signalé)** : impossible d'exécuter l'application depuis `emsp_interface_VXX.zip` — pas de `.bat` de lancement, pas de socle. Cause : cette archive ne contient que la **couche `programme/` (code)** ; le dépôt ne versionne jamais les binaires du socle ni, ici, les lanceurs (ils avaient disparu du jeu de fichiers fourni). **Aucun fichier n'a été supprimé par les lots précédents** : ces éléments ne figuraient simplement pas dans l'archive de code.
- **Rappel du modèle trois couches** (V1.53) : `socle/` installé une fois (Python embeddable + `wheelhouse/`), `programme/` remplacé à chaque mise à jour, `donnees/` jamais écrasé. `config.py` : `DONNEES_DIR = EMSP_DONNEES` ou dossier **frère** `donnees` de `programme/` (`os.path.dirname(BASE_DIR)/donnees`).
- **`Demarrer_EMSP.bat`** : `EMSP_DONNEES = <racine>\donnees` (déterministe) ; **socle prioritaire**, **repli automatique sur le Python 3.12 du système** (poste développeur) avec installation hors-ligne des dépendances depuis `socle\wheelhouse` ; ouvre le navigateur. **CRLF** (impératif cmd.exe).
- **`construire_socle.bat`** (une fois, Internet) : télécharge `python-3.12.x-embed-amd64.zip`, décommente `import site` dans `._pth`, **bootstrappe pip depuis son wheel** (`python.exe ...\pip-x.whl\pip install ...`), installe Flask/openpyxl/colorama depuis le wheelhouse. Reproduit les contraintes connues du Python embeddable (`._pth`, pip par wheel, colorama manuel).
- **`Demarrer_EMSP_RESEAU.bat`** : `EMSP_HOST=0.0.0.0`, ouverture best-effort du pare-feu (port 5000, profil privé), affiche l'IP (postes secondaires en lecture seule, garde-fous V1.54 inchangés).
- **Wheelhouse** : wheels **officiels PyPI** (aucun binaire issu de la clé USB du gestionnaire — rappel sécurité). CPython 3.12 / win_amd64.
- **Tests** : structure du kit montée (`programme/` + `donnees/` frères) ; chemins résolus ; bootstrap superadmin écrit `donnees/instance/comptes.json` ; `/login` → 200, `/` → 302 ; `.bat` vérifiés en CRLF. Kit livré **sans classeurs** (à déposer dans `donnees\data\` : `EMSP_V1.xlsx`, `EMSP_Notes.xlsx`) pour ne pas écraser tes versions à jour.
- **Action côté prod** : déposer les deux classeurs dans `donnees\data\` ; sur un poste neuf, lancer `construire_socle.bat` une fois ; puis `Demarrer_EMSP.bat`.

> **Correctif V1.58 (kit) — suite au 500 `FileNotFoundError`** : le premier kit V1.58 livré était **sans classeurs** dans `donnees\data\` → erreur 500 au premier accès (lecture de P1_Roles). Kit **reconstruit autour du socle hors-ligne éprouvé** (repris du `Kit_EMSP_hors_ligne_V1_50_OK` : `socle/runtime/` avec dépendances pré-installées, lanceur `Demarrer_EMSP.bat` + `_lancer_emsp.py`). `donnees\data\` est désormais **peuplé** : `EMSP_V1.xlsx` (28 onglets, gabarit) + `EMSP_Notes.xlsx` préparé (N1 barème arbitré 642 lignes + N4_Controles ajouté). `_lancer_emsp.py` fixe `EMSP_DONNEES=<kit>\donnees`. **Testé** : `metier.roles()` lit P1_Roles (5 rôles), `/login` 200, `/` 302, barème 642 lignes. Plus de `construire_socle.bat` (socle déjà prêt). **Nouveau document permanent `CONSIGNES_LIVRAISON.md`** (racine du dépôt) : règles de packaging/livraison à respecter pour toute version (deux formats MAJ/KIT, contenu obligatoire d'un kit, test de livraison avant zip, pièges connus) — pour que l'incident ne se reproduise plus.

> **Correctif lanceur V1.58 — `ERR_CONNECTION_REFUSED` au démarrage** : le `.bat` ouvrait le navigateur **avant** que Flask soit lié au port (chargement de `metier.py` ~1–2 s) → connexion refusée à l'ouverture (un simple **Actualiser** suffisait alors). Corrigé : `Demarrer_EMSP.bat` ne pré-ouvre plus le navigateur ; `_lancer_emsp.py` **attend que le port 5000 réponde** (poll socket, thread démon) puis ouvre le navigateur. Validé (poll : pas d'ouverture sans serveur, ouverture dès le bind). Piège ajouté aux `CONSIGNES_LIVRAISON.md`. Fichiers à remplacer dans le kit : `Demarrer_EMSP.bat` + `_lancer_emsp.py`.

## Ce qui change en V1.57 (barème arbitré importé + support de formation)

> **Modification du classeur des NOTES uniquement** (`EMSP_Notes.xlsx`, **sans dessin** → `openpyxl.save`, **pas de chirurgie zip**) : réécriture intégrale de l'onglet **`N1_Bareme_UE`** depuis le barème arbitré. Nouveaux fichiers : `scripts/import_bareme.py` + `scripts/bareme_data.json`. **`EMSP_V1.xlsx` non touché**. Lot code : `config.py` (VERSION 1.57), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Source** : `BL_Bareme_UE_a_valider_EMSP_260622.xlsx` (arbitré par BL « en attendant corrections officielles »), 4 filières (Soins infirmiers, Soins obstétricaux, Imagerie médicale, Maintenance biomédicale ; **AIDES SOIGNANTS absent**). Figé en JSON auto-contenu, l'import ne dépend plus du .xlsx d'origine.
- **Transformations** : 1 ligne par **matière** (éclatement « ; » + nettoyage des puces « - ») ; **S1–S6 → 1–6** ; **Coef = corrigé sinon maquette** ; **Coef confirmé = Non** partout (provisoire). Le « Coef UE corrigé » était quasi vide → reprise du « Coef (maquette) » telle quelle, conforme aux instructions du tableau.
- **Doublons d'UE déjà suffixés à la source** par BL (UE18/UE18b en L2-S3, UE49/UE49b en L3-S6) → chargés tels quels, **aucun suffixe ajouté** à l'import. UE16 en L1-S2 et L2-S3 ne sont pas un doublon (semestres distincts).
- **Supersession** : `import_bareme.py` **remplace `seed_bareme.py`** comme source de N1. Conséquence à connaître : la numérotation des UE suit désormais **les maquettes** (différente de l'ancien seed L2 SI aligné sur RELEVE_NOTES.pdf, qui était « confirmé ») ; tout repasse en **provisoire** jusqu'à validation scolarité. Repasser une UE en « Oui » (Coef confirmé) est une édition d'une cellule, recalcul immédiat.
- **Tests (copie peuplée)** : **642 lignes matières**, 4 filières, import **idempotent**, **0 collision** de clé (filière, niveau, semestre, N° UE, matière) ; `_bareme_ues` renvoie les UE attendues (Imagerie L1 S1 = 6 UE ; Soins inf. L2 S3 contient UE18 **et** UE18b). `py_compile` du script OK.
- **Support de formation** : `Support_formation_saisie_notes_EMSP.docx` (charte EMSP : Calibri, #1F4E79, sans emoji) — chaîne barème → contrôles continus (CC déduit) → examen → calcul → relevé, ordre de saisie, erreurs fréquentes, aide-mémoire. Pour la partie formation.
- **Action côté prod** : `python scripts/import_bareme.py` sur `EMSP_Notes.xlsx` (idempotent), puis vérifier l'écran Barème des UE.
- **Externe, non bloquant** : corrections officielles des coefficients et libellés par la scolarité (passage en « Coef confirmé = Oui »).

## Ce qui change en V1.56 (contrôles continus détaillés : CC dérivé + report des dernières valeurs)

> **Modification du classeur des NOTES uniquement** (`EMSP_Notes.xlsx`, séparé, **sans dessin** → `openpyxl.save` sûr, **pas de chirurgie zip**) : ajout de l'onglet **`N4_Controles`** via `scripts/ajout_N4_controles.py` (idempotent, rejouable sur prod peuplée, ne touche jamais les lignes existantes). **`EMSP_V1.xlsx` n'est pas touché** : md5 canonique inchangé, 28 onglets, 16 dessins. Lot code : `config.py` (VERSION 1.56), `metier.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Base de ce lot** : construit sur le **code V1.55** (ZIP livrable). Le chantier **COMPTA** (onglets `P2_Taux`/`F3_Budget_poste`, md5 `c81ec4c353bc76df5016d6d987783cb8`, `scripts/ajout_P2_F3_compta.py`) reste une **piste indépendante** dont la propagation de code est toujours en attente — non incluse ici, exactement comme au passation. Les deux chantiers ne se croisent pas (notes = classeur séparé).
- **`N4_Controles`** (saisie détaillée des contrôles) : Matricule, Année acad., Session, Semestre, N° UE, Matière, **N° de contrôle + Date** (clé du contrôle), Note /20, **Coef** (1 par défaut), Saisi par (auto-login). Provenance initiative `(*)`. Déclaré dans `ONGLETS_NOTES`, `MODULES_ONGLETS["Notes"]`, `ONGLETS_SAISIE_ACTIVE`, `DICTIONNAIRE_SUPPLEMENT`, Guide. Édition de ligne possible (corriger une note saisie).
- **CC dérivé** (`metier._cc_table`) : CC d'une matière = **moyenne pondérée** de ses contrôles N4 (coef 1 défaut). Branché dans `_notes_effectives` et `_notes_brutes`. **Repli** sur `N2.CC` manuel si aucun contrôle ; **N4 prime** si les deux existent. Onglet N4 absent (script pas encore joué) → `{}` → comportement V1.30 strictement préservé.
- **Report des dernières valeurs** (token `@last` / `@last|<repli>`, `metier._dernier_saisi`) : champs de contexte de `N4_Controles` et `N2_Notes` pré-remplis avec la dernière valeur saisie de la colonne ; replis à froid `2025-2026` (année), `@today` (date), `1` (session/coef/n° contrôle). Seuls Matricule et la note restent vides.
- **Tests (copies jetables peuplées)** : N4 créé + idempotent ; CC dérivé simple (=note), pondéré (16 & 10 → 13), repli N2.CC (=8) ; relevé semestre exact au centième (UE10 13,63 ; UE11 14 ; moy sem 13,91 « Assez bien » / Admis) ; bulletin affiche CC dérivé/repli ; `@last` reporte tout le contexte, replis corrects à froid (date = 23/06/2026) ; `py_compile` 5 modules + import `app.py` OK.
- **En attente (hors lot)** : import du barème `Bareme_UE_a_valider_EMSP_260622.xlsx` (éclatement des matières + suffixe **« b »** sur N° UE en doublon, appliqué à l'import par Webcreatys) — **nécessite le fichier barème** (non fourni). Désambiguïsation des doublons à faire **avant** saisie de masse.

## Ce qui change en V1.55 (heures constatées des enseignants : dérivées des appels)

> **Modification du classeur** (chirurgie du zip) : ajout de l'onglet **`E3_Seances_faites`**. Aucune feuille existante modifiée. 16 dessins et 669 formules **préservés**. 27 → **28 onglets**. **Nouveau md5 canonique : `4544adca513ab6a4b650c0376914d443`** (ancien `bfe96457b7f0dc7fac7041989d77c309`). Lot code : `config.py` (VERSION 1.55), `metier.py`, `app.py`, `templates/presences.html`, `templates/heures_constatees.html` (nouveau), `static/css/style.css`, `scripts/ajout_E3_seances_faites.py` (nouveau), doc.

- **Principe (intuition terrain)** : l'**appel des élèves atteste qu'une séance a eu lieu**. Les heures effectives d'un enseignant se **dérivent** donc des appels (`A2_Presences`) croisés avec le planning (`A3_Sessions`, qui donne l'enseignant programmé et la durée Heure fin − Heure début, à défaut le volume programmé). **Aucune saisie** pour une séance normale.
- **`E3_Seances_faites` = registre des EXCEPTIONS uniquement** : remplaçant, cours annulé, durée différente. Champs (provenance initiative `(*)`) : Date, Session/Matière (ID A3), Créneau, État (Assurée / Cours annulé), Assuré par (matricule ← E1), Matière réelle (← R1), Vol. constaté h, Motif, Saisi par. **Clé d'unicité** Date + ID séance + Créneau (UPSERT).
- **Comptage** : une séance comptée **une seule fois** par (Date, séance, créneau) quel que soit le nombre d'élèves appelés. « Cours annulé » exclut la séance ; un remplaçant attribue les heures à l'enseignant indiqué (et sa matière réelle).
- **Saisie de l'exception** : repliée dans l'écran d'appel (`presences.html`), sous le droit **Présences**. Écrite dans E3 **seulement** en cas d'écart réel ; revenir au cas normal **neutralise** la ligne (pas de doublon).
- **Écran « Heures constatées du mois »** (`/heures-constatees`, droit **Enseignants**) : par enseignant, heures calculées vs valeur E2 actuelle, statut (à reporter / identique / différent), détail des séances, liste des anomalies. Bouton **« Reporter dans E2 »** (UPSERT clé Mois+Matricule). **Garde-fou** : une valeur E2 corrigée à la main et différente du calcul **n'est jamais écrasée** sans **report forcé** explicite.
- **Chaîne paie inchangée** : E2 reste l'onglet stocké et la référence ; `releve_individuel` / `releve_recap` lisent E2.
- **Tests (copie jetable peuplée + client Flask)** : calcul juin conforme (Dupont 2 h ; Martin 4 h dont 1 séance reçue en remplacement) ; comptage unique (2 élèves → 1 séance) ; cours annulé exclu ; mois étranger exclu ; report E2 (création), divergence après correction manuelle, report **non** écrasé sans forcer, écrasé **avec** forcer. Routes GET 200 (`/presences`, `/heures-constatees`, `/module/E3_Seances_faites`), bloc exception pré-rempli (remplaçant pré-sélectionné), POST report 302, écriture/neutralisation E3 OK. Droits : Présences écrit E3 (pas E2) ; Enseignants reporte dans E2. **Classeur livrable vierge** (E3 = 0 ligne, E2 sans données).
- **Décision laissée ouverte (sans engagement)** : circuit de validation formel du chef de département — le report dans E2 fait office de validation pour l'instant.

## Ce qui change en V1.54 (multi-poste réseau câblé : lecture seule + voyant rouge)

> **AUCUNE modification du classeur.** Lot code : `config.py` (VERSION 1.54), `app.py`, `templates/base.html`, `static/css/style.css` + lanceur racine `Demarrer_EMSP_RESEAU.bat` + `LISEZMOI_RESEAU.txt`.

- **Modèle** : le **poste principal** (local) détient et **écrit** les données ; les **postes secondaires** se connectent par le réseau et sont **automatiquement en lecture seule** (consultation), avec **voyant rouge** « LECTURE SEULE ». Un seul poste écrit → pas de risque de corruption (le backend Excel ne supporte pas deux écrivains simultanés).
- **`app.py`** : écoute via `EMSP_HOST` (défaut `127.0.0.1` = mono-poste inchangé ; `0.0.0.0` = réseau). Garde-fou `before_request` : toute écriture (POST) d'un poste non-local est refusée (redirection + message), sauf l'authentification. Helper `_est_poste_local()` ; contexte `poste_secondaire`.
- **`base.html` + `style.css`** : bandeau rouge « LECTURE SEULE » sur les postes secondaires (distinct du bandeau formation).
- **Lancement** : `Demarrer_EMSP_RESEAU.bat` (poste principal) ouvre l'écoute réseau, tente d'ouvrir le pare-feu (port 5000, privé), affiche l'IP. Principal → `http://127.0.0.1:5000` (écriture) ; 2e poste → `http://<IP>:5000` (lecture seule). `Demarrer_EMSP.bat` reste mono-poste local.
- **Tests** : local → pas de voyant, écriture OK ; distant → voyant présent, POST d'écriture bloqué, **classeur inchangé** ; connexion distante possible.
- **Évolution possible (sans engagement)** : verrou d'écriture transférable (passer la main).

## Ce qui change en V1.53 (séparation données / code — structure du kit)

> **AUCUNE modification du classeur** (md5 `bfe96457b7f0dc7fac7041989d77c309` inchangé). Lot code + structure : `config.py` (VERSION 1.53, résolution des chemins), `formation/INSTALLER_FORMATION.bat`, `formation/REINITIALISER_FORMATION.bat`, doc.

- **Objectif** : qu'une mise à jour du programme = **remplacement complet du dossier `programme/`** sans jamais risquer les données, et qu'une réinstallation à blanc ne laisse **aucun reliquat**.
- **`data/` et `instance/` sortent de `programme/`** vers un dossier **frère `donnees/`** (à côté de `programme/`). `config.py` résout désormais `DONNEES_DIR = ../donnees` (surchargeable par la variable d'environnement `EMSP_DONNEES` pour un emplacement protégé distinct), d'où `WORKBOOK`, `WORKBOOK_NOTES`, `INSTANCE_DIR`, `AUTH_FILE`, `JOURNAL_FILE`. Tous les autres modules passant déjà par ces constantes, **seul `config.py` change** côté code.
- **Structure du kit** : `socle/` (Python embarqué + wheels, installé une fois) · `programme/` (code pur, effaçable/remplaçable en bloc) · `donnees/` (`data/` classeurs + `instance/` comptes/journal, jamais écrasés).
- **Formation** : `INSTALLER_FORMATION.bat` et `REINITIALISER_FORMATION.bat` visent `..\donnees\` ; détection du drapeau via `donnees/instance/formation.flag`.
- **Tests (maquette de kit jetable)** : chemins résolus vers `donnees/` ; bootstrap superadmin écrit `donnees/instance/comptes.json` et **rien dans `programme/`** ; détection formation OK depuis `donnees/instance/` ; routes GET sans 500 ; seed `donnees/data/EMSP_V1.xlsx` au md5 canonique.
- **Migration d'un poste existant** : déplacer `programme\data\` → `donnees\data\` et `programme\instance\` → `donnees\instance\` (voir LISEZMOI du kit).

## Ce qui change en V1.52 (périmètre de l'édition en place)

> **AUCUNE modification du classeur** (md5 `bfe96457b7f0dc7fac7041989d77c309` inchangé). Lot 100 % code : `config.py` (VERSION 1.52), `app.py`, `templates/module.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Décision** : l'**édition de ligne** introduite en V1.51 était branchée sur tout `ONGLETS_SAISIE_ACTIVE` (18 onglets). Arbitrage : garder **un seul code générique** (pas de fork « fiches étudiants »), mais **restreindre le périmètre d'usage** via liste blanche. Frontière retenue = *donnée de référence / champ de workflow corrigeable* vs *registre append-only*.
- **`config.py`** : nouvelle `ONGLETS_SANS_EDITION_LIGNE = ("F1_Mouvements",)` et `ONGLETS_EDITION_LIGNE = [t for t in ONGLETS_SAISIE_ACTIVE if t not in ONGLETS_SANS_EDITION_LIGNE]` (17 onglets). Seul **`F1_Mouvements`** (journal financier, contexte audit AFD) reste en **ajout seul** : une erreur s'y corrige par écriture rectificative, jamais en réécrivant la ligne. Durcissement futur = 1 ligne (candidats `F2_Comptes`, `N3_Signalements`).
- **`app.py`** : route `POST /module/<onglet>/modifier` gardée par `ONGLETS_EDITION_LIGNE` (404 sinon) ; l'**ajout** (`/ajouter`) reste gardé par `ONGLETS_SAISIE_ACTIVE` (inchangé).
- **`templates/module.html`** : l'encadré *Modifier une fiche existante* est conditionné par `data.lignes and onglet in cfg.ONGLETS_EDITION_LIGNE` — invisible sur `F1_Mouvements`. Le formulaire de saisie partagé (ajout/modif) reste inchangé.
- **Tests (copie jetable)** : `py_compile` des 5 modules OK ; `ONGLETS_EDITION_LIGNE` = 17 onglets, F1 exclu, A1 inclus, sous-ensemble strict de SAISIE_ACTIVE ; `module.html` parse Jinja + garde-fou présent ; **client de test authentifié** : `/module/F1_Mouvements/modifier` → **404**, A1/N2/E2/F2/N3 → 302 (gate franchi), `/module/F1_Mouvements/ajouter` → 302 (**ajout préservé**) ; classeur **md5 canonique inchangé**, 27 onglets, 16 dessins.
- **Fichiers** : `config.py`, `app.py`, `templates/module.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## Ce qui change en V1.51 (modification des fiches : édition de ligne)

> **AUCUNE modification du classeur** (md5 inchangé). Lot 100 % code : `data.py`, `app.py`, `templates/module.html`, `config.py` (VERSION 1.51), `doc/doc_des_ecrans.md`, `ETAT.md`.

- **Besoin** : pouvoir **corriger une fiche étudiant** déjà saisie (faute de frappe, changement de statut…). Jusqu'ici l'écran générique `A1_Etudiants` (et les autres onglets en saisie active) ne permettait que l'**ajout** et la **consultation**.
- **Édition générique de ligne** pour les onglets `ONGLETS_SAISIE_ACTIVE` :
  - `data.py` → nouvelle primitive `modifier_ligne(onglet, index, valeurs)` : cible la `index`-ième ligne **non vide** (même logique que `lignes()`, donc alignée sur l'affichage), réécrit les colonnes fournies (vide = effacement), **ne touche jamais une colonne calcul** (formule préservée), refuse les onglets en lecture seule. Même voie d'écriture qu'`ajouter_ligne`.
  - `app.py` → route `POST /module/<onglet>/modifier` : garde `ONGLETS_SAISIE_ACTIVE` + droit d'écriture ; lit `_index` ; prend **toutes** les valeurs des `champs_saisie` (vide = effacement) ; réinjecte `Saisi par` = login courant ; `valide_saisie` ; journalise « Modif ligne ».
  - `templates/module.html` → sélecteur **« Modifier une fiche existante »** au-dessus du formulaire (peuplé en JS, libellé = 4 premières valeurs non vides). *Charger pour modification* recopie la ligne dans le formulaire d'ajout réutilisé (champ caché `_index`, action basculée vers `/modifier`, titre + bouton adaptés, bouton *Annuler la modification*). **Le tableau filtrable n'est pas touché** (zéro régression sur recherche/filtres/pagination).
- **Pas de suppression physique** : la sortie d'un étudiant = changement de **Statut** (Diplômé / Abandonné / Radié), cohérent avec la conservation puis l'archivage.
- **Tests (copie jetable)** : `import app` OK, route enregistrée, `module.html` compile ; modification effective (Nom, Genre, Statut) ; **aucun doublon** (nb lignes constant) ; ligne voisine intacte ; **27 onglets** préservés. Classeur de livraison **non modifié**.
- **Fichiers** : `data.py`, `app.py`, `templates/module.html`, `config.py`, `doc/doc_des_ecrans.md`, `ETAT.md`.



> **AUCUNE modification du classeur** (md5 `bfe96457b7f0dc7fac7041989d77c309` inchangé). Lot 100 % code : `static/css/style.css`, `metier.py`, `app.py`, `config.py` (VERSION 1.50).

- **Décisions Bernard** : (1) module clôture/archivage (point 3) = **déjà livré en V1.44, on ne retouche pas** ; sur la ligne « Report a nouveau » de la clôture compta, le champ « Compte (**) » (V1.48) **reste vide** (= comportement déjà en place, audit de non-régression OK : F1 garde ses 17 colonnes sans décalage, états V1.48 tolèrent le Compte vide). (2) Bandeau formation à rendre visible **sur toutes les pages**. (3) Exports Excel formation : en-tête « FORMATION » **et** suffixe `_FORMATION`.
- **Bandeau web** : il était bien émis sur chaque page (porté par `base.html`) mais, en flux normal, masqué par la barre latérale/supérieure au défilement → d'où l'apparence « accueil seulement ». Passé en `position:fixed; top:0; z-index:2000` ; `body.formation` décalé de 30px ; sidebar `top:30px`. Décalage neutralisé en `@media print` (filigrane central inchangé).
- **Exports Excel** (6) : tableau de bord, onglet, vue, pivot, relevé/bulletin, état des signalements. En MODE_FORMATION : ligne d'en-tête rouge « FORMATION — données d'entraînement, sans valeur officielle » (fusionnée sur la largeur) + suffixe `_FORMATION` avant l'extension. Helpers `metier.bandeau_xlsx(ws, ncols)` (insert_rows, aucune fusion en amont → sûr) et `metier.nom_export(nom)`.
- **Tests** : mode formation — A1 = bandeau (fusion, fond #C0241F), titre/en-têtes décalés, `nom_export` ajoute `_FORMATION`, TDB bandeau sur les 6 feuilles ; mode production — aucun bandeau, nom inchangé ; **48 routes GET, 0 erreur 500** ; bandeau `formation-banner` présent dans le HTML de toutes les pages d'application (seules sans bandeau : API JSON, exports fichiers, pages d'impression — légitime) ; CSS servi = `position:fixed` + `body.formation{padding-top:30px}`. Classeur **md5 inchangé** (data/ = racine = seed, 27 onglets / 16 dessins / 669 formules).
- **Fichiers** : `static/css/style.css`, `metier.py`, `app.py`, `config.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## Point d'arrêt & prochaine action (V1.50)
- **V1.50 livrée** (marquage formation : bandeau partout + exports Excel). Classeur gelé inchangé, **md5 `bfe96457b7f0dc7fac7041989d77c309`**. Point 3 (clôture) confirmé clos en V1.44 — non retouché.
- **Reste roadmap** : (3) revue de toutes les sorties PDF ; (4) documents de mission (rapport de cadrage, note de cadrage applicatif, rapport de fin de mission) selon le calendrier ; (5) alignement de la formulation des documents parties prenantes (Tableau_Pointage_EMSP, canevas de formation) sur le messaging approuvé.
- À confirmer côté Bernard : push V1.50 effectué ?

> **Phase de test prévue le 16/06 après-midi.** À partir de là, éviter toute modification du classeur.

## Ce qui change en V1.49 (plan d'action enrichi + tableau de bord + formation tolerante)

> **CLASSEUR MODIFIE.** 6 colonnes ajoutees a `G1_Plan_action` (I..N, inlineStr s=7) : Axe / theme, Objectif (resultat attendu), Priorite, Temporalite, Indicateur de reussite et preuves, Observations. **16 dessins + 669 formules preserves, 27 onglets.** data/ = racine = seed.
> **NOUVEAU md5 canonique : `bfe96457b7f0dc7fac7041989d77c309`** (ancien `90f7454fb74c482d41667e6b31971d73`).

- Decisions Bernard : (1) detection formation tolerante (.txt + casse) -> fait ; (2) plan d'action enrichi AVEC Temporalite -> fait.
- Inspiration : modele MASE/APAVE fourni (structure uniquement, contenu SSE hors EMSP).
- `config.py` : `_detecter_formation()` (os.listdir, casse/.txt) ; LISTES_INLINE Priorite + Temporalite ; DICTIONNAIRE_CHAMPS_SUP G1 (6 champs).
- `metier.plan_action_liste()` reordonnee (14 colonnes, libelles propres) ; `metier.plan_action_kpis()` (etat, priorite, axe, retard, % acheve).
- `app.py` : route `/plan-action/tableau-de-bord` (gate G1) ; edition plan d'action en **paysage**.
- `templates/tableau_bord_plan_action.html` (nouveau) ; lien depuis `tableau_bord.html`.
- Tests : champs saisie G1 OK (Priorite/Temporalite listes) ; KPIs justes (6 actions, 1 achevee=17%, 3 en retard) ; edition paysage 14 colonnes lisible ; **70 routes GET, 0 erreur 500** ; POST G1 avec nouveaux champs 200 ; detection formation `Formation.Flag.txt` -> True.

## Ce qui change en V1.48 (CLASSEUR : colonne Compte + etats comptables + bulletin officiel)

> **CLASSEUR MODIFIE.** Colonne **« Compte (**) »** ajoutee a `F1_Mouvements` (col Q, SAISIE) par chirurgie zip : sharedStrings (+1), `sheet12.xml` (dimension A1:Q300, `<col>` 17, entete Q2). **16 dessins + 669 formules preserves, 27 onglets.** Graine `formation/seed/` realignee sur le master (dessins restaures + colonne).
> **NOUVEAU md5 canonique : `90f7454fb74c482d41667e6b31971d73`** (ancien `4eb8bd6d44595616ebef85f79d462468`). data/ = racine = seed (identiques).

- Decisions Bernard : (1) colonne Compte = champ **saisi** (plan comptable comorien, regroupements) -> fait ; (2) bulletin a l'identique de `RELEVE_NOTES.pdf` -> fait (annuel) ; (3) etat par poste budgetaire valide -> fait.
- `metier.situation_compte` : colonne Compte = champ `Compte` (plus la Categorie).
- `metier.etat_par_poste(mois, compte)` + route `/impressions/etat-poste` + carte hub (profil financier).
- `metier.bulletin_officiel(matricule, annee)` (+ `_notes_brutes`, `_fmt_note`) ; `templates/bulletin_officiel.html` ; route `/impressions/bulletin` -> annuel si semestre vide, sinon un semestre. Reutilise releve_semestre/annuel (calcul decret inchange), expose CC/Examen/session 2.
- Tests : aller-retour ecriture/lecture du champ Compte OK ; bulletin annuel rendu (S5 avec rattrapage session 2 -> 12,21 ; S6 13,5 ; annuelle 12,86) ; situation de compte affiche le Compte saisi (7061/627/7083) ; etat par poste OK ; **71 routes GET, 0 erreur 500** ; POST F1 avec Compte 200.
- Fichiers : classeur (x3), `metier.py`, `app.py`, `config.py`, `templates/impressions.html`, `templates/bulletin_officiel.html`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## Ce qui change en V1.47 (PRESENTATION menu/accueil + compte FORMATION)

> **AUCUNE modification du classeur** (md5 `4eb8bd6d44595616ebef85f79d462468`). config/auth/templates/css.

- Accueil : Scolarite (groupes reordonnes Salles > Etudiants > Enseignants > Referentiel) + Administration en **pleine largeur** (`pleine`) ; Direction + Parametrage cote a cote ; bande Parametrage supprimee (carte de grille) ; ancre `id` par section.
- Menu gauche : Parametrage = chapitre ; titre de chapitre = lien vers le bloc accueil (`#id`) ; menu Parametrage de la topbar retire.
- **Compte formation** : `formation`/`formation` amorce en MODE_FORMATION (sans changement force, droits superutilisateur) via `SUPERUSER_LOGINS` conditionnel + `auth.ensure_superadmin`.
- Tests : login formation OK (302 -> /, doit_changer False) ; accueil 200 (ordre, ancres, 2x principale, plus de param-bande) ; **87 routes GET, 0 erreur 500**.
- Fichiers : `config.py` (VERSION 1.47), `auth.py`, `templates/accueil.html`, `templates/base.html`, `static/css/style.css`.

### RESTE A FAIRE (decisions Bernard 18/06 — lot suivant, V1.48)
1. **Colonne « Compte » saisie** (situation de compte) : decision = champ saisi par l'utilisateur (plan comptable comorien, regroupements), NON derive de la Categorie. => ajout d'une colonne **« Compte »** dans `F1_Mouvements` (SAISIE) = **modification structurelle du classeur** (chirurgie zip + nouveau md5 + propagation saisie/situation/journal). A FAIRE apres confirmation du moment (phase de test).
2. **Bulletin** : refaire la mise en page a l'identique de `RELEVE_NOTES.pdf` (2 pages : 3e + 4e semestre L2 ; colonnes C.Continu / Examen / Moyenne / Exam session2 / Moyenne Session2 / Coef / ECTS ; decision du jury ; mention). Necessite d'exposer CC/Examen (et session 2) par matiere dans `releve_semestre`.
3. **Etats comptables** : opportunite etat par poste budgetaire / par bailleur (recommande : poste budgetaire, utile pour l'audit AFD).

## Ce qui change en V1.46 (EDITIONS — corrections + documents EMSP manquants)

> **AUCUNE modification du classeur** (md5 `4eb8bd6d44595616ebef85f79d462468`). Code + gabarits.

Revue du catalogue par Bernard -> traite point par point :
1. **Situation de compte** : + colonne « Compte » (registre EMSP). Mapping = champ `Categorie` de F1 (Chapitre = `Poste budgetaire`) — **A CONFIRMER**.
2. **Releve d'heures** : periode en clair (« Juin 2026 ») via `_periode_libelle` (individuel + recap).
3. **Feuille de presence de la semaine** (doc A) : NOUVELLE, **paysage**, jours x 4 creneaux (10h/12h/15h/17h), date+lieu de naissance, pre-remplie (`feuille_presence_semaine`, kind `presence_semaine`, `print.css` grille). Ancienne presence vierge conservee.
4. **Liste etudiants** : + colonne « Origine / lieu actuel ».
5. **Fiche d'appreciation de stage** (doc D) : NOUVELLE, vierge a l'identique (`appreciation_stage.html`).
6. **Bulletin de notes** : NOUVELLE edition imprimable (`releve_print.html`) via `releve_semestre` (decret 05-106) + exemple de formation injecte pour la demo.
7. **Plan d'action** : NOUVELLE edition tableau (`plan_action_liste`).
8. **Autres etats comptables** : NOUVEAUX — `journal_treso` (journal de tresorerie) et `balance_comptes` (situation globale), profil financier. Pistes possibles ensuite, sans engagement : etat par poste budgetaire, par bailleur.

Rendu generique « table » + orientation paysage ajoutes a `imprimer.html` ; 6 routes `/impressions/*` ; 6 cartes ajoutees au hub (`impressions.html`).

### Tests V1.46 (client Flask, copie jetable `build46_test` peuplee : etudiants, F1/F2, G1, N1/N2)
- **90 routes GET** : 0 erreur 500. Hub Impressions : 200, 6 nouvelles cartes presentes.
- Rendu PDF controle visuellement : presence semaine (paysage, fidele doc A), bulletin (calcul decret OK : Endocrinologie 13,25 ; moyenne sem 12,54 ; mention Assez bien), situation de compte (colonnes Chapitre+Compte + solde courant).
- Catalogue regenere : `Catalogue_Editions_EMSP_V1_46.pdf` (couverture + table de correspondance + 13 editions).
- Fichiers : `metier.py`, `app.py`, `config.py` (VERSION 1.46), `templates/imprimer.html`, `templates/impressions.html`, `templates/appreciation_stage.html`, `templates/releve_print.html`, `static/css/print.css`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

### Questions ouvertes a confirmer
- **Situation de compte / colonne « Compte »** : source = `Categorie` ? ou un autre champ (n° de compte comptable) a prevoir ?
- **Bulletin** : l'exemple de formation utilise une maquette L3 S5 Soins Infirmiers fabriquee pour la demo ; preciser la formation/maquette de reference souhaitee.
- **Etats comptables** : faut-il l'etat des recettes/depenses par poste budgetaire et/ou par bailleur ?

## Ce qui change en V1.45 (CORRECTIFS — cohérence dates & monétaire)

> **AUCUNE modification du classeur** (md5 `4eb8bd6d44595616ebef85f79d462468` inchangé). Code seul : `metier.py`.

Audit de cohérence demandé (dates, monétaire) → 3 défauts internes corrigés :
1. **`_parse_date_fr` dédoublonné** : la 2ᵉ déf. (tuple) masquait la 1ʳᵉ (date) et cassait **Situation de compte** + **sélecteur mois trésorerie**. Déf. tuple supprimée ; déf. date durcie (accepte `date`/`datetime` et `JJ/MM/AAAA`, `JJ-MM-AAAA`, `AAAA-MM-JJ`).
2. **`_num` dédoublonné** : la 2ᵉ déf. (`float(v)`) renvoyait 0 sur « 50 000 »/« 12,5 ». Conservée : version tolérante (espaces, virgule).
3. **`_fmt_kmf`** aligné sur `_kmf_aff` (séparateur de milliers ESPACE, sans décimale inutile) → affichage monétaire homogène trésorerie/clôture/TdB ↔ situation/reçu. Heures fractionnaires préservées.

### Tests V1.45 (client Flask, copie jetable `build45_test` peuplée)
- Helpers : `_num`, `_parse_date_fr`, cohérence `_fmt_kmf`==`_kmf_aff` sur entiers — OK.
- **85 routes GET** (dont tous les `/module/<onglet>` et impressions) : **0 erreur 500**.
- Écritures : ajout étudiant, présences, trésorerie, clôture élèves, clôture compta — 200.
- Éditions auparavant cassées : situation de compte (Report à nouveau + « 799 423 »), trésorerie, état signalements — OK.
- Fichiers modifiés : `metier.py`, `config.py` (VERSION 1.45), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

### À surveiller (signalé, non corrigé)
- **Seed formation** `formation/seed/EMSP_V1.xlsx` : a perdu ses 16 dessins (sauvegarde openpyxl) — à re-geler à l'identique au prochain passage si l'on veut respecter « maj du seed ».
- `EMSP_V1.xlsx` (racine) = témoin de gel byte-identique à `data/` ; non chargé au runtime (peut être retiré du zip distribué, au choix).

## Ce qui change en V1.44 (lot CLÔTURE / ARCHIVAGE / PASSATION — point 3)

> **CLASSEUR MODIFIÉ (chirurgie du zip).** Deux onglets ajoutés : `J1_Journal_eleves`
> (12 colonnes) et `J2_Journal_compta` (7 colonnes). **16 dessins et 669 formules préservés**,
> 0 onglet supprimé, 3 fichiers de contrôle modifiés (`workbook.xml`, `workbook.xml.rels`,
> `[Content_Types].xml`). 25 → 27 onglets.
> **NOUVEAU md5 canonique : `4eb8bd6d44595616ebef85f79d462468`** (ancien `574f357…`).
> `data/EMSP_V1.xlsx` et la racine `EMSP_V1.xlsx` byte-identiques ; baseline
> `formation/seed/EMSP_V1.xlsx` mise à jour (J1/J2 ajoutés via openpyxl, déjà sans dessins).

- **Écran « Clôture & archivage »** (sous Paramétrage, **réservé à la Direction** — garde
  `_exige_direction` : écriture sur J1 **ou** J2). Trois opérations manuelles, chacune génère
  un **procès-verbal** (Word .docx + page imprimable / PDF navigateur).
- **Clôture des élèves** (année scolaire oct→juil, au 31/07) : les élèves dont le statut
  marque une sortie (Diplômé / Abandonné / Radié) sont inscrits au **journal permanent J1**
  (idempotent par matricule). **Diplôme et mention saisis à la clôture** (option (b) ; mention
  = liste du décret : Passable / Assez bien / Bien / Très bien). Les élèves **restent** dans
  `A1_Etudiants` (~3 ans).
- **Archivage** (bouton séparé) : les cohortes sorties depuis **≥ 3 ans** sont déplacées
  vers `archives/EMSP_Archive_Eleves_AAAA-AAAA.xlsx` (un fichier par année de sortie),
  retirées de `A1_Etudiants`, et leur **réf. archive** est renseignée dans J1.
- **Clôture compta** (année civile) : archive tous les mouvements de l'exercice dans
  `archives/EMSP_Archive_Compta_AAAA.xlsx`, écrit le **journal permanent J2** (totaux + solde
  de clôture), puis **report à nouveau** : `F1_Mouvements` est remplacé par une ligne
  « Report a nouveau » par compte au 01/01/N+1 (= solde de clôture), et `F2.Solde initial`
  est remis à 0 (l'ouverture est portée par la ligne de report). Le **solde courant de chaque
  compte est conservé**.
- **PV Word sans dépendance** : généré au runtime par `metier.generer_docx` (zipfile + XML brut,
  Calibri, titres #1F4E79). **Aucune dépendance ajoutée** (requirements inchangé :
  Flask / openpyxl / pandas). Le « PDF » suit le mécanisme existant (page imprimable + print.css).
- **Couches touchées** : classeur (chirurgie zip) ; `config.py` (constantes clôture
  `ARCHIVES_DIR` / `ANNEES_GARDE_ELEVES` / `STATUTS_SORTIE` / `MENTIONS`, J1/J2 dans
  `ONGLETS_DIRECTION`, menu « Clôture & archivage », `SPECIAL_ROUTES["CLO_Cloture"]`,
  `DICTIONNAIRE_SUPPLEMENT` J1/J2, VERSION 1.44, relabel « Comptes & accès ») ; `metier.py`
  (moteur clôture/archivage + `generer_docx` + `pv_blocs`) ; `app.py` (`_exige_direction` +
  routes `/cloture`, `/cloture/eleves`, `/cloture/eleves/archiver`, `/cloture/compta`,
  `/cloture/pv`, `/cloture/pv.docx`) ; `templates/cloture.html`, `templates/pv_cloture.html`.

### Tests V1.44 (client Flask, sur copie jetable `test_run`)
- Clôture élèves : J1 rempli (4 sorties), diplôme/mention captés, **idempotent** (reste 4 à la
  re-clôture). Élève actif jamais journalisé.
- PV : `/cloture/pv` 200 ; `/cloture/pv.docx` 200, **Word valide** (ouvert par python-docx).
- Clôture compta 2025 : archive 4 mouvements ; J2 = recettes 1 250 000 / dépenses 380 000 /
  solde 1 470 000 ; F1 = 2 lignes report à nouveau (01/01/2026) ; F2 solde initial = 0 ;
  **soldes courants conservés** (270 000 / 1 200 000).
- Archivage ≥ 3 ans : détection sur l'année de **sortie**, déplacement A1→archive,
  réf. archive renseignée dans J1, **idempotent** (plus rien à archiver ensuite).
- Accès Direction-only : 403 sur les 6 endpoints pour un compte sans droits.
- Consultation read-only J1/J2 via le menu : 200. Accueil / Dictionnaire : 200.
- **Master V1_43 intact** après tests (md5 `4eb8bd6d…`, tests menés sur la copie).

## Point d'arrêt & prochaine action (V1.44)
- **V1.44 livrée** (lot Clôture / archivage / passation, point 3). Classeur re-gelé,
  **md5 `4eb8bd6d44595616ebef85f79d462468`**.
- **Lots suivants** (roadmap) : (c) finition des exports Excel « FORMATION » (ligne d'en-tête
  « FORMATION » dans les exports ; filigrane PDF déjà en place) ; (d) vérification de toutes
  les éditions PDF visibles par l'utilisateur. Réunion stakeholder reportée.

## Ce qui change en V1.43 (lot GOUVERNANCE DES COMPTES — point 4 ; classeur inchangé)

Refonte de `/autorisations` en **console « Comptes & accès »** du responsable informatique. Séparation des
responsabilités : l'informatique gère l'**identité** (comptes, mots de passe, validité, rubrique, couleur) ;
la Direction gère les **droits métier** (matrice par module) **directement dans `P1_Roles`** (rien à
développer, comme acté). La matrice rôles × modules reste **affichée en lecture seule**.

- « Responsable informatique » = capacité **`Admin droits (O/N)`** existante (décision actée : zéro chirurgie
  classeur, pas de colonne dédiée).
- **Mot de passe aléatoire 8 caractères** (`secrets`, alphabet sans `O/0/l/1/I`) à la création ET à la
  réinitialisation, **affiché une seule fois** (encart copiable porté par la session), `doit_changer=True`.
  Plus de saisie manuelle de mot de passe par l'informatique.
- **Validité = année scolaire** (31/07). Expiration **NON bloquante** (bandeau « à renouveler », `compte_expire`
  au contexte). Bouton **« Renouveler (année scolaire) »** → 31/07 suivant, sans toucher au mot de passe.
- **Couleur CHOISIE** par l'informatique (sélecteur de pastilles) ; `couleur_login` privilégie la couleur
  stockée, sinon dérive du login (rétrocompatible).
- **Self-service mot de passe SUPPRIMÉ** (décision actée) : lien retiré de la barre supérieure ;
  `/mot-de-passe` accessible **uniquement** au changement forcé (1er login / après réinitialisation).
- **Grande rubrique** : `config.RUBRIQUES` (Direction, Scolarité, Comptabilité, Enseignants / Départements,
  Logistique, Informatique), éditable.
- **Stockage** : rubrique, couleur, `valide_jusqu` dans `instance/comptes.json` (**hors dépôt et hors zip**),
  à côté de l'empreinte. La création écrit dans `P1_Roles` **uniquement** `login + role`
  (`ecrire_lignes_lot` préserve les colonnes de droits en MAJ). **Classeur inchangé, md5 `574f357…`.**
- **auth** : `generer_mdp`, `definir_attributs`, `attributs`, `couleur`, `initialiser_validite`, `renouveler`,
  `est_expire`, `_fin_annee_scolaire`/`_prochain_31_07` ; `reinitialiser(login)` → `(ok, mdp_clair)`.
  **metier** : `couleur_login` sensible à la couleur choisie, `enregistrer_compte_it`, `rubriques`,
  `utilisateurs_admin` enrichi. **app** : `/autorisations/utilisateur` (création/MAJ IT),
  `/autorisations/reinitialiser`, `/autorisations/renouveler` (nouvelle), `/autorisations/supprimer` ;
  `mot_de_passe` verrouillée ; `compte_expire` au contexte. **config** : `RUBRIQUES`, `MDP_*`,
  `ANNEE_SCOLAIRE_FIN_*`, VERSION 1.43.
- Tests : `py_compile` (5 modules) ; flux client Flask complet (création → mdp affiché une fois →
  rubrique/couleur stockées → renouvellement 31/07/2026→31/07/2027 → réinitialisation → self-service
  bloqué 302 → ligne `P1_Roles` login+role) ; compte expiré (200 non bloquant + bandeau). md5 livré inchangé.

## Point d'arrêt & prochaine action (V1.43)
- **V1.43 livrée** (lot Gouvernance des comptes, point 4). Tests OK, classeur gelé inchangé (md5 `574f357…`).
- **Prochain lot : CLÔTURE / ARCHIVAGE / PASSATION (point 3)** — structure déjà figée (voir ci-dessous).
  Confirmer la liste des champs des journaux permanents + format des fichiers d'archive AVANT d'implémenter.
- Ensuite : **finition exports Excel « FORMATION »** (ligne d'en-tête FORMATION dans les exports ; le filigrane
  PDF/navigateur est déjà en place), puis **revue de toutes les éditions PDF**.

## Ce qui change en V1.42 (consolidation : base de code UNIQUE prod/formation)

Suppression du fork « DEMO ». Un seul logiciel ; le mode dépend d'un drapeau local
`instance/formation.flag` (hors zip). Présent -> FORMATION (bandeau rouge, body.formation pour le
filigrane d'impression, plafond `FORMATION_MAX=50`/onglet en ALERTE non bloquante via app.module_ajouter,
données fictives). Absent -> production. `config.MODE_FORMATION` calculé au démarrage ; contexte `formation`
exposé aux gabarits ; bandeau + filigrane dans base.html/CSS.

Kit `formation/` livré avec le logiciel : `seed_formation.py` (régénère le jeu), `seed/` (baseline),
`INSTALLER_FORMATION.bat`, `REINITIALISER_FORMATION.bat`/`.sh` (restaure les exemples + efface saisies ET
comptes stagiaires + journal ; **refuse de tourner sans le drapeau** -> jamais sur la prod),
`LISEZMOI_FORMATION.txt`. Régénération/effacement testés : 13->12 élèves, `STAG-TEST` et `comptes.json`
supprimés, drapeau conservé ; garde-fou anti-prod OK (code retour 1).

Correctif **`Comptes_caisses`** remonté en PRODUCTION (LISTES_ONGLET -> F2) : menu « Compte/caisse » de la
saisie financière et widget trésorerie désormais alimentés. Classeur de prod **inchangé** (md5 `574f357…`,
16 dessins). data/ reste le master VIDE dans le zip ; la baseline seedée vit uniquement dans `formation/seed/`.

## Ce qui change en V1.41 (lot rapide — interface seule, classeur inchangé)

- **Accueil** : Scolarité en carte **pleine largeur** en tête ; Administration + Direction **en dessous**
  sur 2 colonnes (conteneur dédié `.acc-sections`, `.cards` laissé intact pour impressions/requetes).
- **Identité utilisateur** : `config.COULEURS_UTILISATEUR` + `metier.couleur_login` + contexte `couleur_user` ;
  base.html ajoute un **liseré** coloré en haut et une **pastille** colorée autour du login. Couleur stable par
  login (collision possible si beaucoup de comptes -> tranchée par l'informatique au lot gouvernance).
- Classeur non touché (md5 `574f357…`). Tests : `/` 200, Scolarité = carte principale pleine largeur,
  liseré + pastille présents, couleurs distinctes par login.

### Décisions actées pour les lots suivants (réunion de cadrage)
- **Lot FORMATION (point 2)** : bandeau **rouge** « FORMATION » + filigrane « FORMATION » gris (haut/milieu/bas)
  sur impressions/PDF + **plafond 50 lignes/partie** en **ALERTE non bloquante** (validé : on laisse passer).
- **Lot gouvernance comptes (point 4)** — **LIVRÉ en V1.43** : création/affectation à une grande rubrique + reset mot de passe
  **réservés au responsable informatique** (= `Admin droits`) ; mot de passe **aléatoire 8 caractères** affiché une fois,
  validité **année SCOLAIRE**, **expiration non bloquante** (alerte « à renouveler »), retrait total du self-service mot de
  passe (hors 1er login forcé) ; couleur utilisateur choisie par l'informatique. Stockage `comptes.json`, classeur inchangé.
- **Lot clôture/archivage/passation (point 3)** — structure FIGÉE :
  - Élèves (année scolaire oct->juil) : inactifs inscrits au **journal permanent élèves** à la clôture, **gardés
    ~3 ans** dans le fichier actif, puis **archivés** dans `archives/EMSP_Archive_Eleves_AAAA-AAAA.xlsx`.
    Journal = matricule, nom, filière, période (entrée->sortie), statut final, **diplôme** (si obtenu),
    **mention**, réf. archive.
  - Compta (année civile) : mouvements de l'année archivés dans `archives/EMSP_Archive_Compta_AAAA.xlsx`,
    **report à nouveau** des soldes, **journal permanent compta** (année, total recettes, total dépenses,
    solde de clôture, réf. archive). Actif = année civile en cours.
  - Clôture **manuelle** (admin) + génération d'un **PV de clôture/passation** (Word+PDF).
- **Logo** (point 3 d'origine) : reporté.

## Ce qui change en V1.40

### Matériel (M1) + Expression de besoin (L3) — points 3 & 5 de la réunion
- **M1.Etat** devient une **liste éditable** `Etats_materiel` (Actif / En panne / Hors service /
  En maintenance / Réformé) ; défaut M1.Etat aligné sur « Actif ». Nouvelle colonne **« Localisation
  provisoire »** (texte libre).
- **Nouvel onglet `L3_Besoins`** (sheet25, mirroir de S2) — registre des besoins logistiques, module
  Logistique, saisie active. 13 champs (ID auto BES-n, date, type de besoin, équipement concerné
  optionnel = liste vallabel des équipements M1, libellé, quantité, localisation L1, priorité, statut,
  coût KMF, demandeur, observations, saisi par auto).
- **4 listes éditables** ajoutées en P0 : `Etats_materiel`, `Types_besoin`, `Priorites_besoin`,
  `Statuts_besoin`.
- **Déclenchement** : panneau « Matériels indisponibles » sur l'écran M1 (états En panne / Hors service)
  → bouton « Exprimer un besoin » → `/module/L3_Besoins?equip=<ID>&type=Matériel en panne` ; le formulaire
  L3 lit ces paramètres et pré-remplit Équipement concerné + Type de besoin. Manuel, sans automatisme.

**Classeur — ajout additif par chirurgie du zip** : `sheet2.xml` (P0 : 4 listes), `sheet22.xml`
(M1 : colonne Localisation provisoire + bannière A1:K1→A1:L1), **nouveau `sheet25.xml`** (L3) +
`xl/workbook.xml` (+sheet sheetId 25 r:id rId28) + `xl/_rels/workbook.xml.rels` (+relation) +
`[Content_Types].xml` (+override). Vérifié : **5 membres modifiés + 1 ajouté, 16 dessins / 669 formules /
669 valeurs en cache préservés, 25 onglets**. **Nouveau md5 canonique :
`574f357617477a51daf2eac561b7db5a`** (ancien `eb71af4e…`). Deux copies byte-identiques.

Câblages : Dictionnaire L3 via `DICTIONNAIRE_SUPPLEMENT` (onglet entier ajouté) ; `DICTIONNAIRE_SURCHARGE`
M1.Etat → `Etats_materiel` ; `DICTIONNAIRE_CHAMPS_SUP` M1 « Localisation provisoire » ;
`LISTES_ONGLET_VALLABEL` « Equipements (M1) » (en-têtes M1 exacts avec marqueurs) ; ID auto `@next_bes`
(+ `metier._prochain_bes`) ; `CHAMPS_AUTO_LOGIN` L3 ; module Logistique + menu (groupe Logistique) ;
`metier.materiels_en_panne` + panneau M1 + pré-remplissage app/template. Tests : intégrité ; cohérence
entête↔Champ L3 ; champs L3 (ID auto, dates, 3 listes) ; liste équipements vallabel (EQ-n — Désignation) ;
M1.Etat 5 valeurs + Localisation provisoire ; **écriture/relecture d'un besoin lié à EQ-1** ; panneau
indisponibles + lien + **pré-remplissage L3 effectif** ; rendus L3 & M1 = 200.

## Ce qui change en V1.39

### Plan d'action (G1) — enrichissement (suivi des écarts)
Lot « plan d'action » (point 6 de la réunion), sur l'esquisse validée (affinage ultérieur).
- Nouvelle colonne **« Type d'écart »** (liste éditable `Types_ecart` : Budgétaire, Temporel,
  Contenu de formation, Qualité, Autre) pour qualifier la nature de l'écart.
- **« Statut »** passe en **liste éditable** `Statuts_action` (notion de planning : Non démarré,
  En cours, Atteint, En retard, Abandonné). Statut était déjà déclaré « Liste » sans source.
- **Saisie activée** sur G1 (écriture = « Tous » → Direction/EMSP via ONGLETS_DIRECTION).

**Classeur — ajout additif par chirurgie du zip** : `sheet2.xml` (P0 : 2 listes `Types_ecart`,
`Statuts_action`) et `sheet14.xml` (G1 : colonne `Type d'écart`, entête seule). Vérifié : **2 membres
du zip modifiés, 0 ajout/suppression, 16 dessins / 669 formules / 669 valeurs en cache conservés**.
**Nouveau md5 canonique : `eb71af4e758df211814fbdf9289fe06c`** (24 onglets ; ancien `b542ace…`).
Deux copies byte-identiques.

Câblages **sans toucher l'onglet Dictionnaire** : `DICTIONNAIRE_SURCHARGE` G1.Statut → source
`Statuts_action` ; nouveau mécanisme `DICTIONNAIRE_CHAMPS_SUP` (ajout d'un champ à un onglet existant) +
extension de `metier.dictionnaire_par_onglet` pour le champ `Type d'écart` → source `Types_ecart`.
Couches : classeur, config.py (saisie G1 + surcharge + champ sup + VERSION 1.39), metier.py, app.py
(rien de spécifique), templates (formulaire générique), README/doc. Tests : 2 membres zip modifiés ;
intégrité OK ; champs_saisie G1 = Statut + Type d'écart en listes (5+5) ; rendu G1 200 ; **écriture réelle
d'une ligne G1 relue correctement** (Statut + Type d'écart dans les bonnes colonnes).

À affiner : position de « Type d'écart » (ajoutée en dernière colonne) et valeurs des deux listes.

## Ce qui change en V1.38

### Documents officiels (H1) — catégorisation éditable + consultation groupée
Lot « documents officiels » (point 2 de la réunion). 
- La colonne **« Type » de H1 devient la CATEGORIE**, alimentée par une liste **éditable par le directeur**
  `Categories_doc` (P0). Valeurs de départ : Stratégique, Médical, Supports de cours, Réglementaire/officiel,
  OMS/international, Autre.
- **Saisie activée** sur H1 (catégorie en liste déroulante ; écriture = « Tous » → Direction, via ONGLETS_DIRECTION).
- **Consultation groupée par catégorie** (titre, référence, date, responsable, chemin) + barre de puces +
  bouton « Copier le chemin » (pas d'ouverture auto : bloquée par le navigateur). Tableau brut filtrable conservé.

**Classeur — ajout additif par chirurgie du zip** : seule la feuille `sheet2.xml` (P0_Parametres) modifiée
pour ajouter la colonne-liste `Categories_doc` (en chaînes inline, sharedStrings intact). Vérifié : **un seul
membre du zip modifié, 0 ajout/suppression, 16 dessins / 669 formules / 669 valeurs en cache conservés**.
**Nouveau md5 canonique : `b542ace78d1d6b375c3365962839b9ad`** (24 onglets ; ancien `fba973b7…`). Deux copies
byte-identiques (racine + `data/`).

Câblage par **surcharge applicative** (aucune modif de l'onglet Dictionnaire) : `DICTIONNAIRE_SURCHARGE`
H1.Type → source `Categories_doc`. Couches : classeur (P0), `config.py` (ONGLETS_SAISIE_ACTIVE + surcharge,
VERSION 1.38), `metier.py` (`documents_officiels_groupes`), `app.py` (passage au template), `module.html`
(panneau consultation + bouton copier), `static/css/style.css`. Tests : un seul membre zip modifié ;
intégrité OK ; liste résolue (6 catégories) ; saisie Type en liste ; groupement dans l'ordre de la liste ;
rendu H1 200. 

## Ce qui change en V1.37

### Affichage des grands tableaux de consultation (R1 et autres) — aucune modification Excel
Demande issue de la réunion (référentiel R1 = 661 lignes, 14 colonnes, tronqué à droite et tout déroulé).
Amélioration **générique** de l'affichage des tableaux de données (`module.html`), côté client, hors-ligne :
- **Recherche plein texte** (insensible accents/casse) + **filtre par colonne** sous l'en-tête (liste
  déroulante si peu de valeurs distinctes, sinon champ « contient »).
- **Pagination** : 20 lignes par défaut (40 / 100 / Toutes), compteur « 1-20 sur 661 », précédent/suivant.
- **Première colonne figée** + défilement horizontal net pour atteindre les 7 colonnes de droite.
- L'export Excel exporte toujours l'intégralité (les filtres ne touchent que l'affichage).

Profite à tous les onglets de données ; sur un onglet vide, le script ne fait rien (garde-fou). Couches :
`templates/module.html` (barre d'outils + ligne de filtres + pagination + script), `static/css/style.css`
(styles outils + colonne figée), VERSION 1.37. Tests : syntaxe JS OK ; rendu R1 200 avec barre complète.

## Ce qui change en V1.36

### Réorganisation de la présentation (menu + accueil) — aucune modification Excel
Suite aux notes de la réunion (point 4). **Aucun fichier Excel touché** : `config.GUIDE_STRUCTURE` passe à
**deux niveaux** (sections → groupes), avec dérivation à plat de `sec["modules"]` (source unique = `groupes`),
de sorte que `_index()`/TAB_INDEX, le menu, l'accueil, `app.py` et `metier.py` continuent de fonctionner sans
changement.

Nouvelle arborescence (validée) :
- **Scolarité** : *Filières* (R1) · *Enseignants* (E1, E2, séances A3, calendrier) · *Étudiants* (A1, A2,
  stages S1/S2, barème N1, notes N2, signalements N3, état SIG, relevé REL, documents A4) · *Salles* (planning, L1, L2).
- **Administration** : *Finances & pilotage* (F1, F2, requêtes, impressions, plan d'action G1, documents
  officiels H1) · *Logistique / moyens généraux* (équipements M1).
- **Direction** : tableau de bord **uniquement**.
- **Paramétrage** (P0, P1, matrice MAT, import, modèles) : **déporté à droite** — menu dédié dans la barre
  du haut + bandeau séparé en bas de l'accueil (plus en position centrale). Marqué `aside: True` dans la config.

Nettoyage des **mentions « V2 »** dans les aides (`module.html`, `impressions.html`) → formulation charte
« pistes possibles ensuite, sans engagement ».

Couches : `config.py` (GUIDE_STRUCTURE 2 niveaux + flatten, MAT déplacé en Paramétrage, VERSION 1.36),
`templates/base.html` (menu latéral avec sous-titres de groupe + menu Paramétrage dans la barre du haut),
`templates/accueil.html` (cartes avec sous-groupes + bandeau Paramétrage), `static/css/style.css` (styles
sous-groupes / menu paramétrage / bandeau), `templates/module.html` + `impressions.html` (V2). README, doc, ETAT.

Tests : import complet OK ; rendu (client de test) accueil + modules + autorisations + relevé + équipements
= 200 ; 3 sections + sous-groupes + Paramétrage (barre + bandeau) présents ; jeu des 31 clés de modules
inchangé (aucune page orpheline). Classeurs **non touchés**.

> Interprétation à confirmer à l'usage : « Paramétrage à droite » rendu par un menu déroulant dans la barre
> du haut + bandeau d'accueil. Placement exact ajustable après visualisation.

## Ce qui change en V1.35

### Barème N1 pré-rempli + colonne « Coef confirmé » + bandeau « barème provisoire »
Remplissage de l'onglet **`N1_Bareme_UE`** (fichier notes), point d'arrêt de la session précédente.
Le classeur principal `EMSP_V1.xlsx` est **inchangé** (md5 `fba973b7cb4ffcd1a143e49e62bf2ba9`).

- **Nouvelle colonne `Coef confirmé` (Oui/Non)** dans N1 (9e colonne). *Oui* = coefficient validé par un
  document de référence officiel ; *Non* = provisoire (1 par défaut). Défaut de saisie manuelle = Non.
- **L2 Soins infirmiers — S3 et S4** : barème **confirmé** (41 lignes), coefficients + ECTS réels du
  relevé officiel (RELEVE_NOTES.pdf). **Moteur revalidé** : relevé S3 recalculé = **9,89**, identique au
  bulletin (UE par UE : 14,00 / 11,78 / 12,75 / 9,91 / 4,75 / 6,00 / 15,33).
- **4 filières LMD en squelette provisoire** (557 lignes) : SI hors L2, Soins obstétricaux, Maintenance
  biomédicale, Imagerie médicale — structure UE/matières des maquettes, **coef = 1**, ECTS repris,
  `Coef confirmé = Non`. SI S3/S4 exclus (couverts par le relevé). **Aides-soignants non intégré**
  (modèle Modules/Contenus sans UE/ECTS/coef, incompatible avec N1).
- **Bandeau « Barème provisoire »** sur le relevé (écran + impression + sous la moyenne annuelle) dès
  qu'une UE du barème utilisé n'est pas confirmée : moyennes indicatives, coefficients à corriger.
- **`scripts/seed_bareme.py`** (versionné, idempotent) + **`scripts/maquettes_skeleton.json`** (squelette
  figé, sans dépendance au fichier maquettes). Total N1 : **598 lignes** (41 confirmées + 557 provisoires).
- **Stage2** documenté comme légitime en UE16 (S3) et UE21 (S4) — relevé officiel, pas un doublon
  (Lisez-moi du fichier notes + doc des écrans).

Couches : fichier notes (N1 : colonne + données), `config.py` (LISTES_INLINE « Oui/Non », dictionnaire
N1, SAISIE_DEFAUTS, VERSION 1.35), `metier.py` (`_bareme_ues` lit `Coef confirmé` ; `releve_semestre` /
`releve_annuel` exposent `bareme_provisoire`), `templates/releve.html` (bandeau + coef décimal `%g`),
`templates/module.html` (aide N1), `static/css/style.css` (style bandeau), `scripts/` (seed + données),
README, doc des écrans, ETAT.

## Ce qui change en V1.34

### Etat des signalements / indiscipline (par etudiant)
Nouvelle page **`/etat-signalements`** (menu Etudiants) : compte rendu disciplinaire GROUPE PAR
ETUDIANT, a l'usage de la scolarite. Filtres : Annee acad., plage de dates (Du / Au), Semestre,
Contexte, Filiere, Niveau (tous facultatifs). Chaque etudiant concerne est affiche avec son nombre de
signalements et le detail (date, semestre, contexte, fonction, emetteur, motif), trie par date.
Volontairement **sans les notes** (pur disciplinaire). Imprimable + export Excel. Compteurs : nombre
d'etudiants et total de signalements. Accès reserve au module Notes.

Couches : `metier.py` (`etat_signalements`, `_parse_date_fr`), `app.py` (routes affichage + export),
`templates/etat_signalements.html` (nouveau), `config.py` (SPECIAL_ROUTES + menu), `style.css`.
Classeur principal et fichier notes inchanges.

Cela cloture le module Notes : barème, saisie assistee, calcul, releve (semestre/annuel,
impression/export), signalements (saisie + encart releve) et etat des signalements.

## Ce qui change en V1.33

### Signalements / indiscipline (information de deliberation, hors bulletin)
Nouvel onglet **`N3_Signalements`** dans le fichier notes (ajoute par openpyxl, N1/N2 preserves) :
Matricule, Date, Annee acad., Semestre (facultatif), Contexte (Examen/Cours/Stage/Autre),
Emis par - fonction (Surveillant/Enseignant/Scolarite/Chef de departement, listes extensibles),
Nom de l'emetteur, Motif. Saisissable via l'interface (module Notes).

Caractere **non bloquant** : un signalement n'affecte NI le calcul des moyennes NI la proposition
Admis/Ajourne. Aucune decision de jury n'est saisie/archivee (la validation ne releve pas de l'outil).

Sur le **releve a l'ecran** : encart "Signalements a examiner en deliberation" (liste date / contexte /
fonction / emetteur / motif) + mention "N signalement(s) a examiner" a cote de la proposition. Ces
elements sont en `no-print` : ils n'apparaissent PAS sur le bulletin officiel imprime ni dans l'export
Excel du bulletin (verifie).

Couches : fichier notes (onglet N3), `config.py` (ONGLETS_NOTES, module Notes, saisie, menu, listes
inline Contextes/Fonctions, dictionnaire N3), `metier.py` (`signalements_etudiant`, releve enrichi),
`templates/releve.html`, `static/css/style.css`. Classeur principal inchange ; fichier notes livre vide.

### A venir (validation en cours)
- **Etat des signalements / indiscipline** : page filtrable (annee, et facultativement filiere/niveau/
  semestre/contexte), liste des etudiants concernes groupee par etudiant, imprimable + export Excel,
  SANS les notes (compte rendu disciplinaire pour la scolarite). Forme proposee, en attente de GO.

## Ce qui change en V1.32

### Assistance a la saisie des notes (confort)
A la saisie d'une note (`N2_Notes`), les champs **N° UE** et **Matiere** proposent desormais des
suggestions tirees du **barème** (`N1_Bareme_UE`), filtrees par la filiere et le niveau de l'etudiant
(deduits du matricule via `A1_Etudiants`) et par le semestre saisi. Choisir une matiere **pre-remplit
le N° UE** correspondant (si vide). Saisie libre conservee ; filtrage cote client (hors-ligne).

Mecanisme : `metier.notes_assist()` (barème compact + table matricule -> filiere/niveau + bruts N2),
`config.CHAMPS_DATALIST` (datalist generique par onglet), script dedie dans `module.html`. Classeur
principal et fichier notes inchanges (aucune donnee).

### En attente / a venir
- **Avertissement / surveillant** : conception proposee a Bernard (signalement non bloquant, mentionne
  pour la deliberation, hors bulletin officiel). Implementation apres validation du design.

## Ce qui change en V1.31

### Module Notes — moteur de calcul + relevé (semestre & annuel)
Deuxième lot du module Notes. Calcul des moyennes selon le décret 05-106, et édition du relevé.
Aucune modification du classeur principal (`fba973b7cb4ffcd1a143e49e62bf2ba9` inchangé) ; le fichier
notes reste vide de données dans le livrable.

**Moteur de calcul** (`metier`, validé contre le bulletin réel L2 Soins infirmiers) :
- Moyenne d'une matière = ¼ CC + ¾ examen ; matière à note unique (stage) = la note saisie.
- Moyenne d'une UE = moyenne arithmétique de ses matières.
- Moyenne du semestre = moyenne des UE pondérée par le coefficient d'UE.
- **Calcul en cascade sur les valeurs exactes**, arrondi commercial (demi vers le haut) à 2 décimales
  pour l'affichage et la comparaison de validation (reproduit le 9,89 du bulletin, là où un arrondi
  intermédiaire donnerait 9,90). `round()` de Python n'est pas utilisé pour ces moyennes.
- 2ᵉ session : pour chaque matière, la note de session 2 remplace celle de session 1.
- Validation UE (≥ 10) et semestre (toutes UE ≥ 10 **ou** moyenne générale ≥ 10, par compensation) ;
  mention (Passable / Assez bien / Bien / Très bien) ; **proposition** Admis/Ajourné. La décision
  finale (délibération) n'est pas automatisée : c'est une proposition à valider.
- Récapitulatif annuel = moyenne des moyennes de semestre (exactes), pour le niveau (L1=S1/2, L2=S3/4,
  L3=S5/6 ; sinon, semestres présents dans les notes).

**Relevé** (`/releve`) : page avec sélection (matricule, année, semestre ou « année complète »),
affichage proche du bulletin (UE, matières, moyennes, mention, proposition, ECTS acquis/total),
**impression** (mise en page dédiée) et **export Excel**. Filière/niveau et nom de l'étudiant sont
repris de `A1_Etudiants`. Accès soumis au droit de lecture du module « Notes ».

### Couches touchées
- `metier.py` : `_arrondi2` (demi-supérieur), `_moyenne_matiere`, `_mention`, `etudiant_a1`,
  `_bareme_ues`, `_notes_effectives`, `releve_semestre`, `releve_annuel`.
- `app.py` : routes `/releve` (affichage) et `/releve/export` (xlsx en mémoire) ; imports `send_file`, `io`.
- `templates/releve.html` (nouveau), `static/css/style.css` (styles relevé + impression),
  `config.py` (`SPECIAL_ROUTES` + menu).
- Doc : README, doc des écrans, ETAT.

### Reste / en attente
- Assistance à la saisie des notes (proposer N° UE / Matière depuis le barème) — confort, à voir.
- **Avertissement / surveillant** : toujours en attente de ta décision sur son rôle dans la décision
  de passage (au-delà de la note). Non implémenté.
- Tests utilisateurs prévus en fin de développement (à ta demande).

## Ce qui change en V1.30

### Module Notes — socle : fichier séparé + barème + saisie des notes
Premier lot du module Notes (priorité métier). Création du **fichier séparé `EMSP_Notes.xlsx`**
(décision actée en V1.26 : confidentialité par séparation physique), avec trois onglets :
- **Lisez-moi** : explique que c'est le fichier des notes (accès restreint) et **où se définit le
  barème** (onglet `N1_Bareme_UE`), à renseigner avant toute saisie de notes ; rappelle les règles de
  calcul du décret 05-106.
- **`N1_Bareme_UE`** (le barème, référence du calcul) : Filière · Niveau · Semestre (cursus 1-6) ·
  N° UE · Intitulé UE · Matière · Coef UE · ECTS UE.
- **`N2_Notes`** (saisie) : Matricule · Année acad. · Session (1=juin, 2=rattrapage) · Semestre ·
  N° UE · Matière · CC · Examen.

Les deux onglets sont saisissables et consultables via l'interface ; le calcul des moyennes et le
relevé arrivent au lot suivant.

### Accès / confidentialité
Nouveau module de droits **« Notes »** (`MODULES_ONGLETS`). Les rôles « Tous » (Direction,
superadmin) y accèdent ; les autres rôles n'y ont pas accès tant que l'admin n'ajoute pas le module
« Notes » à leur ligne dans `P1_Roles`. La scolarité « Académique/Stages » n'a donc **pas** accès aux
notes par défaut — séparation voulue. Le fichier notes est distinct du classeur principal et peut
être stocké/sauvegardé à part au déploiement (chemin `config.WORKBOOK_NOTES`).

### Couche d'accès au 2ᵉ fichier
`metier._db_notes` (instance `AccesDonnees` dédiée) + `metier._db_pour(onglet)` qui route vers le bon
classeur selon `config.ONGLETS_NOTES`. `entetes_meta`, `table`, `capacite_onglet` et l'ajout de ligne
(app) routent désormais via ce sélecteur. Les listes (Matricule, Niveau…) restent lues dans le
classeur principal, ce qui est correct.

### Couches touchées
- Nouveau fichier `data/EMSP_Notes.xlsx` (vide de données dans le livrable).
- `config.py` : `WORKBOOK_NOTES`, `ONGLETS_NOTES`, `MODULES_ONGLETS["Notes"]`, `ONGLETS_SAISIE_ACTIVE`,
  `GUIDE_STRUCTURE` (menu), `DICTIONNAIRE_SUPPLEMENT` (N1/N2), `LISTES_INLINE` (Sessions, Semestres cursus).
- `metier.py` : `_db_notes`, `_db_pour`, routage de `entetes_meta`/`table`/`capacite_onglet`.
- `app.py` : ajout de ligne routé vers le bon fichier.
- Doc : README, doc des écrans, ETAT.
- Classeur principal **inchangé** (`fba973b7cb4ffcd1a143e49e62bf2ba9`, 24 onglets).

### Reste a faire (suite Notes — lot suivant)
- **Moteur de calcul** : moyenne matière (¼ CC + ¾ examen, ou note unique), moyenne UE (arithmétique),
  moyenne semestre (pondérée par coef UE), validation, mention, proposition Admis/Ajourné ;
  2ᵉ session (note de septembre remplace juin).
- **Relevé par étudiant** : par semestre **et** récapitulatif annuel, imprimable/exportable, format
  proche du bulletin réel.
- Assistance saisie : proposer N° UE / Matière depuis le barème (datalist).

### En attente (décision Bernard)
**Avertissement / surveillant** : Bernard évalue son rôle éventuel dans la décision de passage
(au-delà de la simple note). Non implémenté tant que ce point n'est pas tranché.

## Ce qui change en V1.29

### Module Stages — saisie assistée (contrôle de quota) + tableau de bord
Fin du module Stages (périmètre V1). Aucune modification du classeur (`fba973b7cb4ffcd1a143e49e62bf2ba9`
inchangé) : tout est calculé à l'affichage, côté client, à partir du référentiel `S2_Lieux_stage`
(quotas) et des affectations `S1_Stages`.

**Saisie assistée** : à la saisie d'un stage (`S1_Stages`), un indicateur affiche les **places
restantes** pour le lieu choisi selon l'année et la séance (places = Quota − affectations déjà
enregistrées pour ce lieu / cette année / cette séance). Non bloquant : la décision reste manuelle
(« complet » est signalé en rouge, mais la saisie reste possible).

**Tableau de bord d'occupation** : panneau sur la page Stages avec sélecteurs Année et Séance, un
tableau par lieu (Quota / Occupés / Restants, lignes pleines surlignées) et des compteurs (nombre de
lieux, étudiants affectés, places occupées sur total, taux d'occupation). Le quota s'entend par séance.

### Couches touchées
- `metier.py` : `stages_referentiel_lieux()`, `stages_affectations()`, `stages_cfg_saisie()`,
  helper `_idx_lib` (résolution d'index par libellé propre).
- `app.py` : `module()` passe `stages_cfg` / `stages_lieux` / `stages_affectations` pour `S1_Stages`.
- `templates/module.html` : panneau d'occupation + script local (calcul places restantes + tableau).
- `static/css/style.css` : styles du panneau (filtres, compteurs, ligne pleine, badge places).
- Doc : README, doc des écrans, ETAT.

### Différé (pistes possibles ensuite, sans engagement)
- Répartition par promotion dans le tableau de bord (nécessite la jointure avec A1 pour le niveau).
- Affectation automatique (algorithme), génération de toutes les séances de l'année d'un coup,
  rotation et historique sur les 3 ans, plaintes et évaluations détaillées.

### Suite du projet
Prochain grand chantier : module **Notes / relevés** (fichier séparé `EMSP_Notes.xlsx`, saisie CC +
examen, calcul selon le décret 05-106, délibération/compensation) avec avertissement/surveillant —
spec à figer avant de coder (cf. décision « fichier séparé » actée en V1.26).

## Ce qui change en V1.28

### Module Stages — socle : référentiel des lieux + lien S1
Premier lot du module Stages (demande EMSP via le CDC, hors TDR strict, marquage `*`).
Approche retenue : **saisie assistée avec contrôle humain** (pas d'affectation automatique),
**génération séance par séance**, et « au plus simple pour l'utilisateur ».

Nouvel onglet **`S2_Lieux_stage`** (référentiel des lieux d'accueil avec quotas), créé par
**chirurgie du zip** (aucune feuille existante touchée). Colonnes : Lieu / structure · Service ·
Commune · Niveau concerne (vide = tous) · Quota (nb max de stagiaires par séance) ·
Periode de disponibilite. Onglet saisissable (droits du module Stages).

Le champ **`Lieu de stage` de `S1_Stages`** n'est plus alimenté par la liste P0 simple
(`Lieux_stage`) mais par le référentiel S2, sous forme composite lisible
**« Lieu / structure — Service »** (Service facultatif : si vide, seul le lieu s'affiche). Ce libellé
composite est ce qui est stocké dans S1 et servira de clé pour le suivi des quotas.

### Classeur — nouveau md5 canonique
Ajout de l'onglet `S2_Lieux_stage` par chirurgie du zip. Intégrité vérifiée après opération :
24 onglets (était 23), **669 formules / 13 validations / 16 dessins / 2 noms définis inchangés**,
et **0 différence** sur les 669 valeurs calculées comparées. Nouveau md5 :
`fba973b7cb4ffcd1a143e49e62bf2ba9` (ancien 24 onglets... non : ancien `9337d1a9...` = 23 onglets,
gelé V1.25→V1.27).

### Couches touchées
- Classeur : `S2_Lieux_stage` (chirurgie du zip, en-têtes seuls, vide de données).
- `config.py` : `MODULES_ONGLETS["Stages"]` (+ S2), `ONGLETS_SAISIE_ACTIVE` (+ S2), `GUIDE_STRUCTURE`
  (menu, section Étudiants), `LISTES_ONGLET_COMPOSITE` (« Lieux de stage (S2) »),
  `DICTIONNAIRE_SUPPLEMENT` (champs de S2) et `DICTIONNAIRE_SURCHARGE` (S1 « Lieu de stage » → S2).
- `metier.py` : `dictionnaire_par_onglet()` fusionne supplément + applique surcharge (sans modifier
  l'onglet Dictionnaire du classeur).
- Doc : README, doc des écrans, ETAT.

> Choix d'implémentation : le Dictionnaire des champs de S2 et la nouvelle source de S1 sont gérés
> par surcharge applicative (`config`), pas dans l'onglet Dictionnaire du classeur, pour ne pas
> toucher une feuille existante. L'application (y compris la page Dictionnaire) reflète tout
> correctement. Synchroniser l'onglet Dictionnaire du classeur reste une piste possible ensuite, sans engagement.

### Reste a faire (suite du module Stages)
- **Saisie assistée — contrôle de quota** : à la saisie d'une ligne `S1_Stages`, afficher les places
  restantes pour le lieu choisi selon l'année et le numéro de séance (places = quota − affectations
  déjà enregistrées pour ce lieu/cette séance/cette année), sans blocage (contrôle humain).
- **Tableau de bord stages** : nombre d'étudiants affectés, nombre de lieux, places disponibles /
  occupées, taux d'occupation, répartition par promotion.
- Données réelles (lieux + quotas) à saisir au déploiement.

## Ce qui change en V1.27

### E2 — écart programmé vs constaté (affichage)
La consultation du relevé d'heures (`E2_Releve_heures`) affiche une colonne calculée
**« Ecart (prog. - constate) »** = Vol. horaire prog. − Vol. horaire constate. Signe explicite
(`+` si le programmé dépasse le constaté), sans décimale inutile, virgule décimale tolérée à la
saisie. L'écart n'apparaît **que lorsque les deux valeurs sont saisies** (sinon un programmé seul
afficherait un faux écart). Colonne marquée « calcul » (lecture seule), absente du formulaire de saisie.

Rappel de cadrage : `Vol. horaire prog.` et `Vol. horaire constate` restent **saisis à la main** ;
on ne relie pas E2 à la maquette (E2 est indexé par mois + enseignant, la maquette par
matière/filière/niveau ; les relier passerait par les emplois du temps, écarté par décision).

### Aucune modification du classeur
`EMSP_V1.xlsx` inchangé (md5 `9337d1a9fe74b2e61d5f45e9749479a9`). L'écart est calculé à l'affichage ;
aucune colonne ajoutée au classeur, aucune formule modifiée.

### Couches touchées
- `metier.py` : `_num_h` (conversion robuste), `_fmt_ecart`, `_ecart_prog_constate` ;
  nouveau mécanisme `COLONNES_AFFICHAGE_EXTRA` (colonnes virtuelles calculées, ajoutées en fin de
  table à l'affichage seulement) ; `table()` applique ces colonnes. Réutilisable pour d'autres onglets.
- Doc : README, doc des écrans, ETAT.
- Aucune autre couche (pas de changement de config, d'app.py ni de template : le rendu de table est générique).

### Reste a faire
- Module **Stages** (affectation + quotas + tableau de bord), puis module **Notes/relevés**
  (fichier séparé `EMSP_Notes.xlsx`, délibération/compensation selon décret 05-106) avec
  avertissement/surveillant.

## Ce qui change en V1.26

### A3 « Matiere » en suggestions (datalist) alimentées par la maquette R1
Le champ `Matiere` des séances (`A3_Sessions`) passe d'une saisie texte libre à une saisie
**libre avec suggestions** : la liste proposée vient de la maquette `R1_Maquettes`, filtrée par
la **Filière + le Niveau + le Semestre** de la ligne en cours. La saisie reste libre (on peut
taper une matière hors maquette) — ce sont des suggestions, pas une liste stricte.

Option associée : quand la matière saisie correspond à la maquette, le champ
**`Vol. horaire prog.` est pré-rempli** avec la somme des heures programmées (« Total heures »).
Pré-remplissage **uniquement si le champ est vide** (jamais d'écrasement d'une saisie manuelle) ;
la valeur reste modifiable.

Filtrage et pré-remplissage faits **côté client** (hors-ligne, aucun réseau) à partir des lignes
maquette injectées en JSON dans la page.

> Point d'attention référentiel : la maquette code le **semestre en cursus** (`1..6`) alors que
> A3 saisit le **semestre de l'année** (`S1`/`S2`). Le client **dérive** le semestre cursus de
> (Niveau, Semestre) : L1·S1=1, L1·S2=2, L2·S1=3, L2·S2=4, L3·S1=5, L3·S2=6. Si le niveau n'est pas
> L1/L2/L3 (ex. AS, Master), le filtre semestre est ignoré (on filtre Filière+Niveau seuls). À
> arbitrer plus tard si l'on veut harmoniser les conventions de semestre entre R1 et A3.

### Aucune modification du classeur
`EMSP_V1.xlsx` inchangé (md5 `9337d1a9fe74b2e61d5f45e9749479a9`). Le Dictionnaire garde
`A3_Sessions / Matiere` en `Texte` (suggestions ≠ liste stricte). Pas de chirurgie du zip.

### Couches touchées
- `config.py` : `MAQUETTE_DATALIST` (déclaration des champs matière/volume + filtres, par onglet).
- `metier.py` : `maquette_lignes_datalist()` (lignes compactes f/n/s/m/h), `maquette_datalist_cfg()`
  (résout libellés propres → `name` HTML) ; `champs_saisie()` pose la clé `datalist` sur le champ matière.
- `app.py` : `module()` passe `maquette_cfg` + `maquette_lignes` au template pour les onglets concernés.
- `templates/module.html` : rendu `<input list>` + `<datalist>` + script local de filtrage et de
  pré-remplissage.
- Doc : README, doc des écrans, ETAT.

### Décision actée (pour le futur lot Notes)
Les **notes d'examens** seront stockées dans un **fichier séparé** `EMSP_Notes.xlsx` à accès
restreint (clé = matricule), et non dans un onglet protégé du classeur unique. Motif : seule la
séparation physique du fichier garantit une confidentialité réelle hors application ; la protection
d'onglet Excel se contourne. Côté code, prévoir `WORKBOOK_NOTES` dans `config.py` + un chemin de
lecture/écriture dédié dans `data.py`, et une consigne de sauvegarde séparée. À implémenter au lot Notes.

### Reste a faire
- E2 : afficher programmé (maquette) vs constaté + écart (lot court, ne touche pas au classeur).
- Puis module **Stages** (affectation + quotas + tableau de bord), puis module **Notes/relevés**
  (fichier séparé, délibération/compensation selon décret 05-106) avec avertissement/surveillant.

## Ce qui change en V1.24

### Authentification reelle (identifiant + mot de passe) + journal d'audit
Remplace le simple selecteur de role par une vraie connexion. Les DROITS restent definis par l'admin
dans `P1_Roles` ; l'identite (login + mot de passe) et la tracabilite vivent dans des fichiers LOCAUX
hors depot.
- **Connexion** par identifiant + mot de passe (`/login`), deconnexion, changement de mot de passe
  (`/mot-de-passe`). Garde `before_request` : tout exige une session ; changement force au 1er login
  ou apres reinitialisation.
- **Gestion admin** (`/autorisations`) : creation de compte avec mot de passe initial, reinitialisation,
  suppression (retire aussi l'acces). Etat du compte affiche. Superadmin garanti par le code.
- **Securite depot public** : mots de passe JAMAIS en clair, JAMAIS dans le classeur ni le zip ; seules
  des empreintes `pbkdf2:sha256` dans `instance/comptes.json` (local, gitignore, hors zip). Le classeur
  pousse ne contient que logins + droits.
- **Journal d'audit** (`/journal`, admin) : trace locale append-only « qui a fait quoi, quand »
  (connexions, saisies, tresorerie, import, droits, mots de passe). Aucun secret. `instance/journal.csv`
  (local, gitignore, hors zip).
- **"Saisi par"** devient fiable : c'est l'utilisateur reellement authentifie.

NOTA premier lancement : superadmin / mot de passe `admin` (constante SUPERUSER_MDP_DEFAUT), a changer
immediatement (impose par l'appli). Le fichier `instance/` se cree au runtime sur le poste, il n'est ni
dans le depot ni dans le zip.

Aucune modification du classeur (md5 `0614d315d830492c8407121ebe3b694b`, 22 onglets, 669 formules).

### Reste a faire
- (Couche requetes et droits : complets.) Points de confort eventuels : export du journal en Excel,
  colonne "Saisi par"/horodatage sur d'autres onglets de saisie si besoin de tracabilite fine par ligne.

## Ce qui change en V1.23

### Couche requetes — 2e brique : Q3 + tableau croise (LECTURE SEULE)
- **Vue absences (Q3)** : unifie absences en cours (A2, Present != O) et observations/plaintes de
  stage (S1). Filtres etudiant + origine. Nuances documentees : A2 sans commentaire ; absence stage
  non modelisee => on remonte l'observation S1.
- **Tableau croise (pivot)** : 1-D ou 2-D, mesures Nombre/Somme/Moyenne, totaux ponderes corrects.
  Route /requetes/pivot, export Excel.

=> Les **5 questions** de la Direction sont couvertes (Q1 a Q5) + explorateur generique + pivot, chacun
exportable en Excel. Aucune modification du classeur (md5 `0614d315d830492c8407121ebe3b694b`).

### Reste a faire
- **Explication de la matrice des droits** (Nota 1) : seul point ouvert. Clarifier droits (qui PEUT
  lire/ecrire par role) vs tracabilite/log (qui A SAISI ; aujourd'hui seul le champ "Saisi par" de F1
  et des registres existe ; un journal d'audit "qui a modifie quoi quand" reste a decider, cf. AFD).

## Ce qui change en V1.22

### Couche requetes multicriteres (point 2 — premiere brique) — LECTURE SEULE
Donne a la Direction la puissance d'Excel sans ouvrir une copie du fichier. Hub **Requetes & analyses**
(Finances & pilotage).
- **Explorateur generique** : n'importe quelle table, jusqu'a 3 filtres cumulatifs (contient/egal/
  debut/sup/inf/nonvide/vide), tri numerique-aware, choix des colonnes, export Excel.
- **4 vues metier** sur les questions recurrentes : Q1 equipements & localisation (M1), Q2 salles
  occupees/reservees = **union cours A3 + reservations L2**, Q4 equipements par bailleur (+ total),
  Q5 ecart programme/constate enseignants sur une periode.
- **Export Excel** de chaque selection (`_xlsx_simple`) — la soupape anti "copie Excel".

Aucune modification du classeur (md5 `0614d315d830492c8407121ebe3b694b`, 22 onglets, 669 formules).

### Reste a faire
- **Couche requetes — 2e brique** : vue **absences eleves cours/stage** (Q3, avec ses nuances :
  A2 sans commentaire, absence stage non modelisee, observations via S1) + **tableau croise leger**
  (pivot, pandas).
- **Explication de la matrice des droits** (Nota 1) : droits (qui PEUT) vs tracabilite/log (qui A SAISI ;
  aujourd'hui seul "Saisi par" de F1 ; journal d'audit a discuter pour l'AFD).

## Ce qui change en V1.21

### Edition imprimable "Situation de compte" (point 1 de la feuille de route)
Registre mensuel signe (Gestionnaire + Directeur) reproduisant le document papier transmis. Choix
compte + periode (MM/AAAA) ; report a nouveau (solde initial + mouvements anterieurs) ; mouvements de
la periode avec solde courant ligne a ligne ; "SOLDE AU JJ/MM/AAAA". Convention du document actee :
Debit = Recette, Credit = Depense, Solde = Debit - Credit (= recettes - depenses, coherent F2).
Document parametrable (modele SITUATION_COMPTE), deux signataires. Lecture seule F1/F2.

### Aucune modification du classeur
Code pur (extension du module Impressions). md5 inchange (`0614d315d830492c8407121ebe3b694b`),
22 onglets, 669 formules.

### Reste a faire (dans l'ordre)
2. **Couche requetes multicritères** (lecture seule) : explorateur par table + 5 vues metier predefinies
   + tableau croise leger + export Excel de chaque selection.
3. **Explication de la matrice des droits** (Nota 1) : droits (qui PEUT) vs tracabilite/log (qui A
   SAISI ; aujourd'hui seul "Saisi par" de F1 ; journal d'audit a discuter pour l'AFD).

## Ce qui change en V1.20

### Saisie en grille du registre de tresorerie (priorite ergonomie bete)
Constat terrain (document "Situation de compte" + fiches A/B/C/D, toutes des grilles) : le formulaire
ligne par ligne est contreproductif pour saisir un registre. On passe la **grille comptable avant** la
couche requetes (decision actee). Ecran **Tresorerie -> Saisie en grille** : un compte choisi, solde
d'ouverture = solde courant, plusieurs lignes en mode tableur, **solde recalcule en direct**, un seul
enregistrement par lot. Colonnes dans l'ordre du registre (Recette OU Depense par ligne, sens deduit).
Saisie **atomique** (ligne invalide => rien ecrit, saisie conservee, erreurs detaillees). Lignes vides
ignorees.

### Aucune modification du classeur
V1.20 est du **code pur** : ecriture dans l'onglet F1 existant via la nouvelle primitive
`data.ajouter_lignes` (ajout par lot, une seule ouverture). **md5 inchange (`0614d315d830492c8407121ebe3b694b`)**,
22 onglets, 669 formules. La fenetre additive du classeur reste fermee.

### Reste a faire (dans l'ordre)
1. **Edition imprimable "Situation de compte"** (registre mensuel signe Gestionnaire/Directeur) —
   reproduit le document papier ; calage a confirmer : Chapitre = Poste budgetaire, N de cheque =
   Mode paiement + Reference, ligne d'ouverture "report a nouveau", convention debit/credit.
2. **Couche requetes multicritères** (lecture seule) : explorateur par table + vues metier predefinies
   (les 5 questions : equipements & localisation ; salles reservees et quand = cours U locations ;
   absences eleves cours/stage + observations ; equipements par bailleur ; ecart prog/constate
   enseignants par periode) + tableau croise leger + export Excel de chaque selection.
3. **Explication de la matrice des droits** (Nota 1) : clarifier droits (qui PEUT) vs tracabilite/log
   (qui A SAISI — aujourd'hui seul le champ "Saisi par" de F1 existe ; un journal d'audit reste a
   discuter, cf. demande AFD).

## Ce qui change en V1.19

### Deux registres en vue de la couche « requêtes multicritères »
Préparation d'un futur module de requêtes type Excel (filtres + croisements) pour donner à la
Direction le sentiment de pouvoir tout interroger sans ouvrir une copie du fichier ailleurs.
Première étape : créer les surfaces de données qui manquaient.

- **`L2_Reservations`** — réservations de salles **hors cours** (datées, ponctuelles), tenues à
  part de l'emploi du temps récurrent `A3_Sessions`. Décision actée : table séparée (≠ intégrer
  dans A3), car nature différente (datée vs jour-type récurrent).
- **`M1_Equipements`** — **mini-registre d'immobilisations** (décision actée : vrai registre, pas
  seulement une vue financière F1) : équipement ↔ salle ↔ bailleur. **Inventaire de pilotage
  uniquement** ; la maintenance (pannes, contrats, pièces) reste hors périmètre (futur GMAO).

Les deux sont de **vrais onglets de données** (saisie générique, Dictionnaire, droits, capacité),
intégrés à une nouvelle catégorie de droits **Logistique**. Listes : **Bailleurs** (P0, déjà
partagée avec F1) et **Categories_equipement** (P0, nouvelle). Codes auto `RES-n` / `EQ-n`.
Correctif : `_prochain_code` résout désormais le libellé **brut** (les clés L2/M1 portent `(*)`).

### Couplage classeur — dernier lot additif avant la bêta
Ajout **additif** : 2 onglets + 1 colonne P0 + 21 lignes au Dictionnaire. **669 formules inchangées**,
**22 onglets** (recalcul LibreOffice : `success`, 0 erreur). **Nouveau md5 :
`0614d315d830492c8407121ebe3b694b`** (2 copies byte-identiques racine + `data/`). C'est **le dernier
lot qui touche le classeur** ; la suite est en lecture seule.

### Décisions de cadrage (questions multicritères de la Direction)
Faisabilité établie sur 5 questions types : (1) équipements + localisation = M1/L1 ; (2) salles
réservées et quand = A3 (cours) ∪ L2 (locations) ; (3) absences élèves cours (A2) + observations
stage (S1) — pas de commentaire au niveau cours, absence stage non modélisée ; (4) équipements par
bailleur = M1 ; (5) écart programmé/constaté enseignants = E2, par mois ou cumulé (pas de granularité
jour/semaine). Q2 et Q4 nécessitaient les deux registres ci-dessus → faits.

### Prochaine étape — V1.20 : couche requêtes (LECTURE SEULE, aucune modif classeur)
Explorateur multicritères par table (filtres/tri/colonnes) + vues métier prédéfinies (les 5 questions)
+ tableau croisé léger (pandas) + **export Excel de chaque sélection** (la soupape qui évite d'aller
« taper » dans une copie). Tout en lecture seule sur le classeur maître.

## Ce qui change en V1.18

### Module « Impressions & éditions »
Nouveau module d'édition des documents courants, **100 % hors-ligne** (HTML + `@media print`,
impression/PDF via le navigateur). **6 documents + 1 export :** liste d'étudiants (filtrable A1),
feuille de présence vierge (60 lignes), **relevé d'heures individuel** (paie, E2+E1),
récapitulatif mensuel des heures (tous enseignants + total général), reçu de paiement numéroté
(F1, n° **REC-AAAA-NNNN** par scan, réservé financier), attestation de passage (simple), et
**export Excel** du tableau de bord (.xlsx openpyxl, synthèse + 5 tables).

**Modèles persistants éditables** : parties fixes (en-tête, titre, corps à jetons `{…}`, mentions,
signataire, nb copies) réglées dans **Paramétrages → Modèles de documents**, stockées dans le classeur.
Retouche ponctuelle possible sur l'aperçu avant impression.

### Décisions actées (confirmées)
- Relevé d'heures : **les deux** — individuel (paie) **et** récapitulatif mensuel. Le relevé
  **individuel passe en V1** (retiré des candidats V2).
- N° de reçu **scan-based** (dérivé du MAX de *Référence / N pièce* de l'année + 1), pas de compteur disque.
- Feuille de présence vierge : 60 lignes, en-tête à remplir à la main.

### Couplage classeur — dernière modif additive avant bêta
Ajout **additif** de l'onglet `D1_Modeles_docs` (texte, **aucune formule**). Les 19 onglets et
**669 formules** existants sont **inchangés** (recalcul LibreOffice : `success`, 0 erreur, 669 formules,
20 onglets). **Nouveau md5 du classeur : `805efa5278fab397eb1f90b9536d3d60`** (2 copies byte-identiques :
racine + `data/`). C'est la **dernière modification additive** ; à partir de la bêta, plus aucune
modification du classeur.

### Couches touchées
`config` (VERSION 1.18, `MODELES_DOCS`, menu ED_Modeles/ED_Impressions, `SPECIAL_ROUTES`,
`D1_Modeles_docs` dans `ONGLETS_DIRECTION`) · `metier` (lecture/écriture modèles, builders des
6 documents, `_prochain_recu`, `export_tdb_xlsx`) · `app` (routes `/impressions`, `/modeles`,
vues d'impression, export, `/api/releve-individuels`) · templates `impressions.html`, `modeles.html`,
`imprimer.html` + `static/css/print.css` · boutons contextuels sur A1/F1. `data.py` **inchangé**
(réutilise `ecrire_lignes_lot`). Tests métier + smoke-test Flask : tous passants.

## Ce qui change en V1.17

### Réorganisation du menu (ergonomie pré-test) — AUCUNE modification du classeur
Trois regroupements demandés avant le test, purement au niveau de la **navigation**
(`config.GUIDE_STRUCTURE`, qui pilote le menu latéral ET les cartes d'accueil). On passe de
**6 à 4 sections** :
1. **Paramétrages** (ex-« Avant de commencer ») — Paramètres & listes · Rôles & droits · Import CSV.
2. **Étudiants** — Fiches & inscriptions · Présences par créneau · **Stages (affectation & fiches
   retour)** · Documents & attestations. *(Stages rapatrié ici : la présence en stage est la même
   notion de suivi de l'étudiant.)*
3. **Enseignements & salles** — inchangée.
4. **Finances & pilotage** — Recettes & dépenses · Comptes & caisses · **Tableau de bord · Plan
   d'action · Documents officiels · Matrice des autorisations** *(ex-section Pilotage intégrée)*.
- **Modèle de droits INCHANGÉ.** `MODULES_ONGLETS` (Académique / Présences / **Stages** /
  Enseignants / **Financier**) est indépendant du menu : déplacer un module dans le menu ne change
  pas qui a le droit d'y écrire. La scolarité garde son droit Stages ; le financier reste verrouillé
  Compta/Direction. La matrice des autorisations reste cohérente.
- **Couches touchées** : `config.GUIDE_STRUCTURE` + bump VERSION 1.17 ; `app.tableau_bord` passe
  désormais `info=TAB_INDEX["TDB_Direction"]` ; `tableau_bord.html` fil d'Ariane rendu **dynamique**
  (`{{ info.section_titre }}`) au lieu du « Pilotage » codé en dur. README, doc des écrans, ETAT.
- **Aucune autre couche** : data/metier/app (hors la ligne de contexte ci-dessus) inchangés ; le
  menu et l'accueil itèrent les sections de façon générique (numéros, titres, modules) → renumérotation
  automatique. `TAB_INDEX` se reconstruit depuis `GUIDE_STRUCTURE`.

### Correctif lancement Windows — run.bat en CRLF
`run.bat` était en fins de ligne **LF seules** (défaut présent depuis V1.16) : sous `cmd.exe` les
blocs `if (...) else (...)` et la ligne `&& (set…) || (set…)` échouaient (fenêtre qui se ferme /
« ( n'était pas attendu »). Réécrit en **CRLF**, structure if/else classique, détection de Python,
messages d'erreur explicites et `pause` en cas d'échec (venv/pip/app). Aucun autre fichier touché.

Tests : `py_compile` config/data/metier/app OK ; structure = 4 sections bien composées ;
`TAB_INDEX` rattache S1_Stages→Étudiants, TDB/MAT/G1/H1→Finances & pilotage, P0→Paramétrages ;
`MODULES_ONGLETS` identique ; Flask : `/`, `/tableau-de-bord`, `/module/A1_Etudiants`,
`/autorisations` → 200 ; menu rendu contient « Paramétrages », « Finances &amp; pilotage »,
« Stages — affectation » sous Étudiants, et ne contient plus « Avant de commencer », « Pilotage »,
« SECTION 5/6 ». **Classeur non touché (md5 identique à V1.16).**

## Ce qui change en V1.16

### Import CSV national (IMPORT_zone) — écran dédié
- **Écran `/import`** (menu *Avant de commencer*), réservé **Direction**. On **colle le CSV** national
  (séparateur auto tab/`;`/`,`, en-tête ignorée) → remplit la zone de staging IMPORT_zone (7 colonnes).
- **Statut vs base** en Python live : **NOUVEAU** (matricule absent de A1) / **EXISTANT** + compteurs.
- **Import MANUEL** : la copie des NOUVEAU vers A1 reste **manuelle** ; la zone **ne modifie jamais A1**.
- **Retour en arrière** : instantané disque (`import_undo.json`) avant chaque import/vidage ; bouton
  **Annuler** = restauration (1 niveau). Boutons Importer / Vider / Annuler.
- **data** : `remplacer_donnees` (vide+réécrit, formules recopiées). **metier** : `parser_csv`,
  `import_zone_brut`, `importer_csv`, `vider_zone_import`, `annuler_import`, `import_resume`,
  `CALC_AFFICHAGE["IMPORT_zone"]`. **app** : routes /import (+importer/vider/annuler) + garde Direction.
  **config** : SPECIAL_ROUTES IMPORT_zone→import_csv ; VERSION 1.16. **template** : import.html.
  **Aucune modification du classeur.**

### Correctif (latent) — vidage de cellule openpyxl
`ws.cell(r, c, value=None)` **n'efface pas** la cellule (paramètre ignoré) → corrigé en
`ws.cell(r, c).value = None` dans `remplacer_donnees` et `supprimer_ligne_par_cle`. Sans ce correctif,
la suppression d'une ligne **du milieu** de P1_Roles aurait laissé un doublon. Testé.

Tests (metier + Flask) : routing /module/IMPORT_zone→/import ; NOUVEAU/EXISTANT + compteurs ;
import → annuler → vide ; import1 → import2 → annuler → revient à import1 ; vider → annuler → revient ;
détection d'en-tête robuste ; droits Direction (compta 403) ; suppression milieu P1 sans doublon ;
livrable inchangé (md5 = V1.15) et IMPORT_zone vide.

### Chantiers d'ergonomie à venir (demandés, à planifier)
- Retirer des interfaces les **références au cahier des charges** (codes A1, A4…) → libellés parlants.
- **Icône par module** pour le repérage visuel.
- **Page d'accueil** plus conviviale.

## Ce qui change en V1.15

### Saisie F2_Comptes — formulaire générique (module financier complet)
- **Décisions** : Nom du compte ← P0 `Comptes_caisses` (cohérence F1↔F2 pour le SUMIF) ; Solde
  courant = **affichage Python LIVE** ; Type inline.
- **3 champs saisissables** (Solde courant exclu/calcul). Obligatoires : Nom du compte, Solde initial.
  Accès Comptabilité + Direction.
- **config** : F2 dans ONGLETS_SAISIE_ACTIVE ; LISTES_INLINE += Banque/Caisse/Autre ; VERSION 1.15.
- **metier** : `_solde_courant_f2` (initial + Σ recettes − Σ dépenses du compte d'après F1) +
  helpers `_num`/`_fmt_kmf` ; `CALC_AFFICHAGE["F2_Comptes"]` ; **`_appliquer_calc_affichage` recalcule
  désormais TOUJOURS** (le cache Excel d'une colonne calcul est périmé après une saisie F1 dans l'IHM).
- **module.html** : aide F2.
- **Classeur** : Dictionnaire F2/Nom du compte Texte → Liste (source Comptes_caisses, ligne 110).
  Recalculé **0 erreur** (669 formules) ; copies racine/data byte-identiques ; F2 vide.

Tests (metier + Flask) : 3 champs (Solde courant exclu) ; Nom du compte ← Comptes_caisses ; Type
inline ; **Solde courant LIVE = 75000** (100000 + 5000 − 30000) ; droits compta+direction, scolarité
403 ; non-régression E2 (Total = constaté) ; F2 vide au livrable (les lignes 3-51 = formule pré-posée,
lues à vide par le chemin app data_only).

## Ce qui change en V1.14

### Saisie F1_Mouvements (trésorerie) — formulaire générique
- **Décisions** : Catégorie = liste **combinée** Cat_Recettes + Cat_Depenses (A-a) ; montants =
  **validation conditionnelle** selon le Sens (B-b) ; Date opération défaut @today ; **Saisi par
  auto = login** courant ; Compte/caisse ← P0 Comptes_caisses (cohérence future avec F2).
- **15 champs saisissables** (Saisi par exclu du formulaire, injecté serveur). Obligatoires : Date
  opération, Sens, Catégorie, Compte/caisse, Libellé. Accès Comptabilité + Direction (financier=O).
- **config** : F1 dans ONGLETS_SAISIE_ACTIVE ; LISTES_INLINE += Recette/Depense, Previsionnel/Realise ;
  SAISIE_DEFAUTS F1 (@today) ; `CHAMPS_AUTO_LOGIN={"F1_Mouvements":["Saisi par"]}` ; VERSION 1.14.
- **metier** : options_liste gère le motif **"X OU Y"** (listes P0 combinées) ; champs_saisie exclut
  les CHAMPS_AUTO_LOGIN ; valide_saisie appelle un registre `_VALIDATIONS_SPECIFIQUES` ;
  `_valide_f1_mouvements` (montant ⇔ sens).
- **app.py** : module_ajouter injecte Saisi par = login courant.
- **module.html** : aide F1 (saisie + dépendance P0).
- **Classeur** : **aucune modification** (toutes les sources se résolvent). md5 = V1.13.

Tests (metier + Flask) : 15 champs (Saisi par exclu) ; Catégorie combinée ; Sens/Statut inline ;
défaut date ; validation conditionnelle (Recette⇒montant recette requis, dépense vide ; et inversement) ;
Saisi par auto = login ; droits compta+direction, scolarité 403.

> **Dépendance P0** : avant saisie F1, remplir `Cat_Recettes`, `Cat_Depenses`, `Comptes_caisses`
> (obligatoires) et éventuellement `Postes_budgetaires` (non pré-amorcés, spécifiques à l'école).

## Ce qui change en V1.13

### Administration des droits + superutilisateur (anti-blocage)
- **Matrice des autorisations éditable** par les administrateurs. Répond à la demande : l'admin
  informatique ET le directeur peuvent gérer les droits (sauvegarde mutuelle), et le client est
  **superutilisateur** d'accès garanti.
- **`Admin droits (O/N)`** ajouté à P1_Roles (directeur=O pré-amorcé). Porteurs = administrateurs.
- **Superutilisateur** `config.SUPERUSER_LOGINS=["superadmin"]` (renommable, 1 ligne) : accès total +
  admin **garantis par le code** même si P1_Roles vide/cassé ; **non supprimable ni rétrogradable**.
  Ligne `superadmin` livrée (sélectionnable). => **aucun verrouillage irréversible possible**.
- **Écran admin** (si rôle courant admin) : tableau utilisateurs + formulaire upsert (login, rôle,
  cases lecture/écriture par module + Tous, financier, admin) + suppression confirmée.
- **Garde-fous** : superuser intouchable ; **dernier administrateur non retirable** ; POST réservés
  admin (403 sinon).
- **metier** : roles() enrichi (admin/superuser), `est_admin`, `enregistrer_utilisateur`,
  `supprimer_utilisateur`, `utilisateurs_admin`. **data** : `supprimer_ligne_par_cle` (onglets sans
  colonne calcul). **app** : routes `/autorisations/utilisateur` + `/autorisations/supprimer` +
  `_exige_admin` + `est_admin_courant` au contexte. **template** : `autorisations.html` (UI admin +
  matrice lecture seule). **config** : VERSION 1.13, `SUPERUSER_LOGINS`, `GROUPES_DROITS`, `GROUPE_TOUS`.
- **Classeur** : colonne `Admin droits (O/N) (**)` + ligne `superadmin` + ligne doc Dictionnaire.
  Recalculé **0 erreur** (669 formules) ; copies racine/data byte-identiques ; P1 = 5 rôles de
  référence (propre).

Tests (metier + Flask) : gardes non-admin (403) ; superuser protégé (édition/suppression refusées) ;
upsert sans doublon ; suppression OK ; superuser garanti même synthétisé ; UI admin visible pour
direction, masquée pour scolarité ; classeur **0 erreur**.

## Ce qui change en V1.12

### Matrice des autorisations — page de gouvernance (lecture seule)
- Nouvelle page **Pilotage → Matrice des autorisations** (`/autorisations`). Lecture seule, modèle
  de droits **inchangé**. Répond à la demande Direction « savoir qui a le droit de faire quoi ».
- **Tableau rôles × modules** (depuis `P1_Roles` + `MODULES_ONGLETS`) : Lecture (déclarée) / Écriture
  (effective via `peut_ecrire`, inclut verrou Accès financier) / L+É / — , + colonne Accès financier.
- **Tableau découpage** module → onglets (pour décider d'éventuels regroupements).
- **metier** : `matrice_autorisations()` + `peut_lire()`. **app.py** : route `/autorisations`.
  **config** : VERSION 1.12, entrée menu Pilotage `MAT_Autorisations`, `SPECIAL_ROUTES`.
  **templates** : `autorisations.html`. **Aucune modification du classeur.**
- Disclosure : la **lecture n'est pas encore restreinte** dans l'IHM (seule l'écriture l'est) ; la
  colonne Lecture reflète l'intention déclarée dans P1_Roles (noté sur la page).

Tests : matrice correcte (Direction = tout ; Scolarité = Académique+Stages en R+É ; Compta =
Finances ; Chef dépt = Académique/Enseignants en lecture, Présences en écriture) ; page rendue 200 ;
lien menu présent ; `/module/MAT_Autorisations` redirige (302).

## Ce qui change en V1.11

### Lien Séances ↔ salles (A3_Sessions / Salle ← L1)
- Le champ `Salle` de A3 passe de texte libre à **liste déroulante ← L1** (noms de salles).
  **Facultatif** (Salle non obligatoire) → aucune dépendance bloquante.
- **config** : `LISTES_ONGLET["Salles (L1)"] = ("L1_Salles","Nom / libelle")` ; VERSION 1.11.
- **metier** : aucun code nouveau (LISTES_ONGLET déjà géré par `options_liste`).
- **module.html** : aide A3 complétée (Salle ← L1).
- **Classeur** : Dictionnaire `A3/Salle` `Texte`→`Liste` (source « Salles (L1) », ligne 52).
  Recalculé, **0 erreur** (669 formules) ; copies racine/data byte-identiques.
- **Valeur stockée = nom** (le rattachement `_seance_dans_salle` matche par nom OU id ; reste lisible).

Tests (copie ensemencée) : A3 `Salle` = liste (options = noms L1), **optionnelle** ; ajout séance
avec « Amphi A » → occupation `SAL-1` = 1 séance (rattachement par nom) ; classeur **0 erreur**.

## Ce qui change en V1.10

### Saisie L1_Salles — formulaire générique
- **Décisions** : ID salle auto-suggéré `SAL-<n>` (oui) ; salles **créées par l'école** (livrable
  vierge) ; types de salles = amphi/TD/TP/cours → **Amphithéâtre ajouté** à `Types_salle`.
- **config** : `L1_Salles` dans `ONGLETS_SAISIE_ACTIVE` ; `SAISIE_DEFAUTS["L1_Salles"]["ID salle"]
  = "@next_sal"` ; VERSION 1.10.
- **metier** : pré-suggestion de code **généralisée** `_prochain_code(onglet, colonne, prefixe)`
  (NC pour E1, SAL pour L1) ; `champs_saisie` résout `@next_sal`.
- **module.html** : aide L1.
- **Classeur** : seule modif = valeur de référence `Amphitheatre` ajoutée à `Types_salle` (P0, L6).
  Recalculé, **0 erreur** (669 formules) ; copies racine/data byte-identiques ; L1 vierge.

Tests (copie ensemencée) : 6 champs (obligatoires ID salle, Nom/libellé) ; ID salle défaut `SAL-1`
puis `SAL-2` après ajout ; Type = Cours/TD/TP/Amphitheatre ; **droits scolarité + Direction**
(compta/chef_dept 403) ; ajout salle → remontée dans `salles()` (planning + fiche) ; non-régression
`_prochain_nc` (NC-2) ; classeur **0 erreur** (669 formules).

## Ce qui change en V1.9

### Saisie E2_Releve_heures — formulaire générique (1er écran à colonne calcul)
- **Décisions actées** : (a) **affichage Python** des colonnes calcul ; (b2) `Matricule ens.` =
  liste **lisible** « Matricule — Nom Prénom » mais **stocke le matricule seul** (clé paie + agrégat
  heures). 4 champs éditables (obligatoires : Mois/Année, Matricule, Vol. constaté).
- **config** : `E2_Releve_heures` dans `ONGLETS_SAISIE_ACTIVE` ; `LISTES_ONGLET_VALLABEL =
  {"Enseignants matricule (E1)": ("E1_Enseignants","Matricule ens.",["Nom","Prenom"])}` ; VERSION 1.9.
- **metier** : `options_liste()` gère les listes **valeur≠libellé** (renvoie `{value,label}`) ;
  `champs_saisie` **normalise toutes les options** en `{value,label}` ; nouveau registre
  `CALC_AFFICHAGE` + `_appliquer_calc_affichage()` appliqué par `table()` (Total = heures constatées,
  rempli seulement si la cellule lue est vide). Réutilisable F2/IMPORT.
- **module.html** : rendu `<option value=o.value>o.label</option>` ; aide E2.
- **Classeur** : Dictionnaire `E2/Matricule ens.` `Texte`→`Liste` (source « Enseignants matricule (E1) »,
  ligne 84). Recalculé, **0 erreur** (669 formules) ; copies racine/data byte-identiques ; E2 vierge.

Tests (copie ensemencée) : 4 champs éditables (Total exclu) ; Matricule options `{value,label}`
(value=matricule, label « Matricule — Nom Prénom ») ; inline `{value,label}` sans régression ;
droits (Direction écrit, scolarité/compta/chef_dept **403**) ; ajout relevé → **matricule stocké =
NC-1**, **Total affiché = 20 en Python** ; tableau de bord « heures par enseignant » OK (NC-1→20h) ;
classeur **0 erreur** (669 formules).

> **Point ouvert — matrice des autorisations (demande Direction, 15/06).** Pouvoir **savoir qui a le
> droit de faire quoi sur quel module**, et **redéfinir les découpages** (groupes Académique /
> Présences / Stages / Enseignants / Financier non figés). À traiter à part : (1) vue lisible
> rôles × modules (lecture/écriture + accès financier) dérivée de `P1_Roles` + `MODULES_ONGLETS` ;
> (2) configurabilité des groupes. Non développé en V1.9 ; modèle de droits inchangé.

## Ce qui change en V1.8

### Lien Séances ↔ formateurs (A3_Sessions / Enseignant ← E1)
- **Décision** : valeur stockée = **libellé lisible « Nom Prénom »** (le calendrier et les salles
  l'affichent tel quel, aucune résolution) ; le matricule reste la clé de E2. Liste déroulante =
  enseignants réels de E1 (fin de la saisie libre → plus de fautes de frappe). Ordre `Nom Prénom`
  paramétrable en une ligne.
- **config** : `LISTES_ONGLET_COMPOSITE = {"Enseignants (E1)": ("E1_Enseignants",["Nom","Prenom"]," ")}` ;
  VERSION 1.8.
- **metier** : `options_liste()` résout désormais une liste **composite** (plusieurs colonnes d'un
  autre onglet → libellé, distinct, trié).
- **module.html** : aide A3 (enseignant ← E1, renseigner E1 d'abord).
- **Classeur** : Dictionnaire A3/Enseignant `Texte` → `Liste`, source « Enseignants (E1) » (ligne 51).
  Recalculé, **0 erreur** (669 formules) ; les 2 copies (racine + data/) byte-identiques ; E1 et A3
  vierges.
- **Dépendance** : `Enseignant` obligatoire → saisir E1 **avant** les séances (liste vide sinon).

Tests (copie ensemencée) : `options_liste("Enseignants (E1)")` distincte + triée + dédoublonnée
(2 fiches + 1 doublon Nom/Prénom → 2 options) ; A3 `Enseignant` rendu en liste obligatoire pilotée
par cette source ; **liste vide** sur livrable vierge (dépendance) ; ajout A3 avec enseignant choisi
→ remonte dans `seances()` (calendrier/salles) ; classeur **0 erreur** (669 formules).

## Ce qui change en V1.7

### Saisie E1_Enseignants — formulaire générique
- **Décisions actées** : statut = liste **inline** `Titulaire/Vacataire` (choix (a) : ensemble fermé
  stable, géré en code ; impact d'un changement ultérieur = 1 ligne `config.LISTES_INLINE`, ou
  promotion en colonne P0 sans code métier si la Direction doit la gérer — données existantes
  préservées car stockées en texte). Matricule en **colonne unique** + convention **`NC-<n>`** pour
  les inconnus, **pré-suggéré automatiquement**.
- **config** : `E1_Enseignants` ajouté à `ONGLETS_SAISIE_ACTIVE` ; `LISTES_INLINE["Titulaire/Vacataire"]
  = ["Titulaire","Vacataire"]` ; `SAISIE_DEFAUTS["E1_Enseignants"]["Matricule ens."] = "@next_nc"` ;
  VERSION 1.7.
- **metier** : `_prochain_nc()` (scan E1, max+1, casse ignorée, ignore les vrais matricules) ;
  `champs_saisie` résout le token `@next_nc`.
- **module.html** : aide E1 (matricule clé, NC-<n>, statut). Pas d'autre couche modifiée.
- **Classeur** : **aucune modification** (la liste du statut est inline ; le Dictionnaire E1 pointait
  déjà `Titulaire/Vacataire`). Toujours 0 erreur (669 formules), E1 vierge.
- **Périmètre V1** : fiche enseignant (identité, statut, matières, département). Lien Séances ↔
  formateurs = **étape immédiatement suivante** (A3 `Enseignant` en liste ← E1, une fois E1 peuplé).

Tests (copie ensemencée, livrable resté vierge) : 9 champs (obligatoires Matricule/Nom/Prénom) ;
Statut=Titulaire/Vacataire, Genre=M/F ; `NC-1` à vide → `NC-6` après ensemencement (NC-2, nc-5, 12345)
→ `NC-7` après ajout de NC-6 ; obligatoire manquant rejeté ; **droits** : Direction écrit, scolarité /
compta / chef de dépt **403** ; ajout réel OK ; classeur **0 erreur** (669 formules), md5 inchangé.

> Observation droits : en l'état de `P1_Roles`, **seule la Direction** (`Tous`) a l'écriture sur E1
> (aucun rôle ne liste `Enseignants` en écriture ; `chef_dept` lit Enseignants mais n'écrit que
> Presences). Pour confier les fiches enseignants à la scolarité ou au chef de département, ajouter
> `Enseignants` à leurs modules d'écriture dans P1_Roles (paramètre éditable Direction). Non modifié
> ici (donnée de référence).

## Ce qui change en V1.6

### Saisie S1_Stages — formulaire générique
- Décisions : N° séance = nombre libre ; *Lieux_stage* **pré-amorcée** ; *Matricule* ← A1 ;
  *Fiche retour* défaut `N`.
- **Classeur** : P0 `Lieux_stage` amorcée (CHN El-Maarouf Moroni, CHR Mitsamiouli, Foumbouni, Hombo,
  Domoni, Fomboni — éditable Direction) ; Dico S1 *Matricule* → Liste ← A1.
- **config** : S1 ajouté à `ONGLETS_SAISIE_ACTIVE` ; `SAISIE_DEFAUTS["S1_Stages"]["Fiche retour (O/N)"]="N"`.
- **module.html** : aide S1. Version 1.6.
- **Périmètre** : référentiel lieux + affectation (6 séances) + suivi fiche retour + note/20 +
  observation libre. Grille d'appréciation détaillée (doc D) + plaintes fines = **candidats V2**.

Tests (copie ensemencée) : Matricule←A1, Année←Annees_acad, Lieu←Lieux_stage amorcée, Fiche retour
défaut N ; ajout OK (Direction + scolarité) ; obligatoire manquant rejeté ; comptabilité **403** ;
classeur **0 erreur** (669 formules). Livrable resté vierge (les lieux sont des paramètres de référence).



### Saisie A4_Documents_etud (registre documentaire) — formulaire générique
- Décision actée : listes *Type de document* et *Statut* gérées dans **P0_Parametres**
  (éditables Direction) ; *Matricule* ← A1, *Année concernée* ← liste `Annees_acad`.
- **Classeur** : 2 nouvelles colonnes-listes en P0 — `Types_document (**)` (Attestation de passage,
  Bulletin, Releve de notes) et `Statuts_document (*)` (En attente conseil → En attente delai →
  Imprimable → Remis). Bandeau-titre P0 ré-étendu (A1:Q1). Dictionnaire : 2 lignes P0 ajoutées +
  4 lignes A4 mises à jour (Type=Liste + source A1/P0). P0 passe de 15 à 17 listes.
- **Activation** : `A4_Documents_etud` ajouté à `ONGLETS_SAISIE_ACTIVE` (formulaire générique).
- **Valeurs par défaut** : `config.SAISIE_DEFAUTS` (résolu par `metier.champs_saisie`, rendu par
  `module.html`) → Date génération = `@today`, Statut = *En attente conseil*.
- **Périmètre** : A4 = registre/suivi. Génération PDF, remplissage auto, automatisation du cycle de
  validation = **candidats V2** (gros build, « SI POSSIBLE » du mail, hors-TDR).

Couches propagées : config → metier → module.html (défauts + aide A4) → classeur (P0 + dico) →
README → doc des écrans → ETAT. Tests (copie ensemencée) : listes Matricule←A1, Type/Statut←P0,
Année←Annees_acad ; défauts appliqués (date du jour, statut initial sélectionné) ; ajout OK ;
obligatoire manquant rejeté ; rôle comptabilité **403** sur A4 ; classeur **0 erreur** (669 formules).
Livrable resté **vierge** (les valeurs de listes P0 sont des paramètres de référence, pas des données).



### Saisie des présences PAR SÉANCE (A2_Presences) — écran dédié
- Décision actée (en réponse à la question de cadrage) : **saisie par lot / par séance**, et
  **Matricule/Session pilotés par A1/A3** (pas de texte libre). A2 reste **hors-TDR** (`(**)`,
  besoin du CR du 11/06) — choix délibéré d'une saisie de masse réaliste, documenté.
- Nouvel écran `/presences` (route `presences_saisie`), accessible par bouton depuis la page
  *Présences*. Choix Séance (liste A3) + Date (JJ/MM/AAAA) + Créneau (10/12/15/17, défaut déduit
  de l'heure de début) ; l'**effectif** est tiré de `A1_Etudiants` par Filière+Niveau+Section ;
  on coche les présents (boutons *Tout présent/absent*). « Saisi par » = login du rôle courant.
- **Anti-doublon** : nouvelle primitive `data.ecrire_lignes_lot(onglet, lignes, clés)` en **UPSERT**
  (clé Date+Matricule+Session+Créneau) — ré-saisir une séance **met à jour** au lieu de dupliquer.
  Mêmes garde-fous que `ajouter_ligne` (lecture seule, colonnes calcul, capacité, clés préservées).
- **Listes inter-onglets** : `metier.options_liste()` résout aussi une liste alimentée par une
  colonne d'un autre onglet (`config.LISTES_ONGLET`). Dictionnaire A2 mis à jour : Matricule ←
  « Étudiants inscrits (A1) », Session/Matière ← « Séances (A3) ».
- A2 **n'est PAS** ajouté à `ONGLETS_SAISIE_ACTIVE` (le formulaire générique ligne-à-ligne y reste
  désactivé) ; il passe par `config.ONGLETS_SAISIE_LOT = {A2_Presences: presences_saisie}`.

Couches propagées : config → data → metier → app → module.html + presences.html (nouveau) →
style.css → README → doc des écrans → ETAT. Dictionnaire (classeur) mis à jour.
Tests (sur copie ensemencée, livrable resté vierge) : roster filtré par section OK ; écriture
N lignes/élève ; **ré-saisie = mise à jour sans doublon** (2 → 2) ; multi-créneau (+2) ; rôle
scolarité **403** sur GET et POST ; classeur après écriture **0 erreur** (669 formules), dimensions
inchangées (A2 = A1:F300).

### Point ouvert traité partiellement
- A2_Presences (volumétrie) : la **stratégie dédiée** demandée avant activation est désormais en
  place (saisie par séance, pas ligne-à-ligne). La saisie de masse fonctionne ; reste à éprouver
  à l'usage sur de gros effectifs (554 élèves) en condition réelle.



### 1) Performance (correction d'un défaut de lecture)
- Symptôme V1.2 : pages très lentes (~5 s). Cause mesurée : la couche d'accès **rechargeait
  tout le classeur à chaque accès** à `self.wb` (jusqu'à ~90 fois par page, la V1.2 ayant ajouté
  au contexte de chaque page le calcul des alertes de capacité + lecture des rôles).
  **Ce n'était pas le volume** : dimensions du classeur inchangées (max_row=300), et étendre une
  plage dans une formule n'ajoute aucune cellule.
- Correctif : **cache du classeur par date de modification** (`data._CACHE_LECTURE`), invalidé
  explicitement après chaque écriture. ~90 chargements/page → 1. Mesuré : accueil 5022 ms → 79 ms.

### 2) Saisie A1_Etudiants & A3_Sessions
- **Formulaire d'ajout générique piloté par le Dictionnaire** : `metier.champs_saisie(onglet)`
  produit les champs (type, obligatoire, options de liste) ; `options_liste()` résout les listes
  depuis `P0_Parametres` (par libellé) ou `config.LISTES_INLINE` (jours, O/N, créneaux).
- Activé pour les seuls onglets validés : `config.ONGLETS_SAISIE_ACTIVE = [A1_Etudiants, A3_Sessions]`
  (les autres restent en lecture seule → déploiement incrémental).
- Route générique `POST /module/<onglet>/ajouter` : garde de rôle, validation des champs
  obligatoires côté serveur, capacité, écriture via `data.ajouter_ligne`.
- Une **séance** (A3) saisie apparaît aussitôt dans le **calendrier** et le **planning des salles**.

Couches propagées : config → data → metier → app → module.html → style.css → README → doc → ETAT.
Tests : pages <100 ms ; ajout A1/A3 vérifié ; ligne invalide (obligatoire manquant) rejetée ;
rôles (scolarité écrit A1+A3, compta refusé 403) ; classeur après écriture = 0 erreur, dimensions
inchangées (A1:O300, A3:N300).

## Acquis antérieurs (rappel)
- V1.2 : démarrage écriture sur `P0_Parametres` ; sélecteur de rôle (sans mot de passe) ;
  plages du classeur harmonisées à `CAPACITE = 50 000` ; alertes de capacité ; `F3_Journal_audit`
  retiré du Dictionnaire ; couche d'écriture (`ajouter_ligne` recopie le motif de formule → pas de
  limite de lignes).
- V1.1 : logo, calendrier mois/semaine/jour (projection hebdo), planning des salles, fiche salle.

## Point d'arrêt
**Matériel + expression de besoin** (V1.40 : M1 état éditable + onglet `L3_Besoins` ; classeur md5 `574f357617477a51daf2eac561b7db5a`). **Plan d'action (G1)** (V1.39 : Type d'écart + Statut en listes éditables). **Documents officiels** (V1.38 : catégories éditables + consultation groupée). **Affichage des grands tableaux** (V1.37 : recherche + filtres par colonne + pagination 20 + 1re colonne figée). **Présentation réorganisée** (V1.36) : menu + accueil en 3 ensembles (Scolarité / Administration /
Direction) avec sous-groupes, Paramétrage déporté à droite, mentions « V2 » nettoyées — **sans toucher à
l'Excel**. Module Notes complet, **barème N1 rempli** (L2 SI confirmé revalidé = 9,89 + squelettes
provisoires). Classeur principal **propre et inchangé** (`fba973b7cb4ffcd1a143e49e62bf2ba9`, 24 onglets,
669 formules) ; fichier notes livré avec barème pré-chargé, sans note ni signalement.

## Prochaine action prévue
Backlog issu de la réunion (présentation faite en V1.36). Lots suivants, dans l'ordre proposé :
1. ~~Documents officiels (H1)~~ — **fait en V1.38** (catégories éditables + consultation groupée).
2. ~~Plan d'action (G1)~~ — **fait en V1.39** (Type d'écart + Statut en listes éditables ; esquisse, à affiner :
   position de la colonne et valeurs des listes).
3. ~~Matériel ACTIF / PANNE + localisation provisoire (M1)~~ — **fait en V1.40** (état éditable
   `Etats_materiel`, colonne *Localisation provisoire*).
4. **Révision des droits de la Direction** — point 5 : **Bernard ajuste lui-même dans la matrice
   `P1_Roles`** (donnée). Pas de développement requis de notre côté.
5. ~~Expression de besoin logistique~~ — **fait en V1.40** (nouvel onglet `L3_Besoins` + déclenchement
   depuis un matériel en panne ; les besoins peuvent aussi être autres).
6. **Logo** — remplacement du fichier quand le nouveau sera fourni (trivial). *Reporté (Bernard : « on verra plus tard »).*

Rappel discipline : les lots 1/2/3/5 touchent l'Excel → **ajouts additifs maîtrisés** (chirurgie du zip,
re-gel du md5, contrôle d'intégrité des 669 formules), comme en V1.25/V1.28. Le lot présentation (V1.36)
n'a, lui, pas touché l'Excel. Reste aussi à finir le nettoyage des **codes CDC** (A1, N1…) dans les aides
si l'on veut des libellés 100 % parlants.

## Candidats V2 (non développés)
Réservations d'événements hors-cours, absences partielles, granularité fine des présences,
volumétrie A2_Presences.

## Rappels méthode
- Toute modification : propager sur toutes les couches. Confirmer la liste des champs avant
  d'implémenter chaque écran.
- Push : PowerShell inline, `$env:GITHUB_TOKEN` (jamais collé dans le chat).
- Versionnement : archive ZIP numérotée des fichiers précédents ; seuls les fichiers actifs restent
  au dépôt. Archives : `ARCHIVE_EMSP_Interface_V1_1.zip`, `ARCHIVE_EMSP_Interface_V1_2.zip`,
  `ARCHIVE_EMSP_Interface_V1_3.zip`, `ARCHIVE_EMSP_Interface_V1_4.zip`,
  `ARCHIVE_EMSP_Interface_V1_5.zip`, `ARCHIVE_EMSP_Interface_V1_6.zip`,
  `ARCHIVE_EMSP_Interface_V1_7.zip`, `ARCHIVE_EMSP_Interface_V1_8.zip`,
  `ARCHIVE_EMSP_Interface_V1_9.zip`, `ARCHIVE_EMSP_Interface_V1_10.zip`,
  `ARCHIVE_EMSP_Interface_V1_11.zip`, `ARCHIVE_EMSP_Interface_V1_12.zip`,
  `ARCHIVE_EMSP_Interface_V1_13.zip`, `ARCHIVE_EMSP_Interface_V1_14.zip`,
  `ARCHIVE_EMSP_Interface_V1_15.zip`, `ARCHIVE_EMSP_Interface_V1_16.zip`.
  Archives suivantes (module Notes & barème) : `emsp_interface_V1_25.zip` … `emsp_interface_V1_34.zip`
  (l'archive de la version précédente accompagne chaque livraison ; seuls les fichiers actifs restent au dépôt).

---

## V1.25 — Fondation : référentiel des formations (maquettes)

**Classeur ROUVERT** (la phase de test est passée, EMSP satisfait, l'app n'est plus sur place).
Ajout de l'onglet **`R1_Maquettes`** par **chirurgie du zip** (aucun onglet existant modifié).
- Intégrité vérifiée : 669 formules, valeurs calculées (0 diff sur 200 cellules), 16 dessins, 13 validations, 19 noms définis — **conservés**. 22 → **23 onglets**.
- **Nouveau md5 canonique : `9337d1a9fe74b2e61d5f45e9749479a9`** (ancien `0614d315…` = 22 onglets).
- R1 = 661 matières, 14 colonnes (Filière, Niveau, Semestre, N° UE, Intitulé UE/Module, Matière/Contenu, Enseignant, CM, TD, TP, Total heures, Vol. horaire UE, Crédit (ECTS), Coef). 5 filières ; Aides-soignants en `AS`.
- **config** : R1 au menu (Enseignements & salles), VERSION 1.25. **metier** : `matieres_maquette()`, `heures_programmees()`. **module.html** : aide R1. Route générique `/module/R1_Maquettes` (consultation, export Excel).
- Tests OK (py_compile ; login + rendu R1 200 ; pages existantes 200). Aucune donnée de test dans le livrable.

### Décisions de la réunion d'hier (à traiter, non encore codées)
- Documentation officielle à décliner en **Stratégique / Opérationnel / Supports de cours / Autre** (catégorie éditable par le directeur) → à porter sur `H1`.
- **Notes/relevés** guidés par les 2 bulletins (`RELEVE_NOTES.pdf`) + le règlement 7 p (`DISPOS_GENERALES_NOTES.pdf`) ; export du relevé par étudiant. La séparation « notes » devient une question de **droits d'accès**.
- **Avertissement** + **surveillant** (nouveau) : autorités = surveillant, enseignant, **+ scolarité et chef de département a minima**.
- Modèle de **Plan d'action** : en attente d'un fichier ; on **garde `G1`** en attendant.
- NB : « Plan d'action / classification doc / avertissement / surveillant » **absents des fichiers communs** vus ici (spéc = description orale de Bernard).

### Prochaines actions
1. Brancher la **datalist des matières** sur A3 (depuis la maquette) + volume programmé E2 — **ne touche pas au classeur** (à confirmer l'UX avant de coder).
2. Classification documentaire H1 (rapide).
3. Au choix : module **Stages** (affectation auto + quotas + TdB) ou module **Notes/relevés** (édition relevé + délibération/compensation selon le décret) ; avertissement/surveillant avec les notes.
