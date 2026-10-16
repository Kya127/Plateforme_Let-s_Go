from collections import Counter
from datetime import date
from django.utils import timezone
from django.db.models import Count, Q
from trajets.models import Trajet
from reservations.models import Reservation
from .models import HistoriqueRecherche


def nettoyer_texte(valeur: str) -> str:
    """Nettoie et normalise une chaîne de caractères pour la comparaison d'axes."""
    if not valeur:
        return ""
    return valeur.strip().lower()


def obtenir_axes_frequents_utilisateur(user, top_n: int = 3):
    """
    Identifie les 1 à 3 axes les plus fréquents (couple départ / destination)
    d'un utilisateur en combinant ses réservations passées et ses recherches.
    Pondération :
      - 1 réservation = 3 points d'intérêt
      - 1 recherche = 1 point d'intérêt
    """
    compteur_axes = Counter()

    # 1. Réservations passées et actives de l'utilisateur
    reservations = (
        Reservation.objects
        .filter(passager=user)
        .exclude(statut=Reservation.StatutReservation.ANNULEE)
        .select_related('trajet')
    )
    for r in reservations:
        if r.trajet:
            dep = nettoyer_texte(r.trajet.lieu_depart)
            dest = nettoyer_texte(r.trajet.destination)
            if dep and dest:
                # Clé stockée : (dep_normalise, dest_normalise, affichage_dep, affichage_dest)
                compteur_axes[(dep, dest)] += 3

    # 2. Recherches récentes de l'utilisateur (30 derniers jours max)
    recherches = (
        HistoriqueRecherche.objects
        .filter(user=user)
        .order_by('-created_at')[:50]
    )
    for rech in recherches:
        dep = nettoyer_texte(rech.lieu_depart)
        dest = nettoyer_texte(rech.destination)
        if dep and dest:
            compteur_axes[(dep, dest)] += 1

    if not compteur_axes:
        return []

    # Retourne les top_n couples (dep, dest) les plus fréquents
    top_axes = [axe for axe, _score in compteur_axes.most_common(top_n)]
    return top_axes


def obtenir_axes_populaires_plateforme(top_n: int = 3):
    """
    Cold Start : Calcule les axes les plus populaires de la plateforme
    (couples départ / arrivée ayant le plus de trajets planifiés actifs ou de demandes récentes).
    """
    today = max(timezone.localdate(), date.today())
    
    # 1. Fréquence sur les trajets planifiés actifs
    trajets_actifs = (
        Trajet.objects
        .filter(
            statut=Trajet.StatutTrajet.PLANIFIE,
            places_disponibles__gt=0,
            date__gte=today
        )
        .values('lieu_depart', 'destination')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )

    compteur = Counter()
    for t in trajets_actifs:
        dep = nettoyer_texte(t['lieu_depart'])
        dest = nettoyer_texte(t['destination'])
        if dep and dest:
            compteur[(dep, dest)] += t['total'] * 2

    # 2. Fréquence sur les réservations récentes
    reservations_recentes = (
        Reservation.objects
        .exclude(statut=Reservation.StatutReservation.ANNULEE)
        .select_related('trajet')
        .order_by('-created_at')[:50]
    )
    for r in reservations_recentes:
        if r.trajet:
            dep = nettoyer_texte(r.trajet.lieu_depart)
            dest = nettoyer_texte(r.trajet.destination)
            if dep and dest:
                compteur[(dep, dest)] += 1

    # Si la base est encore jeune / vide, on fournit des axes majeurs au Sénégal par défaut
    if not compteur:
        return [
            ("dakar", "thiès"),
            ("dakar", "saint-louis"),
            ("dakar", "mbour"),
        ]

    return [axe for axe, _ in compteur.most_common(top_n)]


def construire_filtre_axe(dep: str, dest: str) -> Q:
    """
    Construit une requête Q tolérante pour matcher un axe, 
    gérant les virgules, quartiers et variations (ex: 'Dakar, Sacré-Cœur' ou 'Sacré-Cœur').
    """
    q_dep = Q(lieu_depart__iexact=dep) | Q(lieu_depart__icontains=dep)
    for p in dep.split(','):
        p_clean = p.strip()
        if len(p_clean) >= 3:
            q_dep |= Q(lieu_depart__icontains=p_clean)

    q_dest = Q(destination__iexact=dest) | Q(destination__icontains=dest)
    for p in dest.split(','):
        p_clean = p.strip()
        if len(p_clean) >= 3:
            q_dest |= Q(destination__icontains=p_clean)

    return q_dep & q_dest


def get_suggestions_trajets(user=None, limit: int = 6):
    """
    Moteur principal de suggestion de trajets :
    - Cas 1 : Utilisateur connecté avec historique -> Ses 1 à 3 axes favoris
    - Cas 2 : Cold start (anonyme ou sans historique) -> Axes les plus populaires
    
    Retourne un dictionnaire :
    {
        "type_suggestion": "HABITUDES" | "POPULAIRES",
        "tag": "Basé sur vos habitudes" | "Trajets populaires du moment",
        "axes": list of tuples,
        "trajets": QuerySet de trajets actifs correspondants
    }
    """
    today = max(timezone.localdate(), date.today())

    base_queryset = (
        Trajet.objects
        .filter(
            statut=Trajet.StatutTrajet.PLANIFIE,
            places_disponibles__gt=0,
            date__gte=today
        )
        .select_related('conducteur', 'voiture')
        .order_by('date', 'heure_depart')
    )

    # Exclusions spécifiques à l'utilisateur connecté
    if user and user.is_authenticated:
        # Exclure les trajets où l'utilisateur est le conducteur
        base_queryset = base_queryset.exclude(conducteur=user)
        # Exclure les trajets que l'utilisateur a déjà réservés
        base_queryset = base_queryset.exclude(
            reservations__passager=user,
            reservations__statut=Reservation.StatutReservation.CONFIRMEE
        )

    # =========================================================================
    # CAS 1 : Passager régulier (historique existant)
    # =========================================================================
    if user and user.is_authenticated:
        axes_utilisateur = obtenir_axes_frequents_utilisateur(user, top_n=3)

        if axes_utilisateur:
            # Construire une requête Q dynamique pour matcher l'un des 1 à 3 axes
            filtre_axes = Q()
            for dep, dest in axes_utilisateur:
                filtre_axes |= construire_filtre_axe(dep, dest)

            trajets_habitudes = base_queryset.filter(filtre_axes).distinct()[:limit]

            # Si on a trouvé des trajets actifs pour ses habitudes
            if trajets_habitudes.exists():
                return {
                    "type_suggestion": "HABITUDES",
                    "tag": "Basé sur vos habitudes",
                    "description": "Trajets disponibles sur vos trajets les plus fréquents",
                    "axes": axes_utilisateur,
                    "trajets": trajets_habitudes
                }

    # =========================================================================
    # CAS 2 : Cold Start (anonyme, nouvel utilisateur ou aucun trajet sur ses habitudes)
    # =========================================================================
    axes_populaires = obtenir_axes_populaires_plateforme(top_n=3)
    filtre_populaires = Q()
    for dep, dest in axes_populaires:
        filtre_populaires |= construire_filtre_axe(dep, dest)

    trajets_populaires = base_queryset.filter(filtre_populaires).distinct()[:limit]

    # Si le filtre spécifique ne retourne rien (peu de trajets en base), on renvoie les prochains trajets actifs
    if not trajets_populaires.exists():
        trajets_populaires = base_queryset[:limit]

    return {
        "type_suggestion": "POPULAIRES",
        "tag": "Trajets populaires du moment",
        "description": "Les lignes les plus demandées sur Let's Go",
        "axes": axes_populaires,
        "trajets": trajets_populaires
    }
