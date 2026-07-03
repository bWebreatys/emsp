# EMSP — Interface de gestion (Version 1.74)

## V1.74 — Droits par utilisateur : roles-modeles + editeur granulaire
> **AUCUNE modification du classeur.** Les droits sont deja stockes **par login** dans `P1_Roles` (le « role » n'est qu'une etiquette) : deux comptes d'un meme role peuvent donc avoir des droits differents (ex. **gestionnaire** vs **assistant comptable**). Cette version rend cela **pilotable depuis l'ecran** « Comptes & acces » : (1) **roles-modeles** (`config.ROLES_MODELES`, editables) qui **pre-cochent** les droits ; (2) **cases par groupe** Lecture / Ecriture + bascules **Acces financier** et **Admin droits**, ajustables **par utilisateur** (decocher = donner moins, cocher = donner plus) ; (3) ecriture via `metier.enregistrer_utilisateur` (upsert P1_Roles, anti-blocage dernier admin). Lot : `config.py` (VERSION 1.74, `ROLES_MODELES`, `GROUPES_DROITS_LIBELLES`), `app.py` (route `autorisations_utilisateur` granulaire), `templates/autorisations.html` (modele + cases + JS), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.73 — Interface : accueil épuré + fiche enseignant
> **AUCUNE modification du classeur** (md5 maître inchangé). Suite du chantier interface. (1) **Accueil** : le bandeau d'indicateurs (KPI) en tête est retiré — l'accueil est un pur « point de départ » (le Tableau de bord porte les indicateurs) ; les tuiles sont **agrandies** (badge icône, ombre, survol) au langage des cartes. (2) **Fiche enseignant** `/enseignant` — **symétrique de la fiche étudiant** : recherche par matricule/nom, **photo** (`donnees/photos/`, hors classeur), identité depuis `E1_Enseignants` en **lecture seule** (le CRUD reste dans le module `E1`, bouton **« Modifier dans le module »** qui ouvre `E1_Enseignants` pré-positionné sur la ligne via `?modifier=`), **heures** (`E2_Releve_heures` par matricule, avec totaux), **séances planifiées** (`A3_Sessions`, lien par Nom+Prénom — matricule pris en charge dès qu'il sera proposé), **séances réalisées / exceptions** (`E3_Seances_faites`), et **fiche imprimable** (navigateur, paysage). (3) **Fiche étudiant imprimable** ajoutée (même moteur). Pseudo-page `ENS_Fiche` (menu Enseignants + `SPECIAL_ROUTES`). Lot : `config.py` (VERSION 1.73, `ENS_Fiche`), `metier.py` (recherche/fiche/heures/séances enseignant, photo enseignant), `app.py` (routes `/enseignant*`, `/enseignant/<m>/imprimer`, `/etudiant/<m>/imprimer`), `templates/accueil.html`, `templates/enseignant.html` + `enseignant_print.html` + `etudiant_print.html` (nouveaux), `templates/etudiant.html` (bouton imprimer), `templates/module.html` (deep-link `?modifier=`), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.72 — Refonte UX : menu regroupé, masquage par droits, accueil en tuiles
> **AUCUNE modification du classeur** (md5 maître inchangé). Refonte purement IHM à partir des routes **existantes** (TDR). (1) **Menu de gauche en 6 groupes** — Pilotage, Scolarité, Enseignants, Ressources, Finances, Administration — par réécriture de `GUIDE_STRUCTURE` (`config.py`) ; **aucune route perdue**, modules hors-TDR (Examens, Diplômes, Qualifications, Indemnités, Non-conformités, Audits, Conflits) **sortis du menu** (routes conservées). (2) **Masquage par droit de lecture** : un onglet gouverné par `P1_Roles` que le rôle ne peut pas lire (`metier.peut_lire`) est retiré du menu, de même que tout groupe/section devenu vide — fini les murs « lecture seule » ; un **superadmin voit tout**, et les pseudo-pages (Fiche étudiant, Calendrier, Requêtes, Impressions, Tableau de bord…) restent **toujours visibles**. Calcul dans le `context_processor` (`MODULES_CACHES`). (3) **Accueil « point de départ »** : la zone centrale devient une grille de **grandes tuiles** (Élèves, Présences, Notes & bulletins, Trésorerie, Tableau de bord, Impressions), gardées par les droits, au-dessus du bandeau d'indicateurs conservé. Un clic sur une tuile ouvre la même page que l'entrée de menu. Lot : `config.py` (VERSION 1.72, `GUIDE_STRUCTURE` 6 groupes), `app.py` (`MODULES_CACHES` au contexte via `est_admin`/`peut_lire`), `templates/base.html` (menu masqué par droits), `templates/accueil.html` (tuiles), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.71 — Bandeau de filtres multicritère + impression de la sélection
> **AUCUNE modification du classeur** (maître `EMSP_V1_MAITRE_V1_70.xlsx` inchangé, md5 `c44c7864d256a436315a0d1538add70e`, 16 dessins / 30 onglets). Bandeau de filtres commun (**Filière / Niveau / Année académique / Période Du–Au** en JJ/MM/AAAA) en tête de chaque page module et du tableau de bord ; chaque contrôle est **masqué automatiquement** quand l'onglet ne le supporte pas (`bandeau.supporte`), bandeau entièrement masqué sur `P0_Parametres` et les onglets de référence. **Option B** : l'année et la période filtrent finances et heures, mais **seuls filière et niveau** déclenchent le **grisage** des cartes financières du tableau de bord (Recettes / Dépenses / Solde / Heures + note) car non ventilables par filière/niveau ; sans filtre actif, comportement **identique** aux versions antérieures (rétro-compatible). **Impression de la sélection par le navigateur** (pas de WeasyPrint, `window.print()` → Enregistrer en PDF) : bouton « Imprimer cette sélection » (`formaction` + `formtarget=_blank` emporte la sélection courante) → page **autonome paysage** (`@page size: A4 landscape`, `.doc-page.paysage`), en-tête Université des Comores / EMSP + date d'édition + rappel de la sélection ; mode **module** (table filtrée) et mode **dashboard** (table KPI, KMF sans décimale). Lot : `config.py` (VERSION 1.71), `app.py` (`_lire_filtres`, `_bandeau_dashboard`, routes `/module/<onglet>/imprimer` et `/tableau-de-bord/imprimer`, `/api/dashboard` filtré), `templates/_bandeau_filtres.html` + `templates/impression_selection.html` (nouveaux), `templates/module.html` + `templates/tableau_bord.html` (include + option B), `README.md`, `doc/doc_des_ecrans.md`, `CONSIGNES_LIVRAISON.md`, `ETAT.md`.

## V1.70 — Budget compta : prévu / réalisé / écart (+ taux de change)
> **Comparatif budgétaire sans double stockage** : prévu = onglet `F3_Budget_poste`, réalisé agrégé depuis `F1_Mouvements` par poste (calcul Python, **année civile**). Deux onglets attendus depuis V1.58 mais absents du maître à 28 onglets — (re)créés et câblés ici. **Chirurgie ZIP du maître** (16 dessins préservés) : ajout de `F3_Budget_poste` (sheet29) + `P2_Taux` (sheet30), 28 → **30 onglets**, **nouveau md5 `c44c7864d256a436315a0d1538add70e`**. `P2_Taux` semé **EUR = 491 967** (parité fixe). Liste P0 partagée renommée `Bailleurs (*)` → **`Sources_financement (*)`** (AFD / Etat comorien / Ressources propres EMSP / Autres donateurs), unique pour `F1` / `M1` / `F3`. **`F3_Budget_poste`** (menu Finances & pilotage, droit financier) : Exercice · Poste budgétaire · Filière (optionnelle) · Sens · Source de financement · Montant budgété (KMF) · Observations · Saisi par. **`P2_Taux`** (menu Paramétrage, Direction) : Devise · Code · Taux en KMF · Date d'effet · Observations (EUR pré-semé, USD laissé à l'EMSP). **Édition « Budget : prévu / réalisé / écart »** dans `/impressions` (sélecteur d'exercice) : `/impressions/etat-poste?exercice=AAAA` → comparatif par poste Prévu (F3) / Réalisé (F1 année civile) / Écart / Taux de réalisation, en paysage. Couverture sanitaire (658b) hors réconciliation. **Sur installation déployée** : lancer une fois `python scripts/migration_copie_V1_70.py` (idempotent) ; sur le maître, `python scripts/chirurgie_V1_70.py`. Lot : `config.py` (VERSION 1.70, menus + droits + Dictionnaire F3/P2 + surcharge liste), `metier.py` (`taux_change`, `budget_par_poste`, `_realise_par_poste`, `_sens_par_poste`, `etat_poste_budget`), `app.py` (route etat-poste avec `exercice`, filtre vues rebranché), `templates/impressions.html` (carte budget), `scripts/chirurgie_V1_70.py`, `scripts/migration_copie_V1_70.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.69 — Suivi des droits d'inscription par étudiant
> **Vue dérivée de `F1_Mouvements`, sans double stockage** ; tarifs lus dans P0 (éditables), calcul en Python. Chirurgie ZIP du maître (16 dessins préservés) : `F1_Mouvements` + `Matricule` (18) / `Annee academique (*)` (19) ; `P0_Parametres` + `Tarif_inscription_niveau` (26) / `Tarif_inscription_KMF` (27). Tarifs semés L1 = 70 000 / L2 = 70 000 / L3 = 80 000 KMF (éditables). Fiche `/etudiant` : bloc **Droits d'inscription** (Dû / Payé / Reste dû + versements datés), lecture seule scolarité/direction ; niveau hors grille → « Tarif non défini » (pointeur P0). Mini-écran `/etudiant/<matricule>/encaisser` réservé au **droit financier** (journalisé, bloqué sur poste secondaire) : pré-remplit poste 706 du niveau, montant = reste dû, année académique ; **Compte/caisse et Mode de paiement obligatoires**, catégorie laissée à la comptabilité. Redoublant géré (poste 706 du niveau + année). **Sur installation déployée** : lancer une fois `python scripts/import_tarifs_inscription.py` (idempotent). Lot : `config.py` (VERSION 1.69, `POSTE_INSCRIPTION_PAR_NIVEAU`), `metier.py` (`tarifs_inscription`, `droits_inscription`, `enregistrer_encaissement`), `app.py`, `templates/etudiant.html`, `templates/encaisser.html`, `scripts/chirurgie_V1_69.py`, `scripts/import_tarifs_inscription.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.68 — Brique 0 : listes compta opérationnelles
> **Données, pas structure** (openpyxl sur copie déployée, aucune chirurgie ; formule « Solde courant » de F2 intacte). Alimente les listes compta de `P0_Parametres`, jusque-là vides — l'écran `/tresorerie` et la saisie `F1_Mouvements` deviennent **opérationnels** : `Cat_Recettes` (3 : 70/74/13), `Cat_Depenses` (10 : 60/61/62/64/65/66/67/16/20/21), `Postes_budgetaires` (60 articles + sous-articles, format « code — intitulé », codes OCR et suffixes tels quels). Source figée `scripts/listes_compta_data.json` (depuis `Nomenclature_budgetaire_EMSP.xlsx`). Pré-renseigne `F2_Comptes` (Compte bancaire UDC-EMSP-ODS BIC-Comores + Caisse EMSP, soldes initiaux vides). **Sur installation déployée** : lancer une fois `python scripts/import_listes_compta.py` (idempotent ; données non écrasées par une MAJ). Le kit V1.68 livre les listes déjà chargées. Utilitaire `scripts/trouver_maitre.py` (repère le maître de référence à 28 onglets + dessins). **Dépôt Git abandonné** (livraisons par ZIP). Lot : `config.py` (VERSION 1.68), `scripts/import_listes_compta.py`, `scripts/listes_compta_data.json`, `scripts/trouver_maitre.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.67 — inventaire des équipements (patrimoine ↔ compta)
> Colonne `Quantité` ajoutée à `M1_Equipements` (maître : chirurgie ZIP `scripts/ajout_quantite_M1.py`, dessins préservés ; copie déployée : ajoutée par l'import openpyxl). Import de l'inventaire EMSP via `scripts/import_equipements.py` + `scripts/equipements_data.json` : **280 articles** (répartition par bureau et par salle), une ligne par article avec sa quantité, n° d'inventaire = matriculation `UDC/EMSP/…`, état et date repris tels quels. `Montant` / `Bailleur` / `Référence` / `Catégorie` laissés vides, à affecter depuis la compta (lien Patrimoine ↔ Compta : équipement = dépense affectée à un poste budgétaire et un financement, reliée à `F1` par la `Référence / N° pièce`). Idempotent. **Sur installation déployée** : lancer une fois `python scripts/import_equipements.py` (et `ajout_quantite_M1.py` sur le maître). Lot : `config.py`, `scripts/import_equipements.py`, `scripts/ajout_quantite_M1.py`, `scripts/equipements_data.json`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.66 — validation des coefficients du barème
> **Décision : coefficients indiqués validés ; corrections ultérieures par la scolarité.** `Coef confirmé` → **« Oui »** sur les 642 matières de `N1_Bareme_UE` (le bandeau « Barème provisoire » disparaît du bulletin et du relevé). Sur une installation déjà déployée, exécuter une fois `python scripts/confirmer_coefficients.py` (idempotent ; les données ne sont pas écrasées par une mise à jour). Le recoupement avec les 3 documents officiels n'a pas pu être fait (fichiers non accessibles). Anomalies laissées à la scolarité : 1 UE sans ECTS, une UE à coef 0, des UE à coef 11/12. Lot code : `config.py`, `scripts/confirmer_coefficients.py` (nouveau), `scripts/import_bareme.py`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.65 — saisie façon bulletin
> **AUCUNE modification de structure du classeur** (upsert `N2_Notes` uniquement). Nouvel écran `/bulletin` : un étudiant → sa grille (UE → matières du barème), examen saisi, **CC affiché** (dérivé des contrôles `N4`, lecture seule ; saisissable sinon), moyennes **en direct** (matière ¼ CC + ¾ examen, UE = moyenne des matières, semestre = UE pondérées par `Coef UE`, mention, proposition Admis/Ajourné indicative, ECTS). Recherche par matricule, Année, Semestre (du barème), Session 1/2 (session 2 : pré-remplissage + référence session 1). Écriture upsert `N2` (clé `Matricule+Année+Session+Semestre+N°UE+Matière`) **des seules matières renseignées** ; le CC dérivé `N4` n'est pas réécrit. Réservé au droit `N2_Notes`, bloqué sur poste secondaire, journalisé. Lot code : `config.py`, `metier.py`, `app.py`, `templates/bulletin_saisie.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.64 — présences en liste (séance ad hoc, option B)
> **AUCUNE modification de structure du classeur** (écriture de données uniquement : `A2_Presences`, et `A3_Sessions` si « récurrente »). Nouvel écran `/presences/libre` : on définit la séance à la volée (classe + date + heure début/fin + matière du barème + enseignant `E1` + salle optionnelle), le roster vient de `A1` (Filière + Niveau, Section si renseignée), on coche les présents (non coché = absent), re-saisie = correction (upsert). Créneau `A2` = plage `HH:MM-HH:MM`. Clé « Session / Matière » composée (`Filière Niveau - Matière - Enseignant`) ; si « enregistrer comme récurrente », une ligne `A3_Sessions` est créée (ID `Sxxx`, jour déduit de la date) et son ID sert de clé. Réservé au droit `A2_Presences` (création `A3` = droit `A3_Sessions`), bloqué sur poste secondaire, journalisé. Lot code : `config.py`, `metier.py`, `app.py`, `templates/presences_libre.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.63 — dépôt de photo sur la fiche étudiant
> **AUCUNE modification du classeur.** La photo est un fichier image (`donnees/photos/<matricule>.jpg`), hors classeur et hors dépôt. Sous la photo : bouton **« Choisir une photo… » / « Changer la photo »** (sélecteur de fichier, soumission automatique au choix) et bouton **« Retirer la photo »** (rouge, avec confirmation, visible seulement si une photo existe). Formats **JPEG et PNG** détectés par signature binaire (pas de ré-encodage, **aucune dépendance binaire ajoutée**), **1 Mo max**, refus clair sinon. Enregistrement sous `<matricule>.jpg` ; un PNG est servi en `image/png`. Contrôles réservés au **droit d'écriture sur `A1_Etudiants`**, **indisponibles sur poste secondaire**, **journalisés**. Bloc placé dans le flux normal de la carte `.panel` (colonne centrale) : aucun chevauchement avec le menu. Lot code : `config.py` (VERSION 1.63, `PHOTO_MAX_OCTETS`), `metier.py` (`chemin_photo`, `photo_servie`, `enregistrer_photo`, `supprimer_photo`, `_type_image`), `app.py` (routes `televerser`/`retirer`, affichage par détection d'octets, `peut_modifier`), `templates/etudiant.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

# EMSP — Interface de gestion (Version 1.62)

## V1.62 — correctif d'affichage de la fiche étudiant
> `templates/etudiant.html` utilisait par erreur la classe `.bloc` (réservée aux blocs du planning : position absolue, fond bleu, texte blanc) → la fiche s'affichait en bleu plein, illisible, et débordait sous le menu. Corrigé : passage aux cartes standard **`.panel` / `.ph` / `.pb`** (fond blanc, texte noir, contenu dans la colonne centrale) et table `data` pour les stages. Aucun autre changement.

# EMSP — Interface de gestion (Version 1.61)

## V1.61 — fiche étudiant + recherche par matricule

> **AUCUNE modification du classeur.** Nouvel écran dédié. Lot code : `config.py` (VERSION 1.61, `PHOTOS_DIR`, page `ETU_Fiche`), `metier.py` (`recherche_etudiants`, `fiche_etudiant`, `stages_etudiant`, `_photo_existe`), `app.py` (routes `/etudiant`, `/etudiant/photo/<matricule>`), `templates/etudiant.html` (nouveau), doc.

- **Recherche par matricule** (ou nom), sans longue liste déroulante : un champ avec autocomplétion hors-ligne (datalist « matricule — Nom Prénom (filière niveau) ») ; on tape le matricule ou on choisit dans la liste, bouton « Afficher la fiche ». Choisir une entrée soumet directement.
- **Fiche** : identité A1 complète (charte, lisible) + **photo**, et liens vers le **relevé/bulletin** (pré-rempli matricule + année), les **présences** et les **stages**. Les **stages de l'étudiant** sont listés en bas (depuis S1).
- **Photos** : convention `donnees/photos/<matricule>.jpg` ; tant qu'absente, un **placeholder portrait** (#1F4E79) s'affiche. Déposer les photos au fil de l'eau (numérisation / apport étudiant), aucune autre manipulation.
- **Composant réutilisable** : la même recherche par matricule servira à la **sélection de l'élève dans les stages** (prochaine étape).
- **Testé** : recherche (562 entrées), fiche d'un étudiant réel (identité + liens + stages), placeholder photo (SVG), doublon `73395b`, cas introuvable.
- **À venir (validé, à implémenter)** : sélection élève dans les stages ; **présences par séance en liste** (classe → cocher) avec matière + enseignant (sert aussi de feuille de présence enseignant → paie) ; **roster CC** et **roster examens** (saisie en liste, façon bulletin).


## V1.60 — écrans de saisie compacts (champs en ligne, largeur ajustée aux caractères)

> **AUCUNE modification du classeur.** Lot code : `config.py` (VERSION 1.60, `LARGEURS_CHAMPS`, défauts A1), `metier.py` (`_prochain_ordre`, largeur par champ), `templates/module.html`, `static/css/style.css`, doc.

- **Problème traité** : le formulaire de saisie générique imposait 220 px minimum par champ, en colonne (label au-dessus) → Genre (1 caractère), Matricule, N° d'ordre démesurés, identité éclatée sur plusieurs lignes, saisie lente.
- **Nouveau rendu** : les champs s'écoulent **en ligne** (flex-wrap) et chacun est **dimensionné à son nombre de caractères utile** (`config.LARGEURS_CHAMPS`, sinon calcul auto : select = largeur de la plus longue option, date = 12, nombre = 9, texte = 18). L'identité A1 tient sur une seule ligne ; Genre = 4, Matricule = 10, dates = 12, etc.
- **Saisie par matricule** : le **N° d'ordre est pré-suggéré** (prochain libre, `@next_ordre`) et reste modifiable ; le contexte (filière/niveau/section/année/statut) se **reporte de la dernière saisie** (`@last`) pour la saisie en série — d'un étudiant à l'autre, on ne tape que matricule + identité.
- **Couverture** : un seul changement de formulaire → s'applique d'un coup à **A1 (étudiants), N1 (barème), N2 (notes), N3 (signalements), N4 (contrôles)** et à tous les autres onglets en saisie générique.
- **Fiche de présence** : désormais **actualisée** automatiquement (l'effectif est tiré de `A1_Etudiants` par Filière+Niveau dès qu'une séance existe dans A3) — aucun code à modifier.
- **À venir (confirmé séparément)** : saisie des notes **façon bulletin** (chaque note insérée à sa place définitive) ; affinage écran par écran sur la base des états de sortie.


## V1.59 — chargement des élèves et des filières (données réelles)

> **Données chargées dans le classeur de PRODUCTION** (copie déployée `donnees/data/EMSP_V1.xlsx`, via openpyxl — même voie d'écriture que l'IHM ; le master template figé n'est pas touché). Nouveaux fichiers : `scripts/import_eleves.py` + `scripts/eleves_data.json`. Lot code : `config.py` (VERSION 1.59), `templates/base.html` (texte du liseré formation), doc.

- **562 élèves** chargés dans `A1_Etudiants` depuis les listes définitives transmises, et **5 filières** dans `P0_Parametres` : Soins infirmiers (L1 100 / L2 85 / L3 60), Soins obstétricaux (L1 83 / L2 64 / L3 63), Imagerie médicale (L1 57), Maintenance biomédicale (L1 20), Aides-soignants (30, hors LMD). Niveaux en service = ceux où il y a des élèves.
- **Règles** (validées) : année académique `2025-2026` ; Genre / Section / Origine / Date inscription laissés vides (complétés ensuite via la fiche étudiant) ; Statut par défaut `Inscrit`.
- **Doublon de matricule conservé sans perte** : `73395` (HASSANI BAHADJATI) figure en Aides-soignants **et** Imagerie L1. Les deux lignes sont gardées (matricules `73395` et `73395b`), Statut `Doublon a arbitrer` sur les deux, à trancher par la scolarité.
- **Filière officielle** : « Soins obstétricaux » (alias « sages-femmes » des maquettes à placer en zone complémentaire ultérieurement).
- **Formation** : nouveau paradigme — l'environnement de formation utilise **les mêmes données réelles** que la production (plus de jeu fictif). Côté code, seul le **liseré rouge** a été ajusté (texte : « espace d'entraînement, les saisies ici n'affectent pas la production »). L'installation des deux dossiers (formation avec liseré / production sans) reste à la charge de Bernard.
- **Idempotent** : `import_eleves.py` purge et réécrit `A1`/`P0.Filieres`, rejouable sur la production réelle.
- **Action côté prod** : `python scripts/import_eleves.py` sur le `EMSP_V1.xlsx` de production (ou déposer le classeur peuplé fourni dans `donnees/data/`).
- **Suite (non incluse)** : fiabilisation des coefficients du barème depuis les fichiers officiels (Licence imagerie, Licence maintenance, maquettes SI/SO) → passage Coef confirmé Non→Oui ; refonte des écrans de saisie en s'appuyant sur les états de sortie.


## V1.58 — restauration de la couche de lancement (kit exécutable hors-ligne)

> **AUCUNE modification du classeur.** Lot : lanceurs racine `Demarrer_EMSP.bat`, `Demarrer_EMSP_RESEAU.bat`, `construire_socle.bat`, `LISEZMOI_INSTALLATION.txt`, `socle/wheelhouse/` (dépendances hors-ligne) ; `config.py` (VERSION 1.58), doc. Le **code** (couche `programme/`) est inchangé sauf le numéro de version.

- **Problème traité** : l'archive `emsp_interface_VXX.zip` ne contenait que la **couche `programme/` (le code)** — ni lanceur `.bat`, ni socle Python, ni wheelhouse. Le dépôt ne versionne que les fichiers actifs (jamais les binaires du socle), donc l'archive de code seule n'est pas exécutable. La couche de lancement est rétablie ici sous forme de **kit**.
- **Structure du kit (trois couches)** : `socle/` (Python 3.12 embeddable + `wheelhouse/`), `programme/` (code, remplacé à chaque mise à jour), `donnees/` (classeurs + `instance/`, jamais écrasés), et les `.bat` à la racine.
- **`Demarrer_EMSP.bat`** : fixe `EMSP_DONNEES` sur le dossier frère `donnees`, utilise le **socle** s'il existe, sinon **se replie sur le Python 3.12 du système** (poste développeur) et installe au besoin les dépendances **hors-ligne** depuis `socle/wheelhouse`, puis ouvre `http://127.0.0.1:5000`. CRLF.
- **`construire_socle.bat`** (une fois, avec Internet) : télécharge le Python embeddable, active `import site` dans `._pth`, **bootstrappe pip depuis son wheel** puis installe Flask/openpyxl/colorama depuis le wheelhouse (hors-ligne ensuite). `colorama` est présent (marqueur Windows non évalué par `pip download`).
- **`Demarrer_EMSP_RESEAU.bat`** : poste principal en écoute réseau (postes secondaires en lecture seule), ouverture best-effort du port 5000 (profil privé).
- **Wheelhouse** : 11 wheels officiels PyPI (Flask 3.1, openpyxl 3.1, Jinja2, Werkzeug, click, blinker, itsdangerous, markupsafe, et-xmlfile, colorama, pip), CPython 3.12 / win_amd64.
- **Mise à jour** : remplacer le contenu de `programme/` (MAJ_EMSP_V1_xx.zip) ; ne jamais toucher `donnees/` ni `socle/`.
- **Testé** : démarrage avec la structure du kit (chemins `programme`/`donnees` frères résolus, superadmin bootstrappé, `/login` → 200, `/` → 302), `.bat` en CRLF.


## V1.57 — barème arbitré importé (4 filières, matières éclatées)

> **Modification du classeur des NOTES uniquement** (`EMSP_Notes.xlsx`, sans dessin → `openpyxl.save`, pas de chirurgie zip) : réécriture de l'onglet **`N1_Bareme_UE`** depuis le barème arbitré par l'EMSP. Nouveaux fichiers : `scripts/import_bareme.py` + `scripts/bareme_data.json` (barème figé, auto-contenu). `EMSP_V1.xlsx` non touché. Lot code : `config.py` (VERSION 1.57), doc.

- **Source** : `BL_Bareme_UE_a_valider_EMSP_260622.xlsx` (4 filières : Soins infirmiers, Soins obstétricaux, Imagerie médicale, Maintenance biomédicale ; AIDES SOIGNANTS absent). Figé dans `scripts/bareme_data.json`.
- **Transformations** : une ligne par **matière** (éclatement sur « ; », nettoyage des puces) ; semestres S1–S6 → 1–6 ; **Coef UE = corrigé sinon maquette** ; **Coef confirmé = Non** partout (provisoire, en attente des corrections officielles de la scolarité → bandeau « Barème provisoire » sur les relevés).
- **Doublons d'UE déjà désambiguïsés à la source** (suffixe « b » : UE18/UE18b, UE49/UE49b) → chargés tels quels, aucun suffixe ajouté à l'import.
- **Remplace `seed_bareme.py`** comme source du barème : la version arbitrée fait foi (y compris la numérotation des UE, qui suit désormais les maquettes — différente de l'ancien seed aligné sur RELEVE_NOTES.pdf).
- **Résultat (testé sur copie)** : **642 lignes matières**, 4 filières, **0 collision** de clé (filière, niveau, semestre, N° UE, matière), import idempotent ; le moteur retrouve les UE par filière/niveau/semestre (UE18 et UE18b distincts).
- **Support de formation** : document Word `Support_formation_saisie_notes_EMSP.docx` (chaîne barème → contrôles → examen → relevé), pour la partie formation.
- **Action côté prod** : `python scripts/import_bareme.py` sur `EMSP_Notes.xlsx`.


## V1.56 — contrôles continus détaillés (CC dérivé) + report des dernières valeurs en saisie

> **Modification du classeur des NOTES uniquement** (`EMSP_Notes.xlsx`, séparé, sans dessin → `openpyxl.save` sûr, pas de chirurgie zip) : ajout de l'onglet **`N4_Controles`** via `scripts/ajout_N4_controles.py` (idempotent, rejouable sur prod peuplée). **`EMSP_V1.xlsx` n'est pas touché** (md5 canonique inchangé). Lot code : `config.py` (VERSION 1.56), `metier.py`, doc.

- **`N4_Controles`** : une ligne par contrôle (Matricule, Année acad., Session, Semestre, N° UE, Matière, **N° de contrôle + Date** = clé du contrôle, Note /20, **Coef** [1 par défaut], Saisi par [auto]). Saisie par le formulaire générique, sous le module **Notes**.
- **CC dérivé** : la note de contrôle continu d'une matière est désormais **calculée** comme la **moyenne pondérée** de ses contrôles N4 (coef 1 par défaut ; en pratique un seul contrôle → CC = sa note ; un second → moyenne). `metier._cc_table()` ; branché dans `_notes_effectives` et `_notes_brutes`.
- **Repli** : si **aucun** contrôle N4 pour une clé matière, on retombe sur la colonne **`N2.CC`** saisie à la main (compatibilité V1.30). Si N4 **et** N2.CC existent, **N4 prime**. `N2` ne saisit plus en pratique que l'**Examen** (CC laissé optionnel comme repli).
- **Report des dernières valeurs (token `@last`)** : en saisie en série, les champs de **contexte** (Année, Session, Semestre, N° UE, Matière, Date, N° de contrôle, Coef) se **pré-remplissent avec la dernière valeur saisie** ; seuls Matricule et la note changent d'un étudiant à l'autre. Replis au démarrage à froid : `@last|2025-2026` (année), `@last|@today` (date), `@last|1` (session, coef, n° de contrôle). Appliqué à `N4_Controles` et `N2_Notes`.
- **Bulletin / relevés inchangés en aval** : le moteur décret 05-106 (¼ CC + ¾ examen, moyenne UE, semestre pondéré, session 2, mentions, Admis/Ajourné) consomme le CC dérivé sans autre modification.
- **Tests (copies jetables peuplées)** : création N4 + idempotence ; CC dérivé simple (1 contrôle), CC dérivé pondéré (2 contrôles → moyenne), repli N2.CC manuel — moyennes au centième conformes ; bulletin affiche le CC dérivé ; `@last` reporte tout le contexte, replis corrects à froid (date = jour) ; `py_compile` des 5 modules, import `app.py` OK.
- **En attente (hors de ce lot)** : import du barème `Bareme_UE_a_valider_EMSP_260622.xlsx` (éclatement des matières + suffixe **« b »** sur les N° UE en doublon, appliqué à l'import) — nécessite le fichier barème.


Interface web **hors-ligne** posée par-dessus le classeur `EMSP_V1.xlsx`.
Mission Expertise France / AFD — Projet ODS 21SANOC277 — réf. 2026/EAALDDDGPLDGDLS/15420 (Webcreatys SAS).
Volet **ÉCOLE (EMSP) uniquement**, séparé du GMAO. Périmètre **TDR**.

Dépôt : `github.com/webcreatys/emsp` (branche `main`).

## V1.55 — heures constatées des enseignants (dérivées des appels de présence)

> **Modification du classeur** par chirurgie du zip : ajout de l'onglet `E3_Seances_faites`. 16 dessins et 669 formules préservés ; 27 → 28 onglets. **Nouveau md5 canonique : `4544adca513ab6a4b650c0376914d443`** (ancien `bfe96457b7f0dc7fac7041989d77c309`).

L'appel des élèves atteste qu'une séance a eu lieu : les heures effectives d'un enseignant sont **dérivées** des appels (`A2_Presences`) croisés avec le planning (`A3_Sessions`). Une séance normale ne demande **aucune saisie**. L'onglet `E3_Seances_faites` ne stocke que les **exceptions** (remplaçant, cours annulé, durée différente), saisies depuis l'écran d'appel. L'écran **« Heures constatées du mois »** (`/heures-constatees`) calcule les heures par enseignant et les **reporte dans le relevé E2** (base de la paie), sans jamais écraser une valeur corrigée à la main sans confirmation. La chaîne paie (relevé d'heures) est inchangée.

Pour ajouter `E3_Seances_faites` à un classeur **de production** existant (avec données), exécuter `scripts/ajout_E3_seances_faites.py` sur ce classeur (préserve données et dessins) — ne pas remplacer la production par le maître vierge.

## V1.54 — multi-poste réseau câblé (lecture seule + voyant rouge ; classeur inchange)

Le **poste principal** (local) détient et **écrit** les données ; les **postes secondaires** se connectent par le réseau au serveur du poste principal et sont **automatiquement en lecture seule** (consultation), avec un **voyant rouge** « LECTURE SEULE ». Un seul poste écrit, donc aucun risque de corruption du classeur. L'écoute réseau s'active par `Demarrer_EMSP_RESEAU.bat` (variable `EMSP_HOST=0.0.0.0`) ; `Demarrer_EMSP.bat` reste en mono-poste local. Les écritures venant d'un poste distant sont refusées côté serveur (seule l'authentification est permise). Voir `LISEZMOI_RESEAU.txt`.

## V1.53 — séparation données / code (structure du kit ; classeur inchange)

> **AUCUNE modification du classeur** (md5 `bfe96457b7f0dc7fac7041989d77c309` inchange). Lot : `config.py` (VERSION 1.53), scripts `formation\`, doc.

Le kit est structure en trois parties independantes : `socle\` (Python embarque + bibliotheques, installe une fois), `programme\` (le code, remplacable en bloc a chaque version) et `donnees\` (les classeurs `data\` et les secrets `instance\`, jamais ecrases). `config.py` resout `data/` et `instance/` dans `donnees\` (frere de `programme\`), surchargeable par la variable d'environnement `EMSP_DONNEES`. Consequence : une mise a jour = remplacer `programme\` sans aucun risque pour les donnees ; une reinstallation a blanc ne laisse aucun reliquat. Seul `config.py` change cote code (tous les modules passaient deja par ses constantes).

## V1.52 — périmètre de l'édition en place (classeur inchange)

> **AUCUNE modification du classeur** (md5 `bfe96457b7f0dc7fac7041989d77c309` inchange). Lot 100 % code : `config.py` (VERSION 1.52), `app.py`, `templates/module.html`, `doc/doc_des_ecrans.md`, `ETAT.md`.

L'édition de ligne (V1.51) reste **un seul code générique**, mais son **périmètre d'usage** est restreint par liste blanche `ONGLETS_EDITION_LIGNE` (sous-ensemble de `ONGLETS_SAISIE_ACTIVE`). L'**ajout** reste ouvert partout ; seule la **correction en place** est restreinte. Frontière : donnée de référence / champ de workflow (corrigeable sur place) vs registre append-only. Le **journal financier `F1_Mouvements` reste en ajout seul** (contexte audit AFD : une erreur se corrige par écriture rectificative, pas en réécrivant la ligne) — encadré « Modifier » masqué, route `/module/F1_Mouvements/modifier` → 404. Durcissement = ajouter un onglet à `ONGLETS_SANS_EDITION_LIGNE` (candidats `F2_Comptes`, `N3_Signalements`). Toute modification reste journalisée.

## V1.51 — modification des fiches (édition de ligne ; classeur inchange)

> **AUCUNE modification du classeur** (md5 inchange). Lot 100 % code : `data.py`, `app.py`, `templates/module.html`, `config.py` (VERSION 1.51).

Édition en place d'une ligne déjà saisie (sélecteur *Modifier une fiche existante* → *Charger pour modification* → formulaire d'ajout réutilisé, champ caché `_index`, route `POST /module/<onglet>/modifier`). Primitive `AccesDonnees.modifier_ligne(onglet, index, valeurs)` : même voie d'écriture qu'`ajouter_ligne`, **colonnes calcul jamais écrasées**, `Saisi par` réinjecté, journalisé. Pas de suppression physique (sortie = changement de Statut).

## V1.50 — marquage FORMATION : bandeau visible partout + exports Excel (classeur inchange)

> **AUCUNE modification du classeur** (md5 `bfe96457b7f0dc7fac7041989d77c309` inchange). Lot 100 % code : `static/css/style.css`, `metier.py`, `app.py`.

- **Bandeau web visible sur toutes les pages** : le bandeau rouge « ENVIRONNEMENT DE FORMATION » etait bien emis sur chaque page (porte par `base.html`) mais, en flux normal, il etait masque par la barre laterale et la barre superieure des que la page defilait — d'ou son apparente presence sur le seul accueil. Il est desormais **fixe en haut** (`position:fixed`, `z-index` au-dessus de tout) ; en mode formation le contenu et la barre laterale sont decales de sa hauteur. Le decalage est neutralise a l'impression (le filigrane PDF « FORMATION » au centre de page reste inchange).
- **Exports Excel marques en mode formation** : les six exports (`tableau de bord`, `export d'un onglet`, `vue`, `pivot`, `releve / bulletin`, `etat des signalements`) portent desormais, **uniquement en MODE_FORMATION**, une **ligne d'en-tete rouge** « FORMATION — données d'entraînement, sans valeur officielle » en tete de chaque feuille, et un **suffixe `_FORMATION`** dans le nom de fichier (ex. `export_A1_Etudiants_20260618_FORMATION.xlsx`). En production : aucun effet, comportement strictement inchange.
- Industrialisation : `metier.bandeau_xlsx(ws, ncols)` (insere la ligne de bandeau, sans fusion en amont) et `metier.nom_export(nom)` (suffixe avant l'extension), appliques aux six points d'export.

Couches : `static/css/style.css` (bandeau fixe + decalage), `metier.py` (`bandeau_xlsx`, `nom_export`, integration `_xlsx_simple` / `export_tdb_xlsx`), `app.py` (six `download_name` + bandeau sur releve et signalements), `config.py` (VERSION 1.50).

## V1.49 — plan d'action enrichi + tableau de bord + detection formation tolerante

> **CLASSEUR MODIFIE (chirurgie zip).** 6 colonnes ajoutees a `G1_Plan_action` (colonnes I..N, en-tetes inlineStr, aucun decalage de formule) : **Axe / theme, Objectif (resultat attendu), Priorite, Temporalite, Indicateur de reussite et preuves, Observations**. **16 dessins + 669 formules preserves**, 27 onglets. Les colonnes existantes sont conservees (Domaine/module, Ecart constate, Action corrective, Responsable, Echeance, Statut, Type d'ecart).
> **NOUVEAU md5 canonique : `bfe96457b7f0dc7fac7041989d77c309`** (ancien `90f7454fb74c482d41667e6b31971d73`).

- **Saisie** : Priorite (Haute/Moyenne/Basse) et Temporalite (Court/Moyen/Long terme) sont des listes deroulantes ; Statut reste editable dans Parametres ; les autres champs sont libres. Les nouveaux champs apparaissent en fin de formulaire (placement physique sur), mais l'edition les remet dans l'ordre logique.
- **Edition plan d'action** : passee en **paysage**, ordre logique (N, Axe, Domaine, Constat, Objectif, Action, Responsable, Priorite, Temporalite, Echeance, Indicateur, Etat d'avancement, Observations, Type d'ecart).
- **Tableau de bord du plan d'action** (NOUVEAU) : `/plan-action/tableau-de-bord`, accessible depuis la Direction. KPI (total, achevees, taux d'achevement, en retard) + graphiques par etat d'avancement, par priorite, par axe (Chart.js vendu localement). « En retard » = echeance depassee et action non achevee.
- **Detection du mode formation tolerante** : `instance/formation.flag` est detecte sans tenir compte de la casse et accepte l'extension `.txt` (piege Windows des extensions masquees).

Couches : **classeur** (6 colonnes G1), `config.py` (VERSION 1.49, detection formation, listes Priorite/Temporalite, declaration des 6 champs), `metier.py` (`plan_action_liste` reordonnee, `plan_action_kpis`), `app.py` (route `/plan-action/tableau-de-bord`, plan d'action en paysage), `templates/tableau_bord_plan_action.html` (nouveau), `templates/tableau_bord.html` (lien).

## Classeur V1.48 — colonne Compte (plan comptable) + etats comptables + bulletin officiel

> **CLASSEUR MODIFIE (chirurgie du zip).** Une colonne **« Compte (**) »** ajoutee a `F1_Mouvements` (colonne Q, en SAISIE), pour le numero de compte du plan comptable comorien (saisi par l'utilisateur, sans controle de conformite ; permet des regroupements). **16 dessins et 669 formules preserves**, 27 onglets, 0 decalage de reference (ajout en fin de feuille). Graine `formation/seed/` re-alignee (dessins restaures).
> **NOUVEAU md5 canonique : `90f7454fb74c482d41667e6b31971d73`** (ancien `4eb8bd6d44595616ebef85f79d462468`).

- **Situation de compte** : la colonne « Compte » est desormais alimentee par ce champ saisi (et non plus par la Categorie). Ordre du registre EMSP : N / Chapitre (poste budgetaire) / Compte / Date / N piece / Description / Beneficiaire / Debit / Credit / Solde.
- **Etat des recettes et depenses par poste budgetaire** (NOUVEAU, profil financier) : `etat_par_poste(mois, compte)` — recettes, depenses, solde par poste, avec TOTAL.
- **Bulletin de notes officiel** (NOUVEAU) : mise en page identique au releve de notes EMSP (`RELEVE_NOTES.pdf`), **annuel** (un bloc par semestre, colonnes C.Continu / Examen / Moyenne / Exam. session 2 / Moy. session 2 / Coef / ECTS), moyenne de semestre, decision du jury (proposition), mention, puis moyenne annuelle. `bulletin_officiel(matricule, annee)` + `templates/bulletin_officiel.html`. La route `/impressions/bulletin` produit le releve annuel (semestre vide) ou d'un semestre.

OU EDITER LE BULLETIN : les **notes** se saisissent dans *Scolarite > Etudiants > Notes — controle continu & examen* (N2) et le bareme dans *Barème des UE* (N1) ; le bulletin se **genere et s'imprime** depuis *Scolarite > Etudiants > Releve / bulletin* (calcul a l'ecran + export Excel) et depuis *Administration > Impressions > Releve de notes (bulletin)* (PDF, annuel ou par semestre). La mise en page est dans `templates/bulletin_officiel.html`.

Couches : **classeur** (colonne Q F1), `metier.py` (situation Compte, `etat_par_poste`, `bulletin_officiel`/`_notes_brutes`/`_fmt_note`), `app.py` (routes `/impressions/etat-poste`, `/impressions/bulletin` annuel), `templates/impressions.html` (cartes), `templates/bulletin_officiel.html` (nouveau), `config.py` (VERSION 1.48).

## Presentation V1.47 — menu / accueil + compte FORMATION integre (classeur inchange)

- **Accueil reorganise** : Scolarite (pave reordonne du haut vers le bas : Salles, Etudiants, Enseignants, Referentiel des formations) et Administration en **pleine largeur** ; **Direction et Parametrage cote a cote** (2 blocs). La bande Parametrage devient une carte de la grille.
- **Menu de gauche** : **Parametrage** apparait desormais comme chapitre. Cliquer le titre d'un chapitre (Scolarite, Administration, Direction, Parametrage) **renvoie au bloc correspondant de l'accueil** (ancres `#scolarite`, etc.). Le menu Parametrage de la barre du haut (doublon) est retire.
- **Compte FORMATION integre** : en MODE_FORMATION uniquement, un compte pret a l'emploi **`formation` / `formation`** est cree automatiquement, **sans changement de mot de passe force**, avec les droits d'un superutilisateur. En production (drapeau absent) ce compte n'existe pas.

Couches : `config.py` (ordre des groupes Scolarite, flag `pleine`, num Parametrage, `FORMATION_LOGIN`/`FORMATION_MDP_DEFAUT`, `SUPERUSER_LOGINS` + formation si MODE_FORMATION, VERSION 1.47), `auth.py` (amorce du compte formation sans changement force), `templates/accueil.html`, `templates/base.html`, `static/css/style.css`. **Classeur inchange.**

### Mode FORMATION — procedure (sur une COPIE, jamais sur la production)
Le classeur `data/EMSP_V1.xlsx` est le meme en formation et en production : ne pas activer la formation sur l'installation de production (les ecritures pollueraient les donnees et openpyxl supprimerait les 16 dessins a la premiere sauvegarde). Pour une session :
1. Copier tout le dossier de l'application (ex. `emsp_formation`).
2. Dans cette copie, creer un fichier vide `instance/formation.flag`.
3. Lancer l'application : bandeau et filigrane FORMATION actifs ; se connecter avec **formation / formation**.
4. Pour reinitialiser : re-copier le dossier (ou remplacer `data/`). Pour repasser en production : supprimer `instance/formation.flag`.

## Editions V1.46 — corrections et documents EMSP manquants (classeur inchange)

Suite a la revue du catalogue, corrections et ajouts cote EDITIONS uniquement (aucune modification du classeur, md5 `4eb8bd6d44595616ebef85f79d462468`) :

- **Liste des etudiants** : ajout de la colonne « Origine / lieu actuel » (complement du lieu de naissance).
- **Releve d'heures** (individuel et recapitulatif) : la periode s'affiche en clair (« Juin 2026 ») au lieu de « 06/2026 » (helper `_periode_libelle`).
- **Situation de compte** : ajout de la colonne « Compte » apres « Chapitre », conformement au registre EMSP transmis. *Mapping a confirmer : la colonne est alimentee par le champ « Categorie » de F1 (Chapitre = « Poste budgetaire »).*
- **Feuille de presence de la semaine** (document A) : NOUVELLE edition en **paysage**, chaque journee decomposee en 4 creneaux (10h / 12h / 15h / 17h), colonnes date et lieu de naissance, **pre-remplie** avec les etudiants filtres (`feuille_presence_semaine`, kind `presence_semaine`). L'ancienne « feuille de presence vierge » (style stage) est conservee.
- **Fiche d'appreciation de stage** (document D, « Aptitudes generales a la fonction ») : NOUVELLE edition vierge reproduite a l'identique (`templates/appreciation_stage.html`).
- **Bulletin / releve de notes** : NOUVELLE edition imprimable a partir du moteur de notes (decret 05-106), avec exemple de formation (`templates/releve_print.html`).
- **Plan d'action** : NOUVELLE edition tableau (G1) — `plan_action_liste`.
- **Etats comptables** : NOUVEAUX — **Journal de tresorerie** (`journal_treso`) et **Situation globale / balance** (`balance_comptes`), reserves au profil financier. *D'autres etats possibles ensuite, sans engagement : etat des recettes/depenses par poste budgetaire, etat par bailleur.*

Toutes ces editions sont accessibles depuis le hub **Impressions**. Rendu generique « tableau » ajoute a `imprimer.html` + orientation paysage. Verification : **90 routes GET sans erreur 500** ; rendu PDF de chaque edition controle.

Couches : `metier.py`, `app.py` (6 routes `/impressions/*`), `templates/imprimer.html`, `templates/impressions.html`, `templates/appreciation_stage.html` (nouveau), `templates/releve_print.html` (nouveau), `static/css/print.css`, `config.py` (VERSION 1.46). **Classeur inchange.**

## Correctifs V1.45 — cohérence dates & monétaire (aucune modification du classeur)

Audit de cohérence et correction de trois défauts internes à `metier.py`, sans toucher au classeur (md5 inchangé `4eb8bd6d44595616ebef85f79d462468`, 27 onglets / 669 formules / 16 dessins) :

- **Doublon `_parse_date_fr`** : deux définitions coexistaient ; la seconde (renvoyant un tuple) masquait la première (renvoyant une `date`), ce qui **cassait la Situation de compte et le sélecteur de mois de la trésorerie** (erreur `'tuple' has no attribute 'year'`). Doublon supprimé. La fonction restante est **durcie** : elle accepte une `date`/`datetime` (cellule Excel typée) et les formats `JJ/MM/AAAA`, `JJ-MM-AAAA`, `AAAA-MM-JJ`.
- **Doublon `_num`** : la version active (`float(v)`) renvoyait **0** pour un montant écrit « 50 000 » ou « 12,5 ». Doublon supprimé : on conserve la version **tolérante** (espaces et virgule décimale).
- **Séparateur de milliers monétaire** : `_fmt_kmf` n'affichait pas le séparateur (« 799423 ») alors que `_kmf_aff` l'affichait (« 799 423 »), d'où un rendu **incohérent** entre trésorerie/clôture/tableau de bord et situation de compte/reçu. `_fmt_kmf` aligné sur `_kmf_aff` (espace, sans décimale inutile) ; les heures fractionnaires restent correctes.

Vérification : helpers testés unitairement ; **85 routes GET** passées sans erreur 500 ; écritures (ajout, présences, trésorerie, clôtures élèves/compta) OK ; situation de compte, trésorerie et état des signalements rendus correctement.

## Nouveautés V1.44 — Clôture / archivage / passation

- **Écran « Clôture & archivage »** (Paramétrage, **réservé à la Direction**), trois opérations
  manuelles produisant chacune un **procès-verbal** (Word `.docx` + page imprimable / PDF) :
  - **Clôture des élèves** (année scolaire, au 31/07) : les élèves sortis (Diplômé / Abandonné /
    Radié) sont inscrits au **journal permanent `J1_Journal_eleves`** (idempotent). Le **diplôme**
    et la **mention** (Passable / Assez bien / Bien / Très bien) sont **saisis à la clôture**. Les
    élèves restent dans `A1_Etudiants` ~3 ans.
  - **Archivage** : les cohortes sorties depuis **≥ 3 ans** sont déplacées vers
    `archives/EMSP_Archive_Eleves_AAAA-AAAA.xlsx`, retirées de `A1_Etudiants`, et leur référence
    d'archive est notée dans `J1`.
  - **Clôture compta** (année civile) : archive les mouvements de l'exercice dans
    `archives/EMSP_Archive_Compta_AAAA.xlsx`, écrit le **journal permanent `J2_Journal_compta`**,
    puis **report à nouveau** (une ligne par compte au 01/01/N+1 ; `F2.Solde initial` remis à 0 ;
    solde courant conservé).
- **Classeur (chirurgie du zip)** : ajout des onglets `J1_Journal_eleves` (12 colonnes) et
  `J2_Journal_compta` (7 colonnes). **16 dessins et 669 formules préservés**, 25 → 27 onglets.
  Nouveau md5 canonique : **`4eb8bd6d44595616ebef85f79d462468`** (ancien `574f357…`).
- **PV Word sans dépendance** : `.docx` généré au runtime via `zipfile` + XML brut (Calibri,
  titres #1F4E79). `requirements.txt` **inchangé** (Flask / openpyxl / pandas). Le PDF reste produit
  par impression navigateur (page `pv_cloture.html` + `print.css`), comme toutes les éditions.

## Lancer l'interface

**Windows** : double-cliquer sur `run.bat` (crée l'environnement Python au premier lancement, puis ouvre le navigateur sur http://127.0.0.1:5000).

**Linux / macOS** : `./run.sh`

Lancement manuel :
```
pip install -r requirements.txt
python app.py
```
Puis ouvrir http://127.0.0.1:5000

## Principes respectés

- **100 % hors-ligne, desktop only, aucun CDN.** Chart.js et Tabler Icons sont vendorés dans `static/vendor/`.
- **Charte** : couleur `#1F4E79`, police Calibri, zéro emoji, Tabler Icons, dates JJ/MM/AAAA, montants KMF sans décimales.
- **Architecture en couches** :
  - `data.py` — couche d'accès aux données (lecture seule du classeur),
  - `metier.py` — logique métier (provenance des champs, indicateurs, jeux de données),
  - `app.py` — présentation / routage Flask,
  - `config.py` — charte et structure du GUIDE.
- **Fichier Excel unique** : filière et type d'inscrit sont des colonnes (pas de découpage par filière).
- **Colonnes calculées protégées** : marquées « calcul », jamais saisies par l'IHM
  (`Total heures à payer`, `Solde courant`, `Statut vs base`, tout l'onglet TDB).

## Navigation (suit l'onglet GUIDE)

1. Paramétrages — Paramètres, Rôles, Import CSV
2. Étudiants — Fiches, Présences, Stages, Documents
3. Enseignements & salles — **Calendrier (mois/semaine/jour)**, Séances, **Salles — planning du jour**, Salles & équipements, Enseignants, Relevé d'heures
4. Finances & pilotage — Mouvements, Comptes, Tableau de bord, Plan d'action, Documents officiels, Matrice des autorisations
+ Référence — Légende, Guide, Dictionnaire

## Calendrier & salles (façon Outlook) — nouveau en V1.1

- **Logo** Université des Comores sur chaque page : en haut à gauche devant « EMSP » (barre latérale) et en pied de page. Vendoré dans `static/img/logo_udc.jpg`, aucun CDN.
- **Calendrier** (`/calendrier`) : l'emploi du temps des séances est **hebdomadaire récurrent** (`A3_Sessions`, colonne *Jour*) ; les vues **mois / semaine / jour** le **projettent** sur le calendrier.
  - *Mois* : vue d'ensemble, nombre de séances par jour-type ; clic sur un jour → vue *Jour*.
  - *Semaine* : grille Lundi–Samedi par horaire (axe vertical), blocs colorés par type (Cours / TD / TP).
  - *Jour* : séances de la journée + salles occupées + synthèse des présences (`A2_Presences`, par créneau).
- **Salles — planning du jour** (`/salles`) : colonnes façon agenda Outlook, une par salle, pour le jour choisi ; clic sur une salle → fiche détail.
- **Fiche salle** (`/salles/<id>`) : résumé de l'occupation (par qui, quand, pour quel groupe, quel type), équipements, caractéristiques, et boutons **Réserver / Voir qui a réservé / Annuler**.
  - En V1, ces actions sont en **aperçu non écrivant** (l'écriture dans le classeur est la prochaine étape). Le formulaire (nom, motif…) est affiché mais désactivé, avec une mention explicite.
- **Données de démonstration** : lien sur le calendrier et les salles pour visualiser le rendu tant que le classeur est vide (`?demo=1`).

## Saisie / édition depuis l'IHM — nouveau en V1.2

- **Sélecteur de rôle** dans la barre supérieure (liste tirée de `P1_Roles`, sans mot de passe, 100 % local). Il pilote les droits **lecture / écriture** selon la matrice `P1_Roles` (mapping groupes → onglets dans `config.MODULES_ONGLETS`, onglets réservés à la Direction, exigence d'accès financier pour `F1`/`F2`).
- **Premier écran écrivant : `P0_Parametres`** (les listes de référence dont dépendent toutes les listes déroulantes). Ajout / suppression de valeurs par liste, écriture immédiate dans le classeur. Réservé à la Direction.
- **Couche d'écriture** isolée dans `data.py` (`ajouter_ligne`, `ajouter_valeur_liste`, `supprimer_valeur_liste`) :
  - les **colonnes calculées** ne sont jamais saisies ; le **motif de formule est recopié** dans chaque nouvelle ligne → **plus aucune limite de lignes** ;
  - les onglets en lecture seule sont refusés ;
  - garde-fou de capacité (`CAPACITE = 50 000`) + **bandeau d'alerte** à l'approche du seuil.
- **Classeur** : toutes les plages d'agrégat et de colonnes calcul ont été **harmonisées sur 50 000** (fin des plafonds incohérents 300/5000, dont le solde des comptes qui ne sommait les mouvements que jusqu'à la ligne 300). Renvoi résiduel à `F3_Journal_audit` retiré du Dictionnaire. Le classeur sort donc de son état figé (normal dès qu'on écrit) ; version précédente archivée.

## Saisie A1_Etudiants & A3_Sessions + performances — nouveau en V1.3

- **Saisie de lignes** activee sur **Etudiants** (`A1_Etudiants`) et **Seances & planning** (`A3_Sessions`). Formulaire generique **pilote par le dictionnaire** : libelles, champs obligatoires (marques `*`), et **listes deroulantes** alimentees par l'onglet Parametres (filieres, niveaux, sections, annees, statuts, genres, types, jours). Droits par role : la scolarite peut saisir ces deux ecrans ; la comptabilite non.
- Les seances saisies apparaissent immediatement dans le **calendrier** et le **planning des salles**.
- **Performance** : le classeur etait recharge a chaque acces (jusqu'a ~90 fois par page en V1.2, d'ou la lenteur). Il est desormais **mis en cache et recharge uniquement s'il a change** (date de modification), avec invalidation a chaque ecriture. Pages ramenees de ~5 s a <100 ms. Aucun changement de donnees ni de formules : c'etait un defaut de lecture, pas un effet du volume.

## Provenance des champs (code couleur)

- noir = champ exigé par le **TDR**
- bleu + ★ = **initiative Webcreatys** (`*`)
- rouge + ★ = **ajout hors TDR** (`**`)

## État de cette V1 d'interface

Lecture/affichage de toutes les pages, AIDE sur chaque page, tableau de bord
avec graphiques sélectionnables (histogramme / camembert / radar), **calendrier** et **planning des salles**. La **saisie/édition depuis l'IHM** a démarré (écran `P0_Parametres`, écriture via la couche d'accès, droits par rôle). Les écrans d'écriture suivants seront ajoutés de façon incrémentale. Voir `ETAT.md`.

## Saisie des présences PAR SÉANCE (par lot) — nouveau en V1.4

- **Écran dédié** `/presences` (bouton « Ouvrir la saisie par séance » sur la page *Présences par créneau*). On choisit une **séance** (liste tirée de `A3_Sessions`), une **date** (JJ/MM/AAAA) et un **créneau** (10h/12h/15h/17h) ; l'**effectif de la classe** est chargé depuis `A1_Etudiants` (même filière, niveau et section). On coche les **présents** ; les non cochés sont comptés absents. « Saisi par » est renseigné automatiquement avec le login du rôle courant.
- **Anti-doublon (upsert)** : ré-enregistrer la même séance/date/créneau **met à jour** les présences existantes au lieu d'ajouter des lignes (clé d'unicité Date + Matricule + Session + Créneau). Nouvelle primitive `data.ecrire_lignes_lot(onglet, lignes, clés)` (mêmes garde-fous que `ajouter_ligne` : lecture seule refusée, colonnes calcul jamais saisies, clés préservées en mise à jour, capacité).
- **Listes liées inter-onglets** : `metier.options_liste()` résout désormais aussi une liste alimentée par **une colonne d'un autre onglet de données** (mapping lisible → (onglet, champ) dans `config.LISTES_ONGLET`). Dictionnaire mis à jour : `A2_Presences` *Matricule* → « Étudiants inscrits (A1) », *Session / Matière* → « Séances (A3) ».
- **Périmètre assumé** : `A2_Presences` est **hors-TDR** (tous champs `(**)`, besoin issu du CR du 11/06). Choix acté en V1.4 d'en faire une saisie de masse réaliste (et non un simple report V2). Droits : Direction et Chef de département peuvent saisir les présences ; la scolarité (Académique + Stages) et la comptabilité non.

## Saisie A4_Documents_etud (registre documentaire) — nouveau en V1.5

- **Saisie activée** sur *Documents & attestations* (`A4_Documents_etud`) via le formulaire générique (allowlist `ONGLETS_SAISIE_ACTIVE`).
- **Listes liées** : *Matricule* ← A1 (« Étudiants inscrits (A1) »), *Année concernée* ← liste `Annees_acad` (P0). Deux **nouvelles listes de référence dans P0_Parametres**, éditables par la Direction : *Types_document* (Attestation de passage, Bulletin, Relevé de notes) et *Statuts_document* (cycle de validation : En attente conseil → En attente délai → Imprimable → Remis).
- **Valeurs par défaut** dans le formulaire générique (`config.SAISIE_DEFAUTS`, résolu par `metier.champs_saisie`) : *Date génération* = date du jour (`@today`), *Statut* = En attente conseil. Modifiables à la saisie.
- **Périmètre V1** : A4 = **registre / suivi documentaire** (qui / quoi / année / statut / dates). La **génération PDF** des attestations, le **remplissage automatique** et l'**automatisation du cycle** (passage auto en Imprimable après le délai d'1 semaine) sont des **candidats V2**. A4 reste hors-TDR (champs `(**)`/`(*)`), construction issue du CR du 11/06.
- **Droits** : Académique (scolarité, chef de département) et Direction peuvent saisir A4 ; la comptabilité non.

## Saisie S1_Stages — nouveau en V1.6

- **Saisie activée** sur *Stages* (`S1_Stages`) via le formulaire générique.
- **Listes** : *Matricule* ← A1, *Année acad.* ← `Annees_acad` (P0), *Lieu de stage* ← `Lieux_stage` (P0), *Fiche retour* ← `O/N`. La liste **`Lieux_stage`** a été **pré-amorcée** avec les hôpitaux du projet ODS (CHN El-Maarouf, CHR Mitsamiouli, Foumbouni, Hombo, Domoni, Fomboni) — éditable par la Direction dans Paramètres.
- **N° séance (1-6)** : nombre libre. **Fiche retour** : défaut `N` (pas encore reçue).
- **Périmètre V1** : référentiel des lieux + affectation/planification (6 séances) + suivi de la fiche de retour, avec note /20 et observation libre. La **grille d'appréciation détaillée** (doc D) et la **gestion fine des plaintes** sont des **candidats V2**.
- **Droits** : Académique + Stages (scolarité), Direction. Comptabilité refusée (403).

## Saisie E1_Enseignants — nouveau en V1.7

- **Saisie activée** sur *Enseignants & vacataires* (`E1_Enseignants`) via le formulaire générique (allowlist `ONGLETS_SAISIE_ACTIVE`). Aucune colonne calcul sur E1 ; aucune modification du classeur (la liste du statut est résolue en *inline*).
- **9 champs.** Obligatoires : *Matricule ens.*, *Nom*, *Prénom*. Listes : *Genre* ← `Genres` (P0, M/F), *Statut (titulaire/vacataire)* ← liste **inline** `Titulaire/Vacataire` (`config.LISTES_INLINE`). Texte libre : *Matières enseignées*, *Qualifications*, *Département*, *Chef dept validant*.
- **Matricule provisoire `NC-<n>`.** Quand le matricule officiel n'existe pas encore, le formulaire **pré-suggère automatiquement** le prochain code libre `NC-<n>` (NC-1, NC-2…), résolu par `metier._prochain_nc()` (scan de E1, max + 1, insensible à la casse, ignore les vrais matricules). Il distingue chaque enseignant ; on le **remplace** par le vrai matricule le jour où il est connu. Token `@next_nc` dans `config.SAISIE_DEFAUTS`.
- **Périmètre V1** : fiche enseignant (identité, statut, matières, département). Le **lien Séances ↔ formateurs** (A3 `Enseignant` en liste ← E1) est l'étape **immédiatement suivante**, à câbler une fois E1 peuplé.
- **Droits** : groupe *Enseignants* dans `MODULES_ONGLETS`. En l'état de `P1_Roles`, seule la **Direction** (`Tous`) a l'écriture sur E1 ; pour confier les fiches à la scolarité ou au chef de département, ajouter *Enseignants* à leurs modules d'écriture dans P1_Roles (paramètre éditable Direction).

## Lien Séances ↔ formateurs — nouveau en V1.8

- Le champ **`Enseignant` de `A3_Sessions`** devient une **liste déroulante alimentée par les fiches E1** (libellé `Nom Prénom`), au lieu d'une saisie libre. Objectif TDR : garantir que chaque séance référence un formateur réel, sans faute de frappe.
- **Mécanisme** : nouvelle résolution de liste **composite** inter-onglets `config.LISTES_ONGLET_COMPOSITE` = `{ "Enseignants (E1)": ("E1_Enseignants", ["Nom","Prenom"], " ") }`, gérée par `metier.options_liste()` (valeurs distinctes, triées). Le Dictionnaire passe `A3_Sessions / Enseignant` de *Texte* à *Liste* (source « Enseignants (E1) »). Aucune autre couche.
- **Valeur stockée = libellé lisible** « Nom Prénom » : le calendrier et le planning des salles l'affichent tel quel, sans résolution. Le matricule reste la clé de E2 (heures), indépendamment. *(L'ordre `Nom Prénom` est paramétrable en une ligne dans `LISTES_ONGLET_COMPOSITE` si l'on préfère `Prénom Nom`.)*
- **Dépendance** : `Enseignant` étant obligatoire, **il faut saisir les fiches E1 avant de pouvoir enregistrer une séance** (même logique que « remplir P0 d'abord »). Documenté dans l'aide A3.
- **Classeur** : seule modification = la ligne du Dictionnaire (A3/Enseignant). Recalculé, **0 erreur** (669 formules) ; E1 et A3 restent vierges.

## Saisie E2_Releve_heures — nouveau en V1.9

- **Saisie activée** sur *Relevé des heures* (`E2_Releve_heures`) via le formulaire générique. Premier écran à **colonne calcul**.
- **4 champs éditables** (obligatoires : *Mois / Année*, *Matricule ens.*, *Vol. horaire constaté*) ; *Vol. horaire prog.* optionnel. *Mois / Année* : texte libre, format conseillé `MM/AAAA`.
- **`Matricule ens.` relié à E1 (choix (b2))** : liste déroulante **lisible** « Matricule — Nom Prénom », mais on **stocke le matricule seul** (clé du relevé de paie et de l'agrégat « heures par enseignant »). Nouveau mécanisme `config.LISTES_ONGLET_VALLABEL` (valeur ≠ libellé), résolu par `metier.options_liste()` en `{value,label}` ; les options de toutes les listes sont désormais normalisées en `{value,label}` (rendu `module.html` mis à jour, sans régression).
- **Colonne calcul « Total heures à payer » — affichage Python (choix (a))** : la formule (`=heures constatées`, heures seulement, sans taux) reste dans le classeur pour Excel ; l'IHM **calcule la valeur à l'affichage** (registre `metier.CALC_AFFICHAGE`, appliqué par `metier.table()`), donc le total apparaît immédiatement après saisie sans dépendre du recalcul Excel. Mécanisme **réutilisable** pour `F2_Comptes` et `IMPORT_zone` lors de leur activation.
- **Classeur** : seule modification = Dictionnaire `E2_Releve_heures / Matricule ens.` *Texte* → *Liste* (source « Enseignants matricule (E1) »). Recalculé, **0 erreur** (669 formules) ; copies racine/`data` byte-identiques ; E2 vierge.
- **Droits** : groupe *Enseignants*. En l'état de `P1_Roles`, seule la **Direction** écrit E2.

> **Point ouvert — matrice des autorisations (demande Direction).** Besoin exprimé : pouvoir **savoir qui a le droit de faire quoi sur quel module**, et **redéfinir les découpages** de modules (les groupes actuels Académique / Présences / Stages / Enseignants / Financier ne sont pas figés). À traiter à part : (1) une **vue lisible** rôles × modules (lecture/écriture, accès financier) dérivée de `P1_Roles` + `MODULES_ONGLETS`, (2) la **configurabilité** des groupes. Non développé en V1.9 (modèle de droits inchangé).

## Saisie L1_Salles — nouveau en V1.10

- **Saisie activée** sur *Salles & équipements* (`L1_Salles`) via le formulaire générique. Aucune colonne calcul. Les salles sont **créées par l'école elle-même** (le livrable reste vierge).
- **6 champs éditables** (obligatoires : *ID salle*, *Nom / libellé*). *Type* ← `Types_salle` (P0). *Équipements* en texte (séparés par `;`).
- **ID salle auto-suggéré `SAL-<n>`** : pré-rempli avec le prochain identifiant libre (même mécanisme que `NC-<n>`, généralisé en `metier._prochain_code()`), modifiable — les salles ont des **noms explicites** dans *Nom / libellé*, l'ID reste une clé courte. Token `@next_sal`.
- **`Types_salle`** complétée avec **Amphithéâtre** (déjà : Cours, TD, TP) — les salles « seront de plusieurs types (amphi, TD, TP, cours…) ». La Direction peut ajouter d'autres types dans Paramètres.
- **Effet** : les salles saisies alimentent le **planning des salles**, la **fiche salle**, et deviennent référençables par les séances (A3).
- **Classeur** : seule modification = valeur de référence *Amphitheatre* ajoutée à `Types_salle` (P0). Recalculé, **0 erreur** (669 formules) ; copies racine/`data` byte-identiques ; L1 vierge.
- **Droits** : groupe *Académique* → **scolarité ET Direction** peuvent éditer L1 (compta non).
- **Étape suivante** : relier le champ `Salle` de `A3_Sessions` à L1 (liste déroulante), comme pour l'enseignant.

## Lien Séances ↔ salles — nouveau en V1.11

- Le champ **`Salle` de `A3_Sessions`** devient une **liste déroulante alimentée par L1** (noms de salles), au lieu d'une saisie libre. **Facultatif** : une séance peut rester sans salle (champ non obligatoire), donc aucune dépendance bloquante.
- **Mécanisme** : `config.LISTES_ONGLET["Salles (L1)"] = ("L1_Salles", "Nom / libelle")` (déjà géré par `metier.options_liste`, aucun code nouveau). Dictionnaire `A3_Sessions / Salle` *Texte* → *Liste* (source « Salles (L1) »).
- **Valeur stockée = nom de la salle** : le rattachement au planning (`metier._seance_dans_salle`) matche par **nom OU id**, donc stocker le nom suffit et reste lisible dans le calendrier et le planning des salles.
- **Classeur** : seule modification = la ligne du Dictionnaire (A3/Salle). Recalculé, **0 erreur** (669 formules) ; copies racine/`data` byte-identiques.

## Matrice des autorisations — nouveau en V1.12 (lecture seule)

- Nouvelle page **Finances & pilotage → Matrice des autorisations** (`/autorisations`, clé menu `MAT_Autorisations`). **Lecture seule**, aucun changement du modèle de droits.
- **Tableau rôles × modules** dérivé de `P1_Roles` + `config.MODULES_ONGLETS` : pour chaque utilisateur/rôle, état par module — *Lecture*, *Écriture*, *Lecture + Écriture* ou *—* — plus la colonne *Accès financier* (O/N).
  - **Écriture = droit effectif** (`metier.peut_ecrire` : inclut le verrou *Accès financier* pour F1/F2 et les onglets en lecture seule).
  - **Lecture = droit déclaré** dans `P1_Roles` (la lecture n'est pas encore restreinte dans l'IHM ; seule l'écriture l'est — noté sur la page).
- **Définition des modules** : second tableau rappelant le découpage *module → onglets* (vos groupes actuels), pour décider d'éventuels regroupements.
- **metier** : `matrice_autorisations()` + `peut_lire()`. **app.py** : route `/autorisations`. **config** : entrée menu (Finances & pilotage) + `SPECIAL_ROUTES["MAT_Autorisations"]`. **Aucune modification du classeur.**
- **Pour modifier les droits** : éditer `P1_Roles` (réservé Direction). **Étape suivante à décider** : rendre le **découpage des modules configurable** (sortir `MODULES_ONGLETS` vers un onglet du classeur, ex. `P2_Modules`) — non fait (vos découpages ne sont pas figés ; cette vue sert à les arrêter d'abord).

## Administration des droits + superutilisateur — nouveau en V1.13

La page **Matrice des autorisations** devient **éditable** pour les administrateurs (anti-blocage par conception).

- **Colonne `Admin droits (O/N)`** ajoutée à `P1_Roles`. Ses porteurs peuvent gérer les utilisateurs depuis l'IHM. Pré-amorçage : **directeur = O** (à compléter : passer aussi l'administrateur informatique à O pour la sauvegarde mutuelle).
- **Superutilisateur** (`config.SUPERUSER_LOGINS = ["superadmin"]`, renommable en une ligne) : accès total + admin **garantis par le code**, même si `P1_Roles` est vide/cassé. **Ni supprimable ni rétrogradable** depuis l'IHM. Une ligne `superadmin` est livrée dans P1_Roles (sélectionnable dans le bandeau). C'est le **filet anti-blocage** : aucun verrouillage irréversible n'est possible.
- **Écran d'administration** (visible si le rôle courant est admin) : tableau des utilisateurs + formulaire ajouter/modifier (login, rôle, cases lecture/écriture par module + « Tous », accès financier, admin) + suppression. Un login existant ⇒ mise à jour (upsert, pas de doublon).
- **Garde-fous** : superutilisateur intouchable ; **impossible de retirer le dernier administrateur** ; confirmations sur suppression ; routes POST réservées aux admins (403 sinon).
- **metier** : `roles()` enrichi (admin/superuser), `est_admin()`, `enregistrer_utilisateur()`, `supprimer_utilisateur()`, `utilisateurs_admin()`. **data** : `supprimer_ligne_par_cle()`. **app.py** : routes `/autorisations/utilisateur` et `/autorisations/supprimer` + garde `_exige_admin` + `est_admin_courant` au contexte. **Classeur** : colonne `Admin droits` + ligne `superadmin` + doc Dictionnaire ; recalculé **0 erreur** (669 formules).
- **À décider ensuite** : rendre le **découpage des modules** (`MODULES_ONGLETS`) éditable depuis l'IHM (le sortir vers un onglet classeur).

## Saisie F1_Mouvements (trésorerie) — nouveau en V1.14

- **Saisie activée** sur *Recettes & dépenses* (`F1_Mouvements`) via le formulaire générique. 16 colonnes, aucune colonne calcul. **Accès réservé** : Comptabilité et Direction (Accès financier = O).
- **15 champs saisissables** (obligatoires : Date opération, Sens, Catégorie, Compte / caisse, Libellé). *Saisi par* est **exclu du formulaire** et rempli automatiquement avec le login courant (traçabilité AFD).
- **Catégorie (choix A-a)** : liste **combinée** `Cat_Recettes` + `Cat_Depenses` (résolution `metier.options_liste` du motif `"… OU …"`). Pas de liste dépendante du sens en V1.
- **Montants conditionnels (choix B-b)** : validation métier `metier._valide_f1_mouvements` (via registre `_VALIDATIONS_SPECIFIQUES`) — *Sens = Recette* exige le Montant Recette (et interdit le Montant Dépense), et inversement.
- **Listes inline** : *Sens* `Recette/Depense`, *Statut* `Previsionnel/Realise` (`config.LISTES_INLINE`). **Défaut** *Date opération* = `@today`.
- **Bailleur** ← `Bailleurs` (P0, amorcée) — colonne de **traçabilité AFD**. *Mode paiement* ← `Modes_paiement` (amorcée).
- **Dépendance P0** : avant saisie, remplir `Cat_Recettes`, `Cat_Depenses`, `Comptes_caisses` (obligatoires) et éventuellement `Postes_budgetaires` dans Paramètres (non pré-amorcés : spécifiques à l'école). Documenté dans l'aide F1.
- **Cohérence F1 ↔ F2** : *Compte / caisse* ← `Comptes_caisses` (P0) ; à l'activation de F2, *Nom du compte* tirera de la même liste pour que le `SUMIF` du solde corresponde.
- **config** : `F1_Mouvements` dans `ONGLETS_SAISIE_ACTIVE` ; `CHAMPS_AUTO_LOGIN` ; listes inline + défaut date. **app.py** : injection serveur du *Saisi par*. **Aucune modification du classeur.**

## Saisie F2_Comptes (comptes & soldes) — nouveau en V1.15

- **Saisie activée** sur *Comptes & caisses* (`F2_Comptes`), dernier écran financier. **Accès** : Comptabilité et Direction.
- **3 champs saisissables** (obligatoires : Nom du compte, Solde initial) ; *Solde courant* = **colonne calcul** (non saisissable).
- **Nom du compte ← `Comptes_caisses` (P0)** : même liste que `F1.Compte / caisse`, donc le `SUMIF` du solde correspond toujours (cohérence F1 ↔ F2). *(Dictionnaire F2/Nom du compte : Texte → Liste.)*
- **Solde courant — affichage Python LIVE** (`metier._solde_courant_f2`) : `solde initial + Σ recettes − Σ dépenses` du compte, lues dans F1. Recalculé à chaque affichage (l'affichage des colonnes calcul est désormais **toujours recalculé** : une saisie F1 dans l'IHM ne déclenche pas le recalcul Excel, donc la valeur en cache serait périmée). La formule reste dans le classeur pour Excel. KMF sans décimales inutiles (charte).
- **Type** ← inline `Banque / Caisse / Autre`.
- **À noter** : une ligne par compte (ne pas dupliquer) ; remplir `Comptes_caisses` (P0) au préalable.
- **config** : F2 dans `ONGLETS_SAISIE_ACTIVE` ; `LISTES_INLINE += Banque/Caisse/Autre` ; VERSION 1.15. **metier** : `CALC_AFFICHAGE["F2_Comptes"]` + `_solde_courant_f2` + helpers `_num`/`_fmt_kmf` ; `_appliquer_calc_affichage` recalcule toujours. **Classeur** : Dictionnaire F2/Nom du compte (Texte → Liste) ; recalculé **0 erreur** (669 formules).

**Le module financier est complet (F1 + F2).**

## Import CSV national (IMPORT_zone) — nouveau en V1.16

- **Écran dédié** `/import` (menu *Paramétrages*), réservé à la **Direction**. Routage via `SPECIAL_ROUTES["IMPORT_zone"] = "import_csv"`.
- **Coller le CSV** national : séparateur auto-détecté (tabulation / `;` / `,`), ligne d'en-tête ignorée (première cellule sans chiffre = en-tête). Les 7 colonnes A→G (Matricule, Genre, Nom, Prénom, Date naissance, Lieu naissance, Niveau/Filière) remplissent la zone de staging IMPORT_zone.
- **Statut vs base** calculé en Python live (`metier._statut_vs_base_import`) : **NOUVEAU** si le matricule est absent de `A1_Etudiants`, **EXISTANT** sinon. Compteurs nouveaux/existants affichés.
- **Import manuel** : la copie des NOUVEAU vers la fiche étudiants (A1) reste **manuelle** ; cette zone **ne modifie jamais A1** (aucun risque sur les données réelles).
- **Retour en arrière** : avant chaque *Importer* ou *Vider*, un instantané de la zone est sauvegardé sur disque (`import_undo.json`, à côté du classeur) ; le bouton **Annuler** restaure la version précédente (annulation à un niveau).
- **data.py** : `remplacer_donnees(onglet, lignes)` (vide puis réécrit, formules recopiées). **metier.py** : `parser_csv`, `import_zone_brut`, `importer_csv`, `vider_zone_import`, `annuler_import`, `import_resume` ; `CALC_AFFICHAGE["IMPORT_zone"]`. **app.py** : routes `/import`, `/import/importer`, `/import/vider`, `/import/annuler` + garde Direction. **template** : `import.html`. **Aucune modification du classeur** (structure + formule déjà présentes).

### Correctif important (V1.16)
`ws.cell(row, col, value=None)` **n'efface pas** une cellule sous openpyxl (le paramètre est ignoré). Corrigé en `ws.cell(row, col).value = None` dans `remplacer_donnees` **et** `supprimer_ligne_par_cle` (la purge ne vidait pas le résidu — bug latent qui aurait laissé un doublon lors de la suppression d'une ligne du milieu de P1_Roles). Testé.

### Chantiers d'ergonomie à venir (notés, non faits)
- Retirer des interfaces les références au cahier des charges (codes A1, A4…) au profit de libellés parlants.
- Ajouter une **icône par module** pour le repérage visuel.
- Rendre la **page d'accueil** plus conviviale.

## Impressions & éditions — nouveau en V1.18

Module d'édition des documents courants de l'école, **100 % hors-ligne** (rendu HTML +
`@media print`, impression ou export PDF via le navigateur — aucun moteur PDF externe).

**6 documents + 1 export :**
1. **Liste d'étudiants** — filtrable par filière / niveau / section / année (A1).
2. **Feuille de présence vierge** — grille à signer (60 lignes par défaut, en-tête à compléter à la main).
3. **Relevé d'heures individuel** (paie) — un enseignant, une période (E2 + identité E1).
4. **Récapitulatif mensuel des heures** — tous les enseignants pour un mois + total général (E2 + E1).
5. **Reçu de paiement numéroté** — depuis une recette de la trésorerie (F1). N° **REC-AAAA-NNNN**
   déduit par scan de la colonne *Référence / N pièce* (max de l'année + 1, réinitialisé chaque année),
   modifiable à l'impression. Réservé à l'accès financier (Comptabilité / Direction).
6. **Attestation de passage** — version imprimable simple (le cycle de validation automatisé reste V2).
7. **Export Excel du tableau de bord** — vrai `.xlsx` (openpyxl) : synthèse + 5 tables (effectif par
   filière, statuts, recettes/dépenses, présence par créneau, heures par enseignant).

**Modèles persistants éditables.** Les parties fixes (en-tête, titre, corps à **jetons** `{…}`,
mentions/pied, libellé du signataire, nombre de copies) se règlent dans **Paramétrages → Modèles de
documents** et sont stockées dans le classeur (onglet additif `D1_Modeles_docs`). À l'impression, les
jetons sont remplacés par les données réelles et le contenu reste **retouchable à la main** (modifications
ponctuelles non enregistrées) avant impression.

**Couplage classeur.** Ajout **additif** d'un onglet `D1_Modeles_docs` (texte, **aucune formule**) :
les 19 onglets et les **669 formules** existants sont inchangés (vérifié par recalcul LibreOffice,
0 erreur). C'est la **dernière modification additive du classeur avant la bêta**.

Architecture : `config.MODELES_DOCS` (métadonnées + textes par défaut des 6 modèles), `metier`
(lecture/écriture des modèles, builders de chaque document, `_prochain_recu`, `export_tdb_xlsx`),
`app` (`/impressions`, `/modeles`, vues d'impression `/impressions/...`, export), templates
`impressions.html` (hub), `modeles.html` (édition), `imprimer.html` (page autonome) + `static/css/print.css`.

## Registres Réservations & Équipements — nouveau en V1.19

Préparation de la future couche « requêtes multicritères » : deux nouveaux **onglets de données**
(modules de saisie complets), plus une catégorie de droits **Logistique**.

- **Réservations de salles (`L2_Reservations`)** — réservations **hors cours** (réunion, examen,
  événement, partenaire) : salle (liste L1), date, heures, demandeur, motif, statut. Tenu **à part**
  de l'emploi du temps `A3_Sessions`, qui est un planning hebdomadaire récurrent (jour-type, sans
  date) : une réservation est datée et ponctuelle. La future vue d'occupation d'une salle réunira
  les cours (A3) et ces réservations (L2).
- **Équipements & inventaire (`M1_Equipements`)** — **inventaire de pilotage** : désignation,
  catégorie, salle/localisation (liste L1), date d'acquisition, **bailleur** (liste P0 partagée avec
  la trésorerie F1), montant, rappel de la pièce F1, état, n° d'inventaire. **Sans maintenance**
  (pannes, contrats, pièces détachées = futur GMAO, hors périmètre). Permettra de sortir, par exemple,
  les équipements financés par l'AFD et leur localisation.

Listes P0 : **Bailleurs** (déjà partagée avec F1) et **Categories_equipement** (nouvelle, paramétrable).
Codes pré-suggérés `RES-n` / `EQ-n`. Couplage classeur : ajout **additif** de 2 onglets + 1 colonne P0 +
21 lignes au Dictionnaire ; les **669 formules** sont inchangées (recalcul LibreOffice, 0 erreur,
22 onglets). Dernier lot additif avant la bêta.

**À suivre (V1.20, en lecture seule, sans modification du classeur)** : la couche « requêtes » —
explorateur multicritères par table + vues métier prédéfinies (équipements & localisation ;
salles réservées et quand ; absences élèves cours/stage + observations ; équipements par bailleur ;
écart programmé/constaté des enseignants par période) + export Excel de chaque sélection.

## Saisie en grille — Registre de trésorerie — nouveau en V1.20

Réponse à un constat de terrain : le formulaire « une ligne à la fois » convient pour un ajout
ponctuel, mais pas pour **saisir un registre comptable** (le document papier « Situation de compte »
se remplit en grille, avec un solde courant ligne après ligne). On ajoute donc un **mode tableur**
pour la trésorerie, sans rien changer au classeur (écriture dans l'onglet F1 existant).

Écran **Trésorerie → Saisie en grille** (bouton sur la page *Recettes & dépenses*, accès financier) :
on choisit **un compte / caisse** (le **solde d'ouverture** affiché est son solde courant), on saisit
plusieurs lignes en tabulant de cellule en cellule, le **solde se recalcule en direct** à chaque
montant, puis **un seul** « Enregistrer tout » écrit le lot. Colonnes dans l'ordre du registre : Date,
Catégorie, Poste budgétaire (Chapitre), Référence / N° pièce, Mode paiement, Description, Bénéficiaire,
Bailleur, **Recette** et **Dépense** (l'une *ou* l'autre par ligne — le sens en est déduit). Solde =
solde initial du compte + Σ(recettes − dépenses), cohérent avec le solde courant des comptes (F2).

Robustesse : les lignes vides sont ignorées ; la saisie est **atomique** (si une ligne est invalide,
rien n'est écrit et la saisie est conservée à l'écran avec le détail des erreurs, ligne par ligne).
Couche d'accès : nouvelle primitive `data.ajouter_lignes` (ajout par lot en une seule ouverture du
classeur). **Aucune modification de structure du classeur** (md5 inchangé, 22 onglets, 669 formules).

**À suivre** : l'édition imprimable « Situation de compte » (registre signé Gestionnaire/Directeur),
puis la couche requêtes multicritères (lecture seule), puis l'explication de la matrice des droits
(distinction droits / traçabilité « qui a saisi »).

## Édition « Situation de compte » — nouveau en V1.21

Complément du volet comptable : un **registre mensuel imprimable** qui reproduit le document papier
signé (Gestionnaire + Directeur). Dans **Impressions & éditions** (accès financier) : on choisit un
**compte / caisse** et une **période (MM/AAAA)**. L'aperçu présente une ligne **« Report à nouveau »**
(solde au début de période = solde initial + mouvements antérieurs), les **mouvements de la période**
avec un **solde courant ligne après ligne**, puis **« SOLDE AU JJ/MM/AAAA »**. Colonnes : N°, Chapitre
(= Poste budgétaire), Date, N° pièce, Description, Bénéficiaire, **Débit** et **Crédit**, Solde.

Convention reprise du document (Solde = Débit − Crédit) : **Débit = Recette** (entrée), **Crédit =
Dépense** (sortie), donc Solde = recettes − dépenses, cohérent avec le solde des comptes (F2).
Document **paramétrable** comme les autres (en-tête, titre, mentions, signataires) ; il porte **deux
signataires** (Gestionnaire / Directeur). Lecture seule sur F1/F2 — **aucune modification du classeur**.

## Requêtes & analyses (lecture seule) — nouveau en V1.22

Objectif : donner à la Direction la puissance d'Excel (filtres, tri, croisements) **sans ouvrir une
copie du fichier** — donc sans risque pour la source unique ni les formules. Tout est en **lecture
seule** ; chaque sélection s'exporte en Excel (la soupape qui évite d'aller « taper » ailleurs).

**Explorateur de tables** (`/requetes/explorer`) : on choisit n'importe quelle table de données, on pose
jusqu'à 3 **filtres cumulatifs** (contient, égal, commence par, &gt;, &lt;, non vide, vide), on **trie**
(numérique ou texte), on **choisit les colonnes**, et on **exporte en .xlsx**.

**Vues métier prédéfinies** (`/requetes/vue/<id>`) — répondent aux questions récurrentes, y compris
en croisant plusieurs tables :
- **Équipements et localisation** (Q1) — inventaire M1, filtrable par salle / bailleur / catégorie.
- **Salles : qui occupe et quand** (Q2) — union des **cours** (A3) et des **réservations** (L2).
- **Équipements par bailleur** (Q4) — financés par l'AFD ou un autre bailleur, avec total des montants.
- **Enseignants : écart programmé/constaté** (Q5) — heures non assurées par enseignant, sur une période.

Chaque vue et chaque résultat d'explorateur dispose d'un **export Excel** (un classeur d'une feuille,
en-tête + lignes). **Aucune modification du classeur** (md5 inchangé, 22 onglets, 669 formules).

**À suivre (prochaine brique)** : la vue absences élèves cours/stage (Q3, avec ses nuances de données),
un tableau croisé léger (pivot), puis l'explication de la matrice des droits (Nota 1).

## Requêtes — 2ᵉ brique : absences (Q3) + tableau croisé — nouveau en V1.23

Complète la couche requêtes (toujours en lecture seule, aucune modification du classeur).

**Vue « Absences élèves & observations » (Q3)** — unifie deux sources : les **absences en cours**
(A2, lignes où la présence n'est pas « O ») et les **observations / plaintes de stage** (S1). Filtrable
par étudiant et par origine (cours / stage). Nuances assumées et documentées : A2 n'a pas de champ
commentaire, et l'absence en stage n'est pas modélisée comme telle — on remonte donc l'observation
ou la plainte saisie sur le stage.

**Tableau croisé (pivot)** — façon TCD léger : une dimension en **lignes**, une (facultative) en
**colonnes**, une **mesure** (Nombre, Somme, Moyenne sur une colonne). Totaux corrects (la moyenne
d'un total = somme / effectif, pas une moyenne de moyennes). Exemple : effectif par filière × niveau.
Export Excel comme les autres.

Avec cette brique, les **5 questions** de départ sont couvertes (équipements & localisation, salles
occupées/réservées, absences cours/stage, équipements par bailleur, écart enseignants), plus
l'explorateur générique et le pivot. **Reste** : l'explication de la matrice des droits (Nota 1).

## Authentification réelle + journal d'audit — nouveau en V1.24

Fini le simple sélecteur de rôle : l'accès se fait désormais par **identifiant + mot de passe**, et
les droits restent **définis par l'administrateur** (matrice `P1_Roles`). Le champ « Saisi par » et le
journal reflètent donc l'utilisateur **réellement** connecté.

**Sécurité (dépôt public).** Les mots de passe ne sont **jamais** stockés en clair, et **jamais** dans
le classeur ni le dépôt : seules des **empreintes** (`pbkdf2:sha256`) sont écrites dans un fichier
**local** `instance/comptes.json`, créé au premier lancement, listé dans `.gitignore` et **exclu du
zip**. Le classeur poussé sur GitHub ne contient que les **logins et droits**, aucun secret.

**Connexion / compte.** Écran de connexion ; un utilisateur peut **changer** son mot de passe
(`/mot-de-passe`). L'**admin** crée un compte avec un **mot de passe initial** (à changer au premier
login), peut le **réinitialiser**, et la suppression d'un utilisateur retire aussi son accès. Un
**superadmin** est garanti par le code : au tout premier lancement il est créé avec le mot de passe
initial `admin` (constante `SUPERUSER_MDP_DEFAUT`), **à changer immédiatement** (changement forcé).

**Journal d'audit** (`/journal`, réservé admin) : trace locale append-only « qui a fait quoi, quand »
(connexions, saisies, trésorerie, import, changements de droits, mots de passe…). Il ne contient
**aucun secret** et reste **local** (`instance/journal.csv`, gitignoré, hors zip) — utile pour la
traçabilité, notamment financière (AFD).

Aucune modification du classeur (md5 `0614d315…`, 22 onglets, 669 formules) : l'authentification vit
entièrement dans des fichiers locaux séparés.

## Référentiel des formations (maquettes) — nouveau en V1.25

Intégration des **maquettes pédagogiques officielles** des 5 filières comme **référentiel UE / matières**, socle des notes et du suivi des heures.

- **Classeur (fenêtre additive rouverte, proprement)** : nouvel onglet **`R1_Maquettes`** ajouté **par chirurgie du zip** (sans repasser par openpyxl) afin de **ne toucher à aucun onglet existant** : les 669 formules, leurs valeurs calculées, les 16 dessins et les 13 validations sont **conservés à l'identique** (200 cellules-formules comparées, 0 différence). Le classeur passe de **22 à 23 onglets**. Nouveau md5 canonique : **`9337d1a9fe74b2e61d5f45e9749479a9`** (l'ancien `0614d315…` correspondait au classeur 22 onglets, gelé V1.19→V1.24).
- **Contenu R1** (lecture seule, 661 matières) : `Filière, Niveau, Semestre, N° UE, Intitulé UE / Module, Matière / Contenu, Enseignant, CM, TD, TP, Total heures, Vol. horaire UE, Crédit (ECTS), Coef`. Extraction exhaustive des 5 feuilles (dispositions hétérogènes gérées : en-têtes détectés, sections « Semestre », cellules fusionnées propagées). Aides-soignants intégrés en `Niveau = AS`, UE vide, module dans « Intitulé ».
- **config** : `R1_Maquettes` ajouté au menu (section « Enseignements & salles ») ; page servie par la route générique `/module/<onglet>` en **consultation** (filtrable, export Excel). VERSION 1.25.
- **metier** : helpers `matieres_maquette(filière, niveau, semestre)` et `heures_programmees(...)` — prêts pour le branchement des matières dans les séances (A3) et du volume programmé dans le suivi des heures (E2).
- **À venir (sur confirmation, ne touche pas au classeur)** : datalist des matières sur A3 alimentée par la maquette ; volume programmé E2 ; puis modules Notes/relevés et Stages.

## Suggestions matière + pré-remplissage du volume — nouveau en V1.26

- Le champ **`Matiere` de `A3_Sessions`** devient une **saisie libre avec suggestions** (`<datalist>`)
  alimentée par la maquette `R1_Maquettes`, **filtrée par Filière + Niveau + Semestre** de la ligne
  saisie. La saisie reste libre : on peut taper une matière absente de la maquette.
- **Pré-remplissage** : quand la matière correspond à la maquette, le champ **`Vol. horaire prog.`**
  est rempli avec la somme des heures programmées (« Total heures ») — **seulement s'il est vide**,
  et la valeur reste modifiable.
- **Hors-ligne** : filtrage et pré-remplissage exécutés côté navigateur à partir des lignes maquette
  injectées en JSON dans la page (aucun réseau, aucun CDN).
- **Semestre** : la maquette code le semestre en cursus (`1..6`), A3 saisit `S1`/`S2` (année) ; le
  client dérive le cursus de (Niveau, Semestre). Niveau hors L1/L2/L3 ⇒ filtre Filière+Niveau seuls.
- **Mécanisme** : `config.MAQUETTE_DATALIST` (déclaration par onglet), `metier.maquette_lignes_datalist()`
  + `metier.maquette_datalist_cfg()`, passage au template dans `app.module()`, rendu + script dans
  `templates/module.html`. Le **Dictionnaire reste `Texte`** (suggestions, pas liste stricte) :
  **classeur inchangé**.

## Écart programmé vs constaté (relevé d'heures) — nouveau en V1.27

- La page **Relevé d'heures** (`E2_Releve_heures`) affiche une colonne **« Ecart (prog. - constate) »**
  = `Vol. horaire prog.` − `Vol. horaire constate`, avec signe explicite (`+`/`−`) et sans décimale
  inutile. L'écart ne s'affiche **que si les deux valeurs sont renseignées**.
- **Saisie inchangée** : programmé et constaté restent saisis à la main ; le logiciel calcule l'écart
  (et le total à payer reprend le constaté). Pas d'alimentation automatique depuis les emplois du temps.
- **Classeur inchangé** : l'écart est une **colonne d'affichage** (calculée à la volée), pas une colonne
  du classeur. Mécanisme `metier.COLONNES_AFFICHAGE_EXTRA` (colonnes virtuelles, lecture seule),
  réutilisable pour d'autres onglets.

## Module Stages — référentiel des lieux (socle) — nouveau en V1.28

- Nouvel onglet **`S2_Lieux_stage`** : référentiel des lieux d'accueil avec **quotas**. Colonnes :
  Lieu / structure, Service, Commune, Niveau concerné (vide = tous), Quota (nb max de stagiaires par
  séance), Période de disponibilité. Saisissable (droits du module Stages).
- Le champ **`Lieu de stage` de `S1_Stages`** est désormais alimenté par ce référentiel, sous forme
  **« Lieu — Service »** (Service facultatif). Fini la liste P0 générique.
- **Classeur** : `S2_Lieux_stage` ajouté par chirurgie du zip (aucune feuille existante modifiée),
  intégrité vérifiée. Nouveau md5 canonique `fba973b7cb4ffcd1a143e49e62bf2ba9` (24 onglets).
- **Approche** : saisie assistée avec contrôle humain (pas d'affectation automatique), génération
  séance par séance. À venir : contrôle de quota à la saisie (places restantes) et tableau de bord stages.
- **Mécanisme** : `config.DICTIONNAIRE_SUPPLEMENT` / `DICTIONNAIRE_SURCHARGE` (métadonnées de S2 et
  nouvelle source de S1, gérées hors onglet Dictionnaire), `LISTES_ONGLET_COMPOSITE` (« Lieux de stage (S2) »).

## Module Stages — contrôle de quota & tableau de bord — nouveau en V1.29

- **Saisie assistée** : sur la page Stages, à la saisie d'un stage, un indicateur affiche les **places
  restantes** pour le lieu choisi selon l'année et la séance (Quota − affectations déjà enregistrées
  pour ce lieu/cette année/cette séance). Non bloquant : « complet » est signalé mais la saisie reste
  possible (contrôle humain).
- **Tableau de bord d'occupation** : panneau avec sélecteurs Année / Séance, tableau par lieu
  (Quota / Occupés / Restants) et compteurs (lieux, étudiants affectés, places occupées, taux). Le
  quota s'entend par séance.
- **Classeur inchangé** (`fba973b7cb4ffcd1a143e49e62bf2ba9`) : tout est calculé à l'affichage côté
  client, à partir du référentiel S2 et des affectations S1.
- **Mécanisme** : helpers `metier.stages_*`, contexte passé pour `S1_Stages`, panneau + script local
  dans `module.html`. Pas d'affectation automatique (choix : contrôle humain).

## Module Notes — socle (fichier séparé) — nouveau en V1.30

- Nouveau **fichier séparé `EMSP_Notes.xlsx`** (confidentialité par séparation physique), avec un
  onglet **Lisez-moi**, le **barème `N1_Bareme_UE`** (Filière, Niveau, Semestre 1-6, N° UE, Intitulé,
  Matière, Coef UE, ECTS UE) et la **saisie `N2_Notes`** (Matricule, Année, Session 1/2, Semestre,
  N° UE, Matière, CC, Examen).
- **Le barème est la référence du calcul** : c'est dans `N1_Bareme_UE` que l'on définit, par
  filière/niveau/semestre, les UE, leurs matières, coefficients et ECTS — à renseigner avant la
  saisie des notes (rappelé dans l'onglet Lisez-moi du fichier).
- **Accès** : module de droits « Notes ». Les rôles « Tous » (Direction, superadmin) y accèdent ; les
  autres seulement si l'admin ajoute le module « Notes » à leur ligne dans `P1_Roles`. La scolarité
  Académique/Stages n'y a pas accès par défaut.
- **Architecture** : couche d'accès dédiée au 2ᵉ fichier (`metier._db_notes` / `_db_pour`), routée par
  `config.ONGLETS_NOTES`. Classeur principal inchangé.
- À venir : moteur de calcul (moyennes, mention, proposition Admis/Ajourné, 2ᵉ session) et relevé par
  étudiant (semestre + annuel).

## Module Notes — moteur de calcul & relevé — nouveau en V1.31

- **Calcul** (décret 05-106) : moyenne matière = ¼ CC + ¾ examen (ou note unique) ; moyenne UE =
  moyenne des matières ; moyenne semestre = moyenne des UE pondérée par coefficient. Cascade sur
  valeurs **exactes**, arrondi commercial (demi vers le haut) à 2 décimales seulement pour
  l'affichage/validation. 2ᵉ session : la note de septembre remplace celle de juin.
- **Validation / mention / proposition** : UE validée si ≥ 10 ; semestre admis si toutes UE ≥ 10 ou
  moyenne ≥ 10 (compensation) ; mention Passable/AB/B/TB ; proposition Admis/Ajourné. La décision
  finale (délibération) reste manuelle.
- **Relevé** (`/releve`) : par étudiant, par semestre **ou** récapitulatif annuel, format proche du
  bulletin, avec **impression** et **export Excel**. Filière/niveau/nom repris de `A1_Etudiants`.
- Moteur validé contre un bulletin réel (L2 Soins infirmiers).

## Assistance à la saisie des notes — nouveau en V1.32
À la saisie d'une note (`N2_Notes`), les champs **N° UE** et **Matière** proposent des suggestions
tirées du barème (`N1_Bareme_UE`), filtrées par la filière/niveau de l'étudiant (via le matricule) et
le semestre. Choisir une matière pré-remplit le N° UE. Saisie libre conservée, filtrage hors-ligne.

## Signalements / indiscipline — nouveau en V1.33
Onglet `N3_Signalements` (fichier notes) : Matricule, Date, Année, Semestre (facultatif), Contexte,
Émis par (fonction), Nom de l'émetteur, Motif. Information de délibération **non bloquante** : elle
n'affecte ni le calcul ni la proposition. Sur le relevé à l'écran, un encart liste les signalements et
une mention « N signalement(s) à examiner » apparaît près de la proposition — le tout **exclu** du
bulletin officiel imprimé et de l'export. À venir : un état récapitulatif des signalements pour la scolarité.

## État des signalements (par étudiant) — nouveau en V1.34
Page `/etat-signalements` : compte rendu disciplinaire groupé par étudiant, filtrable par année, plage
de dates (du/au), semestre, contexte, filière, niveau. Sans les notes. Imprimable et exportable en
Excel. Réservé au module Notes.

## Barème confirmé / provisoire — nouveau en V1.35
Le barème `N1_Bareme_UE` gagne une colonne **`Coef confirmé` (Oui/Non)** et est désormais **pré-rempli** :

- **L2 Soins infirmiers (S3 et S4)** : barème **confirmé** (`Coef confirmé = Oui`), coefficients et ECTS
  réels issus du relevé de notes officiel. Le moteur de calcul a été revalidé dessus (moyenne S3 = 9,89,
  identique au bulletin).
- **Soins infirmiers (hors L2), Soins obstétricaux, Maintenance biomédicale, Imagerie médicale** :
  structure UE/matières reprise des maquettes, mais **coefficient à 1 par défaut** (`Coef confirmé = Non`),
  car les maquettes ne portent pas de coefficient exploitable. Les ECTS sont repris quand ils existent.
  Aides-soignants non intégré (modèle Modules/Contenus incompatible avec le barème).

Tant qu'une UE n'est pas confirmée, le relevé (écran **et** impression) porte la mention **« Barème
provisoire »** : les coefficients devront être corrigés d'après le document de référence officiel pour
que les moyennes soient conformes aux exigences de passage. La scolarité peut éditer le barème dans
l'écran *Barème des UE* (passer `Coef confirmé` à Oui une fois les coefficients officiels saisis).

Le remplissage est fait par le script versionné **`scripts/seed_bareme.py`** (idempotent ; données du
squelette figées dans `scripts/maquettes_skeleton.json`, sans dépendance au fichier des maquettes).

> Note (relevé L2 SI) : la matière **« Stage2 » figure à la fois en UE16 (S3) et UE21 (S4)**, conformément
> au relevé officiel (L2 Soins infirmiers, session 2024-2025). Ce n'est pas un doublon ; le barème étant
> indexé par semestre, les deux occurrences restent distinctes.

## Présentation réorganisée — nouveau en V1.36
Le menu et la page d'accueil sont regroupés en **trois grands ensembles**, avec des **sous-groupes** :

- **Scolarité** : Filières · Enseignants · Étudiants · Salles.
- **Administration** : Finances & pilotage (trésorerie, comptes, requêtes, impressions, plan d'action,
  documents officiels) · Logistique / moyens généraux (équipements).
- **Direction** : tableau de bord uniquement.

Le **Paramétrage** (paramètres, rôles & droits, matrice des autorisations, import du fichier national,
modèles de documents) n'est plus une rubrique centrale : il est **déporté sur la droite** (menu dédié
dans la barre du haut) et repris dans un bandeau séparé en bas de l'accueil.

Les **textes d'aide** ont été nettoyés des mentions « V2 » (remplacées par « pistes possibles ensuite,
sans engagement », conformément à la charte). Aucun fichier Excel n'est modifié par ce lot (présentation
seule : `config.py` + gabarits + CSS).

> À venir (validé en réunion, lots suivants, avec ajouts Excel additifs maîtrisés) : matériel ACTIF/PANNE
> + localisation provisoire (M1) ; classification des documents officiels (H1, catégories éditables par
> le directeur) ; plan d'action enrichi (types d'écart + statut de planning) ; expression de besoin
> logistique ; révision des droits de la Direction (plus consultation que saisie).

## Affichage des grands tableaux — nouveau en V1.37
Les tableaux de consultation (référentiel des formations R1, mais aussi tout autre onglet de données)
disposent désormais, côté client (hors-ligne), de :

- une **recherche plein texte** au-dessus du tableau (insensible aux accents et à la casse) ;
- un **filtre par colonne** sous chaque en-tête : liste déroulante des valeurs quand elles sont peu
  nombreuses, sinon champ « contient » ;
- une **pagination** (20 lignes par défaut, ou 40 / 100 / Toutes) avec compteur « 1-20 sur 661 » ;
- la **première colonne figée** et un défilement horizontal net pour atteindre toutes les colonnes
  (CM, TD, TP, total, volume UE, ECTS, coefficient, enseignant…).

L'export Excel continue d'exporter l'intégralité des données (les filtres ne concernent que l'affichage).
Aucune modification des fichiers Excel.

## Documents officiels (H1) — nouveau en V1.38
La bibliothèque des documents officiels devient **catégorisée et consultable** :

- La colonne **« Type » devient la catégorie** du document, choisie dans une **liste éditable par le
  directeur** (Paramètres → `Categories_doc`). Catégories de départ : Stratégique · Médical ·
  Supports de cours · Réglementaire / officiel · OMS / international · Autre (le directeur en
  ajoute/retire librement).
- **Saisie activée** sur l'écran Documents officiels (catégorie en liste déroulante).
- **Consultation groupée par catégorie** : chaque document affiché avec titre, référence, date,
  responsable et **chemin / lien local**, avec un bouton « Copier » (l'ouverture directe d'un fichier
  depuis le navigateur étant bloquée pour raisons de sécurité, on copie le chemin puis on l'ouvre depuis
  l'explorateur). Une barre de « puces » permet de sauter à une catégorie.

Impact Excel : **ajout additif** de la seule liste `Categories_doc` dans `P0_Parametres`, par chirurgie
du zip — un seul fichier interne modifié, **16 dessins / 669 formules / valeurs en cache préservés**.
Nouveau md5 du classeur : `b542ace78d1d6b375c3365962839b9ad` (24 onglets). Le câblage « Type → liste »
se fait par surcharge applicative (aucune modification de l'onglet Dictionnaire).

## Plan d'action (G1) — enrichi en V1.39
Le plan d'action devient un véritable outil de suivi des écarts :

- Nouvelle colonne **« Type d'écart »** (liste éditable par l'EMSP, dans Paramètres → `Types_ecart` :
  Budgétaire · Temporel · Contenu de formation · Qualité · Autre) pour qualifier la nature de chaque écart.
- **« Statut »** devient une **liste à notion de planning** (Paramètres → `Statuts_action` :
  Non démarré · En cours · Atteint · En retard · Abandonné), éditable.
- **Saisie activée** sur l'écran Plan d'action : l'EMSP saisit chaque écart constaté, l'action corrective,
  le responsable, l'échéance, le type d'écart et le statut.

Impact Excel : **ajout additif** par chirurgie du zip — colonnes `Types_ecart` et `Statuts_action` dans
`P0_Parametres`, colonne `Type d'écart` dans `G1_Plan_action`. Deux fichiers internes modifiés ;
**16 dessins / 669 formules / valeurs en cache préservés**. Nouveau md5 du classeur :
`eb71af4e758df211814fbdf9289fe06c`. Câblages par surcharge applicative (Statut → liste) et par ajout de
champ (`Type d'écart`), sans modifier l'onglet Dictionnaire.

> À affiner ensuite : la colonne « Type d'écart » est ajoutée en fin de tableau (dernière colonne) ;
> son repositionnement près de « Écart constaté » et l'ajustement des valeurs des deux listes pourront se
> faire à la prochaine itération.

## Matériel et expression de besoin — nouveau en V1.40
- **Matériel (M1)** : l'**état** devient une **liste éditable** `Etats_materiel` (Actif · En panne ·
  Hors service · En maintenance · Réformé) ; ajout d'une colonne **« Localisation provisoire »**
  (matériel déplacé / en réparation).
- **Expression de besoin (`L3_Besoins`)** : nouvel onglet / écran (module Logistique) pour enregistrer les
  besoins — qu'ils viennent d'un matériel en panne **ou** d'autre chose (consommable, nouveau matériel…).
  Champs : ID (auto BES-n), date, type de besoin, équipement concerné (optionnel, liste des équipements M1),
  libellé, quantité, localisation, priorité, statut, coût estimé, demandeur, observations. Quatre listes
  éditables (`Etats_materiel`, `Types_besoin`, `Priorites_besoin`, `Statuts_besoin`) dans Paramètres.
- **Déclenchement depuis une panne** : sur l'écran Équipements, un panneau « Matériels indisponibles »
  liste les matériels *En panne / Hors service* avec un bouton **« Exprimer un besoin »** qui ouvre le
  formulaire pré-rempli (équipement + type). Lien manuel et léger, aucun automatisme caché.

Impact Excel : ajout additif par chirurgie du zip — 4 listes dans `P0_Parametres`, colonne
`Localisation provisoire` dans `M1_Equipements`, **nouvel onglet `L3_Besoins`** (sheet25 ; mirroir de S2).
6 fichiers internes touchés + 1 nouveau ; **16 dessins / 669 formules / valeurs en cache préservés** ;
**25 onglets**. Nouveau md5 du classeur : `574f357617477a51daf2eac561b7db5a`.

## Présentation & identité utilisateur — V1.41 (lot rapide, classeur inchangé)
- **Accueil réorganisé** : la **Scolarité** est mise en avant sur **toute la largeur** en haut ; **Administration**
  et **Direction** passent **en dessous**, sur deux colonnes. Le Paramétrage reste à part.
- **Identité de l'utilisateur connecté** (postes partagés) : chaque compte a une **couleur distincte** (palette
  `COULEURS_UTILISATEUR`, dérivée du login par défaut) affichée en **liseré en haut de l'écran** et en **pastille
  colorée** autour du nom — on voit immédiatement qui est connecté. Le choix définitif de la couleur par
  l'informatique se fera avec le lot « gouvernance des comptes ».

Classeur **inchangé** (md5 `574f357617477a51daf2eac561b7db5a`) : ce lot est purement interface.

## Base de code UNIQUE : production / formation — V1.42
Fini le build de démonstration forké : **un seul logiciel**. La différence prod/formation
tient à un fichier-drapeau local **`instance/formation.flag`** (hors dépôt, propre à chaque poste) :
présent → mode FORMATION (bandeau rouge, filigrane « FORMATION » à l'impression, plafond indicatif
de 50 lignes/onglet en **alerte non bloquante**, données fictives) ; absent → production normale.
Aucune divergence de code : toute amélioration profite aux deux.

Kit `formation/` (livré avec le logiciel) :
- `seed_formation.py` — (re)génère le jeu d'exemples sur une copie du classeur vide ;
- `seed/` — la baseline (classeur pré-rempli) ;
- `INSTALLER_FORMATION.bat` — transforme un dossier copié en poste de formation ;
- `REINITIALISER_FORMATION.bat` / `.sh` — **remet le jeu à neuf et efface toutes les saisies ET les
  utilisateurs créés en formation** ; refuse de s'exécuter si le drapeau est absent (jamais en prod) ;
- `LISEZMOI_FORMATION.txt` — mode d'emploi.

Isolation : utiliser un **dossier séparé** pour la formation. Ce qui est saisi en formation ne touche
jamais les vraies données. Correctif `Comptes_caisses` remonté en production (menu Compte/caisse + trésorerie).

## Gouvernance des comptes — nouveau en V1.43

Refonte de l'écran `/autorisations`, devenu la **console « Comptes & accès »** du responsable informatique. Séparation des responsabilités : l'**informatique gère l'identité** (comptes, mots de passe, validité), la **Direction gère les droits métier** (matrice par module dans `P1_Roles`).

- **Création de comptes, rubrique, couleur, mot de passe et validité** réservés au **responsable informatique** (= capacité `Admin droits (O/N)` existante de `P1_Roles` ; aucune nouvelle colonne, classeur inchangé). L'édition de la matrice de droits par module **disparaît de l'IHM** : la Direction l'ajuste directement dans `P1_Roles`. La matrice reste **affichée en lecture seule**.
- **Grande rubrique** d'appartenance (`Direction`, `Scolarité`, `Comptabilité`, `Enseignants / Départements`, `Logistique`, `Informatique` — liste `config.RUBRIQUES`, éditable).
- **Mot de passe aléatoire 8 caractères** (`secrets`, alphabet sans caractères ambigus `O/0/l/1/I`), généré à la création **et** à la réinitialisation, **affiché une seule fois** dans un encart copiable, à changer au 1er login (`doit_changer`).
- **Validité = année scolaire** (jusqu'au **31/07**). **Expiration NON bloquante** : la connexion reste ouverte, un bandeau « compte à renouveler » s'affiche. Bouton **« Renouveler (année scolaire) »** = repousse au 31/07 suivant **sans toucher au mot de passe**.
- **Couleur d'identité CHOISIE** par l'informatique (sélecteur de pastilles, palette `config.COULEURS_UTILISATEUR`) ; `metier.couleur_login()` lit d'abord la couleur stockée, sinon retombe sur la dérivation par login (rétrocompatible).
- **Self-service mot de passe supprimé** : le lien « Mot de passe » retiré de la barre supérieure ; la route `/mot-de-passe` n'est accessible que pour le **changement forcé au 1er login / après réinitialisation**. Sinon, le changement passe par l'informatique (réinitialisation).
- **Stockage** : tous les nouveaux attributs (rubrique, couleur, `valide_jusqu`) sont écrits dans `instance/comptes.json` — **hors dépôt et hors zip**, à côté de l'empreinte du mot de passe. **Aucune chirurgie du classeur, md5 inchangé** (`574f357617477a51daf2eac561b7db5a`). La création d'un compte écrit dans `P1_Roles` **uniquement** `login + role` (les colonnes de droits sont préservées en mise à jour).
- **auth** : `generer_mdp`, `definir_attributs`, `attributs`, `couleur`, `initialiser_validite`, `renouveler`, `est_expire`, `_fin_annee_scolaire`/`_prochain_31_07` ; `reinitialiser(login)` renvoie désormais `(ok, mdp_clair)` (aléatoire). **metier** : `couleur_login` sensible à la couleur choisie, `enregistrer_compte_it`, `rubriques`, `utilisateurs_admin` enrichi. **app** : routes `/autorisations/utilisateur` (création/MAJ IT), `/autorisations/reinitialiser`, `/autorisations/renouveler` (nouvelle), `/autorisations/supprimer` ; `mot_de_passe` verrouillée au changement forcé ; `compte_expire` au contexte. **config** : `RUBRIQUES`, `MDP_LONGUEUR`/`MDP_ALPHABET`, `ANNEE_SCOLAIRE_FIN_*`, VERSION 1.43. **Aucune modification du classeur.**
- Tests : `py_compile` (5 modules) ; flux complet client Flask (création → mdp affiché une fois → rubrique/couleur stockées → renouvellement 31/07/2026→31/07/2027 → réinitialisation → self-service bloqué 302 → ligne `P1_Roles` login+role) ; compte expiré (connexion 200 non bloquante + bandeau). md5 des classeurs livrés **inchangé**.
