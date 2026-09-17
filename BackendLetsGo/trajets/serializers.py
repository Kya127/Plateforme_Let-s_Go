from rest_framework import serializers
from .models import Trajet
from voitures.models import Voiture

class TrajetSerializer(serializers.ModelSerializer):

    preferences = serializers.MultipleChoiceField(choices=Trajet.CLASS_PREFERENCES, required=False)
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
            'preferences',
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




class TrajetDetailSerializer(serializers.ModelSerializer):
    conducteur_nom = serializers.CharField(source='conducteur.get_full_name', read_only=True)
    voiture_info = serializers.SerializerMethodField()

    class Meta:
        model = Trajet
        fields = (
            'id', 
            'conducteur', 
            'conducteur_nom',
            'voiture_info', 
            'lieu_depart', 
            'lieu_arrivee', 
            'date_depart', 
            'heure_depart', 
            'nombre_de_place', 
            'prix_par_place', 
            'description', 
            'preferences',
            'statut'
        )

    def get_voiture_info(self, obj):
        return f"{obj.voiture.marque_voiture} {obj.voiture.model_voiture} {obj.voiture.couleur} ({obj.voiture.plaque})"
    