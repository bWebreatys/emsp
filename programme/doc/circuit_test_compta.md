# Circuit de test — chaîne heures enseignants → paiement → comptabilité (EMSP)

> Document de recette (P1-C, V1.99.52). À dérouler par l'EMSP avec des données
> réelles, connecté avec un compte disposant de l'**accès financier**.
> Référentiel des comptes : écran **Comptes & caisses (F2)** — c'est lui qui
> alimente les sélecteurs de compte partout dans l'application. Les deux comptes
> réels y figurent : **Compte bancaire UDC-EMSP-ODS (BIC-Comores)**
> (n° 00002130706001KMF, journaux et rapprochements bancaires EMSP) et
> **Caisse EMSP**. Nomenclature des postes chargée ; poste par défaut des
> vacations : **642 — Cours complémentaires (heures supplémentaires)**
> (modifiable au passage en compta).
> Les soldes initiaux (F2) et toutes les écritures réelles restent à saisir par l'EMSP.

## Étape 0 — Pré-requis
1. Écran **Comptes & caisses (F2)** : renseigner le **solde initial** de chaque
   compte (banque et caisse). La colonne « Solde courant » est calculée, ne pas la saisir.
2. Écran **Séances (A3)** : le planning réel est chargé (V1.99.51) ; vérifier
   l'**enseignant** des séances concernées (complété automatiquement quand la matière
   ne correspond qu'à un seul enseignant, sinon à renseigner).

## Étape 1 — Présences → heures constatées
1. **Présences** : choisir la classe et la date, saisir la feuille de la séance
   (créneau + durée). Chaque saisie alimente les heures constatées de l'enseignant.
2. Contrôle : écran **Heures constatées (E3)** — les heures de la séance apparaissent
   pour l'enseignant, au mois concerné.

## Étape 2 — Report d'heures (E2)
1. Écran **Relevé d'heures** : reporter les heures constatées vers E2. Tout écart
   entre constaté et reporté exige un **motif** (traçabilité AFD).
2. Contrôle : le relevé individuel de l'enseignant (Impressions > Relevé individuel)
   affiche les heures du mois ; le récapitulatif mensuel totalise tous les enseignants.

## Étape 3 — Constitution de l'état de paiement (E4)
1. Écran **États de paiement** : constituer l'état du semestre (identifiant
   `PAIE-<année>-<semestre>`). Chaque ligne = un enseignant : heures × taux,
   plafond appliqué le cas échéant, total arrêté **en toutes lettres**.
2. Contrôle : le total de l'état = somme des lignes ; statut **Brouillon**.

## Étape 4 — Arrêté
1. Bouton **Arrêter l'état** : le statut passe à **Arrêté**, la date d'arrêté et
   l'auteur sont posés. L'état n'est plus modifiable.
2. Garde-fous à vérifier : impossible d'arrêter deux fois ; impossible de passer
   en compta un état encore en Brouillon.

## Étape 5 — Passage en comptabilité
1. Bouton **Passer en compta** : choisir le **compte / caisse** (liste des comptes
   réels), le **mode de paiement**, et confirmer le **poste budgétaire**
   (défaut : 642). L'application écrit **une dépense F1 par enseignant**, toutes
   portant la référence commune `PAIE-<n>`.
2. Garde-fous à vérifier : un second clic est refusé (**anti-double-passage**,
   l'état est « Passé en compta ») ; un état non arrêté est refusé.

## Étape 6 — Contrôles comptables
1. Écran **Trésorerie / F1** : filtrer sur la référence `PAIE-<n>` — une ligne de
   dépense par enseignant, poste 642, compte choisi, `Saisi par` renseigné
   automatiquement, source de financement portée par mouvement.
2. Écran **Comptes & caisses (F2)** : le **solde courant** du compte choisi a diminué
   du total de l'état.
3. **Journal** (`journal.csv`) : l'opération de passage est horodatée avec l'auteur.
4. Impressions financières : « Recettes/dépenses par poste budgétaire » et « État
   par source de financement » reflètent les nouvelles dépenses (reporting AFD).

## Étape 7 — Cas limites à tester
- Régularisation d'un mouvement F1 : exiger le **motif** (refus sans motif).
- Enseignant à 0 heure : absent de l'état (aucune dépense à 0).
- Deux semestres : deux états distincts `PAIE-<année>-S1` et `-S2`, références séparées.

---
*Toute anomalie constatée est à remonter avec la copie d'écran et la référence
`PAIE-<n>` concernée.*
