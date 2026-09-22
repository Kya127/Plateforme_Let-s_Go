from rest_framework import serializers
from trajets.models import Trajet
from .models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    nom_auteur = serializers.ReadOnlyField(source="auteur.first_name")
    nom_destinataire = serializers.ReadOnlyField(
        source="destinataire.first_name"
    )

    class Meta:
        model = Evaluation
        fields = (
            "id",
            "trajet",
            "destinataire",
            "nom_destinataire",
            "note",
            "commentaire",
            "nom_auteur",
            "created_at",
        )
        read_only_fields = ("id", "nom_auteur", "nom_destinataire", "created_at")

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None
        trajet = attrs.get("trajet")
        destinataire = attrs.get("destinataire")

        if not user or not user.is_authenticated:
            raise serializers.ValidationError(
                "Vous devez être connecté pour laisser un avis."
            )

        # 1. Interdiction de s'auto-évaluer
        if user == destinataire:
            raise serializers.ValidationError(
                {"destinataire": "Vous ne pouvez pas vous évaluer vous-même."}
            )

        # 2. Le trajet doit être terminé
        if trajet.statut != Trajet.StatutTrajet.TERMINE:
            raise serializers.ValidationError(
                {"trajet": "Vous ne pouvez évaluer qu'un trajet terminé."}
            )

        # 3. Vérification de la participation de l'auteur et du destinataire
        is_user_conducteur = trajet.conducteur == user
        is_user_passager = trajet.reservations.filter(
            passager=user, statut="CONFIRMEE"
        ).exists()

        if not (is_user_conducteur or is_user_passager):
            raise serializers.ValidationError(
                {"trajet": "Vous n'avez pas participé à ce trajet."}
            )

        is_dest_conducteur = trajet.conducteur == destinataire
        is_dest_passager = trajet.reservations.filter(
            passager=destinataire, statut="CONFIRMEE"
        ).exists()

        if not (is_dest_conducteur or is_dest_passager):
            raise serializers.ValidationError(
                {"destinataire": "Cet utilisateur n'a pas participé à ce trajet."}
            )

        return attrs