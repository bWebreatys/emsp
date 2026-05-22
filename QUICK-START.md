# ⚡ QUICK START - Installation en 5 étapes (45 min)

## 🎯 Objectif
Avoir EMSP ou GMAO opérationnel sur votre réseau local aux Comores.

---

## ✅ PRÉREQUIS (Vérifier avant de commencer)

```
☐ Python 3.8+ installé : python --version
☐ pip fonctionne : pip --version
☐ Dossier vide C:\apps\ ou /home/apps/ (ou autre)
☐ Accès administrateur pour installation
☐ Port 5000 libre : netstat -ano | findstr 5000 (Windows)
```

---

## 🚀 INSTALLATION (45 minutes)

### Étape 1 : Télécharger (5 min)

```powershell
# Option A : Avec Git
git clone https://github.com/bWebreatys/emsp.git
cd emsp

# Option B : Sans Git
# Télécharger ZIP depuis https://github.com/bWebreatys/emsp
# Décompresser et ouvrir le dossier
```

### Étape 2 : Créer environnement isolé (5 min)

```powershell
# TRÈS RECOMMANDÉ pour éviter les conflits
python -m venv venv

# Activer (Windows)
.\venv\Scripts\Activate.ps1

# Vous verrez : (venv) C:\apps\emsp>
```

### Étape 3 : Installer dépendances (15 min)

```powershell
pip install -r requirements.txt

# Résultat attendu :
# Successfully installed Flask-2.3.0 openpyxl-3.10.0 ...
```

### Étape 4 : Tester en local (10 min)

```powershell
python app.py

# Vous verrez :
# WARNING: This is a development server.
# Running on http://127.0.0.1:5000

# Ouvrir navigateur → http://127.0.0.1:5000
# Si ça s'affiche : ✅ SUCCESS
# Si erreur : voir TROUBLESHOOTING section
```

### Étape 5 : Configurer réseau (5 min)

Éditer `app.py` à la fin du fichier :

```python
# AVANT
if __name__ == '__main__':
    app.run(debug=True)

# APRÈS (changement à 2 lignes)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Puis relancer :

```powershell
python app.py

# Vous verrez l'IP du serveur :
# Running on http://192.168.1.100:5000

# Sur un autre PC : http://192.168.1.100:5000
# ✅ SUCCESS !
```

---

## 📊 RÉSULTAT

```
Serveur : 1 PC Windows/Linux avec Python 3.8+
Port    : 5000
Client  : N'importe quel autre PC avec navigateur
URL     : http://[IP_SERVEUR]:5000

Exemple :
  Serveur IP : 192.168.1.100
  Clients vont à : http://192.168.1.100:5000
```

---

## ⚠️ TROUBLESHOOTING RAPIDE

| Erreur | Solution |
|--------|----------|
| `python: command not found` | Installer Python + cocher "Add to PATH" |
| `ModuleNotFoundError: flask` | `pip install -r requirements.txt` |
| `Port 5000 already in use` | Fermer autre app ou changer port |
| Clients : `Connection refused` | Modifier app.py → `host='0.0.0.0'` |
| `Permission denied` | Droits d'accès insuffisants |

---

## 🎓 Points clés

1. **Virtual environment (venv)** = ISOLÉ, sans conflit
2. **Port 5000** = DOIT être libre
3. **host='0.0.0.0'** = Accessible depuis réseau
4. **Clients** = Juste navigateur web, pas Python
5. **Serveur** = 1 seul compte utilisateur

---

## 📞 Support détaillé

Si vous avez besoin de plus :
- **PREREQUISITES.md** : Versions Python, droits d'accès, réseau
- **INSTALLATION-STEP-BY-STEP.md** : Étapes très détaillées
- **INSTALLATION-VISUAL-GUIDE.txt** : Diagrammes ASCII

---

**Durée estimée** : 45 minutes
**Contact** : contact@webcreatys.com
**Prochaine étape** : Former les utilisateurs
