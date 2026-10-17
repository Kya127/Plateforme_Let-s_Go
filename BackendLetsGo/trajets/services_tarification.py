import unicodedata
from decimal import Decimal

# ==============================================================================
# RÉFÉRENTIEL OFFICIEL DES ZONES TARIFAIRES ET ADRESSES (LET'S GO SÉNÉGAL)
# ==============================================================================

REFERENTIEL_ZONES = [
    {
        "code": "ZONE_A",
        "nom": "Zone A : Dakar Centre",
        "description": "Dakar Centre, Affaires & Universités",
        "quartiers": [
            "Plateau",
            "Médina",
            "Gueule Tapée",
            "Fass",
            "Colobane",
            "Fann Résidence",
            "Point E",
            "Mermoz",
            "Sacré-Cœur 1",
            "Sacré-Cœur 2",
            "Sacré-Cœur 3",
            "Pyrotechnie",
            "Amitié 1",
            "Amitié 2",
            "Amitié 3",
            "Gibraltar",
        ],
        "reperes": [
            "Sandaga",
            "Petersen",
            "Gare TER Dakar",
            "Place de l'Indépendance",
            "Port Autonome / Embarcadère Gorée",
            "Campus UCAD",
            "ESP",
            "Hôpital Fann",
            "Hôpital Principal",
            "Hôpital Le Dantec",
            "Place de l'Obélisque (Place de la Nation)",
            "Rond-point OMVS",
            "Stèle Mermoz",
        ],
    },
    {
        "code": "ZONE_B",
        "nom": "Zone B : Dakar Nord / Ouest",
        "description": "Dakar Nord / Ouest & Façade Maritime",
        "quartiers": [
            "Almadies",
            "Ngor",
            "Ouakam",
            "Mamelles",
            "Yoff",
            "Cité Avion",
            "Cité Comico Ouakam",
            "Touba Ouakam",
            "Yoff Tonghor",
            "Yoff Layène",
            "Cité BCEAO",
            "Cité Biagui",
            "Diamalaye",
            "Virage",
        ],
        "reperes": [
            "Monument de la Renaissance Africaine",
            "Phare des Mamelles",
            "Ancien Aéroport Léopold Sédar Senghor (LSS)",
            "Rond-point Ngor",
            "Brioche Dorée Ouakam",
            "Plage des Almadies",
            "Plage de Yoff",
        ],
    },
    {
        "code": "ZONE_C",
        "nom": "Zone C : Banlieue Proche",
        "description": "Banlieue Proche & Bassins Démographiques",
        "quartiers": [
            "Parcelles Assainies (Unités 1 à 26)",
            "Grand Yoff",
            "Khar Yalla",
            "Arafat",
            "Cité Millionnaire",
            "Taïba",
            "Scat Urbam",
            "Nord Foire",
            "Ouest Foire",
            "Guédiawaye (Ndiarème, Sam Notaire)",
            "Wakhinane Nimzatt",
            "Golf Sud",
            "Hamo (1 à 6)",
            "Cité Fadia",
            "Cité Gadaye",
            "Pikine (Nord, Ouest / Icotaf, Est)",
            "Guinaw Rails",
            "Tally Boumack",
            "Thiaroye (Gare, Mer)",
        ],
        "reperes": [
            "Rond-point Case Bi",
            "Rond-point 26 Parcelles",
            "Échangeur Patte d'Oie (Aliou Sow)",
            "Stade Léopold Sédar Senghor",
            "Arène Nationale",
            "Hôpital Dalal Jamm",
            "Gare TER Pikine",
            "Bountou Pikine",
        ],
    },
    {
        "code": "ZONE_D",
        "nom": "Zone D : Grande Banlieue",
        "description": "Grande Banlieue, Pôle Urbain & Plateforme Économique",
        "quartiers": [
            "Rufisque (Centre, Dangou, Thiawlène)",
            "Santhiaba",
            "Cité Tacko",
            "Arafat Rufisque",
            "Bargny (Minam, Sendou)",
            "Sébikotane",
            "Diamniadio",
            "Keur Massar (Rond-point, Cité Ainmady)",
            "Jaxaay (1 et 2)",
            "Parcelles Keur Massar",
            "Yène",
            "Dougar",
        ],
        "reperes": [
            "Pôle Urbain Diamniadio",
            "Cité Ministérielle",
            "CICAD",
            "Dakar Arena",
            "Stade Abdoulaye Wade",
            "Gares TER (Rufisque, Bargny, Diamniadio)",
            "Sortie Péage Keur Massar (Sortie 8)",
            "Sortie Péage Rufisque (Sortie 9)",
            "Sortie Péage Diamniadio (Sortie 10)",
        ],
    },
    {
        "code": "ZONE_E",
        "nom": "Zone E : Petite Côte",
        "description": "Petite Côte & Pôle Balnéaire",
        "quartiers": [
            "Saly Portudal",
            "Saly Carrefour",
            "Saly Niakhniakhal",
            "Saly Joseph",
            "Saly Golf",
            "Saly Bambara",
            "Mbour (Centre, Tefess, Oncad)",
            "Grand Mbour",
            "Santessou",
            "Liberté Mbour",
            "Somone",
            "Ngaparou",
            "Popenguine",
            "Pointe Sarène",
            "Diass",
            "Sindia",
        ],
        "reperes": [
            "Aéroport International Blaise Diagne (AIBD)",
            "Rond-point Saly Carrefour",
            "Croisement Saly / Route Ngaparou",
            "Garage de Mbour",
            "Marché Central Mbour",
            "Quai de pêche Tefess",
            "Échangeur Péage AIBD / Malicounda / Mbour",
        ],
    },
]

# ==============================================================================
# MATRICE TARIFAIRE OFFICIELLE SYMÉTRIQUE (EN FCFA PAR PASSAGER)
# ==============================================================================

MATRICE_TARIFS_FCFA = {
    ("ZONE_A", "ZONE_A"): Decimal("500"),
    ("ZONE_A", "ZONE_B"): Decimal("800"),
    ("ZONE_A", "ZONE_C"): Decimal("1000"),
    ("ZONE_A", "ZONE_D"): Decimal("1500"),
    ("ZONE_A", "ZONE_E"): Decimal("3500"),

    ("ZONE_B", "ZONE_A"): Decimal("800"),
    ("ZONE_B", "ZONE_B"): Decimal("500"),
    ("ZONE_B", "ZONE_C"): Decimal("800"),
    ("ZONE_B", "ZONE_D"): Decimal("1800"),
    ("ZONE_B", "ZONE_E"): Decimal("4000"),

    ("ZONE_C", "ZONE_A"): Decimal("1000"),
    ("ZONE_C", "ZONE_B"): Decimal("800"),
    ("ZONE_C", "ZONE_C"): Decimal("500"),
    ("ZONE_C", "ZONE_D"): Decimal("1200"),
    ("ZONE_C", "ZONE_E"): Decimal("3500"),

    ("ZONE_D", "ZONE_A"): Decimal("1500"),
    ("ZONE_D", "ZONE_B"): Decimal("1800"),
    ("ZONE_D", "ZONE_C"): Decimal("1200"),
    ("ZONE_D", "ZONE_D"): Decimal("600"),
    ("ZONE_D", "ZONE_E"): Decimal("2500"),

    ("ZONE_E", "ZONE_A"): Decimal("3500"),
    ("ZONE_E", "ZONE_B"): Decimal("4000"),
    ("ZONE_E", "ZONE_C"): Decimal("3500"),
    ("ZONE_E", "ZONE_D"): Decimal("2500"),
    ("ZONE_E", "ZONE_E"): Decimal("800"),
}


def normaliser_chaine(texte: str) -> str:
    """Supprime les accents, la ponctuation superflue et passe en minuscules."""
    if not texte:
        return ""
    texte = unicodedata.normalize('NFKD', str(texte)).encode('ASCII', 'ignore').decode('utf-8')
    return texte.strip().lower()


def trouver_zone_pour_lieu(nom_lieu: str) -> str:
    """
    Identifie le code de zone (ZONE_A, ZONE_B, etc.) correspondant à un lieu ou repère.
    Effectue une correspondance exacte ou par inclusion souple.
    """
    if not nom_lieu:
        return ""

    nom_norm = normaliser_chaine(nom_lieu)

    # 1. Correspondance exacte ou partielle avec le référentiel statique
    for zone in REFERENTIEL_ZONES:
        tous_les_lieux = zone["quartiers"] + zone["reperes"]
        for lieu in tous_les_lieux:
            lieu_norm = normaliser_chaine(lieu)
            if nom_norm == lieu_norm or lieu_norm in nom_norm or nom_norm in lieu_norm:
                return zone["code"]

    # 2. Vérification base de données si LieuZone existe
    try:
        from .models import LieuZone
        lieu_obj = LieuZone.objects.filter(nom__iexact=nom_lieu.strip()).select_related('zone').first()
        if lieu_obj and lieu_obj.zone:
            return lieu_obj.zone.code
    except Exception:
        pass

    return ""


def resoudre_prix_trajet(lieu_depart: str, destination: str):
    """
    Calcule et retourne le prix par place fixé par la plateforme (en FCFA).
    Retourne Decimal(prix) ou None si les zones ne peuvent être déterminées.
    """
    zone_dep = trouver_zone_pour_lieu(lieu_depart)
    zone_dest = trouver_zone_pour_lieu(destination)

    if not zone_dep or not zone_dest:
        return None

    # Recherche directe dans la matrice
    cle = (zone_dep, zone_dest)
    if cle in MATRICE_TARIFS_FCFA:
        return MATRICE_TARIFS_FCFA[cle]

    # Inversion symétrique de sécurité
    cle_inverse = (zone_dest, zone_dep)
    if cle_inverse in MATRICE_TARIFS_FCFA:
        return MATRICE_TARIFS_FCFA[cle_inverse]

    return None


def obtenir_referentiel_complet():
    """
    Retourne la structure complète pour le frontend et les sélecteurs groupés par zone.
    """
    zones_payload = []
    for z in REFERENTIEL_ZONES:
        # Fusionner quartiers et repères pour constituer les options
        options = []
        for q in z["quartiers"]:
            options.append({"valeur": q, "label": q, "type": "QUARTIER"})
        for r in z["reperes"]:
            options.append({"valeur": r, "label": f"{r} (Repère)", "type": "REPERE"})

        zones_payload.append({
            "code": z["code"],
            "nom": z["nom"],
            "description": z["description"],
            "options": options,
        })

    # Convertir la matrice pour transport JSON
    matrice_json = {}
    for (zd, za), prix in MATRICE_TARIFS_FCFA.items():
        if zd not in matrice_json:
            matrice_json[zd] = {}
        matrice_json[zd][za] = int(prix)

    return {
        "zones": zones_payload,
        "matrice": matrice_json,
    }
