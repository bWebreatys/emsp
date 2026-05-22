# 🔒 Gestion de l'Accès Concurrent au Fichier Excel

**Document commun EMSP & GMAO**
**CRITIQUE pour éviter la corruption de données**

---

## 🎯 Le Problème

**Scénario réel** :
- 14h : Secrétaire ouvre EMSP_v0.1.xlsx
- 14h02 : Admin ouvre AUSSI EMSP_v0.1.xlsx
- 14h05 : Secrétaire ajoute "Formation Infirmière"
- 14h07 : Admin sauvegarde ses modifications
- ❌ **CRASH** : Les données du secrétaire perdues

**Raison** : Excel n'est **pas conçu pour l'accès multi-utilisateur**

**Solution** : Système de verrous (locks) avec indicateurs visuels

---

## 🔴 INDICATEUR VISUEL (Critique)

### État 1 : ROUGE CLIGNOTANT (⚠️ EN UTILISATION)

**Affichage** :
- Sur le serveur : Icône rouge clignotante
- Message : "Fichier en cours d'utilisation par USER003 (Secrétaire) depuis 14h05"
- Qui : Afficher le nom de la personne
- Depuis quand : Heure d'ouverture

**Signification** :
- ❌ Ne PAS ouvrir le fichier
- ❌ Ne PAS télécharger
- ✅ Attendez que l'indicateur devienne vert

### État 2 : VERT FIXE (✅ DISPONIBLE)

**Affichage** :
- Icône verte fixe
- Message : "Fichier disponible (dernière modification 10/06 15h22)"
- Qui : Bernard Leglise
- Quand : "Dernière sauvegarde à 15h22"

**Signification** :
- ✅ Fichier libre
- ✅ Vous pouvez l'ouvrir
- ✅ Synchronisé avec serveur

---

## 🛠️ IMPLÉMENTATION

### Architecture

```
[Serveur Python/Flask]
│
├─ EMSP_v0.1.xlsx (main file)
├─ .emsp_lock (fichier de verrou)
│  ├─ user_id: USER003
│  ├─ user_name: Secrétaire EMSP
│  ├─ timestamp: 2026-06-10 14:05:32
│  ├─ hash: a1b2c3d4... (SHA256 du fichier)
│  └─ status: LOCKED
│
└─ Flask App
   ├─ Endpoint /api/status          → ✅ ou ❌
   ├─ Endpoint /api/lock            → Verrouiller
   ├─ Endpoint /api/unlock          → Déverrouiller
   └─ Endpoint /api/download        → Télécharger si dispo
```

### Fichier de verrou `.emsp_lock`

```json
{
  "status": "LOCKED",
  "locked_by": {
    "user_id": "USER003",
    "user_name": "Secrétaire EMSP",
    "email": "secretaire@emsp.km",
    "etablissement": "EMSP"
  },
  "lock_time": "2026-06-10T14:05:32.123Z",
  "expected_unlock_time": "2026-06-10T15:05:32.123Z",
  "file_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "ip_address": "192.168.1.50",
  "session_id": "sess_abc123def456"
}
```

---

## 📱 INTERFACE UTILISATEUR

### Écran principal (Dashboard)

```
┌─────────────────────────────────────────────────────────┐
│                  STATUS FICHIER EXCEL                   │
│─────────────────────────────────────────────────────────│
│                                                          │
│  EMSP_v0.1.xlsx                                         │
│                                                          │
│  ● Statut : ✅ DISPONIBLE (Vert fixe)                  │
│                                                          │
│  Dernière utilisation :                                 │
│    • Par : Bernard Leglise (ADMIN)                      │
│    • Quand : Aujourd'hui 15h22                          │
│    • Action : Modification FORMATIONS                   │
│                                                          │
│  [Télécharger] [Ouvrir] [Historique]                   │
│                                                          │
└─────────────────────────────────────────────────────────┘

Vs.

┌─────────────────────────────────────────────────────────┐
│                  STATUS FICHIER EXCEL                   │
│─────────────────────────────────────────────────────────│
│                                                          │
│  GMAO_v0.1.xlsx                                         │
│                                                          │
│  🔴 Statut : ⚠️ EN UTILISATION (Clignotant)            │
│                                                          │
│  Actuellement utilisé par :                             │
│    • Nom : Technicien GMAO (USER004)                    │
│    • Email : tech@gmao.km                              │
│    • Depuis : 14h05 (30 minutes)                        │
│                                                          │
│  ⏳ Patientez...                                         │
│  [Rafraîchir] [Forcer déverrouillage] [Attendre]       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Écran de téléchargement

```
┌─ TÉLÉCHARGER EMSP_v0.1.xlsx ─────────────────────────┐
│                                                       │
│ Status: ✅ Disponible                                │
│                                                       │
│ ✓ Fichier synchronisé                                │
│ ✓ Pas de modification en cours                       │
│ ✓ Version : 2026-06-10 15h22                        │
│                                                       │
│ ☐ Créer une copie locale (USER003-EMSP-backup.xlsx) │
│ ☑ Synchroniser avec serveur à la fermeture          │
│                                                       │
│ [Télécharger] [Annuler]                              │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### En cas de fichier verrouillé

```
┌─ ALERTE : FICHIER EN UTILISATION ─────────────────────┐
│                                                        │
│ ⚠️ GMAO_v0.1.xlsx est actuellement modifié            │
│                                                        │
│ Utilisé par : USER004 (Technicien GMAO)              │
│ Depuis : 14h05 (30 min)                              │
│ Poste : 192.168.1.50                                 │
│                                                        │
│ OPTIONS :                                             │
│                                                        │
│ [ ] Attendre (raffraîchit auto chaque 10 sec)        │
│                                                        │
│ [ ] Envoyer message à USER004 :                      │
│     "Pouvez-vous fermer le fichier ?"                │
│     [Envoyer]                                         │
│                                                        │
│ [ ] FORCER DÉVERROUILLAGE (Admin only)               │
│     ⚠️ Attention: risque de perte de données         │
│     [Confirmer]                                       │
│                                                        │
│ [Annuler]                                             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 💻 WORKFLOW UTILISATEUR

### Étape 1 : Vérifier disponibilité

```
1. Utilisateur ouvre la page web
2. Flask affiche STATUS :
   ✅ VERT   → Peut continuer
   🔴 ROUGE → Attend ou notification
```

### Étape 2 : Télécharger le fichier

```
1. Utilisateur clique "Télécharger"
2. Flask :
   a) Vérifie que statut = VERT
   b) Crée fichier de verrou (.emsp_lock)
   c) Marque : LOCKED par USER003
   d) Envoie fichier au client
   e) Tous les autres voient 🔴 ROUGE
```

### Étape 3 : Modifier en local (Excel)

```
1. Utilisateur travaille sur son ordinateur
2. Excel est fermé = Flask relâche le verrou
3. Flask vérifie si fichier a changé (hash)
4. Comparaison version locale vs serveur
5. Fusion smart (merge) ou alerte conflit
```

### Étape 4 : Relâcher le verrou (Fermer fichier)

```
1. Utilisateur ferme EMSP_v0.1.xlsx
2. App web détecte fermeture
3. Flask :
   a) Supprime (.emsp_lock)
   b) Marque : UNLOCKED
   c) Tout le monde voit ✅ VERT
   d) Archive version (EMSP_v0.1_backup_20260610_1422.xlsx)
```

---

## 🔐 DÉVERROUILLAGE D'URGENCE (Admin only)

### Cas 1 : Quelqu'un oublie de fermer (17h, fin de journée)

```
Admin va sur : /admin/force-unlock

Voit :
  • USER003 a verrouillé à 14h05
  • Aucune modification depuis 16h30
  • Fichier probablement abandonné

Action :
  [Forcer déverrouillage]
  → Supprime (.emsp_lock)
  → Envoie email : "Fichier relâché"
```

### Cas 2 : Crash serveur / problème technique

```
(.emsp_lock) reste bloqué même après fermeture

Procédure :
1. Admin vérifie : utilisateur pas connecté
2. Supprime manuellement (.emsp_lock)
3. Teste : fichier OK ?
4. Relance Flask
5. Logs : "Déverrouillage d'urgence par ADMIN"
```

---

## 📊 LOGS DE VERROUS

### Onglet VERROUS (monitoring)

```
Date/Heure    | Utilisateur      | Action      | Fichier         | Durée
──────────────────────────────────────────────────────────────────────────
10/06 14:05   | USER003          | LOCK        | EMSP_v0.1.xlsx  | 
10/06 14:22   | USER003          | UNLOCK      | EMSP_v0.1.xlsx  | 17 min
10/06 14:30   | USER002          | LOCK        | EMSP_v0.1.xlsx  |
10/06 14:45   | USER002          | UNLOCK      | EMSP_v0.1.xlsx  | 15 min
10/06 15:00   | USER999          | LOCK        | GMAO_v0.1.xlsx  |
10/06 15:35   | ADMIN            | FORCE_UL    | GMAO_v0.1.xlsx  | 35 min (forcé)
```

---

## 🔄 SYNCHRONISATION (Multi-établissement)

**Scénario** : EMSP et GMAO sur deux serveurs différents

```
Serveur EMSP                    Serveur GMAO
├─ EMSP_v0.1.xlsx             ├─ GMAO_v0.1.xlsx
└─ .emsp_lock                  └─ .gmao_lock

Chacun indépendant
Pas de conflit possible
```

---

## 🎓 PROCÉDURE JOUR 1

### Formation utilisateurs (30 min)

```
RÈGLE 1 : Vérifier la couleur avant d'ouvrir
  ✅ VERT ? → Ouvrez
  🔴 ROUGE ? → Attendez, ne forcez PAS

RÈGLE 2 : Fermer le fichier quand c'est fait
  ✅ Faire : Fichier → Fermer
  ❌ Pas : Laisser ouvert "pour plus tard"

RÈGLE 3 : Si bloqué, noter et appeler Admin
  ✅ "Fichier bloqué depuis 2h par USER004"
  ✅ Admin déverrouille
  ❌ Pas : Ouvrir en mode "lecture seule"
```

### Tester le système (15 min)

```
1. USER003 ouvre EMSP → 🔴 ROUGE pour autres
2. USER002 essaie d'ouvrir → Alerte "Fichier en utilisation"
3. USER003 ferme → ✅ VERT pour tous
4. USER002 ouvre → OK
5. Vérifier historique dans VERROUS
```

---

## ✅ Checklist déploiement

- [ ] Système de verrous implémenté
- [ ] Indicateur rouge/vert visible
- [ ] Fichier (.lock) crée/supprime automatiquement
- [ ] Interface de déverrouillage (Admin only)
- [ ] Logs de verrous actifs
- [ ] Formation utilisateurs (15 min)
- [ ] Test du système (multi-users)
- [ ] Procédure d'urgence documentée
- [ ] Email de notification (if verrouillé)

---

**Version** : 22 mai 2026
**Audience** : Tous les utilisateurs + Admin
**Criticité** : ⭐⭐⭐⭐⭐ (Très élevée)
