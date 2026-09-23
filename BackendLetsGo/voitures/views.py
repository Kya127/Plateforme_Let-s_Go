from rest_framework import viewsets, permissions
from .models import Voiture
from .serializers import VoitureSerializer

class VoitureViewSet(viewsets.ModelViewSet):
    serializer_class = VoitureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Le conducteur connecté ne voit et ne gère que ses propres véhicules
        return Voiture.objects.filter(conducteur=self.request.user)

    def perform_create(self, serializer):
        # Assigne automatiquement le conducteur connecté lors de la création
        serializer.save(conducteur=self.request.user)