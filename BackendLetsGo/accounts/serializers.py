from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'telephone', 'password', 'role')
        read_only_fields = ('role',)

        
    def create(self, validated_data):
        # Utilisation de create_user pour hacher automatiquement le mot de passe
        user = User.objects.create_user(
            username=validated_data['email'], # On utilise l'email comme username
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            telephone=validated_data['telephone'],
            password=validated_data['password'],
            role=User.Role.PASSAGER
        )
        return user