# 🔨 Gestion des Corruptions et Reconstruction

**Document commun EMSP & GMAO**
**Pour quand ça casse**

---

## 🎯 Vue d'ensemble

**Corruption = fichier Excel devient inaccessible**

Types :
- ❌ "Impossible d'ouvrir le fichier"
- ❌ "Le fichier est corrompu"
- ❌ "Format non valide"
- ❌ "Données manquantes ou incohérentes"

Solutions :
- ✅ Restaurer d'une sauvegarde (90% des cas)
- ✅ Reconstruire le fichier (10% des cas graves)
- ✅ Fusion de données (cas extrême)

---

## 📊 DIAGNOSTIC RAPIDE

### Étape 1 : Identifier le problème

```
Q1 : Le fichier s'ouvre ?
  ├─ OUI → Allez à "Données manquantes" (section B)
  └─ NON → Continue Q2

Q2 : Message d'erreur spécifique ?
  ├─ "Format not valid" → Corruption sérieuse (section C)
  ├─ "Cannot open file" → Corruption sérieuse (section C)
  └─ "File is locked" → Verrou bloqué (section A)

Q3 : Quand exactement le problème a commencé ?
  ├─ Hier/Aujourd'hui → Restaurer sauvegarde précédente
  └─ Plusieurs jours → Différents niveaux corruption
```

### Arbre de décision

```
Fichier corrompu ?
│
├─ OUI, s'ouvre pas
│  ├─ Restaurer sauvegarde
│  │  └─ Marche ? OUI → Fini (Sec. C.2)
│  │              NON → Reconstruire (Sec. C.3)
│  └─ Aucune sauvegarde OK
│     └─ Reconstruire fichier vide (Sec. C.3)
│
└─ OUI, s'ouvre mais données manquantes
   ├─ Restaurer sauvegarde
   │  └─ Marche ? OUI → Fini (Sec. B.2)
   │              NON → Fusionner données (Sec. B.3)
   └─ Aucune sauvegarde OK
      └─ Remplir manuellement (Sec. B.3)
```

---

## A. FICHIER VERROUILLÉ (Verrous bloqués)

### Symptôme

```
🔴 ROUGE CLIGNOTANT depuis longtemps
Message : "Fichier en utilisation par USER999"
Mais USER999 n'est pas connecté
```

### Cause

```
Possibilités :
1. Utilisateur a fermé explorer/terminal, pas l'Excel
2. Crash serveur (power off, réseau mort)
3. Session bloquée inexplicablement
4. Bug Flask verrou pas libéré
```

### Solution

```
Étape 1 : Vérifier USER999 pas connecté
  - Aller sur /admin/users
  - USER999 : "Dernier accès : 4h ago"

Étape 2 : Forcer déverrouillage
  - Admin va sur /admin/backups
  - Cliquer [Force unlock]
  - Confirmer : "OUI, forcer"
  - ✅ Verrou supprimé

Étape 3 : Vérifier intégrité
  - Cliquer [Vérifier intégrité]
  - ✅ OK ? → Continuer
  - ❌ Corrompu ? → Aller section C

Étape 4 : Redémarrer Flask
  - CTRL+C dans terminal serveur
  - python app.py
  - Attendre "Running on..."
  - ✅ Utilisateurs peuvent accéder

Temps : 2-3 minutes
```

---

## B. DONNÉES MANQUANTES OU INCOHÉRENTES

### Symptôme 1 : Onglet vide

```
Fichier s'ouvre
Onglet FORMATIONS parcouru
Mais aucune donnée
→ "Toutes les formations ont disparu ?"
```

### Symptôme 2 : Données incohérentes

```
Fichier s'ouvre
Colonnes ne correspondent pas
Formules cassées (#ERROR!, #N/A)
→ "Les calculs ne fonctionnent plus"
```

### Diagnostic

```
Cause 1 : Suppression accidentelle
  - Un utilisateur a supprimé des lignes
  - Pendant 2h, avant qu'on s'en aperçoive

Cause 2 : Fusion de données mal faite
  - 2 utilisateurs ont modifié, versions fusionnées mal

Cause 3 : Corruption partielle
  - Seul l'onglet FORMATIONS a un problème
  - Autres onglets OK
```

### Solution : Restaurer sauvegarde

```
Procédure : BACKUP-RESTORE-STRATEGY.md (Procédure 3)

Étapes :
1. Admin va sur /admin/backups
2. Voir l'historique
3. Chercher la sauvegarde AVANT le problème
   - "10/06 14h22 OK" vs "10/06 15h22 Corrompu"
   - Choisir 14h22
4. Cliquer [Restaurer]
5. Lire avertissement, taper "RESTORE"
6. Cliquer [RESTAURER]
7. ✅ Fichier restauré

Temps perdu : Données entre 14h22 et restauration (max 1h)
Temps opération : 1-2 minutes
```

### Solution : Fusionner données (Cas avancé)

```
Situation : 
  - Sauvegarde avant corruption = 10h de travail
  - Travail depuis 10h = important aussi
  - → Fusionner les deux

Procédure :
1. Télécharger sauvegarde "backup_good.xlsx"
2. Télécharger version actuelle "EMSP_active.xlsx"
3. Ouvrir les deux en local
4. Copier données manquantes de "EMSP_active" vers "backup_good"
5. Vérifier intégrité (pas de doublons, formules OK)
6. Uploader "backup_good.xlsx" réparé sur serveur
7. Remplacer fichier actif
8. Tester accès, vérifier données

Risque : Moyen (fusion manuelle = erreurs possibles)
Recommandation : Appeler Bernard avant de faire ça
```

---

## C. FICHIER CORROMPU (Impossible à ouvrir)

### Symptôme

```
Vous ouvrez Excel
Sélectionnez EMSP_v0.1.xlsx
❌ "Excel cannot open this file format"
ou
❌ "File is corrupted"
ou
❌ "File cannot be opened"
```

### Cause

```
Possibilités (ordre probabilité) :
1. Sauvegarde interruption en milieu fichier
   → Données partielles, structure cassée
2. Infection/corruption système fichier
   → Rare sur NTFS, plus probable sur FAT32
3. Bug openpyxl lors sauvegarde
   → Très rare avec versions actuelles
4. Problème lecteur disque
   → Physicien problème matériel
```

### Solution 1 : Restaurer sauvegarde (90% des cas)

```
Procédure identique à section B

Étapes :
1. Admin va sur /admin/backups
2. Prendre la sauvegarde la plus récente AVANT corruption
3. Restaurer (voir BACKUP-RESTORE-STRATEGY.md)
4. Vérifier intégrité
5. ✅ Fichier OK

Temps : 2-3 minutes
Risque : Aucun (sauvegarde de sécurité créée)
Données perdues : Max depuis dernière sauvegarde (1h)
```

### Solution 2 : Reconstruire fichier (Si toutes sauvegardes OK)

```
Situation : Corruption détectée, mais aucune sauvegarde OK

Procédure :
1. Créer nouvel Excel EMSP_v0.1_rebuilt.xlsx
   (À partir de template ou depuis zéro)

2. Recréer structure :
   - Onglets : ACCUEIL, FORMATIONS, SALLES, etc.
   - Colonnes : Code, Nom, Description, etc.
   - Formules : Listes déroulantes, validations

3. Importer données depuis ancien fichier (si lisible)
   - Ouvrir "EMSP_corrupted" en lecture seule
   - Copier données par sections
   - Vérifier: pas de doublons, formules OK

4. Tester :
   - Chaque onglet a données ?
   - Listes déroulantes marche ?
   - Formules calculent ?

5. Uploader "EMSP_v0.1_rebuilt.xlsx"
   - Renommer : EMSP_v0.1.xlsx
   - Redémarrer Flask
   - Tester accès

Temps : 30-60 minutes
Risque : Moyen (recréation manuelle = erreurs possibles)
Recommandation : Appelez Bernard AVANT de commencer
```

### Solution 3 : Recherche & Remplacement (Si partiellement lisible)

```
Situation : 
  - Fichier s'ouvre mais "structure cassée"
  - Certains onglets OK, autres pas

Procédure :
1. Identifier onglets OK vs cassés
   - Vérifier chaque onglet
   - OK = données complètes
   - Cassé = données partielles/vides

2. Reconstruire onglets cassés
   - Créer onglet vide avec structure correcte
   - Copier données depuis version fonctionnelle

3. Vérifier intégrité globale
   - Toutes formules marchent ?
   - Listes déroulantes OK ?
   - Validations actives ?

4. Tester complètement
   - Ajouter ligne test
   - Modifier donnée test
   - Supprimer ligne test

5. Sauvegarder
   - Créer sauvegarde étiquetée "REBUILT"
   - Avant de considérer OK

Temps : 30-40 minutes
Risque : Moyen
Recommandation : Appel Bernard pour valider
```

---

## 🔍 SCRIPT DE VÉRIFICATION

### Python script

```python
# verify_and_repair.py
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import os

def verify_excel(file_path):
    """Vérifier intégrité complète"""
    
    print(f"\n🔍 Vérification : {file_path}\n")
    
    try:
        wb = load_workbook(file_path)
        print(f"✅ Fichier ouvert")
        
        # Vérifier onglets
        sheets = wb.sheetnames
        print(f"✅ {len(sheets)} onglets trouvés : {sheets}")
        
        # Vérifier données par onglet
        for sheet in sheets:
            ws = wb[sheet]
            rows = ws.max_row
            cols = ws.max_column
            
            if rows == 0:
                print(f"⚠️  {sheet} : Aucune donnée")
            else:
                print(f"✅ {sheet} : {rows} lignes, {cols} colonnes")
            
            # Vérifier formules
            formula_errors = 0
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value and isinstance(cell.value, str):
                        if cell.value.startswith('='):
                            # C'est une formule
                            pass
                        if '#ERROR!' in str(cell.value):
                            formula_errors += 1
            
            if formula_errors > 0:
                print(f"⚠️  {sheet} : {formula_errors} erreurs formules")
        
        # Hash
        import hashlib
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        
        print(f"\n✅ Hash SHA256 : {sha256.hexdigest()}")
        print(f"✅ FICHIER OK - Peut être utilisé")
        return True
        
    except Exception as e:
        print(f"❌ ERREUR : {e}")
        print(f"❌ FICHIER CORROMPU - Restaurer sauvegarde")
        return False

# Utilisation
if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else "EMSP_v0.1.xlsx"
    verify_excel(file_path)
```

### Utilisation

```bash
# Vérifier fichier actif
python verify_and_repair.py EMSP_v0.1.xlsx

# Vérifier sauvegarde
python verify_and_repair.py backups/EMSP_backup_20260610_1400.xlsx
```

---

## 📋 PROCÉDURES RÉSUMÉES

### Checklist rapide en cas de problème

```
1. ❌ Fichier s'ouvre pas ?
   → Restaurer sauvegarde (BACKUP-RESTORE-STRATEGY.md)
   
2. ❌ Données manquantes/incohérentes ?
   → Restaurer sauvegarde
   → Vérifier dernière version OK
   
3. ❌ Verrou bloqué longtemps ?
   → Force unlock (/admin/backups)
   → Vérifier intégrité
   
4. ❌ Formules cassées (#ERROR!) ?
   → Restaurer sauvegarde
   → Ou reconstruire onglet
   
5. ❌ Toutes sauvegardes OK ?
   → Reconstruire fichier vide
   → Importer données depuis ancien
   → Appeler Bernard
```

---

## 🚨 SCÉNARIOS EXTRÊMES

### Scénario 1 : Serveur crash complet

```
Symptôme : Disque du serveur meurt

Récupération :
1. Disque physiquement récupérable ?
   - Oui → Récupérer données, restaurer sauvegardes
   - Non → Données perdues, refaire à zero

2. Sauvegardes en backup cloud ?
   - Oui → Télécharger, restaurer
   - Non → Utiliser sauvegardes locales

3. Nouveau serveur setup
   - Installer Python
   - Copier sauvegardes
   - Restaurer dernière sauvegarde OK
   - Tester

Recommandation : Backup quotidien sur clé USB (hors site)
```

### Scénario 2 : Fusion accidentelle de 2 versions

```
Situation : 
  - USER003 modifie EMSP_v0.1.xlsx offline
  - USER002 modifie EMSP_v0.1.xlsx online
  - Fichiers fusionnés mal

Diagnostic :
  - Données dupliquées
  - Certaines formules cassées

Solution :
1. Identifier quelle version est "plus à jour"
2. Comparer manuellement les différences
3. Fusionner sélectivement
4. Vérifier intégrité
5. Tester complètement

Recommandation : 
  - Ne pas autoriser modifications offline
  - Utiliser locking pour empêcher cela
```

### Scénario 3 : Attaque/Suppression intentionnelle

```
Situation : Quelqu'un a accès et supprime intentionnellement

Récupération :
1. Audit logs : Qui a supprimé ?
2. Quand exactement ?
3. Restaurer sauvegarde AVANT suppression
4. Enquête avec équipe local

Prévention :
- Logs d'audit = preuves
- Permissions = qui peut supprimer
- Backups = récupération garantie
```

---

## 📞 QUAND APPELER BERNARD

```
❌ Situation trop critique :
  - Impossible reconstruire
  - Corruption de tous les niveaux
  - Besoin expertise

✅ Appelez Bernard si :
  - Toutes sauvegardes semblent corrompues
  - Fichier trop endommagé pour fusionner
  - Perte de données complète > 1 jour
  - Vous êtes pas sure de procédure

Email : contact@webcreatys.com
WhatsApp : +33 9 70 46 33 88
```

---

## ✅ CHECKLIST DÉPLOIEMENT

- [ ] Script verify_and_repair.py disponible
- [ ] Admin formé : restaurer sauvegarde
- [ ] Admin formé : vérifier intégrité
- [ ] Admin formé : force unlock
- [ ] Procédures imprimées (affichées serveur)
- [ ] Numéro Bernard affiché
- [ ] Sauvegardes testées (restauration fonctionne ?)
- [ ] Sauvegarde étiquetée "JOUR1_SETUP" avant go-live

---

**Version** : 22 mai 2026
**Audience** : Admin + Bernard
**Criticité** : ⭐⭐⭐⭐⭐ (Très élevée)
**À lire en cas de crise**
