from rest_framework import serializers
from trajets.models import Trajet
from .models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    nom_auteur = serializers.SerializerMethodField()
    photo_auteur = serializers.SerializerMethodField()
    trajet_info = serializers.SerializerMethodField()
    nom_destinataire = serializers.ReadOnlyField(source="destinataire.first_name")

    class Meta:
        model = Evaluation
        fields = (
            "id",
            "trajet",
            "trajet_info",
            "destinataire",
            "nom_destinataire",
            "note",
            "commentaire",
            "nom_auteur",
            "photo_auteur",
            "created_at",
        )
        read_only_fields = ("id", "nom_auteur", "photo_auteur", "nom_destinataire", "trajet_info", "created_at")

    def get_nom_auteur(self, obj):
        if obj.auteur:
            full = f"{obj.auteur.first_name} {obj.auteur.last_name}".strip()
            return full or obj.auteur.first_name or "Passager"
        return "Passager"

    def get_photo_auteur(self, obj):
        if obj.auteur and obj.auteur.photo:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.auteur.photo.url)
            return obj.auteur.photo.url
        return None

    def get_trajet_info(self, obj):
        if obj.trajet:
            return {
                "id": obj.trajet.id,
                "depart": obj.trajet.lieu_depart,
                "destination": obj.trajet.destination,
                "date": obj.trajet.date.isoformat() if obj.trajet.date else None,
            }
        return None

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None
        trajet = attrs.get("trajet")
        destinataire = attrs.get("destinataire")

        if not user or not user.is_authenticated:
            raise serializers.ValidationError(
                "Vous devez être connecté pour laisser un avis."
            )

        # Si le destinataire n'est pas spécifié, on prend le conducteur du trajet
        if not destinataire and trajet and trajet.conducteur:
            destinataire = trajet.conducteur
            attrs["destinataire"] = destinataire

        # 1. Interdiction de s'auto-évaluer
        if user == destinataire:
            raise serializers.ValidationError(
                {"destinataire": "Vous ne pouvez pas vous évaluer vous-même."}
            )

        # 2. Le trajet ne doit pas être annulé
        if trajet and trajet.statut == Trajet.StatutTrajet.ANNULE:
            raise serializers.ValidationError(
                {"trajet": "Vous ne pouvez pas évaluer un trajet annulé."}
            )

        # 3. Vérification de la relation avec le trajet
        # L'auteur doit être le conducteur, ou avoir une réservation (ou être un passager évaluant le conducteur)
        is_user_conducteur = trajet.conducteur == user
        is_user_passager = trajet.reservations.filter(passager=user, statut="CONFIRMEE").exists()
        is_dest_conducteur = trajet.conducteur == destinataire

        if not (is_user_conducteur or is_user_passager or is_dest_conducteur):
            raise serializers.ValidationError(
                {"trajet": "Vous devez être lié à ce trajet pour évaluer."}
            )

        return attrs