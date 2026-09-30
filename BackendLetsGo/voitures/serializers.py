from rest_framework import serializers
from .models import Voiture

class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = (
            'id', 
            'marque_voiture', 
            'model_voiture', 
            'plaque', 
            'nombres_de_places', 
            'couleur', 
            'est_climatisee', 
            'photo_voiture', 
            'date_creation'
        )
        read_only_fields = ('id', 'date_creation')

    def validate(self, attrs):
        # L'utilisateur connecté peut enregistrer son véhicule lors de son onboarding
        return attrs