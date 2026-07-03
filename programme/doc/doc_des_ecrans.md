# Documentation des écrans — Interface EMSP V1

> **V1.68** — Les listes compta de `P0_Parametres` (catégories recettes/dépenses, postes budgétaires) et les comptes `F2_Comptes` sont désormais alimentés : les déroulants de l'écran **Trésorerie** (`/tresorerie`) et de la saisie `F1_Mouvements` sont opérationnels. Données seulement, aucun changement d'écran.


## Conventions communes à toutes les pages
- **Logo Université des Comores** : en haut à gauche devant « EMSP » (barre latérale) et en pied de page. Vendoré (`static/img/logo_udc.jpg`), aucun CDN.
- **Barre supérieure (V1.2)** : rappel de la page courante à gauche ; à droite, **sélecteur de rôle** (liste des rôles de `P1_Roles`, sans mot de passe) qui pilote les droits lecture/écriture, et rappel de l'accès financier du rôle actif.
- **Messages & alertes (V1.2)** : messages de confirmation/erreur après une action (vert/rouge) ; **bandeau d'alerte de capacité** quand un onglet approche la limite configurée (`CAPACITE`).
- En-tête : icône + grand titre (charte #1F4E79), fil d'Ariane au-dessus.
- Bloc **AIDE** dépliable en haut de chaque page (fond clair jaune pâle).
- Barre latérale gauche : navigation en accordéon (sous-menus dépliants) suivant le GUIDE.
- Pied de page : projet, référence, dépôt GitHub, mention « 100 % hors-ligne ».

## Accueil (`/`)
- Bandeau de 5 indicateurs (effectif, actifs, enseignants, recettes, solde).
- 6 **gros encarts** sur fond clair, un par section du GUIDE ; chaque encart liste ses
  modules avec un compteur de lignes.

## Tableau de bord (`/tableau-de-bord`)
- **9 indicateurs (KPI)** alimentés par `/api/dashboard` : effectif total, actifs, diplômés,
  taux de présence, recettes, dépenses, solde, heures constatées, reste dû. Les KPI
  financiers et horaires sont **grisés** si un filtre filière/niveau est actif (non ventilables).
- **6 graphiques sélectionnables** : effectif par filière, répartition par statut,
  recettes/dépenses par catégorie, taux de présence par créneau, heures par enseignant,
  reste dû par filière. Chaque graphique : boutons de **type** (histogramme/camembert/radar),
  **puces** de valeurs en bas (« Tout » / « Aucun »).
- **Choisir les indicateurs** (#20, V1.99.15, **réservé Direction**) : bloc repliable en tête
  d'écran (3 colonnes : KPI · Graphiques · Budget) pour **cocher quels indicateurs afficher**.
  Sélection **globale établissement** persistée dans `instance/reglages.json` (clé `tdb_selection`)
  via `metier.tdb_selection()/…_set()/…_reset()`. Les indicateurs décochés sont **masqués** ;
  bouton **« Réinitialiser »** = tout afficher. Route POST `/tableau-de-bord/indicateurs`.
- **Indicateurs Budget** (brique C, issus de la synthèse budgétaire) : 5 KPI **bornés sur la
  session courante** (`_annee_acad_defaut()`), **non filtrables** filière/niveau — budget prévu
  total, réalisé total, taux de consommation (%), écart total (rouge si dépassement), nombre de
  postes en dépassement — et un graphe **Prévu vs Réalisé par poste** (`metier.kpis_budget()`).
- **Impression sélective** (`/tableau-de-bord/imprimer`) : ne sort que le **tableau des KPI
  cochés** (standard + budget), KMF formaté charte ; **aucun canvas Chart.js** dans la page
  d'impression (les graphes cochés restent imprimables depuis l'écran via `@media print`).
  Depuis **V1.99.40 (R4)**, l'impression boucle réellement sur les KPI cochés (le tableau n'est
  plus figé) ; si le KPI **Reste dû** est coché, un **tableau « Reste dû d'inscription par filière »**
  (Filière · Attendu · Payé · Reste dû · Total) est ajouté à l'édition. Le même tableau est affiché
  **à l'écran** sous les graphes (montants exacts, en complément du graphe « Reste dû par filière »).
- Interrupteur **Données de démonstration** : valeurs fictives tant que le classeur est vide.

## Pages module (`/module/<onglet>`)
- AIDE contextuelle + rappel du code de provenance + liste des champs (depuis le Dictionnaire).
- Tableau de données avec filtre visuel des en-têtes :
  - en-têtes colorés selon la provenance (noir/bleu★/rouge★),
  - colonnes calculées signalées par l'étiquette « calcul » (lecture seule).
- Si aucune donnée : message clair + aperçu de la structure des colonnes attendues.

### Édition — `P0_Parametres` (premier écran écrivant, V1.2)
- Réservé au rôle **Direction** (les autres rôles voient une note « lecture seule »).
- Une **carte par liste de référence** (Filières, Niveaux, Catégories de recettes/dépenses, etc.),
  avec la provenance (noir / bleu★ / rouge★) en en-tête.
- Valeurs existantes affichées en **puces** ; chaque puce porte une croix pour **retirer** la valeur.
- Champ + bouton **Ajouter** pour insérer une nouvelle valeur (refus des doublons, message de confirmation).
- Écriture immédiate dans le classeur via la couche d'accès (`data.ajouter_valeur_liste` /
  `supprimer_valeur_liste`) ; aucune colonne calcul concernée sur cet onglet.


## États de paiement des vacations (`/paiement`) — nouveau V1.99.3
Écran dédié (section **Enseignement → Heures**), réservé au rôle **Financier** (+ Accès financier). Transforme les heures du relevé en montants, puis en écriture comptable.
- **Constituer / recalculer un état** : on choisit l'**année académique**, le **semestre** (S1/S2) et on coche les **mois** du relevé des heures (`E2`) à inclure. Le moteur produit **1 ligne par enseignant** : heures prévues / effectuées (somme E2), **heures autorisées à payer** (plafond ≤ effectuées, par défaut = effectuées), **taux** (override `E1` sinon défaut global 5 750 KMF/h) et **Montant = autorisées × taux**. Les **moniteurs** (mode *Forfait mensuel* dans `E1`) sont repris en *mois × coût mensuel*. Recalculable tant que l'état est en **brouillon**.
- **Liste des états** : identifiant `PAIE-<année>-<semestre>`, nb de lignes, total KMF, statut (Brouillon / Arrêté / Passé en compta), impression.
- **Détail** : tableau par enseignant + **total** et **total en toutes lettres**. Selon le statut : bouton **« Arrêter l'état »** (le fige) puis **« Passer en compta »** (choix compte/caisse + mode de paiement).
- **Passage en compta** : crée **une dépense `F1` par enseignant** (libellé *Vacation \<semestre\> \<année\> — \<nom\>*), pose une **référence commune** `PAIE-…`, marque l'état **Passé en compta** — **non répétable** (garde-fou anti-double-passage). Audit dans `journal.csv`.
- **Impression** (`/paiement/<id>/imprimer`) : reprend la mise en forme de l'**état de paiement de l'école** (en-tête UDC/EMSP, colonnes, « Arrêté le présent état à la somme de … », signatures Gestionnaire / Administrateur / Directeur).
- **Onglet brut `E4_Etats_paiement`** : table de consultation/audit (réservée Financier) ; la saisie normale passe par l'écran dédié.

## Comptes & acces : droits par utilisateur (roles-modeles) — nouveau V1.74
- Les droits sont stockes **par login** dans `P1_Roles` ; la colonne « Role » est une **etiquette**. Deux comptes d'un meme role peuvent donc avoir des droits differents (ex. **gestionnaire** complet vs **assistant comptable** en lecture seule).
- Le formulaire « Creer ou modifier un compte » propose : un **Role (modele)** qui **pre-coche** les droits (modeles dans `config.ROLES_MODELES`, editables), des **cases par groupe** en **Lecture** et en **Ecriture** (Eleves & scolarite, Presences, Stages, Notes & bulletins, Enseignants & heures, Finances, Logistique, plus « Tous (Direction) »), et deux bascules **Acces financier** (deverrouille l'ecriture F1/F2/F3 et les encaissements) et **Admin droits** (gestion des comptes).
- Apres avoir applique un modele, l'admin **decoche pour donner moins** ou **coche pour donner plus** a CET utilisateur. Enregistrement par login (`metier.enregistrer_utilisateur`), garde-fou : on ne peut pas retirer le droit du **dernier administrateur** ; le superutilisateur reste protege.

## Fiche enseignant `/enseignant` — nouveau V1.73
- **Symétrique de la fiche étudiant.** Recherche par **matricule ou nom** (datalist hors-ligne) ; accès aussi par `?matricule=`.
- **Identité** depuis `E1_Enseignants` (Matricule ens., Genre, Nom, Prénom, Statut, Matières enseignées, Qualifications, Département, Chef de dépt validant), **en lecture seule**. La création / modification se fait dans le **module `E1_Enseignants`** ; le bouton **« Modifier dans le module »** ouvre ce module pré-positionné sur la ligne (`?modifier=<matricule>`, branché sur le sélecteur d'édition existant).
- **Photo** : `donnees/photos/<matricule>.jpg` (hors classeur), téléversement JPEG/PNG ≤ 1 Mo, placeholder #1F4E79 — seule écriture autorisée depuis la fiche.
- **Infos liées (lecture seule)** : **Heures** (`E2_Releve_heures` filtré par matricule, avec totaux programmé / constaté / à payer) ; **Séances planifiées** (`A3_Sessions`, lien par le champ *Enseignant* = Nom+Prénom ; le matricule sera pris en charge dès qu'il sera proposé comme valeur) ; **Séances réalisées / exceptions** (`E3_Seances_faites`, lien par *Assuré par*).
- **Fiche imprimable** (`/enseignant/<matricule>/imprimer`) : page autonome **paysage** (navigateur, `window.print()`), en-tête Université des Comores / EMSP + date d'édition, identité + photo + heures + séances.
- **Statut (V1.99.36, R2)** : champ **« Statut »** (en-tête `Statut (*)`) en **liste éditable** à 4 valeurs par défaut — **Permanent · Contractuel · Vacataire · Bénévole** — alimentée par la colonne `Statuts_enseignant` de `P0_Parametres`. L'administration peut **ajouter d'autres statuts** depuis l'écran **Paramètres** sans intervention sur le code. Saisie et filtre dans le module `E1_Enseignants`.
- Pseudo-page `ENS_Fiche` (groupe **Enseignants** du menu + `SPECIAL_ROUTES`), toujours visible ; l'accès est gardé par le droit de lecture sur `E1_Enseignants`.

## Accueil — épuré V1.73
- Le **bandeau d'indicateurs (KPI)** en tête de l'accueil est **retiré** : l'accueil est un pur « point de départ » (les indicateurs restent au Tableau de bord). Les **tuiles** sont agrandies (badge icône #1F4E79, ombre, survol), gardées par les droits comme avant.

## Fiche étudiant imprimable — nouveau V1.73
- Bouton **« Imprimer la fiche »** sur `/etudiant` → `/etudiant/<matricule>/imprimer` : page autonome paysage (même moteur que la fiche enseignant), identité + photo + droits d'inscription + stages.

## Navigation : menu regroupé, masquage par droits & accueil en tuiles — nouveau V1.72
- **Menu de gauche en 6 groupes** (Pilotage, Scolarité, Enseignants, Ressources, Finances, Administration), pilotés par `GUIDE_STRUCTURE`. Chaque groupe est repliable ; le groupe contenant la page courante est ouvert ; l'élément actif est surligné.
- **Masquage par droit de lecture** : un onglet gouverné par `P1_Roles` que le rôle courant ne peut pas lire (`metier.peut_lire`) est retiré du menu ; un groupe ou une section sans aucun module visible est entièrement masqué. Un **superadmin voit tout** ; les pseudo-pages (Fiche étudiant, Calendrier, Requêtes, Impressions, Tableau de bord…) ne sont **jamais** masquées. Le périmètre masqué (`MODULES_CACHES`) est calculé dans le `context_processor` à partir de `MODULES_ONGLETS` + `ONGLETS_DIRECTION` + `ONGLETS_FINANCIERS`.
- **Modules hors TDR retirés du menu** (routes conservées, accès direct possible) : Examens, Diplômes, Qualifications, Indemnités, Non-conformités, Audits, Conflits.
- **Accueil (`/`)** : la zone centrale est une grille de **grandes tuiles** « point de départ » (Élèves, Présences, Notes & bulletins, Trésorerie, Tableau de bord, Impressions), chacune masquée si le rôle n'a pas le droit, au-dessus du bandeau d'indicateurs conservé. Un clic sur une tuile ouvre la même page que l'entrée de menu correspondante.

## Bandeau de filtres multicritère & impression de la sélection — nouveau V1.71
- **Bandeau commun** (`_bandeau_filtres.html`, inclus en tête des pages module et du tableau de bord) : quatre contrôles — **Filière**, **Niveau**, **Année académique** (listes alimentées par `metier.valeurs_filtres()`) et **Période** (Du / Au en **texte JJ/MM/AAAA**, pas de sélecteur de date natif). Boutons **Appliquer**, **Réinitialiser**, **Imprimer cette sélection**.
- **Masquage selon le support de l'onglet** : un contrôle ne s'affiche que si `bandeau.supporte.<critère>` est vrai (calculé côté présentation — `_bandeau_dashboard` pour le tableau de bord, retour de `/module/<onglet>` pour les modules). Le bandeau est entièrement masqué sur `P0_Parametres` et les onglets de référence (aucun critère applicable).
- **Option B (grisage)** : l'**année** et la **période** filtrent les finances et les heures ; **seuls la filière et le niveau** déclenchent le **grisage** des cartes financières du tableau de bord (Recettes / Dépenses / Solde / Heures), avec une note — ces montants ne se ventilent pas par filière/niveau. Sans filtre actif, le comportement est identique aux versions antérieures.
- **Impression de la sélection** (`impression_selection.html`, **navigateur** : `window.print()` → Enregistrer en PDF, **pas de WeasyPrint**) : le bouton « Imprimer cette sélection » soumet le formulaire vers `/module/<onglet>/imprimer` ou `/tableau-de-bord/imprimer` (`formaction` + `formtarget=_blank`) en **emportant la sélection courante**. Page **autonome paysage** (`@page size: A4 landscape`, `.doc-page.paysage`), en-tête Université des Comores / EMSP, date d'édition et rappel de la sélection. Deux modes : **module** (table filtrée) et **dashboard** (table des KPI, KMF formaté sans décimale, séparateur espace).

## Fiche étudiant — recherche par matricule (`/etudiant`) — nouveau V1.61
Écran d'entrée du dossier d'un étudiant, en tête du menu Étudiants. On **saisit le matricule**
(ou le nom) dans un champ unique avec autocomplétion hors-ligne (« matricule — Nom Prénom (filière
niveau) ») : pas de longue liste déroulante. Le bouton « Afficher la fiche » ouvre la fiche ; choisir
une entrée dans la liste la soumet directement (le matricule est extrait du libellé). La **fiche**
présente l'identité complète (A1) et la **photo** de l'étudiant, des **liens** vers son relevé/bulletin
(pré-rempli), ses présences et ses stages, et la **liste de ses stages** (depuis `S1_Stages`).

Photos : convention `donnees/photos/<matricule>.jpg`. Tant qu'aucune photo n'est déposée, un portrait
générique (placeholder, charte `#1F4E79`) s'affiche.

**Dépôt de photo depuis la fiche (V1.63).** Sous la photo, un bouton **« Choisir une photo… »**
(ou **« Changer la photo »** si une photo existe déjà) ouvre le sélecteur de fichier ; le formulaire
se soumet automatiquement dès qu'un fichier est choisi (un seul clic). Un bouton **« Retirer la photo »**
(rouge, avec confirmation) apparaît quand une photo est présente. Formats acceptés : **JPEG et PNG**
(détectés par leur signature binaire, sans ré-encodage), **1 Mo maximum** ; les autres formats et les
fichiers trop lourds sont refusés avec un message. L'image est enregistrée sous le nom canonique
`<matricule>.jpg` (un PNG est alors servi en `image/png`). Les contrôles n'apparaissent que pour un
utilisateur ayant le **droit d'écriture sur `A1_Etudiants`** et sont **indisponibles sur un poste
secondaire** (lecture seule) ; chaque dépôt ou retrait est **journalisé**. Aucune écriture dans le
classeur : seul le fichier image est touché. La même recherche par matricule sera réutilisée pour
sélectionner l'élève dans les stages.

### Saisie de lignes — `A1_Etudiants` et `A3_Sessions` (V1.3)
- Panneau **Ajouter une ligne** au-dessus du tableau, visible uniquement si le role courant a le droit d'ecriture (sinon note lecture seule).
- Formulaire **genere a partir du Dictionnaire** : un champ par colonne (hors colonnes calcul), type adapte (texte, nombre, date JJ/MM/AAAA), **listes deroulantes** pour les champs de type Liste (valeurs issues de `P0_Parametres` ou de listes en dur comme les jours). Champs obligatoires marques `*` et valides cote serveur.
- Enregistrement via la couche d'ecriture ; une seance ajoutee apparait aussitot dans le calendrier et le planning des salles.
- **Modifier une fiche existante (V1.51)** : au-dessus du formulaire, un selecteur liste les lignes deja saisies. Le bouton *Charger pour modification* recopie la ligne choisie dans le formulaire (qui bascule en mode **Modifier** : titre et bouton adaptes, bouton *Annuler la modification*). L'enregistrement met a jour **la meme ligne** (POST `/module/<onglet>/modifier`, champ cache `_index` = position parmi les lignes non vides), sans creer de doublon. Garde-fous identiques a l'ajout : onglets en saisie active uniquement, droit d'ecriture verifie, **colonnes calcul jamais ecrasees** (formule preservee), `Saisi par` remis a l'identifiant courant. Primitive `AccesDonnees.modifier_ligne(onglet, index, valeurs)`. Pas de suppression physique : la sortie d'un etudiant se traduit par un changement de **Statut** (Diplome / Abandonne / Radie).
- **Perimetre de l'edition en place (V1.52)** : l'**ajout** de lignes reste ouvert sur tous les onglets en saisie active ; la **correction en place** d'une ligne deja enregistree est en revanche restreinte a `ONGLETS_EDITION_LIGNE` (sous-ensemble de `ONGLETS_SAISIE_ACTIVE`). Principe : donnees de reference et champs de workflow se corrigent naturellement sur place ; le **journal financier `F1_Mouvements` reste en ajout seul** (append-only) — une erreur s'y corrige par une ecriture rectificative, jamais en reecrivant la ligne, pour la tracabilite d'audit. Concretement, l'encadre *Modifier une fiche existante* ne s'affiche pas sur `F1_Mouvements`, et la route `/module/F1_Mouvements/modifier` renvoie 404. Le perimetre se durcit en ajoutant un onglet a `ONGLETS_SANS_EDITION_LIGNE` (candidats : `F2_Comptes`, `N3_Signalements`). Toute modification reste journalisee (`instance/journal.csv`).

## Pages référence
- `/reference/Guide`, `/reference/Legende` : rendu lisible du contenu des onglets.
- `/reference/Dictionnaire` : champs regroupés par onglet (type, obligatoire, provenance, description).

## Calendrier (`/calendrier`) — nouveau V1.1
Projection de l'emploi du temps **hebdomadaire récurrent** (`A3_Sessions`, colonne *Jour*).
Barre d'outils : bascule **Mois / Semaine / Jour**, navigation *précédent / Aujourd'hui / suivant*,
libellé de période, lien **Données de démonstration**.
- **Mois** : table 7 colonnes (Lun–Dim) ; chaque jour du mois affiche le nombre de séances du
  jour-type ; clic sur une case → vue *Jour*. Jour courant encadré.
- **Semaine** : grille façon Outlook, axe horaire vertical (7h–18h), colonnes Lundi–Samedi,
  blocs de séances positionnés à l'horaire réel (`Heure début`/`Heure fin`), couleur par type
  (Cours = bleu, TD = bleu clair, TP = vert).
- **Jour** : liste des séances de la journée (horaire, matière, enseignant, groupe, type, salle
  cliquable) + encart **Salles occupées** + encart **Présences du jour** par créneau (`A2_Presences`).

## Salles — planning du jour (`/salles`) — nouveau V1.1
Sélecteur de jour (Lun–Sam). Grille façon Outlook : **une colonne par salle**, blocs des séances
qui l'occupent ce jour-là. En-tête de colonne et blocs cliquables → **fiche salle**. État vide clair
si aucune salle n'est saisie (proposition d'activer la démonstration).

## Fiche salle (`/salles/<id>`) — nouveau V1.1, édition + matériel V1.99.21
- **Résumé de l'occupation** groupé par jour : horaire, matière, *par* (enseignant), *pour* (groupe), type.
- **Matériel de la salle** : liste **en lecture seule** lue de `M1_Equipements` filtrée sur la salle
  (désignation, catégorie, quantité, état). Bandeau de renvoi + bouton **« Gérer le matériel »** vers
  Logistique › Matériel (`/module/M1_Equipements`) — **seul endroit** qui écrit dans `M1` (source unique).
  Depuis **V1.99.41 (R5)**, un bouton **« Imprimer l'inventaire »** sort l'édition paysage du matériel
  de cette salle (ID, Désignation, Catégorie, État, Bailleur, Quantité, Montant KMF + total ; route
  `/salles/<id>/inventaire/imprimer`). Les éditions globales restent dans Impressions › Inventaire
  (par salle / par source de financement / par état).
- **Caractéristiques** : pour un rôle ayant le **droit d'écriture sur `L1_Salles`**, **formulaire
  d'édition** (Nom, Type [liste `config.TYPES_SALLE`], Capacité, Localisation ; **ID en lecture seule**) ;
  sinon table en lecture seule. Enregistrement via `POST /salles/<id>/modifier`, qui réutilise la chaîne
  générique `metier.champs_saisie` → `valide_saisie` → `data.modifier_ligne("L1_Salles")` (pas de logique
  parallèle) ; l'ID est réinjecté pour préserver la clé ; action journalisée (`Modif salle`).
- **Que voulez-vous faire ?** (V1.99.32, écrivant) :
  - **Réserver la salle** (rôle ayant le droit d'écriture sur `L2_Reservations`) : formulaire
    `POST /salles/<id>/reserver` → `metier.creer_reservation` → `data.ajouter_ligne("L2_Reservations")`
    (ID `RES-n` auto, action journalisée). Champs : réservé par, date, créneau, **Type**
    (liste `config.TYPES_RESERVATION`, dont « Cours / séance »), **Séance liée** (planning `A3_Sessions`,
    facultatif), enseignant (matricule via *datalist* `E1`, ou nom libre si externe), filière / niveau /
    matière, motif, statut.
  - **Préremplissage** : si une **séance A3** est choisie, filière / niveau / matière / enseignant sont
    repris du planning ; sinon si un **matricule** est saisi, le nom est résolu depuis `E1_Enseignants`
    (le matricule reste la clé pour le chaînage prof → heures → compta).
  - **Réservations enregistrées** : liste des réservations hors cours de la salle (date, créneau, type,
    objet, par, statut) ; l'occupation par les **cours** reste dans le résumé de gauche (planning A3).

> Structure `L2_Reservations` (V1.99.32) : 10 colonnes d'origine + 6 ajoutées par **chirurgie ZIP** du
> maître (jamais `openpyxl.save`) — `Seance liee (ID session A3)`, `Filiere`, `Niveau`, `Matiere`,
> `Matricule ens.`, `Enseignant`. Vue d'occupation unifiée cours (A3) + réservations (L2) inchangée (Q2).

## Couplage avec le classeur
L'interface lit `data/EMSP_V1.xlsx` à chaque requête. Toute modification du classeur
est reflétée au rafraîchissement de la page.

### Écriture (V1.2)
- Seule la **couche d'accès** (`data.py`) écrit : `ajouter_ligne`, `ajouter_valeur_liste`,
  `supprimer_valeur_liste`. Le classeur est ouvert en préservant les formules (`data_only=False`).
- **Colonnes calculées jamais saisies** : la couche y **recopie le motif de formule** (translaté)
  pour chaque nouvelle ligne — il n'y a donc plus de limite de lignes (validé jusqu'au-delà de
  l'ancien plafond 300). Les onglets en lecture seule (`READONLY_TABS`) sont refusés.
- **Droits** : `metier.peut_ecrire(role, onglet)` applique la matrice `P1_Roles` (mapping
  groupes → onglets dans `config.MODULES_ONGLETS`, onglets Direction, exigence d'accès financier).
- **Capacité** : toutes les plages d'agrégat et de colonnes calcul du classeur sont harmonisées sur
  `CAPACITE` (50 000) ; un bandeau d'alerte prévient à l'approche du seuil.
- Note : openpyxl n'évalue pas les formules à l'enregistrement ; le **tableau de bord est calculé
  en Python** (indépendant du cache), et Excel recalcule les formules à l'ouverture du fichier.
  Le rafraîchissement de l'affichage des colonnes calcul dans l'IHM sera traité avec les écrans
  financiers/relevé d'heures (prochaine étape).

### Performance de lecture (V1.3)
Le classeur est **mis en cache** et n'est rechargé que s'il a changé sur disque (date de modification), avec invalidation explicite après chaque écriture. Cela corrige la lenteur de la V1.2 (le fichier était re-parsé à chaque accès, jusqu'à ~90 fois par page).

## Saisie des présences par séance (`/presences`) — nouveau V1.4
Écran d'écriture dédié à `A2_Presences` (la saisie ligne par ligne générique n'y est volontairement
pas activée : volumétrie 554 élèves × créneaux × séances × dates).
- **Sélecteur** : Séance (liste `A3_Sessions`) + Date + Créneau (10h/12h/15h/17h). **(V1.99.16)** La date propose
  le **jour courant par défaut** et un **calendrier cliquable** (champ date natif ; choisir une date recharge l'écran).
  Les quatre créneaux correspondent aux moments où les feuilles signées reviennent. Le créneau par défaut est
  déduit de l'heure de début de la séance ; il reste modifiable.
- **Effectif** : tiré de `A1_Etudiants` par **Filière + Niveau + Section** de la séance (section ignorée si
  la séance n'en précise pas). Tableau avec case **Présent** par étudiant (+ boutons *Tout présent / Tout absent*),
  et colonne *État actuel* rappelant ce qui est déjà enregistré.
- **Enregistrement** : écrit **une ligne par étudiant** via `metier.enregistrer_presences_lot` →
  `data.ecrire_lignes_lot` en **UPSERT** (clé Date + Matricule + Session + Créneau) : pas de doublon en
  ré-saisie, correction en place. « Saisi par » = login du rôle courant.
- **Droits** : `peut_ecrire(role, 'A2_Presences')` ; route protégée (403 sinon).
- **Feuille de présence vierge** (V1.99.8) : bouton ouvrant la grille vide à imprimer (`impr_presence`, 60 lignes par défaut, nouvel onglet), accessible directement depuis l'écran de saisie. Remplace l'ancienne carte du hub Impressions (retirée).

## Présences — saisie en liste, séance libre (`/presences/libre`) — nouveau V1.64
Écran de saisie de masse **sans emploi du temps préalable** (option B). Complète l'écran séance-first (`/presences`), utilisable dès que `A3_Sessions` est peuplé (option A).
- **Choisir la classe** : Filière → Niveau → Section (sélecteurs en cascade hors-ligne ; Section affichée seulement si la classe en a) puis **Afficher la feuille**.
- **Définir la séance** : Date (JJ/MM/AAAA, jour courant pré-rempli), Heure début / Heure fin, Matière (liste du barème via `matieres_maquette`), Enseignant (liste `E1`), Salle (libre, optionnel).
- **Feuille de présence** : roster de `A1` (Filière + Niveau, Section si renseignée), trié par nom ; cases **Présent** (non coché = absent) ; compteur présents/effectif ; boutons **Tout cocher / décocher**.
- **Enregistrement** : `metier.enregistrer_presences_libre` écrit une ligne `A2_Presences` par étudiant (upsert sur Date + Matricule + Session/Matière + Créneau). Créneau = plage `HH:MM-HH:MM`. Clé « Session / Matière » = clé composée lisible ; si **« enregistrer comme récurrente »** est coché, une ligne `A3_Sessions` est créée (ID `Sxxx`, jour déduit de la date) et son ID sert de clé.
- **Droits** : `peut_ecrire(role, 'A2_Presences')` (403 sinon) ; création `A3` conditionnée au droit `A3_Sessions` (case désactivée sinon) ; indisponible sur poste secondaire ; journalisé.
- **Feuille de présence vierge** (V1.99.8) : même bouton que sur `/presences`, à côté d'« Afficher la feuille » (`impr_presence`, 60 lignes par défaut, nouvel onglet).

## Saisie façon bulletin (`/bulletin`) — nouveau V1.65
Écran de saisie des notes **par étudiant**, présenté comme son bulletin (complément des écrans de notes en liste).
- **Sélection** : recherche par **matricule** (autocomplétion hors-ligne) ; Année (défaut `2025-2026`) ; Semestre (semestres du barème pour la filière/niveau) ; Session 1 / 2 puis **Afficher le bulletin**.
- **Grille** : barème `filière+niveau+semestre` (UE → matières). Par matière : **CC /20** (dérivé des contrôles `N4` en lecture seule si présents, N4 prime ; sinon saisissable), **Examen /20** (saisi), **Moyenne** = ¼ CC + ¾ examen calculée en direct. Par UE : Coef + ECTS, moyenne UE (moyenne arithmétique des matières), validée si ≥ 10. Pied : moyenne semestre (UE pondérées par `Coef UE`), mention, proposition Admis/Ajourné (**indicative**, délibération manuelle), ECTS acquis. Bandeau « barème provisoire » tant que les coef ne sont pas confirmés (**masqué depuis la V1.66** : coefficients validés ; `scripts/confirmer_coefficients.py`).
- **Session 2** : la grille pré-remplit les notes de session 2 déjà saisies et affiche la **session 1** en référence (la session 2 remplace la 1 dans le calcul du relevé).
- **Enregistrement** : `metier.enregistrer_bulletin` → upsert `N2_Notes` (clé `Matricule + Année + Session + Semestre + N° UE + Matière`) **pour les seules matières renseignées** (CC manuel ou Examen non vide). Le CC dérivé de `N4` n'est pas réécrit dans `N2`. Notes contrôlées dans `[0..20]`.
- **Droits** : `peut_ecrire(role, 'N2_Notes')` (403 sinon) ; indisponible sur poste secondaire ; journalisé. Lien vers le **relevé imprimable** existant.

## Équipements / inventaire (`M1_Equipements`) — enrichi V1.67
Écran générique de l'onglet `M1_Equipements` (inventaire du patrimoine de l'école, hors GMAO).
- **Colonnes** : ID équipement, Désignation, Catégorie, Salle / localisation, Date d'acquisition, Source de financement / Bailleur, Montant (KMF), Référence / N° pièce, État, N° inventaire / série, Saisi par, Localisation provisoire, **Quantité** (ajoutée V1.67).
- **Chargement initial** : `scripts/import_equipements.py` (depuis `equipements_data.json`) — 280 articles depuis les inventaires EMSP (par bureau et par salle), une ligne par article avec sa quantité ; n° d'inventaire = matriculation `UDC/EMSP/…`.
- **Lien Patrimoine ↔ Compta** : `Montant`, `Bailleur`, `Référence / N° pièce` et `Catégorie` sont laissés vides à l'import, à renseigner depuis la comptabilité — un équipement acquis correspond à une dépense `F1` affectée à un poste budgétaire (605 / 605A / 21…) et à un financement (AFD / dons / État), reliée par la `Référence / N° pièce`. Sert au suivi des affectations de dépenses et des dérives budgétaires.
- **Maître figé** : ajout de la colonne via chirurgie ZIP (`scripts/ajout_quantite_M1.py`, dessins préservés), jamais openpyxl.save sur le maître.
- **Provenance** : A2 reste **hors-TDR** (`(**)`) — construction délibérée issue du CR du 11/06, documentée.
- **En-tête de séance (exception) — V1.55** : bloc dépliable *« remplaçant / cours annulé / durée différente »*, replié par défaut (à remplir **seulement** en cas d'écart). Champs : État (Assurée / Cours annulé), Assuré par (liste E1, défaut = enseignant programmé), Matière réelle (datalist depuis la maquette R1), Vol. constaté (h, défaut = durée programmée), Motif. À l'enregistrement, écrit dans `E3_Seances_faites` (UPSERT clé Date + Séance + Créneau) **uniquement** si écart réel ; revenir au cas normal **neutralise** la ligne. Sert au calcul des heures constatées (voir écran dédié). Avertit en cas d'homonyme sur l'enseignant programmé.

### Listes liées à un autre onglet (V1.4)
`config.LISTES_ONGLET` mappe un libellé lisible (colonne « Liste / source » du Dictionnaire) vers
`(onglet, champ)`. `metier.options_liste()` renvoie alors les valeurs distinctes non vides de cette colonne
(ex. Matricule ← A1, ID session ← A3). Réutilisable pour les écrans suivants (jointures fiables).

## Saisie Documents étudiants (`A4_Documents_etud`) — nouveau V1.5
Saisie via le **formulaire générique** (pas d'écran dédié) — volumétrie modeste (quelques documents par étudiant).
- **Champs** : Matricule (liste ← A1) · Type de document (liste P0 *Types_document*) · Année concernée
  (liste P0 *Annees_acad*) · Date génération (date, défaut = aujourd'hui) · Statut (liste P0 *Statuts_document*,
  défaut *En attente conseil*) · Date libération (date, manuelle) · Remis le (date, manuelle).
- **Cycle de validation** (manuel en V1) : En attente conseil → En attente délai (contestation 1 semaine)
  → Imprimable → Remis. **Génération PDF / remplissage auto / automatisation du cycle = V2.**
- **Valeurs par défaut** : `config.SAISIE_DEFAUTS["A4_Documents_etud"]` (`@today` pour la date de génération,
  statut initial). Injectées par `metier.champs_saisie` et rendues par `module.html`.
- **Nouvelles listes P0** : *Types_document (**)*, *Statuts_document (*)* — éditables par la Direction sur
  l'écran Paramètres (apparaissent automatiquement, P0 étant lu dynamiquement).
- **Droits** : Académique + Direction ; comptabilité refusée (403).

## Saisie Stages (`S1_Stages`) — nouveau V1.6
Formulaire générique. Champs : Matricule (liste ← A1) · Année acad. (liste P0 `Annees_acad`) ·
N° séance 1-6 (nombre libre) · Lieu de stage (liste P0 `Lieux_stage`, **pré-amorcée**, éditable
Direction) · Date début / Date fin (dates, 1 mois) · Fiche retour O/N (défaut N) · Note /20 (nombre) ·
Observation/plainte (texte libre). Périmètre V1 = référentiel + affectation + suivi fiche retour ;
grille d'appréciation multicritères (doc D) et plaintes détaillées = V2. Droits : Académique+Stages,
Direction ; comptabilité 403.
**R8 (V1.99.45)** : colonne **« Heures d'absence (**) »** ajoutée à `S1_Stages` (chirurgie ZIP, maître +
runtime). C'est l'absence **partielle de stage** (heures manquées sur la période, à valider au retour),
distincte des présences de cours (par créneau, O/N). Saisie via le formulaire générique S1 ; affichée sur
le suivi (`/stages`) et son impression (colonne « Heures abs. », >0 en rouge) ; la fiche d'appréciation
de stage conserve son champ manuscrit « Durée des absences ».

## Affectation des stages (`/stages/affectation`) — modèle manuel (révisé V1.99.42)
Écran de répartition d'une classe sur les lieux de stage. On choisit **Filière · Niveau · Année ·
Séance (1-6) · Session** (Normale / Rattrapage), puis « Afficher ». S'affichent : une **synthèse**
(effectif, affectés, non affectés, capacité), le **tableau des lieux du niveau** (lieu, commune,
**période de disponibilité**, quota, occupé, restant — restant 0 en rouge), un **formulaire
d'affectation par groupe** (choix du lieu, dates début/fin JJ/MM/AAAA, case « autoriser le dépassement
de quota », puis cases à cocher sur le roster) et les **affectations en place** groupées par lieu.
Validation → `POST /stages/affectation/groupe` (`metier.affecter_groupe_stages`) : 1 ligne par élève
dans `S1_Stages`, upsert par Matricule + Année + Séance + Session, contrôle de quota (refus si
dépassement sauf case cochée). En **Rattrapage**, seuls les élèves ayant un stage Normal sur la séance
sont listés ; la ligne Rattrapage **coexiste** avec la Normale (notes/dates/fiches retour conservées).
Impression de l'affectation : `/stages/affectation/imprimer` (paysage). Lecture : Académique+Stages,
Direction. **Note d'historique** : le template livré en 1.99.41 visait une *affectation automatique*
(proposition) dont le backend n'avait pas été écrit (écran non fonctionnel) ; la 1.99.42 rétablit le
modèle **manuel** (validé Bernard, 30/06). L'affectation automatique proposée reste une **piste
possible, sans engagement** (cf. ETAT.md).

## Requêtes embarquées dans les écrans (R9 — V1.99.42)
En complément du hub `/requetes` (explorateur, pivot, vues métier, export Excel), quatre écrans
opérationnels offrent un accès **contextuel en un clic** (lecture seule) aux vues/explorateurs
pertinents, le contexte courant étant transmis quand la vue l'accepte :
`/salles` → vue **Occupation des salles** + explorateur `L1_Salles` ;
`/heures-constatees` → vue **Écart programme/constaté** (mois courant) + explorateur `E2_Releve_heures` ;
`/salles/<id>` → vues **Équipements de la salle** (salle courante) et **Équipements par bailleur** ;
`/presences` → vue **Absences & observations** (origine cours) + explorateur `A2_Presences`.
Aucun moteur nouveau : ces boutons pointent vers les routes `requetes_vue` / `requetes_explorer`
existantes.

## Saisie Enseignants (`E1_Enseignants`) — nouveau V1.7
Formulaire générique (pas d'écran dédié ; volumétrie modeste). 9 champs.
Obligatoires : Matricule ens. · Nom · Prénom.
Listes : Genre (liste P0 `Genres`, M/F) · Statut (liste **inline** `Titulaire/Vacataire` dans
`config.LISTES_INLINE` — choix (a) acté : ensemble fermé stable, géré en code, pas de colonne P0).
Texte libre : Matières enseignées · Qualifications · Département · Chef dept validant.
Matricule provisoire : si pas de matricule officiel, le champ Matricule est **pré-rempli** avec le
prochain `NC-<n>` libre (token `@next_nc` → `metier._prochain_nc()`, scan de E1, max+1, casse ignorée,
vrais matricules ignorés). On le remplace par le vrai matricule quand il arrive (édition de ligne en
place = capacité générique non encore développée → pour l'instant via le fichier ; report aussi sur
E2 si une ligne y référence le `NC-<n>`).
Aucune colonne calcul sur E1 ; aucune modification du classeur en V1.7.
Droits : groupe `Enseignants` (MODULES_ONGLETS). En l'état de P1_Roles, seule la Direction (`Tous`)
écrit E1 ; pour ouvrir à la scolarité/chef de département, ajouter `Enseignants` à leurs modules
d'écriture dans P1_Roles (éditable Direction).
Étape suivante (décidée) : lien Séances ↔ formateurs — A3 `Enseignant` en liste ← E1, une fois E1 peuplé.

## Lien Séances ↔ formateurs (`A3_Sessions` / Enseignant) — nouveau V1.8
Le champ `Enseignant` de A3 passe de texte libre à **liste déroulante alimentée par E1**.
Mécanisme : `config.LISTES_ONGLET_COMPOSITE = {"Enseignants (E1)": ("E1_Enseignants",
["Nom","Prenom"]," ")}`, résolu par `metier.options_liste()` (libellé `Nom Prenom`, distinct, trié).
Dictionnaire (classeur) : A3/Enseignant Type `Texte` → `Liste`, source « Enseignants (E1) ».
Valeur stockée = libellé lisible (le calendrier et les salles l'affichent tel quel, aucune
résolution matricule→nom) ; le matricule reste la clé de E2. Ordre `Nom Prenom` paramétrable
en une ligne. Dépendance : Enseignant obligatoire → saisir E1 avant les séances (liste vide
sinon). Aucune autre modification du classeur ; recalculé, 0 erreur (669 formules).

## Saisie Relevé des heures (`E2_Releve_heures`) — nouveau V1.9
Formulaire générique. Premier écran à **colonne calcul**. 4 champs éditables.
Obligatoires : Mois / Année (texte libre, format conseillé MM/AAAA) · Matricule ens. · Vol. horaire constaté.
Optionnel : Vol. horaire prog. Colonne calcul (non saisissable) : Total heures à payer.

Matricule ens. — choix (b2) : liste déroulante **valeur ≠ libellé**. Affiché « Matricule — Nom Prénom »,
**stocké = matricule seul** (clé paie + agrégat « heures par enseignant »). Mécanisme :
`config.LISTES_ONGLET_VALLABEL = {"Enseignants matricule (E1)": ("E1_Enseignants","Matricule ens.",["Nom","Prenom"])}`,
résolu par `metier.options_liste()` en `{value,label}`. Toutes les options de liste sont désormais
normalisées en `{value,label}` (rendu `module.html` : `<option value=o.value>o.label</option>`).

Total heures à payer — choix (a) : **affichage calculé en Python**. La formule (`=heures constatées`,
heures seulement, sans taux) reste dans le classeur pour Excel ; `metier.table()` remplit la cellule
à l'affichage via le registre `metier.CALC_AFFICHAGE` (uniquement si la cellule lue est vide, sinon on
garde la valeur recalculée par Excel). Réutilisable pour F2_Comptes et IMPORT_zone.

Classeur : seule modif = Dictionnaire E2/Matricule (Texte→Liste). Recalculé, 0 erreur (669 formules).
Droits : groupe Enseignants ; en l'état de P1_Roles, seule la Direction écrit E2.

## Heures constatées du mois (`/heures-constatees`) — nouveau V1.55
Écran de **rapprochement et de report** : les heures effectives des enseignants sont **calculées** à partir des appels de présence, pas saisies.
- **Calcul** : pour le mois choisi (MM/AAAA), chaque triplet (Date, Séance, Créneau) ayant au moins un appel dans `A2_Presences` compte **une fois**. Enseignant et durée viennent de `A3_Sessions` (durée = Heure fin − Heure début, à défaut Vol. horaire prog.). Les **exceptions** `E3_Seances_faites` surchargent : « Cours annulé » exclut la séance, un remplaçant réattribue les heures (et la matière réelle), un volume constaté impose la durée.
- **Tableau** : par enseignant — heures calculées, valeur E2 actuelle, statut (à reporter / identique / différent), nombre de séances + détail dépliable (date, créneau, séance, matière, durée, marque « remplaçant »). Panneau d'**anomalies** (séance sans enseignant identifiable, homonyme, ID séance introuvable) listées et **non comptabilisées**.
- **Report dans E2** : bouton *« Reporter dans E2 »* (cases à cocher par ligne) → `metier.reporter_heures_mois` → `data.ecrire_lignes_lot` en UPSERT (clé Mois + Matricule), écrit la colonne **Vol. horaire constaté**. **Garde-fou** : si E2 contient déjà une valeur **différente** du calcul (correction manuelle : feuille disparue, heures contestées), elle **n'est pas écrasée** sans cocher **« Report forcé »**. La chaîne paie (relevé d'heures) lit E2, inchangée.
- **Droits** : consultation = lecture Enseignants ; report = écriture Enseignants (`/heures-constatees/reporter`, 403 sinon). La saisie des exceptions, elle, relève du droit Présences (écran d'appel).


Point ouvert (Direction) : matrice des autorisations — vue lisible « qui peut quoi par module » +
configurabilité des découpages de modules. À traiter à part ; modèle de droits inchangé en V1.9.

## Saisie Salles (`L1_Salles`) — nouveau V1.10
Formulaire générique. 6 champs, aucune colonne calcul. Obligatoires : ID salle · Nom / libellé.
Type (liste P0 `Types_salle` = Cours/TD/TP/**Amphitheatre**) · Capacité (nombre) · Équipements
(texte, séparés par `;`) · Bâtiment / localisation. ID salle auto-suggéré `SAL-<n>` (token
`@next_sal`, via `metier._prochain_code()` généralisé), modifiable ; noms de salles explicites.
Les salles sont créées par l'école (livrable vierge). Remontée dans le planning des salles + fiche
salle + sélectionnables par les séances. Classeur : seule modif = `Amphitheatre` ajouté à
`Types_salle` (P0) ; recalculé, 0 erreur (669 formules). Droits : groupe Académique → scolarité +
Direction. Étape suivante : A3 `Salle` ← liste L1.

## Lien Séances ↔ salles (`A3_Sessions` / Salle) — nouveau V1.11
Le champ `Salle` de A3 passe de texte libre à **liste déroulante ← L1** (noms de salles).
`config.LISTES_ONGLET["Salles (L1)"] = ("L1_Salles","Nom / libelle")` (déjà géré par options_liste).
Dictionnaire : A3/Salle Type Texte → Liste, source « Salles (L1) ». **Facultatif** (Salle non
obligatoire) : pas de dépendance bloquante. Valeur stockée = nom (le rattachement `_seance_dans_salle`
matche par nom OU id ; le nom reste lisible au calendrier/planning). Seule modif classeur = ligne
Dictionnaire ; recalculé, 0 erreur (669 formules).

## Page Matrice des autorisations (`/autorisations`) — nouveau V1.12, matrice éditable V1.99.23
Page spéciale (menu Administration, clé `MAT_Autorisations`, libellé « Comptes & droits d'accès »,
`SPECIAL_ROUTES`). Tableau comptes × modules depuis `P1_Roles` + `config.MODULES_ONGLETS` : colonnes
Académique, Présences, Stages, Notes, Enseignants, Financier, Logistique, Direction (paramétrage),
+ Accès financier + Admin. **V1.99.23 — la matrice est ÉDITABLE en ligne pour les administrateurs** :
une case **L** (lecture) et **É** (écriture) par module, plus les bascules Accès financier et Admin ;
bouton « Enregistrer la matrice » → route `app.autorisations_matrice` qui boucle sur le **même writer**
que l'éditeur de compte (`metier.enregistrer_utilisateur`), donc **mêmes garde-fous** : superutilisateur
protégé (jamais modifiable), dernier administrateur non retirable, verrou Accès financier. Pour les
non-administrateurs : tableau en **lecture seule**. La colonne Direction (paramétrage) = bascule
« Tous (Direction) ». **L'ancienne grille brute `P1_Roles` est retirée du menu** (`/module/P1_Roles`
renvoie 404) : la matrice est désormais l'unique endroit d'édition des droits par module. La gestion des
comptes (création, mot de passe, validité, rubrique, couleur) reste sur le même écran, en dessous.

## Administration des droits (`/autorisations`, édition) — nouveau V1.13
La page Matrice devient éditable pour les administrateurs. Colonne `Admin droits (O/N)` dans P1_Roles
(directeur=O pré-amorcé). Superutilisateur `config.SUPERUSER_LOGINS=["superadmin"]` garanti par le code
(accès total + admin même si P1_Roles cassé ; non supprimable/rétrogradable) = filet anti-blocage ;
ligne `superadmin` livrée dans P1_Roles. Écran admin : tableau utilisateurs + formulaire upsert
(login, rôle, cases lecture/écriture par module + Tous, financier, admin) + suppression (confirmée).
Garde-fous : superuser intouchable ; dernier administrateur non retirable ; POST réservés admin (403).
metier : roles() enrichi, est_admin, enregistrer_utilisateur, supprimer_utilisateur, utilisateurs_admin.
data : supprimer_ligne_par_cle (onglets sans colonne calcul). app : routes /autorisations/utilisateur
et /autorisations/supprimer + _exige_admin. Classeur : col Admin droits + superadmin + doc ; 0 erreur.
À décider : découpage MODULES_ONGLETS éditable depuis l'IHM (onglet classeur).

## Saisie Trésorerie (`F1_Mouvements`) — nouveau V1.14
Formulaire générique. 16 colonnes, aucune colonne calcul. Accès Comptabilité + Direction (Accès
financier = O). 15 champs saisissables (Saisi par exclu, rempli serveur = login courant).
Obligatoires : Date opération · Sens · Catégorie · Compte / caisse · Libellé.
Catégorie (A-a) = liste combinée `Cat_Recettes` + `Cat_Depenses` (motif "X OU Y" résolu par
options_liste). Montants (B-b) = validation conditionnelle `_valide_f1_mouvements` (registre
`_VALIDATIONS_SPECIFIQUES`) : Recette⇒Montant Recette requis (Dépense vide) et inversement.
Listes inline Sens (Recette/Depense), Statut (Previsionnel/Realise). Défaut Date opération=@today.
Bailleur ← Bailleurs (P0) = traçabilité AFD. Compte/caisse ← Comptes_caisses (P0) ; F2 tirera de la
même liste. Dépendance : remplir Cat_Recettes/Cat_Depenses/Comptes_caisses (et Postes_budgetaires)
dans P0 avant saisie (non pré-amorcés). config : ONGLETS_SAISIE_ACTIVE, CHAMPS_AUTO_LOGIN, LISTES_INLINE,
SAISIE_DEFAUTS. app : injection Saisi par. Aucune modif classeur.

## Saisie Comptes & soldes (`F2_Comptes`) — nouveau V1.15
Formulaire générique. 4 colonnes dont Solde courant en colonne calcul. Accès Comptabilité + Direction.
3 champs saisissables (Solde courant exclu). Obligatoires : Nom du compte · Solde initial (KMF).
Nom du compte ← P0 `Comptes_caisses` (même liste que F1.Compte/caisse → SUMIF du solde cohérent ;
Dictionnaire F2/Nom du compte Texte→Liste). Type ← inline Banque/Caisse/Autre.
Solde courant = affichage Python LIVE (`_solde_courant_f2` : initial + Σ recettes − Σ dépenses du
compte d'après F1) ; l'affichage des colonnes calcul est désormais TOUJOURS recalculé (cache Excel
périmé après saisie F1). Formule conservée pour Excel. KMF sans décimales inutiles.
Note : une ligne par compte ; remplir Comptes_caisses (P0) avant. Recalculé 0 erreur (669 formules).
Le module financier est complet (F1 + F2).

## Import CSV national (`/import`, IMPORT_zone) — nouveau V1.16
Écran dédié (menu Paramétrages), réservé Direction (SPECIAL_ROUTES IMPORT_zone->import_csv).
Coller le CSV : séparateur auto (tab/;/,), en-tête ignorée (1re cellule sans chiffre). 7 colonnes
A-G remplissent la zone de staging. Statut vs base calculé Python (NOUVEAU si matricule absent de A1,
sinon EXISTANT) + compteurs. Import MANUEL : copie des NOUVEAU vers A1 à la main ; la zone ne modifie
jamais A1. Retour en arrière : instantané disque (import_undo.json) avant chaque import/vidage, bouton
Annuler (1 niveau). data : remplacer_donnees (vide+réécrit, formules recopiées). metier : parser_csv,
import_zone_brut, importer_csv, vider_zone_import, annuler_import, import_resume, CALC_AFFICHAGE IMPORT.
app : /import (+importer/vider/annuler) + garde Direction. Aucune modif classeur.
Correctif : ws.cell(r,c,value=None) n'efface pas sous openpyxl -> ws.cell(r,c).value=None (remplacer_donnees
ET supprimer_ligne_par_cle).

## Modèles de documents (`/modeles`, ED_Modeles) — nouveau V1.18
Écran **Paramétrages → Modèles de documents**, réservé à la Direction (`peut_ecrire` sur
`D1_Modeles_docs`, onglet ajouté à `ONGLETS_DIRECTION`). Édite les **parties fixes** des 6 documents :
en-tête, titre, corps (avec **jetons** `{…}`), mentions/pied, libellé signataire, nombre de copies.
Enregistrement **upsert par `Cle doc`** via `data.ecrire_lignes_lot` dans l'onglet additif
`D1_Modeles_docs` (texte, aucune formule). Les jetons disponibles sont rappelés sous chaque corps.
metier : `modeles_docs`, `modele_doc`, `enregistrer_modele`, `rendre_modele`.

## Impressions & éditions (`/impressions`, ED_Impressions) — nouveau V1.18
Hub (section *Finances & pilotage*). Une carte par document ; chaque formulaire ouvre l'**aperçu
imprimable dans un nouvel onglet** (`target="_blank"`).
- **Liste d'étudiants** `/impressions/liste?filiere=&niveau=&section=&annee=` (A1, filtres facultatifs).
- **Feuille de présence vierge** `/impressions/presence-vierge` (V1.99.37, R3) : feuille de **séance ponctuelle**. **Sélection obligatoire d'une classe** (Filière + Niveau ; Section facultative) — sinon retour à l'écran avec message. En-tête : Classe · Date · **Horaire (début – fin libres)** · Matière · Enseignant. Corps **pré-rempli** avec le roster de la classe (N° / Matricule / Noms et Prénoms) + colonne **Émargement** vide ; **repli** en grille numérotée vierge (paramètre « Lignes si classe vide ») si aucun étudiant. La feuille hebdomadaire (créneaux fixes) reste distincte.
- **Relevé individuel** `/impressions/releve-individuel?mois=&matricule=` (sélecteur enseignant **dépendant** du mois via `/api/releve-individuels`).
- **Récapitulatif mensuel** `/impressions/releve-recap?mois=` (tableau + total général).
- **Reçu de paiement** `/impressions/recu?i=<index recette F1>` — **garde financier** (403 sinon) ; N° REC-AAAA-NNNN pré-rempli (`metier._prochain_recu`).
- **Attestation de passage** `/impressions/attestation?matricule=`.
- **Export tableau de bord** `/impressions/export-tdb` → `.xlsx` (openpyxl, 6 feuilles), `send_file`.
Paramètres manquants → message flash + redirection vers le hub. Boutons d'impression **contextuels**
ajoutés sur les pages module A1 (liste/attestation) et F1 (reçu, si financier).

### Éditions logistiques et financières — nouveau V1.75
Trois éditions ajoutées au hub, toutes en rendu générique `kind="table"` (`metier.doc_adhoc` + `imprimer.html`), **lecture seule**, aucun écrit dans le classeur.
- **Inventaire des équipements** `/impressions/inventaire?axe=salle|bailleur|etat` (M1) : regroupement au choix par salle, par source de financement (bailleur) ou par état, avec **sous-totaux** quantité + montant par groupe et **total général**. Paysage. Source : `metier.inventaire_equipements(axe)`.
- **Expression de besoin** `/impressions/bon-besoin?statut=&priorite=&salle=` (L3) : état des besoins exprimés, filtrable, total des coûts estimés. Paysage. Source : `metier.bon_de_besoin(...)`.
- **Recettes / dépenses par source de financement** `/impressions/etat-bailleur?annee=` (F1) — **garde financier** (403 sinon) : regroupement par bailleur (AFD, OMS, EMSP…), total recettes / dépenses / solde ; filtre année civile facultatif (sur `Date operation`). Source : `metier.etat_par_bailleur(annee)`. Couvre le **reporting bailleur AFD** (#26 du reste-à-faire).
Les listes de filtres sont alimentées par `metier.salles_equip_dispo / bailleurs_equip_dispo / etats_equip_dispo / besoin_statuts_dispo / besoin_priorites_dispo / annees_civiles_f1`. Cartes inventaire/besoin dans la section Logistique du hub (la matrice des droits en hérite via le groupe Logistique) ; carte bailleur dans la section financière (`{% if peut_financier %}`).

## Page d'impression (`imprimer.html`) — nouveau V1.18
Page **autonome** (n'étend pas `base.html`), chargée `static/css/print.css`. Barre d'outils non
imprimée (boutons *Imprimer / PDF* → `window.print()`, *Retour*). Zone `contenteditable` : retouche
ponctuelle avant impression (non enregistrée). En-tête = logo + lignes officielles ; gère
`kind` = `prose` (corps à jetons), `liste`, `presence`, `recap`. Le bloc document est répété selon
le **nombre de copies** (`page-break-after` en impression). Jetons rendus via `|e` puis `\n`→`<br>`
(échappement avant mise en forme).

## Couplage classeur (V1.18)
Ajout **additif** de l'onglet `D1_Modeles_docs` (titre + en-têtes + 6 modèles seedés depuis
`config.MODELES_DOCS`, styles repris à l'identique, **aucune formule**). Les 19 onglets et 669 formules
existants sont inchangés (recalcul LibreOffice : `success`, 0 erreur, 669 formules, 20 onglets).
Dernière modification additive du classeur avant la bêta.

## Registres Réservations & Équipements (`L2_Reservations`, `M1_Equipements`) — nouveau V1.19
Deux **onglets de données** intégrés via le pattern générique (aucune route dédiée) : présents dans
`GUIDE_STRUCTURE` (section *Enseignements & salles*), `ONGLETS_SAISIE_ACTIVE`, le Dictionnaire (types,
obligatoires, listes), et une nouvelle catégorie de droits **Logistique** (`MODULES_ONGLETS`). Servis
par `/module/<onglet>` + `/module/<onglet>/ajouter` comme les autres.

`L2_Reservations` : réservations hors cours (datées, ponctuelles), distinctes de l'emploi du temps
récurrent A3. Champs : ID réservation (RES-n auto), Salle (liste L1), Date, Heure début/fin, Type
(liste inline), Réservé par, Motif/objet, Statut (liste inline), Saisi par (auto).
`M1_Equipements` : inventaire de pilotage (sans maintenance). Champs : ID équipement (EQ-n auto),
Désignation, Catégorie (P0 Categories_equipement), Salle/localisation (liste L1), Date d'acquisition,
Source de financement/Bailleur (P0 Bailleurs, partagée F1), Montant (KMF), Référence/N pièce, État
(liste inline), N° inventaire/série, Saisi par (auto).

Codes auto : `metier._prochain_res` / `_prochain_eq` (via `_prochain_code`, corrigé pour résoudre le
libellé **brut** des colonnes marquées). Listes inline ajoutées : types de réservation, statuts de
réservation, états d'équipement. Aide contextuelle ajoutée dans `module.html` pour les deux onglets.

Couplage classeur : ajout **additif** (2 onglets + colonne P0 `Categories_equipement` + 21 lignes au
Dictionnaire). 669 formules inchangées, 22 onglets (recalcul LibreOffice `success`, 0 erreur). Nouveau
md5 `0614d315d830492c8407121ebe3b694b` (2 copies identiques). Dernier lot additif avant la bêta.
La couche requêtes (V1.20) sera en lecture seule.

## Saisie en grille — Trésorerie (`/tresorerie`) — nouveau V1.20
Écran de saisie type tableur pour le registre de trésorerie, écrit dans F1 (aucune route d'écriture
sur une nouvelle structure ; le classeur est inchangé). Garde `peut_ecrire('F1_Mouvements')` (accès
financier). GET `/tresorerie?compte=&lignes=` : sélecteur de compte (solde d'ouverture = solde courant
du compte via `metier.solde_courant_compte`), grille de N lignes éditables (colonnes = sous-ensemble de
`champs_saisie('F1_Mouvements')` via `metier.treso_grille_colonnes`, avec leurs listes déroulantes).
Solde recalculé côté client (JS) : ouverture + Σ(recette − dépense). POST `/tresorerie/enregistrer` :
colonnes parallèles `c0[]..cN[]` reconstituées en lignes, sens déduit du montant rempli, compte +
Saisi par injectés, validation par `metier.enregistrer_treso_lot` (réutilise `valide_saisie`). **Atomique** :
si une ligne est invalide, rien n'est écrit, l'écran est re-rendu avec la saisie conservée et les
erreurs ligne par ligne ; sinon écriture par lot via `data.ajouter_lignes` (une seule ouverture).
Lignes vides ignorées. Bouton « Saisie en grille » ajouté sur la page module F1.

## Édition « Situation de compte » (`/impressions/situation-compte`) — nouveau V1.21
Registre mensuel imprimable d'un compte (kind `situation` dans `imprimer.html`). Garde financier.
`metier.situation_compte(compte, mois)` (MM/AAAA, lecture F1/F2) : report à nouveau = solde initial
(F2) + mouvements antérieurs ; lignes de la période triées par date avec solde courant ; clôture
« SOLDE AU dernier jour ». Convention : Débit = Recette, Crédit = Dépense, Solde = Débit − Crédit.
Modèle `SITUATION_COMPTE` (config, repli si absent de D1) ; deux signataires séparés par `|`. Carte
dédiée dans le hub Impressions (sélecteurs compte + période via `metier.mois_treso_dispo`). Aucune
modification du classeur.

## Requêtes & analyses (`/requetes`, REQ_Hub) — nouveau V1.22
Couche d'interrogation **en lecture seule** (ne modifie jamais le classeur). Hub listant l'explorateur
générique et les vues métier. `metier.explorer(onglet, filtres, colonnes, tri)` : filtres cumulatifs
(`_OPERATEURS` = contient/egal/debut/sup/inf/nonvide/vide), tri numérique-aware, projection de colonnes.
`metier._xlsx_simple` génère l'export (réutilisé partout). Vues prédéfinies dans le registre
`metier.VUES` (`vue_equip_loc` Q1, `vue_salle_occupation` Q2 = union A3∪L2, `vue_equip_bailleur` Q4 +
total, `vue_ens_ecart` Q5 sur plage de mois). Routes : `/requetes/explorer` et `/requetes/vue/<id>`,
chacune avec `?export=xlsx` (send_file). Templates : `requetes.html`, `explorer.html`, `vue.html`.
Entrée menu REQ_Hub (Finances & pilotage). Aucune modification du classeur.

**Marquage FORMATION des exports (V1.50).** En MODE_FORMATION uniquement, tous les exports `.xlsx`
de l'application (tableau de bord, onglet, vue, pivot, relevé/bulletin, état des signalements)
portent une ligne d'en-tête rouge « FORMATION — données d'entraînement, sans valeur officielle »
en tête de feuille (`metier.bandeau_xlsx`) et un suffixe `_FORMATION` dans le nom de fichier
(`metier.nom_export`). En production : sans effet. À l'écran, le bandeau rouge de formation est
fixé en haut de **toutes** les pages (CSS `position:fixed`), en cohérence avec le filigrane PDF.

## Requêtes — Q3 absences + Pivot (`/requetes/pivot`) — nouveau V1.23
Vue `absences` (registre `VUES`) : `metier.vue_absences` unifie absences cours (A2, Présent != O) et
observations de stage (S1, champ Observation/plainte non vide) ; filtres matricule + origine. Nuances
documentées (pas de commentaire en A2 ; absence stage non modélisée → observation S1).
`metier.pivot(onglet, lig, col, mesure, mes_col)` : tableau croisé 1-D ou 2-D, mesures count/somme/
moyenne, totaux pondérés corrects (somme/effectif). Route `/requetes/pivot` (+ `?export=xlsx`),
template `pivot.html`, carte ajoutée au hub. Aucune modification du classeur.

## Authentification + journal d'audit — nouveau V1.24
Module `auth.py` (séparé) : empreintes `pbkdf2:sha256` via werkzeug, stockées dans `instance/comptes.json`
(local, gitignoré, hors zip). `ensure_superadmin()` bootstrappe le superadmin (mdp initial `admin`,
changement forcé). Fonctions : `verifier`, `definir_mdp`, `changer_mdp`, `reinitialiser`, `supprimer`,
`doit_changer`. Journal append-only `instance/journal.csv` : `journal(login, action, cible, detail)` +
`lire_journal(limite, f_login, f_action)` (jamais de secret).
app.py : `@before_request` exige la connexion (sauf `/login`, statiques) et force `/mot-de-passe` si
`doit_changer`. `_role_courant()` lit `session["user"]` et résout les droits via `P1_Roles` (pas de repli
permissif ; superuser garanti par le code). Routes `/login`, `/logout`, `/mot-de-passe`,
`/autorisations/reinitialiser`, `/journal`. La route `/role` (sélecteur) est supprimée.
La page `/autorisations` (admin) gère le mot de passe initial à la création, la réinitialisation, et
affiche l'état du compte ; lien vers le journal. Templates : `login.html` (autonome), `mot_de_passe.html`,
`journal.html` ; bandeau `base.html` affiche l'utilisateur connecté + Déconnexion + Mot de passe.
Le classeur reste inchangé : aucun secret n'y est écrit.

## R1_Maquettes — Référentiel des formations (maquettes) [V1.25, lecture seule]
Reprend les maquettes officielles des 5 filières : pour chaque UE/module et chaque matière, le volume horaire (CM/TD/TP/total), le crédit (ECTS) et le coefficient, par niveau et semestre (661 matières). Page de **consultation** (route `/module/R1_Maquettes`) : tableau filtrable, export Excel. Socle des matières des séances (A3), du volume horaire programmé (suivi des heures) et de la structure UE des relevés de notes. Colonnes : Filière, Niveau, Semestre, N° UE, Intitulé UE / Module, Matière / Contenu, Enseignant, CM, TD, TP, Total heures, Vol. horaire UE, Crédit (ECTS), Coef.

## Planification — volumes par classe (`/planification/volumes`) [R11 Brique 1, V1.99.46]
Vue de **planification** (groupe « Référentiel », menu `PLN_Volumes`) qui restitue, pour une classe
(filière / niveau / semestre), les **heures dues** par UE et par matière, lues depuis `R1_Maquettes` :
chaque UE avec ses contenus (CM/TD/TP/Total), un total par UE et un **total classe**. C'est la référence
des « heures dues » qui alimentera le **compteur** de l'éditeur de grille (Brique 2 : heures placées dans
A3_Sessions vs heures dues). Lecture seule ; pour corriger/compléter un volume, on modifie la ligne dans
« Référentiel des formations (maquettes) » (CRUD générique R1 = override de la décision 1c). Métier :
`volumes_classe`, `volumes_options`. Garde : lecture A3_Sessions.

## Planification — grille hebdomadaire (`/planification/grille`) [R11 Briques 2 & 3, V1.99.48]
**Éditeur de l'emploi du temps hebdomadaire récurrent** d'une classe (gabarit, V1a), stocké dans
`A3_Sessions` — **distinct du calendrier** (vues datées façon Outlook). Filtre filière/niveau (+ section,
semestre, année optionnels) → grille **créneaux × jours (Lundi→Samedi)** : chaque case porte une carte
matière + salle + enseignant (ou « Prof N ») + volume horaire. Un formulaire ajoute une séance (matière
proposée depuis la maquette ; salle depuis L1 ; enseignant en liste E1 avec saisie libre pour les n° de
prof ; jour ; heures HH:MM ; vol. horaire programmé) ; suppression en ligne par séance.
**Compteur d'heures** par matière : placé (Σ Vol. horaire prog. des séances A3) vs dû (R1 via
`volumes_classe`) → reste à placer (négatif = dépassement, « — » = matière hors maquette) ; totaux
classe. **Conflits** salle/enseignant sur un même créneau+jour signalés. Métier : `grille_classe`,
`creer_seance_grille`, `supprimer_seance_grille`. Garde : lecture pour la vue, écriture A3_Sessions pour
ajout/suppression.

**Impression (R11 Brique 3, V1.99.48)** — bouton « Imprimer la grille » (visible dès qu'une séance est
placée) ouvrant un **PDF A4 paysage** par classe (route `/planification/grille/imprimer`, nouvel onglet,
fpdf2) : en-tête charté (logo UdC + identité EMSP), tableau **créneaux × jours (Lundi→Samedi)**, chaque
case listant matière + n° de séance + salle + enseignant + volume ; pied de page reprenant le **compteur**
(placé / dû / reste par matière, dépassement en rouge, total classe) et la **liste des conflits**. Lecture
seule (réutilise `grille_classe`). Métier : `grille_pdf_bytes`, `grille_pdf_nom`. Garde : lecture
A3_Sessions.

## Séances (`A3_Sessions`) — champ Matière en suggestions — nouveau V1.26
À la saisie d'une séance, le champ **Matière** propose les matières de la maquette (`R1_Maquettes`),
filtrées selon la **Filière**, le **Niveau** et le **Semestre** déjà choisis sur la ligne. La liste
se resserre au fur et à mesure que ces trois champs sont renseignés ; elle reste **indicative**
(on peut saisir une matière hors maquette).

Quand la matière choisie figure dans la maquette, le champ **Vol. horaire prog.** se **pré-remplit**
automatiquement (somme des heures programmées) — uniquement s'il est encore vide, et la valeur
peut toujours être corrigée à la main.

## Relevé d'heures (`E2_Releve_heures`) — colonne Écart — nouveau V1.27
Le tableau de consultation ajoute une colonne **Ecart (prog. - constate)** : la différence entre le
volume horaire programmé et le volume constaté, saisis tous deux à la main. Le signe `+` indique des
heures programmées non encore couvertes par le constaté ; `−` indique un dépassement. La colonne est
en lecture seule (marquée « calcul ») et n'apparaît pas dans le formulaire de saisie. Elle reste vide
tant que l'une des deux valeurs n'est pas renseignée.

## Lieux de stage (`S2_Lieux_stage`) — référentiel & quotas — nouveau V1.28
Écran de saisie du référentiel des lieux d'accueil de stage. Pour chaque lieu : structure, service,
commune, niveau concerné (laisser vide pour « tous niveaux »), quota (nombre maximum de stagiaires par
séance) et période de disponibilité. Ce référentiel se renseigne au déploiement avec les lieux réels.

Conséquence sur les stages : à la saisie d'un stage (`S1_Stages`), le champ « Lieu de stage » propose
désormais les unités de ce référentiel, sous la forme « Lieu — Service ». Le contrôle des places
restantes par séance et le tableau de bord d'occupation arrivent au lot suivant.

## Stages (`S1_Stages`) — aide au quota & occupation — nouveau V1.29
La page Stages affiche un panneau « Occupation des lieux de stage » : on choisit l'année académique
et la séance, et le tableau montre pour chaque lieu son quota, le nombre de places occupées et les
places restantes (les lieux complets sont surlignés). Des compteurs résument le nombre de lieux,
d'étudiants affectés, de places occupées et le taux d'occupation pour la sélection.

À la saisie d'un stage, dès qu'un lieu, une année et une séance sont indiqués, un repère affiche les
places restantes pour ce lieu (« complet » apparaît en rouge si le quota est atteint). Ce repère est
indicatif : il n'empêche pas d'enregistrer, la décision restant manuelle.

## Notes — barème (`N1_Bareme_UE`) et saisie (`N2_Notes`) — nouveau V1.30
Ces deux écrans appartiennent au fichier séparé des notes (accès restreint, module « Notes »).

Barème des UE (`N1_Bareme_UE`) : c'est ICI que l'on définit, par filière / niveau / semestre (cursus
1 à 6), les unités d'enseignement, leurs matières, leur coefficient et leurs crédits ECTS. Ce barème
est la référence du calcul des moyennes : il se renseigne avant toute saisie de notes. **Paramétrable
par la scolarité et la direction** (droit d'écriture *Notes*).

**Contrôle de cohérence (V1.99.38, R1)** : un panneau **non bloquant** s'affiche en tête de l'écran
d'édition et signale en clair les écarts du barème — crédits/semestre ≠ 30, crédits/niveau ≠ 60, UE
sans coef, coef ≤ 0 ou > 5, et coef non confirmé. La saisie et les calculs restent possibles ; les
anomalies disparaissent à mesure qu'on corrige les UE concernées. Bandeau vert récapitulatif quand
tout est cohérent.

**Seuil de passage conditionnel paramétrable (V1.99.39)** : sous ce panneau, un champ permet à la
scolarité / direction de fixer l'**écart de crédits ECTS toléré** (au-delà : « Ajourné »). Réglage
local (`instance/reglages.json`), défaut 5 ; pris en compte immédiatement dans les décisions de
passage des bulletins.

Depuis V1.35, une colonne **`Coef confirmé` (Oui/Non)** distingue les barèmes fiables des barèmes
provisoires, et le barème est **pré-rempli** : **L2 Soins infirmiers (S3/S4)** est confirmé (Oui,
coefficients réels du relevé officiel) ; **Soins infirmiers hors L2, Soins obstétricaux, Maintenance
biomédicale, Imagerie médicale** sont fournis comme squelette UE/matières (ECTS repris), mais avec
**coefficient à 1 par défaut** et `Coef confirmé = Non`, car les maquettes ne portent pas de
coefficient exploitable. La scolarité corrige les coefficients d'après le document de référence
officiel puis passe `Coef confirmé` à Oui. Aides-soignants n'est pas intégré (modèle incompatible).

Mise à jour V1.57 : le barème a été **rechargé depuis le tableau arbitré par l'EMSP**
(`scripts/import_bareme.py`, données figées dans `scripts/bareme_data.json`). Il couvre les **4
filières** (Soins infirmiers, Soins obstétricaux, Imagerie médicale, Maintenance biomédicale ;
Aides-soignants toujours absent), soit **642 lignes matières**. Le coefficient repris est le « Coef UE
corrigé » s'il est renseigné, sinon le « Coef (maquette) » ; **tout est en `Coef confirmé = Non`
(provisoire)** en attendant les corrections officielles de la scolarité — le relevé affiche donc le
bandeau « Barème provisoire ». Les rares doublons de numéro d'UE dans un même semestre ont été
**désambiguïsés à la source par un suffixe « b »** (par exemple UE18 et UE18b) : ce sont deux UE
distinctes. Ce rechargement **remplace** le pré-remplissage `seed_bareme.py` ; la numérotation des UE
suit désormais les maquettes.

Saisie des notes (`N2_Notes`) : pour chaque étudiant (matricule), par année, session (1 = juin, 2 =
rattrapage de septembre), semestre, UE et matière, on saisit le contrôle continu et l'examen. Pour une
matière à note unique (par exemple un stage), ne renseigner que la colonne Examen. Le calcul des
moyennes, de la mention et de la proposition de décision, ainsi que l'édition du relevé, arrivent au
lot suivant.

À partir de la V1.56, la colonne **Contrôle continu (CC) de `N2_Notes` est normalement calculée**
depuis l'écran « Contrôles continus » (`N4_Controles`, ci-dessous) : on ne saisit donc en pratique
que la colonne **Examen** dans `N2_Notes`. La colonne CC reste néanmoins saisissable et sert de
**repli manuel** quand aucun contrôle détaillé n'a été enregistré pour la matière.

## Contrôles continus (`N4_Controles`) — nouveau V1.56
C'est ici qu'on saisit le **détail des contrôles** d'un étudiant, **un contrôle par ligne** : par
année, session, semestre, UE et matière, on indique le **N° de contrôle** et la **date** (les deux
identifient le contrôle), la **note /20** et un **coefficient** (1 par défaut). La note de contrôle
continu de la matière en est **dérivée automatiquement** : c'est la **moyenne pondérée** des contrôles
de cette matière (en théorie un seul contrôle, donc CC = sa note ; si un deuxième contrôle est saisi
sur la même matière, la moyenne se fait toute seule). Cette CC dérivée alimente le relevé et le
bulletin sans aucune autre saisie. Si aucune ligne de contrôle n'existe pour une matière, le système
retombe sur la valeur CC saisie à la main dans `N2_Notes` ; si les deux existent, le détail (N4) prime.

**Mise à jour V1.99.50 — coefficient par matière, règle de session 2, Aides-soignants.**
- **Nouvelle colonne `Coef matiere`** dans `N1_Bareme_UE` (après `Matiere`, défaut **1**) : la
  **moyenne d'UE** devient la **moyenne des matières pondérée par ce coefficient**. Tous les coefs à 1
  (défaut de la migration), elle reste la moyenne **arithmétique**, qui est le modèle du **relevé
  officiel** (vérifié au centième sur le relevé L2 SI fourni : UE11 = 11,78 ; semestre 3 = 9,89).
  La scolarité ne renseigne un coef différent de 1 que si l'école applique des coefficients
  différenciés par matière (écran Barème des UE).
- **`Coef UE`** : pour Soins infirmiers et Soins obstétricaux, la migration applique la règle du
  **programme de formation révisé** (`Coef = Crédit/2`, dérivée des ECTS). **`Coef confirmé = Non`
  partout** : le barème N1 suit la **maquette révisée** (numérotation UE différente du relevé
  2024-2025), aucun barème n'est donc couvert ligne à ligne par un document officiel — la mention
  « Barème provisoire » s'affiche à l'écran et à l'impression tant que la scolarité n'a pas confirmé
  filière par filière.
- **Session 2 (rattrapage)** : alignement sur le **relevé officiel** et le décret 05-106 art. 10
  (« la note de la 1ère session est annulée ») — la moyenne d'une matière repassée repose sur les
  **seules notes de la session 2** (CC de rattrapage s'il existe, sinon la note d'examen seule).
  Le CC de session 1 n'est **plus conservé**. Vérifié au centième sur le relevé fourni (moyennes
  session 2 : UE13 = 11,88, UE14 = 10,13, UE15 = 10,50, semestre = 11,87).
- **Aides-soignants** : barème créé (11 modules du programme révisé, une ligne par module, semestre 1,
  coef 1, `Coef confirmé = Non`).
- **Impressions > Relevé de notes (bulletin)** : nouveau sélecteur **Session** — *Première session*
  (page sans colonnes de rattrapage, notes de session 1 seules) ou *Deuxième session* (colonnes
  Exam. sess. 2 / Moy. sess. 2), conformément aux deux pages du relevé officiel fourni ; le libellé
  de session s'imprime en tête de chaque bloc semestre. Jusqu'à 4 éditions possibles (2 semestres ×
  2 sessions).
- Migration : `scripts/migr_bareme_v1_99_50.py` (idempotente, en place sur `EMSP_Notes.xlsx`).

**Report des dernières valeurs** : d'un étudiant au suivant, seuls le matricule et la note changent.
Le formulaire **pré-remplit donc automatiquement** les champs de contexte (année, session, semestre,
N° UE, matière, date, n° de contrôle, coefficient) avec **les dernières valeurs saisies**. Au tout
premier enregistrement, l'année propose `2025-2026` et la date propose la date du jour. Il suffit de
corriger ce qui change réellement (par exemple en passant à une autre matière). Le même report
s'applique à l'écran de saisie des notes (`N2_Notes`).

## Relevé / bulletin (`/releve`) — nouveau V1.31
On saisit un matricule, une année, et on choisit un semestre ou « année complète ». L'application
calcule, à partir du barème et des notes, les moyennes par matière, par UE et par semestre, la
mention et une proposition Admis/Ajourné (à valider à la main : la délibération n'est pas
automatisée). Le relevé peut être imprimé (mise en page dédiée) ou exporté en Excel. Le récapitulatif
annuel regroupe les deux semestres du niveau et donne la moyenne annuelle.

Quand le barème utilisé n'est pas confirmé (au moins une UE à `Coef confirmé = Non`), le relevé porte
un bandeau **« Barème provisoire »** (visible à l'écran et à l'impression, ainsi que sous la moyenne
annuelle) : les moyennes affichées sont indicatives tant que les coefficients officiels ne sont pas
saisis. Note : pour L2 Soins infirmiers, la matière « Stage2 » figure légitimement en UE16 (S3) et en
UE21 (S4), conformément au relevé officiel (session 2024-2025) ; ce n'est pas un doublon.

Rappel : le calcul applique le décret 05-106 (¼ contrôle continu + ¾ examen ; moyenne d'UE ; moyenne
de semestre pondérée par les coefficients ; 2ᵉ session remplaçant la 1ʳᵉ). Les barèmes (coefficients,
ECTS) se définissent dans l'onglet « Barème des UE ».

## Signalements / indiscipline (`N3_Signalements`) — nouveau V1.33
On enregistre ici les signalements disciplinaires liés à un étudiant (date, contexte, fonction de
l'émetteur, nom, motif). C'est une information destinée à la délibération : elle ne modifie pas les
moyennes ni la proposition Admis/Ajourné. Sur le relevé affiché à l'écran, les signalements de
l'étudiant apparaissent dans un encart dédié et une mention signale leur nombre à côté de la
proposition. Ces informations ne figurent jamais sur le bulletin officiel (ni à l'impression, ni à
l'export Excel) ; elles restent réservées à l'usage interne (scolarité, délibération).

## État des signalements (`/etat-signalements`) — nouveau V1.34
Liste, groupés par étudiant, les signalements disciplinaires sur une période choisie (année et/ou
plage de dates), avec filtres facultatifs (semestre, contexte, filière, niveau). C'est un compte rendu
pour la scolarité, sans les notes. Il peut être imprimé ou exporté en Excel.

## Organisation des écrans (navigation) — V1.36
Le menu latéral et la page d'accueil sont regroupés en trois ensembles, avec des sous-groupes :

- **Scolarité** : Filières (référentiel des formations) · Enseignants (fiches, relevé d'heures, séances, calendrier) · Étudiants (inscriptions, présences, stages, barème/notes/relevés/signalements, documents) · Salles (planning, salles, réservations).
- **Administration** : Finances & pilotage (recettes/dépenses, comptes, requêtes, impressions, plan d'action, documents officiels) · Logistique / moyens généraux (équipements).
- **Direction** : tableau de bord uniquement.

Le **Paramétrage** (paramètres, rôles & droits, matrice des autorisations, import du fichier national, modèles de documents) n'est plus une rubrique centrale : on y accède par un **menu dédié sur la droite de la barre du haut**, et il est rappelé dans un bandeau séparé en bas de l'accueil. Les droits d'accès restent appliqués côté serveur (inchangés) : ce regroupement ne modifie pas qui peut faire quoi.

## Affichage des tableaux de consultation — V1.37
Tout tableau de données (en particulier le référentiel des formations R1, volumineux) propose au-dessus de la grille une recherche plein texte et, sous chaque en-tête, un filtre par colonne (liste déroulante si peu de valeurs, sinon champ « contient »). L'affichage est paginé (20 lignes par défaut ; 40 / 100 / Toutes au choix) avec un compteur, et la première colonne reste visible lors du défilement horizontal pour atteindre toutes les colonnes. Ces filtres ne concernent que l'affichage : l'export Excel reste complet.


## Bibliothèque documentaire (`/bibliotheque`) — magasin de fichiers hors-ligne — V1.99.22
Remplace l'ancien écran « Documents officiels » (registre Excel `H1_Biblio_docs`, qui ne stockait aucun fichier). **Vrai magasin de fichiers** sur le poste, 100 % hors ligne, inspiré de la bibliothèque GMAO. Dossier racine `donnees/bibliotheque/` (amorce : « Documents strategiques », « Documents officiels », « Supports de cours ») ; **rangement libre en sous-dossiers**. Fonctions : navigation (fil d'ariane + dossier parent), **ouverture/téléchargement** d'un fichier (tous formats), **dépôt** (upload), **création de sous-dossier**, **suppression** d'un fichier. **Anti-traversée** de répertoire systématique. Droits : **consultation/ouverture = tous** ; **dépôt + création de dossier = rôle ayant un droit d'écriture** (`metier.a_droit_ecriture`) ; **suppression = administration** (`est_admin`). Les écritures sont bloquées depuis un poste secondaire (réseau). Actions journalisées. L'onglet `H1_Biblio_docs` subsiste dans le classeur mais n'est plus exposé au menu.


## Plan d'action (`G1_Plan_action`) — suivi des écarts — V1.39
Saisie activée. Le tableau gagne une colonne **« Type d'écart »** (liste éditable `Types_ecart` : Budgétaire, Temporel, Contenu de formation, Qualité, Autre) qui qualifie la nature de l'écart, et le **« Statut »** devient une liste éditable `Statuts_action` à notion de planning (Non démarré, En cours, Atteint, En retard, Abandonné). L'EMSP saisit chaque écart : domaine/module, écart constaté, action corrective, responsable, échéance, type d'écart, statut. Les deux listes sont gérées dans Paramètres. (Affinage prévu : position de la colonne « Type d'écart » et valeurs des listes.)


## Matériel (`M1_Equipements`) — état & indisponibilité — V1.40
L'**état** est désormais une **liste éditable** `Etats_materiel` : Actif · En panne · Hors service · En maintenance · Réformé. Nouvelle colonne **« Localisation provisoire »** (texte libre : atelier, en réparation, prêté…). Un panneau **« Matériels indisponibles »** liste les matériels *En panne / Hors service* et propose, pour chacun, un bouton **« Exprimer un besoin »** ouvrant le formulaire d'expression de besoin pré-rempli (équipement + type).

## Expression de besoin (`L3_Besoins`) — nouvel écran (Logistique) — V1.40
Registre des besoins logistiques, autonome : un besoin peut découler d'un matériel en panne **ou** être tout autre (consommable, nouveau matériel, réparation…). Champs : ID besoin (auto BES-n), date d'expression, type de besoin (liste `Types_besoin`), équipement concerné (optionnel, liste des équipements M1), libellé, quantité, localisation/salle (liste L1), priorité (liste `Priorites_besoin`), statut (liste `Statuts_besoin`), coût estimé (KMF), demandeur, observations. Les listes sont éditables dans Paramètres. Saisie réservée au module Logistique / Direction.

## Console Comptes & accès (`/autorisations`) — refonte V1.43
Anciennement « Matrice des autorisations ». Réservée au **responsable informatique** (capacité `Admin droits (O/N)`).

**Ce que l'écran fait** : créer / modifier un compte (login, rôle affiché, **rubrique**, **couleur d'identité**), générer le **mot de passe initial** (aléatoire 8 caractères, affiché une seule fois), **réinitialiser** le mot de passe (idem), **renouveler** la validité (année scolaire), **supprimer** un compte. Tableau de gestion : Rôle / Login / Rubrique / Couleur / Valide jusqu'au / Compte / Actions.

**Ce que l'écran NE fait plus** : éditer les droits par module (lecture / écriture / accès financier / administrateur). Ces droits sont gérés par la **Direction directement dans `P1_Roles`** (classeur). La **matrice rôles × modules reste affichée en lecture seule** en haut de page, suivie du découpage module → onglets.

**Règles** :
- Mot de passe : généré (`secrets`, alphabet sans `O/0/l/1/I`), `doit_changer=True`, affiché **une seule fois** (encart copiable, porté par la session puis effacé). Plus de saisie manuelle de mot de passe par l'informatique.
- Validité : `valide_jusqu` = 31/07 de l'année scolaire courante à la création. Expiration **non bloquante** (bandeau « à renouveler » dans `base.html`, via `compte_expire` au contexte). « Renouveler » → 31/07 suivant, mot de passe inchangé.
- Couleur : choisie à la création/MAJ ; `metier.couleur_login()` privilégie la couleur stockée, sinon dérive du login.
- Superutilisateur protégé (ni modifiable ni supprimable).

**Stockage** : rubrique, couleur, `valide_jusqu` dans `instance/comptes.json` (hors dépôt). La création écrit dans `P1_Roles` **uniquement** `login + role` ; `ecrire_lignes_lot` préserve les colonnes de droits en mise à jour. **Classeur inchangé.**

**Self-service mot de passe** : supprimé. Lien retiré de la barre supérieure ; `/mot-de-passe` accessible uniquement en **changement forcé** (1er login / après réinitialisation) — sinon redirection vers l'accueil avec message renvoyant vers l'informatique.

**Code** : `metier.enregistrer_compte_it`, `metier.rubriques`, `metier.utilisateurs_admin` (enrichi) ; `auth.generer_mdp`/`definir_attributs`/`attributs`/`couleur`/`initialiser_validite`/`renouveler`/`est_expire`/`reinitialiser` ; routes `app.autorisations*` + `mot_de_passe` verrouillée. `config.RUBRIQUES`, `MDP_*`, `ANNEE_SCOLAIRE_FIN_*`.

## Clôture & archivage (`/cloture`) — nouveau V1.44
**Accès réservé à la Direction** (garde `_exige_direction` : droit d'écriture sur `J1_Journal_eleves`
ou `J2_Journal_compta`). Menu : Paramétrage → groupe « Clôture & archivage ». Trois opérations
manuelles, chacune génère un **procès-verbal de clôture / passation**.

- **Clôture des élèves** — année scolaire (oct → juil), clôturée au 31/07. Le tableau liste les
  élèves dont le statut marque une **sortie** (Diplômé / Abandonné / Radié) pas encore journalisés.
  Pour chacun, l'admin peut saisir le **diplôme obtenu** (texte) et la **mention** (liste :
  Passable / Assez bien / Bien / Très bien). À la validation, chaque élève est inscrit au **journal
  permanent `J1_Journal_eleves`** (idempotent : un matricule déjà journalisé n'est pas dupliqué).
  Les élèves **restent** dans `A1_Etudiants`.
- **Archivage** — bouton séparé. Déplace les cohortes sorties depuis **≥ 3 ans**
  (`config.ANNEES_GARDE_ELEVES`) vers `archives/EMSP_Archive_Eleves_AAAA-AAAA.xlsx` (un fichier par
  année scolaire de sortie), les retire de `A1_Etudiants` et renseigne la **réf. archive** dans `J1`.
- **Clôture compta** — année civile (champ AAAA). Archive tous les mouvements de l'exercice dans
  `archives/EMSP_Archive_Compta_AAAA.xlsx`, écrit le **journal permanent `J2_Journal_compta`**
  (totaux recettes / dépenses / solde de clôture), puis **report à nouveau** : `F1_Mouvements` est
  remplacé par une ligne « Report a nouveau » par compte au 01/01/N+1 (= solde de clôture) et
  `F2.Solde initial` est remis à 0. Le **solde courant de chaque compte est conservé**.

Après une opération, un encart **« Procès-verbal généré »** propose **« Voir / Imprimer (PDF) »**
(page imprimable `pv_cloture.html`) et **« Télécharger en Word »** (`.docx` généré sans dépendance).

## Procès-verbal de clôture (`/cloture/pv`, `/cloture/pv.docx`) — nouveau V1.44
Page **imprimable** (en-tête logo UdC + identité EMSP, charte #1F4E79, `print.css`), éditable avant
impression, imprimable en PDF par le navigateur. Le bouton **Word** télécharge le même contenu en
`.docx` (police Calibri, titres #1F4E79). Signataires : **Le Directeur** / **Le Gestionnaire**.

## Journaux permanents (`/module/J1_Journal_eleves`, `/module/J2_Journal_compta`) — nouveau V1.44
Onglets **du classeur** consultables en lecture seule via les pages module génériques (filtrage,
export Excel). `J1` = registre des élèves sortis (clôtures successives) ; `J2` = registre des
exercices comptables clos. Alimentés uniquement par l'écran Clôture & archivage.

## V1.45 — Correctifs de cohérence (dates & monétaire)
Correctifs internes `metier.py` (aucune modification du classeur ni des écrans) : déduplication de `_parse_date_fr` (réparation de la Situation de compte et du sélecteur de mois de la trésorerie) et de `_num` (montants « 50 000 »/« 12,5 » correctement lus), et harmonisation du séparateur de milliers monétaire (`_fmt_kmf` aligné sur `_kmf_aff` : « 799 423 »).

## V1.46 — Editions corrigees et nouvelles (hub Impressions)
Liste : + colonne « Origine / lieu actuel ». Releve d'heures : periode en clair (« Juin 2026 »). Situation de compte : + colonne « Compte » (registre EMSP ; alimentee par la Categorie, a confirmer). Nouvelles editions : Feuille de presence de la semaine (document A, paysage, jours x 4 creneaux 10h/12h/15h/17h, date+lieu de naissance, pre-remplie) ; Fiche d'appreciation de stage (document D, vierge a l'identique) ; Releve de notes / bulletin (decret 05-106, exemple de formation) ; Plan d'action (tableau G1) ; Journal de tresorerie et Situation globale / balance (profil financier). Aucune modification du classeur.

## V1.47 — Accueil & menu, compte formation
Accueil : Scolarite (Salles, Etudiants, Enseignants, Referentiel des formations) et Administration en pleine largeur ; Direction et Parametrage cote a cote. Menu de gauche : Parametrage en chapitre ; cliquer un chapitre renvoie au bloc d'accueil correspondant (ancres). Compte formation integre (formation/formation) en MODE_FORMATION, sans changement de mot de passe force. A activer sur une COPIE de l'application (instance/formation.flag), jamais sur la production.

## V1.48 — Colonne Compte (classeur), etats comptables, bulletin officiel
F1_Mouvements : nouvelle colonne « Compte » (saisie, plan comptable comorien) — apparait dans le formulaire de saisie Recettes & depenses et dans la Situation de compte (colonne Compte). Nouvel etat « Recettes/depenses par poste budgetaire » (Impressions, profil financier). Bulletin de notes officiel (Impressions > Releve de notes) au format RELEVE_NOTES.pdf : annuel, colonnes C.Continu/Examen/Moyenne/session 2/Coef/ECTS, decision du jury, mention. OU EDITER : saisir les notes dans Scolarite > Etudiants > Notes (N2) et Barème des UE (N1) ; generer/imprimer depuis Scolarite > Etudiants > Releve / bulletin et Administration > Impressions > Releve de notes (bulletin).

## V1.49 — Plan d'action enrichi + tableau de bord + formation tolerante
G1_Plan_action : 6 colonnes ajoutees (Axe / theme, Objectif, Priorite [liste], Temporalite [liste], Indicateur de reussite et preuves, Observations). Edition « Plan d'action » en paysage, ordre logique. Nouvelle page « Tableau de bord du plan d'action » (/plan-action/tableau-de-bord, depuis la Direction) : total, achevees, taux d'achevement, en retard, et graphiques par etat / priorite / axe. Detection du drapeau instance/formation.flag tolerante (casse + extension .txt).

---

## Fiche étudiant — bloc « Droits d'inscription » (V1.69)

Sous la fiche, un panneau **Droits d'inscription** affiche, pour le **niveau** et l'**année académique** courants de l'étudiant (lus dans A1) : **Dû** (tarif du niveau, depuis P0), **Payé** (somme des recettes F1 du poste 706 du niveau, filtrées par matricule + année académique) et **Reste dû**, puis le détail daté des versements. Lecture seule pour la scolarité et la direction. Si le niveau n'a pas de tarif en P0 (Master, formation continue, AS…), le bloc affiche **« Tarif non défini »** et pointe vers Paramètres.

Le bouton **« Encaisser un droit »** n'apparaît que pour le **rôle financier** (et hors poste secondaire), quand un tarif est défini.

## Écran d'encaissement `/etudiant/<matricule>/encaisser` (V1.69)

Mini-écran dédié, **écriture réservée au droit financier**, bloqué sur poste secondaire, **journalisé**. Il pré-remplit : Date = aujourd'hui, Sens = Recette, **Poste budgétaire = 706 du niveau** (706b L1 / 706c L2 / 706d L3), Montant = reste dû (éditable), Matricule, Tiers, Année académique (reprise de la fiche, éditable via la liste `Annees_acad`). L'opérateur choisit obligatoirement un **Compte / caisse** et un **Mode de paiement** (rattachement caisse + solde) ; une **Référence** facultative. La **catégorie comptable est laissée vide** : la comptabilité la complétera dans `/tresorerie`. À l'enregistrement, une ligne est ajoutée à `F1_Mouvements` et la fiche est rechargée avec le reste dû à jour.

Le rattachement **personne = matricule** et **niveau/année = poste 706 + année académique** isole proprement les versements d'un **redoublant** (un paiement L1 sur 706b ne compte pas pour la L2 sur 706c).

---

## V1.70 — Budget par poste, taux de change, édition « prévu / réalisé / écart »

### Écran « Budget par poste (prévu / réalisé) » — `F3_Budget_poste`
Menu **Finances & pilotage** (réservé au droit financier). Saisie générique d'une ligne de budget
prévisionnel rattachée à un **poste budgétaire**, pour un **exercice** (année civile).
- **Champs** : Exercice · Poste budgétaire (liste `Postes_budgetaires`) · Filière (**facultatif** :
  le budget est rattaché au poste, la filière n'est qu'un détail) · Sens (Recette / Dépense) ·
  Source de financement (liste partagée `Sources_financement`) · Montant budgété (KMF) · Observations ·
  Saisi par (rempli automatiquement).
- Le **réalisé** n'est jamais ressaisi : il est lu depuis `F1_Mouvements` (par poste, année civile)
  au moment de l'édition comparative — pas de double saisie, pas de risque d'incohérence.

### Écran « Taux de change (références) » — `P2_Taux`
Menu **Paramétrage** (Direction). Table de référence des devises.
- **Champs** : Devise (ex. EUR, USD) · Code (ISO, ex. 978) · Taux en KMF · Date d'effet (JJ/MM/AAAA) ·
  Observations.
- **EUR = 491,967 KMF** est pré-renseigné (parité fixe euro / franc comorien). Les autres devises
  (USD…) sont laissées à l'EMSP. `metier.taux_change('EUR')` renvoie la valeur pour réutilisation.

### Écran « Nomenclature budgétaire (codes) » — `P3_Nomenclature` (nouveau V1.99.9)
Menu **Paramétrage** (Direction). Liste paramétrable des codes budgétaires (module budget, touche C-1).
- **Champs** : Code (ex. `706b`) · Intitulé · Sens (Recette / Dépense / Investissement, saisie touche) ·
  Niveau (Chapitre / Article / Sous-article) · Source (OHADA / EMSP) · Actif (Oui / Non).
- **Socle OHADA + sous-articles EMSP** : amorcée avec 150 codes — 125 du plan comptable OHADA
  (classes 2/6/7, socle officiel) et 25 sous-articles propres EMSP (`6022B`, `605A`, `706a–e`…).
- **Curation par la colonne Actif (ressort comptabilité)** : seuls les codes `Actif = Oui` (73 codes
  déjà éprouvés à l'amorçage) apparaîtront dans les menus de saisie ; le socle OHADA en réserve est
  en `Actif = Non`, à activer au besoin **dans cet écran, sans modification de code**. L'application
  ne tranche aucun code : elle fournit la liste éditable, la compta l'affine.
- **Onglet de référence** : ajouté au classeur par chirurgie ZIP (`scripts/chirurgie_V1_99_9_nomenclature.py`,
  dessins préservés), en-têtes ligne 2 selon la convention classeur.
- **Consommation par F1 / F3 (C-3, V1.99.10)** : le champ **« Poste budgetaire »** de `F1_Mouvements`
  (saisie d'un mouvement) et de `F3_Budget_poste` (ligne de budget) propose désormais **les codes
  `Actif = Oui` de P3**, en autocomplete « code — intitulé » (Lot B) ; **le code seul est enregistré**.
  Source de liste `Codes budgétaires actifs (P3)` (variante filtrée de `LISTES_ONGLET_VALLABEL`, filtre
  `Actif = Oui`). Pas de filtrage par Sens en V1.99.10 (tous les codes actifs ; affinage possible plus tard).

### Écran « Nomenclature — curation » — `/parametres/nomenclature` (nouveau V1.99.11, C-2)
Pseudo-page **`NOM_Curation`** (menu Paramétrage → Configuration), réservée au droit d'écriture sur `P3_Nomenclature`.
Complète l'éditeur générique (qui reste l'écran d'**ajout / modification** d'un code).
- **Barre de filtres** (serveur) : Sens (Recette / Dépense / Investissement) · Source (OHADA / EMSP) ·
  Actif (Oui / Non) · recherche par code ou intitulé. Compteurs Total / Actifs / Réserve / Affichés.
- **Bascule Actif en masse** : cocher plusieurs lignes → **« Activer la sélection »** / **« Désactiver
  la sélection »** (`metier.basculer_actif_codes`, upsert clé = `Code`, ne touche qu'à la colonne Actif ;
  codes inconnus ignorés). Gain par rapport au générique : curer des dizaines de codes OHADA d'un coup. Journalisé.
- **Routage** : `SPECIAL_ROUTES["NOM_Curation"] = "nomenclature"` ; l'éditeur générique
  (`/module/P3_Nomenclature`) reste joignable pour l'ajout / l'édition en ligne.

### Édition « Budget : prévu / réalisé / écart »
Hub **Impressions & éditions** → carte « Budget : prévu / réalisé / écart », avec un sélecteur
**Exercice** (année civile, défaut = année en cours). Produit un tableau paysage par poste :
**Prévu (KMF)** (somme F3 du poste pour l'exercice) · **Réalisé (KMF)** (somme F1 du poste sur
l'année civile) · **Écart (KMF)** (réalisé − prévu) · **Taux de réalisation %**, avec ligne TOTAL.
- Le réalisé est raisonné en **année civile** (cohérent avec la clôture comptable).
- La couverture sanitaire (poste 658b) reste **hors réconciliation**.
- Sans paramètre d'exercice, la même route conserve l'**état par poste** classique (recettes /
  dépenses / solde, filtrable par période et compte) inchangé depuis V1.48.

### Liste partagée « Source de financement »
La liste P0 historiquement nommée « Bailleurs » est renommée **« Sources_financement »** :
AFD · Etat comorien · Ressources propres EMSP · Autres donateurs. C'est désormais **une seule liste**
partagée par la trésorerie (`F1`), l'inventaire des équipements (`M1`) et le budget (`F3`) — cohérence
des origines de fonds dans tout l'outil. Les valeurs restent **éditables** dans Paramètres (P0).

## Saisie des notes par classe (grille) — nouveau V1.76
Écran `Scolarité ▸ Notes & bulletins ▸ Saisie des notes par classe (liste matière)`
(pseudo-page `NOT_Grille` → route `saisie_notes_classe`). Saisie en **liste**, façon
feuille de présence, pour une classe et une matière.

- **Sélection** : Filière · Niveau · Section (facultative) · Année · Semestre · Session
  (1 normale / 2 rattrapage) · Matière (groupée par UE, depuis `N1_Bareme_UE`).
  Auto-soumission à chaque changement.
- **Grille** (`templates/saisie_notes_classe.html`) : une ligne par étudiant
  (`liste_etudiants`), **plusieurs contrôles** paramétrables (3 par défaut, coef 1 par
  colonne, modifiable ; boutons ajouter/retirer un contrôle), **CC** = moyenne pondérée
  des contrôles, **Examen**, **Moyenne** = ¼ CC + ¾ examen (décret 05-106, art. 8).
  CC et moyenne recalculés en direct côté client.
- **Écriture** (`metier.enregistrer_notes_grille`) : un upsert dans `N4_Controles`
  (une ligne par étudiant × contrôle : N° contrôle, Note /20, Coef) ; l'examen dans
  `N2_Notes` (le CC reste **dérivé** de N4, non écrit dans N2). Réduire le nombre de
  contrôles vide proprement les contrôles supprimés (pas d'orphelin dans le CC).
  Garde écriture `N2_Notes`.
- **Édition** : bouton « Éditer » → `/impressions/feuille-notes` (`metier.feuille_notes_edition`),
  feuille paysage avec colonnes C1…Cn (+coef), CC, Examen, Moyenne, signatures
  enseignant / chef de département. Rendu générique `kind="table"`.
- Cohérence bulletin préservée : la moyenne d'UE / de semestre reste calculée par le
  relevé (`releve_semestre`) à partir de `N1_Bareme_UE` ; la grille ne produit que
  CC/Examen par matière.


## Matière non dispensée — nouveau V1.77
Ajout sur l'écran **Saisie des notes par classe** d'un interrupteur **« Matière non
dispensée ce semestre »** (case à cocher + motif facultatif), sous la barre des contrôles.

- Quand il est coché : la grille est grisée/bloquée (aucune note à saisir), la matière est
  **tracée** dans le nouvel onglet `N5_Matieres_ND` du classeur `EMSP_Notes.xlsx` au **niveau
  classe** (Filière, Niveau, Section, Année, Session, Semestre, N° UE, Matière, Motif, Saisi par).
  Aucune note n'est enregistrée. Décocher puis enregistrer **retire** la trace (réversible).
- Sur le **relevé de semestre** et le **bulletin annuel** (`releve_print.html`,
  `bulletin_officiel.html`) : la matière ND **n'apparaît pas** (affichage b). Une **mention de
  traçabilité** est imprimée en pied : « Certaines matières prévues n'ont peut-être pas été
  totalement dispensées ce semestre… ». La **moyenne d'UE / de semestre est recalculée** sur les
  seules matières faites et notées.
- **ECTS — option (i)** : l'UE **conserve ses ECTS** tant qu'une matière est faite ; seule une
  **UE entièrement non dispensée** est retirée (du relevé et de l'`ects_total`). Une matière
  enseignée **mais pas encore notée** n'est PAS une ND : elle laisse le relevé marqué
  **incomplet/provisoire** sans être exclue.
- Logique : `metier._matieres_nd` (lecture du set ND pour la classe/semestre),
  `metier._nd_etat_exact` (état de l'interrupteur pour le contexte exact),
  `metier.enregistrer_matiere_nd` (upsert/retrait, réécriture idempotente de l'onglet).
  `releve_semestre` exclut les matières ND et retire les UE entièrement ND ; les flags
  `a_non_dispensee` / `incomplet` pilotent les mentions imprimées.


## Accueil épuré & arborescence — V1.78
- **Accueil** : plus de tuiles centrales (elles refaisaient le menu). La zone centrale est vide ;
  un **filigrane du logo UDC** (léger, centré, persistant derrière tous les écrans, masqué à
  l'impression) sert de décor. Le logo est vendoré dans `static/img/logo_udc.jpg` et alimente
  aussi la barre latérale et le pied de page.
- **Menu de gauche réordonné** (piloté par `config.GUIDE_STRUCTURE`, sans toucher aux modules) :
  1. **Vie académique** — Élèves (fiche étudiant en tête), Présences, Notes & bulletins, Stages,
     Discipline, Référentiel des formations.
  2. **Enseignement** — Enseignants (fiche enseignant en tête), Activité (séances, calendrier,
     séances réalisées), Heures (relevé, heures constatées).
  3. **Patrimoine** — Salles, Matériel.
  4. **Finances** — Trésorerie & budget, Clôture & journaux.
  5. **Pilotage** — Tableau de bord, Requêtes, Impressions, Plan d'action (déplacé en fin).
  6. **Administration** — Documents & modèles, Configuration.
  Principe : mener avec le quotidien, descendre le pilotage ; la navigation transversale se fait
  par les **fiches** (la fiche étudiant pointe déjà vers ses inscriptions/présences/notes/stages ;
  la fiche enseignant suivra la même logique vers séances/heures/paiement).

---
## V1.79 — fiche enseignant reliée + état des heures + correction présences (25/06/2026)

- **Fiche enseignant** : barre **« Accès direct »** (symétrie fiche étudiant) — liens vers
  *État des heures à payer* (imprimable), *Calendrier / séances*, *Heures constatées*, *Imprimer la
  fiche*. La chaîne séances planifiées (A3) → réalisées (E3) → heures (E2) → état des heures reste
  affichée en détail sous la barre. Aucun onglet ni métier ajouté.
- **État des heures à payer** (nouvel imprimable `etat_heures_print.html`, route
  `/enseignant/<matricule>/heures/imprimer`) : en-tête UDC, identité (matricule, nom, statut,
  département), relevé E2 (programmé / constaté / **total à payer**), total en pied, cases de visa
  (enseignant / chef de dépt / comptabilité). **Aucun montant KMF** : la compta valorise sur la
  base des contrats signés et de ce relevé (Option A validée).
- **Présences – séance libre** : **date du jour par défaut** (modifiable) ; nouvelle saisie par
  **Durée (h:mm)** qui calcule l'**Heure fin** (début + durée). Saisie directe de la fin → la durée
  se recalcule. Stockage inchangé (début + fin), aucun impact sur les données.

---
## V1.80 — verrou anti-suppression P0 + sauvegarde horodatée (25/06/2026)

- **Verrou listes P0** : une valeur de liste structurante ne peut plus être retirée si elle est
  encore employée dans les données. Le retrait est bloqué avec un message indiquant le nombre
  d'enregistrements concernés et les onglets (« Aides-soignants est utilisé dans 30 enregistrement(s)
  (A1_Etudiants: 30) »). Table de correspondance dans `config.P0_CONSOMMATEURS` (15 listes
  couvertes : filières, niveaux, sections, semestres, statuts étudiant, années acad., lieux de stage,
  catégories recettes/dépenses, postes budgétaires, modes de paiement, comptes/caisses, sources de
  financement, catégories d'équipement, états matériel). Les listes hors table restent librement
  modifiables. Métier : `valeur_liste_utilisee()` ; branché dans `/parametres/supprimer`.
- **Sauvegarde des données** (Administration → Sauvegarde & maintenance, route `/sauvegarde`,
  réservée admin) : bouton « Créer une sauvegarde » → copie **horodatée** des classeurs de données
  (`EMSP_V1.xlsx` + `EMSP_Notes.xlsx`) dans `donnees/sauvegardes/EMSP_sauvegarde_AAAA-MM-JJ_HHMMSS/`.
  Copie fichier brute (shutil), jamais via openpyxl → aucun dessin altéré. La liste des sauvegardes
  existantes (date lisible, nb de classeurs, taille) est affichée ; restauration manuelle documentée
  (copier le dossier choisi par-dessus `donnees/data/`, application fermée). Métier :
  `sauvegarder_classeurs()`, `liste_sauvegardes()`.

---
## V1.81 — module stages : suivi multicritère + tableau de bord (25/06/2026)

- **Stages — suivi & tableau de bord** (Vie académique → Stages, route `/stages`, lecture S1) :
  écran d'agrégation **en lecture pure** sur S1_Stages (affectations) joint à A1_Etudiants (nom,
  prénom, filière, niveau) et S2_Lieux_stage (quota, niveau, période).
  - **Filtres** (CDC §7) : lieu · période/séance · niveau (L1/L2/L3) · filière · nom/matricule.
  - **Tableau de bord** (CDC §6) : étudiants affectés · nb de lieux · places disponibles · taux
    d'occupation global · répartition par promotion ; détail **occupation par lieu**
    (quota / occupé / disponible / taux), un taux > 100 % signalant un dépassement de quota.
  - **Affectations** : table filtrée (séance, matricule, nom, filière, niveau, lieu, dates, fiche
    retour, note).
- **Impression** (route `/stages/imprimer`, mêmes filtres) : édition paysage des affectations +
  synthèse + occupation par lieu. Couvre la liste des affectations et le planning par période (via
  le filtre séance). Métier : `stages_synthese()`.
- **Non livré (cadré séparément)** : affectation automatique (CDC §4/§11) — à recadrer avec les
  données réelles et les règles confirmées (V1.82).

---
## V1.82 — homogénéisation saisie (ligne unique) + retrait doublon CC (26/06/2026)

- **Saisie sur une seule ligne** : les formulaires « Ajouter une ligne » des modules adoptent une
  disposition **horizontale à ligne unique avec défilement** (comme la table de restitution en bas
  de page), au lieu de champs répartis sur plusieurs rangées. CSS `.saisie-grid`
  (`flex-wrap:nowrap; overflow-x:auto`), champs non rétractables (`flex:0 0 auto`). Aucun changement
  de champ ni de logique : seule la mise en page change, identique sur tous les écrans de saisie.
- **Retrait du doublon « Contrôles continus (détail, CC dérivé) »** (éditeur générique
  `N4_Controles`) du menu Notes & bulletins. La saisie des contrôles continus se fait désormais
  uniquement via la grille **« Saisie des notes par classe »**, qui écrit déjà dans `N4_Controles`
  (C1/C2/C3 + coef) et reste l'entrée recommandée. L'onglet `N4_Controles` et ses données sont
  conservés ; seul l'accès redondant au menu est supprimé (URL directe → 404 propre).

---
## V1.83 — saisie : champs obligatoires regroupés en tête de ligne (26/06/2026)

Complément de la saisie en ligne unique (V1.82). Dans le formulaire « Ajouter une ligne », les
champs **obligatoires** sont désormais regroupés **au début de la ligne** ; les champs facultatifs
suivent. Ainsi l'utilisateur saisit tout le requis sans devoir tabuler/défiler jusqu'au bout de la
ligne. Tri **stable** (`champs_saisie` dans metier) : l'ordre d'origine (Excel) est conservé à
l'intérieur de chaque groupe. Aucun champ ni règle modifiés ; l'enregistrement reste indexé par nom
de colonne (insensible à l'ordre d'affichage). Exemple A1 : Matricule, Nom, Prénom, Niveau, Filière,
Année, Statut (obligatoires) puis N° ordre, Genre, dates, Section, Saisi par.

---
## V1.84 — renommage de l'écran N2_Notes en « correction directe (avancé) » (26/06/2026)

L'entrée de menu « Notes — examen (CC dérivé des contrôles) » (éditeur ligne-à-ligne de `N2_Notes`)
est **conservée mais renommée** « **Notes — correction directe (avancé)** » (icône ti-edit), pour la
positionner clairement comme un outil de correction à l'écart, distinct de la saisie courante.

Rôle / justification : c'est le **seul** écran permettant (a) de **forcer un CC à la main** — la
grille calcule le CC depuis les contrôles et ne le laisse pas saisir, le bulletin ne réécrit pas un
CC dérivé — et (b) de corriger une **note hors d'une classe** (étudiant ayant changé de classe,
matière hors maquette, cas particulier), invisible dans la grille et le bulletin. Les corrections
courantes restent à faire par re-saisie dans « Saisie des notes par classe » ou « Saisie façon
bulletin » (mise à jour par écrasement / upsert).

Note : le sous-titre interne « NOTES PAR ÉTUDIANT — contrôle continu et examen » provient de la
première ligne de l'onglet `N2_Notes` (donnée du classeur) ; il sera aligné lors d'une prochaine
retouche du classeur (hors chantier code).

---
## V1.85 — résultats par classe (synthèse) + année en liste sur le relevé (26/06/2026)

- **Résultats par classe (synthèse)** (Vie académique → Notes & bulletins, route `/resultats-classe`,
  lecture N2_Notes) : on choisit filière / niveau / section (option.) / année / période (la période
  s'adapte à la classe via `semestres_classe` + option « Annuel »). Le logiciel produit **une ligne
  par élève** : N° · Matricule · Nom · Prénom · **Moyenne** (calcul décret 05-106) · Mention ·
  **Décision** (Admis/Ajourné, proposée) · ECTS acquis/total (semestre) · Obs. (incomplet, barème
  provisoire, matière ND). Cartes de synthèse : effectif, admis, ajournés, moyenne de classe.
  Réutilise le calcul bulletin existant (`releve_semestre` / `releve_annuel`) sur le roster
  (`roster_classe`). Lecture/agrégation pure, aucune écriture. Métier : `resultats_classe`.
- **Impression** (route `/resultats-classe/imprimer`, mêmes critères) : tableau paysage (kind=table),
  légende avec effectif/admis/ajournés/moyenne de classe. Mentions : décisions PROPOSÉES, délibération
  validée à la main.
- **Délibération & attestations de passage (R7a — V1.99.43)** : sur le même écran `/resultats-classe`,
  un panneau permet de saisir la **date de délibération** (conseil des professeurs) de la classe
  (filière+niveau+année). À partir de cette date court un **délai de contestation de 7 jours**
  (`config.DELAI_CONTESTATION_JOURS`) ; avant son expiration, les attestations ne sont pas générables
  (garde serveur + UI). Après expiration, l'attestation de passage devient téléchargeable : un lien
  **PDF** par élève **Admis** (en vue annuelle), et un bouton **« Générer le lot »** produisant un
  **ZIP** de tous les admis de la classe. Les PDF sont aussi copiés dans
  `documents/etudiants/<année>/Attestation_passage_<matricule>.pdf`. La décision portée est
  **Admis/Ajourné** (déjà calculée) ; le *passage conditionnel* (règle ECTS) reste à confirmer par le
  Directeur (non traité, R7b). La date de délibération est stockée hors classeur dans
  `instance/deliberations.json` (métadonnée de workflow). PDF produit avec **fpdf2** (police cœur
  Helvetica, logo UdC), mise en page **chartée générique** (modèle Word officiel non encore fourni).
  Métier : `deliberation_classe`, `enregistrer_deliberation`, `attestation_data`, `generer_attestation`,
  `generer_attestations_lot`. Routes : `POST /resultats-classe/deliberation`,
  `GET /resultats-classe/attestation/<matricule>`, `GET /resultats-classe/attestations/lot`.
  **Dépendance hors-ligne** : fpdf2 (+ pillow, fonttools, defusedxml) à ajouter au wheelhouse.
- **Passage conditionnel & validation définitive (R7b — V1.99.44)** : la **décision officielle** de
  passage suit la règle `decision_passage_officielle` : **moyenne ≥ 10 → Admis** ; sinon **écart de
  crédits ECTS ≤ marge paramétrable** (réglage `seuil_passage`) **→ Admis conditionnel** ; sinon
  **→ Ajourné**. Affichée 3 états sur l'écran résultats (carte « Admis cond. » dans la synthèse).
  L'**admission définitive** est une **action manuelle** : liste à cocher par classe (vue annuelle),
  stockée hors classeur (`instance/validations_bulletins.json`). **C'est la validation qui libère
  l'attestation** (la délibération + délai R7a restent un repère). Les **Admis conditionnel** sont
  attestables. Le bulletin officiel porte une **zone « Observations / mention » vierge** pour une
  mention manuscrite. Métier : `decision_passage_officielle`, `bulletins_valides`,
  `est_bulletin_valide`, `enregistrer_validations`. Route : `POST /resultats-classe/validation`.
- **Relevé / bulletin** : le champ **Année** passe en **liste déroulante** (valeurs P0 Annees_acad).
  Le matricule reste en saisie libre (choix retenu). Couvre le besoin « éditer les résultats d'une
  classe globalement » (synthèse 1 ligne/élève). L'impression des bulletins complets reste
  individuelle ; le détail par matière reste disponible via « Saisie des notes par classe » →
  feuille de notes.

---
## V1.86 — relevé : matricule saisissable ET sélectionnable (26/06/2026)

Sur « Relevé / bulletin », le champ **Matricule** reste en saisie libre mais devient aussi
**sélectionnable** : champ texte associé à une `datalist` (`etudiants_dispo()` → « matricule — Nom
Prénom »). L'utilisateur peut taper le numéro, ou choisir dans la liste (recherche par numéro ou par
nom). À la validation, `_matricule_saisi` ré-extrait le matricule, qu'il ait été tapé ou choisi.
100 % hors-ligne (datalist locale, aucune requête).

---
## V1.87 — stages : affectation automatique (proposition, lecture seule) (26/06/2026)

**Stages — affectation automatique** (Vie académique → Stages, route `/stages/affectation`, lecture
S1) : on choisit filière / niveau / année / séance (+ case « autoriser le dépassement de quota »).
Le logiciel **propose** une affectation (rien n'est enregistré). Règles validées (Dr Kamal, 26/06) :
1. quotas respectés, surplus en **liste d'attente** ; dépassement uniquement si demandé, **signalé** ;
2. (rattrapage : remplacera le résultat initial — géré à l'écriture, étape suivante) ;
3. sections de cours **ignorées** ; le groupe = **quota du lieu** ;
4. lieu déjà effectué **évité si possible** (préférence, pas interdiction) ;
5. ordre alphabétique Nom-Prénom avec **rotation** du point de départ selon la séance.
Écran : cartes (effectif, affectés, attente, capacité), occupation par lieu, table des affectations
proposées (obs. dépassement / lieu déjà fait), liste d'attente. **Impression** paysage
(`/stages/affectation/imprimer`). Métier : `proposer_affectation_stages` (lecture/agrégation pure).
**Enregistrement dans S1_Stages : non encore livré** (proposition à valider à la main d'abord).

---
## V1.88 — stages : enregistrement de l'affectation validée (26/06/2026)

Complète V1.87. Sur l'écran « Stages — affectation automatique », un bouton **« Valider et
enregistrer »** (confirmation requise) écrit la proposition dans **S1_Stages** :
- upsert par **Matricule + Année + N° séance** (une ligne de stage par élève et par séance) ;
- seul le **Lieu de stage** est posé ; **notes, dates et fiches retour existantes sont préservées**
  (`ecrire_lignes_lot` n'écrit que les colonnes fournies) — le rattrapage remplace le **résultat** à
  la saisie de la note, pas ici ;
- la **liste d'attente n'est pas enregistrée** ;
- ré-exécuter met à jour les lieux sans créer de doublon (idempotent).
Action journalisée. Métier : `enregistrer_affectation_stages`. Droit d'écriture S1_Stages requis.

---
## V1.89 — statuts enseignants (4) + salles dérivées du matériel (26/06/2026)

Suite réunion Dr Kamal (26/06).
- **Statuts enseignants** : la liste passe de « Titulaire / Vacataire » à **4 statuts** —
  **Permanent, Vacataire, Contractuel, Bénévole** (`config.LISTES_INLINE`). « Titulaire » devient
  « Permanent ». Les saisies futures proposent les 4 ; les données existantes ne sont pas migrées
  (E1 vide à ce stade).
- **Salles** : tant que `L1_Salles` n'a pas de numérotation officielle, l'écran Salles **dérive les
  salles des noms présents dans l'inventaire matériel** (M1 « Salle / localisation »), avec le nombre
  d'équipements inventoriés par salle. Lecture seule (aucune écriture). Débloque l'écran Salles qui
  attendait `L1_Salles`. L'inventaire par salle (édition #13) reste disponible par ailleurs.

## V1.90 — notes : rattrapage corrigé, passage conditionnel, crédits au bulletin (26/06/2026)

- **Rattrapage (2ᵉ session)** : la moyenne de session 2 conserve le **CC de la session 1** (le
  rattrapage ne refait que l'examen) → `Moyenne = ¼ CC(S1) + ¾ Examen(S2)`. Auparavant, sans CC
  re-saisi en S2, la moyenne tombait sur l'examen seul. La session 2 remplace la session 1 dans la
  moyenne effective ; les deux sessions restent stockées dans `N2_Notes` (colonne `Session` :
  1 = juin, 2 = rattrapage) pour consultation.
- **Décision de passage (annuelle)** : écart de crédits = ECTS requis du niveau (somme des UE sur les
  2 semestres) − ECTS acquis (UE validées, moyenne UE ≥ 10). **écart 0 → Admis ; 1…seuil → Admis
  conditionnel ; > seuil → Ajourné.** Le seuil est **paramétrable** dans `config.py`
  (`SEUIL_PASSAGE_CONDITIONNEL`, défaut 5).
- **Bulletin officiel** (Administration > Impressions > Relevé de notes) : le bandeau annuel affiche
  désormais **Crédits : acquis / requis (écart)** et la **Décision** (Admis / Admis conditionnel /
  Ajourné), en plus de la moyenne et de la mention annuelles.

---

## V1.91 — affichage (crédits à la saisie · colonne Session)

- **Saisie des notes par classe** : l'entête du panneau rappelle les **crédits (ECTS) de l'UE** de la matière saisie (lecture seule, issus du barème).
- **Relevé de notes (impression)** : nouvelle colonne **Session** par matière — *Normale* (session 1) ou *Rattrapage* (session 2), selon la session retenue. Les lignes UE et la ligne « Moyenne du semestre » laissent la cellule vide.


---

## V1.92 — heures constatées : régularisations tracées

- **Heures constatées du mois** : le **report forcé** (écrasement d'une valeur E2 corrigée à la main) exige un **motif obligatoire**. Chaque correction est inscrite au **journal d'audit** : enseignant, ancienne → nouvelle valeur, motif, utilisateur, date. Le report normal (E2 vide ou identique) ne demande pas de motif et n'est pas tracé comme régularisation.
- **Pour la comptabilité** : après report, `E2_Releve_heures` porte la valeur réelle ; le journal documente l'historique des corrections.


---

## V1.93 — tableau de bord : reste dû par filière

- **Tableau de bord direction** : nouveau graphique **« Reste dû par filière (KMF) »** et carte KPI **« Reste dû (KMF) »** (total). Reste dû d'inscription par étudiant (tarif P0 − payé F1, trop-perçu plafonné à 0), agrégé par filière. Réagit aux filtres filière/niveau/année du tableau de bord.


---

## V1.94 — clôture comptable stricte par année

- **Clôture & archivage (volet compta)** : le solde de clôture d'un exercice est désormais **arrêté au 31/12 de l'année civile** (solde initial + mouvements de l'année), et non le solde courant. La clôture **n'archive que les mouvements de l'exercice** et **conserve les écritures de l'année suivante** déjà saisies. Le report à nouveau (01/01) reprend ce solde à l'identique. L'année académique, elle, ne reporte pas de solde (elle gère les étudiants).


---

## V1.95 — annee academique courante (bascule explicite)

- **Cloture & archivage** : bloc **« Annee academique courante »** = annee proposee par defaut a l'inscription / la saisie. Bouton **« Passer a l'annee suivante »** (explicite, avec confirmation) et **definition manuelle** (AAAA-AAAA). Stockee dans `instance/reglages.json`. Distincte de la cloture comptable (annee civile). Voir le manuel `doc/MANUEL_BASCULE_ANNEE.md`.


---

## V1.96 — lanceur robuste

- **Demarrage** : relancer pendant que l'appli tourne ne cree plus de 2e fenetre (le navigateur se rouvre sur l'instance en cours).
- **Quitter** : bouton **« Quitter »** dans la barre du haut -> arrete proprement le serveur (a privilegier ; fermer l'onglet n'arrete pas le serveur). Reserve au poste principal.
- **Formation** : tourne sur le port **5001** (production : 5000), donc peut coexister avec la production sans conflit. Un verrou par dossier de donnees empeche toute ecriture concurrente sur le meme classeur.


## V1.99.1 — fiche bailleur : documents liés (3b) + typage des champs (3c)

### Documents liés (3b) — `/bailleur?id=<ID>`
- Bloc **« Documents liés »** sur la fiche : tableau **Document · Type · Date d'ajout · Taille · Ajouté par · Statut**, chaque ligne ouvrant le fichier en téléchargement.
- **Stockage** : un dossier par bailleur `donnees/documents/bailleurs/<ID>/` (hors classeur, hors zip) + un `index.json` de métadonnées ; le dossier fait foi (bibliothèque).
- **Ajout** (réservé module **Financier**) : **Type** dans la liste paramétrable `Types_doc_bailleur` + fichier **PDF / JPG / PNG / DOCX**, 10 Mo maximum.
- **Pas de suppression** : un document obsolète est **marqué** via la colonne **Statut** (libellé libre) — il reste consultable, jamais effacé ; réactivation = vider le libellé.
- **Sécurité** : noms de fichiers assainis, anti-traversée de répertoire, seuls les fichiers réellement indexés sont téléchargeables (le fichier d'index n'est jamais servi). Lecture/téléchargement réservés à l'accès lecture de `F4_Bailleurs` ; ajout/marquage au droit d'écriture financier.
- **Impression** : la fiche imprimable liste les documents (nom · type · date · statut), sans les binaires.
- **Compteur** : la colonne **« Documents liés »** de `F4_Bailleurs` affiche le **nombre de documents** (mis à jour automatiquement, **lecture seule** — non saisissable dans l'éditeur).

### Typage des champs F4 (3c) — éditeur `/module?onglet=F4_Bailleurs`
- Champs de `F4_Bailleurs` **typés via le Dictionnaire** :
  - **Type** → liste **`Types_bailleur`** (International · État · Bilatéral · Multilatéral · ONG / Fondation · Privé · Autre), paramétrable.
  - **Statut** → liste **`Statuts_bailleur`** (Actif · Clôturé · Suspendu · Autre), paramétrable.
  - **Date début** / **Date fin** → saisie **JJ/MM/AAAA**.
  - **Budget alloué (KMF)** → saisie numérique (KMF).
  - **Documents liés** → compteur automatique, **lecture seule**.
- Les listes `Types_bailleur`, `Statuts_bailleur` et `Types_doc_bailleur` s'enrichissent depuis **Paramètres / Dictionnaire**.
- **Classeur** : +3 colonnes-listes `P0_Parametres` + 12 lignes Dictionnaire pour `F4_Bailleurs`. Déployé : `ajout_P0_types_doc_bailleur.py` + `seed_3c_typage_F4.py` (idempotents). Maître : chirurgie ZIP `chirurgie_V1_99_1_typage.py` (16 dessins préservés → `EMSP_V1_MAITRE_V1_99_1.xlsx`).


## V1.99.2 — fiche bailleur : indice de traçabilité (Touche 4)

### Bloc « Traçabilité du financement » — `/bailleur?id=<ID>`
- En-tête (KPIs), par bailleur : **Budget alloué** (F4) · **Dépensé** (F1, dépenses taguées à ce bailleur) · **Reste à dépenser** = Budget − Dépensé avec **% consommé** · **Équipements rattachés** (M1) avec **dont localisés (%)**.
- **Honnête** : tout est calculé à la volée depuis les onglets ; vide/zéro tant que rien n'est tagué, grimpe à mesure que l'école renseigne le champ « Source de financement / Bailleur » de M1/F1/F3.
- **% localisés** : part des équipements rattachés ayant une salle réelle (exclut « (à ventiler) » et « (non localisé) »).
- **Lien « Voir les équipements »** (vue M1 filtrée par bailleur) — affiché seulement s'il y a des équipements.
- **Détail par poste** (facultatif) : tableau **Budgété (F3) / Dépensé (F1)** par poste, affiché seulement s'il y a des données ; sinon une ligne conseille de renseigner le budget par poste (F3) et de taguer les écritures (F1). Repris sur la fiche imprimable.

### Câblage de la liste Bailleur
- Le champ « Source de financement / Bailleur » de **M1, F1 et F3** est déjà une **liste contrôlée** vers `Sources_financement` ; `F4.ID = valeur Sources_financement` assure la **jointure**.
- **2 fiches F4 ajoutées** (« Ressources propres EMSP », « Autres donateurs ») pour que **tout financement tagué soit traçable** (4 bailleurs au total). Maître : chirurgie ZIP `chirurgie_V1_99_2_F4rows.py` (16 dessins préservés, sortie `EMSP_V1_MAITRE_V1_99_2.xlsx`). Déployé : `seed_F4_sources_internes.py` (idempotent).
- **Décision actée** : pas de détail budgétaire par poste imposé au départ — le budget alloué (F4) suffit ; le détail par poste émerge des écritures (F1) et reste une option conseillée (F3).

## V1.99.12 — Budget prévisionnel par formation (module budget C-4)

Nouvel écran **« Budget prévisionnel par formation »** (`/budget/previsionnel`, pseudo-page `BUD_Previsionnel`, menu Finances, droits **Financier**). Saisie détaillée par formation et par niveau (M1, M2, L1, L2, L3), façon `MODEL_BUDGET.xlsx`.

- **Structure (chirurgie ZIP maître)** : +onglet `F5_Budget_Prev` (14 colonnes : Formation, Niveau, Rubrique, Designation, Unite1, Qte1, Unite2, Qte2, Cout unitaire (KMF), Poste budgetaire, Source de financement / Bailleur, Session, Montant (KMF), Montant (EUR)). 16 dessins préservés, 34 onglets. Script `scripts/chirurgie_V1_99_12_budget_prev.py` (idempotent, robuste maître/déployé).
- **Calculs (Python, jamais de cellule formule)** : Montant ligne = Qte1 × Qte2 × Cout unitaire (quantité vide = 1 → coût forfaitaire). Par niveau : Total, frais administratifs EMSP (%), sous-total. Par formation : total. Conversion EUR au taux. Montant (KMF)/(EUR) écrits comme **valeur** (précédent E4), hors `READONLY_COLS`.
- **Réglages (`instance/reglages.json`)** : `taux_eur` (défaut 491,967 — repli P2_Taux puis `config`) et `frais_admin_pct` (défaut 5). Modifiables depuis l'écran (droit écriture), sans toucher au code.
- **Poste budgétaire** : autocomplete des codes P3 **actifs ET de sens Dépense** (mécanisme `LISTES_ONGLET_VALLABEL_FILTRE` étendu au multi-critère ; code seul enregistré). F1/F3 restent non filtrés.
- **Saisie** : écran custom (comme E4 ; F5 hors `ONGLETS_SAISIE_ACTIVE`). CRUD par ligne (ajout, édition en place, suppression par index via `data.supprimer_ligne_par_index`).
- **Impression** : `/budget/previsionnel/imprimer` — A4 paysage, en-tête institutionnel UDC/EMSP, blocs par niveau (Total / frais / sous-total), total formation et total général, signatures (Gestionnaire / Directeur EMSP / Visa bailleur).

Lot : `config.py` (VERSION 1.99.12), `data.py`, `metier.py`, `app.py`, `templates/budget_previsionnel.html` + `budget_previsionnel_print.html`, `scripts/chirurgie_V1_99_12_budget_prev.py`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`.

## V1.99.13 — Synthèse budgétaire : prévu / réalisé / écart (C-5)

Nouvel écran **« Synthèse budgétaire »** (`/budget/synthese`, pseudo-page `SYN_Budget`, menu Finances, droits **Financier**). Croise le **prévu (F5, budget prévisionnel)** et le **réalisé (F1, dépenses)** en trois mailles.

- **Prévu** = somme des lignes F5 de la session (Montant = Qté1 × Qté2 × Coût unitaire). **Réalisé** = dépenses F1 (`Montant Depense (KMF)`) **bornées sur la période de la session** (`MOIS_DEBUT_ANNEE_ACAD` = octobre → `AAAA-AAAA` = 01/10/AAAA au 30/09/(AAAA+1)). **Écart = Prévu − Réalisé** (négatif = dépassement, en rouge), **% consommé**.
- **Trois mailles** : (1) par **poste budgétaire** (intitulé depuis P3), (2) par **bailleur** (#26 AFD), (3) par **formation** — **prévu seul** (F1 ne porte pas la formation → réalisé non ventilable, cohérent option B).
- **Filtres** : Session, Formation, Bailleur (drill-down). Tout calculé en Python.
- **Impression** : `/budget/synthese/imprimer` — A4 paysage, en-tête institutionnel UDC/EMSP, trois sections, signatures (Gestionnaire / Directeur EMSP / Visa bailleur).
- Les écarts alimentent les futurs **plans d'action (G1)** (dépassements / sous-consommations).

Lot : `config.py` (VERSION 1.99.13, pseudo-page `SYN_Budget`, `MOIS_DEBUT_ANNEE_ACAD`), `metier.py` (`_bornes_session`, `_f5_prevu_agrege`, `_f1_realise_agrege`, `synthese_budgetaire`, `sessions_budget`), `app.py` (routes `/budget/synthese*`), `templates/budget_synthese.html` + `budget_synthese_print.html`, `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`. **Maître inchangé** (code seul).

## V1.99.14 — Plans d'action dérivés des écarts budgétaires (C-6)

Depuis la **synthèse budgétaire** (`/budget/synthese`), chaque ligne en **écart ≠ 0** (mailles poste et bailleur) reçoit un bouton **« Action »** qui ouvre l'**éditeur du plan d'action** (`/module/G1_Plan_action`) **pré-rempli** par deep-link :

- `Domaine / module` = « Finances / Budget », `Type d'écart` = « Budgétaire », `Axe / thème` = « Finances » ;
- `Écart constaté` = description automatique : *« Poste/Bailleur … — session … : prévu X, réalisé Y, écart Z KMF (dépassement|sous-consommation) »* (« dépassement » si écart < 0, sinon « sous-consommation »).
- Le reste (Action corrective, Responsable, Échéance, Priorité, Statut) se saisit à la main.

**Léger, sans chirurgie** : réutilise le mécanisme de pré-remplissage par deep-link (comme L3_Besoins) et l'éditeur G1 existant. Bouton visible seulement si le rôle peut écrire G1 ; absent à l'impression. **Pas de lien stocké** en V1 (l'écart se recalcule ; l'action vit dans G1 décrite textuellement). Maille formation exclue (pas de réalisé).

Lot : `config.py` (VERSION 1.99.14), `app.py` (pré-remplissage G1 dans la route module + `peut_g1` au contexte synthèse), `templates/budget_synthese.html` (bouton « Action » par ligne en écart), `README.md`, `doc/doc_des_ecrans.md`, `ETAT.md`. **Maître inchangé.**

## V1.99.24 — Lot Menu : libellés (30/06/2026)
Renommages d'écrans dans `config.GUIDE_STRUCTURE` (display only ; clés d'onglet et routes **inchangées**), lot « Menu » de la correction post-revue :
- **BUL_Saisie** : « Saisie façon bulletin (CC + examen) » → **« Saisie façon bulletin (avancé) »** (point 3 : marquer les écrans de notes secondaires « (avancé) », la grille par classe restant l'écran de travail ; `N2_Notes` portait déjà « (avancé) »).
- **E4_Etats_paiement** : « États de paiement (table) » → **« États de paiement (audit) »** (point 9 : l'écran de travail reste « États de paiement (vacations) »).
- **J1_Journal_eleves** / **J2_Journal_compta** : ajout du suffixe **« (lecture seule) »** (point 15 : journaux alimentés uniquement par la clôture).
Aucune chirurgie ZIP, maître inchangé. Reporté (développement, à cadrer TDR) : point 16 (activer Réserver / Voir / Annuler sur la fiche salle).

## V1.99.25 — Homogénéisation consultation / édition (étudiant) (30/06/2026)
Point 4 de la revue : la **fiche étudiant** (`/etudiant`, consultation) reçoit le bouton **« Modifier dans le
module »** (déjà présent sur la fiche enseignant depuis V1.73), qui ouvre le module `A1_Etudiants` positionné
sur la ligne (`?modifier=<matricule>#form-saisie`). Gardé par `peut_modifier and not poste_secondaire` ;
repli lecture seule = bouton « Imprimer la fiche » seul. `etudiant.html` uniquement ; aucune logique nouvelle
(réutilise le sélecteur d'édition générique V1.51). **Point 5 (enseignant) déjà satisfait**. **Point 11
(bailleur) à venir** (nécessite `bailleur.html`, non encore disponible côté chantier).

## V1.99.26 — Homogénéisation consultation / édition (bailleur) (30/06/2026)
Point 11 de la revue : la **fiche bailleur** (`/bailleur`, consultation) voit son bouton d'édition aligné sur
les fiches étudiant et enseignant. L'ancien « Ajouter / modifier » → module F4 **sans positionnement** devient
**« Modifier dans le module »** avec deep-link `url_for('module', onglet='F4_Bailleurs', modifier=<ID bailleur>)#form-saisie`,
qui pré-sélectionne la ligne (logique générique de `module.html` : match exact sur une cellule). Gardé par
`peut_modifier`. `bailleur.html` uniquement, aucune logique nouvelle. **Le lot consultation/édition (4, 5, 11)
est complet** : étudiant (V1.99.25), enseignant (déjà acquis V1.73), bailleur (présent lot).

## V1.99.27 — Vocabulaire : option d'affichage (12B) (30/06/2026)
Point 12 (option 12B retenue, passe d'affichage légère, **aucune modification du classeur**) : uniformisation
des **contrôles de filtre** sur « Bailleur ». L'option d'axe d'inventaire (Impressions & éditions) passe de
« Source de financement (bailleur) » à **« Bailleur »** (`impressions.html`, `value="bailleur"` inchangée) ;
`vue.html` était déjà en « Bailleur ». **Conservés volontairement** (appariement pédagogique AFD ↔ comptabilité) :
les **colonnes du classeur** (« Source de financement / Bailleur », canonique), les **intros/aides** et le **titre
d'édition** « Recettes / dépenses par source de financement ». Pas de chirurgie maître. **Point 12 clos via 12B.**

## V1.99.28 — Indicateur H prévues / H faites (#8) (30/06/2026)
Développement (périmètre TDR : suivi de l'intervention des enseignants + indemnités).
- **Écran « Heures constatées du mois »** : ajout des colonnes **Prévu** (E2 « Vol. horaire prog. »),
  **Fait (calculé)** (A2 × A3 + E3, déjà calculé), **Enregistré (E2)**, et deux écarts de contrôle —
  **Écart prévu − fait** (séances prévues non assurées/non pointées) et **Écart calculé − enregistré**
  (à reporter / divergence : feuille non remplie ou retard de saisie). Lignes en alerte surlignées,
  **ligne de total** en pied. L'aperçu unionne désormais les enseignants calculés et ceux présents dans E2
  du mois, pour faire apparaître les cas « prévu mais 0 fait ». La case **Reporter** n'apparaît que sur les
  lignes réellement calculées (`reportable`) — aucune régression du report (jamais de report d'un 0).
- **Tableau de bord Direction** : encart **« Synthèse des heures »** (Prévu / Enregistré / Écart, + nombre
  d'enseignants en écart), rendu côté serveur (indépendant du JS des KPI), basé sur E2 (toutes périodes).
- **Aucune chirurgie maître** : tout est re-dérivable de l'existant ; le total calculé est figé dans E2 au report.

## V1.99.29 — Lisibilité du pointage (#1) + mode libre marqué avancé (#3) (30/06/2026)
Développement (TDR : suivi de l'intervention des enseignants).
- **#1 — Écran « Saisie des présences par séance »** : la barre d'info de la séance affiche désormais, en plus
  de matière / filière-niveau-section / salle / jour-horaires, l'**année académique**, l'**enseignant programmé**
  (`prog_lbl`) et la **durée** ; une mention rappelle que « ce pointage compte les heures de la séance pour
  l'enseignant (suivi des heures → relevé → paie) ». La **date par défaut = jour courant** (déjà en place).
  `app.py` (passe `annee`) + `presences.html`. Aucune structure nouvelle.
- **#3 — Mode de pointage de référence** : le mode « par séance » reste l'écran de travail ; le mode en liste
  (`PRESL_Libre`) est marqué **« (avancé) »** au menu (`config.py`, display only, clé inchangée).

## V1.99.30 — Impressions : correction écran brut (relevé) + feuille de séance (#2) (30/06/2026)
- **Correction impression brute** : sur l'écran **« Relevé / bulletin »** (`releve.html`, atteint depuis la fiche
  élève), les boutons « Imprimer » faisaient `window.print()` sur la page (sortie brute avec le menu). Ils pointent
  désormais vers l'**édition chartée** `/impressions/bulletin` : relevé de semestre → `releve_print.html`,
  récap annuel → `bulletin_officiel.html`. (Reste à traiter à l'identique : `etat_signalements.html`.)
- **#2 — Feuille de séance imprimable** (`feuille_seance.html`, nouveau ; route `/presences/feuille`) : édition
  **chartée** (logo UDC, `@page` A4, `print.css`) avec en-tête précis (**filière / année / classe / matière /
  enseignant / date / créneau / salle / horaires / durée**), **roster** des étudiants (N° / Matricule / Nom,
  case « Présent » à cocher) et **ligne de signature de l'enseignant** (justificatif des heures). Bouton
  « Imprimer la feuille de séance » sur l'écran de pointage (séance/date/créneau courants).

## V1.99.31 — Impression chartée de l'état des signalements (30/06/2026)
Dernier bouton d'impression brute corrigé : sur **« État des signalements »** (`etat_signalements.html`), le bouton
« Imprimer » (`window.print()` sur l'écran) pointe désormais vers l'**édition chartée** `/etat-signalements/imprimer`
(kind « table » générique : logo UDC, `print.css`, filtres courants conservés). **Plus aucun écran n'imprime en brut.**

## Plan d'action — écran unique (saisie + synthèse) (`/module/G1_Plan_action`) — V1.99.33 (#19)
Regroupement des deux anciens points d'entrée. L'écran de **saisie** du plan d'action affiche désormais
**en tête** la **synthèse** : bandeau KPIs (total / achevées / taux / en retard, via `metier.plan_action_kpis`)
et, si des actions existent, trois graphes repliables (par état, priorité, axe). La saisie / édition / liste
restent dessous (source unique). L'ancienne route `/plan-action/tableau-de-bord` est conservée en **alias**
(redirige vers l'écran unique) ; le template dédié est supprimé. Impression inchangée
(*Impressions › Plan d'action*).

## Aides « quel écran pour quel cas » — V1.99.34 (Lot B)
Notes d'aide in-app clarifiant les écrans voisins : séances (3 vues), heures (relevé vs report), stages (parcours), impressions (hub central), requêtes (croisements multi-onglets), nomenclature (codes/curation/listes), comptes & droits (comptes vs grille des rôles), documents (modèles/bibliothèque/impressions).

## Lot C — déploiement & circuit (points à revoir #10, #11)
- **Salles (L1) — source unique (#10)** : renseigner le référentiel des salles au déploiement. Tant que L1 est vide, le planning dérive les salles des noms présents dans l'inventaire matériel (M1). Aide ajoutée sur l'écran « Salles & équipements ».
- **Circuit dépense → équipement (#11)** : montant, bailleur et référence de pièce d'un équipement viennent de la trésorerie (F1), pas de l'inventaire. Saisir la dépense F1 puis reporter la référence de pièce dans la fiche équipement (M1). Aide ajoutée sur l'écran « Équipements & inventaire ».
