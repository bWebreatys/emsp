# 📋 Prérequis - Installation et Configuration

## 🎯 Vue d'ensemble

Ce document détaille :
- Versions Python compatibles/incompatibles
- Gestion des versions existantes
- Droits d'accès serveur et clients
- Configuration réseau
- Scénarios de déploiement

---

## 🐍 Python - Versions

### ✅ Versions COMPATIBLES

| Version | Statut | Notes |
|---------|--------|-------|
| **3.11.x** | ✅ Recommandée | Dernière stable, Flask 2.3 OK |
| **3.10.x** | ✅ OK | Très stable, entreprises préfèrent |
| **3.9.x** | ✅ OK | Support jusqu'à mai 2025 |
| **3.8.x** | ✅ OK mais vieux | Support jusqu'à octobre 2024 |

### ❌ Versions INCOMPATIBLES

| Version | Problème |
|---------|----------|
| **3.12+** | ⚠️ Peut causer des problèmes avec certains packages |
| **3.7 ou moins** | ❌ Flask nécessite 3.8+ |
| **2.7.x** | ❌ Python 2 - TRÈS obsolète |

### 📌 Quid si une version est déjà installée ?

#### Scénario 1 : Python 3.8-3.11 existant ✅
```
→ Aucun problème, utiliser la version existante
→ Vérifier : python --version
→ Installer packages : pip install -r requirements.txt
```

#### Scénario 2 : Python 3.12+ existant ⚠️
```
→ Risque de compatibilité avec openpyxl
→ Options :
  A) Tester quand même (70% de chance ça marche)
  B) Installer Python 3.10 en parallèle
  C) Créer un virtual environment (voir section ci-dessous)
```

#### Scénario 3 : Plusieurs Python installés (3.8 ET 3.11) ✅
```
→ Spécifier la version à utiliser :
  Windows : python3.10 --version
  Linux : /usr/bin/python3.10 --version
→ Utiliser cette version pour l'app
```

#### Scénario 4 : Python 2.7 ou 3.5-3.7 existant ❌
```
→ OBLIGATOIRE d'installer une version plus récente
→ Ne pas supprimer l'ancienne (autres apps peuvent la nécessiter)
→ Installer Python 3.10 en parallèle
→ Configurer l'app pour utiliser 3.10
```

---

## 💻 Installation Python - Par plateforme

### Windows

#### Check version existante
```powershell
# Option 1 : Depuis PowerShell
python --version
python3 --version

# Option 2 : Depuis Cmd
python --version

# Option 3 : Chercher dans le système
Get-Command python
```

#### Installer nouvelle version (si nécessaire)
```
1. Télécharger : https://www.python.org/downloads/
2. Choisir : Python 3.10.x (LTS - Long Term Support)
3. ✅ COCHER : "Add Python to PATH" (très important !)
4. Installer pour "All Users" (pas "Current User")
5. Vérifier : python --version
```

#### ⚠️ Points critiques Windows
- ✅ Cocher "Add to PATH" - sinon Python ne sera pas trouvé
- ✅ Installer pour "All Users" - sinon droits insuffisants pour autres utilisateurs
- ✅ Choisir chemin sans accents (C:\Python310\, pas C:\Mes Programmes\)
- ✅ Fermer PowerShell et le rouvrir après installation

### Linux (Ubuntu/Debian)

#### Check version existante
```bash
python3 --version
which python3
```

#### Installer (si nécessaire)
```bash
# Mise à jour repos
sudo apt-get update

# Installer Python 3.10
sudo apt-get install python3.10 python3.10-venv python3-pip

# Vérifier
python3.10 --version
```

### MacOS

#### Check version existante
```bash
python3 --version
which python3
```

#### Installer (si nécessaire)
```bash
# Via Homebrew (recommandé)
brew install python@3.10

# Ou télécharger : https://www.python.org/downloads/
```

---

## 🔐 Droits d'accès SERVEUR

### Compte utilisateur du serveur

Le serveur (celui qui lance `python app.py`) doit avoir :

#### ✅ Droits obligatoires
- **Lecture/Écriture** sur le dossier `/emsp_app/` (pour logs, cache)
- **Lecture** sur `EMSP_v0.1.xlsx`
- **Lecture/Écriture** sur le dossier où sera sauvegardé Excel modifié
- **Port 5000 libre** (ou port choisi)

#### Exemple Windows
```
C:\emsp\                         → Propriétaire = Utilisateur X
├── app.py                       → Lecture (X)
├── EMSP_v0.1.xlsx              → Lecture (X) + Écriture (X pour sauvegardes)
├── emsp_app/
│   ├── app.py                  → Lecture (X)
│   ├── templates/              → Lecture (X)
│   └── __pycache__/            → Lecture/Écriture (X) - créé auto
└── requirements.txt            → Lecture (X)
```

#### Exemple Linux
```bash
# Propriétaire = utilisateur "emsp_admin"
sudo chown -R emsp_admin:emsp_admin /home/emsp/
sudo chmod -R 755 /home/emsp/
sudo chmod -R 755 /home/emsp/emsp_app/

# Test de démarrage
su - emsp_admin
cd /home/emsp/
python3 app.py
```

### Comptes utilisateurs LOCAUX (même serveur)

Si plusieurs utilisateurs accèdent au serveur depuis le même ordinateur :

| Droit | Accès requis |
|-------|--------------|
| Lancer l'app | ❌ Non (pas recommandé) - Utiliser un seul compte |
| Accéder l'app (navigateur local) | ✅ Oui - Tous les comptes peuvent ouvrir navigateur |
| Modifier données Excel | ⚠️ Oui si accès direct, NON si via web |

#### Meilleure pratique
```
1 seul compte utilisateur "emsp_service" avec droits
├─ Lance l'app au démarrage (service Windows) ou cron (Linux)
└─ Les utilisateurs locaux y accèdent via http://localhost:5000

Les utilisateurs n'ont PAS besoin d'accès direct à C:\emsp\
```

---

## 🌐 Droits d'accès CLIENTS (utilisateurs distants)

### Sur le réseau local (établissement Comores)

#### Configuration: Serveur + Clients en réseau local

```
Serveur (PC Windows/Linux)           Clients (PCs sur le réseau)
├─ IP: 192.168.1.100                ├─ IP: 192.168.1.10
├─ Port: 5000                       ├─ Navigateur vers 192.168.1.100:5000
├─ Python tourne                    ├─ Pas besoin Python
├─ Excel stocké localement          ├─ Pas d'accès direct au fichier
└─ Logs serveur                     └─ Voir données en lecture/écriture web
```

#### Droits utilisateurs clients
- ✅ **Navigateur web** : Firefox, Chrome, Edge (n'importe lequel)
- ✅ **Accès réseau** : Pouvoir joindre http://192.168.1.100:5000
- ✅ **Lecture/Écriture** : Via interface web uniquement (pas d'accès direct fichiers)
- ❌ **Pas besoin** : Python, accès dossier serveur, droits administrateur

#### Vérifier la connectivité clients
```powershell
# Depuis un PC client
ping 192.168.1.100          # Vérifier accès réseau
telnet 192.168.1.100 5000   # Vérifier port accessible
# Puis ouvrir navigateur vers http://192.168.1.100:5000
```

---

## 🔌 Configuration Réseau - Scénarios Comores

### Scénario 1 : Réseau stable avec routeur ✅ (RECOMMANDÉ)

```
Internet ou LAN établissement
         │
    [Routeur WiFi/Ethernet]
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
  Serveur   Client1  Client2  Client3
  (PC)      (PC)     (PC)     (Tablette)
 5000       5000     5000     5000
```

**Configuration** :
```
1. Serveur : IP fixe (192.168.1.100)
2. Clients : Navigateur → http://192.168.1.100:5000
3. Pas besoin d'internet (complètement local)
```

**Avantages** : Robuste, rapide, pas de dépendance internet

### Scénario 2 : Réseau instable avec WiFi intermittent ⚠️

```
Serveur reste allumé 24/7
Clients : déconnexions possibles
```

**Configuration** :
```
1. Serveur : Mode "offline-first"
   - Cache local des données
   - Journalisation robuste
   - Reconnexion automatique clients

2. Clients : "Save draft" avant soumission
   - Au cas où déconnexion
   - Replay quand réseau revient
```

**À tester avant départ** :
- [ ] Couper WiFi du serveur pendant 1 min
- [ ] Les clients peuvent-ils se reconnecter ?
- [ ] Les données en cours de saisie sont-elles sauvegardées ?

### Scénario 3 : Pas de réseau - Machine unique ❌ (NON RECOMMANDÉ)

```
1 PC = Serveur + Client local
http://localhost:5000
```

**Limitations** :
- Un seul utilisateur à la fois
- Si PC crash, tout est perdu
- Pas d'accès multi-établissements

**À éviter** : Préférer Scénario 1 même avec WiFi basique

---

## 🛡️ Pare-feu et Sécurité

### Pare-feu Windows (Serveur)

```powershell
# Autoriser Python port 5000
# Via GUI : Windows Defender > Pare-feu > Autoriser une app

# Ou via PowerShell (Admin)
New-NetFirewallRule -DisplayName "Flask EMSP" `
  -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### Pare-feu Linux (Serveur)

```bash
# Si ufw actif
sudo ufw allow 5000/tcp

# Si firewalld
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### Accès distant via Internet (Comores vers Nice) ❌

⚠️ **ATTENTION** : Ne pas exposer l'app directement sur Internet

Si besoin d'accès depuis l'étranger :
- Utiliser **VPN** ou **SSH tunnel**, pas exposition port direct
- Implémenter **authentification** (pas inclus v0.1)
- Utiliser **HTTPS** (pas HTTP brut)

---

## 📋 Checklist de déploiement

### Avant installation (Établissement Comores)

- [ ] Python 3.8-3.11 disponible (vérifier `python --version`)
- [ ] Internet pour `pip install` (ou télécharger packages offline)
- [ ] PC serveur identifié et dédié
- [ ] Accès administrateur pour installer packages
- [ ] Réseau local fonctionnant (WiFi ou Ethernet)
- [ ] Adresse IP serveur noter : ________________
- [ ] Port 5000 libre (vérifier `netstat -ano | findstr 5000`)

### Installation (30 minutes)

- [ ] Cloner/télécharger le repo GitHub
- [ ] `pip install -r requirements.txt` (avec bonne version Python)
- [ ] Vérifier `python app.py` démarre sans erreur
- [ ] Tester `http://localhost:5000` depuis serveur

### Réseau (15 minutes)

- [ ] Trouver IP serveur : `ipconfig` (Windows) ou `ifconfig` (Linux)
- [ ] Tester depuis un client : `http://[IP_SERVEUR]:5000`
- [ ] Vérifier pare-feu autorisant port 5000
- [ ] Documenter l'IP et l'URL pour les utilisateurs

### Utilisation (ongoing)

- [ ] Serveur lance app au démarrage (voir section Services)
- [ ] Sauvegardes Excel : une fois par jour minimum
- [ ] Logs serveur consultés si problèmes
- [ ] Tests utilisateurs multiples simultanés

---

## 🔧 Services Windows (Lancer app au démarrage)

Si l'établissement veut que l'app se lance toute seule au démarrage du serveur :

### Option A : Script batch Windows (Facile)

Créer `lancer_EMSP_startup.bat` :
```batch
@echo off
cd C:\emsp
python app.py
```

Puis placer dans :
```
C:\Users\[Utilisateur]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

### Option B : Service Windows (Robuste)

Installer via `nssm` (Non-Sucking Service Manager) :
```powershell
# Télécharger nssm.exe
nssm install EMSP_Service C:\Python310\python.exe C:\emsp\app.py
nssm start EMSP_Service
nssm query EMSP_Service
```

---

## 📞 Troubleshooting

### "Python not found" / "python: command not found"

```
Cause : Python non dans PATH
Solution :
  Windows : Réinstaller en cochant "Add to PATH"
  Linux : Utiliser /usr/bin/python3.10 ou alias
```

### "Port 5000 already in use"

```
Cause : Autre app utilise le port
Solution :
  Windows : netstat -ano | findstr 5000
           taskkill /PID [PID] /F
  Linux : sudo lsof -i :5000
          sudo kill -9 [PID]
  Ou changer port : app.py ligne 'run(port=5001)'
```

### "Permission denied" (Linux)

```
Cause : Droits d'accès insuffisants
Solution :
  sudo chown -R $USER:$USER /path/to/emsp
  chmod -R 755 /path/to/emsp
```

### "ModuleNotFoundError: No module named 'flask'"

```
Cause : Packages non installés
Solution :
  pip install -r requirements.txt
  (ou pip3 si pip n'existe pas)
```

---

## 📝 Résumé pour Comores

| Question | Réponse |
|----------|---------|
| **Quelle Python ?** | 3.10.x (LTS) ou 3.9/3.11 OK |
| **Serveur quel OS ?** | Windows 10+ ou Linux (Ubuntu 20+) |
| **Droits serveur ?** | Admin pour installation, puis utilisateur local |
| **Droits clients ?** | Juste navigateur web + accès réseau |
| **Réseau requis ?** | Oui (local, pas internet nécessaire) |
| **Un seul utilisateur ?** | Non - simultané OK via web |
| **Sauvegarde Excel ?** | À prévoir (pas auto) |

---

**Version** : 22 mai 2026
**Audience** : Équipes techniques Comores
**Prochaine mise à jour** : Après élicitation sur place
