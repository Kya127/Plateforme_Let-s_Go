from rest_framework import serializers
from .models import User, VerificationDocument

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


# class UserProfileSerializer(serializers.ModelSerializer):
#         class Meta:
#              model = User
#              fields = ('id', 'first_name', 'last_name', 'email', 'telephone', 'role')
#              read_only_fields = ('id', 'role')  # L'utilisateur peut modifier nom, prénom, email et téléphone, mais PAS son rôle ni son id

class UserProfileSerializer(serializers.ModelSerializer):
    is_profile_complete = serializers.ReadOnlyField()  # Champ calculé (read-only)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 
            'telephone', 'role', 'is_verified', 
            'is_profile_complete', 'photo', 'fcm_token'
        )
        read_only_fields = ('id', 'role', 'is_profile_complete')             


class BecomeDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = ('permis_conduire', 'carte_grise', 'assurance', 'photo_vehicule')
        extra_kwargs = {
            'permis_conduire': {
                'required': True,
                'error_messages': {'required': 'Le permis de conduire est obligatoire.'}
            },
            'carte_grise': {
                'required': True,
                'error_messages': {'required': 'La carte grise du véhicule est obligatoire.'}
            },
            'assurance': {
                'required': True,
                'error_messages': {'required': 'L\'attestation d\'assurance est obligatoire.'}
            },
            'photo_vehicule': {
                'required': True,
                'error_messages': {'required': 'La photo du véhicule est obligatoire.'}
            },
        }

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.photo:
            raise serializers.ValidationError({
                "photo": "Vous devez d'abord ajouter une photo de profil à votre compte."
            })
        return attrs