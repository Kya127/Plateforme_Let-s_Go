import unicodedata
from collections import Counter
from datetime import date
from django.utils import timezone
from django.db.models import Count, Q
from trajets.models import Trajet, ZoneTarifaire, LieuZone
from reservations.models import Reservation
from .models import HistoriqueRecherche


def normaliser_chaine(valeur: str) -> str:
    """Normalise une chaîne : minuscules, suppression des accents, tirets et ligatures (œ, æ)."""
    if not valeur:
        return ""
    texte = str(valeur).strip().lower()
    texte = texte.replace('œ', 'oe').replace('æ', 'ae').replace('-', ' ')
    nfkd = unicodedata.normalize('NFKD', texte)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def identifier_zone_lieu(nom_lieu: str):
    """
    Associe un nom de lieu à sa ZoneTarifaire s'il existe dans LieuZone ou par mot-clé géographique.
    """
    if not nom_lieu:
        return None
    nom_norm = normaliser_chaine(nom_lieu)

    # 1. Correspondance EXACTE avec la table LieuZone
    try:
        for lieu in LieuZone.objects.select_related('zone').all():
            l_norm = normaliser_chaine(lieu.nom)
            if l_norm == nom_norm:
                return lieu.zone.code
    except Exception:
        pass

    # 2. Heuristiques sur les communes / quartiers sénégalais (mots composés testés en premier)
    BANLIEUE_PROCHE = [
        'grand yoff', 'patte d oie', 'parcelles assainies', 'parcelles', 'pikine',
        'guediawaye', 'thiaroye', 'fadia', 'golf', 'yeumbeul', 'malika', 'camberene', 'dalifort'
    ]
    GRANDE_BANLIEUE = [
        'keur massar', 'keur mbaye fall', 'tivaouane peulh', 'zac mbao', 'mbao',
        'rufisque', 'diamniadio', 'bargny', 'jaxaay', 'sebikotane', 'yene', 'dougar', 'sangalkam'
    ]
    DAKAR_CENTRE = [
        'sacre coeur', 'point e', 'gueule tapee', 'zone b', 'zone a', 'plateau',
        'medina', 'fann', 'mermoz', 'colobane', 'fass', 'sandaga', 'amitie', 'hlm',
        'dieuppeul', 'derkle', 'liberte', 'castors', 'maristes'
    ]
    DAKAR_NORD = [
        'nord foire', 'ouest foire', 'almadies', 'ngor', 'ouakam', 'yoff', 'mamelles', 'virage'
    ]
    PETITE_COTE = [
        'mbour', 'saly', 'somone', 'ngaparou', 'aibd', 'popenguine', 'diass', 'sindia'
    ]

    for b in BANLIEUE_PROCHE:
        if b in nom_norm:
            return 'ZONE_C'
    for g in GRANDE_BANLIEUE:
        if g in nom_norm:
            return 'ZONE_D'
    for c in DAKAR_CENTRE:
        if c in nom_norm:
            return 'ZONE_A'
    for n in DAKAR_NORD:
        if n in nom_norm:
            return 'ZONE_B'
    for p in PETITE_COTE:
        if p in nom_norm:
            return 'ZONE_E'

    # 3. Correspondance par sous-chaîne dans la table LieuZone
    try:
        for lieu in LieuZone.objects.select_related('zone').all():
            l_norm = normaliser_chaine(lieu.nom)
            if l_norm in nom_norm:
                return lieu.zone.code
    except Exception:
        pass

    return None


def decouper_mots_clefs(chaine: str):
    """Extrait des mots-clés significatifs (longueur >= 2, sans mots vides génériques)."""
    if not chaine:
        return []
    norm = normaliser_chaine(chaine)
    for ch in [',', ';', '.', ':', '/', '-', '_', "'", '(', ')']:
        norm = norm.replace(ch, ' ')
    parties = norm.split()
    mots_vides = {'dakar', 'sn', 'senegal', 'rue', 'route', 'vers', 'point', 'arret', 'rond', 'de', 'du', 'la', 'le', 'les', 'des', 'en', 'a'}
    return [p for p in parties if len(p) >= 2 and p not in mots_vides]


def lieux_sont_proches_ou_similaires(lieu1: str, lieu2: str) -> bool:
    """
    Détermine si deux lieux correspondent au même pôle géographique ou adresse :
    - Égalité normalisée
    - Inclusion directe (ex: 'plateau' dans 'dakar plateau')
    - Partage d'un mot-clé distinctif (ex: 'sacre coeur' et 'sacre coeur 3', 'keur massar' et 'massar')
    """
    if not lieu1 or not lieu2:
        return False
    l1_norm = normaliser_chaine(lieu1)
    l2_norm = normaliser_chaine(lieu2)

    if l1_norm == l2_norm:
        return True
    if l1_norm in l2_norm or l2_norm in l1_norm:
        return True

    mots1 = decouper_mots_clefs(l1_norm)
    mots2 = decouper_mots_clefs(l2_norm)

    intersection = set(mots1).intersection(set(mots2))
    return bool(intersection)


def extraire_centres_interet_passager(user):
    """
    Extrait l'ensemble des centres d'intérêt réels du passager :
    - Axes directs recherchés / réservés (dep_norm, dest_norm)
    - Pôles de départ d'intérêt (recherches, réservations)
    - Pôles de destination d'intérêt (recherches, réservations)
    - Flux de zones géographiques (ex: Banlieue ZONE_C/D ➔ Ville ZONE_A/B)
    - Adresse de résidence déclarée (pôle de départ potentiel)
    """
    axes_directs = set()
    departs_interet = set()
    destinations_interet = set()
    flux_zones_interet = set()

    # 1. Réservations passées et actives de l'utilisateur
    reservations = (
        Reservation.objects
        .filter(passager=user)
        .exclude(statut=Reservation.StatutReservation.ANNULEE)
        .select_related('trajet', 'trajet__zone_depart', 'trajet__zone_destination')
    )
    for r in reservations:
        if r.trajet:
            dep = normaliser_chaine(r.trajet.lieu_depart)
            dest = normaliser_chaine(r.trajet.destination)
            if dep and dest:
                axes_directs.add((dep, dest))
                departs_interet.add(dep)
                destinations_interet.add(dest)

                z_dep = r.trajet.zone_depart.code if r.trajet.zone_depart else identifier_zone_lieu(dep)
                z_dest = r.trajet.zone_destination.code if r.trajet.zone_destination else identifier_zone_lieu(dest)
                if z_dep and z_dest:
                    flux_zones_interet.add((z_dep, z_dest))

    # 2. Recherches récentes de l'utilisateur (manuelles et vocales)
    recherches = (
        HistoriqueRecherche.objects
        .filter(user=user)
        .order_by('-created_at')[:50]
    )
    for rech in recherches:
        dep = normaliser_chaine(rech.lieu_depart)
        dest = normaliser_chaine(rech.destination)
        if dep and dest:
            axes_directs.add((dep, dest))
            departs_interet.add(dep)
            destinations_interet.add(dest)

            z_dep = identifier_zone_lieu(dep)
            z_dest = identifier_zone_lieu(dest)
            if z_dep and z_dest:
                flux_zones_interet.add((z_dep, z_dest))

    # 3. Adresse de résidence déclarée du passager
    if getattr(user, 'adresse', None) and user.adresse.strip():
        adr_norm = normaliser_chaine(user.adresse)
        if adr_norm:
            departs_interet.add(adr_norm)
            z_adr = identifier_zone_lieu(adr_norm)
            if z_adr:
                for dest_i in destinations_interet:
                    z_dest = identifier_zone_lieu(dest_i)
                    if z_dest:
                        flux_zones_interet.add((z_adr, z_dest))

    # Un passager n'a d'intérêts exploitables que s'il a recherché/réservé un axe
    # ou dispose de départs et de destinations identifiés
    has_interests = bool(axes_directs or (departs_interet and destinations_interet))

    return {
        "axes_directs": axes_directs,
        "departs": departs_interet,
        "destinations": destinations_interet,
        "flux_zones": flux_zones_interet,
        "has_interests": has_interests
    }


def trajet_correspond_aux_interets(trajet, interets):
    """
    Vérifie si un trajet disponible correspond aux centres d'intérêt du passager :
    1. Match exact ou partiel d'un axe direct recherché/réservé (départ ET destination)
    2. Départ dans les départs d'intérêt (ou adresse) ET destination dans les destinations d'intérêt
    3. Trajet correspondant au même flux de zones (ex: corridor Banlieue -> Ville)
       avec ancre géographique sur le lieu de son adresse/départ habituel OU sa destination habituelle.
    """
    dep_t = normaliser_chaine(trajet.lieu_depart)
    dest_t = normaliser_chaine(trajet.destination)

    # 1. Match d'un axe direct recherché ou réservé
    for (dep_i, dest_i) in interets['axes_directs']:
        dep_ok = lieux_sont_proches_ou_similaires(dep_t, dep_i)
        dest_ok = lieux_sont_proches_ou_similaires(dest_t, dest_i)
        if dep_ok and dest_ok:
            return True

    # 2. Match croisé départs / destinations d'intérêt
    match_depart = any(lieux_sont_proches_ou_similaires(dep_t, d) for d in interets['departs'])
    match_dest = any(lieux_sont_proches_ou_similaires(dest_t, d) for d in interets['destinations'])

    if match_depart and match_dest:
        return True

    # 3. Match de flux de zones (ex: corridor Banlieue -> Ville ou Ville -> Banlieue)
    # Règle utilisateur : "Si le passager à l'habitude de faire banlieue/ville,
    # les trajets proche du lieu de son adresse ou encore du lieu de destination habituelle."
    if interets['flux_zones']:
        z_dep = trajet.zone_depart.code if trajet.zone_depart else identifier_zone_lieu(dep_t)
        z_dest = trajet.zone_destination.code if trajet.zone_destination else identifier_zone_lieu(dest_t)

        if z_dep and z_dest:
            ZONES_BANLIEUE = {'ZONE_C', 'ZONE_D'}
            ZONES_VILLE = {'ZONE_A', 'ZONE_B'}

            # Habitude Banlieue -> Ville
            a_habitude_banlieue_ville = any(
                zd in ZONES_BANLIEUE and za in ZONES_VILLE
                for (zd, za) in interets['flux_zones']
            )
            est_flux_banlieue_ville = (z_dep in ZONES_BANLIEUE and z_dest in ZONES_VILLE)

            # Habitude Ville -> Banlieue
            a_habitude_ville_banlieue = any(
                zd in ZONES_VILLE and za in ZONES_BANLIEUE
                for (zd, za) in interets['flux_zones']
            )
            est_flux_ville_banlieue = (z_dep in ZONES_VILLE and z_dest in ZONES_BANLIEUE)

            # Correspondance de corridor (Banlieue <-> Ville ou flux exact)
            corridor_correspond = (
                (a_habitude_banlieue_ville and est_flux_banlieue_ville) or
                (a_habitude_ville_banlieue and est_flux_ville_banlieue) or
                ((z_dep, z_dest) in interets['flux_zones'])
            )

            if corridor_correspond:
                # Le trajet doit obligatoirement avoir une proximité avec l'adresse / départ habituel
                # OU avec la destination habituelle
                if match_depart or match_dest:
                    return True

    return False


def get_suggestions_trajets(user=None, limit: int = 6):
    """
    Moteur de suggestion de trajets STRICTEMENT basé sur l'historique et les centres d'intérêt :
    - Si l'utilisateur n'est pas connecté ou n'a aucun centre d'intérêt : aucune suggestion.
    - Seuls les trajets actifs correspondant à ses recherches, réservations ou son adresse sont retenus.
    - Tout trajet étranger à ses centres d'intérêt est exclu (aucun repli générique).
    """
    # Si non connecté : pas de suggestions personnalisées
    if not user or not user.is_authenticated:
        return {
            "type_suggestion": "HABITUDES",
            "tag": "Vos trajets suggérés",
            "description": "",
            "trajets": Trajet.objects.none()
        }

    interets = extraire_centres_interet_passager(user)

    # Si le passager n'a aucun historique ni centre d'intérêt : pas de suggestions
    if not interets['has_interests']:
        return {
            "type_suggestion": "HABITUDES",
            "tag": "Vos trajets suggérés",
            "description": "",
            "trajets": Trajet.objects.none()
        }

    today = max(timezone.localdate(), date.today())

    base_queryset = (
        Trajet.objects
        .filter(
            statut=Trajet.StatutTrajet.PLANIFIE,
            places_disponibles__gt=0,
            date__gte=today
        )
        .exclude(conducteur=user)
        .exclude(
            reservations__passager=user,
            reservations__statut=Reservation.StatutReservation.CONFIRMEE
        )
        .select_related('conducteur', 'voiture', 'zone_depart', 'zone_destination')
        .order_by('date', 'heure_depart')
    )

    # Filtrer uniquement les trajets qui correspondent aux centres d'intérêt du passager
    trajets_pertinents_ids = []
    for t in base_queryset:
        if trajet_correspond_aux_interets(t, interets):
            trajets_pertinents_ids.append(t.id)
            if len(trajets_pertinents_ids) >= limit:
                break

    if not trajets_pertinents_ids:
        return {
            "type_suggestion": "HABITUDES",
            "tag": "Vos trajets suggérés",
            "description": "",
            "trajets": Trajet.objects.none()
        }

    trajets_suggeres = base_queryset.filter(id__in=trajets_pertinents_ids)

    return {
        "type_suggestion": "HABITUDES",
        "tag": "Basé sur vos habitudes",
        "description": "Trajets disponibles selon vos habitudes et centres d'intérêt",
        "trajets": trajets_suggeres
    }
