import unicodedata
import re
import django_filters
from .models import Trajet

DAKAR_SUBURBS = [
    "keur massar",
    "sacre coeur",
    "ouakam",
    "almadies",
    "plateau",
    "parcelles assainies",
    "guediawaye",
    "pikine",
    "rufisque",
    "diamniadio",
    "yoff",
    "medina",
    "fann",
    "point e",
    "mermoz",
    "maristes",
    "colobane",
    "mamelles",
]

def normalize_text(text: str) -> str:
    if not text:
        return ""
    # Remplacement des ligatures françaises (œ -> oe, æ -> ae)
    s = str(text).replace("œ", "oe").replace("Œ", "oe").replace("æ", "ae").replace("Æ", "ae")
    # Décomposition Unicode & suppression des diacritiques (accents)
    nfkd = unicodedata.normalize("NFKD", s)
    s = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()
    # Remplacement des ponctuations et espaces multiples par un espace unique
    return re.sub(r"[\s\-_,;.:/]+", " ", s).strip()


class TrajetFilter(django_filters.FilterSet):
    lieu_depart = django_filters.CharFilter(method="filter_lieu_depart")
    destination = django_filters.CharFilter(method="filter_destination")
    date = django_filters.DateFilter(method="filter_date")
    passagers = django_filters.NumberFilter(field_name="places_disponibles", lookup_expr="gte")
    q = django_filters.CharFilter(method="filter_global")

    class Meta:
        model = Trajet
        fields = ["lieu_depart", "destination", "date", "passagers", "q"]

    def filter_lieu_depart(self, queryset, name, value):
        if not value or not str(value).strip():
            return queryset

        norm_val = normalize_text(value)
        # Ignorer le suffixe "senegal" s'il est présent (ex: "Dakar, Sénégal")
        norm_val = re.sub(r"\bsenegal\b", "", norm_val).strip()

        tokens = [t for t in norm_val.split(" ") if len(t) >= 2]
        if not tokens:
            tokens = [norm_val]

        matching_ids = []
        for trajet in queryset:
            norm_field = normalize_text(trajet.lieu_depart)

            # Correspondance de tous les jetons du lieu
            if all(token in norm_field for token in tokens):
                matching_ids.append(trajet.id)
            # Si recherche "dakar", correspond aussi aux communes de Dakar
            elif norm_val == "dakar" and any(sub in norm_field for sub in DAKAR_SUBURBS):
                matching_ids.append(trajet.id)

        return queryset.filter(id__in=matching_ids)

    def filter_destination(self, queryset, name, value):
        if not value or not str(value).strip():
            return queryset

        norm_val = normalize_text(value)
        norm_val = re.sub(r"\bsenegal\b", "", norm_val).strip()

        tokens = [t for t in norm_val.split(" ") if len(t) >= 2]
        if not tokens:
            tokens = [norm_val]

        matching_ids = []
        for trajet in queryset:
            norm_field = normalize_text(trajet.destination)

            # Correspondance de tous les jetons de destination
            if all(token in norm_field for token in tokens):
                matching_ids.append(trajet.id)
            # Si recherche "dakar", correspond aussi aux communes de Dakar
            elif norm_val == "dakar" and any(sub in norm_field for sub in DAKAR_SUBURBS):
                matching_ids.append(trajet.id)

        return queryset.filter(id__in=matching_ids)

    def filter_date(self, queryset, name, value):
        if not value:
            return queryset

        # 1. Chercher d'abord les trajets correspondant exactement à la date demandée
        exact_qs = queryset.filter(date=value)
        if exact_qs.exists():
            return exact_qs

        # 2. Si aucun trajet à la date exacte, proposer les trajets à venir (date >= demandée)
        gte_qs = queryset.filter(date__gte=value)
        if gte_qs.exists():
            return gte_qs

        return queryset.none()

    def filter_global(self, queryset, name, value):
        if not value or not str(value).strip():
            return queryset

        norm_val = normalize_text(value)
        tokens = [t for t in norm_val.split(" ") if len(t) >= 2]
        if not tokens:
            return queryset

        matching_ids = []
        for trajet in queryset:
            combined = normalize_text(f"{trajet.lieu_depart} {trajet.destination} {trajet.description or ''}")
            if all(tk in combined for tk in tokens):
                matching_ids.append(trajet.id)

        return queryset.filter(id__in=matching_ids)