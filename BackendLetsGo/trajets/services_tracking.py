import math
from datetime import datetime, timedelta
from django.utils import timezone
from .services_tarification import trouver_zone_pour_lieu

# ==============================================================================
# RÉFÉRENTIEL GÉOGRAPHIQUE : COORDONNÉES GPS DE DAKAR & PETITE CÔTE
# ==============================================================================

COORDONNEES_ZONES_CENTRALES = {
    'ZONE_A': {'lat': 14.6780, 'lng': -17.4420},  # Dakar Centre / Plateau / Fann
    'ZONE_B': {'lat': 14.7350, 'lng': -17.4950},  # Almadies / Ouakam / Yoff
    'ZONE_C': {'lat': 14.7550, 'lng': -17.4200},  # Parcelles / Pikine / Guédiawaye
    'ZONE_D': {'lat': 14.7200, 'lng': -17.2400},  # Rufisque / Keur Massar / Diamniadio
    'ZONE_E': {'lat': 14.4400, 'lng': -16.9800},  # Saly / Mbour / AIBD
}

COORDONNEES_POINTS_DAKAR = {
    # Zone A
    'plateau': {'lat': 14.6677, 'lng': -17.4337},
    'médina': {'lat': 14.6853, 'lng': -17.4502},
    'medina': {'lat': 14.6853, 'lng': -17.4502},
    'gueule tapée': {'lat': 14.6890, 'lng': -17.4590},
    'fass': {'lat': 14.6930, 'lng': -17.4530},
    'colobane': {'lat': 14.6990, 'lng': -17.4450},
    'fann résidence': {'lat': 14.6910, 'lng': -17.4680},
    'point e': {'lat': 14.6980, 'lng': -17.4620},
    'mermoz': {'lat': 14.7083, 'lng': -17.4722},
    'sacré-cœur 1': {'lat': 14.7140, 'lng': -17.4650},
    'sacré-cœur 2': {'lat': 14.7170, 'lng': -17.4670},
    'sacré-cœur 3': {'lat': 14.7210, 'lng': -17.4690},
    'amitié 1': {'lat': 14.7050, 'lng': -17.4580},
    'amitié 2': {'lat': 14.7090, 'lng': -17.4590},
    'amitié 3': {'lat': 14.7120, 'lng': -17.4610},
    'sandaga': {'lat': 14.6710, 'lng': -17.4390},
    'petersen': {'lat': 14.6790, 'lng': -17.4370},
    'gare ter dakar': {'lat': 14.6730, 'lng': -17.4320},
    "place de l'indépendance": {'lat': 14.6700, 'lng': -17.4340},
    'campus ucad': {'lat': 14.6890, 'lng': -17.4650},
    'esp': {'lat': 14.6920, 'lng': -17.4670},
    'hôpital fann': {'lat': 14.6950, 'lng': -17.4680},
    'hôpital principal': {'lat': 14.6640, 'lng': -17.4320},

    # Zone B
    'almadies': {'lat': 14.7456, 'lng': -17.5186},
    'ngor': {'lat': 14.7550, 'lng': -17.5140},
    'ouakam': {'lat': 14.7228, 'lng': -17.4894},
    'mamelles': {'lat': 14.7260, 'lng': -17.4980},
    'yoff': {'lat': 14.7597, 'lng': -17.4667},
    'cité bceao': {'lat': 14.7520, 'lng': -17.4610},
    'virage': {'lat': 14.7520, 'lng': -17.4980},
    'monument de la renaissance africaine': {'lat': 14.7220, 'lng': -17.4950},
    'phare des mamelles': {'lat': 14.7240, 'lng': -17.5000},
    'ancien aéroport léopold sédar senghor (lss)': {'lat': 14.7400, 'lng': -17.4900},

    # Zone C
    'parcelles assainies': {'lat': 14.7550, 'lng': -17.4350},
    'grand yoff': {'lat': 14.7300, 'lng': -17.4500},
    'khar yalla': {'lat': 14.7210, 'lng': -17.4480},
    'scat urbam': {'lat': 14.7260, 'lng': -17.4590},
    'nord foire': {'lat': 14.7410, 'lng': -17.4650},
    'ouest foire': {'lat': 14.7360, 'lng': -17.4720},
    'guédiawaye': {'lat': 14.7700, 'lng': -17.3900},
    'pikine': {'lat': 14.7500, 'lng': -17.3950},
    'thiaroye': {'lat': 14.7640, 'lng': -17.3710},
    'échangeur patte d\'oie (aliou sow)': {'lat': 14.7290, 'lng': -17.4410},
    'stade léopold sédar senghor': {'lat': 14.7450, 'lng': -17.4480},
    'arène nationale': {'lat': 14.7520, 'lng': -17.3980},
    'hôpital dalal jamm': {'lat': 14.7780, 'lng': -17.3880},
    'gare ter pikine': {'lat': 14.7520, 'lng': -17.3930},
    'bountou pikine': {'lat': 14.7460, 'lng': -17.4080},

    # Zone D
    'rufisque': {'lat': 14.7167, 'lng': -17.2667},
    'bargny': {'lat': 14.6970, 'lng': -17.2300},
    'sébikotane': {'lat': 14.7420, 'lng': -17.1350},
    'diamniadio': {'lat': 14.7200, 'lng': -17.1800},
    'keur massar': {'lat': 14.7800, 'lng': -17.3100},
    'jaxaay': {'lat': 14.7710, 'lng': -17.2880},
    'dougar': {'lat': 14.7310, 'lng': -17.1120},
    'pôle urbain diamniadio': {'lat': 14.7220, 'lng': -17.1820},
    'cicad': {'lat': 14.7180, 'lng': -17.1750},
    'dakar arena': {'lat': 14.7190, 'lng': -17.1780},
    'stade abdoulaye wade': {'lat': 14.7240, 'lng': -17.1700},

    # Zone E
    'saly portudal': {'lat': 14.4400, 'lng': -16.9900},
    'saly carrefour': {'lat': 14.4480, 'lng': -16.9850},
    'mbour': {'lat': 14.4200, 'lng': -16.9700},
    'somone': {'lat': 14.4850, 'lng': -17.0600},
    'ngaparou': {'lat': 14.4680, 'lng': -17.0350},
    'popenguine': {'lat': 14.5500, 'lng': -17.1100},
    'diass': {'lat': 14.6100, 'lng': -17.0800},
    'sindia': {'lat': 14.5600, 'lng': -17.0200},
    'aéroport international blaise diagne (aibd)': {'lat': 14.6700, 'lng': -17.0700},
}


def obtenir_coordonnees_lieu(nom_lieu):
    """
    Résout les coordonnées géographiques (lat, lng) d'un lieu à Dakar ou Petite Côte.
    Effectue une recherche directe, partielle ou par rattachement de zone tarifaire.
    """
    if not nom_lieu:
        return COORDONNEES_ZONES_CENTRALES['ZONE_A']

    cle = nom_lieu.strip().lower()

    # 1. Correspondance exacte
    if cle in COORDONNEES_POINTS_DAKAR:
        return COORDONNEES_POINTS_DAKAR[cle]

    # 2. Correspondance partielle
    for point, coords in COORDONNEES_POINTS_DAKAR.items():
        if point in cle or cle in point:
            return coords

    # 3. Secours via la zone tarifaire associée
    code_zone = trouver_zone_pour_lieu(nom_lieu)
    if code_zone and code_zone in COORDONNEES_ZONES_CENTRALES:
        return COORDONNEES_ZONES_CENTRALES[code_zone]

    # 4. Fallback par défaut (Dakar Centre)
    return COORDONNEES_ZONES_CENTRALES['ZONE_A']


def calculer_distance_haversine(lat1, lon1, lat2, lon2):
    """
    Calcule la distance géodésique en kilomètres entre deux points GPS (formule de Haversine).
    """
    r = 6371.0  # Rayon moyen de la Terre en kilomètres
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def calculer_eta_trajet(trajet):
    """
    Calcule en temps réel la télémétrie du trajet :
    - Position actuelle du véhicule (ou position de départ si non encore démarré)
    - Distance restante en km
    - Temps restant en minutes
    - Heure d'arrivée estimée (HH:MM)
    - Statut et badge contextuel
    """
    coords_dep = obtenir_coordonnees_lieu(trajet.lieu_depart)
    coords_dest = obtenir_coordonnees_lieu(trajet.destination)

    # Coordonnées actuelles du véhicule
    if trajet.latitude_actuelle is not None and trajet.longitude_actuelle is not None:
        vehicule_lat = trajet.latitude_actuelle
        vehicule_lng = trajet.longitude_actuelle
        cap = trajet.cap_actuel or 0.0
        vitesse = trajet.vitesse_actuelle or 0.0
    else:
        # Si le conducteur n'a pas encore émis de position GPS, on part du point de départ
        vehicule_lat = coords_dep['lat']
        vehicule_lng = coords_dep['lng']
        cap = 0.0
        vitesse = 0.0

    # Distance totale du trajet et distance restante jusqu'à la destination
    distance_totale_km = max(0.5, round(calculer_distance_haversine(
        coords_dep['lat'], coords_dep['lng'],
        coords_dest['lat'], coords_dest['lng']
    ), 1))

    distance_restante_km = max(0.2, round(calculer_distance_haversine(
        vehicule_lat, vehicule_lng,
        coords_dest['lat'], coords_dest['lng']
    ), 1))

    # Détermination de la vitesse moyenne estimée en km/h
    # Si le GPS donne une vitesse positive > 15 km/h, on l'utilise
    if vitesse and vitesse > 15:
        vitesse_utilisee = min(110.0, float(vitesse))
    elif distance_restante_km > 25:
        vitesse_utilisee = 65.0  # Trajet interurbain / autoroute (ex: Dakar - Mbour)
    elif distance_restante_km > 12:
        vitesse_utilisee = 40.0  # Banlieue / VDN
    else:
        vitesse_utilisee = 26.0  # Circulation urbaine dense Dakar

    # Temps restant en minutes (arrondi)
    temps_restant_minutes = max(2, round((distance_restante_km / vitesse_utilisee) * 60))

    # Heure estimée d'arrivée
    maintenant = timezone.localtime(timezone.now()) if timezone.is_aware(timezone.now()) else datetime.now()
    heure_arrivee_dt = maintenant + timedelta(minutes=temps_restant_minutes)
    heure_arrivee_estimee = heure_arrivee_dt.strftime('%H:%M')

    # Badge contextuel et état
    est_en_cours = trajet.statut == 'EN_COURS' and bool(trajet.tracking_actif)
    est_termine = trajet.statut == 'TERMINE'

    if est_termine:
        badge_texte = "Trajet terminé"
    elif est_en_cours:
        badge_texte = f"En route • Arrivée dans {temps_restant_minutes} min"
    else:
        if hasattr(trajet.heure_depart, 'strftime'):
            heure_fmt = trajet.heure_depart.strftime('%H:%M')
        elif trajet.heure_depart:
            heure_fmt = str(trajet.heure_depart)[:5]
        else:
            heure_fmt = '08:30'
        badge_texte = f"Trajet planifié • Départ prévu à {heure_fmt}"

    return {
        "trajet_id": trajet.id,
        "statut": trajet.statut,
        "tracking_actif": est_en_cours,
        "vehicule_position": {
            "lat": vehicule_lat,
            "lng": vehicule_lng,
            "cap": cap,
            "vitesse": vitesse,
            "horodatage": trajet.derniere_position_at.isoformat() if trajet.derniere_position_at else None
        },
        "depart": {
            "nom": trajet.lieu_depart,
            "lat": coords_dep['lat'],
            "lng": coords_dep['lng']
        },
        "destination": {
            "nom": trajet.destination,
            "lat": coords_dest['lat'],
            "lng": coords_dest['lng']
        },
        "distance_totale_km": distance_totale_km,
        "distance_restante_km": distance_restante_km,
        "temps_restant_minutes": temps_restant_minutes,
        "heure_arrivee_estimee": heure_arrivee_estimee,
        "badge_texte": badge_texte,
    }
