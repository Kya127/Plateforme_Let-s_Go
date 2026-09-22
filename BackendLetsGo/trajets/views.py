from rest_framework import viewsets, permissions, status, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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
        # En liste publique, on affiche uniquement les trajets planifiés ayant au moins 1 place libre
        if self.action == 'list':
            queryset = queryset.filter(
                statut=Trajet.StatutTrajet.PLANIFIE,
                places_disponibles__gt=0
            )
        return queryset

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

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
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
        trajet.save()
        return Response({"message": "Trajet démarré avec succès.", "statut": trajet.statut})

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
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
        trajet.save()
        return Response({"message": "Trajet terminé avec succès.", "statut": trajet.statut})



    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
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