from rest_framework import viewsets, permissions, status, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from datetime import date
from django.utils import timezone
from .models import Trajet
from .serializers import TrajetSerializer, TrajetDetailSerializer
from .filters import TrajetFilter


class TrajetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Backends de filtrage, recherche textuelle et tri
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 1. Filtre structuré (Formulaire)
    filterset_class = TrajetFilter

    # 2. Barre de recherche globale ("Où allez-vous ?")
    search_fields = ['lieu_depart', 'destination', 'description']

    # 3. Champs de tri
    ordering_fields = ['prix_par_place', 'date', 'heure_depart']
    ordering = ['date', 'heure_depart']  # Tri par défaut

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TrajetDetailSerializer
        return TrajetSerializer

    def get_queryset(self):
        queryset = Trajet.objects.all()
        # En liste filtrée pour le conducteur connecté
        if self.action == 'list':
            if self.request.query_params.get('conducteur') == 'me' or self.request.query_params.get('mes_trajets') == 'true':
                if self.request.user.is_authenticated:
                    return Trajet.objects.filter(conducteur=self.request.user).order_by('-date', '-heure_depart')
                return Trajet.objects.none()

            # En liste publique, on affiche uniquement les trajets planifiés à venir ayant au moins 1 place libre
            today = max(timezone.localdate(), date.today())
            queryset = queryset.filter(
                statut=Trajet.StatutTrajet.PLANIFIE,
                places_disponibles__gt=0,
                date__gte=today
            )
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mes_trajets(self, request):
        trajets = Trajet.objects.filter(conducteur=request.user).order_by('-date', '-heure_depart')
        serializer = TrajetDetailSerializer(trajets, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(conducteur=self.request.user)

    def perform_update(self, serializer):
        trajet = self.get_object()
        if trajet.statut != Trajet.StatutTrajet.PLANIFIE:
            raise serializers.ValidationError("Impossible de modifier un trajet qui est déjà en cours, terminé ou annulé.")

        # Bloquer aussi la modification si des passagers ont déjà réservé
        if trajet.reservations.filter(statut='CONFIRMEE').exists():
            raise serializers.ValidationError("Impossible de modifier un trajet ayant déjà des réservations confirmées.")
        
        serializer.save()

    @action(detail=True, methods=['patch', 'post'], permission_classes=[permissions.IsAuthenticated])
    def demarrer(self, request, pk=None):
        trajet = self.get_object()

        if trajet.conducteur != request.user:
            return Response({"detail": "Non autorisé."}, status=status.HTTP_403_FORBIDDEN)

        if trajet.statut != Trajet.StatutTrajet.PLANIFIE:
            return Response(
                {"error": f"Impossible de démarrer un trajet avec le statut '{trajet.get_statut_display()}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        trajet.statut = Trajet.StatutTrajet.EN_COURS
        trajet.tracking_actif = True
        trajet.derniere_position_at = timezone.now()
        trajet.save()
        return Response({"message": "Trajet démarré avec succès.", "statut": trajet.statut, "tracking_actif": True})

    @action(detail=True, methods=['patch', 'post'], permission_classes=[permissions.IsAuthenticated])
    def terminer(self, request, pk=None):
        trajet = self.get_object()

        if trajet.conducteur != request.user:
            return Response({"detail": "Non autorisé."}, status=status.HTTP_403_FORBIDDEN)

        if trajet.statut != Trajet.StatutTrajet.EN_COURS:
            return Response(
                {"error": "Seul un trajet en cours peut être terminé."},
                status=status.HTTP_400_BAD_REQUEST
            )

        trajet.statut = Trajet.StatutTrajet.TERMINE
        trajet.tracking_actif = False
        trajet.save()
        return Response({"message": "Trajet terminé avec succès.", "statut": trajet.statut, "tracking_actif": False})

    @action(detail=True, methods=['post'], url_path='mettre-a-jour-position', permission_classes=[permissions.IsAuthenticated])
    def mettre_a_jour_position(self, request, pk=None):
        trajet = self.get_object()

        if trajet.conducteur != request.user:
            return Response({"detail": "Non autorisé."}, status=status.HTTP_403_FORBIDDEN)

        if trajet.statut != Trajet.StatutTrajet.EN_COURS:
            return Response(
                {"error": "Le tracking n'est disponible que pour un trajet en cours."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(request.data.get('latitude'))
            lng = float(request.data.get('longitude'))
        except (TypeError, ValueError):
            return Response(
                {"error": "Latitude et longitude valides requises."},
                status=status.HTTP_400_BAD_REQUEST
            )

        trajet.latitude_actuelle = lat
        trajet.longitude_actuelle = lng
        if request.data.get('cap') is not None:
            try:
                trajet.cap_actuel = float(request.data.get('cap'))
            except (TypeError, ValueError):
                pass
        if request.data.get('vitesse') is not None:
            try:
                trajet.vitesse_actuelle = float(request.data.get('vitesse'))
            except (TypeError, ValueError):
                pass

        trajet.tracking_actif = True
        trajet.derniere_position_at = timezone.now()
        trajet.save()

        from .services_tracking import calculer_eta_trajet
        telemetrie = calculer_eta_trajet(trajet)
        return Response(telemetrie, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='suivi-en-direct', permission_classes=[permissions.AllowAny])
    def suivi_en_direct(self, request, pk=None):
        trajet = self.get_object()
        from .services_tracking import calculer_eta_trajet
        telemetrie = calculer_eta_trajet(trajet)
        return Response(telemetrie, status=status.HTTP_200_OK)



    @action(detail=True, methods=['patch', 'post'], permission_classes=[permissions.IsAuthenticated])
    def annuler(self, request, pk=None):
        trajet = self.get_object()

        # 1. Vérifier que c'est bien le conducteur du trajet
        if trajet.conducteur != request.user:
            return Response({"detail": "Non autorisé."}, status=status.HTTP_403_FORBIDDEN)

        # 2. Règle Métier : Bloquer l'annulation s'il existe au moins une réservation confirmée
        if trajet.reservations.filter(statut='CONFIRMEE').exists():
            return Response(
                {"error": "Impossible d'annuler ce trajet car des passagers ont déjà réservé leur place."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if trajet.statut == Trajet.StatutTrajet.ANNULE:
            return Response({"error": "Ce trajet est déjà annulé."}, status=status.HTTP_400_BAD_REQUEST)

        trajet.statut = Trajet.StatutTrajet.ANNULE
        trajet.save()
        return Response({"message": "Le trajet a été annulé avec succès.", "statut": trajet.statut})

    @action(detail=False, methods=['get'], url_path='referentiel-zones', permission_classes=[permissions.AllowAny])
    def referentiel_zones(self, request):
        """
        Retourne le référentiel complet des zones, quartiers, repères et la matrice tarifaire.
        """
        from .services_tarification import obtenir_referentiel_complet
        data = obtenir_referentiel_complet()
        return Response(data)

    @action(detail=False, methods=['get'], url_path='calculer-prix', permission_classes=[permissions.AllowAny])
    def calculer_prix(self, request):
        """
        Calcule le prix officiel garanti par la plateforme entre deux adresses ou repères.
        """
        from .services_tarification import resoudre_prix_trajet, trouver_zone_pour_lieu, REFERENTIEL_ZONES
        depart = request.query_params.get('depart', '').strip()
        destination = request.query_params.get('destination', '').strip()

        if not depart or not destination:
            return Response(
                {"error": "Veuillez fournir à la fois 'depart' et 'destination'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        code_dep = trouver_zone_pour_lieu(depart)
        code_dest = trouver_zone_pour_lieu(destination)
        prix = resoudre_prix_trajet(depart, destination)

        zones_dict = {z["code"]: z["nom"] for z in REFERENTIEL_ZONES}
        nom_zone_dep = zones_dict.get(code_dep, code_dep)
        nom_zone_dest = zones_dict.get(code_dest, code_dest)

        return Response({
            "depart": depart,
            "destination": destination,
            "zone_depart": code_dep,
            "zone_depart_nom": nom_zone_dep,
            "zone_destination": code_dest,
            "zone_destination_nom": nom_zone_dest,
            "prix_par_place": int(prix) if prix is not None else None,
            "prix_formate": f"{int(prix):,} FCFA".replace(",", " ") if prix is not None else "",
            "badge_texte": f"Tarif fixé par la plateforme : {int(prix):,} FCFA / place ({code_dep} ➔ {code_dest})".replace(",", " ") if prix is not None else ""
        })