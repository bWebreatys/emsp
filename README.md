# EMSP - École de Médecine et Santé Publique

## 📋 Description

Outil de gestion administrative, académique et financière pour l'École de Médecine et de Santé Publique (EMSP) aux Comores.

**Statut:** Version 0.1 - Prototype pour élicitation et discussion

### Fonctionnalités couvertes

- **Gestion académique** : Planification des cours, occupation des salles
- **Gestion des étudiants** : Inscriptions, parcours, résultats
- **Gestion des formations** : Référentiel des formations et sessions
- **Gestion des formateurs** : Suivi des enseignants et vacataires
- **Suivi financier** : Droits d'inscription, indemnités, dépenses
- **Calendrier visuel** : Vue mensuelle et vue journalière
- **Tableaux de bord** : KPIs activité, finance, RH

## 🚀 Démarrage rapide

### Prérequis
- Python 3.8+
- Flask
- openpyxl

### Installation
```bash
# 1. Cloner le repo
git clone https://github.com/bWebreatys/emsp.git
cd emsp

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python lancer_application.py

# 4. Ouvrir le navigateur
# http://127.0.0.1:5000
```

## 📁 Structure du projet

```
emsp/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── EMSP_v0.1.xlsx                    # Données (évolutif)
├── app.py                            # Serveur Flask
├── lancer_application.py             # Lanceur avec ouverture navigateur
├── data-models/
│   ├── data-dictionary.md            # Dictionnaire des données
│   ├── process-flows.md              # Flux de processus
│   └── screen-mockups.md             # Maquettes des écrans
├── documentation/
│   ├── EMSP-guide-utilisateur.docx   # Guide utilisateur
│   ├── EMSP-guide-admin.docx         # Guide administrateur
│   └── formules-emsp.txt             # Formules Excel
└── templates/
    ├── base.html                     # Layout principal
    ├── index.html                    # Tableau de bord
    ├── sheet_list.html               # Listes de données
    ├── sheet_form.html               # Formulaires de saisie
    ├── formules.html                 # Documentation formules
    └── ...
```

## 📊 Onglets Excel - Données

| Onglet | Description | Statut |
|--------|-------------|--------|
| **ACCUEIL** | Navigation principale | ✅ |
| **FORMATIONS** | Référentiel des formations | ✅ |
| **SALLES** | Référentiel des salles | ✅ |
| **FORMATEURS_RH** | Gestion des formateurs | ✅ |
| **SESSIONS** | Planification des sessions | ✅ |
| **INTERVENTIONS** | Détails des interventions | ✅ |
| **RESERVATIONS** | Réservations salle/date | ✅ |
| **DEPENSES** | Suivi financier | ✅ |
| **BILANS** | Tableaux de bord | ✅ |

## 🎯 Points clés pour l'élicitation

### Données actuellement modélisées
- ✅ Formations (code, titre, durée, nb max participants)
- ✅ Salles (code, capacité, équipements)
- ✅ Formateurs (nom, spécialité, disponibilités)
- ✅ Sessions (dates, lieu, formateurs, taux de réalisation)
- ✅ Dépenses (type, montant, responsable, validé)

### À clarifier sur place
- ⚠️ **Processus d'inscription** : Comment gère-t-on les demandes préalables ? Approuvation manuelle ?
- ⚠️ **Suivi académique** : Quels résultats/notes à tracker ? Contrôle continu, exam final ?
- ⚠️ **Gestion financière** : Quel niveau de détail ? Paie des intervenants, frais de structure ?
- ⚠️ **Reporting** : Quels indicateurs clés pour la direction ?
- ⚠️ **Intégration** : Connexion nécessaire avec un système RH ou financier existant ?

## 🔧 Configuration

### Base de données
L'outil utilise un **fichier Excel structuré** (pas de base de données SQL). La structure peut évoluer sans code.

### Utilisateurs
- **Admin** : accès complet, modification des paramètres, sauvegarde
- **Formateurs** : création/modif de leurs sessions
- **Administratifs** : saisie de toutes les données
- **Direction** : consultation des tableaux de bord

## 📝 Notes de développement

- **Version** : 0.1 (prototype)
- **Framework** : Flask (Python web framework léger)
- **Base données** : Excel (openpyxl)
- **Interface** : HTML/CSS/JavaScript
- **Déploiement** : Local ou serveur Windows/Linux
- **Adaptabilité** : Structure complètement flexible, aucune donnée "en dur"

## 🤝 Élicitation et feedback

Pour collecter les remarques lors de la mission aux Comores :

1. **Présentez les écrans** tels qu'ils sont maintenant (version 0.1)
2. **Montrez le fichier Excel** avec les onglets actuels
3. **Demandez pour chaque onglet** :
   - Colonnes manquantes ?
   - Colonnes inutiles ?
   - Données qui doivent être liées ?
   - Validations à mettre en place ?
4. **Présentez les écrans** et demandez si l'ergonomie convient
5. **Collectez les changements** et mettez à jour sur GitHub

## 📞 Support

Bernard Leglise - Webcreatys SAS
contact@webcreatys.com

---

**Dernière mise à jour** : 22 mai 2026
**Prochaines étapes** : Élicitation sur place (juin-juillet 2026)
