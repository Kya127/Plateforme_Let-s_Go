from rest_framework import serializers
from .models import Reservation
from trajets.models import Trajet

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'passager', 'trajet', 'nombre_de_places', 'statut', 'created_at')
        read_only_fields = ('id', 'passager', 'statut', 'created_at')

    def validate(self, attrs):
        user = self.context['request'].user
        trajet = attrs.get('trajet')
        places_demandees = attrs.get('nombre_de_places', 1)

        # 1. Empêcher le conducteur de réserver son propre trajet
        if trajet.conducteur == user:
            raise serializers.ValidationError(
                "Vous ne pouvez pas réserver une place sur votre propre trajet."
            )

        # 2. Vérifier que le trajet est bien au statut PROGRAMME
        if trajet.statut != Trajet.StatutTrajet.PROGRAMME:
            raise serializers.ValidationError(
                "Vous ne pouvez réserver que des trajets programmés."
            )

        # 3. Vérifier la disponibilité des places
        if places_demandees > trajet.nombre_de_place:
            raise serializers.ValidationError({
                "nombre_de_places": f"Places insuffisantes. Il ne reste que {trajet.nombre_de_place} place(s)."
            })

        return attrs