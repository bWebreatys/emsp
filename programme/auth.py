# -*- coding: utf-8 -*-
"""AUTHENTIFICATION & JOURNAL D'AUDIT (stockage LOCAL hors depot).

Les mots de passe ne sont JAMAIS stockes en clair : seules des empreintes
(hash pbkdf2:sha256, via werkzeug) sont conservees, dans instance/comptes.json,
fichier exclu du depot (.gitignore) et du zip de livraison. Les DROITS restent
dans P1_Roles (classeur), definis par l'admin. Ce module ne gere que l'identite
(qui se connecte) et la tracabilite (qui a fait quoi, quand).
"""
import os
import json
import csv
import secrets
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import config


def _ensure_dir():
    os.makedirs(config.INSTANCE_DIR, exist_ok=True)


def _now():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def _charger():
    try:
        with open(config.AUTH_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {}


def _sauver(d):
    _ensure_dir()
    with open(config.AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def existe(login):
    return str(login).strip() in _charger()


def definir_mdp(login, mdp, doit_changer=False):
    """Cree/ecrase l'empreinte du mot de passe d'un login. Jamais de clair stocke."""
    login = str(login).strip()
    if not login or not mdp:
        return False
    d = _charger()
    e = d.get(login, {})
    e["hash"] = generate_password_hash(mdp, method="pbkdf2:sha256")
    e["doit_changer"] = bool(doit_changer)
    e.setdefault("cree_le", _now())
    e["maj_le"] = _now()
    d[login] = e
    _sauver(d)
    return True


def verifier(login, mdp):
    e = _charger().get(str(login).strip())
    if not e or "hash" not in e:
        return False
    try:
        return check_password_hash(e["hash"], mdp or "")
    except Exception:
        return False


def doit_changer(login):
    e = _charger().get(str(login).strip())
    return bool(e and e.get("doit_changer"))


def changer_mdp(login, ancien, nouveau):
    if not verifier(login, ancien):
        return False, "Ancien mot de passe incorrect."
    if not nouveau or len(nouveau) < 4:
        return False, "Le nouveau mot de passe doit faire au moins 4 caracteres."
    definir_mdp(login, nouveau, doit_changer=False)
    return True, "Mot de passe modifie."


# ---------------------------------------------------------------------------
# GOUVERNANCE DES COMPTES (V1.43) — mot de passe aleatoire, rubrique, couleur,
# validite par annee scolaire. Tout est stocke dans instance/comptes.json (hors
# depot) ; le classeur (P1_Roles) ne porte que login + droits par module.
# ---------------------------------------------------------------------------
def generer_mdp(longueur=None):
    """Mot de passe aleatoire (CSPRNG), alphabet sans caracteres ambigus."""
    n = int(longueur or config.MDP_LONGUEUR)
    alpha = config.MDP_ALPHABET
    return "".join(secrets.choice(alpha) for _ in range(n))


def _fin_annee_scolaire(d=None):
    """Date (datetime.date) de fin de l'annee scolaire courante = prochain 31/07
    a partir de d (inclus). Avant ou le 31/07 -> 31/07 de l'annee ; apres -> annee+1."""
    d = d or datetime.date.today()
    fin = datetime.date(d.year, config.ANNEE_SCOLAIRE_FIN_MOIS, config.ANNEE_SCOLAIRE_FIN_JOUR)
    if d > fin:
        fin = datetime.date(d.year + 1, config.ANNEE_SCOLAIRE_FIN_MOIS, config.ANNEE_SCOLAIRE_FIN_JOUR)
    return fin


def _prochain_31_07(apres):
    """Premier 31/07 STRICTEMENT posterieur a la date `apres`."""
    fin = datetime.date(apres.year, config.ANNEE_SCOLAIRE_FIN_MOIS, config.ANNEE_SCOLAIRE_FIN_JOUR)
    if apres >= fin:
        fin = datetime.date(apres.year + 1, config.ANNEE_SCOLAIRE_FIN_MOIS, config.ANNEE_SCOLAIRE_FIN_JOUR)
    return fin


def _fmt(d):
    return d.strftime("%d/%m/%Y")


def _parse(s):
    try:
        return datetime.datetime.strptime(str(s).strip(), "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None


def definir_attributs(login, rubrique=None, couleur=None, valide_jusqu=None):
    """Met a jour, sans toucher au mot de passe, les attributs operationnels d'un
    compte (rubrique, couleur d'identite, fin de validite). Cree l'entree au besoin."""
    login = str(login).strip()
    if not login:
        return False
    d = _charger()
    e = d.get(login, {})
    if rubrique is not None:
        e["rubrique"] = str(rubrique).strip()
    if couleur is not None:
        e["couleur"] = str(couleur).strip()
    if valide_jusqu is not None:
        e["valide_jusqu"] = str(valide_jusqu).strip()
    e.setdefault("cree_le", _now())
    e["maj_le"] = _now()
    d[login] = e
    _sauver(d)
    return True


def attributs(login):
    """Attributs operationnels d'un compte (dict) : rubrique, couleur, valide_jusqu,
    doit_changer, cree_le, maj_le. Dict vide si le compte n'existe pas."""
    return dict(_charger().get(str(login).strip(), {}))


def couleur(login):
    """Couleur d'identite CHOISIE (informatique), ou None si non definie."""
    c = _charger().get(str(login).strip(), {}).get("couleur")
    return c or None


def initialiser_validite(login):
    """Fixe la validite a la fin de l'annee scolaire courante si absente. Renvoie la date (str)."""
    login = str(login).strip()
    e = _charger().get(login, {})
    vj = e.get("valide_jusqu")
    if not vj:
        vj = _fmt(_fin_annee_scolaire())
        definir_attributs(login, valide_jusqu=vj)
    return vj


def renouveler(login):
    """Repousse la validite au 31/07 SUIVANT, sans toucher au mot de passe.
    Renvoie la nouvelle date (str) ou None si le compte est inconnu."""
    login = str(login).strip()
    d = _charger()
    if login not in d:
        return None
    courant = _parse(d[login].get("valide_jusqu")) or datetime.date.today()
    base = max(courant, datetime.date.today())
    nouvelle = _fmt(_prochain_31_07(base))
    definir_attributs(login, valide_jusqu=nouvelle)
    return nouvelle


def est_expire(login):
    """Vrai si la validite est depassee (expiration NON bloquante : info seulement).
    Pas de date de validite -> jamais expire."""
    vj = _parse(_charger().get(str(login).strip(), {}).get("valide_jusqu"))
    return bool(vj and vj < datetime.date.today())


def reinitialiser(login):
    """Reinitialisation par l'informatique : genere un mot de passe ALEATOIRE, a
    changer au prochain login. Renvoie (ok, mdp_en_clair) — affiche une seule fois."""
    login = str(login).strip()
    if not login:
        return False, ""
    mdp = generer_mdp()
    definir_mdp(login, mdp, doit_changer=True)
    return True, mdp


def supprimer(login):
    d = _charger()
    if str(login).strip() in d:
        del d[str(login).strip()]
        _sauver(d)


def ensure_superadmin():
    """Filet anti-blocage : garantit qu'un superadmin peut se connecter (premier
    lancement ou fichier perdu). Mot de passe initial = config.SUPERUSER_MDP_DEFAUT,
    a changer obligatoirement au premier login."""
    d = _charger()
    change = False
    for login in config.SUPERUSER_LOGINS:
        if login not in d or "hash" not in d.get(login, {}):
            est_formation = (login == getattr(config, "FORMATION_LOGIN", None))
            mdp = config.FORMATION_MDP_DEFAUT if est_formation else config.SUPERUSER_MDP_DEFAUT
            d[login] = {"hash": generate_password_hash(mdp, method="pbkdf2:sha256"),
                        "doit_changer": (False if est_formation else True),
                        "cree_le": _now(), "maj_le": _now()}
            change = True
    if change:
        _sauver(d)


# ---------------------------------------------------------------------------
# JOURNAL D'AUDIT (append-only, local) — "qui a fait quoi, quand"
# ---------------------------------------------------------------------------
_JOURNAL_COLS = ["Horodatage", "Utilisateur", "Action", "Cible", "Detail"]


def journal(login, action, cible="", detail=""):
    """Ajoute une entree au journal d'audit local. Ne journalise JAMAIS de secret."""
    try:
        _ensure_dir()
        neuf = not os.path.exists(config.JOURNAL_FILE)
        with open(config.JOURNAL_FILE, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if neuf:
                w.writerow(_JOURNAL_COLS)
            w.writerow([_now(), str(login), str(action), str(cible), str(detail)])
    except Exception:
        pass  # le journal ne doit jamais bloquer une operation metier


def lire_journal(limite=300, f_login="", f_action=""):
    if not os.path.exists(config.JOURNAL_FILE):
        return []
    try:
        with open(config.JOURNAL_FILE, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    except Exception:
        return []
    if len(rows) <= 1:
        return []
    entetes, data = rows[0], rows[1:]
    if f_login:
        data = [r for r in data if len(r) > 1 and f_login.lower() in r[1].lower()]
    if f_action:
        data = [r for r in data if len(r) > 2 and f_action.lower() in r[2].lower()]
    data = data[-limite:][::-1]   # les plus recentes d'abord
    return [dict(zip(entetes, r)) for r in data]
