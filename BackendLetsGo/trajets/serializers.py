from rest_framework import serializers
from .models import Trajet
from voitures.models import Voiture

class TrajetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajet
        fields = (
            'id', 
            'conducteur', 
            'voiture', 
            'lieu_depart', 
            'destination', 
            'date_depart', 
            'places_disponibles', 
            'prix_par_place', 
            'description', 
            'statut', 
            'created_at'
        )
        read_only_fields = ('id', 'conducteur', 'statut', 'created_at')

    def validate(self, attrs):
        user = self.context['request'].user
        voiture = attrs.get('voiture')
        places = attrs.get('places_disponibles')

        # 1. Vérifier si l'utilisateur est un conducteur vérifié
        if not user.is_verified:
            raise serializers.ValidationError(
                "Vous devez être un conducteur vérifié pour publier un trajet."
            )

        # 2. Vérifier que la voiture appartient bien au conducteur
        if voiture.conducteur != user:
            raise serializers.ValidationError({
                "voiture": "Vous ne pouvez pas publier un trajet avec une voiture qui ne vous appartient pas."
            })

        # 3. Vérifier que le nombre de places ne dépasse pas la capacité du véhicule
        if places > voiture.nombres_de_places:
            raise serializers.ValidationError({
                "places_disponibles": f"Le nombre de places proposées dépasse la capacité de la voiture."
            })

        return attrs