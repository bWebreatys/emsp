# 📥 Télécharger et Installer en Local

**Guide complet pour récupérer tous les travaux depuis GitHub**

---

## 🎯 Vue d'ensemble

Tu as deux options :

1. **Option A : Git (recommandé)** - Cloner les repos
2. **Option B : ZIP (simple)** - Télécharger ZIP manuellement

Les deux donnent exactement le même résultat.

---

## OPTION A : AVEC GIT (Recommandé)

### Prérequis

```
✅ Git installé : https://git-scm.com/download
✅ Terminal/PowerShell
✅ Dossier vide pour les projets
```

### Étape 1 : Installer Git (si pas fait)

**Windows** :
```
1. Aller sur https://git-scm.com/download/win
2. Télécharger "Git for Windows"
3. Installer (tout par défaut OK)
4. Redémarrer PowerShell
5. Vérifier : git --version
```

**Mac** :
```
brew install git
```

**Linux** :
```
sudo apt-get install git
```

### Étape 2 : Cloner EMSP

```bash
# Créer dossier
mkdir ~/webcreatys-projects
cd ~/webcreatys-projects

# Cloner EMSP
git clone https://github.com/bWebreatys/emsp.git

# Résultat
emsp/
├── app.py
├── EMSP_v0.1.xlsx
├── requirements.txt
├── README.md
├── USER-MANAGEMENT.md
├── BACKUP-RESTORE-STRATEGY.md
├── CORRUPTION-RECOVERY.md
└── ... (tous les documents)
```

### Étape 3 : Cloner GMAO

```bash
# Cloner GMAO
git clone https://github.com/bWebreatys/gmao.git

# Résultat : même structure que EMSP
gmao/
├── app.py
├── GMAO_v0.1.xlsx
├── requirements.txt
└── ... (tous les documents)
```

### Étape 4 : Vérifier structure

```bash
cd emsp
ls -la

# Vous devez voir :
# -rw-r--r-- app.py
# -rw-r--r-- EMSP_v0.1.xlsx
# -rw-r--r-- requirements.txt
# -rw-r--r-- README.md
# -rw-r--r-- QUICK-START.md
# -rw-r--r-- PREREQUISITES.md
# ... + 17 autres documents
```

---

## OPTION B : TÉLÉCHARGER EN ZIP (Simple)

### Étape 1 : Aller sur GitHub

**Pour EMSP** :
```
1. Ouvrir https://github.com/bWebreatys/emsp
2. Cliquer bouton vert "Code" (en haut à droite)
3. Cliquer "Download ZIP"
4. Fichier "emsp-main.zip" téléchargé
```

**Pour GMAO** :
```
1. Ouvrir https://github.com/bWebreatys/gmao
2. Cliquer bouton vert "Code"
3. Cliquer "Download ZIP"
4. Fichier "gmao-main.zip" téléchargé
```

### Étape 2 : Décompresser

**Windows** :
```
1. Dossier de téléchargement
2. Clic droit emsp-main.zip
3. "Extract All..."
4. Choisir destination : C:\webcreatys\
5. OK
```

**Mac/Linux** :
```bash
unzip ~/Downloads/emsp-main.zip -d ~/webcreatys/
unzip ~/Downloads/gmao-main.zip -d ~/webcreatys/
```

### Étape 3 : Renommer dossier (optionnel)

```bash
# Le dossier s'appelle "emsp-main"
# Renommer en "emsp" (plus simple)

mv emsp-main emsp
mv gmao-main gmao
```

---

## ✅ VÉRIFIER TÉLÉCHARGEMENT

### Lister fichiers

```bash
# EMSP
cd emsp
ls -la

# Devez voir :
app.py                          ← Code Flask
EMSP_v0.1.xlsx                 ← Données
requirements.txt               ← Dépendances Python
README.md                       ← Vue d'ensemble
QUICK-START.md                  ← Installation rapide
PREREQUISITES.md                ← Prérequis détaillés
INSTALLATION-STEP-BY-STEP.md    ← Pas à pas
INSTALLATION-VISUAL-GUIDE.txt   ← Diagrammes ASCII
FINAL-SUMMARY.md                ← Résumé exécutif
INSTALLATION-SUMMARY.md         ← Résumé installation
USER-MANAGEMENT.md              ← Gestion utilisateurs
DROPDOWN-LISTS-MANAGEMENT.md    ← Listes déroulantes
CONCURRENT-ACCESS-CONTROL.md    ← Accès concurrent
ON-SITE-SETUP-GUIDE.md          ← Configuration jour 1-3
BACKUP-RESTORE-STRATEGY.md      ← Sauvegarde/restauration
CORRUPTION-RECOVERY.md          ← Gestion corruptions
lancer_application.py           ← Script de lancement
emsp_app/                       ← Dossier Flask
  ├── templates/                ← Écrans HTML
  └── ...
backups/                        ← Dossier sauvegardes (créé auto)
```

### Vérifier téléchargement complètement

```bash
# Compter fichiers
find . -type f | wc -l

# Emsp devrait avoir : ~25+ fichiers
# Gmao devrait avoir : ~25+ fichiers

# Chercher fichiers critiques
ls -la app.py
ls -la *_v0.1.xlsx
ls -la requirements.txt
ls -la README.md
```

---

## 🚀 INSTALLATION LOCALE (45 min)

### Étape 1 : Créer virtual environment

```bash
cd ~/webcreatys/emsp

# Créer venv
python -m venv venv

# Activer (Windows)
.\venv\Scripts\Activate.ps1

# Activer (Mac/Linux)
source venv/bin/activate

# Vous verrez : (venv) au début du prompt
```

### Étape 2 : Installer dépendances

```bash
# Doit être dans emsp/ avec venv activé
pip install -r requirements.txt

# Résultat attendu :
# Successfully installed Flask-2.3.0 openpyxl-3.10.0 ...
```

### Étape 3 : Tester en local

```bash
# Toujours dans emsp/ avec venv activé
python app.py

# Résultat :
# WARNING: This is a development server...
# Running on http://127.0.0.1:5000
# Press CTRL+C to quit
```

### Étape 4 : Ouvrir dans navigateur

```
Navigateur web → http://127.0.0.1:5000
```

**Vous devez voir** :
- Page d'accueil EMSP
- Listes des onglets (FORMATIONS, SALLES, etc.)
- Écrans de saisie fonctionnels

### Étape 5 : Arrêter l'app

```bash
# Dans le terminal
CTRL+C

# Ou Cmd+C sur Mac
```

---

## 📂 STRUCTURE LOCAL

Après installation, vous avez :

```
~/webcreatys/
│
├── emsp/                       ← Projet EMSP
│   ├── venv/                   ← Virtual environment
│   ├── app.py                  ← Code Flask
│   ├── EMSP_v0.1.xlsx          ← Données
│   ├── requirements.txt        ← Dépendances
│   ├── emsp_app/               ← Dossier Flask
│   │   ├── templates/          ← Écrans HTML
│   │   └── ...
│   ├── backups/                ← Sauvegardes
│   └── *.md files              ← 17 documents
│
├── gmao/                       ← Projet GMAO
│   ├── venv/                   ← Virtual environment
│   ├── app.py                  ← Code Flask
│   ├── GMAO_v0.1.xlsx          ← Données
│   ├── requirements.txt        ← Dépendances
│   ├── gmao_app/               ← Dossier Flask
│   │   ├── templates/          ← Écrans HTML
│   │   └── ...
│   ├── backups/                ← Sauvegardes
│   └── *.md files              ← 17 documents
│
└── README_LOCAL.txt            ← Ce fichier
```

---

## 📖 LIRE LES DOCUMENTS (TRÈS IMPORTANT)

### Ordre recommandé

**Jour 1 : Comprendre structure**

1. **README.md** (5 min)
   - Vue générale du projet
   - Quoi et pourquoi

2. **QUICK-START.md** (20 min)
   - Installation rapide
   - Démarrage app

3. **FINAL-SUMMARY.md** (10 min)
   - Réponses aux 5 questions clés
   - Architecture réseau

**Jour 2 : Approfondissement**

4. **PREREQUISITES.md** (30 min)
   - Détails Python, versions, droits
   - Troubleshooting

5. **USER-MANAGEMENT.md** (20 min)
   - Gestion utilisateurs (5 rôles)
   - Matrice de droits

6. **DROPDOWN-LISTS-MANAGEMENT.md** (20 min)
   - Listes déroulantes
   - Éviter les inventions

7. **CONCURRENT-ACCESS-CONTROL.md** (20 min)
   - Verrous (🔴/✅)
   - Accès concurrent

**Jour 3 : Maintenance**

8. **BACKUP-RESTORE-STRATEGY.md** (20 min)
   - Sauvegarde (3 niveaux)
   - Restauration

9. **CORRUPTION-RECOVERY.md** (20 min)
   - Diagnostic corruptions
   - Solutions

10. **ON-SITE-SETUP-GUIDE.md** (30 min)
    - Timeline jour 1-3 aux Comores
    - Checklists

---

## 🔄 SYNCHRONISER AVEC GITHUB

Si vous modifiez localement et voulez récupérer les mise à jour :

```bash
cd emsp

# Récupérer dernières modifs
git pull origin main

# Résultat :
# Already up to date.
# (Ou liste des fichiers mis à jour)
```

---

## 🚨 PROBLÈMES FRÉQUENTS

### Problème 1 : "git: command not found"

```
Cause : Git pas installé
Solution : Installer Git (voir section Prérequis)
```

### Problème 2 : "Module not found: openpyxl"

```
Cause : requirements.txt pas installé
Solution : 
  pip install -r requirements.txt
```

### Problème 3 : "Port 5000 already in use"

```
Cause : Autre app utilise port 5000
Solution : 
  1. Fermer autre app utilisant port 5000
  2. Ou modifier app.py : port=5001
```

### Problème 4 : Fichier Excel "cannot open"

```
Cause : Possible corruption
Solution :
  1. Vérifier téléchargement complet
  2. Télécharger à nouveau depuis GitHub
  3. Lire CORRUPTION-RECOVERY.md
```

### Problème 5 : "Permission denied" (Linux/Mac)

```
Cause : Droits d'accès insuffisants
Solution :
  chmod -R 755 ~/webcreatys/emsp
  chmod -R 755 ~/webcreatys/gmao
```

---

## ✅ CHECKLIST TÉLÉCHARGEMENT

- [ ] Git installé (ou ZIP téléchargé)
- [ ] emsp/ et gmao/ cloné/téléchargé
- [ ] Fichiers vérifiés (ls -la)
- [ ] 25+ fichiers dans chaque dossier
- [ ] app.py visible
- [ ] *_v0.1.xlsx présent
- [ ] requirements.txt lisible
- [ ] Virtual environment créé
- [ ] Dépendances installées (pip install -r)
- [ ] App testée en local (python app.py)
- [ ] http://127.0.0.1:5000 fonctionne
- [ ] Documents lus (au moins README)

---

## 📞 SUPPORT LOCAL

**Si téléchargement pose problème** :

1. Vérifier connexion internet
2. Essayer avec navigateur différent
3. Essayer Option B (ZIP manuel)
4. Appeler Bernard : contact@webcreatys.com

---

## 🎯 PROCHAINES ÉTAPES

Après avoir installé localement :

1. **Tester l'app** (30 min)
   - Ajouter données test
   - Modifier données
   - Tester écrans

2. **Lire tous les documents** (3-4 heures)
   - Comprendre architecture
   - Préparer mission

3. **Préparer mission** (1 jour)
   - Imprimer checklists
   - Préparer listes d'équipes
   - Tester procédures

4. **Départ Comores** (juin 2026)
   - Laptops + fichiers
   - Documents imprimés
   - Token GitHub accessible

---

**Version** : 22 mai 2026
**Audience** : Bernard + équipes techniques
**Temps total** : 1-2 heures (téléchargement + installation)
