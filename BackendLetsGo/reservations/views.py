from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Un utilisateur ne voit que ses propres réservations
        return Reservation.objects.filter(passager=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        trajet = serializer.validated_data['trajet']
        places = serializer.validated_data['nombre_de_places']

        # 1. Décrémenter les places sur le trajet
        trajet.reserver_places(places)

        # 2. Enregistrer la réservation
        serializer.save(passager=self.request.user)

    @action(detail=True, methods=['patch'])
    @transaction.atomic
    def annuler(self, request, pk=None):
        reservation = self.get_object()

        if reservation.statut == Reservation.StatutReservation.ANNULEE:
            return Response(
                {"error": "Cette réservation est déjà annulée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Remettre à jour le statut
        reservation.statut = Reservation.StatutReservation.ANNULEE
        reservation.save()

        # 2. Libérer les places sur le trajet
        reservation.trajet.liberer_places(reservation.nombre_de_places)

        return Response({"message": "Réservation annulée et places libérées avec succès."})