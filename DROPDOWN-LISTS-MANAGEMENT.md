# 📋 Gestion des Listes Déroulantes (Dropdowns)

**Document commun EMSP & GMAO**
**Applicable dès jour 1 aux Comores**

---

## 🎯 Vue d'ensemble

Les listes déroulantes sont **CRITIQUES** pour :
- ✅ Éviter les erreurs de saisie (fautes, accents, variantes)
- ✅ Standardiser les données (toutes les formations nommées pareil)
- ✅ Faciliter les filtres et recherches (grouper par catégorie)
- ✅ Ajouter dynamiquement (nouvel équipement = ajout à la liste)

**Problème à anticiper** :
Quelqu'un crée "Formation Infirmière" alors qu'il existe déjà "Infirmière" → données fragmentées, filtres ne marchent plus.

---

## 📊 EMSP - Listes déroulantes critiques

### 1. TYPES DE FORMATIONS

**Onglet source** : LISTES (hidden)
**Cellule** : A2:A50 nommée `TYPES_FORMATIONS`

```
Licence
Master
Spécialisation
Certificat
Formation continue
Atelier
Séminaire
```

**Utilisation** :
- Onglet FORMATIONS → colonne "Type_Formation"
- Filtre : "Afficher formations de type Master"

**Cas imprévu** : Formation "Diplôme de base" n'existe pas
- Solution : Jour 1, lister ALL types possibles
- Sinon : Ajouter sur place (Admin → LISTES sheet → ajouter ligne)

---

### 2. SALLES

**Onglet source** : LISTES
**Cellule** : B2:B100 nommée `SALLES_LIST`

```
Amphithéâtre 101
Salle de cours 102
Salle de TP 103A
Laboratoire 201
Salle de réunion 1
```

**Utilisation** :
- SESSIONS → "Code_Salle"
- RESERVATIONS → "Code_Salle"
- INTERVENTIONS → "Code_Salle"

**Cas imprévu** : Nouvelle salle construite en juillet
- Solution : Aller dans LISTES, ajouter "Salle 304"
- Excel recharge automatiquement la liste déroulante

---

### 3. FORMATEURS

**Onglet source** : LISTES
**Cellule** : C2:C200 nommée `FORMATEURS_LIST`

```
Dr. Martin Dupont
Pr. Sophie Martin
Mme Aïchatou Hassan
M. Jean Baptiste
```

**Utilisation** :
- SESSIONS → "Code_Formateur"
- INTERVENTIONS → "Code_Formateur"

**Attention** :
- ⚠️ Cohérence avec onglet FORMATEURS_RH
- Si quelqu'un est retraité : le marquer "Inactif" dans FORMATEURS_RH
- Alors l'Admin retire le nom de LISTES

---

### 4. STATUTS

**Onglet source** : LISTES
**Cellule** : D2:D10 nommée `STATUTS_SESSION`

```
Planifiée
En cours
Terminée
Annulée
Reportée
```

**Utilisation** :
- SESSIONS → "Statut"
- Filtre : "Combien de sessions Terminées ce mois ?"

---

## 📦 GMAO - Listes déroulantes critiques

### 1. CATÉGORIES D'ÉQUIPEMENTS (Biomédicaux)

**Onglet source** : LISTES
**Cellule** : A2:A100 nommée `CATEGORIES_BM`

```
Moniteur cardio
Défibrillateur
Pompe à infusion
Ventilateur
Électrocardiographe
Autoclave
Microscope
Centrifugeuse
Réfrigérateur médical
Lampe opératoire
```

**Utilisation** :
- EQUIPEMENTS → "Catégorie"
- Filtre : "Tous les défibrillateurs"
- Alerte : "Maintenance défib due"

**Cas imprévu** : Nouvel équipement "Scanner" n'existe pas
- Solution : Admin ajoute dans LISTES
- Opérateur peut alors créer l'équipement

---

### 2. STATUTS ÉQUIPEMENTS

**Onglet source** : LISTES
**Cellule** : B2:B10 nommée `STATUTS_EQUIPEMENT`

```
Fonctionnel
Défectueux
En réparation
Immobilisé
Hors service
En maintenance préventive
```

**Utilisation** :
- EQUIPEMENTS → "Statut"
- Alerte : "15 équipements Défectueux"

---

### 3. TYPES D'INTERVENTIONS

**Onglet source** : LISTES
**Cellule** : C2:C10 nommée `TYPES_INTERVENTIONS`

```
Maintenance préventive
Réparation corrective
Maintenance urgente
Inspection
Calibrage
Dépannage électrique
Dépannage mécanique
```

**Utilisation** :
- INTERVENTIONS → "Type_Intervention"
- KPI : "Nombre interventions préventives vs correctives"

---

### 4. ÉTATS PIÈCES DÉTACHÉES

**Onglet source** : LISTES
**Cellule** : D2:D10 nommée `ETATS_PIECES`

```
Stock
Commandée
Livrée
Utilisée
Défectueuse
Écartée
```

---

## 🏗️ STRUCTURE RECOMMANDÉE

### Onglet LISTES (caché / masqué)

```
┌─ LISTES (Hidden) ────────────────────────────────────────┐
│                                                            │
│ A (TYPES_FORMATIONS)  B (SALLES)      C (FORMATEURS)     │
│ ──────────────────    ────────────    ─────────────────  │
│ Licence               Amphi 101       Dr. Martin          │
│ Master                Salle 102       Pr. Sophie          │
│ Spécialisation        Labo 201        Mme Aïchatou        │
│ Certificat            Réunion 1       M. Jean Baptiste    │
│ Formation continue                                        │
│                                                            │
│ D (STATUTS)          E (STATUS_EQ)   F (TYPE_INT)        │
│ ──────────────       ────────────    ──────────────      │
│ Planifiée            Fonctionnel     Préventive          │
│ En cours             Défectueux      Corrective          │
│ Terminée             En réparation    Urgente            │
│ Annulée              Immobilisé       Inspection         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Configuration des noms de plages

Dans Excel : Formules → Définir un nom

```
Nom : TYPES_FORMATIONS
Plage : LISTES!$A$2:$A$50

Nom : SALLES_LIST
Plage : LISTES!$B$2:$B$100

Nom : FORMATEURS_LIST
Plage : LISTES!$C$2:$C$200

... etc pour tous les dropdowns
```

### Validation des données

Pour chaque colonne qui utilise un dropdown :

Dans Excel : Données → Validité (Validation)

```
Critère : Liste
Source : =TYPES_FORMATIONS
Message d'erreur : "Type non reconnu. Consulter la liste LISTES"
```

---

## 🚀 GESTION DYNAMIQUE DES LISTES

### Cas 1 : Ajouter un nouvel élément (Admin)

```
Exemple : Nouvelle salle "Salle de conférence" créée

Étapes :
1. Aller à onglet LISTES
2. Colonne B (SALLES), ajouter une ligne
3. Taper "Salle de conférence"
4. Relancer l'app (Flask : CTRL+C puis python app.py)
5. Tester : Créer une session → dropdown affiche la salle
```

### Cas 2 : Retirer un élément (Admin)

```
Exemple : Dr. Martin a pris sa retraite

Étapes :
1. Aller à onglet FORMATEURS_RH
2. Chercher Dr. Martin
3. Marquer "Statut = Retraité"
4. Aller à onglet LISTES
5. Colonne C (FORMATEURS), supprimer la ligne "Dr. Martin"
6. Relancer l'app
```

### Cas 3 : Renommer un élément (Admin)

```
Exemple : "Formation continue" → "Formation continue courte"

Étapes :
1. Aller à onglet LISTES
2. Colonne A, chercher "Formation continue"
3. Corriger en "Formation continue courte"
4. Relancer l'app
5. ⚠️ ATTENTION : Les données existantes gardent l'ancien nom
   Solution : Chercher-remplacer dans FORMATIONS (CTRL+H)
```

---

## 🔧 Interface de gestion (à ajouter à Flask)

### Écran : Gérer listes déroulantes

```
┌─ GESTION DES LISTES ──────────────────────────────────────┐
│ ADMIN ONLY                                                 │
│                                                            │
│ Catégorie : [TYPES_FORMATIONS ▼]                         │
│                                                            │
│ Éléments (⬇ cliquer pour éditer) :                        │
│ ┌────────────────────────────────┐                        │
│ │ ☐ Licence            [✎] [✕]   │                       │
│ │ ☐ Master             [✎] [✕]   │                       │
│ │ ☐ Spécialisation     [✎] [✕]   │                       │
│ │ ☐ Certificat         [✎] [✕]   │                       │
│ │ ☐ Formation continue [✎] [✕]   │                       │
│ │ ☐ Atelier            [✎] [✕]   │                       │
│ │ ☐ Séminaire          [✎] [✕]   │                       │
│ └────────────────────────────────┘                        │
│                                                            │
│ Nouvel élément : [__________________] [Ajouter]          │
│                                                            │
│ [Exporter] [Importer depuis Excel] [Relancer app]        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🎓 PROCÉDURE JOUR 1

### Phase 1 : Audit des listes existantes (2h)

Avec la direction, valider TOUS les éléments existants :

```
EMSP :
☐ Types de formations (vrais types ? manquants ?)
☐ Salles (toutes ? corrections de noms ?)
☐ Formateurs (tous ? qui n'est plus dispo ?)
☐ Statuts (OK ? manquants ?)

GMAO :
☐ Catégories équipements (vrais types ? manquants ?)
☐ Statuts équipements (cohérent ?)
☐ Types interventions (complet ?)
☐ États pièces (OK ?)
```

### Phase 2 : Entraînement opérateurs (1h)

"Si le dropdown ne montre pas ce que vous cherchez : **ne pas inventer**, appeler Admin"

Montrer :
- ✅ Chercher dans la liste
- ✅ Signaler si manque quelque chose
- ❌ Taper à la main (fragmente les données)

### Phase 3 : Procédure d'ajout (30 min)

Admin montre comment ajouter un élément :
1. Onglet LISTES
2. Ajouter ligne
3. Relancer (CTRL+C + python app.py)

---

## 📱 Code Flask pour gérer listes

```python
# app.py
from openpyxl import load_workbook

def get_dropdown_list(list_name):
    """Récupère la liste déroulante depuis Excel"""
    wb = load_workbook('EMSP_v0.1.xlsx')
    listes = wb['LISTES']
    
    # Colonne A = TYPES_FORMATIONS
    if list_name == 'TYPES_FORMATIONS':
        items = [cell.value for cell in listes['A'] if cell.value]
        return items
    
    # Colonne B = SALLES_LIST
    elif list_name == 'SALLES_LIST':
        items = [cell.value for cell in listes['B'] if cell.value]
        return items
    
    # ... etc pour tous les dropdowns

@app.route('/api/dropdown/<list_name>')
def dropdown_api(list_name):
    """API pour charger les dropdowns dynamiquement"""
    items = get_dropdown_list(list_name)
    return jsonify(items)

# Dans le formulaire HTML
<select name="type_formation">
    <option value="">-- Choisir un type --</option>
    <option value="Licence">Licence</option>
    <option value="Master">Master</option>
    ...
</select>

# Ou dynamiquement (JavaScript)
fetch('/api/dropdown/TYPES_FORMATIONS')
    .then(r => r.json())
    .then(items => {
        items.forEach(item => {
            option = document.createElement('option');
            option.value = item;
            option.text = item;
            select.appendChild(option);
        });
    });
```

---

## ⚠️ POINTS CRITIQUES

1. **Une personne par fois** : Onglet LISTES ne peut être modifié que par Admin
2. **Relancer app** : Chaque ajout/suppression nécessite redémarrage Flask
3. **Cohérence** : Si on retire un formateur de LISTES, il était peut-être en SESSIONS
4. **Logs** : Tracer qui a ajouté/supprimé quoi dans les listes
5. **Backup** : Avant modification, exporter LISTES en CSV

---

## 🔄 Maintenance en cours de mission

### Ajouter formation "Diplôme de base"

```
Email reçu : "On a oublié un type de formation : Diplôme de base"

Étapes :
1. Admin ouvre EMSP_v0.1.xlsx
2. Onglet LISTES
3. Colonne A (TYPES_FORMATIONS)
4. Ajouter "Diplôme de base"
5. Fermer Excel
6. Relancer Flask : python app.py
7. Tester : Créer formation → "Diplôme de base" dans dropdown
```

### Renommer "Infirmière" en "Formation Infirmière"

```
1. LISTES sheet
2. Colonne C (FORMATEURS_LIST), chercher "Infirmière"
3. Changer en "Formation Infirmière"
4. MAIS : Les sessions existantes gardent "Infirmière"
5. Utiliser CTRL+H (Chercher-remplacer) dans FORMATEURS
6. Relancer Flask
7. Vérifier que tout s'affiche correctement
```

---

## ✅ Checklist déploiement

- [ ] Auditer TOUS les éléments (jour 1)
- [ ] Noms de plages configurés dans Excel
- [ ] Validation de données activée sur tous les dropdowns
- [ ] Onglet LISTES masqué (hider)
- [ ] Interface de gestion créée dans Flask
- [ ] Admin formé (ajouter/retirer/renommer)
- [ ] Opérateurs comprennent (pas d'invention)
- [ ] Logs d'audit activés pour LISTES
- [ ] Procédure écrite (doc simple pour Admin local)

---

**Version** : 22 mai 2026
**Audience** : Admin + Opérateurs Comores
**Prochaine étape** : Adapter listes selon réalité locale
