from rest_framework import viewsets, permissions
from .models import Trajet
from .serializers import TrajetSerializer

class TrajetViewSet(viewsets.ModelViewSet):
    serializer_class = TrajetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Permet à tout le monde de consulter les trajets programmés
        queryset = Trajet.objects.filter(statut=Trajet.StatutTrajet.PLANIFIE)
        
        # Filtres optionnels par lieu de départ/arrivée dans l'URL
        depart = self.request.query_params.get('depart')
        arrivee = self.request.query_params.get('arrivee')
        
        if depart:
            queryset = queryset.filter(lieu_depart__icontains=depart)
        if arrivee:
            queryset = queryset.filter(lieu_arrivee__icontains=arrivee)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(conducteur=self.request.user)