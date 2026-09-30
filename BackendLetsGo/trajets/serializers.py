from rest_framework import serializers
from .models import Trajet
from voitures.models import Voiture

class TrajetSerializer(serializers.ModelSerializer):
    preferences = serializers.MultipleChoiceField(choices=Trajet.CLASS_PREFERENCES, required=False)
    conducteur_nom = serializers.CharField(source='conducteur.get_full_name', read_only=True)
    conducteur_photo = serializers.SerializerMethodField()
    conducteur_note = serializers.SerializerMethodField()
    voiture = serializers.PrimaryKeyRelatedField(queryset=Voiture.objects.all(), required=False)
    voiture_info = serializers.SerializerMethodField()
    voiture_details = serializers.SerializerMethodField()
    est_deja_reserve = serializers.SerializerMethodField()

    class Meta:
        model = Trajet
        fields = (
            'id', 
            'conducteur', 
            'conducteur_nom',
            'conducteur_photo',
            'conducteur_note',
            'voiture', 
            'voiture_info',
            'voiture_details',
            'lieu_depart', 
            'destination', 
            'date', 
            'heure_depart',
            'places_disponibles', 
            'prix_par_place', 
            'description', 
            'statut', 
            'preferences',
            'est_deja_reserve',
            'created_at'
        )
        read_only_fields = ('id', 'conducteur', 'statut', 'created_at')

    def get_conducteur_photo(self, obj):
        if obj.conducteur and obj.conducteur.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.conducteur.photo.url)
            return obj.conducteur.photo.url
        return None

    def get_conducteur_note(self, obj):
        evals = obj.conducteur.evaluations_recues.all()
        if evals.exists():
            return round(sum(e.note for e in evals) / evals.count(), 1)
        return 4.9

    def get_est_deja_reserve(self, obj):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.reservations.filter(passager=request.user, statut='CONFIRMEE').exists()

    def get_voiture_info(self, obj):
        if not obj.voiture:
            return None
        v = obj.voiture
        request = self.context.get('request')
        photo = None
        if v.photo_voiture:
            photo = request.build_absolute_uri(v.photo_voiture.url) if request else v.photo_voiture.url
        return {
            'id': v.id,
            'marque': v.marque_voiture,
            'modele': v.model_voiture,
            'brand': v.marque_voiture,
            'model': v.model_voiture,
            'couleur': v.couleur or 'Gris argenté',
            'color': v.couleur or 'Gris argenté',
            'plaque': v.plaque,
            'plate': v.plaque,
            'places': v.nombres_de_places,
            'climatisee': v.est_climatisee,
            'isAirConditioned': v.est_climatisee,
            'photo': photo,
            'texte': f"{v.marque_voiture} {v.model_voiture} {v.couleur or ''} ({v.plaque})".strip()
        }

    def get_voiture_details(self, obj):
        return self.get_voiture_info(obj)

    def validate(self, attrs):
        user = self.context['request'].user
        instance = getattr(self, 'instance', None)
        voiture = attrs.get('voiture') or (instance.voiture if instance else None)
        places = attrs.get('places_disponibles') or (instance.places_disponibles if instance else None)

        # 1. Vérifier si l'utilisateur est un conducteur vérifié
        if not user.is_verified:
            raise serializers.ValidationError(
                "Vous devez être un conducteur vérifié pour publier un trajet."
            )

        # 2. Si la voiture n'est pas spécifiée, rattacher automatiquement la voiture enregistrée du conducteur
        if not voiture:
            user_car = Voiture.objects.filter(conducteur=user).first()
            if user_car:
                attrs['voiture'] = user_car
                voiture = user_car
            else:
                raise serializers.ValidationError({
                    "voiture": "Vous devez d'abord enregistrer un véhicule avant de publier un trajet."
                })

        # 3. Vérifier que la voiture appartient bien au conducteur
        if voiture and voiture.conducteur != user:
            raise serializers.ValidationError({
                "voiture": "Vous ne pouvez pas publier un trajet avec une voiture qui ne vous appartient pas."
            })

        # 4. Vérifier que le nombre de places ne dépasse pas la capacité du véhicule
        if voiture and places and places > voiture.nombres_de_places:
            raise serializers.ValidationError({
                "places_disponibles": "Le nombre de places proposées dépasse la capacité de la voiture."
            })

        return attrs


class TrajetDetailSerializer(serializers.ModelSerializer):
    conducteur_nom = serializers.CharField(source='conducteur.get_full_name', read_only=True)
    conducteur_prenom = serializers.CharField(source='conducteur.first_name', read_only=True)
    conducteur_telephone = serializers.CharField(source='conducteur.telephone', read_only=True)
    conducteur_photo = serializers.SerializerMethodField()
    conducteur_note = serializers.SerializerMethodField()
    voiture_info = serializers.SerializerMethodField()
    voiture_details = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    passagers = serializers.SerializerMethodField()
    est_deja_reserve = serializers.SerializerMethodField()
    ma_reservation = serializers.SerializerMethodField()

    class Meta:
        model = Trajet
        fields = (
            'id', 
            'conducteur', 
            'conducteur_nom',
            'conducteur_prenom',
            'conducteur_telephone',
            'conducteur_photo',
            'conducteur_note',
            'voiture',
            'voiture_info', 
            'voiture_details', 
            'lieu_depart', 
            'destination', 
            'date', 
            'heure_depart', 
            'places_disponibles', 
            'prix_par_place', 
            'description', 
            'preferences',
            'statut',
            'reservations',
            'passagers',
            'est_deja_reserve',
            'ma_reservation',
            'created_at'
        )

    def get_voiture_info(self, obj):
        if not obj.voiture:
            return None
        v = obj.voiture
        request = self.context.get('request')
        photo = None
        if v.photo_voiture:
            photo = request.build_absolute_uri(v.photo_voiture.url) if request else v.photo_voiture.url
        return {
            'id': v.id,
            'marque': v.marque_voiture,
            'modele': v.model_voiture,
            'brand': v.marque_voiture,
            'model': v.model_voiture,
            'couleur': v.couleur or 'Gris argenté',
            'color': v.couleur or 'Gris argenté',
            'plaque': v.plaque,
            'plate': v.plaque,
            'places': v.nombres_de_places,
            'climatisee': v.est_climatisee,
            'isAirConditioned': v.est_climatisee,
            'photo': photo,
            'texte': f"{v.marque_voiture} {v.model_voiture} {v.couleur or ''} ({v.plaque})".strip()
        }

    def get_voiture_details(self, obj):
        return self.get_voiture_info(obj)

    def get_conducteur_photo(self, obj):
        if obj.conducteur and obj.conducteur.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.conducteur.photo.url)
            return obj.conducteur.photo.url
        return None

    def get_conducteur_note(self, obj):
        evals = obj.conducteur.evaluations_recues.all()
        if evals.exists():
            return round(sum(e.note for e in evals) / evals.count(), 1)
        return 4.9

    def get_reservations(self, obj):
        res = obj.reservations.filter(statut='CONFIRMEE')
        request = self.context.get('request')
        result = []
        for r in res:
            photo = None
            if r.passager.photo:
                photo = request.build_absolute_uri(r.passager.photo.url) if request else r.passager.photo.url
            result.append({
                'id': r.id,
                'passengerId': r.passager.id,
                'firstName': r.passager.first_name or 'Passager',
                'lastName': r.passager.last_name or '',
                'fullName': r.passager.get_full_name() or r.passager.email,
                'telephone': r.passager.telephone,
                'profilePhoto': photo,
                'seatsReserved': r.nombre_de_places,
                'message': '',
                'createdAt': r.created_at.isoformat() if r.created_at else None
            })
        return result

    def get_passagers(self, obj):
        return self.get_reservations(obj)

    def get_est_deja_reserve(self, obj):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.reservations.filter(passager=request.user, statut='CONFIRMEE').exists()

    def get_ma_reservation(self, obj):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return None
        res = obj.reservations.filter(passager=request.user, statut='CONFIRMEE').first()
        if not res:
            return None
        return {
            'id': res.id,
            'nombre_de_places': res.nombre_de_places,
            'statut': res.statut,
            'created_at': res.created_at.isoformat() if res.created_at else None
        }


    