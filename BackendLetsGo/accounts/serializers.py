import re
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, VerificationDocument

class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer de connexion JWT sur mesure :
    Permet à l'utilisateur de se connecter avec son email OU son numéro de téléphone,
    et accepte les clés 'email', 'username', 'telephone' ou 'identifiant'.
    """
    email = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True)
    identifiant = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifiant = (
            attrs.get('email') or 
            attrs.get('username') or 
            attrs.get('identifiant') or 
            attrs.get('telephone') or 
            ''
        ).strip()
        password = attrs.get('password')

        if not identifiant:
            raise serializers.ValidationError({"detail": "Veuillez renseigner votre adresse e-mail ou numéro de téléphone."})
        if not password:
            raise serializers.ValidationError({"detail": "Veuillez renseigner votre mot de passe."})

        user = None
        if '@' in identifiant:
            user = User.objects.filter(email__iexact=identifiant).first()
        else:
            # Formatage du numéro de téléphone sénégalais pour matcher en base
            digits = re.sub(r'\D', '', identifiant)
            if digits.startswith('221') and len(digits) > 3:
                digits_9 = digits[3:]
            elif digits.startswith('00221') and len(digits) > 5:
                digits_9 = digits[5:]
            else:
                digits_9 = digits[-9:] if len(digits) >= 9 else digits
            
            user = (
                User.objects.filter(telephone=f"+221{digits_9}").first() or
                User.objects.filter(telephone=digits_9).first() or
                User.objects.filter(telephone=identifiant).first()
            )

        # Vérification cryptographique stricte du mot de passe (respect strict de la casse et des caractères)
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError({
                    "detail": "Votre compte n'est pas encore vérifié. Veuillez saisir votre code de confirmation.",
                    "non_verifie": True,
                    "email": user.email
                })
            
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                }
            }

        raise serializers.ValidationError({"detail": "Identifiants incorrects. Veuillez vérifier votre adresse e-mail/téléphone et mot de passe."})

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'telephone', 'adresse', 'password', 'role')
        read_only_fields = ('role',)

    def create(self, validated_data):
        # Utilisation de create_user pour hacher automatiquement le mot de passe
        user = User.objects.create_user(
            username=validated_data['email'], # On utilise l'email comme username
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            telephone=validated_data['telephone'],
            adresse=validated_data.get('adresse', ''),
            password=validated_data['password'],
            role=User.Role.PASSAGER,
            is_active=False # Compte inactif en attente de vérification du code OTP
        )
        return user


# class UserProfileSerializer(serializers.ModelSerializer):
#         class Meta:
#              model = User
#              fields = ('id', 'first_name', 'last_name', 'email', 'telephone', 'role')
#              read_only_fields = ('id', 'role')  # L'utilisateur peut modifier nom, prénom, email et téléphone, mais PAS son rôle ni son id

class UserProfileSerializer(serializers.ModelSerializer):
    is_profile_complete = serializers.ReadOnlyField()  # Champ calculé (read-only)
    documents = serializers.SerializerMethodField()
    voitures = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 
            'telephone', 'adresse', 'role', 'is_verified', 
            'is_profile_complete', 'photo', 'fcm_token',
            'documents', 'voitures'
        )
        read_only_fields = ('id', 'role', 'is_profile_complete', 'documents', 'voitures')

    def get_documents(self, obj):
        latest_doc = obj.verification_documents.order_by('-created_at').first()
        if latest_doc:
            request = self.context.get('request')
            return {
                'id': latest_doc.id,
                'permis_conduire': request.build_absolute_uri(latest_doc.permis_conduire.url) if latest_doc.permis_conduire and request else (latest_doc.permis_conduire.url if latest_doc.permis_conduire else None),
                'carte_grise': request.build_absolute_uri(latest_doc.carte_grise.url) if latest_doc.carte_grise and request else (latest_doc.carte_grise.url if latest_doc.carte_grise else None),
                'assurance': request.build_absolute_uri(latest_doc.assurance.url) if latest_doc.assurance and request else (latest_doc.assurance.url if latest_doc.assurance else None),
                'photo_vehicule': request.build_absolute_uri(latest_doc.photo_vehicule.url) if latest_doc.photo_vehicule and request else (latest_doc.photo_vehicule.url if latest_doc.photo_vehicule else None),
                'status': latest_doc.status,
                'motif_rejet': latest_doc.motif_rejet or '',
                'created_at': latest_doc.created_at,
            }
        return None

    def get_voitures(self, obj):
        request = self.context.get('request')
        voitures = obj.voitures.all()
        result = []
        for v in voitures:
            photo_url = None
            if v.photo_voiture:
                photo_url = request.build_absolute_uri(v.photo_voiture.url) if request else v.photo_voiture.url
            result.append({
                'id': v.id,
                'marque_voiture': v.marque_voiture,
                'model_voiture': v.model_voiture,
                'plaque': v.plaque,
                'nombres_de_places': v.nombres_de_places,
                'couleur': v.couleur,
                'est_climatisee': v.est_climatisee,
                'photo_voiture': photo_url,
            })
        return result


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
        req = self.context.get('request')
        has_uploaded_photo = bool(req and ('photo_profil' in req.FILES or 'photo' in req.FILES))
        if not user.photo and not has_uploaded_photo:
            raise serializers.ValidationError({
                "photo": "Vous devez d'abord ajouter une photo de profil à votre compte."
            })
        return attrs