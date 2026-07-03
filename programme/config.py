# -*- coding: utf-8 -*-
"""Configuration de l'interface EMSP V1 — charte, structure du GUIDE, metadonnees.
Aucune logique metier ici : uniquement des constantes de presentation.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- DONNEES PERSISTANTES, SEPAREES DU CODE (V1.53) -----------------------
# Les classeurs (data/) et les secrets locaux (instance/) NE sont PLUS dans le
# dossier programme/. Ils vivent dans un dossier FRERE  donnees/  (a cote de
# programme/), pour qu'une mise a jour = remplacement complet du dossier
# programme/ SANS jamais toucher aux donnees. Surchargeable par la variable
# d'environnement EMSP_DONNEES (ex. pour pointer vers un emplacement protege).
#   kit/
#     programme/   <- ce code (effacable/remplacable en bloc)
#     donnees/     <- data/ + instance/ (jamais ecrases par une mise a jour)
DONNEES_DIR = os.environ.get("EMSP_DONNEES") or os.path.join(os.path.dirname(BASE_DIR), "donnees")
DATA_DIR = os.path.join(DONNEES_DIR, "data")
WORKBOOK = os.path.join(DATA_DIR, "EMSP_V1.xlsx")
# Fichier des NOTES, SEPARE du classeur principal (confidentialite). Au deploiement,
# ce chemin peut pointer vers un emplacement protege distinct (via EMSP_DONNEES).
WORKBOOK_NOTES = os.path.join(DATA_DIR, "EMSP_Notes.xlsx")
ONGLETS_NOTES = ("N1_Bareme_UE", "N2_Notes", "N3_Signalements", "N4_Controles", "N5_Matieres_ND")

# --- Stockage LOCAL hors depot (jamais pousse sur GitHub, jamais dans le zip) ---
# Authentification (empreintes de mots de passe) et journal d'audit : fichiers
# locaux dans donnees/instance/, crees au premier lancement, listes dans .gitignore.
# Le classeur public ne contient QUE les logins + droits (P1_Roles), aucun secret.
INSTANCE_DIR = os.path.join(DONNEES_DIR, "instance")
# Photos d'identite des etudiants : donnees/photos/<matricule>.jpg (hors depot,
# hors zip de code). Absente -> placeholder portrait. Deposees au fil de l'eau.
PHOTOS_DIR = os.path.join(DONNEES_DIR, "photos")
SAUVEGARDES_DIR = os.path.join(DONNEES_DIR, "sauvegardes")  # V1.80 : copies horodatees
# Documents lies aux financements (3b) : donnees/documents/bailleurs/<ID>/ avec un
# index.json par dossier. Le dossier fait foi (bibliotheque). Pas de suppression :
# un document obsolete est marque (statut), jamais efface. Hors depot / hors zip.
DOCUMENTS_DIR = os.path.join(DONNEES_DIR, "documents")
BIBLIOTHEQUE_DIR = os.environ.get("EMSP_BIBLIO") or os.path.join(DONNEES_DIR, "bibliotheque")  # V1.99.22 : magasin de fichiers hors-ligne
DOCS_BAILLEURS_DIR = os.path.join(DOCUMENTS_DIR, "bailleurs")
# --- Attestations de passage (R7a — V1.99.43) ----------------------------
# Dossier "documents etudiants" ou sont rangees les attestations PDF generees,
# par annee : documents/etudiants/<annee>/Attestation_passage_<matricule>.pdf
DOCS_ETUDIANTS_DIR = os.path.join(DOCUMENTS_DIR, "etudiants")
# Delai de contestation apres la deliberation (conseil des professeurs) avant
# que l'attestation devienne imprimable/distribuable (CR 11/06/2026 : une semaine).
DELAI_CONTESTATION_JOURS = 7
# Dates de deliberation par classe+annee : metadonnee de workflow (pas un releve
# academique) -> instance/deliberations.json, hors depot/zip, jamais dans le classeur.
DELIBERATIONS_FILE = os.path.join(INSTANCE_DIR, "deliberations.json")
# En-tete officiel de l'attestation (charte ; modele Word officiel non encore
# fourni -> attestation chartee generique, ajustable a reception du modele).
ATTESTATION_ENTETE = ["UNION DES COMORES", "Universite des Comores",
                      "Ecole de Medecine et de Sante Publique (EMSP)"]
ATTESTATION_LIEU = "Moroni"
ATTESTATION_SIGNATAIRE = "Le Directeur de l'EMSP"
ATTESTATION_SIGNATAIRE_NOM = "Dr. Kamal Ahamada Abdallah"
DOC_BAILLEUR_MAX_OCTETS = 10 * 1024 * 1024            # 10 Mo par piece
DOC_BAILLEUR_EXT = (".pdf", ".jpg", ".jpeg", ".png", ".docx")
P0_TYPES_DOC_BAILLEUR = "Types_doc_bailleur"          # liste P0 des natures de piece
# Photo deposee via la fiche etudiant : JPEG ou PNG, 1 Mo maximum. Enregistree
# sous <matricule>.jpg (nom canonique) ; le vrai type est detecte aux octets
# d'en-tete a l'affichage. Pas de re-encodage (aucune dependance binaire).
PHOTO_MAX_OCTETS = 1024 * 1024
AUTH_FILE = os.path.join(INSTANCE_DIR, "comptes.json")
JOURNAL_FILE = os.path.join(INSTANCE_DIR, "journal.csv")
# --- Mode FORMATION (base de code UNIQUE) ---------------------------------
# Le MEME logiciel tourne en PRODUCTION ou en FORMATION selon la presence d'un
# simple fichier-drapeau local : instance/formation.flag (hors depot, hors zip,
# propre a chaque installation). Present => mode formation (bandeau rouge,
# filigrane "FORMATION" a l'impression, plafond indicatif par onglet en ALERTE
# non bloquante). Absent => production normale. Aucune divergence de code.
def _detecter_formation():
    """Mode formation si le dossier instance/ contient un drapeau 'formation.flag'
    (tolerant : casse indifferente, extension .txt acceptee — piege Windows)."""
    try:
        for nom in os.listdir(INSTANCE_DIR):
            if nom.lower().replace(".txt", "") == "formation.flag" or nom.lower().startswith("formation.flag"):
                return True
    except OSError:
        pass
    return False


MODE_FORMATION = _detecter_formation()
FORMATION_MAX = 50  # plafond indicatif par onglet en formation (alerte, ne bloque pas)

# Mot de passe initial du superadmin au tout premier lancement (a changer aussitot).
SUPERUSER_MDP_DEFAUT = "admin"

# --- Compte FORMATION integre (uniquement en MODE_FORMATION) -------------
# En formation, un compte pret a l'emploi "formation"/"formation" est cree
# automatiquement (sans changement de mot de passe force), avec les memes
# droits qu'un superutilisateur, pour laisser les stagiaires travailler tout
# de suite. Inexistant en production (drapeau absent).
FORMATION_LOGIN = "formation"
FORMATION_MDP_DEFAUT = "formation"

# --- Charte (obligatoire) ---
COULEUR = "#1F4E79"
APP_NOM = "EMSP — Outil de gestion"
APP_SOUS_TITRE = "Ecole de Medecine et de Sante Publique — Union des Comores"
PROJET = "Expertise France / AFD — ODS 21SANOC277"
REFERENCE = "2026/EAALDDDGPLDGDLS/15420 — Webcreatys SAS"
GITHUB = "github.com/webcreatys/emsp"
VERSION = "1.99.52"
LOGO = "img/logo_udc.jpg"   # logo Universite des Comores (vendore, aucun CDN)

# --- Paie des vacations (Bloc 3, V1.99.3) ----------------------------------
# Taux horaire par defaut (KMF/h) applique quand E1[Taux horaire (KMF/h)] est
# vide. Override possible par enseignant dans E1. Reference EMSP : 5 750 KMF/h.
TAUX_HORAIRE_DEFAUT = 5750
MODES_REMUNERATION = ["Horaire", "Forfait mensuel"]
STATUTS_ETAT_PAIEMENT = ["Brouillon", "Arrete", "Passe en compta"]
SEMESTRES_PAIE = ["S1", "S2"]
# Poste budgetaire de depense pour le passage en compta des vacations.
# Defaut V1.99.52 (P1-C) : 642 (nomenclature EMSP) — le gestionnaire peut
# toujours choisir un autre poste au moment du passage en compta.
POSTE_DEPENSE_VACATIONS = "642 — Cours complémentaires (heures supplémentaires)"

# --- Passage conditionnel (decision annuelle, V1.90) ----------------------
# Ecart de credits annuels = ECTS requis (somme des UE du niveau, 2 semestres)
# moins ECTS acquis. Decision : ecart 0 -> Admis ; 1..SEUIL -> Admis
# conditionnel ; > SEUIL -> Ajourne. Seuil PARAMETRABLE (l'EMSP peut l'ajuster).
# Defaut SURCHARGEABLE via instance/reglages.json (cle "seuil_passage_conditionnel"),
# editable a l'ecran sur N1_Bareme_UE (metier.seuil_passage / definir_seuil_passage).
SEUIL_PASSAGE_CONDITIONNEL = 5

# --- Calendrier / planning (vues facon Outlook) ---
# Emploi du temps HEBDOMADAIRE recurrent : A3_Sessions porte un Jour (Lun..Sam),
# pas de date calendaire. Les vues mois/semaine/jour PROJETTENT cette grille.
JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
JOURS_PLEINS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
CRENEAUX = ["10h", "12h", "15h", "17h"]   # creneaux de presence (A2_Presences)
CAL_HEURE_MIN = 7    # bornes de l'axe horaire des grilles facon Outlook
CAL_HEURE_MAX = 18

# Types de salle proposes a l'edition de la fiche salle (L1_Salles, colonne Type).
# Liste canonique alignee sur les valeurs reellement presentes en base ; la fiche
# fusionne cette liste avec les types deja saisis pour ne jamais perdre une valeur.
TYPES_SALLE = ["Cours", "TP", "Spécialisée", "Bureau", "Divers"]
# V1.99.32 — types de reservation de salle (L2). « Cours / seance » = lien planning A3.
TYPES_RESERVATION = ["Reunion", "Examen", "Formation", "Evenement", "Cours / seance", "Autre"]
STATUTS_RESERVATION = ["Demandee", "Confirmee", "Annulee"]

# Lignes du classeur : 1 = titre, 2 = en-tetes, 3+ = donnees
LIGNE_ENTETES = 2
LIGNE_DONNEES = 3

# --- Provenance des champs (code couleur des documents) ---
# (sans marqueur) = TDR (noir) ; (*) = initiative Webcreatys (bleu/★) ; (**) = hors TDR (rouge/★)
PROVENANCE = {
    "TDR": {"code": "TDR", "libelle": "Exige par le TDR", "classe": "prov-tdr", "etoile": False},
    "*":   {"code": "*",   "libelle": "Initiative Webcreatys", "classe": "prov-init", "etoile": True},
    "**":  {"code": "**",  "libelle": "Ajout EMSP hors TDR", "classe": "prov-hors", "etoile": True},
}

# Colonnes calculees (formules) : protegees, jamais saisies par l'IHM
READONLY_COLS = {
    "E2_Releve_heures": ["Total heures a payer (*)"],
    "F2_Comptes": ["Solde courant (KMF) (*)"],
    "F4_Bailleurs": ["Documents lies (*)"],   # compteur auto (3c), non saisissable
    # E4_Etats_paiement[Montant (KMF)] : calcule en Python (h. autorisees x taux,
    # ou mois x cout), ecrit comme VALEUR -> pas en READONLY (sinon blanchi, l'onglet
    # etant vide il n'existe aucune formule modele a propager).
    "IMPORT_zone": ["Statut vs base (*)"],
    # TDB_Direction et Dictionnaire sont entierement en lecture seule
}

# Onglets entierement en lecture seule (pas d'edition IHM)
READONLY_TABS = {"TDB_Direction", "Dictionnaire", "Legende", "Guide"}

# --- Capacite des onglets (ecriture V1.2) ---
# Les formules d'agregat et de colonnes calcul du classeur sont harmonisees sur
# cette borne unique (plus de plafond incoherent 300/5000). La couche d'ecriture
# recopie en plus le motif de formule dans chaque nouvelle ligne : aucune limite
# par ligne. CAPACITE sert d'ultime garde-fou + seuil d'alerte dans l'IHM.
CAPACITE = 50000
ALERTE_CAPACITE_RATIO = 0.9   # bandeau d'alerte au-dela de 90 % de CAPACITE

# --- Matrice des droits : groupes de modules (P1_Roles) -> onglets ---
# Les colonnes "Modules lecture/ecriture" de P1_Roles emploient des groupes.
# Ce mapping les traduit en onglets concrets. Le groupe special "Tous" = Direction
# = tous les onglets editables (y compris ceux reserves a la Direction ci-dessous).
MODULES_ONGLETS = {
    "Academique":  ["A1_Etudiants", "A3_Sessions", "A4_Documents_etud", "L1_Salles"],
    "Presences":   ["A2_Presences", "E3_Seances_faites"],
    "Stages":      ["S1_Stages", "S2_Lieux_stage"],
    "Notes":       ["N1_Bareme_UE", "N2_Notes", "N3_Signalements", "N4_Controles"],
    "Enseignants": ["E1_Enseignants", "E2_Releve_heures"],
    "Financier":   ["F1_Mouvements", "F2_Comptes", "F3_Budget_poste", "F5_Budget_Prev", "F4_Bailleurs", "E4_Etats_paiement"],
    "Logistique":  ["L2_Reservations", "M1_Equipements", "L3_Besoins"],
}
# Onglets reserves a la Direction (groupe "Tous") : parametrage, droits, pilotage.
ONGLETS_DIRECTION = ["P0_Parametres", "P1_Roles", "G1_Plan_action",
                     "H1_Biblio_docs", "IMPORT_zone", "D1_Modeles_docs",
                     "J1_Journal_eleves", "J2_Journal_compta", "P2_Taux",
                     "P3_Nomenclature"]
# Onglets qui exigent en plus "Acces financier = O".
ONGLETS_FINANCIERS = ["F1_Mouvements", "F2_Comptes", "F3_Budget_poste", "F5_Budget_Prev", "F4_Bailleurs", "E4_Etats_paiement"]

# --- V1.69 : suivi des droits d'inscription par etudiant ---
# Poste budgetaire recette (nomenclature 706) selon le niveau courant de l'etudiant.
# Sert a la fois au filtre du "Paye" (par code prefixe) et au pre-remplissage du
# mouvement F1 a l'encaissement. La pre-inscription (706a) et la formation continue
# (706e) sont HORS de ce suivi (frais distincts).
POSTE_INSCRIPTION_PAR_NIVEAU = {"L1": "706b", "L2": "706c", "L3": "706d"}

# --- C-4 (V1.99.12) : budget previsionnel par formation -----------------------
# Valeurs par defaut SURCHARGEABLES via instance/reglages.json (cles "taux_eur" et
# "frais_admin_pct"), modifiables sans toucher au code (metier._reglage_get).
TAUX_EUR_DEFAUT = 491.967       # 1 EUR = 491,967 KMF (parite fixe)
FRAIS_ADMIN_PCT_DEFAUT = 5.0    # frais administratifs EMSP (% du total par niveau)

# C-5 (V1.99.13) : 1er mois de l'annee academique (octobre a l'EMSP). Sert a borner
# le realise F1 (annee civile) sur la plage de la session F5 pour l'ecart prevu/realise.
MOIS_DEBUT_ANNEE_ACAD = 10

# --- V1.71 : filtrage multicritere + impression de selection ---------------
# Pour chaque critere, table {onglet -> colonne support}. Un onglet ne reagit a
# un critere QUE s'il y figure ici (sinon le critere est ignore pour cet onglet
# et le controle correspondant est masque dans l'IHM). Les noms de colonnes sont
# donnes en libelle PROPRE (sans marqueur (*)/(**)) ; metier normalise par
# securite. Le marqueur d'origine est rappele en commentaire.
COLONNE_FILIERE_PAR_ONGLET = {
    "A1_Etudiants":    "Filiere",
    "A3_Sessions":     "Filiere",
    "F3_Budget_poste": "Filiere",            # source : "Filiere (*)"
    "F5_Budget_Prev":  "Formation",          # source : "Formation (*)"
}
COLONNE_NIVEAU_PAR_ONGLET = {
    "A1_Etudiants":    "Niveau",
    "A3_Sessions":     "Niveau",
    "S2_Lieux_stage":  "Niveau concerne",    # source : "Niveau concerne (*)"
}
COLONNE_ANNEE_PAR_ONGLET = {
    "A1_Etudiants":      "Annee acad.",       # source : "Annee acad. (*)"
    "A3_Sessions":       "Annee acad.",       # source : "Annee acad. (*)"
    "A4_Documents_etud": "Annee concernee",   # source : "Annee concernee (**)"
    "S1_Stages":         "Annee acad.",       # source : "Annee acad. (*)"
    "E2_Releve_heures":  "Mois / Annee",      # source : "Mois / Annee (*)"
    "F1_Mouvements":     "Annee academique",  # source : "Annee academique (*)"
    "F3_Budget_poste":   "Exercice",
    "F5_Budget_Prev":    "Session",
    "E4_Etats_paiement": "Annee academique",
}
# Colonne date de reference pour le filtre periode (du-au).
COLONNE_DATE_PAR_ONGLET = {
    "A1_Etudiants":      "Date inscription",
    "A2_Presences":      "Date",              # source : "Date (**)"
    "A4_Documents_etud": "Date generation",   # source : "Date generation (**)"
    "S1_Stages":         "Date debut",        # source : "Date debut (*)"
    "F1_Mouvements":     "Date operation",
    "H1_Biblio_docs":    "Date de mise a jour", # source : "Date de mise a jour (**)"
    "L2_Reservations":   "Date",              # source : "Date (**)"
    "M1_Equipements":    "Date d'acquisition", # source : "Date d'acquisition (**)"
    "L3_Besoins":        "Date d'expression",  # source : "Date d'expression (**)"
    "E3_Seances_faites": "Date",              # source : "Date (*)"
    "P2_Taux":           "Date d'effet",
    "E4_Etats_paiement": "Date arrete",
}
# Onglets sans colonne filiere/niveau propre : on resout depuis A1 via le
# Matricule a la lecture (enrichissement valide, option i V1.71).
ONGLETS_ENRICHIS_PAR_MATRICULE = ("A2_Presences", "S1_Stages")


# --- Administration des droits (V1.13) ---
# SUPERUTILISATEUR(S) : login(s) reserve(s) garantis DANS LE CODE. Ils ont
# toujours l'acces total + le droit d'administrer les droits, MEME si P1_Roles
# est vide, casse ou mal configure. Ils ne peuvent etre ni supprimes ni
# retrogrades depuis l'interface. C'est le FILET ANTI-BLOCAGE ultime : il est
# donc impossible de se verrouiller hors de l'application.
# >>> Pour renommer le superutilisateur, modifier la valeur ci-dessous (un seul
#     endroit). Plusieurs superutilisateurs possibles : ["superadmin", "webcreatys"].
SUPERUSER_LOGINS = ["superadmin"] + (["formation"] if MODE_FORMATION else [])

# Groupes de droits assignables dans l'ecran d'administration (cases a cocher).
# "Tous" = acces Direction complet (tous les onglets, y compris parametrage).
GROUPES_DROITS = list(MODULES_ONGLETS.keys())          # Academique, Presences, ...
GROUPE_TOUS = "Tous"

# --- Roles-modeles (V1.74) : profils types pre-remplissant les cases de droits
# dans l'ecran Comptes & acces. Un modele n'est qu'un POINT DE DEPART : apres
# l'avoir applique, l'admin peut DECOCHER pour donner moins (ex. assistant
# comptable en lecture seule) ou cocher pour donner plus (ex. gestionnaire), par
# UTILISATEUR. Les droits reels restent stockes par login dans P1_Roles. Editable
# ici sans toucher au classeur ; ajustable en direct compte par compte a l'usage.
GROUPES_DROITS_LIBELLES = {
    "Academique":  "Eleves & scolarite",
    "Presences":   "Presences",
    "Stages":      "Stages",
    "Notes":       "Notes & bulletins",
    "Enseignants": "Enseignants & heures",
    "Financier":   "Finances",
    "Logistique":  "Logistique / moyens",
}
ROLES_MODELES = [
    {"id": "direction", "libelle": "Direction",
     "lecture_tous": True, "ecriture_tous": True, "financier": True, "admin": True,
     "lecture": [], "ecriture": []},
    {"id": "scolarite", "libelle": "Scolarite",
     "lecture": ["Academique", "Stages", "Notes", "Enseignants"],
     "ecriture": ["Academique", "Stages", "Notes"],
     "lecture_tous": False, "ecriture_tous": False, "financier": False, "admin": False},
    {"id": "compta", "libelle": "Comptabilite",
     "lecture": ["Academique", "Financier"], "ecriture": ["Financier"],
     "lecture_tous": False, "ecriture_tous": False, "financier": True, "admin": False},
    {"id": "chef_dept", "libelle": "Chef de departement",
     "lecture": ["Academique", "Enseignants", "Notes", "Presences"],
     "ecriture": ["Presences", "Enseignants", "Notes"],
     "lecture_tous": False, "ecriture_tous": False, "financier": False, "admin": False},
    {"id": "enseignant", "libelle": "Enseignant / vacataire (consultation)",
     "lecture": ["Enseignants"], "ecriture": [],
     "lecture_tous": False, "ecriture_tous": False, "financier": False, "admin": False},
    {"id": "logistique", "libelle": "Logistique / moyens generaux",
     "lecture": ["Logistique"], "ecriture": ["Logistique"],
     "lecture_tous": False, "ecriture_tous": False, "financier": False, "admin": False},
]

# Palette de couleurs d'identite utilisateur (poste partage) : chaque compte
# recoit une couleur distincte (affichee en haut). Choix definitif par l'informatique
# a la creation du compte (lot a venir) ; par defaut, derivee du login.
COULEURS_UTILISATEUR = ["#1F4E79","#1B7F5C","#9A4D00","#7A3E9D","#A11D33",
                        "#0E6B7A","#5A6B00","#B0306E","#3A4AA0","#8A5A00"]

# --- Gouvernance des comptes (V1.43) ---
# Grande rubrique d'appartenance d'un compte (bucket organisationnel, distinct
# des droits par module de P1_Roles). Editable ici. Stockee dans instance/comptes.json
# (hors depot), comme la couleur choisie et la validite — le classeur reste inchange.
RUBRIQUES = ["Direction", "Scolarite", "Comptabilite",
             "Enseignants / Departements", "Logistique", "Informatique"]

# Mot de passe initial : genere ALEATOIREMENT par le responsable informatique a la
# creation et a la reinitialisation, affiche UNE seule fois en clair, a changer au
# 1er login. Alphabet sans caracteres ambigus (pas de O/0/l/1/I).
MDP_LONGUEUR = 8
MDP_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"

# Fin de validite d'un compte = fin de l'annee SCOLAIRE (Comores : octobre -> juillet),
# soit le 31/07. Expiration NON bloquante : le compte reste utilisable, un bandeau
# "a renouveler" s'affiche, et l'informatique peut "Renouveler (annee scolaire)".
ANNEE_SCOLAIRE_FIN_MOIS = 7
ANNEE_SCOLAIRE_FIN_JOUR = 31

# --- Cloture / archivage / passation (V1.44) ---
# Repertoire des archives generees a la cloture (cree au besoin ; hors classeur actif).
ARCHIVES_DIR = os.path.join(BASE_DIR, "archives")
# Eleves sortis : conserves dans A1_Etudiants ~N ans, puis archivables (deplacement physique).
ANNEES_GARDE_ELEVES = 3
# Statuts qui marquent une SORTIE d'eleve (journalisation a la cloture). Comparaison
# insensible a la casse et aux accents (cf. metier._norm). Tout autre statut = encore actif.
STATUTS_SORTIE = ["Diplome", "Abandonne", "Radie"]
# Mentions (decret Universite des Comores, art. 15) — saisie a la cloture (option (b)).
MENTIONS = ["Passable", "Assez bien", "Bien", "Tres bien"]


# Onglets dont la SAISIE de lignes est activee dans l'IHM (deploiement incremental).
# Les autres onglets restent en lecture seule tant que leurs champs ne sont pas valides.
ONGLETS_SAISIE_ACTIVE = ["A1_Etudiants", "A3_Sessions", "A4_Documents_etud", "S1_Stages",
                         "S2_Lieux_stage",
                         "E1_Enseignants", "E2_Releve_heures", "L1_Salles", "F1_Mouvements",
                         "F2_Comptes", "L2_Reservations", "M1_Equipements",
                         "N1_Bareme_UE", "N2_Notes", "N3_Signalements", "N4_Controles", "H1_Biblio_docs",
                         "G1_Plan_action", "L3_Besoins", "F3_Budget_poste", "P2_Taux",
                         "F4_Bailleurs", "P3_Nomenclature"]

# Onglets ou l'EDITION EN PLACE d'une ligne existante est proposee (sous-ensemble de
# ONGLETS_SAISIE_ACTIVE). La saisie (ajout) reste ouverte sur tous les onglets ci-dessus ;
# seule la CORRECTION d'une ligne deja enregistree est restreinte ici.
# Principe : donnees de reference / champs de workflow = correction en place naturelle ;
# JOURNAL FINANCIER = append-only (une erreur se corrige par une ecriture rectificative,
# jamais en reecrivant la ligne) -> exclu pour la tracabilite (contexte audit AFD).
# Pour durcir davantage, ajouter un onglet a ONGLETS_SANS_EDITION_LIGNE (ex. F2_Comptes,
# N3_Signalements). Chaque modification reste de toute facon journalisee et soumise au
# controle de droit d'ecriture par role (metier.peut_ecrire).
ONGLETS_SANS_EDITION_LIGNE = ("F1_Mouvements",)
ONGLETS_EDITION_LIGNE = [t for t in ONGLETS_SAISIE_ACTIVE
                         if t not in ONGLETS_SANS_EDITION_LIGNE]

# Valeurs PAR DEFAUT proposees dans le formulaire generique (par onglet, par libelle
# de champ propre). "@today" => date du jour au format JJ/MM/AAAA (charte). L'agent
# peut toujours modifier. Resolu par metier.champs_saisie().
SAISIE_DEFAUTS = {
    "N1_Bareme_UE": {
        # A la saisie manuelle d'un bareme, on est provisoire par defaut : le coef
        # n'est confirme (Oui) qu'une fois aligne sur un document de reference officiel.
        # Coef matiere pre-rempli a 1 (moyenne d'UE arithmetique = modele officiel).
        "Coef confirme": "Non",
        "Coef matiere": "1",
    },
    # Saisie etudiants : on saisit par MATRICULE ; le n° d'ordre est pre-suggere
    # (prochain libre) et reste modifiable. Le contexte (filiere/niveau/section/
    # annee/statut) se reporte de la derniere ligne pour la saisie en serie.
    "A1_Etudiants": {
        "N ordre": "@next_ordre",
        "Filiere": "@last",
        "Niveau": "@last",
        "Section": "@last",
        "Annee acad.": "@last|2025-2026",
        "Statut": "@last|Inscrit",
    },
    # Saisie des notes en serie : d'un etudiant a l'autre, seuls Matricule et la note
    # changent. Le token "@last" reporte la DERNIERE valeur saisie de la colonne (lue
    # dans le classeur) ; "@last|<repli>" donne la valeur de depart quand l'onglet est
    # vide. Le repli peut etre un token (@today). Resolu par metier.champs_saisie().
    "N2_Notes": {
        "Annee acad.": "@last|2025-2026",
        "Session": "@last|1",
        "Semestre": "@last",
        "N° UE": "@last",
        "Matiere": "@last",
    },
    "N4_Controles": {
        "Annee acad.": "@last|2025-2026",
        "Session": "@last|1",
        "Semestre": "@last",
        "N° UE": "@last",
        "Matiere": "@last",
        "N° de controle": "@last|1",
        "Date": "@last|@today",
        "Coef": "@last|1",
    },
    "A4_Documents_etud": {
        "Date generation": "@today",
        "Statut": "En attente conseil",
    },
    "S1_Stages": {
        "Fiche retour (O/N)": "N",
        "Session": "Normale",
    },
    "E1_Enseignants": {
        # Pre-suggere le prochain matricule provisoire libre "NC-<n>" (Non Connu)
        # quand l'enseignant/vacataire n'a pas (encore) de matricule officiel.
        # Resolu dynamiquement par metier.champs_saisie (scan de E1, max + 1).
        # Modifiable a la saisie : taper le vrai matricule s'il existe.
        "Matricule ens.": "@next_nc",
    },
    "L1_Salles": {
        # Pre-suggere le prochain identifiant de salle libre "SAL-<n>" (cohérence,
        # pas de collision). Modifiable a la saisie : les salles ont des noms
        # explicites (champ Nom / libelle), l'ID reste une cle courte.
        "ID salle": "@next_sal",
    },
    "F1_Mouvements": {
        "Date operation": "@today",
    },
    "L2_Reservations": {
        "ID reservation": "@next_res",
        "Date": "@today",
        "Statut": "Demandee",
    },
    "M1_Equipements": {
        "ID equipement": "@next_eq",
        "Date d'acquisition": "@today",
        "Etat": "Actif",
    },
    "L3_Besoins": {
        "ID besoin": "@next_bes",
        "Date d'expression": "@today",
        "Statut": "Exprimé",
    },
}

# Largeur de saisie (en CARACTERES) par champ, pour des formulaires compacts :
# chaque champ est dimensionne a son nombre de caracteres utile (V1.60). Cle =
# libelle propre. Defaut par type si absent (cf. metier.champs_saisie). Une valeur
# ici prime sur le calcul automatique (selects = largeur de la plus longue option).
LARGEURS_CHAMPS = {
    # Identite A1 (saisie sur une seule ligne)
    "N ordre": 6, "Matricule": 10, "Genre": 4, "Nom": 18, "Prenom": 18,
    "Date naissance": 12, "Lieu naissance": 22, "Origine / lieu actuel": 22,
    "Niveau": 7, "Filiere": 18, "Section": 7, "Annee acad.": 12,
    "Statut": 16, "Date inscription": 12,
    # Barème N1
    "N° UE": 8, "Intitule UE": 30, "Matiere": 28, "Coef matiere": 8, "Coef UE": 8,
    "ECTS UE": 8, "Coef confirme": 8, "Semestre": 8,
    # Notes N2 / Contrôles N4
    "Session": 7, "CC": 7, "Examen": 8, "N° de controle": 10, "Note /20": 8, "Coef": 6,
    # Signalements N3
    "Date": 12, "Contexte": 12, "Emis par - fonction": 18, "Nom de l'emetteur": 20,
    "Motif": 32, "Annee acad. ": 12,
}

# Champs AUTO-remplis cote serveur (jamais saisis a la main) : "Saisi par" recoit
# le login du role courant a l'enregistrement (tracabilite). Exclus du formulaire
# par metier.champs_saisie ; injectes par app.module_ajouter. Cle = libelle propre.
CHAMPS_AUTO_LOGIN = {
    "F1_Mouvements": ["Saisi par"],
    "L2_Reservations": ["Saisi par"],
    "M1_Equipements": ["Saisi par"],
    "L3_Besoins": ["Saisi par"],
    "N4_Controles": ["Saisi par"],
    "F3_Budget_poste": ["Saisi par"],
    "F4_Bailleurs": ["Saisi par"],
    "E4_Etats_paiement": ["Arrete par"],
}

# Onglets dont la saisie passe par un ECRAN DEDIE (et non le formulaire generique).
# Cle = onglet, valeur = nom de la route Flask. A2_Presences : saisie PAR LOT / PAR SEANCE
# (cocher la classe issue de A1 pour une seance A3 + date + creneau). Choix V1.4 acte :
# saisie de masse realiste, hors-TDR assumee (champs (**), issue du CR du 11/06).
ONGLETS_SAISIE_LOT = {
    "A2_Presences": "presences_saisie",
}

# Options de listes "en dur" (hors P0_Parametres) referencees par le Dictionnaire.
LISTES_INLINE = {
    "Sessions": ["1", "2"],
    "Haute/Moyenne/Basse": ["Haute", "Moyenne", "Basse"],
    "Court/Moyen/Long terme": ["Court terme", "Moyen terme", "Long terme"],
    "Contextes signalement": ["Examen", "Cours", "Stage", "Autre"],
    "Fonctions signalement": ["Surveillant", "Enseignant", "Scolarite", "Chef de departement"],
    "Semestres cursus": ["1", "2", "3", "4", "5", "6"],
    "Lundi..Samedi": JOURS_SEMAINE,
    "10h/12h/15h/17h": CRENEAUX,
    "O/N": ["O", "N"],
    "Oui/Non": ["Oui", "Non"],
    "Titulaire/Vacataire": ["Permanent", "Vacataire", "Contractuel", "Bénévole"],
    "Horaire/Forfait": ["Horaire", "Forfait mensuel"],
    "Etat paiement": ["Brouillon", "Arrete", "Passe en compta"],
    "Semestre S1/S2": ["S1", "S2"],
    "Recette/Depense": ["Recette", "Depense"],
    "Session stage": ["Normale", "Rattrapage"],
    "Previsionnel/Realise": ["Previsionnel", "Realise"],
    "Banque/Caisse/Autre": ["Banque", "Caisse", "Autre"],
    "Reunion/Examen/Evenement/Partenaire/Autre": ["Reunion", "Examen", "Evenement", "Partenaire", "Autre"],
    "Demandee/Confirmee/Annulee": ["Demandee", "Confirmee", "Annulee"],
    "En service/HS/Reforme": ["En service", "HS", "Reforme"],
    "Assuree/Cours annule": ["Assuree", "Cours annule"],
    "Sens budgetaire": ["Recette", "Depense", "Investissement"],
    "Niveau nomenclature": ["Chapitre", "Article", "Sous-article"],
    "Source code": ["OHADA", "EMSP"],
    "Niveaux budget": ["M1", "M2", "L1", "L2", "L3"],
}

# Listes alimentees par une COLONNE D'UN AUTRE ONGLET DE DONNEES (lien inter-onglets).
# Le Dictionnaire (colonne "Liste / source") emploie le libelle lisible ; ce mapping
# le traduit en (onglet, en-tete propre). Resolu par metier.options_liste() en valeurs
# distinctes non vides. Extension V1.4 : fiabilise les cles de jointure (ex. Matricule,
# ID session) sans saisie libre.
LISTES_ONGLET = {
    "Etudiants inscrits (A1)": ("A1_Etudiants", "Matricule"),
    "Seances (A3)":            ("A3_Sessions", "ID session"),
    # Lien Seance -> Salle (V1.11) : A3 'Salle' propose les salles reelles de L1
    # (par leur nom explicite). Optionnel ; le rattachement au planning matche par
    # nom OU id (metier._seance_dans_salle), donc stocker le nom suffit et reste lisible.
    "Salles (L1)":             ("L1_Salles", "Nom / libelle"),
    "Comptes_caisses":         ("F2_Comptes", "Nom du compte / caisse (*)"),
}

# Listes alimentees par PLUSIEURS colonnes d'un autre onglet, presentees comme un
# LIBELLE COMPOSITE lisible (lien lisible). Valeur = (onglet, [colonnes_brutes], separateur).
# Resolu par metier.options_liste() : libelles distincts non vides, tries.
# Lien Seances <-> formateurs (V1.8) : A3 'Enseignant' propose les enseignants reels
# de E1 sous la forme "Nom Prenom" (plus de saisie libre => plus de fautes de frappe).
# Choix V1 : on STOCKE le libelle lisible (le calendrier et les salles l'affichent tel
# quel) ; le matricule reste la cle de E2 (heures), independamment.
LISTES_ONGLET_COMPOSITE = {
    "Enseignants (E1)": ("E1_Enseignants", ["Nom", "Prenom"], " "),
    # Lieu de stage (V1.28) : S1 'Lieu de stage' propose les unites d'accueil du
    # referentiel S2 sous la forme lisible "Lieu / structure — Service" (Service
    # facultatif : si vide, seul le lieu est affiche). On STOCKE ce libelle composite
    # dans S1 ; c'est aussi la cle de rapprochement pour le suivi des quotas.
    "Lieux de stage (S2)": ("S2_Lieux_stage", ["Lieu / structure (*)", "Service (*)"], " — "),
}

# Listes ou le LIBELLE AFFICHE differe de la VALEUR STOCKEE (option value != label).
# Valeur = (onglet, colonne_valeur_stockee, [colonnes_libelle_complementaires]).
# Le libelle affiche = "<valeur> — <colonnes complementaires jointes>".
# Resolu par metier.options_liste() en liste de {value, label}.
# Lien E2 -> E1 (V1.9, choix (b2)) : A la saisie d'un releve d'heures, on choisit
# l'enseignant via "Matricule — Nom Prenom" (lisible) mais on STOCKE le matricule
# seul (cle du releve de paie et de l'agregat "heures par enseignant").
LISTES_ONGLET_VALLABEL = {
    "Enseignants matricule (E1)": ("E1_Enseignants", "Matricule ens.", ["Nom", "Prenom"]),
    "Equipements (M1)": ("M1_Equipements", "ID equipement (*)", ["Designation (**)"]),
}

# Variante FILTREE de VALLABEL (V1.99.10) : meme rendu "valeur — libelle", mais ne
# retient que les lignes dont une (ou plusieurs) colonne(s)-filtre valent une valeur
# donnee. Sert a ne proposer que les codes budgetaires ACTIFS de P3_Nomenclature.
# Forme du filtre (resolu par metier.options_liste) :
#   - 5-uplet : (onglet, col_valeur, [col_libelle], col_filtre, valeur_filtre)  -> 1 critere
#   - 4-uplet : (onglet, col_valeur, [col_libelle], [(col, val), ...])          -> N criteres ET
LISTES_ONGLET_VALLABEL_FILTRE = {
    "Codes budgétaires actifs (P3)": ("P3_Nomenclature", "Code", ["Intitule"], "Actif", "Oui"),
    # C-4b (V1.99.12) : budget previsionnel F5 -> seulement les codes ACTIFS de Sens
    # Depense (un budget previsionnel ne contient que des depenses).
    "Codes depense actifs (P3)": ("P3_Nomenclature", "Code", ["Intitule"],
                                  [("Actif", "Oui"), ("Sens", "Depense")]),
}

# Champs en SUGGESTIONS génériques (datalist) peuplées côté client par un script
# dédié à l'onglet (V1.32). Cle = onglet -> {libelle propre: id datalist}. Utilisé en
# complément de MAQUETTE_DATALIST (A3). Saisie libre conservée (suggestions).
CHAMPS_DATALIST = {
    "N2_Notes": {"N° UE": "dl_ue_N2", "Matiere": "dl_mat_N2"},
}

# Ergonomie de saisie clavier (V1.99.4). metier.champs_saisie classe chaque champ
# LISTE en un "saisie_mode" lu par static/js/saisie_clavier.js :
#   - "touche" : valeurs courtes fixes (LISTES_INLINE) -> 1 frappe = 1 choix + focus
#                automatique au champ suivant (insensible casse/accents ; cycle si
#                deux libelles partagent l'initiale).
#   - "auto"   : referentiels longs (LISTES_ONGLET*, value != label) -> autocomplete
#                "code - intitule" greffe sur un <select> natif conserve en filet de
#                securite si JS off (Lot B).
#   - "normal" : champ non concerne (rendu inchange).
# Regle par defaut appliquee dans champs_saisie : value==label, libelles courts et
# <= MAX_OPTS_TOUCHE options -> "touche" ; value!=label OU > SEUIL_AUTOCOMPLETE -> "auto".
# MODE_SAISIE_LISTE force un mode par NOM DE LISTE (libelle de la colonne
# "Liste / source" du Dictionnaire) pour deroger sans toucher au JS ni a la regle.
MAX_OPTS_TOUCHE = 6
SEUIL_AUTOCOMPLETE = 8
MODE_SAISIE_LISTE = {
    # Overrides explicites (vides par defaut ; exemples) :
    # "Recette/Depense": "touche",
    # "Comptes_caisses": "auto",
}

# Dictionnaire COMPLEMENTAIRE pour les onglets ajoutes par chirurgie du zip dont les
# entrees ne figurent pas (encore) dans l'onglet Dictionnaire du classeur. Evite de
# modifier une feuille existante du classeur. Cles normalisees identiques a l'onglet
# Dictionnaire : Onglet, Champ, Type, Obligatoire, Provenance, Liste, Description.
# Fusionne par metier.dictionnaire_par_onglet().
DICTIONNAIRE_SUPPLEMENT = {
    # Bloc 3 (V1.99.3) : etats de paiement des vacations (onglet ajoute par chirurgie).
    "E4_Etats_paiement": [
        {"Onglet": "E4_Etats_paiement", "Champ": "ID etat", "Type": "Texte", "Obligatoire": "Oui", "Provenance": "TDR", "Liste": "-", "Description": "Identifiant de l'etat (PAIE-<annee>-<semestre>). Cle avec Matricule."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Semestre", "Type": "Liste", "Obligatoire": "Oui", "Provenance": "TDR", "Liste": "Semestre S1/S2", "Description": "Semestre couvert (S1 / S2)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Annee academique", "Type": "Texte", "Obligatoire": "Oui", "Provenance": "TDR", "Liste": "-", "Description": "Annee academique (AAAA-AAAA)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Statut etat", "Type": "Liste", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "Etat paiement", "Description": "Brouillon / Arrete / Passe en compta."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Date arrete", "Type": "Date", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Date d'arrete de l'etat (JJ/MM/AAAA)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Arrete par", "Type": "Texte", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Utilisateur ayant arrete l'etat (auto)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Ref ecriture F1", "Type": "Texte", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Reference de l'ecriture de depense en tresorerie (PAIE-...)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Matricule ens.", "Type": "Liste", "Obligatoire": "Oui", "Provenance": "TDR", "Liste": "Enseignants matricule (E1)", "Description": "Enseignant paye. Cle avec ID etat."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Nom-Prenom", "Type": "Texte", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Nom-Prenom de l'enseignant (repris de E1)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Statut prof.", "Type": "Liste", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "Titulaire/Vacataire", "Description": "Statut professionnel (Permanent / Vacataire / Contractuel / Benevole)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Mode remuneration", "Type": "Liste", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "Horaire/Forfait", "Description": "Horaire ou Forfait mensuel."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Matiere enseignee", "Type": "Texte", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Matiere(s) enseignee(s) (facultatif)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Niveau", "Type": "Texte", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Niveau concerne (facultatif)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Heures prevues", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Heures programmees sur la periode (somme E2)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Heures effectuees", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Heures constatees sur la periode (somme E2)."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Heures autorisees a payer", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Plafond paye (<= effectuees), valide par le gestionnaire."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Taux horaire (KMF/h)", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Taux applique (KMF/h) en mode Horaire."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Mois (forfait)", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Nombre de mois en mode Forfait mensuel."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Cout mensuel (KMF)", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Cout mensuel (KMF) en mode Forfait."},
        {"Onglet": "E4_Etats_paiement", "Champ": "Montant (KMF)", "Type": "Nombre", "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-", "Description": "Montant calcule : heures autorisees x taux, ou mois x cout."},
    ],
    "E3_Seances_faites": [
        {"Onglet": "E3_Seances_faites", "Champ": "Date", "Type": "Date",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Date reelle de la seance (JJ/MM/AAAA). Cle avec Session + Creneau."},
        {"Onglet": "E3_Seances_faites", "Champ": "Session / Matiere", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Seances (A3)",
         "Description": "ID de la seance du planning A3. Cle avec Date + Creneau."},
        {"Onglet": "E3_Seances_faites", "Champ": "Creneau", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "10h/12h/15h/17h",
         "Description": "Creneau de la seance. Cle avec Date + Session."},
        {"Onglet": "E3_Seances_faites", "Champ": "Etat", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Assuree/Cours annule",
         "Description": "Cours annule = seance exclue du comptage des heures."},
        {"Onglet": "E3_Seances_faites", "Champ": "Assure par", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Enseignants matricule (E1)",
         "Description": "Enseignant ayant reellement assure (remplacant). Vide = enseignant programme de la seance."},
        {"Onglet": "E3_Seances_faites", "Champ": "Matiere reelle", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Matiere reellement traitee (cas remplacant changeant de matiere). Vide = matiere programmee."},
        {"Onglet": "E3_Seances_faites", "Champ": "Vol. constate h", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Duree reelle en heures si differente. Vide = duree programmee (Heure fin - Heure debut de A3)."},
        {"Onglet": "E3_Seances_faites", "Champ": "Motif", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Motif / observation (remplacement, annulation, ajustement)."},
        {"Onglet": "E3_Seances_faites", "Champ": "Saisi par", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Login ayant enregistre l'exception (auto)."},
    ],
    "N4_Controles": [
        {"Onglet": "N4_Controles", "Champ": "Matricule", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matricule de l'etudiant."},
        {"Onglet": "N4_Controles", "Champ": "Annee acad.", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Annee academique (ex. 2025-2026)."},
        {"Onglet": "N4_Controles", "Champ": "Session", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Sessions", "Description": "1 = juin, 2 = rattrapage septembre."},
        {"Onglet": "N4_Controles", "Champ": "Semestre", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Semestres cursus", "Description": "Semestre du cursus (1 a 6)."},
        {"Onglet": "N4_Controles", "Champ": "N° UE", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Numero d'UE (doit exister dans le bareme)."},
        {"Onglet": "N4_Controles", "Champ": "Matiere", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matiere (doit exister dans le bareme)."},
        {"Onglet": "N4_Controles", "Champ": "N° de controle", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Numero du controle (cle avec la Date)."},
        {"Onglet": "N4_Controles", "Champ": "Date", "Type": "Date", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Date du controle (JJ/MM/AAAA ; cle avec le N°)."},
        {"Onglet": "N4_Controles", "Champ": "Note /20", "Type": "Nombre", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Note du controle, sur 20."},
        {"Onglet": "N4_Controles", "Champ": "Coef", "Type": "Nombre", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Poids du controle dans la moyenne CC (1 par defaut)."},
        {"Onglet": "N4_Controles", "Champ": "Saisi par", "Type": "Texte", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Login ayant saisi le controle (auto)."},
    ],
    "N5_Matieres_ND": [
        {"Onglet": "N5_Matieres_ND", "Champ": "Filiere", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Filieres", "Description": "Filiere de la classe concernee."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Niveau", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Niveaux", "Description": "Niveau de la classe (L1/L2/L3)."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Section", "Type": "Texte", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "Sections", "Description": "Section, si la mesure ne vise qu une section."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Annee acad.", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Annee academique concernee."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Session", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Session ou la mention a ete posee (1 normale / 2 rattrapage)."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Semestre", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Semestre concerne."},
        {"Onglet": "N5_Matieres_ND", "Champ": "N° UE", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "UE de la matiere non dispensee."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Matiere", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matiere prevue mais non dispensee ce semestre."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Motif", "Type": "Texte", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Motif libre (enseignant absent, non programmee...)."},
        {"Onglet": "N5_Matieres_ND", "Champ": "Saisi par", "Type": "Texte", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Login ayant pose la mention (auto)."},
    ],
    "L3_Besoins": [
        {"Onglet": "L3_Besoins", "Champ": "ID besoin", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Identifiant court (BES-n, pre-suggere)."},
        {"Onglet": "L3_Besoins", "Champ": "Date d'expression", "Type": "Date",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Date d'expression du besoin (JJ/MM/AAAA)."},
        {"Onglet": "L3_Besoins", "Champ": "Type de besoin", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Hors TDR (**)", "Liste": "Types_besoin",
         "Description": "Nature du besoin (parametrable). Un besoin peut venir d'un materiel en panne ou etre autre."},
        {"Onglet": "L3_Besoins", "Champ": "Equipement concerne", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "Equipements (M1)",
         "Description": "Equipement lie (rempli si le besoin decoule d'un materiel)."},
        {"Onglet": "L3_Besoins", "Champ": "Libelle du besoin", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Description du besoin."},
        {"Onglet": "L3_Besoins", "Champ": "Quantite", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Quantite souhaitee."},
        {"Onglet": "L3_Besoins", "Champ": "Localisation / salle", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "Salles (L1)",
         "Description": "Salle / lieu concerne (liste L1)."},
        {"Onglet": "L3_Besoins", "Champ": "Priorite", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "Priorites_besoin",
         "Description": "Niveau de priorite (parametrable)."},
        {"Onglet": "L3_Besoins", "Champ": "Statut", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "Statuts_besoin",
         "Description": "Avancement du besoin (parametrable)."},
        {"Onglet": "L3_Besoins", "Champ": "Cout estime (KMF)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Estimation du cout (KMF)."},
        {"Onglet": "L3_Besoins", "Champ": "Demandeur", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Personne / service demandeur."},
        {"Onglet": "L3_Besoins", "Champ": "Observations", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Remarques."},
        {"Onglet": "L3_Besoins", "Champ": "Saisi par", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Login du saisisseur (auto)."},
    ],
    "J1_Journal_eleves": [
        {"Onglet": "J1_Journal_eleves", "Champ": "Matricule", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "TDR", "Liste": "-",
         "Description": "Matricule de l'eleve sorti."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Nom", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "TDR", "Liste": "-",
         "Description": "Nom."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Prenom", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-",
         "Description": "Prenom."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Filiere", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-",
         "Description": "Filiere."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Niveau atteint", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Dernier niveau atteint (L1/L2/L3)."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Periode (entree - sortie)", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Annees d'entree et de sortie."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Statut final", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Diplome / Abandonne / Radie."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Diplome obtenu", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Diplome obtenu le cas echeant (saisi a la cloture)."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Mention", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Mention saisie a la cloture (Passable/Assez bien/Bien/Tres bien)."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Ref. archive", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Fichier d'archive ou l'eleve a ete deplace (~3 ans)."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Cloture le", "Type": "Date",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Date de la cloture qui a journalise l'eleve."},
        {"Onglet": "J1_Journal_eleves", "Champ": "Cloture par", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Login de l'admin ayant cloture."},
    ],
    "J2_Journal_compta": [
        {"Onglet": "J2_Journal_compta", "Champ": "Annee", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Annee civile close."},
        {"Onglet": "J2_Journal_compta", "Champ": "Total recettes (KMF)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Total des recettes de l'exercice."},
        {"Onglet": "J2_Journal_compta", "Champ": "Total depenses (KMF)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Total des depenses de l'exercice."},
        {"Onglet": "J2_Journal_compta", "Champ": "Solde de cloture (KMF)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Solde reporte a nouveau l'annee suivante."},
        {"Onglet": "J2_Journal_compta", "Champ": "Ref. archive", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Fichier d'archive des mouvements de l'exercice."},
        {"Onglet": "J2_Journal_compta", "Champ": "Cloture le", "Type": "Date",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Date de la cloture."},
        {"Onglet": "J2_Journal_compta", "Champ": "Cloture par", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Login de l'admin ayant cloture."},
    ],
    "S2_Lieux_stage": [
        {"Onglet": "S2_Lieux_stage", "Champ": "Lieu / structure", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Etablissement ou unite d'accueil."},
        {"Onglet": "S2_Lieux_stage", "Champ": "Service", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Service concerne (ex. Reanimation, Chirurgie A)."},
        {"Onglet": "S2_Lieux_stage", "Champ": "Commune", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Commune / localisation."},
        {"Onglet": "S2_Lieux_stage", "Champ": "Niveau concerne", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Niveaux",
         "Description": "Niveau cible (laisser vide = tous niveaux)."},
        {"Onglet": "S2_Lieux_stage", "Champ": "Quota", "Type": "Nombre",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Nombre maximum de stagiaires par seance."},
        {"Onglet": "S2_Lieux_stage", "Champ": "Periode de disponibilite", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Periode d'accueil (optionnel)."},
    ],
    "N1_Bareme_UE": [
        {"Onglet": "N1_Bareme_UE", "Champ": "Filiere", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Filiere concernee."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Niveau", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Niveaux", "Description": "L1/L2/L3."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Semestre", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Semestres cursus", "Description": "Semestre du cursus (1 a 6)."},
        {"Onglet": "N1_Bareme_UE", "Champ": "N° UE", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Numero d'UE (ex. UE10)."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Intitule UE", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Intitule de l'UE."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Matiere", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matiere de l'UE."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Coef matiere", "Type": "Nombre", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Coefficient de la matiere DANS son UE (pondere la moyenne de l'UE). "
                        "1 par defaut : la moyenne d'UE reste la moyenne arithmetique des matieres "
                        "(modele du releve officiel). A ajuster seulement si l'ecole applique des "
                        "coefficients differencies par matiere."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Coef UE", "Type": "Nombre", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Coefficient de l'UE (pondere la moyenne du semestre)."},
        {"Onglet": "N1_Bareme_UE", "Champ": "ECTS UE", "Type": "Nombre", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Credits ECTS de l'UE."},
        {"Onglet": "N1_Bareme_UE", "Champ": "Coef confirme", "Type": "Liste", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "Oui/Non",
         "Description": "Oui = coefficient confirme par un document de reference officiel. "
                        "Non = coefficient provisoire (1 par defaut) ; moyennes non conformes au passage tant qu'il n'est pas corrige."},
    ],
    "N2_Notes": [
        {"Onglet": "N2_Notes", "Champ": "Matricule", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matricule de l'etudiant."},
        {"Onglet": "N2_Notes", "Champ": "Annee acad.", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Annee academique (ex. 2025-2026)."},
        {"Onglet": "N2_Notes", "Champ": "Session", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Sessions", "Description": "1 = juin, 2 = rattrapage septembre."},
        {"Onglet": "N2_Notes", "Champ": "Semestre", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Semestres cursus", "Description": "Semestre du cursus (1 a 6)."},
        {"Onglet": "N2_Notes", "Champ": "N° UE", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Numero d'UE (doit exister dans le bareme)."},
        {"Onglet": "N2_Notes", "Champ": "Matiere", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matiere (doit exister dans le bareme)."},
        {"Onglet": "N2_Notes", "Champ": "CC", "Type": "Nombre", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Note de controle continu /20."},
        {"Onglet": "N2_Notes", "Champ": "Examen", "Type": "Nombre", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Note d'examen /20 (ou note unique pour un stage)."},
    ],
    "N3_Signalements": [
        {"Onglet": "N3_Signalements", "Champ": "Matricule", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Matricule de l'etudiant concerne."},
        {"Onglet": "N3_Signalements", "Champ": "Date", "Type": "Date", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Date du signalement (JJ/MM/AAAA)."},
        {"Onglet": "N3_Signalements", "Champ": "Annee acad.", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Annee academique (ex. 2025-2026)."},
        {"Onglet": "N3_Signalements", "Champ": "Semestre", "Type": "Liste", "Obligatoire": "Non",
         "Provenance": "Initiative (*)", "Liste": "Semestres cursus", "Description": "Semestre concerne (facultatif)."},
        {"Onglet": "N3_Signalements", "Champ": "Contexte", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Contextes signalement", "Description": "Examen / Cours / Stage / Autre."},
        {"Onglet": "N3_Signalements", "Champ": "Emis par - fonction", "Type": "Liste", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "Fonctions signalement", "Description": "Fonction de l'emetteur (extensible)."},
        {"Onglet": "N3_Signalements", "Champ": "Nom de l'emetteur", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Nom de la personne qui signale."},
        {"Onglet": "N3_Signalements", "Champ": "Motif", "Type": "Texte", "Obligatoire": "Oui",
         "Provenance": "Initiative (*)", "Liste": "-", "Description": "Motif du signalement."},
    ],
    # V1.70 — Budget par poste (prevu). Realise agrege depuis F1 par poste (annee civile).
    "F3_Budget_poste": [
        {"Onglet": "F3_Budget_poste", "Champ": "Exercice", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Annee civile du budget (ex. 2026)."},
        {"Onglet": "F3_Budget_poste", "Champ": "Poste budgetaire", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Hors TDR (**)", "Liste": "Codes budgétaires actifs (P3)",
         "Description": "Code budgetaire (nomenclature P3, codes actifs). Le realise F1 est agrege par code."},
        {"Onglet": "F3_Budget_poste", "Champ": "Filiere", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Filieres",
         "Description": "Filiere concernee (optionnel : budget rattache au poste, filiere facultative)."},
        {"Onglet": "F3_Budget_poste", "Champ": "Sens", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Recette/Depense",
         "Description": "Recette ou Depense."},
        {"Onglet": "F3_Budget_poste", "Champ": "Source de financement / Bailleur", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Sources_financement",
         "Description": "Origine des fonds (AFD, Etat comorien, ressources propres, autres donateurs)."},
        {"Onglet": "F3_Budget_poste", "Champ": "Montant budgete (KMF)", "Type": "Nombre",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Montant prevu pour ce poste sur l'exercice (KMF)."},
        {"Onglet": "F3_Budget_poste", "Champ": "Observations", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Remarques."},
        {"Onglet": "F3_Budget_poste", "Champ": "Saisi par", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Login ayant saisi la ligne de budget (auto)."},
    ],
    # V1.70 — Taux de change de reference (EUR = parite fixe ; USD a renseigner par l'EMSP).
    "P2_Taux": [
        {"Onglet": "P2_Taux", "Champ": "Devise", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Code de la devise (ex. EUR, USD)."},
        {"Onglet": "P2_Taux", "Champ": "Code", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Code ISO numerique (ex. 978 pour l'euro)."},
        {"Onglet": "P2_Taux", "Champ": "Taux en KMF", "Type": "Nombre",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Valeur d'une unite de la devise en KMF (EUR = 491,967, parite fixe)."},
        {"Onglet": "P2_Taux", "Champ": "Date d'effet", "Type": "Date",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Date d'effet du taux (JJ/MM/AAAA)."},
        {"Onglet": "P2_Taux", "Champ": "Observations", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Remarques (ex. parite fixe)."},
    ],
    # V1.99.9 — Nomenclature budgetaire (codes recette/depense/investissement).
    # Socle OHADA + sous-articles EMSP ; la colonne Actif sert la curation compta.
    "P3_Nomenclature": [
        {"Onglet": "P3_Nomenclature", "Champ": "Code", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Code budgetaire (OHADA ou sous-article EMSP, ex. 706b)."},
        {"Onglet": "P3_Nomenclature", "Champ": "Intitule", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Libelle du compte."},
        {"Onglet": "P3_Nomenclature", "Champ": "Sens", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Sens budgetaire",
         "Description": "Recette, Depense ou Investissement."},
        {"Onglet": "P3_Nomenclature", "Champ": "Niveau", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Niveau nomenclature",
         "Description": "Chapitre, Article ou Sous-article."},
        {"Onglet": "P3_Nomenclature", "Champ": "Source", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Source code",
         "Description": "OHADA (socle officiel) ou EMSP (sous-article local)."},
        {"Onglet": "P3_Nomenclature", "Champ": "Actif", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Oui/Non",
         "Description": "Oui = visible dans les menus de saisie ; Non = en reserve."},
    ],
    # C-4 (V1.99.12) — Budget previsionnel detaille par formation et niveau.
    # Onglet ne d'une chirurgie ZIP (hors Dictionnaire classeur). Montant (KMF) et
    # Montant (EUR) sont calcules en Python et ecrits comme VALEUR (precedent E4) :
    # ils NE figurent PAS dans READONLY_COLS (onglet vide -> seraient blanchis).
    "F5_Budget_Prev": [
        {"Onglet": "F5_Budget_Prev", "Champ": "Formation", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Filieres",
         "Description": "Formation concernee (meme liste de filieres que F3)."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Niveau", "Type": "Liste",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "Niveaux budget",
         "Description": "Niveau de la formation (M1, M2, L1, L2, L3) : structure les sous-blocs."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Rubrique", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Regroupement optionnel de lignes (ex. 'Facilitation tuteurs')."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Designation", "Type": "Texte",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Libelle de la ligne de depense."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Unite1", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "1re unite (ex. personnes, etudiants, heures, billets)."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Qte1", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "1re quantite (facteur du montant)."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Unite2", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "2e unite (ex. mois, annee, nuitees, modules)."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Qte2", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "2e quantite (facteur du montant)."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Cout unitaire (KMF)", "Type": "Nombre",
         "Obligatoire": "Oui", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Cout unitaire en KMF."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Poste budgetaire", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "Codes depense actifs (P3)",
         "Description": "Code budgetaire P3 (codes ACTIFS de Sens Depense). Autocomplete code — intitule ; code seul enregistre."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Source de financement / Bailleur", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Sources_financement",
         "Description": "Origine des fonds (AFD, Etat comorien, ressources propres, autres)."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Session", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Annee academique du budget (AAAA-AAAA). Defaut : annee acad. courante."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Montant (KMF)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Calcule (Qte1 x Qte2 x Cout unitaire), en KMF. Lecture seule a l'IHM."},
        {"Onglet": "F5_Budget_Prev", "Champ": "Montant (EUR)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Calcule (Montant KMF / taux EUR). Lecture seule a l'IHM."},
    ],
}

# SURCHARGE d'entrees existantes du Dictionnaire (sans modifier le classeur). Cle =
# onglet -> {libelle champ -> {cle a remplacer: valeur}}. Applique apres lecture.
# V1.28 : S1 'Lieu de stage' n'est plus alimente par la liste P0 'Lieux_stage' (simple)
# mais par le referentiel S2 (composite "Lieu — Service").
DICTIONNAIRE_SURCHARGE = {
    "S1_Stages": {"Lieu de stage": {"Liste": "Lieux de stage (S2)"}},
    # H1 : « Type » devient la CATEGORIE du document, alimentee par la liste
    # editable par le directeur « Categories_doc » (P0). Type deja declare Liste
    # dans le Dictionnaire du classeur ; on ne fait que brancher la source.
    "H1_Biblio_docs": {"Type": {"Liste": "Categories_doc",
                                "Description": "Categorie du document (liste editable dans Parametres : Strategique, Medical, Supports de cours, Reglementaire/officiel, OMS/international, Autre...)."}},
    # G1 : Statut deja declare Liste (sans source) -> on branche la liste editable
    # Statuts_action (notion de planning : Non demarre / En cours / Atteint...).
    "G1_Plan_action": {"Statut": {"Liste": "Statuts_action",
                                  "Description": "Avancement de l'action (liste editable dans Parametres)."}},
    # M1 : etat parametrable (Actif / En panne / Hors service / En maintenance / Reforme).
    "M1_Equipements": {"Etat": {"Liste": "Etats_materiel",
                                "Description": "Etat de l'equipement (liste editable dans Parametres). 'En panne' peut declencher une expression de besoin."},
                       # V1.70 : liste partagee renommee "Bailleurs" -> "Sources_financement".
                       "Source de financement / Bailleur": {"Liste": "Sources_financement"}},
    # V1.70 : F1 partage la meme liste renommee (source unique F1 / M1 / F3).
    "F1_Mouvements": {"Source de financement / Bailleur": {"Liste": "Sources_financement"},
                      # V1.99.10 (C-3) : le code budgetaire est choisi dans P3 (codes actifs).
                      "Poste budgetaire": {"Liste": "Codes budgétaires actifs (P3)",
                                           "Description": "Code budgetaire (nomenclature P3, codes actifs). Saisi en autocomplete code — intitule ; le code seul est enregistre."}},
}

# Champs AJOUTES a un onglet deja present dans l'onglet Dictionnaire du classeur
# (DICTIONNAIRE_SUPPLEMENT n'ajoute qu'un onglet entier absent ; ceci ajoute un
# champ a un onglet existant, sans modifier le classeur). Rapproche par 'Champ'
# avec l'en-tete physique reel de la feuille.
DICTIONNAIRE_CHAMPS_SUP = {
    # STAGES-2 (V1.99.7) : rattrapage = seance de stage distincte (S1).
    "S1_Stages": [
        {"Onglet": "S1_Stages", "Champ": "Session", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "TDR", "Liste": "Session stage",
         "Description": "Normale (stage initial) ou Rattrapage. Les deux lignes "
                        "coexistent pour un meme stage (Matricule + Annee + Seance) ; "
                        "au bulletin, la note du Rattrapage prime si elle est saisie. "
                        "Vide est traite comme Normale."},
    ],
    # Bloc 3 (V1.99.3) : remuneration des enseignants / vacataires (E1).
    "E1_Enseignants": [
        {"Onglet": "E1_Enseignants", "Champ": "Taux horaire (KMF/h)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-",
         "Description": "Taux horaire individuel (KMF/h). Vide -> taux global par defaut."},
        {"Onglet": "E1_Enseignants", "Champ": "Mode de remuneration", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "TDR", "Liste": "Horaire/Forfait",
         "Description": "Horaire (vacation a l'heure) ou Forfait mensuel (moniteur)."},
        {"Onglet": "E1_Enseignants", "Champ": "Cout mensuel (KMF)", "Type": "Nombre",
         "Obligatoire": "Non", "Provenance": "TDR", "Liste": "-",
         "Description": "Cout mensuel (KMF) utilise quand le mode est Forfait mensuel."},
    ],
    # Nouvelle colonne G1 'Type d'écart' (categorie de l'ecart) : liste editable
    # Types_ecart (budgetaire / temporel / contenu de formation / qualite / autre).
    "G1_Plan_action": [
        {"Onglet": "G1_Plan_action", "Champ": "Type d'écart", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Types_ecart",
         "Description": "Nature de l'ecart constate (liste editable dans Parametres)."},
        {"Onglet": "G1_Plan_action", "Champ": "Axe / thème", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Grand axe / thematique de pilotage (ex. Scolarite, Pedagogie, Stages, Finances, Organisation)."},
        {"Onglet": "G1_Plan_action", "Champ": "Objectif (résultat attendu)", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Resultat vise par l'action."},
        {"Onglet": "G1_Plan_action", "Champ": "Priorité", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Haute/Moyenne/Basse",
         "Description": "Niveau de priorite de l'action (Haute / Moyenne / Basse)."},
        {"Onglet": "G1_Plan_action", "Champ": "Temporalité", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Court/Moyen/Long terme",
         "Description": "Horizon de l'action (court / moyen / long terme), complementaire de l'echeance datee."},
        {"Onglet": "G1_Plan_action", "Champ": "Indicateur de réussite et preuves", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Indicateur de reussite et preuves attendues (livrable, document, taux...)."},
        {"Onglet": "G1_Plan_action", "Champ": "Observations", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Remarques libres."},
    ],
    # Nouvelle colonne M1 'Localisation provisoire' (materiel deplace / en reparation).
    "M1_Equipements": [
        {"Onglet": "M1_Equipements", "Champ": "Localisation provisoire", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Hors TDR (**)", "Liste": "-",
         "Description": "Emplacement temporaire (ex. atelier, en reparation, prete)."},
    ],
    # V1.69 : colonnes ajoutees a F1_Mouvements pour le suivi des droits d'inscription.
    # Renseignees uniquement pour les recettes d'inscription (via l'ecran d'encaissement
    # de la fiche etudiant), pas pour les autres mouvements de tresorerie.
    "F1_Mouvements": [
        {"Onglet": "F1_Mouvements", "Champ": "Matricule", "Type": "Texte",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "-",
         "Description": "Matricule de l'etudiant rattache a la recette d'inscription (806/706). Vide pour les autres mouvements."},
        {"Onglet": "F1_Mouvements", "Champ": "Annee academique", "Type": "Liste",
         "Obligatoire": "Non", "Provenance": "Initiative (*)", "Liste": "Annees_acad",
         "Description": "Annee academique de l'inscription (ex. 2025-2026), distincte de l'annee civile portee par la date d'operation. Gere les redoublants."},
    ],
}

# Champs en SUGGESTIONS (datalist) alimentees par la maquette R1 (V1.26). Saisie
# libre conservee : le Dictionnaire garde "Texte" (pas de liste stricte), le
# classeur reste inchange. Cle = onglet ; valeurs = libelles PROPRES des champs.
# 'matiere' = champ a suggestions ; 'volume' = champ pre-rempli (si vide) avec la
# somme des heures programmees ; 'filiere'/'niveau'/'semestre' = filtres de la ligne.
MAQUETTE_DATALIST = {
    "A3_Sessions": {
        "matiere":  "Matiere",
        "volume":   "Vol. horaire prog.",
        "filiere":  "Filiere",
        "niveau":   "Niveau",
        "semestre": "Semestre",
    },
}

# --- Structure du GUIDE : sections -> modules ---
# Chaque module : (cle onglet, libelle, icone Tabler)
GUIDE_STRUCTURE = [
    {
        "id": "scolarite", "num": "1", "titre": "Vie académique", "pleine": True,
        "icone": "ti-school", "couleur": "#2E6CA4",
        "intro": "Élèves, présences, notes & bulletins, stages et discipline.",
        "groupes": [
            {"titre": "Élèves", "icone": "ti-users", "modules": [
                ("ETU_Fiche", "Fiche étudiant (recherche par matricule)", "ti-id"),
                ("A1_Etudiants", "Fiches & inscriptions", "ti-user-plus"),
            ]},
            {"titre": "Présences", "icone": "ti-checklist", "modules": [
                ("A2_Presences", "Présences (feuille & saisie)", "ti-checklist"),
            ]},
            {"titre": "Notes & bulletins", "icone": "ti-pencil", "modules": [
                ("NOT_Grille", "Saisie des notes par classe (liste matière)", "ti-table"),
                ("BUL_Saisie", "Saisie façon bulletin (avancé)", "ti-clipboard-text"),
                ("N1_Bareme_UE", "Barème des UE (coefficients, ECTS)", "ti-list-numbers"),
                ("REL_Releve", "Relevé / bulletin (calcul & impression)", "ti-file-certificate"),
                ("RES_Classe", "Résultats par classe (synthèse)", "ti-table"),
                ("A4_Documents_etud", "Documents & attestations", "ti-file-text"),
            ]},
            {"titre": "Stages", "icone": "ti-map-pin", "modules": [
                ("S1_Stages", "Stages — affectation & fiches retour", "ti-map-pin"),
                ("STG_Suivi", "Stages — suivi & tableau de bord", "ti-clipboard-data"),
                ("STG_Auto", "Stages — affectation", "ti-map-pin-check"),
                ("S2_Lieux_stage", "Lieux de stage — référentiel & quotas", "ti-building-hospital"),
            ]},
            {"titre": "Discipline", "icone": "ti-alert-triangle", "modules": [
                ("N3_Signalements", "Signalements / indiscipline", "ti-alert-triangle"),
                ("SIG_Etat", "État des signalements (par étudiant)", "ti-report"),
            ]},
            {"titre": "Référentiel", "icone": "ti-list-details", "modules": [
                ("R1_Maquettes", "Référentiel des formations (maquettes)", "ti-list-details"),
                ("PLN_Volumes", "Planification — volumes par classe", "ti-clock-hour-4"),
                ("PLN_Grille", "Planification — grille hebdomadaire", "ti-calendar-week"),
            ]},
        ],
    },
    {
        "id": "enseignants", "num": "2", "titre": "Enseignement",
        "icone": "ti-user-star", "couleur": "#2E6CA4",
        "intro": "Enseignants & vacataires, séances, calendrier et heures (constaté, paie).",
        "groupes": [
            {"titre": "Enseignants", "icone": "ti-user-star", "modules": [
                ("ENS_Fiche", "Fiche enseignant (recherche)", "ti-id-badge-2"),
                ("E1_Enseignants", "Enseignants & vacataires", "ti-user-star"),
            ]},
            {"titre": "Activité", "icone": "ti-calendar-event", "modules": [
                ("A3_Sessions", "Séances & planning", "ti-calendar-event"),
                ("CAL_Calendrier", "Calendrier (mois/semaine/jour)", "ti-calendar-month"),
                ("E3_Seances_faites", "Séances réalisées (exceptions)", "ti-clipboard-check"),
            ]},
            {"titre": "Heures", "icone": "ti-clock-hour-4", "modules": [
                ("E2_Releve_heures", "Relevé des heures", "ti-clock-hour-4"),
                ("HRS_Heures", "Heures constatées (report paie)", "ti-clock-check"),
                ("PAIE_Etat", "États de paiement (vacations)", "ti-cash-banknote"),
                ("E4_Etats_paiement", "États de paiement (audit)", "ti-table"),
            ]},
        ],
    },
    {
        "id": "ressources", "num": "3", "titre": "Salles, réservations, équipement",
        "icone": "ti-building", "couleur": "#2E6CA4",
        "intro": "Salles & planning, réservations, équipements et expression de besoin.",
        "groupes": [
            {"titre": "Salles", "icone": "ti-door", "modules": [
                ("VUE_Salles", "Salles — planning du jour", "ti-layout-grid"),
                ("L1_Salles", "Salles & équipements", "ti-door"),
                ("L2_Reservations", "Réservations de salles", "ti-calendar-plus"),
            ]},
            {"titre": "Matériel", "icone": "ti-package", "modules": [
                ("M1_Equipements", "Équipements & inventaire", "ti-device-desktop"),
                ("L3_Besoins", "Expression de besoin", "ti-clipboard-list"),
            ]},
        ],
    },
    {
        "id": "finances", "num": "4", "titre": "Finances", "pleine": True,
        "icone": "ti-cash", "couleur": "#1F4E79",
        "intro": "Trésorerie (recettes & dépenses), comptes, budget par poste, clôture et journaux.",
        "groupes": [
            {"titre": "Trésorerie & budget", "icone": "ti-cash", "modules": [
                ("F1_Mouvements", "Trésorerie — recettes & dépenses", "ti-arrows-exchange"),
                ("F2_Comptes", "Comptes & caisses", "ti-wallet"),
                ("F3_Budget_poste", "Budget par poste (prévu / réalisé)", "ti-report-money"),
                ("BUD_Previsionnel", "Budget prévisionnel par formation", "ti-report-money"),
                ("SYN_Budget", "Synthèse budgétaire (prévu / réalisé)", "ti-chart-bar"),
                ("BAIL_Fiche", "Fiche source de financement (recherche)", "ti-building-bank"),
                ("F4_Bailleurs", "Sources de financement", "ti-table"),
            ]},
            {"titre": "Clôture & journaux", "icone": "ti-archive", "modules": [
                ("CLO_Cloture", "Clôture & archivage", "ti-archive"),
                ("J1_Journal_eleves", "Journal permanent élèves (lecture seule)", "ti-history"),
                ("J2_Journal_compta", "Journal permanent compta (lecture seule)", "ti-history"),
            ]},
        ],
    },
    {
        "id": "pilotage", "num": "5", "titre": "Pilotage",
        "icone": "ti-dashboard", "couleur": "#1F4E79",
        "intro": "Tableau de bord de direction, requêtes multicritères, éditions et plan d'action.",
        "groupes": [
            {"titre": "", "icone": "", "modules": [
                ("TDB_Direction", "Tableau de bord", "ti-dashboard"),
                ("REQ_Hub", "Requêtes & analyses", "ti-zoom-question"),
                ("ED_Impressions", "Impressions & éditions", "ti-printer"),
                ("G1_Plan_action", "Plan d'action", "ti-list-check"),
            ]},
        ],
    },
    {
        "id": "administration", "num": "6", "titre": "Administration", "aside": True,
        "icone": "ti-settings", "couleur": "#1F4E79",
        "intro": "Documents & modèles, paramètres, taux de change, rôles & droits, comptes et import national.",
        "groupes": [
            {"titre": "Documents & modèles", "icone": "ti-books", "modules": [
                ("BIBLIO_Docs", "Bibliothèque documentaire", "ti-books"),
                ("ED_Modeles", "Modèles de documents", "ti-template"),
            ]},
            {"titre": "Configuration", "icone": "ti-settings", "modules": [
                ("P0_Parametres", "Paramètres & listes", "ti-list-details"),
                ("P2_Taux", "Taux de change (références)", "ti-coin"),
                ("P3_Nomenclature", "Nomenclature budgétaire (codes)", "ti-list-numbers"),
                ("NOM_Curation", "Nomenclature — curation", "ti-checkbox"),
                ("MAT_Autorisations", "Comptes & droits d'accès", "ti-shield-lock"),
                ("IMPORT_zone", "Import CSV national", "ti-file-import"),
            ]},
            {"titre": "Sauvegarde & maintenance", "icone": "ti-database-export", "modules": [
                ("SAV_Sauvegarde", "Sauvegarde des données", "ti-database-export"),
            ]},
        ],
    },
]
# Compat : liste a plat des modules par section, derivee des groupes (source unique).
# Consommee telle quelle par _index(), le menu, l'accueil, app.py et metier.py.
for _sec in GUIDE_STRUCTURE:
    _sec["modules"] = [m for g in _sec.get("groupes", []) for m in g["modules"]]


# Pages de reference (bas de menu)
PAGES_REF = [
    ("ETU_Fiche", "Fiche étudiant", "ti-id"),
    ("Legende", "Legende", "ti-info-circle"),
    ("Guide", "Guide d'utilisation", "ti-help"),
    ("Dictionnaire", "Dictionnaire des donnees", "ti-book-2"),
]

# Index rapide onglet -> (section_id, libelle, icone)
def _index():
    idx = {}
    for sec in GUIDE_STRUCTURE:
        for cle, lib, ico in sec["modules"]:
            idx[cle] = {"section": sec["id"], "section_titre": sec["titre"],
                        "libelle": lib, "icone": ico, "couleur": sec["couleur"]}
    for cle, lib, ico in PAGES_REF:
        idx[cle] = {"section": "reference", "section_titre": "Reference",
                    "libelle": lib, "icone": ico, "couleur": COULEUR}
    return idx

TAB_INDEX = _index()

# Onglets techniques conserves HORS menu (audit / retro-compat) : garantir leur
# presence dans TAB_INDEX pour qu'une route qui les cite ne plante jamais, meme
# apres retrait du menu. Le menu, lui, reste construit depuis GUIDE_STRUCTURE.
for _cle, _lib, _ico in [("N2_Notes", "Notes \u2014 correction directe (audit)", "ti-edit")]:
    TAB_INDEX.setdefault(_cle, {"section": "scolarite", "section_titre": "Vie acad\u00e9mique",
                                "libelle": _lib, "icone": _ico, "couleur": COULEUR})


# Cles de menu qui ne sont PAS des onglets Excel : route Flask dediee.
# --- Verrou anti-suppression des listes P0 (V1.80) -------------------------
# Une valeur de liste structurante ne peut etre retiree si elle est encore
# employee dans les donnees. Cle = nom de colonne P0 normalise (sans suffixe
# (*) / (**)) ; valeur = liste de (onglet, colonne consommatrice normalisee).
# Les listes absentes de ce dict restent librement supprimables (faible enjeu).
P0_CONSOMMATEURS = {
    "filieres": [("A1_Etudiants", "filiere"), ("A3_Sessions", "filiere"),
                 ("F3_Budget_poste", "filiere")],
    "niveaux": [("A1_Etudiants", "niveau"), ("A3_Sessions", "niveau")],
    "sections": [("A1_Etudiants", "section"), ("A3_Sessions", "section")],
    "semestres": [("A3_Sessions", "semestre")],
    "statuts_etudiant": [("A1_Etudiants", "statut")],
    "annees_acad": [("A1_Etudiants", "annee acad."), ("A3_Sessions", "annee acad."),
                    ("F1_Mouvements", "annee academique")],
    "lieux_stage": [("S1_Stages", "lieu de stage")],
    "cat_recettes": [("F1_Mouvements", "categorie")],
    "cat_depenses": [("F1_Mouvements", "categorie")],
    "postes_budgetaires": [("F1_Mouvements", "poste budgetaire"),
                           ("F3_Budget_poste", "poste budgetaire")],
    "modes_paiement": [("F1_Mouvements", "mode paiement")],
    "comptes_caisses": [("F1_Mouvements", "compte / caisse"),
                        ("F2_Comptes", "nom du compte / caisse")],
    "sources_financement": [("F1_Mouvements", "source de financement / bailleur"),
                            ("F3_Budget_poste", "source de financement / bailleur"),
                            ("M1_Equipements", "source de financement / bailleur")],
    "categories_equipement": [("M1_Equipements", "categorie")],
    "etats_materiel": [("M1_Equipements", "etat")],
}

SPECIAL_ROUTES = {
    "BIBLIO_Docs": "bibliotheque",
    "ETU_Fiche": "etudiant",
    "ENS_Fiche": "enseignant",
    "BAIL_Fiche": "bailleur",
    "PAIE_Etat": "paiement",
    "PRESL_Libre": "presences_libre",
    "BUL_Saisie": "bulletin",
    "NOT_Grille": "saisie_notes_classe",
    "TDB_Direction": "tableau_bord",
    "CAL_Calendrier": "calendrier",
    "VUE_Salles": "salles",
    "L2_Reservations": "reservations",
    "A2_Presences": "presences_saisie",
    "MAT_Autorisations": "autorisations",
    "IMPORT_zone": "import_csv",
    "ED_Modeles": "modeles_docs",
    "NOM_Curation": "nomenclature",
    "BUD_Previsionnel": "budget_previsionnel",
    "SYN_Budget": "budget_synthese",
    "ED_Impressions": "impressions",
    "REQ_Hub": "requetes",
    "REL_Releve": "releve",
    "SIG_Etat": "etat_signalements",
    "CLO_Cloture": "cloture",
    "HRS_Heures": "heures_constatees",
    "SAV_Sauvegarde": "sauvegarde",
    "RES_Classe": "resultats_classe",
    "STG_Auto": "stages_affectation",
    "STG_Suivi": "stages_suivi",
    "PLN_Volumes": "planification_volumes",
    "PLN_Grille": "planification_grille",
}

# --- Specifications du tableau de bord (graphiques selectionnables) ---
# Chaque graphe : id, titre, type par defaut, types autorises
DASHBOARD_CHARTS = [
    {"id": "filieres", "titre": "Effectif par filiere", "defaut": "bar",
     "types": ["bar", "pie", "radar"]},
    {"id": "statuts", "titre": "Repartition par statut", "defaut": "pie",
     "types": ["pie", "bar", "radar"]},
    {"id": "finances", "titre": "Recettes / Depenses par categorie (KMF)", "defaut": "bar",
     "types": ["bar", "pie"]},
    {"id": "presence", "titre": "Taux de presence par creneau", "defaut": "bar",
     "types": ["bar", "radar", "pie"]},
    {"id": "heures", "titre": "Heures constatees par enseignant", "defaut": "bar",
     "types": ["bar", "pie"]},
    {"id": "reste_du_filiere", "titre": "Reste du par filiere (KMF)", "defaut": "bar",
     "types": ["bar", "pie", "radar"]},
]


# ===========================================================================
# TABLEAU DE BORD DIRECTION — V1.99.15 (#20, briques A + B)
# ---------------------------------------------------------------------------
# Catalogue des indicateurs SELECTIONNABLES du tableau de bord (KPI + graphes).
# La selection (quels indicateurs afficher) est GLOBALE etablissement, persistee
# dans instance/reglages.json (cle "tdb_selection") ; defaut = tous. Les ids KPI
# correspondent aux data-k de tableau_bord.html et aux cles de metier.kpis() ;
# les ids graphes correspondent a DASHBOARD_CHARTS ci-dessus.
# ===========================================================================
TDB_KPIS = [
    {"id": "etudiants",     "libelle": "Effectif total"},
    {"id": "actifs",        "libelle": "Actifs"},
    {"id": "diplomes",      "libelle": "Diplomes"},
    {"id": "taux_presence", "libelle": "Taux de presence (%)"},
    {"id": "recettes",      "libelle": "Recettes (KMF)"},
    {"id": "depenses",      "libelle": "Depenses (KMF)"},
    {"id": "solde",         "libelle": "Solde (KMF)"},
    {"id": "heures",        "libelle": "Heures constatees"},
    {"id": "reste_du",      "libelle": "Reste du (KMF)"},
]


def tdb_kpi_ids():
    """Ids des KPI du catalogue TDB, dans l'ordre d'affichage."""
    return [k["id"] for k in TDB_KPIS]


def tdb_chart_ids():
    """Ids des graphes du catalogue TDB (= DASHBOARD_CHARTS), dans l'ordre."""
    return [c["id"] for c in DASHBOARD_CHARTS]


# --- Brique C (#20) : indicateurs BUDGET (issus de synthese_budgetaire, C-5).
# Bornes sur UNE session (defaut annee acad. courante), non filtrables filiere/
# niveau (comme les finances). Ids distincts des KPI standard ; partagent les memes
# champs de selection (name="kpi" / name="chart") -> selection unique. ---
TDB_KPIS_BUDGET = [
    {"id": "bud_prevu",       "libelle": "Budget prevu total (KMF)"},
    {"id": "bud_realise",     "libelle": "Realise total (KMF)"},
    {"id": "bud_taux",        "libelle": "Taux de consommation (%)"},
    {"id": "bud_ecart",       "libelle": "Ecart total (KMF)"},
    {"id": "bud_depassement", "libelle": "Postes en depassement"},
]
TDB_CHARTS_BUDGET = [
    {"id": "budget_poste", "titre": "Budget prevu vs realise par poste (KMF)"},
]


def tdb_kpi_budget_ids():
    return [k["id"] for k in TDB_KPIS_BUDGET]


def tdb_chart_budget_ids():
    return [c["id"] for c in TDB_CHARTS_BUDGET]


# ===========================================================================
# MODULE IMPRESSIONS & EDITIONS — V1.18
# ---------------------------------------------------------------------------
# Onglet additif D1_Modeles_docs : modeles persistants des documents imprimables
# (parties fixes editables : en-tete, titre, corps a jetons, mentions/pied,
# libelle signataire, nombre de copies). Edite depuis l'ecran Parametrages ->
# Modeles de documents. Aucune formule (texte). Conforme au Nota classeur (ajout
# additif d'onglet, ne touche ni les onglets ni les 669 formules existants).
# ===========================================================================
MODELE_TAB = "D1_Modeles_docs"
# En-tetes (sans marqueur de provenance : onglet de parametrage, hors module IHM).
MODELE_COLS = ["Cle doc", "Libelle", "En-tete", "Titre", "Corps",
               "Mentions / pied", "Libelle signataire", "Nb copies"]

# Civilite deduite du Genre (parametrable). Cle = initiale normalisee du genre.
CIVILITES = {"M": "Monsieur", "F": "Madame"}
CIVILITE_DEFAUT = "Monsieur / Madame"

# Feuille de presence vierge : nombre de lignes a signer par defaut (confirme).
PRESENCE_LIGNES_DEFAUT = 60

# En-tete officiel par defaut (mutualise) — accent-free comme le reste du code ;
# l'utilisateur peut ajouter les accents depuis l'ecran Modeles.
_ENTETE_OFFICIEL = (
    "UNION DES COMORES\n"
    "Unite - Solidarite - Developpement\n"
    "Ministere de l'Education Nationale, de l'Enseignement Superieur et de la Recherche\n"
    "Universite des Comores\n"
    "Ecole de Medecine et de Sante Publique"
)

# Specs des 6 documents du lot V1.18. Pour chaque cle :
#   libelle  : intitule lisible (menu / hub)
#   source   : onglet(s) source des donnees
#   tabulaire: True si le corps est une grille generee (liste/presence/recap),
#              False si c'est un corps en prose a jetons (attestation/recu/releve ind.)
#   jetons   : jetons {…} disponibles dans le corps (doc en prose)
#   defauts  : valeurs initiales du modele (En-tete/Titre/Corps/Mentions/Signataire/Nb copies)
MODELES_DOCS = {
    "ATTESTATION": {
        "libelle": "Attestation de passage",
        "source": "A1_Etudiants",
        "tabulaire": False,
        "icone": "ti-certificate",
        "jetons": ["civilite", "nom", "prenom", "matricule", "date_naissance",
                   "lieu_naissance", "niveau", "filiere", "section", "annee", "date_jour"],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "ATTESTATION DE PASSAGE",
            "Corps": (
                "Je soussigne(e), responsable de la scolarite de l'Ecole de Medecine et de "
                "Sante Publique, atteste que :\n\n"
                "{civilite} {prenom} {nom}, ne(e) le {date_naissance} a {lieu_naissance}, "
                "matricule {matricule}, est regulierement inscrit(e) en {niveau} - {filiere} "
                "(section {section}) au titre de l'annee academique {annee}.\n\n"
                "La presente attestation est delivree pour servir et valoir ce que de droit.\n\n"
                "Fait a Moroni, le {date_jour}."
            ),
            "Mentions / pied": "",
            "Libelle signataire": "Le Chef de la Scolarite",
            "Nb copies": "1",
        },
    },
    "RECU": {
        "libelle": "Recu de paiement",
        "source": "F1_Mouvements",
        "tabulaire": False,
        "icone": "ti-receipt",
        "jetons": ["reference", "date_operation", "tiers", "montant", "categorie",
                   "compte", "mode_paiement", "libelle", "date_jour"],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "RECU DE PAIEMENT",
            "Corps": (
                "Recu N {reference}\n\n"
                "Recu de {tiers} la somme de {montant} KMF (Francs comoriens),\n"
                "au titre de : {categorie} - {libelle}.\n\n"
                "Date de l'operation : {date_operation}\n"
                "Mode de paiement : {mode_paiement}\n"
                "Compte / caisse : {compte}\n\n"
                "Fait a Moroni, le {date_jour}."
            ),
            "Mentions / pied": "Ce recu fait foi de paiement.",
            "Libelle signataire": "Le Comptable",
            "Nb copies": "2",
        },
    },
    "LISTE_ETUD": {
        "libelle": "Liste d'etudiants",
        "source": "A1_Etudiants",
        "tabulaire": True,
        "icone": "ti-list-numbers",
        "jetons": [],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "LISTE DES ETUDIANTS",
            "Corps": "",
            "Mentions / pied": "",
            "Libelle signataire": "Le Chef de la Scolarite",
            "Nb copies": "1",
        },
    },
    "PRESENCE_VIERGE": {
        "libelle": "Feuille de presence vierge",
        "source": "—",
        "tabulaire": True,
        "icone": "ti-clipboard-list",
        "jetons": [],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "FICHE DE PRESENCE",
            "Corps": "Hopital ou centre : ......................   Section : ......................\n"
                     "Periode du ...... / ...... / ......  au  ...... / ...... / ......",
            "Mentions / pied": "En cas de rectification, les services concernes seront avertis.",
            "Libelle signataire": "Signature du responsable de service",
            "Nb copies": "1",
        },
    },
    "RELEVE_IND": {
        "libelle": "Releve d'heures individuel (paie)",
        "source": "E2_Releve_heures + E1_Enseignants",
        "tabulaire": False,
        "icone": "ti-clock-hour-4",
        "jetons": ["matricule", "nom", "prenom", "statut", "departement",
                   "mois_annee", "vol_prog", "vol_constate", "total_heures", "date_jour"],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "RELEVE D'HEURES - ENSEIGNANT",
            "Corps": (
                "Enseignant : {nom} {prenom} (matricule {matricule})\n"
                "Statut : {statut}    Departement : {departement}\n"
                "Periode : {mois_annee}\n\n"
                "Volume horaire programme : {vol_prog} h\n"
                "Volume horaire constate : {vol_constate} h\n"
                "Total heures a payer : {total_heures} h\n\n"
                "Releve etabli pour la paie. Fait a Moroni, le {date_jour}."
            ),
            "Mentions / pied": "Heures uniquement (sans taux ni montant).",
            "Libelle signataire": "L'enseignant / Le Chef de departement",
            "Nb copies": "1",
        },
    },
    "RELEVE_RECAP": {
        "libelle": "Recapitulatif mensuel des heures (tous enseignants)",
        "source": "E2_Releve_heures + E1_Enseignants",
        "tabulaire": True,
        "icone": "ti-table",
        "jetons": [],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "RECAPITULATIF MENSUEL DES HEURES - ENSEIGNANTS",
            "Corps": "",
            "Mentions / pied": "Heures uniquement (sans taux ni montant).",
            "Libelle signataire": "La Direction",
            "Nb copies": "1",
        },
    },
    "SITUATION_COMPTE": {
        "libelle": "Situation de compte (registre mensuel)",
        "source": "F1_Mouvements",
        "tabulaire": True,
        "icone": "ti-report-money",
        "jetons": ["compte", "periode", "date_jour"],
        "defauts": {
            "En-tete": _ENTETE_OFFICIEL,
            "Titre": "SITUATION DE COMPTE",
            "Corps": "Compte / caisse : {compte}    Periode : {periode}",
            "Mentions / pied": "Fait a Moroni, le {date_jour}.",
            # Deux signataires (separes par |) : Gestionnaire (gauche) et Directeur (droite).
            "Libelle signataire": "Le Gestionnaire | Le Directeur de l'EMSP",
            "Nb copies": "1",
        },
    },
}
# Ordre d'affichage stable dans le hub et l'ecran Modeles.
MODELES_ORDRE = ["LISTE_ETUD", "PRESENCE_VIERGE", "RELEVE_IND", "RELEVE_RECAP",
                 "RECU", "ATTESTATION", "SITUATION_COMPTE"]
