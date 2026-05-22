# 🎯 GUIDE DE CONFIGURATION SUR PLACE (Jour 1-3 aux Comores)

**Document commun EMSP & GMAO**
**À lire AVANT d'arriver aux Comores**

---

## 📌 Vue d'ensemble

Tu as raison : **tout doit être à zéro**, puis configuré correctement avec les équipes locales.

Trois piliers critiques avant de commencer :

1. **👥 Gestion des utilisateurs** (Qui a accès à quoi ?)
2. **📋 Listes déroulantes** (Éviter les inventions données)
3. **🔒 Accès concurrent** (Une seule personne à la fois sur Excel)

---

## PILIER 1 : GESTION DES UTILISATEURS

### Documents disponibles
- **USER-MANAGEMENT.md** : Modèle complet, 5 rôles prédéfinis

### À faire jour 1 (2-3h)

#### 1. Réunion avec direction (1h)

Identifier les utilisateurs :

```
EMSP :
  Admin (Bernard) : 1 personne
  Superviseur (Direction) : nom + email ?
  Opérateurs (Saisie) : 3-5 personnes
  Validateurs (Approbation) : 1-2 personnes

GMAO :
  Admin (Bernard) : 1 personne
  Superviseur (Direction) : nom ?
  Opérateurs (Techniciens) : 3-5 personnes
  Validateurs : 1-2 personnes
```

#### 2. Créer fichier de configuration (30 min)

`config/users.json` avec :
```json
{
  "users": [
    {"id": "USER001", "nom": "Bernard", "role": "ADMIN", ...},
    {"id": "USER002", "nom": "Directeur", "role": "SUPERVISEUR", ...}
  ],
  "roles": [
    {"code": "ADMIN", "label": "Administrateur", ...},
    {"code": "OPERATEUR", "label": "Opérateur", ...}
  ]
}
```

#### 3. Matrice des droits (30 min)

Pour chaque rôle, définir :
- ✅ Peut créer données ?
- ✅ Peut modifier ses propres données ?
- ✅ Peut modifier données des autres ?
- ✅ Peut consulter ?
- ✅ Peut supprimer ?
- ✅ Peut modifier structure Excel ?

#### 4. Tests d'accès (30 min)

Chaque utilisateur teste depuis son PC :
```
USER002 (Superviseur) → http://192.168.1.100:5000
→ Voit les données
→ Peut consulter
→ NE PEUT PAS créer/modifier
```

### Checklist jour 1

- [ ] Identifié tous les utilisateurs
- [ ] Créé users.json
- [ ] Défini matrice de droits
- [ ] Chaque utilisateur a numéro ID
- [ ] Chaque utilisateur a testé son accès
- [ ] Audit trail activé (tracer qui fait quoi)

---

## PILIER 2 : LISTES DÉROULANTES

### Documents disponibles
- **DROPDOWN-LISTS-MANAGEMENT.md** : Listes EMSP et GMAO, gestion dynamique

### Problème à éviter

```
❌ Mauvais :
EMSP - FORMATIONS
├─ "Infirmière"
├─ "Formation Infirmière"   ← même chose, écrite différemment
└─ "infirmière"             ← minuscule

Résultat : Filtres cassés, données fragmentées
```

```
✅ Bon :
EMSP - FORMATIONS
└─ "Formation Infirmière"   ← une seule version
```

### À faire jour 1-2 (2-3h)

#### 1. Audit des listes existantes (2h)

Avec direction/opérateurs, valider CHAQUE élément :

**EMSP** :
```
Types de formations ?
  ☐ Licence
  ☐ Master
  ☐ Spécialisation
  ☐ Certificat
  ☐ Formation continue
  Manquants ? Doublons ?
```

**GMAO** :
```
Catégories d'équipements ?
  ☐ Moniteur cardio
  ☐ Défibrillateur
  ☐ Pompe à infusion
  ☐ ... (tous les types d'équipements en place)
  Manquants ? Marques spécifiques à ajouter ?
```

#### 2. Créer onglet LISTES (1h)

Structure Excel :

```
Onglet LISTES (caché/masqué)
│
├─ Colonne A : TYPES_FORMATIONS
│  ├─ Licence
│  ├─ Master
│  ├─ Spécialisation
│  └─ ...
│
├─ Colonne B : SALLES
│  ├─ Amphi 101
│  ├─ Salle 102
│  └─ ...
│
├─ Colonne C : FORMATEURS
│  ├─ Dr. Martin
│  ├─ Pr. Sophie
│  └─ ...
│
└─ Colonne D : STATUTS
   ├─ Planifiée
   ├─ En cours
   └─ ...
```

#### 3. Configurer validations (30 min)

Pour chaque colonne qui utilise dropdown :

Excel → Données → Validité
```
Critère : Liste
Source : =TYPES_FORMATIONS
Message : "Sélectionner dans la liste"
```

#### 4. Former opérateurs (1h)

**Règle d'or** : 
```
Si vous ne voyez pas l'élément → Ne l'inventez PAS
Appelez Admin pour l'ajouter
```

Montrer comment ajouter :
```
1. Admin ouvre onglet LISTES
2. Ajoute nouveau ligne
3. Relance Flask
4. Élément apparaît dans dropdown
```

### Checklist jour 2

- [ ] Audité TOUS les types/catégories possibles
- [ ] Créé onglet LISTES avec tous les éléments
- [ ] Configuré validations sur colonnes
- [ ] Formateurs opérateurs (ne pas inventer)
- [ ] Procédure "ajouter élément" documentée
- [ ] Admin comprend comment maintenir

---

## PILIER 3 : ACCÈS CONCURRENT (VERROUS)

### Documents disponibles
- **CONCURRENT-ACCESS-CONTROL.md** : Système verrous + indicateurs

### Problème à éviter

```
❌ Mauvais :
14h00 : USER003 ouvre EMSP_v0.1.xlsx
14h05 : USER002 ouvre AUSSI → "Ouvrir en mode lecture seule"
14h30 : USER002 pense modifier → Les modifications sont perdues

Result : Frustration, perte de données
```

```
✅ Bon :
Écran : "🔴 Fichier en utilisation par USER003 depuis 14h00"
USER002 : "Attend 5 minutes"
14h05 : USER003 ferme → "✅ Disponible"
USER002 : Peut ouvrir maintenant
```

### À faire jour 1-2 (1-2h)

#### 1. Implémenter système de verrous (1h)

Flask doit créer `.emsp_lock` quand fichier ouvert :

```python
# app.py
import json
from datetime import datetime

def lock_file(user_id, user_name):
    lock_data = {
        "status": "LOCKED",
        "locked_by": user_id,
        "user_name": user_name,
        "lock_time": datetime.now().isoformat(),
        "file": "EMSP_v0.1.xlsx"
    }
    with open('.emsp_lock', 'w') as f:
        json.dump(lock_data, f)

def unlock_file():
    if os.path.exists('.emsp_lock'):
        os.remove('.emsp_lock')

def get_lock_status():
    if os.path.exists('.emsp_lock'):
        with open('.emsp_lock', 'r') as f:
            return json.load(f)
    return None
```

#### 2. Créer interface status (30 min)

Dashboard affiche :

```
✅ VERT FIXE
"Fichier disponible"
Dernière modification : 10/06 15h22 par Bernard

OU

🔴 ROUGE CLIGNOTANT
"⚠️ Fichier en utilisation"
Utilisé par : USER003 (Secrétaire EMSP)
Depuis : 14h05
[Attendre] [Envoyer message] [Forcer déverrouillage]
```

#### 3. Formation utilisateurs (30 min)

**Règles simples** :

```
RÈGLE 1 : Vérifier couleur avant d'ouvrir
  ✅ VERT ? → Ouvrez
  🔴 ROUGE ? → Attendez

RÈGLE 2 : Fermer quand c'est fini
  Fichier → Fermer (IMPORTANT)

RÈGLE 3 : Si bloqué longtemps
  Appeler Admin pour déverrouiller
```

#### 4. Test du système (30 min)

```
1. USER003 ouvre EMSP → 🔴 ROUGE
2. USER002 essaie → Alerte "Fichier en utilisation"
3. USER003 ferme → ✅ VERT
4. USER002 ouvre → OK
5. Vérifier logs
```

### Checklist jour 2

- [ ] Système de verrous implémenté
- [ ] Indicateur rouge/vert visible
- [ ] Formation utilisateurs (15 min)
- [ ] Test multi-utilisateurs
- [ ] Procédure déverrouillage d'urgence (Admin)
- [ ] Logs actifs

---

## 📅 TIMELINE JOUR 1-3

### JOUR 1 (Installation + Utilisateurs)

```
Matin
├─ 09h-11h : Réunion direction (identifier utilisateurs)
├─ 11h-12h : Créer users.json
└─ 14h-15h : Tests d'accès

Après-midi
├─ 15h-16h : Formation utilisateurs (rôles)
└─ 16h-17h : Chaque utilisateur teste

Soir
└─ Audit trail fonctionne
```

### JOUR 2 (Listes + Verrous)

```
Matin
├─ 09h-11h : Audit listes déroulantes
├─ 11h-12h : Créer onglet LISTES
└─ 14h-15h : Configurer validations

Après-midi
├─ 15h-16h : Formation listes (ne pas inventer)
├─ 16h-17h : Système verrous implémenté
└─ 17h : Test verrous

Soir
└─ Dashboard rouge/vert visible
```

### JOUR 3 (Tests + Documentation)

```
Matin
├─ 09h-11h : Tests complets multi-utilisateurs
├─ 11h-12h : Documentation locale créée
└─ 14h-15h : Formation complète (30 min par groupe)

Après-midi
├─ 15h-16h : Tests réels avec opérateurs
├─ 16h-17h : Ajustements basés feedback
└─ 17h : Go-live

Soir
└─ Monitoring première utilisation
```

---

## 📋 CHECKLIST COMPLÈTE (À remplir sur place)

### JOUR 1 : UTILISATEURS

- [ ] Réunion direction complétée
- [ ] Liste finale utilisateurs établie
- [ ] Fichier users.json créé
- [ ] Chaque utilisateur a ID + password (ou equiv)
- [ ] Chaque utilisateur a testé accès
- [ ] Rôles compris par tous
- [ ] Audit trail visible

### JOUR 2 : LISTES + VERROUS

- [ ] Listes déroulantes auditées
- [ ] Onglet LISTES créé avec TOUS les éléments
- [ ] Validations configurées
- [ ] Formation "ne pas inventer" (compris)
- [ ] Système verrous implémenté
- [ ] Indicateur rouge/vert visible
- [ ] Formation verrous (30 min)

### JOUR 3 : TESTS + GO-LIVE

- [ ] Tests multi-utilisateurs réussis
- [ ] Aucune perte de données observée
- [ ] Déverrouillage d'urgence testé (Admin)
- [ ] Documentation locale disponible
- [ ] Formation complète terminée
- [ ] Monitoring première journée

---

## 🚀 APRÈS JOUR 3

### Maintenance quotidienne

**Si quelqu'un dit** : "On a oublié de mettre [équipement] dans la liste"

```
Procédure rapide (5 min) :
1. Admin ouvre onglet LISTES
2. Ajoute la ligne
3. Relance Flask
4. C'est disponible dans dropdown
```

**Si quelqu'un oublie de fermer Excel** (fin de journée)

```
Procédure (2 min) :
1. Admin voit 🔴 ROUGE depuis 4h
2. Force déverrouillage
3. Email : "Fichier relâché"
4. Tout le monde peut accéder demain
```

---

## 📞 CONTACTS CLÉS

Identifier et noter (jour 1) :

```
EMSP :
  Admin local : _____________ (Email: _____)
  Direction : _____________ (Email: _____)
  Support IT : _____________ (Email: _____)

GMAO :
  Admin local : _____________ (Email: _____)
  Direction : _____________ (Email: _____)
  Support IT : _____________ (Email: _____)

Bernard (France) : contact@webcreatys.com
WhatsApp : +33 9 70 46 33 88
```

---

## 🎯 KPIs DE SUCCÈS (jour 3)

```
✅ 0 utilisateur "invente" données (100% utilise listes)
✅ 0 corruption de données (verrous fonctionnent)
✅ 5+ utilisateurs accèdent sans problème
✅ Audit trail traçable
✅ Admin peut ajouter/retirer utilisateurs facilement
✅ Admin peut ajouter éléments aux listes en 2 min
✅ Déverrouillage d'urgence documenté et testé
```

---

**Version** : 22 mai 2026
**Audience** : Bernard + équipes locales
**Criticité** : ⭐⭐⭐⭐⭐ (Très élevée)
**Lecture recommandée** : Avant arrivée aux Comores
