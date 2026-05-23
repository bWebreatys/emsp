# 💾 Stratégie de Sauvegarde et Restauration

**Document commun EMSP & GMAO**
**CRITIQUE pour la continuité opérationnelle**

---

## 🎯 Vue d'ensemble

Sans stratégie de sauvegarde :
- ❌ Perte de données → catastrophe
- ❌ Fichier corrompu → travail perdu
- ❌ Impossibilité de revenir en arrière

Avec stratégie :
- ✅ Sauvegardes automatiques horaires
- ✅ Restauration en 5 minutes
- ✅ Historique complet (30 derniers jours)
- ✅ Versions étiquetées (jour clé)

---

## 📊 MODÈLE DE SAUVEGARDE

### Stratégie 3 niveaux

```
NIVEAU 1 : SAUVEGARDE TEMPS RÉEL (toutes les heures)
│
├─ Serveur principal : EMSP_v0.1.xlsx (fichier actif)
├─ Sauvegarde horaire : EMSP_v0.1_backup_20260610_1400.xlsx
├─ Sauvegarde horaire : EMSP_v0.1_backup_20260610_1500.xlsx
└─ Sauvegarde horaire : EMSP_v0.1_backup_20260610_1600.xlsx
   (Garde : 24 dernières = 1 jour)

NIVEAU 2 : SAUVEGARDE QUOTIDIENNE (fin de jour)
│
├─ EMSP_v0.1_daily_20260610.xlsx (jour 1)
├─ EMSP_v0.1_daily_20260611.xlsx (jour 2)
├─ EMSP_v0.1_daily_20260612.xlsx (jour 3)
└─ ...
   (Garde : 30 derniers jours)

NIVEAU 3 : SAUVEGARDE ÉTIQUETÉE (événements clés)
│
├─ EMSP_v0.1_tagged_JOUR1_SETUP.xlsx (jour 1, go-live)
├─ EMSP_v0.1_tagged_SEMAINE1.xlsx (fin semaine 1)
├─ EMSP_v0.1_tagged_MOIS1.xlsx (fin mois)
└─ ...
   (Garde : tous, indéfini)
```

### Espace disque

```
Fichier actif           : 5 MB
Sauvegardes horaires    : 24 × 5 MB = 120 MB
Sauvegardes quotidiennes: 30 × 5 MB = 150 MB
Sauvegardes étiquetées  : ~100 MB (variable)
────────────────────────────────────
TOTAL                   : ~375 MB

Recommandation : 1 GB sur serveur (3× sécurité)
```

---

## 🔧 IMPLÉMENTATION TECHNIQUE

### Architecture de sauvegarde

```python
# backup_system.py
import os
import shutil
import json
from datetime import datetime, timedelta
from openpyxl import load_workbook

class BackupManager:
    def __init__(self, file_path, backup_dir='backups'):
        self.file_path = file_path
        self.backup_dir = backup_dir
        self.lock_file = f"{file_path}.lock"
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def create_backup(self, backup_type='auto'):
        """Créer une sauvegarde (horaire, quotidienne ou étiquetée)"""
        
        # Vérifier que fichier n'est pas verrouillé
        if os.path.exists(self.lock_file):
            lock_data = json.load(open(self.lock_file))
            print(f"⚠️ Fichier verrouillé par {lock_data['user_name']}")
            print(f"   Sauvegarde reportée")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if backup_type == 'auto':
            backup_file = f"{self.backup_dir}/{os.path.basename(self.file_path)}_backup_{timestamp}.xlsx"
        elif backup_type == 'daily':
            date = datetime.now().strftime("%Y%m%d")
            backup_file = f"{self.backup_dir}/{os.path.basename(self.file_path)}_daily_{date}.xlsx"
        elif backup_type == 'tagged':
            tag = input("Tag (ex: JOUR1_SETUP) : ")
            backup_file = f"{self.backup_dir}/{os.path.basename(self.file_path)}_tagged_{tag}.xlsx"
        
        # Copier le fichier
        shutil.copy2(self.file_path, backup_file)
        
        # Enregistrer métadonnées
        metadata = {
            'original': self.file_path,
            'backup': backup_file,
            'timestamp': datetime.now().isoformat(),
            'type': backup_type,
            'size_mb': os.path.getsize(backup_file) / (1024*1024),
            'hash': self._calculate_hash(backup_file)
        }
        
        meta_file = backup_file + '.meta'
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Sauvegarde créée : {backup_file}")
        return True
    
    def restore_backup(self, backup_file):
        """Restaurer une sauvegarde"""
        
        # Vérifier que fichier actif n'est pas verrouillé
        if os.path.exists(self.lock_file):
            lock_data = json.load(open(self.lock_file))
            print(f"❌ Fichier en utilisation par {lock_data['user_name']}")
            print(f"   Impossible de restaurer")
            return False
        
        # Créer sauvegarde de l'état actuel (avant restauration)
        safety_backup = f"{self.backup_dir}/SAFETY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        shutil.copy2(self.file_path, safety_backup)
        print(f"✅ Sauvegarde de sécurité créée : {safety_backup}")
        
        # Restaurer
        shutil.copy2(backup_file, self.file_path)
        
        print(f"✅ Restauration complète : {backup_file}")
        print(f"⚠️  Redémarrez Flask : CTRL+C puis python app.py")
        return True
    
    def list_backups(self, days=30):
        """Lister les sauvegardes disponibles"""
        backups = []
        cutoff = datetime.now() - timedelta(days=days)
        
        for f in os.listdir(self.backup_dir):
            if f.endswith('.xlsx'):
                path = os.path.join(self.backup_dir, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                
                if mtime > cutoff:
                    backups.append({
                        'file': f,
                        'date': mtime.strftime('%Y-%m-%d %H:%M:%S'),
                        'size_mb': os.path.getsize(path) / (1024*1024)
                    })
        
        return sorted(backups, key=lambda x: x['date'], reverse=True)
    
    def cleanup_old_backups(self):
        """Supprimer les vieilles sauvegardes (> 30 jours)"""
        cutoff = datetime.now() - timedelta(days=30)
        deleted = 0
        
        for f in os.listdir(self.backup_dir):
            if '_backup_' in f and f.endswith('.xlsx'):
                path = os.path.join(self.backup_dir, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                
                if mtime < cutoff:
                    os.remove(path)
                    if os.path.exists(f"{path}.meta"):
                        os.remove(f"{path}.meta")
                    deleted += 1
        
        print(f"🧹 {deleted} vieilles sauvegardes supprimées")
    
    @staticmethod
    def _calculate_hash(file_path):
        """Calculer hash SHA256 du fichier"""
        import hashlib
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
```

---

## 🌐 INTERFACE WEB (Flask)

### Écran 1 : Dashboard sauvegarde

```
┌─ GESTION DES SAUVEGARDES ────────────────────────────────────┐
│ ADMIN ONLY                                                    │
│                                                               │
│ Statut fichier actif :                                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 📄 EMSP_v0.1.xlsx                                        │ │
│ │ Taille : 5.2 MB                                          │ │
│ │ Dernière modification : 10/06 15h22 par USER003          │ │
│ │ ✅ Vérification intégrité : OK                           │ │
│ │ 🔒 Verrou : ✅ VERT (Disponible)                         │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│ Actions :                                                     │
│ [Créer sauvegarde immédiate] [Sauvegarde quotidienne]       │
│ [Créer sauvegarde étiquetée] [Nettoyer vieilles saves]      │
│                                                               │
│ Dernières sauvegardes :                                       │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 📅 10/06 15h22 | backup_20260610_1522.xlsx | 5.2 MB   │  │
│ │ 📅 10/06 14h22 | backup_20260610_1422.xlsx | 5.2 MB   │  │
│ │ 📅 10/06 13h22 | backup_20260610_1322.xlsx | 5.2 MB   │  │
│ │ 🏷️  JOUR1_SETUP | tagged_JOUR1_SETUP.xlsx | 5.1 MB    │  │
│ │ 📅 09/06 17h30 | daily_20260609.xlsx      | 5.0 MB    │  │
│ │                                                         │  │
│ │ [Restaurer] [Télécharger] [Supprimer]                  │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Écran 2 : Restaurer une sauvegarde

```
┌─ RESTAURER UNE SAUVEGARDE ──────────────────────────────────┐
│                                                              │
│ ⚠️ ATTENTION : Opération critique !                          │
│                                                              │
│ Vous allez restaurer : backup_20260610_1422.xlsx            │
│ Créée le : 10/06 à 14h22 (1h ago)                          │
│ Taille : 5.2 MB                                             │
│                                                              │
│ État actuel (sera sauvegardé en SAFETY) :                   │
│ ├─ Fichier actif : EMSP_v0.1.xlsx                           │
│ ├─ Dernière modif : 10/06 15h22                            │
│ └─ Données perdues : Entre 14h22 et 15h22 (~1h)            │
│                                                              │
│ Verrou fichier actif : ✅ VERT (Disponible - OK)           │
│                                                              │
│ Après restauration :                                         │
│ ✓ Fichier actif = sauvegarde sélectionnée                   │
│ ✓ Ancien fichier = SAFETY_20260610_1530.xlsx               │
│ ✓ Flask redémarrera                                         │
│ ✓ Les utilisateurs se reconnecteront                        │
│                                                              │
│ Confirmez l'opération :                                      │
│ Taper "RESTORE" pour confirmer : [            ]            │
│                                                              │
│ [ANNULER] [RESTAURER]                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Écran 3 : Historique des sauvegardes

```
┌─ HISTORIQUE DES SAUVEGARDES (30 derniers jours) ────────────┐
│                                                              │
│ 🔍 Filtrer : [Tous ▼] [Jour▼] [Type▼]                      │
│                                                              │
│ Date/Heure      | Type        | Fichier              | Taille │
│─────────────────────────────────────────────────────────────│
│ 10/06 15h22    | auto        | backup_1522.xlsx     | 5.2 MB │
│ 10/06 14h22    | auto        | backup_1422.xlsx     | 5.2 MB │
│ 10/06 13h22    | auto        | backup_1322.xlsx     | 5.2 MB │
│ 10/06 12h22    | auto        | backup_1222.xlsx     | 5.1 MB │
│ 10/06 17h30    | daily       | daily_20260610.xlsx  | 5.2 MB │
│ 09/06 17h30    | daily       | daily_20260609.xlsx  | 5.0 MB │
│ 06/06 10h00    | tagged      | tagged_JOUR1_SETUP   | 5.1 MB │
│                                                              │
│ [Télécharger] [Restaurer] [Supprimer] [Vérifier intégrité] │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔐 SAUVEGARDE AUTOMATIQUE

### Tâche CRON (Linux) ou Task Scheduler (Windows)

**Linux** :
```bash
# /etc/cron.d/emsp_backup
# Sauvegarde horaire
0 * * * * python /home/emsp/backup_system.py --hourly

# Sauvegarde quotidienne (minuit)
0 0 * * * python /home/emsp/backup_system.py --daily

# Nettoyage sauvegardes > 30 jours (chaque dimanche)
0 2 * * 0 python /home/emsp/backup_system.py --cleanup
```

**Windows** :
```
Task Scheduler
├─ Task : "EMSP_Hourly_Backup"
│  └─ Run : python C:\emsp\backup_system.py --hourly
│     Trigger : Every hour (00:00)
│
├─ Task : "EMSP_Daily_Backup"
│  └─ Run : python C:\emsp\backup_system.py --daily
│     Trigger : Every day at 00:00
│
└─ Task : "EMSP_Cleanup"
   └─ Run : python C:\emsp\backup_system.py --cleanup
      Trigger : Every Sunday at 02:00
```

---

## 📋 PROCÉDURES MANUELLES

### Procédure 1 : Créer sauvegarde immédiate

```
Situation : "Je veux sauvegarder avant une grosse modif"

Étapes :
1. Admin va sur http://192.168.1.100:5000/admin/backups
2. Vérifier 🔴/✅ : Doit être ✅ VERT (pas verrouillé)
3. Cliquer [Créer sauvegarde immédiate]
4. Attendre "✅ Sauvegarde créée"
5. ✅ Prêt

Temps : 10 secondes
```

### Procédure 2 : Créer sauvegarde étiquetée (événement clé)

```
Situation : Fin de semaine, je veux marquer le jalon

Étapes :
1. Admin va sur /admin/backups
2. Vérifier ✅ VERT
3. Cliquer [Créer sauvegarde étiquetée]
4. Tag : "SEMAINE1_COMPLET" (ou autre)
5. Attendre "✅ Sauvegarde créée : tagged_SEMAINE1_COMPLET.xlsx"
6. ✅ Archivée indéfiniment (ne sera jamais supprimée)

Temps : 20 secondes
Recommandation : Chaque semaine, fin mois, avant grosse opération
```

### Procédure 3 : Restaurer d'urgence

```
Situation : "Fichier corrompu, perte de données, ou erreur grave"

Étapes :
1. Admin va sur /admin/backups
2. Voir l'historique
3. Choisir la sauvegarde avant le problème
4. Cliquer [Restaurer]
5. Écran de confirmation :
   - Vérifier ✅ VERT (fichier pas verrouillé)
   - Lire l'avertissement
   - Taper "RESTORE" pour confirmer
   - Cliquer [RESTAURER]
6. Attendre "✅ Restauration complète"
7. ⚠️ Flask redémarre (users se reconnectent)
8. ✅ Données restaurées
9. Vérifier : Fichier SAFETY_*.xlsx créé (ancien état)

Temps : 1-2 minutes
Risque : Zéro (sauvegarde de sécurité toujours créée)
```

---

## 🔍 VÉRIFICATION D'INTÉGRITÉ

### Vérifier fichier Excel

```python
def verify_excel_integrity(file_path):
    """Vérifier qu'un fichier Excel est valide"""
    try:
        wb = load_workbook(file_path)
        
        # Vérifier onglets
        if not wb.sheetnames:
            return False, "Aucun onglet trouvé"
        
        # Vérifier données
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            if ws.max_row == 0:
                print(f"⚠️ {sheet_name} : Aucune donnée")
        
        return True, "Fichier OK"
    
    except Exception as e:
        return False, str(e)

# Utilisation
ok, msg = verify_excel_integrity('EMSP_v0.1.xlsx')
if ok:
    print(f"✅ {msg}")
else:
    print(f"❌ Fichier corrompu : {msg}")
```

### Bouton de vérification dans interface

```
[Vérifier intégrité] 
→ "✅ Fichier OK : 9 onglets, 500+ lignes"
ou
→ "❌ ERREUR : Fichier corrompu - 
    Restaurer sauvegarde immédiate ?"
```

---

## 📊 LOGS DE SAUVEGARDE

### Onglet BACKUP_LOGS (Excel)

```
| Date/Heure    | Type      | Fichier                  | Statut | Détails |
|───────────────────────────────────────────────────────────────────────────|
| 10/06 15h22   | auto      | backup_20260610_1522.xlsx| OK     | Hash: a1b2... |
| 10/06 14h22   | auto      | backup_20260610_1422.xlsx| OK     | Hash: c3d4... |
| 10/06 13h22   | auto      | backup_20260610_1322.xlsx| OK     | Hash: e5f6... |
| 10/06 12h30   | daily     | daily_20260610.xlsx      | OK     | Hash: g7h8... |
| 09/06 12h30   | daily     | daily_20260609.xlsx      | OK     | Hash: i9j0... |
| 06/06 10h00   | tagged    | tagged_JOUR1_SETUP.xlsx  | OK     | Hash: k1l2... |
```

**Consulter quand** :
- ✅ Vérifier qu'une sauvegarde a bien eu lieu
- ✅ Comparer hash avant/après
- ✅ Identifier quand problème s'est produit

---

## ⏰ CHRONOLOGIE RECOMMANDÉE

### Jour 1 (Go-live)

```
1. Configurer tâches CRON/Task Scheduler
2. Tester sauvegarde immédiate (admin)
3. Créer sauvegarde étiquetée "JOUR1_SETUP"
4. Montrer à Admin local comment restaurer
```

### Jours 2+

```
Automatique :
  • Chaque heure : sauvegarde horaire
  • Chaque nuit (00:00) : sauvegarde quotidienne
  • Chaque dimanche 02h : nettoyage > 30 jours

Manuel :
  • Chaque fin de semaine : sauvegarde étiquetée "SEMAINE_N"
  • Avant gros travaux : sauvegarde immédiate
```

---

## 🚨 SCÉNARIOS DE SECOURS

### Scénario 1 : Fichier corrompu (impossible à ouvrir)

```
Symptôme : "Excel dit : fichier corrompu"

Diagnostic :
1. Vérifier intégrité → "❌ Corrompu"
2. Regarder le hash dans BACKUP_LOGS
3. Trouver dernière sauvegarde avec hash OK

Solution :
1. Restaurer sauvegarde précédente
2. Vérifier intégrité → "✅ OK"
3. Temps perdu : données entre sauvegardes (max 1h)
```

### Scénario 2 : Suppression accidentelle

```
Symptôme : "J'ai supprimé 50 lignes par erreur"

Diagnostic :
1. Utilisateur demande "annuler"
2. Admin regarde timestamp du problème
3. Cherche sauvegarde avant cette heure

Solution :
1. Restaurer sauvegarde 2 heures avant
2. Temps perdu : 2h de travail max
3. Tout avant = sauvegardé
```

### Scénario 3 : Fichier verrouillé indéfiniment

```
Symptôme : "🔴 ROUGE depuis 4h, personne n'a fermé"

Diagnostic :
1. Vérifier (.emsp_lock) : USER004 depuis 10h
2. USER004 pas connecté
3. Machine probablement crash

Solution :
1. Admin force-déverrouille (page admin)
2. Sauvegarde de sécurité créée immédiatement
3. Utilisateurs peuvent accéder
4. Vérifier intégrité : OK ?
   - Oui → continuer
   - Non → restaurer sauvegarde précédente
```

---

## 📋 CHECKLIST DÉPLOIEMENT

- [ ] Script backup_system.py créé
- [ ] Tâches CRON/Task Scheduler configurées
- [ ] Dossier backups créé
- [ ] Sauvegarde immédiate testée (OK ?)
- [ ] Restauration testée (OK ?)
- [ ] Admin formé (créer/restaurer/étiqueter)
- [ ] Logs de sauvegarde activés
- [ ] Espace disque vérifié (1 GB minimum)
- [ ] Vérification intégrité dans interface
- [ ] Procédures écrites (affichée près du serveur)

---

## 🎓 POINTS CLÉS

1. **3 niveaux** : Horaire (1 jour) + Quotidienne (30 j) + Étiquetée (indéfini)
2. **Automatique** : Pas besoin d'intervenir (CRON/Task)
3. **Rapide** : Restauration 1-2 minutes max
4. **Sûr** : Sauvegarde de sécurité avant chaque restauration
5. **Vérifié** : Hash SHA256 pour détecter corruption

---

**Version** : 22 mai 2026
**Audience** : Admin + Bernard
**Criticité** : ⭐⭐⭐⭐⭐ (Très élevée)
