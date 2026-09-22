from rest_framework import permissions, viewsets
from .models import Evaluation
from .serializers import EvaluationSerializer


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

    def get_queryset(self):
        queryset = Evaluation.objects.all()
        # Permet de filtrer les avis reçus par un utilisateur spécifique ex: /api/evaluations/?destinataire=2
        destinataire_id = self.request.query_params.get("destinataire")
        if destinataire_id:
            queryset = queryset.filter(destinataire_id=destinataire_id)
        return queryset