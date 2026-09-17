from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trajet
from .serializers import TrajetSerializer, TrajetDetailSerializer

class TrajetViewSet(viewsets.ModelViewSet):
    serializer_class = TrajetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
        # Si la requête demande le détail d'UN SEUL trajet (GET /api/trajets/trajets/{id}/)
        if self.action == 'retrieve':
            return TrajetDetailSerializer
        # Pour toutes les autres actions (list, create, update, etc.)
        return TrajetSerializer

    def get_queryset(self):
        queryset = Trajet.objects.all()
        # Seuls les trajets programmés sont visibles publiquement en lecture simple
        if self.action == 'list':
            queryset = queryset.filter(statut=Trajet.StatutTrajet.PLANIFIE)
        return queryset

    def perform_create(self, serializer):
        serializer.save(conducteur=self.request.user)

    def perform_update(self, serializer):
        trajet = self.get_object()
        if trajet.statut != Trajet.StatutTrajet.PLANIFIE:
            raise serializers.ValidationError(
                "Impossible de modifier un trajet qui est déjà en cours, terminé ou annulé."
            )
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