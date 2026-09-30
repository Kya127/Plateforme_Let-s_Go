from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Voiture
from .serializers import VoitureSerializer

class VoitureViewSet(viewsets.ModelViewSet):
    serializer_class = VoitureSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        # Le conducteur connecté ne voit et ne gère que ses propres véhicules
        return Voiture.objects.filter(conducteur=self.request.user)

    def perform_create(self, serializer):
        # Assigne automatiquement le conducteur connecté lors de la création
        serializer.save(conducteur=self.request.user)