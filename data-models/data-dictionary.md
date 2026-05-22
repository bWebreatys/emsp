# Dictionnaire des Données - EMSP

## Vue d'ensemble

L'outil EMSP gère 9 onglets Excel interconnectés pour la gestion administrative, académique et financière.

## 🎓 Onglet FORMATIONS

**Description** : Référentiel des formations proposées

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Formation | Texte | Identifiant unique (ex: MED001) | ✅ |
| Titre | Texte | Nom complet de la formation | ✅ |
| Durée_Jours | Nombre | Durée en jours | ✅ |
| Nb_Max_Participants | Nombre | Capacité maximale d'étudiants | ✅ |
| Objectifs_Généraux | Texte long | Description des objectifs | ⚠️ |
| Pré-requis | Texte | Conditions d'accès | ⚠️ |
| Statut | Dropdown | Actif / Archivé | ✅ |

**À clarifier** :
- [ ] Existe-t-il des catégories de formations (Licence, Master, Spécialisation) ?
- [ ] Faut-il tracker les crédits ECTS ou equivalent ?
- [ ] Quels sont les pré-requis les plus courants ?

---

## 🏫 Onglet SALLES

**Description** : Référentiel des locaux de formation

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Salle | Texte | Identifiant unique (ex: SALLE_101) | ✅ |
| Localisation | Texte | Bâtiment/étage (ex: Bât A, 1er étage) | ✅ |
| Capacité | Nombre | Nombre de places assises | ✅ |
| Type_Salle | Dropdown | Amphithéâtre / Salle de cours / TP | ✅ |
| Équipements | Texte | Vidéoprojecteur, Tableau blanc, Microscopes | ⚠️ |
| Resp_Salle | Texte | Responsable de maintenance | ⚠️ |
| Observations | Texte | Remarques | ⚠️ |
| Statut | Dropdown | Disponible / En maintenance / Fermée | ✅ |

**À clarifier** :
- [ ] Quels sont les équipements critiques pour chaque type de salle ?
- [ ] Y a-t-il une personne responsable par salle ?
- [ ] Comment gère-t-on les salles en maintenance ?

---

## 👥 Onglet FORMATEURS_RH

**Description** : Gestion des enseignants et intervenants

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Formateur | Texte | Identifiant unique | ✅ |
| Nom_Prenom | Texte | Nom et prénom | ✅ |
| Spécialité | Texte | Domaine de compétence | ✅ |
| Email | Texte | Adresse email | ⚠️ |
| Téléphone | Texte | Numéro de contact | ⚠️ |
| Statut | Dropdown | Permanent / Vacataire / Partenaire | ✅ |
| Heures_Max_S1 | Nombre | Heures max disponibles semaine 1 | ⚠️ |
| Disponibilité | Texte | Créneau horaires préférés | ⚠️ |

**À clarifier** :
- [ ] Comment gère-t-on les contrats (CDI, CDD, vacation) ?
- [ ] Faut-il tracker les heures effectuées vs prévues ?
- [ ] Y a-t-il un système de paie intégré ?

---

## 📅 Onglet SESSIONS

**Description** : Planification des cours (instances de formations)

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Session | Texte | Identifiant unique (ex: MED001_JAN2026) | ✅ |
| Code_Formation | FK | Lien vers FORMATIONS | ✅ |
| Date_Debut | Date | Date de démarrage (JJ/MM/AAAA) | ✅ |
| Date_Fin | Date | Date de fin (JJ/MM/AAAA) | ✅ |
| Code_Salle | FK | Lien vers SALLES | ✅ |
| Code_Formateur | FK | Lien vers FORMATEURS_RH | ✅ |
| Nb_Inscrits | Nombre | Nombre d'étudiants inscrits | ⚠️ |
| Lieu_Principal | Texte | Localisation principale | ✅ |
| Taux_Réalisation | % | % de sessions effectuées | ⚠️ |
| Statut | Dropdown | Planifiée / En cours / Terminée / Annulée | ✅ |

**À clarifier** :
- [ ] Comment gère-t-on les sessions qui s'étalent sur plusieurs jours ?
- [ ] Peut-on changer de salle en cours de session ?
- [ ] Comment calcule-t-on le taux de réalisation ?

---

## 🎯 Onglet INTERVENTIONS

**Description** : Détail des interventions (séances) pour chaque session

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Intervention | Texte | Identifiant unique | ✅ |
| Code_Session | FK | Lien vers SESSIONS | ✅ |
| Date_Intervention | Date | Date (JJ/MM/AAAA) | ✅ |
| Heure_Debut | Heure | Format HH:MM | ✅ |
| Heure_Fin | Heure | Format HH:MM | ✅ |
| Code_Formateur | FK | Formateur effectif | ✅ |
| Code_Salle | FK | Salle utilisée | ✅ |
| Nb_Présents | Nombre | Nombre d'étudiants présents | ⚠️ |
| Description | Texte | Sujet du cours | ⚠️ |
| Statut | Dropdown | Prévue / Effectuée / Reportée / Annulée | ✅ |

**À clarifier** :
- [ ] Faut-il tracker la présence étudiant ?
- [ ] Peut-on avoir des changements de formateur/salle ?
- [ ] Comment gère-t-on les reportages ?

---

## 📍 Onglet RESERVATIONS

**Description** : Réservations de salles (suivi occupation)

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Reservation | Texte | Identifiant unique | ✅ |
| Code_Salle | FK | Salle réservée | ✅ |
| Date_Reservation | Date | Date concernée (JJ/MM/AAAA) | ✅ |
| Heure_Debut | Heure | Début du créneau (HH:MM) | ✅ |
| Heure_Fin | Heure | Fin du créneau (HH:MM) | ✅ |
| Code_Session | FK | Session liée (peut être null) | ⚠️ |
| Responsable | Texte | Personne ayant réservé | ✅ |
| Durée | Nombre | Durée en heures (calculée) | ⚠️ |
| Capacité_Salle | Nombre | Capacité de la salle (lookup) | ⚠️ |
| Motif | Texte | Raison de la réservation | ⚠️ |
| Statut | Dropdown | Confirmée / En attente / Annulée | ✅ |

**À clarifier** :
- [ ] Faut-il gérer des salles réservées hors sessions (réunions, etc) ?
- [ ] Comment gère-t-on les chevauchements ?
- [ ] Y a-t-il un système d'approbation ?

---

## 💰 Onglet DEPENSES

**Description** : Suivi financier et budgétaire

| Colonne | Type | Description | Requis |
|---------|------|-------------|--------|
| Code_Dépense | Texte | Identifiant unique | ✅ |
| Date_Dépense | Date | Date d'engagement (JJ/MM/AAAA) | ✅ |
| Type_Dépense | Dropdown | Indemnité / Fourniture / Infrastructure / Autre | ✅ |
| Montant | Devise | En GKF (francs comoriens) | ✅ |
| Responsable | Texte | Personne ayant engagé | ✅ |
| Code_Formation | FK | Formation concernée (optionnel) | ⚠️ |
| Description | Texte | Détail de la dépense | ⚠️ |
| Exercice_Budgétaire | Texte | Année (ex: 2026-2027) | ✅ |
| Validé_par | Texte | Approbateur (directeur, finance) | ⚠️ |
| Statut | Dropdown | Engagée / Validée / Payée / Rejetée | ✅ |

**À clarifier** :
- [ ] Quel est le budget annuel par type de dépense ?
- [ ] Qui approuve les dépenses (montants seuils) ?
- [ ] Faut-il un lien avec un système comptable existant ?

---

## 📊 Onglet BILANS

**Description** : Tableaux de bord et indicateurs clés (lectures seules)

| Indicateur | Formule | Description |
|-----------|---------|-------------|
| Nb_Sessions_Actives | COUNTIF | Sessions en cours ce mois |
| Nb_Formations_Actives | COUNTIF | Formations en cours |
| Nb_Etudiants_Total | SUM | Étudiants inscrits (tous onglets) |
| Nb_Interventions_Mois | COUNTIF | Séances ce mois |
| Taux_Occupation_Salles | AVG | Moyenne occupation salles |
| Budget_Engagé_Mois | SUM | Total dépenses ce mois |
| Budget_Restant | Calcul | Budget - Engagé |

**À clarifier** :
- [ ] Quels indicateurs sont prioritaires pour la direction ?
- [ ] À quel rythme les rapports doivent-ils être actualisés ?
- [ ] Faut-il des comparaisons historiques (année sur année) ?

---

## 🔗 Relations entre onglets

```
FORMATIONS (1) ──many── (n) SESSIONS
                                │
                                ├──> SALLES (1 salle par session)
                                │
                                └──> FORMATEURS_RH (1 formateur principal)

SESSIONS (1) ──many── (n) INTERVENTIONS
                                │
                                ├──> SALLES (peut changer)
                                │
                                └──> FORMATEURS_RH (peut changer)

SALLES ──many── RESERVATIONS
                        │
                        └──> FORMATIONS (optionnel)

FORMATIONS ──many── DEPENSES
FORMATEURS_RH ──many── DEPENSES
```

---

## ⚠️ À clarifier lors de la mission

1. **Flux d'admission** : Y a-t-il un processus de sélection des étudiants ?
2. **Notes et résultats** : Faut-il tracker les notes ? Quel système (notation, points, pourcentages) ?
3. **Diplômes** : Comment gère-t-on la délivrance de certificats/diplômes ?
4. **Intégration financière** : Lien avec un système comptable existant ?
5. **Utilisateurs** : Qui doit avoir accès à quoi (administratif, formateurs, direction) ?
6. **Rapports** : Format et fréquence des reportings demandés ?
7. **Archivage** : Durée de conservation des données ? Besoin d'audit trails ?
