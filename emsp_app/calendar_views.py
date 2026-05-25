"""
Gestion du calendrier et réservations
Interface à 3 zones : Calendrier | Timeline | Détails
"""

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
import calendar

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

# ==============================================================================
# ÉCRAN PRINCIPAL : CALENDRIER & RÉSERVATIONS
# ==============================================================================

@calendar_bp.route('/')
@calendar_bp.route('/jour/<date>')
@calendar_bp.route('/salle/<salle_code>')
def calendar_view(date=None, salle_code=None):
    """
    Vue principale calendrier avec 3 zones
    
    Args:
        date: Format YYYY-MM-DD (optionnel, défaut aujourd'hui)
        salle_code: Code salle pour vue filtrée (optionnel)
    """
    
    # Récupérer la date
    if date:
        try:
            selected_date = datetime.strptime(date, '%Y-%m-%d')
        except:
            selected_date = datetime.now()
    else:
        selected_date = datetime.now()
    
    # Données du calendrier (mois)
    today = datetime.now()
    month_data = get_calendar_month(selected_date.year, selected_date.month)
    
    # Données timeline (jour sélectionné)
    timeline_data = get_timeline_day(selected_date, salle_code)
    
    # Données filtres
    filters = {
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'selected_salle': salle_code or 'TOUTES',
        'salles': get_all_salles(),
        'formations': get_all_formations(),
        'statuts': ['CONFIRMÉE', 'ATTENTE', 'ANNULÉE', 'REPORTÉE'],
    }
    
    return render_template('calendar/calendar_view.html',
                         today=today,
                         selected_date=selected_date,
                         month_data=month_data,
                         timeline_data=timeline_data,
                         filters=filters,
                         salle_code=salle_code)

# ==============================================================================
# DONNÉES CALENDRIER MENSUEL
# ==============================================================================

def get_calendar_month(year, month):
    """
    Récupérer données calendrier pour un mois
    
    Returns:
        {
            'year': 2026,
            'month': 6,
            'month_name': 'JUIN',
            'weeks': [
                [
                    {'date': 1, 'day': 'lun', 'reservations': 2, 'selected': False, ...},
                    ...
                ]
            ]
        }
    """
    
    # Récupérer jours du mois
    cal = calendar.monthcalendar(year, month)
    
    # Récupérer toutes réservations du mois
    all_reservations = get_all_reservations(year, month)
    
    weeks = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                # Jour hors du mois
                week_data.append(None)
            else:
                # Jour du mois
                date_obj = datetime(year, month, day)
                reservations_this_day = [
                    r for r in all_reservations 
                    if r['date'] == date_obj.strftime('%Y-%m-%d')
                ]
                
                week_data.append({
                    'date': day,
                    'day_name': date_obj.strftime('%a')[:3],  # lun, mar, etc.
                    'full_date': date_obj.strftime('%Y-%m-%d'),
                    'num_reservations': len(reservations_this_day),
                    'has_reservations': len(reservations_this_day) > 0,
                    'is_today': date_obj.date() == datetime.now().date(),
                    'is_selected': False,  # Sera mis à jour JS
                    'reservations': reservations_this_day,
                })
        weeks.append(week_data)
    
    return {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month].upper(),
        'weeks': weeks,
    }

# ==============================================================================
# DONNÉES TIMELINE JOURNALIÈRE
# ==============================================================================

def get_timeline_day(date, salle_code=None):
    """
    Récupérer réservations d'une journée heure par heure
    
    Args:
        date: datetime object
        salle_code: Filter by salle (optional)
    
    Returns:
        {
            'date': '2026-06-17',
            'day_name': 'MARDI 17 JUIN 2026',
            'reservations': [...],
            'timeline': [
                {'heure': '07:00', 'statut': 'LIBRE', 'block_height': 60},
                {'heure': '08:00', 'boites': [...]},  # Réservations
                ...
            ]
        }
    """
    
    date_str = date.strftime('%Y-%m-%d')
    
    # Récupérer toutes réservations du jour
    reservations = get_day_reservations(date_str, salle_code)
    
    # Construire timeline heure par heure (07:00-19:00)
    timeline = []
    start_hour = 7
    end_hour = 19
    
    for hour in range(start_hour, end_hour):
        hour_str = f"{hour:02d}:00"
        
        # Réservations commençant à cette heure
        boites_this_hour = get_reservations_at_hour(reservations, hour)
        
        # Vérifier créneau libre
        is_free = len(boites_this_hour) == 0
        
        timeline.append({
            'heure': hour_str,
            'is_free': is_free,
            'boites': boites_this_hour,  # Réservations
            'block_height': 60,  # Hauteur (px) pour 1 heure
        })
    
    return {
        'date': date_str,
        'day_name': date.strftime('%A %d %B %Y').upper(),
        'weekday': date.strftime('%A'),
        'reservations': reservations,
        'num_reservations': len(reservations),
        'timeline': timeline,
    }

def get_reservations_at_hour(reservations, hour):
    """
    Récupérer réservations commençant à une heure donnée
    
    Returns:
        [
            {
                'id': 'RES001',
                'salle_code': 'SALLE 101',
                'salle_nom': 'Amphithéâtre A',
                'salle_type': 'amphi',
                'formation': 'Licence Médecine',
                'heure_debut': '08:00',
                'heure_fin': '11:00',
                'duration_hours': 3,
                'block_height': 180,  # 3 * 60px
                'statut': 'CONFIRMÉE',
                'statut_color': '#2ecc71',
                'formateur': 'Dr. Martin',
                'participants': '40/40',
                'is_recurring': False,
                'color': '#3498db',
            }
        ]
    """
    
    boites = []
    
    for res in reservations:
        heure_debut = int(res['heure_debut'].split(':')[0])
        
        if heure_debut == hour:
            # Durée en heures
            heure_fin = int(res['heure_fin'].split(':')[0])
            duration = heure_fin - heure_debut
            if duration <= 0:
                duration = 1
            
            # Couleur selon statut
            statut_colors = {
                'CONFIRMÉE': '#2ecc71',    # Vert
                'ATTENTE': '#f39c12',      # Orange
                'ANNULÉE': '#e74c3c',      # Rouge
                'REPORTÉE': '#f1c40f',     # Jaune
            }
            
            # Couleur salle
            salle_colors = {
                'amphi': '#3498db',        # Bleu
                'labo': '#9b59b6',         # Violet
                'reunion': '#e67e22',      # Orange foncé
                'cours': '#1abc9c',        # Teal
            }
            
            boites.append({
                'id': res['id'],
                'salle_code': res['salle_code'],
                'salle_nom': res['salle_nom'],
                'salle_type': res['salle_type'],
                'formation': res['formation'],
                'heure_debut': res['heure_debut'],
                'heure_fin': res['heure_fin'],
                'duration_hours': duration,
                'block_height': duration * 60,  # Hauteur px
                'statut': res['statut'],
                'statut_color': statut_colors.get(res['statut'], '#95a5a6'),
                'formateur': res.get('formateur', ''),
                'participants': res.get('participants', ''),
                'is_recurring': res.get('is_recurring', False),
                'repeat_color': res.get('repeat_color', salle_colors.get(res['salle_type'], '#bdc3c7')),
                'color': salle_colors.get(res['salle_type'], '#bdc3c7'),
            })
    
    return boites

# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@calendar_bp.route('/api/reservations/<date>')
def api_reservations(date):
    """API: Récupérer réservations d'un jour"""
    
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except:
        return jsonify({'error': 'Invalid date format'}), 400
    
    salle_code = request.args.get('salle')
    timeline_data = get_timeline_day(date_obj, salle_code)
    
    return jsonify(timeline_data)

@calendar_bp.route('/api/reservation/<res_id>')
def api_reservation_detail(res_id):
    """API: Récupérer détails réservation"""
    
    res = get_reservation_by_id(res_id)
    
    if not res:
        return jsonify({'error': 'Reservation not found'}), 404
    
    return jsonify(res)

@calendar_bp.route('/api/salle/<salle_code>')
def api_salle_detail(salle_code):
    """API: Récupérer détails salle"""
    
    salle = get_salle_by_code(salle_code)
    
    if not salle:
        return jsonify({'error': 'Salle not found'}), 404
    
    # Ajouter réservations du jour pour cette salle
    today = datetime.now().strftime('%Y-%m-%d')
    salle['reservations_today'] = get_day_reservations(today, salle_code)
    
    return jsonify(salle)

@calendar_bp.route('/api/salle-view/<salle_code>')
def api_salle_view(salle_code):
    """API: Vue Salle (toutes les réservations salle, tous les jours)"""
    
    salle = get_salle_by_code(salle_code)
    
    if not salle:
        return jsonify({'error': 'Salle not found'}), 404
    
    # Récupérer réservations salle pour 3 mois
    start_date = datetime.now()
    end_date = start_date + timedelta(days=90)
    
    reservations = get_salle_reservations_range(salle_code, start_date, end_date)
    
    return jsonify({
        'salle': salle,
        'reservations': reservations,
        'period': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
        }
    })

# ==============================================================================
# FONCTIONS UTILITAIRES (À remplacer par Excel/DB)
# ==============================================================================

def get_day_reservations(date_str, salle_code=None):
    """Récupérer réservations d'un jour (depuis Excel)"""
    # TODO: Charger depuis RESERVATIONS.xlsx
    return [
        {
            'id': 'RES001',
            'date': date_str,
            'salle_code': 'SALLE 101',
            'salle_nom': 'Amphithéâtre A',
            'salle_type': 'amphi',
            'formation': 'Licence Médecine',
            'heure_debut': '08:00',
            'heure_fin': '11:00',
            'statut': 'CONFIRMÉE',
            'formateur': 'Dr. Martin Dupont',
            'participants': '40/40',
            'is_recurring': False,
        },
    ]

def get_all_reservations(year, month):
    """Récupérer toutes réservations du mois"""
    # TODO: Charger depuis Excel
    return []

def get_reservation_by_id(res_id):
    """Récupérer détails réservation par ID"""
    # TODO: Charger depuis Excel
    return None

def get_salle_by_code(salle_code):
    """Récupérer détails salle par code"""
    # TODO: Charger depuis Excel
    return {
        'code': salle_code,
        'nom': 'Amphithéâtre A',
        'type': 'amphi',
        'capacite': 40,
        'localisation': 'Bâtiment A, 1er étage',
        'equipements': ['Vidéoproj', 'Audio', 'Tableau blanc'],
        'responsable': 'Mme Aïchatou Hassan',
        'statut_actuel': 'DISPONIBLE',
    }

def get_all_salles():
    """Récupérer liste toutes salles"""
    # TODO: Charger depuis Excel
    return [
        {'code': 'SALLE 101', 'nom': 'Amphithéâtre A'},
        {'code': 'SALLE 102', 'nom': 'Salle Cours B'},
        {'code': 'LABO 201', 'nom': 'Laboratoire 201'},
    ]

def get_all_formations():
    """Récupérer liste toutes formations"""
    # TODO: Charger depuis Excel
    return [
        {'code': 'MED001', 'titre': 'Licence Médecine'},
        {'code': 'INF001', 'titre': 'Formation Infirmière'},
    ]

def get_salle_reservations_range(salle_code, start_date, end_date):
    """Récupérer réservations salle sur période"""
    # TODO: Charger depuis Excel
    return []

