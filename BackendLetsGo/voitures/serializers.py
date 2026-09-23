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
        user = self.context['request'].user
        if not user.is_verified:
            raise serializers.ValidationError("Seuls les conducteurs vérifiés  peuvent ajouter un véhicule.")
        return attrs