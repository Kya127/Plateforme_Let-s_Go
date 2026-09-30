from rest_framework import serializers
from .models import Reservation
from trajets.models import Trajet
from trajets.serializers import TrajetDetailSerializer

class ReservationSerializer(serializers.ModelSerializer):
    trajet_details = TrajetDetailSerializer(source='trajet', read_only=True)
    passager_nom = serializers.CharField(source='passager.get_full_name', read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'passager', 'passager_nom', 'trajet', 'trajet_details', 'nombre_de_places', 'statut', 'created_at')
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

        # 2. Vérifier que le trajet est bien au statut PLANIFIE
        if trajet.statut != Trajet.StatutTrajet.PLANIFIE:
            raise serializers.ValidationError(
                "Vous ne pouvez réserver que des trajets planifiés."
            )

        # 3. Vérifier la disponibilité des places (anti-surbooking capacité)
        if places_demandees > trajet.places_disponibles:
            raise serializers.ValidationError({
                "nombre_de_places": f"Places insuffisantes. Il ne reste que {trajet.places_disponibles} place(s)."
            })

        # 4. Empêcher la double réservation par le même passager sur le même trajet
        reservation_existante = Reservation.objects.filter(
            passager=user,
            trajet=trajet,
            statut=Reservation.StatutReservation.CONFIRMEE
        ).exists()
        if reservation_existante:
            raise serializers.ValidationError({
                "trajet": "Vous avez déjà une réservation active sur ce trajet. Il est impossible de réserver deux fois sur le même trajet."
            })

        return attrs