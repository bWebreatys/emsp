#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seed du JEU DE FORMATION de l'EMSP.

Remplit un classeur EMSP_V1.xlsx (copie du master VIDE) avec un jeu d'exemples
fictif mais realiste, pour rendre les ecrans et les listes parlants en formation.

Usage (depuis la racine du logiciel) :
    python formation/seed_formation.py [chemin_du_classeur]

Sans argument, agit sur config.WORKBOOK. Pour (re)generer la baseline du kit :
    copier le master VIDE -> formation/seed/EMSP_V1.xlsx
    python formation/seed_formation.py formation/seed/EMSP_V1.xlsx

NE JAMAIS lancer sur le classeur de PRODUCTION : ce script ajoute des donnees
fictives. Il est concu pour la baseline de formation uniquement.
"""
import os
import sys

# racine du logiciel = dossier parent de formation/
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

import config            # noqa: E402
import data              # noqa: E402


def seed(chemin=None):
    chemin = chemin or config.WORKBOOK
    db = data.AccesDonnees(chemin)

    def add(onglet, rows):
        db.ajouter_lignes(onglet, rows)
        print("  +%2d -> %s" % (len(rows), onglet))

    etu = [("90001", "M", "ABDOU", "Nasser", "12/03/2003", "Moroni", "Soins infirmiers", "L1", "S.I"),
           ("90002", "F", "SAID", "Anziza", "05/07/2004", "Mutsamudu", "Soins obstétricaux", "L1", "S.O"),
           ("90003", "M", "MZE", "Hamadi", "21/11/2002", "Fomboni", "Soins infirmiers", "L2", "S.I"),
           ("90004", "F", "ALI", "Roukia", "14/02/2005", "Moroni", "Soins obstétricaux", "L2", "S.O"),
           ("90005", "M", "IBRAHIM", "Toufé", "30/09/2003", "Domoni", "Soins infirmiers", "L3", "S.I"),
           ("90006", "F", "MOHAMED", "Salma", "08/06/2004", "Mitsamiouli", "Soins obstétricaux", "L3", "S.O"),
           ("90007", "M", "ALI", "Souf", "19/12/2002", "Moroni", "Maintenance biomédicale", "L1", ""),
           ("90008", "F", "DJOUMOI", "Naïma", "25/04/2005", "Ouani", "Maintenance biomédicale", "L2", ""),
           ("90009", "M", "ABDALLAH", "Kamal", "03/01/2003", "Moroni", "Imagerie médicale", "L1", ""),
           ("90010", "F", "YOUSSOUF", "Hadidja", "17/08/2004", "Mbéni", "Imagerie médicale", "L2", ""),
           ("90011", "M", "MOUSSA", "Anrif", "11/05/2003", "Foumbouni", "Aides-soignants", "L1", "AS"),
           ("90012", "F", "BACAR", "Zalha", "28/10/2005", "Sima", "Aides-soignants", "L1", "AS")]
    add("A1_Etudiants", [{"N ordre (*)": i + 1, "Matricule": m, "Genre (*)": g, "Nom": n, "Prenom": p,
                          "Date naissance": dn, "Lieu naissance": ln, "Niveau": niv, "Filiere": fil,
                          "Section (*)": sec, "Annee acad. (*)": "2025-2026", "Statut (**)": "Actif",
                          "Date inscription": "01/10/2025", "Saisi par (*)": "formation"}
                         for i, (m, g, n, p, dn, ln, fil, niv, sec) in enumerate(etu)])

    ens = [("ENS-01", "M", "HAMIDI", "Said", "Titulaire", "Anatomie", "Médecin", "Soins infirmiers"),
           ("ENS-02", "F", "MAOULIDA", "Fatima", "Vacataire", "Microbiologie", "Pharmacien", "Soins infirmiers"),
           ("ENS-03", "M", "ABDOU", "Ahamada", "Titulaire", "Pédiatrie", "Médecin pédiatre", "Soins infirmiers"),
           ("ENS-04", "F", "SAID", "Mariama", "Vacataire", "Obstétrique", "Sage-femme", "Soins obstétricaux"),
           ("ENS-05", "M", "MZE", "Toihir", "Titulaire", "Maintenance biomédicale", "Ingénieur biomédical", "Maintenance biomédicale"),
           ("ENS-06", "M", "ALI", "Mohamed", "Titulaire", "Imagerie médicale", "Manipulateur radio", "Imagerie médicale"),
           ("ENS-07", "F", "NADHOIM", "Asma", "Vacataire", "Communication", "Formatrice", "Sciences humaines")]
    add("E1_Enseignants", [{"Matricule ens.": m, "Genre (*)": g, "Nom": n, "Prenom": p,
                            "Statut (titulaire/vacataire) (*)": st, "Matieres enseignees": mat,
                            "Qualifications (*)": q, "Departement": dep, "Chef dept validant (*)": "Chef de département"}
                           for (m, g, n, p, st, mat, q, dep) in ens])

    sal = [("SAL-01", "TP Simulation néonatologie", "Salle de TP", 12, "Mannequins néonatologie", "Bâtiment B"),
           ("SAL-02", "TP Simulation pédiatrie", "Salle de TP", 12, "Mannequins pédiatrie", "Bâtiment B"),
           ("SAL-03", "TP LMS", "Salle de TP", 16, "Postes informatiques", "Bâtiment A"),
           ("SAL-04", "TP Urgences réanimation", "Salle de TP", 12, "Mannequin réanimation", "Bâtiment B"),
           ("SAL-05", "TP Simulation accouchement", "Salle de TP", 10, "Mannequin accouchement", "Bâtiment B"),
           ("SAL-06", "TP Hémorragies gynéco-obstétrique", "Salle de TP", 10, "Simulateur obstétrical", "Bâtiment B"),
           ("SAL-07", "TP Soins de base", "Salle de TP", 16, "Lits, matériel de soins", "Bâtiment A"),
           ("SAL-08", "Amphi A", "Amphi", 120, "Vidéoprojecteur, sono", "Bâtiment principal"),
           ("SAL-09", "Salle de cours 1", "Salle de cours", 40, "Tableau, vidéoprojecteur", "Bâtiment A"),
           ("SAL-10", "Salle de cours 2", "Salle de cours", 40, "Tableau", "Bâtiment A")]
    add("L1_Salles", [{"ID salle": i, "Nom / libelle": nm, "Type (*)": ty, "Capacite": cap,
                       "Equipements (*)": eq, "Batiment / localisation (*)": bat}
                      for (i, nm, ty, cap, eq, bat) in sal])

    stg = [("CHN El-Maarouf", "Réanimation", "Moroni", "L3", 7), ("CHN El-Maarouf", "Chirurgie A", "Moroni", "L3", 5),
           ("CHN El-Maarouf", "Pédiatrie", "Moroni", "L2", 6), ("CHN El-Maarouf", "Salle d'accouchement", "Moroni", "L2", 6),
           ("PMI Mitsoudjé", "PMI", "Mitsoudjé", "L1", 4), ("HP Foumbouni", "Médecine", "Foumbouni", "L2", 4),
           ("CSD Mitsamiouli", "Soins", "Mitsamiouli", "L1", 4), ("CHRI Hombo", "Médecine", "Anjouan", "L3", 5),
           ("CHRI Fomboni", "Médecine", "Mohéli", "L3", 4), ("CS CARITAS", "Soins", "Moroni", "L1", 3)]
    add("S2_Lieux_stage", [{"Lieu / structure (*)": l, "Service (*)": s, "Commune (*)": c,
                            "Niveau concerne (*)": n, "Quota (*)": q, "Periode de disponibilite (*)": "Stage 1 à 3"}
                           for (l, s, c, n, q) in stg])

    ses = [("SES-01", "Soins infirmiers", "L1", "S.I", "Anatomie", "HAMIDI Said", "Amphi A", "Lundi", "08:00", "10:00", "CM"),
           ("SES-02", "Soins infirmiers", "L1", "S.I", "Microbiologie", "MAOULIDA Fatima", "Salle de cours 1", "Mardi", "10:00", "12:00", "CM"),
           ("SES-03", "Soins infirmiers", "L3", "S.I", "Pédiatrie", "ABDOU Ahamada", "TP Simulation pédiatrie", "Mercredi", "13:00", "15:00", "TP"),
           ("SES-04", "Soins obstétricaux", "L2", "S.O", "Obstétrique", "SAID Mariama", "TP Simulation accouchement", "Jeudi", "08:00", "10:00", "TP"),
           ("SES-05", "Maintenance biomédicale", "L1", "", "Maintenance biomédicale", "MZE Toihir", "Salle de cours 2", "Vendredi", "10:00", "12:00", "CM")]
    add("A3_Sessions", [{"ID session": sid, "Annee acad. (*)": "2025-2026", "Semestre": "S1", "Filiere": f,
                         "Niveau": n, "Section (*)": sec, "Matiere": mat, "Enseignant": e, "Salle": sa,
                         "Jour": j, "Heure debut": hd, "Heure fin": hf, "Type (*)": ty, "Vol. horaire prog. (*)": 2}
                        for (sid, f, n, sec, mat, e, sa, j, hd, hf, ty) in ses])

    add("F2_Comptes", [
        {"Nom du compte / caisse (*)": "Caisse principale EMSP", "Type (*)": "Caisse", "Solde initial (KMF) (*)": 799423},
        {"Nom du compte / caisse (*)": "Compte bancaire EMSP", "Type (*)": "Banque", "Solde initial (KMF) (*)": 1500000}])

    mv = [("01/02/2026", "Recette", "Inscriptions", "Droits d'inscription", "Espèces", "Caisse principale EMSP", "REC-001", "Frais d'inscription L1", 1575, 0, "Étudiants L1", "Fonds propres"),
          ("05/02/2026", "Dépense", "Fonctionnement", "Fournitures", "Espèces", "Caisse principale EMSP", "DEP-001", "Achat fournitures pédagogiques", 0, 800998, "Librairie Moroni", "Fonds propres"),
          ("10/02/2026", "Recette", "Partenaires", "Subvention", "Virement", "Compte bancaire EMSP", "REC-002", "Appui projet ODS", 5000000, 0, "Expertise France", "AFD"),
          ("15/02/2026", "Dépense", "Indemnités", "Vacations", "Virement", "Compte bancaire EMSP", "DEP-002", "Indemnités vacataires janvier", 0, 1200000, "Vacataires", "AFD")]
    add("F1_Mouvements", [{"Date operation": d, "Sens (*)": s, "Categorie (**)": cat, "Poste budgetaire (**)": pb,
                           "Mode paiement (*)": mp, "Compte / caisse (*)": cpt, "Reference / N piece (*)": ref,
                           "Libelle / description": lib, "Montant Recette (KMF)": mr, "Montant Depense (KMF)": md,
                           "Tiers (*)": t, "Statut (*)": "Validé", "Saisi par (*)": "formation",
                           "Source de financement / Bailleur (*)": bail}
                          for (d, s, cat, pb, mp, cpt, ref, lib, mr, md, t, bail) in mv])

    eqp = [("EQ-1", "Microscope binoculaire", "Materiel pedagogique", "TP LMS", "10/01/2024", "AFD", 350000, "En panne", "MIC-001", "Atelier réparation"),
           ("EQ-2", "Vidéoprojecteur", "Informatique", "Amphi A", "15/09/2023", "Fonds propres", 280000, "Actif", "VP-001", ""),
           ("EQ-3", "Mannequin nouveau-né (simulation)", "Materiel medical", "TP Simulation néonatologie", "20/03/2024", "AFD", 1200000, "Actif", "MAN-001", ""),
           ("EQ-4", "Lit médicalisé", "Materiel medical", "TP Soins de base", "05/06/2023", "Etat", 450000, "Hors service", "LIT-002", "Stockage"),
           ("EQ-5", "Ordinateur de bureau", "Informatique", "Salle de cours 1", "12/11/2023", "Fonds propres", 320000, "Actif", "ORD-005", ""),
           ("EQ-6", "Tensiomètre électronique", "Materiel medical", "TP Soins de base", "01/02/2024", "AFD", 85000, "En maintenance", "TEN-003", "")]
    add("M1_Equipements", [{"ID equipement (*)": i, "Designation (**)": d, "Categorie (**)": cat,
                            "Salle / localisation (**)": sa, "Date d'acquisition (**)": da,
                            "Source de financement / Bailleur (**)": b, "Montant (KMF) (**)": mt, "Etat (**)": et,
                            "N inventaire / serie (**)": ni, "Saisi par (*)": "formation", "Localisation provisoire (**)": lp}
                           for (i, d, cat, sa, da, b, mt, et, ni, lp) in eqp])

    add("L3_Besoins", [
        {"ID besoin (*)": "BES-1", "Date d'expression (**)": "16/06/2026", "Type de besoin (**)": "Matériel en panne",
         "Equipement concerne (**)": "EQ-1", "Libelle du besoin (**)": "Réparer ou remplacer le microscope binoculaire",
         "Quantite (**)": 1, "Localisation / salle (**)": "TP LMS", "Priorite (**)": "Haute", "Statut (**)": "Exprimé",
         "Cout estime (KMF) (**)": 350000, "Demandeur (**)": "Responsable TP", "Observations (**)": "Panne optique", "Saisi par (*)": "formation"},
        {"ID besoin (*)": "BES-2", "Date d'expression (**)": "16/06/2026", "Type de besoin (**)": "Consommable",
         "Libelle du besoin (**)": "Réassort gants et compresses", "Quantite (**)": 200, "Localisation / salle (**)": "TP Soins de base",
         "Priorite (**)": "Moyenne", "Statut (**)": "En cours", "Cout estime (KMF) (**)": 150000, "Demandeur (**)": "Surveillante",
         "Observations (**)": "Stock bas", "Saisi par (*)": "formation"}])

    add("G1_Plan_action", [
        {"N": 1, "Domaine / module": "Finances", "Ecart constate": "Retard de saisie des recettes d'inscription",
         "Action corrective": "Mettre à jour le registre chaque semaine", "Responsable": "Comptable",
         "Echeance": "30/06/2026", "Statut": "En cours", "Type d'écart": "Temporel"},
        {"N": 2, "Domaine / module": "Matériel", "Ecart constate": "Microscope LMS en panne",
         "Action corrective": "Expression de besoin déposée (BES-1)", "Responsable": "Responsable logistique",
         "Echeance": "15/07/2026", "Statut": "En cours", "Type d'écart": "Qualité"},
        {"N": 3, "Domaine / module": "Formation", "Ecart constate": "Volume horaire d'anatomie inférieur au prévu",
         "Action corrective": "Planifier des séances de rattrapage", "Responsable": "Chef de département",
         "Echeance": "31/07/2026", "Statut": "Non démarré", "Type d'écart": "Contenu de formation"}])

    add("H1_Biblio_docs", [
        {"Titre du document (**)": "Plan stratégique de l'EMSP 2026", "Type (**)": "Stratégique", "Reference (**)": "PS-2026",
         "Chemin / lien local (*)": "C:\\EMSP\\Documents\\plan_strategique_2026.pdf", "Date de mise a jour (**)": "01/02/2026", "Responsable mise a jour (**)": "Direction"},
        {"Titre du document (**)": "Règlement général des études (Décret 05-106)", "Type (**)": "Réglementaire / officiel", "Reference (**)": "Décret 05-106/PR",
         "Chemin / lien local (*)": "C:\\EMSP\\Documents\\decret_05-106.pdf", "Date de mise a jour (**)": "28/11/2005", "Responsable mise a jour (**)": "Scolarité"},
        {"Titre du document (**)": "Recommandations OMS — soins infirmiers", "Type (**)": "OMS / international", "Reference (**)": "OMS-SI-2024",
         "Chemin / lien local (*)": "C:\\EMSP\\Documents\\oms_soins_infirmiers.pdf", "Date de mise a jour (**)": "20/02/2026", "Responsable mise a jour (**)": "Direction"},
        {"Titre du document (**)": "Protocole de prise en charge du paludisme", "Type (**)": "Médical", "Reference (**)": "PROT-PALU-03",
         "Chemin / lien local (*)": "C:\\EMSP\\Documents\\protocole_paludisme.pdf", "Date de mise a jour (**)": "15/03/2026", "Responsable mise a jour (**)": "Dr référent"},
        {"Titre du document (**)": "Support de cours — Anatomie L1", "Type (**)": "Supports de cours", "Reference (**)": "SC-ANAT-L1",
         "Chemin / lien local (*)": "C:\\EMSP\\Documents\\cours_anatomie_L1.pdf", "Date de mise a jour (**)": "05/02/2026", "Responsable mise a jour (**)": "Enseignant"}])

    print("Seed de formation termine sur :", chemin)


if __name__ == "__main__":
    seed(sys.argv[1] if len(sys.argv) > 1 else None)
