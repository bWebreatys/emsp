# 🚀 Installation étape par étape - EMSP

## 📌 Objectif
Installer et lancer l'application EMSP sur un serveur Windows/Linux aux Comores.

**Durée estimée** : 45 minutes (sur réseau stable)

---

## Phase 1 : Préparation (5 minutes)

### Étape 1.1 : Vérifier Python

```powershell
# Windows PowerShell
python --version

# Résultat attendu :
# Python 3.10.5  ✅ OK
# Python 3.8.10  ✅ OK
# Python 3.12.0  ⚠️ Possiblement OK, à tester
# Python 2.7.x   ❌ REFUSER
```

**Si aucun Python n'est trouvé** : Installer Python 3.10 depuis https://www.python.org/downloads/
- Télécharger "Windows installer (64-bit)"
- ✅ Cocher "Add Python to PATH"
- ✅ Cocher "Install for all users"
- Redémarrer PowerShell après installation

### Étape 1.2 : Vérifier pip (gestionnaire de packages)

```powershell
pip --version

# Résultat attendu :
# pip 23.0 from C:\Python310\lib\site-packages...  ✅
```

**Si pip ne fonctionne pas** : C'est rare. Réinstaller Python avec "Add Python to PATH".

### Étape 1.3 : Trouver un endroit pour installer l'app

```powershell
# Créer un dossier dédié
mkdir C:\emsp_school
cd C:\emsp_school

# Vérifier qu'on est au bon endroit
pwd  # Affiche : C:\Users\[user]\emsp_school
```

**⚠️ Important** : Ne pas installer dans des chemins avec accents ou espaces
- ❌ C:\Mes Programmes\EMSP
- ❌ C:\Utilisateurs Admin\Bureau\EMSP  
- ✅ C:\emsp_school
- ✅ C:\data\emsp

---

## Phase 2 : Télécharger l'application (10 minutes)

### Étape 2.1 : Cloner depuis GitHub

```powershell
# Option A : Avec Git (si installé)
git clone https://github.com/bWebreatys/emsp.git .

# Option B : Télécharger le ZIP
# Aller sur https://github.com/bWebreatys/emsp
# Cliquer "Code" → "Download ZIP"
# Décompresser dans C:\emsp_school\
```

### Étape 2.2 : Vérifier les fichiers

```powershell
# Depuis C:\emsp_school\
ls
# Vous devez voir :
# Mode   Name
# ----   ----
# d----   emsp_app
# -a---   app.py
# -a---   EMSP_v0.1.xlsx
# -a---   requirements.txt
# -a---   README.md
```

### Étape 2.3 : Vérifier les fichiers Excel

```powershell
# Tester que le fichier Excel s'ouvre
# Cliquer droit sur EMSP_v0.1.xlsx → "Ouvrir avec" → Excel
# Vérifier les 9 onglets : FORMATIONS, SALLES, etc.
```

**Si Excel ne s'ouvre pas** :
- Installer Microsoft Excel ou LibreOffice Calc gratuit
- Ou utiliser Google Sheets (télécharger xlsx puis réupload)

---

## Phase 3 : Installer les dépendances Python (15 minutes)

### ⚠️ Attention : Virtual Environment (TRÈS RECOMMANDÉ)

Un "virtual environment" isole les packages de votre app pour éviter les conflits.

#### Option A : AVEC virtual environment (RECOMMANDÉ)

```powershell
# Créer un environnement virtuel
python -m venv venv

# L'activer
.\venv\Scripts\Activate.ps1
# Vous verrez : (venv) C:\emsp_school>

# Installer les packages
pip install -r requirements.txt

# Vérifier
pip list
# Vous devez voir : Flask, openpyxl, python-dateutil
```

**Avantages** :
- ✅ Isolé (ne touche pas aux packages globaux)
- ✅ Reproductible (autre PC = même versions)
- ✅ Facile à réinitialiser (supprimer dossier `venv`)

#### Option B : SANS virtual environment (RAPIDE mais risqué)

```powershell
# Installer directement
pip install -r requirements.txt
```

**Risques** :
- ❌ Peut entrer en conflit avec autres apps
- ❌ Si quelqu'un met à jour pip, peut casser l'app
- ❌ Difficile à nettoyer après

### Étape 3.1 : Installation

```powershell
# Depuis C:\emsp_school\ (avec venv activé si choisi)

pip install -r requirements.txt

# Résultat attendu :
# Successfully installed Flask-2.3.0 openpyxl-3.10.0 ...
```

### Étape 3.2 : Vérifier installation

```powershell
pip list | grep -E "Flask|openpyxl|python-dateutil"

# Résultat :
# Flask          2.3.0
# openpyxl       3.10.0
# python-dateutil 2.8.2
```

---

## Phase 4 : Tester en local (10 minutes)

### Étape 4.1 : Lancer l'application

```powershell
# Depuis C:\emsp_school\ (avec venv activé si créé)
python app.py

# Résultat attendu :
# WARNING: This is a development server. Do not use it in production.
# Running on http://127.0.0.1:5000
# Press CTRL+C to quit
```

**⚠️ Si vous voyez une erreur** :
- `ModuleNotFoundError: No module named 'flask'` → `pip install -r requirements.txt` non exécuté
- `Port already in use` → Autre app utilise le port 5000 (voir PREREQUISITES.md)
- `No such file or directory: EMSP_v0.1.xlsx` → Excel pas au bon endroit

### Étape 4.2 : Ouvrir dans le navigateur

```
Ouvrir navigateur → http://127.0.0.1:5000
```

**Vous devez voir** :
- ✅ Page d'accueil avec navigation
- ✅ Listes des onglets (FORMATIONS, SALLES, etc.)
- ✅ Écrans de saisie fonctionnels

**Si rien n'apparaît** :
- Copier l'URL exacte depuis PowerShell
- Essayer http://localhost:5000 (alias de 127.0.0.1)
- Vérifier pare-feu (ne doit pas bloquer port 5000)

### Étape 4.3 : Tester un écran

```
1. Cliquer "FORMATIONS"
2. Cliquer "Ajouter une formation"
3. Remplir : Code=TEST001, Titre=Test, Durée=3 jours
4. Cliquer "Enregistrer"
5. Vérifier que la formation apparaît dans la liste
```

### Étape 4.4 : Arrêter l'application

```powershell
# Dans PowerShell où tournait l'app
CTRL+C

# Résultat :
# * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
# KeyboardInterrupt
```

---

## Phase 5 : Configuration réseau (5 minutes)

Maintenant l'app tourne. Pour que les clients la voient :

### Étape 5.1 : Trouver l'adresse IP du serveur

```powershell
ipconfig

# Chercher :
# Ethernet adapter Ethernet:
#    IPv4 Address. . . . . . . . . : 192.168.1.100
#
# OU
#
# Wireless LAN adapter WiFi:
#    IPv4 Address. . . . . . . . . : 192.168.1.105
```

**Prendre la première IPv4 trouvée** (genre 192.168.x.x)

### Étape 5.2 : Modifier l'application pour être accessible

Éditer `app.py` à la fin :

```python
# AVANT
if __name__ == '__main__':
    app.run(debug=True)

# APRÈS
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**Explication** : `0.0.0.0` signifie "accepter les connexions de tous les ordinateurs du réseau"

### Étape 5.3 : Relancer l'application

```powershell
python app.py

# Résultat :
# Running on http://0.0.0.0:5000
# Running on http://192.168.1.100:5000  ← Utiliser cette adresse
```

### Étape 5.4 : Tester depuis un autre PC

```
Sur un autre PC du réseau (client) :
1. Ouvrir navigateur
2. Aller à : http://192.168.1.100:5000  (remplacer 192.168.1.100 par l'IP trouvée)
3. Vérifier que la page EMSP s'affiche
```

**Si ça ne marche pas** :
- Vérifier pare-feu (voir PREREQUISITES.md)
- Vérifier les deux PCs sont sur le même réseau WiFi
- Vérifier l'IP correcte (`ping 192.168.1.100` depuis client)

---

## Phase 6 : Lancer au démarrage (optionnel mais recommandé)

Pour que l'app se relance toute seule si serveur redémarre :

### Option A : Script batch simple

Créer fichier `start_emsp.bat` :

```batch
@echo off
cd C:\emsp_school
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python app.py
```

Placer dans :
```
C:\Users\[Utilisateur]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

### Option B : Service Windows robuste

```powershell
# Installer nssm (service manager Windows)
choco install nssm  # Si chocolatey installé
# Sinon télécharger manuellement : https://nssm.cc/download

# Créer le service
nssm install EMSP_APP C:\Python310\python.exe C:\emsp_school\app.py
nssm set EMSP_APP AppDirectory C:\emsp_school

# Démarrer
nssm start EMSP_APP

# Vérifier
nssm query EMSP_APP
```

---

## ✅ Checklist finale

Avant de déclarer "Installation réussie" :

- [ ] Python 3.8+ trouvé
- [ ] Dossier C:\emsp_school créé avec tous les fichiers
- [ ] `pip install -r requirements.txt` exécuté sans erreur
- [ ] `python app.py` démarre sans erreur
- [ ] http://127.0.0.1:5000 accessible depuis le serveur
- [ ] http://192.168.1.100:5000 (ou IP) accessible depuis un client
- [ ] Un test de données (ajouter une formation) fonctionne
- [ ] L'adresse IP et port documentés : ________________
- [ ] Les utilisateurs savent à quelle URL aller

---

## 🔧 Troubleshooting rapide

| Problème | Cause | Solution |
|----------|-------|----------|
| `python: command not found` | Python non installé ou PATH incorrect | Installer Python 3.10, cocher "Add to PATH" |
| `ModuleNotFoundError: No module named 'flask'` | Packages non installés | `pip install -r requirements.txt` |
| `Port 5000 already in use` | Autre app utilise le port | Changer port ou arrêter autre app |
| Navigateur : Connexion refusée | App pas lancée ou pare-feu | Vérifier `python app.py` tourne, autoriser port 5000 |
| Les clients voient `Connection refused` | App lancée sur localhost seulement | Modifier app.py : `host='0.0.0.0'` |

---

**Prochaines étapes** :
1. [ ] Tester avec vraies données Comores
2. [ ] Former les utilisateurs
3. [ ] Mettre en place sauvegarde Excel quotidienne
4. [ ] Documenter les contacts d'support

---

**Date** : 22 mai 2026
**Audience** : Équipes techniques Comores
