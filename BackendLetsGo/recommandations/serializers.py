from rest_framework import serializers
from .models import HistoriqueRecherche
from trajets.serializers import TrajetSerializer


class HistoriqueRechercheSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueRecherche
        fields = ('id', 'user', 'lieu_depart', 'destination', 'date_voulue', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user if self.context.get('request') and self.context['request'].user.is_authenticated else None
        validated_data['user'] = user
        return super().create(validated_data)


class EnregistrerRechercheInputSerializer(serializers.Serializer):
    lieu_depart = serializers.CharField(max_length=255, required=True)
    destination = serializers.CharField(max_length=255, required=True)
    date_voulue = serializers.DateField(required=False, allow_null=True)


class SuggestionTrajetItemSerializer(TrajetSerializer):
    """
    Étend TrajetSerializer pour ajouter le tag contextuel ("Basé sur vos habitudes" ou "Trajets populaires du moment")
    """
    tag = serializers.SerializerMethodField()
    type_suggestion = serializers.SerializerMethodField()

    class Meta(TrajetSerializer.Meta):
        fields = TrajetSerializer.Meta.fields + ('tag', 'type_suggestion')

    def get_tag(self, obj):
        return self.context.get('tag', 'Basé sur vos habitudes')

    def get_type_suggestion(self, obj):
        return self.context.get('type_suggestion', 'HABITUDES')
