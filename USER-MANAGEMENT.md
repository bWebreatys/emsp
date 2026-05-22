# 👥 Gestion des Utilisateurs et Droits d'Accès

**Document commun EMSP & GMAO**
**Applicable dès jour 1 aux Comores**

---

## 🎯 Vue d'ensemble

En raison de l'absence d'authentification dans Flask v0.1, la gestion des utilisateurs se fera par :
1. **Configuration au démarrage** (fichier de configuration)
2. **Listing des utilisateurs** (qui a accès à quoi)
3. **Niveaux de droits** (consultation vs modification)
4. **Logs d'audit** (qui a fait quoi et quand)

---

## 📋 Modèle de gestion des utilisateurs

### Profil 1 : ADMINISTRATEUR

**Droits** :
- ✅ Créer/modifier/supprimer utilisateurs
- ✅ Modifier structure Excel (ajouter colonnes)
- ✅ Accès à tous les onglets
- ✅ Gérer les listes déroulantes
- ✅ Consulter les logs d'audit
- ✅ Sauvegarder / restaurer données

**Exemple** : Bernard (mission), ou responsable IT local

**Nombre recommandé** : 1-2 max

---

### Profil 2 : SUPERVISEUR (Direction)

**Droits** :
- ✅ Consultation de tous les onglets (lecture seule)
- ✅ Accès aux tableaux de bord/KPIs
- ✅ Rapports d'activité
- ❌ Modification données (sauf cas exceptionnels)
- ❌ Modification structure
- ❌ Gestion utilisateurs

**Exemple** : Directeur EMSP, Chef projet

**Nombre recommandé** : 1-3

---

### Profil 3 : OPÉRATEUR (Saisie de données)

**Droits** :
- ✅ Créer nouvelles données (formations, équipements, etc.)
- ✅ Modifier ses propres saisies (le jour même)
- ✅ Accès aux listes déroulantes
- ❌ Modifier données des autres utilisateurs
- ❌ Supprimer données
- ❌ Accès structure Excel

**Exemple** : Secrétaire EMSP, Technicien GMAO

**Nombre recommandé** : 3-5 par établissement

---

### Profil 4 : VALIDATEUR

**Droits** :
- ✅ Consultation données
- ✅ Approuver/rejeter saisies des opérateurs
- ✅ Corriger erreurs
- ✅ Marquer comme "validé"
- ❌ Supprimer
- ❌ Modifier structure

**Exemple** : Chef de service, Pharmacien (GMAO)

**Nombre recommandé** : 1-2 par établissement

---

### Profil 5 : CONSULTATION (Lecture seule)

**Droits** :
- ✅ Lire toutes les données
- ✅ Générer rapports
- ❌ Créer/modifier/supprimer
- ❌ Accès listes déroulantes

**Exemple** : Stagiaires, visiteurs

**Nombre recommandé** : 0-2

---

## 🔐 Matrice des droits d'accès

```
                        Admin  Superviseur  Opérateur  Validateur  Consultation
────────────────────────────────────────────────────────────────────────────────
Créer données            ✅       ❌           ✅          ❌            ❌
Modifier propres données ✅       ❌           ✅          ✅            ❌
Modifier autres données  ✅       ❌           ❌          ✅            ❌
Supprimer               ✅       ❌           ❌          ❌            ❌
Consulter tous          ✅       ✅           ✅          ✅            ✅
Consulter logs          ✅       ✅           Propres     Propres       ❌
Gérer listes déroulantes ✅      ❌           ❌          ❌            ❌
Gérer utilisateurs      ✅       ❌           ❌          ❌            ❌
Modifier structure      ✅       ❌           ❌          ❌            ❌
```

---

## 📝 Fichier de configuration utilisateurs

À créer : `config/users.json`

```json
{
  "users": [
    {
      "id": "USER001",
      "nom": "Bernard Leglise",
      "role": "ADMIN",
      "email": "bernard@webcreatys.com",
      "etablissement": "EMSP",
      "actif": true,
      "date_creation": "2026-06-01",
      "dernier_acces": "2026-06-10"
    },
    {
      "id": "USER002",
      "nom": "Directeur EMSP",
      "role": "SUPERVISEUR",
      "email": "directeur@emsp.km",
      "etablissement": "EMSP",
      "actif": true,
      "date_creation": "2026-06-02",
      "dernier_acces": "2026-06-10"
    },
    {
      "id": "USER003",
      "nom": "Secrétaire EMSP",
      "role": "OPERATEUR",
      "email": "secretaire@emsp.km",
      "etablissement": "EMSP",
      "actif": true,
      "date_creation": "2026-06-03",
      "dernier_acces": "2026-06-10"
    }
  ],
  "roles": [
    {
      "code": "ADMIN",
      "label": "Administrateur",
      "description": "Accès complet, gestion utilisateurs et structure"
    },
    {
      "code": "SUPERVISEUR",
      "label": "Superviseur",
      "description": "Consultation et rapports, pas de modification"
    },
    {
      "code": "OPERATEUR",
      "label": "Opérateur",
      "description": "Saisie et modification propres données"
    },
    {
      "code": "VALIDATEUR",
      "label": "Validateur",
      "description": "Consultation et approbation saisies"
    },
    {
      "code": "CONSULTATION",
      "label": "Consultation",
      "description": "Lecture seule"
    }
  ]
}
```

---

## 🛠️ Implémentation initiale (jour 1)

### Étape 1 : Identifier les utilisateurs (2h)

En arrivant aux Comores, réunion avec la direction pour identifier :

```
ÉMSP :
├─ Admin (Bernard) : 1 personne
├─ Superviseur (Direction) : nom ?
├─ Opérateurs (Saisie) : nom ?
└─ Validateurs (Approbation) : nom ?

GMAO :
├─ Admin (Bernard) : 1 personne
├─ Superviseur (Direction) : nom ?
├─ Opérateurs (Techniciens) : nom ?
└─ Validateurs (Chef service) : nom ?
```

### Étape 2 : Créer fichier de configuration (30 min)

À partir de la réunion, créer `config/users.json` avec tous les utilisateurs.

### Étape 3 : Paramétrer les droits dans Excel (1h)

Pour chaque utilisateur, définir :
- Quels onglets peut-il voir ?
- Peut-il modifier ou seulement lire ?
- À quels champs a-t-il accès ?

### Étape 4 : Tester accès (30 min)

Chaque utilisateur teste son accès depuis son PC.

---

## 📊 Gestion des droits dans Excel (côté données)

### Colonne de suivi : "CREE_PAR"

Ajouter à chaque onglet de saisie :

| Colonne | Type | Description | Obligatoire |
|---------|------|-------------|-------------|
| CREE_PAR | Texte | User ID qui a créé la ligne | ✅ |
| DATE_CREATION | Date | Date/heure de création | ✅ |
| MODIFIE_PAR | Texte | Dernier utilisateur qui a modifié | ⚠️ |
| DATE_MODIFICATION | Date | Date/heure dernière modification | ⚠️ |
| STATUT | Dropdown | BROUILLON / VALIDÉ / ARCHIVÉ | ✅ |
| VALIDATEUR | Texte | User ID qui a validé | ⚠️ |

### Logique de contrôle

```
Si STATUT = "BROUILLON"
  └─ Modifiable par : CREE_PAR uniquement + VALIDATEUR
  └─ Supprimable par : CREE_PAR uniquement

Si STATUT = "VALIDÉ"
  └─ Modifiable par : VALIDATEUR seulement
  └─ Non supprimable
```

---

## 🔐 Sécurité et audit

### Logs d'audit (obligatoire)

Créer un onglet **AUDIT** avec :

```
| DATE_HEURE | UTILISATEUR | ACTION | OBJET | ANCIEN_VALEUR | NOUVEAU_VALEUR | STATUT |
|------------|------------|--------|-------|----------------|----------------|--------|
| 2026-06-10 14:35 | USER003 | CREATION | FORMATIONS | - | MED001 | OK |
| 2026-06-10 14:40 | USER003 | MODIFICATION | FORMATIONS.DUREE | 5 jours | 6 jours | OK |
| 2026-06-10 15:00 | USER002 | VALIDATION | FORMATIONS.MED001 | BROUILLON | VALIDÉ | OK |
| 2026-06-10 15:05 | USER999 | TENTATIVE_ACCES | FORMATIONS | - | - | REFUSÉ |
```

### Points à auditer

- ✅ Création de ligne (qui, quand, quoi)
- ✅ Modification (qui, quand, ancien, nouveau)
- ✅ Suppression (qui, quand, quoi)
- ✅ Validation (qui, quand)
- ✅ Tentatives d'accès non autorisé (pour bloquer)

---

## 📱 Interface de gestion utilisateurs (à ajouter à Flask)

### Écran 1 : Liste des utilisateurs

```
┌─ GESTION DES UTILISATEURS ───────────────────────────────────┐
│                                                               │
│ 🔍 Chercher : [       ]  🔄 Rafraîchir  ➕ Nouvel utilisateur │
│                                                               │
│ ID      | Nom                | Rôle         | Établissement   │
│────────────────────────────────────────────────────────────────│
│ USER001 | Bernard Leglise    | ADMIN        | EMSP            │
│ USER002 | Directeur EMSP     | SUPERVISEUR  | EMSP            │
│ USER003 | Secrétaire EMSP    | OPERATEUR    | EMSP            │
│ USER004 | Chef Pharmacie     | VALIDATEUR   | GMAO            │
│                                                               │
│ [Modifier] [Désactiver] [Audit]                              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Écran 2 : Créer/Modifier utilisateur

```
┌─ NOUVEL UTILISATEUR ────────────────────────────────────────┐
│                                                              │
│ Nom complet          : [________________________]            │
│ Email               : [________________________]            │
│ Rôle                : [ADMIN ▼]                            │
│ Établissement       : [EMSP ▼]                             │
│ Statut              : ☑ Actif                              │
│                                                              │
│ Permissions spéciales:                                       │
│   ☐ Peut créer utilisateurs                                │
│   ☐ Peut modifier structure Excel                          │
│   ☐ Peut supprimer données                                 │
│   ☐ Peut consulter logs                                    │
│                                                              │
│ [Enregistrer] [Annuler]                                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Écran 3 : Journal d'audit

```
┌─ AUDIT TRAIL ──────────────────────────────────────────────┐
│                                                             │
│ 🔍 Chercher : [Utilisateur______] [Action____▼] [Période ▼]│
│                                                             │
│ Date/Heure      | Utilisateur      | Action    | Objet    │
│─────────────────────────────────────────────────────────────│
│ 10/06 14:35     | USER003          | CREATE    | FORM001  │
│ 10/06 14:40     | USER003          | MODIFY    | FORM001  │
│ 10/06 15:00     | USER002          | APPROVE   | FORM001  │
│ 10/06 15:05     | USER999          | ACCESS    | DENIED   │
│                                                             │
│ [Exporter CSV] [Imprimer]                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Implémentation Flask (pseudocode)

```python
# config/users.py
USERS = {
    'USER001': {
        'nom': 'Bernard Leglise',
        'role': 'ADMIN',
        'droits': ['CREATE', 'READ', 'UPDATE', 'DELETE', 'ADMIN']
    },
    'USER003': {
        'nom': 'Secrétaire EMSP',
        'role': 'OPERATEUR',
        'droits': ['CREATE', 'READ', 'UPDATE_OWN']
    }
}

# app.py
@app.before_request
def check_permissions():
    user_id = request.args.get('user', 'GUEST')
    if user_id == 'GUEST':
        flash('Identifiez-vous d\'abord')
        return redirect('/')
    
    g.user = USERS.get(user_id)
    if not g.user:
        flash('Utilisateur non trouvé')
        return redirect('/')

@app.route('/formations', methods=['POST'])
def create_formation():
    if 'CREATE' not in g.user['droits']:
        flash('Permission refusée')
        return redirect('/formations')
    
    # Ajouter CREE_PAR automatiquement
    data = request.form
    data['CREE_PAR'] = g.user['nom']
    data['DATE_CREATION'] = datetime.now()
    
    # Sauvegarder dans Excel
    # Log dans audit
    log_audit('CREATE', 'FORMATIONS', data)
```

---

## 📋 Checklist déploiement (Jour 1-2)

- [ ] Réunion avec direction (identifier utilisateurs)
- [ ] Créer fichier `config/users.json`
- [ ] Tester accès chaque utilisateur
- [ ] Configurer logs d'audit
- [ ] Entraîner les utilisateurs à se logger
- [ ] Tester audit trail
- [ ] Documenter procédures d'ajout utilisateur
- [ ] Créer liste de contacts (qui contacter pour accès)

---

## 🔄 Maintenance en cours de mission

### Ajouter nouvel utilisateur (procédure rapide)

1. Modifier `config/users.json` (ajouter ligne)
2. Relancer Flask (CTRL+C puis `python app.py`)
3. Tester accès avec nouvel utilisateur

### Retirer accès utilisateur

1. Modifier rôle ou marquer "inactif" dans config
2. Relancer Flask
3. Historique dans audit reste (traçabilité)

---

## 🎓 Points clés

1. **5 rôles prédéfinis** (Admin, Superviseur, Opérateur, Validateur, Consultation)
2. **Fichier de config** (users.json facile à modifier)
3. **Logs d'audit** (traçabilité complète)
4. **Droits granulaires** (qui peut faire quoi)
5. **Interface de gestion** (ajouter utilisateurs facilement)

---

**Version** : 22 mai 2026
**Audience** : Bernard (mission) + équipes Comores
**Prochaine étape** : Adapter selon besoins locaux
